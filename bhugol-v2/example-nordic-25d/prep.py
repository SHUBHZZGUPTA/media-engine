# Nordic "what if" Short: map prep (orthographic world plate + vector overlays).
# Usage: python3 prep.py <fetch_dir_relief> <fetch_dir_context> <out_dir>
import json, os, sys, math
import numpy as np, cv2
from PIL import Image, ImageDraw
from shapely.geometry import shape, mapping, Polygon, MultiPolygon, LineString
from shapely.ops import unary_union, transform

RD, CD, OUT = sys.argv[1:4]
os.makedirs(OUT, exist_ok=True)
LAT0, LON0, R = 67.0, -8.0, 7000.0          # orthographic centre, sphere radius in world px (~0.91 km/px)
# world frame: X right, Y up (projected); world px: wx = X - X0, wy = Y1 - Y
CX0, CX1, CY0, CY1 = -3300.0, 3500.0, -4600.0, 4500.0   # context extent (projected)
DX0, DX1, DY0, DY1 = -2150.0, 2350.0, -1700.0, 2650.0   # detail extent
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
MID = load(os.path.join(CD, 'rb_mid.jpg'))                     # -110..90, 30..90
TBOX = {'rb_00': (-80, -17.5, 50, 68), 'rb_01a': (-80, -48.75, 68, 86), 'rb_01b': (-48.75, -17.5, 68, 86), 'rb_10': (-17.5, 45, 50, 68), 'rb_11': (-17.5, 45, 68, 86)}
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
    put(MID, -110, 90, 30, 90, (lon > -110) & (lon < 90) & (lat > 30))
    for k, (a, b, c, d) in TBOX.items():
        put(TL[k], a, b, c, d, (lon > a) & (lon < b) & (lat > c) & (lat < d))
    return out

def plate(x0, x1, y0, y1, w, h):
    X, Y = np.meshgrid(np.linspace(x0, x1, w), np.linspace(y1, y0, h))
    lon, lat = inv(X, Y)
    return sample(lon, lat), lon, lat

# ---------- vectors ----------
NE = json.load(open('/home/claude/nordic/ne/ne_10m_admin_0_countries.geojson'))
WANT = {'Denmark': 'DNK', 'Norway': 'NOR', 'Sweden': 'SWE', 'Finland': 'FIN', 'Iceland': 'ISL', 'Greenland': 'GRL', 'Faroe Islands': 'FRO', 'Aland': 'ALA'}
NEIGH = {'Russia': 'RUS', 'Estonia': 'EST', 'Germany': 'DEU', 'United Kingdom': 'GBR', 'Canada': 'CAN', 'Latvia': 'LVA', 'Ireland': 'IRL', 'Poland': 'POL', 'Lithuania': 'LTU', 'Netherlands': 'NLD', 'Belarus': 'BLR'}
G = {}
for f in NE['features']:
    a = f['properties']['ADMIN']
    if a in WANT or a in NEIGH: G[WANT.get(a) or NEIGH[a]] = shape(f['geometry'])
def pj(geom):
    def fn(x, y, z=None):
        X, Y = proj(np.asarray(x), np.asarray(y)); return X - CX0, CY1 - Y
    return transform(fn, geom)
PG = {k: pj(g).simplify(1.2, preserve_topology=True) for k, g in G.items()}
def path_d(geom, min_area=6):
    polys = [geom] if isinstance(geom, Polygon) else list(getattr(geom, 'geoms', []))
    out = []
    for p in polys:
        if p.area < min_area: continue
        for ring in [p.exterior] + list(p.interiors):
            c = np.asarray(ring.coords)
            out.append('M' + ' L'.join(f'{x:.0f},{y:.0f}' for x, y in c) + 'Z')
    return ''.join(out)
def line_d(geom):
    ls = [geom] if isinstance(geom, LineString) else [g for g in getattr(geom, 'geoms', []) if isinstance(g, LineString)]
    out = []
    for l in ls:
        c = np.asarray(l.coords)
        if len(c) < 2: continue
        out.append('M' + ' L'.join(f'{x:.0f},{y:.0f}' for x, y in c))
    return ''.join(out)
