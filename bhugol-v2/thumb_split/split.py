# BHUGOL "split" thumbnail (default since 24 Oct 2026, Gulf Stream video; style the user picked from a GeoGlobeTales
# outlier): two satellite halves side by side, each with one region filled in a bold flat colour, a white divider,
# and ONE highlighted label per half (black text on a yellow highlight bar). Cold/warm, before/after, A-vs-B topics.
# Usage: python3 split.py config.json      -> <out>/split_<lang>_v.jpg (1080x1920), split_<lang>_w.jpg (1280x720),
#                                             feed_split_<lang>_*.jpg (140 px feed test), for every language in config
# Config: {"out": "thumb/", "bm": "<Blue Marble equirect jpg>", "ne": "<ne_50m_admin_0_countries.geojson>",
#   "left":  {"lon": [-128, -63], "lat": 42, "iso": ["USA"], "keep": [-126, -66, 24, 50], "look": "cold",
#             "fill": [58, 130, 235], "edge": [215, 235, 255], "label": {"en": "USA", "hi": "अमेरिका"}, "label_at": [-98, 39.5]},
#   "right": {"lon": [-13, 35], "lat": 52, "continent": "Europe", "exclude": ["RUS", "ISL"], "keep": [-25, 45, -90, 72], "look": "warm",
#             "fill": [255, 124, 24], "edge": [255, 214, 150], "label": {"en": "EUROPE", "hi": "यूरोप"}, "label_at": [6, 49]}}
#   lon = the half's longitude span (the half's width), lat = Mercator centre latitude; keep = [lon0, lon1, lat0, lat1] ring
#   centroid filter (drops overseas islands, Alaska/Hawaii); look = cold | warm | none.
# Fetch the Blue Marble once with a jobs/fetch/ job (GIBS WMS BlueMarble_ShadedRelief_Bathymetry, 8192x4096, EPSG:4326).
import json, sys, os, base64, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
Image.MAX_IMAGE_PIXELS = None
CFG = json.load(open(sys.argv[1])); OUT = CFG.get('out', 'thumb/'); os.makedirs(OUT, exist_ok=True)
SRC = np.asarray(Image.open(CFG['bm']).convert('RGB')).astype(np.float32); SH, SW = SRC.shape[:2]
NE = json.load(open(CFG['ne']))
merc = lambda la: np.degrees(np.log(np.tan(np.pi / 4 + np.radians(la) / 2)))
imerc = lambda y: np.degrees(2 * np.arctan(np.exp(np.radians(y))) - np.pi / 2)
def crop(lon0, lon1, yc, W, H):
    k = W / (lon1 - lon0); yy, xx = np.mgrid[0:H, 0:W].astype(np.float64)
    lon = lon0 + xx / k; lat = imerc(yc + (H / 2 - yy) / k)
    u = np.clip((lon + 180) / 360 * (SW - 1), 0, SW - 1).astype(int); v = np.clip((90 - lat) / 180 * (SH - 1), 0, SH - 1).astype(int)
    return Image.fromarray(SRC[v, u].astype(np.uint8)), (lambda lo, la: ((lo - lon0) * k, H / 2 - (merc(la) - yc) * k))
def rings(h):
    for f in NE['features']:
        p = f['properties']
        if h.get('iso') and p.get('ADM0_A3') not in h['iso']: continue
        if h.get('continent') and p.get('CONTINENT') != h['continent']: continue
        if p.get('ADM0_A3') in h.get('exclude', []): continue
        g = f['geometry']
        for poly in (g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]):
            r = poly[0]; kx = h.get('keep')
            if kx and not (kx[0] < np.mean([q[0] for q in r]) < kx[1] and kx[2] < np.mean([q[1] for q in r]) < kx[3]): continue
            yield r
def fill(im, proj, rs, col, edge):
    S = 3; ov = Image.new('RGBA', (im.width * S, im.height * S), (0, 0, 0, 0)); ln = Image.new('RGBA', ov.size, (0, 0, 0, 0))
    d, dl = ImageDraw.Draw(ov), ImageDraw.Draw(ln)
    for r in rs:
        pts = [tuple(c * S for c in proj(*q)) for q in r]
        if len(pts) > 2: d.polygon(pts, fill=tuple(col) + (232,)); dl.line(pts + [pts[0]], fill=tuple(edge) + (255,), width=3 * S)
    ov = ov.resize(im.size, Image.LANCZOS); ln = ln.resize(im.size, Image.LANCZOS)
    shadow = Image.new('RGBA', im.size, (0, 0, 0, 0)); shadow.putalpha(ov.split()[3].filter(ImageFilter.GaussianBlur(10)).point(lambda a: int(a * .55)))
    out = im.convert('RGBA'); out.alpha_composite(shadow, (6, 10)); out.alpha_composite(ov); out.alpha_composite(ln); return out.convert('RGB')
