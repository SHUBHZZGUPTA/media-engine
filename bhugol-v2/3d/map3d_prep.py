"""3D satellite-terrain map assets for a BHUGOL v2 flyover (globe -> region terrain -> glowing border + pin).

Step 1, write the fetch job (NASA GIBS imagery + AWS Terrarium elevation tiles), then push it:
  python3 map3d_prep.py job <id> <lon0> <lon1> <lat0> <lat1> --close lon0,lon1,lat0,lat1
    bbox = the regional terrain (about 12 x 6 degrees around the subject works well)
    --close = a smaller patch inside it that gets sharper Landsat imagery (where the camera ends up)
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


def job(a):
    L0, L1, B0, B1 = a.lon0, a.lon1, a.lat0, a.lat1; c = [float(x) for x in a.close.split(',')]
    f = [{'name': 'globe_bmng.jpg', 'url': GIBS + '&LAYERS=BlueMarble_NextGeneration&BBOX=-90,-180,90,180&WIDTH=8192&HEIGHT=4096'},
         {'name': 'ne_bmng.jpg', 'url': GIBS + f'&LAYERS=BlueMarble_NextGeneration&BBOX={B0},{L0},{B1},{L1}&WIDTH=4096&HEIGHT={int(4096 * (B1 - B0) / (L1 - L0))}'},
         {'name': 'pa_weld.jpg', 'url': GIBS + f'&LAYERS=Landsat_WELD_CorrectedReflectance_TrueColor_Global_Annual&BBOX={c[2]},{c[0]},{c[3]},{c[1]}&WIDTH=4096&HEIGHT={int(4096 * (c[3] - c[2]) / (c[1] - c[0]))}'}]
    z = getattr(a, 'zoom', 8) or 8; tx = lambda lon: int((lon + 180) / 360 * 2 ** z)
    ty = lambda lat: int((1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * 2 ** z)
    for x in range(tx(L0), tx(L1) + 1):
        for y in range(ty(B1), ty(B0) + 1):
            f.append({'name': f'dem_{z}_{x}_{y}.png', 'url': f'https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png'})
    os.makedirs('jobs/fetch', exist_ok=True)
    json.dump({'id': a.id, 'delay': .3, 'bbox': [L0, L1, B0, B1], 'close': c, 'zoom': z, 'files': f}, open(f'jobs/fetch/{a.id}.json', 'w'), indent=1)
    print(f'jobs/fetch/{a.id}.json with {len(f)} files; push it, then run build')


def grade(im, b, c, s): return ImageEnhance.Color(ImageEnhance.Contrast(ImageEnhance.Brightness(im).enhance(b)).enhance(c)).enhance(s)


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
    ref = n[y0:y1, x0:x1].reshape(-1, 3); pc = np.array(grade(Image.open(F + 'pa_weld.jpg').convert('RGB'), 1.05, 1.08, 1.15)).astype(float); src = pc.reshape(-1, 3)
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
    out = [ring[0][:2]]
    for c in ring[1:]:
        if math.hypot(c[0] - out[-1][0], c[1] - out[-1][1]) > .04: out.append(c[:2])
    pin = [float(x) for x in a.pin.split(',')]
    json.dump({'bbox': [L0, L1, B0, B1], 'outline': out, 'pa': out, 'pin': pin, 'centralia': pin, 'pa_close_bbox': CL}, open(A + 'map3d.json', 'w'))
    print('map assets ->', A, '| outline points', len(out), '| elevation cap', round(top))


ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest='cmd', required=True)
j = sp.add_parser('job'); j.add_argument('id'); [j.add_argument(k, type=float) for k in ('lon0', 'lon1', 'lat0', 'lat1')]; j.add_argument('--close', required=True); j.add_argument('--zoom', type=int, default=8)  # 7 for very wide (continent-scale) regions
b = sp.add_parser('build'); b.add_argument('fetch_dir'); b.add_argument('art_dir'); b.add_argument('--admin1'); b.add_argument('--admin0'); b.add_argument('--pin', required=True)
b.add_argument('--bbox'); b.add_argument('--close')
a = ap.parse_args(); job(a) if a.cmd == 'job' else build(a)
