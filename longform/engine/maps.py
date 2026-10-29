#!/usr/bin/env python3
"""Stylised map plates + animated overlays from Natural Earth (public domain).

Usage: python3 maps.py config.json outdir
config: {"plates": [{"name", "bbox": [lon0, lon1, lat0, lat1], "w", "h", "highlight": [ISO_A3...],
                     "rivers": [names], "points": {"Kyiv": [lon, lat]},
                     "overlays": [{"name", "kind": "fill|route|arrow|pin", ...}]}]}
Writes <name>.png (opaque plate), <name>__<overlay>.png (transparent, same size),
<name>__<overlay>.npy (reveal order 0..1 for "draw" overlays), and <name>.json (pixel points).
Longitudes may exceed 180 to cross the date line (e.g. [140, 250]).
"""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
OCEAN, LAND, BORDER, HIGH, HIGH_EDGE, RIVER = (38, 92, 140), (150, 170, 112), (98, 116, 72), (214, 66, 58), (255, 236, 220), (128, 196, 240)

def merc(lat): return math.log(math.tan(math.pi / 4 + math.radians(max(min(lat, 85), -85)) / 2))

class Proj:
    def __init__(self, bbox, w, h):
        self.lon0, self.lon1, lat0, lat1 = bbox; self.w, self.h = w, h
        self.y0, self.y1 = merc(lat1), merc(lat0)
    def ring_offset(self, ring):
        """Shift a whole ring by -360/0/+360 so it lands nearest the plate centre (date-line safe)."""
        c = (self.lon0 + self.lon1) / 2; m = sum(p[0] for p in ring) / len(ring)
        return min((-360, 0, 360), key=lambda o: abs(m + o - c))
    def __call__(self, lon, lat, off=None):
        if off is None: off = min((-360, 0, 360), key=lambda o: abs(lon + o - (self.lon0 + self.lon1) / 2))
        lon += off
        x = (lon - self.lon0) / (self.lon1 - self.lon0) * self.w
        y = (self.y0 - merc(lat)) / (self.y0 - self.y1) * self.h
        return x, y

def rings(geom):
    t, c = geom["type"], geom["coordinates"]
    polys = [c] if t == "Polygon" else c if t == "MultiPolygon" else []
    for p in polys:
        yield p[0]

def draw_ring(d, P, ring, **kw):
    off = P.ring_offset(ring)
    d.polygon([P(lon, lat, off) for lon, lat in ring], **kw)

