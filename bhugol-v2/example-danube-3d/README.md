# Danube: "This River Has 4 Capitals?!" (3D, library-only, Nov 2026)
Three terrain-map instances (two wide Europe views MW/MV + a close view MI) and a karst cutaway block.
New in this build:
- `map3(cfg)` is parametric (several bboxes per video; asset prefix `w_` / `i_`).
- `mapRiver()` glowing river ribbons drawn along Natural Earth polylines (`prog` draws them, width follows camera distance).
- Up to 4 sharp Landsat WELD patches per map (`cfg.patches`), colour-matched to the Blue Marble plate (`prep_hd.py`). Lesson (user, 9 Nov): any close-up outside a sharp patch looks blurry/blocky; keep close-ups inside the patches and fetch patches for every place the camera visits.
- Flag overlays (`f1/f2/f3`, RGBA, lakes cut out) laid on each country's land, with border glow. Lesson (user, 9 Nov): whenever two neighbouring countries/states/cities are shown, demarcate the land and lay each country's flag on it. `f3` = flags drawn rotated for east-up (yaw -90) camera shots.
- Wide portrait shots of a west-east river use yaw -90 (east up) so the whole river fits.
