#!/usr/bin/env python3
"""Shot plan for the India full video, chapters 2-13 + ending (the pilot part, hook + ch1, is rendered separately and joined in front).
Helpers, timeline close and retention pass are the pilot's (pilot/plan_pilot.py).

Shots are pinned to script LINES (index into script_ch2-13.md), never to fixed seconds.
Usage: python3 plan_full.py lines.json spec.json words.txt [speed] [--punch=7]
Also writes clips3d.json (3D globe clips, local times) next to spec.json.
"""
import json, sys, os, re, textwrap, difflib
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..", "..", "..")
A1 = os.path.join(HERE, "..", "art"); A2 = os.path.join(HERE, "..", "art2"); C1 = os.path.join(HERE, "..", "pilot", "cards"); C2 = os.path.join(HERE, "cards")
ARC = os.path.join(ROOT, "outputs", "fetch", "in-pilot-archive")
ARC2 = os.path.join(ROOT, "outputs", "fetch", "in-full-archive"); ARC3 = os.path.join(ROOT, "outputs", "fetch", "in-full-archive2"); ARC4 = os.path.join(ROOT, "outputs", "fetch", "in-full-archive3"); CLIPS = os.path.join(HERE, "clips3d")   # archive3 = replacements, searched first
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
args = [a for a in sys.argv[1:] if not a.startswith("--")]
L = json.load(open(args[0])); END = L[-1]["t1"] + 1.6
WORDS = args[2]; SPEED = float(args[3]) if len(args) > 3 else 1.0
PUNCH = float(next((a.split("=")[1] for a in sys.argv if a.startswith("--punch=")), 7))

# ---- script (speaker + English text per line) ----
SCRIPT, SPK, CHAP = [], [], {}
chap = None
for r in open(os.path.join(HERE, "script_ch2-13.md"), encoding="utf-8"):
    r = r.strip(); m = re.match(r"# (HOOK|CHAPTER (\d+)|ENDING)", r)
    if m: chap = 0 if m.group(1) == "HOOK" else (int(m.group(2)) if m.group(2) else 99); CHAP[chap] = len(SCRIPT); continue
    m = re.match(r"^([A-Z][A-Z .'&]*?):\s*(.+)$", r)
    if m and chap is not None: SPK.append(m.group(1)); SCRIPT.append(m.group(2))
assert len(SCRIPT) == len(L), (len(SCRIPT), len(L))
EN = [re.sub(r"\[[^\]]*\]\s*", "", s).replace("*", "").replace("‡", "") for s in SCRIPT]

def T(i, f=0.0):
    x = L[i]; return x["t0"] + (x["t1"] - x["t0"]) * f if f >= 0 else x["t0"] + f
MISS = []
def kw(i, word):
    s = EN[i]; k = s.find(word)
    if k < 0: k = s.lower().find(word.lower())
    if k < 0: MISS.append((i, word))
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
    for d in (ARC4, ARC3, ARC2, ARC):
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
    """A 3D globe clip (rendered by ../clips3d.py). All times absolute; cam = [[t, lon, lat, dist], ...]."""
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


# ---- (body of plan_full.py: real-speaker portraits, skits, chapters 2-13 + ending) ----
# Real people speak through real artwork (framed portrait + speech bubble + "dramatised" tag). Toy figures only for
# fictional / unnamed people.
REAL = {"ALEXANDER": ("alexander_bust", None), "PORUS": ("porus_coin", None), "CHANAKYA": ("chanakya_sculpture", (0, 0, .56, 1)),
        "ARYABHATA": ("aryabhata_statue", None), "TUGHLAQ": ("tughlaq_token_coin", (0, 0, .52, 1)), "BABUR": ("babur_portrait", None),
        "SHAH JAHAN": ("shah_jahan_old", (.31, .24, .69, .6)), "VICTORIA": ("victoria_portrait", None), "GANDHI": ("gandhi_portrait", None),
        "PATEL": ("patel_portrait", None)}
CAST = {"TRAVELLER": "c_traveller", "TEACHER": "c_guru", "STUDENT": "c_student", "MINISTER": "c_minister", "OFFICIAL": "c_gupta_official",
        "COURTIER": "c_courtier", "SERVANT": "c_mughal_servant", "DIRECTOR ONE": "c_director1", "DIRECTOR TWO": "c_director2",
        "OFFICER": "c_br_officer", "MAHARAJA": "c_maharaja", "PILOT": "c_pilot"}
def crop(key, box):
    p = arc(key)
    if not p or not box: return p
    out = os.path.join(HERE, "cards", f"_crop_{key}.jpg")
    if not os.path.exists(out):
        im = Image.open(p).convert("RGB"); W_, H_ = im.size
        im.crop((int(box[0] * W_), int(box[1] * H_), int(box[2] * W_), int(box[3] * H_))).save(out, quality=92)
    return out
def portrait(who, x, t, enter="pop", maxh=430, y=595):
    key, box = REAL[who]; p = crop(key, box)
    if not p: return None
    f = frame(p); im = Image.open(f); w = int(min(620, maxh * im.width / im.height))
    d = {"img": f, "x": x, "y": y, "h": aspect_h(f, w), "enter": enter, "shadow": True}
    if t is not None: d["in"] = t
    return d
def skit(i0, i1, bg, pos, cast=None):
    """pos: {SPEAKER: (x, flip)}; the first speaker is there from the start, the others slide in on their first line.
    Real people appear as their framed real portrait; fictional ones as toy figures."""
    cast = dict(CAST, **(cast or {})); t0 = T(i0, -.3); lines = list(range(i0, i1 + 1)); lay = []; real = False
    for k, (who, (x, flip)) in enumerate(pos.items()):
        mine = [i for i in lines if SPK[i] == who]; first = mine[0] if mine else i0
        if who in REAL:
            real = True; lay.append(portrait(who, x, None if k == 0 else T(first, -.5)))
            lay.append(txt(who.title(), x, 855, None if k == 0 else T(first, -.5), size=40, box="#222222"))
        else:
            lay.append(ch(cast[who], x, enter=("slideL" if x < 960 else "slideR") if k else "none", t=None if k == 0 else T(first, -.5), flip=flip, talks=mine,
                          h=640 if who == "TRAVELLER" else 560, y=1030 if who == "TRAVELLER" else 1045))
    for i in lines:
        x = pos.get(SPK[i], (960, False))[0]; lay.append(say(i, x, y=120 if real else 380))
    if real: lay.append(txt("dramatised", 1780, 60, t0, size=28, box="#000000aa", scale=1.0))
    for L_ in lay:
        if L_ and L_.get("in") is None: L_.pop("in", None)
    return shot(t0, a(bg) or LAST[0], lay, cam=[[t0, .5, .55, 1.0], [T(i1, 1), .5, .55, 1.12]])
def person(i, key, name, word=None, extra=(), side=1250):
    """Narrator introduces a real person: their real picture on a board with a name tag."""
    t0 = T(i, -.15); tn = K(i, word) if word else t0
    return board(t0, [imgcard(arc(key), side, 640, 620, t0 + .05, framed=True),
                      txt(name, side, 990 - 60, tn, size=60, box="#c99400")] + list(extra))
def seq(i, items, x=1250, y=600, size=86, box="#222222", extra=()):
    """One board per keyword: items = [(keyword, text)], hard cuts."""
    for k, (w, s) in enumerate(items):
        t0 = T(i, -.15) if k == 0 else K(i, w)
        b = board(t0, [txt(s, x, y, t0 + .05, size=size, box=box)] + list(extra)); b["cut"] = "hard" if k else "curve"
def years(s, t, x=330, y=230): return lab(s, t, x=x, y=y, size=100)

# coordinates (lon, lat)
P = dict(PATAL=(85.14, 25.6), KALINGA=(85.84, 20.19), TAXILA=(72.83, 33.75), JHELUM=(73.73, 32.93), BEAS=(75.4, 31.5), BABYLON=(44.42, 32.54),
         PELLA=(22.5, 40.76), PERSEP=(52.89, 29.93), BODHGAYA=(84.99, 24.7), SARNATH=(83.03, 25.38), LUMBINI=(83.28, 27.47), MUZIRIS=(76.2, 10.15),
         BERENIKE=(35.47, 23.91), ALEXANDRIA=(29.9, 31.2), ROME=(12.5, 41.9), THANJ=(79.14, 10.79), PALEMBANG=(104.75, -2.99), GHAZNI=(68.42, 33.55),
         SOMNATH=(70.4, 20.89), DELHI=(77.21, 28.61), TARAIN=(76.9, 29.8), DAULAT=(75.21, 19.94), KABUL=(69.17, 34.53), PANIPAT=(76.97, 29.39),
         AGRA=(78.01, 27.18), PUNE=(73.86, 18.52), MASHHAD=(59.6, 36.3), LONDON=(-0.12, 51.5), CAPE=(18.4, -33.9), SURAT=(72.83, 21.17),
         MADRAS=(80.27, 13.08), BOMBAY=(72.88, 19.08), CALCUTTA=(88.36, 22.57), PLASSEY=(88.25, 23.8), MEERUT=(77.7, 28.98), JHANSI=(78.57, 25.45),
         AMRITSAR=(74.87, 31.63), SABARMATI=(72.58, 23.06), DANDI=(72.8, 20.89), SRIRANGA=(76.69, 12.42), LAHORE=(74.35, 31.55), NALANDA=(85.44, 25.13),
         HAMPI=(76.46, 15.33), DAULATABAD=(75.21, 19.94), MEGA=(85.14, 25.6), BENGALURU=(77.59, 12.97), HYDERABAD=(78.49, 17.39), KARACHI=(67.0, 24.86),
         DHAKA=(90.41, 23.81), BAKU=(49.87, 40.41), BACTRIA=(66.9, 36.76), PESHAWAR=(71.57, 34.01), KANDAHAR=(65.7, 31.6), RANGOON=(96.16, 16.84),
         SRINAGAR=(74.8, 34.08), MATHURA=(77.67, 27.49), MEWAR=(73.71, 24.58))
def pt(k): return list(P[k])

