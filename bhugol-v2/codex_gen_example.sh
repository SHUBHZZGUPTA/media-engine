#!/bin/bash
# Budapest skit art through Codex's built-in image generation (ChatGPT plan, no API credits).
cd "$(dirname "$0")"
STYLE="Soft matte vinyl-toy texture, gentle studio lighting from the upper left, full body visible and centered"
CH() { echo "Single character cut-out on a fully transparent background: a cute chibi 3D figurine of $1, rounded pawn-shaped body with no visible legs (like a board-game piece), big round head, $2. Simple face: small black dot eyes and short eyebrows, $3. $STYLE, facing three-quarters to the $4. No ground, no shadow, no text. Portrait 1024x1536, transparent background PNG."; }
PL() { echo "A photoreal painterly scene of $1, large empty open ground in the lower middle of the frame (space for characters to be added later), no people, no animals, no text. Vertical portrait 1024x1536, opaque PNG."; }
declare -A J
J[plate_aerial]="A painterly illustrated bird's-eye view, looking almost straight down, of two early-1800s towns on opposite banks of a wide blue-grey river that runs vertically down the middle of the frame from top to bottom. LEFT bank: green wooded hills, a baroque royal castle on a hilltop, a small old town with red roofs climbing the hill. RIGHT bank: completely flat land densely packed with houses, market squares and church towers. NO bridges at all across the river. Soft warm daylight, rich storybook colours, no text, no labels, no people visible. Vertical portrait 1024x1536, opaque PNG."
J[plate_river]="$(PL "the frozen Danube in winter in 1820 at dusk, seen from the flat snowy riverbank of Pest: a very wide grey river choked with broken, jagged ice floes; on the far bank a tall hill topped by a baroque royal castle with a few warm lit windows; NO bridge anywhere; cold blue light, light snowfall")"
J[plate_toll]="$(PL "the entrance to a grand 1849 iron chain suspension bridge over a wide river: a massive stone tower with a tall arch, heavy iron chains sweeping up to it, a small wooden toll booth beside the road with a striped lowered barrier, cobblestone ground, soft morning light")"
J[c_buda]="$(CH "a proud personified old hilltop town" "body shaped like a grey stone castle tower with tiny battlements on top of the head, a small golden crown perched on the battlements" "smug proud expression, chin up" "right")"
J[c_pest]="$(CH "a cheerful personified market town" "a red-and-white striped market-stall awning worn as a hat, a merchant's apron, holding a small bag of coins" "cheeky grin, one eyebrow raised" "left")"
J[c_obuda]="$(CH "a tiny personified old village" "a little terracotta cottage roof worn as a hat, a grey walrus moustache, leaning on a walking stick made from a small broken Roman stone column" "grumpy sulky frown" "left")"
J[c_count]="$(CH "a young 1820s Hungarian cavalry officer count" "dark blue hussar jacket with gold braided frogging, a fur-trimmed pelisse cape over one shoulder, a tall black hussar shako hat, a black mourning armband" "sad worried expression, eyebrows tilted up" "right")"
J[c_noble]="$(CH "a pompous 1840s nobleman" "tall black top hat, fur-collared long coat, a gold monocle, holding an ornate walking cane" "outraged shocked expression, mouth open" "right")"
J[c_toll]="$(CH "an 1840s bridge toll collector" "peaked cap, plain brown coat, a leather coin satchel, one hand held out palm up" "smug satisfied little smile" "left")"
for n in plate_aerial plate_river plate_toll c_buda c_pest c_obuda c_count c_noble c_toll; do
  [ -f "$n.png" ] && { echo "skip $n"; continue; }
  t0=$(date +%s)
  timeout 400 codex exec --skip-git-repo-check -s workspace-write "Use your built-in image generation tool to create ONE image and save it in the current directory as $n.png. Image: ${J[$n]} Do not do anything else." > "log_$n.txt" 2>&1
  echo "$n exit=$? $(( $(date +%s) - t0 ))s $( [ -f $n.png ] && echo OK || echo MISSING )"
done
echo ALLDONE
