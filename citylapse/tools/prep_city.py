"""Turn fetched OSM + terrain data into compact scene data for a city timelapse.

Usage: python3 prep_city.py <city.json> <fetch_dir> [<fetch_dir2> ...] <out_dir>
city.json holds the bbox, the local origin, era zones (where buildings get their approximate birth years),
hero landmarks, reclaimed-land overrides and the camera framing. Writes into <out_dir>:
  land.png   R = land code (0 always land, 1..254 reclaimed in year 1900+v/2, 255 sea), G = 255 old town, 1..254 water dug in year 1900+v/2 (land before)
  bld.bin    float32 records [x, z, w, d, rot, h, birth, grow_years] per building (metres, local frame, x east, z south)
  scene.json bbox/extent/landmarks/stats
Building birth years come from era zones (approximate, documented in city.json) unless OSM has start_date.
"""
import json, math, os, sys, glob, random
import numpy as np
from PIL import Image, ImageDraw

cfg = json.load(open(sys.argv[1])); dirs = sys.argv[2:-1]; out = sys.argv[-1]; os.makedirs(out, exist_ok=True)
S, N, W, E = cfg['bbox']; LAT0, LON0 = cfg['origin']
KX = 111320 * math.cos(math.radians(LAT0)); KZ = 110540
def loc(lon, lat): return ((lon - LON0) * KX, (LAT0 - lat) * KZ)          # x east, z south (metres)
X0, Z0 = loc(W, N); X1, Z1 = loc(E, S)
RES = cfg.get('land_res', 8.0)                                             # metres per land pixel
LW, LH = int((X1 - X0) / RES), int((Z1 - Z0) / RES)
def pix(x, z): return ((x - X0) / RES, (z - Z0) / RES)
rnd = random.Random(7)

def files(pat):
    seen = {}
    for d in dirs:
        for f in glob.glob(os.path.join(d, pat)): seen.setdefault(os.path.basename(f), f)   # first dir wins
    return list(seen.values())

# ---------- land: current coast (OSM) flood-filled, old coast from terrain (SRTM ~2000) ----------
bar = Image.new('L', (LW, LH), 0); db = ImageDraw.Draw(bar)
for f in files('coast.json'):
    for w in json.load(open(f))['elements']:
        pts = [pix(*loc(p['lon'], p['lat'])) for p in w.get('geometry', [])]
        if len(pts) > 1: db.line(pts, fill=255, width=3)
def flood(barrier, seeds):
    from collections import deque
    H, Wd = barrier.shape; seen = np.zeros_like(barrier, bool); q = deque()
    for sx, sy in seeds:
        if not barrier[sy, sx]: seen[sy, sx] = True; q.append((sx, sy))
    while q:
        x, y = q.popleft()
        for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if 0 <= nx < Wd and 0 <= ny < H and not seen[ny, nx] and not barrier[ny, nx]: seen[ny, nx] = True; q.append((nx, ny))
    return seen
B = np.asarray(bar) > 0
seeds = [tuple(int(v) for v in pix(*loc(*s))) for s in cfg['sea_seeds']]
sea_now = flood(B, seeds); sea_now |= B & np.roll(sea_now, 2, 0)   # barrier pixels next to sea count as sea

# terrain mosaic (terrarium) -> elevation sampled on the land grid
dem = {}
for f in files('dem_*.png'):
    z, x, y = map(int, os.path.basename(f)[4:-4].split('_')); dem[(x, y)] = f
zoom = next(iter(dem))[0] if False else int(os.path.basename(files('dem_*.png')[0]).split('_')[1])
xs = sorted({k[0] for k in dem}); ys = sorted({k[1] for k in dem})
mos = np.full((256 * len(ys), 256 * len(xs)), -50.0)
for (x, y), f in dem.items():
    a = np.asarray(Image.open(f).convert('RGB')).astype(float)
    mos[(y - ys[0]) * 256:(y - ys[0] + 1) * 256, (x - xs[0]) * 256:(x - xs[0] + 1) * 256] = a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768