# ======================= CHAPTER 2: THE HYMNS =======================
c = CHAP[2]
LAST[0] = a("in_ganga")
chapter_card(2, c)
plate(T(c, .2), a("in_ganga"), layers=[years("~1500 BCE", T(c, .25)), tag("The Vedas", K(c, "know"), y=420)], zoom=(1.0, 1.12))
board(T(c + 1, -.15), [txt("Rigveda", 1250, 330, K(c + 1, "Rigveda"), size=110, box="#c99400"),
                       txt("3,000+ years old\n1,000+ hymns", 1250, 640, K(c + 1, "three"), size=80, box="#222222")])
board(T(c + 2, -.15), [txt("Where did they\ncome from?", 1250, 500, T(c + 2, .05), size=96, box="#d6423a")])
t = T(c + 3, -.15)
globe("G_vedic", t, [[t, 72, 32, 3.0], [T(c + 3, 1), 70, 34, 2.6]],
      arcs=[arcp([[62.0, 43.0], [65.0, 39.0], [68.5, 36.0], [71.5, 33.5], [74.0, 31.0]], K(c + 3, "Indo-Aryan"), 2.6, col="#FF8A3A")],
      layers=[tag("Theory 1: migration from Central Asia", K(c + 3, "Indo-Aryan"), x=1300, y=300), tag("Clues: languages + ancient DNA", K(c + 3, "DNA"), x=1300, y=440)])
board(T(c + 4, -.15), [txt("Theory 2: grew within India", 1250, 420, T(c + 4, .05), size=74, box="#222222"),
                       txt("Debate: still going", 1250, 700, K(c + 4, "debate"), size=80, box="#d6423a")])
quip(c + 5)
plate(T(c + 6, -.15), a("in_hermitage"), layers=[lab("Not written down", K(c + 6, "written"), size=96, box="#d6423a"),
                                                 tag("3,000 years by memory", K(c + 6, "memor"), y=420)], zoom=(1.0, 1.15))
board(T(c + 7, -.15), [txt("Forwards", 1250, 300, K(c + 7, "forwards"), size=86, box="#222222"),
                       txt("Backwards", 1250, 480, K(c + 7, "backwards"), size=86, box="#222222"),
                       txt("Word pairs", 1250, 660, K(c + 7, "pairs"), size=86, box="#222222")])
board(T(c + 8, -.15), [txt("UNESCO", 1250, 360, K(c + 8, "UNESCO"), size=110, box="#2f8f4f"),
                       txt("Intangible heritage\nof humanity", 1250, 640, K(c + 8, "intangible"), size=74, box="#222222")])
skit(c + 9, c + 13, "in_hermitage", {"TEACHER": (560, False), "STUDENT": (1360, True)})
t = T(c + 14, -.15)
globe("G_ganga", t, [[t, 78, 28, 2.4], [T(c + 14, 1), 83, 26, 2.1]],
      arcs=[arcp([[74.5, 30.5], [77.5, 29.0], [80.5, 27.0], [83.5, 25.8], [86.0, 25.3]], T(c + 14, .1), 3.0, col="#FFD84A")],
      layers=[lab("The Ganga plain", K(c + 14, "Ganga"), size=86)])
plate(T(c + 15, -.15), a("in_ganga"), layers=[tag("Villages → towns → kingdoms", T(c + 15, .1), y=300), years("~600 BCE", K(c + 15, "six")),
                                             tag("16 kingdoms", K(c + 15, "sixteen"), y=460)], zoom=(1.1, 1.25), c=(.6, .5))
board(T(c + 16, -.15), [txt("Priests", 1250, 260, T(c + 16, .2), size=74, box="#222222"), txt("Warriors", 1250, 420, T(c + 16, .25), size=74, box="#222222"),
                        txt("Traders", 1250, 580, T(c + 16, .3), size=74, box="#222222"), txt("Workers", 1250, 740, T(c + 16, .35), size=74, box="#222222")])
board(T(c + 17, -.15), [txt("Upanishads", 1250, 360, K(c + 17, "Upanishads"), size=100, box="#c99400"),
                        txt("Big questions", 1250, 620, T(c + 17, .1), size=80, box="#222222")])
quip(c + 18)
t = T(c + 19, -.15)
globe("G_magadha", t, [[t, 82, 26, 2.2], [T(c + 19, 1), 85, 25.5, 1.8]],
      pins=[pin(*P["PATAL"], K(c + 19, "Magadha"), "Magadha", "#FF5A3A", size=64)],
      layers=[tag("Faster. Hungrier.", K(c + 19, "hungrier"), x=1450, y=760)])
plate(T(c + 20, -.15), a("in_palace_hall"), layers=[lab("Two princes", K(c + 20, "two"), size=96)], zoom=(1.0, 1.15))

# ======================= CHAPTER 3: THE PRINCE WHO LEFT =======================
c = CHAP[3]
chapter_card(3, c)
pic(T(c, .25), "buddha_sarnath", [lab("Siddhartha Gautama", K(c, "Siddhartha"), size=80, box="#c99400"), years("~2,500 years ago", K(c, "two"), x=420, y=880)])
plate(T(c + 1, -.15), a("in_palace_hall"), layers=[tag("No sickness", K(c + 1, "sickness"), y=300), tag("No old age", K(c + 1, "old"), y=440)], zoom=(1.0, 1.15))
board(T(c + 2, -.15), [txt("An old man", 1250, 230, K(c + 2, "old man"), size=70, box="#222222"), txt("A sick man", 1250, 390, K(c + 2, "sick"), size=70, box="#222222"),
                       txt("A dead body", 1250, 550, K(c + 2, "dead"), size=70, box="#222222"), txt("A calm monk", 1250, 710, K(c + 2, "calm"), size=70, box="#2f8f4f")])
quip(c + 3)
plate(T(c + 4, -.15), a("in_palace_hall"), layers=[lab("Age 29: he left", T(c + 4, .1), size=90, box="#d6423a")], zoom=(1.2, 1.0))
plate(T(c + 5, -.15), a("in_bodhgaya"), layers=[lab("Bodh Gaya", K(c + 5, "Bodh"), size=100)], zoom=(1.0, 1.15))
pic(T(c + 6, -.15), "mahabodhi", [lab("The Buddha: \"the awakened one\"", K(c + 6, "Buddha"), size=70, box="#c99400"), tag("First sermon: Sarnath", K(c + 6, "Sarnath"), y=420)])
board(T(c + 7, -.15), [txt("The middle way", 1250, 330, K(c + 7, "middle"), size=100, box="#c99400"),
                       txt("Not luxury.\nNot starving.", 1250, 640, K(c + 7, "luxury"), size=80, box="#222222")])
pic(T(c + 8, -.15), "mahavira", [lab("Mahavira", K(c + 8, "Mahavira"), size=100, box="#c99400"), tag("Ahimsa: harm no living thing", K(c + 8, "ahimsa"), y=420)])
quip(c + 9)
t = T(c + 10, -.15)
globe("G_nanda", t, [[t, 84, 25.5, 2.0], [T(c + 10, 1), 82, 25.5, 2.4]],
      pins=[pin(*P["PATAL"], T(c + 10, .1), "Magadha", "#FF5A3A", size=60)],
      layers=[tag("The Nandas: huge army", K(c + 10, "Nanda"), x=1400, y=300), tag("Huge treasury", T(c + 10, .8), x=1400, y=440)])
t = T(c + 11, -.15)
globe("G_alex", t, [[t, 25, 38, 3.4], [T(c + 11, 1), 45, 34, 3.4]],
      arcs=[arcp([pt("PELLA"), [27, 38], [35, 36.5], pt("BABYLON"), pt("PERSEP")], T(c + 11, .1), 4.0, col="#FF5A3A")],
      pins=[pin(*P["PELLA"], T(c + 11, .1), "Macedonia", "#FF5A3A"), pin(*P["PERSEP"], K(c + 11, "mightiest"), "Persia", "#FF5A3A")],
      layers=[tag("Conquered the Persian Empire", K(c + 11, "mightiest"), x=1400, y=300)])
pic(T(c + 12, -.15), "alexander_mosaic", [lab("Alexander", K(c + 12, "Alexander"), size=110, box="#d6423a")], zoom=(1.3, 1.5), c0=(.3, .5))
t = T(c + 13, -.15)
globe("G_alex2", t, [[t, 58, 33, 3.0], [T(c + 13, 1), 72, 33, 2.2]],
      arcs=[arcp([pt("PERSEP"), [60, 33], pt("BACTRIA"), pt("KABUL"), pt("TAXILA"), pt("JHELUM")], T(c + 13, .05), 4.0, col="#FF5A3A")],
      pins=[pin(*P["JHELUM"], K(c + 13, "Jhelum"), "Jhelum river", "#FFD84A")],
      layers=[years("326 BCE", K(c + 13, "three")), tag("King Porus", K(c + 13, "Porus"), x=1400, y=420)])
skit(c + 15, c + 17, "in_jhelum", {"ALEXANDER": (560, False), "PORUS": (1360, True)})
board(T(c + 14, -.15), [imgcard(arc("porus_coin"), 1220, 620, 700, T(c + 14, -.1), framed=True),
                        txt("Alexander won...", 1220, 220, T(c + 14, .05), size=70, box="#222222")])
t = T(c + 18, -.15)
globe("G_beas", t, [[t, 73.5, 32, 1.8], [T(c + 18, 1), 75, 31.5, 1.6]],
      arcs=[arcp([pt("JHELUM"), [74.5, 32.2], pt("BEAS")], T(c + 18, .1), 2.0, col="#FF5A3A")],
      pins=[pin(*P["BEAS"], K(c + 18, "Beas"), "River Beas", "#FFD84A", size=56)],
      layers=[lab("...and stopped", K(c + 18, "stopped"), size=90, box="#d6423a")])
board(T(c + 19, -.15), [txt("8 years marching", 1250, 300, T(c + 19, .05), size=80, box="#222222"),
                        txt("Nanda army waiting", 1250, 500, K(c + 19, "Nanda"), size=80, box="#222222"),
                        txt("Monsoon rains", 1250, 700, T(c + 19, .75), size=80, box="#222222")])
