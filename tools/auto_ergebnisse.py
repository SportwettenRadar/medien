#!/usr/bin/env python3
"""Automatik Sportwetten Radar: liest daten/ergebnisse.json (vom Bot), prüft die Zahlen,
aktualisiert den Homepage-Trackrecord (trackrecord-daten.js), erzeugt Monatsbericht-Seiten
und baut die Grafiken für X.

Aufruf:  python3 auto_ergebnisse.py --medien /home/claude/medien --homepage /home/claude/sportwetten-radar.net [--modus woche|monat] [--trocken]
Ausgabe: JSON-Zusammenfassung auf stdout (status ok|stopp, fehler[], aenderungen[], grafiken[]).
Bei status "stopp" wird NICHTS geschrieben.
Commit/Push und das Einplanen in Metricool übernimmt die Claude-Sitzung.
"""
import argparse, datetime as dt, json, os, re, subprocess, sys

TOL = 0.15  # Toleranz Gewinn vs. Rendite x Wetten / 100 (Rundung)
MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August",
          "September", "Oktober", "November", "Dezember"]


def d(s):
    return dt.date.fromisoformat(s)


def de(n, k=1):
    return f"{abs(n):,.{k}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def signed(n, k=1):
    return ("+" if n > 0 else "−" if n < 0 else "") + de(n, k)


def mehrheitsmonat(von):
    tage = [von + dt.timedelta(days=i) for i in range(7)]
    zaehl = {}
    for t in tage:
        zaehl[t.strftime("%Y-%m")] = zaehl.get(t.strftime("%Y-%m"), 0) + 1
    return max(zaehl, key=zaehl.get)


# ---------------------------------------------------------------- Prüfung
def pruefe_block(name, b, fehler, voll=False):
    L, E = b.get("live", {}), b.get("einzelspiele", {})
    for k in ("wetten", "treffer", "rendite"):
        if not isinstance(L.get(k), (int, float)):
            fehler.append(f"{name}: live.{k} fehlt")
            return
    for k in ("tipps", "treffer"):
        if not isinstance(E.get(k), int):
            fehler.append(f"{name}: einzelspiele.{k} fehlt")
    if not (0 <= L["treffer"] <= L["wetten"]):
        fehler.append(f"{name}: Treffer {L['treffer']} > Wetten {L['wetten']}")
    if E.get("tipps") is not None and not (0 <= E.get("treffer", 0) <= E["tipps"]):
        fehler.append(f"{name}: Einzelspiele Treffer > Tipps")
    if abs(L["rendite"]) > 100:
        fehler.append(f"{name}: Rendite {L['rendite']} unplausibel")
    if L["wetten"] == 0 and L["rendite"] != 0:
        fehler.append(f"{name}: Rendite ohne Wetten")
    if isinstance(L.get("gewinn"), (int, float)):
        soll = L["rendite"] * L["wetten"] / 100
        if abs(soll - L["gewinn"]) > TOL + 0.0005 * L["wetten"]:
            fehler.append(f"{name}: Gewinn {L['gewinn']} passt nicht zu Rendite×Wetten ({soll:.2f})")
    if voll:
        for k in ("verlustserie", "rueckgang", "besterTag", "schlechtesterTag"):
            if not isinstance(L.get(k), (int, float)):
                fehler.append(f"{name}: live.{k} fehlt")


