#!/usr/bin/env python3
"""Shot plan for the BHUGOL Mariana Trench long-form. Helpers, timeline close and retention pass follow india/pilot/plan_pilot.py.

Shots are pinned to script LINES (index into script_en.md), never to fixed seconds.
Usage: python3 plan_pilot.py lines.json spec.json words.txt [speed] [--punch=7]
Also writes clips3d.json (3D globe clips, local times) next to spec.json.
"""
import json, sys, os, re, textwrap, difflib
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..", "..")
A1 = os.path.join(HERE, "art"); A2 = A1; C1 = os.path.join(HERE, "cards"); C2 = C1
ARC = os.path.join(ROOT, "outputs", "fetch", "mt-archive"); CLIPS = os.path.join(HERE, "clips3d")
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
args = [a for a in sys.argv[1:] if not a.startswith("--")]
L = json.load(open(args[0])); END = L[-1]["t1"] + 1.6
WORDS = args[2]; SPEED = float(args[3]) if len(args) > 3 else 1.0
PUNCH = float(next((a.split("=")[1] for a in sys.argv if a.startswith("--punch=")), 7))

# ---- script (speaker + English text per line) ----
SCRIPT, SPK, CHAP = [], [], {}
chap = None
for r in open(os.path.join(HERE, "script_en.md"), encoding="utf-8"):
    r = r.strip(); m = re.match(r"# (HOOK|CHAPTER (\d+)|ENDING)", r)
    if m: chap = 0 if m.group(1) == "HOOK" else (int(m.group(2)) if m.group(2) else 99); CHAP[chap] = len(SCRIPT); continue
    m = re.match(r"^([A-Z][A-Z .'&]*?):\s*(.+)$", r)
    if m and chap is not None: SPK.append(m.group(1)); SCRIPT.append(m.group(2))
assert len(SCRIPT) == len(L), (len(SCRIPT), len(L))
EN = [re.sub(r"\[[^\]]*\]\s*", "", s).replace("*", "").replace("‡", "") for s in SCRIPT]

def T(i, f=0.0):
    x = L[i]; return x["t0"] + (x["t1"] - x["t0"]) * f if f >= 0 else x["t0"] + f
def kw(i, word):
    s = EN[i]; k = s.find(word)
    if k < 0: k = s.lower().find(word.lower())
    return max(0.0, min(0.95, k / max(len(s), 1))) if k >= 0 else 0.0
def K(i, word): return T(i, kw(i, word))
def talk(i): return [T(i), T(i, 1)]
def aspect_h(path, w):
    im = Image.open(path); return int(w * im.height / im.width)
def exists(p): return p and os.path.exists(p)

# ---- assets ----
ART_FALLBACK = {"mt_floor": "challenger_deep", "mt_surface": "okeanos", "mt_twilight": "deep_discoverer", "mt_midnight": "atolla",
                "mt_plastic": "challenger_deep", "mt_trieste": "trieste_1960", "mt_everest": "everest", "mt_plates": "subduction",
                "mt_water": "subduction", "mt_champagne": "eifuku_bubbles"}
def a(n):
    for d in (A2, A1):
        p = os.path.join(d, n + ".png")
        if os.path.exists(p): return p
    return arc(ART_FALLBACK[n]) if n in ART_FALLBACK else None
ARC2 = ARC3 = ARC
def arc(key):
    for d in (ARC3, ARC2, ARC):
        for ext in (".jpg", ".png"):
            p = os.path.join(d, key + ext)
            if os.path.exists(p) and os.path.getsize(p) > 2000: return p
    return None
def card(n):
    for d in (C2, C1):
        p = os.path.join(d, n + ".png")
        if os.path.exists(p): return p
    return None

# ---- layers ----
def txt(s, x, y, t, size=72, box=None, color="#ffffff", out=None, enter="pop", scale=1.25):
    size = int(size * scale)
    font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if any(c in s for c in "→✓↓↑✗") else FONT
    wmax = max(len(r) for r in s.split("\n")) * size * .56 + (60 if box else 0)
    x = int(min(max(x, 40 + wmax / 2), 1880 - wmax / 2)) if wmax < 1800 else 960
    d = {"img": {"text": s, "size": size, "color": color, "box": box, "font": font}, "x": x, "y": y, "in": t, "enter": enter}
    if out is not None: d["out"] = out
    return d
def lab(s, t, x=960, y=250, size=90, box=None, **k): return txt(s, x, y, t, size=size, box=box, **k)
def tag(s, t, x=1250, y=420, size=70): return txt(s, x, y, t, size=size, box="#222222")
def say(i, x, y=380, width=24, size=54):
    if len(EN[i]) > 110: width = 34
    s = "\n".join(textwrap.wrap(EN[i], width)); y = max(y, 70 + s.count("\n") * 34 + 34)
    return txt(s, x, y, T(i), size=size, box="#ffffffee", color="#222222", out=T(i, 1) + .25, scale=1.0)
def ch(name, x, y=1045, h=560, t=None, enter="pop", talks=(), flip=False, out=None):
    p = a(name)
    if not p: return None
    d = {"img": p, "x": x, "y": y, "h": h, "enter": enter, "talk": [talk(i) for i in talks], "flip": flip}
    if t is not None: d["in"] = t
    if out is not None: d["out"] = out
    return d
def traveller(talks=(), x=360, h=700): return ch("c_traveller", x, 1030, h, enter="none", talks=talks)
def panel(path):
    out = path[:-4] + "_panel.png"
    if not os.path.exists(out):
        from PIL import ImageDraw
        im = Image.open(path).convert("RGBA"); pad = 50
        pn = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
        ImageDraw.Draw(pn).rounded_rectangle([0, 0, pn.width - 1, pn.height - 1], radius=40, fill=(244, 240, 232, 240))
        pn.alpha_composite(im, (pad, pad)); pn.save(out)
    return out
def imgcard(path, x, y, w, t, out=None, framed=False):
    if not exists(path): return None
    if framed: path = frame(path)
    elif "cycle" in path or "bars" in path: path = panel(path)
    d = {"img": path, "x": x, "y": y, "h": aspect_h(path, w), "in": t, "enter": "pop", "shadow": False}
    if out is not None: d["out"] = out
    return d
def frame(path):
    """Archive picture as a white-bordered print (for boards)."""
    out = os.path.join(HERE, "cards", "_framed_" + os.path.basename(path).rsplit(".", 1)[0] + ".png")
    if not os.path.exists(out):
        im = Image.open(path).convert("RGB"); im.thumbnail((900, 900)); b = 18
        f = Image.new("RGB", (im.width + 2 * b, im.height + 2 * b), (245, 242, 236)); f.paste(im, (b, b)); f.save(out)
    return out

