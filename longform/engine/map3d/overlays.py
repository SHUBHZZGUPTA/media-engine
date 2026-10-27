#!/usr/bin/env python3
"""Equirectangular overlay textures for the 3D globe (lon -180..180, lat 90..-90), from Natural Earth.

  fill(out, regions, color|flag, alpha)       region polygons filled with a colour, or a flag stretched over the region's box
  edge(out, regions, color, width, blur)      glowing border (soft halo + bright core)
  mask_poly(out, bbox, poly, size)            terrain mask (white inside a lon/lat polygon) for a regional bbox
Regions: {"admin0": "Russia"} / {"admin1": "Alaska"} / {"poly": [[lon, lat], ...]}.
"""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
W, H = 4096, 2048
def xy(lon, lat): return ((lon + 180) / 360 * W, (90 - lat) / 180 * H)

def rings(region):
    if "poly" in region: return [region["poly"]]
    src = "ne_50m_admin_1_states_provinces.geojson" if "admin1" in region else "ne_50m_admin_0_countries.geojson"
    want = region.get("admin1") or region.get("admin0")
    out = []
    for f in json.load(open(os.path.join(D, src)))["features"]:
        p = f["properties"]
        if want in (p.get("name"), p.get("NAME"), p.get("ADMIN"), p.get("NAME_EN")):
            g = f["geometry"]; polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
            out += [poly[0] for poly in polys]
    if not out: raise SystemExit(f"region not found: {region}")
    if "drop" in region:      # drop the polygon parts that contain any of these [lon, lat] points (e.g. Crimea from Russia)
        out = [r for r in out if not any(inside(r, *p) for p in region["drop"])]
    if "add" in region:       # add polygon parts of other regions that contain these points (e.g. Crimea to Ukraine)
        for src_reg, p in region["add"]:
            out += [r for r in rings(src_reg) if inside(r, *p)]
    return out

def inside(ring, x, y):
    c = False; n = len(ring)
    for k in range(n):
        x1, y1 = ring[k][:2]; x2, y2 = ring[k - 1][:2]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: c = not c
    return c

def mask(regions, w=W, h=H, to=xy):
    m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m)
    for r in regions:
        for ring in rings(r): d.polygon([to(*c[:2]) for c in ring], fill=255)
    return m

def fill(out, regions, color=None, flag=None, alpha=200, box=None):
    m = mask(regions)
    if flag:
        # stretch the flag over the region's lon/lat box (box overrides, e.g. to skip far-flung islands)
        x0, y0, x1, y1 = box if box else m.getbbox()
        if box: (x0, y0), (x1, y1) = xy(box[0], box[3]), xy(box[1], box[2])
        f = Image.open(flag).convert("RGB").resize((max(1, int(x1 - x0)), max(1, int(y1 - y0))), Image.LANCZOS)
        rgb = Image.new("RGB", (W, H), (0, 0, 0)); rgb.paste(f, (int(x0), int(y0)))
        # pixels outside the box take the nearest flag edge colour
        arr = np.array(rgb); ys, xs = np.nonzero(np.array(m))
        cx = np.clip(xs, int(x0), int(x0) + f.width - 1); cy = np.clip(ys, int(y0), int(y0) + f.height - 1)
        arr[ys, xs] = np.array(f)[cy - int(y0), cx - int(x0)]
        rgb = Image.fromarray(arr)
    else:
        rgb = Image.new("RGB", (W, H), tuple(color))
    a = np.array(m, np.float32) / 255 * alpha
    Image.fromarray(np.dstack([np.array(rgb), a.astype(np.uint8)])).save(out)

def edge(out, regions, color=(255, 214, 90), width=5, blur=10):
    line = Image.new("L", (W, H), 0); d = ImageDraw.Draw(line)
    for r in regions:
        for ring in rings(r): d.line([xy(*c[:2]) for c in ring] + [xy(*ring[0][:2])], fill=255, width=width, joint="curve")
    halo = np.array(line.filter(ImageFilter.GaussianBlur(blur)), np.float32) * 2.2
    core = np.array(line, np.float32)
    a = np.clip(np.maximum(halo, core), 0, 255)
    col = np.zeros((H, W, 3), np.float32) + np.array(color, np.float32)
    col = col * (1 - core[..., None] / 255 * .7) + 255 * core[..., None] / 255 * .7      # white-hot core
    Image.fromarray(np.dstack([col.astype(np.uint8), a.astype(np.uint8)])).save(out)

def flag_ru(out, w=900, h=600):
    im = Image.new("RGB", (w, h)); d = ImageDraw.Draw(im)
    for k, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 43, 30)]): d.rectangle([0, k * h // 3, w, (k + 1) * h // 3], fill=c)
    im.save(out)

def mask_poly(out, bbox, poly, size=(2048, 1024)):
    L0, L1, B0, B1 = bbox; w, h = size
    to = lambda lo, la: ((lo - L0) / (L1 - L0) * w, (B1 - la) / (B1 - B0) * h)
    m = Image.new("L", size, 0); ImageDraw.Draw(m).polygon([to(*c) for c in poly], fill=255); m.save(out)
