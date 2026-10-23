# Money Mirage ep01 v3: spec + timing + shot plan -> HyperFrames project (one page per render segment).
# Usage: python3 build.py [--fake] [--seg=60] [--preview=A,B] [--port]
#   --port      native portrait Short (1080x1920, its own script and shot plan; money-mirage-shorts skill)
#   --fake      estimate timings at 2.45 words/s (engine work before the voice exists)
import json, os, sys, shutil, re, math
import numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from mmpaths import *
ART = os.path.join(HERE, 'art')
import motion_plan
from note import note_svg
arg = lambda k, d=None: next((a.split('=', 1)[1] for a in sys.argv if a.startswith(k + '=')), d)
SPEC = json.load(open(os.path.join(HERE, 'spec.json'))); PLAN = json.load(open(os.path.join(HERE, 'shots.json')))
OUT = arg('--out', os.path.join(HERE, 'proj')); SHORT = arg('--short'); NATIVE = '--port' in sys.argv   # --short=<id> --out=proj_short/<id>: one portrait page from shorts_v3.json
if '--fake' in sys.argv:
    t = .3; lines = []
    for L in SPEC['lines']:
        ws = L['text'].split(); st = []
        for w in ws: st.append(round(t, 3)); t += .41 + (.25 if w[-1] in '.,!?:;' else 0)
        lines.append({'start': st[0], 'end': round(t, 3), 'words': st}); t += .45
    TIM = {'lines': lines, 'offset': .3}
else: TIM = json.load(open(os.path.join(HERE, 'audio/timing.json')))
TAIL = SPEC.get('tail', 3.0); DUR = round((TIM['lines'][-1]['end'] + TAIL) * 30) / 30
# caption chunks and their times
chunks = []
for li, L in enumerate(SPEC['lines']):
    w0 = 0; ws = TIM['lines'][li]['words']
    for ci, c in enumerate(L['chunks']):
        n = len(c.split(' ')); chunks.append({'li': li, 'ci': ci, 'txt': c, 'sn': ws[min(w0, len(ws) - 1)] - .06, 'wt': [ws[min(w0 + k, len(ws) - 1)] - .03 for k in range(n)]}); w0 += n
for i, c in enumerate(chunks): c['en'] = min(chunks[i + 1]['sn'], c['wt'][-1] + 1.6) if i < len(chunks) - 1 else DUR
Cd = {f'{c["li"]}.{c["ci"]}': round(c['sn'], 3) for c in chunks}
def Cf(li, ci=0, off=0.0): return round(Cd[f'{li}.{ci}'] + off, 3)
EVT = []; ABS = []
def R(v):  # resolve anchors anywhere in a structure (every resolved time is also a planned visual event)
    if isinstance(v, dict):
        if '@' in v: x = Cf(*v['@']); EVT.append(x); return x
        if '@w' in v: li, wi, off = v['@w']; x = round(TIM['lines'][li]['words'][wi] - .03 + off, 3); EVT.append(x); return x
        if 'abs' in v: ABS.append(v['abs']); return v['abs']
        return {k: R(x) for k, x in v.items()}
    if isinstance(v, list): return [R(x) for x in v]
    return v
SH = R(PLAN['shots']); BT = []
for b0 in PLAN['beats']:   # each beat also records the last time it touches (lets a segment page skip beats outside its window)
    EVT.clear(); ABS.clear(); b1 = R(b0); b1['tend'] = round(max([x for x in EVT + ABS if isinstance(x, (int, float))] + [b1['at']]), 3); BT.append(b1)
EVT.clear()
for b0 in PLAN['beats']: R(b0)
for b in PLAN['beats']:
    if b['kind'] == 'moment' and b.get('what') == 'char':
        for li in b.get('lines', []): EVT.append(TIM['lines'][li]['start'])
for b in BT:
    if b['kind'] == 'moment' and b.get('what') == 'char': b['tend'] = max([b['tend']] + [TIM['lines'][li]['end'] for li in b.get('lines', [])])
for i, s in enumerate(SH): s['t'] = 0.0 if i == 0 else s['at']
for i, s in enumerate(SH): s['win'] = [s['t'] - .45 if i else 0, (SH[i + 1]['t'] + .1) if i < len(SH) - 1 else DUR + 1]
for b in BT:
    b['t'] = b.pop('at')
    if 'until' in b: b['u'] = b.pop('until')
