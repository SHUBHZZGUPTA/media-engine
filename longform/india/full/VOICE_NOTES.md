# India full: narrator check log

How it's checked: narrator lines only, cut using lines_en.json `who == Narrator`. Reference = the pilot's Ch1 narrator lines (the voice Ch2 continues from).
Tools: `longform/engine/voicecheck.py` plus a robust pitch measure (pyin limited to 70–200 Hz, which avoids octave errors).

| take | covers | robust median Hz (ref Ch1 117.7) | voicecheck | decision |
|---|---|---|---|---|
| d1 p01 | Ch2 part 1 | 115.0 | -0.6 st, tone ok, timbre 16.6 | keep |
| d1 p02 | Ch2 part 2 | 121.9 | -1.0 st, tone ok, timbre 17.3 | keep |
| d1 p04 | Ch3 part 2 (Nanda / Alexander) | 139.2 (+2.9 st) | +4.7 st | retake p04r on day 4; fallback p04pc (-2.5 st, formant kept, timbre 13.7) |

Note: timbre between the pilot's own hook and its Ch1 measures 25.8, so a timbre of 14–18 is within the range the pilot already uses. Pitch is the deciding check.
