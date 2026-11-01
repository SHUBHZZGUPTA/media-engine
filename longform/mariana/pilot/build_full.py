#!/usr/bin/env python3
"""Mariana Trench, full video in the approved pilot style.
Real NOAA/NASA footage + 3D trench/globe + living stills (slow camera move, drifting marine snow, optional circle/title)
+ the layered sinking shot. Captions at the bottom, ~1 short graphic per 20 s, no mascot (its lines and the narrator's
replies to it are cut from the approved narration).
Writes out_full/spec.json, out_full/mix_spec.json, out_full/voice.wav, out_full/music.json and out_full/stills.json
(the living stills still to render: name -> config)."""
import json, os, subprocess, re
import numpy as np, soundfile as sf
M = "/home/claude/media-engine/longform/mariana"; FE = "/home/claude/media-engine/outputs/fetch"
ART = f"{M}/art"; ARC = f"{FE}/mt-archive"; C3 = f"{M}/clips3d"
P = "/home/claude/pilot"; S = f"{P}/shots"; O = f"{P}/out_full"; os.makedirs(S, exist_ok=True); os.makedirs(O, exist_ok=True)
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
L = json.load(open(f"{M}/lines_en.json"))
W = [(float(a) / 1.12, float(b) / 1.12, w.strip()) for a, b, w in (r.split(None, 2) for r in open(f"{M}/words_en.txt") if r.strip())]

# ---------------- cuts: the mascot / skit lines and the narrator's replies to them ----------------
CHARS = [l["i"] for l in L if l["who"] != "Narrator"]
cuts = []
for i in CHARS:
    nxt = L[i + 1]["t0"] if i + 1 < len(L) else L[i]["t1"] + 2
    cuts.append([L[i]["t0"] - .05, max(L[i]["t1"] + .05, nxt - .5)])
cuts += [[108.68, 109.82], [193.07, 197.36], [541.06, 545.74], [624.81, 629.77],      # "Exactly." / "Someone already has." / "In a way, yes." / "Not quite."
         [L[100]["t0"] - .05, L[101]["t0"] - .5]]                                      # "It does, and we'll keep going after them."
cuts.sort(); SKIP = []
for a, b in cuts:
    if SKIP and a <= SKIP[-1][1] + .05: SKIP[-1][1] = max(SKIP[-1][1], b)
    else: SKIP.append([a, b])
SKIP = [(round(a, 2), round(b, 2)) for a, b in SKIP]
def nt(t):
    d = 0.0
    for a, b in SKIP:
        if t >= b: d += b - a
        elif t > a: return a - d
    return t - d
END = round(nt(L[101]["t1"]) + 3.0, 2)                                                   # CTA + a short tail

def K(i, word, off=-.12):
    """Pilot-time of the first spoken word in line i that starts with `word` (case-insensitive)."""
    w0 = word.lower().split()[0]
    for a, b, w in W:
        if L[i]["t0"] - .3 <= a <= L[i]["t1"] + .3 and re.sub(r"[^a-z0-9]", "", w.lower()).startswith(re.sub(r"[^a-z0-9]", "", w0)):
            return round(nt(a + off), 3)
    txt = re.sub(r"\[[^\]]*\]\s*", "", L[i]["text"]).replace("*", ""); k = txt.lower().find(word.lower())   # transcript spelled it differently:
    if k < 0: raise SystemExit(f"word {word!r} not in line {i}: {L[i]['text']}")                         # place it by its position in the line
    return round(nt(L[i]["t0"] + (L[i]["t1"] - L[i]["t0"]) * k / max(1, len(txt)) + off), 3)
def T(i, off=-.15): return round(nt(L[i]["t0"] + off), 3)

# ---------------- voice ----------------
v, sr = sf.read(f"{M}/voice_en.wav", dtype="float32"); keep, last = [], 0.0
for a, b in SKIP: keep.append(v[int(last * sr):int(a * sr)]); last = b
keep.append(v[int(last * sr):])
vo = np.concatenate(keep)[:int(END * sr)]
if len(vo) < int(END * sr): vo = np.pad(vo, (0, int(END * sr) - len(vo)))
n = int(.4 * sr); vo[-n:] *= np.linspace(1, 0, n)
sf.write(f"{O}/voice.wav", vo, sr, subtype="PCM_16")

