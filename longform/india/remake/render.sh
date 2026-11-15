#!/bin/bash
# India remake render: compose with the 70% film-fade grade applied in the same encode (COMPOSE_VF), then mix and mux.
# One full-length video file at a time, so peak disk use stays near 1.5 GB.
set -e; cd "$(dirname "$0")"; ENG=../../engine; LUT=/home/claude/media-engine/bhugol-v2/grade/film-fade.cube
B=render/india_remake_en; df -h / | tail -1
COMPOSE_VF="split[a][b];[b]lut3d=$LUT[g];[a][g]blend=all_mode=normal:all_opacity=0.7,format=yuv420p" \
  python3 $ENG/compose.py voice/spec_en.json $B.graded.mp4; echo "compose+grade done $(date +%T)"; df -h / | tail -1
python3 $ENG/mixdown.py voice/spec_en.json voice/voice_en.wav voice/music_en.json $B.mix.wav; echo "mix done $(date +%T)"
ffmpeg -v error -y -i $B.graded.mp4 -i $B.mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $B.mp4
rm -f $B.graded.mp4; echo "RENDER DONE $(date +%T)"; ls -la $B.mp4; df -h / | tail -1
