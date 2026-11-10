Here is an art-direction breakdown of the motion graphics and visual design in **PBS Eons: *When the Sahara Was Green***.

---

### 1. ON-SCREEN TEXT LAYOUT

| Text Type | Screen Position & Size | Font Style & Colour | Background / Treatment | Motion & Duration | Words / Density & Anti-Clutter Rules |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Main Series Bumper** (01:42) | Dead centre; ~18% frame height | Bold geometric sans-serif; pure white (`#FFFFFF`) | None; overlaid directly onto painted Cretaceous landscape artwork | Smooth scale-up from 90% to 100% with a 12-frame soft cross-dissolve; holds ~2.0s | Exactly 1 word ("Eons"). High impact, zero clutter. |
| **Topic Banners / Eras** (02:08, 06:46) | Horizontal centre-strip; ~12% frame height | Heavy condensed sans-serif, all-caps; pure white (`#FFFFFF`) | Mint/sage-green solid banner (`#46B876`) flanked by off-white/cream border caps | Expands horizontally outward from center line (0.3s ease-out), stays ~3.5s, collapses or cuts to host | Max 3–4 words ("AFRICAN HUMID PERIOD", "QUATERNARY PERIOD"). No secondary body copy. |
| **Map Feature Labels** (00:14, 04:45) | Anchored to regions / pins; ~3–4% frame height | Bold grotesque/gothic sans-serif; dark grey/black (`#1F1F1F`) or dark red (`#B22222`) | None (flat on vector map) or placed on a white/cream tag card with subtle drop shadow | Fade-in (8–10 frames) + subtle position nudge (5px upward). Stays 4–6s | Max 2–3 words per label ("SAHARA DESERT", "TÉNÉRÉ DESERT"). Clear hierarchy: large bold all-caps for macro regions; smaller regular tracking for secondary countries. |
| **Floating Host Insets & Sidecards** (00:46, 02:20, 02:46, 03:28, 05:08) | Upper-right / mid-right screen (host stands left-of-centre); card is ~30% frame width, ~25% frame height | Bold gothic sans-serif; white text (`#FFFFFF`) on dark pills/headers | Crisp white border (2–3px), charcoal dark pill backing (`#1A1A1A`) or pure white polaroid-style card with soft ambient drop-shadow (`rgba(0,0,0,0.25)`) | Slides in from screen-right with 15% overshoot bounce (0.4s); holds 4–7s; slides back off-screen right | Header: 2–3 words ("SAHARAN DUST FLUX", "AFRICAN MONSOON"). Image dominates 80% of card interior. |
| **Linguistic Data Table** (05:58) | Floating card, mid-right; ~35% frame width, ~45% frame height | Medium condensed sans-serif; header white on deep blue (`#2C4D8A`), body text dark slate (`#222222`) | White card, dark blue header bar, alternating grey zebra striping on table rows | Pop-in scale (0.2s) accompanied by an illustrative cut-out graphic of a hippo; holds 6.5s | 5 rows, 2 columns ("Language" vs "Attestation"). Body copy kept strictly tabular with uniform tab stops. |
| **Scientific Attribution / Citations** (00:42, 01:26, 02:14, 02:26, 04:54, 05:58) | Bottom-left or bottom-right corner; tiny (~1.8–2.2% frame height) | Monospaced or clean condensed sans-serif; all-caps; muted charcoal (`#4A4A4A`) or light grey (`#A0A0A0`) | None; sits flush in margin padding (~40px from edge) | 10-frame cross-dissolve with the graphic element; holds duration of the plate | Format: `BASED ON INFORMATION FROM AUTHOR ET AL. (YEAR)` or `IMAGE CREDIT: [NAME]`. Kept strictly monochromatic to avoid distracting from core visuals. |

**Anti-Clutter System:**
* *Rule of Single Focus:* PBS Eons never displays competing text blocks. If a map is on screen, country text is low-contrast pastel while the active label pops in high-contrast black/red.
* *Stacking:* Stacking only occurs inside dedicated structured modules (e.g., the linguistic table at 05:58 with clear grid gutters, or graph titles centered directly over the plot area).

---

### 2. TIME / ERA INDICATORS

The video tracks deep geological time using a specialized timeline bar:

```
[ 20 KYA ] ─── [░░░░░░░ ACTIVE ERA ░░░░░░░] ─────────── [ PRESENT DAY ]
```

