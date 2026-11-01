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
