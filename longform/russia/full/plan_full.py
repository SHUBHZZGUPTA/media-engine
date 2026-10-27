#!/usr/bin/env python3
"""Shot plan for the Russia full video, chapters 2-11 + ending (the pilot covers hook + chapter 1).

Shots are pinned to script LINES (index into script_full.md), never to fixed seconds.
Usage: python3 plan_full.py lines.json spec.json words.txt [speed] [--punch=7]
Also writes clips3d_full.json (3D globe clips, local times) next to spec.json.
"""
import json, sys, os, re, textwrap, difflib
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..", "..", "..")
A1 = os.path.join(HERE, "..", "art"); A2 = os.path.join(HERE, "..", "art2"); C1 = os.path.join(HERE, "..", "pilot", "cards"); C2 = os.path.join(HERE, "cards")
ARC = os.path.join(ROOT, "outputs", "fetch", "ru-full-archive"); CLIPS = os.path.join(HERE, "clips3d")
STALIN = os.path.join(ROOT, "outputs", "fetch", "ru-pilot-archive-search", "stalin_full.jpg")
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
args = [a for a in sys.argv[1:] if not a.startswith("--")]
L = json.load(open(args[0])); END = L[-1]["t1"] + 2.0
WORDS = args[2]; SPEED = float(args[3]) if len(args) > 3 else 1.0
PUNCH = float(next((a.split("=")[1] for a in sys.argv if a.startswith("--punch=")), 7))

# ---- script (speaker + English text per line) ----
SCRIPT, SPK, CHAP = [], [], {}
chap = None
for r in open(os.path.join(HERE, "script_full.md"), encoding="utf-8"):
    r = r.strip(); m = re.match(r"# (CHAPTER (\d+)|ENDING)", r)
    if m: chap = int(m.group(2)) if m.group(2) else 12; CHAP[chap] = len(SCRIPT); continue
    m = re.match(r"^([A-Z][A-Z .']*?):\s*(.+)$", r)
    if m and chap: SPK.append(m.group(1)); SCRIPT.append(m.group(2))
assert len(SCRIPT) == len(L), (len(SCRIPT), len(L))
EN = [re.sub(r"\[[^\]]*\]\s*", "", s).replace("*", "") for s in SCRIPT]

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
def arc(key):
    for ext in (".jpg", ".png"):
        p = os.path.join(ARC, key + ext)
        if os.path.exists(p): return p
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
    out = os.path.join(ARC, "_framed_" + os.path.basename(path).rsplit(".", 1)[0] + ".png")
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
    return board(t0, [imgcard(card(f"cycle{n}" if n != "chaos" else "cycle_chaos"), 1210, 1010, 1120, t0)] + list(extra))
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
CAST = {"PRINCE": "c_prince_kneel", "KHAN": "c_khan", "SERVANT": "c_servant", "IVAN": "c_ivan4", "DMITRY": "c_false_dmitry", "NOBLE": "c_polish_noble",
        "FOREMAN": "c_dutch_foreman", "PETER": "c_peter_worker", "OFFICER": "c_guard_officer", "CATHERINE": "c_catherine", "NAPOLEON": "c_napoleon",
        "AIDE": "c_french_aide", "SAILOR": "c_sailor_ru", "ADMIRAL": "c_admiral", "COMRADE": "c_comrade", "LENIN": "c_lenin", "EDITOR": "c_photo_editor",
        "GUARD ONE": "c_guard_a", "GUARD TWO": "c_guard_b", "CAPTAIN": "c_sub_captain", "ARKHIPOV": "c_arkhipov"}
def skit(i0, i1, bg, pos, chap_):
    """pos: {SPEAKER: (x, flip)}; first speaker is already there, the second slides in."""
    t0 = T(i0, -.3); lines = list(range(i0, i1 + 1)); lay = []
    for k, (who, (x, flip)) in enumerate(pos.items()):
        name = CAST["OFFICER"] if who == "OFFICER" and chap_ == 6 else ("c_official" if who == "OFFICIAL" else CAST.get(who))
        mine = [i for i in lines if SPK[i] == who]
        first = mine[0] if mine else i0
        lay.append(ch(name, x, enter=("slideL" if x < 960 else "slideR") if k else "none", t=None if k == 0 else T(first, -.5), flip=flip, talks=mine))
    for i in lines:
        x = pos.get(SPK[i], (960, False))[0]; lay.append(say(i, x))
    return shot(t0, a(bg) or LAST[0], lay, cam=[[t0, .5, .55, 1.0], [T(i1, 1), .5, .55, 1.12]])

# ======================= CHAPTER 2: THE MONGOLS =======================
c = CHAP[2]
chapter_card(2, c)
HORDE_PTS = [[104.0, 47.5], [85.0, 49.0], [65.0, 51.0], [50.0, 53.0], [40.0, 54.0]]
t = T(c, -.1)
globe("F_kalka", t, [[t, 48, 50, 2.6], [T(c + 1, 1), 38, 49, 2.2]],
      over=[ov("ov_mn_fill", fadein(t, .8)), ove("ov_mn_edge", fadein(t, 1))],
      arcs=[arcp([[104, 47.5], [80, 46], [55, 46], [38.5, 47.5]], t + .3, 2.0, col="#FF3B30", rad=.009)],
      pins=[pin(38.5, 47.6, K(c, "Kalka"), "Kalka 1223", "#FF3B30")],
      layers=[lab("1223", K(c, "twelve"), x=300, y=230, size=110)])
quip(c + 2)
pic(T(c + 3, -.15), "kalka", [lab("14 years of silence", K(c + 3, "fourteen"), size=80, box="#222222")])
t = T(c + 4, -.15)
globe("F_batu", t, [[t, 70, 50, 2.5], [T(c + 5, 1), 40, 53, 2.0]],
      over=[ov("ov_mn_fill", on(.8)), ove("ov_mn_edge", on(1))],
      arcs=[arcp([[104, 47.5], [70, 50], [50, 53], [39.7, 54.6]], K(c + 4, "came back"), 2.2, col="#FF3B30", rad=.009),
            arcp([[39.7, 54.6], [40.4, 56.1]], K(c + 5, "Vladimir"), .8, col="#FF3B30", rad=.007),
            arcp([[40.4, 56.1], [35, 53], [30.5, 50.45]], K(c + 5, "twelve forty"), 1.4, col="#FF3B30", rad=.007)],
      pins=[pin(39.7, 54.6, K(c + 5, "Ryazan"), "Ryazan", "#FF3B30"), pin(40.4, 56.1, K(c + 5, "Vladimir"), "Vladimir", "#FF3B30"),
            pin(30.5, 50.45, K(c + 5, "Kyiv"), "Kyiv", "#FF3B30")],
      layers=[lab("Batu Khan", K(c + 4, "Batu"), x=1450, y=250, size=90)])
