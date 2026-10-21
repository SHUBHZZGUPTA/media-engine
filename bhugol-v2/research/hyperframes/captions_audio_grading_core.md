# HyperFrames 0.8.181: audit of reusable media, caption, audio, grading, core and CLI items

Scope: skills source at `scratchpad/hf-src/skills/` (abbreviated `S/` below) plus `npx hyperframes <cmd> --help` and the installed CLI at
`/home/claude/work/node_modules/hyperframes/dist/` (abbreviated `D/`). Nothing was modified. No model downloads were run.
The only non-help command run was `media-treatment --capabilities/--capability`, which reads a static catalog.

Feasibility is judged against our pipeline: 1080x1920 at 30fps, a single index.html, GSAP, three.js under SwiftShader, no network at
render time, an external Python music/SFX mix, and ffmpeg mux.

Network notes for the workspace (it reaches npm, pip and raw.githubusercontent.com only):
- These need a GitHub Actions fetch: `static.heygen.ai`, `api.openverse.org`, huggingface.co, and GitHub *release* assets (Kokoro, u2net).
- The registry is reachable: `raw.githubusercontent.com/heygen-com/hyperframes/main/registry` (`S/hyperframes-registry/SKILL.md`).

---

## 1. Master table of reusable items

Column key: **Area** = captions / audio / grading / treatment / core / cli. **Feas.**: W = Works, T = Test needed, B = Blocked.
**Eff.** = effort (S/M/L). **Val.** = retention or quality value (H/M/L).
Channel key: Geo = geography, Hor = horror, Fin = finance/scams, Tech = tech news, AIH = AI history, Kids = kids education, Cart = 2D cartoon.

