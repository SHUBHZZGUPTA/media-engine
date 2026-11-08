#!/bin/bash
# India remake art (new scenes only): same toy-figure template as ../art/gen.sh and russia/art/gen.sh.
# Shubham's rule (31 Oct 2026): every REAL person and every deity appears only through real artwork or photos. Toy figures are for fictional/unnamed characters only.
cd "$(dirname "$0")"
STYLE="Soft matte vinyl-toy texture, gentle studio lighting from the upper left, full body visible and centered"
CH() { echo "Single character cut-out on a fully transparent background: a cute chibi 3D figurine of $1, rounded pawn-shaped body with no visible legs (like a board-game piece), big round head, $2. Simple face: small black dot eyes and short eyebrows, $3. $STYLE, facing three-quarters to the $4. No ground, no shadow, no text. Portrait 1024x1536, transparent background PNG."; }
SC() { echo "A photoreal painterly scene of $1, large empty open ground in the lower middle of the frame (space for characters to be added later), no people, no animals, no text. Horizontal landscape 1536x1024, opaque PNG."; }
declare -A J
# ---- characters (unnamed bystanders only; real people come from archive art) ----
J[c_convict]="$(CH "a Portuguese sailor-convict in 1498" "sunburnt face, messy dark hair and stubble, torn loose off-white linen shirt, rope belt, bare feet, clutching a small cloth bag" "out of breath, wide-eyed, nervous grin" "right")"
J[c_merchant]="$(CH "a North African merchant from Tunis in 1498" "white turban, long striped brown-and-cream robe, neat black beard, one hand raised in surprise" "shocked, mouth open" "left")"
J[c_scholar]="$(CH "a modern archaeologist and script scholar" "grey hair, round glasses, tweed jacket with elbow patches, holding a big magnifying glass" "squinting, puzzled" "right")"
J[c_greek_scribe]="$(CH "a Greek army scribe in 326 BCE" "short curly hair, plain white tunic with a blue border, holding a wax writing tablet and stylus" "whispering behind his hand, worried" "left")"
J[c_clerk_1830]="$(CH "a Bengali office clerk in Calcutta in the 1830s" "white dhoti and white kurta, thin moustache, holding a brass oil lamp" "sleepy, yawning" "left")"
J[c_rajput_general]="$(CH "a young Rajput army general in 1191" "orange safflower turban, curled moustache, chainmail over a red tunic, holding a tall spear" "eager, eyebrows raised" "left")"
J[c_jesuit]="$(CH "a Portuguese Jesuit priest at the Mughal court in 1580" "black cassock, small black skullcap, short brown beard, holding a closed book" "indignant, pointing a finger" "left")"
J[c_assistant_1947]="$(CH "a young British civil service assistant in Delhi in 1947" "white short-sleeved shirt, loosened tie, sweat patches, holding a thick stack of census papers" "anxious" "left")"
# ---- sets ----
J[in_calicut_1498]="$(SC "the busy seaside market of Calicut on India's Malabar coast in 1498: open-fronted wooden shops with sloping tiled roofs, sacks of black pepper and ginger, bolts of brightly painted cotton cloth hanging up, coconut palms, a Portuguese sailing ship anchored in the bay, bright midday sun")"
J[in_museum_study]="$(SC "a cluttered modern archaeology study at night: a wooden desk under a green banker's lamp, trays of small square Indus stone seals, enlarged photos of the seals pinned to the wall, stacks of books")"
J[in_calcutta_study]="$(SC "a scholar's study in British Calcutta in the 1830s at night: a heavy wooden desk covered in paper rubbings of ancient inscriptions, an oil lamp, shuttered tall windows, a punkah fan hanging from the ceiling")"
J[in_rajput_camp]="$(SC "a Rajput army camp near Tarain in north India in 1191 after a victory: colourful tents with flags, horses tied in a row, a distant dusty battlefield, golden late-afternoon light")"
J[in_delhi_office_1947]="$(SC "a hot government office in Delhi in the summer of 1947: a slow ceiling fan, a large desk buried in maps of Punjab and Bengal, wooden filing cabinets, harsh sunlight through blinds")"
ORDER="${!J[@]}"
for n in $(echo $ORDER | tr ' ' '\n' | sort); do
  [ -f "$n.png" ] && { echo "skip $n"; continue; }
  t0=$(date +%s)
  timeout 400 codex exec --skip-git-repo-check -s workspace-write "Use your built-in image generation tool to create ONE image and save it in the current directory as $n.png. Image: ${J[$n]} Do not do anything else." < /dev/null > "log_$n.txt" 2>&1
  echo "$n exit=$? $(( $(date +%s) - t0 ))s $( [ -f $n.png ] && echo OK || echo MISSING )"
done
echo ALLDONE
