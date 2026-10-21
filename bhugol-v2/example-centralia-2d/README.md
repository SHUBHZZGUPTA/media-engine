# Example: Centralia (2D look + motion pass, 21 Oct 2026)

The 2D build of the Centralia Short with the shared motion library wired in. Same spec, timing, `mkscore.py` and
shot plan as `../example-centralia-3d/` (use that folder's `centralia.json` / `mkscore.py`).
- `template.html` — DOM scenes with image-coordinate cameras, SVG overlays, characters, captions; cuts, karaoke captions,
  count-ups and slams come from `../motion/motion.js` (handle `MO`; `M` is the map data in this template).
- `build.py` — spec + timing -> project; reads the spec's `shots` plan via `../motion/motion_plan.py` and copies `motion.js`.
- Render: `hyperframes render --quality looks` (~13 min EN / ~15 min HI), then `../finish.sh`.
