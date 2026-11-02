import sys, os, tempfile
sys.path.insert(0,"/home/claude/medien/tools")
import ig_spezial as s
from playwright.sync_api import sync_playwright
EXTRA = """
.tag{position:absolute;left:88px;bottom:150px;font-family:M;font-size:24px;color:#0a1620;background:#f2c14e;padding:8px 18px;border-radius:12px;letter-spacing:.08em}
.row{display:flex;align-items:center;justify-content:space-between;background:#0f1d2c;border:2px solid #1b2c40;border-radius:26px;padding:22px 32px;margin-top:18px}
.row .t{font-size:33px;line-height:1.25;color:#eef3f8}.row .t small{display:block;font-size:26px;color:#8aa0b5;margin-top:4px}
.ok,.no{flex:none;font-family:B;font-weight:800;font-size:30px;padding:10px 24px;border-radius:40px;margin-left:20px}
.ok{background:#2edb99;color:#0a1620}.no{background:#26364a;color:#c9d6e3;border:2px solid #3a4f68}
.d{display:flex;align-items:center;justify-content:space-between;margin-top:18px;background:#0f1d2c;border:2px solid #1b2c40;border-radius:26px;padding:20px 32px}
.d b{font-family:B;font-weight:800;font-size:36px;width:90px}
.dots{display:flex;gap:12px;flex-wrap:wrap;justify-content:flex-end;flex:1}
.dots i{width:34px;height:34px;border-radius:50%;background:#2edb99}.dots i.l{background:#26364a;border:2px solid #3a4f68}
.main.t h1{font-size:60px}.main.t .row{padding:14px 28px;margin-top:12px;border-radius:22px}.main.t .row .t{font-size:30px}.main.t .row .t small{font-size:24px}.main.t .ok,.main.t .no{font-size:27px;padding:8px 20px}.main.t .d{padding:12px 26px;margin-top:11px;border-radius:22px}.main.t .d b{font-size:32px}.main.t .dots i{width:28px;height:28px}.main.t .sub{font-size:30px;margin-top:18px}.main.t .leg{margin-top:18px}
.leg{display:flex;gap:34px;margin-top:26px;font-size:28px;color:#a9b8c8;align-items:center}
.leg i{display:inline-block;width:26px;height:26px;border-radius:50%;background:#2edb99;margin-right:12px;vertical-align:-4px}.leg i.l{background:#26364a;border:2px solid #3a4f68}
"""
def page(inner):
    top='<div class="top"><img src="LOGO"><span>Sportwetten Radar</span></div>'
    foot='<div class="foot"><span>18+ · Keine Gewinngarantie</span><span>@sportwetten_radar</span></div>'
    return s.RINGS+top+'<div class="tag">BEISPIEL · ERFUNDENE DATEN</div>'+inner+foot
rows=[("Heim FC – Gast SC","Über 1,5 Tore live · Quote 1,62",1),("Stadt United – Real Nord","Über 1,5 Tore live · Quote 1,58",0),
      ("FC Süd – Union West","Über 2,5 Tore live · Quote 1,66",1),("Rot-Weiß A – Blau-Weiß B","Über 1,5 Tore live · Quote 1,60",1),
      ("Sporting X – Athletic Y","Über 1,5 Tore live · Quote 1,64",0)]
p1=page('<div class="eb">Auswertung · Spieltag 14.11.</div><div class="main t"><h1>Alle Einträge von gestern.</h1>'+
 "".join(f'<div class="row"><div class="t">{a}<small>{b}</small></div><div class="{"ok" if w else "no"}">{"gewonnen" if w else "verloren"}</div></div>' for a,b,w in rows)+
 '<div class="sub">Nichts aussortiert. Gewonnene und verlorene gleichberechtigt.</div></div>')
