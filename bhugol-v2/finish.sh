#!/bin/bash
# Mux narration+music onto the silent render, burn the vertical thumbnail into frames 0-2, two-pass encode < 30 MiB.
set -e
cd /home/claude/budapest
S=/tmp/claude-0/-home-claude/e623d760-259f-581e-af15-a54f4b913d1d/scratchpad
mkdir -p final
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 work/silent.mp4)
RATE=$(python3 -c "print(int(30*1024*1024*8/$DUR/1000 - 200 - 160))")
# thumbnail as a 0.1 s clip at 30 fps, then the render from frame 3 on
ffmpeg -y -loglevel error -loop 1 -framerate 30 -i thumb/BHUGOL_Budapest_thumb_v.jpg -frames:v 3 -vf "scale=1080:1920,format=yuv420p" -c:v libx264 -crf 12 $S/head.mp4
ffmpeg -y -loglevel error -i work/silent.mp4 -vf "trim=start_frame=3,setpts=PTS-STARTPTS,format=yuv420p" -an -c:v libx264 -crf 12 $S/tail.mp4
printf "file '%s'\nfile '%s'\n" $S/head.mp4 $S/tail.mp4 > $S/list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i $S/list.txt -c copy $S/joined.mp4
ffmpeg -y -loglevel error -i $S/joined.mp4 -c:v libx264 -preset slow -b:v ${RATE}k -pass 1 -passlogfile $S/p -pix_fmt yuv420p -an -f mp4 /dev/null
ffmpeg -y -loglevel error -i $S/joined.mp4 -i work/mix_norm.wav -c:v libx264 -preset slow -b:v ${RATE}k -pass 2 -passlogfile $S/p -pix_fmt yuv420p -profile:v high -c:a aac -b:a 160k -ar 48000 -shortest -movflags +faststart final/BHUGOL_Budapest.mp4
ls -la final/BHUGOL_Budapest.mp4; ffprobe -v error -show_entries format=duration -of csv=p=0 final/BHUGOL_Budapest.mp4
