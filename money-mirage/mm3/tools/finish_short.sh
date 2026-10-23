#!/bin/bash
# finish_short.sh <thumb_vertical.jpg> <out.mp4> — native portrait Short: thumbnail burned into frames 0-2 (cover-picker trick),
# audio/mix.wav loudness-normalised to -14 LUFS / -1.5 dBTP (two-pass), video two-pass x264 sized to stay under 30 MiB.
# Run from the Short folder (or its hi/ folder) after render_all.sh + mix.py.
source "$(dirname "$0")/env.sh"; set -e; TH="$1"; OUT="$2"; V="$EP/renders/video_silent.mp4"; A="$EP/audio/mix.wav"; mkdir -p "$(dirname "$OUT")"
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
RATE=$(python3 -c "print(int(30*1024*1024*8/float($D)/1000) - 200 - 160)")
J=$(ffmpeg -hide_banner -i "$A" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$J" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -loglevel error -y -i "$A" -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" "$EP/audio/mix_norm.wav"
VF="[1:v]scale=1080:1920,format=yuv420p[t];[0:v][t]overlay=0:0:enable='lt(n\,3)',format=yuv420p[v]"
P=$(mktemp -d)
ffmpeg -loglevel error -y -i "$V" -loop 1 -i "$TH" -filter_complex "$VF" -map "[v]" -c:v libx264 -preset slow -b:v ${RATE}k -pass 1 -passlogfile "$P/p" -an -t "$D" -f mp4 /dev/null
ffmpeg -loglevel error -y -i "$V" -loop 1 -i "$TH" -i "$EP/audio/mix_norm.wav" -filter_complex "$VF" -map "[v]" -map 2:a -c:v libx264 -preset slow -b:v ${RATE}k -pass 2 -passlogfile "$P/p" -profile:v high -c:a aac -b:a 160k -ar 48000 -t "$D" -movflags +faststart "$OUT"
rm -rf "$P"; ls -la "$OUT"; ffmpeg -hide_banner -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I:|Peak:)" | tail -2
