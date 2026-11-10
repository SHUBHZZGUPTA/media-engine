# Lake masks, outlines and overlay shapes for the Baikal Short (Natural Earth 50m lakes + countries).
# Writes art/bk_pa_mask.png (Baikal = 40), art/gl_pa_mask.png (Superior 40, Michigan 80, Huron 120, Erie 160, Ontario 200),
# and art/geo.json: lake rings, Belgium ring re-centred on Baikal at true size, Baikal ring re-centred near Superior.
import json, math, os
from PIL import Image, ImageDraw
H = '/home/claude/work/baikal/'; A = H + 'art/'
L = json.load(open(H + 'ne/ne_50m_lakes.geojson')); C = json.load(open(H + 'ne/ne_50m_admin_0_countries.geojson'))
def ring(fs, key, val):
    for f in fs['features']:
        if f['properties'].get(key) == val:
            g = f['geometry']; polys = [g['coordinates']] if g['type'] == 'Polygon' else g['coordinates']
            return max((p[0] for p in polys), key=len)
def thin(r, d=.03):
    out = [r[0][:2]]
    for c in r[1:]:
        if math.hypot(c[0] - out[-1][0], c[1] - out[-1][1]) > d: out.append(c[:2])
    return out
def mask(m3, rings, vals, name):
    L0, L1, B0, B1 = m3['bbox']; im = Image.new('L', (2048, 1024), 0); d = ImageDraw.Draw(im)
    pt = lambda lo, la: ((lo - L0) / (L1 - L0) * 2048, (B1 - la) / (B1 - B0) * 1024)
    for r, v in zip(rings, vals): d.polygon([pt(*c[:2]) for c in r], fill=v)
    im.save(A + name)
def km(r):  # ring -> local km about its centroid
    lo = sum(p[0] for p in r) / len(r); la = sum(p[1] for p in r) / len(r); k = math.cos(math.radians(la))
    return [((p[0] - lo) * 111.32 * k, (p[1] - la) * 110.57) for p in r], (lo, la)
def place(kmr, lon, lat, rot=0):
    k = math.cos(math.radians(lat)); c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    return [[lon + (x * c - y * s) / (111.32 * k), lat + (x * s + y * c) / 110.57] for x, y in kmr]
bai = ring(L, 'name', 'Lake Baikal'); names = ['Lake Superior', 'Lake Michigan', 'Lake Huron', 'Lake Erie', 'Lake Ontario']
gls = [ring(L, 'name', n) for n in names]; bel = None
for f in C['features']:
    if f['properties'].get('ADMIN') == 'Belgium':
        g = f['geometry']; polys = [g['coordinates']] if g['type'] == 'Polygon' else g['coordinates']; bel = max((p[0] for p in polys), key=len)
bk = json.load(open(A + 'bk/map3d.json')); gl = json.load(open(A + 'gl/map3d.json'))
mask(bk, [bai], [40], 'bk/pa_mask.png'); mask(gl, gls, [40, 80, 120, 160, 200], 'gl/pa_mask.png')
belkm, _ = km(bel); baikm, bc = km(bai)
area = lambda r: abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(r, r[1:] + r[:1]))) / 2
print('area km2: Baikal', round(area(baikm)), 'Belgium', round(area(belkm)), 'Superior', round(area(km(gls[0])[0])), 'Great Lakes', round(sum(area(km(g)[0]) for g in gls)))
G = {'baikal': thin(bai), 'gl': [thin(g) for g in gls], 'superior': thin(gls[0]),
     'belgium_on_baikal': place(belkm, 107.55, 53.05, 38),      # Belgium at true size, laid along the lake's middle
     'baikal_near_superior': place(baikm, -80.8, 48.4, -45)}      # Baikal at true size, set down north-east of Lake Huron
json.dump(G, open(A + 'geo.json', 'w'))
for d, m in (('bk', bk), ('gl', gl)):
    m['pa'] = G['baikal'] if d == 'bk' else G['superior']; m['outline'] = m['pa']; json.dump(m, open(A + d + '/map3d.json', 'w'))
print('ok')
