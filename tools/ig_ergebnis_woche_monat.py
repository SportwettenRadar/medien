#!/usr/bin/env python3
"""Wochen- und Monatsauswertung (Beispiel, erfundene Daten): Punkte je Eintrag, keine Zahlen/Summen/Prozent/Kurve."""
import sys, os, tempfile, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ig_spezial as s
import ig_ergebnis_beispiele_css as X
from playwright.sync_api import sync_playwright
random.seed(5)
def dots(n,p=.63): return [random.random()<p for _ in range(n)]
EX="""
.tag{left:88px;right:auto;bottom:auto;top:228px}
.tb{position:absolute;left:88px;right:88px;top:360px}
.wr{display:flex;align-items:flex-start;background:#0f1d2c;border:2px solid #1b2c40;border-radius:20px;padding:16px 24px;margin-top:10px}
.wr b{font-family:B;font-weight:800;font-size:30px;width:150px;flex:none;line-height:34px}
.wr b small{display:block;font-family:M;font-weight:400;font-size:20px;color:#6f8399;line-height:22px}
.dt{display:flex;flex-wrap:wrap;gap:8px;flex:1;align-content:flex-start;min-height:34px}
.dt i{width:30px;height:30px;border-radius:50%;background:#2edb99}.dt i.l{background:#26364a;border:2px solid #3a4f68}
.m .dt i{width:24px;height:24px}.m .dt{gap:7px}.m .wr b{width:190px}
.leg{display:flex;gap:34px;margin-top:22px;font-size:26px;color:#a9b8c8;align-items:center}
.leg i{display:inline-block;width:26px;height:26px;border-radius:50%;background:#2edb99;margin-right:12px;vertical-align:-4px}.leg i.l{background:#26364a;border:2px solid #3a4f68}
.note{font-size:30px;line-height:1.4;color:#a9b8c8;margin-top:26px}
"""
LEG='<div class="leg"><span><i></i>gewonnen</span><span><i class="l"></i>verloren</span></div>'
def row(lab,sub,ds): return f'<div class="wr"><b>{lab}<small>{sub}</small></b><div class="dt">'+"".join(f'<i class="{"" if w else "l"}"></i>' for w in ds)+'</div></div>'
def page(eb,inner,cls=""):
    return (s.RINGS+'<div class="top"><img src="LOGO"><span>Sportwetten Radar</span></div><div class="tag">BEISPIEL · ERFUNDENE DATEN</div>'
      f'<div class="eb">{eb}</div><div class="tb {cls}">{inner}</div><div class="foot"><span>18+ · Keine Gewinngarantie</span><span>@sportwetten_radar</span></div>')
days=[("Mo","09.11.",3),("Di","10.11.",2),("Mi","11.11.",4),("Do","12.11.",3),("Fr","13.11.",5),("Sa","14.11.",26),("So","15.11.",9)]
w1=page("Woche 09.–15.11. · Live-Wetten","".join(row(d,dt,dots(n)) for d,dt,n in days)+LEG)
w2=page("Woche 09.–15.11. · Einzelspiele","".join(row(d,dt,dots(5)) for d,dt,n in days)+LEG+'<div class="note">Bis zu fünf ausgewählte Einzelspiele pro Tag.</div>')
w3=page("Wochenrückblick","<h1 style='font-family:B;font-weight:800;font-size:70px;line-height:1.05'>Gute und schwache Tage stehen nebeneinander.</h1>"
  '<div class="p">Jeder Eintrag der Woche wird ausgewertet, nichts wird nachträglich geändert. Die Einzelergebnisse aller Tage stehen im Ergebnis-Kanal, Link in der Bio.</div>')
wk=[("KW 41","05.–11.10.",41),("KW 42","12.–18.10.",38),("KW 43","19.–25.10.",55),("KW 44","26.10.–01.11.",47)]
m1=page("Monatsbericht · Oktober · Live-Wetten","".join(row(a,b,dots(n)) for a,b,n in wk)+LEG,"m")
m2=page("Monatsbericht · Oktober · Einzelspiele","".join(row(a,b,dots(25)) for a,b,n in wk)+LEG+'<div class="note">Bis zu fünf ausgewählte Einzelspiele pro Spieltag.</div>',"m")
m3=page("Monatsbericht · Oktober","<h1 style='font-family:B;font-weight:800;font-size:70px;line-height:1.05'>Ein Monat. Jeder Tag öffentlich.</h1>"
  '<div class="p">Alle Auswertungen des Monats stehen im Ergebnis-Kanal, die starken Tage wie die schwachen. Nichts wird nachträglich geändert oder gelöscht.</div>'
  '<div class="p">Ein einzelner Monat ist eine kleine Stichprobe und sagt wenig über den nächsten. Link in der Bio.</div>')
cards=[("woche_1_live",w1),("woche_2_einzelspiele",w2),("woche_3_hinweis",w3),("monat_1_live",m1),("monat_2_einzelspiele",m2),("monat_3_hinweis",m3)]
css=s.CSS.replace("FONTS","file://"+os.path.join(s.HOME,"assets/fonts"))+X.EXTRA+EX
logo="file://"+os.path.join(s.HOME,"logo-icon.png"); out=sys.argv[1]; os.makedirs(out,exist_ok=True); tmp=tempfile.mkdtemp()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    for n,h in cards:
        pg=b.new_page(viewport={"width":1080,"height":1350}); f=os.path.join(tmp,n+".html")
        open(f,"w").write(f'<html><head><meta charset="utf-8"><style>{css}</style></head><body>{h.replace("LOGO",logo)}</body></html>')
        pg.goto("file://"+f); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        print(n,pg.evaluate("Math.round(document.querySelector('.tb').getBoundingClientRect().bottom)"),"/ 1215")
        pg.screenshot(path=os.path.join(out,n+".png")); pg.close()
    b.close()
