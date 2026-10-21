# BHUGOL motion pass (both 2D and 3D)

Every BHUGOL v2 video goes through this pass. It turns the HyperFrames motion doctrine into code + checks.

| File | What it does |
|---|---|
| `motion.js` | Shared library (`BhugolMotion(tl)`): story-aware cuts (curve / zoom / zoomIn / whip / flash / hard), karaoke captions with keyword pops, count-ups, number slams, hold jitter, text in/out without bounce. Full-bleed safe (no edge strips). |
| `motion_plan.py` | The spec's `shots` + `beats` -> cut times for the composition AND matching SFX for `score.py` (whoosh per cut, impact on zoom landings, riser + hit on hero flashes, thuds on slams, ticks on count-ups). Grammar check. |
| `retention_qa.py` | Gate on the silent render: no frozen window > 2 s, >= 85% moving, a visual event every <= 2.7 s (longest gap <= 6 s), hook frame moving, no black frames, transition grammar. |

Spec fields:
```json
"shots": [{"scene": "R1", "at": [0, 0, 0]}, {"scene": "MP", "at": [1, 0, -0.15], "cut": "whip"}, ...],
"beats": [{"kind": "slam", "at": [1, 0, 0]}, {"kind": "count", "at": [5, 2, 0]}]
```
`at` = [line, chunk, offset s]: cut on the caption chunk where the new idea starts, 0.15 s early.

Cut grammar: `curve` = primary (~60-70% of cuts); accents: `zoom` (new chapter / dive in), `zoomIn` (arrival, payoff,
"today"), `whip` (time jump, "rewind", "meanwhile"); `flash` = hero, at most 2 per video (payoff and/or twist); `hard` for
rapid-fire lists. Template wiring: scenes are `.scene` full-frame elements; `MO.shots(D.shots.map(s => ({el, at: s.t, cut: s.cut})))`;
in 3D also draw each plate from `at - 0.45` to `next_at + 0.1` so overlaps never show a blank canvas.
