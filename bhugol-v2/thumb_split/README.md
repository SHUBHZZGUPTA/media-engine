# Split thumbnail (BHUGOL default, 24 Oct 2026)
`python3 split.py <config.json>` -> `split_<lang>_v.jpg` (1080x1920), `split_<lang>_w.jpg` (1280x720) and
`feed_split_<lang>_*.jpg` (140 px feed tests) for every language in the labels. Needs the kit fonts
(`/home/claude/bhugol-kit`), `playwright-core` in `$NODE_WORK` (default `/home/claude/work`) and `HYPERFRAMES_BROWSER_PATH`.
Example config: `gulf.json` (USA cold | Europe warm). Field notes are at the top of `split.py`.
