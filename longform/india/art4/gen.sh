#!/bin/bash
# India remake art batch 4 (storyboard gaps, 13 Nov 2026): same toy-figure/scene template as ../art3/gen.sh.
# Rule: every REAL person appears only through real artwork or photos. Toy figures are for unnamed people only; sets have no people.
cd "$(dirname "$0")"
STYLE="Soft matte vinyl-toy texture, gentle studio lighting from the upper left, full body visible and centered"
CH() { echo "Single character cut-out on a fully transparent background: a cute chibi 3D figurine of $1, rounded pawn-shaped body with no visible legs (like a board-game piece), big round head, $2. Simple face: small black dot eyes and short eyebrows, $3. $STYLE, facing three-quarters to the $4. No ground, no shadow, no text. Portrait 1024x1536, transparent background PNG."; }
SC() { echo "A photoreal painterly scene of $1, large empty open ground in the lower middle of the frame (space for characters to be added later), no people, no text. Horizontal landscape 1536x1024, opaque PNG."; }
BD() { echo "A bold, colourful painterly illustration of $1, centred subject, clean uncluttered background, no people, no letters, no words, no numbers, no text of any kind. Horizontal landscape 1536x1024, opaque PNG."; }
declare -A J
J[c_servant_ancient]="$(CH "an ancient Indian camp servant in 320 BCE" "plain off-white cotton dhoti and shawl, shaved head with a small tuft, holding a wooden comb" "nervous, eyebrows raised" "left")"
J[c_citizen]="$(CH "an ordinary Delhi townsman in 1327" "simple white cotton tunic and loose trousers, small white cap, carrying a big cloth bundle on his back" "dismayed, one hand raised" "left")"
J[in_palace_lumbini]="$(SC "a perfect sunlit palace garden in the Himalayan foothills 2,500 years ago: white pavilions with wooden pillars, lotus pools, flowering trees, distant snowy mountains, everything bright and flawless")"
J[in_four_sights]="$(SC "a dusty village road just outside an ancient Indian palace gate 2,500 years ago, late afternoon: on the left a lone wooden walking stick leaning on a wall, a simple sickbed mat in a doorway, a small cloth-wrapped funeral bier on a bamboo frame by the road, and a monk's saffron robe and begging bowl on a stone, no people")"
J[in_forest_camp_night]="$(SC "a hidden forest camp in ancient India at night: a small campfire, a lean-to of branches, practice swords and a shield leaning on a tree trunk, moonlight through tall sal trees")"
J[board_chaturanga]="$(BD "an ancient Indian chaturanga game: an 8x8 wooden board seen at a low angle, carved wooden pieces shaped as elephants, chariots, horses and foot soldiers in red and green, warm lamplight")"
J[golden_bird]="$(BD "a radiant golden bird with spread wings, made of gold leaf and jewels, gliding over a soft blue-green map of the Indian subcontinent, warm sunrise glow")"
J[in_camel_caravan]="$(SC "a long camel caravan heading away through a rocky Afghan mountain pass around the year 1000, camels heavily loaded with chests and sacks spilling gold coins and jewels, dust in the evening sun, the caravan small in the middle distance")"
J[in_home_mint]="$(SC "a village courtyard in 14th-century north India at dusk: several small clay furnaces glowing orange, clay coin moulds, a blacksmith's anvil, heaps of shiny copper coins in baskets, no people")"
J[in_panipat]="$(SC "the battlefield of Panipat in 1526: thick white cannon smoke rolling across a dusty plain, wheeled bronze cannons in the foreground behind tied carts, war elephants in the far distance turning and stampeding away, dramatic sky")"
J[in_library_stairs]="$(SC "a steep narrow stone staircase inside a red-sandstone Mughal library tower in 1556, scattered books and a fallen turban on the steps, evening light from a small arched window")"
J[in_mughal_library]="$(SC "a grand Mughal library in 1570: shelves of leather-bound manuscripts, a low reading platform with silk cushions, an open illuminated book on a carved wooden stand, warm lamplight, no people")"
J[in_sweet_baskets]="$(SC "the courtyard gate of a Mughal mansion in Agra in 1666 at dusk: a row of huge woven wicker baskets piled with round Indian sweets, carrying poles beside them, one basket lid slightly open, guards' spears leaning by the gate, no people")"
J[board_ledger]="$(BD "a huge open 18th-century merchant ledger with neat columns of ink, a feather quill in an inkpot, brass scales and a small stack of silver coins on a dark wooden table")"
J[board_company_army]="$(BD "an enormous army of 18th-century Indian sepoy soldiers in red coats and white turbans standing in endless ranks on a plain, seen from above, with one tiny British flag on a small pole in the foreground for scale")"
J[in_pietermaritzburg]="$(SC "an empty railway station platform at Pietermaritzburg, South Africa, on a cold winter night in 1893: gas lamps, a steam train pulling away in the background, a single leather suitcase and a hat lying on the platform, no people")"
J[in_waiting_room]="$(SC "a cold, dim, empty railway station waiting room in 1893 at night: a hard wooden bench, a single flickering oil lamp, frosty window, an overcoat left on the bench, no people")"
J[board_symbols]="$(BD "a row of large painted election symbols on a white wall in 1951 India: a pair of bullocks with a yoke, an oil lamp, a hut, a tree and a spinning wheel, simple flat shapes, no letters")"
J[in_green_fields]="$(SC "golden wheat fields in Punjab in the late 1960s at sunrise, a tube well pumping water into an irrigation channel, a red tractor parked at the edge, no people")"
J[board_licence_raj]="$(BD "a towering stack of government permit files tied with red tape, rubber stamps and an ink pad on a cluttered 1980s Indian office desk, a ceiling fan blurred above")"
ORDER="${!J[@]}"
for n in $(echo $ORDER | tr ' ' '\n' | sort); do
  [ -f "$n.png" ] && { echo "skip $n"; continue; }
  t0=$(date +%s)
  timeout 400 codex exec --skip-git-repo-check -s workspace-write "Use your built-in image generation tool to create ONE image and save it in the current directory as $n.png. Image: ${J[$n]} Do not do anything else." < /dev/null > "log_$n.txt" 2>&1
  echo "$n exit=$? $(( $(date +%s) - t0 ))s $( [ -f $n.png ] && echo OK || echo MISSING )"
done
echo ALLDONE
