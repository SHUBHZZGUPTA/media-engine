# OSM -> local metre geometry for the Märket island scene (x east, y north, origin = lighthouse centroid)
import json, math, sys
d = json.load(open(sys.argv[1])); out = sys.argv[2]
E = d['elements']; W = {e['id']: e for e in E if e['type'] == 'way'}
lh = W[298848048]['geometry']; LAT0 = sum(p['lat'] for p in lh) / len(lh); LON0 = sum(p['lon'] for p in lh) / len(lh)
KX = 111320 * math.cos(math.radians(LAT0)); KY = 110540
xy = lambda p: [round((p['lon'] - LON0) * KX, 2), round((p['lat'] - LAT0) * KY, 2)]
# coast rings: join coastline ways end to end
segs = [[(p['lon'], p['lat']) for p in W[i]['geometry']] for i in W if W[i].get('tags', {}).get('natural') == 'coastline']
rings = []
while segs:
    r = segs.pop(0)
    changed = True
    while changed and r[0] != r[-1]:
        changed = False
        for s in segs:
            if s[0] == r[-1]: r += s[1:]; segs.remove(s); changed = True; break
            if s[-1] == r[0]: r = s[:-1] + r; segs.remove(s); changed = True; break
    rings.append(r)
R = [[xy({'lon': a, 'lat': b}) for a, b in r] for r in rings]
area = lambda r: abs(sum(r[i][0] * r[(i + 1) % len(r)][1] - r[(i + 1) % len(r)][0] * r[i][1] for i in range(len(r)))) / 2
R.sort(key=area, reverse=True)
print('rings', [(len(r), round(area(r))) for r in R[:6]])
bd = {i: [xy(p) for p in W[i]['geometry']] for i in W if W[i].get('tags', {}).get('admin_level') == '2'}
for i, v in bd.items(): print('border way', i, W[i]['tags'].get('maritime'), len(v), v[0], v[-1])
bld = [[xy(p) for p in W[i]['geometry']] for i in W if 'building' in W[i].get('tags', {}) or 'building:part' in W[i].get('tags', {})]
json.dump({'origin': [LON0, LAT0], 'coast': R, 'border_ways': {str(k): v for k, v in bd.items()}, 'lighthouse': [xy(p) for p in lh], 'buildings': bld}, open(out, 'w'))
