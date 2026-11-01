#!/bin/bash
set -e; cd /home/claude/pilot/out
ENG=/home/claude/media-engine/longform/engine; LUT=/home/claude/media-engine/bhugol-v2/grade/teal-orange-blockbuster.cube
t0=$(date +%s)
python3 -B $ENG/compose.py pilot_spec.json silent.mp4
ls $LUT >/dev/null 2>&1 || LUT=/home/claude/media-engine/bhugol-v2/grade/film-fade.cube
ffmpeg -v error -y -i silent.mp4 -filter_complex "[0:v]split[a][b];[b]lut3d=$LUT[g];[a][g]blend=all_mode=normal:all_opacity=0.5,format=yuv420p[v]" -map "[v]" -c:v libx264 -preset veryfast -crf 18 graded.mp4
python3 -B $ENG/mixdown.py mix_spec.json voice.wav music.json mix.wav
ffmpeg -v error -y -i graded.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart Mariana_pilot_90s.mp4
echo "DONE $(( $(date +%s) - t0 ))s"
