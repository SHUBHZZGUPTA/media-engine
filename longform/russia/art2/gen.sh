#!/bin/bash
# Russia full video: new characters + sets (same style as ../art/gen.sh). Usage: gen.sh [--print]
cd "$(dirname "$0")"
STYLE="Soft matte vinyl-toy texture, gentle studio lighting from the upper left, full body visible and centered"
CH() { echo "Single character cut-out on a fully transparent background: a cute chibi 3D figurine of $1, rounded pawn-shaped body with no visible legs (like a board-game piece), big round head, $2. Simple face: small black dot eyes and short eyebrows, $3. $STYLE, facing three-quarters to the $4. No ground, no shadow, no text. Portrait 1024x1536, transparent background PNG."; }
SC() { echo "A photoreal painterly scene of $1, large empty open ground in the lower middle of the frame (space for characters to be added later), no people, no animals, no text. Horizontal landscape 1536x1024, opaque PNG."; }
declare -A J
# ---- characters ----
J[c_prince_kneel]="$(CH "a 13th-century Russian prince" "fur-trimmed red kaftan, small fur cap, bowing low and holding out a small wooden gift box with both hands" "nervous, eyebrows up" "right")"
J[c_servant]="$(CH "a 16th-century Kremlin palace servant" "plain long brown kaftan, bowl haircut, holding a lit candle, shoulders hunched" "timid, nervous" "left")"
J[c_false_dmitry]="$(CH "a young early-17th-century pretender to the Russian throne" "fine red Polish-style coat with gold buttons, short reddish hair, a small wart on one cheek, one hand on his chest" "grand, overconfident smile" "right")"
J[c_polish_noble]="$(CH "an early-17th-century Polish nobleman" "long crimson coat with a wide patterned silk sash, fur hat with a feather, shaved head with a long drooping moustache" "doubtful, one eyebrow raised" "left")"
J[c_peter_worker]="$(CH "Tsar Peter the Great disguised as a shipyard carpenter, very tall and thin" "plain white linen shirt with rolled sleeves, leather work apron, small dark moustache, holding a wooden mallet" "casual, trying to look innocent" "right")"
J[c_dutch_foreman]="$(CH "a 17th-century Dutch shipyard foreman" "wide-brimmed black hat, white collar, brown work coat, holding a small wooden writing board with papers" "squinting upwards, suspicious" "left")"
J[c_catherine]="$(CH "Empress Catherine the Great as a young woman in 1762" "powdered grey-white hair, pale blue silk gown with a wide red sash and a small jewelled crown" "calm, confident smile" "right")"
J[c_guard_officer]="$(CH "an 18th-century Russian imperial guards officer" "dark green coat with red cuffs, black tricorn hat, white cross-belt, sword at the hip" "serious, conspiratorial" "left")"
J[c_napoleon]="$(CH "Napoleon Bonaparte" "black bicorne hat worn sideways, grey greatcoat over a blue uniform with gold buttons, one hand tucked into his waistcoat" "impatient frown" "right")"
J[c_french_aide]="$(CH "a French army aide of 1812" "tall black shako hat, blue uniform with white cross-belts, holding a tall stack of letters tied with ribbon" "worried, sweating" "left")"
J[c_nicholas2]="$(CH "Tsar Nicholas the Second" "neat short brown beard and moustache, plain olive military tunic with a few medals, peaked cap" "gentle, mild smile" "right")"
J[c_admiral]="$(CH "a Russian navy admiral of 1904" "white beard, dark navy coat with gold epaulettes, peaked admiral's cap, holding a brass telescope" "stern, peering" "left")"
J[c_sailor_ru]="$(CH "a young Russian navy sailor of 1904" "blue-and-white striped shirt, dark flat sailor cap with two ribbons" "panicking, eyes wide" "right")"
J[c_rasputin]="$(CH "the Russian mystic Grigori Rasputin" "long straggly dark hair and a long dark beard, black peasant robe with a belt, a simple cross on a chain" "intense, staring eyes" "right")"
J[c_lenin]="$(CH "the revolutionary Vladimir Lenin" "bald head, short reddish goatee and moustache, dark three-piece suit with a red ribbon on the lapel, holding a flat cap" "determined, pointing forward" "right")"
J[c_comrade]="$(CH "a young Bolshevik party comrade of 1917" "black leather jacket, flat cap, red armband, holding a small notebook and pencil" "earnest, slightly confused" "left")"
J[c_official]="$(CH "a stern 1930s Soviet secret-police official" "khaki tunic, peaked cap with a dark blue top and red band, holding up a black-and-white photograph" "cold, suspicious stare" "right")"
J[c_photo_editor]="$(CH "a nervous 1930s Soviet photo retoucher" "round wire glasses, white shirt with sleeve garters and a vest, holding a tiny paintbrush" "forced nervous smile, sweating" "left")"
J[c_guard_a]="$(CH "a 1950s Soviet palace guard" "khaki uniform with a peaked cap and red shoulder boards, holding his cap nervously" "frightened, whispering" "right")"
J[c_guard_b]="$(CH "a second 1950s Soviet palace guard, shorter and rounder" "khaki uniform, fur ushanka hat with a red star" "anxious, eyebrows up" "left")"
J[c_sub_captain]="$(CH "a 1962 Soviet submarine captain" "dark navy sweater, navy officer's cap, sweat drops on his forehead" "panicking, shouting" "right")"
J[c_arkhipov]="$(CH "a calm 1962 Soviet navy officer" "dark navy uniform with officer's cap, neatly combed dark hair, arms folded" "calm, steady, slight smile" "left")"
# ---- sets ----
J[ru_mongol_tent]="$(SC "the inside of a grand 13th-century Mongol khan's tent: round felt walls, rich red and gold carpets, a low throne covered in furs, brass lamps, warm light")"
J[ru_kremlin_night]="$(SC "a dark 16th-century Moscow Kremlin throne room at night: painted vaulted ceiling with gold patterns, a single carved throne, flickering candles, deep shadows")"
J[ru_polish_hall]="$(SC "an early-17th-century Polish palace hall: tall windows, red damask walls, oil portraits, a long table, bright daylight")"
J[ru_dutch_shipyard]="$(SC "a busy 1690s Dutch shipyard: a half-built wooden sailing ship on slipways, timber piles, ropes, a windmill and a canal in the background, grey sky")"
J[ru_palace_room]="$(SC "an elegant 18th-century Saint Petersburg palace room: white and gold walls, a writing desk with candles and papers, tall window with blue evening light")"
J[ru_moscow_fire]="$(SC "an empty palace room in the Moscow Kremlin in 1812: grand windows showing the city burning outside with orange smoke, scattered papers on a table")"
J[ru_snow_retreat]="$(SC "a vast frozen Russian plain in a blizzard: deep snow, dead trees, an abandoned cannon and broken wagon half-buried in snow, grey-blue light")"
J[ru_ship_deck]="$(SC "the foggy night deck of a 1904 battleship: steel rails, a big gun turret, ropes and a lantern glowing in thick fog over a dark sea")"
J[ru_backroom]="$(SC "a smoky 1917 back room in Petrograd: bare plaster walls, a wooden table covered in pamphlets and maps, a single hanging bulb, red banners rolled up in a corner")"
J[ru_photo_lab]="$(SC "a 1930s Soviet photo darkroom: red safelight, photographs drying on lines, trays of chemicals, a retouching desk with a magnifier")"
J[ru_corridor]="$(SC "a dim 1950s Soviet dacha corridor: wood panelled walls, a red carpet runner, a tall closed wooden door at the end, a single wall lamp")"
J[ru_submarine]="$(SC "the cramped control room of a 1960s Soviet diesel submarine lit in red emergency light: pipes, valves, gauges, a periscope column, condensation dripping")"
J[ru_red_square]="$(SC "Red Square in Moscow on a bright winter day: Saint Basil's Cathedral with its colourful onion domes on the right, the red Kremlin wall on the left, snow on the cobblestones")"
J[ru_spb_build]="$(SC "Saint Petersburg being built in 1704: a marshy river bank by the wide Neva, wooden scaffolding, a half-built stone fortress with a thin golden spire, piles of logs, misty morning")"
J[ru_soviet_shop]="$(SC "a 1980s Soviet grocery shop: long counter, almost empty shelves with a few identical jars, a cash register, flat fluorescent light")"
J[ru_steppe]="$(SC "the endless green Eurasian steppe under a huge sky, a row of round white Mongol yurts in the distance, wind in the grass")"
ORDER="c_prince_kneel c_servant c_false_dmitry c_polish_noble c_peter_worker c_dutch_foreman c_catherine c_guard_officer c_napoleon c_french_aide c_nicholas2 c_admiral c_sailor_ru c_rasputin c_lenin c_comrade c_official c_photo_editor c_guard_a c_guard_b c_sub_captain c_arkhipov ru_mongol_tent ru_kremlin_night ru_polish_hall ru_dutch_shipyard ru_palace_room ru_moscow_fire ru_snow_retreat ru_ship_deck ru_backroom ru_photo_lab ru_corridor ru_submarine ru_red_square ru_spb_build ru_soviet_shop ru_steppe"
if [ "$1" = "--print" ]; then for n in $ORDER; do echo "$n|${J[$n]}"; done; exit; fi
for n in ${ONLY:-$ORDER}; do
  [ -f "$n.png" ] && { echo "skip $n"; continue; }
  t0=$(date +%s)
  timeout 400 codex exec --skip-git-repo-check -s workspace-write "Use your built-in image generation tool to create ONE image and save it in the current directory as $n.png. Image: ${J[$n]} Do not do anything else." < /dev/null > "log_$n.txt" 2>&1
  echo "$n exit=$? $(( $(date +%s) - t0 ))s $( [ -f $n.png ] && echo OK || echo MISSING )"
done
echo ALLDONE