# ---- shots ----
shots = []; LAST = [None]; CLIP = {}
def shot(t0, bg, layers=(), cam=None, over=(), **kw_):
    if bg is None: bg = LAST[0] or "#1d2733"
    b = {"img": bg, **kw_}
    if cam: b["cam"] = cam
    if over: b["over"] = list(over)
    if not str(bg).startswith("#") and not kw_.get("blur"): LAST[0] = bg
    s = {"t0": t0, "bg": b, "layers": [x for x in layers if x]}; shots.append(s); return s
def board(t0, layers=(), talks=(), dur=6.0, x=360):
    bg = LAST[0] or "#1d2733"
    return shot(t0, bg, [traveller(talks, x=x)] + list(layers), cam=[[t0, .5, .5, 1.0], [t0 + dur, .5, .5, 1.08]], blur=14, dim=.5)
def quip(i, extra=()):          # traveller line on a board, with his words in a bubble
    return board(T(i, -.15), [say(i, 760, 330)] + list(extra), talks=[i])
def plate(t0, img, cam=None, layers=(), zoom=(1.0, 1.12), c=(.5, .5)):
    if cam is None: cam = [[t0, c[0], c[1], zoom[0]], [t0 + 6, c[0], c[1], zoom[1]]]
    return shot(t0, img, layers, cam=cam)
def pic(t0, key, layers=(), zoom=(1.0, 1.15), c0=(.5, .5), c1=None, fallback=None):
    """Archive picture / photo with a slow Ken Burns move (falls back to a plate if it didn't download)."""
    p = arc(key) or fallback
    if p is None: return board(t0, list(layers))
    c1 = c1 or c0
    return shot(t0, p, layers, cam=[[t0, c0[0], c0[1], zoom[0]], [t0 + 6, c1[0], c1[1], zoom[1]]])
def chapter_card(n, i):
    t0 = T(i, -.6)
    return shot(t0, LAST[0] or "#1d2733", [imgcard(card(f"chapter{n}"), 960, 1000, 1550, t0 + .05)],
                cam=[[t0, .5, .5, 1.0], [t0 + 4, .5, .5, 1.06]], blur=14, dim=.5)
def cycle(t0, n, extra=()):
    return board(t0, [imgcard(card(f"cycle{n}" if isinstance(n, int) else f"cycle_{n}"), 1210, 1010, 1120, t0)] + list(extra))
def globe(cid, t0, cam, over=(), arcs=(), pins=(), layers=(), fallback=None):
    """A 3D globe clip (rendered by clips3d_full.py). All times absolute; cam = [[t, lon, lat, dist], ...]."""
    out = os.path.join(CLIPS, cid + ".mp4")
    CLIP[cid] = {"t0": t0, "data": {"mode": "globe", "globe": {"tex": "globe.jpg", "cam": cam, "over": list(over), "arcs": list(arcs), "pins": list(pins)}}}
    if os.path.exists(out): s = shot(t0, {"video": out}, layers); s["bg"] = {"video": out, "img": "#02070d"}; s["clip"] = cid
    else: s = shot(t0, fallback or "#0b1a2a", list(layers) + [txt(f"[3D {cid}]", 1700, 80, t0, size=30, scale=1)]); s["clip"] = cid
    LAST[0] = os.path.join(CLIPS, cid + "_last.jpg") if os.path.exists(out) else LAST[0]
    return s
def ov(img, a_): return {"img": img + ".png", "a": a_}
def ove(img, a_): return {"img": img + ".png", "a": a_, "add": 1}
def fadein(t, to=.9, d=.6): return [[0, 0], [t, 0], [t + d, to]]
def on(v=.9): return [[0, v]]
def pin(lon, lat, t, label=None, col=None, s=.05, size=44):
    p = {"lon": lon, "lat": lat, "at": t, "s": s}
    if label: p["label"] = label; p["size"] = size
    if col: p["col"] = col
    return p
def arcp(pts, t, d, col="#FFD84A", rad=.008, lift=.04, fade=None):
    x = {"pts": pts, "draw": [[0, 0], [t, 0], [t + d, 1]], "col": col, "rad": rad, "lift": lift}
    if fade: x["fade"] = fade
    return x


# ---- skits: one set, cast enters, each line gets a bubble over its speaker ----
CAST = {"TRAVELLER": "c_traveller", "SNAILFISH": "c_snailfish", "AMPHIPOD": "c_amphipod"}
def skit(i0, i1, bg, pos):
    """pos: {SPEAKER: (x, flip)}; first speaker is already there, the others slide in on their first line."""
    t0 = T(i0, -.3); lines = list(range(i0, i1 + 1)); lay = []
    for k, (who, (x, flip)) in enumerate(pos.items()):
        mine = [i for i in lines if SPK[i] == who]; first = mine[0] if mine else i0
        lay.append(ch(CAST[who], x, enter=("slideL" if x < 960 else "slideR") if k else "none", t=None if k == 0 else T(first, -.5), flip=flip, talks=mine,
                      h=640 if who == "TRAVELLER" else 560, y=1030 if who == "TRAVELLER" else 1045))
    for i in lines:
        x = pos.get(SPK[i], (960, False))[0]; lay.append(say(i, x))
    return shot(t0, a(bg) or LAST[0], lay, cam=[[t0, .5, .55, 1.0], [T(i1, 1), .5, .55, 1.12]])
def seq(i, items, x=1250, y=600, size=86, box="#222222", extra=()):
    """One board per keyword: items = [(keyword, text)], hard cuts."""
    for k, (w, s) in enumerate(items):
        t0 = T(i, -.15) if k == 0 else K(i, w)
        b = board(t0, [txt(s, x, y, t0 + .05, size=size, box=box)] + list(extra)); b["cut"] = "hard" if k else "curve"


# ---- Mariana additions: terrain (bathymetry relief) clips, photo cards, depth gauge ----
BATHY = json.load(open(os.path.join(HERE, "art", "map3d", "bathy.json"))) if os.path.exists(os.path.join(HERE, "art", "map3d", "bathy.json")) else {"bbox": [138, 150, 9, 22], "deepest_lonlat": [142.59, 11.37]}
CD = tuple(BATHY["deepest_lonlat"])                       # Challenger Deep (deepest cell of the DEM)
TRENCH = BATHY.get("axis") or [[139.8, 10.9], [141.2, 11.2], [142.6, 11.37], [144.3, 11.9], [145.9, 12.9], [146.9, 14.3], [147.5, 16.2],
                                [147.7, 18.2], [147.4, 20.2], [146.8, 21.8]]