# ---------------- sources ----------------
V = {}
for d in ("mt-video", "mt-video2", "mt-video3"):
    for f in os.listdir(f"{FE}/{d}"):
        if f.endswith(".webm"): V[f[2:-5]] = f"{FE}/{d}/{f}"
def vdur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
CROP = {"nasa_drain": "crop=iw:ih*0.86:0:0", "garbage_patch": "crop=iw:ih*0.9:0:0"}
SPEED = {"nasa_drain": 2.0}

shots, stills = [], {}
def add(t0, bg, layers=(), cut="curve", kind=""):
    shots.append({"t0": round(t0, 3), "bg": bg, "layers": list(layers), "cut": cut, "kind": kind})
def foot(t0, key, start):
    """Real footage from `start` s of clip `key`; its length is fixed later, once the next shot's start is known."""
    add(t0, {"video": None, "img": "#02070d"}, kind=f"foot:{key}:{start}")
def clip(t0, name, layers=(), cut="curve"): add(t0, {"video": f"{C3}/{name}.mp4", "img": "#02070d"}, layers, cut, kind="clip")
def still(t0, img, cfg=None, layers=(), cut="curve"):
    """Living still: slow camera move + drifting particles over a picture (AI art or archive photo)."""
    add(t0, {"video": None, "img": "#02070d"}, layers, cut, kind="still")
    shots[-1]["still"] = (img, cfg or {})
def premade(t0, path, layers=(), cut="curve"): add(t0, {"video": path, "img": "#02070d"}, layers, cut, kind="premade")
def title(text, t_in, t_out, y=170, size=92, box=None, color="#ffffff"):
    return {"img": {"text": text, "size": size, "color": color, "box": box, "font": FONT}, "x": 960, "y": y, "in": round(t_in, 3), "out": round(t_out, 3), "enter": "fade", "exit": "fade"}
def chapter(t0, n, name, bg_fn):
    bg_fn(t0)
    shots[-1]["cut"] = "zoom"
    shots[-1]["layers"] += [title(f"CHAPTER {n}", t0 + .3, t0 + 2.6, y=470, size=60, color="#9fd6ff", box="#0a0f18d0"),
                            title(name, t0 + .3, t0 + 2.6, y=600, size=84, box="#0a0f18d0")]
A = lambda n: f"{ART}/{n}.png"
def R(n):
    for e in (".jpg", ".png"):
        if os.path.exists(f"{ARC}/{n}{e}"): return f"{ARC}/{n}{e}"
    raise SystemExit("missing archive " + n)
PUSH, PULL = {"z0": 1.0, "z1": 1.22}, {"z0": 1.22, "z1": 1.02}
def pan(a, b, z=1.18): return {"z0": z, "z1": z + .04, "c0": a, "c1": b}

# ======================= HOOK + CHAPTER 1 opening (the approved pilot, same cut points) =======================
premade(0.0, f"{S}/sink.mp4", cut="hard")
foot(T(1, -.6), "medusa", 12.0)
foot(K(1, "looked"), "bathynomus", 9.0)
premade(T(2, -1.8), f"{S}/plastic.mp4")
clip(T(4), "G_pacific", [title("THE MARIANA TRENCH", K(4, "Mariana"), K(4, "Mariana") + 3.1, size=96)])
foot(K(5, "Down"), "vents", 12.0)
foot(K(5, "fish"), "jelly_mariana", 23.6)
foot(K(5, "shrimp"), "bathynomus", 34.0)
foot(K(5, "and", -.25) if False else K(5, "under", -.45), "nasa_drain", 5.0)
foot(K(6, "So"), "okeanos_guyot", 12.0)
foot(K(6, "metre", -.3) if False else K(6, "meter", -.3), "dive11_fish", 0.0)
shots[-1]["layers"] += [title("CHAPTER 1", T(8, -2.2), T(8, -.1), y=470, size=60, color="#9fd6ff", box="#0a0f18d0"),
                        title("The Hole at the Bottom of the World", T(8, -2.2), T(8, -.1), y=600, size=84, box="#0a0f18d0")]
