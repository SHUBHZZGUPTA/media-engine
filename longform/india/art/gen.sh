#!/bin/bash
# India pilot (hook + ch1) art: same toy-figure template as russia/art/gen.sh. c_traveller is reused from Russia.
cd "$(dirname "$0")"
STYLE="Soft matte vinyl-toy texture, gentle studio lighting from the upper left, full body visible and centered"
CH() { echo "Single character cut-out on a fully transparent background: a cute chibi 3D figurine of $1, rounded pawn-shaped body with no visible legs (like a board-game piece), big round head, $2. Simple face: small black dot eyes and short eyebrows, $3. $STYLE, facing three-quarters to the $4. No ground, no shadow, no text. Portrait 1024x1536, transparent background PNG."; }
SC() { echo "A photoreal painterly scene of $1, large empty open ground in the lower middle of the frame (space for characters to be added later), no people, no animals, no text. Horizontal landscape 1536x1024, opaque PNG."; }
declare -A J
J[c_inspector]="$(CH "a Bronze Age Indus Valley city inspector from about 2500 BCE" "short trimmed beard, a simple white cotton robe draped over the left shoulder with a red trefoil pattern, a narrow headband with a small round ornament on the forehead, holding a straight wooden measuring rod with notches" "stern, unimpressed, one eyebrow raised" "right")"
J[c_brickmaker]="$(CH "a young Bronze Age Indus Valley brick-maker from about 2500 BCE" "bare arms dusted with clay, plain off-white cotton wrap, short dark hair, holding one slightly oversized reddish-brown fired brick in both hands" "nervous, sheepish smile" "left")"
J[c_engineer]="$(CH "a British railway engineer in 1850s colonial Punjab" "white pith sun helmet, tan linen jacket, a thick moustache, holding a clipboard and a rolled-up map" "smug and delighted" "left")"
J[c_foreman]="$(CH "a Punjabi railway construction foreman in the 1850s" "simple white kurta, a loosely tied saffron turban, a neat black beard, a shovel resting on one shoulder" "polite, pointing helpfully to the side" "right")"
J[in_bazaar]="$(SC "a rich 17th-century Indian port bazaar at Surat: stalls overflowing with sacks of pepper, cinnamon and cardamom, bolts of bright printed cotton and silk, brass pots, sunlight through cloth awnings, tall wooden sailing ships in the harbour behind")"
J[in_indus]="$(SC "the Indus river valley about 4,500 years ago: a wide, slow brown river winding through flat green floodplain fields, palm trees, and a large walled brick city on a raised mound in the distance, hazy warm morning light")"
J[in_street]="$(SC "a straight street in the Bronze Age Indus city of Mohenjo-daro about 2500 BCE: two-storey houses of uniform reddish-brown fired brick, small windowless walls facing the street, a covered brick drain with stone lids running along the side of the street, clear midday light")"
J[in_bath]="$(SC "the Great Bath of Mohenjo-daro when new, about 2500 BCE: a large rectangular sunken pool of finely fitted reddish-brown bricks, wide brick steps leading down at both ends, a colonnade of brick piers around it, calm water reflecting the sky")"
J[in_railway]="$(SC "an 1850s railway construction site on the flat dry plains of Punjab: a half-built embankment with wooden sleepers and iron rails, wooden carts, and beside it a low earth mound with hundreds of old, perfect reddish-brown bricks sticking out, dusty afternoon light")"
ORDER="c_inspector c_brickmaker c_engineer c_foreman in_bazaar in_indus in_street in_bath in_railway"
for n in $ORDER; do
  [ -f "$n.png" ] && { echo "skip $n"; continue; }
  t0=$(date +%s)
  timeout 400 codex exec --skip-git-repo-check -s workspace-write "Use your built-in image generation tool to create ONE image and save it in the current directory as $n.png. Image: ${J[$n]} Do not do anything else." < /dev/null > "log_$n.txt" 2>&1
  echo "$n exit=$? $(( $(date +%s) - t0 ))s $( [ -f $n.png ] && echo OK || echo MISSING )"
done
echo ALLDONE
