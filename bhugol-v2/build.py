# Builds the HyperFrames project for the BHUGOL Budapest Short (v2 pipeline: Gemini voice + Codex art).
# Usage: python3 build.py <spec.json> <timing_final.json> <out_dir>
import json, math, os, sys, shutil
from PIL import Image

spec_p, tim_p, out = sys.argv[1:4]
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = '/home/claude/bhugol-kit'; ART = os.path.join(HERE, 'art')
SPEC = json.load(open(spec_p)); TIM = json.load(open(tim_p)); DUR = TIM['dur']
os.makedirs(os.path.join(out, 'assets'), exist_ok=True)

# ---- caption chunks (real seconds) ----
chunks = []
for li, L in enumerate(SPEC['lines']):
    w0 = 0; row = []
    for ci, c in enumerate(L['chunks']):
        n = len(c.replace('|', ' ').split(' '))
        row.append({'li': li, 'ci': ci, 'txt': c, 'sn': TIM['lines'][li]['words'][w0] - .06,
                    'wt': [TIM['lines'][li]['words'][w0 + k] - .03 for k in range(n)]})
        w0 += n
    chunks.append(row)
flat = [c for r in chunks for c in r]
for i, c in enumerate(flat): c['en'] = flat[i + 1]['sn'] if i < len(flat) - 1 else DUR + 1
Cd = {f'{c["li"]}.{c["ci"]}': round(c['sn'], 3) for c in flat}
LN = [{'a': L['start'], 'b': L['end'], 'spk': SPEC['lines'][i].get('speaker')} for i, L in enumerate(TIM['lines'])]

# ---- Europe map (Web Mercator image) ----
EU = json.load(open(os.path.join(HERE, 'img/europe.json')))
def merc(lon, lat):
    l0, b0, l1, b1 = EU['bbox']; my = lambda la: math.log(math.tan(math.pi / 4 + math.radians(la) / 2))
    return {'x': round((lon - l0) / (l1 - l0) * EU['w'], 1), 'y': round((my(b1) - my(lat)) / (my(b1) - my(b0)) * EU['h'], 1)}
EUP = {'bud': merc(19.04, 47.50), 'vie': merc(16.37, 48.21)}

# ---- art: trimmed characters + plates ----
AR = {}
for n in ('c_buda', 'c_pest', 'c_obuda', 'c_count', 'c_noble', 'c_toll'):
    im = Image.open(os.path.join(ART, n + '.png')).convert('RGBA'); im = im.crop(im.getbbox()); im.thumbnail((900, 900))
    im.save(os.path.join(out, 'assets', n + '.png'), optimize=True); AR[n] = round(im.width / im.height, 4)
PL = {}
for n in ('plate_aerial', 'plate_river', 'plate_toll'):
    im = Image.open(os.path.join(ART, n + '.png')).convert('RGB'); im.save(os.path.join(out, 'assets', n + '.jpg'), quality=90); PL[n] = im.size
shutil.copy(os.path.join(HERE, 'img/europe.jpg'), os.path.join(out, 'assets/europe.jpg')); PL['europe'] = (EU['w'], EU['h'])

def C(li, ci=0, off=0.0): return round(Cd[f'{li}.{ci}'] + off, 3)
E = SPEC['end']
TITLES = [  # id, lines, start, end
    ('t1873', ['BEFORE *1873*'], .35, C(0, 3, -.1)),
    ('t1820', ['*1820*', '~COUNT SZÉCHENYI'], C(8, 1), C(9, 0, -.1)),
    ('tChain', ['*CHAIN BRIDGE*', '~1849'], C(12, 0), C(12, 1, -.1)),
    ('t1873b', ['*1873*'], C(14, 1), C(14, 2, -.1)),
    ('tEq', ['*BUDA* + *PEST*'], C(14, 2), C(14, 3, -.05)),
    ('tBP', ['*BUDAPEST*'], C(14, 3), C(15, 0, -.05)),
]
D = {'dur': DUR, 'C': Cd, 'LN': LN, 'chunks': [{k: c[k] for k in ('txt', 'sn', 'en', 'wt')} for c in flat],
     'titles': [dict(id=a, lines=b, a=c, b=d) for a, b, c, d in TITLES], 'ar': AR, 'pl': PL, 'eu': EUP,
     'end': {'start': E['start'], 'btn': E['button_at'], 'tap': E['tap_at'], 'button': E['button'], 'following': 'FOLLOWING'}}

FONTS = {'bsd900.woff2': 'big-shoulders-display/files/big-shoulders-display-latin-900-normal.woff2',
         'bsd800.woff2': 'big-shoulders-display/files/big-shoulders-display-latin-800-normal.woff2',
         'arch800.woff2': 'archivo/files/archivo-latin-800-normal.woff2'}
for dst, src in FONTS.items(): shutil.copy(os.path.join(KIT, 'node_modules/@fontsource', src), os.path.join(out, 'assets', dst))
shutil.copy('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', os.path.join(out, 'assets/emoji.ttf'))
shutil.copy(os.path.join(KIT, 'assets/bhugol_badge.png'), os.path.join(out, 'assets/bhugol_badge.png'))
shutil.copy('/home/claude/egypt-hf/node_modules/gsap/dist/gsap.min.js', os.path.join(out, 'gsap.min.js'))
tpl = open(os.path.join(HERE, 'template.html')).read()
open(os.path.join(out, 'index.html'), 'w').write(tpl.replace('__DATA__', json.dumps(D, ensure_ascii=False)).replace('__DUR__', '%.3f' % DUR))
print('built', out, 'dur', DUR)
