#!/bin/bash
# Render every 60 s segment page of the long-form (skips finished ones; safe to re-run after a stop), then join losslessly.
source "$(dirname "$0")/env.sh"; mkdir -p "$EP/renders"
for f in $(ls "$EP"/proj/seg*.html | sort); do n=$(basename $f .html); out="$EP/renders/$n.mp4"
  [ -s "$out" ] && { echo "skip $n"; continue; }
  t0=$(date +%s); (cd "$ENGD" && timeout 7000 npx hyperframes render "$EP/proj" -c $n.html -o "$out.tmp.mp4" --quality looks --no-low-memory-mode --workers 2 --quiet > "$EP/renders/$n.log" 2>&1)
  rc=$?; [ $rc -eq 0 ] && mv "$out.tmp.mp4" "$out"; echo "$n rc=$rc $(( $(date +%s)-t0 ))s $(TZ=Asia/Kolkata date +%H:%M)"
done
ls "$EP"/renders/seg*.mp4 | grep -v tmp | sort | sed "s/^/file '/;s/$/'/" > "$EP/renders/list.txt"
ffmpeg -loglevel error -y -f concat -safe 0 -i "$EP/renders/list.txt" -c copy "$EP/renders/video_silent.mp4" && echo JOINED