clip(T(8, -.1), "G_where", cut="zoom")
clip(T(8, -.1) + 13.5, "T_length", [title("~2,550 km long", K(10, "two"), K(10, "two") + 4.3, size=88)])
clip(T(8, -.1) + 20.55, "T_deep")
still(K(12, "Mount"), R("everest"), PUSH)
still(K(12, "drop"), A("mt_everest"), {"z0": 1.25, "z1": 1.0, "c0": [.5, .2], "c1": [.5, .5]})
still(T(14), A("mt_everest"), {"z0": 1.05, "z1": 1.3, "c0": [.5, .45], "c1": [.5, .3]},
      [title("Still ~2 km under water", K(14, "two"), K(14, "two") + 3.4, size=88, box="#0a0f18c0")])
foot(T(15), "tohoku_spin", 1.0)
still(T(16), A("mt_plates"), pan([.35, .5], [.6, .5]))
still(K(16, "slides", -.3), A("mt_plates"), {"z0": 1.1, "z1": 1.35, "c0": [.55, .55], "c1": [.48, .6]})
still(T(17), A("mt_plates"), {"z0": 1.35, "z1": 1.5, "c0": [.48, .62], "c1": [.48, .58], "circle": [.47, .53, 120, 160, 1.4]})
still(T(19), A("mt_plates"), {"z0": 1.0, "z1": 1.1}, [title("A few cm per year", K(19, "few"), K(19, "few") + 3.5, size=88, box="#0a0f18c0")])

# ======================= CHAPTER 2: WHERE THE LIGHT DIES =======================
chapter(T(20, -.6), 2, "Where the Light Dies", lambda t: still(t, A("mt_surface"), {"z0": 1.0, "z1": 1.12, "rise": 6, "snow": 40}))
still(T(21), A("mt_twilight"), {"z0": 1.0, "z1": 1.15, "c0": [.5, .3], "c1": [.5, .55], "rise": 30})
still(T(22), A("mt_twilight"), {"z0": 1.15, "z1": 1.35, "c0": [.5, .6], "c1": [.5, .75], "rise": 40, "dim": .35},
      [title("200 m", K(22, "200"), K(22, "200") + 3.0, size=96, color="#9fd6ff")])
still(T(23), A("mt_midnight"), {"z0": 1.0, "z1": 1.15, "rise": 45}, [title("1,000 m · no sunlight", K(23, "1"), K(23, "1") + 3.4, size=88, color="#9fd6ff")])
foot(T(25, -.15) if False else K(25, "Down", -.4), "drifters", 96.0)
foot(K(25, "bioluminescence", -.4), "drifters", 151.0)
foot(T(26), "jelly_mariana2", 13.5)
foot(K(26, "Some"), "medusa", 44.0)
still(K(26, "anglerfish"), R("anglerfish"), PUSH)
foot(T(29), "jelly_mariana", 25.0)

# ======================= CHAPTER 3: THE WEIGHT OF THE OCEAN =======================
chapter(T(30, -.6), 3, "The Weight of the Ocean", lambda t: still(t, A("mt_midnight"), {"z0": 1.2, "z1": 1.0, "rise": 40}))
premade(T(31), f"{S}/pressure.mp4")
still(T(35), A("mt_floor"), {"z0": 1.0, "z1": 1.25, "rise": 12}, [title("> 7 tonnes on every square inch", K(35, "7"), K(35, "7") + 4.0, size=80, box="#0a0f18c0")])
foot(T(37), "hohonu_dive7", 27.0)
still(K(38, "1960"), R("trieste_hoist"), PUSH, [title("1960", K(38, "1960"), K(38, "1960") + 2.8, y=230, size=120)])

