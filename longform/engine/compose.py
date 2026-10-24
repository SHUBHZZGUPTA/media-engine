#!/usr/bin/env python3
"""Long-form still-layer compositor (v0).

Renders a shot list to MP4 fast: each frame = background plate with a camera move
+ RGBA sprite layers (characters, props, text cards) with simple entrances and a
talking bob. Frames are composed with OpenCV/numpy and piped to ffmpeg.

Usage: python3 compose.py spec.json out.mp4 [--from S --to S] [--fps 30]
Spec: {"w":1920,"h":1080,"fps":30,"shots":[{t0,t1,bg,layers}...]}
  bg:     {"img": path | "#rrggbb", "cam": [[t, cx, cy, zoom], ...],   cx,cy in 0..1 of the plate, zoom>=1
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
    def __init__(self, bg, W, H):
        self.W, self.H = W, H; src = bg["img"]
        if isinstance(src, str) and src.startswith("#"):
            self.img = None; self.col = hex_bgr(src); return
        im = load_rgba(src)[:, :, :3]
        s = max(W / im.shape[1], H / im.shape[0]); self.k = min(2.0, max(1.0, 1 / s))
        size = (math.ceil(im.shape[1] * s * self.k), math.ceil(im.shape[0] * s * self.k))
        self.img = cv2.resize(im, size, interpolation=cv2.INTER_AREA if s * self.k < 1 else cv2.INTER_CUBIC)
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
    def render(self, cx, cy, zoom, t=0.0):
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
        M = np.float32([[z, 0, -x0 * z], [0, z, -y0 * z]])
        return cv2.warpAffine(base, M, (self.W, self.H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

def layer_state(L, t):
    """Return (x, y_bottom, h, alpha) for a layer at time t, or None if hidden."""
    t_in, t_out = L.get("in", -1e9), L.get("out", 1e9)
    if t < t_in or t >= t_out: return None
    x, y, h = L["x"], L["y"], L["h"]
    if "move" in L: x, y = keyed(L["move"], t)
    a, du, en = 1.0, t - t_in, L.get("enter", "pop")
    if en == "pop" and du < .35:   h *= max(ease(du / .35, "back"), .01)
    elif en == "slideL" and du < .45: x -= (1 - ease(du / .45, "out")) * 900
    elif en == "slideR" and du < .45: x += (1 - ease(du / .45, "out")) * 900
    elif en == "up" and du < .4:   y += (1 - ease(du / .4, "out")) * 300
    elif en == "fade" and du < .3: a = du / .3
    if L.get("exit") == "fade" and t_out - t < .25: a *= (t_out - t) / .25
    for p, q in L.get("talk", []):                    # talking bob + squash
        if p <= t < q:
            ph = (t - p) * 2 * math.pi * 3.2
            y -= abs(math.sin(ph)) * h * .025; h *= 1 + .015 * math.sin(ph * 2)
    return x, y, h, a

def render_frame(shot, t, plates, W, H):
    cam = shot["bg"].get("cam", [[shot["t0"], .5, .5, 1.0]])
    frame = plates[id(shot)].render(*keyed(cam, t), t=t)
    for L in shot.get("layers", []):
        st = layer_state(L, t)
        if not st: continue
        x, y, h, a = st
        src = L["img"]
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
            if isinstance(L["img"], dict) and "h" not in L:
                n = L["img"]["text"].count("\n") + 1; L["h"] = int(L["img"].get("size", 64) * (1.18 * n + .5))
    plates = {}
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                            "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    n = int(round((T1 - T0) * fps)); si = 0
    for i in range(n):
        t = T0 + i / fps
        while si < len(shots) - 1 and t >= shots[si]["t1"]:
            plates.pop(id(shots[si]), None); si += 1
        shot = shots[si]
        if id(shot) not in plates: plates[id(shot)] = Plate(shot["bg"], W, H)
        enc.stdin.write(render_frame(shot, t, plates, W, H).tobytes())
    enc.stdin.close(); enc.wait()

if __name__ == "__main__":
    main()
