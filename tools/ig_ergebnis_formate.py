#!/usr/bin/env python3
"""Beispiel-Formate Ergebnis-Beiträge (Instagram/TikTok/YouTube Short), 02.11.2026. Erfundene Daten, Regeln siehe ergebnis-beitraege-regeln.md.
Aufruf: python3 ig_ergebnis_formate.py <zielordner>   -> karussell_1-3.png, story.png, wettschein.png, reel_auswertung.mp4"""
import sys, os, json, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ig_spezial as s
import ig_ergebnis_beispiele_css as X
from playwright.sync_api import sync_playwright

ROWS = [("Heim FC – Gast SC","Über 1,5 Tore live","1,62",1),("Stadt United – Real Nord","Über 1,5 Tore live","1,58",0),
        ("FC Süd – Union West","Über 2,5 Tore live","1,66",1),("Rot-Weiß A – Blau-Weiß B","Über 1,5 Tore live","1,60",1),
        ("Sporting X – Athletic Y","Über 1,5 Tore live","1,64",0)]
def page(inner, tag=True, foot=True):
    top='<div class="top"><img src="LOGO"><span>Sportwetten Radar</span></div>'
    f='<div class="foot"><span>18+ · Keine Gewinngarantie</span><span>@sportwetten_radar</span></div>' if foot else ''
    return s.RINGS+top+('<div class="tag">BEISPIEL · ERFUNDENE DATEN</div>' if tag else '')+inner+f
def row(a,b,q,w):
    return f'<div class="row"><div class="t">{a}<small>{b} · Quote {q}</small></div><div class="{"ok" if w else "no"}">{"gewonnen" if w else "verloren"}</div></div>'

# Karussell
k1=page('<div class="eb">Auswertung · Spieltag 14.11.</div><div class="main"><h1 class="c">Alle Einträge von <em>gestern</em>.</h1><div class="hint">Nichts aussortiert. Wischen →</div></div>')
k2=page('<div class="eb">Auswertung · Spieltag 14.11.</div><div class="main t"><h1>Die Einträge im Überblick.</h1>'+"".join(row(*r) for r in ROWS)+'</div>')
k3=page('<div class="eb">So lesen</div><div class="main"><h1>Gewonnen und verloren stehen nebeneinander.</h1>'
 '<div class="p">Jeder Eintrag wird ausgewertet, auch die verlorenen. Nichts wird nachträglich geändert.</div>'
 '<div class="p">Ein einzelner Tag sagt wenig. Die komplette Auswertung steht im Ergebnis-Kanal, Link in der Bio.</div></div>')
# Wettschein-Karte (Ticket-Optik, ohne Einsatz/Gewinn)
ticket=("".join(f'<div class="tk"><div class="tkl"><b>{a}</b><small>{b}</small></div><div class="tkq">{q}</div><div class="{"ok" if w else "no"}">{"✓" if w else "✗"}</div></div>' for a,b,q,w in ROWS))
k4=page('<div class="eb">Wettschein-Ansicht · Spieltag 14.11.</div><div class="main t"><div class="ticket"><div class="tkh"><span>AUSWERTUNG</span><span>Quote</span><span></span></div>'+ticket+
 '<div class="perf"></div><div class="tkf">Alle Einträge, nichts aussortiert</div></div></div>')
# Story 1080x1920
st=page('<div class="eb" style="top:560px">Auswertung · Spieltag 14.11.</div><div class="main t" style="top:630px"><h1>Alle Einträge von gestern.</h1>'+"".join(row(*r) for r in ROWS)+
 '<div class="sub">Nichts aussortiert. Link zum Ergebnis-Kanal in der Bio.</div></div>')
css=s.CSS.replace("FONTS","file://"+os.path.join(s.HOME,"assets/fonts"))+X.EXTRA+X.EXTRA2
logo="file://"+os.path.join(s.HOME,"logo-icon.png")
out=sys.argv[1]; os.makedirs(out,exist_ok=True); tmp=tempfile.mkdtemp()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    for n,h,hh in [("karussell_1",k1,1350),("karussell_2",k2,1350),("karussell_3",k3,1350),("wettschein",k4,1350),("story",st,1920)]:
        pg=b.new_page(viewport={"width":1080,"height":hh})
        f=os.path.join(tmp,n+".html")
        open(f,"w").write(f'<html><head><meta charset="utf-8"><style>{css}html,body{{height:{hh}px!important}}</style></head><body>{h.replace("LOGO",logo)}</body></html>')
        pg.goto("file://"+f); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        print(n,pg.evaluate("Math.round(document.querySelector('.main').getBoundingClientRect().bottom)"),"/",hh-170)
        pg.screenshot(path=os.path.join(out,n+".png")); pg.close()
    b.close()

# Reel
import erklaervideo as E
E.HOCH=True; E.W,E.H=1080,1920
orig=E.folie_html
def fh(f,lg):
    if f["typ"]=="ende":
        return (f'<div class="top"><img src="{lg}"><span>Sportwetten <b>Radar</b></span></div>'
          '<div class="main end"><div class="eb">Sportwetten Radar</div><h1 class="k">Jeder Eintrag. <em>Jeden Tag.</em></h1>'
          '<div class="hint">Die komplette Auswertung im Ergebnis-Kanal, Link in der Bio · 18+ · Keine Gewinngarantie · Glücksspiel kann süchtig machen · check-dein-spiel.de</div></div>')
    return orig(f,lg).replace("<span>sportwetten-radar.net</span>","<span>@sportwetten_radar</span>")
E.folie_html=fh
def eint(r): return f"<b>{r[0]}</b> · Quote {r[2]} · {'gewonnen' if r[3] else 'verloren'}"
sp={"titel":"Auswertung Beispiel","folien":[
 {"typ":"hook","dauer":2.6,"text":"Alle Einträge\nvon [[gestern.]]"},
 {"typ":"liste","dauer":6,"eyebrow":"Auswertung · Spieltag 14.11.","text":"Teil 1","punkte":[eint(r) for r in ROWS[:3]]},
 {"typ":"liste","dauer":5,"eyebrow":"Auswertung · Spieltag 14.11.","text":"Teil 2","punkte":[eint(r) for r in ROWS[3:]]},
 {"typ":"text","dauer":4.5,"eyebrow":"Unsere Regel","text":"Nichts aussortiert.\nNichts nachträglich geändert.","sub":"Beispiel mit erfundenen Daten."},
 {"typ":"ende","dauer":4}]}
t2=tempfile.mkdtemp(); pngs=E.render(sp,s.HOME,t2); print("reel",E.baue(sp,pngs,os.path.join(out,"reel_auswertung.mp4")))
