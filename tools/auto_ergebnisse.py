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
JAHR_MIN_WETTEN = 100  # Einsätze und Rendite werden je Kalenderjahr erst ab dieser Zahl gewerteter Live-Wetten ausgewiesen
HINWEIS_JAHR = ("Einsätze und Rendite weisen wir je Kalenderjahr aus, sobald 100 Live-Wetten vorliegen. "
                "Für Tage, Wochen und Monate nicht, weil kurze Zeiträume stark vom Zufall abhängen.")
MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August",
          "September", "Oktober", "November", "Dezember"]


def d(s):
    return dt.date.fromisoformat(s)


def de(n, k=1):
    return f"{abs(n):,.{k}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def signed(n, k=1):
    return ("+" if n > 0 else "−" if n < 0 else "") + de(n, k)


# ---------------------------------------------------------------- Durchschnittsquote
# Ø-Quote = Durchschnitt der Quoten ALLER gesetzten Live-Wetten des Zeitraums (nicht nur der gewonnenen).
# Quelle in dieser Reihenfolge: (1) Feld live.quote in ergebnisse.json (vom Bot), (2) Einzelquoten in daten/signale.json,
# aber nur, wenn dort alle Wetten des Zeitraums vorliegen (Anzahl stimmt mit ergebnisse.json überein). Sonst None (nicht anzeigen).
_SIG = {}


def lade_signale(medien):
    p = os.path.join(medien, "daten/signale.json")
    _SIG.clear()
    if not os.path.exists(p):
        return
    for x in json.load(open(p, encoding="utf-8")).get("signale", []):
        if x.get("art") == "live" and x.get("ergebnis") in ("gewonnen", "verloren") and isinstance(x.get("quote"), (int, float)):
            _SIG.setdefault(x["datum"], []).append(x["quote"])


def quote_tag(t):
    q = t.get("live", {}).get("quote")
    if isinstance(q, (int, float)):
        return q, t["live"]["wetten"]
    qs = _SIG.get(t["datum"], [])
    if t["live"]["wetten"] == 0:
        return None, 0
    if len(qs) == t["live"]["wetten"]:
        return sum(qs) / len(qs), len(qs)
    return None, t["live"]["wetten"]


def quote_zeitraum(data, von, bis):
    """Gewichteter Durchschnitt über alle Tage von..bis (ISO-Strings); None, wenn für einen Tag mit Wetten die Quote fehlt."""
    n = 0
    summe = 0.0
    for t in data.get("tage", []):
        if von <= t["datum"] <= bis and t["live"]["wetten"] > 0:
            q, w = quote_tag(t)
            if q is None:
                return None
            summe += q * w
            n += w
    return round(summe / n, 2) if n else None


def quote_block(data, b, von, bis):
    q = b.get("live", {}).get("quote")
    if isinstance(q, (int, float)):
        return round(q, 2)
    return quote_zeitraum(data, von, bis)


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
        if z["wetten"] and abs(z["gewinn"] / z["wetten"] * 100 - z["rendite"]) > 0.15 + 5.0 / z["wetten"]:
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
        "global.window={};require(process.argv[1]);console.log(JSON.stringify({m:window.TRACKRECORD,w:window.TRACKRECORD_WOCHEN||[],h:window.TRACKRECORD_WOCHEN_HINWEIS||'',t:window.TRACKRECORD_TAGE||[],j:window.TRACKRECORD_JAHRE||[]}))",
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
    im_zeitraum = [t for t in data.get("tage", []) if von is None or von <= t["datum"] <= bis]
    if len(tl) == len(im_zeitraum):  # komplett Testphase (z. B. September): Zeitraum der ganzen Testphase nennen
        tl = [t["datum"] for t in data.get("tage", []) if t.get("rueckrechnung")]
    a, b = min(tl), max(tl)
    f = lambda x: f"{x[8:10]}.{x[5:7]}."
    return f"* {f(a)}–{f(b)}: Testphase, mit den Regeln vom 11.10.2026 berechnet."
PFLICHT = "Alle Zahlen gelten bei gleichem Einsatz auf jede Live-Wette. Verlustserien gehören dazu."
QUOTE_DEF = "Ø-Quote: Durchschnitt der Quoten aller gesetzten Live-Wetten im Zeitraum."


