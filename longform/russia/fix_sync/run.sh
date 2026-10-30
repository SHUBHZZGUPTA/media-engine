#!/bin/bash
# Russia EN sync fix (30 Oct 2026): rebuild the published video from the saved project with ONE change:
# the Ch2-11 part's first frame is pinned to 0:00 (it started at 1.4 s, so pictures + subtitles ran 1.4 s ahead of the voice
# and the last 1.4 s of audio was cut). Hook + Ch1 part already started at 0:00 and is rebuilt unchanged.
set -e
R=/home/claude/media-engine/longform/russia; F=$R/fix_sync; S=/tmp/claude-0/-home-claude/10377bb8-c502-51d7-9f18-3e382cc6f75f/scratchpad
cd $R
# 0) the rebuilt hook+Ch1 plan must equal the published one (spec_en_3d7.json)
python3 - <<'PY'
import json
a = json.load(open("/home/claude/media-engine/longform/russia/pilot/spec_en_3d7.json"))
b = json.load(open("/tmp/claude-0/-home-claude/10377bb8-c502-51d7-9f18-3e382cc6f75f/scratchpad/ru_spec_3d7_rebuilt.json"))
print("SPEC CHECK hook+Ch1:", "IDENTICAL to published plan" if a == b else "DIFFERENT")
if a != b:
    for k, (x, y) in enumerate(zip(a["shots"], b["shots"])):
        if x != y: print(" first differing shot", k, x["t0"]); break
    raise SystemExit(1)
PY
# 1) Ch2-11 plan: identical to published except shots[0].t0 = 0
python3 - <<'PY'
import json
s = json.load(open("/home/claude/media-engine/longform/russia/full/spec_full.json")); print("Ch2-11 first shot was at", s["shots"][0]["t0"])
s["shots"][0]["t0"] = 0.0
json.dump(s, open("/home/claude/media-engine/longform/russia/fix_sync/spec_full_sync.json", "w"))
PY
# 2) render both parts with the same finish script as the original
bash $R/full/finish.sh $R/pilot/spec_en_3d7.json $R/pilot/voice_en_fast.wav $R/pilot/music_en_fast.json $F/part1_hook_ch1.mp4
bash $R/full/finish.sh $F/spec_full_sync.json $R/full/voice_full.wav $R/full/music_full.json $F/part2_ch2_11.mp4
# 3) join
printf "file '%s'\nfile '%s'\n" $F/part1_hook_ch1.mp4 $F/part2_ch2_11.mp4 > $F/concat.txt
ffmpeg -v error -y -f concat -safe 0 -i $F/concat.txt -c copy -movflags +faststart $F/russia_en_final_sync.mp4
P1=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $F/part1_hook_ch1.mp4)
echo "part1 $P1 s"
printf '{"name":"Hook + Ch1","spec":"%s","voice":"%s","offset":0}' $R/pilot/spec_en_3d7.json $R/pilot/voice_en_fast.wav > $F/qc_p1.json
printf '{"name":"Ch2-11 + ending","spec":"%s","voice":"%s","offset":%s}' $F/spec_full_sync.json $R/full/voice_full.wav $P1 > $F/qc_p2.json
python3 /home/claude/media-engine/longform/engine/qc_video.py $F/russia_en_final_sync.mp4 $F/qc_p1.json $F/qc_p2.json --report $F/qc_report.md || true
echo FIX_DONE
