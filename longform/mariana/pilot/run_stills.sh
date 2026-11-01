#!/bin/bash
# render every living still that isn't done yet, 2 at a time
cd /home/claude/pilot
t0=$(date +%s)
while IFS=$'\t' read -r n src cfg; do
  [ -f shots/$n.mp4 ] && continue
  echo "$n"$'\t'"$src"$'\t'"$cfg"
done < stills_jobs.txt | xargs -P 2 -d '\n' -I{} bash -c 'IFS=$'"'"'\t'"'"' read -r n src cfg <<< "{}"; plate/render_plate.sh "$n" "$src" "$cfg" || echo "FAIL $n"'
echo "STILLS DONE in $(( $(date +%s) - t0 ))s; $(ls shots/st*.mp4 | wc -l) files"