NORD = ['DNK', 'NOR', 'SWE', 'FIN', 'ISL', 'GRL', 'FRO', 'ALA']
union = unary_union([PG[k].buffer(0.6) for k in NORD]).buffer(-0.6)
# internal land borders (Norway-Sweden, Sweden-Finland, Norway-Finland): shared boundary segments
from shapely.ops import linemerge
def shared(a, b):
    i = PG[a].buffer(1.5).intersection(PG[b].buffer(1.5)).boundary.intersection(PG[a].buffer(0.1).boundary.buffer(3))
    return i
raw = {}
for a, b in (('NOR', 'SWE'), ('SWE', 'FIN'), ('NOR', 'FIN')):
    gi = G[a].boundary.intersection(G[b].buffer(0.01))   # geographic, then project
    raw[a + b] = line_d(pj(linemerge(gi) if gi.geom_type == 'MultiLineString' else gi).simplify(1.2))
bb = {k: [round(v, 1) for v in PG[k].bounds] for k in PG}
def main_poly(g): return g if isinstance(g, Polygon) else max(g.geoms, key=lambda p: p.area)
ANC = {}
for k in NORD:
    mp = main_poly(PG[k]); x0, y0, x1, y1 = mp.bounds; rp = mp.representative_point()
    ANC[k] = [round(rp.x, 1), round(rp.y, 1), round(x1 - x0, 1), round(y1 - y0, 1)]

PTS = {'copenhagen': (12.57, 55.68), 'stockholm': (18.07, 59.33), 'oslo': (10.75, 59.91), 'helsinki': (24.94, 60.17), 'reykjavik': (-21.94, 64.15),
       'kalmar': (16.36, 56.66), 'greenland': (-41.0, 73.5), 'nuuk': (-51.7, 64.18), 'norway_c': (12.5, 64.5), 'sweden_c': (16.0, 62.0), 'finland_c': (26.0, 63.0),
       'iceland_c': (-18.7, 64.95), 'denmark_c': (9.3, 56.1), 'center': (5.0, 64.5), 'scand': (16.0, 63.0), 'svalbard': (17.0, 78.5)}
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
    oc = np.clip((img - 128) * 1.08 + 128, 0, 255)               # ocean stays vivid
    return np.clip(land * (1 - ocean) + oc * ocean, 0, 255).astype(np.uint8)
Image.fromarray(grade(det, DX0 - CX0, CY1 - DY1, 1.0)).save(os.path.join(OUT, 'detail.jpg'), quality=88)
Image.fromarray(grade(ctx, 0, 0, cs)).save(os.path.join(OUT, 'context.jpg'), quality=88)

PP = json.load(open('/home/claude/nordic/ne/ne_10m_populated_places_simple.geojson'))
CITIES = []
for f in PP['features']:
    p = f['properties']
    if p.get('adm0_a3') in ('DNK', 'NOR', 'SWE', 'FIN', 'ISL', 'GRL', 'FRO', 'ALA') and (p.get('pop_max') or 0) > 20000:
        lo, la = f['geometry']['coordinates']; x, y = world(lo, la); r = 5 + min(16, (p['pop_max'] / 1e5) ** .5 * 5)
        CITIES.append([round(float(x), 1), round(float(y), 1), round(r, 1)])
M = {'cities': CITIES, 'W': W, 'H': H, 'detail': [DX0 - CX0, CY1 - DY1, dw, dh], 'context': [0, 0, W, H], 'R': R,
     'paths': {k: path_d(PG[k]) for k in NORD}, 'neigh': {k: path_d(PG[k], 40) for k in NEIGH if k in PG},
     'union': path_d(union), 'anchor': ANC, 'borders': raw, 'bbox': bb, 'pt': PT}
json.dump(M, open(os.path.join(OUT, 'map.json'), 'w'))
print('world', W, H, 'detail', dw, dh, 'context', cw, ch, {k: len(v) for k, v in M['paths'].items()}, {k: len(v) for k, v in raw.items()})
print(PT)