def look(im, kind, seed):
    if kind == 'none': return im
    rng = np.random.default_rng(seed); w, h = im.size
    if kind == 'cold':
        a = np.asarray(ImageEnhance.Color(im).enhance(.55)).astype(np.float32) * [.78, .92, 1.08] + [10, 28, 48]; dots, col, rr, n = 2600, (255, 255, 255), (1.5, 4.5), 1.2
    else:
        a = np.asarray(ImageEnhance.Color(im).enhance(1.1)).astype(np.float32) * [1.18, 1.04, .7] + [38, 20, -8]; dots, col, rr, n = 9000, (255, 190, 90), (3, 9), 2.5
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA'); sp = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(sp)
    for _ in range(int(w * h / dots)):
        x, y, r = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(*rr); d.ellipse([x - r, y - r, x + r, y + r], fill=col + (int(rng.uniform(70, 190)),))
    im.alpha_composite(sp.filter(ImageFilter.GaussianBlur(n))); return im.convert('RGB')
K = '/home/claude/bhugol-kit/node_modules/@fontsource/'; b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
FA = b64(K + 'archivo/files/archivo-latin-800-normal.woff2'); FM = b64(K + 'mukta/files/mukta-devanagari-800-normal.woff2')
CSS = (f"@font-face{{font-family:A;src:url(data:font/woff2;base64,{FA})}}@font-face{{font-family:A;src:url(data:font/woff2;base64,{FM})}}"
       "body{margin:0;background:#222}.lb{position:absolute;transform:translate(-50%,-50%);font-family:A,sans-serif;font-weight:800;color:#0B0B0B;"
       "background:#FFE14D;padding:.06em .28em .1em;border-radius:.16em;border:.05em solid #fff;box-shadow:0 .08em 0 rgba(0,0,0,.35),0 .2em .5em rgba(0,0,0,.5);"
       "line-height:1.05;letter-spacing:.01em;white-space:nowrap}")
langs = sorted(set(CFG['left']['label']) | set(CFG['right']['label']))
halves = {}
for tag, W, H in (('v', 540, 1920), ('w', 640, 720)):
    for side, seed in (('left', 3), ('right', 5)):
        h = CFG[side]; im, pj = crop(h['lon'][0], h['lon'][1], merc(h['lat']), W, H)
        im = fill(look(im, h.get('look', 'none'), seed), pj, list(rings(h)), h['fill'], h.get('edge', [255, 255, 255]))
        p = os.path.join(OUT, f'bg_{tag}_{side}.jpg'); im.save(p, quality=92); halves[(tag, side)] = (p, pj(*h['label_at']), W, H)
for lang in langs:
    html = []
    for tag, fs in (('v', 104), ('w', 92)):
        (pl, ql, W, H), (pr, qr, _, _) = halves[(tag, 'left')], halves[(tag, 'right')]
        def lab(side, q, x0):   # keep the whole label bar inside its own half (estimated width; Latin ~0.7 em per char)
            t = CFG[side]['label'].get(lang, CFG[side]['label'].get('en', '')); f = int(fs * min(1, 6.5 / max(4, len(t)))); hw = (len(t) * .7 + .7) * f / 2
            x = min(max(q[0], hw + 14), W - hw - 14); return f'<div class="lb" style="left:{x0 + x:.0f}px;top:{q[1]:.0f}px;font-size:{f}px">{t}</div>'
        html.append(f'<div id="{tag}" style="position:relative;width:{2 * W}px;height:{H}px;overflow:hidden"><img src="data:image/jpeg;base64,{b64(pl)}" style="position:absolute;left:0;top:0">'
                    f'<img src="data:image/jpeg;base64,{b64(pr)}" style="position:absolute;left:{W}px;top:0"><div style="position:absolute;left:{W - 4}px;top:0;width:8px;height:{H}px;background:#fff;box-shadow:0 0 18px rgba(0,0,0,.5)"></div>'
                    f'{lab("left", ql, 0)}{lab("right", qr, W)}</div><div style="height:20px"></div>')
    hp = os.path.abspath(os.path.join(OUT, f'split_{lang}.html')); open(hp, 'w').write(f'<!doctype html><meta charset="utf-8"><style>{CSS}</style>' + ''.join(html))
    base = os.path.abspath(os.path.join(OUT, f'split_{lang}'))
    WK = os.environ.get('NODE_WORK', '/home/claude/work')   # folder with playwright-core in node_modules (ESM resolves from the script's folder)
    import shutil; shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shot.mjs'), os.path.join(WK, 'split_shot.mjs'))
    subprocess.run(['node', 'split_shot.mjs', hp, base], check=True, cwd=WK)
    for t in ('v', 'w'):
        im = Image.open(f'{base}_{t}.png').convert('RGB'); im.save(f'{base}_{t}.jpg', quality=93)
        im.resize((140, int(140 * im.height / im.width))).save(os.path.join(OUT, f'feed_split_{lang}_{t}.jpg'))
print('split thumbnails ->', OUT, langs)
