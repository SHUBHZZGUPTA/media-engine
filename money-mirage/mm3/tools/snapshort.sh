#!/bin/bash
# snapshort.sh <short id> [...] — build each Short page and snapshot 12 frames (hook, body, outro) into review/sh_<nn>/sheet.jpg
source "$(dirname "$0")/env.sh"
for id in "$@"; do n=${id:0:2}
  python3 "$TOOLS/build.py" --short=$id --out="$EP/proj_short/$n" > /dev/null 2>&1
  TS=$(python3 -c "
import json;s=[x for x in json.load(open('shorts_v3.json'))['shorts'] if x['id']=='$id'][0];D=s['dur'];H=s['hook']['dur'];O=D-s['outro']['dur']
print(','.join(str(round(t,2)) for t in [1.2,H-.6]+[H+(O-H)*k/9 for k in range(1,9)]+[O+2.5,D-.4]))")
  rm -rf "$EP/review/sh_$n"; (cd "$ENGD" && timeout 1700 npx hyperframes snapshot "$EP/proj_short/$n" -o "$EP/review/sh_$n" --at $TS --no-end --describe false --timeout 300000 > /dev/null 2>&1)
  python3 "$TOOLS/sheet.py" "$EP/review/sh_$n" "$TS" 6 240 427; echo "$id done"
done
