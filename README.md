# BHUGOL music library (branch `music`)

Background music for BHUGOL long-form videos. It lives on its own branch so the GitHub Actions jobs, which check out `main`, don't download it.

Get it: `git clone --depth 1 --branch music https://github.com/SHUBHZZGUPTA/media-engine.git music` (or `git fetch origin music && git worktree add ../music music`).

- `library.json`: every track with title, artist, mood, length, licence and the credit line (`credit: null` = no credit needed).
- `ytal/`: YouTube Audio Library, standard licence, no credit needed. **YouTube only**: don't use these in anything also posted to Instagram or other platforms.
- `kevin-macleod/`: Kevin MacLeod (incompetech.com), CC BY 4.0. The credit line from `library.json` **must** go in the description. `catalog_pieces.json` indexes his full ~1,440-track catalogue.

## Style (Shubham, 20 Nov 2026)
- Few long cues, each running across 2–3 facts. Change only on a chapter card.
- Curious pulse for the hook, dark drones for ocean/volcano facts, an epic build for the #1 fact.
- No bright, festive, comedic or busy-pulse beds.
