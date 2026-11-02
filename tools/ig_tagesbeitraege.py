#!/usr/bin/env python3
"""Ergebnis-Beiträge aus daten/signale.json (Regeln: tools/ergebnis-beitraege-regeln.md, Entscheidung Daniel 02.11.2026).

  python3 ig_tagesbeitraege.py --medien <repo> --modus tag   --datum 2026-11-02 --out <ordner>
  python3 ig_tagesbeitraege.py --medien <repo> --modus woche --datum 2026-11-09 --out <ordner>   (datum = Montag der Auswertung, Woche Mo-So davor)
  python3 ig_tagesbeitraege.py --medien <repo> --modus monat --datum 2026-12-01 --out <ordner>   (datum = 1. des Folgemonats)

Ausgabe: PNGs (Karussell 1080x1350: k1..kN, Stories 1080x1920: s1..sN), bei modus tag zusätzlich reel.mp4 (1080x1920),
dazu manifest.json (Dateien, Texte, Status). Keine Kennzahlen, keine Prozente, keine Summen, keine Kurve, keine Beträge.
Exit 0 = ok, 3 = Daten unvollständig (nichts erzeugt).
"""
import argparse, datetime as dt, json, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ig_spezial as s
import ig_ergebnis_css as C

WT = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
WK = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
MON = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
STATUS_OK = {"gewonnen", "verloren", "storniert"}
PFLICHT = "18+ · Keine Gewinngarantie · Glücksspiel kann süchtig machen · check-dein-spiel.de"
HASH = "#Fußball #Statistik #Analyse"
D = lambda x: dt.date.fromisoformat(x)
dm = lambda d: d.strftime("%d.%m.")


def markt(m):
    m = m.replace(".", ",")
    if m.startswith("Über "): return "Ü " + m[5:].replace(" Tore", "")
    if m.startswith("Unter "): return "U " + m[6:].replace(" Tore", "")
    return m


def lade(medien):
    d = json.load(open(os.path.join(medien, "daten", "signale.json"), encoding="utf-8"))
    return d["signale"], d.get("stand", "")


def eintraege(sig, von, bis, art):
    out = [x for x in sig if x["art"] == art and von <= D(x["datum"]) <= bis]
    return sorted(out, key=lambda x: (x["datum"], x["id"]))


def zeile(x):
    q = f"{x['quote']:.2f}".replace(".", ",")
    return (f"{x['heim']} – {x['gast']}", markt(x["markt"]), q, x["ergebnis"])


def sym(st): return ("✓", "w") if st == "gewonnen" else ("✕", "l") if st == "verloren" else ("–", "l")


def rows(rs, k0=0):
    o = ""
    for i, (sp, mk, q, st) in enumerate(rs):
        t, c = sym(st)
        o += f'<div class="tr"><em>{k0+i+1}</em><div>{sp}</div><span>{mk}</span><b>{q}</b><u class="{c}">{t}</u></div>'
    return o


HEAD = '<div class="th"><span>NR.</span><span>SPIEL</span><span>MARKT</span><span>QUOTE</span><span></span></div>'
LEG = ('<div class="leg"><span><u>✓</u>gewonnen</span><span><u class="l">✕</u>verloren</span>'
       '<span><u class="l">–</u>storniert</span></div>')
EXTRA = """
.tr span{width:150px;font-size:22px}.th span:nth-child(3){width:150px}
.tr div{font-size:27px}
.story .eb{top:330px}.story .tb{top:392px}.story .foot{bottom:300px}.story .top{top:130px}
.tag{display:none}
.nl{font-size:30px;line-height:1.4;color:#a9b8c8;margin-top:26px}
"""


def page(eb, inner, story=False):
    return (f'<div class="{"story" if story else ""}">' + s.RINGS + '<div class="top"><img src="LOGO"><span>Sportwetten Radar</span></div>'
            f'<div class="eb">{eb}</div>{inner}<div class="foot"><span>18+ · Keine Gewinngarantie</span><span>@sportwetten_radar</span></div></div>')


