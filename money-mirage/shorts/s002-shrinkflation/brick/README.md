# s002 toy-brick build (anidoodle test)

`brick.ts` draws with anidoodle's `toyBrickKit.ts` (Apache-2.0). Scaffold a 9:16 project, copy `brick.ts` + `s002timing.ts`
into `src/canvas-core/`, and generate `fontdata.ts` (exports INTER900 and MUKTA800 as base64 of `mm3/library/fonts/inter900.woff2`
and `mukta800.woff2`). In `src/hosts/page.ts`, after the image preload in `ready`, add
`await globalThis.__FONTS_READY__;` so frame 0 waits for the fonts. Render: `node tools/render.mjs brick --out out/brick_silent.mp4` (~4.5 min).
Audio: `python3 mix_brick.py <narration.wav> s002timing.ts ../../../mm3/library/music/5_rapid.mp3 ../../../mm3/library/sfx 65.0 ../audio/mix_brick.wav`.