gx, gz = np.meshgrid(np.arange(LW) * RES + X0 + RES / 2, np.arange(LH) * RES + Z0 + RES / 2)
lon = gx / KX + LON0; lat = LAT0 - gz / KZ; n2 = 2 ** zoom
tx = (lon + 180) / 360 * n2; ty = (1 - np.arcsinh(np.tan(np.radians(lat))) / math.pi) / 2 * n2
px_ = np.clip(((tx - xs[0]) * 256).astype(int), 0, mos.shape[1] - 1); py_ = np.clip(((ty - ys[0]) * 256).astype(int), 0, mos.shape[0] - 1)
elev = mos[py_, px_]
low = elev <= cfg.get('sea_level_m', 0.5)
sea_old = flood(~low, seeds)                                  # sea in ~2000 = low ground connected to open sea
land_now = ~sea_now
code = np.full((LH, LW), 255, np.uint8); code[land_now] = 0
recl = land_now & sea_old                                     # land today that was sea in the old survey
yr = np.full((LH, LW), cfg.get('default_reclaim_year', 2004), float)
for r in cfg.get('reclaim', []):                              # named reclaimed areas get their own year
    x, z = loc(r['lon'], r['lat']); cx, cy = pix(x, z); rr = r['r_km'] * 1000 / RES
    m = (np.hypot(np.arange(LW)[None, :] - cx, np.arange(LH)[:, None] - cy) < rr); yr[m] = r['year']
    if r.get('force'): recl |= m & land_now
code[recl] = np.clip((yr[recl] - 1900) * 2, 1, 254).astype(np.uint8)
old = np.zeros((LH, LW), np.uint8)
for o in cfg.get('old_town', []):
    x, z = loc(o['lon'], o['lat']); cx, cy = pix(x, z); rr = o['r_km'] * 1000 / RES
    old[(np.hypot(np.arange(LW)[None, :] - cx, np.arange(LH)[:, None] - cy) < rr) & land_now] = 255
for dg in cfg.get('dug', []):                                 # water dug later (canals): land before that year
    lo0, lo1, la0, la1 = dg['box']
    m = sea_now & (lon >= lo0) & (lon < lo1) & (lat >= la0) & (lat < la1)
    old[m] = np.uint8(min(254, max(1, (dg['year'] - 1900) * 2)))
el8 = np.clip(elev * 2, 0, 255).astype(np.uint8)
Image.fromarray(np.dstack([code, old, el8])).save(os.path.join(out, 'land.png'))

# ---------- buildings ----------
zones = cfg['zones']
def zone_for(lon, lat):
    best = None
    for zn in zones:
        d = math.hypot((lon - zn['lon']) * KX, (lat - zn['lat']) * KZ) / 1000
        if d <= zn['r_km'] and (best is None or zn['r_km'] < best[1]['r_km']): best = (d, zn)
    return best
