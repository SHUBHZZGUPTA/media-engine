# BHUGOL motion pass (both 2D and 3D)

Every BHUGOL v2 video goes through this pass. It turns the HyperFrames motion doctrine into code + checks.

| File | What it does |
|---|---|
| `motion.js` | Shared library (`BhugolMotion(tl)`): story-aware cuts (curve / zoom / zoomIn / whip / flash / hard), karaoke captions with keyword pops, count-ups, number slams, hold jitter, text in/out without bounce. Full-bleed safe (no edge strips). |
| `motion_plan.py` | The spec's `shots` + `beats` -> cut times for the composition AND matching SFX for `score.py` (whoosh per cut, impact on zoom landings, riser + hit on hero flashes, thuds on slams, ticks on count-ups). Grammar check. |
| `retention_qa.py` | Gate on the silent render of the WHOLE video (never only a preview slice): no frozen window > 2 s, >= 85% moving, a visual event every <= 2.7 s (longest gap <= 6 s), hook frame moving, no black frames, transition grammar. |
| `shader_xfade.js` (v2, 3D) | Hero `burn` cut: ridged fire burn ported from @hyperframes/shader-transitions (MIT), drawn by our own WebGL overlay so only the 0.8 s cut costs anything (HyperFrames' own `HyperShader.init` switches the whole render to a ~5 s/frame route). |
| `vendor/motion-blur.html` (v2) | HyperFrames registry motion blur (Apache-2.0). Mark only 1-3 snapping elements: `data-hf-motion-blur='{"samplesPerFrame": 8}'`; never an element containing a canvas. Cost measured: ~9% render time. |
| `sfxlayer.py` (v2) | Layers HyperFrames' bundled Pixabay SFX (commercial use, no credit) peak-aligned onto the synth mix: impact on the hook title, whoosh-cinematic + impact on hero cuts. |
| `sfx_check.py` (v2) | Sound QA: every cut and visual beat has a sound-effect onset within 100 ms (uses `hyperframes audio` onsets on an FX-only stem). |
| `motion_plan.unwarp()` (v2) | **Bug fix (22 Oct):** score.py re-maps times through its own chunk warp; mkscore must call `unwarp(S, TIM)` last, or mid-line effects land up to ~1 s off (Centralia had 11 of 18 timed sounds >100 ms off). |
| `../grade/*.cube` (v2) | HyperFrames' 3 LUT looks built offline: teal-orange-blockbuster (BHUGOL default, 80% blend), bleach-bypass (horror/war), film-fade (history). Applied at finish with ffmpeg `lut3d` + `blend`. |

Spec fields:
```json
"shots": [{"scene": "R1", "at": [0, 0, 0]}, {"scene": "MP", "at": [1, 0, -0.15], "cut": "whip"}, ...],
"beats": [{"kind": "slam", "at": [1, 0, 0]}, {"kind": "count", "at": [5, 2, 0]}]
```
`at` = [line, chunk, offset s]: cut on the caption chunk where the new idea starts, 0.15 s early.

Cut grammar: `curve` = primary (~60-70% of cuts); accents: `zoom` (new chapter / dive in), `zoomIn` (arrival, payoff,
"today"), `whip` (time jump, "rewind", "meanwhile"); `flash` = hero, at most 2 per video (payoff and/or twist); `hard` for
rapid-fire lists. Template wiring: scenes are `.scene` full-frame elements; `MO.shots(D.shots.map(s => ({el, at: s.t, cut: s.cut})))`;
in 3D also draw each plate from `at - 0.45` to `next_at + 0.1` so overlaps never show a blank canvas.

## v2 library ports (HyperFrames registry items, all seek-safe property-setter drivers)
| Call | From | Use |
|---|---|---|
| `MO.shake(at, dur, profile, k, {decay})` + `MO.shakeOn(wrap, dur)` | reg:camera-shake (measured lens profiles) | `rig-6d-wobble` k~0.75 for impacts; `handheld-normal-mild` k~0.1-0.12, decay:false for live-action plates. Wrap only the scenes (`#cshake`), never captions. |
| `MO.hwCircle` / `MO.hwArrow` | reg:hw-callout-circle / hw-arrow | A red marker loop or arrow on the exact thing the voice names; position is a function of time (3D: project world point each frame). Beats `circle` / `arrow` with `scene`, `at`, `until`. |
| `MO.charSlam` | reg:char-slam-explode + rules/kinetic-beat-slam | Hook title: each word lands on its own beat, letters fly in from a scatter. Beat `charslam`. |
| `MO.countGrow` | rules/counting-dynamic-scale | Number grows while counting, unit lands after. Beat `grow` (+ `to`). |
| `MO.flap` | reg:split-flap-board | Solari flip for short stats / place names. Beat `flap`. |
| `MO.sweep` | reg:caption-highlight | TikTok bar behind keywords (no outline on the bar). |
| map card + flag fill | motion-graphics maps (callout-card, flag-in-borders) | 3D: flag texture inside the region mask on the terrain shader; DOM card pinned to the projected pin with a connector. Beat `card`. |
| `burn` cut | @hyperframes/shader-transitions ridged-burn | 3D via `shader_xfade.js`; in 2D it falls back to a warm flash. Counts as a hero cut (flash + burn <= 2). |

## Planning the whole video (22 Oct 2026 fix)
Lesson from Centralia: the 25 s preview had every upgrade, the full video did not, because the spec only planned beats for the
first ~22 s and the template had Centralia text hard-coded. Now:
- **Plan beats for the entire script, whatever its length.** Every beat is data in the spec; the templates hold no per-video text.
- **Pre-render plan check** (`motion_plan.gaps`, run by `build.py` / `build3d.py` before writing `index.html`): every cut, beat
  and title time is a "visual moment"; any stretch longer than 5 s without one stops the build and prints `PLAN GAP a-b`.
  Fix the spec (add a circle / arrow / grow / flap / card / moment on the line the voice is on). `--allow-gaps` exists only for a
  deliberate hold, and the reason must be told to the user. With `PREVIEW` set, it checks up to the preview end; otherwise to the end card.
- **retention_qa.py on the full silent render** before finishing; a preview pass does not count.

Beat fields (positions are plate-image pixels; `at`/`until` are `[line, chunk, offset s]`; `until` is optional and defaults to
the next caption chunk that starts at least 0.5 s after the beat):
| kind | fields |
|---|---|
| `slam`, `count`, `punch`, `impact` | `at` (impact = sound only) |
| `charslam` | `at` (hook title) |
| `circle` | `scene`, `at`, `until`, `c` [x,y], `r` [rx,ry], 2D overrides `c2d` / `r2d`, `col` |
| `arrow` | `scene`, `at`, `until`, `from` [x,y], `to` [x,y], 2D overrides `from2d` / `to2d`, `col` |
| `grow` | `at`, `until`, `to`, `unit`, `prefix`, `from`, `y` (box top px, default 150) |
| `flap` | `at`, `until`, `text`, `y` |
| `card` | `scene` (map), `at`, `until`, `flag`, `name`, `to`, `unit`, `tag` |
| `moment` | `at`, `what` — a hand-made animation already in the template (emoji pop, thermometer, bars, character); counts for the plan check |
