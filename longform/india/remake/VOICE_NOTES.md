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
Process note (corrected 10 Nov): tts_quota.py check DOES exit 1 on DON'T PUSH; piping it through `tail` hid that. Run it without a pipe (or with set -o pipefail) and push only after "OK to push".

## Matching rule for the final voice (agreed 9 Nov)
Kept 3.8 takes, narrator vs old ref 119.1 Hz: p01 -0.3, p02 -0.4, p05 -1.2, p06 -1.0, p07 -1.1, p09 +0.3, p12 -0.3, p18 -1.2 st (all lines clean;
p02 may have dropped "Jar" in "Fish. Jar. Unicorn."). 3.8 reference = their median, 114.8 Hz. Every take: same model, Sadaltager + Puck, one identical base direction.
New takes must: narrator within ±1.0 st of 114.8 Hz; every seam (last ~30 s vs next take's first ~30 s, all takes in script order) within 1.0 st;
speaking rate within ±8%; loudness within ±1.5 dB after normalising; timbre (voicecheck.py) inside the kept takes' range. Fail = retake (Wed), never pitch-shift.
Shubham also gets 3 clips straddling old/new seams before the render.

## 9 Nov (later): Shubham's call: re-voice the whole video in fewer, longer 3.8 takes
14 takes of up to ~690 words (4.5-5 min, inside the stable zone of the long-take test) instead of 8 kept + 10 new (18 takes):
13 seams instead of 17. f1 = p01-p10 (Tue 10 Nov), f2 = p11-p14 (Wed 11 Nov). The 8 short 3.8 takes (t38 + e1) stay as a fallback.
Matching rule unchanged (narrator within ±1.0 st of 114.8 Hz, every seam within 1.0 st, rate ±8%, loudness ±1.5 dB, timbre in range).
10 Nov: another project (bhugol-desert) reserved 6 of today's 3.8 requests, so f1 = p01-p04 today (4) and f2 = p05-p14 Wed 11 Nov (10, reserved).

## 10 Nov: batch f1 (p01-p04) checked
Lines: 32/32, 21/21, 23/23, 14/15 (the 1 flag = whisper merging two sentences; all words heard). matchcheck.py:
p01 +0.4 st, p02 -0.3, p03 -0.9, p04 +0.7 (all within ±1.0 of 114.8 Hz); rate -4% to +1%; loudness within 0.5 dB; timbre 6.8-9.9 (all PASS).
Seams: p01->p02 -0.8 st PASS; p02->p03 +2.3 st and p03->p04 +2.2 st FAIL by the rule. All three seams sit on chapter breaks;
the failing ones end on a quiet low cliffhanger (99 / 102 Hz) and the next take starts on the reference (113 / 116 Hz). Seam clips sent to Shubham to judge by ear.

## 10-11 Nov: "white noise" in the seam clips = clip-building error, not the voice
The first p02->p03 / p03->p04 seam clips had a constant hiss and rumble at about -47 dBFS (plus a DC offset); the takes themselves sit at -73 to -77 dBFS in pauses.
Rebuilt straight from the takes with ffmpeg (sseof tail + 1.2 s anullsrc + head, libmp3lame 192k): -73 / -77 dBFS, no hiss. 3.8's floor is ~15 dB above 3.1's, but it can't be heard in the raw takes, so no denoise step (a gate risks clipping word endings).
Rule from now on: measure the pause noise floor (quietest 5% of 30 ms frames) on every review clip and on the final mix; above -65 dBFS = fix before sending.

## 11 Nov: batch f2 (p05-p13 recorded; p14 got a 429 after 9 requests, moved to Thu 12 Nov, 2 reserved)
Lines: all clean (flags = whisper spellings: "Mahmoud", "ma 'am", merged sentences). Pause noise floor on review clips -72 to -76 dBFS.
matchcheck narrator vs 114.8 Hz: p05 +2.0 FAIL, p06 -1.8 FAIL, p07 0.0, p08 +0.1, p09 -1.2 FAIL, p10 0.0, p11 +0.1, p12 -1.8 FAIL, p13 -0.2. Rate -6% to +2%, loudness within 1 dB (all pass).
Seams (all on chapter breaks): p04->p05 +2.2, p05->p06 -2.7, p06->p07 +3.4, p07->p08 +1.2, p08->p09 +1.3, p09->p10 +2.5, p10->p11 +0.2, p11->p12 -2.3, p12->p13 0.0.
Takes are steady inside themselves; the spread is take to take (3.8 still lands each take somewhere in about +-2 st). Clips of the 4 biggest seams sent to Shubham; retakes wait on his call.

## 12 Nov: retakes r1 (p05, p06, p12 retakes + p14 first take), all lines clean
Narrator vs 114.8 Hz: p05 +1.7 FAIL (was +2.0), p06 +0.3 PASS (was -1.8), p12 -0.9 PASS (was -1.8), p14 +1.3 FAIL.
Seams: p04->p05 +0.2, p05->p06 -1.2, p06->p07 -0.5, p12->p13 -0.1, p13->p14 0.0. p11->p12 -2.9: p12 opens on the hushed 1893 train scene;
both p12 takes start low (100 / 97 Hz) on that same text, so it is the line, not chance. Kept r1 p06 + r1 p12.
13 Nov (4 reserved): r2 = p05, p09, p14 (pending/in-rm-en-r2.json) + 1 spare.
