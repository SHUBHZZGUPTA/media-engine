# Example: Same-size country twins (3D, 13 Nov 2026), code-drawn, no AI images

Top-5 "countries that look different but are the same size" Short (Nepal/Bangladesh, Guinea/UK, Chile/Zambia,
Italy/Philippines, Malaysia/Vietnam). Holden (Higgsfield Seed Audio) narration EN + HI; seamless loop back to the opening globe.
- 5 `map3` scenes (one per pair) on NASA GIBS + AWS terrain fetch jobs `twins-sa|wa|zc|it|sea`; per-country masks + baked
  flag fills (`tools/prep.py`, flag-icons SVG via rsvg-convert), white country edges in the terrain shader, a flag-painted globe.
- True-size overlays moved across the map (UK on Guinea, Philippines sitting on Italy), a Zambia -> Chile shape morph,
  a 22 km measure line, rank badges (#1 with rays, crown and confetti), code-drawn country characters (UK sobbing, MY + VN blushing).
- **Size comparisons are filmed top-down (el >= 86)**: at a tilt the near end of a tall shape is magnified, which made the UK look
  twice Guinea's size in the first test.
- **No HyperFrames motion blur**: with motion-blur attributes on the hook letters + rank badges the render ran at ~24 s/frame.
- Chunked render (`tools/render_chunks.sh`, `build.py --from= --to=`): 10 s chunks so a workspace restart loses one chunk only.
- `tools/pad_lines.py`: adds breaths between lines + slows a rushed TTS take (the Holden Hindi take came back at 43.7 s, no pauses).
- Thumbnail: `tools/make.html` + `tools/shot.cjs` (title headline, yellow box on the last word, red circle, emoji) over a clean
  frame from a `--thumb` build (captions/ranks hidden).
