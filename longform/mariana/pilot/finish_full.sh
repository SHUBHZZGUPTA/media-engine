#!/bin/bash
# compose (2 halves in parallel) -> 50% teal-orange grade -> mix -> mux, for out_full/
set -e; cd /home/claude/pilot/out_full
ENG=/home/claude/media-engine/longform/engine; LUT=/home/claude/media-engine/bhugol-v2/grade/teal-orange-blockbuster.cube
END=$(python3 -c "import json;s=json.load(open('spec.json'))['shots'];print(round(s[-1]['t1'],3))")
MID=$(python3 -c "import json;s=json.load(open('spec.json'))['shots'];e=$END;print(min((x['t0'] for x in s), key=lambda t: abs(t-e/2)))")
t0=$(date +%s)
python3 -B $ENG/compose.py spec.json part1.mp4 --from 0 --to $MID > part1.log 2>&1 &
python3 -B $ENG/compose.py spec.json part2.mp4 --from $MID --to $END > part2.log 2>&1 &
wait; echo "compose $(( $(date +%s) - t0 ))s"
printf "file 'part1.mp4'\nfile 'part2.mp4'\n" > concat.txt; ffmpeg -v error -y -f concat -safe 0 -i concat.txt -c copy silent.mp4
ffmpeg -v error -y -i silent.mp4 -filter_complex "[0:v]split[a][b];[b]lut3d=$LUT[g];[a][g]blend=all_mode=normal:all_opacity=0.5,format=yuv420p[v]" -map "[v]" -c:v libx264 -preset veryfast -crf 18 graded.mp4
python3 -B $ENG/mixdown.py mix_spec.json voice.wav music.json mix.wav
ffmpeg -v error -y -i graded.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart Mariana_Trench_EN.mp4
echo "DONE $(( $(date +%s) - t0 ))s"