pic(K(c + 5, "In twelve"), "batu_suzdal", [lab("1240: Kyiv burns", K(c + 5, "Kyiv"), size=86)])
quip(c + 6)
t = T(c + 7, -.15)
globe("F_horde", t, [[t, 48, 52, 2.4], [T(c + 7, 1), 50, 51, 2.0]],
      over=[ov("ov_horde", fadein(K(c + 7, "Golden"), .85)), ove("ov_horde_edge", fadein(K(c + 7, "Golden"), 1))],
      pins=[pin(47.0, 48.5, K(c + 7, "Volga"), "Sarai (on the Volga)", "#FFD84A")],
      layers=[lab("The Golden Horde", K(c + 7, "Golden"), y=230, size=96)])
board(T(c + 8, -.15), [txt("Permission slip\nrequired", 1250, 600, K(c + 8, "permission"), size=96, box="#c99400")])
skit(c + 9, c + 14, "ru_mongol_tent", {"PRINCE": (620, False), "KHAN": (1340, True)}, 2)
pic(T(c + 15, -.15), "golden_horde_tribute", [lab("240 years", K(c + 15, "two hundred"), size=110), tag("The Mongol yoke", K(c + 15, "Mongol"), y=900 - 600)])
plate(T(c + 16, -.15), a("ru_red_square"), layers=[lab("Moscow", K(c + 16, "Moscow"), size=110)], zoom=(1.25, 1.05))
pic(T(c + 17, -.15), "kalita", [tag("Ivan \"Moneybag\"", K(c + 17, "Moneybag"))])
quip(c + 18)
board(T(c + 19, -.15), [txt("Buy land\nSwallow neighbours\nGet the Church", 1250, 600, K(c + 19, "bought"), size=70, box="#222222")])
board(T(c + 20, -.15), [txt("One ruler\nTotal control\nEveryone pays", 1250, 600, K(c + 20, "one ruler"), size=80, box="#d6423a")])
pic(T(c + 21, -.15), "kulikovo", [lab("1380", K(c + 21, "thirteen"), x=300, y=230, size=110), tag("Kulikovo Field", K(c + 21, "Kulikovo"))])
quip(c + 22)
pic(T(c + 23, -.15), "ugra", [lab("1480", K(c + 23, "fourteen"), x=300, y=230, size=110), tag("The Ugra River", K(c + 23, "Ugra"))])
board(T(c + 24, -.15), [txt("No battle.\nThey just... left.", 1250, 600, K(c + 24, "No great"), size=86, box="#222222")])
quip(c + 25)
pic(T(c + 26, -.15), "ivan3", [tag("Ivan the Third", T(c + 26, .02)), txt("Land ×3", 1450, 700, K(c + 26, "tripled"), size=90, box="#2f8f4f")])
pic(K(c + 26, "double-headed"), "double_eagle", [lab("The double-headed eagle", K(c + 26, "double"), size=80)])
board(T(c + 27, -.15), [txt("The Third Rome", 1250, 330, K(c + 27, "Third"), size=96, box="#c99400"),
                        imgcard(card("cycle2"), 1210, 1030, 900, K(c + 27, "Chaos"))])

# ======================= CHAPTER 3: IVAN THE TERRIBLE =======================
c = CHAP[3]
chapter_card(3, c)
pic(T(c, -.1), "ivan4_portrait", [lab("Ruler at age 3", K(c, "three"), size=96)])
board(T(c + 1, -.15), [ch("c_ivan4", 1250, h=560, t=T(c + 1, 0)), tag("Mother: poisoned?", K(c + 1, "poisoned"), y=260)])
plate(T(c + 2, -.15), a("ru_kremlin_night"), layers=[lab("The boyars", K(c + 2, "boyars"), size=96)], zoom=(1.0, 1.2))
quip(c + 3)
plate(T(c + 4, -.15), a("ru_kremlin_night"), layers=[ch("c_ivan4", 960, h=640, t=T(c + 4, .2)), lab("1547: TSAR", K(c + 4, "Tsar"), size=110),
                                                   tag("Caesar → Tsar", K(c + 4, "Caesar"), y=420)])
t = T(c + 5, -.15)
globe("G_volga", t, [[t, 45, 54, 2.3], [T(c + 5, 1), 47, 50, 1.9]],
      over=[ov("ov_rudj_red", [[0, 0]])],
      arcs=[arcp([[37.6, 55.75], [44.0, 56.3], [49.1, 55.8], [48.5, 52.0], [46.0, 48.5], [48.0, 46.35]], K(c + 5, "conquered"), 2.6, rad=.008)],
      pins=[pin(37.6, 55.75, t, "Moscow"), pin(49.1, 55.8, K(c + 5, "Kazan"), "Kazan", "#FFD84A"), pin(48.0, 46.35, K(c + 5, "Astrakhan"), "Astrakhan", "#FFD84A")],
      layers=[lab("The Volga: now Moscow's", K(c + 5, "opening"), y=230, size=80)])
pic(T(c + 6, -.15), "st_basil", [lab("Saint Basil's", K(c + 6, "Saint"), size=96)], fallback=a("ru_red_square"))
quip(c + 7)
board(T(c + 8, -.15), [tag("1560: Anastasia dies", T(c + 8, .05), y=300), ch("c_ivan4", 1300, h=560, t=K(c + 8, "broke"))])
pic(T(c + 9, -.15), "oprichniki", [lab("The Oprichnina", K(c + 9, "Oprichnina"), size=90)])
quip(c + 10, [txt("🐕 + 🧹", 1500, 620, T(c + 10, .1), size=1, scale=1)] if False else [])
pic(T(c + 11, -.15), "oprichniki", [lab("Novgorod, 1570", K(c + 11, "Novgorod"), size=90)], c0=(.3, .5), c1=(.6, .5), zoom=(1.3, 1.4))
pic(T(c + 12, -.15), "ivan_son", [lab("1581", K(c + 12, "fifteen"), x=300, y=230, size=110)], zoom=(1.0, 1.25), c0=(.5, .45))
board(T(c + 13, -.15), [txt("He never recovered.", 1250, 600, K(c + 13, "never"), size=86, box="#222222")])
skit(c + 14, c + 17, "ru_kremlin_night", {"IVAN": (620, False), "SERVANT": (1340, True)}, 3)
t = T(c + 18, -.15)
globe("G_siberia", t, [[t, 50, 57, 2.4], [T(c + 18, 1), 75, 60, 2.6]],
      over=[ov("ov_rudj_red", [[0, 0]])],
      arcs=[arcp([[56.2, 58.0], [60.0, 58.3], [65.5, 57.2], [68.25, 58.2]], t + .5, 2.0, rad=.008)],
      pins=[pin(56.2, 58.0, t + .3, "Urals"), pin(68.25, 58.2, t + 2.4, "Siberia", "#FFD84A")],
      layers=[lab("1584", T(c + 18, .02), x=300, y=230, size=110)])
pic(K(c + 18, "thanks"), "yermak", [tag("Yermak", K(c + 18, "Yermak"))])
board(T(c + 19, -.15), [txt("Exhausted\nTerrified\nBroke", 1250, 600, K(c + 19, "exhausted"), size=86, box="#222222")])
quip(c + 20, [imgcard(card("cycle4"), 1350, 1000, 700, K(c + 20, "too far"))])

