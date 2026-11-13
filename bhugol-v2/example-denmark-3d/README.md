# Example: "A Desert in Europe?!" Denmark's walking dune (3D, 89 s EN / 83 s HI, 13 Nov 2026), code-drawn, no AI images

- **MW / MC**: two `map3()` instances on the same assets (`denmark-map` fetch: Blue Marble 4-16E 53.5-59.5N + Landsat WELD patch over the Skagen peninsula).
  The terrain shader gains: `flagA` (Danish flag drawn procedurally inside the country mask, `frect` = flag bbox), `forA/forT` (forest cover shrinking by a noise
  threshold, `sepia` old-map look), `sandA/sandKm` (sand drift spreading inland from the Skagerrak coast, `art/sd.png` = km from the NW sea / 10, `art/land.png`),
  `plantA/plantP` (plantations growing over the sand, textured from the Landsat patch), `duneHL` (`art/dunemask.png`, the OSM Råbjerg Mile polygon), a road ribbon
  (OSM route 40, `roadP`) and a 2D rain layer.
- **DU**: the dune in code (1 unit = 10 m): transverse dune height field with a steep slip face (`HFUN`, shift = walking), blowing sand points, instanced pines,
  a 40 m gauge, a to-scale cricket pitch, a main road with a moving car emoji, rain.
- **CH**: Skagen's old church in code (red-brick nave, whitewashed tower with crow-stepped gables), a sand height field whose level rises, a dug pit at the door,
  the nave sinking in 1795. Characters (dune, church tower) are SVG drawn in code; talk = mouth swap on word times.
- Covers: `tools/mkthumb.py <build> <out> <en|hi> <a|b>` injects a cover overlay and snapshots one frame. The user picked `a` (Denmark flag-filled + cactus ringed on
  Skagen) with the title words on it ("A DESERT IN / EUROPE?!", "EUROPE में / रेगिस्तान?!").
- Kit (`kit.json`) was over the 4 MB read cap again: mm3 `align.py` / `words_fit.py` / `voices.py` + `tools/mixbk.py` used.
- Gotchas: a `ShaderMaterial` with `fog: true` but no fog uniforms throws inside the render driver (scene silently stays blank); `countGrow` formats years as
  "1,795": build.py patches motion.js so beats with `to >= 1000` print raw; background renders started with `nohup ... &` were killed when the shell call ended,
  so run them through the tool's own background mode.
