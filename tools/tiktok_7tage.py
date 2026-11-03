#!/usr/bin/env python3
"""TikTok 18:00: "Die letzten 7 Tage: Auswertung" (Punkte je Eintrag, keine Zahlen). Entscheidung Daniel 03.11.2026.

  python3 tiktok_7tage.py --medien <repo> --datum 2026-11-04 --out <ordner>

datum = heutiger Tag; Fenster = die 7 Spieltage davor (datum-7 .. datum-1). Liest daten/signale.json,
prüft Stand == datum und je Tag Live-Wetten/Treffer und Einzeltipps/Treffer gegen daten/ergebnisse.json.
Ausgabe: <out>/reel.mp4 (1080x1920) und manifest.json (Texte, Status). Exit 0 = ok, 3 = Daten unvollständig/Abweichung.
Regeln wie tools/ergebnis-beitraege-regeln.md: keine Kennzahlen, keine Prozente, keine Summen, keine Beträge, Wort "Auswertung".
"""
import argparse, datetime as dt, json, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ig_spezial as s
import ig_tagesbeitraege as T

D = T.D; WK = T.WK; dm = T.dm


def punkte(ergs):
    if not ergs: return '<span class="none">keine Einträge</span>'
    return "".join(f'<i class="{"w" if e == "gewonnen" else "l"}"></i>' for e in ergs)


