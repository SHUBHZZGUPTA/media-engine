# HyperFrames 0.8.181: what BHUGOL (and any channel) can reuse

**Read this at the start of every video build (bhugol-shorts-v2 §1), and look things up here before building any effect.**
Researched 22 Oct 2026: every skill file (946) and every registry item (448), plus tests on our own renderer
(Chromium headless_shell 1194, software WebGL / SwiftShader, 2 CPUs, no network at render time).

| File | What's in it |
|---|---|
| `animation_and_library.md` | 48 motion rules, 22 blueprints, 13 examples, ~40 CSS + 14 shader transitions, all 448 registry blocks/components with feasibility, effort, value and best channel; ranked top 15; shader-transition, motion-blur, WebGPU and `hyperframes add` notes |
| `captions_audio_grading_core.md` | 49 items: the 35 caption identities (genre fit, best 4 for geography, best 2 for horror), audio (fx chains, voice carve, `audio`/`beats` CLI), grading (3 LUTs, media-treatment), core (variables, batch renders, sub-compositions), CLI gates |
| `maps_graphics_story.md` | Maps deep-dive (flag-in-borders, flow arcs, pin rollout, callout cards, choropleth, basemap licensing + free alternatives), ~75 other items, 14 story tools for the script stage, ranked top 12 |
| `registry_catalog_0.8.181.json` | Raw registry listing (name, type, tags, description) |

## Tested on our setup (measured, not from the docs)
| Thing | Result |
|---|---|
| `hyperframes add <item>` | Works (fetches from GitHub raw). Items load CDN libs (jsdelivr GSAP/d3/three, Google Fonts): vendor from npm before rendering. |
| WebGPU items (40) | Work only with `--enable-unsafe-webgpu` on a localhost page / `PRODUCER_ALLOW_SOFTWARE_WEBGPU=true`; software, slow. Render their 2 s loops once to video. 13 html-in-canvas / liquid-glass items are blocked. |
| `HyperShader.init` shader transitions | Work, but switch the WHOLE render to the layered screenshot route: ~5 s/frame (an 85 s video = hours). We port the GLSL into `bhugol-v2/motion/shader_xfade.js` instead (only the 0.8 s cut costs anything). |
| Motion blur component (`data-hf-motion-blur`) | Works on DOM elements, not canvases. +9% render time (6 s 3D slice: 238 s -> 259 s). Engine whole-frame motion blur has no CLI flag. |
| v2 motion library ports (shake, hand-drawn, hook kit, card, sweep, burn overlay) | +4% render time (228 s -> 238 s on the same slice). |
| LUT looks | Build offline: `npx hyperframes media-use resolve --type lut --intent "<look>" --project . --local-only`; already saved in `bhugol-v2/grade/`. `grade-compare --for frame.png --luts a,b,c` makes a choice sheet. |
| `hyperframes audio --quality fast --only onsets` | Works locally; drives `bhugol-v2/motion/sfx_check.py`. |
| Bundled SFX (21, Pixabay) | In `node_modules/hyperframes/dist/skills/media-use/audio/assets/sfx/`; commercial use, no credit. |
| `hyperframes check` | Times out on our heavy 3D pages; fine on 2D. `snapshot` works (always `--describe false`). |
| Plain Playwright screenshots | Black (the runtime shows the stage); use `snapshot`. |

## Already built into BHUGOL v2 (see `bhugol-v2/motion/README.md`)
camera-shake profiles, hw-callout-circle / hw-arrow, char-slam + kinetic beats, counting-dynamic-scale, split-flap board,
caption-highlight sweep, maps callout-card + flag-in-borders, motion blur, ridged-burn shader cut, LUT grades, bundled SFX,
`audio`-based sound check, faceless-explainer cut catalog + motion language.

## Best unused next (ranked for retention, any channel)
1. Route arcs with a moving plane/marker (reg:nyc-paris-flight, arc-motion-path) for routes, trade, migrations.
2. Cinemagraph (reg:cinemagraph): one moving region in a still AI image.
3. Bar chart race / slot-machine numbers / chart-story for rankings and money.
4. Phone text / notification threads (vertical already) for scam and horror stories.
5. Pull-back reveal / zoom-out reveal as a 20-30 s re-hook.
6. Before/after wipe for then-vs-now.
7. Horror stack: camcorder HUD + grain + vignette + RGB glitch + VHS transition; bleach-bypass LUT.
8. Caption identities: anchor / scoreboard / chalkboard (geography), vhs / dossier (horror).
9. Lottie characters + stop-motion cadence + speech bubbles + iris-out for cartoons and kids.
10. Story tools: hook-type rotation, a named persuasion move per beat with a callback ending, delete-tests, silent beat before the twist.
