# HyperFrames 0.8.181: reusable graphics, maps and story tools for our Shorts pipeline

Base path for every citation: `hf-src/skills/` (under the scratchpad). The audit is read-only. Nothing was run.
Our pipeline: 1080x1920 at 30 fps, 60–100 s, one HF composition with a GSAP timeline, Chromium headless_shell 1194 with SwiftShader, no network at render. The workspace can reach npm, pip and GitHub raw. A GitHub Actions (GHA) job can reach the full internet.
Effort scale: S < 0.5 day, M 0.5–2 days, L > 2 days.

---

## 1. Maps deep-dive

### 1.0 What the sources actually ship (vs what the docs imply)

| Claim in docs | Reality in code | Consequence for us |
|---|---|---|
| Vector lane reuses `us-map`, `world-map`, `spain-map` (`motion-graphics/categories/maps/module.md`, `catalog-map.md`) | These are hosted registry blocks (`npx hyperframes add`). They are not in `hf-src`. | Treat them as reference at most; the hosted registry may be unreachable from the workspace (Test needed). |
| `geo-highlight`, `geo-flow`, `flag-borders`, `pin-rollout` | Explicitly **hand-author only**: no code, just "signatures" (`maps/module.md` lines "Hand-author these"; `catalog-map.md` allow-list comment) | The only map code shipped is `bake-basemap.mjs`. Everything else is a recipe we implement ourselves in SVG. |
| "Globe intro" | **Not implemented.** The bake hardcodes `projection:{type:"mercator"}`. The globe is listed as a "stretch: extend bake-basemap.mjs". | Our three.js globe already does this better. |
| Capability menu: "`grounding/locate.mjs` (geocode)" (`hyperframes/references/capability-menu.md`) | **Wrong.** `locate.mjs` is image-region grounding (a strip grid read by the model) and has no geocoder. | Lat/lon still has to come from Natural Earth populated places or our own gazetteer. |
| Sub-national regions | Not supported (world-atlas is country-only). The docs say "use Natural Earth admin-1". | We already have NE admin-1, so we are ahead here. |

### 1.1 `bake-basemap.mjs` fully dissected (`motion-graphics/categories/maps/bake-basemap.mjs`, 273 lines)

**Env vars**

| Var | Default | Meaning |
|---|---|---|
| `NAME` | `basemap` | Output stem: `<NAME>.mp4`, `<NAME>-coords.json`, `frames-<NAME>/f%04d.png` |
| `STYLE` | `satellite` | `satellite` (Esri World Imagery), `dark` or `light` (CARTO), or **any raw `{z}/{x}/{y}` URL template** |
| `CENTER` | `2.6,46.6` | `lng,lat`. The camera never pans; it only zooms about this point. |
| `ZSTART`/`ZEND` | 4.2 / 5.4 | MapLibre zoom (512-px world) |
| `PITCH`/`BEARING` | 0 / 0 | Interpolated from 0 to the value with the same ease (0 at the start, never at the start value) |
| `FPS`/`DUR` | 30 / 5 | Frame count N = round(FPS·DUR) |
| `HOLD` | 0.5 | Fraction p at which the zoom finishes. Every frame after it is an identical held frame, still baked one by one. |
| `KEEPMARGIN` | `16,13` | Lon/lat box around the vertex-richest polygon. It keeps near islands and drops overseas territories. |
| `COUNTRIES` | — | `"Name:#hex,..."`. Names must match world-atlas `properties.name` **exactly** (e.g. "United States of America", "Dem. Rep. Congo"). |
| `OUT` | cwd | Output dir |
| `CHROME` | auto | Path to a headless shell. It otherwise searches `~/.cache/puppeteer/chrome-headless-shell`, then system Chrome. |

**Mechanics**
- Puppeteer-core runs with `--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader`. That is **already software WebGL, the same as our renderer.**
- Before every screenshot it runs `jumpTo(camAt(p))`, then `await idle` with a 9 s timeout. On timeout it checks `areTilesLoaded()`, because CARTO/Esri `idle` is flaky. If any frame times out it exits with code 1 and the message "fail loud".
- The map is set up with `fadeDuration:0`, `preserveDrawingBuffer:true` and `maxTileCacheSize:6000`.
- The ease is `easeInOutCubic`.
- It encodes all-intra with ffmpeg: `-g 1 -crf 16 -pix_fmt yuv420p +faststart`. Every frame is a keyframe, so the clip seeks safely in HF.
- **coords.json** is captured on the first frame where p ≥ HOLD. Shape: `{view:{center,zoom,pitch,bearing}, countries:[{name,color,d,bbox:{x,y,w,h},label:{x,y}}]}`.
  - `d` is the SVG path built from per-vertex `map.project()`.
  - `label` is the **vertex average** of the mainland ring, which is poor for concave countries.
  - Antimeridian handling: longitudes are unwrapped around `CENTER[0]` before projecting. It warns if the span is still over 180°.

**Hard limits for us**

| # | Limit | Fix | Effort |
|---|---|---|---|
| 1 | Viewport hardcoded **1920x1080** (CSS, `setViewport`, `clip`) | Add `W`/`H` env (1080x1920). Fitting a country across 1080 px needs about 0.83 less zoom (log2 1920/1080). | S |
| 2 | Libraries load from **cdn.jsdelivr.net**: maplibre-gl 5.24.0, topojson-client 3.1.0, world-atlas 2.0.2. jsdelivr is not npm, so this **fails in our workspace.** | `npm i` the three pinned versions. Use `page.setRequestInterception(true)` and answer the jsdelivr URLs from `node_modules`. The bake then runs offline. | S |
| 3 | Tiles come from Esri and CARTO, which have licence problems for monetized YouTube (see 1.2). | Point `STYLE` at a **local tile pyramid** served through the same interception (`http://tiles.local/{z}/{x}/{y}.jpg`), or use a file template from GHA. | S (wiring) |
| 4 | Borders come from `countries-110m.json`, which visibly jags at z ≥ 5 over imagery. | world-atlas `countries-50m.json` (npm), or our NE 10m admin-0/admin-1 GeoJSON via a new `FEATURES=path.geojson` env | S |
| 5 | Zoom-only camera with no pan or multi-leg move | Use `d3.interpolateZoom` (van Wijk smooth zoom/pan, in npm d3-interpolate) for a `[cx,cy,w]` path, and set the camera per frame from it | S–M |
| 6 | The overlay is valid **only during the hold** (the docs say so) | Pitch 0 / bearing 0 web-mercator is a similarity transform. Export `camAt(p)` for every frame (`frames.json`). In HF, drive one CSS `scale(2^(z(t)−ZEND))` + translate on the overlay `<g>` (`vector-effect:non-scaling-stroke`). Borders then stick **during** the zoom too. | S |
| 7 | Hold frames are baked one by one (wasted SwiftShader time) | Bake only the frames where p ≤ HOLD and hold on a PNG of the last frame in HF | S |
| 8 | Vertex-average labels | Use `polylabel` (npm, pole of inaccessibility), or `d3.geoCentroid` and then the legibility nudge | S |
| 9 | No admin-1 | Feed NE admin-1 GeoJSON (we have it) through change 4 | S |

