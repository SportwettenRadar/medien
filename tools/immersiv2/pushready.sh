#!/bin/bash
cd /home/claude/medien
n=0
for f in immersiv/*.mp4; do
  [ $(( $(date +%s) - $(stat -c %Y "$f") )) -lt 90 ] && continue
  ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" >/dev/null 2>&1 || continue
  git add "$f"; n=$((n+1))
done
git add immersiv/hook tools
git diff --cached --quiet && { echo "nothing"; exit 0; }
git commit -qm "Immersiv-Videos: weitere Videos

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01U9SB1W9YKRGE7Am12d1CP1"
git push -q 2>&1 | grep -v "moved\|new location\|^remote: *$" ; git log --oneline | head -1; git ls-files immersiv | grep -c mp4
