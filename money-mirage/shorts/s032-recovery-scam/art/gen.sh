#!/bin/bash
# s032 new painted plates via Codex (ChatGPT login). Usage: bash art/gen.sh name [name...]  (run from the Short folder)
cd "$(dirname "$0")/src"
STYLE="Cinematic painterly illustration for a dark, mysterious history documentary: rich oil-painting texture, chiaroscuro lighting with warm amber-gold highlights against deep navy-blue shadows, muted desaturated palette, light haze, shallow depth of field, composed like a film still with the main subject slightly off-centre and calm darker space in the lower third for captions. No text, no letters, no numbers, no writing, no logos, no watermarks, no signatures, no borders. No recognizable real people; any people are anonymous, seen from behind, in silhouette or partly in shadow. Portrait 1024x1536, opaque PNG."
declare -A J
J[rs_kitchen]="A person seen from behind sitting alone at a small kitchen table late at night, head lowered, an open empty wallet and a few scattered unpaid bills on the table, a smartphone lying face up beside them starting to glow with an incoming call; one warm lamp, the rest of the room in deep blue shadow."
J[rs_list]="Close view of a thick old ledger book lying open on a dark desk under a single lamp, both pages filled with long neat rows of tiny illegible handwritten entries (blurred scribbles, not readable as letters or numbers), one row marked with a small red ink tick; a fountain pen and a stack of cash beside it; the ledger fully visible in the upper half of the frame, nothing cropped."
J[rs_deepfake]="A laptop on a dark desk whose screen shows an anonymous man in a dark suit standing at an official-looking podium in front of two blurred flags, his face softly blurred and the image broken by digital glitch distortions, coloured pixel smears and scan lines; the laptop screen is the only bright light in the room."
J[rs_rescue]="A bright orange-and-white lifebuoy ring floating on dark choppy water at night, held by a taut thin fishing line that rises out of frame; a sharp steel fishing hook is clearly visible fastened to the lifebuoy; moonlight glints on the waves; ominous, quiet atmosphere; the lifebuoy fully visible in the upper half of the frame."
for n in "$@"; do
  [ -f "$n.png" ] && { echo "skip $n"; continue; }
  t0=$(date +%s)
  timeout 420 codex exec --skip-git-repo-check -s workspace-write "Use your built-in image generation tool to create ONE image and save it in the current directory as $n.png. Image: ${J[$n]} $STYLE Do not do anything else." < /dev/null > "log_$n.txt" 2>&1
  echo "$n exit=$? $(( $(date +%s) - t0 ))s $( [ -f $n.png ] && echo OK || echo MISSING )"
done
