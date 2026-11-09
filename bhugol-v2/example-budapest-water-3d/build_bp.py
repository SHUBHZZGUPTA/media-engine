# Builds the 3D HyperFrames project for "What's Hiding Under Budapest?". Usage: python3 build_bp.py <spec.json> <timing_final.json> <out_dir> [en|hi] [--preview=25]
import json, os, sys, shutil
args = [x for x in sys.argv[1:] if not x.startswith('--')]; spec_p, tim_p, out = args[:3]; LANG = args[3] if len(args) > 3 else 'en'
PREVIEW = next((float(x.split('=')[1]) for x in sys.argv if x.startswith('--preview=')), None)
MOT = '/home/claude/media-engine/bhugol-v2/motion'; sys.path.insert(0, MOT); import motion_plan
HERE = os.path.dirname(os.path.abspath(__file__)); ART = os.path.join(HERE, 'art'); KIT = '/home/claude/bhugol-kit'; TPL = os.path.join(HERE, 'tpl')
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
_BT = [C(*b['at']) for b in SPEC.get('beats', [])]
for f in os.listdir(ART):
    if f.endswith(('.jpg', '.png')): shutil.copy(os.path.join(ART, f), os.path.join(out, 'assets', f))
HI = LANG == 'hi'
# on-screen text stays English in the Hindi video (user's choice); only the end-card button is localised as before
TITLES = [('tHook', ["WHAT'S *BELOW?*"], .3, C(0, 2, -.1)),
          ('tAbove', ['FROM *ABOVE* ↓'], C(8, 0, .1), C(8, 1, -.1)), ('tBelow', ['FROM *BELOW* ↑'], C(8, 2), C(9, 0, -.1))]
D = {'beats': [dict(b, t=C(*b['at']), **({'u': C(*b['until'])} if 'until' in b else {})) for b in SPEC.get('beats', [])], 'shots': PLAN, 'dur': DUR, 'lang': LANG, 'C': Cd, 'LN': LN,
     'chunks': [{k: c[k] for k in ('txt', 'sn', 'en', 'wt')} for c in chunks], 'titles': [dict(id=a, lines=b, a=c, b=d) for a, b, c, d in TITLES], 'i18n': {}, 'pt': {},
     'map3': json.load(open(os.path.join(ART, 'map3d.json'))), 'block': json.load(open(os.path.join(ART, 'block.json'))),
     'end': {'start': END_START, 'btn': round(END_START + .8, 3), 'tap': round(END_START + 2.0, 3), 'button': 'फॉलो करें BHUGOL' if HI else 'FOLLOW BHUGOL', 'following': 'FOLLOWING'}}
FONTS = {'bsd900.woff2': 'big-shoulders-display/files/big-shoulders-display-latin-900-normal.woff2', 'bsd800.woff2': 'big-shoulders-display/files/big-shoulders-display-latin-800-normal.woff2',
         'arch800.woff2': 'archivo/files/archivo-latin-800-normal.woff2', 'muk800.woff2': 'mukta/files/mukta-devanagari-800-normal.woff2', 'muk700.woff2': 'mukta/files/mukta-devanagari-700-normal.woff2'}
for dst, src in FONTS.items(): shutil.copy(os.path.join(KIT, 'node_modules/@fontsource', src), os.path.join(out, 'assets', dst))
shutil.copy('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', os.path.join(out, 'assets/emoji.ttf'))
shutil.copy(os.path.join(KIT, 'assets/bhugol_badge.png'), os.path.join(out, 'assets/bhugol_badge.png'))
shutil.copy('/home/claude/work/node_modules/gsap/dist/gsap.min.js', os.path.join(out, 'gsap.min.js'))
shutil.copy('/home/claude/work/node_modules/three/build/three.min.js', os.path.join(out, 'three.min.js'))
shutil.copy(os.path.join(MOT, 'motion.js'), os.path.join(out, 'motion.js')); shutil.copy(os.path.join(MOT, 'shader_xfade.js'), os.path.join(out, 'shader_xfade.js'))
if PREVIEW: DUR = PREVIEW; D['dur'] = DUR
_end = min(END_START, PREVIEW) if PREVIEW else END_START
_G = motion_plan.gaps(PLAN, [{'t': t} for t in _BT], _end, extra=[t[2] for t in TITLES])
for a, b in _G: print(f'PLAN GAP {a:.1f}-{b:.1f} s ({b - a:.1f} s) with nothing new on screen')
if _G and '--allow-gaps' not in sys.argv: sys.exit('plan check failed')
print('plan check: no stretch over 5 s without a new visual moment (0-%.1f s)' % _end)
_SG = motion_plan.sharp_gaps(PLAN, [{'t': C(*b['at']), 'kind': b['kind']} for b in SPEC.get('beats', [])], _end)
for a, b in _SG: print(f'SHARP GAP {a:.1f}-{b:.1f} s ({b - a:.1f} s)')
if _SG and '--allow-gaps' not in sys.argv: sys.exit('sharp-beat check failed')
tpl = ''.join(open(os.path.join(TPL, p)).read() for p in ('part_head.html', 'part_engine.js', 'part_map.js', 'part_bp.js', 'part_titles.js', 'part_build.js'))
open(os.path.join(HERE, 'template_bp.html'), 'w').write(tpl)
import subprocess as _sp
_QA = os.path.join(os.path.dirname(MOT), 'qa')
_sp.run(['python3', os.path.join(_QA, 'shader_lint.py'), os.path.join(HERE, 'template_bp.html')], check=True)
tpl = tpl.replace('__MBLUR__', open(os.path.join(MOT, 'vendor/motion-blur.html')).read())
open(os.path.join(out, 'index.html'), 'w').write(tpl.replace('__DATA__', json.dumps(D, ensure_ascii=False)).replace('__DUR__', '%.3f' % DUR))
json.dump({'dur': DUR, 'end': D['end'], 'C': Cd}, open(os.path.join(out, 'times.json'), 'w'), indent=1)
print('built', out, 'dur', DUR)
if '--no-gate' not in sys.argv:
    if _sp.run(['bash', os.path.join(_QA, 'gates.sh'), os.path.abspath(out)]).returncode: sys.exit('pre-render gates failed: do not render')
