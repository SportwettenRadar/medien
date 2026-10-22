#!/usr/bin/env python3
"""Setzt eine 2-Sekunden-Eröffnung (Hook, Zoom) vor einen bestehenden hochkant-Short.
Aufruf: python3 hook_vor_short.py --homepage <homepage> --short <alt.mp4> --text "<Hook, [[Akzent]]>" --out <neu.mp4>"""
import argparse, json, os, subprocess, tempfile, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
a = argparse.ArgumentParser()
for k in ("--homepage", "--short", "--text", "--out"):
    a.add_argument(k, required=True)
x = a.parse_args()
tmp = tempfile.mkdtemp()
spec = os.path.join(tmp, "s.json")
json.dump({"titel": "", "folien": [{"typ": "hook", "dauer": 2.4, "text": x.text.replace("\\n", "\n")}]}, open(spec, "w"), ensure_ascii=False)
hook = os.path.join(tmp, "hook.mp4")
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "erklaervideo.py"), "--hoch",
                "--spec", spec, "--homepage", x.homepage, "--out", hook], check=True, stdout=subprocess.DEVNULL)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", hook, "-i", x.short, "-filter_complex",
                "[0:v]fps=30,scale=1080:1920,setsar=1,format=yuv420p[a];[1:v]fps=30,scale=1080:1920,setsar=1,format=yuv420p[b];"
                "[a][b]xfade=transition=fade:duration=0.4:offset=1.6[v]",
                "-map", "[v]", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-movflags", "+faststart", x.out], check=True)
print("ok", x.out)
