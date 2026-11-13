#!/usr/bin/env python3
"""Storyboard sheets for the India remake: one still per shot (shots.txt), one sheet per chapter.
Times come from the current takes (word-proportional inside each take, 1.2 s gap between takes, 3 s per chapter card),
so they are approximate until the voice is locked.
Usage: python3 build.py [outdir]   -> outdir/ch00.jpg ... + shots.json
"""
import json, os, re, sys, glob, textwrap, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../../.."))
IN = os.path.join(ROOT, "longform/india"); OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
FB = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"; FR = "/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf"
if not os.path.exists(FR): FR = FB
TAKES = [("in-rm-en-f1", f"p0{i}") for i in range(1, 5)] + [("in-rm-en-r1", "p05"), ("in-rm-en-r1", "p06")] + \
        [("in-rm-en-f2", n) for n in ("p07", "p08", "p09", "p10", "p11")] + [("in-rm-en-r1", "p12"), ("in-rm-en-f2", "p13"), ("in-rm-en-r1", "p14")]
TAKES = [(("in-rm-en-r2" if os.path.exists(f"{ROOT}/outputs/tts/in-rm-en-r2/{n}.wav") and os.environ.get("USE_R2") and n in os.environ["USE_R2"].split(",") else j), n) for j, n in TAKES]

# ---- spoken script lines (file line numbers) and chapter of each ----
spoken, chap_of, chap_name, cur = [], {}, {}, None
for no, r in enumerate(open(os.path.join(IN, "remake/script_en.md"), encoding="utf-8"), 1):
    r = r.rstrip("\n"); m = re.match(r"# (HOOK|CHAPTER (\d+): (.+)|ENDING: (.+))$", r)
    if m: cur = 0 if m.group(1) == "HOOK" else (int(m.group(2)) if m.group(2) else 15); chap_name[cur] = m.group(3) or m.group(4) or "HOOK"; chap_of[no] = cur; continue
    chap_of[no] = cur
    m = re.match(r"^([A-Z][A-Z .'&]*?):\s*(.+)$", r)
    if m and cur is not None: spoken.append((no, m.group(1), re.sub(r"\[[^\]]*\]\s*", "", m.group(2)).replace("*", "").replace("‡", "")))
# ---- time per spoken line ----
dur = lambda p: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
times, k, t, seen_ch = {}, 0, 0.0, set()
for job, n in TAKES:
    it = next(i for i in json.load(open(f"{ROOT}/jobs/tts/{job}.json"))["items"] if i["name"] == n)
    d = dur(f"{ROOT}/outputs/tts/{job}/{n}.wav"); words = [max(1, len(x[1].split())) for x in it["lines"]]; tot = sum(words); acc = 0
    for w in words:
        no = spoken[k][0]; c = chap_of[no]
        if c not in seen_ch and c: seen_ch.add(c); t += 3.0          # chapter card
        times[no] = t + d * acc / tot; acc += w; k += 1
    t += d + 1.2
assert k == len(spoken), (k, len(spoken))
TOTAL = t
def tline(no):
    while no not in times and no < 400: no += 1
    return times.get(no, TOTAL)
txt_of = {no: (who, s) for no, who, s in spoken}
def line_text(no):
    while no not in txt_of and no < 400: no += 1
    return txt_of.get(no, ("", ""))

# ---- assets ----
ART = [os.path.join(IN, d) for d in ("art3", "art2", "art")]; ARC = [os.path.join(ROOT, "outputs/fetch", d) for d in ("in-full-archive3", "in-full-archive2", "in-full-archive", "in-pilot-archive")]
CL = [os.path.join(IN, "full/clips3d"), os.path.join(IN, "pilot/clips3d")]; CARDS = [os.path.join(IN, "full/cards"), os.path.join(IN, "pilot/cards")]
def find(key):
    key = key.strip()
    for d in ART:
        p = os.path.join(d, key + ".png")
        if os.path.exists(p): return p
    for d in ARC:
        for e in (".jpg", ".png"):
            p = os.path.join(d, key + e)
            if os.path.exists(p) and os.path.getsize(p) > 2000: return p
    for d in CL:
        p = os.path.join(d, key + "_last.jpg")
        if os.path.exists(p): return p
    for d in CARDS:
        for p in (os.path.join(d, key + ".png"), os.path.join(d, "_framed_" + key + ".png"), os.path.join(d, "_framed__crop_" + key + ".png")):
            if os.path.exists(p): return p
    return None

