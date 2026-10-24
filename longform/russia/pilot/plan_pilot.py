#!/usr/bin/env python3
"""Shot plan for the Russia pilot (hook + chapter 1).

Shots are pinned to script LINES (and fractions of a line), never to fixed seconds,
so the same plan renders the English and Hindi takes on their own timings.
Usage: python3 plan_pilot.py lines_<lang>.json spec_<lang>.json
"""
import json, sys, os, textwrap
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "..", "art"); M = os.path.join(HERE, "..", "maps", "out"); C = os.path.join(HERE, "cards")
ARC = os.path.join(HERE, "..", "..", "..", "outputs", "fetch", "ru-pilot-archive")
ARC2 = os.path.join(HERE, "..", "..", "..", "outputs", "fetch", "ru-pilot-archive2")
def arc(name, fallback):
    for d in (ARC2, ARC):
        if os.path.exists(os.path.join(d, name)): return os.path.join(d, name)
    return fallback
STALIN = os.path.join(HERE, "..", "..", "..", "outputs", "fetch", "ru-pilot-archive-search", "stalin_full.jpg")
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
EN = json.load(open(os.path.join(HERE, "lines_en.json")))     # keyword fractions come from the English text
L = json.load(open(sys.argv[1])); END = L[-1]["t1"] + 1.4
GREY = "#d6d6d6"

def a(n): return os.path.join(A, n + ".png")
def card(n): return os.path.join(C, n + ".png")
def mp(n): return os.path.join(M, n + ".png")
def ov(plate, name): return os.path.join(M, f"{plate}__{name}.png")
def T(i, f=0.0):
    """Time at fraction f through line i (f<0 = before the line starts)."""
    x = L[i]; return x["t0"] + (x["t1"] - x["t0"]) * f if f >= 0 else x["t0"] + f
def kw(i, word):
    """Fraction of line i where `word` starts, measured on the English text (shared by both languages)."""
    s = EN[i]["text"]; k = s.find(word)
    return max(0.0, min(0.95, k / max(len(s), 1))) if k >= 0 else 0.0
def talk(i): return [T(i), T(i, 1)]
def aspect_h(path, w):
    im = Image.open(path); return int(w * im.height / im.width)

def txt(s, x, y, t, size=72, box=None, color="#ffffff", out=None, enter="pop"):
    font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if any(c in s for c in "→✓↓↑") else FONT
    L_ = {"img": {"text": s, "size": size, "color": color, "box": box, "font": font}, "x": x, "y": y, "in": t, "enter": enter}
    if out is not None: L_["out"] = out
    return L_
def say(i, x, y=360, width=26, size=44):
    """Skit dialogue shown above the speaker (English text in both videos)."""
    s = EN[i]["text"]
    import re; s = re.sub(r"\[[^\]]*\]\s*", "", s).replace("*", "").strip()
    return txt("\n".join(textwrap.wrap(s, width)), x, y, T(i), size=size, box="#ffffffee", color="#222222", out=T(i, 1) + .25)
def ch(name, x, y=1045, h=560, t=None, enter="pop", talks=(), flip=False, out=None):
    d = {"img": a(name), "x": x, "y": y, "h": h, "enter": enter, "talk": [talk(i) for i in talks], "flip": flip}
    if t is not None: d["in"] = t
    if out is not None: d["out"] = out
    return d
def traveller(talks=(), t=None, x=360, h=700, enter="none"):
    return ch("c_traveller", x, 1030, h, t=t, enter=enter, talks=talks)

shots = []
def shot(t0, bg, layers=(), cam=None, over=()):
    b = {"img": bg}
    if cam: b["cam"] = cam
    if over: b["over"] = list(over)
    shots.append({"t0": t0, "bg": b, "layers": list(layers)})
def board(t0, layers=(), talks=()):
    shot(t0, GREY, [traveller(talks)] + list(layers))
def imgcard(path, x, y, w, t, out=None):
    d = {"img": path, "x": x, "y": y, "h": aspect_h(path, w), "in": t, "enter": "pop", "shadow": False}
    if out is not None: d["out"] = out
    return d
def plate_pan(t0, img, cam, layers=()):
    shot(t0, img, layers, cam=cam)

