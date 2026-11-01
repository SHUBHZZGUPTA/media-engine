#!/bin/bash
# compose (2 halves in parallel) -> 70% film-fade grade -> mix -> mux.   Usage: finish.sh spec.json voice.wav music.json out.mp4
set -e
SPEC=$1; VOICE=$2; MUSIC=$3; OUT=$4
ENG=/home/claude/media-engine/longform/engine; LUT=/home/claude/media-engine/bhugol-v2/grade/film-fade.cube
B=${OUT%.mp4}
END=$(python3 -c "import json;s=json.load(open('$SPEC'))['shots'];print(round(s[-1]['t1'],3))")
MID=$(python3 -c "import json;s=json.load(open('$SPEC'))['shots'];e=$END;print(min((x['t0'] for x in s), key=lambda t: abs(t-e/2)))")
t0=$(date +%s)
python3 -B $ENG/compose.py "$SPEC" "$B.part1.mp4" --from 0 --to $MID > "$B.part1.log" 2>&1 &
python3 -B $ENG/compose.py "$SPEC" "$B.part2.mp4" --from $MID --to $END > "$B.part2.log" 2>&1 &
wait
echo "compose $(( $(date +%s) - t0 ))s (split at $MID of $END)"
printf "file '%s'\nfile '%s'\n" "$B.part1.mp4" "$B.part2.mp4" > "$B.concat.txt"
ffmpeg -v error -y -f concat -safe 0 -i "$B.concat.txt" -c copy "$B.silent.mp4"
ffmpeg -v error -y -i "$B.silent.mp4" -filter_complex "[0:v]split[a][b];[b]lut3d=$LUT[g];[a][g]blend=all_mode=normal:all_opacity=0.7,format=yuv420p[v]" \
  -map "[v]" -c:v libx264 -preset veryfast -crf 18 "$B.graded.mp4"
python3 -B $ENG/mixdown.py "$SPEC" "$VOICE" "$MUSIC" "$B.mix.wav"
ffmpeg -v error -y -i "$B.graded.mp4" -i "$B.mix.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
echo "DONE $OUT total $(( $(date +%s) - t0 ))s"