board(T(c + 20, -.15), [txt("They refused.", 1250, 420, T(c + 20, .05), size=100, box="#d6423a"), txt("Alexander turned back", 1250, 680, K(c + 20, "turn"), size=74, box="#222222")])
quip(c + 21)
board(T(c + 22, -.15), [imgcard(arc("alexander_bust"), 1050, 620, 460, T(c + 22, -.1), framed=True), txt("Died in Babylon\nage 32", 1560, 560, K(c + 22, "Babylon"), size=66, box="#222222")])
quip_like = board(T(c + 23, -.15), [imgcard(arc("chandragupta_jain"), 1250, 640, 760, T(c + 23, -.1), framed=True),
                                    txt("A young man... and a teacher with a plan", 1050, 180, K(c + 23, "teacher"), size=56, box="#222222")])

# ======================= CHAPTER 4: THE FIRST EMPIRE =======================
c = CHAP[4]
chapter_card(4, c)
board(T(c, .2), [imgcard(crop("chanakya_sculpture", None), 1250, 640, 900, T(c, .2), framed=True), txt("Chandragupta  +  Chanakya", 1250, 180, K(c, "Chanakya"), size=66, box="#c99400")])
plate(T(c + 1, -.15), a("in_pataliputra"), layers=[tag("Insulted at the Nanda court", K(c + 1, "insulted"), y=300), tag("Swore revenge", T(c + 1, .7), y=440)], zoom=(1.0, 1.15))
quip(c + 2)
plate(T(c + 3, -.15), a("in_pataliputra"), layers=[years("~321 BCE", K(c + 3, "three")), tag("The Nandas fall", K(c + 3, "overthrew"), y=420)], zoom=(1.15, 1.3), c=(.6, .5))
t = T(c + 4, -.15)
globe("G_maurya", t, [[t, 80, 24, 3.0], [T(c + 4, 1), 76, 26, 2.6]],
      over=[ov("ov_maurya", fadein(K(c + 4, "united"), .8, 1.2)), ove("ov_maurya_edge", fadein(K(c + 4, "united"), 1, 1.2)), ove("ov_in_edge", [[0, .45]])],
      pins=[pin(*P["PATAL"], T(c + 4, .1), "Pataliputra", "#FFD84A", size=56)],
      layers=[lab("The Maurya Empire", K(c + 4, "united"), size=86, box="#c99400")])
board(T(c + 5, -.15), [txt("Seleucus", 1250, 300, K(c + 5, "Seleucus"), size=96, box="#222222"), txt("Lands for 500 elephants", 1250, 560, T(c + 5, .6), size=74, box="#c99400")])
plate(T(c + 6, -.15), a("in_pataliputra"), layers=[lab("Pataliputra", K(c + 6, "Pataliputra"), size=96), tag("Megasthenes, Greek envoy", K(c + 6, "Megasthenes"), y=420)],
      zoom=(1.0, 1.2), c=(.45, .5))
plate(T(c + 7, -.15), a("in_maurya_office"), layers=[lab("Arthashastra", K(c + 7, "Arthashastra"), size=100, box="#c99400"), tag("Taxes · Spies · War", T(c + 7, .6), y=420)],
      zoom=(1.0, 1.12))
skit(c + 8, c + 13, "in_maurya_office", {"MINISTER": (1360, True), "CHANAKYA": (560, False)})
pic(T(c + 14, -.15), "shravanabelagola", [lab("Became a Jain monk", T(c + 14, .3), size=86, box="#222222")])
board(T(c + 15, -.15), [imgcard(arc("ashoka_relief"), 1250, 640, 760, T(c + 15, -.1), framed=True), txt("Ashoka", 1250, 180, K(c + 15, "Ashoka"), size=110, box="#c99400")])
plate(T(c + 16, -.15), a("in_kalinga"), layers=[years("~261 BCE", K(c + 16, "two")), lab("Kalinga", K(c + 16, "Kalinga"), size=100), tag("Today's Odisha", K(c + 16, "Odisha"), y=420)],
      zoom=(1.0, 1.15))
pic(T(c + 17, -.15), "ashoka_edict", [lab("100,000 killed", K(c + 17, "hundred"), size=96, box="#d6423a"), tag("In his own words, in stone", T(c + 17, .1), y=420)])
board(T(c + 18, -.15), [txt("He was SORRY.", 1250, 560, K(c + 18, "sorry"), size=120, box="#d6423a")])
quip(c + 19)
pic(T(c + 20, -.15), "sanchi", [lab("Dhamma", K(c + 20, "dhamma"), size=110, box="#c99400"), tag("Kindness · Tolerance", K(c + 20, "kindness"), y=420)])
pic(T(c + 21, -.15), "ashoka_edict", [lab("Brahmi script", K(c + 21, "Brahmi"), size=96)], zoom=(1.3, 1.5))
board(T(c + 22, -.15), [years("1837", K(c + 22, "eighteen"), x=1250, y=400), txt("James Prinsep cracks Brahmi", 1250, 650, T(c + 22, .6), size=66, box="#222222")])
pic(T(c + 23, -.15), "lion_capital", [lab("India's national emblem", T(c + 23, .7), size=80, box="#c99400")])
t = T(c + 24, -.15)
globe("G_chakra", t, [[t, 79, 22, 2.8], [T(c + 24, 1), 79, 22, 2.5]], over=[ov("ov_in_flag", fadein(t + .1, .9, .6)), ove("ov_in_edge", [[0, 1]])],
      layers=[lab("Ashoka Chakra", K(c + 24, "Ashoka Chakra"), size=96, box="#1d3f8f")])
quip(c + 25)
board(T(c + 26, -.15), [txt("Empires built by one man...", 1250, 600, T(c + 26, .05), size=80, box="#222222")])
plate(T(c + 27, -.15), a("in_pataliputra"), layers=[tag("Last Maurya killed by his general", T(c + 27, .3), y=300)], zoom=(1.3, 1.0))
cycle(T(c + 27, .75), "shatter")
t = T(c + 28, -.15)
globe("G_passes", t, [[t, 74, 30, 2.6], [T(c + 28, 1), 70, 34, 2.2]],
      arcs=[arcp([[64, 38], pt("BACTRIA"), pt("KABUL"), pt("PESHAWAR"), pt("TAXILA")], T(c + 28, .2), 2.6, col="#FF8A3A")],
      layers=[tag("Through the mountain passes", T(c + 28, .2), y=300)])

# ======================= CHAPTER 5: THE GOLDEN AGE =======================
c = CHAP[5]
chapter_card(5, c)
board(T(c, .2), [txt("Many kingdoms at once", 1250, 400, T(c, .25), size=80, box="#222222"), txt("...and richer", 1250, 640, T(c, .8), size=80, box="#c99400")])
pic(T(c + 1, -.15), "kanishka_coin", [lab("Kanishka", K(c + 1, "Kanishka"), size=100, box="#c99400"), tag("The Kushans", K(c + 1, "Kushans"), y=420)])
t = T(c + 2, -.15)
globe("G_rome", t, [[t, 60, 20, 3.6], [T(c + 2, 1), 40, 25, 3.8]],
      arcs=[arcp([pt("MUZIRIS"), [70, 11], [60, 13], [50, 13], [43.5, 12.6], [38, 19], pt("BERENIKE")], K(c + 2, "monsoon"), 3.0),
            arcp([pt("BERENIKE"), [32.5, 26.5], pt("ALEXANDRIA"), [20, 37], pt("ROME")], K(c + 2, "Rome"), 2.4)],
      pins=[pin(*P["MUZIRIS"], T(c + 2, .1), "Muziris", "#FFD84A"), pin(*P["ROME"], K(c + 2, "Rome"), "Rome", "#FF5A3A")],
      layers=[tag("Pepper · Cotton · Gems", K(c + 2, "pepper"), x=1400, y=300)])
board(T(c + 3, -.15), [txt("Roman gold → India", 1250, 300, T(c + 3, .05), size=86, box="#c99400"), txt("Pliny complains", 1250, 560, K(c + 3, "Pliny"), size=80, box="#222222")])
quip(c + 4)
t = T(c + 5, -.15)
globe("G_gupta", t, [[t, 82, 25, 2.8], [T(c + 5, 1), 80, 24, 2.6]],
      over=[ov("ov_gupta", fadein(K(c + 5, "Guptas"), .8, 1.0)), ove("ov_gupta_edge", fadein(K(c + 5, "Guptas"), 1, 1.0)), ove("ov_in_edge", [[0, .45]])],
      layers=[years("~320 CE", K(c + 5, "three")), lab("The Guptas", K(c + 5, "Guptas"), size=100, box="#c99400")])
pic(T(c + 6, -.15), "gupta_coin", [lab("India's classical age", K(c + 6, "classical"), size=84, box="#c99400"), tag("Ideas, not battles", T(c + 6, .7), y=420)])
plate(T(c + 7, -.15), a("in_palace_hall"), layers=[lab("Kalidasa", K(c + 7, "Kalidasa"), size=100), tag("Plays still performed today", T(c + 7, .6), y=420)], zoom=(1.0, 1.12))
plate(T(c + 8, -.15), a("in_observatory"), layers=[lab("Aryabhata, age 23", K(c + 8, "Aryabhata"), size=86, box="#c99400"), tag("The Earth spins", K(c + 8, "Earth"), y=420)],
      zoom=(1.0, 1.15))
