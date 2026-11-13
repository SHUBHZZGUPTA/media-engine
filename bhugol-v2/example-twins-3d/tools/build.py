# Builds the same-size countries HyperFrames project. Usage: python3 build.py <spec.json> <timing.json> <out_dir> [en|hi] [--preview=N] [--allow-gaps]
import json, os, sys, shutil
args = [x for x in sys.argv[1:] if not x.startswith('--')]; spec_p, tim_p, out = args[:3]; LANG = args[3] if len(args) > 3 else 'en'
PREVIEW = next((float(x.split('=')[1]) for x in sys.argv if x.startswith('--preview=')), None)
MOT = '/home/claude/media-engine/bhugol-v2/motion'; sys.path.insert(0, MOT); import motion_plan
W = '/home/claude/work/twins'; ART = W + '/art'; NM = '/home/claude/hf/node_modules'
SPEC = json.load(open(spec_p)); TIM = json.load(open(tim_p)); os.makedirs(os.path.join(out, 'assets'), exist_ok=True)
LAST = TIM['lines'][-1]; DUR = round(LAST['end'] + SPEC.get('tail', .35) + .9, 3); END_START = DUR
chunks = []
for li, L in enumerate(SPEC['lines']):
    w0 = 0; ws = TIM['lines'][li]['words']
    for ci, c in enumerate(L['chunks']):
        n = len(c.replace('|', ' ').split(' '))
        sn = ws[min(w0, len(ws) - 1)] - .06; wt = [ws[min(w0 + k, len(ws) - 1)] - .03 for k in range(n)]
        chunks.append({'li': li, 'ci': ci, 'txt': c, 'sn': sn, 'wt': wt, 'w0': w0}); w0 += n
for i, c in enumerate(chunks): c['en'] = chunks[i + 1]['sn'] if i < len(chunks) - 1 else DUR + 1
Cd = {f'{c["li"]}.{c["ci"]}': round(c['sn'], 3) for c in chunks}
LN = [{'a': L['start'], 'b': L['end']} for L in TIM['lines']]
def C(li, ci=0, off=0.0): return max(0.0, round(Cd[f'{li}.{ci}'] + off, 3))
def wordT(li, ci, word, off=0.0):
    ch = next(c for c in chunks if c['li'] == li and c['ci'] == ci); toks = ch['txt'].replace('|', ' ').replace('*', '').split(' ')
    k = next((i for i, w in enumerate(toks) if word.upper() in w.upper()), None)
    if k is None: print('  word not found:', word, 'in', li, ci, toks)
    return round((ch['wt'][k] if k is not None else ch['sn']) + off, 3)
def at(b, key='at', wkey='word'):
    a = b[key]; off = a[2] if len(a) > 2 else 0
    return wordT(a[0], a[1], b[wkey], off) if b.get(wkey) else C(*a)
PLAN = motion_plan.plan(SPEC, C)
for w in motion_plan.check(PLAN): print('motion check:', w)
BEATS = []
for b in SPEC.get('beats', []):
    if b.get('lang') not in (None, LANG): continue
    d = dict(b, t=at(b))
    if 'until' in b: d['u'] = C(*b['until'])
    if 'off' in b: d['off'] = C(*b['off'])
    if isinstance(b.get('back'), list): d['back'] = C(*b['back'])
    BEATS.append(d)
LABELS = []
for b in SPEC.get('labels', []):
    d = dict(b, t=at(b), u=C(*b['until']))
    if 'fall' in b: d['fall'] = wordT(b['fall'][0], b['fall'][1], b['fallword'], b['fall'][2]) if b.get('fallword') else C(*b['fall'])
    LABELS.append(d)
TITLES = [('tHook', ['*10* COUNTRIES', '~5 SAME-SIZE TWINS'], .3, C(0, 2, -.2), {})]
geo = json.load(open(ART + '/geo.json')); shapes = json.load(open(ART + '/shapes.json'))
D = {'beats': BEATS, 'labels': LABELS, 'shots': PLAN, 'dur': DUR, 'lang': LANG, 'C': Cd, 'LN': LN, 'chunks': [{k: c[k] for k in ('li', 'ci', 'txt', 'sn', 'en', 'wt')} for c in chunks],
     'titles': [dict(id=a, lines=b, a=c, b=d, **o) for a, b, c, d, o in TITLES], 'loopPose': {'lon': 74, 'lat': 18, 'dist': 3.4},
     'maps': {s: json.load(open(f'{ART}/{s}/map3d.json')) for s in ('sa', 'wa', 'zc', 'it', 'sea')}, 'geo': geo, 'shapes': shapes,
     'face': {'gb': [370, 330, .9], 'my': [440, 300, .62], 'vn': [300, 190, .62]},
     'hand': [], 'impacts': [C(*x) for x in SPEC.get('impacts', [])]}
