# Builds the Baikal HyperFrames project. Usage: python3 build.py <spec.json> <timing.json> <out_dir> [en|hi] [--preview=N] [--allow-gaps]
import json, os, sys, shutil
args = [x for x in sys.argv[1:] if not x.startswith('--')]; spec_p, tim_p, out = args[:3]; LANG = args[3] if len(args) > 3 else 'en'
PREVIEW = next((float(x.split('=')[1]) for x in sys.argv if x.startswith('--preview=')), None)
MOT = '/home/claude/media-engine/bhugol-v2/motion'; sys.path.insert(0, MOT); import motion_plan
HERE = os.path.dirname(os.path.abspath(__file__)); W = '/home/claude/work/baikal'; ART = W + '/art'; KIT = '/home/claude/bhugol-kit'; NM = '/home/claude/hf/node_modules'
SPEC = json.load(open(spec_p)); TIM = json.load(open(tim_p)); os.makedirs(os.path.join(out, 'assets'), exist_ok=True)
LAST = TIM['lines'][-1]; END_START = round(LAST['start'] - .25, 3); DUR = round(LAST['end'] + 2.3, 3)
chunks = []
for li, L in enumerate(SPEC['lines']):
    w0 = 0; ws = TIM['lines'][li]['words']
    for ci, c in enumerate(L['chunks']):
        n = len(c.replace('|', ' ').split(' '))
        if 'chunk_t' in L:   # Hindi with English captions: chunk times given directly
            sn = L['chunk_t'][ci]; wt = [sn + k * .01 for k in range(n)]
        else:
            sn = ws[min(w0, len(ws) - 1)] - .06; wt = [ws[min(w0 + k, len(ws) - 1)] - .03 for k in range(n)]
        chunks.append({'li': li, 'ci': ci, 'txt': c, 'sn': sn, 'wt': wt, 'w0': w0}); w0 += n
for i, c in enumerate(chunks): c['en'] = chunks[i + 1]['sn'] if i < len(chunks) - 1 else DUR + 1
Cd = {f'{c["li"]}.{c["ci"]}': round(c['sn'], 3) for c in chunks}
LN = [{'a': L['start'], 'b': L['end']} for L in TIM['lines']]
def C(li, ci=0, off=0.0): return max(0.0, round(Cd[f'{li}.{ci}'] + off, 3))
def wordT(li, ci, word, off=0.0):   # time of a word inside a chunk (falls back to the chunk start)
    ch = next(c for c in chunks if c['li'] == li and c['ci'] == ci); toks = ch['txt'].replace('|', ' ').replace('*', '').split(' ')
    k = next((i for i, w in enumerate(toks) if word.upper() in w.upper()), None)
    return round((ch['wt'][k] if k is not None else ch['sn']) + off, 3)
PLAN = motion_plan.plan(SPEC, C)
for w in motion_plan.check(PLAN): print('motion check:', w)
def bt(b):
    if 'word' in b: return wordT(b['at'][0], b['at'][1], b['word'], b['at'][2] if len(b['at']) > 2 else 0)
    return C(*b['at'])
BEATS = []
for b in SPEC.get('beats', []):
    if b.get('lang') not in (None, LANG): continue
    d = dict(b, t=bt(b))
    if 'until' in b: d['u'] = C(*b['until'])
    if isinstance(b.get('back'), list): d['back'] = C(*b['back'])
    BEATS.append(d)
TITLES = [('tHook', ['1 LAKE *vs 5*'], .3, C(1, 0, -.2), {}), ('tOld', ['*OLDEST*', '~LAKE ON EARTH'], C(11, 3, -.05), C(12, 0, -.2), {'slam': 1}),
          ('tDepth', ['*DEPTH* WINS'], C(15, 1, .1), C(16, 0, -.2), {'slam': 1})]
