#!/usr/bin/env python3
"""Long-form still-layer compositor (v0).

Renders a shot list to MP4 fast: each frame = background plate with a camera move
+ RGBA sprite layers (characters, props, text cards) with simple entrances and a
talking bob. Frames are composed with OpenCV/numpy and piped to ffmpeg.

Usage: python3 compose.py spec.json out.mp4 [--from S --to S] [--fps 30]
Spec: {"w":1920,"h":1080,"fps":30,"shots":[{t0,t1,bg,layers}...]}
  bg:     {"video": clip.mp4} plays a pre-rendered clip from the shot's start (camera keys ignored), or
          {"img": path | "#rrggbb", "cam": [[t, cx, cy, zoom], ...],   cx,cy in 0..1 of the plate, zoom>=1
           "blur": px, "dim": 0..1   (backdrop mode: blurred, darkened copy of a scene)
           "over": [{"img": overlay.png, "in": t, "dur": s, "mode": "fade|draw", "out": t}]}  (draw needs overlay.npy)
  layer:  {"img": path | {"text": str, "size": px, "color": "#fff", "box": "#000"|null, "font": path},
           "x": px (centre), "y": px (bottom), "h": px height,
           "in": t, "out": t, "enter": "pop|slideL|slideR|up|fade|none", "exit": "fade|none",
           "talk": [[a, b], ...], "flip": bool, "move": [[t, x, y], ...]}
Times are absolute seconds on the video timeline.
"""
import json, math, subprocess, sys, functools
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

def ease(u, kind="io"):
    u = min(max(u, 0.0), 1.0)
    if kind == "io":   return u * u * (3 - 2 * u)
    if kind == "out":  return 1 - (1 - u) ** 3
    if kind == "back":
        c1, c3 = 1.70158, 2.70158
        return 1 + c3 * (u - 1) ** 3 + c1 * (u - 1) ** 2
    return u

def keyed(keys, t):
    """Piecewise ease-in-out interpolation over [[t, v...], ...]."""
    if t <= keys[0][0]: return keys[0][1:]
    for a, b in zip(keys, keys[1:]):
        if t <= b[0]:
            u = ease((t - a[0]) / max(b[0] - a[0], 1e-6))
            return [x + (y - x) * u for x, y in zip(a[1:], b[1:])]
    return keys[-1][1:]

def hex_bgr(h):
    h = h.lstrip("#"); return (int(h[4:6], 16), int(h[2:4], 16), int(h[0:2], 16))

