#!/bin/bash
# s031 new painted plates via Codex (ChatGPT login). Usage: bash art/gen.sh name [name...]  (run from the Short folder)
cd "$(dirname "$0")/src"
STYLE="Cinematic painterly illustration for a dark, mysterious history documentary: rich oil-painting texture, chiaroscuro lighting with warm amber-gold highlights against deep navy-blue shadows, muted desaturated palette, light haze, shallow depth of field, composed like a film still with the main subject slightly off-centre and calm darker space in the lower third for captions. No text, no letters, no numbers, no writing, no logos, no watermarks, no signatures, no borders. No recognizable real people; any people are anonymous, seen from behind, in silhouette or partly in shadow. Portrait 1024x1536, opaque PNG."
declare -A J
J[coin_case]="A single giant gold coin, about half a metre wide and three centimetres thick, standing upright on a small stand inside a glass museum display case in a dim museum hall at night, one narrow spotlight from above making the gold glow; the face of the coin shows a large embossed maple leaf and a raised rim, no portrait, no lettering; the whole coin fully visible and centred in the upper half of the frame, nothing cropped."
J[museum_tracks]="A grand neo-baroque museum building with a large dome on a river island at night, seen from a low angle; an elevated brick railway viaduct with train tracks runs right beside its stone wall; a thin metal ladder leans from the tracks up to a dark open upper window; wet stones, one distant streetlamp, misty river below."
J[wheelbarrow]="Two anonymous figures in dark hooded clothes seen from behind, pushing a wheelbarrow along night railway tracks on a bridge over a dark river; in the wheelbarrow lies a huge round gold coin disc catching faint city light; distant blurred city lights and haze; tense, quiet atmosphere."
J[furnace]="Close view of a dark makeshift workshop: thick chunks of a cut-up gold disc lying on a scarred workbench beside a glowing crucible that pours a stream of molten gold into a mould; only gloved hands visible, sparks and smoke, intense orange firelight against deep blue shadows."
J[jail_bars]="An empty prison cell seen through heavy iron bars, cold pale light falling through a high small window and casting bar shadows on a concrete floor; on the floor one tiny glinting fleck of gold; bleak, quiet atmosphere."
for n in "$@"; do
  [ -f "$n.png" ] && { echo "skip $n"; continue; }
  t0=$(date +%s)
  timeout 420 codex exec --skip-git-repo-check -s workspace-write "Use your built-in image generation tool to create ONE image and save it in the current directory as $n.png. Image: ${J[$n]} $STYLE Do not do anything else." < /dev/null > "log_$n.txt" 2>&1
  echo "$n exit=$? $(( $(date +%s) - t0 ))s $( [ -f $n.png ] && echo OK || echo MISSING )"
done
