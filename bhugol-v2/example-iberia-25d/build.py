# Build the HyperFrames project for the Iberia what-if Short.
# Usage: python3 build.py <out_dir> [--from=a --to=b for a render slice]
import json, os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1]; HI = len(sys.argv) > 2 and sys.argv[2] == 'hi'
S = json.load(open(os.path.join(HERE, 'script_hi.json' if HI else 'script.json'))); TIM = json.load(open(os.path.join(HERE, 'audio_hi/timing.json' if HI else 'audio/timing.json')))
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
WIDE = dict(x=4600, y=6960, z=.42, tilt=0, rot=0)
K = [dict(at=0, dur=0, **WIDE)]
def k(at, dur, x, y, z, tilt=0, ease='glide', **o): K.append(dict(at=round(at, 3), dur=round(dur, 3), x=x, y=y, z=z, tilt=tilt, ease=ease, **o))
k(C(0, 2, -.2), 1.0, 4580, 6990, .45, 10, 'soft')
k(C(1, 1, -.2), 1.0, 4550, 7050, .45, 12)
k(C(2, 0, -.1), 1.1, 3820, 7120, .72, 14, 'snap')
k(C(3, 0, -.1), 1.0, 4150, 7060, .6, 10)
k(C(3, 2, -.15), 1.0, 4600, 7110, .42, 8)
k(C(4, 0, -.1), .9, 4600, 7080, .40, 16, 'snap')
k(C(5, 0, -.1), 1.0, 4600, 7050, .44, 8)
k(C(6, 0, -.1), 1.0, 4620, 7150, .42, 14)
k(C(7, 0, -.1), 1.0, 4600, 7060, .46, 0)
k(C(8, 0, -.1), .9, 3900, 7060, .85, 10, 'snap')
k(C(9, 0, .1), 1.2, 4250, 7060, .52, 16)
k(C(10, 0, -.1), 1.0, 3850, 7040, .8, 10)
k(C(11, 0, -.1), 1.0, 3900, 7080, .7, 14)
k(C(12, 0, -.1), 1.0, 4450, 7100, .45, 8)
k(C(13, 0, -.25), .8, 4003, 7210, 1.25, 18, 'snap')
k(C(14, 0, .1), 1.2, 4003, 7200, 1.1, 10)
k(C(15, 0, -.1), 1.0, 4120, 7080, .72, 14)
k(C(16, 0, -.2), .6, 3880, 7060, .85, 10, 'snap')
tE = C(17, 1, -.1); k(tE, DUR - .08 - tE, WIDE['x'], WIDE['y'], WIDE['z'], 0, 'glide')
LN = [{'a': L['start'], 'b': L['end']} for L in TIM['lines']]
D = {'dur': DUR, 'map': MAP, 'cities': MAP['cities'], 'C': Cd, 'LN': LN, 'chunks': chunks, 'cam': K, 'drift': .006,
     'cover': (['🇪🇸 + 🇵🇹', 'फिर से <span class="box">एक देश?</span>'] if HI else ['🇪🇸 + 🇵🇹', 'ONE COUNTRY <span class="box">AGAIN?</span>']), 'bubble': 'NATA BEATS CHURROS! 😤', 'lang': 'hi' if HI else 'en'}
A = os.path.join(OUT, 'assets'); W = '/home/claude/work/node_modules'
for f in ('detail.jpg', 'context.jpg', 'flag_ESP.png', 'flag_PRT.png'): shutil.copy(os.path.join(HERE, 'assets', f), A)
shutil.copy(W + '/@fontsource/big-shoulders-display/files/big-shoulders-display-latin-900-normal.woff2', A + '/bsd900.woff2')
shutil.copy(W + '/@fontsource/big-shoulders-display/files/big-shoulders-display-latin-800-normal.woff2', A + '/bsd800.woff2')
shutil.copy(W + '/@fontsource/archivo/files/archivo-latin-800-normal.woff2', A + '/arch800.woff2')
shutil.copy(W + '/@fontsource/mukta/files/mukta-devanagari-800-normal.woff2', A + '/muk800.woff2')
shutil.copy('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', A + '/emoji.ttf')
shutil.copy('/home/claude/media-engine/citylapse/engine/assets/bhugol_badge.png', A + '/bhugol_badge.png')
shutil.copy(W + '/gsap/dist/gsap.min.js', OUT)
shutil.copy('/home/claude/media-engine/bhugol-v2/motion/motion.js', OUT)
tpl = open(os.path.join(HERE, 'template.html')).read()
open(os.path.join(OUT, 'index.html'), 'w').write(tpl.replace('__DATA__', json.dumps(D)).replace('__DUR__', '%.3f' % DUR))
json.dump({'dur': DUR, 'C': Cd, 'LN': LN, 'cam': K}, open(os.path.join(OUT, 'times.json'), 'w'), indent=1)
print('built', OUT, 'dur', DUR, 'chunks', len(chunks), 'cam keys', len(K))