def plate(cfg, out):
    w, h = cfg.get("w", 3200), cfg.get("h", 1800); P = Proj(cfg["bbox"], w, h)
    countries = json.load(open(os.environ.get("MAP_COUNTRIES") or os.path.join(D, "ne_50m_admin_0_countries.geojson")))["features"]  # MAP_COUNTRIES: per-video border override (e.g. India official view)
    hi = set(cfg.get("highlight", []))
    img = Image.new("RGB", (w, h), OCEAN); d = ImageDraw.Draw(img)
    for f in countries:
        for r in rings(f["geometry"]): draw_ring(d, P, r, fill=LAND)
    # soft relief texture on land: blurred noise multiplied in
    rng = np.random.default_rng(7)
    noise = Image.fromarray((rng.random((h // 8, w // 8)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6))
    land_mask = Image.new("L", (w, h), 0); lm = ImageDraw.Draw(land_mask)
    for f in countries:
        for r in rings(f["geometry"]): draw_ring(lm, P, r, fill=255)
    arr = np.asarray(img).astype(np.float32); n = (np.asarray(noise, np.float32) / 255 - .5) * 34
    m = np.asarray(land_mask, np.float32)[..., None] / 255
    arr = arr + n[..., None] * m
    # gentle ocean depth gradient
    yy = np.linspace(-1, 1, h)[:, None, None]; arr = arr - (1 - m) * (np.abs(yy) * 18)
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(img)
    for f in countries:
        iso = f["properties"].get("ADM0_A3") or f["properties"].get("ISO_A3")
        for r in rings(f["geometry"]):
            if iso in hi: draw_ring(d, P, r, fill=HIGH, outline=HIGH_EDGE, width=6)
            else: draw_ring(d, P, r, outline=BORDER, width=2)
    if cfg.get("rivers"):
        rv = json.load(open(os.path.join(D, "ne_50m_rivers_lake_centerlines.geojson")))["features"]
        for f in rv:
            if (f["properties"].get("name_en") or f["properties"].get("name")) in cfg["rivers"]:
                g = f["geometry"]; lines = [g["coordinates"]] if g["type"] == "LineString" else g["coordinates"]
                for ln in lines: d.line([P(*c) for c in ln], fill=RIVER, width=7, joint="curve")
    name = cfg["name"]; img.save(os.path.join(out, name + ".png"))
    pts = {k: P(*v) for k, v in cfg.get("points", {}).items()}
    for ov in cfg.get("overlays", []): overlay(ov, P, w, h, out, name, pts, countries)
    json.dump({"w": w, "h": h, "points": pts}, open(os.path.join(out, name + ".json"), "w"), indent=1)

def path_order(segs, w, h):
    """Reveal-order map: each painted pixel gets its arc-length fraction along the path."""
    total = sum(math.dist(a, b) for a, b in segs) or 1; acc, order = 0, np.full((h, w), 2.0, np.float32)
    for a, b in segs:
        L = math.dist(a, b); n = max(int(L / 3), 1)
        for k in range(n + 1):
            u = k / n; x, y = a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u
            v = (acc + L * u) / total; r = 26
            x0, x1, y0, y1 = int(max(x - r, 0)), int(min(x + r, w)), int(max(y - r, 0)), int(min(y + r, h))
            if x0 < x1 and y0 < y1: order[y0:y1, x0:x1] = np.minimum(order[y0:y1, x0:x1], v)
        acc += L
    return order

def overlay(ov, P, w, h, out, name, pts, countries):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); order = None
    kind = ov["kind"]; col = tuple(ov.get("color", [255, 214, 64])) + (255,)
    if kind == "fill":                       # a polygon (lon/lat list) or a country/region by ISO + filter
        polys = []
        if "poly" in ov: polys = [ov["poly"]]
        for f in countries:
            if (f["properties"].get("ADM0_A3") or f["properties"].get("ISO_A3")) == ov.get("iso"):
                for r in rings(f["geometry"]):
                    lo = [p[0] for p in r]; la = [p[1] for p in r]
                    flt = ov.get("filter")  # [lon_max, lat_min] keeps parts west/north of these
                    if not flt or (sum(lo) / len(lo) < flt[0] and sum(la) / len(la) > flt[1]): polys.append(r)
        a = int(ov.get("alpha", 200))
        for r in polys: draw_ring(d, P, r, fill=col[:3] + (a,), outline=(255, 255, 255, 255), width=6)
    elif kind in ("route", "arrow"):
        xy = [P(*c) for c in ov["path"]]; segs = list(zip(xy, xy[1:]))
        wid = ov.get("width", 14)
        if ov.get("dash"):
            for a, b in segs:
                L = math.dist(a, b); n = max(int(L / 46), 1)
                for k in range(0, n, 2):
                    u0, u1 = k / n, min((k + 1) / n, 1)
                    d.line([(a[0] + (b[0] - a[0]) * u0, a[1] + (b[1] - a[1]) * u0), (a[0] + (b[0] - a[0]) * u1, a[1] + (b[1] - a[1]) * u1)], fill=col, width=wid)
        else:
            d.line(xy, fill=(0, 0, 0, 120), width=wid + 8, joint="curve"); d.line(xy, fill=col, width=wid, joint="curve")
        if kind == "arrow":
            (x0, y0), (x1, y1) = xy[-2], xy[-1]; ang = math.atan2(y1 - y0, x1 - x0); s = wid * 3.2
            tip = [(x1 + math.cos(ang) * s * .6, y1 + math.sin(ang) * s * .6),
                   (x1 + math.cos(ang + 2.5) * s, y1 + math.sin(ang + 2.5) * s),
                   (x1 + math.cos(ang - 2.5) * s, y1 + math.sin(ang - 2.5) * s)]
            d.polygon(tip, fill=col); segs.append(((x1, y1), tip[0]))
        order = path_order(segs, w, h)
    elif kind == "pin":
        x, y = pts[ov["point"]]; r = ov.get("r", 22)
        d.ellipse([x - r - 6, y - r - 6, x + r + 6, y + r + 6], fill=(255, 255, 255, 255))
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    fn = f"{name}__{ov['name']}"
    im.save(os.path.join(out, fn + ".png"))
    if order is not None: np.save(os.path.join(out, fn + ".npy"), np.clip(order, 0, 2).astype(np.float16))

if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1])); os.makedirs(sys.argv[2], exist_ok=True)
    for p in cfg["plates"]: plate(p, sys.argv[2]); print("plate", p["name"])
