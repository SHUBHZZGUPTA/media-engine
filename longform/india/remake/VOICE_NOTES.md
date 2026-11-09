# India remake: voice log

Script: `script_en.md` (playbook v1.1). 26 takes (`ttsjob.py ... 330 --pack`), Narrator Sadaltager + Chars Puck, gemini-3.1-flash-tts-preview, longform key.
Checks per take: `full/takecheck.py` (line by line vs script) and narrator-only pitch vs the pilot Ch1 narrator (119.1 Hz); a take more than 1.5 st off is re-recorded, never pitch-shifted.

## Day 1 (9 Nov IST, PT day 2026-11-08): p01-p10, all full length

| take | covers | narrator pitch | lines | decision |
|---|---|---|---|---|
| p01 | hook | 136.0 Hz, +2.3 st | 15/15 clean | retake |
| p02 | ch1 part 1 | 134.5 Hz, +2.1 st | 13/13 ("4,500" = number form) | retake |
| p03 | ch1 part 2 | +0.5 st | 12/12 | keep |
| p04 | ch1 end + ch2 start | -1.3 st | 13/13 | keep |
| p05 | ch2 | -0.5 st | 17/17 | keep |
| p06 | ch2 end | -0.2 st | 6/6 | keep |
| p07 | ch3 | -0.7 st | 15/15 (Piyadasi heard "Pia dasi"; "Keep that wheel in mind" heard "Psst, that wheel in mind" at 115.4 s, "for long" heard "for law" at 125.3 s) | keep; re-voice the two ch4 lines in a fix job |
| p08 | ch3 end / ch4 | 132.1 Hz, +1.8 st | 10/10 | retake if quota allows |
| p09 | ch4 end / ch5 | 137.6 Hz, +2.5 st | 8/8 (pi digits = number form) | retake |
| p10 | ch5 | +0.6 st | 15/15 | keep |

## Plan
- PT 2026-11-09 (from 13:30 IST 9 Nov): in-rm-en-d2 = p11-p20.
- PT 2026-11-10: in-rm-en-d3 = p21-p26 + retakes p01r, p02r, p09r + fix job (2 ch4 lines) = 10.
- PT 2026-11-11 if needed: p08r and any day-2/3 take that drifts.

## Day 2 (9 Nov IST, PT day 2026-11-09): p11-p20, all full length, all lines clean
Pronunciation hints in the direction from this day on. Stage tags read aloud in p11 and p20 (auto-cut). "Ooh, that's the army" (p16) and "Ma 'am" (p18) are transcription spellings, fine.

| take | narrator pitch | decision |
|---|---|---|
| p11 | +0.4 st | keep |
| p12 | +1.9 st | retake |
| p13 | -1.6 st | retake if quota allows (borderline) |
| p14 | -1.9 st | retake |
| p15 | +0.5 st | keep |
| p16 | +0.3 st | keep |
| p17 | +0.5 st | keep |
| p18 | +2.6 st | retake |
| p19 | +0.7 st | keep |
| p20 | +0.5 st | keep |

Retake queue: Tue (PT 11-10) = p21-p26 + p01r, p02r, p09r + fix_a (full). Wed (PT 11-11) = p18r, p12r, p14r, p08r, p13r + any day-3 drift (6 reserved).

## 9 Nov: switched to gemini-3.8-flash-tts (Shubham approved after an A/B listen)
Test (in-rm-en-t38, same prebuilt Sadaltager + Puck, same script): narrator pitch p01 -0.3, p05 -1.2, p09 +0.3, p12 -0.3, p18 -1.2 st
(3.1 on the same takes: +2.3, -0.5, +2.5, +1.9, +2.6). Spread 1.5 st vs 3.1 st; all lines clean; [tags] go in speech_metadata.style
and are no longer read aloud; ~5-10% faster. The whole video is re-voiced on 3.8 (no mixing models in one video).
Takes: p01, p05, p09, p12, p18 = in-rm-en-t38. e1 (9 Nov) p02 p03 p04 p06 p07 · e2 (10 Nov) p08 p10 p11 p13-p17 p19 p20 · e3 (11 Nov) p21-p26.
3.8 free-tier daily limit not published (AI Studio shows it per project); planned as 10/day. 3.1 reservations for 10-11 Nov released.

## 9 Nov: how long can a 3.8 take be? (long-take test)
3.8 free tier confirmed at 10 requests/day (429 says so). One long take got through: in-rm-en-long p04, 1,337 words, 9 min 28 s:
57/59 lines clean (2 known spelling quirks), no tail breakdown (3.1 broke at 350-520 words).
Narrator pitch by quarter: -1.8, -2.0, -1.1, +0.1 st, i.e. steady for ~4.7 min, then a slow ~2 st rise. A long take would jump ~2 st at the next seam.
Decision: 3.8 takes up to ~650 words (~4-5 min). Hard ceiling anyway: 16,384 output tokens = ~10.9 min per request.
Plan: keep the 8 short 3.8 takes (p01 p02 p05 p06 p07 p09 p12 p18); fill the gaps with 10 takes of 210-620 words = job in-rm-en-g (10 Nov).
Process note: tts_quota.py check prints DON'T PUSH with exit code 0; gate pushes on `grep -q "OK to push"`, never on the exit code.