@functools.lru_cache(maxsize=256)
def load_rgba(path):
    im = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if im is None: raise FileNotFoundError(path)
    if im.ndim == 2: im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGRA)
    if im.shape[2] == 3: im = np.dstack([im, np.full(im.shape[:2], 255, np.uint8)])
    ys, xs = np.where(im[:, :, 3] > 8)          # trim transparent margins
    if len(xs): im = im[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return im

@functools.lru_cache(maxsize=256)
def text_rgba(text, size, color, box, font):
    f = ImageFont.truetype(font, size) if font else ImageFont.load_default(size)
    l, t, r, b = ImageDraw.Draw(Image.new("RGBA", (1, 1))).multiline_textbbox((0, 0), text, font=f, align="center", spacing=int(size * .18))
    l, t, r, b = int(l), int(t), int(r + .999), int(b + .999)
    pad = int(size * 0.35) if box else 4
    im = Image.new("RGBA", (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if box: d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=int(size * .2), fill=box)
    d.multiline_text((pad - l, pad - t), text, font=f, fill=color, align="center", spacing=int(size * .18),
                     stroke_width=0 if box else max(2, size // 14), stroke_fill="#000000")
    return cv2.cvtColor(np.array(im), cv2.COLOR_RGBA2BGRA)

@functools.lru_cache(maxsize=1024)
def scaled(key, h, flip):
    src = text_rgba(*key[1:]) if key[0] == "text" else load_rgba(key[1])
    s = max(h, 1) / src.shape[0]
    out = cv2.resize(src, (max(1, int(src.shape[1] * s)), max(1, int(h))), interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_LINEAR)
    return out[:, ::-1].copy() if flip else out

def blend(frame, spr, x, y, alpha=1.0):
    """Alpha-blend sprite with its top-left at (x, y)."""
    H, W = frame.shape[:2]; h, w = spr.shape[:2]
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
    if x0 >= x1 or y0 >= y1: return
    s = spr[y0 - y:y1 - y, x0 - x:x1 - x]
    a = s[:, :, 3:4].astype(np.float32) * (alpha / 255.0)
    roi = frame[y0:y1, x0:x1]
    roi[:] = (s[:, :, :3] * a + roi * (1 - a)).astype(np.uint8)

class Plate:
    """Background plate kept at up to 2x frame resolution so camera zooms stay sharp.
    Optional overlays (same size as the source plate) fade or draw on in plate space."""
    def __init__(self, bg, W, H, t0=0.0):
        self.W, self.H = W, H; src = bg["img"]; self.video = None
        if bg.get("video"):                                  # pre-rendered clip (e.g. a 3D map), frame = time since shot start
            self.video = bg["video"]; self.t0 = t0; self.cap = None; self.idx = -1; self.last = None
            self.img = None; self.col = hex_bgr("#02070d"); return
        if isinstance(src, str) and src.startswith("#"):
            self.img = None; self.col = hex_bgr(src); return
        im = load_rgba(src)[:, :, :3]
        s = max(W / im.shape[1], H / im.shape[0]); self.k = min(2.0, max(1.0, 1 / s))
        size = (math.ceil(im.shape[1] * s * self.k), math.ceil(im.shape[0] * s * self.k))
        self.img = cv2.resize(im, size, interpolation=cv2.INTER_AREA if s * self.k < 1 else cv2.INTER_CUBIC)
        if bg.get("blur"):                                  # backdrop mode: soft, darker copy of a scene
            r = int(bg["blur"] * self.k) | 1
            self.img = cv2.GaussianBlur(self.img, (0, 0), r)
        if bg.get("dim"): self.img = (self.img.astype(np.float32) * bg["dim"]).astype(np.uint8)
        self.over = []
        for ov in bg.get("over", []):
            o = cv2.resize(cv2.imread(ov["img"], cv2.IMREAD_UNCHANGED), size, interpolation=cv2.INTER_AREA)
            ys, xs = np.where(o[:, :, 3] > 0)
            if not len(xs): continue
            y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
            order = None
            if ov.get("mode") == "draw":
                order = cv2.resize(np.load(ov["img"][:-4] + ".npy").astype(np.float32), size, interpolation=cv2.INTER_NEAREST)[y0:y1, x0:x1]
            self.over.append(dict(ov, rgba=o[y0:y1, x0:x1], box=(y0, y1, x0, x1), order=order))
    def vframe(self, t):
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.video); self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30; self.idx = -1
        want = max(0, int(round((t - self.t0) * self.fps)))
        if want < self.idx: self.cap.release(); self.cap = None; return self.vframe(t)
        while self.idx < want:
            ok, fr = self.cap.read()
            if not ok: break
            self.idx += 1; self.last = fr
        f = self.last if self.last is not None else np.zeros((self.H, self.W, 3), np.uint8)
        return f if f.shape[:2] == (self.H, self.W) else cv2.resize(f, (self.W, self.H), interpolation=cv2.INTER_AREA)
    def render(self, cx, cy, zoom, t=0.0):
        if self.video: return self.vframe(t).copy()
        if self.img is None:
            return np.full((self.H, self.W, 3), self.col, np.uint8)
        base = self.img
        active = [o for o in self.over if o.get("in", 0) <= t < o.get("out", 1e9)]
        if active:
            base = base.copy()
            for o in active:
                u = ease((t - o.get("in", 0)) / max(o.get("dur", .5), 1e-3), "io")
                rgba = o["rgba"]; y0, y1, x0, x1 = o["box"]
                a = rgba[:, :, 3:4].astype(np.float32) / 255
                if o.get("mode") == "draw": a = a * (o["order"] <= u)[..., None]
                else: a = a * u
                roi = base[y0:y1, x0:x1]; roi[:] = (rgba[:, :, :3] * a + roi * (1 - a)).astype(np.uint8)
        ih, iw = base.shape[:2]; z = zoom / self.k; vw, vh = self.W / z, self.H / z
        x0 = min(max(cx * iw - vw / 2, 0), iw - vw); y0 = min(max(cy * ih - vh / 2, 0), ih - vh)
        M = np.float32([[z, 0, -x0 * z], [0, z, -y0 * z]]); self.view = (z, x0, y0, iw, ih)
        return cv2.warpAffine(base, M, (self.W, self.H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    def to_screen(self, nx, ny):
        """Plate point (0..1 of the plate) -> screen pixels for the current camera."""
        if self.img is None: return nx * self.W, ny * self.H
        z, x0, y0, iw, ih = self.view; return (nx * iw - x0) * z, (ny * ih - y0) * z

def layer_state(L, t):
    """Return (x, y_bottom, h, alpha) for a layer at time t, or None if hidden."""
    t_in, t_out = L.get("in", -1e9), L.get("out", 1e9)
    if t < t_in or t >= t_out: return None
    x, y, h = L["x"], L["y"], L["h"]
    if "move" in L: x, y = keyed(L["move"], t)
    a, du, en = 1.0, t - t_in, L.get("enter", "pop")
    if en == "pop" and du < .35:   h *= max(ease(du / .35, "back"), .01)
    elif en == "slam" and du < .22: h *= 2.1 - 1.1 * ease(du / .22, "out"); a = min(1.0, du / .08)
    elif en == "slideL" and du < .45: x -= (1 - ease(du / .45, "out")) * 900
    elif en == "slideR" and du < .45: x += (1 - ease(du / .45, "out")) * 900
    elif en == "up" and du < .4:   y += (1 - ease(du / .4, "out")) * 300
    elif en == "fade" and du < .3: a = du / .3
    if L.get("exit") == "fade" and t_out - t < .25: a *= (t_out - t) / .25
    if not isinstance(L["img"], dict) and not L.get("still"):   # idle sway so characters never freeze
        ph = (L["x"] * 0.013) % 6.283
        y -= (math.sin(t * 2 * math.pi * .45 + ph) * .5 + .5) * h * .012; x += math.sin(t * 2 * math.pi * .23 + ph) * h * .006
    for p, q in L.get("talk", []):                    # talking bob + squash
        if p <= t < q:
            ph = (t - p) * 2 * math.pi * 3.2
            y -= abs(math.sin(ph)) * h * .025; h *= 1 + .015 * math.sin(ph * 2)
    return x, y, h, a

def render_frame(shot, t, plates, W, H):
    cam = shot["bg"].get("cam", [[shot["t0"], .5, .5, 1.0]])
    plate = plates[id(shot)]
    frame = plate.render(*keyed(cam, t), t=t)
    for L in shot.get("layers", []):
        if "circle" in L:                                   # hand-drawn marker loop on the named thing
            if not (L.get("in", 0) <= t < L.get("out", 1e9)): continue
            c = L["circle"]; u = ease((t - L.get("in", 0)) / L.get("dur", .55), "out")
            cx, cy = plate.to_screen(c["cx"], c["cy"]) if c.get("space") == "plate" else (c["cx"], c["cy"])
            col = hex_bgr(c.get("color", "#ff3b30")); end = -100 + 400 * u
            for k, (dx, dy, s) in enumerate([(0, 0, 1.0), (3, -2, 1.04)]):
                if k and u < .8: break
                cv2.ellipse(frame, (int(cx + dx), int(cy + dy)), (int(c["rx"] * s), int(c["ry"] * s)), -8, -100, end, col, 9 - 3 * k, cv2.LINE_AA)
            continue
        st = layer_state(L, t)
        if not st: continue
        x, y, h, a = st
        src = L["img"]
        if isinstance(src, dict) and "count" in L:          # number counts up with its spoken word
            cn = L["count"]; u = ease((t - L.get("in", 0)) / cn.get("dur", 1.2), "out")
            v = cn["from"] + (cn["to"] - cn["from"]) * u
            src = dict(src, text=cn["fmt"].format(v=int(round(v))))
            h = text_rgba(src["text"], src.get("size", 64), src.get("color", "#ffffff"), src.get("box"), src.get("font")).shape[0] * (h / L["h"])
        key = ("text", src["text"], src.get("size", 64), src.get("color", "#ffffff"), src.get("box"), src.get("font")) \
              if isinstance(src, dict) else ("img", src)
        spr = scaled(key, int(h * (1 if key[0] == "img" else 1)) if key[0] == "img" else int(h), bool(L.get("flip")))
        if key[0] == "img" and L.get("shadow", True):   # soft contact shadow under characters
            sw, sh = int(spr.shape[1] * .42), max(int(spr.shape[0] * .035), 4)
            x0, x1, y0, y1 = max(int(x) - sw, 0), min(int(x) + sw, W), max(int(y) - sh, 0), min(int(y) + sh, H)
            if x0 < x1 and y0 < y1:
                m = np.zeros((y1 - y0, x1 - x0), np.uint8)
                cv2.ellipse(m, (int(x) - x0, int(y) - y0), (sw, sh), 0, 0, 360, 255, -1)
                m = cv2.GaussianBlur(m, (0, 0), sh * .6).astype(np.float32)[..., None] * (.35 * a / 255)
                frame[y0:y1, x0:x1] = (frame[y0:y1, x0:x1] * (1 - m)).astype(np.uint8)
        blend(frame, spr, int(x - spr.shape[1] / 2), int(y - spr.shape[0]), a)
    return frame

def main():
    args = sys.argv[1:]
    spec = json.load(open(args[0])); out = args[1]
    W, H, fps = spec.get("w", 1920), spec.get("h", 1080), spec.get("fps", 30)
    if "--fps" in args: fps = float(args[args.index("--fps") + 1])
    shots = sorted(spec["shots"], key=lambda s: s["t0"])
    T0 = float(args[args.index("--from") + 1]) if "--from" in args else shots[0]["t0"]
    T1 = float(args[args.index("--to") + 1]) if "--to" in args else shots[-1]["t1"]
    # text layers need a height: derive from font size if missing
    for s in shots:
        for L in s.get("layers", []):
            if isinstance(L.get("img"), dict) and "h" not in L:      # text keeps its natural rendered size
                src = L["img"]
                L["h"] = text_rgba(src["text"], src.get("size", 64), src.get("color", "#ffffff"), src.get("box"), src.get("font")).shape[0]
    plates = {}
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                            "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    caps = Captions(spec.get("captions", []), W, H)
    punches = sorted(spec.get("punch", [])); shakes = spec.get("shake", [])
    n = int(round((T1 - T0) * fps)); si = 0
    for i in range(n):
        t = T0 + i / fps
        while si < len(shots) - 1 and t >= shots[si]["t1"]: si += 1
        shot = shots[si]
        for s in (shots[si - 1] if si else None, shot):
            if s is not None and id(s) not in plates: plates[id(s)] = Plate(s["bg"], W, H, s["t0"])
        for k in list(plates):                              # free plates no longer needed
            if k not in (id(shot), id(shots[si - 1]) if si else None): plates.pop(k)
        frame = render_frame(shot, t, plates, W, H)
        cut, du = shot.get("cut", "curve"), t - shot["t0"]
        if si and cut != "hard" and du < CUT_LEN.get(cut, .3):
            frame = transition(render_frame(shots[si - 1], t, plates, W, H), frame, cut, du / CUT_LEN.get(cut, .3), W, H)
        z, dx, dy = 1.0, 0.0, 0.0
        for pt, lvl in punches:                              # punch-in: fast zoom up, settle back
            if pt <= t < pt + .9:
                d = t - pt; env = ease(d / .09, "out") if d < .09 else math.exp(-(d - .09) / .28)
                z = max(z, 1 + (lvl - 1) * env)
        for st, dur, amp in shakes:                          # decaying camera shake on impacts
            if st <= t < st + dur:
                k = 1 - (t - st) / dur; dx += math.sin(t * 71) * amp * k; dy += math.cos(t * 53) * amp * k
        if z != 1.0 or dx or dy:
            M = np.float32([[z, 0, (1 - z) * W / 2 + dx], [0, z, (1 - z) * H / 2 + dy]])
            frame = cv2.warpAffine(frame, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        caps.draw(frame, t)
        enc.stdin.write(frame.tobytes())
    enc.stdin.close(); enc.wait()

CUT_LEN = {"curve": .32, "whip": .3, "zoom": .4, "flash": .45}
def transition(a, b, cut, u, W, H):
    """Blend outgoing frame a into incoming frame b; u = 0..1 through the cut. Full-bleed: never shows an edge."""
    def scale(img, s):
        M = np.float32([[s, 0, (1 - s) * W / 2], [0, s, (1 - s) * H / 2]])
        return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    e = ease(u, "io")
    if cut == "curve":
        return cv2.addWeighted(scale(a, 1 + .05 * e), 1 - e, scale(b, 1.06 - .06 * e), e, 0)
    if cut == "zoom":
        return cv2.addWeighted(scale(a, 1 + .35 * e), 1 - e, scale(b, 1.25 - .25 * e), e, 0)
    if cut == "whip":
        off = int(W * e); k = int(9 + 70 * math.sin(math.pi * u)) | 1
        out = np.empty_like(a); out[:, :W - off] = a[:, off:]; out[:, W - off:] = b[:, :off]
        return cv2.blur(out, (k, 1))
    if cut == "flash":
        w = max(0.0, 1 - u / .55); img = b if u > .12 else a
        return cv2.addWeighted(img, 1 - w * .9, np.full_like(img, 255), w * .9, 0)
    return b

class Captions:
    """Anchor-style caption rail: dark rounded bar, spoken words white, upcoming words dim,
    keywords get a red bar once spoken. Rendered per chunk state and cached."""
    FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
    def __init__(self, chunks, W, H, size=58):
        self.chunks = chunks; self.W, self.H = W, H; self.size = size; self.cache = {}
        self.f = ImageFont.truetype(self.FONT, size)
    def img(self, ci, n):
        key = (ci, n)
        if key in self.cache: return self.cache[key]
        words = self.chunks[ci]["words"]; d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        sp = d0.textlength(" ", font=self.f); ws = [d0.textlength(w[0], font=self.f) for w in words]
        pad, hgt = 34, int(self.size * 1.55); width = int(sum(ws) + sp * (len(ws) - 1) + 2 * pad)
        im = Image.new("RGBA", (width, hgt), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, width - 1, hgt - 1], radius=hgt // 2, fill=(14, 14, 18, 190))
        x = pad
        for k, (w, wl) in enumerate(zip(words, ws)):
            if k < n and w[3]: d.rounded_rectangle([x - 8, 10, x + wl + 8, hgt - 10], radius=10, fill=(255, 59, 48, 255))
            d.text((x, hgt / 2), w[0], font=self.f, anchor="lm", fill=(255, 255, 255, 255) if k < n else (255, 255, 255, 120))
            x += wl + sp
        arr = cv2.cvtColor(np.array(im), cv2.COLOR_RGBA2BGRA); self.cache[key] = arr
        if len(self.cache) > 400: self.cache.pop(next(iter(self.cache)))
        return arr
    def draw(self, frame, t):
        for ci, c in enumerate(self.chunks):
            if c["t0"] <= t < c["t1"]:
                n = sum(1 for w in c["words"] if w[1] <= t)
                spr = self.img(ci, max(n, 1)); h, w = spr.shape[:2]
                blend(frame, spr, (self.W - w) // 2, self.H - h - 46)
                return

if __name__ == "__main__":
    main()
