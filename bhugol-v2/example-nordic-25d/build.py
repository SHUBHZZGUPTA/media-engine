# Build the HyperFrames project for the Nordic what-if Short.
# Usage: python3 build.py <out_dir> [--from=a --to=b for a render slice]
import json, os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1]
S = json.load(open(os.path.join(HERE, 'script.json'))); TIM = json.load(open(os.path.join(HERE, 'audio/timing.json')))
MAP = json.load(open(os.path.join(HERE, 'assets/map.json')))
os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
DUR = round(TIM['lines'][-1]['end'] + .2, 3)
chunks, Cd = [], {}
for li, L in enumerate(S['lines']):
    for ci, txt in enumerate(L['chunks']):
        tk = TIM['lines'][li]['chunks'][ci]['tok']; caps = txt.split(' ')
        wt = [round(tk[min(len(tk) - 1, int(k * len(tk) / len(caps)))] - .03, 3) for k in range(len(caps))]
        sn = round(tk[0] - .06, 3); chunks.append({'txt': txt, 'sn': sn, 'wt': wt}); Cd[f'{li}.{ci}'] = round(tk[0], 3)
for i, c in enumerate(chunks): c['en'] = chunks[i + 1]['sn'] if i < len(chunks) - 1 else DUR - .45
def C(li, ci=0, off=0.0): return round(Cd[f'{li}.{ci}'] + off, 3)
WIDE = dict(x=3290, y=4100, z=.245, tilt=0, rot=0)
K = [dict(at=0, dur=0, **WIDE)]
def k(at, dur, x, y, z, tilt=0, ease='glide', **o): K.append(dict(at=round(at, 3), dur=round(dur, 3), x=x, y=y, z=z, tilt=tilt, ease=ease, **o))
k(C(0, 3, -.2), 1.2, 3420, 4450, .27, 8, 'soft')
k(C(1, 0, -.2), 1.1, 4450, 4950, .5, 14)
k(C(1, 3, -.25), .9, 3800, 4880, .36, 12)
k(C(2, 0, -.1), 1.3, 3450, 4300, .26, 20, 'snap')
k(C(3, 0, .1), 1.2, 2300, 3500, .40, 12)
k(C(4, 0, -.15), 1.0, 3500, 4550, .25, 4)
k(C(5, 0, -.1), 1.0, 4000, 4800, .32, 16)
k(C(6, 0, -.1), 1.1, 4450, 5080, .95, 22)
k(C(7, 0, -.1), .9, 3420, 4450, .27, 0, 'snap')
k(C(9, 0, -.1), 1.2, 4650, 5150, .55, 16)
k(C(9, 5, -.3), 1.0, 4890, 5400, 1.05, 20)
k(C(10, 0, .2), 2.5, 4800, 5250, .8, 14, 'soft')
k(C(11, 0, -.1), 1.0, 4720, 4980, .66, 10)
k(C(12, 2, -.2), 1.0, 4800, 4960, .6, 12)
k(C(14, 0, -.15), 1.0, 4000, 5000, .36, 10)
k(C(15, 0, -.1), 1.0, 4800, 5230, .82, 18)
k(C(16, 0, -.25), .55, 2700, 4770, .95, 12, 'snap')
k(C(17, 0, -.15), .8, 4890, 5420, 1.25, 20, 'snap')
tE = C(18, 1, -.1); k(tE, DUR - .08 - tE, WIDE['x'], WIDE['y'], WIDE['z'], 0, 'glide')
LN = [{'a': L['start'], 'b': L['end']} for L in TIM['lines']]
D = {'dur': DUR, 'map': MAP, 'cities': MAP['cities'], 'C': Cd, 'LN': LN, 'chunks': chunks, 'cam': K, 'drift': .006,
     'cover': ['5 COUNTRIES,', '<span class="box">1 FLAG?</span>']}
A = os.path.join(OUT, 'assets'); W = '/home/claude/work/node_modules'
for f in ('detail.jpg', 'context.jpg'): shutil.copy(os.path.join(HERE, 'assets', f), A)
shutil.copy(W + '/@fontsource/big-shoulders-display/files/big-shoulders-display-latin-900-normal.woff2', A + '/bsd900.woff2')
shutil.copy(W + '/@fontsource/big-shoulders-display/files/big-shoulders-display-latin-800-normal.woff2', A + '/bsd800.woff2')
shutil.copy(W + '/@fontsource/archivo/files/archivo-latin-800-normal.woff2', A + '/arch800.woff2')
shutil.copy('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', A + '/emoji.ttf')
shutil.copy('/home/claude/media-engine/citylapse/engine/assets/bhugol_badge.png', A + '/bhugol_badge.png')
shutil.copy(W + '/gsap/dist/gsap.min.js', OUT)
shutil.copy('/home/claude/media-engine/bhugol-v2/motion/motion.js', OUT)
tpl = open(os.path.join(HERE, 'template.html')).read()
open(os.path.join(OUT, 'index.html'), 'w').write(tpl.replace('__DATA__', json.dumps(D)).replace('__DUR__', '%.3f' % DUR))
json.dump({'dur': DUR, 'C': Cd, 'LN': LN, 'cam': K}, open(os.path.join(OUT, 'times.json'), 'w'), indent=1)
print('built', OUT, 'dur', DUR, 'chunks', len(chunks), 'cam keys', len(K))
