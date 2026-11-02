#!/usr/bin/env python3
"""Tabellen-Layout (Entscheidung Daniel 02.11.): Nr, Spiel, Markt, Quote, Haken (grün) / Kreuz (grau). 12 Zeilen je Karte. Einzelspiele als eigene Zusatzkarte im selben Karussell. Erfundene Daten."""
import sys, os, tempfile, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ig_spezial as s
import ig_ergebnis_beispiele_css as X
from playwright.sync_api import sync_playwright
random.seed(11)
teams=["Heim FC","Gast SC","Stadt United","Real Nord","FC Süd","Union West","Rot-Weiß A","Blau-Weiß B","Sporting X","Athletic Y","Dynamo K","Borussia Z","City Ost","Racing W","Inter Q","Lokal R"]
def gen(n,mk):
    out=[]
    for i in range(n):
        a,b=random.sample(teams,2); out.append((f"{a} – {b}",random.choice(mk),f"{random.uniform(1.3,1.9):.2f}".replace(".",","),random.random()<.62))
    return out
LIVE=gen(24,["Ü 1,5","Ü 2,5","Ü 0,5","Ü 3,5"]); EINZ=gen(5,["Ü 1,5","1X","X2","Ü 2,5"])
EX="""
.tag{left:88px;right:auto;bottom:auto;top:228px}
.tb{position:absolute;left:88px;right:88px;top:352px}
.th{display:flex;font-family:M;font-size:21px;letter-spacing:.14em;color:#6f8399;padding:0 22px 8px}
.th span:nth-child(1){width:52px}.th span:nth-child(2){flex:1}.th span:nth-child(3){width:110px}.th span:nth-child(4){width:100px;text-align:right}.th span:nth-child(5){width:70px}
.tr{display:flex;align-items:center;height:56px;margin-top:5px;background:#0f1d2c;border:2px solid #1b2c40;border-radius:16px;padding:0 22px;font-size:27px;color:#eef3f8}
.tr em{font-style:normal;font-family:M;font-size:22px;color:#6f8399;width:52px}
.tr div{flex:1;white-space:nowrap;overflow:hidden}
.tr span{font-family:M;font-size:24px;color:#a9b8c8;width:110px}
.tr b{font-family:M;font-weight:500;font-size:26px;width:100px;text-align:right}
.tr u{text-decoration:none;width:44px;height:44px;margin-left:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:B;font-weight:800;font-size:28px}
.tr u.w{background:#2edb99;color:#0a1620}.tr u.l{background:#26364a;color:#c9d6e3;border:2px solid #3a4f68}
.tr.e{height:84px}.tr.e div{font-size:30px}
.leg{display:flex;gap:34px;margin-top:20px;font-size:25px;color:#a9b8c8;align-items:center}
.leg u{display:inline-flex;width:30px;height:30px;border-radius:50%;text-decoration:none;align-items:center;justify-content:center;font-size:19px;font-weight:800;margin-right:10px;background:#2edb99;color:#0a1620}.leg u.l{background:#26364a;color:#c9d6e3;border:2px solid #3a4f68}
.note{font-size:30px;line-height:1.4;color:#a9b8c8;margin-top:30px}
"""
def rows(rs,k0=0,cls=""):
    return "".join(f'<div class="tr {cls}"><em>{k0+i+1}</em><div>{r[0]}</div><span>{r[1]}</span><b>{r[2]}</b><u class="{"w" if r[3] else "l"}">{"✓" if r[3] else "✕"}</u></div>' for i,r in enumerate(rs))
HEAD='<div class="th"><span>NR.</span><span>SPIEL</span><span>MARKT</span><span>QUOTE</span><span></span></div>'
LEG='<div class="leg"><span><u>✓</u>gewonnen</span><span><u class="l">✕</u>verloren</span></div>'
def page(eb,inner):
    return (s.RINGS+'<div class="top"><img src="LOGO"><span>Sportwetten Radar</span></div><div class="tag">BEISPIEL · ERFUNDENE DATEN</div>'
      f'<div class="eb">{eb}</div>'+inner+'<div class="foot"><span>18+ · Keine Gewinngarantie</span><span>@sportwetten_radar</span></div>')
cards=[("tabelle_live_1",page("Live-Wetten · Samstag 14.11. · 1–12",'<div class="tb">'+HEAD+rows(LIVE[:12])+LEG+'</div>')),
       ("tabelle_live_2",page("Live-Wetten · Samstag 14.11. · 13–24",'<div class="tb">'+HEAD+rows(LIVE[12:],12)+LEG+'</div>')),
       ("tabelle_einzelspiele",page("Einzelspiele · Samstag 14.11.",'<div class="tb">'+HEAD+rows(EINZ,0,"e")+LEG+
        '<div class="note">Bis zu fünf ausgewählte Einzelspiele vor Anpfiff. Ob einzeln oder selbst kombiniert, entscheidet jeder selbst.</div></div>'))]
css=s.CSS.replace("FONTS","file://"+os.path.join(s.HOME,"assets/fonts"))+X.EXTRA+EX
logo="file://"+os.path.join(s.HOME,"logo-icon.png")
out=sys.argv[1]; os.makedirs(out,exist_ok=True); tmp=tempfile.mkdtemp()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    for n,h in cards:
        pg=b.new_page(viewport={"width":1080,"height":1350}); f=os.path.join(tmp,n+".html")
        open(f,"w").write(f'<html><head><meta charset="utf-8"><style>{css}</style></head><body>{h.replace("LOGO",logo)}</body></html>')
        pg.goto("file://"+f); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        print(n,pg.evaluate("Math.round(document.querySelector('.tb').getBoundingClientRect().bottom)"),"/ 1215")
        pg.screenshot(path=os.path.join(out,n+".png")); pg.close()
    b.close()
