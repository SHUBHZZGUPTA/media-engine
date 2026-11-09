# Sharp Landsat patches (colour-matched to the Blue Marble plate), a finer close DEM for MI, and flag overlays
# (each country filled with its flag + a light border) for the Danube Short. Inputs: outputs/fetch/danube-hd.
import json, math, glob, os, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
F = '/home/claude/media-engine/outputs/fetch/danube-hd/'; A = '/home/claude/work/dn/art/'
Image.MAX_IMAGE_PIXELS = None
def grade(im, b, c, s): return ImageEnhance.Color(ImageEnhance.Contrast(ImageEnhance.Brightness(im).enhance(b)).enhance(c)).enhance(s)
J = json.load(open('/home/claude/media-engine/jobs/fetch/danube-hd.json')); PB = J['patches']
WB = json.load(open(A + 'w_map3d.json'))['bbox']; IB = json.load(open(A + 'i_map3d.json'))['bbox']

def match(src_im, ref_im, bbox, rb):
    """colour-match a Landsat patch to the same area of the reference plate (per-channel mean/std)"""
    L0, L1, B0, B1 = rb; l0, l1, b0, b1 = bbox; r = np.array(ref_im).astype(float); h, w, _ = r.shape
    x0, x1 = int((max(l0, L0) - L0) / (L1 - L0) * w), int((min(l1, L1) - L0) / (L1 - L0) * w)
    y0, y1 = int((B1 - min(b1, B1)) / (B1 - B0) * h), int((B1 - max(b0, B0)) / (B1 - B0) * h)
    ref = r[y0:y1, x0:x1].reshape(-1, 3); s = np.array(grade(src_im, 1.05, 1.08, 1.15)).astype(float); flat = s.reshape(-1, 3)
    out = (s - flat.mean(0)) / (flat.std(0) + 1e-6) * (ref.std(0) * 1.15) + ref.mean(0)
    out = .55 * out + .45 * (s - flat.mean(0) + ref.mean(0))   # keep some of Landsat's own detail and contrast
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

wne = Image.open(A + 'w_ne.jpg').convert('RGB'); ine = Image.open(A + 'i_ne.jpg').convert('RGB')
patches = {}
for k in ['hd_vb', 'hd_bu', 'hd_be', 'hd_src']:
    im = match(Image.open(F + k + '.jpg').convert('RGB'), wne, PB[k], WB); im.save(A + k + '.jpg', quality=92); patches[k] = PB[k]
# MI: the whole bbox becomes Landsat (replaces the Blue Marble plate)
mi = match(Image.open(F + 'hd_mi.jpg').convert('RGB'), ine, PB['hd_mi'], IB); mi.save(A + 'i_ne.jpg', quality=93)
json.dump(patches, open(A + 'hd_patches.json', 'w'))

# MI finer DEM (z12) -> 2048 wide
L0, L1, B0, B1 = IB; N = 2 ** 12; tiles = {}
for f in glob.glob(F + 'mdem_12_*.png'):
    _, _, x, y = os.path.basename(f)[:-4].split('_'); tiles[(int(x), int(y))] = np.array(Image.open(f).convert('RGB')).astype(np.float64)
W, H = 2048, 1024; LON, LAT = np.meshgrid(np.linspace(L0, L1, W), np.linspace(B1, B0, H))
X = (LON + 180) / 360 * N; Y = (1 - np.log(np.tan(np.radians(LAT)) + 1 / np.cos(np.radians(LAT))) / np.pi) / 2 * N
tx, ty = X.astype(int), Y.astype(int); px = ((X - tx) * 256).astype(int).clip(0, 255); py = ((Y - ty) * 256).astype(int).clip(0, 255)
el = np.zeros((H, W))
for (x, y), t in tiles.items():
    m = (tx == x) & (ty == y); el[m] = t[py[m], px[m], 0] * 256 + t[py[m], px[m], 1] + t[py[m], px[m], 2] / 256 - 32768
el = np.maximum(el, 0); top = max(200.0, float(np.percentile(el, 99.9)) * 1.45); el = np.minimum(el, top)
Image.fromarray((el / top * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6)).save(A + 'i_dem8.png')
lat0 = (B0 + B1) / 2; gy, gx = np.gradient(el * 2.0, (B1 - B0) / H * 111000, (L1 - L0) / W * 111000 * math.cos(math.radians(lat0)))
def shade(az, alt):
    az, alt = math.radians(az), math.radians(alt); sl = np.arctan(np.hypot(gx, gy)); asp = np.arctan2(-gx, gy)
    return np.sin(alt) * np.cos(sl) + np.cos(alt) * np.sin(sl) * np.cos(az - asp)
hs = .5 * shade(315, 45) + .25 * shade(270, 50) + .25 * shade(0, 55); med = np.median(hs); sp = np.percentile(hs, 99) - np.percentile(hs, 1)
Image.fromarray((np.clip(.8 + (hs - med) / sp * 1.1, .3, 1.2) / 1.2 * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.8)).save(A + 'i_hillshade.png')
print('MI dem cap', round(top), 'tiles', len(tiles))