W, H = 480, 270
def font(f, s): return ImageFont.truetype(f, s)
def cover(p, w=W, h=H):
    im = Image.open(p).convert("RGB"); r = max(w / im.width, h / im.height); im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1))
    x, y = (im.width - w) // 2, (im.height - h) // 2; return im.crop((x, y, x + w, y + h))
def contain(p, h=200):
    im = Image.open(p).convert("RGBA"); r = h / im.height; return im.resize((max(1, int(im.width * r)), h))
def placeholder(label, kind):
    col = {"NEW-ART": (120, 28, 40), "NEW-ARC": (30, 60, 120), "NEW-3D": (25, 95, 70)}[kind]
    im = Image.new("RGB", (W, H), col); d = ImageDraw.Draw(im)
    d.rectangle([6, 6, W - 7, H - 7], outline=(255, 255, 255), width=2)
    d.text((18, 14), {"NEW-ART": "NEW ART NEEDED", "NEW-ARC": "ARCHIVE IMAGE TO FETCH", "NEW-3D": "NEW 3D MAP CLIP"}[kind], font=font(FB, 22), fill=(255, 216, 74))
    y = 52
    for ln in textwrap.wrap(label.replace("_", " "), 34)[:6]: d.text((18, y), ln, font=font(FB, 21), fill="white"); y += 30
    return im
def compose(types, assets):
    parts = [a.strip() for a in assets.split("+") if a.strip()]
    base = None; missing = []
    for i, a in enumerate(parts):
        m = re.match(r"(NEW-ART|NEW-ARC|NEW-3D):(\S+)\s*(\(.*\))?", a)
        key = m.group(2) if m else re.split(r"[\s(→]", a)[0]
        p = None if m else find(key)
        if m: missing.append((m.group(1), m.group(2) + (" " + m.group(3) if m.group(3) else "")))
        if i == 0:
            if p: base = cover(p)
            elif m: base = placeholder(missing[-1][1], missing[-1][0])
            else: base = Image.new("RGB", (W, H), (34, 34, 34))
        elif p and base is not None:   # layered figure/portrait
            fg = contain(p, 150 if key.startswith("c_") else 130); x = 40 + (i - 1) * 140
            if fg.mode == "RGBA": base.paste(fg, (min(x, W - fg.width - 10), H - fg.height - 8), fg)
            else: base.paste(fg, (min(x, W - fg.width - 10), H - fg.height - 8))
        elif m and base is not None:
            d = ImageDraw.Draw(base); x = 30 + (i - 1) * 150; col = {"NEW-ART": (190, 40, 55), "NEW-ARC": (40, 90, 190), "NEW-3D": (30, 140, 100)}[m.group(1)]
            d.rectangle([x, H - 112, x + 140, H - 10], fill=col, outline="white", width=2)
            for j, ln in enumerate(textwrap.wrap("NEEDS: " + m.group(2).replace("_", " "), 13)[:4]): d.text((x + 8, H - 104 + j * 23), ln, font=font(FB, 17), fill="white")
    if base is None: base = Image.new("RGB", (W, H), (34, 34, 34))
    return base, missing