# ======================= CHAPTER 4: THE TIME OF TROUBLES =======================
c = CHAP[4]
chapter_card(4, c)
board(T(c, -.1), [txt("1598: Rurik's line ends", 1250, 330, K(c, "fifteen"), size=80, box="#222222"), txt("700+ years", 1250, 620, K(c, "seven"), size=100, box="#d6423a")])
board(T(c + 1, -.15), [txt("The Time of\nTroubles", 1250, 600, K(c + 1, "Time"), size=110, box="#d6423a")])
pic(T(c + 2, -.15), "godunov", [tag("Boris Godunov", K(c + 2, "Boris"))])
pic(T(c + 3, -.15), "famine_1601", [lab("1601: famine", K(c + 3, "sixteen"), size=96)], fallback=a("ru_snow_retreat"))
board(T(c + 4, -.15), [txt("Meanwhile, in Poland...", 1250, 600, K(c + 4, "Poland"), size=86, box="#222222")])
skit(c + 5, c + 8, "ru_polish_hall", {"NOBLE": (1340, True), "DMITRY": (620, False)}, 4)
pic(T(c + 9, -.15), "false_dmitry", [tag("The False Dmitry", K(c + 9, "False"))])
board(K(c + 9, "marched"), [txt("Crowned tsar", 1250, 600, K(c + 9, "crowned"), size=100, box="#c99400")])
board(T(c + 10, -.15), [txt("Fired from a cannon\nback to Poland", 1250, 600, K(c + 10, "ashes"), size=80, box="#d6423a")])
quip(c + 11)
t = T(c + 12, -.15)
globe("H_poles", t, [[t, 28, 54, 1.9], [T(c + 12, 1), 33, 55, 1.6]],
      over=[ov("ov_pl", fadein(K(c + 12, "Polish"), .8)), ov("ov_se", fadein(K(c + 12, "Swedes"), .7))],
      arcs=[arcp([[18.0, 59.3], [24, 59.5], [31.3, 58.5]], K(c + 12, "Swedes"), 1.2, col="#4aa3ff", rad=.006),
            arcp([[21.0, 52.2], [28, 54], [37.6, 55.75]], K(c + 12, "Polish"), 1.6, col="#FF3B30", rad=.008)],
      pins=[pin(37.6, 55.75, K(c + 12, "Kremlin"), "Moscow 1610", "#FF3B30")],
      layers=[lab("1610", K(c + 12, "sixteen ten"), x=300, y=230, size=110)])
board(T(c + 13, -.15), [txt("No tsar ✗\nNo government ✗\nForeign army ✓", 1250, 600, T(c + 13, .05), size=76, box="#222222")])
board(T(c + 14, -.15), [txt("Ordinary people\nfixed it.", 1250, 600, K(c + 14, "Ordinary"), size=96, box="#2f8f4f")])
pic(T(c + 15, -.15), "minin_pozharsky", [tag("Minin & Pozharsky", K(c + 15, "Kuzma"))], zoom=(1.0, 1.2), c0=(.5, .4))
pic(T(c + 16, -.15), "poles_kremlin", [lab("1612", K(c + 16, "sixteen"), x=300, y=230, size=110)])
quip(c + 17)
pic(T(c + 18, -.15), "michael_romanov", [lab("1613", K(c + 18, "sixteen"), x=300, y=230, size=110), tag("Michael Romanov, 16", K(c + 18, "Michael"))])
board(T(c + 19, -.15), [txt("304 years", 1250, 600, K(c + 19, "three"), size=120, box="#c99400")])
cycle(T(c + 20, -.15), 2)

# ======================= CHAPTER 5: PETER THE GREAT =======================
c = CHAP[5]
chapter_card(5, c)
pic(T(c, -.1), "peter_portrait", [lab("1672", K(c, "sixteen"), x=300, y=230, size=110)])
board(T(c + 1, -.15), [txt("Co-tsar at 10", 1250, 330, T(c + 1, .05), size=90, box="#222222"), tag("Sophia runs things", K(c + 1, "Sophia"), y=620)])
pic(T(c + 2, -.15), "streltsy", [lab("The Streltsy", K(c + 2, "Streltsy"), size=90)])
board(T(c + 3, -.15), [ch("c_peter1", 1300, h=760, t=K(c + 3, "two")), txt("2.03 m", 1650, 400, K(c + 3, "two"), size=90, box="#c99400")])
quip(c + 4, [ch("c_peter1", 1500, h=760, t=None, enter="none")])
board(T(c + 5, -.15), [txt("\"Peter Mikhailov\"", 1250, 600, K(c + 5, "Peter Mikhailov"), size=100, box="#222222")])
plate(T(c + 6, -.15), a("ru_dutch_shipyard"), layers=[lab("Holland & England", T(c + 6, .1), size=86)])
skit(c + 7, c + 10, "ru_dutch_shipyard", {"FOREMAN": (1340, True), "PETER": (620, False)}, 5)
pic(T(c + 11, -.15), "beard_cut", [lab("No beards!", K(c + 11, "beards"), size=110)])
pic(T(c + 12, -.15), "beard_token", [tag("Beard tax token", K(c + 12, "token"))])
quip(c + 13)
board(T(c + 14, -.15), [txt("New Year: 1 Jan\nSchools\nA navy", 1250, 600, K(c + 14, "January"), size=80, box="#222222")])
pic(T(c + 15, -.15), "poltava", [lab("Poltava 1709", K(c + 15, "Poltava"), size=96)])
t = T(c + 16, -.15)
globe("I_baltic", t, [[t, 30, 58, 2.0], [T(c + 17, 1), 30.3, 59.9, 1.45]],
      over=[ov("ov_se", fadein(t, .6))],
      pins=[pin(30.3, 59.9, K(c + 17, "Saint"), "Saint Petersburg", "#FFD84A")],
      arcs=[arcp([[37.6, 55.75], [34, 58], [30.3, 59.9]], K(c + 16, "Baltic"), 1.4, rad=.007)],
      layers=[lab("The Baltic Sea", K(c + 16, "Baltic"), y=230, size=90)])
plate(K(c + 17, "Thousands"), a("ru_spb_build"), layers=[tag("Built on a swamp", K(c + 17, "Thousands"))])
board(T(c + 18, -.15), [txt("EMPEROR", 1250, 600, K(c + 18, "Emperor"), size=120, box="#c99400")])
pic(T(c + 19, -.15), "peter_alexei", [tag("His son Alexei", K(c + 19, "Alexei"))])
board(T(c + 20, -.15), [txt("1718", 1250, 600, K(c + 20, "seventeen"), size=120, box="#222222")])
quip(c + 21)
board(T(c + 22, -.15), [txt("Pick any heir", 1250, 330, T(c + 22, .1), size=86, box="#222222"), txt("1725: picked no one", 1250, 620, K(c + 22, "seventeen"), size=86, box="#d6423a")])
quip(c + 23)

