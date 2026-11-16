#!/usr/bin/env python3
"""Sharp satellite map plates for the BHUGOL GTA engine (make.py `mapshot`).

  plan:   python3 maps.py plan  <fetch_id> <name> <usgs|eox> <z> <lon0> <lon1> <lat0> <lat1>
          -> writes jobs/fetch/<fetch_id>.json (run from the media-engine root, then commit + push it alone;
             the fetch workflow downloads the tiles into outputs/fetch/<fetch_id>/)
  stitch: python3 maps.py stitch <fetch_id> <name> <z> <lon0> <lon1> <lat0> <lat1> <out_dir>
          -> <out_dir>/map_<name>.jpg + map_<name>.json  ({bbox, z, px0, size}: what make.py's MAPS/mxy() read)

Sources (both free, credit in the description):
  usgs = USGS USGSImageryOnly (public domain, US only, sharp to z16). City-level plates: z15 (z16 for a single street).
  eox  = Sentinel-2 cloudless by EOX (CC BY 4.0, worldwide, ~z13 max). State/country plates: z9 (z10-11 for a region).
Rule from the GTA video: a plate is only used where the camera never stretches it past ~1.2x (no blur, no pixelation).
"""
import json, math, os, sys
UA = 'media-engine/1.0 (BHUGOL maps; https://github.com/SHUBHZZGUPTA/media-engine)'
URL = {'usgs': 'https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}',
       'eox': 'https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless_3857/default/g/{z}/{y}/{x}.jpg'}

def tile(lon, lat, z):
    n = 2 ** z; s = math.sin(math.radians(lat))
    return (lon + 180) / 360 * n, (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * n

def rng(z, lon0, lon1, lat0, lat1):
    x0, y0 = tile(lon0, lat1, z); x1, y1 = tile(lon1, lat0, z)
    return int(x0), int(x1), int(y0), int(y1), (x0, y0, x1, y1)

cmd = sys.argv[1]
if cmd == 'plan':
    fid, name, src, z = sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]); lon0, lon1, lat0, lat1 = map(float, sys.argv[6:10])
    X0, X1, Y0, Y1, _ = rng(z, lon0, lon1, lat0, lat1)
    files = [{'name': f'{name}_{z}_{x}_{y}.jpg', 'url': URL[src].format(z=z, x=x, y=y)} for x in range(X0, X1 + 1) for y in range(Y0, Y1 + 1)]
    job = {'id': fid, 'ua': UA, 'delay': 0.1, 'meta': {name: {'bbox': [lon0, lon1, lat0, lat1], 'z': z, 'x': [X0, X1], 'y': [Y0, Y1], 'src': src}}, 'files': files}
    os.makedirs('jobs/fetch', exist_ok=True); json.dump(job, open(f'jobs/fetch/{fid}.json', 'w'), indent=1)
    print(f'{len(files)} tiles -> jobs/fetch/{fid}.json  (~{len(files) * 256 // 1000}k px wide total; keep under ~600 tiles per job)')
elif cmd == 'stitch':
    from PIL import Image
    fid, name, z = sys.argv[2], sys.argv[3], int(sys.argv[4]); lon0, lon1, lat0, lat1 = map(float, sys.argv[5:9]); out = sys.argv[9]
    X0, X1, Y0, Y1, (fx0, fy0, fx1, fy1) = rng(z, lon0, lon1, lat0, lat1)
    big = Image.new('RGB', ((X1 - X0 + 1) * 256, (Y1 - Y0 + 1) * 256), (12, 36, 66)); miss = 0
    for x in range(X0, X1 + 1):
        for y in range(Y0, Y1 + 1):
            p = f'outputs/fetch/{fid}/{name}_{z}_{x}_{y}.jpg'
            if os.path.exists(p): big.paste(Image.open(p).convert('RGB'), ((x - X0) * 256, (y - Y0) * 256))
            else: miss += 1
    l, t = round((fx0 - X0) * 256), round((fy0 - Y0) * 256); r, b = round((fx1 - X0) * 256), round((fy1 - Y0) * 256)
    big = big.crop((l, t, r, b)); os.makedirs(out, exist_ok=True); big.save(f'{out}/map_{name}.jpg', quality=92)
    json.dump({'bbox': [lon0, lon1, lat0, lat1], 'z': z, 'px0': [fx0 * 256, fy0 * 256], 'size': list(big.size)}, open(f'{out}/map_{name}.json', 'w'))
    print(f'map_{name}.jpg {big.size} missing tiles: {miss}')
