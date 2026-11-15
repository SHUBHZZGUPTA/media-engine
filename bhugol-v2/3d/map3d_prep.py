"""3D satellite-terrain map assets for a BHUGOL v2 flyover (globe -> region terrain -> glowing border + pin).

Step 1, write the fetch job (NASA GIBS imagery + AWS Terrarium elevation tiles), then push it:
  python3 map3d_prep.py job <id> <lon0> <lon1> <lat0> <lat1> --close lon0,lon1,lat0,lat1
    bbox = the regional terrain (about 12 x 6 degrees around the subject works well)
    --close = a smaller patch inside it that gets sharper Landsat imagery (where the camera ends up)
  Better (15 Nov 2026): size the sharp patch from the camera, not by eye. Build the video once, run
    NODE_PATH=<hf>/node_modules node footprint.cjs <build_dir> fp.json
  then  python3 map3d_prep.py job <id> ... --footprint fp.json --map mp/
  which takes the patch from fp.json zones.lt300 (every frame that needs finer than 300 m per screen pixel, +15%),
  picks the pixel size from the closest frame (mpp_min; Landsat floor ~30 m) and splits it into <=4096 px WMS tiles.
  --patch-only writes a fetch job with just those tiles (to re-sharpen a map that was already built).
  map3d_prep.py patch <fetch_dir> <art_dir> [--land-only ne_10m_admin_0_countries.geojson]: stitch + colour-match; --land-only
  blacks out water so turbid seas (Channel, North Sea, deltas) don't show Landsat swath seams; the sea comes from the regional plate.
Step 2, after outputs/fetch/<id>/ arrives, build the assets:
  python3 map3d_prep.py build outputs/fetch/<id> <art_dir> --admin1 "Pennsylvania" --pin -76.343,40.804
    or --admin0 "Hungary" for a country outline (Natural Earth 50m, fetched from raw.githubusercontent.com)
Writes into <art_dir>: globe.jpg, ne.jpg (regional, graded), pa_close.jpg (colour-matched patch), dem.png (16-bit),
dem8.png (vertex heights), hillshade.png, pa_mask.png (region mask), map3d.json {bbox, outline, pin, pa_close_bbox}.
"""
import argparse, glob, json, math, os, sys, urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

GIBS = 'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?SERVICE=WMS&REQUEST=GetMap&VERSION=1.3.0&CRS=EPSG:4326&FORMAT=image/jpeg&STYLES='
NE = 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/'


def patch_tiles(c, mpp_min=None, prefix='pa_t'):
    """WMS tiles (<= 4096 px each) for the sharp Landsat patch c = [lon0, lon1, lat0, lat1]; both sides <= 8192 (WebGL-safe)."""
    w_m = (c[1] - c[0]) * 111320 * math.cos(math.radians((c[2] + c[3]) / 2)); h_m = (c[3] - c[2]) * 110540
    target = max(30.0, .6 * mpp_min) if mpp_min else 35.0; W = min(8192, int(8192 * w_m / h_m), max(2048, int(w_m / target)))   # both sides <= 8192 (WebGL)   # 0.6: headroom for frames between samples
    if w_m / W > target * 1.05: print(f'WARNING: patch needs {target:.0f} m/px but 8192 px gives {w_m / W:.0f} m/px: narrow it, split the map, or use Sentinel-2 cloudless 2016 (10 m, CC BY 4.0, credit EOX)')
    H = int(W * h_m / w_m); nx, ny = math.ceil(W / 4096), math.ceil(H / 4096); f = []
    for r in range(ny):
        for k in range(nx):
            l0 = c[0] + (c[1] - c[0]) * k / nx; l1 = c[0] + (c[1] - c[0]) * (k + 1) / nx; b1 = c[3] - (c[3] - c[2]) * r / ny; b0 = c[3] - (c[3] - c[2]) * (r + 1) / ny
            f.append({'name': f'{prefix}_{r}{k}.jpg', 'url': GIBS + f'&LAYERS=Landsat_WELD_CorrectedReflectance_TrueColor_Global_Annual&BBOX={b0},{l0},{b1},{l1}&WIDTH={W // nx}&HEIGHT={H // ny}'})
    print(f'sharp patch {c}: {W}x{H} px = {w_m / W:.0f} m/px in {ny}x{nx} tiles')
    return f, [ny, nx]


