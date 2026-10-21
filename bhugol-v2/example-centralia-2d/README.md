# Example: Centralia (2D look + motion pass, 21 Oct 2026)

The 2D build of the Centralia Short with the shared motion library wired in. Same spec, timing, `mkscore.py` and
shot plan as `../example-centralia-3d/` (use that folder's `centralia.json` / `mkscore.py`).
- `template.html` — DOM scenes with image-coordinate cameras, SVG overlays, characters, captions; cuts, karaoke captions,
  count-ups and slams come from `../motion/motion.js` (handle `MO`; `M` is the map data in this template).
- `build.py` — spec + timing -> project; reads the spec's `shots` plan via `../motion/motion_plan.py` and copies `motion.js`.
- Render: `hyperframes render --quality looks` (~13 min EN / ~15 min HI), then `../finish.sh`.

## v2 (22 Oct 2026): HyperFrames library upgrades
Same beats as the 3D example (use `../example-centralia-3d/centralia.json` as the spec): char-slam hook title, "64 YEARS" growing
count, "POPULATION: 5" flip board, measured camera shake, hand-drawn arrows/circles in each plate's image space (they ride the
camera), US flag clipped into the Pennsylvania border, a stat card pinned to the map pin, caption highlight bars, motion blur on
the hook letters and the 1962 slam. The `burn` cut becomes a warm fire flash in 2D (no WebGL overlay). `mkscore.py` has the
sound-timing fix and the bundled-SFX layer (writes `mix_final.wav`). Grade at finish with `../grade/teal-orange-blockbuster.cube`.

## Whole-video spec (22 Oct 2026)
`centralia.json` now plans 47 beats across all 80 s (was ~22 s), so the full video gets the same circles, arrows, number
trackers, flip boards and card as the preview. The template reads every label, number and position from the beats (no
Centralia text hard-coded). The build stops if any stretch over 5 s has no visual moment (old spec: 5 gaps, worst 14.4 s at
51-66 s; new spec: none).