EIFUKU = (144.04, 21.49); GUAM = (144.79, 13.44); IZU = (142.2, 29.5)
TER = {"bbox": BATHY["bbox"], "ne": "ne.jpg", "hs": "hs.png", "dem": "dem.png", "mask": "mask_none.png", "exag": .45}
def terrain(cid, t0, cam, routes=(), pins=(), layers=(), fallback=None):
    """A 3D sea-floor relief clip. cam = [[t, lon, lat, dist, elev_deg, yaw_deg], ...] (absolute times)."""
    out = os.path.join(CLIPS, cid + ".mp4")
    CLIP[cid] = {"t0": t0, "data": {"mode": "terrain", "terrain": dict(TER, cam=cam, routes=list(routes), pins=list(pins))}}
    if os.path.exists(out): s = shot(t0, {"video": out}, layers); s["bg"] = {"video": out, "img": "#02070d"}; s["clip"] = cid
    else: s = shot(t0, fallback or "#0b1a2a", list(layers) + [txt(f"[3D {cid}]", 1700, 80, t0, size=30, scale=1)]); s["clip"] = cid
    LAST[0] = os.path.join(CLIPS, cid + "_last.jpg") if os.path.exists(out) else LAST[0]
    return s
def tpin(lon, lat, t, label=None, col=None, s=.5, size=48):
    p = {"lon": lon, "lat": lat, "at": t, "s": s}
    if label: p["label"] = label; p["size"] = size
    if col: p["col"] = col
    return p
def depth(t, metres, x=1700, y=170):
    """Depth gauge chip, top right."""
    return txt(f"▼ {metres:,} m" if isinstance(metres, int) else f"▼ {metres}", x, y, t, size=58, box="#0b3a5a")
def photo(t0, key, layers=(), zoom=(1.0, 1.15), c0=(.5, .5), c1=None, credit=True):
    """Archive photo full-frame with Ken Burns (falls back to a blurred board)."""
    return pic(t0, key, layers, zoom=zoom, c0=c0, c1=c1, fallback=None)

CAST = {"TRAVELLER": "c_traveller", "SNAILFISH": "c_snailfish", "AMPHIPOD": "c_amphipod"}
def creature_talk(i, who, bg, extra=(), x=1250):
    """One creature line: the creature on its scene with a bubble (traveller joins on his own lines via skit())."""
    t0 = T(i, -.2)
    lay = [ch(CAST[who], x, enter="pop", t=t0, talks=[i], h=600), say(i, x, 330)] + list(extra)
    return shot(t0, a(bg) or LAST[0], lay, cam=[[t0, .5, .55, 1.0], [T(i, 1), .5, .55, 1.1]])

# ======================= HOOK =======================
c = CHAP[0]
photo(T(c, -.1), "limiting_factor", [lab("2019", K(c, "2019"), x=300, y=230, size=110), depth(K(c, "eleven"), "~11,000 m")], zoom=(1.0, 1.15))
plate(T(c + 1, -.15), a("mt_floor"), layers=[tag("Only a handful of humans", K(c + 1, "handful"), y=330)], zoom=(1.0, 1.2))
plate(T(c + 2, -.1), a("mt_plastic"), layers=[lab("A PLASTIC BAG", K(c + 2, "plastic"), size=120, box="#d6423a")], zoom=(1.05, 1.3), c=(.5, .55))
plate(T(c + 3, -.15), a("mt_plastic"), layers=[traveller(talks=[c + 3], x=380), say(c + 3, 900, 330)], zoom=(1.2, 1.3), c=(.6, .55))
t = T(c + 4, -.15)
globe("G_pacific", t, [[t, 120, 15, 3.6], [T(c + 4, 1), 143, 15, 2.4]],
      arcs=[arcp(TRENCH, T(c + 4, .3), 2.2, col="#FF3B30", rad=.007, lift=.01)],
      layers=[lab("THE MARIANA TRENCH", K(c + 4, "Mariana"), size=96)])
for k, (w, s_, key) in enumerate([("crush", "Crushes steel", None), ("glow", "Fish glow", "jelly_biolum"), ("Shrimp", "Giant shrimp-like creatures", "amphipod")]):
    t0 = T(c + 5, -.15) if k == 0 else K(c + 5, w)
    lay = [txt(s_, 1250, 300 if key else 600, t0 + .05, size=80, box="#222222")]
    if key: lay.append(imgcard(arc(key), 1250, 900, 640, t0 + .05, framed=True))
    b = board(t0, lay); b["cut"] = "hard" if k else "curve"
plate(K(c + 5, "swallowing"), a("mt_water"),
      layers=[lab("Swallowing the ocean?!", K(c + 5, "swallowing"), size=96, box="#d6423a")], zoom=(1.0, 1.15))
plate(T(c + 6, -.15), a("mt_surface"), layers=[lab("All the way down", K(c + 6, "all the way"), size=96)], zoom=(1.0, 1.12))
quip(c + 7)
chapter_card(1, c + 8)

# ======================= CHAPTER 1: THE HOLE AT THE BOTTOM OF THE WORLD =======================
c = CHAP[1]
t = T(c, -.1)
globe("G_where", t, [[t, 100, 20, 3.4], [K(c + 1, "Guam"), 140, 18, 2.2], [T(c + 1, 1), 144, 15, 1.9]],
      pins=[pin(139.7, 35.7, K(c + 1, "Japan"), "Japan", "#FFFFFF"), pin(121.0, 14.6, K(c + 1, "Philippines"), "Philippines", "#FFFFFF"),
            pin(*GUAM, K(c + 1, "Guam"), "Guam", "#FFD84A", size=56)],
      arcs=[arcp(TRENCH, K(c + 1, "scar"), 2.4, col="#FF3B30", rad=.006, lift=.01)])
t = T(c + 2, -.15)
terrain("T_length", t, [[t, 145.0, 13.0, 18.0, 62, -10], [T(c + 2, 1), 145.5, 15.5, 15.0, 55, 10]],
        routes=[{"pts": TRENCH, "rad": .06, "col": "#FF3B30", "draw": [[t + .3, 0], [t + 2.6, 1]]}],
        layers=[lab("~2,550 km long", K(c + 2, "two and a half"), size=96, box="#222222")])
