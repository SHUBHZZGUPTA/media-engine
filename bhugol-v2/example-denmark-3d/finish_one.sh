# usage: finish_one.sh en|hi
set -e
L=$1; D=/home/claude/work/den; R=/home/claude/media-engine/bhugol-v2
cd $D/out
ffmpeg -y -loglevel error -i silent_$L.mp4 -filter_complex "[0:v]split[a][b];[b]lut3d=file=$R/grade/teal-orange-blockbuster.cube[g];[a][g]blend=all_mode=normal:all_opacity=0.8,format=yuv420p" -c:v libx264 -crf 12 -preset fast silent_graded_$L.mp4
NAME=BHUGOL_A_Desert_in_Europe; [ $L = hi ] && NAME=${NAME}_HI
bash $R/3d/finish_hq.sh silent_graded_$L.mp4 $D/au_$L/mix_final.wav $D/thumbs/cover_$L.jpg $D/out/$NAME.mp4
