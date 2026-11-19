# BHUGOL score library

Background music for BHUGOL long-form videos, sorted by mood. Every track is free to use on monetized YouTube videos **as long as its credit line is in the description** (`credit` field in `library.json`).

- Audio files: `outputs/fetch/bhugol-music/` + `outputs/fetch/bhugol-music2/` (Kevin MacLeod, CC BY 4.0, fetched by `jobs/fetch/bhugol-music.json`) and `music-library/ytal/` (YouTube Audio Library, "attribution not required").
- **YouTube Audio Library tracks are licensed for YouTube only.** Don't use them in anything that is also posted to Instagram/Reels or other platforms; use the Kevin MacLeod tracks there.
- Catalogue index (all ~1,440 Kevin MacLeod tracks with feel/bpm/instruments): `outputs/fetch/bhugol-music-index/pieces.json`. Use it to add more tracks.
- Game videos (GTA style) keep their synth score in `outputs/fetch/gta6-music/`.

## Moods
| Mood | Use for |
|---|---|
| wonder | scenic aerials, beautiful places, "little Paris" type facts |
| quirky | funny or absurd facts, cheeky hooks |
| mystery | caves, legends, strange history, "nobody knows" facts |
| epic | the big reveal, dictators, record-breaking scale, #1 fact |
| outro | ending, comments question, subscribe line |

## Rules
1. Pick one track per chapter by that chapter's mood; switch at the chapter card (mixdown crossfades).
2. Don't reuse the same track in back-to-back videos on the channel.
3. Paste every used track's `credit` line into the description (YouTube Audio Library tracks have `credit: null`: no credit needed).
4. If YouTube shows a Content ID claim on a Kevin MacLeod track, it is a false claim: keep the credit in the description and dispute it (incompetech.com/music/royalty-free/youtube-contentid.html).