cre = cfg['spread_from']; recs = []; seen = set()
for f in files('bld_*.json'):
    for b in json.load(open(f))['elements']:
        if b['id'] in seen: continue
        seen.add(b['id']); c = np.array(b['geometry']['coordinates'])
        if len(c) < 4: continue
        P = np.array([loc(*p) for p in c[:-1]])
        # minimum-area rectangle over hull edges (good enough for diorama boxes)
        best = None
        for i in range(len(P)):
            e = P[(i + 1) % len(P)] - P[i]; L = np.hypot(*e)
            if L < 0.5: continue
            u = e / L; v = np.array([-u[1], u[0]]); a = P @ u; bb = P @ v
            A = (a.max() - a.min()) * (bb.max() - bb.min())
            if best is None or A < best[0]: best = (A, u, v, a, bb)
        if best is None: continue
        A, u, v, a, bb = best; w_ = a.max() - a.min(); d_ = bb.max() - bb.min()
        if w_ * d_ < 12: continue
        ctr = u * (a.max() + a.min()) / 2 + v * (bb.max() + bb.min()) / 2; rot = math.atan2(u[1], u[0])
        lo, la = c[:, 0].mean(), c[:, 1].mean(); t = b['tags']; kind = t.get('b', 'yes')
        zb = zone_for(lo, la); zn = zb[1] if zb else None
        # birth year
        sd = t.get('sd', '')[:4]
        if sd.isdigit() and 1700 < int(sd) < 2027: birth = int(sd) + rnd.uniform(0, .9)
        elif zn: birth = rnd.uniform(*zn['years'])
        else:
            dk = math.hypot((lo - cre['lon']) * KX, (la - cre['lat']) * KZ) / 1000
            birth = min(2023, cre['y0'] + cre['per_km'] * dk + rnd.gauss(0, 3))
        # height
        if t.get('h', '').replace('.', '', 1).isdigit(): h = float(t['h'])
        elif t.get('l', '').isdigit(): h = int(t['l']) * 3.4 + 2
        elif kind in ('house', 'detached', 'terrace', 'semidetached_house', 'carport', 'roof', 'hut', 'shed', 'garage'): h = rnd.uniform(4, 8)
        elif zn and zn.get('tower') and w_ * d_ > 500: h = rnd.uniform(*zn['tower'])
        else: h = rnd.uniform(*(zn.get('low', [5, 14]) if zn else [5, 14]))
        if birth < 1950: h = min(h, rnd.uniform(3.5, 7))
        recs.append([ctr[0], ctr[1], w_, d_, rot, h, birth, 0.8 if birth < 1960 else 1.2])
for lm in cfg.get('heroes', []):                              # landmark hero buildings (exact heights)
    x, z = loc(lm['lon'], lm['lat']); recs.append([x, z, lm['w'], lm['d'], lm.get('rot', 0), lm['h'], lm['year'], lm.get('grow', 1)])
R = np.array(recs, np.float32); R.tofile(os.path.join(out, 'bld.bin'))
# ---------- roads: raster with birth year (same era logic as buildings, a little earlier) ----------
WID = {'motorway': 5, 'trunk': 4, 'primary': 3, 'secondary': 2}
rimg = Image.new('L', (LW, LH), 0); dr = ImageDraw.Draw(rimg); nr = 0
for f in files('roads.json'):
    for w in json.load(open(f))['elements']:
        g = w.get('geometry'); t = w.get('tags', {})
        if not g: continue
        lo = sum(p['lon'] for p in g) / len(g); la = sum(p['lat'] for p in g) / len(g); zb = zone_for(lo, la)
        if zb: by = zb[1]['years'][0] - 1 + rnd.uniform(0, 3)
        else: by = min(2020, cre['y0'] + cre['per_km'] * math.hypot((lo - cre['lon']) * KX, (la - cre['lat']) * KZ) / 1000 - 3)
        by = max(by, cfg.get('roads_from', 1955))
        code_r = int(np.clip((by - 1900) * 2, 1, 254))
        dr.line([pix(*loc(p['lon'], p['lat'])) for p in g], fill=code_r, width=WID.get(t.get('highway'), 2)); nr += 1
rimg.save(os.path.join(out, 'roads.png'))
lms = []
for lm in cfg.get('labels', []):
    x, z = loc(lm['lon'], lm['lat']); lms.append({**lm, 'x': x, 'z': z})
json.dump({'extent': [X0, Z0, X1, Z1], 'land_res': RES, 'land_size': [LW, LH], 'n_bld': len(R), 'labels': lms, 'coast_line': cfg.get('coast_line'), 'inland_point': cfg.get('inland_point'),
           'origin': cfg['origin']}, open(os.path.join(out, 'scene.json'), 'w'), indent=1)
print('roads', nr, 'buildings', len(R), 'land', LW, LH, 'reclaimed px', int(recl.sum()), 'births', np.percentile(R[:, 6], [5, 50, 95]).round())