**Key equivalence, so MapLibre is not needed for alignment.** At pitch 0 and bearing 0, `map.project()` gives the same screen coordinates as `d3.geoMercator().center(CENTER).scale(512·2^z/(2π)).translate([W/2,H/2])`. MapLibre's world width is 512·2^z, as `module.md` "Tile world-scale" notes. So coords.json can be generated in pure Node with d3-geo, against **any** raster that is web-mercator at a known zoom and center. MapLibre's real value is **level-of-detail tiling for deep zooms** (more than about 4x zoom range in one move). Alignment does not need it.

### 1.2 Tile sources used, their terms, and free offline alternatives

| Source in bake | Endpoint | Terms (checked 2026-10-22) | Verdict for monetized Shorts |
|---|---|---|---|
| Esri World Imagery (`satellite`) | `server.arcgisonline.com/.../World_Imagery/MapServer/tile/{z}/{y}/{x}` | Free use needs an ArcGIS Developer account, **no ad/subscription revenue**, under 1M tiles/mo, and attribution to "Esri, Maxar, Earthstar Geographics". Commercial use goes through Esri pricing. ([OSM wiki: Esri](https://wiki.openstreetmap.org/wiki/Esri)) | **Do not use.** Monetized YouTube is revenue-generating. |
| CARTO dark_all / light_all (`dark`/`light`) | `a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png` | Commercial use is free up to 1M req/mo, and "© CARTO, © OpenStreetMap" must stay visible. **Since 25 Sep 2026, raster `dark_all`/`light_all` need an API key** ([CARTO basemaps FAQ](https://docs.carto.com/faqs/carto-basemaps), [terms](https://carto.com/legal/basemap-terms/)). | Probably **broken as shipped** (no key in the script). It would also need a CARTO account. Avoid. |

**Free, offline-capable replacements**

| Need | Source | Terms | How we get it | Max useful zoom |
|---|---|---|---|---|
| Satellite look, world to region | **Our NASA Blue Marble NG** raster (already in the 3D pipeline) | Public domain; credit "NASA Earth Observatory" | Python (numpy/Pillow, pip). Equirectangular to web-mercator is a pure **row remap** (y = ln tan(π/4+φ/2)). Cut a z0–7 pyramid to `tiles/bm/{z}/{x}/{y}.jpg`, about 21k tiles at z7. Or cut **one plate per shot** at the target bbox. | ≈ z7–8 (500 m/px source) |
| Satellite look, pre-tiled | **NASA GIBS** WMTS, e.g. `BlueMarble_ShadedRelief_Bathymetry`, `VIIRS_CityLights_2012` (night lights look great for "population" Shorts) | NASA open data. GIBS asks for an acknowledgement (credit "NASA GIBS / EOSDIS"). | **GHA job** (GIBS is not reachable from the workspace). Fetch a bbox pyramid and commit to the repo as library art. | z8 for Blue Marble layers |
| Satellite, city/country zoom (z9–13) | Our **Landsat** fetch (GHA) or **EOX Sentinel-2 cloudless 2016** (`s2cloudless_3857`; the 2016 edition is CC BY 4.0, later editions are NC. *Verify before use*) | Landsat: USGS public domain. EOX 2016: "Sentinel-2 cloudless by EOX — contains modified Copernicus Sentinel data 2016". | GHA fetch of only the bbox pyramid needed per episode | z13+ |
| Dark/light "broadcast" basemap | **Natural Earth** land/ocean/coast/admin-0/admin-1 (public domain, no credit required), styled by us | PD | Already in our SVG pipeline. As a MapLibre GeoJSON source if baking. | any (vector) |
| OSM-detail dark basemap (roads/cities) | OpenFreeMap or Protomaps PMTiles extract | ODbL: "© OpenStreetMap contributors" | GHA: `pmtiles extract --maxzoom 10 --bbox` | z14 |
| Relief | Our AWS terrain tiles (Terrarium) → hillshade (numpy) multiplied over the plate | Credit the terrain-tile sources (SRTM/GMTED/ETOPO1, etc.) | Existing GHA job | z12+ |

**Attribution rule to keep (module.md "Attribution — hard rule"):** whenever imagery is on screen, show a small low-corner credit element in the composition, e.g. "Imagery: NASA Blue Marble · Borders: Natural Earth". Keep a credits map keyed by source so the builder auto-inserts it.

### 1.3 Every map capability: how we would do it in our pipeline

| Capability (source) | What it is | Our implementation | Feasibility | Effort | Value |
|---|---|---|---|---|---|
| **geo-highlight** (`maps/module.md` vector lane) | N countries filled with a stagger, labels, border pulse | Existing NE SVG: fill-in stagger plus a **border `stroke-dashoffset` draw-on**, gated with `autoAlpha:0` before the draw (`asset-fusion/module.md` gotcha). The pulse is a finite yoyo on the tl. | Works | S | H |
| **geo-flow arcs** | World arcs or a hub network, drawn on, with a "flyer" | `d3.geoPath` on a `LineString` (d3 densifies it into a projected great circle). Draw it on with dashoffset. Move the flyer (dot/plane/ship SVG) with one proxy tween `{u:0→1}` whose `onUpdate` calls `getPointAtLength(u·L)` and `atan2` for heading. That is seek-safe, never `tl.call`. | Works | S–M | H (trade routes, migrations, scam money trails, invasion paths) |
| **flag-borders** | Flag clipped into the country shape | `<clipPath id="c" clipPathUnits="userSpaceOnUse"><path d=…/></clipPath>` plus `<image href="flags/in.svg" x,y,w,h=bbox preserveAspectRatio="xMidYMid slice" clip-path="url(#c)">`. Flags from npm **`flag-icons`** (MIT SVG). Reveal by fading the flag over the draw-on border. | Works | S | H (BHUGOL signature look) |
| **pin-rollout** | Cities pulse in sequence plus a counter | NE `populated_places` for lat/lon. Each pin drops (`back.out` is allowed here) with a pulse ring (scale 0.6→2.2, opacity 1→0, finite repeats on the tl). The counter is a proxy tween with `onUpdate` and `tabular-nums`. | Works | S | H |
| **choropleth** | Colour reveal driven by data | d3-scale + d3-scale-chromatic (npm). Data from OWID/World Bank CSVs on GitHub raw. Reveal by sweeping west to east (stagger by centroid lon) or by value rank. A legend only if needed (`data-in-motion.md` says no legends; prefer a direct label on 2–3 extremes). | Works | S–M | H |
| **labels** | Country/city names | Use `polylabel` anchors with offsets and clamp to safe area. Legibility rule: no pill over a border or another label, readable ≥ 0.3 s (`module.md` Legibility). | Works | S | M |
| **viewBox zoom** | Camera by animating the SVG `viewBox` | GSAP `attr:{viewBox:"x y w h"}`. The docs prefer it to hand-computed group transforms. It stays vector-crisp, while a composited CSS-scaled layer can blur. Put the raster plate **inside** the same SVG (`<image>`) so plate and vectors share one camera. Keep our CSS camera for image plates outside maps. | Works | S | H |
| **zoom-to (camera path)** | Jump from the world to a target | `d3.interpolateZoom` for the viewBox path. For deep dives (over 4x), crossfade a world plate into a regional plate at the hold, or use the bake. | Works | S | H |
| **callout-card** ("documentary popup", `module.md`) | Pinned card: flag chip, stat, progress bar | HTML card anchored at the projected point. **Animate the outer wrapper only (opacity, y); the inner div keeps `translate(-50%)`.** A centring transform plus GSAP y/scale overwrite each other (`module.md` Determinism). Count up the stat with a proxy tween and fill the bar with scaleX. | Works | S | H |
| **Basemap lane: satellite zoom-to** (`bake-basemap.mjs`) | Real imagery zoom, then a hold | **Option A (pure SVG, preferred):** a Blue Marble or Landsat plate cut per shot in Python at the end zoom, in the SVG camera, with NE paths from d3 mercator. No WebGL, deterministic, about 2x–4x zoom range. **Option B (local bake):** patched bake (fixes 1–9) with tiles served locally from our pyramid. Handles z2→z10 dives with LOD; SwiftShader is fine for raster tiles. | A: Works · B: Test needed (MapLibre 5 needs WebGL2 under SwiftShader, which the script's own flags imply works) | A: S–M · B: M | H |
| **Basemap lane on GHA** | Same bake, run on a GHA runner | Viable for fetching tiles (GIBS, Landsat, EOX). Do **not** use the shipped Esri/CARTO URLs. Commit `<NAME>.mp4` + coords/frames JSON to the repo. | Works (needs the GHA job extended) | M | M |
| **Globe intro** (stretch) | MapLibre globe easing into mercator (MapLibre 5.0+, [roadmap](https://maplibre.org/roadmap/maplibre-gl-js/globe-view)) | **Use our three.js globe** (Blue Marble + terrain). Hand over to the 2D map with a **flash or zoomIn cut** at a matched zoom so small framing mismatches are hidden. MapLibre globe would duplicate what we have and is untested under SwiftShader. | Works (ours) | S | H |
| **coords.json export** | Geo to screen paths, bbox, label | Generate in Node: d3-geo mercator at the same center/zoom/W/H (equivalence in 1.1). Add a per-frame camera to stick overlays during moves. Output schema identical to the bake's, so either source feeds one overlay builder. | Works | S | H |
| **Flag clipPath into real borders** (validated `smooth-flag`, `module.md`) | Flag texture over satellite context | Same as flag-borders, but over the plate, with a `mix-blend-mode:multiply` or 0.85 opacity variant so the terrain shows through | Works | S | H |
| **Mainland filter** (`KEEPMARGIN`) | Drop overseas territories that blow up the bbox | Port the 10-line `mainland()` function into our SVG builder. It fixes France+Guiana, USA+Hawaii and similar framing. | Works | S | M |
| **Antimeridian unwrap** | Russia, Fiji, NZ smearing | d3 `geoPath` already clips the antimeridian. Port `unwrapLon` only for custom per-vertex projections. | Works | S | M |
| **Pre-hold hidden state** | A bare `fromTo` does not apply its "from" until the tween starts, so overlays show early | Run `gsap.set(hidden)` at build time for every overlay revealed later. Add this to our QA lint. | Works | S | H |
| **Attribution element** | Credit when imagery is visible | Credits component keyed by source (see 1.2) | Works | S | H (compliance) |
| **Out of scope in sources** | 3D photoreal landmarks (Cesium) | We cover terrain flyovers with three.js; no change. | — | — | — |

**Recommended maps plan.** (1) Add geo-flow, flag-borders, pin-rollout, callout-card, choropleth and border draw-on to the existing SVG map module (all S). (2) Build a Python plate cutter from Blue Marble, giving web-mercator crops by bbox, plus a d3 coords generator, so imagery highlights need no WebGL. (3) Do the local MapLibre bake (patched) only when a Short needs a continuous world-to-city dive, with tiles prefetched by GHA from GIBS, Landsat or EOX-2016.

---

## 2. Every other reusable item

Feasibility key: **W** = works with our stack · **T** = test needed (why) · **B** = blocked (why).
Channel key: G geography · H horror · F finance/scams · T tech · A AI history · K kids · C cartoon.

### 2a. motion-graphics

| Item | Path | What it does | Feas. | Eff. | Val. | Channels |
|---|---|---|---|---|---|---|
| locate grid-grounding | `motion-graphics/grounding/locate.mjs`, `PROTOCOL.md` | Finds a target in an image by having the model pick numbered strips on a 9x9 grid, then on a 6x6 crop grid, then `mark` to verify. Measured centre error 6.5% → 2.3%. Needs node and ffmpeg (drawtext with DejaVu TTF). The optional `auto` mode uses GEMINI_API_KEY; ask before routing his key. | W | S | H | G H F T A |
| Circle-highlight template | `motion-graphics/samples/asset-fusion/_ref-circle-highlight.html` | From one box it computes a radial wash, an amber double ring, connector, label, corner brackets and scanlines. `CFG.mode` is `full` or `circle`. Static even `data-width/height` are required. | W (set 1080x1920) | S | H | H (circle the figure), G, F |
| Asset-fusion logic | `motion-graphics/categories/asset-fusion/module.md`, `catalog-map.md` | The asset's geometry becomes the chart (straw as gauge, glass as pie). Affordance map: linearity → gauge, volume → pie, height → bar. Eyedropper palette. | W | M | M | F G K |
| Render gotchas | `asset-fusion/module.md` "Render gotchas" | Even W/H; static `data-width` attrs; draw-on needs `autoAlpha` gating plus `getTotalLength() \|\| const`; scope CSS var tweens to the element; no camera push under a fixed overlay | W | S | H | all |
| News marker-band highlight | `motion-graphics/categories/news/module.md` | Keyword band grows via `background-size` with `box-decoration-break:clone`, so it **wraps across lines**. Swept on after the text settles, never zoomed. Layout A (9:16 centered sentence) fits Shorts directly. | W | S | H | T F A G |
| News Layout B article card | same | Logo, date, serif headline, dek, person cutout sliding up. 16:9 spec, so it needs a 9:16 re-layout. The cutout needs `hyperframes remove-background` (model download; untested here). | T | M | M | T F A |
| Tweet card | `categories/tweet/module.md` (registry `x-post`) | Card in, type-on text, metrics count-up | T (registry reachability) – or hand-build W | S–M | M | T F |
| Webpage capture animation | `categories/webpage/module.md` | `hyperframes capture`, then scroll-through, spotlight, cursor click-ripple and zoom to the real DOM rect. Rules: `3d-page-scroll`, `coordinate-target-zoom`, `cursor-click-ripple`. | B in workspace (capture needs site network) / W on GHA | M | M | F (scam sites), T |
| Stat ring | `categories/stat/module.md` | Count-up proxy, ring `stroke-dashoffset` finishing in sync with the count, label **after** the number lands | W | S | M | F G T |
| Charts / bar-chart-race | `categories/charts/module.md`, `catalog-map.md` | `data-chart` (bar+line) and `bar-chart-race` blocks; dashboard skeleton variant | T (registry) / hand-build W | M | H (race: "top 10 countries by X, 1960–2025") | G F A |
| Logo sting | `categories/logo-reveal/module.md` | `logo-outro`, `svg-path-draw` draw-on, mask/scale plus glow, alpha export | W | S | M | all channel idents |
| Lower-thirds / social overlays | `categories/lower-thirds/module.md` | Bar wipe (`scaleX`, origin left) with text slide; `yt-lower-third`, subscribe cards | W (hand) / T (registry) | S | M | all |
| Shot-plan IR | `motion-graphics/references/shot-plan-ir.md` | One JSON contract: envelope, asset_needs, block, content per category | W | S | M | pipeline |
| Motion vocabulary | `motion-graphics/references/motion-vocabulary.md` | Named entry/emphasis/exit primitives mapped to GSAP recipes (slam, scale_punch, fade_blur, wave, glow, underline_sweep, hold_breath) | W | S | M | all |
| Builder contract | `motion-graphics/references/builder-contract.md` | Size the root; `fromTo` inside `.clip`; count-ups only render when seeks fire events (a bare `seek(t,true)` freezes them at 0); palette in one object | W | S | H (QA) | all |
| Director heuristics | `motion-graphics/agents/director.md` | One dominant motif; **pattern-interrupt changing exactly one thing past ~2.5 s**; a key element readable ≥ 0.3 s; anticipate beats by ~0.1 s | W | S | H | all |
| Finalize/repair loop | `motion-graphics/agents/finalize.md` | Snapshot QA (overflow, off-canvas, collisions, empty frames), one in-place fix, recheck; never change duration to hide a defect | W | S | M | QA |

### 2b. hyperframes-creative

| Item | Path | What it does | Feas. | Eff. | Val. | Ch. |
|---|---|---|---|---|---|---|
| Load-bearing GSAP rules | `hyperframes-creative/references/motion-principles.md` | Never two concurrent transform tweens on one element (split entrance to parent and Ken Burns to child); `fromTo` over `from` in clips; ambient loops on `tl`, never bare `gsap.to`; hard-kill inner elements at boundaries with `tl.set` | W | S | H (lint rules) | all |
| Motion guardrails | same | ≤ 2 tweens per scene share an ease; slowest scene 3x slower than fastest; vary entry direction; first anim offset 0.1–0.3 s; build 0–30% / breathe 30–70% / resolve 70–100%; exits faster than entrances; full stagger < 500 ms | W | S | H | all |
| Velocity-matched transitions | `references/beat-direction.md` | Exit `power2/3.in` plus blur ramp, entry `.out` plus blur clear, velocities matched within ~5% at the cut. Quick picks with numbers (whip x±400 blur 24 px 0.3 s; zoom-through 1→1.2 / 0.75→1). | W | S | M (tightens our whip/zoom) | all |
| Shader transitions (14) | `references/beat-direction.md` table | domain-warp, ridged-burn, sdf-iris, ripple, gravitational-lens, cinematic-zoom, chromatic-split, swirl-vortex, thermal-distortion, flash-through-white, cross-warp-morph, light-leak, glitch | T (registry install, and WebGL cost under SwiftShader) | M | M (H: glitch / thermal for horror) | H T A |
| CSS transition families | same (→ `hyperframes-animation/transitions/css-*.md`) | 30+ patterns: blinds, shutter, clock wipe, grid dissolve, page burn, light leak, VHS | W (DOM/CSS) | S each | M | H K C |
| Audio-reactive mapping | `references/audio-reactive.md`, `scripts/extract-audio-data.py` | Per-frame FFT bands as JSON (numpy + ffmpeg). Maps bass to scale and treble to glow. Text swings 3–6%, backgrounds 10–30%. Bans EQ bars and orbs. Use one `onUpdate` that indexes `frames[floor(t·fps)]`, not 2,700 `tl.call`s. | W (pip numpy) | S | M (H: drone swells drive vignette) | H C K |
| Narration pacing & TTS numbers | `references/narration.md` | 2.5 wps, so 60–100 s ≈ 140–230 words; write numbers as spoken ("nearly two trillion"); vary hook type; ~2.3 wps leaves pauses | W | S | H | all (also for Hindi: write lakh/crore out) |
| Video-composition scale | `references/video-composition.md` | Video sizes: headline 64–120, body 28–42, labels 18–24, decorative opacity 12–25%, borders 2–4 px. **No full-screen linear gradients on dark (H.264 banding).** Two focal points; anchor to edges. | W | S | H | all |
| Typography rules | `references/typography.md` | 18 **bundled offline fonts**. Bundled and not on the banned list: Montserrat, Oswald, League Gothic, Archivo Black, Space Mono, IBM Plex Mono, JetBrains Mono, Source Code Pro, Noto Sans JP. League Gothic and Archivo Black ship weight 400 only. In-feed floor: headlines ≥ 90 px, body ≥ 32 px. Tracking −0.03 to −0.05 em. **No Devanagari is bundled**, so Hindi needs our own `@font-face` woff2 (e.g. `@fontsource/noto-sans-devanagari`, `@fontsource/mukta` via npm) or the Google fetch fails closed. | W | S | H | all, esp. Hindi versions |
| Visual styles (8) | `references/visual-styles.md` | Named styles with mood routing: Shadow Cut (dark exposé) for H/F, Data Drift for A/T, Swiss Pulse for G/F data, Folk Frequency for K, Maximalist Type for T | W | S | M | all |
| Palettes (9) | `hyperframes-creative/palettes/*.md` | Curated 5-colour rows per mood (dark-premium, nature-earth, neon-electric, …) | W | S | L–M | all |
| Frame presets (13) | `hyperframes-creative/frame-presets/<name>/FRAME.md` | Token files (colours, type ramp in cqw, components) with 9:16 guidance; `frame-showcase.html` previews. Several use non-bundled fonts (e.g. Barlow), so ship woff2 (only `code-editorial` bundles its fonts). | W | S–M | M | per-channel brand kits |
| Caption skins | `frame-presets/*/caption-skin.html` | Karaoke skins with a fixed token vocabulary (`--cap-ink`, `--cap-accent`, …). States `.is-active`/`.is-spoken` via **`gsap.set({className})`, never `tl.call`**. | W | S | M (we have karaoke; adds per-channel looks) | all |
| House style | `references/house-style.md` | Lazy-default list (gradient text, left accent stripes, cyan-on-dark, pure #000/#fff, identical card grids); 2–5 background decoratives | W | S | M | all |
| Text-behind-subject | `references/composition-patterns.md` | Headline between a base and a cutout. Opacity goes on a **wrapper div** (the framework forces `opacity:1` on timed clips). Both layers start at t=0 to avoid decoder jitter. For stills, a PNG cutout is enough. | T (cutout tool: `hyperframes remove-background` or pip `rembg` model download) | S–M | H (hooks and thumbnails) | G H A T |
| Data-in-motion | `references/data-in-motion.md` | Same visual space for successive stats; every number gets a weight object (bar, ring, fill); no pie, gridlines or legends | W | S | M | F G |
| Contrast report | `hyperframes-creative/scripts/contrast-report.mjs` | Seeks N times, measures WCAG contrast of each text element against the **actual pixels behind it** (text paint hidden), outputs a magenta/yellow/green overlay sprite, exit 1 on AA fail | T (bootstraps `@hyperframes/producer` from npm; SwiftShader) | S | H (captions over satellite/AI plates) | all |
| Storyboard stills recipe | `references/storyboard-recipe.md` | Pose each shot at its key moment, `snapshot --at` all at once into `boards/stills`, review board before animating | W | S | H (catches layout before slow renders) | all |
| Prompt expansion | `references/prompt-expansion.md` | Seed → per-scene spec: rhythm declaration, depth layers, verb per element, transition params, negative prompt | W | S | M | all |
| Design picker | `references/design-picker.md`, `templates/design-picker.html` | Generated mood-board picker page | W | M | L | branding |

### 2c. faceless-explainer (beyond cut-catalog / motion-language)

| Item | Path | What it does | Feas. | Eff. | Val. | Ch. |
|---|---|---|---|---|---|---|
| VO-paced time-coded shots | `faceless-explainer/references/visual-design.md` | Each frame is a set of `Scene n (a–b s)` windows; **nothing appears before the VO names it**; reveals concentrate in the back ~50%; end on a held read; "front-loaded-then-frozen" is the failure | W | S | H | all |
| Portrait layout rules | same, "Portrait & square" | Stack vertically; centred hero at **y ≈ 0.42·H (≈806)**; avoid split/triptych; bigger type, fewer words per line | W | S | H | all |
| Caption-band keep-out | same | Bottom ~17% reserved for captions; key content in the top 83% | W | S | H (QA check) | all |
| Video direction block | same | Write palette, motion grammar, held-frame allocation and negative list **once**; frames carry deltas | W | S | M | all |
| Framing variety | same, "Layout" | ≥ 3 framings per video, never the same twice in a row; hero 40–60% of frame; ≥ 3 depth layers; squint test | W | S | H (QA) | all |
| focal / roles / sfx tags | same | Per frame: hero element, role per element (foreground / background dimmed 30–50% / supporting), named SFX cue | W | S | M | all |
| Blueprint tagging | `visual-design.md` → `hyperframes-animation/blueprints-index.md` | 22 time-coded shot templates with a signature move, used as Reproduce / Adapt / Compose. Relevant: `spatial-pan-stations` (timeline/map stations), `zoom-out-workspace-reveal` (tight detail then reveal, i.e. "guess the place"), `dataviz-countup`, `kinetic-type-beats`, `fixed-anchor-cycle`, `ticker-takeover`, `overwhelm-surround`, `comparison-split`, `titlecard-reveal`, `grid-card-assemble` | W (1920 examples need re-layout) | M | H | all |
| Transition injector | `faceless-explainer/scripts/transitions.mjs`, `lib/transitions.json` | 5 GSAP templates (crossfade, blur-crossfade, push-slide, zoom-through, squeeze) applied **extend-outgoing-only**, so voice, captions and SFX timing never shift | W | S | M (adopt the principle) | all |
| Caption builder | `scripts/captions.mjs` | Scene-aware word groups with skin injection and brand fonts | W | M | L (we have karaoke) | — |
| Duration sync | `scripts/audio.mjs sync-durations` | Real voice length overrides estimates; synced values are never hand-edited | W | S | L–M | all |

### 2d. music-to-video

| Item | Path | What it does | Feas. | Eff. | Val. | Ch. |
|---|---|---|---|---|---|---|
| Beat-grid analyzer | `music-to-video/scripts/analyze-beatgrid.py` | Deterministic `audiomap.json`: beats/downbeats, onsets (kick/snare/hihat), energy phases, rolls, risers, hard-stops, key_moments, phrases. Needs librosa, numpy, soundfile and ffmpeg. bpm is reliable only on rhythmic music. | W (pip) | S | H (snap slams and cuts to BGM) | all w/ BGM |
| Timing & latency rules | `references/motion-primitive-catalog.md` | **Hard hits are 0 ms `tl.set`**; lead the anchor 40–190 ms so moves *land* on it; eased entrances 300–500 ms; at most one camera move per phrase; builds resolve on a downbeat | W | S | H | all |
| 37 motion primitives | `references/motion-primitives/<id>/scene.html` | All deterministic (no `Math.random`), 1920x1080 sub-comps. Picks: **spotlight-sweep, dolly-zoom, neon-flicker, datamosh-smear, pixel-dissolve, screen-shake** (H); **binary-decrypt, typewriter-reveal, chromatic-split** (T/A); **slot-machine-reveal, counting-punch** (G/F number reveals); iris-open, mask-reveal, outline-to-fill, crash-zoom-in, radial-burst-lines, 3d-card-flip, word-grid-burst, staggered-exit | W (re-layout to 9:16) | S each | H | all |
| WebGL/SVG-filter primitives | `bg-flow-field`, `text-spectral-rays` (WebGL), `gooey-metaball` (feGaussian/SVG filter) | Generative background bed; hero wordmark light rays (one source only, per its USAGE.md); metaball merge | T (SwiftShader / CPU filter speed at 1080x1920) | S–M | M (channel intro sting) | T A |
| Doc-only primitives | listed in catalog, no folder: `content-swap`, `palette-flip`, `freeze-hold`, `negative-space-hold`, `system-replace`, `overlay-pop`, `staggered-reveal`, `value-counter`, `color-grid-shuffle`, `chromatic-pressure` | Patterns described in one line each. `negative-space-hold` and `system-replace` are strong for twists. | W (hand-build) | S | M | H F |
| 9 group templates | `references/templates/*/index.html`, `template-catalog.md` | card-flyby, held-message-living-field (WebGL), held-text-strobe-burst (ships ~70 texture-mask PNGs; licence not stated, names match ambientCG CC0, so verify), intro-kinetic-cascade, logo-split-lockup-pulse, poster-tile-mosaic, roll-flipbook-word-cycle, split-anchor-word-slot, typewriter-phrase-keyword-shuffle. All 1920x1080 and seeded. | W/T (re-layout; the WebGL one under SwiftShader) | M | M (intros, montage hooks) | T A G |
| Asset treatments | `references/montage.md` | `beat_cut` (one clip per anchor), `ken_burns` (calm), `bg_under_text` (dim 30–50%); pacing decides which; clips muted | W | S | M | all |

### 2e. Router, other workflows, adjacent assets the sources point to

| Item | Path | What it does | Feas. | Eff. | Val. | Ch. |
|---|---|---|---|---|---|---|
| Pitch round | `hyperframes/references/pitch-round.md` | Five concepts from five paths (subject world, emotion, audience, inverted anti-pattern, unusual format). **≥ 2 must be under 10% likely** (the anti-median constraint), then a silhouette check | W | S | H (angle ideation) | all |
| Review loop | `hyperframes/references/review-loop.md` | Plan as "This video tells [audience] that [message]" plus a table (frame · beat · on screen · **why**); sketch pass of posed stills; final look; recipe freeze | W | S | H | all |
| Production loop economics | `hyperframes/references/production-loop.md` | Fire all generations concurrently; **batch visual checks into contact sheets** (single-image checks re-price the context); install blocks before parallel work | W | S | M | pipeline |
| BGM voice carve | `hyperframes-audio/scripts/carve.mjs` (referenced by production-loop) | Spectral dips in the music bed where the voice sits plus a level match (better than a plain duck) | T (needs npm `@hyperframes/core`) | S | H (mix quality) | all |
| Bundled SFX pack | `media-use/audio/assets/sfx/` (+ `manifest.json`, `CREDITS.md`) | 20 Pixabay-licence MP3s, **commercial use without attribution**: whoosh ×3, impact-bass ×2, riser, glitch ×3, typing, key-press, click ×2, pop, ping, chime, sparkle, notification, error | W | S | H | all |
| LUT looks | `media-use/luts/index.json` | teal-orange-blockbuster, **bleach-bypass**, film-fade, each with an offline `params` cube builder; apply to plates with ffmpeg `lut3d` | T (`resolve -t lut --local-only` path) | S | M (H: bleach-bypass; A: film-fade) | H A |
| Error-diffusion dither | `media-use/scripts/dither.mjs` | Floyd–Steinberg-family dithering of images (retro / 1-bit / VHS-era look) | W | S | M | H A C |
| Transcribe / transcript-cut | `media-use/scripts/transcribe.mjs`, `transcript-cut.mjs` | Local ASR to word timings (prefers Parakeet-MLX, which is Apple Silicon only, else whisper); cut by sentences | T (Linux path = whisper) | S | L (TTS already gives timings) | — |
| Talking-head card styles | `talking-head-recut/references/styles/*.html` (MIT, `NOTICE.md`) | 10 self-contained card HTML styles: **audit** (manila plus APPROVED stamp), **terminal**, **whiteboard** (Caveat), swiss, editorial, xhs, … Fonts bundled (`assets/fonts`). | W | S | M (F: stamp "SCAM"; T: terminal; K: whiteboard) | F T K |
| Dense-keyframe rule | `talking-head-recut/SKILL.md` §9 | Re-encode every video source with `-g <fps> -keyint_min <fps>`. **A sparse GOP freezes on seek in the renderer.** | W | S | H (baked basemaps, AI clips) | all |
| Portrait card layouts | `talking-head-recut/references/layouts/{stack,pip,split,overlay}.html` | Video plus card zone recipes with GSAP for `#video-wrap` | W | S | L–M (UGC clips) | — |
| Code blocks | `pr-to-video/references/code-vocabulary.md` | code-diff, code-morph, code-typing, code-highlight, code-scroll, code-3d-extrude/particle/shader (WebGL); deterministic and seeded. Gotchas: fit typing cadence to the duration; 0- vs 1-based lines; no caption band. | T (registry) | S–M | M | T A |
| Hook script bank | `product-launch-video/references/story-design.md` § "script bank" | Hook shapes by blueprint: ticker-takeover ("A X? A Y? — no, it's Z"), fixed-anchor-cycle roll-call, typewriter with a mid-line edit, cold-open single stat, overwhelm pile-up | W | S | M | F T A |
| cut-catalog / motion-language diffs | `pr-to-video/references/*`, `product-launch-video/references/*` | **Rules are identical to faceless-explainer's.** Only the genre nouns and "Shipped example" lines differ (PLV cut-catalog adds 2 example lines). `general-video` has none of its own. **Nothing new to adopt.** | — | — | — | — |
| SSIM regression diff | `remotion-to-hyperframes/scripts/render_diff.sh`, `frame_strip.sh` | Per-frame SSIM between two MP4s (summary JSON, threshold env) plus a side-by-side strip. Use it to golden-test our templates after code or Chromium changes. | W (ffmpeg) | S | M–H | pipeline |
| Lottie playback | `remotion-to-hyperframes/references/lottie.md` → `hyperframes-animation/adapters/lottie.md` | Seekable Lottie on the timeline (LottieFiles assets, licences vary) | T | S–M | M | K C |
| Motion-energy PSNR | `figma/scripts/verify-motion.mjs` | Compares choreography of two renders while cancelling static differences (frame-delta PSNR) | W (ffmpeg) | S | L–M (match a reference motion) | — |
| Figma import | `figma/SKILL.md` | REST asset, token and component import (needs `FIGMA_TOKEN`) | T | M | L | — |
| Slideshow | `slideshow/SKILL.md` | Navigable deck; **`render` silently truncates to the first slide's MP4** | B (not an MP4 path) | — | L | — |
| Animation rules (adjacent) | `hyperframes-animation/rules/*.md` | Notables: `asr-keyword-glow` (glow envelope on word timings), `css-marker-patterns` (highlight/circle/scribble/sketchout), `ai-tracking-box` (L-brackets plus confidence, per-frame), `viewport-change` vs `coordinate-target-zoom` (two different counter-translate formulas: `T=−offset·S` vs `T=−offset`), `3d-camera-flight`, `depth-of-field-blur`, `motion-blur-streak`, `svg-path-draw`, `chart-scrub-readout`, `vertical-spring-ticker` | W | S each | H (`css-marker-patterns`, `ai-tracking-box`, `asr-keyword-glow`) | all |

---

## 3. Story and structure tools for the Shorts script stage

Each item adds something beyond what we already use (logline, but/so chain, re-question at ~20 s, payoff at 70–80%, twist ending, joke every 10–15 s).

| # | Tool | Source | What it adds | How to wire into the script stage |
|---|---|---|---|---|
| 1 | **Value by beat 2 plus two delete-tests** | `hyperframes-creative/references/story-spine.md` §2 | Our chain orders *events*; this checks *claim vs evidence*. Delete every evidence beat: the value must still stand. Delete the value beats: if it still "works", it was a fact list. | Script QA asserts `message` lands by ~5–8 s and runs both delete-tests on the beat list |
| 2 | **Hook strategy table (9 named)** | `faceless-explainer/references/story-design.md` "Hook strategy"; `narration.md` "vary the hook type" | Shocking stat, rhetorical question, counterintuitive claim, pain validation, visceral metaphor, concept announcement, direct address, imagine/scenario, stakes. Forces a deliberate choice and **rotation across uploads**. | `hook_type:` field per script, plus a channel-level log so no type repeats 3x in a row |
| 3 | **One structure, no splicing** | story-design.md §3 | concept-explainer / how-to / listicle / story-explainer, or a named compound. Stops hybrid scripts that lose the thread. | `arc:` field; pacing defaults by arc (listicle → cut seams, story → held beats) |
| 4 | **Named persuasion technique per beat** | story-design.md "Clarity / rhetoric technique catalog" | Each beat names *how* it lands: analogy, worked example, before/after, myth vs reality, counterexample, causal chain, **callback to the hook image**, coined term/mnemonic, distillation. A beat that cannot name one gets cut. | `persuasion:` per beat. Prefer **callback** for the final beat, which seeds the Shorts replay loop into the twist. |
| 5 | **Emotional beat vocabulary and arc variation** | story-design.md "Emotional beats" | Valley → pivot → build → resolution words (puzzlement, unease, "aha", inevitability). Checks the arc isn't flat between jokes. | `beat:` per beat; QA flags 3 identical consecutive beats |
| 6 | **VO written as discrete cues** | story-design.md "Script rules"; visual-design.md | Phrase boundaries ("First the X — then the Y — then Z") hand the visuals their reveal cadence; nothing appears before it is spoken | Script lint flags clauses over ~12 words with no break; each cue maps to one reveal |
| 7 | **Source-traceable props** | story-spine.md §4 | Every visual prop must come from *this* subject ("could this prop appear unchanged in another video? swap it") | Storyboard column `source_line:` per visual |
| 8 | **Rhythm declaration plus held beats** | `beat-direction.md` "Rhythm Planning"; visual-design.md "Video direction" | Name the pattern (e.g. `fast-fast-SLOW-fast-HOLD-twist`) before building. **Allocate deliberate held or silent beats** before the turn; silence before a twist is a tool. | `rhythm:` line in the script header; silent beats allowed with an empty VO |
| 9 | **Pattern interrupt every ~2.5 s, changing ONE thing** | `motion-graphics/agents/director.md` | A finer-grained visual cadence under our 10–15 s joke cadence | Retention QA: max gap between visual changes ≤ ~2.5–3 s |
| 10 | **Pitch round with anti-median constraint** | `hyperframes/references/pitch-round.md` | Five angles, ≥ 2 deliberately unlikely, anti-pattern inverted, silhouette check | Topic → angle stage before the logline |
| 11 | **Proposal table with a Why column** | story-spine.md §3; `review-loop.md` §1 | "This Short tells [audience] that [message]" plus frame · beat · on screen · why. A frame whose why doesn't trace to the message gets cut. | Approval message format for the user gate |
| 12 | **Sketch pass (posed stills board)** | `storyboard-recipe.md`; `review-loop.md` §2 | Layout and copy are approved on stills before slow SwiftShader renders | `snapshot --at` key moments, one contact sheet, then animate |
| 13 | **Hook shapes from the launch script bank** | `product-launch-video/references/story-design.md` | Ticker-takeover ("A loan? A gift? — no, it's a trap"), fixed-anchor roll-call, typed-then-edited line | Hook menu for F and T channels |
| 14 | Narration budget plus TTS number spelling | `narration.md` | ~2.3–2.5 wps, so 60 s ≈ 140–150 words and 100 s ≈ 230–250; numbers written as spoken | Word-count gate per target length; number normaliser (EN and HI) |

Skip: story-design's product `type` enum (product_intro, etc.), which is only needed for their pacing engine; the prompt-expansion "always expand" rule, which our pipeline already covers; and the slideshow and Figma flows.

---

## 4. Top 12, ranked

1. **Vector map kit (geo-flow arcs, flag-in-borders, border draw-on, pin-rollout, callout-card, choropleth, viewBox camera)** (`maps/module.md`): add these to BHUGOL's SVG map module so every geography Short gets animated routes, flag-filled countries and pinned stat popups with no new dependencies.
2. **Satellite basemap without Esri/CARTO: Blue Marble/Landsat web-mercator plates plus a d3-generated coords.json** (equivalence in 1.1, patched `bake-basemap.mjs` for deep dives): gives the "satellite with coloured borders" look offline and deterministically, licence-clean for monetized uploads.
3. **locate.mjs grounding plus the circle-highlight template** (`grounding/`, `samples/asset-fusion/`): accurately ring the ghost in the window, the landmark in a photo or the clause in a contract on AI plates, instead of eyeballing coordinates.
4. **Load-bearing GSAP rules and builder gotchas as lint checks** (`motion-principles.md`, `builder-contract.md`, `asset-fusion` render gotchas, maps pre-hold rule): turn them into retention-QA lints to catch invisible elements, frozen counters and early-showing overlays before render.
5. **VO-paced reveals plus portrait layout QA** (`visual-design.md`): enforce reveal-on-cue, hero at y≈806, caption band bottom 17%, ≥ 3 framings and no repeat framing in every Short.
6. **Beat-grid analyzer plus music timing rules** (`analyze-beatgrid.py`, `motion-primitive-catalog.md`): land slams, cuts and count-up locks on BGM downbeats with the 40–190 ms lead, and use 0 ms hard hits.
7. **Motion-primitive library** (`music-to-video/references/motion-primitives/`): port spotlight-sweep, dolly-zoom, neon-flicker and datamosh for Nishachar, plus binary-decrypt, slot-machine-reveal and counting-punch for Tech Minister, Money Mirage and BHUGOL stats, re-laid to 9:16.
8. **News marker-band highlight (Layout A 9:16)** (`news/module.md`): a multi-line keyword sweep over real headlines and quotes for tech news, scam exposés and AI-history citations.
9. **Typography floor plus bundled-font map and a Devanagari fix** (`typography.md`): headlines ≥ 90 px and body ≥ 32 px in feed, bundled distinctive fonts, and our own Noto Sans Devanagari/Mukta woff2 so Hindi versions never fail the font fetch.
10. **Bundled Pixabay SFX pack plus voice carve** (`media-use/audio/assets/sfx/`, `hyperframes-audio/scripts/carve.mjs`): 20 commercial-safe whooshes, impacts, risers and glitches to tag per beat, and a cleaner BGM-under-voice mix once carve is tested.
11. **Story tools: hook-type rotation, persuasion-per-beat with callback ending, delete-tests, pitch round** (`story-design.md`, `story-spine.md`, `pitch-round.md`): add these fields to the script stage so hooks vary, every beat has a job, and the ending loops back to the hook.
12. **Contrast report plus SSIM regression** (`contrast-report.mjs`, `render_diff.sh`): add automated WCAG checks of captions and labels against real plate pixels, and golden-render diffs that catch determinism or font regressions after pipeline changes.
