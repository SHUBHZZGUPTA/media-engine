# s002 mixed-media build (anidoodle) — the shipped version

Looks: archival scrapbook (base) + marker comic (objects), with toy-theatre collage, newsprint and toy-brick beats.
`mirageKit.ts` is the reusable kit for every Money Mirage Short in this look; `shrinkMix.ts` is the film, `shrinkThumb.ts` the frame-0 thumbnail.

Build: scaffold a 9:16 anidoodle project, copy these three + `../chalk/s002timing.ts` into `src/canvas-core/`, generate `fontdata.ts`
(INTER900, MUKTA800 as base64 of `mm3/library/fonts/inter900.woff2`, `mukta800.woff2`), put the logo (520 px, from `money-mirage/logo/`)
at the project root as `logo_s.png`, add `src/hosts/page-shrinkMix.ts` / `page-shrinkThumb.ts`, and in `src/hosts/page.ts` add
`await globalThis.__FONTS_READY__;` before `mount(1)` in `ready`. Render: `node tools/render.mjs shrinkMix --out out/shrinkMix_silent.mp4` (~5 min);
thumb: `node tools/still.mjs shrinkThumb --frame 0 --out out/thumb_v.png`.
Audio: `python3 mix_mixed.py <narration.wav> <s002timing.ts> ../../../mm3/library/music/5_rapid.mp3 ../../../mm3/library/sfx 65.0 ../audio/mix.wav`,
then `finish_short.sh` from the Short folder.
