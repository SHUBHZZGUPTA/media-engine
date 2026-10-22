#!/bin/bash
# snapseg.sh <seg index> <comma times (absolute s)> <outdir>  — snapshot one segment page (its own scenes only)
cd /home/claude/mm-work/ep01v3
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_NO_UPDATE_CHECK=1 HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
i=$(printf "%02d" $1); rm -rf ptest; mkdir ptest; for f in proj/*; do b=$(basename $f); [[ $b == seg*.html || $b == index.html ]] && continue; ln -s $(pwd)/$f ptest/$b; done
cp proj/seg$i.html ptest/index.html
A=$(python3 -c "import json;print(json.load(open('proj/times.json'))['segs'][$1][0])")
REL=$(python3 -c "print(','.join(str(round(float(x)-$A,2)) for x in '$2'.split(',')))")
rm -rf $3; npx hyperframes snapshot ptest -o $3 --at $REL --no-end --describe false --timeout 120000 2>&1 | tail -2
python3 - $3 "$2" <<'PY'
import sys,glob,re
from PIL import Image, ImageDraw
d=sys.argv[1]; ts=sys.argv[2].split(',')
fs=sorted(glob.glob(d+'/frame-*.png'),key=lambda f: float(re.search(r'at-([\d.]+)s',f).group(1)))
cols=4; W=Image.new('RGB',(cols*480,((len(fs)+cols-1)//cols)*280),'#111'); dr=ImageDraw.Draw(W)
for i,f in enumerate(fs):
    im=Image.open(f).convert('RGB').resize((480,270)); x=(i%cols)*480; y=(i//cols)*280; W.paste(im,(x,y)); dr.text((x+6,y+4),ts[i] if i<len(ts) else '',fill='#ff0')
W.save(d+'/sheet.jpg',quality=85); print('sheet',len(fs))
PY