board(T(c + 9, -.15), [txt("π ≈ 3.1416", 1250, 560, K(c + 9, "pi"), size=130, box="#1d3f8f")])
board(T(c + 10, -.15), [txt("1 2 3 4 5 6 7 8 9", 1250, 400, T(c + 10, .4), size=96, box="#222222"), txt("+ 0", 1250, 640, T(c + 10, .85), size=130, box="#c99400")])
board(T(c + 11, -.15), [txt("Brahmagupta", 1250, 330, K(c + 11, "Brahmagupta"), size=96, box="#c99400"), txt("Rules for ZERO", 1250, 620, K(c + 11, "zero"), size=96, box="#d6423a")])
board(T(c + 12, -.15), [txt("India → Arab world → Europe", 1250, 400, T(c + 12, .1), size=70, box="#222222"), txt("\"Arabic\" numerals", 1250, 660, K(c + 12, "Ar"), size=86, box="#c99400")])
skit(c + 13, c + 16, "in_observatory", {"OFFICIAL": (1360, True), "ARYABHATA": (560, False)})
pic(T(c + 17, -.15), "nalanda_ruins", [lab("Nalanda", K(c + 17, "Nalanda"), size=110, box="#c99400"), tag("Students from across Asia", T(c + 17, .2), y=420)])
pic(T(c + 18, -.15), "iron_pillar", [lab("Iron Pillar of Delhi", K(c + 18, "Iron"), size=84), tag("1,600 years, barely any rust", T(c + 18, .7), y=420)])
quip(c + 19)
t = T(c + 20, -.15)
globe("G_huna", t, [[t, 72, 32, 2.8], [T(c + 20, 1), 76, 28, 2.6]],
      over=[ov("ov_gupta", [[0, .8], [T(c + 20, .5), .8], [T(c + 20, .9), 0]]), ove("ov_in_edge", [[0, .45]])],
      arcs=[arcp([[66, 39], pt("BACTRIA"), pt("KABUL"), pt("PESHAWAR"), [75, 31]], K(c + 20, "Huna"), 2.4, col="#FF5A3A")],
      layers=[lab("The Huna", K(c + 20, "Huna"), size=96, box="#d6423a")])
plate(T(c + 21, -.15), a("in_thanjavur"), layers=[lab("Meanwhile, in the south...", T(c + 21, .1), size=80)], zoom=(1.0, 1.12))
pic(T(c + 22, -.15), "brihadeeswarar", [lab("The Cholas", K(c + 22, "Chola"), size=100, box="#c99400"), tag("Rajaraja the Great", K(c + 22, "Rajaraja"), y=420)])
t = T(c + 23, -.15)
globe("G_chola", t, [[t, 85, 10, 3.0], [T(c + 23, 1), 95, 5, 3.0]],
      over=[ov("ov_chola", [[0, .85]]), ove("ov_chola_edge", [[0, 1]]), ov("ov_srilanka_n", [[0, .8]])],
      arcs=[arcp([[80.3, 13.0], [86, 10], [92, 7], [97, 5], [101, 2.5], pt("PALEMBANG")], K(c + 23, "fleet"), 3.0, col="#FFD84A")],
      pins=[pin(*P["THANJ"], T(c + 23, .05), "Thanjavur", "#FFD84A"), pin(*P["PALEMBANG"], K(c + 23, "Srivijaya"), "Srivijaya", "#FF5A3A")],
      layers=[lab("Rajendra's fleet", K(c + 23, "Rajendra"), size=86, box="#c99400")])
quip(c + 24)
board(T(c + 25, -.15), [txt("But in the north...", 1250, 600, T(c + 25, .05), size=90, box="#d6423a")])

# ======================= CHAPTER 6: THE SULTANS =======================
c = CHAP[6]
chapter_card(6, c)
t = T(c, .15)
globe("G_ghazni", t, [[t, 70, 30, 2.6], [T(c, 1), 70, 26, 2.4]],
      arcs=[arcp([pt("GHAZNI"), [69.5, 30], [70, 26], pt("SOMNATH")], T(c, .5), 2.4, col="#FF5A3A")],
      pins=[pin(*P["GHAZNI"], T(c, .3), "Ghazni", "#FF5A3A"), pin(*P["SOMNATH"], T(c, .7), "Somnath", "#FFD84A")],
      layers=[lab("Mahmud of Ghazni", K(c, "Mahmud"), size=86, box="#d6423a"), years("~1000 CE", K(c, "year")), tag("17 raids", T(c, .8), y=420)])
board(T(c + 1, -.15), [txt("He came for gold", 1250, 360, T(c + 1, .05), size=90, box="#c99400"), txt("Somnath temple looted", 1250, 620, K(c + 1, "Somnath"), size=76, box="#d6423a")])
plate(T(c + 2, -.15), a("in_delhi_court"), layers=[lab("Muhammad of Ghor", K(c + 2, "Mu"), size=86)], zoom=(1.0, 1.12))
board(T(c + 3, -.15), [years("1191", K(c + 3, "eleven"), x=1250, y=260), txt("Tarain", 1250, 480, K(c + 3, "Tarain"), size=90, box="#222222"),
                       txt("Prithviraj Chauhan wins", 1250, 700, K(c + 3, "Prithviraj"), size=70, box="#2f8f4f")])
board(T(c + 4, -.15), [txt("1192: same battlefield", 1250, 400, T(c + 4, .2), size=80, box="#222222"), txt("Prithviraj lost", 1250, 650, K(c + 4, "lost"), size=96, box="#d6423a")])
quip(c + 5)
pic(T(c + 6, -.15), "qutb_minar", [years("1206", K(c + 6, "twelve")), lab("The Delhi Sultanate", K(c + 6, "Delhi Su"), size=84, box="#c99400")])
pic(T(c + 7, -.15), "nalanda_ruins", [lab("Nalanda attacked", K(c + 7, "attacked"), size=90, box="#d6423a"), tag("Bakhtiyar Khalji", K(c + 7, "Bakhtiyar"), y=420)], zoom=(1.2, 1.0))
t = T(c + 8, -.15)
globe("G_sultanate", t, [[t, 79, 25, 2.8], [T(c + 9, 1), 75, 30, 3.4]],
      over=[ov("ov_sultanate", fadein(t + .2, .8, 1.0)), ove("ov_sultanate_edge", fadein(t + .2, 1, 1.0)), ove("ov_in_edge", [[0, .45]])],
      arcs=[arcp([[100, 47], [85, 44], [72, 40], [68, 36], [70, 33]], K(c + 9, "Mongol"), 2.6, col="#FF5A3A")],
      layers=[tag("5 dynasties · 300 years", T(c + 8, .2), x=1400, y=300), lab("Alauddin Khalji", K(c + 9, "Alauddin"), size=84), tag("Mongols: stopped", K(c + 9, "Mongol"), x=1400, y=440)])
plate(T(c + 10, -.15), a("in_delhi_court"), layers=[lab("Price controls", K(c + 10, "price"), size=100, box="#c99400"), tag("Grain · Horses · Cloth", K(c + 10, "grain"), y=420)],
      zoom=(1.0, 1.15))
quip(c + 11)
pic(T(c + 12, -.15), "tughlaqabad", [lab("Muhammad bin Tughlaq", K(c + 12, "Muhammad"), size=80, box="#c99400"), tag("Clever... and strange", T(c + 12, .6), y=420)])
t = T(c + 13, -.15)
globe("G_daulat", t, [[t, 77, 25, 2.2], [T(c + 13, 1), 76, 24, 2.2]],
      arcs=[arcp([pt("DELHI"), [76.5, 25.5], [75.8, 22.5], pt("DAULATABAD")], K(c + 13, "Daulatabad"), 2.4, col="#FF5A3A")],
      pins=[pin(*P["DELHI"], T(c + 13, .1), "Delhi", "#FFD84A"), pin(*P["DAULATABAD"], K(c + 13, "Daulatabad"), "Daulatabad", "#FF5A3A")],
      layers=[years("1327", K(c + 13, "thirteen")), tag("~1,100 km", T(c + 13, .8), x=1400, y=420)])
skit(c + 14, c + 18, "in_delhi_court", {"TUGHLAQ": (560, False), "COURTIER": (1360, True)})
quip(c + 19)
pic(T(c + 20, -.15), "tughlaq_token_coin", [lab("Copper coins = silver?", K(c + 20, "copper"), size=86, box="#222222")])
board(T(c + 21, -.15), [txt("Fake money at home", 1250, 400, K(c + 21, "home"), size=86, box="#d6423a"), txt("Huge piles", 1250, 640, K(c + 21, "piles"), size=86, box="#222222")])
quip(c + 22)
plate(T(c + 23, -.15), a("in_delhi_court"), layers=[years("1398", K(c + 23, "thirteen")), lab("Timur sacks Delhi", K(c + 23, "Timur"), size=90, box="#d6423a")], zoom=(1.3, 1.0))
pic(T(c + 24, -.15), "hampi", [lab("Vijayanagara", K(c + 24, "Vijayanagara"), size=96, box="#c99400"), tag("Capital: Hampi", K(c + 24, "capital"), y=420)])
board(T(c + 25, -.15), [txt("Something new was being MADE", 1250, 600, K(c + 25, "made"), size=74, box="#c99400")])
pic(T(c + 26, -.15), "qutb_minar", [tag("Arches · Domes · Minarets", K(c + 26, "arches"), y=300), tag("Amir Khusrau", K(c + 26, "Amir"), y=440)], zoom=(1.3, 1.1))
board(T(c + 27, -.15), [txt("Urdu", 1250, 360, K(c + 27, "Urdu"), size=120, box="#2f8f4f"), txt("Hindi + Persian + Arabic + Turkish", 1250, 620, T(c + 27, .6), size=60, box="#222222")])
cycle(T(c + 28, -.15), 4)
quip(c + 29)
t = T(c + 30, -.15)
globe("G_babur", t, [[t, 70, 33, 2.4], [T(c + 30, 1), 74, 31, 2.2]],
      arcs=[arcp([pt("KABUL"), pt("PESHAWAR"), pt("LAHORE"), pt("PANIPAT")], T(c + 30, .4), 3.0, col="#FF5A3A")],
      pins=[pin(*P["KABUL"], T(c + 30, .3), "Kabul", "#FF5A3A")],
      layers=[years("1526", K(c + 30, "fifteen"))])
board(T(c + 31, -.15), [imgcard(arc("babur_portrait"), 1050, 620, 480, T(c + 31, -.1), framed=True), txt("Timur", 1560, 400, K(c + 31, "Timur"), size=80, box="#222222"),
                        txt("+ Genghis Khan", 1560, 620, K(c + 31, "Genghis"), size=70, box="#d6423a")])

