#!/usr/bin/env python3
"""Erklärvideos 16:9 für YouTube (Sportwetten Radar).

Aufruf: python3 erklaervideo.py --spec videos/<name>.json --homepage <pfad homepage-repo> --out <ziel.mp4>
Spec: {"titel": ..., "folien": [{"typ": "titel|text|liste|ende", "dauer": s, ...}]}
Erzeugt Folien als PNG (Playwright, Schriften der Homepage), setzt sie mit Überblendung
und einer Fortschrittsleiste zu einem MP4 (1920x1080, 30 fps, ohne Ton) zusammen.
Zusätzlich: Vorschaubild 1280x720 (<out>_thumb.png).
"""
import argparse, json, os, subprocess, tempfile, html

W, H = 1920, 1080
FADE = 0.5

CSS = """
@font-face{font-family:B;font-weight:700;src:url('FONTS/baloo-2-latin-700-normal.woff2')}
@font-face{font-family:B;font-weight:800;src:url('FONTS/baloo-2-latin-800-normal.woff2')}
@font-face{font-family:I;font-weight:400;src:url('FONTS/inter-latin-400-normal.woff2')}
@font-face{font-family:I;font-weight:600;src:url('FONTS/inter-latin-600-normal.woff2')}
@font-face{font-family:M;font-weight:400;src:url('FONTS/ibm-plex-mono-latin-400-normal.woff2')}
@font-face{font-family:M;font-weight:500;src:url('FONTS/ibm-plex-mono-latin-500-normal.woff2')}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:WPXpx;height:HPXpx;background:#0a131d;color:#eef3f8;overflow:hidden}
body{position:relative;font-family:I;
 background:radial-gradient(1100px 700px at 85% 10%,rgba(46,219,153,.10),transparent 60%),
            radial-gradient(900px 600px at 0% 100%,rgba(77,163,255,.08),transparent 60%),#0a131d}
.top{position:absolute;left:120px;top:80px;display:flex;align-items:center;gap:20px}
.top img{width:64px;height:64px;border-radius:14px}
.top span{font-family:B;font-weight:700;font-size:36px}
.top span b{color:#2edb99;font-weight:700}
.foot{position:absolute;left:120px;right:120px;bottom:70px;display:flex;justify-content:space-between;
 font-family:M;font-size:26px;color:#6f8399}
.main{position:absolute;left:120px;right:120px;top:50%;transform:translateY(-46%)}
.eb{font-family:M;font-weight:500;font-size:30px;letter-spacing:.14em;color:#2edb99;text-transform:uppercase;margin-bottom:28px}
h1{font-family:B;font-weight:800;font-size:104px;line-height:1.02;letter-spacing:-.01em}
h1.k{font-size:84px;line-height:1.08}
h1 em{font-style:normal;background:linear-gradient(90deg,#4da3ff,#2edb99);-webkit-background-clip:text;background-clip:text;color:transparent}
.bar{width:150px;height:8px;background:#2edb99;border-radius:4px;margin:40px 0 0}
.sub{font-size:40px;line-height:1.45;color:#a9b8c8;margin-top:36px;max-width:1500px}
ul{list-style:none;margin-top:44px;display:grid;gap:26px}
li{display:flex;gap:28px;align-items:flex-start;font-size:42px;line-height:1.35;color:#d6e0ea}
li i{flex:none;font-style:normal;font-family:M;font-weight:500;font-size:30px;color:#0a131d;background:#2edb99;
 width:54px;height:54px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin-top:2px}
li b{color:#fff;font-weight:600}
.end .rows{margin-top:46px;display:grid;gap:22px}
.end .row{display:flex;gap:30px;align-items:baseline;font-size:42px}
.end .row span{font-family:M;font-size:28px;color:#6f8399;width:290px;flex:none;text-transform:uppercase;letter-spacing:.08em}
.end .row b{font-weight:600;color:#fff}
.end .hint{margin-top:48px;font-family:M;font-size:26px;color:#8a9bb0}
"""


def esc(s):
    return html.escape(s).replace("[[", "<em>").replace("]]", "</em>").replace("**", "")


