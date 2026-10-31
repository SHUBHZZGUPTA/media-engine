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

# ---- pilot (Indus) overlays ----
INDUS = {"poly": [[61.6, 25.2], [64.0, 27.5], [66.5, 30.0], [68.5, 32.5], [71.0, 33.8], [74.6, 33.2], [76.5, 31.5], [77.8, 29.5], [77.5, 28.0],
                  [75.5, 26.5], [73.5, 24.0], [73.2, 22.0], [74.8, 19.5], [72.8, 20.8], [72.5, 21.8], [70.0, 21.2], [68.8, 22.4], [67.5, 23.8],
                  [66.6, 25.4], [63.0, 25.2]]}   # approximate extent of Mature Harappan sites (Sutkagen Dor - Manda - Alamgirpur - Daimabad)
def build_pilot():
    build()
    once("ov_indus.png", lambda p: OVL.fill(p, [INDUS], color=(240, 186, 50), alpha=170))
    once("ov_indus_edge.png", lambda p: OVL.edge(p, [INDUS], (255, 226, 140), 4, 10))
if __name__ == "__main__" and "--pilot" in sys.argv:
    build_pilot(); print(sorted(os.listdir(A)))

# ---- full video (ch2-13) overlays: approximate historical extents (labelled "approx." on screen) ----
MAURYA = {"poly": [[61, 31], [64, 35], [69, 37], [71, 36.5], [74, 35.5], [76, 34], [79, 31], [81, 30], [84, 28], [88, 27], [92, 26], [92, 23], [88, 21.5], [86, 20], [84, 18],
                   [82, 16.5], [80, 14], [78, 12.5], [76, 12.5], [74, 14.5], [73, 17], [72.8, 19.5], [72.5, 21], [70, 21], [68.5, 22.5], [66.5, 25], [63, 25.5], [61.5, 27]]}
GUPTA = {"poly": [[69, 24], [71, 29], [73, 31], [75, 32.5], [77, 31], [80, 29.5], [84, 27.5], [88, 27], [90, 25.5], [89, 22], [87, 21.5], [85, 20.5], [82, 21.5], [79, 22],
                  [76, 22], [74, 22.5], [72, 22], [70, 22.5]]}
CHOLA = {"poly": [[77.3, 8.1], [76.9, 9.5], [76.6, 10.6], [76.5, 11.8], [77.2, 13.2], [78.4, 14.8], [79.6, 16.4], [81.3, 17.5], [83.2, 18.6], [85.2, 20.0], [86.4, 20.3],
                  [84.9, 19.0], [82.6, 17.1], [81.2, 16.0], [80.3, 15.2], [80.2, 13.2], [79.9, 11.8], [79.8, 10.4], [79.2, 9.3], [78.4, 8.6]]}
SRI_N = {"poly": [[79.7, 9.8], [80.3, 9.9], [81.2, 8.6], [81.5, 7.3], [80.8, 7.0], [79.9, 7.2], [79.8, 8.3]]}
SULTANATE = {"poly": [[67, 24.5], [70, 29], [72, 32.5], [74.5, 34], [76, 32], [79, 30.5], [84, 27.5], [88, 26.5], [92, 24.5], [91, 22], [88, 21.5], [86, 20], [84, 18], [82, 16.5],
                      [80, 13], [79, 10], [78, 8.5], [77, 9.5], [76, 12], [74.5, 14.5], [73, 17], [72.7, 20], [70.5, 21], [68.5, 22.5]]}
MUGHAL_1605 = {"poly": [[61.5, 31.5], [64, 34.5], [68, 36], [71, 36.5], [74, 36], [76, 34.5], [78, 32.5], [80, 30.5], [84, 27.6], [88, 26.8], [92, 25.5], [92.5, 22.5], [89, 21.5],
                        [87, 21.6], [85, 21], [82, 21], [79, 20], [76, 19.5], [74, 19], [72.8, 19.5], [72.5, 21], [70, 21], [68.5, 23], [66.5, 25], [63, 25.5], [61.5, 28]]}
MUGHAL_1707 = {"poly": [[61.5, 31.5], [64, 34.5], [68, 36], [71, 36.5], [74, 36], [76, 34.5], [78, 32.5], [80, 30.5], [84, 27.6], [88, 26.8], [92, 25.5], [92.5, 22.5], [89, 21.5],
                        [87, 21.6], [85, 21], [84, 18.5], [82, 16.5], [80.3, 14], [79.8, 12], [78.5, 11], [77, 11], [76, 12.5], [74.5, 14.5], [73.3, 16.5], [72.8, 19], [72.5, 21],
                        [70, 21], [68.5, 23], [66.5, 25], [63, 25.5], [61.5, 28]]}
RAJ = [IN, {"admin0": "Pakistan"}, {"admin0": "Bangladesh"}]
def build_full():
    build_pilot()
    for name, reg, col in [("maurya", MAURYA, (230, 140, 40)), ("gupta", GUPTA, (240, 186, 50)), ("chola", CHOLA, (40, 150, 200)), ("sultanate", SULTANATE, (60, 140, 80)),
                           ("mughal1605", MUGHAL_1605, (60, 150, 90)), ("mughal1707", MUGHAL_1707, (40, 120, 70))]:
        once(f"ov_{name}.png", lambda p, r=reg, c=col: OVL.fill(p, [r], color=c, alpha=175))
        once(f"ov_{name}_edge.png", lambda p, r=reg: OVL.edge(p, [r], (255, 236, 170), 4, 10))
    once("ov_srilanka_n.png", lambda p: OVL.fill(p, [SRI_N], color=(40, 150, 200), alpha=175))
    once("ov_raj.png", lambda p: OVL.fill(p, RAJ, color=(200, 40, 50), alpha=170))
    def raj_outline():      # one outer border for British India (no 1947 borders inside it)
        import json as _j
        from shapely.geometry import shape as _sh
        from shapely.ops import unary_union as _uu
        F = {f["properties"]["ADM0_A3"]: _sh(f["geometry"]) for f in _j.load(open(os.environ["MAP_COUNTRIES"]))["features"] if f["properties"]["ADM0_A3"] in ("IND", "PAK", "BGD")}
        u = _uu(list(F.values())).buffer(0.02).buffer(-0.02)
        polys = [u] if u.geom_type == "Polygon" else list(u.geoms)
        return [{"poly": [list(c) for c in g.exterior.coords]} for g in polys if g.area > 0.5]
    once("ov_raj_edge.png", lambda p: OVL.edge(p, raj_outline(), (255, 200, 190), 4, 10))
    once("ov_pak.png", lambda p: OVL.fill(p, [{"admin0": "Pakistan"}, {"admin0": "Bangladesh"}], color=(20, 110, 60), alpha=200))
    once("ov_pak_edge.png", lambda p: OVL.edge(p, [{"admin0": "Pakistan"}, {"admin0": "Bangladesh"}], (200, 255, 210), 4, 10))
if __name__ == "__main__" and "--full" in sys.argv:
    build_full(); print(sorted(os.listdir(A)))
