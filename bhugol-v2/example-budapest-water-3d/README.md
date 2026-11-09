# Example: "What's Hiding Under Budapest?" (3D, library-art-only, 9 Nov 2026)

First BHUGOL v2 Short built with **no generated art at all**: every picture is real data or engine-drawn.
- Two `map3()` terrain instances (MP, MQ: NASA GIBS Blue Marble + Landsat WELD, AWS Terrarium terrain), with `mapDot` glow pins
  (depthTest off, size scales with camera distance) and pin ring/beam hidden when the camera is close (they read as a "hook" shape).
- `block3()`: a cutaway block of the real Buda Hills. Top = one CPU-built mesh from a z12 Terrarium DEM + Landsat; the four
  walls are built from the same CPU heights (so top and walls always meet). The front wall's shader draws the section: strata,
  heat with depth, the fault, rain/hot-water flow paths (`rainP`, `hotP`), caves dissolving from below (`caveP`), flooding (`waterA`),
  the growing edge (`growA`) and the payoff reservoir glow (`resA`, `glowCity`).
- Assets: `map3d_prep.py job` + extra `hdem_12_*` tiles and a `buda_weld.jpg` crop in the same fetch job; block DEM/hillshade/texture
  and wall profiles made by the snippet in this chat (see `block.json`).
- Thumbnail: Hungary flag-filled on the regional satellite (PIL, from `ne.jpg` + `pa_mask.png`), red circle + pin on Budapest,
  zoom bubble of the cutaway, headline box = title. The user rejected thumbnails without the country's flag on the map.

## Bugs hit (fixed)
- Wall vertices were destructured as [x, z, y] instead of [x, y, z]: the walls folded into "panels" and the top looked like a ribbon.
- `noise.png` from prep3d is not tileable; with RepeatWrapping it draws rectangular seams. Use the FFT tileable noise.
- In this workspace the headless shell is `/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell`
  (not 1194), and the gates need `playwright-core` linked into /home/claude/work/node_modules (from /opt/node-tools).
- Continuous `stream` SFX above ~0.15 masks cut pops (sfx_check misses); keep water beds at 0.10-0.12.
- Hindi read "बहुत... बहुत... धीरे" with no pauses: insert them with the kit's `pause.py` before the CTA too.
