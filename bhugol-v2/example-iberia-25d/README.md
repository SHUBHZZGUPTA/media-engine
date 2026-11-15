# Example: "Spain + Portugal... again?" Iberia what-if Short (2.5D one-camera, 16 Nov 2026) — the BHUGOL Shorts v3 reference

Same craft as `example-nordic-25d` (one orthographic satellite map, one continuous camera with ease-out glides + CSS
perspective tilt, a literal visual for every line, vote ending, seamless loop, cover on frame 0 only), plus the v3 fixes:

- Featured countries use geoBoundaries gbOpen ADM0 borders (`iberia-borders.json` fetch job), simplified at 0.6 world px,
  Chaikin x2; union simplified 0.8 px. Natural Earth 10m only for neighbours. Natural Earth borders looked boxy in close-ups.
- Flags baked to PNG layers at 1:1 world px (`bake_flags.cjs`), not live SVG clip-paths (fast render) and not half-res.
- SFX: no pop/click/tick sounds (Shubham, 16 Nov 2026); whoosh per camera key, impacts on slam/stamp/thud/boom/flash.
- Render with `HF_CAPTURE_PARALLEL_STREAM=true` (2 workers, streams frames, no ~3.7 GB disk spool). 59 s EN took ~10 min.

Files: `mkscript.py` (EN+HI script + both Gemini 3.8 TTS jobs), `prep.py <tiles> <tiles> assets` (plates + map.json),
`bake_flags.cjs`, `template_base.html` + `scenes.js` -> `template.html`, `build.py <out> [hi]`, `evs.cjs <build>` (visual
beats for the sound plan), `retime.py` (GLOBAL_SIL=1 for Hindi), `mix.py <build> <audio>`, then a -14 LUFS static master,
`cover_ov.html` -> `shot_ov.cjs` -> `cover_ov.png`, `finish2.sh silent.mp4 master.wav out.mp4 <dur>`.
