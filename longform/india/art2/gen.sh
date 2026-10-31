#!/bin/bash
# India full video (ch2-13) art: same toy-figure template as ../art/gen.sh and russia/art/gen.sh.
# Revered religious figures (Buddha, Mahavira) and Shivaji appear only through archive art; living politicians only through real photos.
cd "$(dirname "$0")"
STYLE="Soft matte vinyl-toy texture, gentle studio lighting from the upper left, full body visible and centered"
CH() { echo "Single character cut-out on a fully transparent background: a cute chibi 3D figurine of $1, rounded pawn-shaped body with no visible legs (like a board-game piece), big round head, $2. Simple face: small black dot eyes and short eyebrows, $3. $STYLE, facing three-quarters to the $4. No ground, no shadow, no text. Portrait 1024x1536, transparent background PNG."; }
SC() { echo "A photoreal painterly scene of $1, large empty open ground in the lower middle of the frame (space for characters to be added later), no people, no animals, no text. Horizontal landscape 1536x1024, opaque PNG."; }
declare -A J
# ---- characters ----
J[c_guru]="$(CH "an ancient Vedic teacher from about 1000 BCE" "long grey beard, hair tied in a top knot, simple saffron cotton cloth draped over one shoulder, a string of brown rudraksha beads in one hand" "calm, patient half-smile" "right")"
J[c_student]="$(CH "a young Vedic student about twelve years old" "shaved head with a small tuft, plain white cotton wrap, sitting cross-legged" "sleepy, mid-yawn" "left")"
J[c_alexander]="$(CH "Alexander the Great in 326 BCE" "bronze Greek helmet with a tall white plume, red cloak, bronze breastplate, curly golden-brown hair" "curious, confident" "right")"
J[c_porus]="$(CH "King Porus of the Punjab in 326 BCE, very tall" "white turban with a gold band, a bandage on one arm, simple armour over a white tunic, thick black beard" "proud, calm, chin up" "left")"
J[c_chanakya]="$(CH "Chanakya, an ancient Indian Brahmin strategist" "shaved head with one long untied lock of hair at the back, plain white dhoti and shawl, holding a palm-leaf scroll" "sly knowing smile, one eyebrow raised" "right")"
J[c_minister]="$(CH "a junior minister of the Maurya court around 300 BCE" "neat white turban, light blue cotton robe, holding a very long rolled list that trails to the floor" "nervous, sweating" "left")"
J[c_chandragupta]="$(CH "Emperor Chandragupta Maurya around 320 BCE" "golden crown-like turban, deep red robe with gold border, pearl necklaces, a sword at his waist" "determined, confident" "right")"
J[c_ashoka]="$(CH "Emperor Ashoka around 260 BCE" "simple gold crown, white robe with a saffron shawl, holding a small wheel-shaped emblem with 24 spokes" "sad, thoughtful" "right")"
J[c_aryabhata]="$(CH "the ancient Indian astronomer Aryabhata around 500 CE" "white cotton robe, short beard, holding a palm-leaf manuscript and pointing upward" "excited, wide-eyed" "right")"
J[c_gupta_official]="$(CH "a Gupta court official around 500 CE" "orange turban, green robe, holding a small oil lamp" "confused, looking down at his own feet" "left")"
J[c_tughlaq]="$(CH "Sultan Muhammad bin Tughlaq around 1330" "tall white turban with a jewel, green brocade robe, trimmed black beard, sitting on a small throne" "cheerful, overconfident grin" "right")"
J[c_courtier]="$(CH "a Delhi Sultanate courtier around 1330" "small white cap, brown robe, holding a rolled map" "worried, eyebrows up" "left")"
J[c_babur]="$(CH "Emperor Babur around 1527" "Central Asian fur-trimmed cap, long green coat, small beard and moustache, holding a quill and a small diary" "gloomy, grumpy" "right")"
J[c_mughal_servant]="$(CH "a Mughal palace servant around 1600" "white turban, white kurta with a red waist sash, holding a silver tray" "polite, eager" "left")"
J[c_akbar]="$(CH "Emperor Akbar around 1580" "Mughal turban with a feather plume and jewel, rich orange and gold jama robe, moustache, pearl necklaces" "wise, curious" "right")"
J[c_shahjahan_old]="$(CH "the old Mughal emperor Shah Jahan around 1665" "white beard, simple white robe with a pale gold shawl, white turban, leaning on a cane" "sad, wistful" "right")"
J[c_director1]="$(CH "an 18th-century London East India Company director" "white powdered wig, dark blue frock coat with brass buttons, holding a quill" "relaxed, smug" "right")"
J[c_director2]="$(CH "a second 18th-century London East India Company director" "grey powdered wig, maroon frock coat, round spectacles, holding a large ledger" "shocked, eyebrows up" "left")"
J[c_victoria]="$(CH "Queen Victoria around 1870" "black dress with white lace collar, small diamond crown, grey hair in a bun" "pleased, slight smile" "right")"
J[c_br_minister]="$(CH "a Victorian British government minister" "black frock coat, tall top hat, mutton-chop whiskers, holding a red velvet cushion with a small crown" "nervous, sweating" "left")"
J[c_gandhi]="$(CH "Mahatma Gandhi in 1930, kind and dignified" "bald head, round wire spectacles, plain white khadi dhoti and shawl, holding a wooden walking stick in one hand and a pinch of salt in the other" "gentle, calm smile" "left")"
J[c_br_officer]="$(CH "a British police officer in India in 1930" "khaki uniform, khaki sun helmet, holding a small notebook and pencil" "stern, then nervous" "right")"
J[c_maharaja]="$(CH "an Indian maharaja in 1947" "jewelled turban with a feather, silk sherwani in deep purple, many pearl necklaces, sitting on a cushion" "grand, suspicious" "right")"
J[c_patel]="$(CH "Sardar Vallabhbhai Patel in 1947, respectful portrayal" "white dhoti and kurta, white shawl, bald head, holding a single sheet of paper" "calm, firm" "left")"
J[c_pilot]="$(CH "an Indian cargo pilot in 1991" "white pilot shirt with epaulettes, pilot cap, aviator sunglasses pushed up, holding a clipboard" "confused" "right")"
J[c_gov_official]="$(CH "an Indian government official in 1991" "white kurta, grey Nehru jacket, thick glasses, holding a file marked with a red ribbon" "worried, whispering" "left")"
# ---- sets ----
J[in_hermitage]="$(SC "a forest hermitage in the Ganga plain about 1000 BCE at dawn: a small thatched hut, a sacred fire burning in a brick altar, tall trees, morning mist, golden light")"
J[in_ganga]="$(SC "the Ganga river plain about 600 BCE: farmers' rice fields, a growing town with wooden walls on the river bank, boats on the wide river, warm evening light")"
J[in_bodhgaya]="$(SC "a peaceful Bihar countryside about 500 BCE: a large old peepal (fig) tree with a stone seat beneath it, a river beyond, soft dawn light, a sense of calm")"
J[in_jhelum]="$(SC "the bank of the Jhelum river in Punjab in 326 BCE after a battle: a Greek army tent with a red canopy, discarded shields and spears, distant war elephants, stormy monsoon sky")"
J[in_pataliputra]="$(SC "the Maurya capital Pataliputra about 300 BCE: tall wooden city walls with towers and a moat, wooden palaces with carved pillars, river Ganga beside it, clear morning")"
J[in_maurya_office]="$(SC "an office inside a Maurya palace about 300 BCE: carved wooden pillars, shelves of palm-leaf manuscripts, a low desk with an oil lamp, warm light")"
J[in_kalinga]="$(SC "a quiet battlefield in Kalinga (Odisha) in 261 BCE after the war: broken chariots and spears, smoke rising, a river, grey sky, sombre mood")"
J[in_observatory]="$(SC "a rooftop observatory in Gupta-era India about 500 CE at night: a brick terrace with simple stone instruments, a vast starry sky, the Milky Way, an oil lamp glowing")"
J[in_nalanda]="$(SC "Nalanda university about 600 CE: long red-brick monastery buildings with courtyards, terraces and stupas, students' rooms, green lawns, bright day")"
J[in_thanjavur]="$(SC "the Brihadeeswarar temple at Thanjavur around 1010 CE, newly built: a towering granite temple tower with carved tiers, a vast stone courtyard, blue sky")"
J[in_delhi_court]="$(SC "a Delhi Sultanate royal court around 1330: arched sandstone hall with Persian carpets, a raised throne platform, hanging lamps, warm light")"
J[in_hampi]="$(SC "the Vijayanagara capital Hampi around 1520: a busy stone bazaar street lined with pillared halls, giant granite boulders around, a temple tower in the distance, morning light")"
J[in_babur_camp]="$(SC "Babur's army camp near Delhi in 1526: rows of white tents, cannons, horses tied up, a low wooden writing table with a carpet, dusty afternoon light")"
J[in_fatehpur]="$(SC "Fatehpur Sikri around 1580: red sandstone palace courtyards and pavilions, arched halls, a large open courtyard, clear blue sky")"
J[in_agra_fort]="$(SC "a marble balcony of Agra Fort around 1665 at sunset, looking across the Yamuna river to the white Taj Mahal in the distance, warm golden light")"
J[in_surat_port]="$(SC "Surat port in Gujarat around 1650: European sailing ships at anchor, warehouses, bales of cotton and sacks of spices on a wooden dock, busy harbour, clear day")"
J[in_london_board]="$(SC "an 18th-century East India Company boardroom in London: dark wood panelling, a long table with giant ledgers and quills, a painted map of India on the wall, candlelight")"
J[in_meerut]="$(SC "an army cantonment in north India in 1857: white colonial barracks, a dusty parade ground, a flagpole, tense evening sky")"
J[in_victoria_palace]="$(SC "a Victorian palace study in London around 1870: dark red walls, gold-framed paintings, a writing desk with letters, tall windows, soft daylight")"
J[in_railway_1853]="$(SC "Bombay in 1853: an early steam locomotive with carriages at a simple platform, palm trees, colonial buildings, steam and smoke, morning light")"
J[in_dandi]="$(SC "Dandi beach in Gujarat in 1930 at dawn: a wide flat beach with white salt crust at the water's edge, gentle waves, a distant crowd silhouette on the horizon line only, soft pink sky")"
J[in_jallianwala]="$(SC "Jallianwala Bagh in Amritsar in 1919: an enclosed walled garden with high brick walls, a narrow entrance passage, an old well, sombre grey light")"
J[in_partition_train]="$(SC "a crowded railway station in Punjab in August 1947: an old steam train, luggage bundles and trunks on the platform, dusty heat haze, sombre mood")"
J[in_palace_hall]="$(SC "a princely state palace hall in 1947: marble floors, chandeliers, portraits of maharajas on the walls, silk cushions, afternoon light")"
J[in_parliament]="$(SC "the Constituent Assembly hall in New Delhi in 1949: a circular wood-panelled chamber with rows of green benches, a high dome, soft daylight")"
J[in_runway_1991]="$(SC "an Indian airport runway at night in 1991: a cargo plane with open loading ramp, metal crates on a trolley, floodlights, dark sky")"
J[in_bengaluru]="$(SC "modern Bengaluru tech park at golden hour: glass office towers, palm trees, a busy road with cars, warm evening light")"
ORDER="${!J[@]}"
for n in $(echo $ORDER | tr ' ' '\n' | sort); do
  [ -f "$n.png" ] && { echo "skip $n"; continue; }
  t0=$(date +%s)
  timeout 400 codex exec --skip-git-repo-check -s workspace-write "Use your built-in image generation tool to create ONE image and save it in the current directory as $n.png. Image: ${J[$n]} Do not do anything else." < /dev/null > "log_$n.txt" 2>&1
  echo "$n exit=$? $(( $(date +%s) - t0 ))s $( [ -f $n.png ] && echo OK || echo MISSING )"
done
echo ALLDONE