for s in ('sa', 'wa', 'zc', 'it', 'sea'):
    os.makedirs(os.path.join(out, 'assets', s), exist_ok=True)
    for f in ('ne.jpg', 'pa_close.jpg', 'pa_mask.png', 'hillshade.png', 'dem8.png', 'flags.jpg'): shutil.copy(os.path.join(ART, s, f), os.path.join(out, 'assets', s, f))
shutil.copy(ART + '/globe_flags.jpg', out + '/assets/globe_flags.jpg')
for iso in ('GB', 'CL', 'ZM', 'PH', 'MY', 'VN'): shutil.copy(f'{W}/flags/{iso}.png', f'{out}/assets/flag_{iso}.png')
for k in ('gb', 'my', 'vn'): shutil.copy(f'{W}/flags/{k.upper()}.png', f'{out}/assets/flag_{k}.png')
FONTS = {'bsd900.woff2': 'big-shoulders-display/files/big-shoulders-display-latin-900-normal.woff2', 'bsd800.woff2': 'big-shoulders-display/files/big-shoulders-display-latin-800-normal.woff2',
         'arch800.woff2': 'archivo/files/archivo-latin-800-normal.woff2', 'muk800.woff2': 'mukta/files/mukta-devanagari-800-normal.woff2', 'muk700.woff2': 'mukta/files/mukta-devanagari-700-normal.woff2'}
for dst, src in FONTS.items(): shutil.copy(os.path.join(NM, '@fontsource', src), os.path.join(out, 'assets', dst))
shutil.copy('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', os.path.join(out, 'assets/emoji.ttf'))
shutil.copy(W + '/art/bhugol_badge.png', os.path.join(out, 'assets/bhugol_badge.png'))
shutil.copy(os.path.join(NM, 'gsap/dist/gsap.min.js'), os.path.join(out, 'gsap.min.js'))
shutil.copy(os.path.join(NM, 'three/build/three.min.js'), os.path.join(out, 'three.min.js'))
shutil.copy(os.path.join(MOT, 'motion.js'), os.path.join(out, 'motion.js')); shutil.copy(os.path.join(MOT, 'shader_xfade.js'), os.path.join(out, 'shader_xfade.js'))
_end = min(LAST['end'], PREVIEW) if PREVIEW else LAST['end']
VIS = [b for b in BEATS if b['kind'] != 'impact'] + [{'t': l['t']} for l in LABELS]
_G = motion_plan.gaps(PLAN, [{'t': b['t']} for b in VIS], _end, extra=[t[2] for t in TITLES])
for a, b in _G: print(f'PLAN GAP {a:.1f}-{b:.1f} s ({b - a:.1f} s)')
_SG = motion_plan.sharp_gaps(PLAN, [{'t': b['t'], 'kind': b['kind']} for b in BEATS], _end)
for a, b in _SG: print(f'SHARP GAP {a:.1f}-{b:.1f} s ({b - a:.1f} s)')
if (_G or _SG) and '--allow-gaps' not in sys.argv: sys.exit('plan check failed')
print('plan check: ok 0-%.1f s' % _end)
if PREVIEW: D['dur'] = DUR = PREVIEW
if '--thumb' in sys.argv: D['thumb'] = True
FR = next((float(x.split('=')[1]) for x in sys.argv if x.startswith('--from=')), None); TO = next((float(x.split('=')[1]) for x in sys.argv if x.startswith('--to=')), None)
CHUNK_DUR = None
if TO is not None: D['t0'] = FR; D['t1'] = min(TO, DUR); CHUNK_DUR = round(D['t1'] - FR, 4)
tpl = open(W + '/tpl/template.html').read().replace('__MBLUR__', '')
open(os.path.join(out, 'index.html'), 'w').write(tpl.replace('__DATA__', json.dumps(D, ensure_ascii=False)).replace('__DUR__', str(CHUNK_DUR or DUR)))
json.dump({'dur': DUR, 'end': END_START, 'shots': [{'t': p['t'], 'cut': p['cut'], 'scene': p['scene']} for p in PLAN], 'beats': [{'kind': b['kind'], 't': b['t']} for b in BEATS],
           'sections': {k: [[0 if a == [0, 0, -.5] else C(*a), 'end' if z == 'end' else C(*z), lv] for a, z, lv in v] for k, v in SPEC.get('music_sections', {}).items()}, 'story': []}, open(os.path.join(out, 'times.json'), 'w'), indent=1)
print('built', out, 'dur', DUR)
