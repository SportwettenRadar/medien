#!/bin/bash
cd /home/claude/medien/tools/immersiv2
python3 - <<'P' > work/names_v.txt
src=open('topics_all.py').read().split("if __name__")[0]
g={'__name__':'t'};exec(compile(src,'t','exec'),g)
print("\n".join(sorted(g['V'])))
P
cat work/names_v.txt | xargs -P 4 -I{} sh -c 'python3 topics_all.py video {} >> work/render2.log 2>&1'
echo "$(date +%H:%M) RENDER2 V-ENGINE FERTIG" >> work/state.txt
