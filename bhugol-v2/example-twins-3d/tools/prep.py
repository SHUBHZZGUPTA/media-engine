# Geo assets for the same-size countries Short: per-scene country masks + baked flag fills, a flag-painted globe,
# overlay rings (true size, moved), the Zambia->Chile morph rings, and SVG character paths.
import json, math, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
W = '/home/claude/work/twins/'; A = W + 'art/'; FL = W + 'flags/'
NM = '/home/claude/hf/node_modules/flag-icons/flags/4x3/'
C = json.load(open(W + 'ne/ne_50m_admin_0_countries.geojson'))
ISO = {'NP': 'Nepal', 'BD': 'Bangladesh', 'GN': 'Guinea', 'GB': 'United Kingdom', 'CL': 'Chile', 'ZM': 'Zambia', 'IT': 'Italy', 'PH': 'Philippines', 'MY': 'Malaysia', 'VN': 'Vietnam'}
def polys(name):
    for f in C['features']:
        if f['properties'].get('ADMIN') == name:
            g = f['geometry']; P = [g['coordinates']] if g['type'] == 'Polygon' else g['coordinates']; return [p[0] for p in P]
    raise SystemExit('missing ' + name)
def area_km(r):
    la = sum(p[1] for p in r) / len(r); k = math.cos(math.radians(la))
    pts = [(p[0] * 111.32 * k, p[1] * 110.57) for p in r]; return abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]))) / 2
def thin(r, d=.04):
    out = [r[0][:2]]
    for c in r[1:]:
        if math.hypot(c[0] - out[-1][0], c[1] - out[-1][1]) > d: out.append(c[:2])
    if len(out) > 3 and out[0] == out[-1]: out = out[:-1]
    return out
G = {}
for iso, nm in ISO.items():
    P = sorted(polys(nm), key=area_km, reverse=True); big = area_km(P[0])
    G[iso] = [thin(p) for p in P if area_km(p) > max(big * .004, 150)]
    print(iso, len(P), '->', len(G[iso]), 'rings; total km2', round(sum(area_km(p) for p in P)))
# ---- flags (raster, from flag-icons SVG) ----
os.makedirs(FL, exist_ok=True)
for iso in ISO:
    subprocess.run(['rsvg-convert', '-w', '1200', '-h', '900', NM + iso.lower() + '.svg', '-o', FL + iso + '.png'], check=True)
np_im = Image.open(FL + 'NP.png').convert('RGBA'); bg = Image.new('RGBA', np_im.size, (220, 20, 60, 255)); bg.alpha_composite(np_im); bg.convert('RGB').save(FL + 'NP.png')
def flag(iso): return Image.open(FL + iso + '.png').convert('RGB')
def centroid(rings):
    sx = sy = sa = 0
    for r in rings:
        a = area_km(r); sx += a * sum(p[0] for p in r) / len(r); sy += a * sum(p[1] for p in r) / len(r); sa += a
    return sx / sa, sy / sa
def km(rings, c):
    lo, la = c; k = math.cos(math.radians(la)); return [[((p[0] - lo) * 111.32 * k, (p[1] - la) * 110.57) for p in r] for r in rings]
def place(kmr, lon, lat, rot=0):
    k = math.cos(math.radians(lat)); c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    return [[[lon + (x * c - y * s) / (111.32 * k), lat + (x * s + y * c) / 110.57] for x, y in r] for r in kmr]
def moved(iso, lon, lat, rot=0): return place(km(G[iso], centroid(G[iso])), lon, lat, rot)
# ---- per-scene masks + flag fills ----
SC = {'sa': ['NP', 'BD'], 'wa': ['GN'], 'zc': ['ZM'], 'it': ['IT'], 'sea': ['MY', 'VN']}
def paint(img_size, bbox, isos, base=None, alpha=1.0, edge=True):
    L0, L1, B0, B1 = bbox; Wd, Hd = img_size
    pt = lambda lo, la: ((lo - L0) / (L1 - L0) * Wd, (B1 - la) / (B1 - B0) * Hd)
    out = base.copy() if base else Image.new('RGB', img_size, (0, 0, 0)); mask = Image.new('L', img_size, 0); md = ImageDraw.Draw(mask)
    for k, iso in enumerate(isos):
        m = Image.new('L', img_size, 0); d = ImageDraw.Draw(m)
        for r in G[iso]: d.polygon([pt(*c) for c in r], fill=255)
        allp = [c for r in G[iso] for c in r]; xs = [pt(*c)[0] for c in allp]; ys = [pt(*c)[1] for c in allp]
        x0, x1, y0, y1 = int(min(xs)), int(max(xs)) + 1, int(min(ys)), int(max(ys)) + 1
        f = flag(iso).resize((max(2, x1 - x0), max(2, y1 - y0)), Image.LANCZOS); lay = Image.new('RGB', img_size); lay.paste(f, (x0, y0))
        a = m.point(lambda v: int(v * alpha)); out.paste(lay, (0, 0), a)
        if edge:
            e = m.filter(ImageFilter.MaxFilter(5)); e = Image.fromarray(np.clip(np.asarray(e, np.int16) - np.asarray(m, np.int16), 0, 255).astype(np.uint8))
            out.paste((255, 255, 255), (0, 0), e)
        for r in G[iso]: md.polygon([pt(*c) for c in r], fill=40 * (k + 1))
    return out, mask