def folie_html(f, logo):
    top = f'<div class="top"><img src="{logo}"><span>Sportwetten <b>Radar</b></span></div>'
    foot = '<div class="foot"><span>18+ · Keine Gewinngarantie</span><span>sportwetten-radar.net</span></div>'
    t = f["typ"]
    if t == "titel":
        body = (f'<div class="main"><div class="eb">{esc(f.get("eyebrow",""))}</div>'
                f'<h1>{esc(f["text"]).replace(chr(10),"<br>")}</h1><div class="bar"></div></div>')
    elif t == "text":
        body = (f'<div class="main"><div class="eb">{esc(f.get("eyebrow",""))}</div>'
                f'<h1 class="k">{esc(f["text"]).replace(chr(10),"<br>")}</h1>'
                + (f'<div class="sub">{esc(f["sub"])}</div>' if f.get("sub") else "") + '</div>')
    elif t == "liste":
        items = "".join(
            f'<li><i>{i+1}</i><div>{esc(x).replace("&lt;b&gt;","<b>").replace("&lt;/b&gt;","</b>")}</div></li>'
            for i, x in enumerate(f["punkte"]))
        body = (f'<div class="main"><div class="eb">{esc(f.get("eyebrow",""))}</div>'
                f'<h1 class="k">{esc(f["text"])}</h1><ul>{items}</ul></div>')
    elif t == "ende":
        body = ('<div class="main end"><div class="eb">Sportwetten Radar</div>'
                '<h1 class="k">Start am <em>8. Januar 2027</em>.</h1><div class="rows">'
                '<div class="row"><span>Warteliste</span><b>Telegram-Bot @KILivewetten_bot</b></div>'
                '<div class="row"><span>Ergebnisse</span><b>t.me/sportwettenradar</b></div>'
                '<div class="row"><span>Trackrecord</span><b>sportwetten-radar.net</b></div></div>'
                '<div class="hint">Links in der Beschreibung · 18+ · Glücksspiel kann süchtig machen · check-dein-spiel.de</div></div>')
        foot = ""
    else:
        raise ValueError(t)
    return top + body + foot


def render(spec, homepage, tmp):
    from playwright.sync_api import sync_playwright
    fonts = "file://" + os.path.abspath(os.path.join(homepage, "assets/fonts"))
    logo = "file://" + os.path.abspath(os.path.join(homepage, "logo-icon.png"))
    css = CSS.replace("FONTS", fonts).replace("WPX", str(W)).replace("HPX", str(H))
    pngs = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        pg = b.new_page(viewport={"width": W, "height": H})
        for n, f in enumerate(spec["folien"]):
            hp = os.path.join(tmp, f"f{n:02d}.html")
            open(hp, "w", encoding="utf-8").write(f"<html><head><meta charset=utf-8><style>{css}</style></head><body>{folie_html(f, logo)}</body></html>")
            pg.goto("file://" + hp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
            ub = pg.evaluate("(()=>{const m=document.querySelector('.main');const r=m.getBoundingClientRect();return [Math.round(r.top),Math.round(r.bottom),m.scrollWidth>m.clientWidth+2]})()")
            if ub[0] < 170 or ub[1] > 990 or ub[2]:
                print(f"WARNUNG Folie {n}: Platz {ub}")
            path = os.path.join(tmp, f"f{n:02d}.png")
            pg.screenshot(path=path)
            pngs.append(path)
        b.close()
    return pngs


def baue(spec, pngs, out):
    d = [float(f["dauer"]) for f in spec["folien"]]
    total = sum(d) - FADE * (len(d) - 1)
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for p, du in zip(pngs, d):
        cmd += ["-loop", "1", "-t", str(du), "-framerate", "30", "-i", p]
    fl, last, off = [], "[0:v]", 0.0
    for i in range(1, len(pngs)):
        off += d[i - 1] - FADE
        fl.append(f"{last}[{i}:v]xfade=transition=fade:duration={FADE}:offset={off:.3f}[x{i}]")
        last = f"[x{i}]"
    fl.append(f"{last}drawbox=x=0:y=ih-10:w=iw:h=10:color=0x16263a:t=fill[bg]")
    fl.append(f"color=c=0x2edb99:s={W}x10:r=30:d={total:.3f}[pb]")
    fl.append(f"[bg][pb]overlay=x='-w+w*t/{total:.3f}':y=H-10:shortest=1,format=yuv420p[v]")
    cmd += ["-filter_complex", ";".join(fl), "-map", "[v]", "-r", "30", "-c:v", "libx264",
            "-preset", "slow", "-crf", "20", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    return total


def thumb(spec, homepage, out):
    from playwright.sync_api import sync_playwright
    fonts = "file://" + os.path.abspath(os.path.join(homepage, "assets/fonts"))
    logo = "file://" + os.path.abspath(os.path.join(homepage, "logo-icon.png"))
    css = CSS.replace("FONTS", fonts).replace("WPX", str(W)).replace("HPX", str(H))
    t = spec.get("thumb", {"eyebrow": spec["folien"][0].get("eyebrow", ""), "text": spec["folien"][0]["text"]})
    f = {"typ": "titel", **t}
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1280 / W)
        hp = tempfile.mktemp(suffix=".html")
        open(hp, "w", encoding="utf-8").write(f"<html><head><meta charset=utf-8><style>{css} h1{{font-size:128px}}</style></head><body>{folie_html(f, logo)}</body></html>")
        pg.goto("file://" + hp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        pg.screenshot(path=out)
        b.close()


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--spec", required=True)
    a.add_argument("--homepage", required=True)
    a.add_argument("--out", required=True)
    a.add_argument("--nur-folien", action="store_true")
    x = a.parse_args()
    spec = json.load(open(x.spec, encoding="utf-8"))
    tmp = tempfile.mkdtemp()
    pngs = render(spec, x.homepage, tmp)
    if x.nur_folien:
        print("\n".join(pngs))
    else:
        dauer = baue(spec, pngs, x.out)
        thumb(spec, x.homepage, x.out.rsplit(".", 1)[0] + "_thumb.png")
        print(f"ok {x.out} {dauer:.1f}s")
