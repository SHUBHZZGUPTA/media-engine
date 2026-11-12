#!/bin/bash
# grade (teal-orange 80%) + thumbnail in frames 0-1 + mix -> out.mp4   usage: finish.sh <silent> <mix> <thumb> <out>
set -e; SIL=$1; MIX=$2; T=$3; OUT=$4; S=$(mktemp -d); LUT=/home/claude/media-engine/bhugol-v2/grade/teal-orange-blockbuster.cube
ffmpeg -y -loglevel error -i "$SIL" -filter_complex "[0:v]split[a][b];[b]lut3d=file=$LUT[g];[a][g]blend=all_mode=normal:all_opacity=0.8,format=yuv420p" -c:v libx264 -crf 12 -preset fast $S/graded.mp4
ffmpeg -y -loglevel error -loop 1 -framerate 30 -i "$T" -frames:v 2 -vf "scale=1080:1920,format=yuv420p" -c:v libx264 -crf 10 -r 30 $S/head.mp4
ffmpeg -y -loglevel error -i $S/graded.mp4 -vf "trim=start_frame=2,setpts=PTS-STARTPTS,format=yuv420p" -an -c:v libx264 -crf 10 -preset fast -r 30 $S/tail.mp4
printf "file '%s'\nfile '%s'\n" $S/head.mp4 $S/tail.mp4 > $S/list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i $S/list.txt -c copy $S/joined.mp4
ffmpeg -y -loglevel error -i $S/joined.mp4 -i "$MIX" -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -profile:v high -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart "$OUT"
rm -rf $S; ls -la "$OUT"; ffprobe -v error -show_entries format=duration,bit_rate -of csv=p=0 "$OUT"
