#!/bin/bash
source /home/claude/work/twins/tools/env.sh
cd /home/claude/work/twins/build-en && hyperframes render --crf 14 --no-browser-gpu --output /home/claude/work/twins/work/silent_en.mp4 > /home/claude/work/twins/work/render_en.log 2>&1
cd /home/claude/work/twins/build-hi && hyperframes render --crf 14 --no-browser-gpu --output /home/claude/work/twins/work/silent_hi.mp4 > /home/claude/work/twins/work/render_hi.log 2>&1
echo done > /home/claude/work/twins/work/render.done