* **Position & Anatomy (02:00, 05:40, 06:47):** Sits horizontally in the middle third of the frame across a charcoal dotted/halftone background.
* **Bar Design:** A clean off-white horizontal bar with fixed bounds: **"20 KYA"** on the far-left terminal, **"PRESENT DAY"** on the far-right terminal (bold sans-serif, all-caps, ~3% frame height).
* **Time Slice Highlighting:** 
  * At 02:02, as the narrator introduces the 15,000–5,000 year window, a segment from the left-center sweeps out in bright mint green (`#52D689`).
  * The green block snaps outward using an ease-in-out wipe, immediately expanding vertically into a full banner titled **"AFRICAN HUMID PERIOD"** (02:08).
* **Voice-Graphic Sync:** The highlight animation triggers precisely on the narrator’s voice ("*...starting somewhere between 15,000 and 11,000 years ago, and ending 5,000 years ago*"). 
* **Era Reset (06:50):** When returning to macro time, the bar transitions to **"QUATERNARY PERIOD"** anchored from **"2.5 MYA"** to **"PRESENT DAY"**, compressing the green slice down to a micro sliver on the far right to communicate human-scale insignificance against deep time.

---

### 3. MAPS & GEOGRAPHIC VISUALIZATIONS

The production alternates between two core cartographic languages:

#### A. The Editorial/Parchment Vector Map (00:14, 00:42, 02:14, 04:45, 05:10)
* **Canvas Style:** Antique textured paper/parchment base (`#E8DFC8`) with faint map grain, layered with flat vector continental silhouettes.
* **Color Palette:**
  * Arid Sahara: Warm ochre/terracotta orange (`#E08738`).
  * Sahel / Savanna: Sand/khaki yellow (`#DFB76C`).
  * Sub-Saharan Africa: Muted olive green (`#85A947`).
  * Water / Oceans: Soft powdery slate-blue (`#97BEE3`).
  * Highlight swaths: Vibrant crimson red (`#E63946`) with 1px dark stroke to denote rock-art distribution zones (00:42).
* **Camera Movement:** Subtle continuous push-ins (100% to 108% scale over 6 seconds) combined with slow diagonal pans along river paths.

#### B. The Satellite Eco-Transformation Sequence (01:36, 03:32–03:42, 04:17, 07:28)
* **Base Plate:** High-resolution photorealistic satellite mosaic (Blue Marble style).
* **Water Animation:** 
  * Inland drainage basins (such as Mega-Lake Chad, 04:17) and river systems (Nile, Niger, ancient Saharan paleorivers) grow outward via animated mask reveals (stroke-write animations in deep cobalt blue `#1D3557` with soft cyan outer glows `#48CAE4`).
* **Greening Sweep (03:32):** An organic, feathered horizontal matte sweeps from south (Equator) to north (Mediterranean). The arid tan sands morph into lush forest and savanna greens (`#2D6A4F` to `#52B788`) using an animated noise mask.
* **Keeping Long Map Holds Dynamic:**
  1. *Multi-layer particle dust:* Overlaying NASA wind vectors and atmospheric swirl simulations (03:18).
  2. *Topographic bathymetry outlines:* Elevation contours rendered with colored altitude ramps (blue to orange, 04:10).

---

### 4. NUMBERS, CHARTS, AND STATS

The video avoids raw floating floating numbers; every metric is contextualized inside rigorous data visualisations:

```
 DUST FLUX (G/CM²/KA)
 1.0 ┤
 0.8 ┤        /\
 0.6 ┤   _/\_/  \
 0.4 ┤  /        \________
 0.2 ┤ /         [ HUMID ]
 0.0 └───┴────┴────┴────┴────
     0   5   10   15   20  AGE (KA)
```

#### Line Graphs (Dust Flux: 02:34, 06:18)
* **Frame Integration:** Sits centered against a dark charcoal-black textured canvas (`#141414`).
* **Typography & Axis:** Axis lines are 2px solid black; tick numbers and labels ("AGE (KA)", "DUST FLUX") are set in bold condensed sans-serif, sized at ~2.5% frame height.
* **Data Animation:** 
  * The data line is a bold 6px goldenrod-yellow vector path (`#E9A03F`).
  * Animated with a linear path-trim/stroke-draw effect from past (right, 22 ka) toward present (left, 4 ka), taking ~2.5s.
  * A semi-transparent mint-green vertical band (`rgba(82, 214, 137, 0.4)`) wipes on over the 11 ka–5 ka bracket to visually highlight the "Humid Period" trough.

