import sys
sys.path.insert(0,"/home/claude/medien/tools")
import ig_spezial as s
from playwright.sync_api import sync_playwright
H="/home/claude/sportwetten-radar.net"
css=s.CSS.replace("FONTS","file://"+H+"/assets/fonts").replace("height:1350px","height:1080px")
dots="".join('<i class="%s"></i>'%("" if k<16 else "l") for k in range(20))
body=f'''<style>
svg.r{{display:none}}
.top{{top:60px}}.top img{{width:84px;height:84px;border-radius:20px}}.top span{{font-size:42px}}
.dt{{position:absolute;right:88px;top:84px;font-family:M;font-weight:500;font-size:26px;letter-spacing:.12em;color:#2edb99}}
.big{{position:absolute;left:88px;top:190px;font-family:B;font-weight:800;font-size:230px;line-height:1;color:#2edb99;white-space:nowrap}}
.big small{{font-size:70px;color:#eef3f8;margin-left:14px}}
.sub{{position:absolute;left:92px;top:450px;right:88px;font-size:36px;line-height:1.3;color:#a9b8c8}}
.sub b{{color:#eef3f8}}
.grid{{position:absolute;left:88px;right:88px;top:590px;display:grid;grid-template-columns:repeat(10,1fr);gap:16px}}
.grid i{{aspect-ratio:1;border-radius:50%;background:#2edb99}}.grid i.l{{background:#26364a;border:3px solid #3a4f68}}
.stats{{position:absolute;left:88px;right:88px;top:810px;display:flex;gap:20px}}
.stats div{{flex:1;background:#0f1d2c;border:2px solid #1b2c40;border-radius:26px;padding:20px 28px}}
.stats small{{display:block;font-family:M;font-size:22px;letter-spacing:.1em;color:#6f8399}}
.stats b{{font-family:B;font-weight:800;font-size:54px;color:#eef3f8}}
.foot{{position:absolute;left:88px;right:88px;bottom:40px;font-size:24px;color:#7f93a8}}
</style>
<div class="top"><img src="LOGO"><span>Sportwetten Radar</span></div><div class="dt">SO · 08.11.2026</div>
<div class="big">80 %<small>Trefferquote</small></div>
<div class="sub"><b>16 von 20</b> Live-Wetten getroffen. Alle Wetten des Tages, nichts aussortiert.</div>
<div class="grid">{dots}</div>
<div class="stats"><div><small>TREFFER</small><b>16 / 20</b></div><div><small>Ø-QUOTE</small><b>1,43</b></div></div>
<div class="foot">Einzelner Tag, kein Durchschnitt · 18+ · Keine Gewinngarantie</div>'''
html=f'<html><head><meta charset="utf-8"><style>{css}</style></head><body>{body.replace("LOGO","file://"+H+"/logo-icon.png")}</body></html>'
open("/tmp/ad.html","w").write(html)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium");pg=b.new_page(viewport={"width":1080,"height":1080})
    pg.goto("file:///tmp/ad.html");pg.evaluate("document.fonts.ready");pg.wait_for_timeout(400)
    pg.screenshot(path="mango_ergebniskanal_0811_1x1.png");b.close()
