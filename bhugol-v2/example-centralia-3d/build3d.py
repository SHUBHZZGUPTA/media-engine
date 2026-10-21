# Builds the 3D HyperFrames project for Centralia. Usage: python3 build3d.py <spec.json> <timing_final.json> <out_dir> [en|hi]
import json, os, sys, shutil
from PIL import Image
spec_p, tim_p, out = sys.argv[1:4]; LANG = sys.argv[4] if len(sys.argv) > 4 else 'en'
HERE = os.path.dirname(os.path.abspath(__file__)); ART = os.path.join(HERE, 'art'); KIT = '/home/claude/bhugol-kit'
SPEC = json.load(open(spec_p)); TIM = json.load(open(tim_p)); os.makedirs(os.path.join(out, 'assets'), exist_ok=True)
LAST = TIM['lines'][-1]; END_START = round(LAST['start'] - .25, 3); DUR = TIM.get('dur') or round(LAST['end'] + 2.3, 3)
chunks = []
for li, L in enumerate(SPEC['lines']):
    w0 = 0; ws = TIM['lines'][li]['words']
    for ci, c in enumerate(L['chunks']):
        n = len(c.replace('|', ' ').split(' '))
        chunks.append({'li': li, 'ci': ci, 'txt': c, 'sn': ws[min(w0, len(ws) - 1)] - .06, 'wt': [ws[min(w0 + k, len(ws) - 1)] - .03 for k in range(n)]}); w0 += n
for i, c in enumerate(chunks): c['en'] = chunks[i + 1]['sn'] if i < len(chunks) - 1 else DUR + 1
Cd = {f'{c["li"]}.{c["ci"]}': round(c['sn'], 3) for c in chunks}
LN = [{'a': L['start'], 'b': L['end']} for L in TIM['lines']]
def C(li, ci=0, off=0.0): return round(Cd[f'{li}.{ci}'] + off, 3)
AR = {}
for n in ('c_fire', 'c_centralia'):
    im = Image.open(os.path.join(ART, n + '.png')); AR[n] = round(im.width / im.height, 4)
for f in os.listdir(ART):
    if f.endswith(('.jpg', '.png')): shutil.copy(os.path.join(ART, f), os.path.join(out, 'assets', f))
HI = LANG == 'hi'
TITLES = [('tFog', ['ये *धुंध* नहीं 🔥' if HI else "THAT'S NOT *FOG* 🔥"], .3, C(0, 1, -.1)), ('t1962', ['*1962*'], C(1, 0), C(1, 1, -.1)),
          ('tPA', ['~PENNSYLVANIA, USA'], C(1, 1), C(2, 0, -.2)), ('t42k', ['*$42,000*'], C(5, 2), C(5, 3, .6)), ('t1979', ['*1979*'], C(7, 0), C(7, 1, -.1)),
          ('t1981', ['*1981*'], C(9, 0), C(9, 1, -.1)), ('tZIP', ['ZIP *17927* ❌'], C(14, 2), C(15, 0, -.15)), ('t250', ['*+250 साल?*' if HI else '*+250 YEARS?*'], C(16, 2), C(17, 0, -.15))]
I18N = {'CENTRALIA': 'सेंट्रेलिया', 'OLD MINE TUNNELS': 'पुरानी खदानें', '45 m': '45 मीटर'} if HI else {}
PT = {'road': [512, 790], 'pit': [630, 720], 'hole': [512, 770], 'grid': [20, 140, 900, 780]}
D = {'dur': DUR, 'lang': LANG, 'C': Cd, 'LN': LN, 'chunks': [{k: c[k] for k in ('txt', 'sn', 'en', 'wt')} for c in chunks],
     'titles': [dict(id=a, lines=b, a=c, b=d) for a, b, c, d in TITLES], 'ar': AR, 'pt': PT, 'i18n': I18N, 'map3': json.load(open(os.path.join(ART, 'map3d.json'))),
     'end': {'start': END_START, 'btn': round(END_START + .8, 3), 'tap': round(END_START + 2.0, 3), 'button': 'फॉलो करें BHUGOL' if HI else 'FOLLOW BHUGOL', 'following': 'FOLLOWING'}}
FONTS = {'bsd900.woff2': 'big-shoulders-display/files/big-shoulders-display-latin-900-normal.woff2', 'bsd800.woff2': 'big-shoulders-display/files/big-shoulders-display-latin-800-normal.woff2',
         'arch800.woff2': 'archivo/files/archivo-latin-800-normal.woff2', 'muk800.woff2': 'mukta/files/mukta-devanagari-800-normal.woff2', 'muk700.woff2': 'mukta/files/mukta-devanagari-700-normal.woff2'}
for dst, src in FONTS.items(): shutil.copy(os.path.join(KIT, 'node_modules/@fontsource', src), os.path.join(out, 'assets', dst))
shutil.copy('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', os.path.join(out, 'assets/emoji.ttf'))
shutil.copy(os.path.join(KIT, 'assets/bhugol_badge.png'), os.path.join(out, 'assets/bhugol_badge.png'))
shutil.copy('/home/claude/work/node_modules/gsap/dist/gsap.min.js', os.path.join(out, 'gsap.min.js'))
shutil.copy('/home/claude/work/node_modules/three/build/three.min.js', os.path.join(out, 'three.min.js'))
tpl = open(os.path.join(HERE, 'template3d.html')).read()
open(os.path.join(out, 'index.html'), 'w').write(tpl.replace('__DATA__', json.dumps(D, ensure_ascii=False)).replace('__DUR__', '%.3f' % DUR))
json.dump({'dur': DUR, 'end': D['end'], 'C': Cd}, open(os.path.join(out, 'times.json'), 'w'), indent=1)
print('built', out, 'dur', DUR)
