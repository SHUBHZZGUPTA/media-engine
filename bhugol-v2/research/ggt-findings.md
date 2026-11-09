# GeoGlobeTales findings: brief for the BHUGOL test Short

These are research notes only, so **no skill has been changed**. If the test Short beats BHUGOL's baseline, the learnings go into the bhugol-shorts-v2 skill set, including the remake rule below.

- Full research doc: https://claude.ai/artifact/XPsyLmjwoZtSJRDiLutwV8
- Raw Gemini audio-visual analysis, one per video: `outputs/watch/ggt-<id>/full.md`
- Research date: 2026-11-09. It covers all 169 GeoGlobeTales (@GeoGlobeTales) videos: transcripts, comment samples and Gemini watch reports.

## Step 0 — before any topic is picked: check our analytics against these findings

Run this before the topic stage on every BHUGOL Short (Shubham, 2026-11-09).

1. **Pull fresh analytics.**
   - Use the latest `outputs/ytdeep/mon-*/report.json` if it is under 24h old.
   - Otherwise push a `jobs/ytdeep/<id>.json` job with tokens `YT_RT_BHUGOL_EN` and `YT_RT_BHUGOL_HI`.
   - Analytics come from the YouTube connection, not the Gemini key.
2. **Set the baseline** for each channel:
   - median views and the top 5;
   - engaged views, average % viewed and comments per 1K views;
   - views by country, with average % viewed per country;
   - traffic sources.
3. **Score our own past Shorts by topic type**, using the same types as the table below. Also note which of them were GeoGlobeTales remakes and how each did against our median.
4. **Rank candidate topics** on three things:
   - GeoGlobeTales' result for that topic type, or for that exact video if it's a remake;
   - BHUGOL's own result for that topic type;
   - not already posted on BHUGOL.

   Remakes and re-angles are both allowed. Use no country framing unless the audience data supports it.
5. **Show Shubham the ranked table with the evidence**, and let him pick before scripting.

For this test Short, Step 0 was run on 2026-11-09 and gave the topic below. The new chat only needs to log the baseline at upload time.

## The test Short (decided 2026-11-09)

