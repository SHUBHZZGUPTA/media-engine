#!/bin/bash
# Render the full video in segments, stitch, mux the final mix. Usage: ./render.sh [first_seg]
set -e
cd /home/claude/mm-work/engine
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_NO_UPDATE_CHECK=1 HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
DUR=$(python3 -c "import json;print(json.load(open('build/timing.json'))['dur'])")
SEGS=$(python3 -c "
d=$DUR; s=[];a=0
while a<d: b=min(d,a+60); s.append([a,round(b,3)]); a=b
import json;print(json.dumps(s))")
python3 build.py proj "$SEGS" > /dev/null
N=$(python3 -c "import json;print(len(json.loads('$SEGS')))")
mkdir -p segs
for i in $(seq ${1:-0} $((N-1))); do f=$(printf "seg%02d" $i)
  [ -s segs/$f.mp4 ] && continue
  echo "$(date +%T) rendering $f"; timeout 1800 npx hyperframes render proj -c $f.html -o segs/$f.mp4 --quality looks --quiet > segs/$f.log 2>&1
done
(cd segs && ls seg*.mp4 | sort | sed "s/^/file '/;s/$/'/" > list.txt)
ffmpeg -v error -y -f concat -safe 0 -i segs/list.txt -c copy segs/video.mp4
ffmpeg -v error -y -i segs/video.mp4 -i build/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 -af "loudnorm=I=-14:TP=-1.5:LRA=11" -shortest final.mp4
echo "$(date +%T) done"; ffprobe -v error -show_entries format=duration -of csv=p=0 final.mp4
