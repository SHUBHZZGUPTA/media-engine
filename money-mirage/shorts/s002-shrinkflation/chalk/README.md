# s002 chalkboard build (anidoodle test)

Visuals are drawn in code with [anidoodle](https://github.com/alexgreensh/anidoodle) (Apache-2.0), chalkboard hand.
Build: `node <anidoodle>/skills/anidoodle/engine/tools/scaffold.mjs <dir> --film shrink --format 9x16`, copy these three
files into `<dir>/src/canvas-core/`, `npm install`, then `node tools/render.mjs shrink --out out/shrink_silent.mp4`.
Timing: `python3 ../gen_timing.py ../script_marked.md <align words.txt> 1.0 s002timing.ts`.
Audio: `python3 ../mix_chalk.py <narration.wav> s002timing.ts ../../../mm3/library/music/5_rapid.mp3 ../../../mm3/library/sfx 65.0 ../audio/mix.wav`.
