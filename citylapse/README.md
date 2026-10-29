# citylapse — "Cities Through Time" (BHUGOL long-form series)

Diorama-style 3D "watch a city grow" timelapses (three.js + HyperFrames-compatible page), with the signature
day↔night sweep (day→night right-to-left, night→day left-to-right, 3.5 s, windows switch on/off behind the line)
and the countdown bar. No narration; event cards carry the story.

## Pipeline (per city)
1. `cities/<city>.json` — bbox, origin, era zones (approximate building birth years), reclaimed land, dug canals,
   hero landmarks (exact heights/years), labels, coast line beyond the data.
2. Fetch data with `jobs/fetch/*.json` (OSM via Overpass, split into small tiles; AWS Terrarium terrain).
3. `python3 tools/prep_city.py cities/<city>.json <fetch dirs...> <data_dir>` → land.png, roads.png, bld.bin, scene.json
4. `python3 tools/build_page.py <plan.json> <data_dir> <proj_dir>` → index.html + assets
5. Render: `node tools/render_frames.js <proj_dir> <frames_dir> 30 <t0> <t1>` (resumable), then ffmpeg.

## Night-flip standard (starting point; tune with retention data after 2-3 videos)
Sweep 3.5 s; night 8-12 s; countdown always on; night 1 at 0:45-1:15, night 2 ~3:00, night 3 ~6:00,
extra every ~2.5-3 min only for videos over 10 min; final night in the last 30-45 s (lit city → dawn → opening shot).
Each slot snaps to the nearest real light event within ±30 s, else an honest "city size at night".

Engine deps: `cd engine && npm ci` (three 0.149, gsap, hyperframes, @fontsource/oswald).
