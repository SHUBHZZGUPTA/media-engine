# Example: Bengaluru's lakes (3D, 22 Oct 2026)

Second 3D reference build. Use it instead of Centralia when a video needs any of these (all spec-driven):
- **one scene in several shots** (LK opens, pays off and loops; CT and CS return later): `S.wins` + `live(S)`, first shot forced visible
- **map labels and arrows by lon/lat** (`mapLabel`, `mapProj`; arrow beats on `MP` take `[lon, lat]` ends), flag texture from `flag_in.png`
- **circle beats with their own label** (`text`, drawn inside the circle by default; `tdx`/`tdy`/`fs`/`tcol` optional)
- **before -> after water / city reveals** without fire flicker (`tex2` + `burn` spread map; `flick: 1` only for fire)
- characters on a reused scene (Drop on the cascade, Bus at the terminal)

Files: `template3d.html`, `build3d.py` (runs shader lint, plan + sharp-beat checks and the pre-render gates), `mkscore.py`
(soft pen-swish marks, quiet on-beat clicks, ambience beds kept low so clicks read), `bengaluru.json` / `bengaluru-hi.json`
(full 90 s spec, 55 beats, both languages), `plan.py` (writes shots + beats into the spec), `mkspec.py` / `mkhi.py` (lines + chunks).

## What went wrong on this video (and the fix now in the pipeline)
| Problem | Cause | Now prevented by |
|---|---|---|
| 3 scenes black in the delivered video | `//` comment inside a one-line GLSL string | `qa/shader_lint.py` (build) + `qa/scene_gate.mjs` (pre-render) + retention_qa `plate missing` |
| Circles drawn off screen, labels under the top fade / in captions | 3D projection only checked by eye on a few snapshots | `qa/layout_gate.mjs` samples every 0.25 s |
| Patched slices glitched (badge vanished, counter reset) | renderer ignores a time-shifted timeline | rule: no post-render patching, fix + full re-render |
| City reveal flickered | fire flicker baked into every reveal | `flick` is opt-in per plate |
| Harsh slide-whistle on every arrow/circle | `motion_plan.sfx` default | soft pen-swish + quiet click |
| Curve-cut shots at 35% opacity | `motion.js` set/fade order | fixed in `motion.js` |
| Depth job never ran (~45 min lost) | GitHub keeps one pending run per group | `depth.yml` also runs recent jobs with no outputs |
| Hindi lake names lost | Whisper on one long Hindi take | `hindi_align_job.py` (segmented, default) |
