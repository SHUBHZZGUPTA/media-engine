# Example: Russia's time zones (3D, 40 s, 12 Nov 2026), code-drawn, no AI images

- **globe3()**: day/night Earth (Blue Marble day + VIIRS Black Marble night, sun direction per shot = real UTC time), Russia's 11 zones
  as a live mask (`art/zones.png`, value = (UTC offset - 1) x 20; built by `tools/prep_geo.py` from Natural Earth admin-1, Crimea/Sevastopol excluded,
  Sakha split by longitude), per-zone colour + alpha tracks, `mg` merges zone +4 -> +3 and +12 -> +11 (2010) and back (2014), Russia flag fill,
  Trans-Siberian route tube revealed by `prog` with a riding emoji, pins, cards pinned to lon/lat at fixed screen anchors (`cardpos`).
- **world3()**: flat satellite world map, France + territories fill (tricolour on the mainland), Russia tint, 13 island pins popping as the camera pans.
- **KM**: the shared map3 terrain (Kamchatka) for the protest beat.
- Characters drawn in code: an alarm clock (02:00 display) and France (Natural Earth outline + tricolour + face).
- Hindi build uses lang-specific beats (`'lang': 'hi'` + Devanagari `word`) so merge/restore land on हटा / वापस.
- Thumbnail: `tools/mkthumb.py <build> <out> <en|hi> [q|t]` injects a cover overlay into a copy of the build and snapshots t=2 (q = question words + clock, t = title words, no clock: the user's pick).
- Gotcha: background renders die when the cloud session restarts while waiting on the user; restart with `render.sh` and keep polling in the foreground.
