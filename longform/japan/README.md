# BHUGOL long-form: "6 Japan Facts Nobody Believes" (14 Nov 2026)

Approved by Shubham in chat (session_01Qv21gGVWzC8w8naopAEo7L). Approval page: https://claude.ai/artifact/MQLyfuDroqGbBVzgmxQk3P

| Decision | Value |
|---|---|
| Format | Long-form 16:9 1920x1080, ~3:45, 3D style (BHUGOL 3D pipeline, Thar-style design), render on Kaggle GPU |
| Script | `script.json` (54 lines, EN + HI). Lines 1-8 = hook "I bet you $100 you won't believe these are real." Facts spoken "Fact one … Fact six" |
| Ending | Seamless loop: last line "…So, how many did you believe? Be honest. Because" -> line 1 |
| Title | `6 Japan Facts Nobody Believes 🇯🇵` · thumbnail headline `6 JAPAN FACTS THAT SOUND FAKE` (yellow box on FAKE); show thumbnail before burn-in |
| EN voice | Higgsfield Eleven v4, Holden, stability 0.3, emotion tags (`narration_en_tagged.txt`). Raw: outputs/fetch/japan-en-holden-full/ (240.7 s); WAV outputs/tts/japan-en-holden/; words outputs/align/japan-en-holden/ |
| HI voice | Gemini 3.8 Sadaltager, CHAPTER BLOCKS (8 blocks, never one block per line), direction in `gemini_direction.txt` adapted to Hindi; long-form key |
| Captions | EN video English; HI video Devanagari karaoke; on-screen elements stay English in HI |
| Skits | none |
| Visual devices | red pen + FIXED n/6 tracker, FACT n chapter cards, map pins; shot plan per line in `approval_page_build.py` (L entries) |
