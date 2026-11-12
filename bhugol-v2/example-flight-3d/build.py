# Builds the Flight HyperFrames project. Usage: python3 build.py <spec.json> <timing.json> <out_dir> [en|hi] [--preview=N] [--allow-gaps]
import json, os, sys, shutil, re, math
args = [x for x in sys.argv[1:] if not x.startswith('--')]; spec_p, tim_p, out = args[:3]; LANG = args[3] if len(args) > 3 else 'en'
PREVIEW = next((float(x.split('=')[1]) for x in sys.argv if x.startswith('--preview=')), None)
MOT = '/home/claude/media-engine/bhugol-v2/motion'; sys.path.insert(0, MOT); import motion_plan
HERE = os.path.dirname(os.path.abspath(__file__)); ART = HERE + '/art'; NM = '/home/claude/hf/node_modules'
SPEC = json.load(open(spec_p)); TIM = json.load(open(tim_p)); os.makedirs(os.path.join(out, 'assets'), exist_ok=True)
LAST = TIM['lines'][-1]; END_START = round(LAST['start'] - .25, 3); DUR = round(LAST['end'] + 2.6, 3)
NUM = re.compile(r'\d')
chunks = []
for li, L in enumerate(SPEC['lines']):
    w0 = 0; ws = TIM['lines'][li]['words']
    for ci, (cap, n) in enumerate(L['chunks']):
        toks = cap.replace('|', ' ').split(' '); m = len(toks); extra = n - m
        # caption word -> spoken token: a number absorbs the extra spoken tokens ("17,000" = "seventeen thousand")
        idx = []; k = w0
        for t in toks:
            idx.append(k); k += 1
            if extra > 0 and NUM.search(t): k += extra; extra = 0
        sn = ws[min(w0, len(ws) - 1)] - .06; wt = [ws[min(i, len(ws) - 1)] - .03 for i in idx]
        chunks.append({'li': li, 'ci': ci, 'txt': cap, 'sn': round(sn, 3), 'wt': [round(x, 3) for x in wt], 'toks': [x.replace('*', '').upper() for x in toks]}); w0 += n
for i, c in enumerate(chunks): c['en'] = chunks[i + 1]['sn'] if i < len(chunks) - 1 else round(LAST['end'] + .25, 3)
Cd = {f'{c["li"]}.{c["ci"]}': c['sn'] for c in chunks}
LN = [{'a': L['start'], 'b': L['end']} for L in TIM['lines']]
def C(li, ci=0, off=0.0): return max(0.0, round(Cd[f'{li}.{ci}'] + off, 3))
def W(li, word, off=0.0):  # time of the first caption word in line li containing `word` (str, or {'en':..,'hi':..})
    w = word[LANG] if isinstance(word, dict) else word
    for c in chunks:
        if c['li'] != li: continue
        for k, t in enumerate(c['toks']):
            if w.upper() in t: return round(c['wt'][k] + off, 3)
    sys.exit(f'word not found: line {li} {w}')
NAMED = {'west': (0, 'WEST'), 'east': (1, 'EAST'), 'hours': (1, '24'), 'record': (1, 'RECORD'), 'india': (2, 'INDIA'), 'km17': (2, '17,000'),
         'pacific': (3, 'PACIFIC'), 'america': (3, 'AMERICA'), 'atlantic': (3, 'ATLANTIC'), 'sunsets': (3, 'SUNSET'), 'sunrises': (3, 'SUNRISE'),
         'why': (4, {'en': 'WHY', 'hi': 'क्यों'}), 'distance': (5, 'DISTANCE'), 'km23': (5, '23,000'), 'halfway': (5, {'en': 'HALFWAY', 'hi': 'आधी'}),
         'boeing': (6, {'en': 'BOEING', 'hi': '2005'}), 'y2005': (6, '2005'), 'too': (6, {'en': 'TOO', 'hi': 'था'}), 'shortcut': (7, 'SHORTCUT'), 'no': (7, {'en': 'NO.', 'hi': 'मना'}),
         'wrong': (8, {'en': 'WRONG', 'hi': 'गलत'}), 'right': (8, {'en': 'RIGHT', 'hi': 'सही'})}
T = {k: W(*v) for k, v in NAMED.items()}
# ---- shots ----
SHOTS = [('GA', 0, None), ('GB', C(1, 0, -.15), 'curve'), ('GA', C(2, 0, -.15), 'curve'), ('GB', C(3, 0, -.15), 'whip'), ('GA', C(4, 0, -.15), 'curve'),
         ('GB', C(5, 0, -.15), 'flash'), ('GA', C(6, 0, -.15), 'whip'), ('GB', C(7, 0, -.15), 'curve'), ('GA', C(8, 0, -.15), 'zoomIn')]
