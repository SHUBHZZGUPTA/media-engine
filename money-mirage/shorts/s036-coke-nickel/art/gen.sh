#!/bin/bash
# s036 new painted plates via Codex (ChatGPT login). Usage: bash art/gen.sh name [name...]  (run from the Short folder)
cd "$(dirname "$0")/src"
STYLE="Cinematic painterly illustration for a dark, mysterious history documentary: rich oil-painting texture, chiaroscuro lighting with warm amber-gold highlights against deep navy-blue shadows, muted desaturated palette, light haze, shallow depth of field, composed like a film still with the main subject slightly off-centre and calm darker space in the lower third for captions. No text, no letters, no numbers, no writing, no logos, no watermarks, no signatures, no borders. No recognizable real people; any people are anonymous, seen from behind, in silhouette or partly in shadow. Portrait 1024x1536, opaque PNG."
declare -A J
J[ck_fountain]="An early-1900s American drugstore soda fountain counter with marble top and brass taps, a row of tall glasses filled with fizzy dark cola and a few plain straight-sided glass bottles of dark soda with no labels; a single small nickel coin lying on the counter in the foreground; anonymous customers in period clothes in soft focus."
J[ck_lawyers]="Two anonymous lawyers in 1899 suits and bowler hats seen from behind or in shadow, shaking hands across a desk in a wood-panelled office; on the desk a signed contract with illegible lines, a fountain pen and one plain glass bottle of dark soda with no label; gaslight glow."
J[ck_vending]="A heavy 1940s red metal soda vending machine with a chrome coin slot and a small window showing rows of plain dark glass soda bottles with no labels and no lettering on the machine; a single nickel coin held in an anonymous hand about to enter the coin slot; night, one overhead bulb."
J[ck_office]="An empty grand government office in the 1950s at night: a large polished wooden desk with a black rotary telephone, a brass desk lamp and neat papers with illegible lines; tall windows with heavy drapes and the faint shadow of a flag; nobody present."
J[ck_bottles]="A 1950s bottling plant line: hundreds of plain straight-sided glass bottles of dark soda with no labels moving along a conveyor, steam and amber light, anonymous workers in caps seen from behind in the haze; the bottles sharp in the foreground."
for n in "$@"; do
  [ -f "$n.png" ] && { echo "skip $n"; continue; }
  t0=$(date +%s)
  timeout 420 codex exec --skip-git-repo-check -s workspace-write "Use your built-in image generation tool to create ONE image and save it in the current directory as $n.png. Image: ${J[$n]} $STYLE Do not do anything else." < /dev/null > "log_$n.txt" 2>&1
  echo "$n exit=$? $(( $(date +%s) - t0 ))s $( [ -f $n.png ] && echo OK || echo MISSING )"
done
