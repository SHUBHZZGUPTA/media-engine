# Builds the 3D HyperFrames project for Bengaluru's lakes (reference build, 22 Oct 2026). Usage: python3 build3d.py <spec.json> <timing_final.json> <out_dir> [en|hi]
import json, os, sys, shutil
from PIL import Image
args = [x for x in sys.argv[1:] if not x.startswith('--')]; spec_p, tim_p, out = args[:3]; LANG = args[3] if len(args) > 3 else 'en'
PREVIEW = next((float(x.split('=')[1]) for x in sys.argv if x.startswith('--preview=')), None)  # --preview=25 renders only the first 25 s
MOT = '/home/claude/media-engine/bhugol-v2/motion'; sys.path.insert(0, MOT); import motion_plan
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
PLAN = motion_plan.plan(SPEC, C)
for w in motion_plan.check(PLAN): print('motion check:', w)
_BT = [C(*b['at']) for b in SPEC.get('beats', [])]   # pre-render plan gap check (any length): titles + beats + cuts
AR = {}
for n in ('c_drop', 'c_bus'):
    im = Image.open(os.path.join(ART, n + '.png')); AR[n] = round(im.width / im.height, 4)
shutil.copy(os.path.join(HERE, 'flag_in.png'), os.path.join(ART, 'flag_in.png')) if os.path.isdir(ART) else None
for f in os.listdir(ART):
    if f.endswith(('.jpg', '.png')): shutil.copy(os.path.join(ART, f), os.path.join(out, 'assets', f))
HI = LANG == 'hi'
TITLES = [('tHook', ['NO *RIVER?!*'], .3, C(1, 0, -.15), {}), ('t1537', ['*1537*'], C(11, 0, .05), C(11, 1, .7), {'slam': 1}),
          ('t79', ['*79%*', '~WATER BODIES LOST 1973–2013'], C(13, 1, .15), C(14, 0, -.2), {'slam': 1, 'shake': 1})]
I18N = {}   # Hindi video keeps on-screen text in English (user's choice)
PT = {}
D = {'beats': [dict(b, t=C(*b['at']), **({'u': C(*b['until'])} if 'until' in b else {}), **({'back': C(*b['back'])} if isinstance(b.get('back'), list) else {})) for b in SPEC.get('beats', [])], 'shots': PLAN, 'dur': DUR, 'lang': LANG, 'C': Cd, 'LN': LN, 'chunks': [{k: c[k] for k in ('txt', 'sn', 'en', 'wt')} for c in chunks],
     'titles': [dict(id=a, lines=b, a=c, b=d, **o) for a, b, c, d, o in TITLES], 'ar': AR, 'pt': PT, 'i18n': I18N, 'map3': json.load(open(os.path.join(ART, 'map3d.json'))), 'kaveri': SPEC['kaveri'],
     'hand': [[C(*a) if isinstance(a, list) else a, C(*b) if isinstance(b, list) else (END_START if b == 'end' else b)] for a, b in SPEC.get('hand', [])], 'impacts': [C(*x) for x in SPEC.get('impacts', [])],
     'end': {'start': END_START, 'btn': round(END_START + .8, 3), 'tap': round(END_START + 2.0, 3), 'button': 'फॉलो करें BHUGOL' if HI else 'FOLLOW BHUGOL', 'following': 'FOLLOWING'}}
FONTS = {'bsd900.woff2': 'big-shoulders-display/files/big-shoulders-display-latin-900-normal.woff2', 'bsd800.woff2': 'big-shoulders-display/files/big-shoulders-display-latin-800-normal.woff2',
         'arch800.woff2': 'archivo/files/archivo-latin-800-normal.woff2', 'muk800.woff2': 'mukta/files/mukta-devanagari-800-normal.woff2', 'muk700.woff2': 'mukta/files/mukta-devanagari-700-normal.woff2'}
for dst, src in FONTS.items(): shutil.copy(os.path.join(KIT, 'node_modules/@fontsource', src), os.path.join(out, 'assets', dst))
shutil.copy('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', os.path.join(out, 'assets/emoji.ttf'))
shutil.copy(os.path.join(KIT, 'assets/bhugol_badge.png'), os.path.join(out, 'assets/bhugol_badge.png'))
shutil.copy('/home/claude/work/node_modules/gsap/dist/gsap.min.js', os.path.join(out, 'gsap.min.js'))
shutil.copy('/home/claude/work/node_modules/three/build/three.min.js', os.path.join(out, 'three.min.js'))
shutil.copy(os.path.join(MOT, 'motion.js'), os.path.join(out, 'motion.js')); shutil.copy(os.path.join(MOT, 'shader_xfade.js'), os.path.join(out, 'shader_xfade.js'))
if PREVIEW: DUR = PREVIEW
_end = min(END_START, PREVIEW) if globals().get('PREVIEW') else END_START
_G = motion_plan.gaps(PLAN, [{'t': t} for t in _BT], _end, extra=[t[2] for t in TITLES])
for a, b in _G: print(f'PLAN GAP {a:.1f}-{b:.1f} s ({b - a:.1f} s) with nothing new on screen: add a beat (circle/arrow/grow/flap/card/punch) or a cut')
if _G and '--allow-gaps' not in sys.argv: sys.exit('plan check failed: fix the gaps above in the spec (or rerun with --allow-gaps and say why)')
print('plan check: no stretch over 5 s without a new visual moment (0-%.1f s)' % _end)
# ---- 22 Oct 2026 hardening: sharp-beat check, shader lint, pre-render gates (see ../qa/) ----
_SG = motion_plan.sharp_gaps(PLAN, [{'t': C(*b['at']), 'kind': b['kind']} for b in SPEC.get('beats', [])], _end)
for a, b in _SG: print(f'SHARP GAP {a:.1f}-{b:.1f} s ({b - a:.1f} s): no cut/punch/slam/count/grow/flap/card - continuous motion hides soft beats from viewers and QA; add a punch or count here')
if _SG and '--allow-gaps' not in sys.argv: sys.exit('sharp-beat check failed (or rerun with --allow-gaps and say why)')
import subprocess as _sp
_QA = os.path.join(os.path.dirname(MOT), 'qa')
_sp.run(['python3', os.path.join(_QA, 'shader_lint.py'), os.path.join(HERE, 'template3d.html')], check=True)

tpl = open(os.path.join(HERE, 'template3d.html')).read().replace('__MBLUR__', open(os.path.join(MOT, 'vendor/motion-blur.html')).read())
open(os.path.join(out, 'index.html'), 'w').write(tpl.replace('__DATA__', json.dumps(D, ensure_ascii=False)).replace('__DUR__', '%.3f' % DUR))
json.dump({'dur': DUR, 'end': D['end'], 'C': Cd}, open(os.path.join(out, 'times.json'), 'w'), indent=1)
print('built', out, 'dur', DUR)
if '--no-gate' not in sys.argv:   # scene gate (every shot draws, no WebGL errors) + layout gate (marks/labels on screen, out of captions)
    if _sp.run(['bash', os.path.join(_QA, 'gates.sh'), os.path.abspath(out)]).returncode: sys.exit('pre-render gates failed: do not render')
