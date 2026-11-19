# Example: "Europe's Weirdest Border?" Märket island (3D, EN 78.6 s / HI 76.8 s, 19-20 Nov 2026), code-drawn, no AI images

GeoGlobeTales remake (Märket, GGT 31M) on BHUGOL v2: own script, narrator only (skit lines turned into narration by Shubham), Gemini 3.8 upbeat Sadaltager.
- **MK / MK2**: the island in code from OpenStreetMap (fetch job `marke-osm`, Overpass): `tools/prep_island.py` -> metre geometry, `tools/prep_raster.py` ->
  `art/isl.png` (R = signed distance to coast, G = Swedish side of the 1809 straight line, B = Swedish side of the 1985 S border). The 1809 line is rebuilt
  from the S border's own coastal endpoints (coast ownership never changed). Rock = displaced plane, sea shader with foam from the SDF, flag crosses painted
  per half in world space, swapped patches pulse gold (areas come out ~3,700 vs ~3,950 m2 = "same area"), border ribbon morphs straight -> S, lighthouse +
  keeper buildings from OSM footprints, rotating beam, clocks, a walker whose own clock flips on every crossing. Two instances so cuts can alternate.
- **MW / MH**: map3 (Blue Marble + DEM, `marke-map`) with Sweden/Finland flag fills from `pa_cov` (R = SE, G = FI, **B = land mask from Natural Earth 10m**:
  BMNG oceans are near-black, so the sea is painted from the mask) and a sepia 1809 mode with Finland in Russian-Empire green.
- Cover = frame 0 = loop seam: cover camera pose + headline + red hand-drawn circle on the lighthouse + both flag emoji; the last 0.42 s eases back in.
- Renders: Kaggle T4 via `gpu/hf3d_render.py` (`window.__seek` added in the template), ~6.5 min per language. **Only one Kaggle job can be pending**:
  pushing a second job cancels the pending one; queue the next language only after the previous one is `in_progress`.
- Retention gate: smooth camera drifts hide beats; split long drifts into hold-then-snap camera moves on the beats (v5 passed: EN 2.2 s cadence, HI 2.1 s).
- Late layout fixes without a GPU re-render: `tools/patch.py` splices locally snapshotted frames (HyperFrames snapshot at f/30) into the GPU master
  (mean abs diff vs the GPU frame ~2.5/255).
- Kit (`kit.json`) over the read cap again: mm3 `align.py` / `words_fit.py`; Hindi aligned with the segmented job (`hindi_align_job.py`).
- Music: "Carefree" (Kevin MacLeod, CC BY 4.0), bed wrapped across the loop seam (`tools/mix.py`).