days=[("Mo",[1,1,0]),("Di",[0,1]),("Mi",[1,1,1,0]),("Do",[0,0,1]),("Fr",[1,0,1,1]),("Sa",[0,1,1,1,0,1]),("So",[1,0,0])]
p2=page('<div class="eb">Wochenrückblick · 09.–15.11.</div><div class="main t"><h1>Jeder Punkt ist ein Eintrag.</h1>'+
 "".join(f'<div class="d"><b>{d}</b><div class="dots">'+"".join(f'<i class="{"" if w else "l"}"></i>' for w in v)+'</div></div>' for d,v in days)+
 '<div class="leg"><span><i></i>gewonnen</span><span><i class="l"></i>verloren</span></div>'
 '<div class="sub">Gute und schwache Tage stehen nebeneinander.</div></div>')
p3=page('<div class="eb">Monatsbericht · Oktober</div><div class="main"><h1>Ein Monat. Jeder Tag öffentlich.</h1>'
 '<div class="p">Alle Auswertungen des Monats stehen im Ergebnis-Kanal auf Telegram, die starken Tage wie die schwachen. Nichts wird nachträglich geändert oder gelöscht.</div>'
 '<div class="p">Ein einzelner Monat ist eine kleine Stichprobe und sagt wenig über den nächsten.</div>'
 '<div class="hint">Link zum Kanal in der Bio</div></div>')

import random
random.seed(7)
v=[0];
for i in range(44): v.append(v[-1]+random.choice([-1.4,-0.8,-0.3,0.5,0.9,1.3,0.6,-0.5]))
lo,hi=min(v+[0])-1.5,max(v+[0])+1.5
W,H=904,560
def X(i): return 28+i*(W-56)/(len(v)-1)
def Y(x): return H-(x-lo)/(hi-lo)*H
pts=" ".join(f"{X(i):.1f},{Y(x):.1f}" for i,x in enumerate(v))
area=f"{X(0):.1f},{Y(0):.1f} "+pts+f" {X(len(v)-1):.1f},{Y(0):.1f}"
svg=(f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="margin-top:34px">'
 f'<line x1="0" y1="{Y(0):.1f}" x2="{W}" y2="{Y(0):.1f}" stroke="#f2c14e" stroke-width="3" stroke-dasharray="12 10"/>'
 f'<polyline points="{pts}" fill="none" stroke="#2edb99" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/>'
 f'<circle cx="{X(len(v)-1):.1f}" cy="{Y(v[-1]):.1f}" r="11" fill="#2edb99"/>'
 f'<text x="{W-6}" y="{Y(0)-14:.1f}" text-anchor="end" font-family="I" font-size="28" fill="#f2c14e">0 Einsätze</text></svg>')
p4=page('<div class="eb">Gesamtverlauf · seit 01.09.</div><div class="main"><h1>Auf und ab, fortlaufend.</h1>'+svg+
 '<div class="sub">Die Linie zeigt den Verlauf in Einsätzen. Die gestrichelte Linie ist null.</div></div>')
out=sys.argv[1]; os.makedirs(out,exist_ok=True)
css=s.CSS.replace("FONTS","file://"+os.path.join(s.HOME,"assets/fonts"))+EXTRA
logo="file://"+os.path.join(s.HOME,"logo-icon.png")
tmp=tempfile.mkdtemp()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium"); pg=b.new_page(viewport={"width":1080,"height":1350})
    for n,h in [("bsp_tagesauswertung",p1),("bsp_woche",p2),("bsp_monat",p3),("bsp_verlauf",p4)]:
        f=os.path.join(tmp,n+".html"); open(f,"w").write(f'<html><head><meta charset="utf-8"><style>{css}</style></head><body>{h.replace("LOGO",logo)}</body></html>')
        pg.goto("file://"+f); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        print(n,pg.evaluate("Math.round(document.querySelector('.main').getBoundingClientRect().bottom)"))
        pg.screenshot(path=os.path.join(out,n+".png"))
    b.close()
