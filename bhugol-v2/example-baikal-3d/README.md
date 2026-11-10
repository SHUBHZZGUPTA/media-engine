# Example: Lake Baikal (3D, 11 Nov 2026) — code-drawn, no AI images

Built when Codex was unavailable and the BHUGOL kit (kit.json, 6 MB) could not be read in the session (4 MB artifact-read cap).
Everything visual is drawn in code:
- **Two map3 scenes in one video** (`map3(prefix, map3d.json, opts)`): Baikal + Great Lakes, globe dive, lake masks with per-lake index
  (`lit` lights lakes one by one), ice-sheet retreat shader (`ice`, `iceA`), true-size overlays laid on the terrain (`overlay(ring, flagTex|col)`:
  Belgium on Baikal, Baikal beside the Great Lakes) with a bounce drop.
- **Wide fetch bboxes** (`baikal-map2`, `greatlakes-map2`): portrait frames must never show the map edge.
- **XS: 3D clay cross-section** built from extruded profiles: true vertical km (water 1.642, mud to 8.64, rift floor 9.3), floating
  Lake Superior block (0.406), Eiffel Tower stack, Everest outline, rift-opening animation (`open`), bubbles.
- **Characters drawn in code**: the real Natural Earth outline (Lake Superior, Belgium) + SVG face; talk = mouth swap on each word time,
  blink, bounce entrance, jolt beats.
- Beats can be word-timed (`word`), language-filtered (`lang`), and `slam` with `what: pop|jolt|mudlit` for real on-screen events.
- `tools/mixbk.py`: voice + synthesized light bed + SFX from `motion_plan.sfx` (real seconds; no kit score.py). `tools/sfxcheck_bk.py`:
  sound-on-beat check against the build's own `times.json`.
Punch-ins kept to the hook (3) + 4 story beats (user rule, 8 Nov).