# ======================= CHAPTER 4: THE FIRST TWO MEN =======================
chapter(T(39, -.6), 4, "The First Two Men", lambda t: still(t, R("trieste_1960"), {"z0": 1.0, "z1": 1.15}))
still(T(40), A("mt_trieste"), pan([.4, .45], [.6, .5], 1.1))
still(T(41), R("trieste_crew"), {"z0": 1.0, "z1": 1.12, "c0": [.5, .4], "c1": [.5, .3]})
clip(T(42), "T_dive1960", [title("23 January 1960", K(42, "23rd"), K(42, "23rd") + 3.2, size=84)])
premade(T(43), f"{S}/sink.mp4")
still(T(44, -.1), A("mt_trieste"), {"z0": 1.35, "z1": 1.45, "flicker": .25, "dim": .5}, cut="flash")
still(T(46), A("mt_trieste"), {"z0": 1.5, "z1": 1.65, "c0": [.48, .55], "c1": [.47, .58], "dim": .45, "circle": [.47, .55, 120, 120, 1.0]})
still(T(47), A("mt_trieste"), {"z0": 1.2, "z1": 1.0, "dim": .4})
still(T(48), A("mt_floor"), {"z0": 1.0, "z1": 1.2, "rise": 10}, [title("10,900 m · the bottom", K(48, "touched"), K(48, "touched") + 3.2, size=84, color="#9fd6ff")])
still(T(49), A("mt_floor"), {"z0": 1.2, "z1": 1.3, "rise": 4, "snow": 420})
still(T(51), R("trieste_1960"), {"z0": 1.15, "z1": 1.0, "dim": .2}, [title("52 years", K(51, "52"), K(51, "52") + 3.0, size=120)])
still(T(52), R("deepsea_challenger"), PUSH, [title("2012 · James Cameron", K(52, "2012"), K(52, "2012") + 3.4, size=80, box="#0a0f18c0")])
still(K(52, "Victor", -.3), R("limiting_factor"), PUSH)
still(T(53), A("mt_surface"), {"z0": 1.0, "z1": 1.1, "c0": [.6, .3], "c1": [.7, .25], "rise": 6, "snow": 40},
      [title("Moon: 12 people", K(53, "Twelve"), K(53, "Twelve") + 5.0, y=230, size=88, box="#0a0f18c0"),
       title("Challenger Deep (to 2019): 3", K(53, "three"), K(53, "three") + 2.6, y=380, size=80, box="#8a1a20d0")])
foot(T(54), "dive06_red", 2.0)

# ======================= CHAPTER 5: SOMETHING IS ALIVE DOWN HERE =======================
chapter(T(55, -.6), 5, "Something Is Alive Down Here", lambda t: foot(t, "dive06_red", 19.0))
foot(T(56), "bathynomus", 40.0)
still(T(57), R("snailfish_mariana"), {"z0": 1.0, "z1": 1.2, "c0": [.5, .45], "c1": [.5, .4]})
still(T(59), R("snailfish"), {"z0": 1.0, "z1": 1.15})
clip(T(60), "G_japan", [title("8,336 m · deepest fish ever filmed", K(60, "8"), K(60, "8") + 4.0, y=200, size=76, box="#0a0f18c0")])
foot(T(61), "dive11_fish", 6.0)
foot(T(63), "amphipod_live", 2.0)
still(K(63, "deep", -.3), R("alicella_hand"), PUSH)
foot(T(65), "dive11_fish", 0.0) if False else still(T(65), R("amphipod_giant"), {"z0": 1.0, "z1": 1.18})
still(T(66), R("xenophyophore"), PUSH, [title("ONE cell · the size of a lemon", K(66, "one"), K(66, "one") + 3.6, size=80, box="#0a0f18c0")])
foot(T(67), "okeanos_guyot", 28.0)
still(T(68), A("mt_floor"), {"z0": 1.0, "z1": 1.15, "rise": 10})
still(T(69), A("mt_plates"), {"z0": 1.1, "z1": 1.4, "c0": [.5, .55], "c1": [.5, .7]})

# ======================= CHAPTER 6: THE TRENCH THAT DRINKS THE OCEAN =======================
chapter(T(70, -.6), 6, "The Trench That Drinks the Ocean", lambda t: clip(t, "T_slab"))
still(T(72), A("mt_water"), {"z0": 1.0, "z1": 1.25, "c0": [.45, .5], "c1": [.55, .6]})
still(K(74, "And", -.3), R("ocean_seismometer"), PUSH, [title("2018", K(74, "2018"), K(74, "2018") + 2.6, y=230, size=120)])
still(T(75), R("ocean_seismometer"), {"z0": 1.2, "z1": 1.05}, [title("19 sea-floor sensors · 1+ year", K(75, "19"), K(75, "19") + 4.0, size=80, box="#0a0f18c0")])
still(T(76), A("mt_water"), {"z0": 1.2, "z1": 1.5, "c0": [.5, .6], "c1": [.5, .72]}, [title("~30 km deep", K(76, "30"), K(76, "30") + 3.0, size=96, box="#0a0f18c0")])
foot(T(77), "nasa_drain", 18.0)
shots[-1]["layers"].append(title("~3× more water than thought (2018 estimate)", K(77, "worldwide"), K(77, "worldwide") + 4.0, size=64, box="#0a0f18c0"))
foot(T(79), "vents", 28.0)
foot(K(79, "volcanoes"), "vents", 44.0)
clip(T(80, -.15), "T_eifuku")
still(K(82, "Because", -.3), R("champagne_vent"), PUSH)
still(K(82, "liquid", -.4), R("eifuku_bubbles"), {"z0": 1.0, "z1": 1.2, "rise": 60}, [title("Liquid CO2", K(82, "liquid"), K(82, "liquid") + 3.0, size=104, box="#0a0f18c0")])
still(K(84, "The", -.3), R("eifuku_mussels"), PUSH)
still(T(85), A("mt_water"), {"z0": 1.1, "z1": 1.0, "c0": [.6, .5], "c1": [.5, .5]})
foot(T(86), "garbage_patch", 40.0)

