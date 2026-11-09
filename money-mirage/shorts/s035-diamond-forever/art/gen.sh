#!/bin/bash
# s035 new painted plates via Codex (ChatGPT login). Usage: bash art/gen.sh name [name...]  (run from the Short folder)
cd "$(dirname "$0")/src"
STYLE="Cinematic painterly illustration for a dark, mysterious history documentary: rich oil-painting texture, chiaroscuro lighting with warm amber-gold highlights against deep navy-blue shadows, muted desaturated palette, light haze, shallow depth of field, composed like a film still with the main subject slightly off-centre and calm darker space in the lower third for captions. No text, no letters, no numbers, no writing, no logos, no watermarks, no signatures, no borders. No recognizable real people; any people are anonymous, seen from behind, in silhouette or partly in shadow. Portrait 1024x1536, opaque PNG."
declare -A J
J[dm_ring]="A single solitaire diamond engagement ring standing in an open dark velvet ring box on a dark table, a narrow beam of light making the diamond throw sharp sparkles and tiny rainbow flares; the ring and box fully visible and centred in the upper half of the frame, nothing cropped."
J[dm_vault]="A dark vault room with a sorting table covered in a glittering heap of thousands of loose rough and cut diamonds, a jeweller's loupe and brass tweezers beside it, a single lamp overhead; the heap fully visible in the upper half of the frame."
J[dm_ad]="A 1940s city street at night: a young couple seen from behind, standing arm in arm in front of a glowing jewellery shop window full of sparkling rings on velvet stands; snow falling softly; vintage cars blurred in the background; romantic but slightly eerie mood."
J[dm_lab]="A modern laboratory at night with rows of steel diamond-growing reactors, one open chamber revealing a tray of many identical clear diamonds glowing under cold white and violet light; an anonymous scientist in a white coat seen from behind holding tweezers; sterile, clinical atmosphere."
for n in "$@"; do
  [ -f "$n.png" ] && { echo "skip $n"; continue; }
  t0=$(date +%s)
  timeout 420 codex exec --skip-git-repo-check -s workspace-write "Use your built-in image generation tool to create ONE image and save it in the current directory as $n.png. Image: ${J[$n]} $STYLE Do not do anything else." < /dev/null > "log_$n.txt" 2>&1
  echo "$n exit=$? $(( $(date +%s) - t0 ))s $( [ -f $n.png ] && echo OK || echo MISSING )"
done
