#!/bin/bash
# Märket finish: teal-orange grade at 80% + mix muxed, x264 CRF 20 (< 100 MB). Frame 0 is already the cover (loop seam).
# Usage: finish.sh <silent.mp4> <mix_final.wav> <out.mp4>
set -e
SIL=$1; MIX=$2; OUT=$3; L=/home/claude/media-engine/bhugol-v2/grade/teal-orange-blockbuster.cube
ffmpeg -y -loglevel error -i "$SIL" -i "$MIX" -filter_complex "[0:v]split[a][b];[b]lut3d=file=$L[g];[a][g]blend=all_mode=normal:all_opacity=0.8,format=yuv420p[v]" \
  -map "[v]" -map 1:a -c:v libx264 -preset slow -crf 20 -profile:v high -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart "$OUT"
ls -la "$OUT"; ffprobe -v error -count_frames -show_entries stream=nb_read_frames:format=duration -of csv=p=0 "$OUT"