# ======================= CHAPTER 7: WE GOT THERE FIRST =======================
chapter(T(87, -.6), 7, "We Got There First", lambda t: premade(t, f"{S}/plastic.mp4"))
still(T(88), R("wright_vescovo"), PUSH)
still(T(89), R("amphipod"), {"z0": 1.0, "z1": 1.2}, [title("2019", K(89, "2019"), K(89, "2019") + 2.6, y=230, size=120)])
still(T(90), R("microplastic"), PUSH, [title("Mariana Trench samples: 100%", K(90, "every"), K(90, "every") + 3.8, size=84, box="#8a1a20d0")])
foot(T(93), "garbage_patch", 52.0)
clip(T(94), "T_fingerprint")

# ======================= ENDING =======================
clip(T(95, -.4), "T_outro", cut="zoom")
still(K(96, "A", -.3), A("mt_everest"), {"z0": 1.0, "z1": 1.12})
foot(K(96, "where"), "jelly_mariana", 28.0)
still(K(96, "window", -.2), A("mt_trieste"), {"z0": 1.2, "z1": 1.35, "dim": .3})
foot(K(96, "fish", -.2), "medusa", 46.0)
foot(K(96, "shrimp", -.2), "bathynomus", 44.0)
foot(T(97), "nasa_drain", 34.0)
foot(T(98), "okeanos_guyot", 60.0)
still(T(101), A("mt_surface"), {"z0": 1.0, "z1": 1.15, "rise": 6, "snow": 40},
      [title("SUBSCRIBE · BHUGOL", K(101, "subscribe"), END, y=470, size=96, box="#8a1a20d0"),
       title("Would YOU go down?", K(101, "would"), END, y=620, size=80, box="#0a0f18c0")])