def tabellen(titel, rs, k0_max=12, story=False, hinweis=None):
    """Seiten mit je max 12 Zeilen."""
    seiten = []
    n = max(1, -(-len(rs) // k0_max))
    for p in range(n):
        ch = rs[p * k0_max:(p + 1) * k0_max]
        suf = f" · {p*k0_max+1}–{p*k0_max+len(ch)}" if n > 1 else ""
        note = f'<div class="nl">{hinweis}</div>' if (hinweis and story and p == n - 1) else ""
        seiten.append(page(titel + suf, '<div class="tb">' + HEAD + rows(ch, p * k0_max) + LEG + note + '</div>', story))
    return seiten


def einzel_seite(titel, rs, story=False, hinweis=None):
    note = '<div class="note">Bis zu fünf ausgewählte Einzelspiele vor Anpfiff. Ob einzeln oder selbst kombiniert, entscheidet jeder selbst.</div>'
    if story and hinweis: note += f'<div class="nl">{hinweis}</div>'
    return page(titel, '<div class="tb big">' + HEAD + rows(rs) + LEG + note + '</div>', story)


def hinweis_seite(eb, kopf, absaetze):
    return page(eb, f"<div class='tb'><h1 style='font-family:B;font-weight:800;font-size:70px;line-height:1.05'>{kopf}</h1>" +
                "".join(f'<div class="p">{a}</div>' for a in absaetze) + "</div>")


def dots_row(lab, sub, ds):
    if not ds: return f'<div class="wr"><b>{lab}<small>{sub}</small></b><div class="dt" style="color:#6f8399;font-size:24px">keine Einträge</div></div>'
    return (f'<div class="wr"><b>{lab}<small>{sub}</small></b><div class="dt">' +
            "".join(f'<i class="{"" if st=="gewonnen" else "l"}"></i>' for st in ds) + '</div></div>')


def render_html(seiten, css, hoehe, outdir, prefix):
    from playwright.sync_api import sync_playwright
    logo = "file://" + os.path.join(s.HOME, "logo-icon.png")
    tmp = tempfile.mkdtemp(); files = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        for i, h in enumerate(seiten, 1):
            pg = b.new_page(viewport={"width": 1080, "height": hoehe})
            f = os.path.join(tmp, f"{prefix}{i}.html")
            open(f, "w", encoding="utf-8").write(f'<html><head><meta charset="utf-8"><style>{css}html,body{{height:{hoehe}px!important}}</style></head><body>{h.replace("LOGO", logo)}</body></html>')
            pg.goto("file://" + f); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(250)
            # lange Spielnamen verkleinern statt abschneiden
            pg.evaluate("document.querySelectorAll('.tr div').forEach(e=>{let f=parseFloat(getComputedStyle(e).fontSize);while(e.scrollWidth>e.clientWidth+1&&f>16){f-=1;e.style.fontSize=f+'px'}})")
            ub = pg.evaluate("(()=>{const m=document.querySelector('.tb');return m?Math.round(m.getBoundingClientRect().bottom):0})()")
            if ub > hoehe - (170 if hoehe == 1350 else 330): print(f"WARNUNG {prefix}{i}: Unterkante {ub}", file=sys.stderr)
            path = os.path.join(outdir, f"{prefix}{i}.png")
            pg.screenshot(path=path); files.append(os.path.basename(path)); pg.close()
        b.close()
    return files


def reel(live, einzel, titel_tag, out):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import erklaervideo as E
    E.HOCH = True; E.W, E.H = 1080, 1920
    orig = E.folie_html
    E.CSS_HOCH += """
.rt{display:grid;gap:12px;margin-top:30px}.rr{display:flex;align-items:center;gap:18px;background:#0f1d2c;border:2px solid #1b2c40;border-radius:22px;padding:14px 24px;min-height:96px}
.rr em{font-style:normal;font-family:M;font-size:26px;color:#6f8399;width:52px;flex:none}.rr div{flex:1;font-size:32px;line-height:1.15;color:#eef3f8}
.rr small{display:block;font-family:M;font-size:23px;color:#8aa0b5;margin-top:3px}.rr b{font-family:M;font-weight:500;font-size:30px;color:#eef3f8}
.rr u{text-decoration:none;flex:none;width:58px;height:58px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:B;font-weight:800;font-size:34px;margin-left:10px}
.rr u.w{background:#2edb99;color:#0a1620}.rr u.l{background:#26364a;color:#c9d6e3;border:2px solid #3a4f68}
.rn{font-size:30px;color:#a9b8c8;margin-top:22px}
"""
    def fh(f, logo):
        top = f'<div class="top"><img src="{logo}"><span>Sportwetten <b>Radar</b></span></div>'
        if f["typ"] == "tabelle":
            r = "".join(f'<div class="rr"><em>{f["k0"]+i+1}</em><div>{sp}<small>{mk}</small></div><b>{q}</b><u class="{sym(st)[1]}">{sym(st)[0]}</u></div>' for i, (sp, mk, q, st) in enumerate(f["rows"]))
            return (top + f'<div class="main"><div class="eb">{f["eyebrow"]}</div><div class="rt">{r}</div>' +
                    (f'<div class="rn">{f["rest"]}</div>' if f.get("rest") else "") + '</div><div class="foot"><span>18+ · Keine Gewinngarantie</span><span>@sportwetten_radar</span></div>')
        if f["typ"] == "ende":
            return (top + '<div class="main end"><div class="eb">Sportwetten Radar</div><h1 class="k">Jeder Eintrag. <em>Jeden Tag.</em></h1>'
                    '<div class="hint">Alle Auswertungen öffentlich im Ergebnis-Kanal, Link in der Bio · 18+ · Keine Gewinngarantie · Glücksspiel kann süchtig machen · check-dein-spiel.de</div></div>')
        return orig(f, logo).replace("<span>sportwetten-radar.net</span>", "<span>@sportwetten_radar</span>")
    E.folie_html = fh
    folien = [{"typ": "hook", "dauer": 2.6, "text": f"Auswertung\nvom [[{titel_tag}.]]"}]
    MAXR = 8
    if live:
        ch = live[:MAXR * 3]
        for k in range(0, len(ch), MAXR):
            part = ch[k:k + MAXR]
            rest = f"Weitere {len(live)-len(ch)} Einträge im Karussell." if (k + MAXR >= len(ch) and len(live) > len(ch)) else ""
            folien.append({"typ": "tabelle", "dauer": max(4.0, 1.2 + 0.6 * len(part)), "k0": k, "rows": part,
                           "eyebrow": f"Live-Wetten · {k+1}–{k+len(part)}" if len(live) > MAXR else "Live-Wetten", "rest": rest})
    if einzel:
        folien.append({"typ": "tabelle", "dauer": max(4.0, 1.2 + 0.6 * len(einzel)), "k0": 0, "rows": einzel, "eyebrow": "Einzelspiele zum Kombinieren"})
    folien.append({"typ": "text", "dauer": 4.0, "eyebrow": "Unsere Regel", "text": "Nichts aussortiert.\nNichts nachträglich geändert."})
    folien.append({"typ": "ende", "dauer": 3.5})
    sp = {"titel": "Auswertung", "folien": folien}
    t2 = tempfile.mkdtemp(); pngs = E.render(sp, s.HOME, t2); return E.baue(sp, pngs, out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--medien", required=True); ap.add_argument("--modus", choices=["tag", "woche", "monat"], required=True)
    ap.add_argument("--datum", required=True); ap.add_argument("--out", required=True); ap.add_argument("--ohne-reel", action="store_true")
    a = ap.parse_args()
    sig, stand = lade(a.medien); os.makedirs(a.out, exist_ok=True)
    heute = D(a.datum)
    css = s.CSS.replace("FONTS", "file://" + os.path.join(s.HOME, "assets/fonts")) + C.BASE + C.TAB + C.WOCHE + EXTRA
    man = {"modus": a.modus, "datum": a.datum, "stand": stand, "status": "ok", "fehler": []}
    if a.modus == "tag":
        tag = heute - dt.timedelta(days=1)
        live, ein = eintraege(sig, tag, tag, "live"), eintraege(sig, tag, tag, "einzel")
        if not live and not ein: man["status"] = "stopp"; man["fehler"].append(f"keine Einträge für {tag}")
        elif any(x["ergebnis"] not in STATUS_OK for x in live + ein): man["status"] = "stopp"; man["fehler"].append("Einträge ohne Ergebnis")
        elif stand[:10] != a.datum: man["status"] = "stopp"; man["fehler"].append(f"signale.json Stand {stand}, erwartet {a.datum}")
        if man["status"] != "ok": json.dump(man, open(os.path.join(a.out, "manifest.json"), "w"), ensure_ascii=False, indent=1); print(json.dumps(man, ensure_ascii=False)); return 3
        lr, er = [zeile(x) for x in live], [zeile(x) for x in ein]
        wt = f"{WK[tag.weekday()]} {dm(tag)}"; HW = "Alle Auswertungen im Ergebnis-Kanal. Link in der Bio."
        ks, ss = [], []
        if lr: ks += tabellen(f"Live-Wetten · {wt}", lr)
        if er: ks.append(einzel_seite(f"Einzelspiele · {wt}", er))
        ks.append(hinweis_seite("So lesen", "Gewonnen und verloren stehen nebeneinander.",
                  ["Jeder Eintrag wird ausgewertet, auch die verlorenen. Nichts wird nachträglich geändert.",
                   "Ein einzelner Tag sagt wenig. Die komplette Auswertung steht im Ergebnis-Kanal, Link in der Bio."]))
        if lr: ss += tabellen(f"Live-Wetten · {wt}", lr, story=True, hinweis=None if er else HW)
        if er: ss.append(einzel_seite(f"Einzelspiele · {wt}", er, story=True, hinweis=HW))
        man["karussell"] = render_html(ks, css, 1350, a.out, "k"); man["stories"] = render_html(ss, css, 1920, a.out, "s")
        if not a.ohne_reel and (lr or er):
            man["reel_sekunden"] = round(reel(lr, er, WT[tag.weekday()], os.path.join(a.out, "reel.mp4")), 1); man["reel"] = "reel.mp4"
        long = f"{WT[tag.weekday()]}, {tag.strftime('%d.%m.%Y')}"
        man["texte"] = {
            "instagram": f"Auswertung vom {long}: alle Einträge, gewonnen wie verloren. Nichts wird aussortiert.\n\nAlle Auswertungen öffentlich im Ergebnis-Kanal. Link in der Bio.\n\n{PFLICHT}\n\n{HASH}",
            "tiktok": f"Auswertung vom {long}: alle Einträge, gewonnen wie verloren. Link in der Bio. {PFLICHT} #Fußball #Statistik",
            "youtube_titel": f"Auswertung {WK[tag.weekday()]} {dm(tag)}: alle Einträge",
            "youtube": f"Auswertung vom {long}: alle Live-Wetten und Einzelspiele, gewonnen wie verloren. Nichts wird aussortiert oder nachträglich geändert.\nAlle Auswertungen öffentlich im Ergebnis-Kanal, Link in der Kanalbeschreibung.\n\n{PFLICHT}"}
        man["anzahl"] = {"live": len(lr), "einzel": len(er)}
    else:
        if a.modus == "woche":
            bis = heute - dt.timedelta(days=1); von = bis - dt.timedelta(days=6); eb = f"Woche {dm(von)}–{dm(bis)}"
            if von.weekday() != 0: man["status"] = "stopp"; man["fehler"].append("datum ist kein Montag")
            gruppen = [(WK[(von + dt.timedelta(days=i)).weekday()], dm(von + dt.timedelta(days=i)), von + dt.timedelta(days=i), von + dt.timedelta(days=i)) for i in range(7)]
        else:
            bis = heute - dt.timedelta(days=1); von = bis.replace(day=1); eb = f"Monatsbericht {MON[bis.month-1]}"
            gruppen = []; cur = von
            while cur <= bis:
                ende = min(cur + dt.timedelta(days=6 - cur.weekday()), bis)
                lab = f"KW {cur.isocalendar()[1]}"; gruppen.append((lab, f"{dm(cur)}–{dm(ende)}", cur, ende)); cur = ende + dt.timedelta(days=1)
        if stand[:10] != a.datum: man["status"] = "stopp"; man["fehler"].append(f"signale.json Stand {stand}, erwartet {a.datum}")
        live, ein = eintraege(sig, von, bis, "live"), eintraege(sig, von, bis, "einzel")
        if any(x["ergebnis"] not in STATUS_OK for x in live + ein): man["status"] = "stopp"; man["fehler"].append("Einträge ohne Ergebnis")
        if man["status"] != "ok": json.dump(man, open(os.path.join(a.out, "manifest.json"), "w"), ensure_ascii=False, indent=1); print(json.dumps(man, ensure_ascii=False)); return 3
        cls = "" if a.modus == "woche" else "m"
        def kart(art, titel, big):
            r = "".join(dots_row(l, sb, [x["ergebnis"] for x in eintraege(sig, v, b2, art)]) for l, sb, v, b2 in gruppen)
            extra = '<div class="note">Bis zu fünf ausgewählte Einzelspiele pro Spieltag.</div>' if (art == "einzel" and a.modus == "monat") else ""
            return page(titel, f'<div class="tb {cls} {big}">{r}{LEG}{extra}</div>')
        ks = [kart("live", f"{eb} · Live-Wetten", ""), kart("einzel", f"{eb} · Einzelspiele", "big w2" if a.modus == "woche" else "big")]
        kopf = "Gute und schwache Tage stehen nebeneinander." if a.modus == "woche" else "Ein Monat. Jeder Tag öffentlich."
        absatz = (["Jeder Eintrag der Woche wird ausgewertet, nichts wird nachträglich geändert. Die Einzelergebnisse aller Tage stehen im Ergebnis-Kanal, Link in der Bio."] if a.modus == "woche" else
                  ["Alle Auswertungen des Monats stehen im Ergebnis-Kanal, die starken Tage wie die schwachen. Nichts wird nachträglich geändert oder gelöscht.",
                   "Ein einzelner Monat ist eine kleine Stichprobe und sagt wenig über den nächsten. Link in der Bio."])
        ks.append(hinweis_seite(eb.split(" · ")[0], kopf, absatz))
        man["karussell"] = render_html(ks, css, 1350, a.out, "k")
        # Story: Live-Karte der Woche/des Monats im Story-Format
        r = "".join(dots_row(l, sb, [x["ergebnis"] for x in eintraege(sig, v, b2, "live")]) for l, sb, v, b2 in gruppen)
        st = page(f"{eb} · Live-Wetten", f'<div class="tb {cls}">{r}{LEG}<div class="nl">Alle Auswertungen im Ergebnis-Kanal. Link in der Bio.</div></div>', True)
        man["stories"] = render_html([st], css, 1920, a.out, "s")
        txt = (f"{eb.replace('Woche', 'Wochenauswertung')}: jeder Eintrag der Woche als Punkt, gewonnen wie verloren." if a.modus == "woche" else
               f"Monatsbericht {MON[bis.month-1]} {bis.year}: jeder Eintrag des Monats als Punkt, gewonnen wie verloren.")
        man["texte"] = {"instagram": f"{txt}\n\nAlle Auswertungen öffentlich im Ergebnis-Kanal. Link in der Bio.\n\n{PFLICHT}\n\n{HASH}"}
    json.dump(man, open(os.path.join(a.out, "manifest.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(man, ensure_ascii=False)); return 0


if __name__ == "__main__":
    sys.exit(main())
