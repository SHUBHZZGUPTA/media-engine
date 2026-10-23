#!/bin/bash
# build + render + mix + master every Short in shorts_v3.json (skips finished ones; safe to re-run)
source "$(dirname "$0")/env.sh"; mkdir -p "$EP/renders_short" "$EP/deliver/shorts"
for id in $(python3 -c "import json;print(' '.join(s['id'] for s in json.load(open('shorts_v3.json'))['shorts']))"); do n=${id:0:2}
  out="$EP/deliver/shorts/MoneyMirage_short_${id}.mp4"; [ -s "$out" ] && { echo "skip $id"; continue; }
  python3 "$TOOLS/build.py" --short=$id --out="$EP/proj_short/$n" > /dev/null 2>&1; t0=$(date +%s)
  (cd "$ENGD" && timeout 6000 npx hyperframes render "$EP/proj_short/$n" -o "$EP/renders_short/$id.mp4" --quality looks --no-low-memory-mode --workers 2 --quiet > "$EP/renders_short/$id.log" 2>&1) || { echo "$id render FAILED"; continue; }
  python3 "$TOOLS/mix_short.py" $id > /dev/null; A="$EP/audio/shorts/${id}_mix.wav"
  J=$(ffmpeg -hide_banner -i "$A" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
  g(){ echo "$J" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
  ffmpeg -loglevel error -y -i "$EP/renders_short/$id.mp4" -i "$A" -map 0:v -map 1:a -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" -c:a aac -b:a 256k -shortest -movflags +faststart "$out"
  echo "$id done $(( $(date +%s)-t0 ))s $(TZ=Asia/Kolkata date +%H:%M)"
done; echo ALLDONE
