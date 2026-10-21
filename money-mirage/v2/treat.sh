#!/bin/bash
# Apply HyperFrames media treatments listed in proj/treat.json (one CLI call per media element).
cd "$(dirname "$0")"
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_NO_UPDATE_CHECK=1 HYPERFRAMES_SKIP_SKILLS=1
python3 -c "
import json
for s in json.load(open('proj/treat.json')):
    for sel,g in s['treat']: print(s['file']+'\t'+sel+'\t'+g)
" | while IFS=$'\t' read -r f sel g; do
  npx hyperframes media-treatment --project proj --file "$f" --selector "$sel" --grading "$g" --apply --json > /tmp/claude-0/-home-claude/af5ff343-7369-5664-abc8-263fcf3254bc/scratchpad/treat_last.json 2>&1 || { echo "FAILED $f $sel"; cat /tmp/claude-0/-home-claude/af5ff343-7369-5664-abc8-263fcf3254bc/scratchpad/treat_last.json | head -5; }
done
echo treated