# ---------------- close the timeline, cut footage, list stills ----------------
shots.sort(key=lambda s: s["t0"])
for s, n_ in zip(shots, shots[1:] + [None]): s["t1"] = n_["t0"] if n_ else END
# long stills / footage: split so the picture changes at least every ~9 s (stills get a new framing, footage a new moment)
import copy
out = []
for s in shots:
    d = s["t1"] - s["t0"]
    if d <= 10.5 or s["kind"] not in ("still",) and not s["kind"].startswith("foot:"): out.append(s); continue
    parts = int(d // 8.0) + (1 if d % 8.0 > 3 else 0); parts = max(2, parts); seg_ = d / parts
    for q in range(parts):
        s2 = copy.deepcopy(s); s2["t0"] = round(s["t0"] + seg_ * q, 3); s2["t1"] = round(s["t0"] + seg_ * (q + 1), 3)
        if q:
            s2["cut"] = "curve"; s2["layers"] = [L_ for L_ in s["layers"] if L_["in"] < s2["t1"] and L_["out"] > s2["t0"]]
            if s["kind"] == "still":
                img, cfg = s["still"]; cfg = dict(cfg)
                cfg.update([({"z0": 1.3, "z1": 1.45, "c0": [.38, .45], "c1": [.44, .48]}), ({"z0": 1.25, "z1": 1.1, "c0": [.62, .52], "c1": [.55, .5]})][q % 2])
                cfg.pop("circle", None); s2["still"] = (img, cfg)
            else:
                _, key, st = s["kind"].split(":"); s2["kind"] = f"foot:{key}:{float(st) + 14.0 * q}"
        else:
            s2["layers"] = [L_ for L_ in s["layers"] if L_["in"] < s2["t1"]]
        out.append(s2)
shots[:] = out
bad = [(s["t0"], s["t1"]) for s in shots if s["t1"] - s["t0"] < .8]
if bad: raise SystemExit(f"shots shorter than 0.8 s: {bad}")
for k, s in enumerate(shots):
    d = s["t1"] - s["t0"] + .4
    if s["kind"].startswith("foot:"):
        _, key, st = s["kind"].split(":"); src = V[key]; sp = SPEED.get(key, 1.0); st = float(st)
        st = max(0.0, min(st, vdur(src) - d * sp - .3))
        out = f"{S}/f{k:03d}_{key}.mp4"
        vf = (CROP[key] + "," if key in CROP else "") + (f"setpts=PTS/{sp}," if sp != 1 else "") + \
             "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,format=yuv420p"
        if not os.path.exists(out):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{st:.2f}", "-i", src, "-t", f"{d * sp:.2f}", "-vf", vf, "-an",
                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", out], check=True)
        s["bg"]["video"] = out; s["src"] = [key, round(st, 2)]
    elif s["kind"] == "still":
        img, cfg = s.pop("still"); name = f"st{k:03d}"
        c = {"dur": round(d, 2), "img": os.path.basename(img), "z0": 1.0, "z1": 1.15, "c0": [.5, .5], "c1": [.5, .5], "snow": 160, "rise": 20, "flicker": .03}
        c.update(cfg); stills[name] = {"src": img, "cfg": c}
        s["bg"]["video"] = f"{S}/{name}.mp4"
    elif s["kind"] in ("clip", "premade"):
        pass
json.dump(stills, open(f"{O}/stills.json", "w"), indent=1)

# ---------------- captions (approved ones; words inside cuts removed; re-timed) ----------------
spec0 = json.load(open(f"{M}/spec_en.json")); caps = []
inside = lambda t: any(a - .02 <= t < b for a, b in SKIP)
for c in spec0["captions"]:
    ws = [[w, nt(a), nt(b), k] for w, a, b, k in c["words"] if not inside(a)]
    if not ws: continue
    caps.append({"t0": ws[0][1] - .05, "t1": ws[-1][2] + .25, "words": ws})
for x, y in zip(caps, caps[1:]): x["t1"] = min(x["t1"], y["t0"])
caps = [c for c in caps if c["t0"] < END - .3]
spec = {"w": 1920, "h": 1080, "fps": 30, "shots": [{k: v for k, v in s.items() if k != "kind"} for s in shots], "punch": [], "shake": [], "captions": caps, "fx": []}
json.dump(spec, open(f"{O}/spec.json", "w"), indent=1)
# sound: designed whoosh only on chapter cuts and the one flash; low impact on "A plastic bag" and on the BANG
fx = [["impact-bass-1", K(2, "plastic", 0), -16], ["impact-bass-1", K(44, "bang", 0), -10]]
mspec = dict(spec, shots=[dict(spec["shots"][0], layers=[])] + [dict(s, layers=[]) for s in spec["shots"][1:] if s["cut"] in ("zoom", "flash", "whip")], fx=fx)
json.dump(mspec, open(f"{O}/mix_spec.json", "w"), indent=1)
MU = "/home/claude/media-engine/money-mirage/mm3/library/music/"
ch = [0, T(8, -2.2), T(30, -.6), T(55, -.6), T(70, -.6), T(87, -.6), T(95, -.4), END]
tracks = [("4_standoff.mp3", -18), ("1_keys.mp3", -19), ("5b_shadows.mp3", -19), ("3_something.mp3", -19), ("6_system.mp3", -19), ("2_never.mp3", -19), ("7_fact.mp3", -18)]
secs = [{"file": MU + f, "from": round(max(0, ch[k] - (.8 if k else 0)), 2), "to": round(ch[k + 1], 2), "gain_db": g} for k, (f, g) in enumerate(tracks)]
json.dump({"sfx_dir": "/home/claude/media-engine/money-mirage/mm3/library/sfx", "below_voice_db": 21, "swell_db": 3, "sections": secs}, open(f"{O}/music.json", "w"), indent=1)
nf = sum(1 for s in shots if s["kind"].startswith("foot")); nst = len(stills); nc = sum(1 for s in shots if s["kind"] == "clip")
ntit = sum(len(s["layers"]) for s in shots)
print(f"{len(shots)} shots | footage {nf} | living stills {nst} | 3D clips {nc} | premade {len(shots) - nf - nst - nc} | graphics {ntit} | end {END:.1f} s | cuts {len(SKIP)} removing {sum(b - a for a, b in SKIP):.1f} s")