# ======================= CHAPTER 6: CATHERINE THE GREAT =======================
c = CHAP[6]
chapter_card(6, c)
board(T(c, -.1), [txt("37 years of\npalace coups", 1250, 600, K(c, "thirty"), size=96, box="#222222")])
pic(T(c + 1, -.15), "peter3", [tag("Coup after coup", T(c + 1, .1))], fallback=a("ru_palace_room"))
plate(T(c + 2, -.15), a("ru_palace_room"), layers=[ch("c_catherine", 960, h=620, t=K(c + 2, "Sophie")), lab("1744", K(c + 2, "seventeen"), x=300, y=230, size=110)])
board(T(c + 3, -.15), [ch("c_catherine", 1250, h=600, t=T(c + 3, 0)), tag("Sophie → Catherine", K(c + 3, "Catherine"), y=260)])
pic(T(c + 4, -.15), "peter3", [tag("Peter (the Third)", T(c + 4, .05))])
board(T(c + 5, -.15), [txt("Gives it all back\nto Prussia", 1250, 600, K(c + 5, "handed"), size=86, box="#d6423a")])
quip(c + 6)
skit(c + 7, c + 10, "ru_palace_room", {"CATHERINE": (620, False), "OFFICER": (1340, True)}, 6)
pic(T(c + 11, -.15), "catherine_horse", [tag("\"Stomach problem\"", K(c + 11, "stomach"))])
quip(c + 12)
pic(T(c + 13, -.15), "hermitage", [lab("34 years", K(c + 13, "thirty"), size=100), tag("The Hermitage", K(c + 13, "Hermitage"))])
t = T(c + 14, -.15)
globe("J_crimea1783", t, [[t, 30, 50, 1.9], [T(c + 14, 1), 26, 52, 1.7]],
      over=[ov("ov_crimea", fadein(K(c + 14, "Crimea"), .9)), ov("ov_pl", fadein(K(c + 14, "Poland"), .8))],
      pins=[pin(34.1, 45.0, K(c + 14, "Crimea"), "Crimea 1783", "#FFD84A"), pin(19.5, 52.0, K(c + 14, "Poland"), "Poland: carved up", "#FF3B30")])
t = T(c + 15, -.15)
globe("J_alaska1784", t, [[t, 140, 60, 2.6], [T(c + 16, 1), -160, 58, 2.0]],
      over=[ov("ov_rudj_flag", on(.85)), ove("ov_rudj_edge", on(.9)), ove("ov_ak_edge", fadein(K(c + 15, "Alaska"), 1))],
      arcs=[arcp([[158.6, 53.0], [175, 55], [-170, 56], [-153.3, 57.1]], K(c + 15, "Pacific"), 2.2, rad=.007)],
      pins=[pin(-153.3, 57.1, K(c + 15, "Alaska"), "Alaska 1784", "#FFD84A")])
pic(T(c + 17, -.15), "serfs", [lab("Serfs", K(c + 17, "serfs"), size=110)])
pic(T(c + 18, -.15), "pugachev", [tag("Pugachev's rising", K(c + 18, "Pugachev"))])
cycle(T(c + 19, -.15), 3, [tag("...in a powdered wig", K(c + 19, "powdered"), y=230)])
quip(c + 20, [txt("SUBSCRIBE", 1500, 650, K(c + 20, "subscribe"), size=96, box="#d6423a")])
pic(T(c + 21, -.15), "catherine_horse", [lab("1796", K(c + 21, "seventeen"), x=300, y=230, size=110)], zoom=(1.2, 1.0))
board(T(c + 22, -.15), [ch("c_napoleon", 1250, h=560, t=K(c + 22, "short")), tag("A short French general", K(c + 22, "short"), y=260)])

# ======================= CHAPTER 7: NAPOLEON =======================
c = CHAP[7]
chapter_card(7, c)
pic(T(c, -.1), "napoleon_portrait", [lab("1812", K(c, "eighteen"), x=300, y=230, size=110)])
t = T(c + 1, -.15)
NAP = [[-0.5, 48.0], [8, 51], [16, 53], [23.9, 54.9], [32.0, 54.8], [35.8, 55.5], [37.6, 55.75]]
globe("K_napoleon", t, [[t, 15, 52, 2.0], [T(c + 3, 1), 30, 54, 1.75]],
      over=[ov("ov_fr_blue", fadein(t, .85)), ov("ov_rudj_red", fadein(t, .35))],
      arcs=[arcp(NAP, K(c + 1, "invaded"), 3.4, col="#4aa3ff", rad=.018, lift=.01)],
      pins=[pin(37.6, 55.75, K(c + 1, "invaded") + 3.0, "Moscow", "#FFD84A"), pin(35.8, 55.5, K(c + 3, "Borodino"), "Borodino", "#FF3B30")],
      layers=[lab("600,000 men", K(c + 1, "six"), y=230, size=100)])
quip(c + 2)
pic(T(c + 3, -.15), "moscow_fire", [lab("Scorched earth", K(c + 3, "burned"), size=96)], fallback=a("ru_snow_retreat"))
pic(T(c + 4, -.15), "borodino", [lab("Borodino", K(c + 4, "Borodino"), size=96), txt("70,000", 1450, 700, K(c + 4, "seventy"), size=110, box="#d6423a")])
pic(T(c + 5, -.15), "moscow_fire", [lab("Moscow", K(c + 5, "Moscow"), size=100)], zoom=(1.15, 1.0))
pic(T(c + 6, -.15), "moscow_fire", [lab("Moscow burns", K(c + 6, "burned"), size=100)], zoom=(1.0, 1.3))
skit(c + 7, c + 11, "ru_moscow_fire", {"NAPOLEON": (620, False), "AIDE": (1340, True)}, 7)
board(T(c + 12, -.15), [txt("5 weeks.\nNo answer.", 1250, 600, K(c + 12, "five"), size=96, box="#222222")])
t = T(c + 13, -.15)
globe("K_retreat", t, [[t, 37, 55, 1.7], [T(c + 14, 1), 18, 53, 2.1]],
      over=[ov("ov_fr_blue", on(.85)), ov("ov_rudj_red", on(.35))],
      arcs=[arcp(NAP, 0, .01, col="#4aa3ff", rad=.018, lift=.01, fade=[[0, 1], [K(c + 13, "winter"), 1], [K(c + 13, "winter") + 1.2, .15]]),
            arcp(NAP[::-1], K(c + 14, "Starving"), 3.0, col="#9fd0ff", rad=.004, lift=.01)],
      layers=[lab("WINTER", K(c + 13, "winter"), y=230, size=120)])
