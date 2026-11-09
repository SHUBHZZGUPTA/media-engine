# GeoGlobeTales research (used by the bhugol-geo skill)

| File | What it is |
|---|---|
| `full-research.md` | The complete research doc, read in full in Step 0. The corrections block at the top overrides the body. |
| `../ggt-findings.md` | Brief for test Short #1: Spain's Strangest Borders |
| `rank_topics.py` | Step 0: our analytics vs the GeoGlobeTales data. Prints the baseline, audience, topic types and ranked remake candidates. |
| `inv.json` | All 169 GeoGlobeTales videos: id, title, secs, date, views, likes, comments, tags, dubs, format, age, views/day |
| `invS.json` | The 167 Shorts, plus `rel`: views ÷ the median of the same half-year cohort |
| `tx/*.json` | Transcripts plus the top 12 comments, 74 newest videos |
| `openings_all.json` | First line of every transcript |
| `gem/parsed.json` | Parsed Gemini audio-visual metrics per video |
| `tests.md` | Log of BHUGOL tests run with this playbook, and their results |
| `../../../outputs/watch/ggt-<id>/full.md` | Gemini picture-and-sound teardown of each video (169/169). Read the one for any topic you remake. |
