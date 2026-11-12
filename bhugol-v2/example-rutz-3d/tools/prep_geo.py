# Russia time-zone mask (equirect), zone centres, France territories mask + pins, France outline for the character.
import json, math
from PIL import Image, ImageDraw
W = '/home/claude/work/rutz/'; NE = W + 'ne/'; A = W + 'art/'
A1 = json.load(open(NE + 'ne_50m_admin_1_states_provinces.geojson')); C10 = json.load(open(NE + 'ne_10m_admin_0_countries.geojson'))
Z = {2: ['Kaliningrad'], 4: ['Samara', 'Udmurt', "Astrakhan'", 'Saratov', "Ul'yanovsk"],
     5: ['Bashkortostan', 'Chelyabinsk', 'Kurgan', 'Orenburg', "Perm'", 'Sverdlovsk', "Tyumen'", 'Khanty-Mansiy', 'Yamal-Nenets'],
     6: ['Omsk'], 7: ['Altay', 'Gorno-Altay', 'Kemerovo', 'Krasnoyarsk', 'Khakass', 'Tuva', 'Novosibirsk', 'Tomsk'], 8: ['Irkutsk', 'Buryat'],
     9: ['Chita', 'Amur'], 10: ["Primor'ye", 'Khabarovsk', 'Yevrey'], 11: ['Maga Buryatdan', 'Sakhalin'], 12: ['Kamchatka', 'Chukchi Autonomous Okrug']}
EXCL = {'Crimea', 'Sevastopol'}   # internationally recognised borders only
off = {n: o for o, ns in Z.items() for n in ns}
WM, HM = 4096, 2048
pt = lambda lo, la: ((lo + 180) / 360 * WM, (90 - la) / 180 * HM)
im = Image.new('L', (WM, HM), 0); d = ImageDraw.Draw(im)
acc = {o: [0, 0, 0] for o in range(2, 13)}
def polys(g): return [g['coordinates']] if g['type'] == 'Polygon' else g['coordinates']
for f in A1['features']:
    p = f['properties']
    if p.get('adm0_a3') != 'RUS' or p['name'] in EXCL: continue
    for poly in polys(f['geometry']):
        ring = poly[0]
        if p['name'] == 'Sakha (Yakutia)':
            # split Sakha by longitude bands (+9 west, +10 middle, +11 east), approximating its three zones
            for o, (l0, l1) in {9: (-180, 134), 10: (134, 144), 11: (144, 180)}.items():
                m = Image.new('L', (WM, HM), 0); ImageDraw.Draw(m).polygon([pt(*c[:2]) for c in ring], fill=255)
                x0, x1 = int(pt(l0, 0)[0]), int(pt(l1, 0)[0]); band = Image.new('L', (WM, HM), 0); ImageDraw.Draw(band).rectangle([x0, 0, x1, HM], fill=255)
                from PIL import ImageChops; mm = ImageChops.multiply(m, band); im.paste((o - 1) * 20, mask=mm)
                bb = mm.getbbox()
                if bb: acc[o][0] += (bb[0] + bb[2]) / 2 * 1; acc[o][1] += (bb[1] + bb[3]) / 2; acc[o][2] += 1
            continue
        o = off.get(p['name'], 3); d.polygon([pt(*c[:2]) for c in ring], fill=(o - 1) * 20)
        if len(ring) > 30:
            xs = [pt(*c[:2]) for c in ring]; acc[o][0] += sum(x for x, _ in xs) / len(xs) * len(ring) / 1000; acc[o][1] += sum(y for _, y in xs) / len(xs) * len(ring) / 1000; acc[o][2] += len(ring) / 1000
im.save(A + 'zones.png')
cent = {}
for o, (sx, sy, n) in acc.items():
    if n: x, y = sx / n, sy / n; cent[o] = [round(x / WM * 360 - 180, 2), round(90 - y / HM * 180, 2)]
# hand-placed label points (zone centroids drift north on big Arctic regions)
LBL = {2: [20.5, 54.7], 3: [40, 57], 4: [50.5, 53.5], 5: [62, 60], 6: [73.4, 56], 7: [92, 62], 8: [106, 56], 9: [122, 60], 10: [135, 52], 11: [150, 63], 12: [162, 63]}
print('centroids', cent)
# France + overseas territories (10m countries, by sovereignty)
fm = Image.new('L', (WM, HM), 0); fd = ImageDraw.Draw(fm); n = 0
for f in C10['features']:
    p = f['properties']
    if p.get('SOVEREIGNT') == 'France' or p.get('ADMIN') == 'France':
        for poly in polys(f['geometry']): fd.polygon([pt(*c[:2]) for c in poly[0]], fill=255); n += 1
fm.save(A + 'france_mask.png'); print('france polys', n)
PINS = [['TAHITI', -149.4, -17.6, '−10'], ['MARQUESAS', -140.0, -9.0, '−9:30'], ['GAMBIER', -134.9, -23.1, '−9'], ['CLIPPERTON', -109.2, 10.3, '−8'],
        ['GUADELOUPE', -61.5, 16.2, '−4'], ['GUIANA', -53.0, 4.0, '−3'], ['ST PIERRE', -56.2, 46.8, '−3'], ['PARIS', 2.35, 48.86, '+1'], ['MAYOTTE', 45.1, -12.8, '+3'],
        ['RÉUNION', 55.5, -21.1, '+4'], ['KERGUELEN', 69.3, -49.3, '+5'], ['NEW CALEDONIA', 165.6, -21.3, '+11'], ['WALLIS', -176.2, -13.3, '+12']]
# France metropolitan outline -> SVG path in a 600x600 box (character body)
fr = next(f for f in C10['features'] if f['properties'].get('ADMIN') == 'France')
ring = max((p[0] for p in polys(fr['geometry']) if all(-6 < c[0] < 10 and 41 < c[1] < 52 for c in p[0])), key=len)
k = math.cos(math.radians(46.5)); xs = [c[0] * k for c in ring]; ys = [-c[1] for c in ring]
x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys); s = 560 / max(x1 - x0, y1 - y0); ox = (600 - (x1 - x0) * s) / 2; oy = (600 - (y1 - y0) * s) / 2
pts = [((x - x0) * s + ox, (y - y0) * s + oy) for x, y in zip(xs, ys)]; th = [pts[0]]
for q in pts[1:]:
    if math.hypot(q[0] - th[-1][0], q[1] - th[-1][1]) > 3: th.append(q)
dpath = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in th) + 'Z'
TRAIN = [[37.62, 55.75], [39.9, 57.63], [49.67, 58.6], [56.25, 58.01], [60.6, 56.84], [65.53, 57.15], [73.37, 54.99], [82.92, 55.03], [92.87, 56.01],
         [104.28, 52.29], [107.58, 51.83], [113.5, 52.03], [123.9, 53.99], [127.5, 50.27], [135.07, 48.48], [131.89, 43.12]]
json.dump({'zone_lbl': LBL, 'cent': cent, 'fr_pins': PINS, 'train': TRAIN, 'fr_path': dpath,
           'kam': [158.65, 53.02], 'kal': [20.51, 54.71], 'msk': [37.62, 55.75], 'vla': [131.89, 43.12]}, open(A + 'geo.json', 'w'))
print('ok', len(th), 'france path pts')