def reel(tage, out):
    import erklaervideo as E
    E.HOCH = True; E.W, E.H = 1080, 1920
    orig = E.folie_html
    E.CSS_HOCH += """
.dr{display:grid;gap:16px;margin-top:34px}.dd{display:flex;align-items:center;gap:24px;background:#0f1d2c;border:2px solid #1b2c40;border-radius:22px;padding:16px 24px;min-height:86px}
.dd b{font-family:M;font-weight:500;font-size:28px;color:#eef3f8;width:210px;flex:none;line-height:1.2}.dd b small{display:block;font-size:22px;color:#6f8399}
.dd .pt{display:flex;flex-wrap:wrap;gap:9px;flex:1}.dd i{width:30px;height:30px;border-radius:50%;display:block}
.dd i.w{background:#2edb99}.dd i.l{background:#26364a;border:2px solid #3a4f68;box-sizing:border-box}
.dd .none{font-size:24px;color:#6f8399}
.lg{display:flex;gap:34px;margin-top:26px;font-size:26px;color:#a9b8c8}.lg span{display:flex;align-items:center;gap:12px}
.lg i{width:26px;height:26px;border-radius:50%;display:block}.lg i.w{background:#2edb99}.lg i.l{background:#26364a;border:2px solid #3a4f68;box-sizing:border-box}
"""
    def fh(f, logo):
        top = f'<div class="top"><img src="{logo}"><span>Sportwetten <b>Radar</b></span></div>'
        if f["typ"] == "dots":
            r = "".join(f'<div class="dd"><b>{l}<small>{sb}</small></b><div class="pt">{punkte(ds)}</div></div>' for l, sb, ds in f["rows"])
            leg = '<div class="lg"><span><i class="w"></i>gewonnen</span><span><i class="l"></i>verloren</span></div>'
            return (top + f'<div class="main"><div class="eb">{f["eyebrow"]}</div><div class="dr">{r}</div>{leg}</div>'
                    '<div class="foot"><span>18+ · Keine Gewinngarantie</span><span>@sportwetten_radar</span></div>')
        if f["typ"] == "ende":
            return (top + '<div class="main end"><div class="eb">Sportwetten Radar</div><h1 class="k">Jeder Eintrag. <em>Jeden Tag.</em></h1>'
                    '<div class="hint">Alle Auswertungen öffentlich im Ergebnis-Kanal, Link in der Bio · 18+ · Keine Gewinngarantie · Glücksspiel kann süchtig machen · check-dein-spiel.de</div></div>')
        return orig(f, logo).replace("<span>sportwetten-radar.net</span>", "<span>@sportwetten_radar</span>")
    E.folie_html = fh
    live = [(f"{WK[d.weekday()]} {dm(d)}", "Live", [x["ergebnis"] for x in l if x["ergebnis"] != "storniert"]) for d, l, e in tage]
    ein = [(f"{WK[d.weekday()]} {dm(d)}", "Einzel", [x["ergebnis"] for x in e if x["ergebnis"] != "storniert"]) for d, l, e in tage]
    folien = [{"typ": "hook", "dauer": 2.6, "text": "Die letzten 7 Tage:\n[[Auswertung.]]"},
              {"typ": "dots", "dauer": 6.0, "eyebrow": "Live-Wetten · ein Punkt je Eintrag", "rows": live},
              {"typ": "dots", "dauer": 6.0, "eyebrow": "Einzelspiele · ein Punkt je Eintrag", "rows": ein},
              {"typ": "text", "dauer": 4.5, "eyebrow": "Unsere Regel", "text": "Gute und schwache Tage\nstehen nebeneinander."},
              {"typ": "ende", "dauer": 3.5}]
    sp = {"titel": "Auswertung", "folien": folien}
    t2 = tempfile.mkdtemp(); pngs = E.render(sp, s.HOME, t2); return E.baue(sp, pngs, out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--medien", required=True); ap.add_argument("--datum", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    heute = D(a.datum); bis = heute - dt.timedelta(days=1); von = bis - dt.timedelta(days=6)
    sig, stand = T.lade(a.medien)
    erg = {t["datum"]: t for t in json.load(open(os.path.join(a.medien, "daten", "ergebnisse.json"), encoding="utf-8"))["tage"]}
    man = {"modus": "7tage", "datum": a.datum, "stand": stand, "status": "ok", "fehler": []}
    if stand[:10] != a.datum: man["fehler"].append(f"signale.json Stand {stand}, erwartet {a.datum}")
    tage = []
    for i in range(7):
        d = von + dt.timedelta(days=i)
        l, e = T.eintraege(sig, d, d, "live"), T.eintraege(sig, d, d, "einzel")
        if any(x["ergebnis"] not in T.STATUS_OK for x in l + e): man["fehler"].append(f"{d}: Einträge ohne Ergebnis")
        ed = erg.get(d.isoformat())
        if l or e or ed:
            if not ed: man["fehler"].append(f"{d}: Tag fehlt in ergebnisse.json")
            else:
                lw = sum(1 for x in l if x["ergebnis"] != "storniert"); lt = sum(1 for x in l if x["ergebnis"] == "gewonnen")
                ew = sum(1 for x in e if x["ergebnis"] != "storniert"); et = sum(1 for x in e if x["ergebnis"] == "gewonnen")
                if (lw, lt) != (ed["live"]["wetten"], ed["live"]["treffer"]): man["fehler"].append(f"{d}: Live {lw}/{lt} statt {ed['live']['wetten']}/{ed['live']['treffer']}")
                if (ew, et) != (ed["einzelspiele"]["tipps"], ed["einzelspiele"]["treffer"]): man["fehler"].append(f"{d}: Einzel {ew}/{et} statt {ed['einzelspiele']['tipps']}/{ed['einzelspiele']['treffer']}")
        tage.append((d, l, e))
    if sum(len(l) + len(e) for _, l, e in tage) == 0: man["fehler"].append("keine Einträge im Fenster")
    if man["fehler"]:
        man["status"] = "stopp"; json.dump(man, open(os.path.join(a.out, "manifest.json"), "w"), ensure_ascii=False, indent=1)
        print(json.dumps(man, ensure_ascii=False)); return 3
    man["reel_sekunden"] = round(reel(tage, os.path.join(a.out, "reel.mp4")), 1); man["reel"] = "reel.mp4"
    zr = f"{dm(von)}–{dm(bis)}"
    man["texte"] = {
        "tiktok": f"Auswertung der letzten 7 Tage ({zr}): jeder Eintrag als Punkt, gewonnen wie verloren. Link in der Bio. {T.PFLICHT} #Fußball #Statistik",
        "tiktok_titel": f"Die letzten 7 Tage: Auswertung {zr}"}
    json.dump(man, open(os.path.join(a.out, "manifest.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(man, ensure_ascii=False)); return 0


if __name__ == "__main__":
    sys.exit(main())
