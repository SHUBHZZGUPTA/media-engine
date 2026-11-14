# BHUGOL Shorts: seamless loop close + Countdown Twins framework (14 Nov 2026)

From the same-size countries Short (EN `-PJYpUVDU_k`: 1,336 views at 16 h, above every recent EN Short's 24 h count;
HI `waRS0ZxSYQI`: 991 at 17 h, a seeded Hindi Short). Source: `bhugol-v2/example-twins-3d/`. Board rules L26-L35, test H10.

## 1. Seamless loop close (every Short, EN + HI; replaces the sign-off) — L26
The video never ends; it hands back to its own first line so viewers don't notice the restart.
- **Script.** The last line is the **loop line**: a callback to the hook that reads as one sentence with line 1.
  The last word is the loop word. Example: "...I think they were made for each other. Want to go double or nothing? Because..."
  → (restart) "I bet $100 you didn't know..."
  - Read the last line and line 1 aloud back to back; if it doesn't sound like one sentence, rewrite one of them.
  - No spoken sign-off, no spoken comment prompt, no "follow". The pinned comment carries the question.
  - Hindi gets its own loop line that flows into Hindi line 1 ("Double or nothing करें? क्योंकि..." → "मैं हंड्रेड डॉलर की शर्त...").
- **Picture.** No end card. The BHUGOL badge stays on screen the whole video. The last shot travels back to the exact
  frame-0 composition (same scene, same camera pose, same lit regions), e.g. the closing pull-back to the opening globe.
- **Cover = frame 0 = the loop seam (option B, L33).** Over the last ~0.4 s the cover headline (the title, white outlined
  caps, yellow box on the last/second-last word) eases in over that composition; frames 0-2 are that same picture with the
  headline fully shown; from ~0.1 s the headline animates out as the hook title comes in. The burned cover is therefore
  also the last frame, so the restart is invisible and "first frame" still works as the Shorts thumbnail.
- **Sound.** The loop word ends ≤ 0.15 s before the last frame. The music bed has no fade-in at 0 and no fade-out at the
  end, at the same level on both sides of the seam; no SFX hit lands on the seam.
- **QA (seam check, both languages).** Put the last 0.5 s and the first 0.5 s side by side (frames + waveform): the last
  frame and frame 0 should match, the RMS jump across the seam should be < 6 dB, and no caption should pop at the seam.

## 2. Countdown Twins (one format in the topic mix, not the default) — H10
A #5→#1 countdown on ONE premise a viewer gets at a glance (same size, same latitude, same shape, same distance).
| Slot | Time | Line pattern (example) |
|---|---|---|
| Hook | 0-6 s | Dare + whole premise: "I bet $100 you didn't know there are some countries that look completely different but are almost exactly the same size!" |
| Item opener | 1 line | "Number N is A and B." |
| Contrast | 1 line | "One touches the sky with Mount Everest, the other touches the ocean with its rivers." |
| Physical metaphor | 1 line | Something the visuals can literally do: "Pull Zambia like chewing gum…", "boot + sitting man = a human body" |
| Reaction | 2-3 words | "So sad." (a code-drawn character) |
| #1 reveal | slowest line | "And number one… is Malaysia and Vietnam!" — the biggest moment of the video |
| Loop line | last 2 s | Callback to the hook's dare: "Want to go double or nothing? Because…" |
- ~150-160 words, ~60-70 s; sentences ~9 words; each item 8-13 s, so a rank re-hook lands every ~10 s.
- Pairs/items are international (no India-first anchors, L27): pick places viewers anywhere know.
- Facts: every area/number from one primary source (CIA World Factbook etc.), hedged with "almost/about".

## 3. Rules that apply to every Short (not just countdowns)
- **Dare hook (option, L28):** second person, the whole premise in sentence one, ≤ 25 words.
- **Proof within 2 s (L29):** every spoken claim gets its visual proof on screen within 2 s (true-size overlay, flag fill, count-up card).
- **List items (L30):** subject → contrast → physical metaphor, and the shot plan animates the metaphor literally.
- **Countdowns (L31):** rank slam every item; #1 gets gold + rays + crown + confetti + one shake.
- **Personality beats (L32):** 2-3 words, ~one every 15 s.
- **International framing (L27).**

## 4. Visual and production rules
- **Size comparisons are filmed top-down (L34):** camera elevation ≥ 86°. At a tilt the near end of a tall shape is
  magnified (the UK looked twice Guinea's size at 74°).
- Mask the Landsat close patch where it is near-black (ocean tiles) and drop it entirely in wide scenes (`cls: false`).
- Masks/flag fills at 4096 px wide, or country edges look blocky in close-ups.
- **Motion blur (L35): only on elements on screen < 1 s** (hook letters, one slam). Never on anything that stays up:
  blur on the five persistent rank badges made the render 24 s/frame.
- **Render (L35):** 3D on Kaggle GPU (Shubham's rule). Until that path exists: 10 s chunks (`build.py --from --to`,
  `render_one.sh`), each well under the 10-minute foreground limit, so a workspace restart only loses one chunk.
- **Finish:** x264 CRF 19 for Shorts (CRF 17 made a 67 s Short 111 MB, over the uploader's 100 MB cap). QC the re-encode:
  same frame count and duration.
- **Hindi pace check:** measure the Hindi take's words/s; Holden's Hindi came back at 43.7 s with no pauses, fixed by
  adding breaths between lines and slowing 5% (`example-twins-3d/tools/pad_lines.py`).
- **Upload:** post the pinned comment only after go-live; the comment job can time out on `pip install` (5-minute job cap).
- **Gemini quota:** `tts_quota.py` misreads a shallow clone (every file looks committed now); check the day's TTS commits
  with `gh api .../commits?path=outputs/tts&since=<08:00 UTC>`.
