# Money Mirage ep01 v2: SPEC (preview = cold open + chapter 1, ~90 s)

GOAL:    The viewer feels "wait, then what IS my money?" and keeps watching, because one banknote's promise
         is shrinking in front of them (4.84 oz -> 2.86 oz -> a sliver).
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps. Long-form YouTube (16:9); Shorts recomposed 1080 x 1920 later.
TIME:    preview ~90 s x 30 = ~2,700 frames. Narrated: the voice is the clock. No beat grid (music is a bed).

STORYLINE (picked): "The Promise on the Note". Device: one object across eras (an engraved banknote carrying
         "I promise to pay the bearer") + a number that lands (ounces of gold that note could claim).
         Form: object-to-object chain: each shot ends on the thing that opens the next.
         Not built: "The Sunday" (hour-by-hour Camp David countdown with flashbacks) and
         "The Mirage" (a literal desert mirage of gold that recedes as we walk through eras).

LOOK:    Medium = a 1970s news magazine: evidence is printed, reconstructions are colour plates.
         - Archival photos/documents (real evidence): HyperFrames Two-Ink Editorial Print
           {contrast .08, highlights -.06, shadows .04, twoInkPrint 1, size .42}; same as thumbnail A.
         - Codex paintings (reconstructions): Film Memory {preset vintage-wash .6, vignette .12, grain .12}.
         - The carrier object: one invented engraved note, green ink #2F4A37 on #E6E9D6 paper, guilloche
           rosettes, engraved portrait (HyperFrames Engraving). Never a real currency design.
         - Ground: always a full-bleed image or the note itself. No empty navy frames.
         - Ink #F3EBDD, accent gold #E9B44C (hero numbers only), red #E8322A (one hand-drawn circle or
           stamp per scene, max).
         - Type: Inter only. Hero numbers Inter 900, 9-14% of frame height (100-150 px), tabular-nums.
           Captions Inter 800, 54 px, 3-5 words a group, one group at a time, 96 px from the bottom.
OBJECTS: the engraved note (reads as money without a label: paper texture, rosettes, serial, portrait oval);
         gold coins (Lydian trite photo, real); a balance scale (note vs gold) for the ounce numbers.
MOTION:  arrivals expo.out 0.6-0.9 s; camera moves power2.inOut; exits power3.in, 40% shorter.
         Camera push on plates max 1.00 -> 1.08 per shot. Numbers count up 1.2-1.6 s then hold dead still.
         Shots average 3-6 s with motion inside; something new every 2-4 s.
TRANSITIONS (3-5 kinds, each caused): push into note detail (zoom through), object becomes the world,
         whip on the scale swing, dip cut for the 1971 hard turn, blur swap on one stage.
SOUND:   music bed from the 8 YouTube Audio Library tracks (Keys To Unravel first), ~0.14 under voice,
         ducked + edge fades. SFX: real recordings only, ~1 per 8-10 s, each caused on screen
         (paper rustle on the note, coin clink on Lydia, stamp on 1933, low hit on 1971), 3-6 dB over bed,
         rotate takes. Mix -14 LUFS, true peak <= -1 dBTP.
VOICE:   Gemini TTS, no time-stretch, no pitch-shift. Only gaps trimmed (>0.6 s -> 0.45 s).
BANNED:  dark navy void with small floating elements; corner logo bug; chapter title cards; label lines /
         small caps captions; glow, particles, neon; everything fading + sliding up; three cards in a row;
         titles that keep moving after landing; code-synthesised SFX; CSS-filter grades on photos;
         the same plate more than twice in the film; any on-screen text other than captions + hero numbers.
QA:      frame 0 shows the wallet plate (not empty); the 3 ounce numbers readable at 360 px phone width;
         check --json craft warnings reviewed; snapshot --review sheets; audio measured (not heard).
