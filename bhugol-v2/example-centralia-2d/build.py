# Builds the HyperFrames project for the BHUGOL Centralia Short (v2 pipeline).
# Usage: python3 build.py <spec.json> <timing.json> <out_dir> [en|hi]
import json, os, sys, shutil
from PIL import Image

spec_p, tim_p, out = sys.argv[1:4]
LANG = sys.argv[4] if len(sys.argv) > 4 else 'en'
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = '/home/claude/bhugol-kit'; ART = os.path.join(HERE, 'art')
SPEC = json.load(open(spec_p)); TIM = json.load(open(tim_p))
os.makedirs(os.path.join(out, 'assets'), exist_ok=True)
LAST = TIM['lines'][-1]
END_START = round(LAST['start'] - .25, 3)
DUR = TIM.get('dur') or round(LAST['end'] + SPEC.get('tail', 2.3), 3)

# ---- caption chunks (real seconds) ----
chunks = []
for li, L in enumerate(SPEC['lines']):
    w0 = 0
    for ci, c in enumerate(L['chunks']):
        n = len(c.replace('|', ' ').split(' '))
        ws = TIM['lines'][li]['words']
        chunks.append({'li': li, 'ci': ci, 'txt': c, 'sn': ws[min(w0, len(ws) - 1)] - .06,
                       'wt': [ws[min(w0 + k, len(ws) - 1)] - .03 for k in range(n)]})
        w0 += n
for i, c in enumerate(chunks): c['en'] = chunks[i + 1]['sn'] if i < len(chunks) - 1 else DUR + 1
Cd = {f'{c["li"]}.{c["ci"]}': round(c['sn'], 3) for c in chunks}
LN = [{'a': L['start'], 'b': L['end']} for L in TIM['lines']]
def C(li, ci=0, off=0.0): return round(Cd[f'{li}.{ci}'] + off, 3)
MOT = '/home/claude/media-engine/bhugol-v2/motion'; sys.path.insert(0, MOT); import motion_plan
PLAN = motion_plan.plan(SPEC, C)
for w in motion_plan.check(PLAN): print('motion check:', w)

# ---- art ----
AR = {}
for n in ('c_fire', 'c_centralia'):
    im = Image.open(os.path.join(ART, n + '.png')).convert('RGBA'); im = im.crop(im.getbbox()); im.thumbnail((900, 900))
    im.save(os.path.join(out, 'assets', n + '.png'), optimize=True); AR[n] = round(im.width / im.height, 4)
PL = {}
for n in ('plate_road', 'plate_pit', 'plate_hole', 'plate_town', 'xsec', 'map_ne'):
    im = Image.open(os.path.join(ART, n + ('.jpg' if n in ('xsec', 'map_ne') else '.png'))).convert('RGB')
    im.save(os.path.join(out, 'assets', n + '.jpg'), quality=90); PL[n] = im.size
MAP = json.load(open(os.path.join(ART, 'map_ne.json')))
PT = json.load(open(os.path.join(ART, 'points.json')))

HI = LANG == 'hi'
TITLES = [  # id, lines, start, end
    ('tFog', ['ये *धुंध* नहीं 🔥' if HI else "THAT'S NOT *FOG* 🔥"], .3, C(0, 1, -.1)),
    ('t1962', ['*1962*'], C(1, 0), C(1, 1, -.1)),
    ('tPA', ['~PENNSYLVANIA, USA'], C(1, 1), C(2, 0, -.2)),
    ('t42k', ['*$42,000*'], C(5, 2), C(5, 3, .6)),
    ('t1979', ['*1979*'], C(7, 0), C(7, 1, -.1)),
    ('t1981', ['*1981*'], C(9, 0), C(9, 1, -.1)),
    ('tZIP', ['ZIP *17927* ❌'], C(14, 2), C(15, 0, -.15)),
    ('t250', ['*+250 साल?*' if HI else '*+250 YEARS?*'], C(16, 2), C(17, 0, -.15)),
]
I18N = {'CENTRALIA': 'सेंट्रेलिया', 'OLD MINE TUNNELS': 'पुरानी खदानें', '45 m': '45 मीटर'} if HI else {}
D = {'beats': [dict(b, t=C(*b['at'])) for b in SPEC.get('beats', [])], 'shots': PLAN, 'dur': DUR, 'lang': LANG, 'C': Cd, 'LN': LN, 'chunks': [{k: c[k] for k in ('txt', 'sn', 'en', 'wt')} for c in chunks],
     'titles': [dict(id=a, lines=b, a=c, b=d) for a, b, c, d in TITLES], 'ar': AR, 'pl': PL, 'map': MAP, 'pt': PT, 'i18n': I18N,
     'end': {'start': END_START, 'btn': round(END_START + .8, 3), 'tap': round(END_START + 2.0, 3),
             'button': 'फॉलो करें BHUGOL' if HI else 'FOLLOW BHUGOL', 'following': 'FOLLOWING'}}

FONTS = {'bsd900.woff2': 'big-shoulders-display/files/big-shoulders-display-latin-900-normal.woff2',
         'bsd800.woff2': 'big-shoulders-display/files/big-shoulders-display-latin-800-normal.woff2',
         'arch800.woff2': 'archivo/files/archivo-latin-800-normal.woff2',
         'muk800.woff2': 'mukta/files/mukta-devanagari-800-normal.woff2',
         'muk700.woff2': 'mukta/files/mukta-devanagari-700-normal.woff2'}
for dst, src in FONTS.items(): shutil.copy(os.path.join(KIT, 'node_modules/@fontsource', src), os.path.join(out, 'assets', dst))
shutil.copy('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', os.path.join(out, 'assets/emoji.ttf'))
shutil.copy(os.path.join(KIT, 'assets/bhugol_badge.png'), os.path.join(out, 'assets/bhugol_badge.png'))
shutil.copy('/home/claude/work/node_modules/gsap/dist/gsap.min.js', os.path.join(out, 'gsap.min.js'))
shutil.copy(os.path.join(MOT, 'motion.js'), os.path.join(out, 'motion.js'))
tpl = open(os.path.join(HERE, 'template.html')).read()
open(os.path.join(out, 'index.html'), 'w').write(tpl.replace('__DATA__', json.dumps(D, ensure_ascii=False)).replace('__DUR__', '%.3f' % DUR))
json.dump({'dur': DUR, 'end': D['end'], 'C': Cd, 'LN': LN}, open(os.path.join(out, 'times.json'), 'w'), indent=1)
print('built', out, 'dur', DUR, 'end', END_START)