def job(a):
    L0, L1, B0, B1 = a.lon0, a.lon1, a.lat0, a.lat1; mpp = None
    if a.footprint:
        fp = json.load(open(a.footprint))[a.map]; c = fp['patch'] or fp['bbox']; mpp = fp['mpp_min']
        if fp.get('horizon'): print('note: a shot shows the horizon; the far field uses the globe/regional plates')
    else:
        c = [float(x) for x in a.close.split(',')]
    tiles, grid = patch_tiles(c, mpp)
    if a.patch_only:
        os.makedirs('jobs/fetch', exist_ok=True)
        json.dump({'id': a.id, 'delay': .5, 'close': c, 'close_grid': grid, 'files': tiles}, open(f'jobs/fetch/{a.id}.json', 'w'), indent=1)
        print(f'jobs/fetch/{a.id}.json (patch only, {len(tiles)} tiles); after it lands: map3d_prep.py patch outputs/fetch/{a.id} <art_dir>'); return
    f = [{'name': 'globe_bmng.jpg', 'url': GIBS + '&LAYERS=BlueMarble_NextGeneration&BBOX=-90,-180,90,180&WIDTH=8192&HEIGHT=4096'},
         {'name': 'ne_bmng.jpg', 'url': GIBS + f'&LAYERS=BlueMarble_NextGeneration&BBOX={B0},{L0},{B1},{L1}&WIDTH=4096&HEIGHT={int(4096 * (B1 - B0) / (L1 - L0))}'},
         ] + tiles
    z = getattr(a, 'zoom', 8) or 8; tx = lambda lon: int((lon + 180) / 360 * 2 ** z)
    ty = lambda lat: int((1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * 2 ** z)
    for x in range(tx(L0), tx(L1) + 1):
        for y in range(ty(B1), ty(B0) + 1):
            f.append({'name': f'dem_{z}_{x}_{y}.png', 'url': f'https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png'})
    os.makedirs('jobs/fetch', exist_ok=True)
    json.dump({'id': a.id, 'delay': .3, 'bbox': [L0, L1, B0, B1], 'close': c, 'close_grid': grid, 'zoom': z, 'files': f}, open(f'jobs/fetch/{a.id}.json', 'w'), indent=1)
    print(f'jobs/fetch/{a.id}.json with {len(f)} files; push it, then run build')


def grade(im, b, c, s): return ImageEnhance.Color(ImageEnhance.Contrast(ImageEnhance.Brightness(im).enhance(b)).enhance(c)).enhance(s)


def load_patch(F, J):
    """the sharp patch: stitched WMS tiles (pa_t_<row><col>.jpg, new jobs) or the single pa_weld.jpg (older jobs); <= 8192 px wide"""
    if J and J.get('close_grid'):
        ny, nx = J['close_grid']; rows = [np.hstack([np.array(Image.open(F + f'pa_t_{r}{k}.jpg').convert('RGB')) for k in range(nx)]) for r in range(ny)]
        hmin = min(r.shape[1] for r in rows); im = Image.fromarray(np.vstack([r[:, :hmin] for r in rows]))
    else:
        im = Image.open(F + 'pa_weld.jpg').convert('RGB')
    k = min(1.0, 8192 / im.width, 8192 / im.height)
    if k < 1: im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    return im


def cov_from_polys(polys_by_region, bbox, path, width=8192):
    """anti-aliased coverage texture for the map shader (R = region 1, G = region 2): smooth flag fills + border line at any zoom.
    polys_by_region: [[ring, ...], ...] lon/lat rings. Drawn at 2x and box-filtered, then a light blur."""
    L0, L1, B0, B1 = bbox; H = int(width * (B1 - B0) / (L1 - L0)) // 2 * 2; W2, H2 = width * 2, H * 2
    pt = lambda lo, la: ((lo - L0) / (L1 - L0) * W2, (B1 - la) / (B1 - B0) * H2); ch = []
    for rings in polys_by_region[:2]:
        m = Image.new('L', (W2, H2), 0); d = ImageDraw.Draw(m)
        for r in rings: d.polygon([pt(*c[:2]) for c in r], fill=255)
        ch.append(m.resize((width, H), Image.BOX).filter(ImageFilter.GaussianBlur(1.6)))
    while len(ch) < 3: ch.append(Image.new('L', (width, H), 0))
    Image.merge('RGB', ch[:3]).save(path)


def patch_cmd(a):
    """re-sharpen an already-built map: stitch a --patch-only fetch into <art_dir>/pa_close.jpg, colour-matched to the current look"""
    F = a.fetch_dir.rstrip('/') + '/'; A = a.art_dir.rstrip('/') + '/'; J = json.load(open(F.replace('outputs/fetch', 'jobs/fetch').rstrip('/') + '.json'))
    pc = np.array(grade(load_patch(F, J), 1.05, 1.08, 1.15)).astype(float); src = pc.reshape(-1, 3)
    old = A + 'pa_close.jpg'; M = json.load(open(A + 'map3d.json'))
    if os.path.exists(old) and M.get('pa_close_bbox'): ref = np.array(Image.open(old).convert('RGB')).astype(float).reshape(-1, 3); k = 1.0
    else:
        L0, L1, B0, B1 = M['bbox']; CL = J['close']; n = np.array(Image.open(A + 'ne.jpg').convert('RGB')).astype(float); h_, w_, _ = n.shape
        x0, x1 = int((CL[0] - L0) / (L1 - L0) * w_), int((CL[1] - L0) / (L1 - L0) * w_); y0, y1 = int((B1 - CL[3]) / (B1 - B0) * h_), int((B1 - CL[2]) / (B1 - B0) * h_)
        ref = n[max(0, y0):y1, max(0, x0):x1].reshape(-1, 3); k = 1.15
    if os.path.exists(old): os.replace(old, A + 'pa_close_prev.jpg')
    out = np.clip((pc - src.mean(0)) / (src.std(0) + 1e-6) * (ref.std(0) * k) + ref.mean(0), 0, 255)
    if a.land_only:   # water -> black, so the shader falls back to the smooth regional plate (turbid seas show Landsat swath seams)
        CL = J['close']; H_, W_ = out.shape[:2]; m = Image.new('L', (W_, H_), 0); d = ImageDraw.Draw(m)
        pt = lambda lo, la: ((lo - CL[0]) / (CL[1] - CL[0]) * W_, (CL[3] - la) / (CL[3] - CL[2]) * H_)
        for f in json.load(open(a.land_only))['features']:
            g = f['geometry']; polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
            for poly in polys:
                r = poly[0]; lo = [c[0] for c in r]; la = [c[1] for c in r]
                if max(lo) < CL[0] or min(lo) > CL[1] or max(la) < CL[2] or min(la) > CL[3]: continue
                d.polygon([pt(*c[:2]) for c in r], fill=255)
        m = m.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(4))   # ~4 px past the vector coast, feathered
        out = out * (np.asarray(m, np.float32)[..., None] / 255)
    Image.fromarray(out.astype(np.uint8)).save(old, quality=92)
    M['pa_close_bbox'] = J['close']; json.dump(M, open(A + 'map3d.json', 'w')); print('sharp patch ->', old, J['close'])


