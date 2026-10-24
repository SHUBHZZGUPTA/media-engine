#!/bin/bash
cd "$(dirname "$0")"
STYLE="Soft matte vinyl-toy texture, gentle studio lighting from the upper left, full body visible and centered"
CH() { echo "Single character cut-out on a fully transparent background: a cute chibi 3D figurine of $1, rounded pawn-shaped body with no visible legs (like a board-game piece), big round head, $2. Simple face: small black dot eyes and short eyebrows, $3. $STYLE, facing three-quarters to the $4. No ground, no shadow, no text. Portrait 1024x1536, transparent background PNG."; }
SC() { echo "A photoreal painterly scene of $1, large empty open ground in the lower middle of the frame (space for characters to be added later), no people, no animals, no text. Horizontal landscape 1536x1024, opaque PNG."; }
declare -A J
J[c_traveller]="$(CH "a curious young time-traveller" "brass aviator goggles pushed up on the forehead, messy brown hair, a worn olive-green explorer jacket with many pockets, a red scarf, holding an oversized golden pocket watch on a chain" "cheeky excited grin" "right")"
J[c_slav_elder1]="$(CH "an early-medieval East Slav village elder" "long white beard, plain linen tunic with red embroidered collar, fur hat, holding a sheet of birch bark and a stylus" "serious, dictating" "right")"
J[c_slav_elder2]="$(CH "an early-medieval East Slav villager" "brown beard, belted wool tunic, bowl haircut" "horrified, eyebrows up" "left")"
J[c_slav_elder3]="$(CH "a young early-medieval East Slav villager" "short beard, simple grey tunic, straw-coloured hair" "hopeful, shy" "left")"
J[c_rurik]="$(CH "a 9th-century Viking chieftain" "round iron helmet without horns, red braided beard, fur-trimmed cloak, round wooden shield on the back" "confident smirk" "left")"
J[c_olga]="$(CH "a 10th-century Kyivan princess" "embroidered red-and-gold robe, white veil under a small golden crown" "sweet smile with narrowed, scheming eyes" "left")"
J[c_drevlian]="$(CH "a 10th-century forest-tribe envoy" "rough brown wool cloak, fur cap, holding a small gift box" "eager, bowing politely" "right")"
J[c_vladimir]="$(CH "a 10th-century Kyivan grand prince" "fur-trimmed crimson cloak, pointed golden crown with a fur rim, seated pose on a small throne" "sceptical, one eyebrow raised" "right")"
J[c_byz_envoy]="$(CH "a 10th-century Byzantine envoy" "purple-and-gold silk robe, small round cap, holding a tiny model of a domed church" "excited whisper, hand by mouth" "left")"
J[c_khan]="$(CH "a 13th-century Mongol khan" "fur-trimmed conical helmet, lamellar armour, bow on the back" "fierce frown" "left")"
J[c_ivan4]="$(CH "Tsar Ivan the Terrible" "dark robe, fur-rimmed Monomakh-style crown, long dark beard, holding a staff" "glaring, intense" "right")"
J[c_peter1]="$(CH "Tsar Peter the Great, very tall and thin" "green 18th-century military coat, tricorn hat, holding a large pair of scissors" "determined grin" "right")"
J[ru_rivers]="$(SC "an endless early-medieval Russian landscape of dark pine forest, marshes and winding silver rivers under a pale sky, seen from a low hill")"
J[ru_cabin]="$(SC "the interior of a 9th-century Slavic log cabin: rough log walls, a clay stove with a fire, a heavy wooden table in the middle, warm firelight")"
J[ru_novgorod]="$(SC "a 9th-century wooden trading town on a wide river: log palisade walls, wooden houses, Viking longships moored at a wooden pier, grey northern sky")"
J[ru_kyiv]="$(SC "10th-century Kyiv on high green hills above the wide Dnieper river: wooden walls, a wooden fortress, river boats loaded with furs, summer light")"
J[ru_dock]="$(SC "a wooden river dock beside a small medieval wooden town in a forest, calm river, a simple wooden boat tied up, golden afternoon light")"
J[ru_bathhouse]="$(SC "a small 10th-century wooden Slavic bathhouse with a smoking chimney in a forest clearing at dusk, door closed, ominous mood")"
J[ru_hall]="$(SC "the interior of a 10th-century Kyivan prince's great hall: carved wooden pillars, red and gold banners, a wooden throne on a low dais")"
J[ru_constantinople]="$(SC "the skyline of 10th-century Constantinople from the sea: the huge dome of Hagia Sophia, golden morning light, ships in the harbour")"
ORDER="c_traveller c_slav_elder1 c_slav_elder2 c_slav_elder3 c_rurik c_olga c_drevlian c_vladimir c_byz_envoy c_khan c_ivan4 c_peter1 ru_rivers ru_cabin ru_novgorod ru_kyiv ru_dock ru_bathhouse ru_hall ru_constantinople"
for n in $ORDER; do
  [ -f "$n.png" ] && { echo "skip $n"; continue; }
  t0=$(date +%s)
  timeout 400 codex exec --skip-git-repo-check -s workspace-write "Use your built-in image generation tool to create ONE image and save it in the current directory as $n.png. Image: ${J[$n]} Do not do anything else." < /dev/null > "log_$n.txt" 2>&1
  echo "$n exit=$? $(( $(date +%s) - t0 ))s $( [ -f $n.png ] && echo OK || echo MISSING )"
done
echo ALLDONE