def pruefe(data):
    fehler = []
    if data.get("version") != 1:
        fehler.append("version != 1")
    tage = {t["datum"]: t for t in data.get("tage", [])}
    for t in tage.values():
        pruefe_block("Tag " + t["datum"], t, fehler)
    prev = None
    for t in sorted(data.get("tage", []), key=lambda x: x["datum"]):
        z = seit_start(t)
        if z is None:
            continue
        n = "Tag " + t["datum"] + " seitStart"
        if not all(isinstance(z.get(k), (int, float)) for k in ("wetten", "treffer", "rendite", "gewinn")):
            fehler.append(n + ": Felder fehlen")
            prev = None
            continue
        if z["wetten"] and abs(z["gewinn"] / z["wetten"] * 100 - z["rendite"]) > 0.15:
            fehler.append(n + f": Rendite {z['rendite']} passt nicht zu Gewinn/Wetten")
        if prev is not None and isinstance(t.get("live", {}).get("gewinn"), (int, float)):
            if abs((z["gewinn"] - prev["gewinn"]) - t["live"]["gewinn"]) > TOL:
                fehler.append(n + f": Änderung seit Start {z['gewinn'] - prev['gewinn']:.1f} ≠ Tagesgewinn {t['live']['gewinn']}")
            if z["wetten"] - prev["wetten"] != t["live"]["wetten"]:
                fehler.append(n + ": Wetten seit Start passen nicht zur Summe der Tage")
        prev = z
    for w in data.get("wochen", []):
        n = f"Woche {w.get('von')}–{w.get('bis')}"
        try:
            von, bis = d(w["von"]), d(w["bis"])
        except Exception:
            fehler.append(n + ": Datum fehlt")
            continue
        if von.weekday() != 0 or (bis - von).days != 6:
            fehler.append(n + ": keine volle Woche Mo–So")
        if w.get("monat") != mehrheitsmonat(von):
            fehler.append(n + f": monat {w.get('monat')} statt {mehrheitsmonat(von)} (Mehrheitsregel)")
        pruefe_block(n, w, fehler, voll=False)
        # Summe der Tage = Woche (wenn alle 7 Tage vorliegen)
        tl = [tage.get((von + dt.timedelta(days=i)).isoformat()) for i in range(7)]
        if all(tl):
            for k in ("wetten", "treffer"):
                s = sum(t["live"][k] for t in tl)
                if s != w["live"][k]:
                    fehler.append(n + f": Summe Tage live.{k}={s} ≠ Woche {w['live'][k]}")
            for k in ("tipps", "treffer"):
                s = sum(t["einzelspiele"][k] for t in tl)
                if s != w["einzelspiele"][k]:
                    fehler.append(n + f": Summe Tage einzelspiele.{k}={s} ≠ Woche {w['einzelspiele'][k]}")
    for m in data.get("monate", []):
        n = "Monat " + m.get("monat", "?")
        pruefe_block(n, m, fehler, voll=True)
        y, mo = map(int, m["monat"].split("-"))
        erster = dt.date(y, mo, 1)
        letzter = (dt.date(y + (mo == 12), mo % 12 + 1, 1) - dt.timedelta(days=1))
        tl = [tage.get((erster + dt.timedelta(days=i)).isoformat()) for i in range((letzter - erster).days + 1)]
        if all(tl):
            s = sum(t["live"]["wetten"] for t in tl)
            if s != m["live"]["wetten"]:
                fehler.append(n + f": Summe Tage live.wetten={s} ≠ Monat {m['live']['wetten']}")
    return fehler


