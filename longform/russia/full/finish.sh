#!/bin/bash
# compose -> 70% film-fade grade -> mix -> mux.   Usage: finish.sh spec.json voice.wav music.json out.mp4
set -e
SPEC=$1; VOICE=$2; MUSIC=$3; OUT=$4
ENG=/home/claude/media-engine/longform/engine; LUT=/home/claude/media-engine/bhugol-v2/grade/film-fade.cube
B=${OUT%.mp4}
python3 $ENG/compose.py "$SPEC" "$B.silent.mp4"
ffmpeg -v error -y -i "$B.silent.mp4" -filter_complex "[0:v]split[a][b];[b]lut3d=$LUT[g];[a][g]blend=all_mode=normal:all_opacity=0.7,format=yuv420p[v]" \
  -map "[v]" -c:v libx264 -preset veryfast -crf 18 "$B.graded.mp4"
python3 $ENG/mixdown.py "$SPEC" "$VOICE" "$MUSIC" "$B.mix.wav"
ffmpeg -v error -y -i "$B.graded.mp4" -i "$B.mix.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
echo "DONE $OUT"
