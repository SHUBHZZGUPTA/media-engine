# Body of plan_remake.py: turns storyboard/shots.txt into spec shots (exec'd inside plan_remake.py, which supplies the
# helpers copied from full/plan_full.py: T, K, txt, lab, tag, shot, plate, pic, imgcard, frame, crop, ch, say, skit, globe...).
import re as _re
RM = os.path.join(HERE)                                   # longform/india/remake
CARDS_RM = os.path.join(RM, "cards")
ART_DIRS = [os.path.join(HERE, "..", d) for d in ("art4", "art3", "art2", "art")]
ARC_DIRS = [os.path.join(ROOT, "outputs", "fetch", d) for d in ("in-rm-archive", "in-full-archive3", "in-full-archive2", "in-full-archive", "in-pilot-archive")]
CLIP_DIRS = [os.path.join(RM, "clips3d"), os.path.join(HERE, "..", "full", "clips3d"), os.path.join(HERE, "..", "pilot", "clips3d")]
def a(n):
    for d in ART_DIRS:
        p = os.path.join(d, n + ".png")
        if os.path.exists(p): return p
    return None
def arc(key):
    for d in ARC_DIRS:
        for ext in (".jpg", ".png"):
            p = os.path.join(d, key + ext)
            if os.path.exists(p) and os.path.getsize(p) > 2000: return p
    return None
def card(n):
    for d in (CARDS_RM, os.path.join(HERE, "..", "pilot", "cards")):
        p = os.path.join(d, n + ".png")
        if os.path.exists(p): return p
    return None
def anyimg(key): return a(key) or arc(key) or card(key)
def clip_path(cid):
    for d in CLIP_DIRS:
        p = os.path.join(d, cid + ".mp4")
        if os.path.exists(p): return p
    return None

# ---- storyboard rows ----
ROWS = []
for r in open(os.path.join(RM, "storyboard", "shots.txt"), encoding="utf-8"):
    if not r.strip() or r.startswith("#"): continue
    f = [x.strip() for x in r.rstrip("\n").split("|")] + ["", "", ""]
    ROWS.append(dict(line=int(f[0]), type=f[1], asset=f[2], text=f[3], note=f[4]))
def idx_of(fileline):                                    # spoken-line index at or after a file line
    for k, n in enumerate(LNO):
        if n >= fileline: return k
    return len(LNO) - 1
def keys_of(asset):                                       # "x + NEW-ARC:y (desc) + z" -> ["x", "y", "z"]
    out = []
    for part in asset.split("+"):
        part = _re.sub(r"\(.*?\)", "", part).strip()
        part = part.split(":", 1)[1] if _re.match(r"NEW-[A-Z0-9]+:", part) else part
        part = part.split("→")[0].split(" or ")[0].strip()
        if part: out.append(part.split()[0])
    return out
def seq_keys(asset):                                      # "a → b" = two pictures one after the other
    first = _re.sub(r"\(.*?\)", "", asset.split("+")[0])
    return [_re.sub(r"NEW-[A-Z0-9]+:", "", x).strip().split()[0] for x in first.split("→") if x.strip()]
def clean(s): return s.replace("*", "").replace("‡", "‡")
def box_for(s): return "#c99400" if any(c.isdigit() for c in s) or "*" in s else "#222222"
def wrap(s, n=26): return "\n".join(textwrap.wrap(clean(s), n))
def blur_board(t0, layers, dur=6.0):
    bg = LAST[0] or "#1d2733"
    return shot(t0, bg, list(layers), cam=[[t0, .5, .5, 1.0], [t0 + dur, .5, .5, 1.08]], blur=14, dim=.5)

# real people speak through their real picture; unnamed people are toy figures
REAL.update({"PRINSEP": ("james_prinsep", None), "PRITHVIRAJ": ("prithviraj_chauhan", None), "AKBAR": ("akbar_painting", None),
             "RADCLIFFE": ("cyril_radcliffe", None), "SHAH JAHAN": ("shah_jahan_old", (.31, .24, .69, .6))})
POS = {1: [(960, False)], 2: [(520, False), (1400, True)], 3: [(440, False), (1480, True), (960, False)], 4: [(380, False), (1540, True), (960, False), (1180, True)]}

