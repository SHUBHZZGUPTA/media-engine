#!/usr/bin/env python3
"""Shot plan for the India pilot (hook + chapter 1). Helpers, timeline close and retention pass follow russia/full/plan_full.py.

Shots are pinned to script LINES (index into script_en.md), never to fixed seconds.
Usage: python3 plan_pilot.py lines.json spec.json words.txt [speed] [--punch=7]
Also writes clips3d.json (3D globe clips, local times) next to spec.json.
"""
import json, sys, os, re, textwrap, difflib
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..", "..", "..")
A1 = os.path.join(HERE, "..", "art"); A2 = A1; C1 = os.path.join(HERE, "cards"); C2 = C1
ARC = os.path.join(ROOT, "outputs", "fetch", "in-pilot-archive"); CLIPS = os.path.join(HERE, "clips3d")
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
def a(n):
    for d in (A2, A1):
        p = os.path.join(d, n + ".png")
        if os.path.exists(p): return p
    return None
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
CAST = {"INSPECTOR": "c_inspector", "BRICKMAKER": "c_brickmaker", "FOREMAN": "c_foreman", "ENGINEER": "c_engineer", "TRAVELLER": "c_traveller"}
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

# ======================= HOOK =======================
c = CHAP[0]
t = T(c, -.1)
globe("G_world", t, [[t, -10, 20, 3.7], [T(c, 1), 45, 18, 3.3]],
      layers=[lab("1700", T(c, .03), x=300, y=230, size=110), txt("¼ of the world's\neconomy", 1450, 300, K(c, "quarter"), size=80, box="#c99400")])
board(T(c + 1, -.15), [txt("Britain  ✗", 1250, 380, K(c + 1, "Britain"), size=86, box="#222222"),
                       txt("China  ✗", 1250, 580, K(c + 1, "China"), size=86, box="#222222"),
                       txt("America  ✗", 1250, 780, K(c + 1, "America"), size=86, box="#222222")])
t = T(c + 2, -.2)
globe("G_india", t, [[t, 66, 18, 3.0], [K(c + 3, "Ships"), 79, 22, 2.2]],
      over=[ove("ov_in_edge", fadein(t + .1, 1, .5)), ov("ov_in_flag", fadein(t + .7, .85, .7))],
      layers=[lab("INDIA", T(c + 2, .1), size=130), tag("Spices", K(c + 3, "Spices"), x=1560, y=330), tag("Cotton", K(c + 3, "cotton"), x=1560, y=470),
              tag("Steel", K(c + 3, "steel"), x=1560, y=610), tag("Diamonds", K(c + 3, "diamonds"), x=1560, y=750)])
plate(K(c + 3, "Ships"), a("in_bazaar"), layers=[lab("Ships from across the world", K(c + 3, "Ships") + .1, size=72, box="#222222")], zoom=(1.0, 1.15), c=(.4, .45))
plate(T(c + 4, -.15), a("in_bazaar"), layers=[traveller(talks=[c + 4], x=420), say(c + 4, 900, 330)], zoom=(1.1, 1.2), c=(.6, .5))
board(T(c + 5, -.15), [txt("Sone ki Chidiya", 1250, 450, K(c + 5, "Sone"), size=110, box="#c99400"),
                       txt("THE GOLDEN BIRD", 1250, 700, K(c + 5, "Golden"), size=96, box="#222222")])
quip(c + 6)
board(T(c + 7, -.15), [imgcard(card("bars"), 1200, 900, 1100, T(c + 7, -.1)), txt("~4%", 1500, 300, K(c + 7, "four"), size=130, box="#d6423a")])
quip(c + 8)
seq(c + 9, [("And here", "Not the first time"), ("rich", "Rich"), ("robbed", "Robbed"), ("rebuilt", "Rebuilt"), ("five", "5,000 years")], size=110)
G = [("Over", "City-builders\nnobody can name", "priest_king"), ("an emperor", "An emperor who\ngave up war", None), ("sultans", "Sultans", None),
     ("Mughals", "Mughals", None), ("company", "A company?!", None), ("its own", "Its own people", None)]
