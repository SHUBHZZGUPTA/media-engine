---
name: bhugol-shorts-v2
description: Make a BHUGOL world-geography Short end to end with the free v2 pipeline (yt-viral topic, story script, Gemini voices, Codex skit art, HyperFrames), in English plus Hindi, with data-backed thumbnails and YouTube kits. Use instead of bhugol-shorts when the user asks for v2 or the free pipeline.
---

# BHUGOL Shorts v2 (free pipeline)

One BHUGOL world-geography Short, English + Hindi on the same visuals. Costs nothing beyond the user's Claude,
ChatGPT and Google subscriptions. The original `bhugol-shorts` skill stays unchanged; this is a separate skill.
One video per chat (it keeps Claude usage low); if this chat already holds a finished video, suggest a new chat.

The run stops for the user **twice**: the topic pick (1), and the approval stop (5). It then runs to delivery.

Task list:
1. Setup
2. Topic
3. Package
4. Script, hooks, Hindi
5. Approval stop
6. Voices
7. Timings
8. Art (library first)
9. Build + check
10. Render both
11. Thumbnails
12. YouTube kits
13. Deliver

## 1. Setup (every new chat)
1. **Repo.**
   - Call `add_repo` with owner `SHUBHZZGUPTA`, repo `media-engine`, access `push`.
   - Clone it to `/home/claude/media-engine`.
   - It holds everything the run needs:
     - `tools/`: Gemini TTS, Whisper, fetch, yt-dlp collector
     - `.github/workflows/`: the GitHub Actions mailbox jobs
     - `bhugol-v2/`: `build.py`, `template.html`, `finish.sh`, `thumbnail_template.html`, `thumb_shot.mjs`, `thumbnail_rules.md`, `voice.md`, `example-budapest/`
     - `library/`: characters, scenes, `index.json`
2. **Kit.** `Artifact` read `https://claude.ai/artifact/QL2xuVyTsyzJ49Lw7Pqggi` path `kit.json`. Unpack it into `/home/claude/bhugol-kit` exactly as in bhugol-shorts §1, then run `./setup.sh`. The kit's tools are reused: `align.py`, `voices.py`, `score.py`, `pause.py`, `words_fit.py`, `transcribe.py`, `attention.py`.
3. **HyperFrames + GSAP.**
   - Install in a work folder with `npm i hyperframes@0.8.181 gsap@3`.
   - Always export these environment variables:
     ```
     HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_NO_UPDATE_CHECK=1 HYPERFRAMES_SKIP_SKILLS=1
     HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
     ```
   - `build.py` copies `gsap.min.js` from `node_modules/gsap/dist/`; fix that path for the new work folder.
4. **Read** `bhugol-v2/voice.md` and `bhugol-v2/thumbnail_rules.md` before writing anything.
5. **Codex login is the user's call each video.** Ask at the approval stop: "Codex for new art: log in here now (device code on your phone), or reuse library art only?" Never automate or store the Codex login without the user's explicit go-ahead.

**GitHub mailbox pattern.** The GitHub Actions API is blocked from this workspace. To run a job:
1. Commit a job JSON under `jobs/<kind>/` and push it. That push triggers the workflow.
2. The workflow commits its outputs back with `[skip ci]`.
3. Poll with `git pull` until the output appears (`until ...; do sleep 10; done` with `run_in_background`).