# ---- 12 new 3D clips (rendered on Kaggle; until then a dark placeholder) ----
NEW3D = {
 "G_calicut":   dict(cam=[(20, 25, 4.2), (76, 11, 2.6)], arcs=[["LISBON", "CAPE", "CALICUT"]], pins=[("CALICUT", "Calicut")]),
 "G_indus_dry": dict(cam=[(70, 27, 2.6), (70, 27, 2.3)], arcs=[], pins=[("MOHENJO", "Mohenjo-daro"), ("HARAPPA", "Harappa")]),
 "G_buddhism":  dict(cam=[(84, 25, 3.2), (105, 25, 4.2)], arcs=[["BODHGAYA", "XIAN"], ["XIAN", "NARA"], ["BODHGAYA", "BAGAN"]], pins=[("BODHGAYA", "Bodh Gaya")]),
 "G_dhamma":    dict(cam=[(82, 22, 3.0), (80, 12, 2.8)], arcs=[["PATAL", "ANURADHA"], ["PATAL", "KANDAHAR"]], pins=[("PATAL", "Pataliputra")]),
 "G_numerals":  dict(cam=[(75, 22, 3.4), (40, 35, 4.4)], arcs=[["UJJAIN", "BAGHDAD"], ["BAGHDAD", "CORDOBA"]], pins=[("BAGHDAD", "Baghdad")]),
 "G_tarain":    dict(cam=[(72, 30, 3.4), (76.9, 29.8, 2.3)], arcs=[["GHOR", "TARAIN"]], pins=[("TARAIN", "Tarain"), ("DELHI", "Delhi")]),
 "G_mongols":   dict(cam=[(90, 42, 4.6), (77, 30, 3.2)], arcs=[], pins=[("DELHI", "Delhi")]),
 "G_timur":     dict(cam=[(72, 34, 3.2), (68, 38, 3.4)], arcs=[["DELHI", "SAMARKAND"]], pins=[("SAMARKAND", "Samarkand"), ("DELHI", "Delhi")]),
 "G_cloth":     dict(cam=[(75, 20, 3.6), (40, 20, 5.0)], arcs=[["SURAT", "LONDON"], ["CALCUTTA", "NAGASAKI"], ["SURAT", "MOMBASA"]], pins=[("SURAT", "Surat")]),
 "G_nadir":     dict(cam=[(70, 30, 3.2), (60, 33, 3.4)], arcs=[["DELHI", "MASHHAD"]], pins=[("DELHI", "Delhi"), ("MASHHAD", "Persia")]),
 "G_manchester":dict(cam=[(60, 30, 4.6), (20, 40, 5.0)], arcs=[["BOMBAY", "MANCHESTER"], ["MANCHESTER", "CALCUTTA"]], pins=[("MANCHESTER", "Manchester")]),
 "G_wars6265":  dict(cam=[(80, 30, 3.2), (78, 32, 2.8)], arcs=[], pins=[("LADAKH", "1962"), ("LAHORE", "1965")]),
}
P.update(dict(LISBON=(-9.14, 38.72), CALICUT=(75.78, 11.25), MOHENJO=(68.14, 27.33), HARAPPA=(72.86, 30.63), XIAN=(108.94, 34.34),
              NARA=(135.8, 34.69), BAGAN=(94.86, 21.17), ANURADHA=(80.4, 8.31), UJJAIN=(75.78, 23.18), BAGHDAD=(44.36, 33.31),
              CORDOBA=(-4.78, 37.89), GHOR=(64.9, 34.1), SAMARKAND=(66.97, 39.65), NAGASAKI=(129.87, 32.75), MOMBASA=(39.67, -4.04),
              MANCHESTER=(-2.24, 53.48), LADAKH=(78.3, 34.5)))
def new_globe(cid, t0, t1, layers):
    S = NEW3D[cid]; cam = [[t0] + list(S["cam"][0]), [t1] + list(S["cam"][1])]
    arcs = [arcp([pt(k) for k in A], t0 + .8 + j * .9, 1.6) for j, A in enumerate(S["arcs"])]
    pins = [pin(*pt(k), t0 + .5 + j * .5, label=lbl) for j, (k, lbl) in enumerate(S["pins"])]
    return globe(cid, t0, cam, over=[ove("ov_in_edge", [[0, 1]])], arcs=arcs, pins=pins, layers=layers)

# ---- interpret rows ----
skit_spans = []
for r in ROWS:
    if r["type"] != "SKIT" or not LNO_SKIT.get(r["line"]): continue
    skit_spans.append((r["line"],) + tuple(LNO_SKIT[r["line"]]))
def in_skit(fileline):
    for sl, i0, i1 in skit_spans:
        if LNO[i0] <= fileline <= LNO[i1] and fileline != sl: return (sl, i0, i1)
    return None
from collections import OrderedDict
groups = OrderedDict()
for r in ROWS: groups.setdefault(r["line"], []).append(r)
pending_skit_inserts = {}
for fl, rs in groups.items():
    sk = in_skit(fl)
    if sk:                                                 # a picture called for inside a scene: show it as a card in the scene
        pending_skit_inserts.setdefault(sk[0], []).extend((idx_of(fl), r) for r in rs); continue