geo = json.load(open(ART + '/geo.json')); shapes = json.load(open(W + '/shapes.json'))
D = {'beats': BEATS, 'shots': PLAN, 'dur': DUR, 'lang': LANG, 'C': Cd, 'LN': LN, 'chunks': [{k: c[k] for k in ('li', 'txt', 'sn', 'en', 'wt')} for c in chunks],
     'titles': [dict(id=a, lines=b, a=c, b=d, **o) for a, b, c, d, o in TITLES], 'i18n': {},
     'maps': {'bk': json.load(open(ART + '/bk/map3d.json')), 'gl': json.load(open(ART + '/gl/map3d.json'))}, 'geo': geo, 'shapes': {'sup': shapes['sup'], 'bel': shapes['bel']},
     'hand': [[C(*a), C(*b)] for a, b in SPEC.get('hand', [])], 'impacts': [C(*x) for x in SPEC.get('impacts', [])],
     'end': {'start': END_START, 'btn': round(END_START + .8, 3), 'tap': round(END_START + 2.0, 3), 'button': 'फॉलो करें BHUGOL' if LANG == 'hi' else 'FOLLOW BHUGOL', 'following': 'FOLLOWING'}}
# assets
for d in ('bk', 'gl'):
    os.makedirs(os.path.join(out, 'assets', d), exist_ok=True)
    for f in ('globe.jpg', 'ne.jpg', 'pa_close.jpg', 'pa_mask.png', 'hillshade.png', 'dem8.png'): shutil.copy(os.path.join(ART, d, f), os.path.join(out, 'assets', d, f))
FONTS = {'bsd900.woff2': 'big-shoulders-display/files/big-shoulders-display-latin-900-normal.woff2', 'bsd800.woff2': 'big-shoulders-display/files/big-shoulders-display-latin-800-normal.woff2',
         'arch800.woff2': 'archivo/files/archivo-latin-800-normal.woff2', 'muk800.woff2': 'mukta/files/mukta-devanagari-800-normal.woff2', 'muk700.woff2': 'mukta/files/mukta-devanagari-700-normal.woff2'}
for dst, src in FONTS.items(): shutil.copy(os.path.join(NM, '@fontsource', src), os.path.join(out, 'assets', dst))
shutil.copy('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', os.path.join(out, 'assets/emoji.ttf'))
shutil.copy(os.path.join(KIT, 'assets/bhugol_badge.png'), os.path.join(out, 'assets/bhugol_badge.png'))
shutil.copy(os.path.join(NM, 'gsap/dist/gsap.min.js'), os.path.join(out, 'gsap.min.js'))
shutil.copy(os.path.join(NM, 'three/build/three.min.js'), os.path.join(out, 'three.min.js'))
shutil.copy(os.path.join(MOT, 'motion.js'), os.path.join(out, 'motion.js')); shutil.copy(os.path.join(MOT, 'shader_xfade.js'), os.path.join(out, 'shader_xfade.js'))
# plan checks (whole video unless --preview)
_end = min(END_START, PREVIEW) if PREVIEW else END_START
VIS = [b for b in BEATS if b['kind'] != 'impact']
_G = motion_plan.gaps(PLAN, [{'t': b['t']} for b in VIS], _end, extra=[t[2] for t in TITLES])
for a, b in _G: print(f'PLAN GAP {a:.1f}-{b:.1f} s ({b - a:.1f} s)')
_SG = motion_plan.sharp_gaps(PLAN, [{'t': b['t'], 'kind': b['kind']} for b in BEATS], _end)
for a, b in _SG: print(f'SHARP GAP {a:.1f}-{b:.1f} s ({b - a:.1f} s)')
if (_G or _SG) and '--allow-gaps' not in sys.argv: sys.exit('plan check failed')
print('plan check: ok 0-%.1f s' % _end)
if PREVIEW: D['dur'] = DUR = PREVIEW
tpl = open(os.path.join(HERE, 'template.html')).read().replace('__MBLUR__', open(os.path.join(MOT, 'vendor/motion-blur.html')).read())
open(os.path.join(out, 'index.html'), 'w').write(tpl.replace('__DATA__', json.dumps(D, ensure_ascii=False)).replace('__DUR__', str(DUR)))
json.dump({'dur': DUR, 'end': END_START, 'shots': [{'t': p['t'], 'cut': p['cut'], 'scene': p['scene']} for p in PLAN], 'beats': [{'kind': b['kind'], 't': b['t']} for b in BEATS],
           'sections': {k: [[0 if a == [0, 0, -.5] else C(*a), 'end' if z == 'end' else C(*z), lv] for a, z, lv in v] for k, v in SPEC.get('music_sections', {}).items()}, 'story': SPEC.get('story', [])}, open(os.path.join(out, 'times.json'), 'w'), indent=1)
print('built', out, 'dur', DUR, 'end card', END_START)