t = T(c + 3, -.15)
terrain("T_deep", t, [[t, 143.5, 12.0, 9.0, 50, -20], [T(c + 3, 1), CD[0], CD[1] + .25, 5.5, 52, 10]],
        pins=[tpin(*CD, K(c + 3, "Challenger"), "Challenger Deep", "#FFD84A", size=56)],
        layers=[depth(K(c + 3, "eleven"), "~10,935 m")])
plate(T(c + 4, -.15), a("mt_everest"), layers=[lab("Mount Everest  8,849 m", K(c + 4, "Everest"), size=80, box="#222222")], zoom=(1.0, 1.1))
quip(c + 5, [imgcard(arc("everest"), 1500, 800, 560, T(c + 5, -.1), framed=True)])
plate(T(c + 6, -.15), a("mt_everest"), layers=[lab("Still ~2 km under water", K(c + 6, "two"), size=90, box="#d6423a")], zoom=(1.1, 1.35), c=(.5, .3))
board(T(c + 7, -.15), [txt("How does a hole\nthis big exist?", 1250, 600, T(c + 7, .05), size=96, box="#222222")])
plate(T(c + 8, -.15), a("mt_plates"), layers=[tag("Pacific Plate", K(c + 8, "Pacific"), x=1450, y=330), tag("Mariana Plate", K(c + 8, "Mariana Plate"), x=500, y=330)],
      zoom=(1.0, 1.12))
plate(T(c + 9, -.15), a("mt_plates"), layers=[lab("The trench", K(c + 9, "valley"), size=96, box="#d6423a")], zoom=(1.2, 1.45), c=(.5, .45))
quip(c + 10)
board(T(c + 11, -.15), [txt("A few cm / year", 1250, 420, K(c + 11, "few"), size=96, box="#0b3a5a"),
                        txt("= fingernail speed", 1250, 680, K(c + 11, "fingernails"), size=80, box="#222222")])
chapter_card(2, c + 12)

# ======================= CHAPTER 2: WHERE THE LIGHT DIES =======================
c = CHAP[2]
plate(T(c, -.1), a("mt_surface"), layers=[depth(T(c, .1), 0)], zoom=(1.0, 1.2), c=(.5, .7))
plate(T(c + 1, -.15), a("mt_twilight"), layers=[depth(T(c + 1, .1), 50), tag("Sunlight fades fast", K(c + 1, "sunlight"), y=330)], zoom=(1.0, 1.12))
plate(T(c + 2, -.15), a("mt_twilight"), layers=[depth(T(c + 2, .05), 200), tag("Red → Yellow → Green → Blue", K(c + 2, "Red"), y=330)], zoom=(1.15, 1.35))
plate(T(c + 3, -.15), a("mt_midnight"), layers=[depth(T(c + 3, .05), 1000), lab("NO SUNLIGHT", K(c + 3, "gone"), size=110, box="#222222")], zoom=(1.0, 1.1))
quip(c + 4)
photo(T(c + 5, -.15), "atolla", [lab("Bioluminescence", K(c + 5, "bioluminescence"), size=96)])
photo(T(c + 6, -.15), "jelly_biolum", [tag("Jellyfish flash blue", K(c + 6, "Jellyfish"), y=330)])
photo(K(c + 6, "anglerfish"), "anglerfish", [tag("The anglerfish's lure", K(c + 6, "anglerfish") + .1, y=330)], zoom=(1.0, 1.25))
creature_talk(c + 7, "SNAILFISH", "mt_midnight")
skit(c + 8, c + 8, "mt_midnight", {"TRAVELLER": (700, False)})
plate(T(c + 9, -.15), a("mt_midnight"), layers=[depth(T(c + 9, .05), 1000), tag("10 more km to go", K(c + 9, "ten"), y=330)], zoom=(1.3, 1.0))
chapter_card(3, c + 10)

# ======================= CHAPTER 3: THE WEIGHT OF THE OCEAN =======================
c = CHAP[3]
plate(T(c, -.1), a("mt_midnight"), layers=[lab("The real monster", T(c, .3), size=96)], zoom=(1.0, 1.12))
board(T(c + 1, -.15), [txt("PRESSURE", 1250, 600, K(c + 1, "pressure"), size=150, box="#d6423a")])
board(T(c + 2, -.15), [txt("Surface = 1 atmosphere", 1250, 600, K(c + 2, "atmosphere"), size=84, box="#0b3a5a")])
board(T(c + 3, -.15), [txt("Every 10 m down", 1250, 420, K(c + 3, "Every"), size=84, box="#222222"), txt("+1 atmosphere", 1250, 680, K(c + 3, "add"), size=96, box="#0b3a5a")])
board(T(c + 4, -.15), [txt(">1,000 atmospheres", 1250, 600, K(c + 4, "thousand"), size=110, box="#d6423a")])
board(T(c + 5, -.15), [txt(">7 tonnes", 1250, 380, K(c + 5, "seven"), size=120, box="#d6423a"), txt("on every square inch", 1250, 620, K(c + 5, "square"), size=72, box="#222222"),
                       txt("🐘 on your thumbnail", 1250, 840, K(c + 5, "elephant"), size=70, box="#222222")])
quip(c + 6)
plate(T(c + 7, -.15), a("mt_floor"), layers=[tag("Lungs", K(c + 7, "Lungs"), x=600, y=330), tag("Bottles", K(c + 7, "bottles"), x=960, y=480),
                                             tag("Submarines", K(c + 7, "submarines"), x=1350, y=330)], zoom=(1.0, 1.15))
photo(K(c + 8, "1960"), "trieste_hoist", [lab("1960", K(c + 8, "1960"), x=300, y=230, size=110)])
chapter_card(4, c + 9)

# ======================= CHAPTER 4: THE FIRST TWO MEN =======================
c = CHAP[4]
photo(T(c, -.1), "trieste_1960", [lab("TRIESTE", K(c, "Trieste"), size=120)])
plate(T(c + 1, -.15), a("mt_trieste"), layers=[tag("Float full of petrol", K(c + 1, "petrol"), y=330), tag("Steel crew sphere", K(c + 1, "steel ball"), y=480)],
      zoom=(1.0, 1.15))