# flag overlays (RGBA): stripes span each country's part inside the clip box, so a close-up still shows the whole flag
G = json.load(open('/home/claude/work/dn/ne/adm10.geojson'))
LAKES = []
for f in json.load(open('/home/claude/work/dn/ne/lakes10.geojson'))['features']:
    g = f['geometry']; LAKES += [p[0] for p in ([g['coordinates']] if g['type'] == 'Polygon' else g['coordinates'])]
FL = {'Austria': ('h', [(237, 41, 57), (255, 255, 255), (237, 41, 57)]), 'Slovakia': ('h', [(255, 255, 255), (11, 78, 162), (238, 28, 37)]),
      'Hungary': ('h', [(205, 42, 62), (255, 255, 255), (67, 111, 77)]), 'Republic of Serbia': ('h', [(198, 54, 60), (12, 64, 118), (255, 255, 255)]),
      'Germany': ('h', [(70, 70, 70), (221, 0, 0), (255, 206, 0)]), 'Switzerland': ('ch', None)}
def overlay(bbox, W, H, items, out, bw, rot=False):
    L0, L1, B0, B1 = bbox; P = lambda lo, la: ((lo - L0) / (L1 - L0) * W, (B1 - la) / (B1 - B0) * H)
    rgb = np.zeros((H, W, 3)); al = np.zeros((H, W)); edge = Image.new('L', (W, H), 0)
    for name, clip in items:
        f = [f for f in G['features'] if f['properties']['ADMIN'] == name][0]; g = f['geometry']
        polys = [g['coordinates']] if g['type'] == 'Polygon' else g['coordinates']
        m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
        for p in polys:
            d.polygon([P(*c[:2]) for c in p[0]], fill=255)
            for hole in p[1:]: d.polygon([P(*c[:2]) for c in hole], fill=0)
            ImageDraw.Draw(edge).line([P(*c[:2]) for c in p[0]] + [P(*p[0][0][:2])], fill=255, width=bw)
        for p in LAKES:
            if any(L0 - 1 < c[0] < L1 + 1 and B0 - 1 < c[1] < B1 + 1 for c in p[:: max(1, len(p) // 20)]): d.polygon([P(*c[:2]) for c in p], fill=0)
        M = np.array(m) / 255.0
        cx0, cy0 = P(clip[0], clip[3]); cx1, cy1 = P(clip[1], clip[2])
        ys, xs = np.nonzero(M[max(0, int(cy0)):int(cy1), max(0, int(cx0)):int(cx1)])
        if not len(ys): continue
        y0, y1 = ys.min() + max(0, int(cy0)), ys.max() + max(0, int(cy0)); x0, x1 = xs.min() + max(0, int(cx0)), xs.max() + max(0, int(cx0))
        kind, cols = FL[name]; fl = np.zeros((H, W, 3))
        if kind == 'h' and rot:   # for an east-up camera: the flag's top stripe on the east side
            xx = np.clip((x1 - np.arange(W)) / max(1, x1 - x0), 0, .9999); band = (xx * 3).astype(int)
            for i, c in enumerate(cols): fl[:, band == i] = c
        elif kind == 'h':
            yy = np.clip((np.arange(H) - y0) / max(1, y1 - y0), 0, .9999); band = (yy * 3).astype(int)
            for i, c in enumerate(cols): fl[band == i] = c
        else:
            fl[:] = (218, 41, 28); cxm, cym = (x0 + x1) / 2, (y0 + y1) / 2; s = min(x1 - x0, y1 - y0) * .32; t = s * .33
            Y, X = np.mgrid[0:H, 0:W]; cross = ((abs(X - cxm) < t / 2) & (abs(Y - cym) < s / 2)) | ((abs(Y - cym) < t / 2) & (abs(X - cxm) < s / 2)); fl[cross] = (255, 255, 255)
        rgb = rgb * (1 - M[..., None]) + fl * M[..., None]; al = np.maximum(al, M * .82)
    e = np.array(edge.filter(ImageFilter.GaussianBlur(bw * .35))) / 255.0
    rgb = rgb * (1 - e[..., None]) + np.array([255, 246, 214]) * e[..., None]; al = np.maximum(al, e)
    Image.fromarray(np.dstack([np.clip(rgb, 0, 255), al * 255]).astype(np.uint8), 'RGBA').save(out); print('overlay', out)
big = (-180, 180, -90, 90)
overlay(WB, 4096, 1911, [('Austria', big), ('Slovakia', big), ('Hungary', big), ('Republic of Serbia', big)], A + 'w_flag1.png', 7)
overlay(WB, 4096, 1911, [('Germany', (7.0, 11.0, 47.2, 49.4)), ('Switzerland', (7.0, 10.5, 45.8, 47.9)), ('Austria', big)], A + 'w_flag2.png', 7)
overlay(IB, 2048, 1170, [('Germany', IB), ('Switzerland', IB), ('Austria', IB)], A + 'i_flag1.png', 5)
overlay(WB, 4096, 1911, [('Austria', big), ('Slovakia', big), ('Hungary', big), ('Republic of Serbia', big)], A + 'w_flag1r.png', 7, rot=True)