#### Comparative Solar Cycles (07:18)
* **Stacking Architecture:** Three vertically stacked synchronized line plots:
  1. *Obliquity* (Red-orange line `#D9534F`)
  2. *Precession Index* (Dark maroon line `#8A1C14`)
  3. *Eccentricity of Earth's Orbit* (Gold line `#F0AD4E`)
* **Motion:** The three waveforms trace simultaneously across a unified horizontal time axis (800,000 Years Before Present to 0), demonstrating how Milankovitch cycles lock together over deep time.

#### Matrix Visualization of Repetition (07:11)
* To illustrate "230 green periods", the animation scales down a single green vector silhouette of the Sahara and duplicates it into a tightly registered **23 × 10 grid** filling the entire 16:9 canvas. 
* They populate in a rapid row-by-row cascade (staggered by 2 frames per icon) over 1.8 seconds.

---

### 5. CHAPTER / SECTION TRANSITIONS

* **Host-to-Graphics Handoff:**
  * Uses a physical stage metaphor: Host Michael Molina is shot full-body against a dark mottled slate-grey textured limbo studio (00:00, 01:12, 02:44).
  * Rather than abrupt hard cuts, the camera often dollies gently into a graphic that wipes across the screen or fades up over the host’s shoulder, expanding to fill the frame (e.g., 01:21 from host to dust plumes over the Atlantic).
* **Segment Delimiters:**
  * Clean cut-and-push transitions: A subtle whoosh sound accompanied by an illustrated graphic card sliding in to push the prior visual off-screen (04:44 entering Ténéré Desert).
  * Eras end with an environmental reverse: The green satellite map desaturates back to arid tan using a reverse wipe from North to South (06:40), symbolizing desertification.

---

### 6. THE 10 REUSABLE MOTION-GRAPHICS RULES

1. **Use Grounded Texture Backplates, Never Flat Hex Solids:** Never place charts, maps, or host pop-ups on a digital `#000000` or `#FFFFFF`. Always use a tactile texture—such as slate rock, parchment, or subtle 10% halftone dot patterns—to keep scientific graphics feeling archival and organic.
2. **Restrict Every Graphic Plate to Two Brand Colors + Neutral:** Charts and maps rely on a disciplined palette: Slate/Charcoal neutral (`#1A1A1A`), Parchment Cream (`#F4EEDD`), vivid Green (`#46B876`) for humid periods, and Ochre/Gold (`#E08738`) for arid cycles.
3. **Pin Attributions in Ultra-Muted Corners:** Scientific credibility requires citing academic papers (`SERENO ET AL. 2008`). Keep them legible but subordinate: 2% screen height, mono/condensed sans-serif, low-contrast grey, zero background box, anchored strictly to lower margins.
4. **Isolate Artifact Cut-Outs with Consistent Depth:** Archaeological finds (arrowheads, fish hooks, pottery at 01:26, 05:08) must be cleanly rotoscoped onto white/cream cards with identical 4px soft contact drop-shadows, matching museum display vitrines.
5. **Always Bind Time Indicators to Horizontal Spatial Space:** Do not show standalone digital counters ticking down. Always anchor dates to a spatial bar where the left is the past, the right is the present, and the period discussed is a highlighted slice between them.
6. **Trigger Text Transitions Synchronously with Syllables:** Topic text ("AFRICAN HUMID PERIOD") should expand exactly on the narrator's vocal stress, never arriving early to wait for the host to catch up.
7. **Use Organic Path-Drawing for Natural Features:** Rivers, coastlines, and lake boundaries should never dissolve into place. Animate their vector stroke paths from source to delta, giving water an active sense of flow and geographic agency.
8. **Differentiate Diagrammatic Lines from Illustrative Art:** When explaining physical mechanics (orbital tilt at 03:06; convection at 03:22), shift immediately to clean, wireframe vectors with clear direction arrows, separating analytical theory from observational landscape footage.
9. **Display Data En Masse to Communicate Scale:** When quoting massive frequencies (e.g., "230 green periods" at 07:11), do not show the number "230". Instead, populate a tight visual matrix of 230 miniaturized graphic units so the viewer instantly feels the magnitude.
10. **Use Split-Screen Polaroids for Over-the-Shoulder Focus:** When the host is on camera, limit graphic callouts to a single 16:9 or square card docked on the opposite third of the frame, bordered with a clean 2px frame and a distinct header pill. Never clutter both sides of the host simultaneously.