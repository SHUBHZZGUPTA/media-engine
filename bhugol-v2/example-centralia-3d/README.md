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
