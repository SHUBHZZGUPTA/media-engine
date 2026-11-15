# Iberia "what if" Short: map prep (orthographic world plate + vector overlays).
# Usage: python3 prep.py <fetch_dir_relief> <fetch_dir_context> <out_dir>
import json, os, sys, math
import numpy as np, cv2
from PIL import Image, ImageDraw
from shapely.geometry import shape, mapping, Polygon, MultiPolygon, LineString
from shapely.ops import unary_union, transform

RD, CD, OUT = sys.argv[1:4]
os.makedirs(OUT, exist_ok=True)
LAT0, LON0, R = 40.0, -4.0, 12000.0          # orthographic centre, sphere radius in world px (~0.53 km/px)
# world frame: X right, Y up (projected); world px: wx = X - X0, wy = Y1 - Y
CX0, CX1, CY0, CY1 = -4500.0, 4500.0, -7000.0, 7000.0   # context extent (projected)
DX0, DX1, DY0, DY1 = -2300.0, 2500.0, -1500.0, 1500.0   # detail extent
W, H = CX1 - CX0, CY1 - CY0
p0, l0 = math.radians(LAT0), math.radians(LON0)

def proj(lon, lat):
    p, l = np.radians(lat), np.radians(lon)
    x = R * np.cos(p) * np.sin(l - l0)
    y = R * (math.cos(p0) * np.sin(p) - math.sin(p0) * np.cos(p) * np.cos(l - l0))
    return x, y
def world(lon, lat):
    x, y = proj(lon, lat); return x - CX0, CY1 - y
def inv(X, Y):  # projected -> lon, lat (orthographic inverse)
    rho = np.hypot(X, Y); c = np.arcsin(np.clip(rho / R, -1, 1))
    lat = np.arcsin(np.cos(c) * math.sin(p0) + np.where(rho > 0, Y * np.sin(c) * math.cos(p0) / np.maximum(rho, 1e-9), 0))
    lon = l0 + np.arctan2(X * np.sin(c), rho * np.cos(c) * math.cos(p0) - Y * np.sin(c) * math.sin(p0))
    return np.degrees(lon), np.degrees(lat)

