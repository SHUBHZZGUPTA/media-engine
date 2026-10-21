# Example: Centralia (3D look, 21 Oct 2026)

The first BHUGOL v2 video in the 3D look. Copy and adapt per topic.

- `template3d.html` — the composition. Reusable engine at the top (keyframe `Track`/`key`/`valAt`, `plate3` depth-mesh scenes,
  `map3` globe -> terrain flyover, `particles` (steam/smoke/embers), `glow`, `label`, camera-attached 3D props, characters,
  captions, titles, badge + end card, one render driver that reads time only). Per-video parts: the "build scenes" block and
  the per-shot blocks inside `build()`.
- `build3d.py` — spec + timing -> HyperFrames project (expects `art/` next to it with the 3D assets; copies gsap + three r149).
- `centralia.json` / `centralia.hi.json` — script, caption chunks, voices, pacing (English + Hindi).
- `mkscore.py` — music sections and sound effects in real seconds, then the kit's `score.py`.
- Assets came from: `3d/map3d_prep.py` (map), the `depth` workflow + `3d/prep3d.py` (2x plates + depth maps),
  Codex dioramas (cold, then a hot EDIT of it) + `3d/burnmap.py` (fire spread), thumbnails from `3d/thumb_a.py`.
- Render: `hyperframes render --crf 14 --no-browser-gpu` (EN 85 s took 38 min, HI 100 s took 49 min), then `3d/finish_hq.sh`.

## v2 (22 Oct 2026): HyperFrames library upgrades
The template now wires the v2 motion library (see `../motion/README.md`): fire-burn hero cut (map -> pit), char-slam hook title,
"64 YEARS" growing count, "POPULATION: 5" flip board, measured camera shake, hand-drawn arrows/circles, US flag inside the
Pennsylvania border, a pinned stat card, caption highlight bars, motion blur on the hook letters and the 1962 slam.
`mkscore.py` now calls `motion_plan.unwarp` (sound-timing fix) and layers bundled SFX (writes `mix_final.wav`); finish with the
teal-orange LUT: `ffmpeg -i silent.mp4 -i mix_final.wav -filter_complex "[0:v]split[a][b];[b]lut3d=file=../grade/teal-orange-blockbuster.cube[g];[a][g]blend=all_mode=normal:all_opacity=0.8,format=yuv420p[v]" ...`.
`flag_us.png` is drawn from the public-domain design; for other countries rasterise the MIT `flag-icons` npm SVGs.
Checks on the first 25 s: retention_qa PASS (an event every 2.2 s), sfx_check 17/17.
