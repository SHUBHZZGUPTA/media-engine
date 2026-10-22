#!/bin/bash
# join -> loudness-normalised mux (-14 LUFS, -1.5 dBTP, two-pass) -> 720p preview
set -e; cd /home/claude/mm-work/ep01v3; mkdir -p deliver
V=renders/video_silent.mp4; A=audio/mix.wav
J=$(ffmpeg -hide_banner -i $A -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$J" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -loglevel error -y -i $V -i $A -map 0:v -map 1:a -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" -c:a aac -b:a 320k -shortest -movflags +faststart deliver/MoneyMirage_ep01_v3_FINAL_1080p.mp4
ffmpeg -loglevel error -y -i deliver/MoneyMirage_ep01_v3_FINAL_1080p.mp4 -vf scale=1280:-2 -c:v libx264 -crf 23 -preset veryfast -c:a aac -b:a 160k -movflags +faststart deliver/MoneyMirage_ep01_v3_FINAL_preview_720p.mp4
ffmpeg -hide_banner -i deliver/MoneyMirage_ep01_v3_FINAL_1080p.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I:|True peak|Peak:)" | tail -3
ls -la deliver/
