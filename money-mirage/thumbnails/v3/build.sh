#!/bin/bash
# usage: ./build.sh [a b c]  — regenerate html, apply HyperFrames treatments, snapshot, export 1280x720 jpgs
set -e; cd "$(dirname "$0")"
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_NO_UPDATE_CHECK=1 HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
python3 make.py
for k in ${@:-a b c}; do
  while IFS=$'\t' read -r sel g || [ -n "$sel" ]; do [ -n "$sel" ] && npx hyperframes media-treatment --project v$k --selector "$sel" --grading "$g" --apply >/dev/null; done < v$k/treat.txt
  npx hyperframes snapshot v$k -o snap_$k --at 0.5 --no-end --describe false >/dev/null 2>&1
  python3 -c "from PIL import Image; Image.open('snap_$k/frame-00-at-0.5s.png').convert('RGB').resize((1280,720),Image.LANCZOS).save('MoneyMirage_ep01_thumb_$k.jpg',quality=93)"
  echo built $k
done