# ======================= CHAPTER 7: THE MUGHALS RISE =======================
c = CHAP[7]
chapter_card(7, c)
plate(T(c, .2), a("in_babur_camp"), layers=[lab("Babur", K(c, "Babur"), size=110, box="#c99400"), tag("Panipat vs Ibrahim Lodi", K(c, "Panipat"), y=420)], zoom=(1.0, 1.15))
pic(T(c + 1, -.15), "babur_painting", [lab("Cannons + guns", K(c + 1, "cannons"), size=96, box="#d6423a"), tag("The elephants panicked", K(c + 1, "elephants"), y=420)])
cycle(T(c + 2, -.15), 1, [txt("The Mughal Empire", 1250, 230, K(c + 2, "Mughal"), size=74, box="#c99400")])
pic(T(c + 3, -.15), "babur_portrait", [lab("The Baburnama", K(c + 3, "Baburnama"), size=90, box="#c99400")])
board(T(c + 4, -.15), [txt("No good horses", 1250, 300, K(c + 4, "horses"), size=76, box="#222222"), txt("No good grapes", 1250, 480, K(c + 4, "grapes"), size=76, box="#222222"),
                       txt("No good MELONS", 1250, 660, K(c + 4, "melons"), size=76, box="#d6423a")])
skit(c + 5, c + 8, "in_babur_camp", {"BABUR": (560, False), "SERVANT": (1360, True)})
plate(T(c + 9, -.15), a("in_babur_camp"), layers=[lab("Humayun loses it all", K(c + 9, "Humayun"), size=86, box="#d6423a"), tag("Sher Shah Suri", T(c + 9, .8), y=420)],
      zoom=(1.2, 1.0))
t = T(c + 10, -.15)
globe("G_road", t, [[t, 80, 27, 3.0], [T(c + 10, 1), 78, 28, 2.8]],
      arcs=[arcp([[89.9, 23.5], pt("CALCUTTA"), [85.1, 25.6], [80.3, 26.4], pt("AGRA"), pt("DELHI"), pt("LAHORE"), pt("PESHAWAR"), pt("KABUL")], T(c + 10, .2), 3.5, col="#FFD84A")],
      layers=[tag("Grand Trunk Road", T(c + 10, .25), x=1400, y=300), tag("Post · Rest houses", T(c + 10, .7), x=1400, y=440)])
board(T(c + 11, -.15), [txt("The RUPIYA", 1250, 560, K(c + 11, "rupiya"), size=120, box="#c99400")])
quip(c + 12)
plate(T(c + 13, -.15), a("in_agra_fort"), layers=[tag("Humayun returns", T(c + 13, .1), y=300), tag("...slipped on the stairs", K(c + 13, "slipped"), y=440)], zoom=(1.0, 1.15))
pic(T(c + 14, -.15), "akbar_painting", [lab("Akbar, age 13", K(c + 14, "Akbar"), size=96, box="#c99400")])
board(T(c + 15, -.15), [years("1556", K(c + 15, "fifteen"), x=1250, y=300), txt("2nd Battle of Panipat", 1250, 520, K(c + 15, "Panipat"), size=70, box="#222222"),
                        txt("Hemu defeated", 1250, 720, K(c + 15, "Hemu"), size=70, box="#d6423a")])
board(T(c + 16, -.15), [txt("Not cannons.", 1250, 380, T(c + 16, .1), size=86, box="#222222"), txt("INCLUDING people", 1250, 640, K(c + 16, "including"), size=96, box="#2f8f4f")])
plate(T(c + 17, -.15), a("in_fatehpur"), layers=[tag("Rajput alliances", K(c + 17, "Rajput"), y=300), tag("Rajput princes as generals", T(c + 17, .7), y=440)], zoom=(1.0, 1.12))
board(T(c + 18, -.15), [txt("Jizya scrapped", 1250, 380, K(c + 18, "jizya"), size=86, box="#2f8f4f"), txt("Raja Todar Mal: fair land tax", 1250, 640, K(c + 18, "Todar"), size=66, box="#222222")])
pic(T(c + 19, -.15), "akbar_painting", [lab("Could barely read", T(c + 19, .05), size=86, box="#222222"), tag("Huge library", K(c + 19, "library"), y=420)], zoom=(1.3, 1.5))
pic(T(c + 20, -.15), "fatehpur_sikri", [lab("Fatehpur Sikri", K(c + 20, "Fatehpur"), size=96), tag("Muslim · Hindu · Jain · Zoroastrian · Christian", K(c + 20, "Muslim"), y=420)])
quip(c + 21)
plate(T(c + 22, -.15), a("in_fatehpur"), layers=[lab("Maharana Pratap", K(c + 22, "Maharana"), size=90, box="#c99400"), tag("Never submitted", T(c + 22, .6), y=420)], zoom=(1.2, 1.0))
t = T(c + 23, -.15)
globe("G_mughal1605", t, [[t, 77, 26, 3.0], [T(c + 23, 1), 76, 27, 2.6]],
      over=[ov("ov_mughal1605", fadein(t + .2, .8, 1.0)), ove("ov_mughal1605_edge", fadein(t + .2, 1, 1.0)), ove("ov_in_edge", [[0, .45]])],
      layers=[years("1605", K(c + 23, "sixteen")), lab("Enormous. And rich.", T(c + 23, .6), size=84, box="#c99400")])
board(T(c + 24, -.15), [imgcard(card("bars"), 1200, 900, 1100, T(c + 24, -.1)), txt("¼ of the world", 1500, 260, K(c + 24, "quarter"), size=86, box="#c99400")])
quip(c + 25)

# ======================= CHAPTER 8: THE PEACOCK THRONE =======================
c = CHAP[8]
chapter_card(8, c)
plate(T(c, .2), a("in_palace_hall"), layers=[lab("Jahangir", K(c, "Jahangir"), size=100, box="#c99400"), tag("Art · Gardens · Wine", T(c, .3), y=420)], zoom=(1.0, 1.12))
plate(T(c + 1, -.15), a("in_palace_hall"), layers=[lab("Nur Jahan", K(c + 1, "Nur"), size=100, box="#c99400"), tag("Orders · Coins in her name", K(c + 1, "coins"), y=420)],
      zoom=(1.15, 1.3), c=(.6, .5))
quip(c + 2)
board(T(c + 3, -.15), [imgcard(crop("shah_jahan_old", (.31, .24, .69, .6)), 1250, 640, 600, T(c + 3, -.1), framed=True), txt("Shah Jahan", 1250, 180, K(c + 3, "Shah"), size=100, box="#c99400")])
plate(T(c + 4, -.15), a("in_palace_hall"), layers=[lab("The Peacock Throne", K(c + 4, "Peacock"), size=90, box="#c99400"), tag("7 years to make", K(c + 4, "seven"), y=420)],
      zoom=(1.0, 1.2), c=(.5, .45))
pic(T(c + 5, -.15), "taj_mahal", [lab("Mumtaz Mahal", K(c + 5, "Mumtaz"), size=96)], zoom=(1.4, 1.2), c0=(.5, .4))
pic(T(c + 6, -.15), "taj_mahal", [tag("~20,000 workers", K(c + 6, "twenty"), y=300), tag("20+ years", K(c + 6, "more than"), y=440), tag("Marble from Rajasthan", K(c + 6, "Marble"), y=580)],
    zoom=(1.2, 1.05))
pic(T(c + 7, -.15), "taj_mahal", [lab("The Taj Mahal", K(c + 7, "Taj"), size=120, box="#c99400")], zoom=(1.0, 1.08))
board(T(c + 8, -.15), [txt("One of the richest\nplaces on Earth", 1250, 380, T(c + 8, .1), size=80, box="#c99400"),
                       txt("Indian cotton dressed\nhalf the world", 1250, 680, K(c + 8, "cotton"), size=70, box="#222222")])
cycle(T(c + 9, -.15), "shine", [txt("The Golden Bird", 1250, 230, K(c + 9, "Golden"), size=74, box="#c99400")])
quip(c + 10)
pic(T(c + 11, -.15), "aurangzeb_portrait", [lab("Aurangzeb", K(c + 11, "Aurangzeb"), size=110, box="#d6423a"), tag("War of the brothers", T(c + 11, .2), y=420)])
pic(T(c + 12, -.15), "taj_mahal", [lab("Locked in Agra Fort", K(c + 12, "Agra"), size=86, box="#222222"), tag("Staring at the Taj", T(c + 12, .8), y=420)], zoom=(1.0, 1.0))
skit(c + 13, c + 16, "in_agra_fort", {"SHAH JAHAN": (560, False), "SERVANT": (1360, True)})
t = T(c + 17, -.15)
globe("G_mughal1707", t, [[t, 78, 23, 3.0], [T(c + 17, 1), 77, 22, 2.8]],
      over=[ov("ov_mughal1605", [[0, .8], [T(c + 17, .2), .8], [T(c + 17, .4), 0]]), ov("ov_mughal1707", fadein(T(c + 17, .2), .8, 1.2)),
            ove("ov_mughal1707_edge", fadein(T(c + 17, .2), 1, 1.2)), ove("ov_in_edge", [[0, .45]])],
      layers=[tag("Largest ever", T(c + 17, .3), x=1400, y=300), tag("~50 years on the throne", T(c + 17, .05), x=1400, y=440)])
plate(T(c + 18, -.15), a("in_babur_camp"), layers=[lab("25 years in the Deccan", T(c + 18, .1), size=84, box="#222222"), tag("Treasury drained", T(c + 18, .7), y=420)],
      zoom=(1.2, 1.0))
t = T(c + 19, -.15)
globe("G_shivaji", t, [[t, 75, 21, 2.2], [T(c + 19, 1), 74, 19, 1.8]],
      pins=[pin(*P["PUNE"], K(c + 19, "Pune"), "Pune", "#FF8A3A", size=56)], layers=[lab("Shivaji", K(c + 19, "Shivaji"), size=110, box="#FF8A3A")])
plate(T(c + 20, -.15), a("in_agra_fort"), layers=[years("1666", K(c + 20, "sixteen")), tag("Invited to Agra... and trapped", T(c + 20, .5), y=420)], zoom=(1.0, 1.15))
plate(T(c + 21, -.15), a("in_agra_fort"), layers=[lab("Baskets of sweets", K(c + 21, "baskets"), size=96, box="#c99400")], zoom=(1.3, 1.5), c=(.55, .6))
quip(c + 22)
board(T(c + 23, -.15), [years("1674", K(c + 23, "sixteen"), x=1250, y=320), txt("Shivaji crowned", 1250, 560, K(c + 23, "crowned"), size=86, box="#FF8A3A"),
                        txt("The Marathas keep growing", 1250, 760, K(c + 23, "Maratha"), size=60, box="#222222")])