# ---------------- HOOK ----------------
t = 0.0
shot(t, mp("map_alaska"), [txt("1867", 300, 230, T(0, .02), size=110)],
     cam=[[T(0), .22, .45, 1.25], [T(0, 1), .52, .38, 1.15]],
     over=[{"img": ov("map_alaska", "alaska"), "in": T(0, kw(0, "bigger")), "dur": .6, "mode": "fade"}])
board(T(1, -.15), [txt("~2¢ per acre", 1250, 620, T(1, .25), size=120, box="#222222")])
shot(T(2, -.15), mp("map_alaska"), [txt("America", 1500, 900, T(2, .02), size=90), txt("ALASKA", 900, 330, T(2, kw(2, "Alaska")), size=100)],
     cam=[[T(2), .52, .36, 1.5], [T(2, .5), .55, .36, 1.7]],
     over=[{"img": ov("map_alaska", "alaska"), "in": 0, "dur": .01, "mode": "fade"}])
board(T(2, kw(2, "And not")), [txt("Gold", 1050, 560, T(2, kw(2, "gold")), size=110, box="#c99400"),
                                txt("Oil", 1500, 560, T(2, kw(2, "oil")), size=110, box="#111111")])
board(T(3, -.15), [say(3, 760, 330)], talks=[3])
shot(T(4, -.15), mp("map_eurasia"), [txt("Still #1", 960, 260, T(4, kw(4, "biggest")), size=100)],
     cam=[[T(4), .45, .4, 1.6], [T(4, .6), .5, .42, 1.0]])
board(T(4, kw(4, "Because")), [imgcard(card("bars"), 1200, 900, 1100, T(4, kw(4, "Because")))])
shot(T(5, -.15), mp("map_eurasia"), [txt("11 time zones", 960, 230, T(5, .05), size=96)],
     cam=[[T(5), .5, .42, 1.05], [T(5, 1), .5, .42, 1.12]],
     over=[{"img": ov("map_eurasia", "span"), "in": T(5, .02), "dur": 2.2, "mode": "draw"}])
board(T(5, kw(5, "When")), [txt("Moscow\n11 PM", 1000, 640, T(5, kw(5, "When")), size=80, box="#2b3a67"),
                             txt("Far East\n8 AM, next day", 1520, 640, T(5, kw(5, "the far")), size=80, box="#e0902f")])
# rogues' gallery: one quick cut per ruler
G = [("Viking", "c_rurik", "Viking chiefs"), ("Mongol", "c_khan", "Mongol khans"), ("a tsar", "c_ivan4", "Killed his own son"),
     ("a giant", "c_peter1", "Banned beards"), ("a German", None, "Took her husband's throne"), ("a dictator", None, "Erased people from photos")]
for k, (w, c, label) in enumerate(G):
    t0 = T(6, -.15) if k == 0 else T(6, kw(6, w))
    lay = [txt(label, 1250, 300, t0 + .1, size=70, box="#222222")]
    if c: lay.append(ch(c, 1250, 1045, 620, t=t0 + .05))
    elif k == 4: lay.append(imgcard(os.path.join(ARC, "catherine.jpg"), 1250, 1000, 470, t0 + .05))
    else: lay.append(imgcard(STALIN, 1250, 1000, 430, t0 + .05))
    board(t0, lay)
board(T(7, -.15), [say(7, 760, 330)], talks=[7])
shot(T(8, -.15), mp("map_eurasia"), [txt("The same story", 960, 240, T(8, kw(8, "same")), size=100)],
     cam=[[T(8), .5, .42, 1.0], [T(8, 1), .5, .44, 1.2]])
steps = [("chaos", 1), ("total control", 2), ("freedom", 3), ("too far", 4), ("collapses", 5)]
for k, (w, n) in enumerate(steps):
    t0 = T(9, -.15) if k == 0 else T(9, kw(9, w))
    board(t0, [imgcard(card(f"cycle{n}"), 1200, 1000, 1000, t0, )])
for k, (w, c) in enumerate([("Vikings", "c_rurik"), ("Mongols", "c_khan"), ("Tsars", "c_ivan4"), ("Communists", None)]):
    t0 = T(10, -.15) if k == 0 else T(10, kw(10, w))
    lay = [ch(c, 1250, 1045, 620, t=t0 + .05)] if c else [imgcard(STALIN, 1250, 1000, 430, t0 + .05)]
    board(t0, lay + [txt(w, 1250, 300, t0 + .1, size=80, box="#222222")])
