#!/bin/bash
# Join the India pilot part (hook + ch1) and the full part (ch2-ending) into one video.
# Video: stream copy (both parts are the same H.264 1080p30 settings). Audio: the two mixes are trimmed/padded to their video's
# exact length, joined as ONE continuous WAV and encoded once (two separately encoded AAC parts drift ~35 ms at the seam).
set -e
cd "$(dirname "$0")"
P=../pilot/render/india_pilot_en; F=render/india_full_en; OUT=render/india_en_final.mp4
dur() { ffprobe -v error -select_streams v:0 -show_entries stream=duration -of csv=p=0 "$1"; }
DP=$(dur $P.mp4); DF=$(dur $F.mp4); echo "pilot $DP s, full $DF s"
ffmpeg -v error -y -i $P.mix.wav -i $F.mix.wav -filter_complex \
  "[0:a]apad,atrim=0:$DP,asetpts=N/SR/TB[a0];[1:a]apad,atrim=0:$DF,asetpts=N/SR/TB[a1];[a0][a1]concat=n=2:v=0:a=1[a]" \
  -map "[a]" -c:a pcm_s16le render/india_en_final.mix.wav
printf "file '%s'\nfile '%s'\n" "$(realpath $P.mp4)" "$(realpath $F.mp4)" > render/join_list.txt
ffmpeg -v error -y -f concat -safe 0 -i render/join_list.txt -map 0:v -c:v copy render/india_en_final.video.mp4
ffmpeg -v error -y -i render/india_en_final.video.mp4 -i render/india_en_final.mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k \
  -shortest -movflags +faststart $OUT
echo "final: $(ffprobe -v error -show_entries format=duration -of csv=p=0 $OUT) s -> $OUT"
