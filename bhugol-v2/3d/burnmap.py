"""Spread map for a 'before -> after' reveal (fire spreading through tunnels, water flooding a valley, a border growing...).
Usage: python3 burnmap.py <before.png> <after.png> <seed_x> <seed_y> <out.png>
before/after must be pixel-aligned (make 'after' as a Codex EDIT of 'before'). seed = image px where the change starts.
Writes a grey map: dark = changes first, white = never changes. The 3D plate shader reveals 'after' where map < prog,
so animating prog 0 -> 1.1 plays the spread outward from the seed along the changed pixels.
"""
import sys
from collections import deque
import numpy as np
from PIL import Image
bp, ap_, sx, sy, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
c = np.array(Image.open(bp).convert('RGB')).astype(float); h = np.array(Image.open(ap_).convert('RGB')).astype(float)
diff = np.abs(h - c).sum(2); hot = (h[..., 0] > 170) & (h[..., 0] > h[..., 2] + 70); mask = (diff > 70) | (hot & (diff > 40))
s = 4; H, W = mask.shape[0] // s * s, mask.shape[1] // s * s
m = mask[:H, :W].reshape(H // s, s, W // s, s).mean((1, 3)) > .25; Hh, Ww = m.shape
ys, xs = np.nonzero(m); k = np.argmin((ys - sy // s) ** 2 + (xs - sx // s) ** 2); seed = (ys[k], xs[k])
dist = np.full(m.shape, -1.0); dist[seed] = 0; q = deque([seed])
while q:
    y, x = q.popleft()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
        yy, xx = y + dy, x + dx
        if 0 <= yy < Hh and 0 <= xx < Ww and m[yy, xx] and dist[yy, xx] < 0: dist[yy, xx] = dist[y, x] + (1.414 if dy and dx else 1); q.append((yy, xx))
reach = dist >= 0; dmax = dist[reach].max(); dist[m & ~reach] = dmax * .95
dn = np.where(m, dist / dmax, 1.0)
Image.fromarray((dn * 255).astype(np.uint8)).resize((c.shape[1], c.shape[0]), Image.BILINEAR).save(out)
print('spread map ->', out, '| changed area', round(float(m.mean()) * 100, 1), '% | reached from seed', round(float(reach.sum() / m.sum()) * 100), '%')