board(T(10, kw(10, "Different")), [imgcard(card("cycle5"), 1200, 1000, 1000, T(10, kw(10, "Different")))])
shot(T(11, -.15), mp("map_eurasia"), [txt("How?", 960, 260, T(11, .1), size=120), txt("Why?", 960, 260, T(11, kw(11, "why")), size=120)],
     cam=[[T(11), .48, .42, 1.0], [T(11, 1), .3, .45, 1.6]])
board(T(12, -.15), [say(12, 760, 330)], talks=[12])
board(T(13, -.15), [txt("Back to the beginning", 1200, 600, T(13, .05), size=90, box="#222222")], talks=[13])
shot(T(13, 1) + .1, GREY, [imgcard(card("chapter1"), 960, 980, 1500, T(13, 1) + .15)])

# ---------------- CHAPTER 1 ----------------
plate_pan(T(14, -.15), a("ru_rivers"), [[T(14), .3, .5, 1.25], [T(14, 1), .7, .5, 1.25]], [txt("~800 AD", 300, 230, T(14, .05), size=90)])
plate_pan(T(15, -.15), a("ru_rivers"), [[T(15), .5, .55, 1.0], [T(15, 1), .5, .55, 1.1]],
          [ch("c_slav_elder2", 760, t=T(15, .25)), ch("c_slav_elder3", 1180, t=T(15, .4), flip=True),
           txt("East Slavs", 960, 250, T(15, kw(15, "East")), size=90)])
plate_pan(T(16, -.15), a("ru_rivers"), [[T(16), .5, .6, 1.2], [T(16, 1), .5, .6, 1.35]],
          [ch("c_slav_elder2", 760, enter="none", talks=[16]), ch("c_slav_elder3", 1160, enter="none", flip=True, talks=[16])])
board(T(17, -.15), [txt("Foreigners?!", 1200, 600, T(17, kw(17, "foreigners")), size=110, box="#222222")])
plate_pan(T(18, -.15), a("ru_novgorod"), [[T(18), .5, .5, 1.3], [T(18, 1), .5, .5, 1.1]],
          [ch("c_rurik", 960, t=T(18, kw(18, "Vikings")), h=640), txt("Vikings!", 960, 260, T(18, kw(18, "Vikings")), size=110)])
# skit: the letter
cab = [[T(19), .5, .55, 1.0], [T(24, 1), .5, .55, 1.12]]
plate_pan(T(19, -.15), a("ru_cabin"), cab,
          [ch("c_slav_elder1", 520, enter="slideL", t=T(19, -.15), talks=[19, 21, 23, 24]),
           ch("c_slav_elder2", 1060, enter="slideR", t=T(19, .4), flip=True, talks=[20, 23]),
           ch("c_slav_elder3", 1440, enter="slideR", t=T(22, -.2), flip=True, talks=[22]),
           say(19, 560), say(20, 1080), say(21, 560), say(22, 1440), say(23, 800), say(24, 560)])
board(T(25, -.15), [say(25, 760, 330)], talks=[25])
shot(T(26, -.15), mp("map_rus"), [txt("862", 300, 230, T(26, kw(26, "eight")), size=110), txt("Novgorod", 1450, 330, T(26, kw(26, "Novgorod")), size=76)],
     cam=[[T(26), .45, .3, 1.6], [T(26, 1), .45, .32, 1.8]],
     over=[{"img": ov("map_rus", "pin_novgorod"), "in": T(26, kw(26, "Novgorod")), "dur": .3, "mode": "fade"}])
