# Island raster for the MK scene: R = signed distance to coast (128 + 2*metres, +inside), G = Sweden side (1809 straight line), B = Sweden side (1985 S border)
# Also writes art/mk_geo.json: border polyline (units = 10 m, x east / y north), old straight endpoints, buildings, extents.
import json, math
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
g = json.load(open('art/island.json'))
X0, X1, Y0, Y1, RES = -160.0, 280.0, -170.0, 120.0, .5       # metres, 0.5 m/px
W, H = int((X1 - X0) / RES), int((Y1 - Y0) / RES)
P = lambda p: ((p[0] - X0) / RES, (Y1 - p[1]) / RES)
land = Image.new('L', (W, H), 0); d = ImageDraw.Draw(land)
for r in g['coast']: d.polygon([P(p) for p in r], fill=255)
L = np.array(land) > 127
din = ndimage.distance_transform_edt(L) * RES; dout = ndimage.distance_transform_edt(~L) * RES
sd = np.where(L, din, -dout); R = np.clip(128 + sd * 2, 0, 255).astype(np.uint8)
B = g['border_ways']['722582744'] + g['border_ways']['1092471860'][1:]
def side(poly):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([P(p) for p in poly], fill=255); return np.array(m)
a, b = B[0], B[-1]
far_s = [a[0] - (b[0] - a[0]) * 3, a[1] - (b[1] - a[1]) * 3]; far_n = [b[0] + (b[0] - a[0]) * 3, b[1] + (b[1] - a[1]) * 3]
old = side([far_s, a, b, far_n, [-2000, far_n[1]], [-2000, far_s[1]]])
new = side([far_s] + B + [far_n, [-2000, far_n[1]], [-2000, far_s[1]]])
img = np.dstack([R, old, new]); Image.fromarray(img, 'RGB').save('art/isl.png')
# smooth version of masks for nicer edges not needed (bilinear in GPU)
u = lambda p: [round(p[0] / 10, 3), round(p[1] / 10, 3)]
json.dump({'ext': [X0 / 10, X1 / 10, Y0 / 10, Y1 / 10], 'border': [u(p) for p in B], 'buildings': [[u(p) for p in q] for q in g['buildings']],
           'lighthouse': [u(p) for p in g['lighthouse']], 'coast0': [u(p) for p in g['coast'][0]]}, open('art/mk_geo.json', 'w'))
# areas swapped (sanity: equal)
lm = L; s_old = (old > 127) & lm; s_new = (new > 127) & lm
print('island m2', lm.sum() * RES * RES, 'SE old', s_old.sum() * .25, 'SE new', s_new.sum() * .25, 'SE->FI', (s_old & ~s_new).sum() * .25, 'FI->SE', (~s_old & s_new).sum() * .25)
