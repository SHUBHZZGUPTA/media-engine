set -e
cd "$(dirname "$0")"
IN=$1; AUD=$2; OUT=$3; DUR=$4
G=/home/claude/media-engine/bhugol-v2/grade/teal-orange-blockbuster.cube
ffmpeg -y -loglevel error -i $IN -loop 1 -t $DUR -i cover_ov.png -i $AUD -filter_complex "\
[0:v]split[a][b];[b]lut3d=file=$G[g];[a][g]blend=all_mode=normal:all_opacity=0.8,format=yuv420p[v0];\
[1:v]format=rgba,fade=out:st=0.12:d=0.28:alpha=1[o1];[v0][o1]overlay=enable='lt(t,0.45)',format=yuv420p[v]" \
 -map "[v]" -map 2:a -c:v libx264 -preset slow -crf 19 -profile:v high -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -t $DUR -movflags +faststart $OUT
ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames:format=duration,size -of default=nw=1 $OUT