photo(T(c + 2, -.15), "trieste_crew", [tag("Jacques Piccard", K(c + 2, "Piccard"), x=600, y=330), tag("Don Walsh", K(c + 2, "Walsh"), x=1350, y=330)])
t = T(c + 3, -.15)
terrain("T_dive1960", t, [[t, CD[0], CD[1], 10.0, 70, 0], [T(c + 3, 1), CD[0], CD[1] + .25, 5.5, 52, 25]],
        pins=[tpin(*CD, T(c + 3, .3), "Challenger Deep", "#FFD84A")], layers=[lab("23 Jan 1960", K(c + 3, "twenty-third"), x=330, y=230, size=90)])
plate(T(c + 4, -.15), a("mt_trieste"), layers=[tag("~5 hours down", K(c + 4, "five"), y=330), depth(K(c + 4, "nine"), "~9,000 m")], zoom=(1.1, 1.3))
b = plate(T(c + 5, -.1), a("mt_trieste"), layers=[lab("BANG", K(c + 5, "bang"), size=160, box="#d6423a")], zoom=(1.4, 1.5)); b["cut"] = "flash"
quip(c + 6)
board(T(c + 7, -.15), [txt("A WINDOW CRACKED", 1250, 450, K(c + 7, "cracked"), size=100, box="#d6423a"), txt("1,000 atmospheres outside", 1250, 700, K(c + 7, "thousand"), size=70, box="#222222")])
plate(T(c + 8, -.15), a("mt_trieste"), layers=[lab("They kept going", K(c + 8, "kept"), size=100)], zoom=(1.0, 1.2), c=(.5, .6))
plate(T(c + 9, -.15), a("mt_floor"), layers=[lab("THE BOTTOM", K(c + 9, "touched"), size=110, box="#c99400"), depth(T(c + 9, .1), "~10,900 m")], zoom=(1.0, 1.12))
plate(T(c + 10, -.15), a("mt_floor"), layers=[tag("~20 minutes", K(c + 10, "twenty"), y=330), tag("Mud cloud: barely any view", K(c + 10, "mud"), y=480)], zoom=(1.2, 1.4))
quip(c + 11)
board(T(c + 12, -.15), [txt("52 years", 1250, 600, K(c + 12, "fifty"), size=140, box="#222222")])
photo(T(c + 13, -.15), "deepsea_challenger", [lab("2012", K(c + 13, "2012"), x=300, y=230, size=110), tag("James Cameron, solo", K(c + 13, "Cameron"), y=430)])
board(T(c + 14, -.15), [txt("Moon: 12 people", 1250, 420, K(c + 14, "Twelve"), size=96, box="#222222"), txt("Challenger Deep (to 2019): 3", 1250, 680, K(c + 14, "three"), size=80, box="#d6423a")])
plate(T(c + 15, -.15), a("mt_floor"), layers=[lab("Something unexpected", K(c + 15, "nobody"), size=90)], zoom=(1.0, 1.15))
chapter_card(5, c + 16)

# ======================= CHAPTER 5: SOMETHING IS ALIVE DOWN HERE =======================
c = CHAP[5]
b = board(T(c, -.1), [txt("LIFE", 1250, 600, T(c, .05), size=170, box="#2f8f4f")]); b["cut"] = "flash"
plate(T(c + 1, -.15), a("mt_floor"), layers=[tag("No sunlight", K(c + 1, "No sunlight"), x=500, y=330), tag("Freezing", K(c + 1, "Freezing"), x=960, y=480),
                                             tag("Crushing pressure", K(c + 1, "Crushing"), x=1400, y=330)], zoom=(1.0, 1.15))
photo(T(c + 2, -.15), "snailfish", [lab("The snailfish", K(c + 2, "snailfish"), size=100)])
creature_talk(c + 3, "SNAILFISH", "mt_floor")
board(T(c + 4, -.15), [txt("Soft bones", 1250, 330, K(c + 4, "bones"), size=84, box="#222222"), txt("No air bladder", 1250, 560, K(c + 4, "swim"), size=84, box="#222222"),
                       txt("Pressure-proof proteins", 1250, 790, K(c + 4, "molecules"), size=72, box="#0b3a5a")])
t = T(c + 5, -.15)
globe("G_japan", t, [[t, 145, 18, 2.4], [T(c + 5, 1), 142, 29, 1.9]],
      pins=[pin(*IZU, K(c + 5, "trench just"), "Izu-Ogasawara Trench", "#FFD84A", size=50), pin(*CD, t + .3, "Mariana", "#FF3B30", size=44)],
      layers=[depth(K(c + 5, "eight"), 8336), lab("Deepest fish ever filmed", K(c + 5, "deepest"), y=230, size=76, box="#222222")])
board(T(c + 6, -.15), [txt("Below ~8,200 m:\nno fish", 1250, 600, K(c + 6, "Below"), size=90, box="#222222")])
creature_talk(c + 7, "AMPHIPOD", "mt_floor")
photo(T(c + 8, -.15), "amphipod", [lab("Amphipods", K(c + 8, "amphipods"), size=100), tag("Deep-sea gigantism", K(c + 8, "gigantism"), y=430)])
quip(c + 9, [imgcard(arc("amphipod_giant"), 1500, 800, 600, T(c + 9, -.1), framed=True)])
photo(T(c + 10, -.15), "amphipod_giant", [tag("Eats whatever sinks", K(c + 10, "eating"), y=330)], zoom=(1.15, 1.35))
photo(T(c + 11, -.15), "xenophyophore", [lab("Xenophyophores", K(c + 11, "xenophyophores"), size=96), tag("ONE cell, lemon-sized", K(c + 11, "one cell"), y=430)])
photo(T(c + 12, -.15), "deep_holothurian", [lab("Life moves in anywhere", K(c + 12, "anywhere"), size=84)])
plate(T(c + 13, -.15), a("mt_floor"), layers=[], zoom=(1.0, 1.2), c=(.5, .7))
b = plate(T(c + 14, -.1), a("mt_plates"), layers=[lab("UNDERNEATH", K(c + 14, "underneath"), size=130, box="#d6423a")], zoom=(1.3, 1.5), c=(.5, .7)); b["cut"] = "flash"
chapter_card(6, c + 15)

# ======================= CHAPTER 6: THE TRENCH THAT DRINKS THE OCEAN =======================
c = CHAP[6]
t = T(c, -.1)
terrain("T_slab", t, [[t, 147.0, 16.0, 14.0, 35, 80], [T(c + 1, 1), 146.5, 14.5, 10.0, 25, 110]],
        routes=[{"pts": TRENCH, "rad": .05, "col": "#FF3B30", "draw": [[0, 1]]}], layers=[tag("Pacific Plate → under", T(c, .3), y=330)])