PLAN = [{'scene': s, 't': round(t, 3), 'cut': c or 'curve'} for s, t, c in SHOTS]
for w in motion_plan.check(PLAN): print('motion check:', w)
def shot(i): return PLAN[i]['t']
# ---- beats (all times in real seconds) ----
BEATS = [
 {'kind': 'charslam', 't': .1},
 {'kind': 'punch', 'scene': 'GA', 't': T['west'], 'level': 1.15, 'back': T['west'] + .8},
 {'kind': 'arrow', 'scene': 'GA', 't': T['west'] + .05, 'from': [141, -33], 'to': [104, -24], 'col': '#FF3B30', 'u': shot(1) - .15, 'bend': -.12},
 {'kind': 'punch', 'scene': 'GB', 't': T['east'], 'level': 1.25, 'back': T['east'] + .9},
 {'kind': 'grow', 't': T['hours'], 'to': 24, 'unit': 'HOURS', 'y': 150, 'dur': .8, 'u': T['record'] - .15},
 {'kind': 'slam', 'what': 'trophy', 't': T['record'], 'u': shot(2) - .1},
 {'kind': 'circle', 'scene': 'GA', 't': T['india'], 'c': [79, 22], 'r': [95, 120], 'col': '#FF3B30', 'u': T['km17'] + 1.2},
 {'kind': 'grow', 't': T['km17'], 'to': 17000, 'unit': 'KM', 'prefix': '≈', 'y': 150, 'dur': .9, 'u': shot(3) - .15},
 {'kind': 'slam', 'what': 'pop', 'lab': 'PACIFIC', 't': T['pacific']},
 {'kind': 'slam', 'what': 'pop', 'lab': 'AMERICA', 't': T['america']},
 {'kind': 'slam', 'what': 'pop', 'lab': 'ATLANTIC', 't': T['atlantic']},
 {'kind': 'grow', 't': T['sunsets'], 'to': 2, 'prefix': '🌇 ×', 'unit': 'SUNSETS', 'y': 150, 'dur': .45, 'u': T['sunrises'] - .12},
 {'kind': 'grow', 't': T['sunrises'], 'to': 2, 'prefix': '🌅 ×', 'unit': 'SUNRISES', 'y': 150, 'dur': .45, 'u': shot(4) - .1},
 {'kind': 'punch', 'scene': 'GA', 't': T['why'], 'level': 1.3, 'back': shot(5) - .3},
 {'kind': 'card', 't': T['km23'] - .05, 'to': 23155, 'y': 150, 'dur': 1.0, 'u': T['halfway'] - .2},
 {'kind': 'slam', 'what': 'card', 't': T['km23'] + 1.0},
 {'kind': 'slam', 'what': 'ring', 'scene': 'GB', 't': T['halfway'], 'u': shot(6) - .15},
 {'kind': 'flap', 't': T['y2005'], 'text': '2005', 'y': 150, 'u': T['y2005'] + 1.05},
 {'kind': 'slam', 'what': 'bars', 't': T['y2005'] + 1.25, 'y': 140, 'u': shot(7) - .1},
 {'kind': 'punch', 'scene': 'GA', 't': T['too'], 'level': 1.14, 'back': shot(7) - .3},
 {'kind': 'circle', 'scene': 'GB', 't': T['shortcut'] + .3, 'route': 'B777S', 'p': .5, 'r': [140, 100], 'col': '#FFC23A', 'u': T['no'] - .1},
 {'kind': 'slam', 'what': 'xmark', 'scene': 'GB', 't': T['no'], 'u': shot(8) - .1},
 {'kind': 'slam', 'what': 'pop', 'lab': 'FRA', 't': T['right'] + .02},
 {'kind': 'punch', 'scene': 'GA', 't': T['right'], 'level': 1.16, 'back': END_START - .1},
]
if LANG == 'hi': BEATS = [b for b in BEATS if b['kind'] != 'charslam'] + [{'kind': 'slam', 't': .1, 'what': 'hooktitle'}]
BEATS.sort(key=lambda b: b['t'])
TITLES = [('tHook', ['WRONG WAY?!'], .1, C(1, 0, -.2), {'size': 170, 'y': 330, 'slam': LANG == 'hi'}),
          ('tWhy', ['*WHY?*'], T['why'] - .05, shot(5) - .2, {'slam': 1, 'size': 230, 'y': 360})]