def seit_start(t):
    """Block "seit Start" eines Tages (Feldname im erweiterten JSON: seitStart)."""
    return t.get("seitStart") or t.get("seit_start") or t.get("seitstart")


ALT_FELDER = ("rendite", "gewinn", "rueckgang", "besterTag", "schlechtesterTag")  # werden für Monate/Wochen nicht mehr veröffentlicht


def zeitraum(b):
    if "monat" in b and "von" not in b:
        return b["monat"] + "-01", b["monat"] + "-31"
    return b["von"], b["bis"]


def homepage_eintrag(b, data):
    L, E = b["live"], b["einzelspiele"]
    live = {"wetten": L["wetten"], "treffer": L["treffer"]}
    q = quote_block(data, b, *zeitraum(b))
    if q is not None:
        live["quote"] = q
    if "verlustserie" in L:
        live["verlustserie"] = L["verlustserie"]
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
    return a["einzelspiele"] == {"tipps": b["einzelspiele"]["tipps"], "treffer": b["einzelspiele"]["treffer"]}


def ergaenze(alt, neu, data):
    """Bereinigt alte Felder (Einsätze/Rendite je Monat/Woche) und ergänzt Ø-Quote und Verlustserie, nie vorhandene Werte überschreiben."""
    geaendert = False
    for k in ALT_FELDER:
        if k in alt["live"]:
            del alt["live"][k]
            geaendert = True
    if "verlustserie" in neu["live"] and "verlustserie" not in alt["live"]:
        alt["live"]["verlustserie"] = neu["live"]["verlustserie"]
        geaendert = True
    q = quote_block(data, neu, *zeitraum(neu))
    if q is not None and alt["live"].get("quote") != q:
        alt["live"]["quote"] = q
        geaendert = True
    return geaendert


KURVE_AB_WETTEN = 20  # die Trefferquoten-Kurve beginnt erst, wenn das Jahr 20 Live-Wetten hat (davor springt sie zu stark)
X_GRAFIKEN = False  # X-Konto gelöscht (10.11.2026); True nur, wenn Grafiken wieder gebraucht werden


def baue_jahre(data):
    """Kurve (kumulierte Trefferquote in % je Tag, je Kalenderjahr neu beginnend) und Jahresblöcke aus ergebnisse.json.
    Einsätze/Rendite und Kurve eines Jahres werden erst veröffentlicht, wenn das Jahr JAHR_MIN_WETTEN gewertete Live-Wetten hat.
    Gibt (None, None) zurück, solange das erweiterte JSON (Tage mit seitStart) fehlt."""
    tl = sorted(data.get("tage", []), key=lambda x: x["datum"])
    if not tl or not all(isinstance(seit_start(t), dict) and isinstance(seit_start(t).get("gewinn"), (int, float)) for t in tl):
        return None, None
    kurve, jahre = [], []
    for jahr in sorted({t["datum"][:4] for t in tl}):
        tj = [t for t in tl if t["datum"][:4] == jahr]
        vor = [t for t in tl if t["datum"][:4] < jahr]
        v = seit_start(vor[-1]) if vor else {"wetten": 0, "treffer": 0, "gewinn": 0.0}
        z = seit_start(tj[-1])
        w, tr, g = z["wetten"] - v["wetten"], z["treffer"] - v["treffer"], round(z["gewinn"] - v["gewinn"], 1)
        frei = w >= JAHR_MIN_WETTEN
        rendite = z["rendite"] if not vor else (round(g / w * 100, 1) if w else 0.0)
        j = {"jahr": int(jahr), "ab": tj[0]["datum"], "stand": tj[-1]["datum"], "wetten": w, "treffer": tr}
        q = quote_zeitraum(data, tj[0]["datum"], tj[-1]["datum"])
        if q is not None:
            j["quote"] = q
        j["gewinn"] = g if frei else None
        j["rendite"] = rendite if frei else None
        j["rueckrechnung"] = any(t.get("rueckrechnung") for t in tj)
        jahre.append(j)
        if frei:
            for t in tj:
                zt = seit_start(t)
                wt, tt = zt["wetten"] - v["wetten"], zt["treffer"] - v["treffer"]
                if wt >= KURVE_AB_WETTEN:
                    kurve.append({"d": t["datum"], "q": round(tt / wt * 100, 1), "rr": bool(t.get("rueckrechnung"))})
    return kurve, jahre