for k, (w, s, key) in enumerate(G):
    t0 = T(c + 10, -.15) if k == 0 else K(c + 10, w)
    lay = [txt(s, 1250, 300 if key else 600, t0 + .05, size=80, box="#222222")]
    if key: lay.append(imgcard(arc(key), 1250, 760, 420, t0 + .05, framed=True))
    b = board(t0, lay); b["cut"] = "hard" if k else "curve"
quip(c + 11)
board(T(c + 12, -.15), [txt("The same story", 1250, 600, K(c + 12, "same"), size=110, box="#d6423a")])
for k, (w, n) in enumerate([("stitches", 1), ("shines", 2), ("shatters", 3)]):
    t0 = T(c + 13, -.15) if k == 0 else K(c + 13, w); cycle(t0, n)
cycle(K(c + 14, "absorbs"), 4, [txt("Invaders → Indians", 1250, 230, K(c + 14, "eating"), size=70, box="#222222")])
board(T(c + 15, -.15), [imgcard(card("cycle4"), 1210, 1010, 1120, T(c + 15, -.15))])
board(T(c + 16, -.15), [txt("Richest  →  Lost it all  →  Climbing back", 1150, 600, T(c + 16, .05), size=64, box="#222222")])
quip(c + 17)
chapter_card(1, c + 18)

# ======================= CHAPTER 1: THE CITY NOBODY CAN READ =======================
c = CHAP[1]
HAR, MOH, DHO, LOT, RAK = (72.86, 30.63), (68.14, 27.33), (70.21, 23.89), (72.25, 22.52), (76.12, 29.29)
plate(T(c, -.15), a("in_indus"), layers=[lab("~2500 BCE", T(c, .03), x=330, y=230, size=100), tag("Egypt: building pyramids", K(c, "Egypt"), y=420)],
      zoom=(1.0, 1.15), c=(.5, .45))
t = K(c, "Indus River")
globe("G_indus", t, [[t, 74, 24, 2.6], [K(c + 1, "huge"), 69, 27, 1.75]],
      over=[ove("ov_in_edge", [[0, .45]]), ov("ov_indus", fadein(K(c, "Pakistan"), .85, .8)), ove("ov_indus_edge", fadein(K(c, "Pakistan"), 1, .8))],
      layers=[tag("Today: Pakistan + NW India", K(c, "Pakistan"), x=1400, y=300), lab("Indus Valley Civilisation", K(c + 1, "Indus"), y=200, size=80)])
board(K(c + 1, "huge"), [txt("HUGE", 1250, 330, K(c + 1, "huge"), size=120, box="#d6423a"),
                          txt("Bigger than\nEgypt + Mesopotamia\ncombined", 1250, 680, K(c + 1, "more land"), size=72, box="#222222")])
t = T(c + 2, -.15)
globe("G_cities", t, [[t, 70, 27, 1.75], [T(c + 2, 1), 70.5, 27.5, 1.6]],
      over=[ove("ov_in_edge", [[0, .45]]), ov("ov_indus", [[0, .85]]), ove("ov_indus_edge", [[0, 1]])],
      pins=[pin(*HAR, K(c + 2, "Harappa"), "Harappa", "#FFD84A"), pin(*MOH, K(c + 2, "Mohenjo"), "Mohenjo-daro", "#FFD84A")],
      layers=[tag("Tens of thousands of people", K(c + 2, "tens"), x=1400, y=900 - 600)])
pic(T(c + 3, -.15), "mohenjo_ruins", [lab("Weirdly modern", K(c + 3, "modern"), size=100)])
plate(T(c + 4, -.15), a("in_street"), layers=[lab("Straight streets", K(c + 4, "Streets"), size=90), tag("Same-size bricks", K(c + 4, "same"), y=420)],
      zoom=(1.0, 1.15), c=(.5, .5))
plate(T(c + 5, -.15), a("in_street"), layers=[lab("Private bathrooms", K(c + 5, "bathroom"), size=84),
                                             tag("Covered drains", K(c + 5, "covered"), x=600, y=420)], zoom=(1.15, 1.45), c=(.3, .62))
