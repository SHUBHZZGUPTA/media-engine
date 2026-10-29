#!/usr/bin/env python3
"""Globe overlay textures for the India video (built once into ../map3d_art).
Borders: India's official boundary (see README.md), via MAP_COUNTRIES."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["MAP_COUNTRIES"] = os.path.join(HERE, "ne_50m_admin_0_countries_ind.geojson")
sys.path.insert(0, os.path.join(HERE, "..", "..", "engine", "map3d"))
import overlays as OVL
from PIL import Image, ImageDraw, ImageEnhance
A = os.path.join(HERE, "..", "map3d_art"); os.makedirs(A, exist_ok=True)
IN = {"admin0": "India"}
BM = os.path.join(HERE, "..", "..", "..", "outputs", "fetch", "ru-pilot-3d-rus", "globe_bmng.jpg")   # NASA Blue Marble NG (public domain)

def flag_in(out, w=1350, h=900):
    im = Image.new("RGB", (w, h)); d = ImageDraw.Draw(im)
    for k, c in enumerate([(255, 153, 51), (255, 255, 255), (19, 136, 8)]): d.rectangle([0, k * h // 3, w, (k + 1) * h // 3], fill=c)
    cx, cy, r = w / 2, h / 2, h / 3 * 0.43; navy = (0, 0, 128); lw = max(3, int(r * .07))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=navy, width=lw)
    d.ellipse([cx - r * .17, cy - r * .17, cx + r * .17, cy + r * .17], fill=navy)
    for k in range(24):
        a = k * 2 * math.pi / 24; d.line([cx, cy, cx + math.cos(a) * r, cy + math.sin(a) * r], fill=navy, width=max(2, lw // 2))
    im.save(out)
def once(name, fn):
    p = os.path.join(A, name)
    if not os.path.exists(p): fn(p)
    return name
def build():
    once("globe.jpg", lambda p: ImageEnhance.Color(ImageEnhance.Contrast(ImageEnhance.Brightness(Image.open(BM).convert("RGB")).enhance(1.45)).enhance(1.1)).enhance(1.3).save(p, quality=92))
    once("flag_in.png", flag_in)
    once("ov_in_flag.png", lambda p: OVL.fill(p, [IN], flag=os.path.join(A, "flag_in.png"), alpha=200, box=[68.0, 97.5, 6.5, 37.2]))
    once("ov_in_edge.png", lambda p: OVL.edge(p, [IN], (255, 214, 90), 5, 10))
    once("ov_in_red.png", lambda p: OVL.fill(p, [IN], color=(214, 66, 58), alpha=200))
if __name__ == "__main__":
    build(); print(sorted(os.listdir(A)))
