# Russia EN: subtitle/picture sync fix (30 Oct 2026)

**Bug:** the Ch2-11 part of the published video was rendered from plan time 1.4 s while its audio started at 0, so from
Chapter 2 (5:18) to the end the pictures and subtitles ran 1.4 s ahead of the narration, and the last 1.4 s of audio was cut.

**Fix (minimal):** pictures are frame-for-frame the published ones (hook+Ch1 rebuilt from the identical published plan
`pilot/spec_en_3d7.json`; Ch2-11 rendered from the unmodified `full/spec_full.json` starting at its original 1.4 s). Only the
Ch2-11 audio moves 1.4 s earlier: its first 1.4 s (silent lead-in under the empty frames before the Chapter 2 card) is
dropped, so narration, subtitles and pictures line up and the ending's audio is complete. Length 35:10.07 (same as published),
chapter timestamps unchanged.

**QC:** `qc_report.md` (engine/qc_video.py) - ALL PASS: length, 58 planned cuts at their planned times (median +0.02 s),
narration present at offset 0 in all 201 speech windows, subtitles within 0.1 s of speech in every minute, ending complete.
Audio join at 5:18.13 click-free.
