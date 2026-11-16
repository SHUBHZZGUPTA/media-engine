# bhugol-gta: the GTA 6 vs Miami long-form kit

Engine and worked example behind "GTA 6 Places That Are Real?!" (BHUGOL EN, 17 Nov 2026, youtube.com/watch?v=CE2MXjBVRLE).
The `bhugol-gta` skill is the how-to; this folder is what it runs. Changes are logged in `LEDGER.md`.

- `engine/` copy into `/home/claude/<project>/build/` and run there.
  - `make.py` builds `out/hf/index.html` (+ assets, clip frame sequences), `narration.wav`, `spec.json`, `music.json`, `times.json`.
    Everything above the line `# ================= SAMPLE` is reusable; the shot plan below it is per video (rewrite it).
    Env: `PROJ` (project folder), `GSAP` (gsap.min.js path).
  - `engine.html` GSAP timeline page (`window.__seek`, `window.__ready`), Thar typography, captions, tags, kicks, chapter cards, tracker, subscribe beat.
  - `render_local.mjs` frame-exact CPU render to H.264 (env `PW` playwright index.mjs, `CHROME` headless shell).
  - `serve.py` static server with HTTP Range. `snap.mjs` QC stills. `maps.py` USGS/EOX plate planning + stitching. `fonts/` BSD, Archivo, Fraunces, Inter, Mukta, emoji, BHUGOL badge.
- `example-gta6-vs-miami/` script, kit, credits, music sections, TTS job (full single take), clip cut list (`lib/sel.txt` + `cut.sh`), map plate metadata, thumbnail HTML templates.
- Music used: `outputs/fetch/gta6-music/` (Kevin MacLeod, CC BY 4.0).