def cov_cmd(a):
    """pa_cov.png for maps whose flag mask came from elsewhere: upsample the id mask (40 = region 1, 80 = region 2) smoothly"""
    A = a.art_dir.rstrip('/') + '/'; m = np.array(Image.open(A + 'pa_mask.png').convert('L')); W = 8192; H = int(W * m.shape[0] / m.shape[1])
    ch = [Image.fromarray(((np.abs(m.astype(int) - v) < 20) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(2.4)) for v in (40, 80)]
    if m.max() == 255 and not (m == 40).any(): ch[0] = Image.fromarray(((m > 127) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(2.4))
    Image.merge('RGB', ch + [Image.new('L', (W, H), 0)]).save(A + 'pa_cov.png'); print('pa_cov.png', W, H)


def build(a):
    F = a.fetch_dir.rstrip('/') + '/'; A = a.art_dir.rstrip('/') + '/'; os.makedirs(A, exist_ok=True)
    jp = F.replace('outputs/fetch', 'jobs/fetch').rstrip('/') + '.json'; J = json.load(open(jp)) if os.path.exists(jp) else None
    if J and 'bbox' not in J: J = None
    L0, L1, B0, B1 = (J['bbox'] if J else [float(x) for x in a.bbox.split(',')]); CL = J['close'] if J else [float(x) for x in a.close.split(',')]
    # DEM mosaic (web mercator z8 terrarium) -> equirect 1024x512 over the bbox
    ZM = (J or {}).get('zoom', 8); N = 2 ** ZM; tiles = {}
    for f in glob.glob(F + f'dem_{ZM}_*.png'):
        _, _, x, y = os.path.basename(f)[:-4].split('_'); tiles[(int(x), int(y))] = np.array(Image.open(f).convert('RGB')).astype(np.float64)
    W, H = 1024, 512; LON, LAT = np.meshgrid(np.linspace(L0, L1, W), np.linspace(B1, B0, H))
    X = (LON + 180) / 360 * N; Y = (1 - np.log(np.tan(np.radians(LAT)) + 1 / np.cos(np.radians(LAT))) / np.pi) / 2 * N
    tx, ty = X.astype(int), Y.astype(int); px = ((X - tx) * 256).astype(int).clip(0, 255); py = ((Y - ty) * 256).astype(int).clip(0, 255)
    el = np.zeros((H, W))
    for (x, y), t in tiles.items():
        m = (tx == x) & (ty == y); el[m] = t[py[m], px[m], 0] * 256 + t[py[m], px[m], 1] + t[py[m], px[m], 2] / 256 - 32768
    el = np.maximum(el, 0); top = max(200.0, float(np.percentile(el, 99.9)) * 1.45); el = np.minimum(el, top)
    Image.fromarray((el / top * 65535).astype(np.uint16)).save(A + 'dem.png')
    Image.fromarray((el / top * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)).save(A + 'dem8.png')
    # multidirectional hillshade (2048x1024), median-centred so flat land stays mid-grey
    D = np.array(Image.fromarray(el.astype(np.float32)).resize((2048, 1024), Image.BICUBIC))
    lat0 = (B0 + B1) / 2; gy, gx = np.gradient(D * 3.0, (B1 - B0) / 1024 * 111000, (L1 - L0) / 2048 * 111000 * math.cos(math.radians(lat0)))
    def shade(az, alt):
        az, alt = math.radians(az), math.radians(alt); sl = np.arctan(np.hypot(gx, gy)); asp = np.arctan2(-gx, gy)
        return np.sin(alt) * np.cos(sl) + np.cos(alt) * np.sin(sl) * np.cos(az - asp)
    hs = .5 * shade(315, 45) + .25 * shade(270, 50) + .25 * shade(0, 55); med = np.median(hs); sp = np.percentile(hs, 99) - np.percentile(hs, 1)
    Image.fromarray((np.clip(.8 + (hs - med) / sp * 1.1, .3, 1.2) / 1.2 * 255).astype(np.uint8)).save(A + 'hillshade.png')
    # textures: graded Blue Marble (regional + globe), Landsat close patch colour-matched to the regional plate
    ne = grade(Image.open(F + 'ne_bmng.jpg').convert('RGB'), 1.55, 1.12, 1.35); ne.save(A + 'ne.jpg', quality=93)
    grade(Image.open(F + 'globe_bmng.jpg').convert('RGB'), 1.45, 1.1, 1.3).save(A + 'globe.jpg', quality=92)
    n = np.array(ne).astype(float); h_, w_, _ = n.shape
    x0, x1 = int((CL[0] - L0) / (L1 - L0) * w_), int((CL[1] - L0) / (L1 - L0) * w_); y0, y1 = int((B1 - CL[3]) / (B1 - B0) * h_), int((B1 - CL[2]) / (B1 - B0) * h_)
    ref = n[max(0, y0):y1, max(0, x0):x1].reshape(-1, 3); pc = np.array(grade(load_patch(F, J), 1.05, 1.08, 1.15)).astype(float); src = pc.reshape(-1, 3)
    Image.fromarray(np.clip((pc - src.mean(0)) / (src.std(0) + 1e-6) * (ref.std(0) * 1.15) + ref.mean(0), 0, 255).astype(np.uint8)).save(A + 'pa_close.jpg', quality=93)
    # region outline + mask
    src_name = 'ne_50m_admin_1_states_provinces.geojson' if a.admin1 else 'ne_50m_admin_0_countries.geojson'; want = a.admin1 or a.admin0
    cache = os.path.join('/tmp', src_name)
    if not os.path.exists(cache): urllib.request.urlretrieve(NE + src_name, cache)
    feats = [f for f in json.load(open(cache))['features'] if want in (f['properties'].get('name'), f['properties'].get('NAME'), f['properties'].get('ADMIN'))]
    if not feats: sys.exit(f'region "{want}" not found in {src_name}')
    g = feats[0]['geometry']; polys = [g['coordinates']] if g['type'] == 'Polygon' else g['coordinates']
    ring = max((p[0] for p in polys), key=len)
    mk = Image.new('L', (2048, 1024), 0); pt = lambda lo, la: ((lo - L0) / (L1 - L0) * 2048, (B1 - la) / (B1 - B0) * 1024)
    for p in polys: ImageDraw.Draw(mk).polygon([pt(*c[:2]) for c in p[0]], fill=255)
    mk.save(A + 'pa_mask.png')
    cov_from_polys([[p[0] for p in polys]], [L0, L1, B0, B1], A + 'pa_cov.png')   # smooth border/fill texture the map shader samples
    out = [ring[0][:2]]
    for c in ring[1:]:
        if math.hypot(c[0] - out[-1][0], c[1] - out[-1][1]) > .04: out.append(c[:2])
    pin = [float(x) for x in a.pin.split(',')]
    json.dump({'bbox': [L0, L1, B0, B1], 'outline': out, 'pa': out, 'pin': pin, 'centralia': pin, 'pa_close_bbox': CL, 'top': round(top, 1)}, open(A + 'map3d.json', 'w'))
    print('map assets ->', A, '| outline points', len(out), '| elevation cap', round(top))


ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest='cmd', required=True)
j = sp.add_parser('job'); j.add_argument('id'); [j.add_argument(k, type=float) for k in ('lon0', 'lon1', 'lat0', 'lat1')]; j.add_argument('--close'); j.add_argument('--zoom', type=int, default=8)  # 7 for very wide (continent-scale) regions
j.add_argument('--footprint'); j.add_argument('--map'); j.add_argument('--patch-only', action='store_true')
pp = sp.add_parser('patch'); pp.add_argument('fetch_dir'); pp.add_argument('art_dir'); pp.add_argument('--land-only', help='Natural Earth admin-0 GeoJSON: keep the patch on land only (sea from the regional plate)')
cv = sp.add_parser('cov'); cv.add_argument('art_dir')
b = sp.add_parser('build'); b.add_argument('fetch_dir'); b.add_argument('art_dir'); b.add_argument('--admin1'); b.add_argument('--admin0'); b.add_argument('--pin', required=True)
b.add_argument('--bbox'); b.add_argument('--close')
a = ap.parse_args()
if a.cmd == 'job' and not (a.close or a.footprint): sys.exit('job needs --close or --footprint fp.json --map <prefix>')
{'job': job, 'build': build, 'patch': patch_cmd, 'cov': cov_cmd}[a.cmd](a)
