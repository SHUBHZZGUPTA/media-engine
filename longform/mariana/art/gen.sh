#!/bin/bash
# Mariana Trench art (hybrid: real NOAA photos elsewhere). Same toy-figure template as russia/art/gen.sh.
cd "$(dirname "$0")"
STYLE="Soft matte vinyl-toy texture, gentle studio lighting from the upper left, full body visible and centered"
CH() { echo "Single character cut-out on a fully transparent background: a cute chibi 3D figurine of $1, $2. Simple face: small black dot eyes and short eyebrows, $3. $STYLE, facing three-quarters to the $4. No ground, no shadow, no text. Portrait 1024x1536, transparent background PNG."; }
SC() { echo "A photoreal painterly scene of $1, large empty open space in the lower middle of the frame (space for characters to be added later), no people, no text. Horizontal landscape 1536x1024, opaque PNG."; }
CUT() { echo "A painterly, cinematic educational cutaway illustration (side cross-section view, like a high-end science documentary graphic) of $1. Rich deep-ocean blues, dramatic lighting, realistic textures. Absolutely no text, no labels, no arrows with words, no people. Horizontal landscape 1536x1024, opaque PNG."; }
declare -A J
J[c_snailfish]="$(CH "a deep-sea snailfish" "small pale pink, slightly translucent soft jelly-like body with a big round head, tapering tadpole-like tail, tiny fins, a faint glow" "cheerful happy grin" "right")"
J[c_amphipod]="$(CH "a giant deep-sea amphipod (a pale shrimp-like crustacean)" "curved segmented pale cream-white shell, many small legs, two long antennae, comically big and chunky" "proud booming grin, chest puffed out" "left")"
J[mt_surface]="$(SC "the open western Pacific Ocean at night under a starry sky, calm dark waves, a small white research ship with deck lights in the distance, moonlight on the water")"
J[mt_twilight]="$(SC "deep blue underwater twilight about 200 metres down: faint shafts of sunlight fading from above, a few small silvery fish, colours fading to deep blue")"
J[mt_midnight]="$(SC "the pitch-black deep ocean at 1,000 metres: glowing blue bioluminescent jellyfish, sparks of light from tiny creatures, and the faint glowing lure of an anglerfish in the distance")"
J[mt_floor]="$(SC "the muddy floor of the deepest ocean trench, nearly 11 km down, lit by two bright submarine spotlights from above: fine grey silt drifting, soft sediment, total darkness beyond the light")"
J[mt_plastic]="$(SC "the muddy floor of the deepest ocean trench lit by submarine spotlights, with a single crumpled plastic bag half-buried in the grey silt in the centre, eerie and lonely mood")"
J[mt_champagne]="$(SC "a deep-sea volcanic vent on a dark rocky seamount: a stream of shiny silvery-white droplets of liquid carbon dioxide rising like champagne bubbles from cracks in the rock, pale mussels and white bacterial mats around the vent")"
J[mt_trieste]="$(SC "a vintage 1960 bathyscaphe deep-sea vessel (a long grey cigar-shaped float with a small steel crew sphere hanging underneath) slowly sinking through dark blue water, a beam of light from its lamp, bubbles rising, vehicle only")"
J[mt_everest]="$(CUT "Mount Everest placed inside the Mariana Trench: the whole snowy mountain sitting in the deep V-shaped trench with about two kilometres of dark blue ocean still above its summit, the sea surface at the top of the frame")"
J[mt_plates]="$(CUT "an ocean subduction zone: a thick oceanic plate bending and diving under another plate, forming a deep narrow trench on the sea floor, the glowing orange mantle below, a chain of volcanic islands on the upper plate")"
J[mt_water]="$(CUT "seawater being carried into the Earth at an ocean trench: the bending ocean plate is cracked, blue seawater seeps down into the cracks and soaked rock, the wet plate carries the blue water deep down into the orange mantle, and nearby a volcano on the sea floor releases plumes back into the ocean")"
ORDER="c_snailfish c_amphipod mt_surface mt_twilight mt_midnight mt_floor mt_plastic mt_champagne mt_trieste mt_everest mt_plates mt_water"
for n in ${@:-$ORDER}; do
  [ -f "$n.png" ] && { echo "skip $n"; continue; }
  t0=$(date +%s)
  timeout 400 codex exec --skip-git-repo-check -s workspace-write "Use your built-in image generation tool to create ONE image and save it in the current directory as $n.png. Image: ${J[$n]} Do not do anything else." < /dev/null > "log_$n.txt" 2>&1
  echo "$n exit=$? $(( $(date +%s) - t0 ))s $( [ -f $n.png ] && echo OK || echo MISSING )"
done
echo ALLDONE