plate(K(c + 14, "Cossacks"), a("ru_snow_retreat"), layers=[tag("A small fraction made it out", K(c + 14, "Only"), y=250)], zoom=(1.0, 1.2))
quip(c + 15)
pic(T(c + 16, -.15), "russians_paris", [lab("Paris, 1814", K(c + 16, "Paris"), size=96)])
board(T(c + 17, -.15), [txt("Constitutions?", 1250, 600, K(c + 17, "Constitutions"), size=100, box="#2b3a67")])
pic(T(c + 18, -.15), "decembrists", [lab("The Decembrists", K(c + 18, "Decembrists"), size=96)], fallback=arc("hermitage"))
board(T(c + 19, -.15), [txt("5 hanged\n100+ to Siberia", 1250, 600, K(c + 19, "Five"), size=90, box="#222222")])
pic(T(c + 20, -.15), "crimean_war", [lab("The Crimean War", K(c + 20, "Crimean"), size=96)])
pic(T(c + 21, -.15), "alexander2", [lab("1861", K(c + 21, "eighteen"), x=300, y=230, size=110), txt("23 million\nserfs freed", 1450, 640, K(c + 21, "twenty"), size=90, box="#2f8f4f")])
board(K(c + 21, "Two years"), [txt("2 years before\nLincoln", 1250, 600, K(c + 21, "Two years"), size=90, box="#2b3a67")])
t = T(c + 22, -.15)
globe("K_alaska_sale", t, [[t, -175, 58, 2.4], [T(c + 22, 1), -153, 62, 1.8]],
      over=[ov("ov_rudj_flag", on(.6)), ove("ov_rudj_edge", on(.6)), ov("ov_ak_us", fadein(K(c + 22, "sold"), .95)), ove("ov_ak_edge", on(1))],
      layers=[lab("1867", K(c + 22, "eighteen"), x=300, y=230, size=110), txt("$7.2 million", 1450, 300, K(c + 22, "seven point"), size=96, box="#2f8f4f")])
quip(c + 23)
pic(T(c + 24, -.15), "alaska_check", [tag("\"Seward's Folly\"", K(c + 24, "Seward"))], fallback=None)
board(K(c + 24, "Then came"), [txt("Gold", 1050, 560, K(c + 24, "gold"), size=110, box="#c99400"), txt("Oil", 1500, 560, K(c + 24, "oil"), size=110, box="#111111")])
pic(T(c + 25, -.15), "alexander2", [tag("Step 1: an elected assembly?", K(c + 25, "approved"), y=250)], zoom=(1.2, 1.3))
pic(T(c + 26, -.15), "alexander2_assassination", [lab("13 March 1881", T(c + 26, .02), size=86)])
quip(c + 27)
cycle(T(c + 28, -.15), "chaos", [tag("The last tsar...", K(c + 28, "last"), y=230)])

# ======================= CHAPTER 8: THE LAST TSAR =======================
c = CHAP[8]
chapter_card(8, c)
plate(T(c, -.1), a("ru_palace_room"), layers=[ch("c_nicholas2", 960, h=640, t=T(c, .1)), lab("1894", K(c, "eighteen"), x=300, y=230, size=110)])
pic(T(c + 1, -.15), "nicholas2_family", [tag("Alexandra + 5 children", K(c + 1, "five"))])
board(T(c + 2, -.15), [ch("c_nicholas2", 1250, h=600, t=T(c + 2, 0)), tag("Unprepared", K(c + 2, "unprepared"), y=260)])
quip(c + 3)
t = T(c + 4, -.15)
FLEET = [[21.0, 56.5], [11.0, 57.8], [2.5, 54.7], [-9.5, 43.0], [-17.0, 21.0], [-17.5, 0.0], [5.0, -20.0], [18.5, -35.5], [35.0, -30.0], [48.3, -13.3],
         [75.0, -2.0], [95.0, 5.0], [109.2, 11.9], [120.0, 25.0], [129.4, 34.4]]
globe("L_fleet", t, [[t, 15, 52, 2.3], [K(c + 4, "Baltic") + 1, 10, 30, 3.0], [T(c + 4, 1), 60, 0, 3.4], [T(c + 5, 1), 4, 55, 1.7]],
      over=[ov("ov_jp", fadein(K(c + 4, "Japan"), .85))],
      arcs=[arcp(FLEET, K(c + 4, "Baltic"), 4.5, rad=.008, lift=.01)],
      pins=[pin(21.0, 56.5, K(c + 4, "Baltic"), "Baltic Fleet"), pin(129.4, 34.4, K(c + 4, "Baltic") + 4.0, "Japan", "#FF3B30"),
            pin(2.5, 54.7, K(c + 5, "North Sea"), "Dogger Bank", "#FF3B30")],
      layers=[lab("1904", K(c + 4, "nineteen"), x=300, y=230, size=110)])
skit(c + 6, c + 10, "ru_ship_deck", {"SAILOR": (1340, True), "ADMIRAL": (620, False)}, 8)
pic(T(c + 11, -.15), "dogger_bank", [tag("This really happened.", T(c + 11, .05))])
pic(T(c + 12, -.15), "tsushima", [lab("Tsushima", K(c + 12, "Tsushima"), size=100), txt("8 months → 2 days", 1300, 700, K(c + 12, "two days"), size=80, box="#d6423a")])
board(T(c + 13, -.15), [txt("Asia beats\na European empire", 1250, 600, K(c + 13, "Asian"), size=86, box="#222222")])
pic(T(c + 14, -.15), "bloody_sunday", [lab("January 1905", K(c + 14, "January"), size=90)], zoom=(1.0, 1.2))
pic(T(c + 15, -.15), "bloody_sunday", [lab("Bloody Sunday", K(c + 15, "Bloody"), size=100)], zoom=(1.3, 1.45), c0=(.4, .5), c1=(.6, .5))
board(T(c + 16, -.15), [txt("\"Loving father\"  ✗", 1250, 600, K(c + 16, "loving"), size=90, box="#d6423a")])
t = T(c + 17, -.15)
FRONT = [[24.1, 57.0], [25.5, 55.0], [26.0, 53.0], [25.5, 51.5], [26.2, 49.8], [27.5, 48.3], [29.0, 46.5]]
globe("L_ww1", t, [[t, 30, 52, 2.0], [T(c + 18, 1), 22, 53, 1.55]],
      over=[ov("ov_rudj_red", fadein(t, .3))],
      arcs=[arcp(FRONT, K(c + 18, "front"), 2.4, col="#FF3B30", rad=.007, lift=.0)],
      pins=[pin(20.1, 53.5, K(c + 18, "Tannenberg"), "Tannenberg", "#FF3B30")],
      layers=[lab("1914", K(c + 17, "nineteen"), x=300, y=230, size=110), tag("World War One", K(c + 17, "World"), y=900)])
pic(T(c + 19, -.15), "tannenberg", [lab("Millions lost", K(c + 19, "Millions"), size=96)])
board(T(c + 20, -.15), [ch("c_nicholas2", 1100, h=540, t=T(c + 20, .1)), tag("Alexandra in charge", K(c + 20, "Alexandra"), x=1500, y=300)])
plate(T(c + 21, -.15), a("ru_palace_room"), layers=[ch("c_rasputin", 960, h=660, t=K(c + 21, "Rasputin")), lab("Rasputin", K(c + 21, "Rasputin"), size=100)])
pic(K(c + 21, "who seemed"), "rasputin", [tag("Alexei: haemophilia", K(c + 21, "haemophilia"))])
board(T(c + 22, -.15), [txt("Miracle", 1050, 520, K(c + 22, "miracle"), size=96, box="#2f8f4f"), txt("Scandal", 1500, 700, K(c + 22, "scandal"), size=96, box="#d6423a")])
board(T(c + 23, -.15), [ch("c_rasputin", 1250, h=560, t=T(c + 23, 0)), tag("December 1916", T(c + 23, .05), y=260)])
board(T(c + 24, -.15), [txt("Poison ✗", 1250, 380, K(c + 24, "poisoned"), size=80, box="#222222"), txt("Bullets ✗", 1250, 560, K(c + 24, "bullets"), size=80, box="#222222"),
                        txt("Icy river", 1250, 740, K(c + 24, "icy"), size=80, box="#2b3a67")])
