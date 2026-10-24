---
name: "bhugol-shorts-v2"
description: "Make a BHUGOL world-geography Short end to end with the free v2 pipeline (trend check + yt-viral topic, story script, Gemini voices, Codex skit art, HyperFrames), in English plus Hindi, with data-backed thumbnails and YouTube kits. Use instead of bhugol-shorts when the user asks for v2 or the free pipeline."
---

# BHUGOL Shorts v2 (free pipeline)

One BHUGOL world-geography Short, English + Hindi on the same visuals. Costs nothing beyond the user's Claude,
ChatGPT and Google subscriptions. The original `bhugol-shorts` skill stays unchanged; this is a separate skill.
One video per chat (it keeps Claude usage low); if this chat already holds a finished video, suggest a new chat.

**Visual style is the user's choice every video (asked at the approval stop, §5):**

| | 2D | 3D (recommended when there's no rush) |
|---|---|---|
| Look | flat illustrated maps + painterly plates with camera moves (`example-centralia-2d/`) | 3D satellite-terrain flyovers, depth-mapped scenes the camera moves through with live steam/smoke/embers, 3D dioramas and props, 2x-upscaled art (`example-centralia-3d/`) |
| Render, both languages (85 s EN + 100 s HI) | ~32 min | ~100 min |
| Extra prep | none | ~15 min (depth + 2x job, map fetch, dioramas; mostly in parallel) |
| Finish | `finish.sh`, two-pass, < 30 MiB | `3d/finish_hq.sh`, CRF 17, ~120-140 MB |
| Total extra wait vs 2D | — | about +75-90 min |
| Thumbnail | 2D flag-filled vector map (`thumbnail_template.html`) | recipe A on the 3D terrain (`3d/thumb_a.py`) |

(Measured on Centralia, 21-22 Oct 2026. The v2 motion upgrades add ~14%, measured on 3D: a 6 s slice took 228 s before,
238 s with them, 259 s with motion blur too; the 2D figure assumes the same ~14%. Recommend 2D for trend topics with a tight posting window.) The thumbnail always
matches the chosen style.

**Both styles always get the motion and retention pass** (§9a): story-aware cuts, sound locked to every cut, karaoke
captions with keyword highlight bars, count-ups, slams, hook punch-ins, plus the v2 HyperFrames library ports (hook kit,
hand-drawn marks, measured camera shake, map card + flag in the border, motion blur, fire-burn hero cut in 3D, teal-orange
grade, bundled SFX) and two QA gates on the render (retention + sound-on-beat). Library: `bhugol-v2/motion/`.

**Quality rule (22 Oct 2026, Bengaluru):** nothing renders until the pre-render gates pass, nothing is delivered until the QA has run on the *exact file being delivered* and every audit sheet has been looked at, and any fix after a render is a full re-render (never a patched slice). See §9b and §10.

The run stops for the user **twice**: the topic pick (2), and the approval stop (5). It then runs to delivery, except
that thumbnails are shown to the user before they are burned into the videos (11).

Task list:
1. Setup
2. Topic (trend check + proven formats)
3. Package
4. Script, hooks, Hindi, shot plan
5. Approval stop
6. Voices
7. Timings + sound
8. Art (library first; 3D assets if 3D)
9. Build + motion pass + check
10. Render both + retention QA
11. Thumbnails
12. YouTube kits
13. Deliver

## 1. Setup (every new chat)
1. **Repo.**
   - Call `add_repo` with owner `SHUBHZZGUPTA`, repo `media-engine`, access `push`.
   - Clone it to `/home/claude/media-engine`.
   - It holds everything the run needs:
     - `tools/`: Gemini TTS, Whisper, fetch, yt-dlp collector, `depth_upscale.py`
     - `.github/workflows/`: the GitHub Actions mailbox jobs (incl. `depth.yml`)
     - `bhugol-v2/`: `build.py`, `template.html`, `finish.sh`, `thumbnail_template.html`, `thumb_shot.mjs`, `thumbnail_rules.md`, `voice.md`, `example-budapest/` (legacy 2D)
     - `bhugol-v2/motion/`: `motion.js` (v2), `motion_plan.py` (plan, sfx, `unwarp`), `retention_qa.py`, `shader_xfade.js` (3D hero cut), `vendor/motion-blur.html`, `sfxlayer.py`, `sfx_check.py`, README (the motion and retention pass)
     - `bhugol-v2/grade/`: `teal-orange-blockbuster.cube` (BHUGOL default), `bleach-bypass.cube`, `film-fade.cube`
     - `bhugol-v2/3d/`: `map3d_prep.py`, `prep3d.py`, `burnmap.py`, `thumb3d.html`, `thumb_a.py`, `finish_hq.sh`
     - `bhugol-v2/example-centralia-2d/` and `example-centralia-3d/`: the reference builds with the motion pass wired in (`template*.html`, `build*.py`; the 3D folder also holds the full-length spec, 47 beats over 80 s, and `mkscore.py`)
     - `bhugol-v2/example-bengaluru-3d/`: second 3D reference (one scene in several shots, lon/lat map labels + arrows, labelled circles, water/city reveals without fire flicker, full EN + HI spec); its README lists every mistake of that run and the guard that now prevents it
     - `bhugol-v2/qa/`: `shader_lint.py`, `scene_gate.mjs`, `layout_gate.mjs`, `gates.sh` (pre-render) and `audit_sheets.py` (pre-delivery)
     - `bhugol-v2/hindi_align_job.py`: segmented Hindi Whisper job (the default)
     - `bhugol-v2/research/hyperframes/`: the HyperFrames 0.8.181 research (all 448 library items, what works on our renderer, measured costs, ranked next steps)
     - `library/`: characters, scenes, `index.json`
   - Commit as media-engine-bot (`git -c user.name="media-engine-bot" -c user.email="media-engine-bot@users.noreply.github.com" commit ...`).
2. **Kit.** `Artifact` read `https://claude.ai/artifact/QL2xuVyTsyzJ49Lw7Pqggi` path `kit.json`. Unpack it into `/home/claude/bhugol-kit` exactly as in bhugol-shorts §1, then run `./setup.sh`. The kit's tools are reused: `align.py`, `voices.py`, `score.py`, `pause.py`, `words_fit.py`, `transcribe.py`, `attention.py`, `hindi_spec.py`.
3. **HyperFrames + GSAP (+ three.js for 3D).**
   - Install in a work folder with `npm i hyperframes@0.8.181 gsap@3 three@0.149.0 playwright-core` (three r149 still ships `build/three.min.js`; playwright-core drives the pre-render gates in `bhugol-v2/qa/`).
   - Always export these environment variables:
     ```
     HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_NO_UPDATE_CHECK=1 HYPERFRAMES_SKIP_SKILLS=1
     HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
     ```
   - `build.py` / `build3d.py` copy `gsap.min.js`, `three.min.js`, `motion/motion.js` (+ `shader_xfade.js` in 3D), inline `motion/vendor/motion-blur.html` at `__MBLUR__`, and copy the region flag PNG; fix the node_modules paths for the new work folder.
   - Bundled HyperFrames SFX live in `node_modules/hyperframes/dist/skills/media-use/audio/assets/sfx/` (Pixabay licence, commercial use, no credit); `sfxlayer.py` reads them from there (env `SFX_DIR`).
4. **Read** `bhugol-v2/voice.md`, `bhugol-v2/thumbnail_rules.md`, `bhugol-v2/motion/README.md` and `bhugol-v2/research/hyperframes/README.md` before writing anything. Whenever a scene needs an effect, transition, caption look, map move, sound or check that isn't built yet, look it up in `research/hyperframes/` first (feasibility, cost, licence) instead of inventing it.
5. **Codex login is the user's call each video.** Ask at the approval stop: "Codex for new art: log in here now (device code on your phone), or reuse library art only?" Never automate or store the Codex login without the user's explicit go-ahead.
   - Login: `codex login --device-auth` in the background; send the user the link and code. Codes expire after 15 minutes; if one lapses, offer a fresh one.
   - Always run `codex exec ... < /dev/null` (otherwise it waits on stdin), and put `-i <image>` AFTER the prompt.

**GitHub mailbox pattern.** The GitHub Actions API is blocked from this workspace. To run a job:
1. Commit a job JSON under `jobs/<kind>/` and push it. That push triggers the workflow.
2. The workflow commits its outputs back with `[skip ci]`.
3. Poll with `git pull` until the output appears (`until ...; do sleep 10; done` with `run_in_background`).

Job kinds:
- `jobs/tts/` → `outputs/tts/` (Gemini; key in the `GEMINI_API_KEY` secret, never printed)
- `jobs/align/` → `outputs/align/` (Whisper word timings; the job JSON needs an `"id"`)
- `jobs/fetch/` → `outputs/fetch/` (public files from hosts this workspace can't reach, e.g. NASA GIBS, AWS terrain tiles)
- `jobs/viral/` → `outputs/viral/` (public channel listings, optionally thumbnails)
- `jobs/depth/` → `outputs/depth/` (3D only: Depth-Anything-V2 depth maps + Real-ESRGAN 2x upscales of repo images, CPU; ~85 s per 1024x1536 upscale)

If a push is rejected, `git pull --rebase` and push again. If a job's first run failed and a fixed re-push produces nothing, bump a field (e.g. `"try": 2`) and push again.

**Queue rule:** GitHub keeps only ONE pending run per workflow; other sessions pushing jobs of the same kind can silently replace yours. `depth.yml` now also runs any depth job from the last 12 h that has no outputs, but still: after pushing, confirm the run started (outputs or a new commit within ~3 min of the previous run ending); if another session's job is running, expect yours to start after it, and if 10 min pass after that run finished with nothing, bump `"try"` and push again.

## 2. Topic (stop 1)
1. Find past topics with `Artifact` list (BHUGOL video pages). Never repeat one.
2. **Trend check (first, unless the user asked for evergreen only).**
   - Run several WebSearch queries in one turn (`mode: "extended"`) for news from the last 7 days in categories BHUGOL can map: space and launches, vehicle and tech reveals, natural events (eclipses, quakes, storms, volcanoes), sports venues and events, record journeys, new records about places, notable anniversaries.
   - Keep only trends with a **real map angle** (a place, route, border, orbit, distance). Drop wars, live disputes, tragedies and anything communal or religious.
   - Every trend fact gets a dated source. The script avoids claims that could be outdated by posting day.
3. Push a `jobs/viral/` job for the channels (`per_channel` 80):
   - `@Glore3`, `@geoglobetales`, `@worldjike`, `@geofactguy1`, `@RealLifeLore`, `@GeographyNow`
   - `channel/UCMaiQM2iWS97VZp7RjG8_nA`, `channel/UCfP7cEpQZ74cd26yuP4bCYg`, `channel/UC2Cl2g2xFTZoAEldxYVzQFg`, `channel/UCjJY5RvdQW9aEMGSfAbVrfA`
   - Plus any channels the user adds.
4. Rank with yt-viral's `swipe.py --min 2.0` (multiple over each channel's own median).
5. Drop unsafe topics: war-as-spectacle, live disputes, Partition, communal or religious topics.
6. **Merge into one table of 6 ideas** (about 3 trend-riders + 3 evergreen).
   - Columns: idea · 🔥 trend heat (how recent and big the news is; "—" for evergreen) · 🗺️ geography fit · ✅ proven pattern (which outlier pattern it matches, with its multiple) · ⏰ timing ("post within ~3 days" for trends, "evergreen" otherwise).
   - Name the ONE pattern the yt-viral outliers share. (yt-viral's formula labels judge the title only; say so.)
7. Recommend 3 and let the user pick. Write our own story; never copy a source video's script.

## 3. Package first (yt-package)
1. Write 10 titles and lint them with `title.py`:
   - under 60 characters (subject inside the 40-character mobile cut)
   - a number, name or date
   - at most 2 words in capitals
   - the top outliers' style (an impossible claim + a number + an emoji) is a good default
2. Thumbnail text: ≤3 words that **don't repeat the title**. Lint the pairing with `title.py --title ... --thumb ...`.
3. Write the thumbnail brief: framing, the 3 words, and what keeps contrast at feed size.

## 4. Script, hooks, Hindi, shot plan
**Research and fact-check every claim first.** Keep source links. Frame anecdotes as "the story goes". Hedge estimates.

**Hooks (yt-script).**
- Write 5 hooks against `hooks.json` and score them with `hookscore.py`. Keep the top 2 and show their scores.
- Shorts timing: a visual surprise in 2 s, the question by about 5-8 s, around 9-24 words.
- Reject any hook that overstates. A high score never justifies an untrue line.

**Story, not a list (the main v2 fix).**
- Write a one-sentence logline.
- Build a **but / so** chain: every line causes the next. Cut lines that only add "and also".
- Re-ask the question at about 20-25 s ("So how…?").
- Payoff at 70-80%, stated as one quotable line.
- **Twist ending**, often a deadpan character line.
- A joke every 10-15 s.
- 1-3 characters with lines of 8 words or fewer.
- ~170-200 words → about 75-85 s.
- Follow `voice.md`: tone, signature moves, scale anchors, the banned words.

**Loop point (yt-shorts).** The last content line should set up the first, so a replay feels seamless (e.g. the twist sends the viewer back to the hook's question).

**Openers (yt-shorts).** On-screen text in the first 2 s must use **different words** from the spoken hook (Budapest broke this: "BEFORE 1873" repeated the narration).

**CTA.**
- One spoken ask: the fixed sign-off "This is BHUGOL. Follow for more Geography Fun Facts."
- Plus a pinned-comment question tied to the twist.

**Hindi version.**
- Write it line by line, following bhugol-shorts §2d:
  - same speakers and the same chunk count per line
  - simple spoken Hindi
  - numbers and English terms spoken in English
  - no line longer than its English counterpart
  - jokes must land in Hindi
- Sign-off: "ये है भूगोल। ऐसे ही मज़ेदार जियोग्राफी फैक्ट्स के लिए फॉलो करें।"
- Budapest is the reference (`example-budapest/` and the `jobs/tts/budapest-hi.json` job in the repo).

**Shot plan (retention, both styles).** Plan the picture with the script, as spec fields (see `motion/README.md`, which lists every beat's fields).
**Plan the WHOLE script, whatever its length** (60 s, 85 s, 3 min): every line gets its shots and beats in the spec. The 25 s preview only proves the effects; it never stands in for the video (Centralia lesson: the preview had every upgrade, the full video did not, because the spec stopped at ~22 s).
- `shots`: one shot per new idea, each cut at the caption chunk where that idea starts, 0.15 s early. Cut types: `curve` primary (~60-70% of cuts); accents `zoom` (new chapter, dive from map to ground), `zoomIn` (arrival, payoff, "today"), `whip` (time jump, "rewind", "meanwhile"); `flash` hero at most twice (payoff and/or twist); `hard` for rapid-fire lists.
- `beats`: in-shot beats so a viewer gets a new visual event every 2-3 s (target: ≤2.7 s on average, no gap > 6 s):
  - **hook (0-8 s): a punch-in on every stressed phrase** (`{"kind": "punch", "scene", "at", "level": 1.15-1.4}`, rising levels), plus the title in the first 0.3 s
  - every on-screen number **counts up** in sync with its word (`count`), 1-2 climax numbers **slam** (`slam`)
  - reveals land when the voiceover names them (never front-load a scene); camera moves keep going in the back half
  - **v2 beats** (each is placed by the template AND gets its sound from `motion_plan.sfx`): `charslam` (hook title letters fly in, one word per beat), `grow` + `to` (a hook number grows while it counts, unit lands after), `flap` (split-flap board for a short stat), `circle` / `arrow` + `scene` + `until` (hand-drawn marker on the exact thing the voice names; aim for one every ~3-5 s where nothing else lands), `card` + `scene` + `until` (map stat card pinned to the pin), `impact` (sound-less marker for a shake)
  - hero cut: `burn` (fire burn, 3D) or `flash`; at most 2 hero cuts per video together
  - `moment` + `what`: a hand-made animation the template already has for that line (emoji pop, thermometer, bars, character entrance); it counts as a visual moment for the plan check
  - all text, numbers and positions live in the beat fields (`text`, `to`, `unit`, `prefix`, `name`, `flag`, `tag`, `c`/`r`, `from`/`to`, 2D overrides `c2d`/`r2d`/`from2d`/`to2d`, `col`); positions are plate-image pixels; `until` is optional (defaults to the next caption chunk at least 0.5 s later). Never hard-code per-video text in the template.
  - **no stretch over 5 s without a new visual moment** (cut, beat or title), from 0 s to the end card; the build enforces this (§9)

## 5. Approval stop (stop 2, one message + one AskUserQuestion)
Send one table: #, ~time, who, English line, Hindi line, retention job, **[ON SCREEN: …]**, **cut/beat** (the shot plan, for every line to the end, not just the hook).

Also include:
- the 2 hooks with scores
- the title/thumbnail pairing
- the **full list of on-screen text**
- the fact-check list (with dates for trend facts)
- the runtime estimate
- the hook formula used

Never add unrequested on-screen content without listing it here (punch-ins, count-ups of numbers already in the script and cuts add no new text). Then ask (AskUserQuestion takes at most 4 questions, so ask the first four together and **Codex** in a second call right after):
- **Style: 2D or 3D.** Give the times from the table at the top (2D: ~32 min render for both languages; 3D: ~100 min + ~15 min prep, sharper and more cinematic). Recommend 3D unless it's a trend topic with a tight posting window.
- **Skits:** A + C rules. Recommend skits when the script has a story moment with people or places, and say which characters come from the library. The user can say no.
- **Codex:** log in now or library only (§1.5).
- **Title:** which pairing.
- **Hindi captions: English or Hindi?** Every video with Hindi narration (the user is testing both). Hindi = Devanagari karaoke on the Hindi word timings; English = the English caption chunks shown under the Hindi voice, timed per line (each Hindi line's span split across that line's English chunks, no word karaoke).

If nobody answers, make the recommended choices and say so at the top.

## 6. Voices (Gemini, free)
**Engine.** One `jobs/tts/` job per language: speakers `{"Narrator": "Sadaltager", "Chars": "Puck"}`, all lines in ONE request.
- Character lines go to `Chars` with style tags (e.g. `[outraged, pompous]`).
- Direction: deep, warm, confident storyteller; comic pause before punchlines; softer for sad moments. For Hindi: "natural spoken Hindi like an Indian geography explainer channel; numbers and English words in English".
- TTS spellings: "Bhoogol", plus phonetic names (e.g. "Say-chen-yee", "Oh-buda").

**Quota.**
- Free tier: 10 requests/day per model: `gemini-3.1-flash-tts-preview` and `gemini-2.5-flash-preview-tts` (Pro TTS is 0).
- Up to 3 a minute; the runner waits these out.
- Resets at midnight Pacific (12:30 PM IST, 1:30 PM in US winter time).
- Check quota on aistudio.google.com/rate-limit. Never suggest enabling billing.
- Cost per video: about 2 requests (English + Hindi). Retakes: redo only the bad line (1 request) and splice it in at silences.

**Checks.**
- Scan loudness every 0.5 s for dropouts and noise.
- Add comic pauses with the kit's `pause.py` where a gap is under 0.6 s.
- Character voices: kit `voices.py` with `spec.voices` (e.g. Buda −3 preserved, Pest +2 preserved, Noble −1 preserved, Óbuda +4 shifted). Characters who talk to each other differ by at least 3 semitones. Run `voices.py` exactly once per `align.py` output (it re-pitches in place).

## 7. Timings (Whisper on Actions) + sound
1. Push `jobs/align/<id>.json` (`{"id": "<id>", "audio": "outputs/tts/<job>/<name>.wav", "lang": "en", "model": "small.en"}`).
   - Hindi: **always segmented**: `python3 bhugol-v2/hindi_align_job.py <id> outputs/tts/<job>/narration_hi.wav` writes the job (cut at pauses into 6-10 s pieces; one long take dropped whole lines of lake names). After `words_fit.py`, read its `interpolated` list: any proper noun in it gets its time patched from `words.txt` by hand before `align.py`.
2. Run `words_fit.py` (Whisper words → script tokens).
3. Run `align.py`: pause cap 0.42, `long_before` on punchlines, tempo 1.05 (Hindi 1.08), character lines at `line_tempo` 1.0.
4. Set every line's nominal `o` to its aligned start.
5. Then run `voices.py`, then the score (`example-bengaluru-3d/mkscore.py` pattern; `motion_plan.sfx` now gives every cut and beat a quiet on-beat click and hand-drawn marks a soft pen-swish, never a slide whistle; keep ambience beds (rain, stream, rumble) at gain <= 0.16 under beats so the clicks read without being loud): music `pad`/`drone`/`drums`/`bass` sections in real seconds, story-specific SFX, and **`motion_plan.sfx(plan, beats)` for the sound locked to the shot plan** (whoosh on every cut, impact on zoom landings, riser + hit on a hero flash, thud/pop on slams, ticks on count-ups, soft thud + whoosh on punch-ins). Don't also hand-place whooshes at cuts. One big spike (`shot`) at the payoff.
6. **Sound-timing fix (mandatory):** mkscore must call `motion_plan.unwarp(S, TIM)` after filling `fx` and `music`. score.py re-maps every time through its own chunk warp; without the inverse, anything on a mid-line chunk lands up to ~1 s off (Centralia had 11 of 18 timed sounds > 100 ms off).
7. **Bundled SFX layer:** mkscore ends with `motion/sfxlayer.py` (impact-bass-1 on the hook title landing, whoosh-cinematic + impact-bass-2 on each hero cut, peak-aligned) → `mix_final.wav`. Finish with `mix_final.wav`, not `mix_norm.wav`.
8. Hindi spec: `hindi_spec.py` needs a `tts` field in the Hindi file (the joined Hindi narration text); it deep-copies the English spec, so `shots`/`beats` carry over.

## 8. Art (library first, then Codex; 3D assets only for 3D)
1. Read `library/index.json`. Reuse any character or scene that fits (zero generation, identical look). Re-dress via a Codex edit with the library image as reference when a costume change is enough.
2. New art: Codex `exec --skip-git-repo-check -s workspace-write "Use your built-in image generation tool to create ONE image and save it…" < /dev/null`, one image per call (35-90 s each).
   - Use the prompt templates in `bhugol-v2/codex_gen_example.sh`, with the identical style sentence for every character.
   - Scenes: painterly/photoreal, empty ground in the lower middle, no people, no text, 1024x1536.
   - 3D style: **explainer moments become 3D dioramas** (the Centralia cross-section): "a 3D isometric cutaway diorama, high-end clay/vinyl-toy miniature, soft global illumination ... floats on a plain dark navy background". For a before→after reveal, generate the BEFORE, then make the AFTER as a Codex EDIT of it (`-i before.png` after the prompt, "keep everything identical, change only ...") so the two are pixel-aligned.
   - Aerial map plates: label the landmark pixel positions in `index.json`.
   - Never draw real living public figures; show them only through places, products and real quotes.
3. **Add every new character and scene to `library/` + `index.json` and push** (who, where it came from, pose, facing direction).
4. **3D assets (3D style only):**
   - **Depth + 2x:** push `jobs/depth/<id>.json` `{"id", "images": [...repo paths], "depth": [...], "upscale": [...]}` for every plate, diorama and character; then `3d/prep3d.py outputs/depth/<id> <art> --chars c_a,c_b` → `plate_<stem>.jpg`, `depth_<stem>.png`, trimmed 2x characters, `noise.png`.
   - **Map flyover:** `3d/map3d_prep.py job <id> lon0 lon1 lat0 lat1 --close ...` (≈12°x6° around the subject; close patch where the camera lands), push it, then `3d/map3d_prep.py build outputs/fetch/<id> <art> --admin1 "<state>" | --admin0 "<country>" --pin=<lon>,<lat>` → globe, graded Blue Marble, colour-matched Landsat patch, terrain heights, hillshade, region mask/outline.
   - **Reveal map:** `3d/burnmap.py before.png after.png seed_x seed_y spread.png` for spreading fire/water/borders.
5. Map imagery from hosts this workspace can't reach (NASA GIBS, AWS terrain tiles, public domain) comes via a `jobs/fetch/` job. Natural Earth comes straight from raw.githubusercontent.com.

## 9. Build and check (HyperFrames)
**2D style:** start from `example-centralia-2d/template.html` + `build.py`.
- The pattern: one DOM scene per shot; a camera in image coordinates per plate (`camTo` keyframes pinned to caption chunks `C(line, chunk, offset)`); screen-space characters with entrances, talking bob and a whip-zoom to the speaker; SVG overlays in image coordinates (labels, red X, borders, rings); captions; titles; badge → end card with FOLLOW BHUGOL and a tap.

**3D style:** start from `example-bengaluru-3d/` (newest; reused scenes, lon/lat labels, labelled circles) or `example-centralia-3d/` (fire, cost bars, thermometer). Both builds run the shader lint, the plan + sharp-beat checks and the pre-render gates automatically (§9b).
- Keep the engine section as is: `Track`/`key`/`valAt` keyframes (every scene update depends only on time), `plate3` (depth-displaced mesh with a camera that dollies/orbits via `x, y, z, yaw, pitch`, 10% overscan), `map3` (globe with atmosphere → terrain flyover with rising gold border wall, pin beam and label), `particles` (steam/smoke/embers), `glow`, `label`, camera-attached 3D props (thermometer, bars), characters, captions, titles, badge → end card, and the single render driver.
- Adapt per topic: the "build scenes" block (one scene per shot, its plate/depth/particles/labels) and the per-shot blocks in `build()` pinned to caption chunks.
- Shader extras on any plate: `prog` + spread map (before→after reveal), `grassP` + grid rect (things disappearing back to land), `bright`/`sat` (grey-out on the payoff), `heat`, `shim` (heat shimmer rect). The reveal's fire flicker is **opt-in** (`flick: 1` on fire plates only); on a city or water reveal it reads as a flickering screen.
- **Never write `//` comments inside the one-line shader strings** (use `/* */`): one blanked three scenes of a delivered video. `qa/shader_lint.py` now stops the build on it.
- A scene can appear in several shots (`S.wins`); a hand-drawn mark, label or card must sit where that shot's camera actually looks (the layout gate checks it).
- Steam/smoke: big soft particles (Gaussian falloff), alpha ≤ 0.5; embers additive and flickering.
- Each plate draws from its cut − 0.45 s to the next cut + 0.1 s, so cut overlaps never show a blank canvas.

### 9a. Motion and retention pass (mandatory, both styles)
Wired through `motion/motion.js` (handle **`MO`**; `M` may be the map data in a template). Rules from the HyperFrames motion doctrine (faceless-explainer motion-language + cut-catalog, hyperframes-animation, embedded-captions):
- **Cuts:** `MO.shots(D.shots...)` from the spec plan. Every shot change gets a designed cut; the cut is the exit (no separate exit animation except the final scene). Full-bleed safe: incoming shots never go below scale 1 and the outgoing shot stays under the incoming one, so no edge strip or black frame ever shows.
- **Captions:** `MO.karaoke(words, times, isKey)`: keywords (the `*starred*` words) pop 1.15 with a glow, others 1.03; `power3.out`; captions keep `display:inline-block; white-space:pre` spans.
- **Numbers:** every number shown on screen counts up with its spoken word (`MO.countUp`, 0.6-2.5 s, `power3.out`; `noScale` for 3D-projected labels); 1-2 climax numbers slam (`MO.slam`, shake only on the one climax).
- **Hook beats:** `MO.punch(scene.push, t, level)` on stressed phrases in the first 8 s (rising 1.15 → 1.4); more punch-ins wherever a shot has no beat for > 3 s.
- **Easing:** `power3`/`power4`/`expo` for camera, cuts and reading text; no `back`/`bounce`/`elastic` on text or cameras (playful `back.out` only on character entrances and emoji props). No slow pan alone in the back half of a shot; holds use only finite micro-jitter (`MO.jitter`), never endless "breathing".
- **Sound:** comes from the same plan via `motion_plan.sfx` (§7.5), so every cut and beat is heard; every cut also gets a short pop/crack so its onset is measurable.
- **v2 library ports (both styles; see `motion/README.md`):**
  - **Camera shake:** `MO.shake(at, .6, 'rig-6d-wobble', .75)` for impacts (replaces the old keyframe shake), `handheld-normal-mild` k 0.1-0.12 with `decay:false` across live-action plates; wrap only the scenes in `#cshake`; call `MO.shakeOn($('cshake'), D.dur)` once, last.
  - **Hook kit:** `MO.charSlam` on the hook title, `MO.countGrow` for the hook number, `MO.flap` for a short stat (top title area, y 150-420).
  - **Hand-drawn marks:** `MO.hwCircle` / `MO.hwArrow`, red (#FF3B30) on bright plates, yellow (#FFC23A) on dark ones. 3D: project the world point each frame. 2D: put them in the plate's image space (`S.cam`) so they ride the camera; sizes in image px (circles ~150x75).
  - **Maps:** fill the subject region with its flag (3D: `flag` texture in the terrain shader inside the region mask; 2D: `<image>` clipped by the border path) while the region is framed wide, fade it out as the camera dives in (it would fill the screen); then a stat card pinned to the pin with a dotted connector (count-up inside). Card position must be a pure function of time.
  - **Captions:** `MO.sweep` puts a red bar behind each keyword as it is spoken (no outline on the bar); call `layout()` again at the end of build.
  - **Motion blur:** mark only 1-3 snapping DOM elements (hook letters via `charSlam({blur: true})`, the climax slam): `data-hf-motion-blur='{"samplesPerFrame": 8}'`; never an element containing a canvas. ~9% render time.
  - **Hero cut `burn`:** 3D only, through `shader_xfade.js` (`BhugolMotion(tl, {xfade: true})`); in 2D the same cut becomes a warm flash.

**Sharp-beat check (automatic, 22 Oct 2026):** every stretch also needs a *sharp* event (a cut, punch, slam, count, grow, flap or card) at least every 4 s; circles, arrows and `moment`s alone don't count, because continuous motion (water filling, rain, particles) hides soft beats from viewers and from retention_qa. The build prints `SHARP GAP a-b` and stops.

**Plan check (automatic, before `index.html` is written):** `build.py` / `build3d.py` run `motion_plan.gaps` over every cut, beat and title time and **stop** on any stretch over 5 s with no visual moment (`PLAN GAP a-b`). Fix it in the spec (add a circle, arrow, grow, flap, card or moment on the line being spoken). `--allow-gaps` only for a deliberate hold, and tell the user which gap and why. (Old Centralia spec: 5 gaps, worst 14.4 s at 51-66 s; the full spec passes.)

**Both:**
1. No layout-property tweens (use x/y/scale). Bundle the emoji font (`assets/emoji.ttf`).
2. Run `hyperframes check`: fix errors (text overlaps, missing fonts). Structure warnings (file size, nested timeline) are fine. On 3D pages its browser session can hit its deadline ("Check did not finish"); then rely on snapshots + the two render gates.
3. Run `hyperframes snapshot --no-end --describe false --at <20-27 times>`, including frames at −0.15/+0.05/+0.15/+0.3 s around every cut. Review the contact sheets for clipped labels, overlaps with captions (keep key visuals at y 200-1250), edge strips at cuts, map seams, props too close to the camera, and anything covering the subject. Fix, then re-snapshot the problem times.
4. To preview a fix cheaply, build with `--preview=25` (3D) and render just the first 25 s (~17 min with v2). For a quick A/B of one effect, build `--preview=6` twice and render both (~4 min each). A preview checks the effects only: the full video still needs the full spec, the plan check to the end card, and the retention gate on the full render (§10).

### 9b. Pre-render gates (mandatory, both styles; the build runs them, `--no-gate` only to debug)
`bash bhugol-v2/qa/gates.sh <build_dir>` must print **ALL GATES PASS** for each language before any render:
- **scene gate** (`scene_gate.mjs`): seeks into every shot of the plan; fails on any WebGL/shader/page error or a shot whose plate is blank or hidden.
- **layout gate** (`layout_gate.mjs`): every 0.25 s measures every hand-drawn mark, plate label and map card on screen; fails when one is drawn entirely off screen, leaves the frame, sits under the dark top fade (label top < 160 px) or overlaps the caption band (y 1300-1470).
Fix the spec/template, rebuild, rerun. Both gates were checked against the Bengaluru failures (they catch all of them) and pass the fixed builds.

## 10. Render both languages + retention QA
1. Render in the background; make the thumbnails meanwhile.
   - 2D: `hyperframes render --quality looks --output work/silent.mp4` (EN 85 s ≈ 15 min, HI 100 s ≈ 17 min).
   - 3D: `hyperframes render --crf 14 --no-browser-gpu --output work/silent.mp4` (EN 85 s ≈ 45 min, HI 100 s ≈ 56 min).
2. **No post-render patching.** Re-rendering a few seconds and splicing them in does not work here (the renderer ignores a time-shifted timeline: the badge vanished and a counter reset in the patched parts). Any fix after a render = fix the spec/template, rerun the gates, full re-render.
3. **Retention QA gate, on the full render of each language (never a preview slice):** `python3 motion/retention_qa.py work/silent.mp4 --end <end_card_start> --spec <spec> --timing <timing_final>`. Targets: no frozen window > 2 s, **no `plate missing` stretch** (picture area flat while captions run), ≥ 85% of the time moving, a visual event every ≤ 2.7 s on average with no gap > 6 s, the hook frame already moving, no black frames, transition grammar OK. Fix a CHECK by adding beats/cuts where the gaps are, or say why it is deliberate. (Centralia 3D first 25 s: one event every 4.1 s, longest gap 8.8 s before the pass; 3.1 s and 5.5 s after.)
4. **Sound-on-beat gate:** render an FX-only stem (same mkscore with music `level` 0 and a silent `voice.wav`, then `sfxlayer.py`), `npx hyperframes audio <stem> --quality fast --json --only onsets > on.json`, then `python3 motion/sfx_check.py on.json <spec> <build>/times.json`. Target: every cut and beat has a sound-effect onset within 100 ms (Centralia preview: 17/17).
5. **Grade** the silent render before finishing (BHUGOL default teal-orange at 80%; if ffmpeg runs out of memory, open the file as separate inputs instead of `split`): `ffmpeg -i silent.mp4 -filter_complex "[0:v]split[a][b];[b]lut3d=file=bhugol-v2/grade/teal-orange-blockbuster.cube[g];[a][g]blend=all_mode=normal:all_opacity=0.8,format=yuv420p" -c:v libx264 -crf 12 silent_graded.mp4`. To pick another look, `npx hyperframes grade-compare --for <frame.png> --luts a.cube,b.cube,c.cube` and choose from the sheet.
6. Finish (thumbnail into frames 0-2, `mix_final.wav` muxed in):
   - 2D: `finish.sh` (adapt its paths to `silent_graded.mp4` + `mix_final.wav`), two-pass encode under 30 MiB.
   - 3D: `3d/finish_hq.sh <silent_graded.mp4> <mix_final.wav> <thumb_v.jpg> <out.mp4>`, x264 CRF 17, AAC 192k, no size cap (~11-12 Mbps, ~120-140 MB).
7. Also run the kit's `attention.py` (≥ 85% moving; Centralia 2D 85%, 3D 91%).
8. **Final-file QA (mandatory before delivery):** on the exact MP4s being sent, run `retention_qa.py` again (black frames, plate missing) and `python3 bhugol-v2/qa/audit_sheets.py <final.mp4> <dir>`, then **view every sheet** (frames every 0.5 s). A number (jitter, cadence, loudness) never stands in for looking: the Bengaluru re-delivery passed a flicker metric while three scenes were black.
9. Check sync on 4-8 words (crop the caption band at word times) and check frames 0, 2 and 3.
10. **Hindi:** the same composition with Hindi caption chunks, `i18n` labels and titles, and a Devanagari font (bundle Mukta 700/800 from the kit's node_modules as a fallback in `.cl`/`.tl`/`.lbl`/`.plbl`), re-timed to the Hindi alignment. Captions follow the user's English/Hindi answer from §5. The v2 on-screen elements (flip boards, hook numbers like "64 YEARS", map cards) **stay in English** in the Hindi video (the user's choice: Hindi speakers who prefer reading English). Check 6-8 stills for clipped Devanagari.
11. File names: `BHUGOL_<Title>.mp4` and `BHUGOL_<Title>_HI.mp4`.

## 11. Thumbnails (follow thumbnail_rules.md; same recipe for English and Hindi)
1. **Default for every video, 2D or 3D, English and Hindi → the split thumbnail** (`thumb_split/split.py <config.json>`; the user's pick on 24 Oct 2026, modelled on a GeoGlobeTales outlier):
   - two satellite halves side by side with a **white divider**: the "cold / before / A" place on the left, the "warm / after / B" place on the right
   - in each half **one region filled in a bold flat colour** with a light edge and soft drop shadow (e.g. USA blue, Europe orange)
   - a **look** per half that tells the story at a glance: `cold` (frosty blue grade + snow specks), `warm` (golden grade + glowing embers) or `none`
   - **one label per half, highlighted**: black text on a **yellow highlight bar** with a thin white border (Hindi labels in Devanagari: अमेरिका | यूरोप); 1-2 words each, kept inside its half
   - no characters, people, faces, emoji clutter or extra headline; badge optional
   - config lists the two halves (`lon` span, Mercator centre `lat`, `iso` or `continent` + `exclude`, `keep` filter, `look`, `fill`, `edge`, `label` {en, hi}, `label_at`); Blue Marble via a `jobs/fetch/` job (see `thumb_split/gulf.json`)
   - for a topic with no natural pair, show the user one split option and one recipe-A / map-led option, and let them choose
2. **Alternatives (only when the user asks, or as the second option above):** 3D recipe A (`3d/thumb_a.py`, flag-filled terrain + fire/glow + red circle + zoom bubble + giant number) or the 2D map-led design (`thumbnail_template.html`: flag-coloured region, red hand-drawn circle + arrow, 2-3 emoji, 1-3 words).
3. **Two versions per language**, English and Hindi: vertical 1080x1920 (`split_<lang>_v.jpg`) and 16:9 1280x720 (`split_<lang>_w.jpg`); `split.py` makes all four in one run.
4. **Shrink to ~140 px wide and check both regions and both labels survive** (yt-audit); `split.py` writes `feed_split_<lang>_*.jpg`.
5. **Show all four to the user and get a yes before burning frame 0 into the videos.** If they want another direction, build 2-3 variants, show them side by side with the 140 px test, recommend one with the evidence, and ask.

## 12. YouTube kits (yt-seo + yt-package), English first, then Hindi
1. **Re-check the facts first:** verify every number and date in the script against sources the same day (WebSearch/WebFetch; prefer official/primary pages), keep each source URL, and keep disputed origins as "the story goes".
2. **Query test:** write the 3 searches each video should win. The title + description lines 1-2 must contain those words. This applies to **both** kits, each in its own audience's words: the English kit uses English searches; the Hindi kit uses what Hindi viewers type (Devanagari terms such as सेंट्रेलिया / जलता हुआ शहर, Hinglish, plus the place name in English letters). For trend topics, include the trending term people are searching this week.
3. **Titles:** 5 ranked per language, **each in its own code block** with its character count and `title.py` score. Lint each title against that language's **actual thumbnail words** (`title.py --title ... --thumb "<the thumbnail's words>"`): never repeat the thumbnail's words or number (e.g. thumbnail "STILL BURNING 1962" → titles use 64 years, not 1962 or burning). Keep the subject inside 40 characters, a number in it, no hype words from `voice.md`. Title 1 = feed-first (the pattern of the top outliers: impossible claim + number + emoji); include at least one search-first title with the place name.
4. **Description:**
   - lines 1-2 search-led (what the video gives, in that audience's search words), not the hook
   - then one short paragraph with the key facts in `voice.md` style (hedges kept)
   - then `Sources:` (one per line, with URLs)
   - imagery/map credits (e.g. NASA GIBS Blue Marble/Landsat, AWS Terrain Tiles, Natural Earth) and "Scenes are AI-generated illustrations" (Hindi: "दृश्य AI से बनाए गए चित्र हैं।"); bundled HyperFrames SFX need no credit
   - last line: `#Shorts` + 2 topical hashtags (one in Hindi for the Hindi kit)
5. **Tags:** ≤15 in one comma-separated copy block, mostly name or spelling variants people type (e.g. Széchenyi/Szechenyi, Óbuda/Obuda; Devanagari spellings in the Hindi kit) + topic + BHUGOL. Never stuff or add terms the video doesn't cover.
6. **Pinned comment:** the question most viewers will have, tied to the twist (<300 characters), in each language.
7. **Upload note:** when the video has realistic AI scenes of a real place or event, tell the user to set YouTube's "Altered or synthetic content" to **Yes** on both uploads.
8. End every kit with: **ship it, or change it?**

## 13. Deliver
1. SendUserFile both MP4s (attach), English first, then the thumbnails (render).
2. Put the kits in the reply as copy blocks.
3. Report the plan check (longest planned gap), the pre-render gates (scene + layout), the full-render retention QA result (cadence, longest gap, moving share, plate missing) and the sound-on-beat result (n/n), and confirm the audit sheets of the final files were viewed.
4. Push new library art.
5. Report the Gemini requests used (out of 10/day per model).
6. For trend topics, remind the user of the posting window (⏰).

## After publishing (offer once, don't nag)
- **Retention (yt-retention):**
  1. After about 48 h the user exports the Studio audience-retention CSV.
  2. Run `retention.py`.
  3. Name the ONE biggest leak: **hook leak** (healthy: <25% lost in 30 s), a **cliff**, or a **slide**. Give one fix, and carry the lesson into the next script and shot plan.
- **Comments (yt-comment):** triage into questions / corrections / praise / bait. Replies under 30 words. Pin the question most people share. Repeated questions become topic ideas.
- **Monthly audit (yt-audit):**
  - the last 10 titles as a set (variety)
  - thumbnails at feed size
  - hook scores of the last 3
  - upload **consistency**

  Ends in ONE fix + 3 things that work.
- **Weekly plan (yt-plan):** sized to the hours the user actually has; consistency over frequency; post on the channel's best day from analytics (ask, don't assume). Mix trend-riders with evergreen topics.

## Gotchas learned
- (22 Oct, Bengaluru) A `//` comment inside a one-line GLSL string compiled to a broken shader: three scenes rendered black and the video was delivered that way. Shader lint + scene gate + `plate missing` now catch it; also always look at the audit sheets of the final file.
- (22 Oct) Re-rendering a slice by wrapping/offsetting the timeline is unreliable (renderer stalls, or badge/counters break). Full re-render only.
- (22 Oct) ffmpeg `split` on one input feeding a long concat + LUT blend buffered ~6 GB and was OOM-killed; open the same file as separate inputs per segment.
- (22 Oct) `motion.js` curve cut set the incoming shot to 35% opacity after its fade-in; fixed. A scene reused later in the plan is hidden at 0 by its later cuts unless the first shot is forced visible (templates do this now).
- (22 Oct) Never name a map-scene field `ll`: it is the lon/lat->globe function; use `lls` for lon/lat labels.
- `pkill -f` patterns can kill your own shell; avoid them, or anchor the pattern.
- `~` is `/root`; use absolute `/home/claude` paths.
- YouTube blocks full video/caption downloads from GitHub runners ("not a bot"); listings and thumbnails work. Script text of past BHUGOL videos lives in their Artifact pages (`read` with `path: index.html`, then extract the `"text"` fields).
- Gemini 429 "limit: 3" = per-minute (wait); "limit: 10" with hours to retry = daily (switch model or wait).
- The faster-whisper + PyAV clash on Actions is fixed by decoding WAV with numpy (already in `tools/whisper_words.py`).
- HyperFrames lint: never animate left/top; the emoji font needs `@font-face`.
- Titles and caption chunks: put punctuation inside the `*keyword*` markers (`*1873,*`, not `*1873*,`).
- Codex: `codex exec` hangs on "Reading additional input from stdin" unless stdin is `/dev/null`; `-i file` placed before the prompt swallows the prompt.
- A CSS `filter` tween with no starting value flashes one black frame; set the starting filter explicitly (motion.js always does).
- Don't put a `//` comment in the middle of a one-line JS statement when patching templates; it silently comments out the rest of the line.
- 3D props attached to the camera: keep them ~1.3-1.4 units away and small, or they fill the frame.
- 3D map: clamp the elevation outliers (p99.9) and colour-match the Landsat close patch to the Blue Marble plate, or the terrain shows walls and a visible seam.
- 3D thumbnails: render with `--use-angle=swiftshader` in the headless shell; take the payoff point from the page (`window.__C`) instead of guessing.
- Playwright `waitForFunction` must return a boolean (`!!(window.__timelines && window.__timelines.main)`); returning the GSAP timeline object hangs.
- The HyperFrames docs' zoom-through values (0.75/0.8) and ±230 px partial travel are for text on a shared background; on full-bleed plates use the scale-up variants in `motion.js`.
- HyperFrames' own `HyperShader.init()` shader transitions switch the WHOLE render to a layered screenshot route (~5 s per frame here); use `motion/shader_xfade.js` instead. WebGPU registry items only run with `--enable-unsafe-webgpu` on a localhost page (`PRODUCER_ALLOW_SOFTWARE_WEBGPU=true` for renders) and are slow; pre-render their loops to video.
- `hyperframes add <item>` works here (it fetches from GitHub raw), but item files load GSAP/d3/three/fonts from jsdelivr/Google; vendor those from npm before rendering offline. Registry 3D blocks pin other three.js versions than our r149.
- Effects driven by property-setter "drivers" must compute everything from the driver's own time argument, never from another tween's state (render order between tweens is not guaranteed on a seek). That bug hid the 2D map card until fixed.
- A `fromTo` with `immediateRender:false` shows the element's END state before the tween starts; hide per-glyph/per-word elements explicitly (`tl.set(el, {opacity: 0}, 0)`), or words flash fully formed before flying in.
- Beats with `until` need the build to convert it (`u: C(*until)`); without it, hand-drawn marks silently never draw. Without `until`, the template ends the beat at the next caption chunk that starts **at least 0.5 s later** (a tighter 0.05 s window picked the beat's own chunk through float rounding, so the hook flip board never faded and later overlapped "500 HOMES").
- `hyperframes snapshot` sends frames to Gemini when GEMINI_API_KEY is set; always pass `--describe false`. A plain Playwright screenshot of a HyperFrames page is black (the runtime shows the stage); use `snapshot` for stills.
- Re-mixing a finished video (sound fix only): rebuild the mix with the original fx list + `motion_plan.unwarp`, then `ffmpeg -i video.mp4 -i mix_norm.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k` (no re-render).
- Before building any new effect, check `bhugol-v2/research/hyperframes/` (README first): it lists what already exists in HyperFrames, what runs on our renderer, and what it costs.
- A feature that only exists in the preview is not shipped: after any template upgrade, re-run the plan check on the full spec and snapshot beat times from the back half too (Centralia's full video was rendered before the upgrades and its spec covered only the first ~22 s).