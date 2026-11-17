#!/usr/bin/env python3
"""BHUGOL GTA 6 vs Miami long-form (16:9) HyperFrames page builder.
usage: python3 make.py "<tts_id>/<item>:<first>-<last>,..."  -> out/hf/index.html (+ assets), narration.wav, spec.json, music.json
Each part is a Gemini TTS take (outputs/tts/<tts_id>/<item>.wav) aligned in outputs/align/<tts_id>/; parts are joined with a short gap."""
import json, re, sys, os, shutil, difflib, math
B = os.path.dirname(os.path.abspath(__file__)); ME = '/home/claude/media-engine'
PROJ = os.environ.get('PROJ', '/home/claude/gta6')   # project folder: script_en.txt, credits.json, photos/, lib/clips/, lib/sel.txt, vo/
PARTS = []
for spec in sys.argv[1].split(','):
    pid, rng = spec.split(':'); a, b = map(int, rng.split('-')); tid, item = pid.split('/'); PARTS.append((tid, item, a, b))
L0, L1 = PARTS[0][2], PARTS[-1][3]; GAP = .45
OUT = f'{B}/out/hf'; A = OUT + '/assets'
os.makedirs(A + '/clips', exist_ok=True)
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())
lines = {}
for l in open(PROJ + '/script_en.txt'):
    m = re.match(r'^(\d+) (.*)', l.strip())
    if m: lines[int(m.group(1))] = m.group(2)
S = [lines[i] for i in range(L0, L1 + 1)]

