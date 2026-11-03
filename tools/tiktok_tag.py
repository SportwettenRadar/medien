#!/usr/bin/env python3
"""TikTok 10:00: Tagesauswertung des Vortags NUR als Punkte (keine Teamnamen, keine Kreuze, keine Zahlen).
Entscheidung Daniel 03.11.2026 nach TikTok-Verweis (Fehlalarm "Belästigung und Mobbing" beim Tabellen-Reel).

  python3 tiktok_tag.py --medien <repo> --datum 2026-11-04 --out <ordner>

datum = heutiger Tag; gezeigt wird datum-1. Prüft Stand == datum und Live-/Einzel-Zahlen gegen daten/ergebnisse.json.
Ausgabe: <out>/reel.mp4 (1080x1920), manifest.json (status ok/stopp, texte.tiktok, texte.tiktok_titel). Exit 3 = stopp.
"""
import argparse, datetime as dt, json, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ig_spezial as s
import ig_tagesbeitraege as T
import tiktok_7tage as K

D = T.D; WK = T.WK; dm = T.dm


def kapseln(ergs, dot):
    if not ergs: return '<span class="none">keine Einträge</span>'
    pt = lambda e: f'<i class="{"w" if e == "gewonnen" else "l"}" style="width:{dot}px;height:{dot}px"></i>'
    zeilen = [ergs[i:i + 10] for i in range(0, len(ergs), 10)]
    return "".join('<div class="ln">' + "".join(f'<div class="gp">{"".join(pt(e) for e in z[i:i + 5])}</div>' for i in range(0, len(z), 5)) + '</div>' for z in zeilen)


def einzel(ergs):
    return '<div class="ez">' + "".join(f'<span><i class="{"w" if e == "gewonnen" else "l"}" style="width:84px;height:84px"></i></span>' for e in ergs) + '</div>' if ergs else '<span class="none">keine Einträge</span>'


def reel(d, live, ein, out):
    import erklaervideo as E
    E.HOCH = True; E.W, E.H = 1080, 1920
    orig = E.folie_html
    E.CSS_HOCH += """
.pn{margin-top:46px;background:#0f1d2c;border:2px solid #1b2c40;border-radius:28px;padding:34px 30px;display:flex;flex-direction:column;gap:14px}
.ln{display:flex;margin:10px 0}.gp{display:flex;gap:10px;background:#0b1623;border:2px solid #1f3248;border-radius:44px;padding:10px 14px;margin-right:18px}
.pn i{display:block;border-radius:50%;flex:none}.pn i.w{background:#2edb99}.pn i.l{background:#26364a;border:2px solid #3a4f68;box-sizing:border-box}
.ez{display:flex;background:#0b1623;border:2px solid #1f3248;border-radius:60px;padding:14px 0}.ez span{flex:1 1 0;display:flex;justify-content:center;max-width:20%}
.pn .none{font-size:30px;color:#6f8399}
.lg{display:flex;gap:34px;margin-top:30px;font-size:28px;color:#a9b8c8}.lg span{display:flex;align-items:center;gap:12px}
.lg i{width:28px;height:28px;border-radius:50%;display:block}.lg i.w{background:#2edb99}.lg i.l{background:#26364a;border:2px solid #3a4f68;box-sizing:border-box}
"""
    def fh(f, logo):
        top = f'<div class="top"><img src="{logo}"><span>Sportwetten <b>Radar</b></span></div>'
        if f["typ"] == "dots":
            leg = '<div class="lg"><span><i class="w"></i>gewonnen</span><span><i class="l"></i>verloren</span></div>'
            return (top + f'<div class="main"><div class="eb">{f["eyebrow"]}</div><div class="pn">{f["html"]}</div>{leg}</div>'
                    '<div class="foot"><span>18+ · Keine Gewinngarantie</span><span>@sportwetten.radar</span></div>')
        if f["typ"] == "ende":
            return (top + '<div class="main end"><div class="eb">Sportwetten Radar</div><h1 class="k">Jeder Eintrag. <em>Jeden Tag.</em></h1>'
                    '<div class="hint">18+ · Keine Gewinngarantie · Glücksspiel kann süchtig machen · check-dein-spiel.de</div></div>')
        return orig(f, logo).replace("<span>sportwetten-radar.net</span>", "<span>@sportwetten.radar</span>")
    E.folie_html = fh
    tag = f"{WK[d.weekday()]} {dm(d)}"
    lw = [x["ergebnis"] for x in live if x["ergebnis"] != "storniert"]
    ew = [x["ergebnis"] for x in ein if x["ergebnis"] != "storniert"]
    folien = [{"typ": "hook", "dauer": 2.4, "text": f"{tag}:\n[[Auswertung.]]"},
              {"typ": "dots", "dauer": 5.5, "eyebrow": f"Live · {tag}", "html": kapseln(lw, 70 if len(lw) <= 10 else 62 if len(lw) <= 20 else 52)},
              {"typ": "dots", "dauer": 4.5, "eyebrow": f"Einzelspiele · {tag}", "html": einzel(ew)},
              {"typ": "ende", "dauer": 3.0}]
    sp = {"titel": "Auswertung", "folien": folien}
    t2 = tempfile.mkdtemp(); pngs = E.render(sp, s.HOME, t2); return E.baue(sp, pngs, out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--medien", required=True); ap.add_argument("--datum", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    heute = D(a.datum); d = heute - dt.timedelta(days=1)
    sig, stand = T.lade(a.medien)
    erg = {t["datum"]: t for t in json.load(open(os.path.join(a.medien, "daten", "ergebnisse.json"), encoding="utf-8"))["tage"]}
    man = {"modus": "tiktok_tag", "datum": a.datum, "stand": stand, "status": "ok", "fehler": []}
    if stand[:10] != a.datum: man["fehler"].append(f"signale.json Stand {stand}, erwartet {a.datum}")
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
    if not (l or e): man["fehler"].append("keine Einträge am Vortag")
    if man["fehler"]:
        man["status"] = "stopp"; json.dump(man, open(os.path.join(a.out, "manifest.json"), "w"), ensure_ascii=False, indent=1)
        print(json.dumps(man, ensure_ascii=False)); return 3
    man["reel_sekunden"] = round(reel(d, l, e, os.path.join(a.out, "reel.mp4")), 1); man["reel"] = "reel.mp4"
    tg = f"{WK[d.weekday()]}, {dm(d)}"
    man["texte"] = {"tiktok": f"Auswertung vom {tg}: jeder Eintrag als Punkt. Link in der Bio. {T.PFLICHT} #Fußball #Statistik",
                    "tiktok_titel": f"Auswertung {WK[d.weekday()]} {dm(d)}"}
    json.dump(man, open(os.path.join(a.out, "manifest.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(man, ensure_ascii=False)); return 0


if __name__ == "__main__":
    sys.exit(main())
