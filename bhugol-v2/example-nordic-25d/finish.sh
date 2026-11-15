set -e
cd /home/claude/nordic
DUR=$(python3 -c "import json;print(json.load(open('build/times.json'))['dur'])")
G=/home/claude/media-engine/bhugol-v2/grade/teal-orange-blockbuster.cube
E1=$(python3 -c "print(round($DUR-0.47,3))")
ffmpeg -y -loglevel error -i silent.mp4 -loop 1 -t $DUR -i cover_ov.png -loop 1 -t $DUR -i cover_ov.png -i audio/mix_master.wav -filter_complex "\
[0:v]split[a][b];[b]lut3d=file=$G[g];[a][g]blend=all_mode=normal:all_opacity=0.8,format=yuv420p[v0];\
[1:v]format=rgba,fade=out:st=0.12:d=0.28:alpha=1[o1];\
[2:v]format=rgba,fade=in:st=$E1:d=0.38:alpha=1[o2];\
[v0][o1]overlay=enable='lt(t,0.45)'[v1];[v1][o2]overlay=enable='gte(t,$E1)',format=yuv420p[v]" \
 -map "[v]" -map 3:a -c:v libx264 -preset slow -crf 19 -profile:v high -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -t $DUR -movflags +faststart BHUGOL_5_Countries_1_Flag.mp4
ffprobe -v error -show_entries format=duration,size -of default=nw=1 BHUGOL_5_Countries_1_Flag.mp4