quip(c + 25)
board(T(c + 26, -.15), [txt("Weeks left.", 1250, 600, K(c + 26, "weeks"), size=100, box="#d6423a")])
pic(T(c + 27, -.15), "feb_revolution", [lab("February 1917", K(c + 27, "February"), size=90)])
pic(T(c + 28, -.15), "feb_revolution", [tag("The soldiers switch sides", K(c + 28, "joined"))], zoom=(1.3, 1.4))
pic(T(c + 29, -.15), "nicholas2_family", [txt("304 years → 1 signature", 960, 250, K(c + 29, "Three"), size=80, box="#222222")], zoom=(1.1, 1.3))
board(T(c + 30, -.15), [txt("Keeps fighting\nthe war", 1250, 600, K(c + 30, "kept"), size=90, box="#d6423a")])
pic(T(c + 31, -.15), "lenin_1917", [txt("Peace. Land. Bread.", 960, 250, K(c + 31, "Peace"), size=90, box="#d6423a")])
skit(c + 32, c + 36, "ru_backroom", {"COMRADE": (1340, True), "LENIN": (620, False)}, 8)
pic(T(c + 37, -.15), "winter_palace_1917", [lab("October 1917", K(c + 37, "October"), size=90), tag("Bolsheviks", K(c + 37, "Bolsheviks"))])
pic(T(c + 38, -.15), "civil_war", [txt("Reds", 900, 520, K(c + 38, "Reds"), size=100, box="#d6423a"), txt("Whites", 1400, 700, K(c + 38, "Whites"), size=100, box="#eeeeee", color="#222222")])
pic(T(c + 39, -.15), "ipatiev", [lab("July 1918", K(c + 39, "July"), size=90), tag("Yekaterinburg", K(c + 39, "Yekaterinburg"))])
t = T(c + 40, -.15)
globe("L_ussr1922", t, [[t, 60, 55, 2.5], [T(c + 40, 1), 75, 55, 3.0]],
      over=[ov("ov_ussr_red", fadein(K(c + 40, "brand"), .9)), ove("ov_ussr_edge", fadein(K(c + 40, "brand"), 1))],
      layers=[lab("1922", K(c + 40, "nineteen"), x=300, y=230, size=110), lab("USSR", K(c + 40, "USSR"), y=900 - 650, size=120)])
quip(c + 41, [imgcard(card("cycle5"), 1350, 1000, 700, K(c + 41, "Collapse"))])

# ======================= CHAPTER 9: STALIN =======================
c = CHAP[9]
chapter_card(9, c)
pic(T(c, -.1), "lenin_mausoleum", [lab("1924", K(c, "nineteen"), x=300, y=230, size=110)])
board(T(c + 1, -.15), [txt("Brain: 30,000 slices", 1250, 330, K(c + 1, "sliced"), size=76, box="#222222"), tag("Still on display", K(c + 1, "display"), y=620)])
quip(c + 2)
pic(T(c + 3, -.15), "stalin_full", [txt("\"Too rude.\nRemove him.\"", 1350, 600, K(c + 3, "rude"), size=80, box="#ffffffee", color="#222222")], fallback=STALIN)
board(T(c + 4, -.15), [txt("The party\nignored him.", 1250, 600, T(c + 4, .1), size=96, box="#222222")])
pic(T(c + 5, -.15), "trotsky", [tag("Trotsky", K(c + 5, "Trotsky")), txt("Mexico, 1940", 1400, 700, K(c + 5, "Mexico"), size=80, box="#d6423a")])
board(T(c + 6, -.15), [txt("Farms → factories\nin 10 years", 1250, 600, K(c + 6, "industrial"), size=86, box="#222222")])
pic(T(c + 7, -.15), "collectivisation", [lab("Collective farms", K(c + 7, "giant"), size=90), tag("The Gulag", K(c + 7, "Gulag"), y=900 - 600)])
pic(T(c + 8, -.15), "collectivisation", [lab("1932-33: famine", K(c + 8, "nineteen"), size=90), tag("Holodomor", K(c + 8, "Holodomor"), y=420)], zoom=(1.3, 1.4))
pic(T(c + 9, -.15), "gulag", [txt("1.5 million arrested", 960, 250, K(c + 9, "one and"), size=80, box="#222222"), txt("~700,000 shot", 960, 800 - 500, K(c + 9, "seven"), size=80, box="#d6423a")])
board(T(c + 10, -.15), [txt("Generals.", 1250, 380, K(c + 10, "Generals"), size=80, box="#222222"), txt("Scientists.", 1250, 540, K(c + 10, "Scientists"), size=80, box="#222222"),
                        txt("Poets.", 1250, 700, K(c + 10, "Poets"), size=80, box="#222222")])
pic(T(c + 11, -.15), "yezhov_photo", [lab("...from photos", K(c + 11, "photos"), size=96)])
skit(c + 12, c + 16, "ru_photo_lab", {"OFFICIAL": (620, False), "EDITOR": (1340, True)}, 9)
pic(T(c + 17, -.15), "yezhov_photo", [tag("Nikolai Yezhov", K(c + 17, "Yezhov"))], zoom=(1.0, 1.3))
quip(c + 18)
pic(T(c + 19, -.15), "pact_1939", [lab("1939", K(c + 19, "nineteen"), x=300, y=230, size=110), tag("Stalin + Hitler", K(c + 19, "Hitler"))])
board(T(c + 20, -.15), [txt("Spies: \"Germany is coming!\"", 1250, 450, K(c + 20, "spies"), size=66, box="#222222"), txt("Stalin: ignored", 1250, 700, K(c + 20, "ignored"), size=80, box="#d6423a")])
t = T(c + 21, -.15)
BARB = [[[20.5, 54.7], [24.5, 57], [30.3, 59.9]], [[23.0, 52.4], [28, 54.5], [33, 55], [37.6, 55.75]], [[23.0, 50.5], [30.5, 50.45], [38, 48.5], [44.5, 48.7]]]
globe("M_barbarossa", t, [[t, 28, 52, 1.9], [T(c + 22, 1), 34, 54, 1.6]],
      over=[ov("ov_ussr_red", on(.45))],
      arcs=[arcp(BARB[0], K(c + 21, "Leningrad"), 1.5, col="#444444", rad=.012, lift=.01), arcp(BARB[1], K(c + 21, "Moscow"), 1.5, col="#444444", rad=.012, lift=.01),
            arcp(BARB[2], K(c + 21, "south"), 1.5, col="#444444", rad=.012, lift=.01)],
      pins=[pin(30.3, 59.9, K(c + 21, "Leningrad") + 1.4, "Leningrad"), pin(37.6, 55.75, K(c + 21, "Moscow") + 1.4, "Moscow"), pin(44.5, 48.7, K(c + 21, "south") + 1.4, "Stalingrad")],
      layers=[lab("22 June 1941", K(c + 21, "June"), y=230, size=90), txt("3 million+", 1500, 900 - 620, K(c + 21, "three"), size=80, box="#222222")])