R = json.load(open(ART + '/routes.json'))
def interp(path, f):
    d = [0]
    for a, b in zip(path, path[1:]):
        p1 = [math.cos(math.radians(a[1])) * math.cos(math.radians(a[0])), math.cos(math.radians(a[1])) * math.sin(math.radians(a[0])), math.sin(math.radians(a[1]))]
        p2 = [math.cos(math.radians(b[1])) * math.cos(math.radians(b[0])), math.cos(math.radians(b[1])) * math.sin(math.radians(b[0])), math.sin(math.radians(b[1]))]
        d.append(d[-1] + math.acos(max(-1, min(1, sum(x * y for x, y in zip(p1, p2))))))
    t = f * d[-1]
    for i in range(len(path) - 1):
        if d[i + 1] >= t: g = (t - d[i]) / max(1e-9, d[i + 1] - d[i]); return [path[i][0] + (((path[i + 1][0] - path[i][0] + 540) % 360) - 180) * g, path[i][1] + (path[i + 1][1] - path[i][1]) * g]
    return path[-1]
camPath = [interp(R['A350'], f) for f in (.14, .30, .62, .86, 1.0)]
camPath = [[lo, la - 8] for lo, la in camPath]
for i in range(1, len(camPath)):
    while camPath[i][0] - camPath[i - 1][0] > 180: camPath[i][0] -= 360
    while camPath[i][0] - camPath[i - 1][0] < -180: camPath[i][0] += 360   # look a little south of the plane so it sits in the upper-middle of the frame
LABELS = [dict(id='MEL', txt='MELBOURNE 🇦🇺', lon=144.8, lat=-37.7, fs=58, dy=-70), dict(id='FRA', txt='🇫🇷 FRANCE', lon=1.4, lat=43.6, fs=66, dy=-80),
          dict(id='INDIA', txt='🇮🇳 INDIA', lon=79, lat=22, fs=64, dy=-150), dict(id='PACIFIC', txt='PACIFIC', lon=-150, lat=-2, fs=72, dy=0, col='#BFEFFF'),
          dict(id='AMERICA', txt='🇺🇸 AMERICA', lon=-100, lat=42, fs=66, dy=-90), dict(id='ATLANTIC', txt='ATLANTIC', lon=-38, lat=40, fs=72, dy=40, col='#BFEFFF'),
          dict(id='HKG', txt='HONG KONG', lon=113.9, lat=22.3, fs=56, dy=-70), dict(id='LHR', txt='LONDON', lon=-.45, lat=51.5, fs=56, dy=-70)]
D = {'beats': BEATS, 'shots': PLAN, 'dur': DUR, 'lang': LANG, 'C': Cd, 'T': T, 'LN': LN,
     'chunks': [{k: c[k] for k in ('li', 'txt', 'sn', 'en', 'wt')} for c in chunks],
     'titles': [dict(id=a, lines=b, a=c, b=d, **o) for a, b, c, d, o in TITLES],
     'routes': {'A350': R['A350'], 'SHORT': R['SHORT'], 'B777': R['B777'], 'B777S': R['B777S']}, 'sunEvents': R['sunEvents'], 'camPath': camPath,
     'sun': {'dep': R['dep_utc'], 'hours': R['hours'], 'dec': R['dec']}, 'planeRot': 45,
     'places': {'MEL': [144.84, -37.67, '#FFC23A'], 'TLS': [1.37, 43.63, '#FFC23A'], 'HKG': [113.91, 22.31, '#38D6FF'], 'LHR': [-.45, 51.47, '#38D6FF']},
     'labels': LABELS, 'txt': {'cardTag': 'AIRLINER RECORD', 'ring': '58% 🌍'},
     'bars': [{'name': '2026', 'val': '23,155 KM', 'frac': 1, 'col': '#FF8A1A'}, {'name': '2005', 'val': '21,601 KM', 'frac': round(21601 / 23155, 3), 'col': '#38D6FF'}],
     'impacts': [], 'end': {'start': END_START, 'btn': round(END_START + .8, 3), 'tap': round(END_START + 2.0, 3), 'sub': round(LAST['end'] + .3, 3), 'button': 'FOLLOW BHUGOL', 'following': 'FOLLOWING',
     'sub': 'Follow for more Geography Fun Facts' if LANG == 'en' else 'Follow for more Geography Fun Facts'}}
for f in ('day.jpg', 'night.jpg'): shutil.copy(os.path.join(ART, f), os.path.join(out, 'assets', f))
FONTS = {'bsd900.woff2': 'big-shoulders-display/files/big-shoulders-display-latin-900-normal.woff2', 'bsd800.woff2': 'big-shoulders-display/files/big-shoulders-display-latin-800-normal.woff2',
         'arch800.woff2': 'archivo/files/archivo-latin-800-normal.woff2', 'muk800.woff2': 'mukta/files/mukta-devanagari-800-normal.woff2', 'muk700.woff2': 'mukta/files/mukta-devanagari-700-normal.woff2'}