board(T(27, -.15), [txt("Rus  →  Russia", 1200, 620, T(27, kw(27, "name")), size=120, box="#d6423a")])
board(T(28, -.15), [ch("c_rurik", 1050, t=T(28, -.1), h=600), txt("700+ years", 1500, 560, T(28, kw(28, "seven")), size=100, box="#222222")])
shot(T(29, -.15), mp("map_rus"), [txt("Kyiv", 1150, 690, T(29, kw(29, "Kyiv")), size=80), txt("Oleg", 300, 230, T(29, kw(29, "Oleg")), size=90)],
     cam=[[T(29), .45, .45, 1.1], [T(29, 1), .45, .55, 1.3]],
     over=[{"img": ov("map_rus", "pin_novgorod"), "in": 0, "dur": .01, "mode": "fade"},
           {"img": ov("map_rus", "oleg"), "in": T(29, kw(29, "sailed")), "dur": 2.5, "mode": "draw"},
           {"img": ov("map_rus", "pin_kyiv"), "in": T(29, kw(29, "Kyiv")), "dur": .3, "mode": "fade"}])
shot(T(30, -.15), mp("map_rus"), [txt("Constantinople", 900, 960, T(30, kw(30, "Constantinople")), size=70)],
     cam=[[T(30), .45, .5, 1.0], [T(30, .55), .45, .55, 1.05]],
     over=[{"img": ov("map_rus", "pin_novgorod"), "in": 0, "dur": .01}, {"img": ov("map_rus", "pin_kyiv"), "in": 0, "dur": .01},
           {"img": ov("map_rus", "trade"), "in": T(30, .05), "dur": 3.5, "mode": "draw"},
           {"img": ov("map_rus", "pin_const"), "in": T(30, kw(30, "Constantinople")), "dur": .3}])
plate_pan(T(30, kw(30, "Furs")), a("ru_kyiv"), [[T(30, kw(30, "Furs")), .4, .5, 1.2], [T(30, 1), .6, .5, 1.2]],
          [txt("Furs & honey  ↓", 520, 260, T(30, kw(30, "Furs")), size=70), txt("Silver & silk  ↑", 1400, 260, T(30, kw(30, "Silver")), size=70)])
shot(T(31, -.15), mp("map_rus"), [txt("Kievan Rus", 960, 250, T(31, kw(31, "Kievan")), size=110)],
     cam=[[T(31), .45, .45, 1.0], [T(31, 1), .45, .45, 1.08]],
     over=[{"img": ov("map_rus", "kievanrus"), "in": T(31, kw(31, "Kievan")), "dur": 1.0, "mode": "fade"}])
board(T(32, -.4), [imgcard(card("cycle2"), 1200, 1000, 1000, T(32, -.4)), txt("Step 1  ✓", 1500, 230, T(32, .3), size=80, box="#2f8f4f")], talks=[32])
# Olga
plate_pan(T(33, -.15), a("ru_kyiv"), [[T(33), .5, .5, 1.0], [T(33, 1), .5, .55, 1.15]],
          [ch("c_olga", 960, t=T(33, kw(33, "Princess")), h=620), txt("Princess Olga", 960, 260, T(33, kw(33, "Princess")), size=96)])
plate_pan(T(34, -.15), a("ru_kyiv"), [[T(34), .5, .55, 1.15], [T(34, 1), .5, .55, 1.3]],
          [ch("c_olga", 960, enter="none", h=620), txt("945", 300, 230, T(34, kw(34, "nine")), size=110),
           txt("Prince Igor: killed", 1350, 330, T(34, kw(34, "killed")), size=66, box="#222222")])
plate_pan(T(35, -.15), a("ru_dock"), [[T(35), .5, .55, 1.0], [T(36, 1), .5, .55, 1.1]],
          [ch("c_drevlian", 1350, enter="slideR", t=T(35, .2), flip=True, talks=[36]), ch("c_olga", 560, enter="slideL", t=T(35, .5), talks=[37]),
           say(36, 1350), say(37, 560)])
plate_pan(T(38, -.15), a("ru_dock"), [[T(38), .5, .6, 1.2], [T(38, .45), .5, .7, 1.45]], [txt("Buried alive", 960, 250, T(38, kw(38, "buried")), size=96)])
plate_pan(T(38, kw(38, "The second")), a("ru_bathhouse"), [[T(38, kw(38, "The second")), .5, .5, 1.0], [T(38, 1), .5, .5, 1.3]],
          [txt("The doors were locked", 960, 250, T(38, kw(38, "doors")), size=86)])
board(T(39, -.15), [say(39, 760, 330)], talks=[39])
shot(T(40, -.15), arc("olga_revenge.jpg", os.path.join(A, "ru_bathhouse.png")), [txt("Burned to the ground", 960, 980, T(40, kw(40, "burned")), size=86)],
     cam=[[T(40), .5, .4, 1.0], [T(40, 1), .5, .5, 1.15]])
