# India full: narrator check log

How it's checked: narrator lines only, cut using lines_en.json `who == Narrator`. Reference = the pilot's Ch1 narrator lines (the voice Ch2 continues from).
Tools: `longform/engine/voicecheck.py` plus a robust pitch measure (pyin limited to 70–200 Hz, which avoids octave errors).

| take | covers | robust median Hz (ref Ch1 117.7) | voicecheck | decision |
|---|---|---|---|---|
| d1 p01 | Ch2 part 1 | 115.0 | -0.6 st, tone ok, timbre 16.6 | keep |
| d1 p02 | Ch2 part 2 | 121.9 | -1.0 st, tone ok, timbre 17.3 | keep |
| d1 p04 | Ch3 part 2 (Nanda / Alexander) | 139.2 (+2.9 st) | +4.7 st | retake p04r (in d4); fallback p04pc (-2.5 st, formant kept, timbre 13.7) |

Note: timbre between the pilot's own hook and its Ch1 measures 25.8, so a timbre of 14–18 is within the range the pilot already uses. Pitch is the deciding check.

## Take length: stay at <= ~330 words (decided 1 Nov, after checking Russia)
A plan for 2-chapter takes (~900-1,000 words) was dropped. Russia's long takes came back full length at a normal pace, but their
tails degraded and had to be re-voiced (ru-full-en-fix1..3):

| Russia take | words | degraded from |
|---|---|---|
| a / ch2 | 412 | word 354 (86%) |
| b / ch7 | 509 | word 408 (80%) |
| b / ch8 | 629 | words 471 and 523 (75%, 83%) |

So the break-down starts around 350-520 words. Duration / words-per-minute checks do NOT catch it: only the transcript vs script does.
Every take is checked by transcript, line by line, not only by length.

## Voice schedule (longform key, 10 requests/day)
| job | items | covers |
|---|---|---|
| in-full-en-d1 (done) | p01, p02, p04 | Ch2, Ch3 part 2 (p04 to retake) |
| in-full-en-d2 | p03, p05, p06, p07-p13 | Ch3 part 1 to Ch8 part 1 |
| in-full-en-d3 | p14-p23 | Ch8 part 2 to Ch13 part 1 |
| in-full-en-d4 | p24, p25, p04r | Ch13 part 2 + ending, Ch3 part 2 retake |

## Day 2 (2 Nov): 10/10 takes back full length
Line check (`takecheck.py`): 7 stage tags read aloud (cut automatically by assemble_voice.py); real problems:

| global line | take | problem | fix |
|---|---|---|---|
| 73 | d2 p06, last line (Ch4 end) | "came new arrivals" heard as "can be a virus" (late-take garble) | re-voice in in-full-en-d1-fix1 |
| 106-110 | d2 p09 | "according to later chronicles, raiders led by Bakhtiyar" skipped | re-voice 106-110 (from the traveller line before to the one after) |
| 119 | d2 p10 | whispered traveller line ~22 dB too quiet | `--gain=119:18` in assembly, no retake |
| 130-131 | d2 p10, last 2 lines (Ch6 end) | "lost his homeland more than once. He was" skipped (late-take) | re-voice in fix1 |

Narrator pitch per take (robust median of narrator lines vs pilot Ch1 = 119.1 Hz):

| take | lines | Hz | st | |
|---|---|---|---|---|
| d1 p01 | 0-13 | 115.0 | -0.6 | ok |
| d1 p02 | 14-20 | 121.9 | +0.4 | ok |
| d2 p03 | 21-30 | 129.1 | +1.4 | ok |
| d1 p04 | 31-44 | 136.8 | +2.4 | out (retake p04r in d4) |
| d2 p05 | 45-58 | 128.4 | +1.3 | ok |
| d2 p06 | 59-73 | 135.2 | +2.2 | out |
| d2 p07 | 74-90 | 142.4 | +3.1 | out |
| d2 p08 | 91-99 | 153.6 | +4.4 | out |
| d2 p09 | 100-111 | 116.4 | -0.4 | ok |
| d2 p10 | 112-131 | 136.0 | +2.3 | out |
| d2 p11 | 132-144 | 109.8 | -1.4 | ok |
| d2 p12 | 145-157 | 125.4 | +0.9 | ok |
| d2 p13 | 158-174 | 132.1 | +1.8 | out |

Biggest jumps at take switches: p08 -> p09 (Ch6 card) -4.7 st, p09 -> p10 (mid Ch6, after a character line) +2.8 st, p10 -> p11 (Ch7 card) -3.7 st.
3D clips rendered from the provisional voice (timings final): G_vedic, G_ganga, G_magadha, G_maurya, G_chakra, G_road, G_mughal1605.

## Decision 3 Nov: Gemini stays; drifted takes are re-recorded, never pitch-shifted
Shubham found the pitch-levelled (B) switch clips robotic and the clean p09 take natural. Rule: a take whose narrator median is
more than ~1.5 st from the pilot Ch1 narrator gets re-recorded. Wed (d4): p07r, p08r, p10r with p24, p25, p04r + fix1 = 7 requests.
p06 (+2.2) and p13 (+1.8) next if the Wed re-takes leave quota or time.

## Day 3 (3 Nov): 10/10 takes full length
Line check: 4 stage tags read aloud (auto-cut). Real problems, added to fix1 (Wed):
| global | take | problem |
|---|---|---|
| 251 | d3 p19 | Gandhi's line replaced by its stage tag ("Holding up a pinch of salt?"); fix line uses [calmly] |
| 291 | d3 p22, last line (Ch12 end) | "The Golden Bird was free." skipped (late-take) |

Narrator pitch (vs 119.1 Hz): p14 +2.9 OUT, p15 +0.9, p16 +0.7, p17 +0.3, p18 +2.8 OUT, p19 +3.1 OUT, p20 -0.2, p21 -0.3, p22 +0.5, p23 +0.6.
Wed d4 (10 requests, full day): p24, p25, p04r, p07r, p08r, p10r, p14r, p18r, p19r + fix1 job (1 request).
Thu if needed: p06 (+2.2), p13 (+1.8), and any re-take that drifts again.

## Day 4 (4 Nov): 9 takes + fix1, all lines clean
Narrator pitch: p24 +1.8, p25 +3.1, p04r +1.9, p07r +3.9 (worse than p07 +3.1), p08r +3.1 (better than +4.4), p10r +0.2, p14r +0.8, p18r -0.6, p19r +2.0.
Golden Age material (Ch5) comes out high on every take (energetic delivery).
Final pick (voice_parts.txt): best take per part: p04r, p07 (orig), p08r, p10r, p14r, p18r, p19r, rest original.
fix1 spliced at 73, 106-110, 291 only (p10r/p19r already say 130, 131, 251 right; those map entries set negative = unused).
Line 119 (whisper) +7 dB. Bug fixed: tag cutting removed the real word "Then" (tag word "the"); short tag words now only continue a cut.
Still above 1.5 st: p04r, p06, p07, p08r, p13, p19r, p24, p25 -> Thu re-takes if Shubham hears a change in the review copy.