skit(c + 6, c + 7, "in_street", {"TRAVELLER": (760, False)})
pic(T(c + 8, -.15), "great_bath", [lab("The Great Bath", K(c + 8, "Great"), size=96), tag("Sealed with tar", K(c + 8, "tar"), y=420)])
plate(T(c + 9, -.15), a("in_bath"), layers=[tag("Ceremonies?", K(c + 9, "ceremonies"), x=600, y=300), tag("Fancy pool?", K(c + 9, "swimming"), x=1350, y=300)],
      zoom=(1.0, 1.15))
skit(c + 10, c + 14, "in_street", {"INSPECTOR": (600, False), "BRICKMAKER": (1340, True)})
pic(T(c + 15, -.15), "indus_weights", [lab("Standard weights", K(c + 15, "standard"), size=90)])
t = T(c + 16, -.15)
globe("G_trade", t, [[t, 66, 25, 2.2], [T(c + 16, 1), 58, 27, 2.6]],
      over=[ov("ov_indus", [[0, .8]]), ove("ov_indus_edge", [[0, 1]])],
      arcs=[arcp([[72.25, 22.52], [66.5, 23.5], [58.5, 24.0], [56.3, 26.5], [50.5, 28.7], [46.1, 30.96]], K(c + 16, "far"), 2.4)],
      pins=[pin(*LOT, K(c + 16, "far"), "Lothal", "#FFD84A"), pin(46.1, 30.96, K(c + 16, "Mesopotamia"), "Mesopotamia (Iraq)", "#FF5A3A")])
board(T(c + 17, -.15), [txt("The mystery", 1250, 600, T(c + 17, .05), size=120, box="#d6423a")])
pic(T(c + 18, -.15), "indus_script", [lab("Hundreds of signs", K(c + 18, "Hundreds"), size=90)])
pic(T(c + 19, -.15), "indus_script", [lab("Nobody can read them", K(c + 19, "nobody"), size=96, box="#d6423a")], zoom=(1.3, 1.5))
quip(c + 20, [imgcard(arc("unicorn_seal"), 1500, 760, 560, T(c + 20, -.1), framed=True)])
pic(T(c + 21, -.15), "priest_king", [tag("Their name?  Kings?  Gods?", K(c + 21, "we don't"), y=300), lab("UNKNOWN", K(c + 21, "stories"), y=700, size=110, box="#d6423a")])
pic(T(c + 22, -.15), "harappa_ruins", [lab("No palaces. No royal tombs.", K(c + 22, "palaces"), size=76, box="#222222")])
pic(T(c + 23, -.15), "dholavira", [lab("~1900 BCE", K(c + 23, "nineteen"), x=330, y=230, size=100), tag("The cities emptied", K(c + 23, "emptied"), y=420)])
plate(T(c + 24, -.15), a("in_indus"), layers=[tag("Rivers moved", K(c + 24, "rivers"), y=300), tag("A river dried up", K(c + 24, "drying"), y=450),
                                             tag("Weaker monsoon", K(c + 24, "monsoon"), y=600)], zoom=(1.15, 1.0))
pic(T(c + 25, -.15), "mohenjo_ruins", [lab("Forgotten", K(c + 25, "forgotten"), size=120)], zoom=(1.3, 1.05), c0=(.4, .5))
board(T(c + 26, -.15), [txt("~4,000 years", 1250, 600, T(c + 26, .05), size=120, box="#222222")])
plate(T(c + 27, -.15), a("in_railway"), layers=[lab("A railway?!", K(c + 27, "railway"), size=110)], zoom=(1.0, 1.12))
plate(T(c + 28, -.15), a("in_railway"), layers=[lab("1850s", K(c + 28, "eighteen"), x=300, y=230, size=110), tag("Punjab", K(c + 28, "Punjab"), y=420)],
      zoom=(1.0, 1.1), c=(.4, .5))
plate(T(c + 29, -.15), a("in_railway"), layers=[lab("Harappa", K(c + 29, "Harappa"), size=96), tag("Old, perfect bricks", K(c + 29, "perfect"), y=420)],
      zoom=(1.2, 1.5), c=(.75, .6))
