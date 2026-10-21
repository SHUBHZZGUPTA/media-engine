#!/bin/bash
# Painted plates via Codex built-in image generation (ChatGPT plan). Usage: ./gen.sh name [name...]
cd /home/claude/mm-work/plates
STYLE="Cinematic painterly illustration for a dark, mysterious history documentary: rich oil-painting texture, chiaroscuro lighting with warm amber-gold highlights against deep navy-blue shadows, muted desaturated palette, light haze, shallow depth of field, composed like a film still with the main subject slightly off-centre and calm darker space in the lower third for captions. No text, no letters, no numbers, no writing, no logos, no watermarks, no signatures, no borders. No recognizable real people; any people are anonymous, seen from behind, in silhouette or partly in shadow. Landscape 1536x1024, opaque PNG."
declare -A J
J[wallet_desk]="A worn brown leather wallet lying open on a dark wooden desk at night, a single paper banknote half pulled out of it, lit by one warm desk lamp from the left, dust floating in the lamplight, deep shadows around."
J[barter_market]="An ancient Near-Eastern open-air market at dusk around 700 BC: a farmer holding a pair of chickens faces a goat herder with a goat, both arguing with frustrated gestures, baskets and clay jars around, warm torchlight and long shadows."
J[lydia_mint]="An ancient Lydian workshop around 600 BC lit by a glowing furnace: a craftsman's hands striking small lumps of pale gold-silver electrum on an anvil with a hammer and a punch, sparks flying, a few small stamped coin-lumps on the anvil, smoke and firelight."
J[chengdu_market]="A crowded street market in Song-dynasty China around the year 1000, at dusk with lanterns: merchants in robes struggling under very heavy long strings of dark iron coins carried on shoulder poles, wooden shopfronts with tiled roofs, misty atmosphere."
J[deposit_shop]="Interior of a small Song-dynasty Chinese deposit shop at night lit by paper lanterns: across a wooden counter, a merchant hands over heavy strings of iron coins and receives a single folded paper slip in return, shelves stacked with strings of coins behind."
J[song_printing]="A Song-dynasty Chinese workshop printing paper money: wooden printing blocks, ink, and growing tall stacks of freshly printed blank paper notes hanging to dry on lines, workers in silhouette, candlelight, an atmosphere of excess."
J[bank_vault_1700s]="An 18th-century London bank vault by candlelight: stone arches, iron-bound wooden chests, neat stacks of gold bars and piles of gold coins on shelves, a clerk's silhouette holding a candle at the far end."
J[tv_1971]="An American living room at night in 1971: a family seen from behind in silhouette on a sofa watching a glowing wood-cabinet television, the screen only a bright blank glow, lamp light, wood panelling, a sense of an important announcement."
J[gold_window]="A heavy bank teller window with brass bars being slammed shut, a rolling metal shutter coming down over it, behind the bars a dimly lit vault with stacks of gold bars, 1970s style, dramatic moody lighting."
J[gold_cube]="A single gigantic solid gold cube, about seven storeys tall, standing alone in the middle of a wide empty city plaza at dusk, tiny anonymous people at its base for scale, its surface reflecting a stormy navy sky and warm streetlights."
J[central_bank]="A grand neoclassical central bank building at night in the rain, columns lit from below, heavy iron chains wrapped around the columns as if locked, wet reflective pavement, a few umbrellas in silhouette."
J[oil_tanker]="A huge oil tanker on a calm sea at sunset off a desert coastline, oil-field flares burning on the shore, heat haze, golden sky fading into deep blue."
J[trading_room]="A vast modern currency trading floor at night seen from above: rows of glowing screens with abstract charts (no readable text), traders in silhouette, cool blue light with warm gold accents."
for n in "$@"; do
  [ -f "$n.png" ] && { echo "skip $n"; continue; }
  t0=$(date +%s)
  timeout 420 codex exec --skip-git-repo-check -s workspace-write "Use your built-in image generation tool to create ONE image and save it in the current directory as $n.png. Image: ${J[$n]} $STYLE Do not do anything else." < /dev/null > "log_$n.txt" 2>&1
  echo "$n exit=$? $(( $(date +%s) - t0 ))s $( [ -f $n.png ] && echo OK || echo MISSING )"
done