pic(T(c + 22, -.15), "barbarossa", [lab("The largest invasion ever", K(c + 22, "largest"), size=80)])
pic(T(c + 23, -.15), "leningrad_siege", [lab("Leningrad: ~900 days", K(c + 23, "nine"), size=86), txt("~1 million died", 1350, 700, K(c + 23, "million"), size=80, box="#d6423a")])
pic(T(c + 24, -.15), "moscow_1941", [lab("...winter. Again.", K(c + 24, "winter"), size=96)], fallback=a("ru_snow_retreat"))
quip(c + 25)
pic(T(c + 26, -.15), "stalingrad", [lab("Stalingrad", K(c + 26, "Stalingrad"), size=110)])
pic(T(c + 27, -.15), "stalingrad", [tag("A whole German army surrenders", K(c + 27, "surrender"))], zoom=(1.3, 1.45))
pic(T(c + 28, -.15), "berlin_1945", [lab("Berlin, 1945", K(c + 28, "Berlin"), size=96)])
board(T(c + 29, -.15), [txt("~27 million", 1250, 600, K(c + 29, "twenty"), size=120, box="#d6423a")])
pic(T(c + 30, -.15), "stalin_full", [tag("Half of Europe", K(c + 30, "half")), txt("1949: the bomb", 1400, 700, K(c + 30, "atomic"), size=80, box="#222222")], fallback=STALIN)
board(T(c + 31, -.15), [txt("1953", 1250, 600, K(c + 31, "nineteen"), size=130, box="#222222")])
skit(c + 32, c + 35, "ru_corridor", {"GUARD ONE": (620, False), "GUARD TWO": (1340, True)}, 9)
board(T(c + 36, -.15), [txt("Top doctors:\narrested", 1250, 600, K(c + 36, "doctors"), size=90, box="#d6423a")])
pic(T(c + 37, -.15), "stalin_funeral", [lab("Too terrified to help", K(c + 37, "terrified"), size=80)])

# ======================= CHAPTER 10: THE COLD WAR =======================
c = CHAP[10]
chapter_card(10, c)
t = T(c, -.1)
globe("N_coldwar", t, [[t, 0, 55, 3.2], [T(c + 1, 1), -40, 50, 3.4]],
      over=[ov("ov_ussr_red", fadein(K(c + 1, "Red"), .9)), ov("ov_east_red", fadein(K(c + 1, "Red"), .9)), ov("ov_west_blue", fadein(K(c + 1, "blue"), .9))],
      arcs=[arcp([[-98, 39], [-40, 70], [37.6, 55.75]], K(c + 1, "nuclear"), 1.4, col="#FFFFFF", rad=.006, lift=.12),
            arcp([[37.6, 55.75], [-20, 75], [-98, 39]], K(c + 1, "nuclear") + .3, 1.4, col="#FFFFFF", rad=.006, lift=.12)],
      layers=[lab("The Cold War", K(c, "Cold"), y=230, size=100)])
pic(T(c + 2, -.15), "sputnik", [lab("Sputnik, 1957", K(c + 2, "Sputnik"), size=96)])
pic(T(c + 3, -.15), "gagarin", [lab("Yuri Gagarin, 1961", K(c + 3, "Yuri"), size=86)])
quip(c + 4)
t = T(c + 5, -.15)
globe("N_cuba", t, [[t, -82, 26, 2.2], [T(c + 6, 1), -80.5, 24.0, 1.45]],
      over=[ov("ov_cuba", fadein(K(c + 5, "Cuba"), .9)), ov("ov_us", fadein(t, .7))],
      arcs=[arcp([[-80.2, 25.8], [-81.0, 24.5], [-82.4, 23.1]], K(c + 5, "ninety"), 1.0, col="#FFFFFF", rad=.003, lift=.0)],
      pins=[pin(-82.4, 23.1, K(c + 5, "Cuba"), "Cuba", "#FF3B30"), pin(-80.2, 25.8, K(c + 5, "Florida"), "Florida", "#4aa3ff")],
      layers=[lab("1962", K(c + 5, "nineteen"), x=300, y=230, size=110), txt("90 miles", 1450, 300, K(c + 5, "ninety"), size=96, box="#222222")])
pic(T(c + 6, -.15), "cuba_missiles", [txt("13 days", 960, 250, K(c + 6, "thirteen"), size=110, box="#d6423a")])
plate(T(c + 7, -.15), a("ru_submarine"), layers=[tag("No contact with Moscow", K(c + 7, "lost contact"), y=250)], zoom=(1.0, 1.25))
board(T(c + 8, -.15), [txt("☢ NUCLEAR\nTORPEDO", 1250, 600, K(c + 8, "nuclear"), size=96, box="#d6423a")])
skit(c + 9, c + 12, "ru_submarine", {"CAPTAIN": (620, False), "ARKHIPOV": (1340, True)}, 10)
pic(T(c + 13, -.15), "arkhipov", [tag("Vasily Arkhipov", K(c + 13, "Vasily")), txt("3 votes needed\n1 said NO", 1400, 650, K(c + 13, "said no"), size=76, box="#2f8f4f")])
quip(c + 14)
plate(T(c + 15, -.15), a("ru_soviet_shop"), layers=[txt("Giant rockets ✓", 960, 250, K(c + 15, "rockets"), size=80, box="#2f8f4f"), txt("Shoes ✗", 960, 420, K(c + 15, "shoes"), size=80, box="#d6423a")])
pic(T(c + 16, -.15), "soviet_queue", [lab("The queue", T(c + 16, .1), size=100)], fallback=a("ru_soviet_shop"))
pic(T(c + 17, -.15), "gorbachev", [lab("1985", K(c + 17, "nineteen"), x=300, y=230, size=110), tag("Glasnost: speak freely", K(c + 17, "glasnost"))])
t = T(c + 18, -.15)
globe("N_chernobyl", t, [[t, 30, 54, 1.7], [T(c + 19, 1), 22, 57, 1.6]],
      arcs=[arcp([[30.1, 51.4], [25, 56], [18.2, 60.4]], K(c + 19, "Sweden"), 1.6, col="#9dff6a", rad=.006, lift=.02)],
      pins=[pin(30.1, 51.4, K(c + 18, "Chernobyl"), "Chernobyl", "#9dff6a"), pin(18.2, 60.4, K(c + 19, "Sweden"), "Sweden: alarms!", "#FFD84A")],
      layers=[lab("1986", T(c + 18, .02), x=300, y=230, size=110), txt("1,000+ km", 1450, 300, K(c + 19, "thousand"), size=90, box="#222222")])
