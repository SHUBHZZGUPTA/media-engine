# India remake: render QC (15 Nov 2026)

Final: render/india_remake_en.mp4 (not in git), 47:30, 1920x1080 30 fps, 932 MB, film-fade grade in one encode (COMPOSE_VF).

| Check | Result |
|---|---|
| Sync: subtitles vs real speech (whisper small.en on the finished soundtrack, 4,774 words) | median -0.01 s, 95% within 0.17 s, flat in every 6-min block (no drift); 91 scattered words >0.5 s (whisper word-boundary noise) |
| Loudness | -15.4 LUFS integrated, LRA 3.5 LU |
| Voice noise floor (pauses) | takes -73 to -77 dBFS (rule: fail above -65) |
| Frames every 10 s (285) | render 1 failed: clipped bubbles/labels, missing arrow glyphs, tall pictures cropped, empty ending strips, end screen pointing at the private Russia video, graphic famine images. All fixed; render 2 clean (edge "clips" on the sheet were mid-transition frames, checked settled) |
| Layer bounds (472 shots) | 0 cards over the top edge, 0 layers off-frame |
| Graphic imagery | 1943 famine photo and 1770 famine engraving replaced by text boards |
| Known, accepted for this video | set art is 3:2 cropped to 16:9 (~8% top/bottom of backgrounds); Muhammad of Ghor has a name card (no real portrait exists) |
