#!/bin/bash
# render_plate.sh name image.png '{json cfg incl. dur}'
set -e; cd "$(dirname "$0")"; N=$1; IMG=$2; CFG=$3
P=work/$N; rm -rf $P; mkdir -p $P/assets; cp gsap.min.js $P/; cp assets/pop.ttf $P/assets/; cp "$IMG" $P/assets/$(basename "$IMG"); ln -sf /home/claude/work3d/node_modules $P/node_modules
DUR=$(python3 -c "import json,sys;print(json.loads(sys.argv[1])['dur'])" "$CFG")
python3 - "$CFG" "$DUR" $P <<'P'
import sys; t=open('tpl.html').read().replace('__CFG__',sys.argv[1]).replace('__DUR__',sys.argv[2]); open(sys.argv[3]+'/index.html','w').write(t)
P
cd $P && HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_NO_UPDATE_CHECK=1 HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell npx --prefix /home/claude/work3d hyperframes render --crf 16 --no-browser-gpu --fps 30 --output /home/claude/pilot/shots/$N.mp4 > /home/claude/pilot/plate/work/$N.log 2>&1 && echo "$N ok"