# ---------- word timings ----------
import subprocess as _sp
W = []; off = 0.0; cat = []
for tid, item, a, b in PARTS:
    wav = f'{ME}/outputs/tts/{tid}/{item}.wav'
    if os.path.exists(f'{PROJ}/vo/{item}.wav'): wav = f'{PROJ}/vo/{item}.wav'   # pitch-matched take (same voice, aligned to part 1's tone)
    dur = float(_sp.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', wav], capture_output=True, text=True).stdout)
    pw = []
    for l in open(f"{ME}/outputs/align/{os.environ.get('ALIGN', tid)}/words.txt"):
        p = l.split(None, 2)
        if len(p) == 3 and p[0][0].isdigit(): pw.append((float(p[0]) + off, float(p[1]) + off, p[2].strip()))
    end = min(dur, pw[-1][1] - off + .35)                 # trim trailing silence of the take
    W += pw; cat.append((wav, end)); off += end + GAP
DUR = round(W[-1][1] + 2.2, 2)
fl = []
for k, (wav, end) in enumerate(cat):
    fl += ['-i', wav]
flt = ''.join(f'[{k}:a]atrim=0:{end},apad=pad_dur={GAP},aresample=48000[a{k}];' for k, (w, end) in enumerate(cat)) + ''.join(f'[a{k}]' for k in range(len(cat))) + f'concat=n={len(cat)}:v=0:a=1[o]'
_sp.run(['ffmpeg', '-v', 'error', '-y'] + fl + ['-filter_complex', flt, '-map', '[o]', '-ac', '1', f'{B}/narration.wav'], check=True)
SPOKEN = {'$100': 'a hundred dollars', 'Twenty-four': '24', "2002's": "2002s", 'colours': 'colors', 'metres': 'meters'}
sw, sl, disp = [], [], []
for i, l in enumerate(S):
    key = False
    for w in l.split():
        k = w.startswith('*'); key = key or k; wd = w.replace('*', '')
        sp = wd
        for a, b in SPOKEN.items(): sp = sp.replace(a, b)
        for x in sp.split():
            n = norm(x)
            if n: sw.append(n); sl.append(i)
        disp.append((i, wd, key, len([x for x in sp.split() if norm(x)]) or 1))
        if re.search(r'\*[.,?!…]*$', w): key = False
wn = [norm(w[2]) for w in W]
sm = difflib.SequenceMatcher(None, sw, wn, autojunk=False); M = {}
for a, b, n in sm.get_matching_blocks():
    for k in range(n): M[a + k] = b + k
tt = [None] * len(sw)
for k in range(len(sw)):
    if k in M: tt[k] = (W[M[k]][0], W[M[k]][1])
for k in range(len(sw)):
    if tt[k] is None:
        pv = next((tt[j] for j in range(k - 1, -1, -1) if tt[j]), (0, 0)); nx = next((tt[j] for j in range(k + 1, len(sw)) if tt[j]), (DUR, DUR))
        tt[k] = (pv[1], max(pv[1] + .05, min(nx[0], pv[1] + .3)))
print('unmatched script tokens:', [sw[k] for k in range(len(sw)) if k not in M])
ST = [tt[[k for k in range(len(sw)) if sl[k] == i][0]][0] for i in range(len(S))] + [DUR]
st = lambda n: ST[n - L0]
def wt(n, word, occ=1, end=False):
    c = 0
    for k in range(len(sw)):
        if sl[k] == n - L0 and norm(word) in sw[k]:
            c += 1
            if c == occ: return tt[k][1] if end else tt[k][0]
    raise SystemExit(f'word {word} not in line {n}')

# ---------- captions ----------
caps, cur, ti = [], [], 0
for idx, (i, wd, key, nt) in enumerate(disp):
    t0 = tt[min(ti, len(tt) - 1)][0]; t1 = tt[min(ti + nt - 1, len(tt) - 1)][1]; ti += nt
    cur.append([round(t0, 3), round(t1, 3), wd, 1 if key else 0])
    nxt_line = idx + 1 < len(disp) and disp[idx + 1][0] != i
    if len(cur) >= 6 or wd[-1:] in '.?!' or (wd[-1:] == ',' and len(cur) >= 3) or nxt_line: caps.append(cur); cur = []
if cur: caps.append(cur)
CAPS = []
for j, c in enumerate(caps):
    a = c[0][0]; b = caps[j + 1][0][0] if j + 1 < len(caps) else DUR
    CAPS.append({'a': round(a - .05, 3), 'b': round(min(b, c[-1][1] + 1.2), 3), 'w': c})

# ---------- assets ----------
TH = B + '/fonts'
for f in ['bsd800.woff2', 'bsd900.woff2', 'arch800.woff2', 'mukta800.woff2', 'emoji.ttf', 'fr600.woff2', 'fr700.woff2', 'in800.woff2', 'bhugol_badge.png']: shutil.copy(f'{TH}/{f}', A)
PH = PROJ + '/photos'; CL = PROJ + '/lib/clips'
CRED = {c['file']: c for c in json.load(open(PROJ + '/credits.json'))}
def PF(prefix):
    for c in CRED.values():
        if c['title'].startswith(prefix): return c['file']
    raise SystemExit('no photo ' + prefix)
def photo_credit(f):
    c = CRED[f]; a = re.sub(r'^Photograph:\s*', '', c['artist']).replace(' from Australia', '')
    m_ = re.search(r'User:([^/"\s]+)', c['artist']) or re.search(r'\. (\w[\w .-]+?) assumed', c['artist'])
    if 'machine-readable' in a: a = (m_.group(1) if m_ else 'Wikimedia Commons').replace('_', ' ')
    a = re.split(r'\s{2,}|\n| from ', a.strip())[0][:40]
    return f"Photo: {a} · {c['license']}" if 'domain' not in c['license'].lower() else f"Photo: {a} · public domain"
used = set()
def P(f): used.add(('p', f)); return 'p/' + f
CLIPLEN = {}
def C(n):
    used.add(('c', n))
    if n not in CLIPLEN:
        import subprocess
        CLIPLEN[n] = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{CL}/{n}.webm'], capture_output=True, text=True).stdout)
    return n
SEL = {l.split()[0]: l.split() for l in open(PROJ + '/lib/sel.txt') if l.strip()}
CLIPCRED = json.load(open(PROJ + '/clip_credits.json')) if os.path.exists(PROJ + '/clip_credits.json') else {}
GTA_CRED = {'1': 'Trailer 1', '2': 'Trailer 2', 'L': 'Launch Trailer', 'F': 'Features Trailer', 'P': 'Pre-Load Trailer'}
def tcredit(n):
    k = SEL[n][4]
    if k in CLIPCRED: return CLIPCRED[k]
    return 'GTA VI ' + GTA_CRED[k] + ' · © Rockstar Games'
CLIPTAG = {}   # clip name -> (tag, label); default ('game', None)
import glob as _glob
MAPKEYS = sorted(os.path.basename(p)[4:-5] for p in _glob.glob(f'{B}/assets/map_*.json'))
MAPTEX = {k: (f'map_{k}2.jpg' if os.path.exists(f'{B}/assets/map_{k}2.jpg') else f'map_{k}.jpg') for k in MAPKEYS}
for k in MAPKEYS: shutil.copy(f'{B}/assets/{MAPTEX[k]}', A)
MAPS = {k: json.load(open(f'{B}/assets/map_{k}.json')) for k in MAPKEYS}
MAPSRC = {'mia': 'usgs'}   # plan may override; default eox
def mxy(k, lon, lat):
    m = MAPS[k]; n = 2 ** m['z'] * 256; x = (lon + 180) / 360 * n; s = math.sin(math.radians(lat)); y = (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * n
    return [round(x - m['px0'][0], 1), round(y - m['px0'][1], 1)]

shots, beats = [], []
def shot(**o): shots.append(o); return o
def beat(**b): beats.append(b); return b
POOLS = {'city': ['night_aerial', 'beach_aerial', 'yacht', 'jetski', 'port_boat', 'neon_drive', 'night_drive', 'metromover', 'towers_up', 'boat_dusk', 'dock_sunset', 'sunset_balcony', 'street_police', 'beach_gym', 'ocean_night'],
         'swamp': ['swamp_gold', 'swamp_heli', 'airboat', 'flamingos', 'iguana', 'boat_dusk', 'dock_sunset', 'sunset_pier'],
         'keys': ['keys_sign', 'keys_bridge', 'keys_village', 'stilt_house', 'seaplane', 'marina', 'dock_sunset', 'sunset_pier'],
         'rural': ['desert_car', 'dirt_trail', 'hwy_pov', 'driving_billboard', 'chase_street'],
         'air': ['vice_sign', 'plane_takeoff', 'plane_signs', 'sunset_pier', 'skydive', 'hwy_pov']}
CLIPUSE = {}
def vids(t0, t1, names, zoom=(1, 1)):
    """fill [t0,t1] with trailer clips in order at normal speed (no slow motion: slowed clips stutter).
    If the listed clips run out, continue with unused clips from the same theme pool. Clip-to-clip changes are quick cuts."""
    pool = next((v for v in POOLS.values() if names[0] in v), [])
    seq = list(names) + [c for c in pool if c not in names]
    t = t0; k = 0
    while t < t1 - .05 and k < len(seq):
        n = seq[k]; k += 1
        if shots and shots[-1]['type'] == 'vid' and shots[-1].get('clip') == n: continue
        l = CLIPLEN.get(C(n)); MS = CLIPUSE.get(n, .03)
        if l - MS < min(t1 - t, 2.0) + .4: MS = .03          # not enough left in this clip: start it from the top again
        prev_vid = bool(shots) and shots[-1]['type'] == 'vid' and abs(shots[-1]['t1'] - t) < .01
        fade = .12 if prev_vid else (0 if t == 0 else .5)
        cap = l - MS - .04 - fade / 2 - .08
        last = k == len(seq) or t + cap >= t1 - .05
        if not last and t1 - (t + cap) < .5: cap = t1 - t - .5      # leave at least half a second for the next clip
        e = t1 if last else t + cap
        if e - t > cap + .02: print(f'  SHORT {n}: needs {e - t:.2f}s, clip gives {cap:.2f}s (freeze {e - t - cap:.2f}s)')
        shot(type='vid', src='clips/' + n + '.webm', clip=n, clipDur=l, ms=MS, rate=1, fade=fade or .5, t0=round(t, 3), t1=round(e, 3), zoom=list(zoom), tag=CLIPTAG.get(n, ('game', None))[0], label=CLIPTAG.get(n, ('game', None))[1], credit=tcredit(n))
        CLIPUSE[n] = MS + (e - t) + .1
        t = e
def photo(t0, t1, f, mode='full', zoom=(1, 1.06), pos=None, box=None, tag='real', label=None):
    o = shot(type='photo', src=P(f), mode=mode, t0=round(t0, 3), t1=round(t1, 3), zoom=list(zoom), tag=tag, label=label, credit=photo_credit(f))
    if pos: o['pos'] = pos
    if mode == 'card': o['box'] = box or [640, 64, 1100, 825]
    return o
def mapshot(t0, t1, k, cam, items=(), zoom=(1, 1)):
    m = MAPS[k]; tex = MAPTEX[k]
    return shot(type='paper', bgc='linear-gradient(#0F2D56, #0C2442)' if k == 'fl' else None, tex=tex, pw=m['size'][0], ph=m['size'][1], t0=round(t0, 3), t1=round(t1, 3), cam=cam, items=list(items), zoom=list(zoom),
                credit='Aerial imagery: USGS (public domain)' if MAPSRC.get(k) == 'usgs' else 'Satellite: Sentinel-2 cloudless by EOX (CC BY 4.0)')
def pin(k, lon, lat, a0, a1, txt=None, fs=46, dy=-58):
    p = mxy(k, lon, lat); out = [{'k': 'pin', 'p': p, 'a': [[a0, 1, .4, 'power2.out'], [a1, 0, .3]]}]
    if txt: out.append({'k': 'lbl', 'p': p, 'txt': txt, 'fs': fs, 'dy': dy, 'a': [[a0 + .15, 1, .4, 'power2.out'], [a1, 0, .3]]})
    return out

NSTOPS, COUNTDOWN, TRKWORD, MUSIC_SECTIONS = 10, False, 'STOP', None
exec(open(os.environ.get('PLAN', PROJ + '/plan.py')).read())
for b in beats:
    if 'frm' in b: b.pop('frm')

shots.sort(key=lambda o: o['t0'])
# ---------- write ----------
import subprocess, hashlib
os.makedirs(A + '/f', exist_ok=True)
for j, s_ in enumerate(shots):
    if s_['type'] != 'vid': continue
    lead = 0 if j == 0 else s_['fade'] / 2
    n = int(math.ceil((s_['t1'] - s_['t0'] + lead + .65) * 30)); first = int(round(s_['ms'] * 30))
    key = f"{s_['clip']}_{first}_{n}"; d = f'{A}/f/{key}'
    if not os.path.exists(d + '/done'):
        os.makedirs(d, exist_ok=True)
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', f"{CL}/{s_['clip']}.webm", '-vf', f'select=gte(n\\,{first})', '-vsync', '0', '-frames:v', str(n), '-q:v', '3', f'{d}/%04d.jpg'], check=True)
        open(d + '/done', 'w').write('1')
    s_['frames'] = 'f/' + key; s_['nFrames'] = len([x for x in os.listdir(d) if x.endswith('.jpg')])
used = {u for u in used if u[0] != 'c'}
for kind, f in used:
    if kind == 'p': os.makedirs(A + '/p', exist_ok=True); shutil.copy(f'{PH}/{f}', f'{A}/p/{f}')
    else: shutil.copy(f'{CL}/{f}.webm', f'{A}/clips/{f}.webm')
DATA = {'lang': 'en', 'dur': DUR, 'shots': shots, 'beats': beats, 'caps': CAPS, 'stops': [[a_, b_, n_] for (a_, n_), (b_, _) in zip(sorted(STOPS_T), sorted(STOPS_T)[1:] + [(END_STOPS, 0)])], 'nStops': NSTOPS, 'countdown': COUNTDOWN, 'trkWord': TRKWORD}
html = open(f'{B}/engine.html').read().replace('__DATA__', json.dumps(DATA, ensure_ascii=False)).replace('__DUR__', str(DUR)).replace('__LANG__', 'en')
open(f'{OUT}/index.html', 'w').write(html)
shutil.copy(os.environ.get('GSAP', '/home/claude/hfwork/node_modules/gsap/dist/gsap.min.js'), OUT)
json.dump({'ST': ST, 'DUR': DUR}, open(f'{B}/times.json', 'w'))
gaps = []; ev = sorted([s['t0'] for s in shots] + [b['at'] for b in beats])
for a, b in zip(ev, ev[1:] + [DUR]):
    if b - a > 4: gaps.append((round(a, 1), round(b, 1)))
print('dur', DUR, 'shots', len(shots), 'beats', len(beats), 'caps', len(CAPS), '| gaps>4s', gaps)
for s in shots: print(f"  {s['t0']:6.2f}-{s['t1']:6.2f} {s['type']:6s} {s.get('src', s.get('tex', ''))}")

# ---------- sound spec + music ----------
spec_shots = []
for j, s_ in enumerate(shots):
    prev = shots[j - 1] if j else None
    cut = 'silent' if (prev and prev['type'] == 'vid' and s_['type'] == 'vid') else 'curve'
    spec_shots.append({'t0': s_['t0'], 't1': s_['t1'], 'cut': cut})
fx = [['impact-bass-1', b['at'], -22] for b in beats if b['k'] == 'chap']
json.dump({'shots': spec_shots, 'fx': fx}, open(f'{B}/spec.json', 'w'))
MUS = ME + '/outputs/fetch/gta6-music/'
if MUSIC_SECTIONS is not None:
    json.dump({'sfx_dir': ME + '/money-mirage/mm3/library/sfx', 'below_voice_db': 19, 'swell_db': 4, 'sections': MUSIC_SECTIONS}, open(f'{B}/music.json', 'w'))
else:
  json.dump({'sfx_dir': ME + '/money-mirage/mm3/library/sfx', 'below_voice_db': 19, 'swell_db': 4, 'sections': [
    *([{'file': MUS + 'eighties_action.mp3', 'from': 0, 'to': DUR, 'gain_db': -18}] if L1 < 79 else [
    {'file': MUS + 'eighties_action.mp3', 'from': 0, 'to': st(36), 'gain_db': -18},
    {'file': MUS + 'cyborg_ninja.mp3', 'from': st(36) - .75, 'to': st(58), 'gain_db': -18},
    {'file': MUS + 'ouroboros.mp3', 'from': st(58) - .75, 'to': st(79), 'gain_db': -18},
    {'file': MUS + 'eighties_action.mp3', 'from': st(79) - .75, 'to': DUR, 'gain_db': -18}])]}, open(f'{B}/music.json', 'w'))
