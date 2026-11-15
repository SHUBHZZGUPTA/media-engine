# Example: "5 Countries, 1 Flag?" Nordic what-if Short (2.5D, 15 Nov 2026), GeohistoryShort-style test

Built to test the GeohistoryShort (@GeohistoryShort) craft: ONE flat satellite map (orthographic BlueMarble relief+bathymetry,
`prep.py`), ONE continuous camera with heavy ease-out glides + CSS perspective tilt (no cuts), a literal visual for every
line (flag fills, eraser, gold merge with extrusion, cards, emoji props, countryball), dense object-matched SFX, vote ending,
seamless loop (cover = frame 0 = last frame). Voice: Gemini 3.8 Sadaltager upbeat; `retime.py` caps pauses + tempo 1.05
and maps Whisper words (incl. digits) onto TTS tokens. `mix.py` wraps the music bed and ducking around the seam (RMS jump <1 dB).
Render: 71 s took 60 min on 2 CPUs (SVG flag clip-paths at high zoom are the slow part, ~0.2 fps); next time bake the flag
fills to raster layers. Retention QA: PASS (90% moving, one change every 2.2 s, longest gap 4.8 s).
