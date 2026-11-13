#!/usr/bin/env python3
"""Shot plan for the India REMAKE (built from storyboard/shots.txt via plan_body.py; helpers + close copied from full/plan_full.py).
Old docstring: Shot plan for the India full video, chapters 2-13 + ending (the pilot part, hook + ch1, is rendered separately and joined in front).
Helpers, timeline close and retention pass are the pilot's (pilot/plan_pilot.py).

Shots are pinned to script LINES (index into script_ch2-13.md), never to fixed seconds.
Usage: python3 plan_full.py lines.json spec.json words.txt [speed] [--punch=7]
Also writes clips3d.json (3D globe clips, local times) next to spec.json.
"""
import json, sys, os, re, textwrap, difflib
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
A1 = os.path.join(HERE, "..", "art"); A2 = os.path.join(HERE, "..", "art2"); C1 = os.path.join(HERE, "..", "pilot", "cards"); C2 = os.path.join(HERE, "cards")
ARC = os.path.join(ROOT, "outputs", "fetch", "in-pilot-archive")
ARC2 = os.path.join(ROOT, "outputs", "fetch", "in-full-archive"); ARC3 = os.path.join(ROOT, "outputs", "fetch", "in-full-archive2"); ARC4 = os.path.join(ROOT, "outputs", "fetch", "in-full-archive3"); CLIPS = os.path.join(HERE, "clips3d"); os.makedirs(CLIPS, exist_ok=True)   # archive3 = replacements, searched first
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
args = [a for a in sys.argv[1:] if not a.startswith("--")]
L = json.load(open(args[0])); END = L[-1]["t1"] + 1.6
WORDS = args[2]; SPEED = float(args[3]) if len(args) > 3 else 1.0
PUNCH = float(next((a.split("=")[1] for a in sys.argv if a.startswith("--punch=")), 7))


# ---- script (speaker + English text per line), file line numbers, skit spans ----
SCRIPT, SPK, CHAP, LNO, LNO_SKIT = [], [], {}, [], {}
chap = None; _pend = None
for _no, r in enumerate(open(os.path.join(HERE, "script_en.md"), encoding="utf-8"), 1):
    r = r.strip(); m = re.match(r"# (HOOK|CHAPTER (\d+)|ENDING)", r)
    if m: chap = 0 if m.group(1) == "HOOK" else (int(m.group(2)) if m.group(2) else 99); CHAP[chap] = len(SCRIPT); continue
    if r.startswith("[SKIT"): _pend = _no; continue
    m = re.match(r"^([A-Z][A-Z .'&]*?):\s*(.+)$", r)
    if m and chap is not None:
        if m.group(1) == "N": _pend = None
        elif _pend:                                        # scene lines after a [SKIT] row: span = first..last
            LNO_SKIT.setdefault(_pend, [len(SCRIPT), len(SCRIPT)])[1] = len(SCRIPT)
        SPK.append(m.group(1)); SCRIPT.append(m.group(2)); LNO.append(_no)
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
    font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if any(c in s for c in "→✓↓↑✗⅓π≈") else FONT
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
def years(s, t, x=330, y=105): return lab(s, t, x=x, y=y, size=92)   # own row above the titles (y~250)

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


exec(open(os.path.join(HERE, 'plan_body.py'), encoding='utf-8').read())

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
sys.path.insert(0, os.path.join(HERE, "..", "full")); from num_in import digits
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
