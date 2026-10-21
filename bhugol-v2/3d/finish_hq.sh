#!/bin/bash
# High-quality finish for the 3D look: thumbnail into frames 0-2, mix muxed in, x264 CRF 17 (no size cap).
# Usage: finish_hq.sh <silent.mp4> <mix_norm.wav> <thumb_v.jpg> <out.mp4>
# (Render first with: hyperframes render --crf 14 --no-browser-gpu --output silent.mp4 ; ~27 s of render per video second)
set -e
SIL=$1; MIX=$2; T=$3; OUT=$4; S=$(mktemp -d)
ffmpeg -y -loglevel error -loop 1 -framerate 30 -i "$T" -frames:v 3 -vf "scale=1080:1920,format=yuv420p" -c:v libx264 -crf 10 -r 30 $S/head.mp4
ffmpeg -y -loglevel error -i "$SIL" -vf "trim=start_frame=3,setpts=PTS-STARTPTS,format=yuv420p" -an -c:v libx264 -crf 10 -preset fast -r 30 $S/tail.mp4
printf "file '%s'\nfile '%s'\n" $S/head.mp4 $S/tail.mp4 > $S/list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i $S/list.txt -c copy $S/joined.mp4
ffmpeg -y -loglevel error -i $S/joined.mp4 -i "$MIX" -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -profile:v high -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart "$OUT"
rm -rf $S; ls -la "$OUT"; ffprobe -v error -show_entries format=duration,bit_rate -of csv=p=0 "$OUT"
