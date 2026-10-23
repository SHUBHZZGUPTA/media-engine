# Money Mirage v3 engine (mm3)

3D depth-plate documentary engine for Money Mirage long-form + vertical Shorts (HyperFrames 0.8.181, three 0.149, gsap 3.15).
Every tool runs **from the episode folder** (`money-mirage/episodes/epNN`), which holds:

| file | what |
|---|---|
| `episode.json` | slug, title, plate source dir, depth job names, TTS parts + speakers, character voices, music tracks per chapter, Shorts definitions |
| `script_marked.md` | `# CHAPTER` headings; lines `N:` / `GOLDIE:` / `BILL:`; `*keywords*` get the red caption sweep; `[tag]` = character delivery |
| `shots.py` | the shot plan (plates, looks, cameras, cuts) + beats (numbers, circles, moments, CTAs) anchored to caption chunks/words |
| `art/` | baked looks (`art/baked/<plate>__<look>.jpg`) and episode-only plates |

## Pipeline (T = ../../mm3/tools)
1. `python3 $T/make_spec.py` → `spec.json` + `tts_job.json` (copy to `jobs/tts/`, push, wait for the workflow)
2. Join parts → align job (Whisper) → `python3 $T/words_fit.py spec.json words.txt audio/words_fit.txt` → `python3 $T/align.py spec.json vo.wav audio/words_fit.txt audio` → `python3 $T/voices.py spec.json audio` → `python3 $T/level.py`
3. `python3 shots.py && python3 $T/build.py` (plan check must pass: no 5 s without a visual event) — `--fake` builds on estimated timing before the voice exists
4. QA snapshots: `bash $T/snapseg.sh <seg> <t1,t2,...> review/sN` (times from `python3 $T/checkframes.py`)
5. `bash $T/render_all.sh` (resumable, 60 s segments) → `python3 $T/mix.py` → `python3 $T/mix.py --fx-only && python3 $T/sfxcheck.py` → `bash $T/finalize.sh`
6. Retention gate: `python3 ../../../bhugol-v2/motion/retention_qa.py renders/video_silent.mp4 --end <end_start>`
7. Shorts: `python3 $T/make_shorts.py --tts-job` → voice + align → `python3 $T/make_shorts.py --split hooks_ctas.wav words.txt` → `python3 $T/make_shorts.py` → `bash $T/snapshort.sh <ids>` → `bash $T/render_shorts.sh`

Library: `library/fonts` (Inter 800/900, Noto Color Emoji), `library/sfx` (HyperFrames bundled set + CC0 Openverse story sounds), `library/music` (YouTube Audio Library tracks chosen by Shubham), `library/img` (logo, Lydian coin cutout).
