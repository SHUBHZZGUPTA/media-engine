# HyperFrames 0.8.181: what our Shorts pipeline can reuse

Audit date: 2026-10-22. I only read the sources and wrote this file.

**Path keys**
- `A/` = `scratchpad/hf-src/skills/hyperframes-animation/`
- `reg:x` = registry item `x` from `scratchpad/catalog.json`, which lists 448 items: 210 blocks and 238 components. I read all 448.
- `pkg/` = `scratchpad/npmpkg/package/`
- `cli/` = `/home/claude/work/node_modules/hyperframes/dist/` (the installed CLI, version 0.8.181)

I opened about 45 item files from GitHub raw to check what each one loads. Every item uses GSAP from `cdn.jsdelivr.net/npm/gsap@3.14.2`. Some also load `d3@7`, `topojson-client@3.1.0`, `world-atlas@2`, `us-atlas@3`, `es-atlas@0.6.0`, `three@0.147/0.170/0.184` or `lottie-web@5.12.2`, and a few load Google Fonts.

**Baseline port.** One fixed cost applies to every row:
- Vendor the CDN libraries into the repo. All of them are npm packages, so the workspace can fetch them.
- Replace Google Fonts with local woff2 files from `@fontsource` on npm. `A/transitions/catalog.md` says the compiler embeds supported fonts on its own, but that still needs a test per font.
- Re-lay 1920x1080 blocks to 1080x1920. Components have no fixed size and only need restyling.

"Works" below means the item works once this baseline port is done.

**Columns**
- Feasibility: **W** = Works, **T** = Test needed, **B** = Blocked.
- Effort: S = paste or under 1 hour, M = re-layout or wiring (half a day), L = real port.
- Retention value: H, M or L.

**Channel codes:** GEO geography, HOR horror, FIN finance/scams, TECH tech news, HIST AI history, KIDS kids education, TOON 2D cartoon, ALL any niche.

**Already in our pipeline, so not listed again:**
- `rules/asr-keyword-glow` (we have keyword pop and glow).
- `rules/viewport-change` (our CSS camera).
- `reg:count-up`, `reg:push-in`.
- `reg:cut-the-curve`, `reg:zoom-through-transition`, `reg:directional-wipe`.
- The CSS zoom-through, zoom-out, push-slide and blur-crossfade transitions.

Exceptions, where the shipped version is better than ours, are marked in the rows.

---

## 1. Reuse table

### 1a. Atomic rules (`A/rules/*.md`, all GSAP, transform-only, seek-safe)