SAN = lambda x: x.replace("→", "›").replace("←", "‹").replace("⇄", "for").replace("▸", "-").replace("≈", "~")
def overlay(im, text, typ):
    d = ImageDraw.Draw(im); text = SAN(text)
    if text and text != "DRAMATISED":
        f = font(FB, 24); lines = textwrap.wrap(text.replace("*", ""), 30)[:3]
        hh = 34 * len(lines) + 12; y0 = 18 if typ in ("SKIT", "PORT", "SET", "MAP") else (H - hh) // 2
        for j, ln in enumerate(lines):
            w = d.textlength(ln, font=f); x = (W - w) / 2
            d.rectangle([x - 10, y0 + j * 34 - 3, x + w + 10, y0 + j * 34 + 31], fill=(34, 34, 34))
            gold = any(c.isdigit() for c in ln) or "*" in text
            d.text((x, y0 + j * 34), ln, font=f, fill=(201, 148, 0) if gold and j == 0 else "white")
    if typ == "SKIT": d.rectangle([W - 132, H - 30, W - 8, H - 8], fill=(34, 34, 34)); d.text((W - 124, H - 29), "DRAMATISED", font=font(FB, 15), fill="white")
    d.rectangle([0, 0, 64, 24], fill=(201, 148, 0)); d.text((6, 0), typ, font=font(FB, 16), fill="black")
    return im

# ---- parse shots ----
shots = []
for r in open(os.path.join(HERE, "shots.txt"), encoding="utf-8"):
    if not r.strip() or r.startswith("#"): continue
    f = [x.strip() for x in r.rstrip("\n").split("|")] + ["", "", ""]
    no, typ, asset, text, note = int(f[0]), f[1], f[2], f[3], f[4]
    shots.append(dict(line=no, type=typ, asset=asset, text=text, note=note, chap=chap_of[no], t=tline(no), spoken=line_text(no)))
# shots on the same line share that line's span
from collections import defaultdict
byline = defaultdict(list)
for s in shots: byline[s["line"]].append(s)
nxt = sorted(times.items())
for no, ss in byline.items():
    t0 = tline(no); later = [t for n, t in nxt if n > no]; t1 = later[0] if later else TOTAL
    for j, s in enumerate(ss): s["t"] = t0 + (t1 - t0) * j / len(ss)

# ---- sheets ----
COLS, CW, CH = 4, W, H + 118
allmiss = []
for c in sorted(set(s["chap"] for s in shots)):
    S = [s for s in shots if s["chap"] == c]; rows = (len(S) + COLS - 1) // COLS
    sheet = Image.new("RGB", (COLS * (CW + 16) + 16, 90 + rows * (CH + 16)), (245, 243, 238)); d = ImageDraw.Draw(sheet)
    title = "HOOK" if c == 0 else ("ENDING: " + chap_name[c] if c == 15 else f"CHAPTER {c}: {chap_name[c]}")
    d.text((18, 20), title, font=font(FB, 40), fill=(34, 34, 34))
    for i, s in enumerate(S):
        x, y = 16 + (i % COLS) * (CW + 16), 90 + (i // COLS) * (CH + 16)
        im, miss = compose(s["type"], s["asset"]); s["missing"] = miss; allmiss += [(c, s["line"], *m) for m in miss]
        sheet.paste(overlay(im, s["text"], s["type"]), (x, y))
        mm, ss_ = divmod(int(s["t"]), 60)
        d.text((x, y + H + 4), f"#{shots.index(s) + 1}  ~{mm}:{ss_:02d}  · line {s['line']}", font=font(FB, 17), fill=(150, 110, 0))
        who, sp = s["spoken"]; cap = (who + ": " if who and who != "N" else "") + sp
        for j, ln in enumerate(textwrap.wrap(cap, 52)[:3]): d.text((x, y + H + 27 + j * 22), ln, font=font(FR, 16), fill=(60, 60, 60))
        if s["note"]: d.text((x, y + H + 94), textwrap.shorten("- " + SAN(s["note"]), 58), font=font(FB, 14), fill=(214, 66, 58))
    sheet.save(os.path.join(OUT, f"ch{c:02d}.jpg"), quality=82)
json.dump(dict(total=TOTAL, shots=shots, missing=allmiss), open(os.path.join(OUT, "shots.json"), "w"), indent=1, default=str)
print(f"{len(shots)} shots, total ~{TOTAL/60:.1f} min, {len(set((m[2], m[3]) for m in allmiss))} missing assets; sheets in {OUT}")
