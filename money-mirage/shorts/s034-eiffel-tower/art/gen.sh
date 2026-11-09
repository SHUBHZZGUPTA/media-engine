#!/bin/bash
# s034 new painted plates via Codex (ChatGPT login). Usage: bash art/gen.sh name [name...]  (run from the Short folder)
cd "$(dirname "$0")/src"
STYLE="Cinematic painterly illustration for a dark, mysterious history documentary: rich oil-painting texture, chiaroscuro lighting with warm amber-gold highlights against deep navy-blue shadows, muted desaturated palette, light haze, shallow depth of field, composed like a film still with the main subject slightly off-centre and calm darker space in the lower third for captions. No text, no letters, no numbers, no writing, no logos, no watermarks, no signatures, no borders. No recognizable real people; any people are anonymous, seen from behind, in silhouette or partly in shadow. Portrait 1024x1536, opaque PNG."
declare -A J
J[et_tower]="The Eiffel Tower in Paris in the 1920s at dusk, seen from below at a low angle through light fog, its iron lattice visibly streaked with rust and peeling paint; a few anonymous 1920s pedestrians in coats and hats far below; gas street lamps; the whole tower top fully visible in the upper part of the frame."
J[et_hotel]="An opulent 1920s Paris hotel salon with a crystal chandelier, gilded mirrors and heavy curtains; five anonymous businessmen in 1920s suits seen from behind or in shadow sitting around a polished table, listening to a standing man in a dark tailored suit whose face is in shadow; cigar smoke in the warm light."
J[et_letter]="Close view on a dark desk of an official-looking cream envelope and letter with an ornate embossed seal and a red wax seal, a fountain pen and an inkwell beside it, a small stack of old French banknotes; the paper shows only faint illegible lines, no readable writing; warm lamp light."
J[et_cash]="Two pairs of hands in 1920s suit sleeves passing a fat bundle of old French franc banknotes and a leather briefcase across a table in a dim hotel room; only the hands and cuffs visible; a hat and gloves on the table; tense, secretive mood."
for n in "$@"; do
  [ -f "$n.png" ] && { echo "skip $n"; continue; }
  t0=$(date +%s)
  timeout 420 codex exec --skip-git-repo-check -s workspace-write "Use your built-in image generation tool to create ONE image and save it in the current directory as $n.png. Image: ${J[$n]} $STYLE Do not do anything else." < /dev/null > "log_$n.txt" 2>&1
  echo "$n exit=$? $(( $(date +%s) - t0 ))s $( [ -f $n.png ] && echo OK || echo MISSING )"
done