for dst, src in FONTS.items(): shutil.copy(os.path.join(NM, '@fontsource', src), os.path.join(out, 'assets', dst))
shutil.copy('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', os.path.join(out, 'assets/emoji.ttf'))
shutil.copy('/home/claude/media-engine/citylapse/engine/assets/bhugol_badge.png', os.path.join(out, 'assets/bhugol_badge.png'))
shutil.copy(os.path.join(NM, 'gsap/dist/gsap.min.js'), os.path.join(out, 'gsap.min.js'))
shutil.copy(os.path.join(NM, 'three/build/three.min.js'), os.path.join(out, 'three.min.js'))
shutil.copy(os.path.join(MOT, 'motion.js'), os.path.join(out, 'motion.js'))
# plan checks (whole video unless --preview)
_end = min(END_START, PREVIEW) if PREVIEW else END_START
VIS = [b for b in BEATS if b['kind'] != 'impact']
_G = motion_plan.gaps(PLAN, [{'t': b['t']} for b in VIS], _end, extra=[t[2] for t in TITLES])
for a, b in _G: print(f'PLAN GAP {a:.1f}-{b:.1f} s ({b - a:.1f} s)')
_SG = motion_plan.sharp_gaps(PLAN, [{'t': b['t'], 'kind': b['kind']} for b in BEATS], _end)
for a, b in _SG: print(f'SHARP GAP {a:.1f}-{b:.1f} s ({b - a:.1f} s)')
if (_G or _SG) and '--allow-gaps' not in sys.argv: sys.exit('plan check failed')
print('plan check: ok 0-%.1f s' % _end)
THUMB = next((x.split('=')[1] for x in sys.argv if x.startswith('--thumb=')), None)
if THUMB:
    W1, W2 = (('LONGEST FLIGHT', 'EVER?') if LANG == 'en' else ('सबसे लंबी', 'FLIGHT?'))
    st = "font-family:'BSD','Muk',sans-serif;font-weight:900;line-height:1;white-space:nowrap;"
    D['thumb'] = {'t': 1.5, 'cam': {'lon': 147, 'lat': -24, 'dist': 3.45, 'oy': -130, 'roll': 0}, 'ra': .09, 'rs': .16, 'xat': .09,
      'html': f"""<div style="position:absolute;left:0;top:150px;width:1080px;text-align:center;{st}font-size:160px;color:#fff;paint-order:stroke fill;-webkit-text-stroke:16px #03101A;text-shadow:0 0 6px #03101A,0 10px 30px rgba(0,0,0,.7)">{W1}</div>
      <div style="position:absolute;left:0;top:370px;width:1080px;text-align:center"><span style="display:inline-block;{st}font-size:200px;color:#03101A;background:#FFD21F;border:10px solid #fff;border-radius:26px;padding:10px 40px 4px;box-shadow:0 14px 34px rgba(0,0,0,.55);transform:rotate(-2deg)">{W2}</span></div>
      <div class="tx" style="position:absolute;font-family:'Emo';font-size:200px;line-height:1;filter:drop-shadow(0 8px 10px rgba(0,0,0,.6))">❌</div>"""}
if PREVIEW: D['dur'] = DUR = PREVIEW
tpl = open(os.path.join(HERE, 'template.html')).read().replace('__MBLUR__', open(os.path.join(MOT, 'vendor/motion-blur.html')).read())
open(os.path.join(out, 'index.html'), 'w').write(tpl.replace('__DATA__', json.dumps(D, ensure_ascii=False)).replace('__DUR__', str(DUR)))
SEC = {'pad': [[0, DUR, .9]], 'arp': [[0, shot(4), .8], [shot(5), shot(6), .9], [shot(8), DUR, 1]], 'drums': [[C(1, 0), shot(4) - .2, .6], [shot(5), shot(6) - .2, .7], [shot(8) + .3, DUR, .5]],
       'bass': [[C(1, 0), shot(4), .8], [shot(5), DUR, .8]]}
json.dump({'dur': DUR, 'end': END_START, 'shots': [{'t': p['t'], 'cut': p['cut'], 'scene': p['scene']} for p in PLAN], 'beats': [{'kind': b['kind'] if b['kind'] != 'slam' or b.get('what') not in ('ring',) else 'slam', 't': b['t']} for b in BEATS],
           'sections': SEC, 'story': [['chime.mp3', T['record'] + .05, .5], ['stamp.mp3', T['no'] + .08, .8], ['sparkle.mp3', T['right'] + .05, .5]]}, open(os.path.join(out, 'times.json'), 'w'), indent=1)
print('built', out, 'dur', DUR, 'end card', END_START, 'shots', [p['t'] for p in PLAN])