board(T(c + 20, -.15), [txt("A lot to say.", 1250, 600, K(c + 20, "lot"), size=100, box="#222222")])
pic(T(c + 21, -.15), "berlin_wall", [lab("1989", K(c + 21, "nineteen"), x=300, y=230, size=110), tag("The Berlin Wall falls", K(c + 21, "Berlin"))])
pic(T(c + 22, -.15), "yeltsin_tank", [lab("August 1991", K(c + 22, "August"), size=86), tag("Boris Yeltsin", K(c + 22, "Boris"))])
board(T(c + 23, -.15), [txt("Coup: 3 days", 1250, 450, T(c + 23, .05), size=86, box="#222222"), txt("USSR: gone", 1250, 680, K(c + 23, "so did"), size=86, box="#d6423a")])
t = T(c + 24, -.15)
globe("N_breakup", t, [[t, 60, 52, 3.0], [T(c + 24, 1), 62, 50, 2.6]],
      over=[ov("ov_ussr_red", [[0, .9], [K(c + 24, "fifteen"), .9], [K(c + 24, "fifteen") + .5, 0]]),
            ov("ov_ussr15", fadein(K(c + 24, "fifteen"), .95, .5)), ove("ov_ussr15_edge", fadein(K(c + 24, "fifteen"), 1, .5))],
      layers=[lab("25 Dec 1991", K(c + 24, "December"), y=230, size=90), txt("1 → 15", 1450, 900 - 600, K(c + 24, "fifteen"), size=100, box="#222222")])

# ======================= CHAPTER 11: TODAY =======================
c = CHAP[11]
chapter_card(11, c)
pic(T(c, -.1), "moscow_1990s", [lab("The 1990s", T(c, .05), size=100), tag("Savings: gone", K(c, "savings"))])
board(T(c + 1, -.15), [txt("Oil & gas → billionaires", 1250, 600, K(c + 1, "billionaires"), size=72, box="#c99400")])
board(T(c + 2, -.15), [txt("Teachers & soldiers:\nno pay for months", 1250, 600, T(c + 2, .1), size=72, box="#222222")])
pic(T(c + 3, -.15), "gorbachev", [lab("Pizza Hut ad", K(c + 3, "Pizza"), size=96)], zoom=(1.2, 1.3))
quip(c + 4)
cycle(T(c + 5, -.15), "chaos")
pic(T(c + 6, -.15), "kremlin", [lab("31 Dec 1999", K(c + 6, "New"), size=90), tag("Vladimir Putin", K(c + 6, "Vladimir"))])
pic(K(c + 6, "Vladimir"), "putin_2000", [tag("Former KGB officer", K(c + 6, "KGB"))])
board(T(c + 7, -.15), [txt("Supporters: stability,\nrising incomes", 1250, 600, K(c + 7, "Supporters"), size=70, box="#2f8f4f")])
board(T(c + 8, -.15), [txt("Critics: TV taken over,\nopponents jailed or exiled", 1250, 600, K(c + 8, "Critics"), size=64, box="#d6423a")])
t = T(c + 9, -.15)
globe("O_crimea", t, [[t, 36, 50, 1.8], [T(c + 9, 1), 34.5, 46, 1.35]],
      over=[ov("ov_rudj_flag", on(.5)), ove("ov_ua_edge", on(.8)), ov("ov_crimea", fadein(K(c + 9, "Crimea"), .9)), ove("ov_crimea_edge", fadein(K(c + 9, "Crimea"), 1))],
      pins=[pin(34.1, 45.0, K(c + 9, "Crimea"), "Crimea", "#FF3B30")],
      layers=[lab("2014", K(c + 9, "twenty"), x=300, y=230, size=110)])
board(T(c + 10, -.15), [txt("2020: rules changed", 1250, 420, K(c + 10, "twenty twenty"), size=76, box="#222222"), txt("→ 2036", 1250, 640, K(c + 10, "thirty"), size=110, box="#d6423a")])
t = T(c + 11, -.15)
globe("O_ukraine", t, [[t, 38, 52, 2.0], [T(c + 11, 1), 33, 49, 1.6]],
      over=[ov("ov_rudj_flag", on(.5)), ov("ov_ua", fadein(K(c + 11, "Ukraine"), .6)), ove("ov_ua_edge", fadein(K(c + 11, "Ukraine"), 1))],
      pins=[pin(30.5, 50.45, K(c + 11, "Ukraine"), "Ukraine", "#FFD84A")],
      layers=[lab("February 2022", K(c + 11, "February"), y=230, size=90), tag("Biggest war in Europe since WWII", K(c + 11, "biggest"), y=900 - 600)])
pic(T(c + 12, -.15), "kremlin", [lab("Still going on", K(c + 12, "still"), size=100)], zoom=(1.0, 1.2))

# ======================= ENDING =======================
c = CHAP[12]
board(T(c, -.1), [imgcard(card("cycle5"), 1210, 1010, 1120, T(c, -.1))])
for k, (who, key, word) in enumerate([("Vikings", "c_rurik", "Vikings"), ("Mongols", "c_khan", "Mongols"), ("Romanovs", "michael_romanov", "Romanovs"),
                                      ("Lenin & Stalin", "c_lenin", "Lenin"), ("Putin", "kremlin", "Putin")]):
    i = c + 1 + k; t0 = T(i, -.15)
    lay = [ch(key, 1250, h=600, t=t0 + .05)] if key.startswith("c_") else [imgcard(arc(key), 1250, 960, 520, t0 + .05, framed=True)]
    board(t0, lay + [tag(who, K(i, word))])
board(T(c + 6, -.15), [txt("1,100 years", 1250, 380, K(c + 6, "Eleven"), size=96, box="#222222"), txt("Same story.", 1250, 640, K(c + 6, "Same"), size=110, box="#d6423a")])
quip(c + 7)
board(T(c + 8, -.15), [txt("Nobody knows.", 1250, 600, T(c + 8, .05), size=100, box="#222222")])
quip(c + 9, [txt("Next: the Ottomans", 1250, 760, K(c + 9, "Ottomans"), size=80, box="#c99400")])

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
json.dump(clips_out, open(os.path.join(os.path.dirname(os.path.abspath(args[1])), "clips3d_full.json"), "w"), indent=1)

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
        if re.fullmatch(r"\d{3,4}", tx_):
            L_["enter"] = "slam"; shake.append([L_["in"], .35, 8]); fx.append(["thud", L_["in"], -14])
# chapter cards and key shocks: a flash cut
for s in shots:
    if any(x in " ".join(text_of(L_) for L_ in s["layers"]) for x in ("Moscow burns", "Bloody Sunday", "NUCLEAR", "WINTER", "22 June 1941")):
        s["cut"] = "flash"
for s in shots:   # labels never sit in the caption band
    for L_ in s["layers"]:
        if isinstance(L_.get("img"), dict) and L_["y"] > 860: L_["y"] = 250

# captions from the script words, timed by the transcriber
sys.path.insert(0, HERE); from numwords import digits
Wt = [(float(x) / SPEED, float(y) / SPEED, w.strip()) for x, y, w in (l.split(None, 2) for l in open(WORDS) if l.strip())]
STOP = {"and", "the", "a", "an", "of", "to", "in", "on", "it", "is"}
def norm(w): return re.sub(r"[^a-z0-9']", "", w.lower())
caps = []
for i, ln in enumerate(L):
    if SPK[i] != "N": continue
    text = digits(re.sub(r"\[[^\]]*\]", "", SCRIPT[i]))
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