def jahre_homepage(jahre):
    """Jahresblöcke für die Homepage: ohne Einsätze und Rendite (die gibt es nur in Telegram)."""
    return [{k: v for k, v in j.items() if k not in ("gewinn", "rendite")} for j in jahre]


KOPF = """/* =====================================================================
   TRACKRECORD-DATEN  —  wird von tools/auto_ergebnisse.py aus daten/ergebnisse.json
   (und daten/signale.json für die Ø-Quote) geschrieben. Nicht von Hand ändern.

   Anzeige-Regeln (Daniel, 06.11.2026):
   - Tage, Wochen, Monate: Wetten, Treffer (mit Prozent) und Ø-Quote. KEINE Einsätze, KEINE Rendite.
   - Einsätze und Rendite stehen NICHT auf der Homepage (nur in den Telegram-Kanälen, je Kalenderjahr ab 100 Live-Wetten).
   - Jahreskurve: kumulierte Trefferquote je Tag, erst ab 100 Live-Wetten im Jahr, Beginn ab 20 Wetten (Entscheidung 09.11.2026).
   - Ø-Quote = Durchschnitt der Quoten aller gesetzten Live-Wetten des Zeitraums.
   ===================================================================== */

"""


def schreibe_homepage(hp, monate, wochen, hinweis, kurve=None, jahre=None):
    p = os.path.join(hp, "trackrecord-daten.js")
    mon = ",\n\n".join(js_block(x) for x in sorted(monate, key=lambda x: x["monat"], reverse=True))
    wo = ",\n".join(js_block(x) for x in sorted(wochen, key=lambda x: x["von"]))
    neu = (KOPF + "window.TRACKRECORD = [\n\n" + mon + "\n\n];\n\n"
           "/* Wochen (Mo–So). Der Monat ist der Mehrheitsmonat der Woche. */\n"
           "window.TRACKRECORD_WOCHEN = [\n" + wo + "\n];\n\n"
           "/* Hinweis, wenn für einen Monat keine Wochenwerte angezeigt werden können. */\n"
           "window.TRACKRECORD_WOCHEN_HINWEIS = " + json.dumps(hinweis, ensure_ascii=False) + ";\n\n"
           "/* Kurve: kumulierte Trefferquote in % je Tag, je Kalenderjahr neu beginnend (d = Datum, q = Stand am Tagesende, rr = nur Logik für Fußnote/Hinterlegung).\n"
           "   Ein Jahr erscheint erst ab 100 Live-Wetten. */\n"
           "window.TRACKRECORD_TAGE = [\n" + ",\n".join("  " + json.dumps(x, ensure_ascii=False) for x in (kurve or [])) + "\n];\n\n"
           "/* Kalenderjahre: Wetten, Treffer, Ø-Quote; keine Einsätze/Rendite. */\n"
           "window.TRACKRECORD_JAHRE = [\n" + ",\n".join("  " + json.dumps(x, ensure_ascii=False) for x in (jahre or [])) + "\n];\n")
    open(p, "w", encoding="utf-8").write(neu)


# ---------------------------------------------------------------- Grafik für X
def zeilen(L, quote=None, klein=False, stern=""):
    """Tag/Woche/Monat (Daniel, 06.11.2026): "n von m Treffer", Trefferquote, Ø-Quote. Keine Einsätze, keine Rendite."""
    c = "z s" if klein else "z"
    if L["wetten"] == 0:
        return f'<div class="{c}">Keine Live-Wetten</div>'
    q = L["treffer"] / L["wetten"] * 100
    out = (f'<div class="{c} lead"><b>{L["treffer"]} von {L["wetten"]}</b> Treffer{stern}</div>'
           f'<div class="{c}">Trefferquote <b>{de(q)} %</b></div>')
    if quote:
        out += f'<div class="{c}">Ø-Quote <b>{de(quote, 2)}</b></div>'
    return out


