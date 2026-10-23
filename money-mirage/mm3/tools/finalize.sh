#!/bin/bash
# silent render + audio/mix.wav -> loudness-normalised master (-14 LUFS, -1.5 dBTP, two-pass), upload copy (<500 MB) and 720p preview
source "$(dirname "$0")/env.sh"; set -e; mkdir -p "$EP/deliver"; S=$(python3 -c "import json;print(json.load(open('episode.json'))['slug'])")
V="$EP/renders/video_silent.mp4"; A="$EP/audio/mix.wav"; M="$EP/deliver/${S}_master_1080p.mp4"
J=$(ffmpeg -hide_banner -i "$A" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$J" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -loglevel error -y -i "$V" -i "$A" -map 0:v -map 1:a -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" -c:a aac -b:a 320k -shortest -movflags +faststart "$M"
ffmpeg -loglevel error -y -i "$M" -c:v libx264 -preset fast -crf 18 -maxrate 6.6M -bufsize 13M -pix_fmt yuv420p -c:a copy -movflags +faststart "$EP/deliver/${S}_1080p_upload.mp4"
ffmpeg -loglevel error -y -i "$M" -vf scale=1280:-2 -c:v libx264 -crf 23 -preset veryfast -c:a aac -b:a 160k -movflags +faststart "$EP/deliver/${S}_preview_720p.mp4"
ffmpeg -hide_banner -i "$M" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I:|Peak:)" | tail -2; ls -la "$EP/deliver"
