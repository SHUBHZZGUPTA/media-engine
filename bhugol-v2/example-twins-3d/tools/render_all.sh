#!/bin/bash
W=/home/claude/work/twins
$W/tools/render_chunks.sh en twins.json audio/hf-en/timing.json && $W/tools/render_chunks.sh hi twins-hi.json audio/hf-hi/timing.json