for s, isos in SC.items():
    m3 = json.load(open(A + s + '/map3d.json')); bbox = m3['bbox']; L0, L1, B0, B1 = bbox
    Wd = 4096; Hd = int(4096 * (B1 - B0) / (L1 - L0)) // 2 * 2
    fills, mask = paint((Wd, Hd), bbox, isos, edge=False); fills.save(A + s + '/flags.jpg', quality=92); mask.save(A + s + '/pa_mask.png')
    m3['pa'] = max(G[isos[0]], key=len); m3['outline'] = m3['pa']; json.dump(m3, open(A + s + '/map3d.json', 'w'))
# ---- globe with all 10 flags ----
gl = Image.open(A + 'sa/globe.jpg').convert('RGB'); print('globe', gl.size)
gfl, _ = paint(gl.size, [-180, 180, -90, 90], list(ISO), base=gl, alpha=.92, edge=True); gfl.save(A + 'globe_flags.jpg', quality=93)
# ---- overlays / morph ----
zc = centroid(G['ZM'])
def resample(r, n=320):
    pts = np.array(r + [r[0]], float); seg = np.hypot(*np.diff(pts, axis=0).T); L = np.concatenate([[0], np.cumsum(seg)])
    s = np.linspace(0, L[-1], n, endpoint=False); x = np.interp(s, L, pts[:, 0]); y = np.interp(s, L, pts[:, 1]); return np.stack([x, y], 1)
def orient_start(a):
    sa = np.sum(a[:, 0] * np.roll(a[:, 1], -1) - np.roll(a[:, 0], -1) * a[:, 1])
    if sa < 0: a = a[::-1]
    i = int(np.argmax(a[:, 1])); return np.roll(a, -i, axis=0)
zm_main = max(G['ZM'], key=len); cl_main = max(G['CL'], key=lambda r: area_km(r))
cl_on_zm = place(km([cl_main], centroid([cl_main])), zc[0], zc[1])[0]
ma = orient_start(resample(zm_main)); mb = orient_start(resample(cl_on_zm))
GEO = {'rings': G,
       'gb_on_gn': moved('GB', *centroid(G['GN'])),
       'cl_side': moved('CL', 12.5, zc[1]),          # real Chile at true size, parked off Africa's west coast
       'morph_a': ma.round(4).tolist(), 'morph_b': mb.round(4).tolist(),
       'ph_side': moved('PH', 31.0, 52.0),           # Philippines parked east of Italy
       'ph_top': moved('PH', 12.4, 54.0, -12),       # Philippines sitting on top of Italy (the body)
       'my_up': moved('MY', 104.8, 6.6, 0),
       'cent': {k: centroid(v) for k, v in G.items()}}
json.dump(GEO, open(A + 'geo.json', 'w'))
# ---- character outlines (SVG path in a 600x600 box) ----
def svgpath(rings, keep=6):
    rings = sorted(rings, key=area_km, reverse=True)[:keep]; c = centroid(rings); K = km(rings, c)
    xs = [x for r in K for x, y in r]; ys = [y for r in K for x, y in r]; s = 520 / max(max(xs) - min(xs), max(ys) - min(ys))
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    return ' '.join('M' + ' L'.join(f'{300 + (x - cx) * s:.1f},{300 - (y - cy) * s:.1f}' for x, y in r) + 'Z' for r in K)
json.dump({'gb': svgpath(G['GB'], 2), 'my': svgpath(G['MY'], 2), 'vn': svgpath(G['VN'], 1)}, open(A + 'shapes.json', 'w'))
print('ok')