cycle(T(c + 24, -.15), "shatter", [years("1707", K(c + 24, "seventeen"), x=1250, y=220)])
pic(T(c + 25, -.15), "nadir_shah", [years("1739", K(c + 25, "seventeen")), lab("Nadir Shah sacks Delhi", K(c + 25, "Nadir"), size=80, box="#d6423a")])
pic(T(c + 26, -.15), "koh_i_noor", [lab("The Koh-i-Noor", K(c + 26, "Koh"), size=100, box="#c99400"), tag("+ the Peacock Throne", T(c + 26, .1), y=420)])
quip(c + 27)
plate(T(c + 28, -.15), a("in_surat_port"), layers=[lab("A different kind of visitor", T(c + 28, .5), size=76, box="#222222")], zoom=(1.0, 1.12))

# ======================= CHAPTER 9: THE COMPANY =======================
c = CHAP[9]
chapter_card(9, c)
plate(T(c, .2), a("in_london_board"), layers=[years("1600", K(c, "sixteen")), lab("The East India Company", T(c, .7), size=80, box="#d6423a")], zoom=(1.0, 1.12))
t = T(c + 1, -.15)
globe("G_sea", t, [[t, 20, 10, 4.2], [T(c + 1, 1), 70, 15, 3.4]],
      arcs=[arcp([pt("LONDON"), [-10, 40], [-18, 15], [-5, -10], [10, -30], pt("CAPE"), [35, -30], [55, -10], [65, 5], pt("BOMBAY")], T(c + 1, .1), 5.0)],
      layers=[tag("Portuguese · Dutch · French too", K(c + 1, "Portuguese"), x=1400, y=300)])
t = T(c + 2, -.15)
globe("G_ports", t, [[t, 80, 18, 2.8], [T(c + 2, 1), 80, 19, 2.6]],
      pins=[pin(*P["SURAT"], K(c + 2, "Surat"), "Surat", "#FFD84A"), pin(*P["MADRAS"], K(c + 2, "Madras"), "Madras", "#FFD84A"),
            pin(*P["BOMBAY"], K(c + 2, "Bombay"), "Bombay", "#FFD84A"), pin(*P["CALCUTTA"], K(c + 2, "Calcutta"), "Calcutta", "#FFD84A")],
      layers=[tag("Pepper · Cotton · Indigo · Tea", K(c + 2, "Pepper"), x=1400, y=300)])
plate(T(c + 3, -.15), a("in_surat_port"), layers=[lab("Bombay = a wedding dowry", K(c + 3, "dowry"), size=80, box="#c99400"), tag("1661", T(c + 3, .6), y=420)], zoom=(1.0, 1.15))
quip(c + 4)
seq(c + 5, [("hired", "Soldiers"), ("Then more", "More soldiers"), ("lot", "A LOT more")], size=100)
board(T(c + 6, -.15), [txt("~200,000", 1250, 400, K(c + 6, "two"), size=130, box="#d6423a"), txt("A private army", 1250, 660, K(c + 6, "private"), size=80, box="#222222")])
skit(c + 7, c + 11, "in_london_board", {"DIRECTOR ONE": (560, False), "DIRECTOR TWO": (1360, True)})
pic(T(c + 12, -.15), "clive_mir_jafar", [years("1757", K(c + 12, "seventeen")), lab("Plassey", K(c + 12, "Plassey"), size=100), tag("Robert Clive vs the Nawab", K(c + 12, "Clive"), y=420)])
pic(T(c + 13, -.15), "clive_mir_jafar", [lab("A secret deal: Mir Jafar", K(c + 13, "deal"), size=80, box="#d6423a")], zoom=(1.3, 1.5), c0=(.6, .5))
quip(c + 14)
t = T(c + 15, -.15)
globe("G_bengal", t, [[t, 86, 24, 2.2], [T(c + 15, 1), 88, 23.5, 1.8]],
      pins=[pin(*P["PLASSEY"], T(c + 15, .05), "Plassey", "#FF5A3A"), pin(*P["CALCUTTA"], T(c + 15, .3), "Calcutta", "#FFD84A")],
      layers=[lab("Taxes of Bengal → the Company", T(c + 15, .3), size=70, box="#d6423a")])
board(T(c + 16, -.15), [txt("A company ruled millions", 1250, 400, T(c + 16, .05), size=80, box="#222222"), txt("Priority: profit", 1250, 660, K(c + 16, "profit"), size=90, box="#d6423a")])
pic(T(c + 17, -.15), "famine_1876", [years("1770", K(c + 17, "seventeen")), lab("Bengal famine", K(c + 17, "famine"), size=96, box="#d6423a"), tag("Up to ⅓ of Bengal died", K(c + 17, "third"), y=420)],
    zoom=(1.1, 1.2))
t = T(c + 18, -.15)
globe("G_mysore", t, [[t, 77, 14, 2.0], [T(c + 18, 1), 76.7, 12.5, 1.7]],
      pins=[pin(*P["SRIRANGA"], T(c + 18, .1), "Mysore", "#FF8A3A", size=56)],
      layers=[lab("Hyder Ali + Tipu Sultan", K(c + 18, "Hyder"), size=80, box="#FF8A3A")])
board(T(c + 19, -.15), [years("1799", K(c + 19, "seventeen"), x=1250, y=360), txt("Tipu dies defending his capital", 1250, 620, T(c + 19, .2), size=66, box="#222222")])
pic(T(c + 20, -.15), "ranjit_singh", [lab("Maharaja Ranjit Singh", K(c + 20, "Ranjit"), size=80, box="#c99400"), tag("The Sikh Empire", K(c + 20, "Sikh"), y=420)])
pic(T(c + 21, -.15), "koh_i_noor", [years("1849", K(c + 21, "eighteen")), lab("Punjab taken. Koh-i-Noor too.", T(c + 21, .6), size=70, box="#d6423a")])
quip(c + 22)
t = T(c + 23, -.15)
globe("G_company", t, [[t, 80, 23, 3.0], [T(c + 24, 1), 79, 23, 2.8]], over=[ov("ov_raj", fadein(t + .2, .75, 1.2)), ove("ov_raj_edge", fadein(t + .2, 1, 1.2))],
      layers=[years("1850s", K(c + 23, "eighteen")), tag("Most of India: Company-run", T(c + 23, .4), x=1400, y=420)])
plate(T(c + 24, -.15), a("in_meerut"), layers=[lab("The sepoys", K(c + 24, "sepoys"), size=100), tag("Indian soldiers", K(c + 24, "Indian"), y=420)], zoom=(1.0, 1.12))

# ======================= CHAPTER 10: THE REVOLT AND THE RAJ =======================
c = CHAP[10]
chapter_card(10, c)
plate(T(c, .2), a("in_meerut"), layers=[years("1857", K(c, "eighteen")), lab("A new rifle", K(c, "rifle"), size=90), tag("Bite the cartridge open", T(c, .7), y=420)], zoom=(1.0, 1.15))
plate(T(c + 1, -.15), a("in_meerut"), layers=[lab("A rumour", T(c + 1, .05), size=100, box="#d6423a"), tag("Cow + pig fat", K(c + 1, "cow"), y=420)], zoom=(1.2, 1.4), c=(.55, .55))
t = T(c + 2, -.15)
globe("G_meerut", t, [[t, 77.5, 29, 1.6], [T(c + 3, 1), 77.3, 28.7, 1.4]],
      arcs=[arcp([pt("MEERUT"), pt("DELHI")], K(c + 2, "Delhi"), 1.6, col="#FF5A3A")],
      pins=[pin(*P["MEERUT"], T(c + 2, .1), "Meerut", "#FF5A3A"), pin(*P["DELHI"], K(c + 2, "Delhi"), "Delhi", "#FFD84A")],
      layers=[tag("May 1857: the rising", T(c + 2, .3), x=1400, y=300)])
pic(T(c + 3, -.15), "bahadur_shah_zafar", [lab("Bahadur Shah Zafar", K(c + 3, "Bahadur"), size=80, box="#c99400")])
quip(c + 4)
pic(T(c + 5, -.15), "lakshmibai", [lab("Rani Lakshmibai", K(c + 5, "Rani"), size=90, box="#c99400"), tag("Jhansi", K(c + 5, "Jhansi"), y=420)])
plate(T(c + 6, -.15), a("in_meerut"), layers=[lab("Crushed with brutality", T(c + 6, .1), size=80, box="#d6423a"), tag("Villages burned", K(c + 6, "Villages"), y=420)], zoom=(1.3, 1.0))
pic(T(c + 7, -.15), "bahadur_shah_zafar", [lab("Exiled to Rangoon", K(c + 7, "Rangoon"), size=86, box="#222222"), tag("The Mughal dynasty ends", K(c + 7, "Mughal"), y=420)], zoom=(1.3, 1.1))
board(T(c + 8, -.15), [years("1858", K(c + 8, "eighteen"), x=1250, y=320), txt("Company → the Crown", 1250, 600, T(c + 8, .6), size=86, box="#d6423a")])
skit(c + 9, c + 14, "in_victoria_palace", {"VICTORIA": (560, False), "MINISTER": (1360, True)}, cast={"MINISTER": "c_br_minister"})
board(T(c + 15, -.15), [imgcard(arc("victoria_portrait"), 1050, 620, 480, T(c + 15, -.1), framed=True), years("1876", K(c + 15, "eighteen"), x=1560, y=380),
                        txt("Empress of India", 1560, 620, K(c + 15, "Empress"), size=66, box="#c99400")])
t = T(c + 16, -.15)
globe("G_raj", t, [[t, 80, 23, 3.0], [T(c + 16, 1), 79, 23, 2.7]], over=[ov("ov_raj", fadein(t + .2, .75, 1.0)), ove("ov_raj_edge", fadein(t + .2, 1, 1.0))],
      layers=[lab("The British Raj", T(c + 16, .05), size=90, box="#d6423a"), tag("Railways · Telegraph · Universities", K(c + 16, "railways"), x=1400, y=420)])
