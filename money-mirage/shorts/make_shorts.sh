#!/bin/bash
# Cut 9:16 Shorts from the final 16:9 video: blurred fill + centred video + title overlay.
set -e; cd /home/claude/mm-work/shorts; SRC=/home/claude/mm-work/MoneyMirage_ep01_FINAL.mp4
python3 -c "import json;[print(s['id'],s['a'],s['b']) for s in json.load(open('shorts.json'))]" | while read id a b; do
  d=$(python3 -c "print(round($b-$a,3))")
  ffmpeg -v error -y -ss $a -t $d -i $SRC -i ov_$id.png -filter_complex "[0:v]split[a][b];[a]scale=-2:1920,crop=1080:1920,boxblur=28:2,eq=brightness=-0.28[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=0:656[v1];[v1][1:v]overlay=0:0,fade=t=in:st=0:d=0.25,fade=t=out:st=$(python3 -c "print(round($d-0.4,3))"):d=0.4[v]" -map "[v]" -map 0:a -c:v libx264 -crf 18 -preset medium -c:a aac -b:a 160k -af "afade=t=in:d=0.2,afade=t=out:st=$(python3 -c "print(round($d-0.5,3))"):d=0.5" -movflags +faststart MoneyMirage_short_$id.mp4 < /dev/null
  echo "$id $d s"
done