# ---------- imagery ----------
def load(p): return cv2.cvtColor(cv2.imread(p, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB).astype(np.float32)
GL = load(os.path.join(CD, 'rb_global.jpg'))                  # -180..180, -90..90
MID = load(os.path.join(RD, 'rb_mid.jpg'))                     # -35..35, 15..65
TBOX = {'rb_00': (-12, -3, 34, 40), 'rb_01': (-12, -3, 40, 46), 'rb_10': (-3, 6, 34, 40), 'rb_11': (-3, 6, 40, 46)}
TL = {k: load(os.path.join(RD, k + '.jpg')) for k in TBOX}

def sample(lon, lat):
    lon = (lon + 180) % 360 - 180
    out = np.zeros(lon.shape + (3,), np.float32)
    def put(img, lo0, lo1, la0, la1, m):
        h, w = img.shape[:2]
        u = ((lon - lo0) / (lo1 - lo0) * w - .5).astype(np.float32); v = ((la1 - lat) / (la1 - la0) * h - .5).astype(np.float32)
        s = cv2.remap(img, u, v, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        out[m] = s[m]
    put(GL, -180, 180, -90, 90, np.ones(lon.shape, bool))
    put(MID, -35, 35, 15, 65, (lon > -35) & (lon < 35) & (lat > 15) & (lat < 65))
    for k, (a, b, c, d) in TBOX.items():
        put(TL[k], a, b, c, d, (lon > a) & (lon < b) & (lat > c) & (lat < d))
    return out

def plate(x0, x1, y0, y1, w, h):
    X, Y = np.meshgrid(np.linspace(x0, x1, w, dtype=np.float32), np.linspace(y1, y0, h, dtype=np.float32))
    lon, lat = inv(X, Y)
    img = sample(lon, lat); rho = np.hypot(X, Y); del X, Y
    if rho.max() <= R * .98: return img, lon, lat
    # beyond the limb: deep space + a soft blue atmosphere glow
    edge = np.clip((rho - R) / (R * .06), 0, 1)[..., None]
    glow = np.exp(-np.clip(rho - R, 0, None) / (R * .035))[..., None]
    space = np.array([6, 10, 24], np.float32) + glow * np.array([70, 140, 255], np.float32) * .85
    inside = (rho <= R)[..., None]
    rim = np.clip(1 - (R - rho) / (R * .02), 0, 1)[..., None] * inside   # thin bright rim inside the limb
    img = img * inside + space * (1 - inside)
    img = img * (1 - rim * .35) + np.array([120, 180, 255], np.float32) * rim * .35
    return img, lon, lat

# ---------- vectors ----------
NE = json.load(open('/home/claude/nordic/ne/ne_10m_admin_0_countries.geojson'))
WANT = {'Spain': 'ESP', 'Portugal': 'PRT'}
NEIGH = {'France': 'FRA', 'Morocco': 'MAR', 'Andorra': 'AND', 'Algeria': 'DZA', 'Gibraltar': 'GIB'}
G = {}
for f in NE['features']:
    a = f['properties']['ADMIN']
    if a in WANT or a in NEIGH: G[WANT.get(a) or NEIGH[a]] = shape(f['geometry'])
def pj(geom):
    def fn(x, y, z=None):
        X, Y = proj(np.asarray(x), np.asarray(y)); return X - CX0, CY1 - Y
    return transform(fn, geom)
from shapely.geometry import box as _box
NORD0 = ('ESP', 'PRT')
for _c in ('ESP', 'PRT'):   # detailed borders (geoBoundaries gbOpen ADM0) instead of Natural Earth 10m
    _g = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gb', f'gb_{_c}.geojson')))
    G[_c] = unary_union([shape(f['geometry']) for f in _g['features']]).buffer(0)
G['ESP'] = G['ESP'].intersection(_box(-10, 36.0, 4.6, 44)); G['PRT'] = G['PRT'].intersection(_box(-9.7, 36.9, -6.0, 42.2)); G['FRA'] = G['FRA'].intersection(_box(-6, 41, 10, 52))
PG = {k: pj(g).simplify(1.2 if k not in NORD0 else .6, preserve_topology=True) for k, g in G.items()}
def chaikin(c, n=2, closed=True):
    c = np.asarray(c, float)
    for _ in range(n):
        if closed: a, b = c, np.roll(c, -1, 0)
        else: a, b = c[:-1], c[1:]
        q, r = .75 * a + .25 * b, .25 * a + .75 * b
        m = np.empty((len(q) * 2, 2)); m[0::2], m[1::2] = q, r
        c = m if closed else np.vstack([c[:1], m, c[-1:]])
    return c
def path_d(geom, min_area=6):
    polys = [geom] if isinstance(geom, Polygon) else list(getattr(geom, 'geoms', []))
    out = []
    for p in polys:
        if p.area < min_area: continue
        for ring in [p.exterior] + list(p.interiors):
            c = chaikin(np.asarray(ring.coords)[:-1])
            out.append('M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in c) + 'Z')
    return ''.join(out)
def line_d(geom):
    ls = [geom] if isinstance(geom, LineString) else [g for g in getattr(geom, 'geoms', []) if isinstance(g, LineString)]
    out = []
    for l in ls:
        c = np.asarray(l.coords)
        if len(c) < 2: continue
        c = chaikin(c, 2, False)
        out.append('M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in c))
    return ''.join(out)
NORD = ['ESP', 'PRT']
union = unary_union([PG[k].buffer(0.6) for k in NORD]).buffer(-0.6).simplify(.8, preserve_topology=True)
# internal land borders (Norway-Sweden, Sweden-Finland, Norway-Finland): shared boundary segments
from shapely.ops import linemerge
def shared(a, b):
    i = PG[a].buffer(1.5).intersection(PG[b].buffer(1.5)).boundary.intersection(PG[a].buffer(0.1).boundary.buffer(3))
    return i
bord = G['ESP'].boundary.intersection(G['PRT'].buffer(0.03))
raw = {'states': line_d(pj(bord).simplify(.6))}
STC = {}
bb = {k: [round(v, 1) for v in PG[k].bounds] for k in PG}
def main_poly(g): return g if isinstance(g, Polygon) else max(g.geoms, key=lambda p: p.area)
ANC = {}
for k in NORD:
    mp = main_poly(PG[k]); x0, y0, x1, y1 = mp.bounds; rp = mp.representative_point()
    ANC[k] = [round(rp.x, 1), round(rp.y, 1), round(x1 - x0, 1), round(y1 - y0, 1)]

PTS = {'madrid': (-3.70, 40.42), 'lisbon': (-9.14, 38.72), 'porto': (-8.61, 41.15), 'barcelona': (2.17, 41.39), 'seville': (-5.98, 37.39), 'valencia': (-0.38, 39.47),
       'badajoz': (-6.97, 38.88), 'elvas': (-7.16, 38.88), 'border': (-7.05, 38.9), 'es_c': (-3.6, 40.1), 'pt_c': (-8.1, 39.7), 'center': (-4.0, 40.0), 'atl': (-11.5, 39.5)}
PT = {k: [round(float(v), 1) for v in world(*ll)] for k, ll in PTS.items()}

# ---------- plates ----------
dw, dh = int(DX1 - DX0), int(DY1 - DY0)
det, lon, lat = plate(DX0, DX1, DY0, DY1, dw, dh)
cs = 3.0
cw, ch = int(W / cs), int(H / cs)
ctx, clon, clat = plate(CX0, CX1, CY0, CY1, cw, ch)

def mask_for(keys, x0, y0, sc, w, h):
    im = Image.new('L', (w, h), 0); d = ImageDraw.Draw(im)
    for k in keys:
        g = PG[k]; polys = [g] if isinstance(g, Polygon) else list(g.geoms)
        for p in polys:
            d.polygon([((x - x0) / sc, (y - y0) / sc) for x, y in p.exterior.coords], fill=255)
            for ri in p.interiors: d.polygon([((x - x0) / sc, (y - y0) / sc) for x, y in ri.coords], fill=0)
    return np.asarray(im, np.float32) / 255.
def grade(img, x0, y0, sc):
    h, w = img.shape[:2]
    nord = cv2.GaussianBlur(mask_for(NORD, x0, y0, sc, w, h), (0, 0), 2.0 / sc + .6)[..., None]
    # land vs ocean from the bathymetry colours (ocean is blue-dominant)
    r, g, b = img[..., 0], img[..., 1], img[..., 2]
    ocean = np.clip((b - np.maximum(r, g) - 8) / 30, 0, 1)[..., None]
    lum = img.mean(2, keepdims=True)
    other = (img * .78 + lum * .22) * .72                         # neighbours: a little darker + less saturated
    nordc = np.clip((img - 128) * 1.12 + 128 + 10, 0, 255)       # Nordic land: a touch brighter/punchier
    land = other * (1 - nord) + nordc * nord
    oc = np.clip((img - 128) * 1.08 + 128 + 14, 0, 255) * 1.06   # ocean lifted + vivid
    return np.clip(land * (1 - ocean) + oc * ocean, 0, 255).astype(np.uint8)
Image.fromarray(grade(det, DX0 - CX0, CY1 - DY1, 1.0)).save(os.path.join(OUT, 'detail.jpg'), quality=88)
Image.fromarray(grade(ctx, 0, 0, cs)).save(os.path.join(OUT, 'context.jpg'), quality=88)

PP = json.load(open('/home/claude/nordic/ne/ne_10m_populated_places_simple.geojson'))
CITIES = []
for f in PP['features']:
    p = f['properties']
    if p.get('adm0_a3') in ('ESP', 'PRT') and (p.get('pop_max') or 0) > 40000 and f['geometry']['coordinates'][1] > 36 and f['geometry']['coordinates'][0] > -10:
        lo, la = f['geometry']['coordinates']; x, y = world(lo, la); r = 5 + min(16, (p['pop_max'] / 1e5) ** .5 * 5)
        CITIES.append([round(float(x), 1), round(float(y), 1), round(r, 1)])
M = {'cities': CITIES, 'W': W, 'H': H, 'detail': [DX0 - CX0, CY1 - DY1, dw, dh], 'context': [0, 0, W, H], 'R': R,
     'paths': {k: path_d(PG[k]) for k in NORD}, 'neigh': {k: path_d(PG[k], 40) for k in NEIGH if k in PG},
     'union': path_d(union), 'anchor': ANC, 'stc': STC, 'borders': raw, 'bbox': bb, 'pt': PT}
json.dump(M, open(os.path.join(OUT, 'map.json'), 'w'))
print('world', W, H, 'detail', dw, dh, 'context', cw, ch, {k: len(v) for k, v in M['paths'].items()}, {k: len(v) for k, v in raw.items()})
print(PT)