plate(T(c + 17, -.15), a("in_railway_1853"), layers=[years("1853", K(c + 17, "eighteen")), lab("Bombay → Thane", K(c + 17, "Bombay"), size=90)], zoom=(1.0, 1.15))
quip(c + 18)
plate(T(c + 19, -.15), a("in_railway_1853"), layers=[tag("Raw cotton → ports", K(c + 19, "cotton"), y=300), tag("British cloth → Indian markets", T(c + 19, .7), y=440)],
      zoom=(1.2, 1.4), c=(.4, .5))
board(T(c + 20, -.15), [txt("World's cloth-maker", 1250, 380, T(c + 20, .1), size=80, box="#222222"), txt("→ buys from Manchester", 1250, 640, K(c + 20, "Manchester"), size=80, box="#d6423a")])
pic(T(c + 21, -.15), "famine_1876", [years("1876", K(c + 21, "eighteen")), lab("The Great Famine", K(c + 21, "Great"), size=96, box="#d6423a"), tag("Grain still exported", T(c + 21, .75), y=420)])
board(T(c + 22, -.15), [txt("Dadabhai Naoroji", 1250, 330, K(c + 22, "Dadabhai"), size=86, box="#c99400"), txt("The DRAIN of wealth", 1250, 620, K(c + 22, "drain"), size=96, box="#d6423a")])
board(T(c + 23, -.15), [imgcard(card("bars"), 1200, 900, 1100, T(c + 23, -.1)), txt("~4%", 1500, 300, K(c + 23, "nineteen"), size=130, box="#d6423a")])
quip(c + 24)
plate(T(c + 25, -.15), a("in_railway_1853"), layers=[lab("Schools + newspapers", T(c + 25, .1), size=86), tag("Tools to fight back", K(c + 25, "fight"), y=420)], zoom=(1.0, 1.12))

# ======================= CHAPTER 11: THE FREEDOM STRUGGLE =======================
c = CHAP[11]
chapter_card(11, c)
board(T(c, .2), [years("1885", K(c, "eighteen"), x=1250, y=320), txt("Indian National Congress", 1250, 580, K(c, "Indian"), size=80, box="#2f8f4f")])
board(T(c + 1, -.15), [years("1905", K(c + 1, "nineteen"), x=1250, y=260), txt("Bengal split in two", 1250, 480, K(c + 1, "split"), size=80, box="#d6423a"),
                       txt("Swadeshi: burn British cloth", 1250, 700, K(c + 1, "burn"), size=66, box="#222222")])
board(T(c + 2, -.15), [years("1915", K(c + 2, "nineteen"), x=1250, y=320), txt("Home from South Africa", 1250, 580, K(c + 2, "South"), size=76, box="#222222")])
pic(T(c + 3, -.15), "gandhi_portrait", [lab("Mohandas K. Gandhi", K(c + 3, "Mohandas"), size=80, box="#c99400"), tag("\"Mahatma\"", T(c + 3, .85), y=420)])
board(T(c + 4, -.15), [txt("Satyagraha", 1250, 360, K(c + 4, "satyagraha"), size=110, box="#c99400"), txt("Truth + non-violence", 1250, 620, K(c + 4, "without"), size=80, box="#222222")])
quip(c + 5)
plate(T(c + 6, -.15), a("in_jallianwala"), layers=[years("1919", K(c + 6, "nineteen")), lab("Amritsar", K(c + 6, "Amritsar"), size=96), tag("A peaceful crowd", K(c + 6, "peacefully"), y=420)],
      zoom=(1.0, 1.12))
plate(T(c + 7, -.15), a("in_jallianwala"), layers=[lab("General Dyer: \"Fire\"", K(c + 7, "Dyer"), size=80, box="#d6423a"), tag("The only exit: blocked", K(c + 7, "exit"), y=420)],
      zoom=(1.2, 1.4), c=(.5, .55))
pic(T(c + 8, -.15), "jallianwala", [lab("379 official · 1,000+ Indian estimates", T(c + 8, .2), size=64, box="#d6423a")])
board(T(c + 9, -.15), [txt("Trust: broken", 1250, 600, T(c + 9, .2), size=110, box="#d6423a")])
plate(T(c + 10, -.15), a("in_dandi"), layers=[lab("Non-cooperation", T(c + 10, .1), size=90, box="#2f8f4f"), tag("Leave British schools · courts · jobs", T(c + 10, .4), y=420)],
      zoom=(1.0, 1.12))
t = T(c + 11, -.15)
globe("G_salt", t, [[t, 73, 22.5, 1.5], [T(c + 11, 1), 72.8, 22, 1.35]],
      arcs=[arcp([pt("SABARMATI"), [72.75, 22.4], [72.9, 21.7], pt("DANDI")], K(c + 11, "salt"), 3.0, col="#FFFFFF")],
      pins=[pin(*P["SABARMATI"], T(c + 11, .1), "Sabarmati", "#FFD84A"), pin(*P["DANDI"], K(c + 11, "salt"), "Dandi", "#FFD84A")],
      layers=[years("1930", K(c + 11, "nineteen")), lab("SALT", K(c + 11, "salt"), size=120, box="#c99400")])
skit(c + 12, c + 16, "in_dandi", {"GANDHI": (560, False), "OFFICER": (1360, True)})
pic(T(c + 17, -.15), "gandhi_salt_march", [lab("The Salt March", T(c + 17, .05), size=96, box="#c99400"), tag("~380 km · 24 days", K(c + 17, "three"), y=420)])
pic(T(c + 18, -.15), "bhagat_singh", [lab("Bhagat Singh", K(c + 18, "Bhagat"), size=96, box="#d6423a"), tag("Hanged at 23", T(c + 18, .8), y=420)])
pic(T(c + 19, -.15), "ambedkar", [lab("Dr B. R. Ambedkar", K(c + 19, "Ambedkar"), size=86, box="#1d3f8f"), tag("Rights for the oppressed", T(c + 19, .6), y=420)])
board(T(c + 20, -.15), [txt("2.5 million", 1250, 400, K(c + 20, "two"), size=120, box="#222222"), txt("Indian soldiers in WWII", 1250, 650, T(c + 20, .4), size=74, box="#222222")])
pic(T(c + 21, -.15), "bose_portrait", [lab("Subhas Chandra Bose", K(c + 21, "Subhas"), size=80, box="#c99400"), tag("Indian National Army", K(c + 21, "Indian National"), y=420)])
board(T(c + 22, -.15), [years("1942", K(c + 22, "nineteen"), x=1250, y=300), txt("QUIT INDIA", 1250, 560, K(c + 22, "Quit"), size=120, box="#d6423a")])
pic(T(c + 23, -.15), "famine_1876", [years("1943", K(c + 23, "nineteen")), lab("Bengal famine: ~3 million dead", T(c + 23, .5), size=70, box="#d6423a")], zoom=(1.3, 1.1))
quip(c + 24)
board(T(c + 25, -.15), [txt("Britain: broke + exhausted", 1250, 600, T(c + 25, .1), size=80, box="#222222")])
board(T(c + 26, -.15), [txt("Freedom was coming...", 1250, 400, T(c + 26, .05), size=86, box="#2f8f4f"), txt("...but not whole", 1250, 660, K(c + 26, "whole"), size=86, box="#d6423a")])

# ======================= CHAPTER 12: MIDNIGHT =======================
c = CHAP[12]
chapter_card(12, c)
board(T(c, .2), [txt("Congress  vs  Muslim League", 1250, 400, K(c, "Muslim"), size=76, box="#222222"), txt("Jinnah: a separate nation", 1250, 660, K(c, "Jinnah"), size=70, box="#222222")])
t = T(c + 1, -.15)
globe("G_partition", t, [[t, 79, 26, 2.5], [T(c + 3, 1), 77, 27, 2.2]],
      over=[ov("ov_raj", [[0, .75], [T(c + 1, .3), .75], [T(c + 1, .9), 0]]), ove("ov_raj_edge", [[0, 1], [T(c + 1, .3), 1], [T(c + 1, .9), 0]]),
            ov("ov_in_flag", fadein(T(c + 1, .5), .85, .8)), ove("ov_in_edge", fadein(T(c + 1, .5), 1, .8)), ov("ov_pak", fadein(T(c + 1, .5), .75, .8)),
            ove("ov_pak_edge", fadein(T(c + 1, .5), 1, .8))],
      layers=[lab("Partition", T(c + 1, .3), size=110, box="#d6423a"), tag("Cyril Radcliffe: never been to India", K(c + 2, "Radcliffe"), x=1350, y=420),
              tag("5 weeks to draw it", T(c + 2, .8), x=1350, y=560)])
quip(c + 3)
board(T(c + 4, -.15), [txt("Midnight", 1250, 280, T(c + 4, .05), size=100, box="#222222"), years("15 August 1947", K(c + 4, "fifteenth"), x=1250, y=500),
                       txt("INDIA IS FREE", 1250, 740, K(c + 4, "free"), size=100, box="#2f8f4f")])
pic(T(c + 5, -.15), "red_fort", [lab("Jawaharlal Nehru", K(c + 5, "Nehru"), size=86, box="#c99400"), tag("\"A tryst with destiny\"", T(c + 5, .6), y=420)])
plate(T(c + 6, -.15), a("in_partition_train"), layers=[lab("Wrong side of the line", T(c + 6, .6), size=80, box="#d6423a"), tag("Punjab · Bengal", K(c + 6, "Punjab"), y=420)],
      zoom=(1.0, 1.15))