skit(c + 30, c + 32, "in_railway", {"FOREMAN": (520, False), "ENGINEER": (1380, True), "TRAVELLER": (960, False)})
plate(T(c + 33, -.15), a("in_railway"), layers=[lab("Under the tracks", K(c + 33, "under"), size=100)], zoom=(1.0, 1.2), c=(.3, .55))
pic(T(c + 34, -.15), "dancing_girl", [lab("1920s", K(c + 34, "nineteen"), x=300, y=230, size=110),
                                       tag("One of the oldest civilisations", K(c + 34, "oldest"), y=420)])
cycle(T(c + 35, -.15), "shine")
cycle(T(c + 36, -.15), "shatter")
quip(c + 37, [txt("Step 1  ✓", 1500, 230, T(c + 37, .3), size=80, box="#2f8f4f")])
t = T(c + 38, -.15)
globe("G_nw", t, [[t, 76, 26, 2.3], [T(c + 38, 1), 70, 33, 2.0]],
      arcs=[arcp([[66.0, 39.5], [68.5, 36.5], [71.0, 34.0], [73.0, 31.0]], K(c + 38, "northwest"), 2.4, col="#FF8A3A")],
      layers=[tag("Horses  ·  Chariots", K(c + 38, "horses"), y=300)])
board(T(c + 39, -.15), [txt("Sacred hymns", 1250, 380, K(c + 39, "hymns"), size=100, box="#c99400"),
                        txt("Passed down by memory\nfor 3,000+ years", 1250, 660, K(c + 39, "memory"), size=72, box="#222222")])
quip(c + 40)
# ======================= close the timeline =======================
shots.sort(key=lambda s: s["t0"])
for k, s in enumerate(shots[:-1]):
    if any("chapter" in str(L_.get("img")) for L_ in s["layers"]):
        s["t0"] = max(0.0, s["t0"]); hold = s["t0"] + 2.4
        for n in shots[k + 1:]:
            if n["t0"] < hold: n["t0"] = hold
shots.sort(key=lambda s: s["t0"])
shots[:] = [s for s, n in zip(shots, shots[1:] + [None]) if not n or n["t0"] - s["t0"] > .25]
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
    t0 = s["t0"]; G = CLIP[cid]["data"]["globe"]; dur = round(s["t1"] - t0 + .6, 3)
    loc = lambda x: round(max(0.0, x - t0), 3)
    G["cam"] = [[loc(k[0])] + k[1:] for k in G["cam"]]; G["cam"][-1][0] = max(G["cam"][-1][0], dur - .6)
    def fit(K):     # keyframes in local time, shifted earlier if the event would finish after the shot ends
        K = [[loc(k[0]) if k[0] else 0, k[1]] for k in K]
        over_ = K[-1][0] - (dur - 1.0)
        if over_ > 0 and len(K) > 1: K = [K[0]] + [[max(0.0, round(k[0] - over_, 3)), k[1]] for k in K[1:]]
        return K
    for o in G["over"]: o["a"] = fit(o["a"])
    for x in G["arcs"]:
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
    if any(x in " ".join(text_of(L_) for L_ in s["layers"]) for x in ("INDIA", "Nobody can read them", "HUGE")):
        s["cut"] = "flash"
for s in shots:   # labels never sit in the caption band
    for L_ in s["layers"]:
        if isinstance(L_.get("img"), dict) and L_["y"] > 860: L_["y"] = 250

# captions from the script words, timed by the transcriber
sys.path.insert(0, os.path.join(HERE, "..", "..", "russia", "full")); from numwords import digits as _digits
IN_NUM = [("forty-five hundred", "4,500"), ("four and a half thousand", "4,500"), ("nineteen hundred BCE", "1900 BCE"), ("eighteen-fifties", "1850s"),
          ("nineteen-twenties", "1920s"), ("two hundred and fifty", "250"), ("four-thousand-year-old", "4,000-year-old"), ("four thousand", "4,000"),
          ("three hundred", "300"), ("five thousand", "5,000"), ("three thousand", "3,000"), ("four percent", "4%"), ("One to two to four", "1 : 2 : 4")]
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
for x, y in zip(caps, caps[1:]): x["t1"] = min(x["t1"], y["t0"])

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