for fl, rs in groups.items():
    if in_skit(fl): continue
    if rs[0]["type"] == "SKIT" and fl in LNO_SKIT:
        i0, i1 = LNO_SKIT[fl]; r = rs[0]; ks = keys_of(r["asset"]); bg = ks[0]
        figs = [k for k in ks[1:] if k.startswith("c_")]; spk = []
        for i in range(i0, i1 + 1):
            if SPK[i] != "N" and SPK[i] not in spk: spk.append(SPK[i])
        cast, pos = {}, {}
        for j, w in enumerate(spk): pos[w] = POS[min(len(spk), 4)][j]
        for w in spk:                                      # figures matched to speakers by name first, then in order
            if w in REAL: continue
            hit = next((f_ for f_ in figs if w.lower().split()[0] in f_), None)
            if hit: cast[w] = hit; figs.remove(hit)
        for w in spk:
            if w not in REAL and w not in cast: cast[w] = figs.pop(0) if figs else "c_courtier"
        s = skit(i0, i1, bg, pos, cast=cast)
        for (ii, rr) in pending_skit_inserts.get(fl, []):
            p_ = anyimg(keys_of(rr["asset"])[0])
            if p_: s["layers"].append(imgcard(p_, 960, 560, 520, T(ii, 0), out=T(ii, 1), framed=True))
        continue
    i = idx_of(fl); n = len(rs)
    for k, r in enumerate(rs):
        t0 = T(i, -.15) if k == 0 else T(i, k / n); t1 = T(i, (k + 1) / n) if k + 1 < n else T(i, 1)
        typ, text = r["type"], r["text"]; ks = keys_of(r["asset"])
        L_ = [lab(wrap(text, 30), t0 + .1, size=70, box=box_for(text))] if text and text != "DRAMATISED" else []
        if typ == "CARD":
            nm = ks[0] if ks else "ending"
            shot(t0, LAST[0] or "#1d2733", [imgcard(card(nm), 960, 1000, 1550, t0 + .05)], cam=[[t0, .5, .5, 1.0], [t0 + 4, .5, .5, 1.06]], blur=14, dim=.5)
        elif typ == "STING":
            s = blur_board(t0, [txt("BHUGOL", 960, 540, t0 + .05, size=150, box="#c99400")], dur=2.0); s["cut"] = "flash"
        elif typ == "MAP":
            cid = ks[0]
            if cid in NEW3D: new_globe(cid, t0, t1, L_)
            elif clip_path(cid):
                cp = clip_path(cid); s = shot(t0, {"video": cp}, L_); s["bg"] = {"video": cp, "img": "#02070d"}
                LAST[0] = cp[:-4] + "_last.jpg"
            else: blur_board(t0, L_)
        elif typ == "PIC":
            sk = seq_keys(r["asset"])
            if len(sk) > 1:
                for j, key in enumerate(sk):
                    tj = t0 + (t1 - t0) * j / len(sk); pic(tj, key, L_ if j == 0 else [], fallback=a(key))
            else:
                extra = [imgcard(anyimg(x), 1500, 700, 560, t0 + .4, framed=True) for x in ks[1:] if anyimg(x)]
                p_ = anyimg(ks[0]) if ks else None
                if p_ and p_ in (a(ks[0]),): plate(t0, p_, layers=L_ + extra)
                else: pic(t0, ks[0], L_ + extra, fallback=a(ks[0]))
        elif typ == "PORT":
            key = ks[0]; key, box = (key, None) if key not in ("tughlaq_token_coin", "shah_jahan_old", "chanakya_sculpture") else \
                {"tughlaq_token_coin": ("tughlaq_token_coin", (0, 0, .52, 1)), "shah_jahan_old": ("shah_jahan_old", (.31, .24, .69, .6)),
                 "chanakya_sculpture": ("chanakya_sculpture", (0, 0, .56, 1))}[key]
            p_ = crop(key, box) if box else anyimg(key)
            lay = [imgcard(p_, 960, 560, 640, t0 + .05, framed=True)] if p_ else [txt(f"[{key}]", 960, 540, t0, size=40, scale=1)]
            lay.append(txt(clean(text), 960, 930, t0 + .3, size=56, box="#c99400"))
            blur_board(t0, lay)
        elif typ == "SKIT":                                # scene beat on a narrator line: set + figures, no bubbles
            p_ = a(ks[0]) if ks else None; xs = [620, 1300, 960]
            figs = [ch(f_, xs[j % 3], t=t0 + .3 * j, flip=xs[j % 3] > 960) for j, f_ in enumerate(x for x in ks[1:] if x.startswith("c_"))]
            if p_: plate(t0, p_, layers=L_ + figs)
            else: blur_board(t0, L_ + figs)
        elif typ == "SET":
            p_ = a(ks[0]) if ks else None
            if p_: plate(t0, p_, layers=L_)
            else: blur_board(t0, L_)
        else:   # BOARD
            imgs = [anyimg(x) for x in ks if anyimg(x)]
            lay = []
            if imgs: lay.append(imgcard(imgs[0], 960, 640, 900 if len(imgs) == 1 else 700, t0 + .05, framed=not imgs[0].endswith("_panel.png")))
            if text: lay.append(txt(wrap(text, 28), 960, 240 if imgs else 540, t0 + .2, size=78 if not imgs else 64, box=box_for(text)))
            blur_board(t0, lay)
