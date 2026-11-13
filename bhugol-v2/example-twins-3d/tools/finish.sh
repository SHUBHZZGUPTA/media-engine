#!/bin/bash
# finish.sh <lang> : join chunks -> retention QA -> grade -> cover + mix -> final MP4
set -e; L=$1; W=/home/claude/work/twins; O=$W/out; mkdir -p $O; cd $W/work/$L
ls c*.mp4 | sort | sed "s/^/file '/; s/$/'/" > list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i list.txt -c copy $W/work/silent_$L.mp4
python3 /home/claude/media-engine/bhugol-v2/motion/retention_qa.py $W/work/silent_$L.mp4 --end $(python3 -c "import json;print(json.load(open('$W/build-$L/times.json'))['dur'])") --spec $W/$( [ $L = en ] && echo twins.json || echo twins-hi.json ) --timing $W/audio/hf-$L/timing.json > $W/work/qa_$L.txt 2>&1 || true
ffmpeg -y -loglevel error -i $W/work/silent_$L.mp4 -filter_complex "[0:v]split[a][b];[b]lut3d=file=/home/claude/media-engine/bhugol-v2/grade/teal-orange-blockbuster.cube[g];[a][g]blend=all_mode=normal:all_opacity=0.8,format=yuv420p" -c:v libx264 -crf 12 $W/work/graded_$L.mp4
NAME=$( [ $L = en ] && echo BHUGOL_Countries_With_a_Hidden_Twin.mp4 || echo BHUGOL_Countries_With_a_Hidden_Twin_HI.mp4 )
bash /home/claude/media-engine/bhugol-v2/3d/finish_hq.sh $W/work/graded_$L.mp4 $W/audio/hf-$L/mix_final.wav $W/thumb/thumbA_${L}_v.jpg $O/$NAME
