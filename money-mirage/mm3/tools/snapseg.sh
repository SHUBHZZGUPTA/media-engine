#!/bin/bash
# snapseg.sh <seg index> <comma times (absolute s)> <outdir> — snapshot one long-form segment page; writes <outdir>/sheet.jpg
source "$(dirname "$0")/env.sh"; i=$(printf "%02d" $1); P="$EP/ptest"; rm -rf "$P"; mkdir "$P"
for f in "$EP"/proj/*; do b=$(basename $f); [[ $b == seg*.html || $b == index.html ]] && continue; ln -s "$f" "$P/$b"; done
cp "$EP/proj/seg$i.html" "$P/index.html"
A=$(python3 -c "import json;print(json.load(open('$EP/proj/times.json'))['segs'][$1][0])")
REL=$(python3 -c "print(','.join(str(round(float(x)-$A,2)) for x in '$2'.split(',')))")
rm -rf "$3"; (cd "$ENGD" && npx hyperframes snapshot "$P" -o "$3" --at $REL --no-end --describe false --timeout 300000 2>&1 | tail -1)
python3 "$TOOLS/sheet.py" "$3" "$2" 4 480 270