plate(T(c + 2, -.15), a("mt_water"), layers=[tag("Cracks", K(c + 2, "cracks"), x=600, y=330), tag("Seawater seeps in", K(c + 2, "seeps"), x=1350, y=330),
                                             tag("Carried down", K(c + 2, "carried"), x=960, y=480)], zoom=(1.0, 1.2))
quip(c + 3)
photo(T(c + 4, -.15), "ocean_seismometer", [lab("2018", K(c + 4, "2018"), x=300, y=230, size=110)])
photo(T(c + 5, -.15), "ocean_seismometer", [tag("19 sea-floor seismometers", K(c + 5, "nineteen"), y=330), tag("Listening for 1+ year", K(c + 5, "year"), y=480)], zoom=(1.2, 1.4))
plate(T(c + 6, -.15), a("mt_water"), layers=[lab("~30 km deep", K(c + 6, "thirty"), size=110, box="#0b3a5a")], zoom=(1.2, 1.4), c=(.5, .7))
board(T(c + 7, -.15), [txt("Mariana: ~4× more water", 1250, 420, K(c + 7, "four"), size=84, box="#d6423a"), txt("Worldwide: ~3× more", 1250, 680, K(c + 7, "three"), size=84, box="#222222"),
                       txt("(estimate, WashU 2018)", 1250, 860, K(c + 7, "estimated"), size=48, box="#222222")])
quip(c + 8)
plate(T(c + 9, -.15), a("mt_water"), layers=[tag("Sea levels: steady", K(c + 9, "steady"), y=330), tag("Volcanoes + vents send it back", K(c + 9, "volcanoes"), y=480)], zoom=(1.0, 1.15))
t = T(c + 10, -.15)
terrain("T_eifuku", t, [[t, 145.0, 18.0, 14.0, 55, 0], [T(c + 11, 1), EIFUKU[0], EIFUKU[1], 4.5, 40, 25]],
        pins=[tpin(*EIFUKU, K(c + 11, "Eifuku"), "NW Eifuku", "#FFD84A", size=56)], layers=[depth(K(c + 11, "one and a half"), "~1,600 m")])
photo(T(c + 12, -.15), "champagne_vent", [lab("Liquid CO₂", K(c + 12, "liquid"), size=110, box="#0b3a5a")])
quip(c + 13, [imgcard(a("mt_champagne"), 1500, 800, 640, T(c + 13, -.1))])
plate(T(c + 14, -.15), a("mt_champagne"), layers=[tag("Acidic water: thin shells", K(c + 14, "acidic"), y=330)], zoom=(1.15, 1.35))
plate(T(c + 15, -.15), a("mt_water"), layers=[tag("Ocean goes IN", K(c + 15, "in"), x=600, y=330), tag("Planet breathes OUT", K(c + 15, "out"), x=1350, y=330)], zoom=(1.0, 1.12))
plate(T(c + 16, -.15), a("mt_plastic"), layers=[lab("A bigger problem", K(c + 16, "bigger"), size=96, box="#d6423a")], zoom=(1.0, 1.15))
chapter_card(7, c + 17)

# ======================= CHAPTER 7: WE GOT THERE FIRST =======================
c = CHAP[7]
plate(T(c, -.1), a("mt_plastic"), layers=[], zoom=(1.0, 1.25), c=(.5, .55))
photo(T(c + 1, -.15), "wright_vescovo", [tag("Candy wrappers too", K(c + 1, "candy"), y=330)])
photo(T(c + 2, -.15), "amphipod", [lab("2019", K(c + 2, "2019"), x=300, y=230, size=110), tag("Prof. Alan Jamieson's team", K(c + 2, "Jamieson"), y=430)])
board(T(c + 3, -.15), [imgcard(arc("microplastic"), 1050, 980, 620, T(c + 3, -.1), framed=True), txt("Plastic in their guts", 1560, 380, K(c + 3, "plastic"), size=70, box="#222222"),
                       txt("Mariana: 100%", 1560, 700, K(c + 3, "every single"), size=96, box="#d6423a")])
creature_talk(c + 4, "AMPHIPOD", "mt_plastic")
skit(c + 5, c + 5, "mt_floor", {"TRAVELLER": (700, False)})
plate(T(c + 6, -.15), a("mt_plastic"), layers=[tag("Sinks · Drifts · Breaks up", K(c + 6, "sinks"), y=330), tag("The trench: a giant funnel", K(c + 6, "funnel"), y=480)], zoom=(1.1, 1.3))
t = T(c + 7, -.15)
terrain("T_fingerprint", t, [[t, CD[0], CD[1] + .25, 5.0, 50, 40], [T(c + 7, 1), CD[0], CD[1] + .4, 8.0, 60, 70]],
        pins=[tpin(*CD, t + .2, "Our fingerprints", "#FF3B30", size=56)])

# ======================= ENDING =======================
c = CHAP[99]
t = T(c, -.1)
terrain("T_outro", t, [[t, 145.0, 15.5, 16.0, 60, -30], [T(c + 2, 1), 145.0, 14.0, 24.0, 70, 20]],
        routes=[{"pts": TRENCH, "rad": .05, "col": "#FF3B30", "draw": [[0, 1]]}])
plate(T(c + 1, -.15), a("mt_everest"), layers=[tag("Swallows Everest", K(c + 1, "Everest"), y=330)], zoom=(1.0, 1.1))
plate(K(c + 1, "light dies"), a("mt_midnight"), layers=[], zoom=(1.0, 1.15))
plate(K(c + 1, "window"), a("mt_trieste"), layers=[], zoom=(1.2, 1.35))
plate(K(c + 1, "fish glow"), a("mt_floor"), layers=[], zoom=(1.0, 1.15))
plate(T(c + 2, -.15), a("mt_water"), layers=[tag("Drinking the ocean… breathing it out", K(c + 2, "drinking"), y=330)], zoom=(1.0, 1.12))
plate(T(c + 3, -.15), a("mt_floor"), layers=[lab("Most of the deep sea: never seen", K(c + 3, "never"), size=80, box="#222222")], zoom=(1.0, 1.2))
quip(c + 4)
plate(T(c + 5, -.15), a("mt_surface"), layers=[], zoom=(1.0, 1.12))
board(T(c + 6, -.15), [txt("SUBSCRIBE · BHUGOL", 1250, 450, K(c + 6, "subscribe"), size=96, box="#d6423a"), txt("Would YOU go down?", 1250, 700, K(c + 6, "would"), size=84, box="#222222")])
quip(c + 7)
# ======================= close the timeline =======================
shots.sort(key=lambda s: s["t0"])
for k, s in enumerate(shots[:-1]):
    if any("chapter" in str(L_.get("img")) for L_ in s["layers"]):
        s["t0"] = max(0.0, s["t0"]); hold = s["t0"] + 2.4
        for n in shots[k + 1:]:
            if n["t0"] < hold: n["t0"] = hold
