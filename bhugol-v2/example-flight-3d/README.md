# Example: World's Longest Flight (3D globe, 12 Nov 2026) — code-drawn, no AI images, 40 s
- One shared WebGL globe (Blue Marble day + Black Marble night, `art/day.jpg`/`night.jpg` from `prep.py`) drawn into each scene's 2D canvas, so two scenes (GA/GB) share textures and still get designed cuts.
- Real day/night: the sun position follows the flight clock (dep 07:27 UTC, 24.4 h); the plane crosses the terminator at the real sunset/sunrise points (`routes.json` sunEvents).
- Routes are tubes on the sphere drawn by progress (uv.x), optional dashes; ✈️ marker rotates to the screen heading. Ocean-lift uniform `oc` for bright thumbnails.
- `--thumb=1` builds the cover as a frame of the video (captions/titles hidden, overlay text + ❌ on the shortcut).
- Lessons: unwrap longitudes in camera tracks across the date line; never put `data-hf-motion-blur` on a full-screen title group (black frames in Hindi); keep the whole-globe views at dist ~7-9 (fov 30, portrait).
- Kit was over the 4 MB read cap again: mm3 `align.py`/`words_fit.py` + `mix.py` (Baikal bed) used instead.