# grammar + plan-gap checks (motion_plan, BHUGOL v2)
P = [{'scene': s['id'], 't': s['t'], 'cut': s['cut']} for s in SH]
for w in motion_plan.check(P): print('motion check:', w)
vis = [b for b in BT if b['kind'] != 'sfx']
END_START = TIM['lines'][-1]['start']
EX = [k['t'] for s in SH for k in s.get('keys', [])] + [e for e in EVT if isinstance(e, (int, float))]
G = motion_plan.gaps(P, [{'t': b['t']} for b in vis], END_START, extra=EX)
# BHUGOL v2 rule: more punch-ins wherever a shot has no beat for > 3 s. Fill the remaining gaps with soft punch-ins on the live shot.
auto = 0
for a, b in G:
    t = a + 2.6
    while t < b - 1.4:
        sh = max((s for s in SH if s['t'] <= t), key=lambda s: s['t']); BT.append({'kind': 'punch', 't': round(t, 3), 'shot': sh['id'], 'level': 1.07 + .03 * (auto % 3), 'back': round(t + 1.3, 3), 'auto': True}); auto += 1; t += 2.6
vis = [b for b in BT if b['kind'] != 'sfx']
G = motion_plan.gaps(P, [{'t': b['t']} for b in vis], END_START, extra=EX)
print('auto punch-ins added:', auto)
for a, b in G: print(f'PLAN GAP {a:.1f}-{b:.1f} s ({b - a:.1f} s)')
if G and '--allow-gaps' not in sys.argv: sys.exit('plan check failed')
print('plan check: no stretch over 5 s without a new visual moment (0-%.1f s)' % END_START)

# assets
os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
def depth_png(stem):
    """8-bit landscape depth (768x432, grown + softened so edges don't tear); flat for the map, raised poster for the doc."""
    dst = os.path.join(OUT, 'assets', f'depth_{stem}.png')
    if os.path.exists(dst): return f'depth_{stem}.png'
    if stem == 'map_world': Image.new('L', (768, 432), 128).save(dst); return f'depth_{stem}.png'
    if stem == 'doc_eo6102': Image.open(os.path.join(ART, 'depth_doc_eo6102.png')).save(dst); return f'depth_{stem}.png'
    src = next((os.path.join(DEP, j, stem + '_depth.png') for j in DEPTH_JOBS if os.path.exists(os.path.join(DEP, j, stem + '_depth.png'))), None)
    if not src: Image.new('L', (768, 432), 128).save(dst); print('  (no depth yet for', stem, '- flat)'); return f'depth_{stem}.png'
    d = np.array(Image.open(src)).astype(np.float32); d = d / max(1.0, d.max()); h0, w0 = d.shape[:2]
    sz = (768, 432) if w0 >= h0 else (round(768 * w0 / h0), 768)   # keep a portrait plate's aspect
    Image.fromarray((d * 255).astype(np.uint8)).resize(sz, Image.BILINEAR).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(3)).save(dst)
    return f'depth_{stem}.png'
need = set()
for s in SH:
    base = s['img']; look = s['look']; fn = f"{base}__{look}.jpg"
    p = os.path.join(ART, 'baked', fn)
    if not os.path.exists(p): need.add(f'{base}:{look}'); s['tex'] = fn
    else: shutil.copy(p, os.path.join(OUT, 'assets', fn)); s['tex'] = fn
    s['dep'] = depth_png(s.get('depthOf', base)); s['ar'] = 16 / 9
    if os.path.exists(p): w0, h0 = Image.open(p).size; s['ar'] = round(w0 / h0, 4)   # portrait plates keep their own aspect
if need: print('NEED BAKE:', ' '.join(sorted(need)))
for f in ('c_goldie.png', 'c_bill.png'): shutil.copy(os.path.join(SRC, f), os.path.join(OUT, 'assets', f))
shutil.copy(os.path.join(LIB, 'img/coin_lion.png'), os.path.join(OUT, 'assets/coin_lion.png'))
shutil.copy(os.path.join(LIB, 'img/logo.png'), os.path.join(OUT, 'assets/logo.png'))
shutil.copy(os.path.join(LIB, 'fonts/emoji.ttf'), os.path.join(OUT, 'assets/emoji.ttf'))
for w in ('800', '900'): shutil.copy(os.path.join(LIB, f'fonts/inter{w}.woff2'), os.path.join(OUT, f'assets/inter{w}.woff2'))
for w in ('700', '800'): shutil.copy(os.path.join(LIB, f'fonts/mukta{w}.woff2'), os.path.join(OUT, f'assets/mukta{w}.woff2'))   # Devanagari fallback
for f, s in (('gsap.min.js', 'node_modules/gsap/dist/gsap.min.js'), ('three.min.js', 'node_modules/three/build/three.min.js'), ('motion_ls.js', 'motion_ls.js')):
    shutil.copy(os.path.join(ENG, s), os.path.join(OUT, f))