# ---------------------------------------------------------------- Homepage-Daten
def lade_homepage(hp):
    out = subprocess.run(["node", "-e",
        "global.window={};require(process.argv[1]);console.log(JSON.stringify({m:window.TRACKRECORD,w:window.TRACKRECORD_WOCHEN||[],h:window.TRACKRECORD_WOCHEN_HINWEIS||'',t:window.TRACKRECORD_TAGE||[],s:window.TRACKRECORD_START||null}))",
        os.path.abspath(os.path.join(hp, "trackrecord-daten.js"))], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def js_block(o, ind="  "):
    """Objekt im Stil von trackrecord-daten.js (Schlüssel ohne Anführungszeichen)."""
    s = json.dumps(o, ensure_ascii=False, indent=2)
    s = re.sub(r'"([a-zA-Z_]+)":', r"\1:", s)
    return "\n".join(ind + z for z in s.splitlines())


# Die eine Fußnote (Daniel, 02.11.2026). Sie erscheint nur, wo Tage vor dem 11.10.2026 enthalten sind
# (Erkennung ausschließlich über das Feld "rueckrechnung" in ergebnisse.json, das Feld selbst wird nie angezeigt).
def fussnote(data, von=None, bis=None):
    """Die eine Fußnote, mit Zeitraum aus den Tagen mit rueckrechnung=true (nur Logik, das Feld wird nie angezeigt)."""
    tl = [t["datum"] for t in data.get("tage", []) if t.get("rueckrechnung") and (von is None or von <= t["datum"] <= bis)]
    if not tl:
        return None
    a, b = min(tl), max(tl)
    f = lambda x: f"{x[8:10]}.{x[5:7]}."
    return f"* {f(a)}–{f(b)}: Testphase, mit den heutigen Regeln berechnet."
PFLICHT = "Alle Zahlen gelten bei gleichem Einsatz auf jede Live-Wette. Verlustserien gehören dazu."


def seit_start(t):
    """Block "seit Start" eines Tages (Feldname im erweiterten JSON: seitStart)."""
    return t.get("seitStart") or t.get("seit_start") or t.get("seitstart")


def homepage_eintrag(b, mit_monat=True):
    L, E = b["live"], b["einzelspiele"]
    live = {"wetten": L["wetten"], "treffer": L["treffer"], "rendite": L["rendite"]}
    for k in ("gewinn", "verlustserie", "rueckgang", "besterTag", "schlechtesterTag"):
        if k in L:
            live[k] = L[k]
    e = {}
    if "monat" in b:
        e["monat"] = b["monat"]
    if "von" in b:
        e["von"], e["bis"] = b["von"], b["bis"]
    if b.get("rueckrechnung"):
        e["rueckrechnung"] = True
    e["live"] = live
    e["einzelspiele"] = {"tipps": E["tipps"], "treffer": E["treffer"]}
    return e


def gleich(a, b):
    """Vergleicht Homepage-Eintrag mit Bot-Eintrag auf den Kernzahlen."""
    for k in ("wetten", "treffer"):
        if a["live"].get(k) != b["live"].get(k):
            return False
    if abs(a["live"].get("rendite", 0) - b["live"].get("rendite", 0)) > 0.05:
        return False
    return a["einzelspiele"] == {"tipps": b["einzelspiele"]["tipps"], "treffer": b["einzelspiele"]["treffer"]}


def ergaenze(alt, neu):
    """Fehlende Felder (z. B. gewinn) aus den Bot-Daten ergänzen, nie vorhandene überschreiben."""
    geaendert = False
    for k in ("gewinn", "verlustserie", "rueckgang", "besterTag", "schlechtesterTag"):
        if k in neu["live"] and k not in alt["live"]:
            alt["live"][k] = neu["live"][k]
            geaendert = True
    return geaendert


def baue_tage(data):
    """Kurve (kumulierte Einsätze je Tag seit Start) und Stand "seit Start" aus ergebnisse.json.
    Gibt (None, None) zurück, solange das erweiterte JSON (Tage ab 01.09. mit seitStart) fehlt."""
    tl = sorted(data.get("tage", []), key=lambda x: x["datum"])
    if not tl or not all(isinstance(seit_start(t), dict) and isinstance(seit_start(t).get("gewinn"), (int, float)) for t in tl):
        return None, None
    kurve = [{"d": t["datum"], "g": round(seit_start(t)["gewinn"], 1), "rr": bool(t.get("rueckrechnung"))} for t in tl]
    z = seit_start(tl[-1])
    start = {"stand": tl[-1]["datum"], "wetten": z["wetten"], "treffer": z["treffer"],
             "gewinn": round(z["gewinn"], 1), "rendite": z["rendite"], "rueckrechnung": any(t.get("rueckrechnung") for t in tl)}
    return kurve, start


def schreibe_homepage(hp, monate, wochen, hinweis, tage=None, start=None):
    p = os.path.join(hp, "trackrecord-daten.js")
    js = open(p, encoding="utf-8").read()
    m = re.search(r"^window\.TRACKRECORD = \[", js, flags=re.M)
    kopf = js[:m.start()]
    mon = ",\n\n".join(js_block(x) for x in sorted(monate, key=lambda x: x["monat"], reverse=True))
    wo = ",\n".join(js_block(x) for x in sorted(wochen, key=lambda x: x["von"]))
    rest = js[m.start():]
    wk = rest.find("/* Wochen.")
    wochen_kommentar = rest[wk:rest.find("window.TRACKRECORD_WOCHEN")] if wk >= 0 else ""
    neu = (kopf + "window.TRACKRECORD = [\n\n" + mon + "\n\n];\n\n" + wochen_kommentar +
           "window.TRACKRECORD_WOCHEN = [\n" + wo + "\n];\n\n"
           "/* Hinweis, wenn für einen Monat keine Wochenwerte angezeigt werden können. */\n"
           "window.TRACKRECORD_WOCHEN_HINWEIS = " + json.dumps(hinweis, ensure_ascii=False) + ";\n\n"
           "/* Kurve: kumulierte Einsätze je Tag seit Start (d = Datum, g = Stand am Tagesende, rr = nur Logik für Fußnote/Hinterlegung).\n"
           "   Wird von tools/auto_ergebnisse.py aus ergebnisse.json geschrieben, nicht von Hand ändern. */\n"
           "window.TRACKRECORD_TAGE = [\n" + ",\n".join("  " + json.dumps(x, ensure_ascii=False) for x in (tage or [])) + "\n];\n\n"
           "/* Stand seit Start (Kennzahlen über der Kurve). */\n"
           "window.TRACKRECORD_START = " + json.dumps(start, ensure_ascii=False) + ";\n")
    open(p, "w", encoding="utf-8").write(neu)


# ---------------------------------------------------------------- Grafik für X
def zeilen(L, klein=False):
    """Kennzahlen jeweils in eigener Zeile. Reihenfolge (Daniel, 02.11.2026): Wetten, Treffer, Einsätze, Rendite."""
    q = L["treffer"] / L["wetten"] * 100 if L["wetten"] else 0
    G = L.get("gewinn", round(L["rendite"] * L["wetten"]) / 100)
    c = "z s" if klein else "z"
    return (f'<div class="{c}"><b>{L["wetten"]}</b> Wetten</div>'
            f'<div class="{c}"><b>{L["treffer"]}</b> Treffer ({de(q)} %)</div>'
            f'<div class="{c} lead"><b>{signed(G)}</b> Einsätze</div>'
            f'<div class="{c}">Rendite <b>{signed(L["rendite"])} %</b></div>')


def grafik(b, titel, kicker, ziel, hp, start=None, fuss_text=None):
    L, E = b["live"], b["einzelspiele"]
    eq = E["treffer"] / E["tipps"] * 100 if E["tipps"] else 0
    f = "file://" + os.path.join(os.path.abspath(hp), "assets/fonts/")
    logo = "file://" + os.path.join(os.path.abspath(hp), "assets/logo-icon.png")
    fuss = f'<div class="rr">{fuss_text}</div>' if fuss_text else ""
    stern_live = "*" if (fuss_text and b.get("rueckrechnung")) else ""
    stern_seit = "*" if (fuss_text and start is not None) else ""
    seit = ""
    if start:
        seit = (f'<div class="card"><div class="ct">Seit Start</div>{zeilen(start, klein=True)}</div>')
    einzel = (f'<div class="card"><div class="ct">Einzelspiele zum Kombinieren</div>'
              f'<div class="z s"><b>{E["treffer"]}</b> von {E["tipps"]} Tipps getroffen ({de(eq)} %)</div></div>') if E["tipps"] else ""
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:B;font-weight:800;src:url({f}baloo-2-latin-800-normal.woff2)}}
@font-face{{font-family:B;font-weight:700;src:url({f}baloo-2-latin-700-normal.woff2)}}
@font-face{{font-family:I;font-weight:500;src:url({f}inter-latin-500-normal.woff2)}}
@font-face{{font-family:I;font-weight:700;src:url({f}inter-latin-700-normal.woff2)}}
@font-face{{font-family:M;font-weight:500;src:url({f}ibm-plex-mono-latin-500-normal.woff2)}}
*{{margin:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;background:#0a1620;color:#eef4f8;font-family:I;padding:70px 84px;position:relative;
background-image:linear-gradient(#0f2232 1px,transparent 1px),linear-gradient(90deg,#0f2232 1px,transparent 1px);background-size:120px 120px}}
.top{{display:flex;align-items:center;gap:18px;font-family:B;font-weight:700;font-size:38px}}
.top img{{width:64px;height:64px}} .top span{{color:#2ee6a6}}
.k{{font-family:M;font-size:24px;letter-spacing:.14em;color:#2ee6a6;text-transform:uppercase;margin-top:50px}}
h1{{font-family:B;font-weight:800;font-size:88px;line-height:1.02;margin-top:10px}}
.card{{background:#0f1f30;border:1px solid #1e3448;border-radius:22px;padding:26px 44px;margin-top:24px}}
.ct{{font-family:M;font-size:22px;letter-spacing:.12em;color:#86a0b4;text-transform:uppercase;margin-bottom:12px}}
.z{{font-size:38px;line-height:1.3;color:#86a0b4;font-variant-numeric:tabular-nums}} .z b{{color:#eef4f8;font-weight:700}}
.z.lead{{font-family:B;font-weight:800;font-size:76px;line-height:1.1;color:#eef4f8}} .z.lead b{{color:#eef4f8;font-weight:800}}
.z.s{{font-size:31px}} .z.s.lead{{font-size:52px}}
.rr{{font-size:21px;color:#86a0b4;margin-top:18px}}
.pf{{font-size:21px;color:#4d6478;margin-top:20px;line-height:1.35}}
.foot{{position:absolute;left:84px;right:84px;bottom:56px;display:flex;justify-content:space-between;font-family:M;font-size:22px;color:#4d6478}}
</style></head><body>
<div class="top"><img src="{logo}"><div>Sportwetten <span>Radar</span></div></div>
<div class="k">{kicker}</div><h1>{titel}</h1>
<div class="card"><div class="ct">Live-Wetten</div>{zeilen(L).replace('</b> Einsätze', '</b> Einsätze' + stern_live, 1)}</div>
{seit.replace('Einsätze</div>', 'Einsätze' + stern_seit + '</div>', 1) if seit else ''}
{einzel}
<div class="pf">{fuss}{'<br>' if fuss else ''}{PFLICHT}</div>
<div class="foot"><span>18+ · Keine Gewinngarantie</span><span>sportwetten-radar.net</span></div>
</body></html>"""
    tmp = ziel + ".html"
    open(tmp, "w", encoding="utf-8").write(html)
    js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});"
          "const p=await b.newPage({viewport:{width:1080,height:1350}});await p.goto(process.argv[1]);await p.waitForTimeout(400);"
          "await p.screenshot({path:process.argv[2]});await b.close();})();")
    env = dict(os.environ, NODE_PATH=subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip())
    subprocess.run(["node", "-e", js, "file://" + os.path.abspath(tmp), ziel], check=True, env=env)
    os.remove(tmp)
    return ziel


def kurz(s):
    x = d(s)
    return f"{x.day}.{x.month}."


# ---------------------------------------------------------------- Hauptablauf
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--medien", required=True)
    ap.add_argument("--homepage", required=True)
    ap.add_argument("--modus", choices=["tag", "woche", "monat"], default="woche")
    ap.add_argument("--trocken", action="store_true")
    a = ap.parse_args()
    res = {"status": "ok", "fehler": [], "aenderungen": [], "grafiken": []}

    data = json.load(open(os.path.join(a.medien, "daten/ergebnisse.json"), encoding="utf-8"))
    res["fehler"] = pruefe(data)

    hp = lade_homepage(a.homepage)
    monate = {m["monat"]: m for m in hp["m"]}
    wochen = {w["von"]: w for w in hp["w"]}

    # Bestehende Homepage-Werte dürfen nicht stillschweigend überschrieben werden
    for m in data.get("monate", []):
        alt = monate.get(m["monat"])
        if alt and not gleich(alt, m):
            res["fehler"].append(f"Monat {m['monat']}: Bot-Zahlen weichen von der Homepage ab (Homepage {alt['live']}, Bot {m['live']})")
        elif alt and ergaenze(alt, m):
            res["aenderungen"].append(f"Monat {m['monat']} ergänzt")
        elif not alt:
            monate[m["monat"]] = homepage_eintrag(m)
            res["aenderungen"].append(f"Monat {m['monat']} neu")
    for w in data.get("wochen", []):
        alt = wochen.get(w["von"])
        if alt and not gleich(alt, w):
            res["fehler"].append(f"Woche {w['von']}: Bot-Zahlen weichen von der Homepage ab")
        elif alt and ergaenze(alt, w):
            res["aenderungen"].append(f"Woche {w['von']}–{w['bis']} ergänzt")
        elif not alt:
            wochen[w["von"]] = homepage_eintrag(w)
            res["aenderungen"].append(f"Woche {w['von']}–{w['bis']} neu")

    kurve, start = baue_tage(data)
    if kurve is not None and (kurve != hp["t"] or start != hp["s"]):
        res["aenderungen"].append("Kurve seit Start aktualisiert")
    if kurve is None:
        kurve, start = hp["t"], hp["s"]

    if res["fehler"]:
        res["status"] = "stopp"
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 2

    if not a.trocken and res["aenderungen"]:
        schreibe_homepage(a.homepage, list(monate.values()), list(wochen.values()), hp["h"], kurve, start)
        ix = os.path.join(a.homepage, "index.html")
        h = open(ix, encoding="utf-8").read()
        h = re.sub(r"trackrecord-daten\.js\?v=[0-9a-z]+", "trackrecord-daten.js?v=" + dt.datetime.now().strftime("%Y%m%d%H%M"), h)
        open(ix, "w", encoding="utf-8").write(h)
        gen = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seiten_generator.py")
        subprocess.run([sys.executable, gen, a.homepage], check=True, capture_output=True)

    # Grafik für X: neueste Woche bzw. neuester Monat
    ziel_dir = os.path.join(a.medien, "x")
    os.makedirs(ziel_dir, exist_ok=True)
    if a.modus == "tag" and data.get("tage"):
        t = max(data["tage"], key=lambda x: x["datum"])
        wt = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"][d(t["datum"]).weekday()]
        z = os.path.join(ziel_dir, f"{t['datum']}_tagesbilanz.png")
        if not a.trocken:
            grafik(t, f"{wt} {kurz(t['datum'])}", "Tagesbilanz", z, a.homepage, start=seit_start(t), fuss_text=fussnote(data))
        res["grafiken"].append({"art": "tag", "datei": os.path.relpath(z, a.medien), "datum": t["datum"],
                                "live": t["live"], "einzelspiele": t["einzelspiele"], "rueckrechnung": bool(t.get("rueckrechnung"))})
    if a.modus == "woche" and data.get("wochen"):
        w = max(data["wochen"], key=lambda x: x["von"])
        z = os.path.join(ziel_dir, f"{w['bis']}_wochenbilanz.png")
        if not a.trocken:
            grafik(w, f"{kurz(w['von'])}–{kurz(w['bis'])}", "Wochenbilanz", z, a.homepage, fuss_text=fussnote(data, w["von"], w["bis"]))
        res["grafiken"].append({"art": "woche", "datei": os.path.relpath(z, a.medien), "von": w["von"], "bis": w["bis"],
                                "live": w["live"], "einzelspiele": w["einzelspiele"], "rueckrechnung": bool(w.get("rueckrechnung"))})
    if a.modus == "monat" and data.get("monate"):
        m = max(data["monate"], key=lambda x: x["monat"])
        y, mo = map(int, m["monat"].split("-"))
        z = os.path.join(ziel_dir, f"{m['monat']}_monatsbericht.png")
        if not a.trocken:
            grafik(m, f"{MONATE[mo - 1]} {y}", "Monatsbericht", z, a.homepage, fuss_text=fussnote(data, m["monat"] + "-01", m["monat"] + "-31"))
        res["grafiken"].append({"art": "monat", "datei": os.path.relpath(z, a.medien), "monat": m["monat"],
                                "live": m["live"], "einzelspiele": m["einzelspiele"], "rueckrechnung": bool(m.get("rueckrechnung"))})
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