| item | kind | path | what it does | feasibility | eff | ret | best for |
|---|---|---|---|---|---|---|---|
| 3D camera flight | rule | A/rules/3d-camera-flight.md | `perspective` stage with a `preserve-3d` world; dive, tilt-to-flatten and fly past standing cards | W (CSS 3D; check image-plate sharpness at scale) | M | H | GEO flyover of map plates, HIST, ALL |
| 3D page scroll | rule | A/rules/3d-page-scroll.md | Tilted 3D "web page" card that scrolls to a section | W | M | M | FIN (scam article), TECH news |
| 3D text depth layers | rule | A/rules/3d-text-depth-layers.md | N offset text copies make a fake extrusion | W | S | M | ALL titles, KIDS, HOR |
| AI tracking box | rule | A/rules/ai-tracking-box.md | Yellow L-bracket box with a 95-99% label that follows a target | W | S | M | TECH, HOR ("subject detected"), GEO |
| Ambient glow bloom | rule | A/rules/ambient-glow-bloom.md | Soft radial bloom behind a hero element, or one sheen pass | W | S | L | ALL |
| Avatar cloud network | rule | A/rules/avatar-cloud-network.md | Avatars on an ellipse with SVG links to a centre | W | S | M | FIN (victim network), TECH |
| Card morph anchor | rule | A/rules/card-morph-anchor.md | A container morphs size and radius, then reveals the real target | W | M | M | FIN, TECH |
| Centre-outward expansion | rule | A/rules/center-outward-expansion.md | Items burst from the centre to their slots | W | S | M | ALL list beats |
| Chart scrub readout | rule | A/rules/chart-scrub-readout.md | A playhead line and tooltip step through a drawn chart | W | M | H | FIN (price history), GEO (population) |
| Chromatic glitch | rule | A/rules/chromatic-glitch.md | RGB split or slice glitch on a quantised-time hash, then snaps clean | W | S | H | HOR, TECH |
| Coordinate target zoom | rule | A/rules/coordinate-target-zoom.md | Scale plus counter-translate math for zooming to an off-centre point | W (worth a check against our camera math) | S | H | GEO zoom-to-country |
| Counting with dynamic scale | rule | A/rules/counting-dynamic-scale.md | The counter's scale grows with its value | W (adds to our count-up) | S | M | FIN, GEO |
| CSS marker patterns | rule | A/rules/css-marker-patterns.md | Highlight sweep, hand ellipse, burst lines, scribble, sketch box | W | S | H | ALL explainers |
| Depth-of-field blur | rule | A/rules/depth-of-field-blur.md | Rack focus by tweening `filter: blur()` on off-focus layers | T (large CSS blurs are CPU-heavy on SwiftShader; measure) | S | H | HIST, HOR, GEO |
| Depth scatter / assemble | rule | A/rules/depth-scatter-assemble.md | Elements tumble from a 3D cloud into a flat layout | W | M | M | titles, TECH |
| Discrete text sequence | rule | A/rules/discrete-text-sequence.md | Typing with typos, holds and backspaces as threshold states | W | S | M | HOR (creepy texts), FIN (scam SMS) |
| Dynamic content sequencing | rule | A/rules/dynamic-content-sequencing.md | Builds phrase timing from the script (chars × speed + hold) | W | S | M | infra, ALL |
| Gradient text sweep | rule | A/rules/gradient-text-sweep.md | Gradient travels through the letterforms (`background-clip: text`) | W | S | M | ALL titles |
| GSAP effects | rule | A/rules/gsap-effects.md | Drop-in typewriter and audio-visualiser blocks | W | S | L | ALL |
| Hacker flip 3D | rule | A/rules/hacker-flip-3d.md | Per-glyph 3D flip with deterministic decryption | W | S | M | TECH, HOR, HIST (cipher) |
| Kinetic beat slam | rule | A/rules/kinetic-beat-slam.md | Phrases slam on one beat array, each with its own entrance (scale, side, rise-rotate) | W (new: we only slam numbers) | S | H | ALL hooks |
| Motion-blur streak | rule | A/rules/motion-blur-streak.md | Directional SVG `feGaussianBlur` or echo-ghost trail, peaking at top speed | W (SVG blur cost; keep small) | S | M | ALL slams |
| Multi-phase camera | rule | A/rules/multi-phase-camera.md | Pull-back, focus and push phases plus continuous micro-drift | W (pull-back and drift are new) | S | M | ALL |
| Nudge curve | rule | A/rules/nudge-curve.md | Slow-fast-slow group slide that reveals during the burst | W | S | M | ALL |
| Orbit with 3D entry | rule | A/rules/orbit-3d-entry.md | Icons flip in from 3D, then orbit on an ellipse | W | S | M | KIDS (planets), TECH |
| Particle burst | rule | A/rules/particle-burst.md | Confetti, dot burst or glyph dissolve, ≤40 particles, ballistic and deterministic | W | S | H | KIDS, TOON, FIN (money) |
| Reactive displacement | rule | A/rules/reactive-displacement.md | An incoming element physically shoves the old one out | W | S | M | ALL ("myth pushed out by fact") |
| Scale-swap transition | rule | A/rules/scale-swap-transition.md | Exit shrinks while entry pops with `back.out` at the same centre | W | S | M | ALL |
| Sine wave loop | rule | A/rules/sine-wave-loop.md | Finite idle breathing loop | W | S | L | TOON (idle characters), ALL |
| Split tilt cards | rule | A/rules/split-tilt-cards.md | A/B cards with mirrored `rotateY` tilts and opposite-phase float | W | S | H | FIN (scam vs real), GEO (country vs country) |
| Spring-pop entrance | rule | A/rules/spring-pop-entrance.md | `scale 0→1` with `back.out`, staggered ≤0.5 s | W | S | H | emoji props, KIDS, ALL |
| Stat bars and fills | rule | A/rules/stat-bars-and-fills.md | Growth bars, progress fill or ring, fractional star wipe | W | S | H | FIN, GEO |
| SVG icon enrichment | rule | A/rules/svg-icon-enrichment.md | Internal SVG parts move (hands, blades, pulses) | W | S | L | KIDS, TECH |
| SVG path draw | rule | A/rules/svg-path-draw.md | Stroke draws on via `dashoffset` | W | S | H | GEO (borders, rivers, routes), HIST |
| Theme crossfade morph | rule | A/rules/theme-crossfade-morph.md | Whole-skin crossfade under one fixed anchor | W | M | M | HIST (same map, era restyle) |
| Vertical spring ticker | rule | A/rules/vertical-spring-ticker.md | Slot-machine column with stepped tweens | W | S | H | FIN (prices), GEO (rank #) |
| Waterfall entry | rule | A/rules/waterfall-entry.md | Words whip up from below in an accelerating cascade | W | S | M | ALL titles and lists |

### 1b. Blueprints (`A/blueprints/<id>.md`) and examples (`A/examples/*.html`, all 1920x1080, CDN GSAP)

| item | kind | path | what it does | feasibility | eff | ret | best for |
|---|---|---|---|---|---|---|---|
| kinetic-type-beats | blueprint | A/blueprints/kinetic-type-beats.md | Bold centred type where swapping words is the motion; ends on a spring-pop payoff | W | S | H | ALL hooks and CTAs |
| zoom-out-workspace-reveal | blueprint | A/blueprints/zoom-out-workspace-reveal.md | Open tight on a detail, then one decelerating zoom-out reveals the whole | W | M | H | GEO ("this dot is…"), FIN |
| spatial-pan-stations | blueprint | A/blueprints/spatial-pan-stations.md | Oversized canvas with stations; the camera pans station to station | W | M | H | HIST timelines, GEO route stops |
| camera-journey | blueprint | A/blueprints/camera-journey.md | Multi-leg motivated camera flight (dive, beat, travel, landing push) | W (DOM version) | M | H | GEO, HIST |
| dataviz-countup | blueprint | A/blueprints/dataviz-countup.md | Camera pushes through stat rings and charts to one hero metric | W | M | H | FIN, GEO |
| comparison-split | blueprint | A/blueprints/comparison-split.md | Book-open A/B cards with pill badges | W | S | H | FIN, GEO |
| constellation-hub | blueprint | A/blueprints/constellation-hub.md | Nodes ring a centre, then the camera pushes in on the core | W | M | M | FIN (scam network), GEO (neighbours) |
| overwhelm-surround | blueprint | A/blueprints/overwhelm-surround.md | Clutter closes in on a centre subject | W | M | M | FIN (debt), HOR (closing in) |
| grid-card-assemble | blueprint | A/blueprints/grid-card-assemble.md | Staggered grid or list assemble, optional zoom-out | W | S | M | lists ALL |
| ticker-takeover | blueprint | A/blueprints/ticker-takeover.md | Word cycles through options, then a hero crashes in and shoves it aside | W | S | M | hooks ALL |
| typewriter-reveal | blueprint | A/blueprints/typewriter-reveal.md | Human-typed line with edits, then a payoff | W | S | M | HOR, FIN |
| fixed-anchor-cycle | blueprint | A/blueprints/fixed-anchor-cycle.md | One pinned element while the area around it cycles states | W | S | M | GEO ("found in X, Y, Z…") |
| titlecard-reveal | blueprint | A/blueprints/titlecard-reveal.md | Calm chapter card with one restrained move | W | S | M | chapter breaks ALL |
| video-text-pivot | blueprint | A/blueprints/video-text-pivot.md | Clip slides aside to hand over to a hero stat | W | M | M | TECH, FIN |
| logo-assemble-lockup | blueprint | A/blueprints/logo-assemble-lockup.md | Brand mark assembles into a lockup | W | S | L | channel sting or outro |
| hook-counter-burst | example | A/examples/hook-counter-burst.html | Counter plus icon burst as a 3.5 s hook (runnable reference) | W (re-layout) | M | H | FIN, GEO hooks |
| comparison-split-cards | example | A/examples/comparison-split-cards.html | Full A/B split scene | W (re-layout) | M | H | FIN, GEO |
| messaging-multi-phrase | example | A/examples/messaging-multi-phrase.html | Multi-phrase kinetic message | W | M | M | ALL |
| takeover-ticker-displace | example | A/examples/takeover-ticker-displace.html | Typewriter plus ticker, then a displacement takeover | W | M | M | hooks |
| concept-demo-decode-pan | example | A/examples/concept-demo-decode-pan.html | Decode text, then a pan track | W | M | M | TECH, HIST |
| metric-video-text-pivot | example | A/examples/metric-video-text-pivot.html | Video card hands over to a metric | W | M | M | TECH, FIN |
| problem-mockup-overwhelm | example | A/examples/problem-mockup-overwhelm.html | Mockup cluster and icons overwhelm | W | M | M | FIN |
| brand-reveal-assemble-zoom | example | A/examples/brand-reveal-assemble-zoom.html | Assemble-and-zoom brand reveal | W | M | L | outro |

### 1c. Transitions: CSS catalog (`A/transitions/css-*.md`; code also exists as `reg:transitions-*` showcase blocks)

| item | kind | path | what it does | feasibility | eff | ret | best for |
|---|---|---|---|---|---|---|---|
| Elastic push / squeeze / vertical push | transition | A/transitions/css-push.md | Push with overshoot; squeeze to a line and expand | W | S | M | KIDS, TOON (elastic), ALL |
| Circle iris / diamond iris / diagonal split | transition | A/transitions/css-radial.md | `clip-path` iris or diagonal wipe | W | S | H | TOON (cartoon iris-out), KIDS |
| 3D card flip | transition | A/transitions/css-3d.md | Scene flips like a card | W | S | M | KIDS, FIN (myth/fact) |
| Focus pull / colour dip | transition | A/transitions/css-dissolve.md | Rack-blur dissolve; dip to black or colour | T (blur cost) / W | S | M | HOR, HIST (dip to black) |
| Staggered colour blocks / blinds | transition | A/transitions/css-cover.md | Full-frame blocks or blinds cover, then reveal | W | S | H | high-energy ALL, TECH |
| Light leak / overexposure burn / film burn | transition | A/transitions/css-light.md | Warm radial overlays; `brightness()` blow-out; amber edge bleed | W (overexposure beats our white flash: it blows out the scene itself) | S | M | HIST, HOR |
| Glitch / chromatic aberration / ripple / VHS tape | transition | A/transitions/css-distortion.md | RGB overlays; cloned-strip VHS with seeded offsets | W | M | H | HOR (VHS), TECH |
| Shutter / clock wipe | transition | A/transitions/css-mechanical.md | Mechanical shutter; 9-point polygon clock wipe | W | S | M | HIST and KIDS ("time passes") |
| Grid dissolve | transition | A/transitions/css-grid.md | 12- or 120-cell palette dissolve | W | S | L | TECH |
| Gravity drop / morph circle | transition | A/transitions/css-other.md | Old scene falls away; circle morph | W | S | M | TOON (comedic) |
| Blur through / directional blur | transition | A/transitions/css-blur.md | Heavy blur pass | T (blur cost) | S | L | calm HIST |
| Page burn | transition | A/transitions/css-destruction.md | Noise fire front clips the scene; canvas scorch edge | W (canvas 2D) | M | H | HOR, HIST hero moment |
| Transition registry (5 Tier-B) | transition | A/transitions/TRANSITION-REGISTRY.md | Machine templates (`__OLD__/__NEW__/__T__`) for wrapper-only transitions | W (pattern for our cut injector) | S | M | infra |
| Mood and energy tables | guide | A/transitions/overview.md | Energy/mood → transition, durations, presets, "1 primary + 1-2 accents" | W | S | M | infra ALL |

### 1d. Shader transitions (`@hyperframes/shader-transitions` 0.8.181; also `reg:<same-name>` demo blocks)

All 14 rows share one status: **T**. At render time the engine blends them on the CPU, in Node worker threads, so no WebGL is needed (see note 3a). What needs testing is the CPU cost at 1080x1920 and the fact that the whole render switches to the layered screenshot route. Effort is M for each: one `HyperShader.init` per composition, plus `.scene` restructuring.

| shader | kind | what it does | ret | best for |
|---|---|---|---|---|
| domain-warp (`reg:domain-warp-dissolve`) | shader | Organic FBM noise warp with a glowing edge | H | HOR, HIST dream or flashback |
| ridged-burn | shader | Ridged-noise burn with sparks | H | HOR, high-energy |
| thermal-distortion | shader | Heat shimmer rising from below | M | GEO deserts and heat, calm |
| cross-warp-morph | shader | Noise morph blending both scenes | M | HIST then→now, GEO |
| sdf-iris | shader | Iris with a glowing ring | M | TOON, KIDS |
| ripple-waves | shader | Concentric ripple distortion | M | KIDS, HIST flashback |
| swirl-vortex | shader | Spiral plus noise warp | M | KIDS, TOON dream |
| gravitational-lens | shader | Gravity-well warp with chromatic fringe | M | KIDS space, TECH |
| glitch | shader | Block displacement and scanlines | M | HOR, TECH |
| chromatic-split (`reg:chromatic-radial-split`) | shader | RGB channels separate from the centre | M | TECH |
| light-leak | shader | Warm leak with flare | M | HIST |
| cinematic-zoom | shader | Radial zoom blur with fringing | L (we have zoom-through; this only adds the fringe) | ALL |
| whip-pan | shader | Horizontal motion-blur pan | L (we have blurred whip push) | ALL |
| flash-through-white | shader | Flash to white | L (we have it) | ALL |

### 1e. Registry blocks (sub-compositions with their own size and timeline; 1920x1080 unless stated)

| item | kind | path | what it does | feasibility | eff | ret | best for |
|---|---|---|---|---|---|---|---|
| north-korea-locked-down | block | reg:north-korea-locked-down | Realistic map zoom into a country, red scribble circle, pop-up label, red wash (PNG map asset) | W (swap in our map plate) | M | H | GEO hooks |
| world-map | block | reg:world-map | D3 Natural Earth choropleth with country-by-country reveal, labels and globe inset | W (vendor d3, topojson-client, world-atlas from npm) | M | H | GEO, FIN (by country) |
| us-map / -bubble / -flow / -hex | block | reg:us-map, us-map-bubble, us-map-flow, us-map-hex | US choropleth, city bubbles, flow arcs, hex tile map (inline SVG + D3) | W (us-atlas via npm) | M | M | GEO (US topics), FIN |
| spain-map | block | reg:spain-map | Admin-1 choropleth (es-atlas, conic projection); template for any country's regions | W (other countries need admin-1 TopoJSON from GitHub raw) | M | M | GEO |
| nyc-paris-flight | block | reg:nyc-paris-flight | Plane flies an arc between cities with marker circle, landing pop and SFX wav | W (swap PNG map and cities) | M | H | GEO routes and travel |
| bar-chart-race | block | reg:bar-chart-race | Ranked bars overtake as time advances; the axis rescales | W | M | H | GEO (populations), FIN |
| data-chart | block | reg:data-chart | NYT-style bar + line chart reveal | W | M | M | FIN, GEO |
| mk-line-graph / mk-progress-stat / mk-specs-list | block | reg:mk-line-graph, mk-progress-stat, mk-specs-list | Series draw-on with labels; big numeral with progress; checklist rows | W | M | M | FIN |
| apple-money-count | block | reg:apple-money-count | $0→$10,000 counter, green flash, money-icon burst, SFX | W (we have count-up; the burst and SFX are new) | S | H | FIN hooks |
| flowchart-vertical / flowchart | block | reg:flowchart-vertical (1440x2560), reg:flowchart | Decision tree with SVG connectors and sticky notes | W (portrait version exists) | M | M | FIN ("how the scam works"), KIDS |
| split-flap-board | block | reg:split-flap-board | Solari board; each cell walks its drum to the target text | W | S | H | GEO place names, HIST dates |
| cinemagraph | block | reg:cinemagraph | Still photo with one feathered living region (seek-pure loop) | W | M | H | HIST and GEO (AI stills come alive), HOR |
| camera-dolly-zoom | block | reg:camera-dolly-zoom | Vertigo dolly zoom (CSS `perspective` + `preserve-3d` layers) | W (feed our depth plates) | M | H | HOR, GEO, HIST |
| camcorder-hud | block | reg:camcorder-hud | REC dot, battery, date, running counter overlay | W | S | H | HOR found footage |
| freeze-frame-dressing | block | reg:freeze-frame-dressing | Paper, tape and flash dressing for a freeze-frame or cut-out subject | W | S | H | TOON, FIN, ALL with cut-outs |
| editorial-flash-overlay | block | reg:editorial-flash-overlay | Warm, neutral camera-flash light layers | W (we have a plain white flash; this is a warmer variant) | S | L | ALL |
| organic-light-leak-overlay | block | reg:organic-light-leak-overlay | Finite CSS light leak for memory beats | W | S | M | HIST |
| snow / starfield | block | reg:snow, reg:starfield | Seek-safe snow; twinkling 2-layer star parallax; centre kept clear | W | S | M | GEO (poles), HOR, KIDS space |
| beat-freeze-cut | block | reg:beat-freeze-cut | Speed ramp, freeze hit, hard cut | W | M | M | ALL montage |
| hw-write-title | block | reg:hw-write-title | True pen write-on of Caveat glyphs (baked strokes; ships woff2) | W | S | H | HIST, KIDS titles |
| hw-path-text | block | reg:hw-path-text | Handwriting flows along any SVG path | W | S | M | GEO (label along a river or border) |
| hw-text-cloud | block | reg:hw-text-cloud | Hand-drawn speech bubble with tail; text types in; boils | W | S | H | TOON, KIDS |
| hw-title / hw-frame / hw-pipeline | block | reg:hw-title, hw-frame, hw-pipeline | Handwritten title sweep; doodle frame; wobbly box diagram | W | S | M | KIDS, TOON |
| hw-scribble-transition | block | reg:hw-scribble-transition | Scribble bands cover the frame and clear (overlay transition) | W | S | H | KIDS, TOON |
| mk-clone-wall-transition | block | reg:mk-clone-wall-transition | Tiled word wall covers, inverts and clears | W | S | M | ALL bold |
| mk-callout-highlight | block | reg:mk-callout-highlight | Word emphasis driven by one scalar synced to the voiceover | W | S | M | ALL |
| mk-placeholder-grid | block | reg:mk-placeholder-grid | 2-up to 3x2 media grid box-in | W | S | M | GEO, HIST image sets |
| message-thread-reveal | block | reg:message-thread-reveal (1080x1920) | Full phone text conversation with typing dots, link card and receipts | W (vertical already) | S | H | FIN scams, HOR text stories |
| thread-message-stack | block | reg:thread-message-stack | Editable message stack | W | S | M | FIN, HOR |
| notes-reveal | block | reg:notes-reveal (1080x1920) | Notes-app confession typed, then a paper card | W | S | M | HOR, FIN |
| notification-cascade | block | reg:notification-cascade (1080x1920) | Phone notifications stack up | W | S | M | FIN (scam alerts) |
| chatgpt-exchange / claude-exchange / ai-chat-reveal | block | reg:… (1080x1920) | AI chat UIs with streamed answers | W (brand-styled UI; use for commentary only, and consider de-branding) | S | M | TECH AI news |
| reddit-post / x-post / yt-comment-card | block | reg:reddit-post, x-post, yt-comment-card | Social post and comment overlays | W | S | M | HOR (Reddit stories), TECH, FIN |
| news-ticker / lower-third-bild | block | reg:news-ticker, lower-third-bild | Broadcast ticker; news lower third | W | S | M | TECH, FIN news |
| oscilloscope-trace | block | reg:oscilloscope-trace | CRT beam with phosphor decay | W | S | L | HOR, TECH |
| vfx-anamorphic-flare | block | reg:vfx-anamorphic-flare | Canvas 2D anamorphic streak field | T (full-frame 2D canvas cost) | S | L | TECH, sci-fi |
| lottie-character-walk | block | reg:lottie-character-walk | Jointed Lottie character walks, stops and points; GSAP stage | W (vendor lottie-web; mascot.json in block) | M | H | TOON, KIDS |
| carousel-orbit-1..5 / circle-1..5 / path-1..5 / vision-1..5 / text-circle-1..5 | block | reg:carousel-* (25) | Image cards on a sphere, circle, bezier path or 3D ring (12-24 slots) | W (DOM 3D; vertical re-layout) | M | M | GEO and HIST "top 10" galleries |
| transitions-* (13 showcases) | block | reg:transitions-3d … transitions-scale | Working code for every CSS transition family | W (reference source) | S | M | infra |
| exploded-stack | block | reg:exploded-stack | three@0.184 isometric layers explode with labels | T (three version clash with our r149; SwiftShader cost) | M | M | GEO (Earth or atmosphere layers), KIDS |
| spiral-galaxy | block | reg:spiral-galaxy | 20k-point galaxy with differential rotation (three@0.147) | T (version clash; point cost) | M | M | KIDS space, TECH |
| gallery-tunnel | block | reg:gallery-tunnel | Infinite corridor of image panels (three@0.147) | T (version clash) | M | M | HIST ("through time"), GEO |
| canopy-part-title | block | reg:canopy-part-title | Leaves sweep and part to reveal a headline (three@0.170) | T (version clash, DoF cost) | M | M | GEO nature titles |
| extruded-logo / product-turntable | block | reg:extruded-logo, product-turntable | Bevelled 3D letters; GLB turntable | T (three version) | M | L | channel intro; spin a 3D globe or prop |
| rack-focus / halftone-field / cosmic-orb | block | reg:rack-focus, halftone-field, cosmic-orb | Raw WebGL full-frame bokeh, halftone and nebula-orb shaders | T (heavy per-pixel shaders on SwiftShader) | M | L | HIST, TECH backgrounds |
| wireframe-portal-title / glass-shard-title / code-slice-hero | block | reg:… | Post-processed 3D titles | T, probably too slow (post-processing, HDR, shadows on SwiftShader) | L | L | TECH |
| code-typing / code-highlight / code-diff | block | reg:code-typing, code-highlight, code-diff | Token typing, line highlight, diff | W | S | L | TECH |

### 1f. Registry components (paste-in snippets, no fixed size)

| item | kind | path | what it does | feasibility | eff | ret | best for |
|---|---|---|---|---|---|---|---|
| camera-shake | component | reg:camera-shake | 9 measured handheld/tele/wide/rig shake profiles with rotation; closed-form, seek-safe | W (better than our micro-jitter: real lens profiles plus roll/tilt) | S | H | HOR, impacts ALL |
| motion-blur | component | reg:motion-blur | After Effects-style shutter integration via `data-hf-motion-blur` (see note 3b) | W | S | H | ALL slams and whips |
| shutter-slam | component | reg:shutter-slam | One word through 6 beats under shutter blur | W | S | M | hooks |
| echo-smear / echo-trail / extended-keyframe | component | reg:echo-smear, echo-trail, extended-keyframe | Speed-adaptive echo streak; onion-skin ghosts; "never fully lands" arrival | W | S | M | TOON (onion skin), ALL |
| whip-pan-cut | component | reg:whip-pan-cut | Both scenes on one strip, one `power3.inOut` tween, blur capped at 16 px and peaking mid-whip | W (adopt only if our whip lacks exact seam velocity matching) | S | L | ALL |
| char-slam-explode | component | reg:char-slam-explode | Glyphs held in scatter, then slam together with a 3-frame landing shake | W (new vs our number slam) | S | H | hooks ALL |
| headline-slam | component | reg:headline-slam | Heavy headline lands with a 3-frame shake, drifts, whips up on exit | W | S | M | hooks |
| text-match-cut / type-match-cut / match-cut | component | reg:text-match-cut, type-match-cut, match-cut | One line becomes the next at peak speed; headline splits around a panel; shape match cut | W | S | H | ALL |
| strikethrough-replace | component | reg:strikethrough-replace | Strike old text, reveal the replacement | W | S | H | FIN (myth→fact), GEO |
| marker-highlight / inline-highlight | component | reg:marker-highlight, inline-highlight | Hand marker stroke (highlight, circle, underline, scribble) on cue | W | S | H | ALL explainers |
| vox-annotate | component | reg:vox-annotate | Marker on a keyword plus a connector to a mono callout label | W | S | H | GEO, FIN, HIST |
| cursor-annotate | component | reg:cursor-annotate | Marker pen draws a loop, underline or arrow around a region, then lifts | W | S | H | GEO maps, FIN screenshots |
| hw-arrow / hw-box-label / hw-callout-circle / hw-underline / hw-boil | component | reg:hw-* | Wobbly hand-drawn arrows, boxes, circles, underlines; boil jitter on quantised time | W | S | H | ALL, especially KIDS, TOON, GEO |
| yt-circle-pointer / yt-feather-highlight | component | reg:yt-circle-pointer, yt-feather-highlight | Draw-on ellipse with countdown chip; dim everything except a feathered spotlight | W | S | H | GEO, FIN |
| whiteboard-ink | component | reg:whiteboard-ink | Whiteboard sketch drawn stroke by stroke with a pen nib | W | S | H | KIDS, HIST |
| arc-motion-path / offset-path-traveler | component | reg:arc-motion-path, offset-path-traveler | MotionPath flight along an arc with auto-rotate; traveler on an authored path | W (vendor the GSAP MotionPathPlugin) | S | H | GEO routes, migrations, trade |
| svg-stroke-trace / outline-draw / tracing-beam | component | reg:svg-stroke-trace, outline-draw, tracing-beam | Path trace and fill; conic outline draw; glowing dash visits elements | W | S | M | GEO, KIDS |
| pull-back-reveal | component | reg:pull-back-reveal | Tight detail holds, then one decelerating pull-back recontextualises it | W | S | H | GEO, FIN |
| pan-stations / scroll-camera-story | component | reg:pan-stations, scroll-camera-story | Lateral pan with a dwell at each station; forced-scroll parallax story | W | M | H | HIST timeline, GEO |
| focus-rack / focus-swap | component | reg:focus-rack, focus-swap | Focus shift between two depth cards (blur, dim, scale, parallax) | T (blur cost) | S | M | ALL A/B |
| yt-camera-move | component | reg:yt-camera-move | Zoom, slide and 3D tilt-pan helpers plus an edge-defocus pulse | W (overlaps our camera; the defocus pulse is new) | S | M | ALL |
| parallax-zoom / parallax-unzoom / camera-rig-depth-stack | component | reg:… | Card fills the frame while siblings parallax out (or the reverse); depth stack | W | S | M | GEO and HIST galleries |
| caption-kinetic-slam | component | reg:caption-kinetic-slam | Full-screen single-word captions with alternating entrances | W | S | H | hooks ALL |
| caption-emoji-pop | component | reg:caption-emoji-pop | Stroked captions with emoji and a squeeze entrance | W | S | H | KIDS, FIN, TOON |
| caption-highlight | component | reg:caption-highlight | Red TikTok-style sweep behind the active word | W (alternative to our karaoke) | S | H | ALL |
| caption-glitch-rgb | component | reg:caption-glitch-rgb | RGB aberration captions with CRT scanlines | W | S | H | HOR, TECH |
| caption-parallax-layers | component | reg:caption-parallax-layers | Text behind the subject (we have cut-outs to put in front) | W | S | H | ALL with cut-outs |
| caption-blend-difference | component | reg:caption-blend-difference | `mix-blend-mode: difference` text that auto-inverts against the background | W | S | M | ALL (legibility over busy plates) |
| caption-texture / texture-mask-text | component | reg:caption-texture, texture-mask-text | Lava, marble or rock texture inside letters (66 ambientCG masks, CC0) | W | S | M | HIST, GEO (rock, ice titles) |
| caption-matrix-decode / -neon-glow / -neon-accent / -gradient-fill / -editorial-emphasis / -clip-wipe / -particle-burst / -camera-follow / -weight-shift / -pill-karaoke | component | reg:caption-* | Ten more caption looks (scramble, neon, gradient, dual-font, wipe, particles, camera follow, weight shift, pill karaoke) | W | S | M | TECH (matrix, neon), others ALL |
| rgb-glitch-text / scan-band / scramble-reveal / matrix-decode | component | reg:… | RGB jitter window; chromatic scan band; hacker scramble lock-in | W | S | M | HOR, TECH |
| kinetic-type-swap / kinetic-center-build / line-swap / caret-swap / morph-text | component | reg:… | Rolling word slot; centre-build; masked line swap; caret retype; gooey word morph | W | S | M | ALL hooks |
| Text entrance set (17) | component | reg:soft-blur-in, blur-in, focus-blur-resolve, per-word-rise, per-word-crossfade, staggered-fade-up, bottom-up-letters, top-down-letters, tracking-in, blur-out-up, shared-axis-y, shared-axis-z, line-by-line-slide, typewriter, text-shimmer, shimmer-sweep, colorama-wipe | Licensed GSAP versions of the `animate-text` effect names | W (blur variants need a cost test) | S | M | ALL |
| slot-machine-roll / number-wheel / number-pop-in | component | reg:… | Reel digits; rolling odometer; blur-lift digit pop | W | S | H | FIN prices, GEO ranks |
| variable-axis-type / variable-font-flex / mk-emphasis-type | component | reg:… | Weight and width axis emphasis; huge low-contrast background word | W (needs a local variable font) | S | M | ALL |
| chart-story / decline-chart / animated-bar-chart | component | reg:… | Bars, line, donut or progress landing exact values; falling line with a darkening background | W | S | H | FIN |
| conic-progress-ring / mk-usage-arc / star-rating-fill | component | reg:… | Ring fill with count; gauge; fractional star sweep | W | S | M | FIN (fake reviews), GEO % |
| before-after-wipe / comparison-split | component | reg:before-after-wipe, comparison-split | Persistent divider wipe between two slots | W | S | H | GEO and HIST then/now, FIN |
| grade-split-reveal | component | reg:grade-split-reveal | Flat-to-graded hard edge sweep, hold, commit | W | S | M | HIST (colourised photo) |
| iris-reveal | component | reg:iris-reveal | Circle `clip-path` from an authored origin; dims the before state | W | S | H | TOON, KIDS |
| torn-paper-rip / paper-collage-reveal | component | reg:… | Fibrous paper tear lifts away; torn scraps scatter | W | S | H | HIST, KIDS, FIN |
| curtain-reveal | component | reg:curtain-reveal | Pleated stage curtains open, plus a spotlight | W | S | M | TOON, KIDS story openers |
| ink-bleed-reveal | component | reg:ink-bleed-reveal | Gooey ink bloom through paper (SVG blur + threshold) | T (SVG filter cost) | S | M | HIST, HOR |
| halftone-dissolve / grid-pixelate-wipe / chromatic-aberration-wipe / fade-through / morph-swap / rubber-band-bumper | component | reg:… | Halftone, pixel or RGB wipes; wash fade; condense morph; elastic snap | W | S | M | TECH (pixel, RGB), TOON (rubber band) |
| particle-image-reveal / particle-text-dissolve | component | reg:… | Seeded particles converge to reveal an image; text to and from particles (canvas) | T (canvas particle cost at 1080x1920) | M | H | ALL reveals of AI images |
| ordered-dither-pass / slit-scan-reveal / ascii-render-pass / ascii-trail-reveal | component | reg:… | Bayer dither emerge; slit-scan time smear; live ASCII render; ASCII sweep | T (canvas rasterises the scene once at mount, so it cannot take live 3D) | M | M | HOR (dither, slit-scan), TECH (ASCII) |
| light-sweep-pass | component | reg:light-sweep-pass | Key light crosses and re-shades a slotted scene | W | S | M | titles ALL |
| segmentation-flood / telemetry-hud | component | reg:segmentation-flood, telemetry-hud | AI segmentation masks with labels; mono HUD readouts | W | S | H/M | TECH, HOR, GEO ("AI scans terrain") |
| grain-overlay / vignette | component | reg:grain-overlay, reg:vignette | CSS-keyframe film grain (CSS-animations adapter); radial vignette | W | S | M | HOR, HIST |
| yt-screen-warp | component | reg:yt-screen-warp | Grid, scanline and sheen plus a 3D-warp "footage on a display" wrapper | W | S | M | HOR, TECH |
| stop-motion-cadence | component | reg:stop-motion-cadence | Quantises time to `floor(t*fps)/fps` for stepped, boiled motion | W | S | H | TOON, KIDS |
| pendulum-swing / physical-exit / spring-pop / icon-morph-beat | component | reg:… | Damped hanging-sign swing; toss, drop or slide exit; badge pop; icon state morph | W | S | M | TOON, KIDS |
| confetti / beat-accent / beat-pulse-background / beat-timeline | component | reg:… | Seeded confetti; music-hit sting; beat-grid glow; label-pinned beat spine | W | S | M | KIDS, music beats, infra |
| chat-thread / chat-message / typing-indicator / notes-typing | component | reg:… | iMessage-faithful thread, bubbles, typing dots, notes typing | W | S | H | FIN scams, HOR |
| native-notification-pop / notification-pileup / notification-stack | component | reg:… | iOS banner on a real spring; accelerating anxious pile-up; stack | W | S | H | FIN scams, TECH |
| radial-surround / overwhelm-surround / scroll-feed | component | reg:… | Chips ring and converge on the subject; overload closes in; doomscroll feed | W | S | M | FIN, HOR |
| constellation-hub / grid-card-assemble / split-tilt-cards / avatar-cloud | component | reg:… | Hub-node connectors; card grid; book-open A/B; avatar network | W | S | M | FIN, GEO, TECH |
| ticker-takeover / titlecard-calm / titlecard-lockup / logo-sting / cta-close / cta-lockup | component | reg:… | Ticker lock and promote; chapter cards; channel sting; end cards | W | S | M (sting and chapters) / L (CTA) | ALL |
| typed-prompt / streaming-text / terminal-simulator / device-frame-stage | component | reg:… | Prompt typing; AI-cadence word streaming; terminal log; phone or tablet prop | W | S | M | TECH |
| aurora-drift / grain-field / mesh-gradient-bg / dynamic-grid / drift-hold | component | reg:… | DOM ambient backgrounds and loop-exact drift | W | S | L | ALL fill |

### 1g. Adapters, techniques and tools

| item | kind | path | what it does | feasibility | eff | ret | best for |
|---|---|---|---|---|---|---|---|
| Lottie adapter (Characters section) | adapter | A/adapters/lottie.md | `window.__hfLottie` seek contract; the character owns its body and GSAP owns the stage; no per-animation start offset (author offsets inside the file) | W | M | H | TOON, KIDS |
| Three.js adapter | adapter | A/adapters/three.md | `hf-seek` / `__hfThreeTime`; `window.__hf.buildReady[...]` hold for heavy builds; one constant per camera cut; pinned pixel ratio | W (we use r149; adopt `buildReady` and the cut-constant rule) | S | M | 3D videos |
| CSS animations / WAAPI / Anime.js adapters | adapter | A/adapters/css-animations.md, waapi.md, animejs.md | Seekable CSS keyframes (`play-state`/`delay`), `element.animate()`, Anime.js | W | S | L | grain and shimmer loops |
| GSAP easing and stagger | adapter | A/adapters/gsap-easing-and-stagger.md | Ease families mapped to mood; "≥3 eases per video" | W | S | M | ALL |
| Techniques #2, #8, #9, #11, #12 | technique | A/techniques.md | Canvas2D hash art; variable-font axes; MotionPath; audio-reactive JSON (per-frame `tl.call`); clip-path masks with glyph padding | W (#11 needs `extract-audio-data.py` from the hyperframes-creative skill) | S | M | ALL |
| animation-map audit | script | A/scripts/animation-map.mjs | Samples every tween's bbox and flags dead zones, stagger drift and lifecycle issues | T (bootstraps the HyperFrames package from npm; needs Chromium) | S | M | QA, ALL |
| html-in-canvas patterns | adapter | A/adapters/html-in-canvas-patterns.md | DOM to texture via `drawElementImage`, then shatter, portal, liquid or CRT post-fx | B (CanvasDrawElement in headless_shell plus SwiftShader is not supported per typegpu.md; liquid glass needs Brave or Canary) | L | M | TECH |
| TypeGPU / WebGPU | adapter | A/adapters/typegpu.md | WGSL canvases; `data-requires-webgpu`; `PRODUCER_ALLOW_SOFTWARE_WEBGPU=true` runs on SwiftShader "several times slower" | T / slow | L | L | backgrounds |
| animate-text (24 named effects) | adapter | A/adapters/animate-text.md | Points to the external `pixel-point/animate-text` skill | B (licence: "no explicit license declared upstream"; use the registry text-entrance set instead) | – | – | – |

### 1h. WebGPU background shaders (36, `reg:<name>`, 2 s loops from shaders.com, MIT)

| item | kind | path | what it does | feasibility | eff | ret | best for |
|---|---|---|---|---|---|---|---|
| aurora, godrays, lens-flare, prism, sun-burst, strands, light-edge | block | reg:… | Light, sky and flare loops | T (WebGPU: software-only via `PRODUCER_ALLOW_SOFTWARE_WEBGPU`, several times slower). Better: render each 2 s loop once to MP4 and use it as a `<video>` plate | M once | M | GEO (aurora), HIST, TECH |
| fractal-noise, gabor-noise, worley-noise, voronoi, marble, ripples, falling-lines, stripes, spiral, sine-wave, waveform | block | reg:… | Texture and pattern loops | same as above | M once | L | HOR (noise), TECH |
| plasma, mesh-gradient, flowing-gradient, color-wheel, swirl, blob | block | reg:… | Gradient loops | same as above | M once | L | backgrounds |
| chrome-orb, frost, goo, heatmap, hologram, holographic, liquid-metal, nebula, obsidian, plastic, thin-film, water | block | reg:… | Material orb loops | same as above | M once | L | TECH, KIDS (nebula, water) |

**Skipped: no use for narrated Shorts (pure UI or product-demo, brand ads, or blocked)**
- Rules: anchored-layout-expand, camera-cursor-tracking, context-sensitive-cursor, control-target-sync, cursor-click-ripple, cursor-drag, multi-cursor-choreography, physics-press-reaction, press-release-spring.
- Blueprints: agent-progress-theater, cursor-ui-demo, device-surface-showcase, panel-edit-live-sync, prompt-type-submit-generate, transcript-scroll-artifact-reveal, cta-morph-press.
- Examples: demo-page-scroll-spotlight, cta-morph-press, cta-orbit-collapse, workflow-approve-press, proof-logo-chain.
- Blocks: ai-answer-rank, app-showcase, blue-sweater-intro-video, heygen-avatar-promo-card, slack-notification-ad, share-sheet-carousel, vpn-youtube-spot, spotify-card, macos-notification, instagram-follow, tiktok-follow, yt-lower-third, yt-logo-intro, yt-lcd-background, yt-prism-title, yt-vertical-fill, logo-outro, mk-background, week-in-merges, ui-3d-reveal, orbit-card, cuboid-carousel, code-3d-extrude, code-morph, code-particle-assemble, code-scroll, code-shader-dissolve, code-snippet-apple-terminal-pro, code-snippet-dark-2026, code-snippet-dark-modern, glass-hero, all 12 lt-* lower thirds.
- Blocked html-in-canvas blocks: ios26-liquid-glass, macos-tahoe-liquid-glass, liquid-glass-notification, liquid-glass-widgets, vfx-iphone-device, vfx-liquid-background, vfx-liquid-glass, vfx-magnetic, vfx-portal, vfx-shatter, vfx-text-cursor, filmed-screen.
- Blocked WebGPU 3D: frost-sequence-camera-orbit.
- Components: agent-cursor, avatar-group-hover, badge-pop, browser-device-stage, camera-scan-gate, card-resize, code-terminal-run, cursor-context-menu, cursor-drag-drop, cursor-glyph-trail, cursor-marquee-select, cursor-text-select, cursor-zoom-follow, dart-cursor, gesture-tap, gloss-sweep, facet-morph, icon-swap, input-feedback, keyframe-scrub-stack, locked-nucleus-orbit, logo-brand-close, logo-wall, magnetic-cursor, marker-checklist-card, menu-morph, micro-transitions, modal-morph, multi-device-splay, multiplayer-cursors, onboarding-stepper-flow, oversized-cursor, page-slide, panel-reveal, parallax-device-dive, perspective-marquee, press-ripple, pull-to-refresh, screen-flow-carousel, separator, settings-toggle-flow, sheet-spring-up, signup-flow, skeleton-reveal, social-proof-card, soft-blob-touch, spotlight-card, spring-stack-shuffle, stagger-cascade, stagger-lattice, state-chip-rail, sticky-mock-swap, stitched-text-draw, store-badge-lockup, success-check, svg-line-draw-loader, swipe-rail, svg-mask-reveal, tabs-slide-indicator, testimonial-card, testimonial-proof-card, text-stagger, text-state-swap, three-orbiting-cards, tilt-card, toggle-flip, touch-indicator, trust-strip, ui-focus-zoom, vector-editor-rig, velocity-throw-snap, wordmark-tiles, x-follow-card.

---

## 2. Top 15 for retention (ranked)

1. **reg:north-korea-locked-down.** Open a GEO Short on a satellite plate that slams into the target country, gets a red scribble circle and a "LOCKED DOWN"-style label. That is a ready-made 2-second hook.
2. **reg:world-map (plus the us-map family).** Data-driven choropleths reveal country by country as the narration lists them, and D3 and world-atlas are both on npm, so they render offline.
3. **reg:nyc-paris-flight + reg:arc-motion-path / offset-path-traveler.** A plane or marker flies an arc between two places, with a landing pop and SFX, for routes, migrations, trade and "how far is…" beats.
4. **Annotation family (reg:hw-callout-circle, hw-arrow, vox-annotate, cursor-annotate, yt-circle-pointer, yt-feather-highlight).** Every 2-3 s a hand-drawn circle, arrow or spotlight lands on the exact thing the voice names, which is a cheap pattern interrupt.
5. **Phone-text family (reg:message-thread-reveal, chat-thread, native-notification-pop, notification-pileup).** Scam SMS and horror text stories play out bubble by bubble, already at 1080x1920, so viewers stay to read the next message.
6. **reg:camera-shake.** The handheld-strong and tele profiles, with roll, sell horror scares and impacts far better than our micro-jitter. Fire it on the jump-scare frame and on number slams.
7. **reg:cinemagraph.** Bring Codex history and geography stills to life with one moving region (smoke, water, flag) so a static image never reads as a slideshow.
8. **reg:char-slam-explode + rules/kinetic-beat-slam.** Scattered glyphs slam into the hook headline with a 3-frame shake, and following phrases use distinct entrances on one beat grid.
9. **reg:bar-chart-race.** "Largest countries by X, 1950→2025" or "who loses most to scams" as an overtaking race carries a built-in "who wins?" curiosity loop.
10. **Caption style pack (reg:caption-kinetic-slam, caption-highlight, caption-emoji-pop, caption-glitch-rgb, caption-parallax-layers).** Pick a style per channel (glitch for horror, emoji-pop for kids and finance) and put text behind our character cut-outs for depth.
11. **reg:pull-back-reveal / blueprints/zoom-out-workspace-reveal.** Hold tight on a detail ("this tiny island…"), then one decelerating pull-back reveals the continent. A strong re-hook at the 20-30 s mark.
12. **reg:split-flap-board.** Place names, dates and prices flip in Solari style for openers and chapter cards.
13. **reg:motion-blur (`data-hf-motion-blur`).** Real shutter smear on the 1-3 fastest beats per video (slam, whip, spin) makes 2D moves feel filmed, and it costs nothing to the three.js canvas (see note 3b).
14. **Horror treatment stack (reg:camcorder-hud + grain-overlay + vignette + rgb-glitch-text / rules/chromatic-glitch + the VHS transition).** A found-footage look across the whole Short for NISHACHAR.
15. **reg:before-after-wipe / grade-split-reveal.** Then/now maps, a colourised history photo, or a scam page vs the real page, with a divider the eye tracks.

Honourable mention for TOON and KIDS: **reg:lottie-character-walk** with **reg:stop-motion-cadence**, **reg:hw-text-cloud** and **reg:iris-reveal**.

---

## 3. Notes

### 3a. How shader transitions fit an existing GSAP timeline and DOM scenes

Sources: `pkg/README.md`, `pkg/dist/index.js` (minified), `cli/chunk-HODBPO4A.js`, `cli/chunk-3GXQPCJC.js`.

**API.** `HyperShader.init({ bgColor, accentColor?, scenes:[ids], transitions:[{time, shader?, duration=0.7, ease="power2.inOut"}], timeline?, compositionId? })`. The IIFE global is `HyperShader`, from `dist/index.global.js` (256 KB, with html2canvas 1.4.1 bundled; MIT).

`init` throws unless:
- `scenes.length === transitions.length + 1`;
- every scene id exists; and
- every scene has `class="scene"`.

**So every scene boundary must be listed.** An entry without `shader` is an opacity crossfade.

**Render path (what matters for us).**

When the engine sets `window.__HF_VIRTUAL_TIME__`, `init` takes the engine branch (`function vf`). In that branch it:
- creates no WebGL canvas;
- does no html2canvas capture;
- does no `drawElementImage`.

It only writes `window.__hf.transitions = [{time, duration, shader, ease, fromScene, toScene}]` and adds opacity flips to the timeline:
- At t=0, scenes 2..n get opacity 0.
- At a shader boundary, `to` is set to opacity 1 at `T` and `from` to 0 at `T+dur`.
- Crossfade entries get `fromTo` opacity tweens.

**The engine detects shader use by regex on inline scripts:**

`/\bHyperShader\s*\.\s*init\s*\(|\b__hf\s*\.\s*transitions\s*=/` (`cli/chunk-HODBPO4A.js`, `detectShaderTransitionUsage`).

So the call must sit in an inline `<script>` as literal `HyperShader.init(`. Calling it through an ESM import (`init(`) or a renamed alias is not detected, and the render silently degrades to hard opacity cuts.

**What the engine then does with `hasShaderTransitions`:**
- It switches the whole render to the `hdr_layered` plan: `forceScreenshot: true`, no parallel stream.
- On a transition frame, it captures scene A and scene B separately (`captureSceneIntoBuffer`, showing only that scene's element ids on a transparent background) into rgb48 buffers.
- It then blends them with a **CPU port** of the shader (`TRANSITIONS[shader]` in `cli/chunk-3GXQPCJC.js`, the same 14 names plus `crossfade`), run in a `worker_threads` pool (`shaderTransitionWorkerPool.ts`).
- On normal frames it composites the layer stack (`compositeHdrFrame`).

**Consequences for us:**
- **No WebGL or WebGPU is needed for the blend, so SwiftShader is not a blocker.** The costs are:
  - two screenshot captures per transition frame;
  - CPU shader math at 1080x1920 for about 21 frames per transition;
  - the slower screenshot and layered route for every frame of the video.
- Benchmark one 60 s render before adopting.
- The engine's sub-frame `motionBlur` route throws on `hdr_layered` (`motionBlurRoute.ts`), and so does `--resolution` scaling.
- **Opt-in page-side compositing.** It is enabled by `EngineConfig.enablePageSideCompositing` and the `__HF_PAGE_SIDE_COMPOSITING__` stub, and it uses `drawElementImage` plus WebGL in the page. If either is missing it logs and falls back to the Node pipeline above. On our headless_shell with SwiftShader, expect that fallback.
- **Preview path only (`hyperframes preview`/Studio):**
  - Scenes are pre-captured via `drawElementImage` if CanvasDrawElement exists, otherwise via html2canvas.
  - Captures are cached in IndexedDB.
  - The blend runs on a `#gl-canvas` (z-index 100).
  - html2canvas cannot read a WebGL canvas whose `preserveDrawingBuffer` is false (the bundled code warns exactly this). **Three.js scenes therefore show blank or stale inside shader transitions in preview, but not in the final render.**
  - The "shader-compatible CSS rules" in `A/transitions/overview.md` (no `transparent` in gradients, no `var()` on captured elements, explicit `.scene` background equal to `bgColor`) are about this html2canvas path. They are harmless to follow anyway.

**Existing-timeline integration.** Pass `timeline: tl` with our paused `window.__timelines.main` (the README shows this). In engine mode, with a timeline passed, it appends a dummy `{t:0→1}` tween of `data-duration` from the root, **defaulting to 40 s if the attribute is missing**, so always set `data-duration`.

Note that `A/transitions/overview.md` instead says "let it create the timeline (don't pass `timeline:`)". Both work; ours must keep `window.__timelines.main` as one timeline.

**What breaks with our current structure:**
- (1) The package owns scene-wrapper opacity, so our own six cut types cannot run on the same wrappers. Workaround: make each HyperShader `.scene` a group of several of our story scenes, keep our CSS cuts inside a group, and use shader transitions only at group boundaries.
- (2) The layered capture needs every element of a scene to be a descendant of that `.scene`. Global overlays (captions, emoji props) are composited by stacking order, so z-index needs a test so captions don't vanish or double during the blend.
- (3) Three.js canvases inside a scene are captured by screenshot, which is fine in principle. But during the overlap both scenes' `hf-seek` renders run, so 3D cost doubles for those frames. An `alpha:true` canvas over a transparent capture background needs a visual check for premultiplied edges.

### 3b. Motion blur, exactly

Source: `A/references/motion-blur.md`; snippet at `reg:motion-blur` (`registry/components/motion-blur/motion-blur.html`).

**Contract: one attribute.** Paste the snippet, then mark the elements that move:
- `data-hf-motion-blur` with an empty value means defaults.
- Otherwise use a JSON object, e.g. `data-hf-motion-blur='{"shutterAngle": 360}'`.
- A marked element attaches automatically once the timeline of its nearest `data-composition-id` ancestor registers. The registry is polled for about 8 s after load.
- `attachMotionBlur(target, timeline, options)` is only for elements created later, and must be called after every tween is added.

**Options. Exactly these five; anything else is refused by name:**
- `shutterAngle`, default 720 (two frames).
- `shutterPhase`, default -360 (centred).
- `samplesPerFrame`, default 16, max 64.
- `fps`, default the root's `data-fps`, else 30.
- `sharp`, default 1. With 0, only the smear shows.

There is no axis, strength or radius: the smear is speed × shutter time.

**Mechanism.** After each frame update, the snippet:
1. seeks the timeline (events suppressed, so no callbacks fire) to N sub-frame times;
2. reads each target's resolved `transform`;
3. stacks N+1 copies of the element subtree in an isolated group at 1/N opacity with `mix-blend-mode: plus-lighter`;
4. paints the sharp element on top.

The group hides when the element is at rest.

**Cost as stated.** Each target costs N+1 copies of its whole subtree, restyled on attach and resize and re-transformed every frame, plus N+1 timeline seeks per frame:
- **17 copies and 17 seeks per target per frame at default 16.**
- "Three marked elements is fine. Thirty is a different render."
- `samplesPerFrame: 8` halves the cost.

**Measured numbers.**
- The defaults come from a 1920x1080 30 fps After Effects export of translating text.
- Staircase step: 0.063 ± 0.002 per copy, flat 1/16.
- Triangle weighting scores 1.6 dB worse.
- PSNR gain over sharp: translate +3.38 dB, scale +0.62, rotateX +0.43, rotateY +0.84, rotateZ +1.15.
- Example: 2000 px/s at 30 fps smears 133 px.

**Silent failures:**
- tweening `left/top/width/height`;
- marking a container whose children move;
- an ancestor doing the moving (the smear lags);
- reparenting after attach;
- selecting by a class (copies carry it).

**Don't blur** travel under one element-width per frame, fades, text meant to be read, slow drifts, or whole scenes. Use it on 1-3 snapping beats per video.

**Our pipeline.**
- Because sampling seeks GSAP with events suppressed, three.js scenes driven by `hf-seek` are not re-rendered, so the extra cost is DOM-only.
- **Never mark an element containing a `<canvas>`.** The copies are DOM clones and would be blank.
- The second route, the engine's whole-frame `motionBlur`, does true sub-frame accumulation. Engine defaults: 180° shutter, -90° phase, 16 samples adapting to 32 or 64, PNG capture. That is about 16-64 full captures per moving frame, impossible at our 0.45 s/frame for 3D.
- In 0.8.181 I found no CLI flag or env var for that route (only `job.config.motionBlur` in `cli/chunk-HODBPO4A.js`), and it is incompatible with shader transitions.

### 3c. WebGPU-only registry items: 40

- **36 shaders.com backgrounds (tag `webgpu-shader`):** aurora, blob, chrome-orb, color-wheel, falling-lines, flowing-gradient, fractal-noise, frost, gabor-noise, godrays, goo, heatmap, hologram, holographic, lens-flare, light-edge, liquid-metal, marble, mesh-gradient, nebula, obsidian, plasma, plastic, prism, ripples, sine-wave, spiral, strands, stripes, sun-burst, swirl, thin-film, voronoi, water, waveform, worley-noise.
- **Plus 4:** frost-sequence-camera-orbit, ios26-liquid-glass, liquid-glass-notification, liquid-glass-widgets.

The shader blocks carry `data-requires-webgpu`. Per `A/adapters/typegpu.md`, the engine passes `--enable-unsafe-webgpu`. On a GPU-less host, rendering needs `PRODUCER_ALLOW_SOFTWARE_WEBGPU=true`, which runs on SwiftShader "several times slower". The liquid-glass ones also need CanvasDrawElement together with WebGPU, which "stock Chromium and the bundled headless-shell do not support"; they need Brave or Canary via `PRODUCER_HEADLESS_SHELL_PATH`. Treat those as blocked.

Separately, 12 html-in-canvas items need `drawElementImage`, and 9 of them are not WebGPU: macos-tahoe-liquid-glass, vfx-iphone-device, vfx-liquid-background, vfx-liquid-glass, vfx-magnetic, vfx-portal, vfx-shatter, vfx-text-cursor, filmed-screen. Treat them as blocked too.

**Practical route for the 36 loops:** they are 2 s seamless loops. Render each one once (slow software WebGPU is fine, or in a GitHub Actions job), commit it as an MP4 or WebM, and use it as a looping `<video>` plate.

### 3d. What `hyperframes add <name>` needs

Source: `hf-src/skills/hyperframes-registry/SKILL.md`, plus `references/install-locations.md` and `discovery.md`.

- **Host.** It fetches from the `registry` URL in `hyperframes.json`. The default is `https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry`, which is **GitHub raw, so our workspace can reach it**. I fetched `registry/registry.json` and several item files successfully.
- Install targets: blocks go to `compositions/<name>.html`, components to `compositions/components/<name>.html`, and item assets (PNG maps, wav, json, woff2) alongside.
- Registry dependencies install first. A tag name installs every block with that tag.
- Use `--no-clipboard` and `--json` in CI. Examples use `hyperframes init <dir> --example <name>`, not `add`.
- **Network is needed for every add:** "`add` still needs the network, even for an item you installed yesterday. Only manifests are cached; the item's actual files are fetched on every install." The manifest has a 24 h TTL and stale copies keep serving discovery.
- `catalog --query` search is local. `--on-device` semantic search needs a consented ~33 MB model plus vectors download into `~/.hyperframes/` (host not stated in the skill; unverified whether it is GitHub raw).
- **Render-time network.** Installed files still point at `cdn.jsdelivr.net` (gsap@3.14.2, d3@7, topojson-client, world-atlas@2, us-atlas@3, es-atlas@0.6.0, three@0.147/0.170/0.184, lottie-web@5.12.2) and `fonts.googleapis.com`. Preview media sits on `static.heygen.ai`, but that is unused at render time. With no network at render, rewrite these to vendored npm copies at `add` time. A small post-add script that rewrites `https://cdn.jsdelivr.net/npm/<pkg>@<v>/…` to `vendor/<pkg>@<v>/…` from `node_modules` covers them all.
- **Three.js clash.** Blocks pin three@0.147, 0.170 or 0.184 as globals, while our compositions use r149. Two global THREE builds in one page will conflict, so port those blocks to r149, or keep them in separately rendered segments.
