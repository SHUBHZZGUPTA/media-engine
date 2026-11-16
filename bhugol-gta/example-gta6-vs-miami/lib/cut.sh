while read n T a b src; do
  [ -f clips/$n.webm ] && continue
  c=$(ffmpeg -nostdin -v info -ss $a -to $b -i $T.mp4 -vf cropdetect=24:2:0 -f null - 2>&1 | grep -o "crop=[0-9:]*" | tail -1); c=${c:-crop=1920:1080:0:0}
  p=$(python3 -c "print(max(0,$a-2))"); ra=$(python3 -c "print($a-max(0,$a-2))"); rb=$(python3 -c "print($b-max(0,$a-2))")
  ffmpeg -nostdin -v error -y -ss $p -i $T.mp4 -an -vf "trim=start=$ra:end=$rb,setpts=PTS-STARTPTS,$c,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30" -c:v libvpx-vp9 -crf 24 -b:v 0 -g 10 -deadline good -cpu-used 5 -row-mt 1 -pix_fmt yuv420p clips/$n.webm
  echo "$n $c $(ffprobe -v error -show_entries format=duration -of csv=p=0 clips/$n.webm)" >> cut.log
done < sel.txt
echo ALLDONE >> cut.log
