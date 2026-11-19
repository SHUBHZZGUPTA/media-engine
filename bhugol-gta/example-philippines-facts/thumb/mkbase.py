#!/usr/bin/env python3
"""Bright thumbnail map base: EOX plate regraded (turquoise sea, vivid land) + the Philippines filled (red relief or flag).
usage: python3 mkbase.py <out.jpg> <lon_c> <lat_c> <scale> <fill: red|flag|none> [glow_trench]
Writes <out>.json with the projector (so the HTML overlay can place callouts by lon/lat)."""
import json, math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
A = '/home/claude/ph/build/assets/'
out, lonc, latc, sc, fill = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
glow = len(sys.argv) > 6 and sys.argv[6] == 'trench'
m = json.load(open(A + 'map_phz6.json')); plate = Image.open(A + 'map_phz6.jpg').convert('RGB')
Z = m['z']; N = 2 ** Z * 256
def merc(lon, lat):
    s = math.sin(math.radians(lat)); return (lon + 180) / 360 * N, (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * N
cx, cy = merc(lonc, latc); W, H = 1280, 720
def P(lon, lat):
    x, y = merc(lon, lat); return ((x - cx) * sc + W / 2, (y - cy) * sc + H / 2)
# crop + scale the plate to the canvas
x0 = cx - W / 2 / sc - m['px0'][0]; y0 = cy - H / 2 / sc - m['px0'][1]
img = plate.transform((W, H), Image.AFFINE, (1 / sc, 0, x0, 0, 1 / sc, y0), resample=Image.BICUBIC, fillcolor=(23, 42, 75))
a = np.asarray(img).astype(np.float32) / 255
r, g, b = a[..., 0], a[..., 1], a[..., 2]
lum = .3 * r + .59 * g + .11 * b
LANDM = Image.new('L', (W * 2, H * 2), 0); ld = ImageDraw.Draw(LANDM)
for f_ in json.load(open('/tmp/ne10_view.json')):
    polys = f_ if isinstance(f_[0][0][0], list) else [f_]
    for poly in polys:
        ring = [tuple(c * 2 for c in P(lo, la)) for lo, la in poly[0]]
        if len(ring) > 2: ld.polygon(ring, fill=255)
LANDM = LANDM.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.0))
sea = 1 - np.asarray(LANDM).astype(np.float32) / 255
sea = sea > .5
sea = np.asarray(Image.fromarray((sea * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32) / 255
# sea: map its own brightness (bathymetry) onto a deep→shallow turquoise ramp
t = np.clip((lum - .10) / .16, 0, 1)[..., None]
deep, shallow = np.array([.05, .42, .66]), np.array([.36, .83, .90])
sea_rgb = deep * (1 - t) + shallow * t
from scipy.ndimage import gaussian_filter
sea_rgb = np.stack([gaussian_filter(sea_rgb[..., k], 5) for k in range(3)], -1)
# land: vivid, brighter, a touch warm
hsvish = a.copy(); mean = lum[..., None]
land = np.clip(mean + (a - mean) * 1.9, 0, 1) * 1.35 + np.array([.03, .02, -.02])
land = np.clip(land, 0, 1)
res = land * (1 - sea[..., None]) + sea_rgb * sea[..., None]
res_img = Image.fromarray((res * 255).astype(np.uint8))
# country fill
geo = json.load(open('/tmp/ph_ne10.json'))['geometry']['coordinates']
S = 2
mask = Image.new('L', (W * S, H * S), 0); d = ImageDraw.Draw(mask)
for poly in geo:
    ring = [tuple(c * S for c in P(lo, la)) for lo, la in poly[0]]
    if len(ring) > 2: d.polygon(ring, fill=255)
mask = mask.resize((W, H), Image.LANCZOS)
mk = np.asarray(mask).astype(np.float32)[..., None] / 255
if fill in ('red', 'flag'):
    shade = np.clip(.55 + 1.1 * (lum - lum.mean()) + .25, .45, 1.15)[..., None]
    if fill == 'red':
        col = np.array([.90, .08, .07])[None, None, :] * shade
    else:  # flag colours by latitude band: blue north, red south, white/yellow sun on Visayas
        bx0, by0 = P(116.9, 21.1); bx1, by1 = P(126.7, 4.6)
        X, Y = np.meshgrid(np.arange(W), np.arange(H)); u = (X - bx0) / (bx1 - bx0); v = (Y - by0) / (by1 - by0)
        top = (v < .5)[..., None]
        col = np.where(top, np.array([.0, .22, .66]), np.array([.81, .07, .15]))
        tri = (u < .5 * (1 - np.abs(v - .5) * 2))[..., None]
        col = np.where(tri, np.array([.97, .97, .97]), col)
        sun = (((u - .16) / .07) ** 2 + ((v - .5) / .045) ** 2 < 1)[..., None]
        col = np.where(sun, np.array([.99, .82, .09]), col) * shade
    res = res * (1 - mk) + np.clip(col, 0, 1) * mk
    if fill == 'flag':
        res_img = Image.fromarray((np.clip(res, 0, 1) * 255).astype(np.uint8))
    res_img = Image.fromarray((np.clip(res, 0, 1) * 255).astype(np.uint8))
    # white edge + dark halo
    edge = mask.filter(ImageFilter.MaxFilter(5)); halo = mask.filter(ImageFilter.MaxFilter(13)).filter(ImageFilter.GaussianBlur(6))
    hal = np.asarray(halo).astype(np.float32)[..., None] / 255 * (1 - np.asarray(edge).astype(np.float32)[..., None] / 255)
    ed = (np.asarray(edge).astype(np.float32) - np.asarray(mask).astype(np.float32))[..., None] / 255
    base = np.asarray(res_img).astype(np.float32) / 255
    base = base * (1 - .45 * hal)
    base = base * (1 - np.clip(ed, 0, 1)) + np.clip(ed, 0, 1)
    res_img = Image.fromarray((np.clip(base, 0, 1) * 255).astype(np.uint8))
if glow:
    tr = [(126.2, 14.6), (126.6, 13.0), (126.55, 11.5), (126.85, 10.0), (127.1, 8.5), (126.9, 7.0), (126.4, 5.6)]
    gl = Image.new('RGB', (W, H), (0, 0, 0)); gd = ImageDraw.Draw(gl)
    pts = [P(*p) for p in tr]
    for wdt, c in [(26, (255, 40, 0)), (14, (255, 120, 0)), (5, (255, 230, 140))]:
        gd.line(pts, fill=c, width=wdt, joint='curve')
    gl = gl.filter(ImageFilter.GaussianBlur(6))
    res_img = Image.fromarray(np.clip(np.asarray(res_img).astype(np.int32) + np.asarray(gl).astype(np.int32), 0, 255).astype(np.uint8))
res_img.save(out, quality=94)
proj = {'lonc': lonc, 'latc': latc, 'sc': sc, 'z': Z}
json.dump(proj, open(out[:-4] + '.json', 'w'))