| # | Item | Area | Path / command | What it does | Feas. | Eff. | Val. | Best for |
|---|------|------|----------------|--------------|-------|------|------|----------|
| 1 | Bundled SFX library (21 mp3) | audio | `D/skills/media-use/audio/assets/sfx/` + `manifest.json` | Ships riser (10.03 s, peak at end), whoosh / whoosh-short / whoosh-cinematic, impact-bass-1/2, glitch-1/2/3, typing, key-press, pop, ping, chime, sparkle, notification, error, click / click-soft. Each has a duration and a usage note. | W: already on disk; Pixabay licence, commercial use, no attribution (`CREDITS.md`) | S | M | All. glitch suits Tech/Hor; typing suits Fin/Tech; impact suits Geo hooks |
| 2 | Manifest cue rules | audio | `S/media-use/audio/references/sfx.md`, `manifest.json` | Timing rules such as "riser at climax−10.03 s", "whoosh-cinematic swell peaks on the cut", "impact decay J-cuts into the next shot", plus SFX at volume about 0.35 under voice. | W: rules port straight into our score script | S | M | All |
| 3 | Openverse SFX retrieval | audio | `npx hyperframes media-use resolve --type sfx --intent "glass shatter"` | Searches CC0/CC-BY Freesound clips and writes CREDITS.md. Limit is 20 searches/min and 200/day. | B in workspace (api.openverse.org). T via GH Actions, freezing files into the repo | M | M | Hor (creaks, drones), Geo (ambience) |
| 4 | Voiceover carve | audio | `data-fx-carve` on the bed; `node S/hyperframes-audio/scripts/carve.mjs --comp index.html` | Spectral duck: cuts 6 bands of the bed (250 Hz to 2.5 kHz, about 7 dB, 15 dB at 1.6 kHz) plus a slow level envelope that follows the voice. | T: needs narration and music as **separate placed `<audio>` tracks**, `npm i -D @hyperframes/core`, and ffmpeg. Not usable on mix_norm.wav | M | H | All narrated channels |
| 5 | `data-fx-chain` effects (per track) | audio | `S/hyperframes-audio/references/attributes.md`, `fx-registry.md` | Web Audio chain run in an OfflineAudioContext at render: highpass/lowpass/peaking/shelves, compressor, limiter, truepeak, gate, saturate, delay, reverb, chorus, phaser, bitcrush. | T: works on any placed `<audio>`, including mix_norm.wav. Means HyperFrames muxes the audio instead of ffmpeg | S | M | All |
| 6 | Master-bus chain | audio | `data-fx-chain` on top-level root (`attributes.md` §master bus) | One chain over the summed mix, for example a `truepeak` delivery ceiling. Has no automation. | T: as #5 | S | M | All |
| 7 | Character voice presets | audio | Node lists in `D/studio/assets/index-CFrZAwKo.js` (`ys("telephone",…)`); catalogue in `S/hyperframes-audio/references/presets.md` | Presets: telephone (HP 300 / LP 3400 + 1.2 kHz honk + tanh grit), radio-am, megaphone, pa-system, intercom, lofi-tape. Space presets: room-tight, room-natural, hall, slap-echo, dub-throw. | T: Studio-only UI. Copy the node JSON into `data-fx-chain`, or port it to our Python/ffmpeg chain | S | H | Hor (radio/phone voice of 2nd character), Fin (scam-call re-enactment), Cart |
| 8 | Voice cleanup presets and jobs | audio | `presets.md` (voice-clean / broadcast / warm; Add Clarity 3 kHz +2.5 dB; Reduce Mud 250 Hz −3 dB …) | Named EQ moves for TTS polish. | W as a recipe (port to Python) / T in-composition | S | M | All |
| 9 | Audio groups and submix bus | audio | `<hf-audio-group id="voiceover">` + `data-audio-group` (`S/hyperframes-audio/SKILL.md`) | One chain, fader and automation clock for several clips (narrator + 2nd voice). Its lanes run on composition time. | T: requires stems placed in the composition | M | M | All |
| 10 | `audio-duck.mjs` | audio | `S/media-use/scripts/audio-duck.mjs --meta audio_meta.json --target "#bgm"` | Writes a volume-lane `data-automation` from speech spans. Simpler than carve. | T: needs a separate bed track | S | M | All |
| 11 | Volume-lane automation | core | `data-automation` `{"lanes":[{"target":"volume","points":[…]}]}` (`S/hyperframes-core/references/creator-editing-recipes.md` §Volume fades) | Clip-local fades and ducks, up to 512 points. It wins over GSAP volume tweens. | W for fades on any placed audio | S | L | All |
| 12 | `hyperframes audio` analyser | cli | `npx hyperframes audio <file> --quality fast --json [--place-at T] [--only moments,onsets] [--band lo,hi]` | Measures kind, moments (onset/steepest/peak/tailEnd), onset hits with strength, LUFS and clipping, silence spans, and envelope. Film queries via `--at/--range/--element`. | W with `--quality fast` (signal-only, local). The `api` provider needs env URL+key. beats/sections/describe are unavailable on Linux unless Beat-This is installed | S | H | QA for every channel (SFX-on-cut check, see §3) |
| 13 | `hyperframes beats` | cli | `npx hyperframes beats <dir> --json` | Finds the `<audio data-timeline-role="music">` (or id music/bgm), then writes `beats/<rel>.json` = `{version:1,audio,beats:[{time,strength}]}` and prints the bpm and its confidence. | T: our music must be a placed `<audio>`. It **fails on beatless drones**. Our score script already knows its own grid, so this is a cross-check only | S | L | Tech, Fin (beat-driven reels) |
| 14 | `normalize-audio` | cli | `npx hyperframes normalize-audio --target <id> --lufs -14 --write` | Sets `data-volume` so a placed clip hits the target LUFS, or matches it to a reference clip. | T: placed tracks only. Redundant with our Python loudnorm | S | L | — |
| 15 | Two-pass loudnorm recipe | audio | `S/media-use/references/operations.md` §Publish loudness | ffmpeg loudnorm targeting I=-14, TP=-1.5, LRA=11 with measured_* values. | W: check it matches our mix_norm step | S | M | All |
| 16 | Kokoro TTS (local, free) | cli | `npx hyperframes tts text.txt -v am_michael -l hi -o out.wav` | Offline 82M TTS with 12 listed voices. Phonemizer languages include `hi`. | T: needs pip `kokoro-onnx soundfile` (reachable), model and voices from GitHub *releases* (fetch via GH Actions), and espeak-ng for Hindi. A free fallback when Gemini hits rate limits | M | M | Kids, Cart (extra character voices) |
| 17 | Gemini TTS via audio engine | audio | `S/media-use/audio/scripts/audio.mjs --request audio_request.json` with `provider:"gemini"` | Line-based request (`lines[].sfx` cues) giving `audio_meta.json` with word timings (it auto-transcribes). | T: overlaps our own Gemini step and routes our key through their script. Only the request/meta **schema** is worth copying | M | L | — |
| 18 | `hyperframes transcribe` import/export | cli | `npx hyperframes transcribe words.json --to srt -o captions.srt`; also `.srt/.vtt` import | Normalises word JSON to `[{id,text,start,end}]` and exports SRT/VTT sidecars, which can go to YouTube as an uploaded CC track. | W for import/export (no model). Whisper engine: B in workspace (whisper.cpp built via git+cmake, model from HuggingFace) | S | M | All (SRT upload helps search/accessibility) |
| 19 | Transcript quality rules | audio | `S/media-use/audio/references/transcribe.md`, `captions/transcript-handling.md` | Rules: `.en` models silently **translate** non-English; pick `small --language hi` for Hindi; gate for silence hallucination. | W as rules for our Whisper step | S | M | Hindi versions |
| 20 | remove-background | cli | `npx hyperframes remove-background in.png -o cut.png` (also video to .webm alpha, `-b` bg plate) | u2net_human_seg cutouts, about 2 fps at 1080p on CPU. | T: model from GitHub release (fetch via GH Actions, cache at `~/.cache/hyperframes/background-removal/models/`) | M | M | AIH (portrait cut-outs), Cart, Hor (figure silhouettes) |
| 21 | LUT library (3 looks) | grading | `S/media-use/luts/index.json` | teal-orange-blockbuster, bleach-bypass, film-fade. Each has a CDN url plus a `params` fallback. | W offline via params/buildCube (`resolve --type lut --intent … --local-only`). CDN url: B | S | M | §4 |
| 22 | Parametric LUT builder | grading | `npx hyperframes media-use resolve --type lut --params '{"contrast":0.2,"temperature":-0.3}' --project . --local-only` | Writes a validated `.cube` (max size 64) to `.media/luts/`. | W (local math), T for exact CLI behaviour | S | H | 3D variants (feeds three.js LUTPass or ffmpeg lut3d) |
| 23 | Media-treatment shader (DOM media) | treatment | `npx hyperframes media-treatment --selector '#x' --grading '<json>' --apply`; `data-color-grading` | WebGL grade on `<img>`/`<video>` only: 18 presets, adjust/wheels/curves/HSL, vignette/grain, retro-glitch (tapeDamage, filmArtifacts, scanlines, chromaticAberration, crtCurvature, digitalGlitch, chromaBleed), print, ASCII, LUT. | T: our plates are JS-created `<img class="plate">` (`centralia/template.html:96`), so set the attribute in JS (the CLI only patches static HTML). Cost under SwiftShader is unmeasured. **Not for `<canvas>`** | M | H | Geo 2D, AIH, Hor |
| 24 | Treatment recipes | treatment | `S/media-use/references/media-treatment-recipes.md` (VHS Playback, 8mm Home Movie, Film Memory, Creator Camcorder, Editorial Halftone, Two-Ink Print, CRT Display, Procedural ASCII, Organic Light Leak, Freeze-Frame Cutout, Social Flash) | Tested payloads. | T: same as #23 | S | H | Hor (VHS/8mm), AIH (Film Memory/8mm), Fin (Halftone/Two-Ink), Tech (CRT/ASCII) |
| 25 | Animatable grade vars | treatment | `--hf-color-grading-{intensity,exposure,blur,bloom,pixelate,ascii,dither,…}` (`S/media-use/references/grading.md`) | Seek-safe GSAP `tl.to()` on these CSS vars gives reveals and depixelate effects. | T (as #23) | S | M | Hor (blur-to-sharp reveal), Tech |
| 26 | `media-treatment --analyze` | treatment | `… --selector '#hero' --analyze --json` | signalstats evidence plus a bounded exposure/contrast correction. | T: static `<img>` only | S | L | Geo (AI plate consistency) |
| 27 | `grade-compare` | cli | `npx hyperframes grade-compare --for frame.png --grades grades.json` or `--luts a.cube,b.cube` | Grid PNG of up to 16 candidate grades plus an ungraded baseline. | W (local Chrome); see §4 | S | M | Look-dev per channel |
| 28 | `render --variables / --batch` | cli/core | `npx hyperframes render --batch rows.json --output "renders/{name}.mp4" --strict-variables` | One template, many outputs (EN/HI, channel skins), with a manifest.json. | W | M | All (EN+HI batch) |
| 29 | Composition variables | core | `data-composition-variables`, `data-var-text`, `data-var-src`, auto `--{id}` CSS vars, `getVariables()` (`S/hyperframes-core/references/variables-and-media.md`) | Parameterises text, images, colours and enums, plus `$gradingPreset` inside `data-color-grading`. | W. **Root `data-duration` cannot be a variable** (fixed at compile) | M | H | All (see §5) |
| 30 | Sub-compositions | core | `data-composition-src` + `<template>` file (`sub-compositions.md`, `composition-patterns.md`) | Reusable scene/overlay blocks with per-instance `data-variable-values`. | W (three ids must match) | M | H | All (see §5) |
| 31 | Relative clip timing | core | `data-start="intro + 2"` (`tracks-and-clips.md` §Relative Timing) | Chains clips with no absolute math. | W but **fails silently to 0**; needs spaces around the operator | S | L | — |
| 32 | `check` gate | cli | `npx hyperframes check --caption-zone "x0=0;y0=.82;x1=1;y1=1;severity=error" --frame-check --at-transitions --json` | One Chrome boot runs lint, runtime errors, layout overflow/overlap, WCAG contrast (with suggested colour), and media-out-of-frame. | W | S | H | All (Shorts UI zone, legibility) |
| 33 | Motion sidecar assertions | cli | `index.motion.json` with `appearsBy / before / staysInFrame / keepsMoving(maxStaticSec)` | Fails on a **frozen shot more than 2 s** (a retention killer), late reveals, or off-frame drift. | W | S | H | All |
| 34 | `snapshot` | cli | `npx hyperframes snapshot --at 1.5,12 --describe false [--zoom "#cap"] [--angle iso] [--against ref.mp4]` | Exact-time PNGs plus a contact sheet; zoom crops; 3D tilt view; side-by-side against a reference. | W. **Pass `--describe false`**: otherwise it sends frames to Gemini whenever GEMINI_API_KEY is set | S | M | All |
| 35 | `keyframes --shot --ghost` | cli | `npx hyperframes keyframes . --selector '#globe' --shot onion.png --ghost` | Onion-skin of real canvas/WebGL frames over time, to check 3D motion paths. | W/T (SwiftShader) | S | M | Geo 3D, Tech |
| 36 | `compare` | cli | `npx hyperframes compare a/ b/ --at 3 --labels old,new` | Labelled side-by-side of up to 16 variants at one time. | W | S | M | A/B caption or grade looks |
| 37 | `timeline --json` | cli | `npx hyperframes timeline . --json` | Static (no browser) clip table: absolute start/end, src, volume, automation. | W | S | M | QA of SFX placement if SFX become clips |
| 38 | `benchmark` | cli | `npx hyperframes benchmark . --runs 2` | Times fps/quality/worker presets. | W (slow) | S | M | Tuning cloud render workers |
| 39 | Render flags worth adopting | cli | `--no-browser-gpu` (force SwiftShader, deterministic), `--quality delivery` / `--crf`, `--format png-sequence`, `--low-memory-mode`, `--resume` (+`HF_SEGMENTED_CAPTURE=true`), `--strict` | Control over determinism, quality and memory. | W/T (`--resume` needs segmented capture) | S | M | All |
| 40 | Registry caption components (15) | captions | `npx hyperframes add caption-highlight --no-clipboard --json` (also pill-karaoke, editorial-emphasis, glitch-rgb, kinetic-slam, neon-glow, clip-wipe, matrix-decode, emoji-pop, particle-burst, weight-shift, …; `S/media-use/audio/references/captions/authoring.md`) | Sub-composition overlays that mount **inside our composition**. | T: fetched from raw.githubusercontent (reachable). Check 1080x1920 and Devanagari | M | H | Tech (glitch/matrix), Fin (kinetic-slam), Kids (emoji-pop) |
| 41 | Frame-preset caption skins (13) | captions | `S/hyperframes-creative/frame-presets/*/caption-skin.html` | Brand-token skins with `GROUPS`/`DURATION` holes, filled by `S/faceless-explainer/scripts/captions.mjs`. | T: mounts as a sub-comp; low effort to wire | M | M | Fin, Tech |
| 42 | Embedded-caption identities (35) | captions | `S/embedded-captions/CATALOG.md`, `themes/*.json`, `dna/*.json` | Themed rail plus apex setpiece engines. | T: separate pipeline, or port the generated layer (§2) | L | H | §2 |
| 43 | Caption fonts (40 woff2, Latin subsets) | captions | `S/embedded-captions/modes/standard/fonts/files/` + `fonts.css`, `scripts/inject-fonts.cjs` | Offline fonts, base64-inlined: Creepster, Special Elite, VT323, Press Start 2P, Cinzel, Bangers, Baloo 2, Fredoka, Anton, Monoton, Permanent Marker, Caveat, Shippori Mincho, … | W for Latin. **Latin-only, no Devanagari** | S | M | Hor (Creepster/Special Elite), Kids (Fredoka/Baloo), Tech (VT323/Orbitron) |
| 44 | Hershey stroke-path writer | captions | `S/embedded-captions/scripts/gen-stroke-path.py` + `assets/strokefonts/*.svg` | Turns any word into sequential per-stroke SVG paths for hand-written draw-on, with no per-word tuning. | W (python3, Latin only) | S | H | Kids (chalk), Geo (hand-labelled maps), Cart |
| 45 | Caption rules (rail spec) | captions | `S/embedded-captions/references/rail.md`, `caption-grouping.md`, `anti-patterns.md` | Rules: portrait rail about 600-700 px from bottom; ≤2 lines of 32-42 chars; ≥0.5 s per group; group window must contain its words; ±80 ms sync; never animate `letter-spacing` / `filter:blur` on word entrance. | W as QA rules for our karaoke | S | M | All |
| 46 | `check-timing.cjs` / `check-overflow.cjs` | captions | `S/embedded-captions/scripts/` | Caption timing (80 ms) and overflow gates. | T: they expect their plan.json shape; adapt | M | M | All |
| 47 | `audio-envelope.cjs` | captions | `S/embedded-captions/scripts/audio-envelope.cjs` | RMS envelope that drives hero amplitude from loudness. | W (ffmpeg); we can do the same in Python | S | L | Hor (scream-scaled type) |
| 48 | Studio safe zones | core | `S/hyperframes-studio/SKILL.md` §4 | Action-safe 90% (5% inset), title-safe 80% (10% inset). | W as a rule | S | L | All |
| 49 | Faceless-explainer transitions | core | `S/faceless-explainer/scripts/lib/transitions.json`, `references/cut-catalog.md` (zoom-through, cut-the-curve, waterfall cut) | Registry of scene transitions with energy defaults. | T: port as GSAP | M | M | Geo, Fin, Tech |

---

## 2. Caption identities

**Count note:** CATALOG.md has **35**, not 37: 10 classic DNA (`dna/*.json`) + 25 themes (`themes/*.json`). It and SKILL.md both say "35 identities" (`S/embedded-captions/SKILL.md:18`). The only other templates are the legacy `modes/cinematic/cinematic-cream` and three archived ones (`_archive/champion|memory-wall|portrait-header`).

### 2a. How an identity is authored and rendered

- **Classic DNA, Cinematic engine.** Author `cinematic.json` (dna + thought blocks + one `hero:true` line). Then `node scripts/make-cinematic.cjs <proj>` produces plan.json and then index.html, using `modes/cinematic/engine.html` and `lib-dna.cjs`.
- **Themes, Theme engine.** Author `theme.json`: `dna`, verbatim `lines`, `minors`, `hero.match`, optional `width/height/fps`. Then `bash scripts/render-theme.sh <proj>` does three things:
  - `make-theme.cjs` (8.6k lines) emits `index.html` (bg layer: `<video id="a-roll" src="source.mp4">` + the apex setpiece) and `rail.html` (fg alpha layer: body rail + front FX).
  - `render-and-composite.sh` runs **two `hyperframes render` passes** (bg mp4 + fg alpha webm), overlays the matte `frames_fg/` so the subject occludes the apex, then lays the rail on top.
  - `_postfx.sh` applies the plate punch/shake/grain with ffmpeg and writes `final_fx.mp4`.
- **Inputs:** `source.mp4`, `transcript.json` (`{words:[{text,start,end}]}`), `frames_fg/` + `matte.fps` (from `remove-background`), and optionally `safe-zones.json`.
- **Gates:** compile-time verbatim matcher (every transcript word covered, 80 ms), overflow, rail-climax, PAGEERROR.
- **Hard rules:** paused GSAP on `window.__timelines["main"]`, seeded PRNG, no CSS keyframes. These are the same as ours (`S/embedded-captions/themes/README.md`).

### 2b. Can an identity run inside OUR composition?

Not as shipped. The engines are locked compilers built around talking-head footage and a person matte.

Three blockers:
- **16:9 tuning.** Theme DNAs are tuned for 1280x720 (`themes/README.md` schema: "vertical needs a DNA variant"). The geometry is in px (`fontPx`, `bottomPx`, strip geometry).
- **Latin-only fonts.** `fonts/files/*-latin-*`, so Hindi versions fall back to system fonts.
- **Person matte.** The apex "behind the subject" needs a matte of a person (`matte.cjs` uses u2net_human_seg).

Two workable routes:
1. **Post-pass route (T, M).** Treat our silent render as `source.mp4` and our Whisper words as `transcript.json`. For the matte, supply either all-transparent `frames_fg/` (the apex sits in front) or, better, a **foreground-only alpha pass of our own scene**. That pass is our landmark/character layer rendered `--format png-sequence` and gives genuine occlusion with no AI matting.
   - Copy the theme JSON to a `*-v` variant scaled for 1080x1920.
   - Cost: +2 HyperFrames renders + an ffmpeg composite per video, plus the `_postfx.sh` plate reaction.
2. **Port route (T, M-L).** Compile once and lift `rail.html` (already a HyperFrames composition with its own GSAP timeline) into a `<template>` sub-composition mounted in our index.html (`data-composition-id` must match). Then:
   - Strip the `<video id="a-roll">` from the bg layer and mount the setpiece as a second overlay.
   - Drop the matte (the apex goes in front of the scene) or reorder z-index under our foreground layer.
   - This is cheapest per video once it is templated, but must be redone per identity.

Lower-effort alternatives that are native sub-compositions: the registry caption components (#40) and frame-preset skins (#41).

### 2c. The 35 identities: look and genre fit

Classic DNA (column-flow; every caption embedded, mood over verbatim; `cinematic.json` → make-cinematic):

| Identity | Look | Fits our genres |
|---|---|---|
| cream | warm cream Inter, screen blend, glowing emergence hero; needs dark/mid warm scene | AIH reflective, Hor quiet dread (weak) |
| ink | near-black multiply "letterpress" for bright scenes (luma >150) | Geo on bright parchment maps, Kids |
| editorial | Bodoni Moda, lowercase-italic hero, magazine elegance | AIH, Fin premium |
| keynote | opaque white Inter 800, dead-centre stillness | Tech news, Fin |
| documentary | burn-in bone-on-charcoal, no hero, gravitas | Hor true story, AIH, serious Geo |
| loud | Anton slam + scene-sampled accent, body in front | Fin/scam hooks, Tech hype |
| neon | electric-cyan signage that ignites, dark scenes | Tech (night), Hor (motel/neon noir) |
| glitch | RGB-split echoes snapping together | Tech/AI news, Fin (hacker scams), Hor (digital haunting) |
| chrome | liquid-metal hero + sheen sweep | Tech product |
| velocity | words arrive along motion vectors with streak trails | Geo (speed/travel facts), Tech |

Themes (rail/panel/takeover paradigms + apex setpiece + plate reaction; `theme.json` → make-theme). Rail-type surfaces are **verbatim**, so every word reads:

| Identity | Look | Fits our genres |
|---|---|---|
| anchor | quiet fade-up Sora rail + one apex settling behind subject with drawn underline | Geo (default), Fin, Kids, AIH |
| ordnance | military stencil stamped rail + detonation apex + edge charge-dim | Geo (wars/borders), Fin shock stats |
| terminal | typed console panel + glyph-decode apex (redact-until-hero) | Tech, Fin (scam forensics), AIH |
| neonsign | warm neon-tube rail + hand-written neon apex (needs python3) | Hor (motel sign), lifestyle |
| stardust | accumulating poem, letters condense from dust | AIH wonder, Geo space/planet |
| stomp | full-frame hard-cut takeover cards with a void before the drop | Hooks for every channel (first 2 s), Fin |
| lastpage | typed manuscript rail + blurred "future field" that rack-focuses to the apex | Hor (prophecy/curse), AIH ("the future") |
| scoreboard | split-flap chyron rail + giant departures-board apex, ROW counter | Geo rankings/stats, Fin markets, countdowns |
| transit | amber LED departure strip + column-by-column LED wipe apex | Geo travel/transit, countdowns |
| vhs | camcorder OSD (PLAY/REC/timestamp), red/cyan fringe, REC-FREEZE tracking-slam apex | Hor found-footage, retro Tech |
| arcade | 8-bit HUD bar, CRT scanlines, pixel-block BOSS INTRO apex | Kids, gaming Tech |
| dossier | manila case-file strip typed in Special Elite + sepia rubber-stamp apex | Hor true crime, Fin scam exposés, AIH declassified |
| laser | concert beams ignite each word, 6-beam laser-cage apex | Hype only (weak fit) |
| thunder | slate storm mood, rain in front, sky flash per word, branched-bolt strike apex | Hor (storm night), Geo weather/disasters |
| hologram | scanlined projection plate + 7-layer hologram boot apex | Tech/AI news, AIH futurism, Geo space |
| biolume | abyss grade, jellyfish glow-on rail, bioluminescent bloom apex | Geo oceans, Kids science, Hor deep-sea |
| aurora | iridescent silk serif rail + aurora ribbon hand-written apex | Geo polar/night sky, travel |
| spectrum | oscilloscope band with live waveform + phosphor trace-write apex, "SIGNAL LOST" end | Tech/science, Hor (EVP/ghost radio) |
| papercut | stop-motion paper chips on kraft strip + torn-chip papermat apex | Kids, Cart |
| popup | pop-up book page rail + centerfold starburst apex | Kids, Cart, storytelling |
| chalkboard | deep-green chalk band, scribbled words, eraser swipes, hand-chalked apex | Kids edu, Geo explainers, Fin basics |
| graffiti | marker rail + spray-tagged apex with drips | Street/youth (weak fit) |
| brush | washi paper band + sumi-e brush-gesture apex + seal chop | Geo Japan/Asia episodes, calm explainers |
| inkwater | three-row ink rail + ink-drop bloom apex | AIH, Hor slow dread, contemplative Geo |
| ransom | cut-out chip collage rail + ransom-note slam apex | Hor/true crime, Fin scams (fraud/ransom), mystery |

**Best 4 for a geography explainer.** All four are verbatim rail surfaces, because Shorts viewers read along and a map must stay legible.
1. **anchor.** The conservative default: an opaque rail reads on any map, with one restrained apex per section. It is closest to our current karaoke, so it is the least risky.
2. **scoreboard.** Split-flap flip on stat and country reveals ("#1 … RUSSIA") is a built-in retention device for rankings and numbers, and it brings its own dark contrast.
3. **chalkboard.** The teacher-explainer register. The hand-chalked apex word uses the Hershey writer (#44), which also serves Kids. The self-lit green band survives busy maps.
4. **ordnance.** Punchy stamped mass for border, war and "shock fact" beats. Its charge-dim edge vignette makes its own contrast.

Episode alternates: biolume (oceans), aurora (polar), transit (travel).

**Best 2 for horror.**
1. **vhs.** The found-footage OSD is an instant genre signal. The REC-FREEZE tear apex is a built-in jump-scare beat, and the backlight scrim keeps text readable.
2. **dossier.** Typed case file + sepia stamp ("CLASSIFIED") fits true-story and urban-legend narration. It is verbatim and self-lit.

Alternates: thunder (storm), ransom (crime), lastpage (prophecy).

---

## 3. Audio

**Can the externally mixed WAV use `data-fx-chain` or ducking?**
- **Chain: yes.** Place it as `<audio id="mix" src="mix_norm.wav" data-start="0">` (an id is mandatory, otherwise the render is silent; `variables-and-media.md`). Any per-clip `data-fx-chain` or root master-bus chain is then rendered in an OfflineAudioContext, and HyperFrames muxes the audio itself (`S/hyperframes-audio/SKILL.md` "How it fits together").
  - Useful additions: a `truepeak` ceiling, or a character preset. But a preset on a full mix colours everything.
  - The render **fails the whole mix on an unparsable chain** (no silent dry fallback). Worklet effects (compressor/limiter/truepeak/gate/bitcrush) **cannot be automated**.
- **Ducking/carve: no.** Carve measures voice against bed and writes filters plus a gain envelope onto the **bed** element with `sources:["voiceover"]` (a group of voice clips). A pre-summed WAV has no separable voice. A volume lane on the mix would duck narration too.
  - **Narration, second voice, music and SFX must be separate placed tracks:** voices in `data-audio-group="voiceover"`, the bed with `data-fx-carve`, SFX in their own `sfx` group. Never put SFX or bed in the voice group (`SKILL.md` carve rules).
  - Our score script would then export stems instead of mix_norm.wav. Then run `carve.mjs --comp index.html` (needs `@hyperframes/core` from npm + ffmpeg).
- **Recommendation:** keep the Python mix as the default.
  - Port the carve *idea* (6-band 250 Hz to 2.5 kHz voice-following dips + slow-release level envelope, about −7 dB/−15 dB @1.6 kHz at strength 0.8) into the score script.
  - Hand-copy the telephone/radio-am/megaphone node chains (#7) for the second character.

**What `hyperframes audio` measures** (`D/audio-Q7I473UN.js`). Default capabilities:
- `kind`
- `moments`: onset, steepest, peak, tailEnd per file/clip
- `onsets`: spectral-flux hit events `{t, strength}`, with `--threshold` and `--band lo,hi`
- `loudness`: integrated LUFS, clipping count and first time
- `silence`: spans below `--silence-db`
- `envelope`

Optional: `beats, downbeats, bpm, sections, describe`. These need the cloud `api` provider (env URL+key), macOS, or Beat-This weights. Use `--quality fast` for pure local signal analysis. Film queries: `--at T`, `--range a,b`, `--element #id`, and `--place-at T` for a file not yet in the film.

**Can it verify SFX land on cuts? Yes.** Three methods, best first:
1. Per cue: `npx hyperframes audio sfx/whoosh.mp3 --place-at <cue_start> --only moments --json`. This gives the peak in film seconds; assert `|peak − cut_t| ≤ 1 frame (33 ms)`. A riser should peak on the reveal.
2. Have the score script also write an **SFX-only stem**, then `audio sfx_stem.wav --only onsets --quality fast --json` and match onsets to the cut list from `times.json`.
3. On mix_norm.wav itself, use onsets with `--band` (for example 30-150 Hz for thuds). Narration onsets add noise here, so prefer method 2.

If SFX ever become placed `<audio>` clips, `timeline --json` and `audio --range` list them directly.

**What `beats` outputs** (`D/beats-P4LENNVT.js`):
- It requires an `<audio data-timeline-role="music">` (or an id matching music/bgm/soundtrack) in index.html.
- It writes `beats/<audio-rel-path>.json` = `{"version":1,"audio":"…","beats":[{"time":s,"strength":0..1}]}`, and stdout gives the count, bpm and `high|low|uncertain` confidence.
- It writes nothing and fails on a track with no steady beat. Our pad/drone beds may fail, though drum sections should pass.

---

## 4. Grading

**The three LUT looks** (`S/media-use/luts/index.json`). Each has a CDN `url` (static.heygen.ai, B in workspace) and a `params` fallback that buildCube generates locally.
- **teal-orange-blockbuster** (intensity 0.85): contrast .18, sat .08, vibrance .12, split-tone teal shadows / warm highlights. Use for Geo hero landscapes and AIH dramatisations.
- **bleach-bypass** (0.8): contrast .55, saturation −.72, crushed blacks and lifted whites. Use for Hor and gritty war/disaster Geo.
- **film-fade** (0.75): blacks +.35, contrast −.28, warm (temp +.16). Use for AIH archival, nostalgic Fin ("how money used to work").

**What it applies to.**
- `media-treatment` and `data-color-grading` target **`<img>` and `<video>` only** (`--capabilities` → `targetTags:["img","video"]`). The runtime swaps the element for a WebGL canvas (`data-hf-color-grading-canvas` in `D/hyperframe-runtime.js`).
- They do **not** apply to `<canvas>`/three.js, CSS backgrounds, SVG or text.
- **DOM plates (2D variant):** feasible, but our plates are created in JS (`centralia/template.html:96`). Set `img.setAttribute('data-color-grading', JSON)` at creation, before the timeline is registered. Then test three things: dynamic discovery, interaction with our `cam` transforms, and SwiftShader frame cost on large plates (multipass blur/bloom/kuwahara is the expensive lane).
- **WebGL canvases (3D variant):** use the same `.cube` from `resolve --type lut --params … --local-only` with three@0.149's bundled `examples/jsm/postprocessing/LUTPass.js` + `loaders/LUTCubeLoader.js` (present in `/home/claude/work/node_modules/three/`). This is deterministic and in-scene, so captions stay ungraded if drawn in DOM. Alternatively, use ffmpeg `lut3d=file.cube` on the final MP4 (that grades captions too). `ColorCorrectionShader` / `VignetteShader` cover simple adjusts.
- **Offline fallback:** `params` → buildCube runs locally (`resolve --type lut --intent "<look>" --local-only` or `--params '{…}'`), cube max size 64. Presets such as warm-daylight are shader controls, not cubes, so a 3D look must be expressed as params.

**What `grade-compare` needs:**
- Headless Chrome (bundled).
- `--for` a reference PNG, or a video (first frame).
- **Exactly one** of `--grades grades.json` (`[{label, grading:{…}}]`, up to 16) or `--luts a.cube,b.cube`.
- Optional `--no-baseline`, `--out`, `--timeout`.

It only produces a comparison PNG; it applies nothing. For 3D scenes, first `snapshot --at T --describe false`, then grade-compare on that PNG with `--luts` from params cubes.

---

## 5. Core features for reusable cross-channel templates

1. **One template per format, channel as data.** Declare on `<html>`:
   - `data-composition-variables` for channel, accent, ink, fontDisplay (enum), captionStyle (enum), badgeSrc, gradingPreset, lang (enum en/hi).
   - Bind with `data-var-text`, `data-var-src`, and auto `--accent` CSS vars.
   - `data-color-grading='{"preset":"$gradingPreset"}'` resolves from variables.

   Render EN and HI (or several channels) with `render --batch rows.json --strict-variables`.
   Constraint: the **root `data-duration` is fixed at compile time**, so our build script must still write each video's duration statically (`determinism-rules.md`).
2. **Sub-composition library** (`<template>` files under `compositions/`, ids matching host = inner = `__timelines` key; use `gsap.fromTo` inside):
   - captions track (one file per style; swap the `data-composition-src`)
   - BHUGOL/Nishachar/Money Mirage intro sting and end card
   - map-pin callout, stat counter, horror jump-scare stinger, "scam alert" stamp

   Each takes `data-variable-values` per instance. A sub-comp cannot animate host elements. Media inside sub-comps is time-rebased automatically. Only the **top-level** root's `data-fx-chain` acts as master bus.
3. **Audio structure, if we move the mix in-composition:** `<hf-audio-group>` buses (voiceover / music / sfx) with group-level chain and fader, carve on the bed against the voice group, and SFX as timed `<audio>` clips. This makes `timeline --json`, `audio --range` and `beats` work as QA.
4. **QA contract per template:**
   - `check --caption-zone` (keep key content out of the bottom Shorts UI band).
   - `--frame-check`.
   - A shared `index.motion.json` with `keepsMoving maxStaticSec:2`, which catches dead frames that hurt retention.
   - `snapshot --describe false` contact sheets.
5. **Relative timing** (`data-start="scene3 + 0.2"`) can chain scene clips. Lint does not catch its silent-zero failure modes, so snapshot-verify.

Sources: `S/embedded-captions/{SKILL.md,CATALOG.md,themes/README.md,references/rail.md,scripts/*}`, `S/media-use/{SKILL.md,references/grading.md,media-treatments.md,media-treatment-recipes.md,operations.md,luts/index.json,audio/references/*,audio/assets/sfx/*}`, `S/hyperframes-audio/{SKILL.md,references/*}`, `S/hyperframes-core/references/*`, `S/hyperframes-cli/references/*`, `S/hyperframes-registry/SKILL.md`, `S/hyperframes-studio/SKILL.md`, `D/audio-Q7I473UN.js`, `D/beats-P4LENNVT.js`, `D/hyperframe-runtime.js`, `D/studio/assets/index-CFrZAwKo.js`, CLI `--help` output for all 17 requested commands.
