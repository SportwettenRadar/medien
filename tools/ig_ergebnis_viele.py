#!/usr/bin/env python3
"""Beispiel Samstag mit vielen Einträgen (24): Raster-Karte + kompakte Listenkarten (je 8) + Story-Raster. Erfundene Daten."""
import sys, os, tempfile, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ig_spezial as s
import ig_ergebnis_beispiele_css as X
from playwright.sync_api import sync_playwright
random.seed(11)
teams=["Heim FC","Gast SC","Stadt United","Real Nord","FC Süd","Union West","Rot-Weiß A","Blau-Weiß B","Sporting X","Athletic Y","Dynamo K","Borussia Z","City Ost","Racing W","Inter Q","Lokal R"]
mk=["Über 1,5","Über 2,5","Über 0,5","Über 3,5"]
R=[]
for i in range(24):
    a,b=random.sample(teams,2); R.append((f"{a} – {b}",random.choice(mk)+" Tore live",f"{random.uniform(1.5,1.9):.2f}".replace(".",","),random.random()<.62))
EX2="""
.grid{display:grid;grid-template-columns:repeat(6,1fr);gap:16px;margin-top:34px}
.grid i{font-style:normal;font-family:B;font-weight:800;font-size:34px;height:100px;border-radius:24px;display:flex;align-items:center;justify-content:center;background:#2edb99;color:#0a1620}
.grid i.l{background:#26364a;color:#c9d6e3;border:2px solid #3a4f68}
.leg{display:flex;gap:34px;margin-top:30px;font-size:28px;color:#a9b8c8}
.leg i{display:inline-block;width:26px;height:26px;border-radius:50%;background:#2edb99;margin-right:12px;vertical-align:-4px}.leg i.l{background:#26364a;border:2px solid #3a4f68}
.cr{display:flex;align-items:center;gap:18px;background:#0f1d2c;border:2px solid #1b2c40;border-radius:20px;padding:12px 22px;margin-top:10px}
.cr em{font-style:normal;font-family:M;font-size:24px;color:#6f8399;width:44px}
.cr div{flex:1;font-size:28px;color:#eef3f8;line-height:1.2}.cr small{display:block;font-size:22px;color:#8aa0b5}
.cr b{font-family:M;font-weight:500;font-size:26px;color:#eef3f8;width:70px;text-align:right}
.cr u{text-decoration:none;font-family:B;font-weight:800;font-size:24px;padding:6px 16px;border-radius:30px;background:#2edb99;color:#0a1620}
.cr u.l{background:#26364a;color:#c9d6e3;border:2px solid #3a4f68}
.main.g{top:380px}
"""
def page(inner,pg=None):
    return (s.RINGS+'<div class="top"><img src="LOGO"><span>Sportwetten Radar</span></div><div class="tag">BEISPIEL · ERFUNDENE DATEN</div>'+inner+
      '<div class="foot"><span>18+ · Keine Gewinngarantie</span><span>@sportwetten_radar</span></div>')
def raster(n=len(R)):
    return ('<div class="grid">'+"".join(f'<i class="{"" if r[3] else "l"}">{k+1}</i>' for k,r in enumerate(R))+'</div>'
            '<div class="leg"><span><i></i>gewonnen</span><span><i class="l"></i>verloren</span></div>')
def crow(k,r): return f'<div class="cr"><em>{k+1}</em><div>{r[0]}<small>{r[1]} · Quote {r[2]}</small></div><u class="{"" if r[3] else "l"}">{"gewonnen" if r[3] else "verloren"}</u></div>'
cards=[("raster",page('<div class="eb">Samstag 14.11. · 24 Einträge</div><div class="main g"><h1>Der Tag im Überblick.</h1>'+raster()+'<div class="sub">Jede Kachel ist ein Eintrag. Details →</div></div>'))]
for p in range(3):
    ch=R[p*8:(p+1)*8]
    cards.append((f"liste_{p+1}",page(f'<div class="eb">Einträge {p*8+1}–{p*8+len(ch)} von {len(R)}</div><div class="main g" style="top:350px">'+"".join(crow(p*8+i,r) for i,r in enumerate(ch))+'</div>')))
story=page('<div class="eb" style="top:420px">Auswertung · Samstag 14.11.</div><div class="main g" style="top:490px"><h1>Alle Einträge von gestern.</h1>'+raster()+'<div class="sub">Details im Beitrag und im Ergebnis-Kanal, Link in der Bio.</div></div>')
css=s.CSS.replace("FONTS","file://"+os.path.join(s.HOME,"assets/fonts"))+X.EXTRA+EX2
logo="file://"+os.path.join(s.HOME,"logo-icon.png")
out=sys.argv[1]; os.makedirs(out,exist_ok=True); tmp=tempfile.mkdtemp()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    for n,h,hh in [(n,h,1350) for n,h in cards]+[("story_samstag",story,1920)]:
        pg=b.new_page(viewport={"width":1080,"height":hh}); f=os.path.join(tmp,n+".html")
        open(f,"w").write(f'<html><head><meta charset="utf-8"><style>{css}html,body{{height:{hh}px!important}}</style></head><body>{h.replace("LOGO",logo)}</body></html>')
        pg.goto("file://"+f); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        print(n,pg.evaluate("Math.round(document.querySelector('.main').getBoundingClientRect().bottom)"),"/",hh-170)
        pg.screenshot(path=os.path.join(out,n+".png")); pg.close()
    b.close()