def jahr_card(J, stern=""):
    """Jahresübersicht: Einsätze und Rendite nur hier, und erst ab JAHR_MIN_WETTEN Live-Wetten im Jahr."""
    ab = "" if J["ab"][5:] == "01-01" else f" · ab {J['ab'][8:10]}.{J['ab'][5:7]}."
    q = J["treffer"] / J["wetten"] * 100 if J["wetten"] else 0
    z = f'<div class="z s"><b>{J["treffer"]} von {J["wetten"]}</b> Treffer ({de(q)} %)</div>'
    if J.get("quote"):
        z += f'<div class="z s">Ø-Quote <b>{de(J["quote"], 2)}</b></div>'
    if J.get("gewinn") is not None:
        z += (f'<div class="z s lead"><b>{signed(J["gewinn"])}</b> Einsätze{stern}</div>'
              f'<div class="z s">Rendite <b>{signed(J["rendite"])} %</b></div>')
    else:
        z += f'<div class="z s">Einsätze und Rendite ab {JAHR_MIN_WETTEN} Wetten{stern}</div>'
    return f'<div class="card"><div class="ct">Jahr {J["jahr"]}{ab}</div>{z}</div>'


def grafik(b, titel, kicker, ziel, hp, jahr=None, fuss_text=None, quote=None):
    L, E = b["live"], b["einzelspiele"]
    eq = E["treffer"] / E["tipps"] * 100 if E["tipps"] else 0
    f = "file://" + os.path.join(os.path.abspath(hp), "assets/fonts/")
    logo = "file://" + os.path.join(os.path.abspath(hp), "assets/logo-icon.png")
    fuss = f'<div class="rr">{fuss_text}</div>' if fuss_text else ""
    stern_live = "*" if (fuss_text and b.get("rueckrechnung")) else ""
    stern_jahr = "*" if (fuss_text and jahr and jahr.get("rueckrechnung")) else ""
    jahr_html = jahr_card(jahr, stern_jahr) if jahr else ""
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
<div class="card"><div class="ct">Live-Wetten</div>{zeilen(L, quote, stern=stern_live)}</div>
{jahr_html}
{einzel}
<div class="pf">{fuss}{'<br>' if fuss else ''}{QUOTE_DEF}<br>{PFLICHT}</div>
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

    lade_signale(a.medien)
    hp = lade_homepage(a.homepage)
    monate = {m["monat"]: m for m in hp["m"]}
    wochen = {w["von"]: w for w in hp["w"]}

    # Bestehende Homepage-Werte dürfen nicht stillschweigend überschrieben werden
    for m in data.get("monate", []):
        alt = monate.get(m["monat"])
        if alt and not gleich(alt, m):
            res["fehler"].append(f"Monat {m['monat']}: Bot-Zahlen weichen von der Homepage ab (Homepage {alt['live']}, Bot {m['live']})")
        elif alt and ergaenze(alt, m, data):
            res["aenderungen"].append(f"Monat {m['monat']} ergänzt/bereinigt")
        elif not alt:
            monate[m["monat"]] = homepage_eintrag(m, data)
            res["aenderungen"].append(f"Monat {m['monat']} neu")
    for w in data.get("wochen", []):
        alt = wochen.get(w["von"])
        if alt and not gleich(alt, w):
            res["fehler"].append(f"Woche {w['von']}: Bot-Zahlen weichen von der Homepage ab")
        elif alt and ergaenze(alt, w, data):
            res["aenderungen"].append(f"Woche {w['von']}–{w['bis']} ergänzt/bereinigt")
        elif not alt:
            wochen[w["von"]] = homepage_eintrag(w, data)
            res["aenderungen"].append(f"Woche {w['von']}–{w['bis']} neu")

    kurve, jahre_voll = baue_jahre(data)
    if kurve is None:
        kurve, jahre_voll = hp["t"], hp["j"]
    jahre = jahre_homepage(jahre_voll)
    if kurve != hp["t"] or jahre != hp["j"]:
        res["aenderungen"].append("Kurve/Jahresblock aktualisiert")

    if res["fehler"]:
        res["status"] = "stopp"
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 2

    if not a.trocken and res["aenderungen"]:
        schreibe_homepage(a.homepage, list(monate.values()), list(wochen.values()), hp["h"], kurve, jahre)
        ix = os.path.join(a.homepage, "index.html")
        h = open(ix, encoding="utf-8").read()
        h = re.sub(r"trackrecord-daten\.js\?v=[0-9a-z]+", "trackrecord-daten.js?v=" + dt.datetime.now().strftime("%Y%m%d%H%M"), h)
        open(ix, "w", encoding="utf-8").write(h)
        gen = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seiten_generator.py")
        subprocess.run([sys.executable, gen, a.homepage], check=True, capture_output=True)

    def jahr_von(datum):
        return next((j for j in (jahre_voll or []) if str(j["jahr"]) == datum[:4]), None)

    def ausgabe(b, quote):
        """Nur die erlaubten Zahlen weitergeben (Wetten, Treffer, Ø-Quote) — Einsätze/Rendite nie aus Tag/Woche/Monat."""
        o = {"wetten": b["live"]["wetten"], "treffer": b["live"]["treffer"]}
        if quote is not None:
            o["quote"] = quote
        return o

    # X-Konto gelöscht (10.11.2026): keine Grafiken mehr erzeugen. Die Ausgabe grafiken[] bleibt (Kennzahlen), Datei wird nicht geschrieben.
    ziel_dir = os.path.join(a.medien, "x")
    if a.modus == "tag" and data.get("tage"):
        t = max(data["tage"], key=lambda x: x["datum"])
        wt = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"][d(t["datum"]).weekday()]
        z = os.path.join(ziel_dir, f"{t['datum']}_tagesbilanz.png")
        J = jahr_von(t["datum"])
        q = quote_tag(t)[0]
        q = round(q, 2) if q is not None else None
        if X_GRAFIKEN and not a.trocken:
            os.makedirs(ziel_dir, exist_ok=True)
            grafik(t, f"{wt} {kurz(t['datum'])}", "Tagesbilanz", z, a.homepage, jahr=J,
                   fuss_text=(fussnote(data) if (J and J.get("rueckrechnung")) or t.get("rueckrechnung") else None), quote=q)
        res["grafiken"].append({"art": "tag", "datei": os.path.relpath(z, a.medien), "datum": t["datum"],
                                "live": ausgabe(t, q), "jahr": J, "einzelspiele": t["einzelspiele"], "rueckrechnung": bool(t.get("rueckrechnung"))})
    if a.modus == "woche" and data.get("wochen"):
        w = max(data["wochen"], key=lambda x: x["von"])
        z = os.path.join(ziel_dir, f"{w['bis']}_wochenbilanz.png")
        q = quote_block(data, w, w["von"], w["bis"])
        if X_GRAFIKEN and not a.trocken:
            os.makedirs(ziel_dir, exist_ok=True)
            grafik(w, f"{kurz(w['von'])}–{kurz(w['bis'])}", "Wochenbilanz", z, a.homepage, fuss_text=fussnote(data, w["von"], w["bis"]), quote=q)
        res["grafiken"].append({"art": "woche", "datei": os.path.relpath(z, a.medien), "von": w["von"], "bis": w["bis"],
                                "live": ausgabe(w, q), "jahr": jahr_von(w["bis"]), "verlustserie": w["live"].get("verlustserie"),
                                "einzelspiele": w["einzelspiele"], "rueckrechnung": bool(w.get("rueckrechnung"))})
    if a.modus == "monat" and data.get("monate"):
        m = max(data["monate"], key=lambda x: x["monat"])
        y, mo = map(int, m["monat"].split("-"))
        z = os.path.join(ziel_dir, f"{m['monat']}_monatsbericht.png")
        J = jahr_von(m["monat"] + "-01")
        q = quote_block(data, m, m["monat"] + "-01", m["monat"] + "-31")
        if X_GRAFIKEN and not a.trocken:
            os.makedirs(ziel_dir, exist_ok=True)
            grafik(m, f"{MONATE[mo - 1]} {y}", "Monatsbericht", z, a.homepage, jahr=J,
                   fuss_text=(fussnote(data) if (J and J.get("rueckrechnung")) else fussnote(data, m["monat"] + "-01", m["monat"] + "-31")), quote=q)
        res["grafiken"].append({"art": "monat", "datei": os.path.relpath(z, a.medien), "monat": m["monat"],
                                "live": ausgabe(m, q), "jahr": J, "verlustserie": m["live"].get("verlustserie"),
                                "einzelspiele": m["einzelspiele"], "rueckrechnung": bool(m.get("rueckrechnung"))})
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
