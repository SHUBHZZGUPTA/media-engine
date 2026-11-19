# BHUGOL music library: moved to branch `music`

The audio files live on the `music` branch (89 tracks: YouTube Audio Library + Kevin MacLeod), so the GitHub Actions jobs, which check out `main`, don't download ~670 MB of MP3s on every run.

Get it: `git clone --depth 1 --branch music https://github.com/SHUBHZZGUPTA/media-engine.git music`

`library.json` here is a copy of the branch's index; its `file` paths are relative to the `music` branch root. See the branch README for licences, credit rules and the scoring style.