| Item | Decision |
|---|---|
| Topic | **Spain's Strangest Borders**: a remake of GeoGlobeTales `f3DnZlduEoE`. It ran 47.1M views and 5.8× its cohort, with 9.7K comments. Remake the topic and structure only. Write our own script, visuals and art, and copy none of their wording or footage (avoids copyright claims and "reused content" rejection). |
| Versions | English + Hindi on the same visuals (skill default) |
| Ending | Character punchline as the last story beat, then a short BHUGOL sign-off (comment prompt folded into the punchline) |
| Thumbnail | New BHUGOL cover: one subject, one visual joke, our own colour-popping palette, 1–4 words carrying the title's question. Shown to Shubham before burning in. Not the old split thumbnail. |
| Framing | **World audience, no country framing.** BhuGol EN all-time views: IN 35.8%, US 29.5%, PH 13.7%, GB 3.4%, CA 3.0%. Indian viewers watch the least (58% average viewed, vs US 72% and PH 86%). |
| Upload | Via media-publish. "Altered or synthetic content" = **No** (Shubham's standing rule; it overrides skill §12.7). |

### What the original did, and what to improve

- **Structure:**
  - **Opening:** "Spain is the country with the strangest borders", then a neighbour counter flips 0 → 2 (France, Portugal) → 5+.
  - **Story order:** Llívia (first payoff at 12.5s), then Pheasant Island, Andorra, Gibraltar, and Ceuta/Melilla plus the 85 m Peñón border as the last line.
  - It ends on a stat, with no CTA and a seamless loop.
- **Comment magnet: Pheasant Island.** It changes country every 6 months, and it drove almost every top comment ("Where do you live?" "Depends on the month" — 86K, 25K, 11K likes). The original had **no skit**. Our improvement: a 2–4 line Pheasant Island skit with a quotable punchline.
- **Weak spots (Gemini read):**
  - The UK/Gibraltar distance detour (51–58s).
  - A repeated "Spain borders Africa" beat (73–78s).
  - Tighten or cut both.
- **Pace:** visual change every ~2.1s (28/min); ~5 SFX/min; one quiet looped electronic bed; ~165 wpm.
- **Facts to verify before scripting** (their wording was loose):
  - Llívia's distance from the border (they say 2 km).
  - Pheasant Island's handover dates (Feb–Jul Spain, Aug–Jan France).
  - Andorra's population and area.
  - The Peñón de Vélez de la Gomera border length (they say 85 m).
  - Their transcript also mis-spells names (Llívia → "Libya", Ceuta → "Suda").
- Put sources in the description.

## Findings to apply (all 169 GeoGlobeTales videos)

### Topic

- **Remakes are allowed** (Shubham, 2026-11-09).
  - GeoGlobeTales remaking its *own* hits lost 83–94%, because it was the same audience.
  - BHUGOL remaking GeoGlobeTales topics worked: 6 of 8 beat BHUGOL's median of 897 views. Half of America 4.2×, Country Inside a Country 3.3×, Point Nemo 3.1×, Time Zones 2.2×, Russia–US 2.2×, Tree Wall 2.0×. UAE (0.1×) and the Chile walk (0.1×) flopped.
  - Use remakes now and then for a boost, with our own script and visuals.
- **Re-angles** (same question, new place) also work at GeoGlobeTales: Korea, 1.05M → 27.2M.
- **Topic type medians** (167 Shorts, × the median of their half-year cohort; regex-tagged, so treat as rough):

| Topic type | Median | Ran 2×+ |
|---|---|---|
| Record journey | 1.95× | 40% |
| Name confusion | 1.72× | 29% |
| Strange border / enclave | 1.56× | 43% |
| True size | 1.26× | 14% |
| Why is the shape like this | 1.25× | 38% |
| Why no X | 1.07× | 40% |
| History deal / conflict | 1.03× | 24% |
| Extreme place | 1.00× | 33% |
| Present-day news | 0.32× | 14% |

  - **Correction:** an earlier note said "present-day stakes beat pure history". This cut doesn't support it.
- **No home-country framing for BHUGOL.** GeoGlobeTales anchors on its US audience (39 of 95 long-running openings name the US, Americans, a US state or Canada). BHUGOL's audience is mixed (see above).

### Script: six beats

1. **Surprise (0–3s).** Challenge an assumption with a specific, checkable claim. Assumption-challenge openings ran 1.74×; other opening types about 1.0×.
2. **Scale anchor and first payoff (by ~9–12s).**
3. **Backstory.**
4. **Turning point / skit.**
5. **Map payoff.**
6. **Quotable close.**

- Use open loops between beats.
- One complete story, not a list of separate points.

### Skits

- GeoGlobeTales skits began Mar 2026. The first three ran 4.9×, 2.6× and 5.4×. The 19 dialogue videos averaged 1.26×, vs 1.02× without dialogue. Long skits underperformed.
- Keep skits to 2–4 lines, with a punchline viewers will quote back in comments.

### Visuals and audio

- A visual change every 2–3s (~27/min).
- Annotations must land on what the narration names.
- One quiet looped bed, plus pops and whooshes.
- GeoGlobeTales' narrator is AI (Gemini median 95% confidence), and viewers notice it.

### Ending

- Only ~1 in 8 GeoGlobeTales videos asks viewers to subscribe; most end on a punchline or stat that loops.

### Comments

- Most top comments are jokes riffing on a video line.
- Corrections draw huge likes ("you won't be arrested" — 93K).
- Locals and graphics praise follow.
- Write for a quotable line, and get the facts exactly right.

### Cover and title

- A frame from the video, one subject, 1–4 words, one visual joke.
- Two-part title template; the exact wording barely mattered.
- Hashtags are not a lever.

### Execution beats topic

- GeoFactGuy made the same US–Russia topic and got 4.8K views, vs 36.7M for GeoGlobeTales.

### Fact errors seen at GeoGlobeTales

- The Caspian swim was 32 days at sea, not 40.
- The "Giant Wall" title is sensational.

## How to judge the test

- Compare the English Short at 48h and 7 days with BhuGol EN's median (897 views) and its top 5. Also compare engaged views, average % viewed and comments per 1K views.
- Do the same for the Hindi Short against Bhugol Hindi.
- If it wins, propose skill edits to Shubham: remakes, six beats, skit length, ending, cover style. Do not edit without his OK.