Job kinds:
- `jobs/tts/` → `outputs/tts/` (Gemini; key in the `GEMINI_API_KEY` secret, never printed)
- `jobs/align/` → `outputs/align/` (Whisper word timings)
- `jobs/fetch/` → `outputs/fetch/` (public files from hosts this workspace can't reach, e.g. NASA GIBS)
- `jobs/viral/` → `outputs/viral/` (public channel listings, optionally thumbnails)

If a push is rejected, `git pull --rebase` and push again.

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

## 4. Script, hooks, Hindi
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

## 5. Approval stop (stop 2, one message + one AskUserQuestion)
Send one table: #, ~time, who, English line, Hindi line, retention job, **[ON SCREEN: …]**.

Also include:
- the 2 hooks with scores
- the title/thumbnail pairing
- the **full list of on-screen text**
- the fact-check list
- the runtime estimate
- the hook formula used

Never add unrequested on-screen content without listing it here. Then ask in one AskUserQuestion:
- **Skits:** A + C rules. Recommend skits when the script has a story moment with people or places, and say which characters come from the library. The user can say no.
- **Codex:** log in now or library only (§1.5).
- **Title:** which pairing.

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
- Character voices: kit `voices.py` with `spec.voices` (e.g. Buda −3 preserved, Pest +2 preserved, Noble −1 preserved, Óbuda +4 shifted). Characters who talk to each other differ by at least 3 semitones.

## 7. Timings (Whisper on Actions)
1. Push `jobs/align/<id>.json` (`{"audio": "outputs/tts/<job>/<name>.wav", "lang": "en", "model": "small.en"}`).
   - Hindi: `"lang": "hi", "model": "small"`. Long Hindi takes may need the kit's chunked `transcribe.py` approach if words drop out.
2. Run `words_fit.py` (Whisper words → script tokens).
3. Run `align.py`: pause cap 0.42, `long_before` on punchlines, tempo 1.05, character lines at `line_tempo` 1.0.
4. Set every line's nominal `o` to its aligned start.
5. Then run `voices.py`, then `score.py` (music `pad` sections and `fx` cues in real seconds; one big spike, e.g. `shot`, at the payoff).

## 8. Art (library first, then Codex)
1. Read `library/index.json`. Reuse any character or scene that fits (zero generation, identical look). Re-dress via a Codex edit with the library image as reference when a costume change is enough.
2. New art: Codex `exec --skip-git-repo-check -s workspace-write "Use your built-in image generation tool to create ONE image and save it…"`, one image per call (35-90 s each).
   - Use the prompt templates in `bhugol-v2/codex_gen_example.sh`, with the identical style sentence for every character.
   - Scenes: painterly, empty ground in the lower middle, no people, no text, 1024x1536.
   - Aerial map plates: label the landmark pixel positions in `index.json`.
3. **Add every new character and scene to `library/` + `index.json` and push** (who, where it came from, pose, facing direction).
4. Map imagery from hosts this workspace can't reach (NASA GIBS Blue Marble/VIIRS, public domain) comes via a `jobs/fetch/` job. Natural Earth comes straight from raw.githubusercontent.com.

## 9. Build and check (HyperFrames)
1. Start from `bhugol-v2/build.py` + `template.html` (Budapest).
   - The pattern: one DOM scene per shot; a camera in image coordinates per plate (`camTo` keyframes pinned to caption chunks `C(line, chunk, offset)`); screen-space characters with entrances, talking bob and a whip-zoom to the speaker; SVG overlays in image coordinates (labels, red X, bridges, rings); house captions; titles; badge → end card with FOLLOW BHUGOL and a tap.
   - Copy and adapt it per topic.
2. Every scene update depends only on time. No layout-property tweens (use x/y/scale). Bundle the emoji font (`assets/emoji.ttf`).
3. Run `hyperframes check`: fix errors (text overlaps, missing fonts).
4. Run `hyperframes snapshot --no-end --describe false --at <20-27 times>`. Review the contact sheets for clipped labels, overlaps with captions (keep key visuals at y 200-1250), and anything covering the subject. Fix, then re-snapshot the problem times.

## 10. Render both languages
1. Run `hyperframes render --quality looks --output work/silent.mp4` in the background (about 15-20 min for 80 s). Make the thumbnails meanwhile.
2. Run `finish.sh` (adapt its paths):
   - the vertical thumbnail into frames 0-2
   - the mix muxed in
   - a two-pass encode under 30 MiB
3. Then run `attention.py`: aim for a change every ≤2.4 s and ≥70% of the time moving.
4. Check sync on 4-8 words (crop the caption band at word times) and check frames 0, 2 and 3.
5. **Hindi:** the same composition with Hindi caption chunks, `i18n` labels and titles, and a Devanagari font (bundle Mukta 700/800 from the kit's node_modules as a fallback in `.cl`/`.tl`/`.lbl`), re-timed to the Hindi alignment. The first Hindi render is untested: check 6-8 stills for clipped Devanagari and untranslated labels.
6. File names: `BHUGOL_<Title>.mp4` and `BHUGOL_<Title>_HI.mp4`.

## 11. Thumbnails (follow thumbnail_rules.md)
1. **Style.**
   - Map-led; **no characters, people or faces**.
   - The subject region coloured in its **flag colours**.
   - A **red hand-drawn circle + arrow** on the payoff spot.
   - 2-3 emoji stickers (🤯 😱 + the flag emoji).
   - 1-3 words, never repeating the title.
   - High saturation with red accents.
   - A number if the title has none.
   - Badge small, top-left.
2. **Two versions.**
   - Vertical 1080x1920.
   - 16:9 1280x720: re-crop or rotate so the coloured regions still read; text left, subject right.
3. Start from `thumbnail_template.html` + `thumb_shot.mjs`.
4. **Shrink both to ~140 px wide and check the subject, circle and words survive** (yt-audit). Hindi thumbnails get Hindi words.

## 12. YouTube kits (yt-seo), per language
1. **Query test first:** write the 3 searches the video should win. The title + description lines 1-2 must contain those words.
2. **Titles:** 5 ranked, **each in its own code block** with its character count.
3. **Description:**
   - lines 1-2 search-led (what the video gives, in searchers' words), not the hook
   - then `Sources:` (one per line)
   - imagery/map credits
   - last line: `#Shorts` + 2 topical hashtags (one in Hindi for the Hindi kit)
4. **Tags:** ≤15, mostly name or spelling variants people type (e.g. Széchenyi/Szechenyi, Óbuda/Obuda) + topic + BHUGOL. Never stuff.
5. **Pinned comment:** the question most viewers will have, tied to the twist (<300 characters).
6. End every kit with: **ship it, or change it?**

## 13. Deliver
1. SendUserFile both MP4s (attach), English first, then the thumbnails (render).
2. Put the kits in the reply as copy blocks.
3. Push new library art.
4. Report the Gemini requests used (out of 10/day per model).

## After publishing (offer once, don't nag)
- **Retention (yt-retention):**
  1. After about 48 h the user exports the Studio audience-retention CSV.
  2. Run `retention.py`.
  3. Name the ONE biggest leak: **hook leak** (healthy: <25% lost in 30 s), a **cliff**, or a **slide**. Give one fix, and carry the lesson into the next script.
- **Comments (yt-comment):** triage into questions / corrections / praise / bait. Replies under 30 words. Pin the question most people share. Repeated questions become topic ideas.
- **Monthly audit (yt-audit):**
  - the last 10 titles as a set (variety)
  - thumbnails at feed size
  - hook scores of the last 3
  - upload **consistency**

  Ends in ONE fix + 3 things that work.
- **Weekly plan (yt-plan):** sized to the hours the user actually has; consistency over frequency; post on the channel's best day from analytics (ask, don't assume).

## Gotchas learned
- `pkill -f` patterns can kill your own shell; avoid them, or anchor the pattern.
- `~` is `/root`; use absolute `/home/claude` paths.
- YouTube blocks full video/caption downloads from GitHub runners ("not a bot"); listings and thumbnails work. Script text of past BHUGOL videos lives in their Artifact pages (`read` with `path: index.html`, then extract the `"text"` fields).
- Gemini 429 "limit: 3" = per-minute (wait); "limit: 10" with hours to retry = daily (switch model or wait).
- The faster-whisper + PyAV clash on Actions is fixed by decoding WAV with numpy (already in `tools/whisper_words.py`).
- HyperFrames lint: never animate left/top; the emoji font needs `@font-face`.
- Titles and caption chunks: put punctuation inside the `*keyword*` markers (`*1873,*`, not `*1873*,`).
