#!/bin/bash
# Render every 60 s segment page (skips finished ones), then join them losslessly.
cd /home/claude/mm-work/ep01v3/engine
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_NO_UPDATE_CHECK=1 HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
mkdir -p ../renders
for f in $(ls ../proj/seg*.html | sort); do n=$(basename $f .html); out=../renders/$n.mp4
  [ -s $out ] && { echo "skip $n"; continue; }
  t0=$(date +%s); timeout 7000 npx hyperframes render ../proj -c $n.html -o $out.tmp.mp4 --quality looks --no-low-memory-mode --workers 2 --quiet > ../renders/$n.log 2>&1
  rc=$?; [ $rc -eq 0 ] && mv $out.tmp.mp4 $out; echo "$n rc=$rc $(( $(date +%s)-t0 ))s $(TZ=Asia/Kolkata date +%H:%M)"
done
ls ../renders/seg*.mp4 | grep -v tmp | sort | sed "s/^/file '/;s/$/'/" > ../renders/list.txt
ffmpeg -loglevel error -y -f concat -safe 0 -i ../renders/list.txt -c copy ../renders/video_silent.mp4 && echo JOINED