shots.sort(key=lambda s: s["t0"])
shots[:] = [s for s, n in zip(shots, shots[1:] + [None]) if not n or n["t0"] - s["t0"] > .25]
shots[0]["t0"] = 0.0   # the video's first frame is 0:00, same as the audio (else pictures + captions run early)
for s, n in zip(shots, shots[1:] + [None]): s["t1"] = n["t0"] if n else END
for s in shots:
    cam = s["bg"].get("cam")
    if not cam: continue
    for k in cam:
        z = max(k[3], 1.0); lo, hi = .5 / z, 1 - .5 / z
        k[1] = min(max(k[1], lo), hi); k[2] = min(max(k[2], lo), hi)
    if len(cam) >= 2: cam[-1][0] = max(cam[-1][0], s["t1"])
    else: cam.append([s["t1"], cam[0][1], cam[0][2], cam[0][3] * 1.06])
    if all(abs(cam[0][q] - cam[-1][q]) < 1e-3 for q in (1, 2, 3)): cam[-1][3] = cam[0][3] * 1.06
# long still shots: split into two framings (hard cut to a tighter crop) so the picture changes at least every ~6 s
import copy
def split_long(maxlen=6.5):
    out = []
    for s in shots:
        d = s["t1"] - s["t0"]; b = s["bg"]
        if d <= maxlen or s.get("clip") or "video" in b or not b.get("cam") or b.get("blur") or str(b.get("img", "")).startswith("#"):
            out.append(s); continue
        n = int(d // 5.0); seg = d / (n + 1)
        for k in range(n + 1):
            a0, a1 = s["t0"] + seg * k, s["t0"] + seg * (k + 1)
            if k == 0:
                s2 = copy.deepcopy(s); s2["t1"] = a1; s2["bg"]["cam"] = [[a0, .5, .5, b["cam"][0][3]], [a1, .5, .5, b["cam"][0][3] * 1.06]]
                s2["layers"] = [L_ for L_ in s["layers"] if L_.get("in", a0) < a1]
            else:
                z = 1.35 if k % 2 else 1.15; cx, cy = (.38, .45) if k % 2 else (.62, .5)
                s2 = {"t0": a0, "t1": a1, "bg": dict(copy.deepcopy(b), cam=[[a0, cx, cy, z], [a1, cx + (.04 if k % 2 else -.04), cy, z * 1.05]]), "cut": "hard",
                      "layers": []}
                for L_ in s["layers"]:
                    t_in = L_.get("in", s["t0"]); t_out = L_.get("out", 1e9)
                    if t_out <= a0 or t_in >= a1: continue
                    L2 = copy.deepcopy(L_)
                    if t_in < a0: L2["in"] = a0; L2["enter"] = "none"
                    s2["layers"].append(L2)
            out.append(s2)
    return out
shots[:] = split_long()
for s in shots:
    cam = s["bg"].get("cam")
    if cam:
        for k in cam:
            z = max(k[3], 1.0); lo, hi = .5 / z, 1 - .5 / z
            k[1] = min(max(k[1], lo), hi); k[2] = min(max(k[2], lo), hi)
# 3D clips: local times; camera runs to the end of the shot
clips_out = {}
for s in shots:
    cid = s.get("clip")
    if not cid: continue
    t0 = s["t0"]; mode = CLIP[cid]["data"]["mode"]; G = CLIP[cid]["data"][mode]; dur = round(s["t1"] - t0 + .6, 3)
    loc = lambda x: round(max(0.0, x - t0), 3)
    G["cam"] = [[loc(k[0])] + k[1:] for k in G["cam"]]; G["cam"][-1][0] = max(G["cam"][-1][0], dur - .6)
    def fit(K):     # keyframes in local time, shifted earlier if the event would finish after the shot ends
        K = [[loc(k[0]) if k[0] else 0, k[1]] for k in K]
        over_ = K[-1][0] - (dur - 1.0)
        if over_ > 0 and len(K) > 1: K = [K[0]] + [[max(0.0, round(k[0] - over_, 3)), k[1]] for k in K[1:]]
        return K
    for o in G.get("over", []): o["a"] = fit(o["a"])
    for x in G.get("routes", []): x["draw"] = fit(x["draw"])
    for x in G.get("arcs", []):
        x["draw"] = fit(x["draw"])
        if "fade" in x: x["fade"] = fit(x["fade"])
    for p in G["pins"]: p["at"] = min(loc(p["at"]), round(dur - 1.6, 3))
    clips_out[cid] = dict(CLIP[cid]["data"], dur=dur)
json.dump(clips_out, open(os.path.join(os.path.dirname(os.path.abspath(args[1])), "clips3d.json"), "w"), indent=1)

# ======================= retention pass =======================
punch, shake, fx = [], [], []
def text_of(L_): return L_["img"]["text"] if isinstance(L_.get("img"), dict) else ""
for k, s in enumerate(shots):
    s["cut"] = s.get("cut") or "curve"
    if any("chapter" in str(L_.get("img")) for L_ in s["layers"]): s["cut"] = "zoom"
    elif s.get("clip") and k and not shots[k - 1].get("clip"): s["cut"] = "whip"
for s in shots:   # big years and numbers slam in
    for L_ in s["layers"]:
        tx_ = text_of(L_)
        if re.fullmatch(r"~?\d{3,4}s?( BCE)?", tx_):
            L_["enter"] = "slam"; shake.append([L_["in"], .35, 8]); fx.append(["thud", L_["in"], -14])
# chapter cards and key shocks: a flash cut
for s in shots:
    if any(x in " ".join(text_of(L_) for L_ in s["layers"]) for x in ("THE MARIANA TRENCH", "A PLASTIC BAG", "PRESSURE", "A WINDOW CRACKED")):
        s["cut"] = "flash"
for s in shots:   # labels never sit in the caption band
    for L_ in s["layers"]:
        if isinstance(L_.get("img"), dict) and L_["y"] > 860: L_["y"] = 250

# captions from the script words, timed by the transcriber
sys.path.insert(0, os.path.join(HERE, "..", "russia", "full")); from numwords import digits as _digits
IN_NUM = [("eight thousand three hundred and thirty-six metres", "8,336 metres"), ("two and a half thousand kilometres", "2,500 kilometres"), ("one thousand atmospheres", "1,000 atmospheres"),
          ("a thousand atmospheres", "1,000 atmospheres"), ("one thousand metres", "1,000 metres"), ("two hundred metres", "200 metres"), ("twenty-third of January", "23rd of January"),
          ("eleven kilometres", "11 kilometres"), ("two kilometres", "2 kilometres"), ("nine kilometres", "9 kilometres"), ("thirty kilometres", "30 kilometres"),
          ("ten kilometres", "10 kilometres"), ("fifty-two years", "52 years"), ("twenty minutes", "20 minutes"), ("seven tonnes", "7 tonnes"), ("five hours", "5 hours")]
def digits(text):
    for a_, b_ in IN_NUM: text = re.sub(re.escape(a_), b_, text, flags=re.I)
    return _digits(text)
Wt = [(float(x) / SPEED, float(y) / SPEED, w.strip()) for x, y, w in (l.split(None, 2) for l in open(WORDS) if l.strip())]
STOP = {"and", "the", "a", "an", "of", "to", "in", "on", "it", "is"}
def norm(w): return re.sub(r"[^a-z0-9']", "", w.lower())
caps = []
for i, ln in enumerate(L):
    if SPK[i] != "N": continue
    text = digits(re.sub(r"\[[^\]]*\]", "", SCRIPT[i]).replace("‡", ""))
    toks = text.split(); keys = [False] * len(toks); inside = False
    for k, t_ in enumerate(toks):
        if t_.startswith("*"): inside = True
        keys[k] = inside and norm(t_) not in STOP
        if t_.rstrip(".,!?;:\"").endswith("*"): inside = False
    toks = [t_.replace("*", "") for t_ in toks]
    ws = [w for w in Wt if ln["t0"] - .1 <= w[0] < ln["t1"] + .1]
    sm = difflib.SequenceMatcher(None, [norm(x) for x in toks], [norm(w[2]) for w in ws], autojunk=False)
    tim = [None] * len(toks)
    for a_, b_, n_ in sm.get_matching_blocks():
        for q in range(n_): tim[a_ + q] = (ws[b_ + q][0], ws[b_ + q][1])
    known = [k for k, v in enumerate(tim) if v]
    for k in range(len(toks)):
        if tim[k]: continue
        lo = max([q for q in known if q < k], default=None); hi = min([q for q in known if q > k], default=None)
        t_lo = tim[lo][1] if lo is not None else ln["t0"]; t_hi = tim[hi][0] if hi is not None else ln["t1"]
        span = (hi if hi is not None else len(toks)) - (lo if lo is not None else -1)
        f = (k - (lo if lo is not None else -1)) / span; s_ = t_lo + (t_hi - t_lo) * (f - 1 / span) if span else t_lo
        tim[k] = (s_, s_ + (t_hi - t_lo) / max(span, 1))
    chunk = []
    for k, w in enumerate(toks):
        chunk.append([w, tim[k][0], tim[k][1], keys[k]])
        if len(chunk) >= 4 or w[-1:] in ".,!?;:" or k == len(toks) - 1:
            caps.append({"t0": chunk[0][1] - .05, "t1": chunk[-1][2] + .25, "words": chunk}); chunk = []
# snap subtitle words that start inside a pause to where the voice actually starts (word timings can include the silence
# before a word, or drift a little inside a phrase). One ordered pass over all words: no word starts before the previous
# word ends, then each chunk's start/end is rebuilt from its words.
try:
    import librosa as _lr, numpy as _np
    _vp = os.path.join(os.path.dirname(os.path.abspath(WORDS)), "voice_en.wav")
    _y, _sr = _lr.load(_vp, sr=16000); _r = _lr.feature.rms(y=_y, frame_length=320, hop_length=160)[0]; _thr = 0.008
    _moved, _prev = 0, -1.0
    for c_ in caps:
        for w_ in c_["words"]:
            i = int(w_[1] * 100)
            if i < len(_r) and _r[i:i + 6].max() < _thr:                      # starts in a pause: move to the voice onset (max 1.2 s)
                j = i
                while j < min(len(_r), i + 120) and _r[j] < _thr: j += 1
                if j < i + 120: w_[1] = j / 100; _moved += 1
            w_[1] = max(w_[1], _prev); w_[2] = max(w_[2], w_[1] + .1); _prev = w_[2]
    for k_, c_ in enumerate(caps):
        c_["t0"] = c_["words"][0][1] - .05
        if k_: c_["t0"] = max(c_["t0"], caps[k_ - 1]["words"][-1][2])
        c_["t1"] = c_["words"][-1][2] + .25
    print("subtitle words snapped to voice onset:", _moved)
except Exception as e_: print("snap skipped:", e_)
for x, y in zip(caps, caps[1:]): x["t1"] = min(x["t1"], y["t0"])
_m = []                                                            # a chunk shown for < 0.35 s would flash: merge it into the next one
for c_ in caps:
    if _m and _m[-1]["t1"] - _m[-1]["t0"] < .35 and len(_m[-1]["words"]) + len(c_["words"]) <= 6:
        c_ = {"t0": _m[-1]["t0"], "t1": c_["t1"], "words": _m.pop()["words"] + c_["words"]}
    _m.append(c_)
caps[:] = _m


# punch-in every PUNCH seconds (approved look), nudged off cuts
cuts = [s["t0"] for s in shots]
t = 2.0
while t < END - 1:
    tt = t
    if min(abs(tt - c_) for c_ in cuts) < .3: tt += .7
    punch.append([round(tt, 2), 1.075]); t += PUNCH

json.dump({"w": 1920, "h": 1080, "fps": 30, "shots": shots, "punch": punch, "shake": shake, "captions": caps, "fx": fx}, open(args[1], "w"), indent=1)
gaps = [round(s["t1"] - s["t0"], 1) for s in shots]
print(len(shots), "shots; mean", round(sum(gaps) / len(gaps), 1), "s; longest", max(gaps), "s; end", round(END, 1), "| clips", len(clips_out),
      "| punches", len(punch), "| captions", len(caps))
miss = sorted({s["bg"]["img"] for s in shots if isinstance(s["bg"]["img"], str) and s["bg"]["img"].startswith("#") and not s.get("clip")})
print("placeholder bgs:", len([s for s in shots if str(s["bg"].get("img")) .startswith("#") and not s.get("clip")]))