board(T(41, -.15), [ch("c_olga", 1250, t=T(41, -.1), h=600), txt("SAINT", 1250, 300, T(41, kw(41, "saint")), size=120, box="#c99400")])
board(T(42, -.15), [say(42, 760, 330), ch("c_olga", 1500, h=520, enter="none")], talks=[42])
# Vladimir
plate_pan(T(43, -.15), a("ru_hall"), [[T(43), .5, .5, 1.0], [T(43, 1), .5, .55, 1.12]],
          [ch("c_vladimir", 960, t=T(43, kw(43, "Vladimir")), h=620), txt("Vladimir", 960, 260, T(43, kw(43, "Vladimir")), size=96)])
board(T(44, -.15), [txt("Job interview:\nReligion", 1200, 640, T(44, kw(44, "interviewed")), size=100, box="#222222")])
plate_pan(T(45, -.3), a("ru_hall"), [[T(45), .5, .55, 1.0], [T(47, 1), .5, .55, 1.12]],
          [ch("c_vladimir", 620, enter="none", talks=[45, 47]), ch("c_byz_envoy", 1380, enter="slideR", t=T(46, -.4), flip=True, talks=[46]),
           say(45, 620), say(46, 1380), say(47, 620)])
plate_pan(T(48, -.15), a("ru_constantinople"), [[T(48), .5, .5, 1.0], [T(48, .4), .5, .45, 1.15]], [txt("988", 300, 230, T(48, kw(48, "nine")), size=110)])
shot(T(48, kw(48, "and had")), arc("baptism.jpg", os.path.join(A, "ru_kyiv.png")), [txt("Baptism of Kyiv", 960, 980, T(48, kw(48, "baptized")), size=80)],
     cam=[[T(48, kw(48, "and had")), .5, .45, 1.0], [T(48, 1), .5, .5, 1.15]])
shot(T(49, -.15), mp("map_rus"), [txt("Yaroslav the Wise", 960, 250, T(49, kw(49, "Yaroslav")), size=96)],
     cam=[[T(49), .45, .45, 1.0], [T(49, 1), .45, .45, 1.1]],
     over=[{"img": ov("map_rus", "kievanrus"), "in": 0, "dur": .01}, {"img": ov("map_rus", "trade"), "in": 0, "dur": .01, "mode": "draw"}])
board(T(50, -.15), [], talks=[])
board(T(51, -.15), [say(51, 760, 330)], talks=[51])
plate_pan(T(52, -.15), a("ru_rivers"), [[T(52), .5, .6, 1.2], [T(52, 1), .5, .6, 1.4]],
          [ch("c_slav_elder1", 640, enter="none", talks=[52]), ch("c_slav_elder2", 1000, enter="none", flip=True, talks=[52]),
           ch("c_slav_elder3", 1340, t=T(52, .4), flip=True, talks=[52]), txt("Brothers vs brothers", 960, 250, T(52, .05), size=86)])
board(T(53, -.15), [imgcard(card("cycle_chaos"), 1200, 1000, 1000, T(53, -.15))])
shot(T(54, -.15), mp("map_mongol"), [txt("Mongols", 1500, 400, T(54, kw(54, "army")), size=100)],
     cam=[[T(54), .75, .5, 1.4], [T(54, 1), .45, .5, 1.0]],
     over=[{"img": ov("map_mongol", "horde"), "in": T(54, kw(54, "riding")), "dur": 2.0, "mode": "draw"}])
board(T(55, -.15), [say(55, 760, 330)], talks=[55])

# close the timeline
shots.sort(key=lambda s: s["t0"])
for s, n in zip(shots, shots[1:] + [None]): s["t1"] = n["t0"] if n else END
shots[0]["t0"] = 0.0
json.dump({"w": 1920, "h": 1080, "fps": 30, "shots": shots}, open(sys.argv[2], "w"), indent=1)
gaps = [round(s["t1"] - s["t0"], 1) for s in shots]
print(len(shots), "shots; mean", round(sum(gaps) / len(gaps), 1), "s; longest", max(gaps), "s; end", round(END, 1))
