#!/bin/bash
# Usage: render_chunks.sh <lang> <spec> <timing> ; renders 10 s chunks into work/<lang>/cNN.mp4, skipping finished ones.
L=$1; SPEC=$2; TIM=$3; W=/home/claude/work/twins; source $W/tools/env.sh
DUR=$(python3 -c "import json;print(json.load(open('$W/build-$L/times.json'))['dur'])")
mkdir -p $W/work/$L; i=0; t=0
while python3 -c "import sys; sys.exit(0 if $t < $DUR - 0.001 else 1)"; do
  n=$(printf %02d $i); t1=$(python3 -c "print(round(min($t+10, $DUR),4))")
  if [ ! -s $W/work/$L/c$n.mp4 ]; then
    rm -rf $W/work/$L/b$n; python3 $W/tools/build.py $W/$SPEC $W/$TIM $W/work/$L/b$n $L --from=$t --to=$t1 --allow-gaps > /dev/null
    (cd $W/work/$L/b$n && hyperframes render --crf 14 --no-browser-gpu --output $W/work/$L/tmp$n.mp4 > $W/work/$L/log$n.txt 2>&1) && mv $W/work/$L/tmp$n.mp4 $W/work/$L/c$n.mp4 && rm -rf $W/work/$L/b$n
    echo "chunk $L $n done $(date +%T)"
  fi
  i=$((i+1)); t=$t1
done
echo "ALL $L DONE"