AR = {}
for n in ('c_goldie', 'c_bill'): im = Image.open(os.path.join(SRC, n + '.png')); bb = im.getbbox(); AR[n] = round((bb[2] - bb[0]) / (bb[3] - bb[1]), 4)
for n in ('c_goldie', 'c_bill'):  # trim to the alpha box so feet sit on the floor line
    im = Image.open(os.path.join(SRC, n + '.png')); im.crop(im.getbbox()).save(os.path.join(OUT, 'assets', n + '.png'))
LN = [{'a': L['start'], 'b': L['end']} for L in TIM['lines']]
D = {'shots': SH, 'beats': BT, 'dur': DUR, 'C': Cd, 'LN': LN, 'ar': AR,
     'chunks': [{k: c[k] for k in ('txt', 'sn', 'en', 'wt')} for c in chunks],
     'noteSvg': note_svg('NTID', promise=True), 'noteSvgNP': note_svg('NTID', promise=False)}
tpl = open(os.path.join(ENG, 'template.html')).read().replace('__MBLUR__', open(os.path.join(ENG, 'motion-blur.html')).read())
if SHORT:   # portrait Short: hook card + pieces of the main timeline, one page
    SS = next(x for x in json.load(open(os.path.join(HERE, 'shorts_v3.json')))['shorts'] if x['id'] == SHORT)
    hk = SS['hook']; shutil.copy(os.path.join(ART, 'baked', hk['img']), os.path.join(OUT, 'assets', hk['img']))
    shutil.copy(os.path.join(ART, 'baked', SS['outro']['img']), os.path.join(OUT, 'assets', SS['outro']['img']))
    Ds = dict(D, seg=None, port=True, pieces=SS['pieces'], hook=hk, outro=SS['outro'], pcam=SS.get('pcam', {}))
    dur = hk['dur'] + sum(b - a for a, b in SS['pieces']) + SS['outro']['dur']
    for f in os.listdir(OUT):
        if f.endswith('.html'): os.remove(os.path.join(OUT, f))
    open(os.path.join(OUT, 'index.html'), 'w').write(tpl.replace('__DATA__', json.dumps(Ds, ensure_ascii=False)).replace('__DUR__', '%.3f' % dur).replace('__W__', '1080').replace('__H__', '1920'))
    print('short', SHORT, 'dur %.1f s' % dur, OUT); sys.exit()
if NATIVE: D.update(port=True, native=True, lang=EPC.get('lang', 'en')); tpl = tpl.replace('__W__', '1080').replace('__H__', '1920')
else: tpl = tpl.replace('__W__', '1920').replace('__H__', '1080')
SEG = float(arg('--seg', 60)); segs = []; a = 0.0
while a < DUR - .01: b = min(DUR, a + SEG); segs.append([round(a, 3), round(b, 3)]); a = b
for f in os.listdir(OUT):
    if re.match(r'(seg\d+|index)\.html', f): os.remove(os.path.join(OUT, f))
pv = arg('--preview')
if pv: segs = [[float(x) for x in pv.split(',')]]
for i, (a, b) in enumerate(segs):
    Dd = dict(D, seg=[a, b]); open(os.path.join(OUT, f'seg{i:02d}.html'), 'w').write(tpl.replace('__DATA__', json.dumps(Dd, ensure_ascii=False)).replace('__DUR__', '%.3f' % (b - a)))
open(os.path.join(HERE, 'index_full.html'), 'w').write(tpl.replace('__DATA__', json.dumps(dict(D, seg=None), ensure_ascii=False)).replace('__DUR__', '%.3f' % DUR))
json.dump({'dur': DUR, 'C': Cd, 'segs': segs, 'end_start': END_START, 'shots': [{'id': s['id'], 't': s['t'], 'cut': s['cut']} for s in SH],
           'beats': [{'kind': b['kind'], 't': b['t'], **({'name': b['name'], 'vol': b.get('vol', 1)} if b['kind'] == 'sfx' else {}), **({'what': b['what']} if b['kind'] == 'moment' else {})} for b in BT]},
          open(os.path.join(OUT, 'times.json'), 'w'), indent=1)
print('built', OUT, 'dur %.1f s' % DUR, len(segs), 'segments', len(SH), 'shots', len(BT), 'beats')