pic(T(c + 7, -.15), "partition_refugees", [lab("10-20 million uprooted", T(c + 7, .5), size=80, box="#222222")])
plate(T(c + 8, -.15), a("in_partition_train"), layers=[lab("200,000 - 2 million dead", T(c + 8, .5), size=74, box="#d6423a")], zoom=(1.3, 1.1))
quip(c + 9)
pic(T(c + 10, -.15), "gandhi_portrait", [lab("Fasting in Calcutta", K(c + 10, "Calcutta"), size=86, box="#222222")], zoom=(1.2, 1.35))
board(T(c + 11, -.15), [years("30 January 1948", K(c + 11, "thirtieth"), x=1250, y=360), txt("Gandhi assassinated", 1250, 620, K(c + 11, "shot"), size=86, box="#d6423a")])
board(T(c + 12, -.15), [txt("560+", 1250, 380, K(c + 12, "five"), size=150, box="#c99400"), txt("princely states", 1250, 640, K(c + 12, "princely"), size=86, box="#222222")])
person(c + 13, "patel_portrait", "Sardar Vallabhbhai Patel", "Patel", extra=[tag("+ V. P. Menon", T(c + 13, .8), x=420, y=300)], side=1250)
skit(c + 14, c + 18, "in_palace_hall", {"MAHARAJA": (1360, True), "PATEL": (560, False)})
board(T(c + 19, -.15), [txt("Most rulers signed", 1250, 300, T(c + 19, .05), size=80, box="#2f8f4f"), txt("Hyderabad", 1250, 520, K(c + 19, "Hyderabad"), size=80, box="#222222"),
                        years("1948", K(c + 19, "nineteen"), x=1250, y=740)])
pic(T(c + 20, -.15), "patel_statue", [lab("The Iron Man of India", K(c + 20, "Iron"), size=84, box="#c99400")])
t = T(c + 20, .55)
globe("G_union", t, [[t, 79, 22, 2.8], [T(c + 20, 1) + 1.0, 79, 22, 2.6]], over=[ov("ov_in_flag", fadein(t + .1, .85, .6)), ove("ov_in_edge", [[0, 1]])],
      layers=[lab("STITCH", t + .1, size=110, box="#c99400")])
pic(T(c + 21, -.15), "constitution", [lab("The Constitution", K(c + 21, "Constitution"), size=96, box="#1d3f8f"), tag("Led by Dr Ambedkar", K(c + 21, "Ambedkar"), y=420)])
board(T(c + 22, -.15), [years("26 January 1950", K(c + 22, "twenty"), x=1250, y=360), txt("Republic Day", 1250, 620, K(c + 22, "Republic"), size=96, box="#c99400")])
board(T(c + 23, -.15), [txt("EVERY adult votes", 1250, 400, K(c + 23, "every"), size=96, box="#2f8f4f"), txt("Rich or poor · Literate or not", 1250, 660, T(c + 23, .6), size=66, box="#222222")])
pic(T(c + 24, -.15), "first_election", [years("1951", K(c + 24, "nineteen")), lab("~170 million voters", K(c + 24, "hundred"), size=80, box="#c99400"),
                                        tag("Party symbols on ballots", T(c + 24, .8), y=420)])
quip(c + 25)
board(T(c + 26, -.15), [txt("Free.", 1250, 380, T(c + 26, .1), size=110, box="#2f8f4f"), txt("Now: learn to fly again", 1250, 640, T(c + 26, .5), size=80, box="#c99400")])

# ======================= CHAPTER 13: THE COMEBACK =======================
c = CHAP[13]
chapter_card(13, c)
board(T(c, .2), [years("1962", K(c, "nineteen"), x=1250, y=300), txt("Border war with China: lost", 1250, 540, K(c, "China"), size=70, box="#d6423a"),
                 txt("Wars with Pakistan", 1250, 740, T(c, .8), size=70, box="#222222")])
board(T(c + 1, -.15), [txt("Grain from America", 1250, 600, K(c + 1, "America"), size=90, box="#d6423a")])
board(T(c + 2, -.15), [txt("Green Revolution", 1250, 360, K(c + 2, "Green"), size=110, box="#2f8f4f"), txt("Wheat · Rice · Irrigation", 1250, 620, K(c + 2, "wheat"), size=74, box="#222222")])
quip(c + 3)
t = T(c + 4, -.15)
globe("G_bangla", t, [[t, 86, 24, 2.4], [T(c + 4, 1), 90, 23.8, 1.9]], over=[ove("ov_in_edge", [[0, .6]])],
      pins=[pin(*P["DHAKA"], K(c + 4, "East"), "Bangladesh", "#2f8f4f", size=60)],
      layers=[years("1971", K(c + 4, "nineteen")), tag("Bangladesh is born", T(c + 4, .7), x=1400, y=420)])
pic(T(c + 5, -.15), "indira_gandhi", [years("1975", K(c + 5, "nineteen")), lab("The Emergency", K(c + 5, "Emergency"), size=96, box="#d6423a"),
                                       tag("Elections suspended · press censored", T(c + 5, .6), y=420)])
pic(T(c + 6, -.15), "first_election", [years("1977", K(c + 6, "nineteen")), lab("Voters threw her out", K(c + 6, "threw"), size=84, box="#2f8f4f")])
quip(c + 7)
pic(T(c + 8, -.15), "indira_gandhi", [years("1984", K(c + 8, "nineteen")), lab("Assassinated", K(c + 8, "assassinated"), size=96, box="#d6423a")], zoom=(1.2, 1.35))
board(T(c + 9, -.15), [txt("The Licence Raj", 1250, 380, T(c + 9, .3), size=96, box="#222222"), txt("Permission for everything", 1250, 640, K(c + 9, "permission"), size=74, box="#d6423a")])
board(T(c + 10, -.15), [years("1991", K(c + 10, "nineteen"), x=1250, y=320), txt("Reserves: ~3 weeks of imports", 1250, 600, T(c + 10, .5), size=70, box="#d6423a")])
plate(T(c + 11, -.15), a("in_runway_1991"), layers=[lab("47 tonnes of gold", K(c + 11, "forty"), size=96, box="#c99400"), tag("→ Bank of England", K(c + 11, "Bank"), y=420)],
      zoom=(1.0, 1.15))
skit(c + 12, c + 15, "in_runway_1991", {"PILOT": (560, False), "OFFICIAL": (1360, True)}, cast={"OFFICIAL": "c_gov_official"})
pic(T(c + 16, -.15), "manmohan_singh", [lab("1991 reforms", T(c + 16, .1), size=90, box="#2f8f4f"), tag("P. V. Narasimha Rao + Manmohan Singh", K(c + 16, "Narasimha"), y=420)])
pic(T(c + 17, -.15), "bengaluru_skyline", [lab("Growth takes off", T(c + 17, .05), size=90, box="#2f8f4f"), tag("Bengaluru · Hyderabad", K(c + 17, "Bengaluru"), y=420)])
pic(T(c + 18, -.15), "mangalyaan", [years("2014", K(c + 18, "two")), lab("Mars, first try", K(c + 18, "Mars"), size=96, box="#c99400")])
quip(c + 19)
pic(T(c + 20, -.15), "chandrayaan3", [years("2023", K(c + 20, "two")), lab("Chandrayaan-3", K(c + 20, "Chandrayaan"), size=90, box="#c99400"), tag("First near the Moon's south pole", T(c + 20, .6), y=420)])
pic(T(c + 21, -.15), "modi_portrait", [lab("Narendra Modi", K(c + 21, "Narendra"), size=90, box="#c99400"), tag("PM since 2014", K(c + 21, "since"), y=420),
                                        tag("Supporters: roads · digital payments · welfare", T(c + 21, .6), y=560)])
board(T(c + 22, -.15), [txt("Critics worry about:", 1250, 260, T(c + 22, .05), size=74, box="#222222"), txt("Jobs · Inequality", 1250, 460, K(c + 22, "jobs"), size=74, box="#222222"),
                        txt("Press freedom · Minorities", 1250, 660, K(c + 22, "press"), size=70, box="#222222")])
t = T(c + 23, -.15)
globe("G_today", t, [[t, 60, 20, 3.8], [T(c + 23, 1), 79, 22, 2.8]], over=[ov("ov_in_flag", fadein(t + .3, .85, .8)), ove("ov_in_edge", [[0, 1]])],
      layers=[lab("5th-largest economy", T(c + 23, .2), size=84, box="#c99400"), tag("Next: passing Japan, then Germany", K(c + 23, "Japan"), x=1400, y=420)])

# ======================= ENDING =======================
c = CHAP[99]
cycle(T(c, -.3), 4, [txt("The loop", 1250, 230, T(c, .1), size=86, box="#222222")])
for k, n in enumerate([1, 2, 3]):
    cycle(T(c + 1, k / 3.0), n)
cycle(T(c + 2, -.15), 4, [txt("Always absorbed", 1250, 230, T(c + 2, .3), size=70, box="#222222")])
quip(c + 3, [imgcard(card("cycle4"), 1500, 760, 560, T(c + 3, -.1))])
board(T(c + 4, -.15), [imgcard(card("bars"), 1200, 900, 1100, T(c + 4, -.1)), txt("1700: ~24%", 1500, 230, T(c + 4, .1), size=74, box="#c99400"), txt("1950: ~4%", 1500, 370, T(c + 4, .5), size=74, box="#d6423a")])
t = T(c + 5, -.15)
globe("G_rising", t, [[t, 79, 22, 3.2], [T(c + 6, 1), 79, 22, 2.5]], over=[ov("ov_in_flag", fadein(t + .2, .9, .8)), ove("ov_in_edge", [[0, 1]])],
      layers=[lab("Climbing back. Fast.", T(c + 5, .1), size=90, box="#2f8f4f"), tag("Can the Golden Bird fly again?", T(c + 6, .1), x=1400, y=420)])
quip(c + 7)
board(T(c + 8, -.15), [txt("Can India break the loop?", 1250, 480, T(c + 8, .1), size=86, box="#c99400"), txt("Tell us in the comments", 1250, 720, T(c + 8, .5), size=64, box="#222222")])
quip(c + 9, [txt("Next: CHINA", 1500, 230, T(c + 9, .3), size=86, box="#d6423a")])

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
    if any(x in " ".join(text_of(L_) for L_ in s["layers"]) for x in ("He was SORRY.", "INDIA IS FREE", "QUIT INDIA", "Partition", "SALT", "Assassinated")):
        s["cut"] = "flash"
for s in shots:   # labels never sit in the caption band
    for L_ in s["layers"]:
        if isinstance(L_.get("img"), dict) and L_["y"] > 860: L_["y"] = 250

# captions from the script words, timed by the transcriber
from num_in import digits
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
print("keywords not found:", MISS)
print("placeholder bgs:", len([s for s in shots if str(s["bg"].get("img")) .startswith("#") and not s.get("clip")]))
