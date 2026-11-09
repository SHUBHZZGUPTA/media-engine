#!/bin/bash
# s033 new painted plates via Codex (ChatGPT login). Usage: bash art/gen.sh name [name...]  (run from the Short folder)
cd "$(dirname "$0")/src"
STYLE="Cinematic painterly illustration for a dark, mysterious history documentary: rich oil-painting texture, chiaroscuro lighting with warm amber-gold highlights against deep navy-blue shadows, muted desaturated palette, light haze, shallow depth of field, composed like a film still with the main subject slightly off-centre and calm darker space in the lower third for captions. No text, no letters, no numbers, no writing, no logos, no watermarks, no signatures, no borders. No recognizable real people; any people are anonymous, seen from behind, in silhouette or partly in shadow. Portrait 1024x1536, opaque PNG."
declare -A J
J[ram_chip]="Dramatic close-up of a single computer RAM memory stick (a long thin green circuit board with a row of black rectangular chips and a gold-contact edge) standing on a dark wooden desk, lit from above so the gold contacts glow; tiny sparks of light; the whole stick fully visible and centred in the upper half of the frame, nothing cropped."
J[ram_datacenter]="A vast data centre aisle seen at eye level, endless rows of tall black server racks stretching into the distance on both sides, thousands of tiny blue and amber status lights, cold mist on the floor, one small anonymous technician silhouette far down the aisle for scale."
J[ram_fab]="Inside a semiconductor chip factory cleanroom bathed in amber light, anonymous workers in white full-body cleanroom suits and hoods seen from behind, one holding up a large shiny round silicon wafer that reflects rainbow light; rows of machines receding into haze."
J[ram_shop]="An electronics shop counter at night: a new smartphone box and a slim laptop box sitting on the counter, a very long paper receipt curling off the counter edge onto the floor; an anonymous shopper seen from behind with hands in pockets; warm shop lights against a dark blue street outside the window."
for n in "$@"; do
  [ -f "$n.png" ] && { echo "skip $n"; continue; }
  t0=$(date +%s)
  timeout 420 codex exec --skip-git-repo-check -s workspace-write "Use your built-in image generation tool to create ONE image and save it in the current directory as $n.png. Image: ${J[$n]} $STYLE Do not do anything else." < /dev/null > "log_$n.txt" 2>&1
  echo "$n exit=$? $(( $(date +%s) - t0 ))s $( [ -f $n.png ] && echo OK || echo MISSING )"
done
