#!/bin/bash
# India remake render: same steps as ../finish.sh (compose -> 70% film-fade grade -> mix -> mux), deleting each
# intermediate as soon as the next step has it, so the peak disk use stays near 3.5 GB.
set -e; cd "$(dirname "$0")"; ENG=../../engine; LUT=$(grep -o 'LUT=[^ ]*' ../finish.sh | head -1 | cut -d= -f2-)
B=render/india_remake_en; df -h / | tail -1
python3 $ENG/compose.py voice/spec_en.json $B.silent.mp4; echo "compose done $(date +%T)"; df -h / | tail -1
ffmpeg -v error -y -i $B.silent.mp4 -filter_complex "[0:v]split[a][b];[b]lut3d=$LUT[g];[a][g]blend=all_mode=normal:all_opacity=0.7,format=yuv420p[v]" \
  -map "[v]" -c:v libx264 -preset veryfast -crf 18 $B.graded.mp4; rm -f $B.silent.mp4; echo "grade done $(date +%T)"
python3 $ENG/mixdown.py voice/spec_en.json voice/voice_en.wav voice/music_en.json $B.mix.wav; echo "mix done $(date +%T)"
ffmpeg -v error -y -i $B.graded.mp4 -i $B.mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $B.mp4
rm -f $B.graded.mp4; echo "RENDER DONE $(date +%T)"; ls -la $B.mp4; df -h / | tail -1
