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
    for l in open(f'{ME}/outputs/align/{tid}/words.txt'):
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
TRAILER = {l.split()[0]: l.split()[4] for l in open(PROJ + '/lib/sel.txt') if l.strip()}
def tcredit(n):
    k = TRAILER[n]; return 'GTA VI ' + ({'1': 'Trailer 1', '2': 'Trailer 2', 'L': 'Launch Trailer', 'F': 'Features Trailer', 'P': 'Pre-Load Trailer'}[k]) + ' · © Rockstar Games'
for f in ['map_fl2.jpg', 'map_mia.jpg']: shutil.copy(f'{B}/assets/{f}', A)
MAPS = {k: json.load(open(f'{B}/assets/map_{k}.json')) for k in ['fl', 'mia']}
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
def vids(t0, t1, names, zoom=(1, 1)):
    """fill [t0,t1] with trailer clips in order at normal speed (no slow motion: slowed clips stutter).
    If the listed clips run out, continue with unused clips from the same theme pool. Clip-to-clip changes are quick cuts."""
    pool = next((v for v in POOLS.values() if names[0] in v), POOLS['city'])
    seq = list(names) + [c for c in pool if c not in names]
    t = t0; k = 0
    while t < t1 - .05 and k < len(seq):
        n = seq[k]; k += 1
        if shots and shots[-1]['type'] == 'vid' and shots[-1].get('clip') == n: continue
        l = CLIPLEN.get(C(n)); MS = .03
        prev_vid = bool(shots) and shots[-1]['type'] == 'vid' and abs(shots[-1]['t1'] - t) < .01
        fade = .12 if prev_vid else (0 if t == 0 else .5)
        cap = l - MS - .04 - fade / 2 - .08
        last = k == len(seq) or t + cap >= t1 - .05
        if not last and t1 - (t + cap) < .5: cap = t1 - t - .5      # leave at least half a second for the next clip
        e = t1 if last else t + cap
        if e - t > cap + .02: print(f'  SHORT {n}: needs {e - t:.2f}s, clip gives {cap:.2f}s (freeze {e - t - cap:.2f}s)')
        shot(type='vid', src='clips/' + n + '.webm', clip=n, clipDur=l, ms=MS, rate=1, fade=fade or .5, t0=round(t, 3), t1=round(e, 3), zoom=list(zoom), tag='game', credit=tcredit(n))
        t = e
def photo(t0, t1, f, mode='full', zoom=(1, 1.06), pos=None, box=None, tag='real'):
    o = shot(type='photo', src=P(f), mode=mode, t0=round(t0, 3), t1=round(t1, 3), zoom=list(zoom), tag=tag, credit=photo_credit(f))
    if pos: o['pos'] = pos
    if mode == 'card': o['box'] = box or [640, 64, 1100, 825]
    return o
def mapshot(t0, t1, k, cam, items=(), zoom=(1, 1)):
    m = MAPS[k]; tex = {'fl': 'map_fl2.jpg', 'mia': 'map_mia.jpg'}[k]
    return shot(type='paper', bgc='linear-gradient(#0F2D56, #0C2442)' if k == 'fl' else None, tex=tex, pw=m['size'][0], ph=m['size'][1], t0=round(t0, 3), t1=round(t1, 3), cam=cam, items=list(items), zoom=list(zoom),
                credit='Satellite: Sentinel-2 cloudless by EOX (CC BY 4.0)' if k == 'fl' else 'Aerial imagery: USGS (public domain)')
def pin(k, lon, lat, a0, a1, txt=None, fs=46, dy=-58):
    p = mxy(k, lon, lat); out = [{'k': 'pin', 'p': p, 'a': [[a0, 1, .4, 'power2.out'], [a1, 0, .3]]}]
    if txt: out.append({'k': 'lbl', 'p': p, 'txt': txt, 'fs': fs, 'dy': dy, 'a': [[a0 + .15, 1, .4, 'power2.out'], [a1, 0, .3]]})
    return out

# ================= SAMPLE: hook (1-9) + stop 1 (10-17) =================
# hook
vids(0, st(2), ['sunset_hwy', 'skydive', 'yacht', 'port_boat'])
vids(st(2), wt(2, 'from'), ['beach_aerial', 'night_aerial'])
photo(wt(2, 'from'), st(3), 'miami_city_skyline_from_biscayne_bay_1_jpg.jpg')
vids(st(3), st(4), ['ocean_night', 'neon_drive', 'ocean_day', 'dominion_hotel', 'beach_gym'])
c = mxy('mia', -80.188, 25.800)
mapshot(st(4), wt(4, 'except'), 'mia', [[st(4) - .5, {'x': c[0], 'y': c[1], 'z': 1.25}, .1], [st(4), {'z': 1.6}, wt(4, 'except') - st(4) + .5, 'sine.inOut']],
        pin('mia', -80.188, 25.800, st(4) + .4, wt(4, 'except') + .3, 'EDGEWATER'))
vids(wt(4, 'except'), st(5), ['towers_up', 'sunset_balcony', 'night_drive'])
vids(st(5), wt(5, 'sugar'), ['swamp_gold', 'airboat'])
vids(wt(5, 'sugar'), wt(5, 'giant'), ['desert_car'])
vids(wt(5, 'giant'), st(6), ['keys_village', 'keys_bridge', 'stilt_house'])
cf = mxy('fl', -83.7, 27.7)
mapshot(st(6), st(7), 'fl', [[st(6) - .5, {'x': cf[0], 'y': cf[1], 'z': .86}, .1], [st(6), {'z': .9}, st(7) - st(6) + .5, 'none']],
        pin('fl', -86.282, 30.988, wt(6, '105') - .2, st(7) + .3, 'BRITTON HILL', fs=40, dy=58))
beat(k='count', at=wt(6, '105'), until=st(7) - .1, frm=0, to=105, unit=' m', y=300, fs=190)
beats[-1]['from'] = 0
vids(st(7), st(8), ['vice_sign', 'sunset_pier', 'plane_signs', 'metromover', 'hwy_pov'])
beat(k='kick', at=wt(7, 'november'), until=st(8) - .2, top='LAUNCH DAY', txt='Nov <b style="color:#FFD86A">19</b>', x=110, y=650, fs=110)
vids(st(8), wt(8, 'miami'), ['beach_plane', 'jetski'])
photo(wt(8, 'miami'), st(9), 'miami_skyline_feb_2020_jpg.jpg', zoom=(1.04, 1.1))
STOPS = [(-80.130, 25.780), (-80.141, 25.771), (-80.188, 25.800), (-80.199, 25.801), (-80.188, 25.781), (-80.290, 25.795), (-80.90, 25.55), (-80.93, 26.75), (-80.63, 24.92), (-86.282, 30.988)]
its = []
for j, (lo, la) in enumerate(STOPS):
    p = mxy('fl', lo, la); its.append({'k': 'pin', 'p': p, 'a': [[wt(9, 'ten') + .08 * j, 1, .35, 'back.out'], [DUR, 0, .3]]})
mapshot(st(9), st(10) + .2, 'fl', [[st(9) - .5, {'x': cf[0], 'y': cf[1], 'z': .86}, .1], [st(9), {'z': .9}, st(10) - st(9) + .5, 'none']], its)
# stop 1: Ocean Drive
sb = mxy('mia', -80.131, 25.780)
mapshot(st(10), st(11), 'mia', [[st(10) - .5, {'x': c[0], 'y': c[1], 'z': 1.0}, .1], [st(10), {'x': sb[0], 'y': sb[1], 'z': 2.4}, st(11) - st(10) + .3, 'sine.inOut']],
        pin('mia', -80.131, 25.780, st(10) + 1.0, st(11) + .3))
beat(k='chap', at=st(10) + .1, until=st(11) - .3, top='STOP 1', txt='Ocean Drive')
photo(st(11), wt(11, 'neon'), 'ocean_drive_in_the_miami_beach_art_deco_historic_d.jpg')
photo(wt(11, 'neon'), wt(11, 'beach'), 'boulevard_hotel_neon_sign_miami_beach_jpg.jpg')
photo(wt(11, 'beach'), st(12), 'ocean_drive_art_deco_buildings_in_miami_5410502514.jpg', zoom=(1.0, 1.05))
vids(st(12), st(13), ['neon_drive', 'dominion_hotel', 'ocean_day', 'ocean_night', 'beach_gym'])
beat(k='kick', at=wt(12, 'ocean'), until=st(13) - .2, top='IN GTA 6 IT\'S', txt='Ocean Beach', x=110, y=650)
photo(st(13), wt(13, 'victor'), 'art_deco_colony_hotel_boulevard_hotel_miami_beach_.jpg', zoom=(1.0, 1.06))
beat(k='kick', at=wt(13, 'cortez') - .1, until=wt(13, 'victor') - .15, top='COLONY HOTEL  →', txt='The Cortez', x=110, y=650)
photo(wt(13, 'victor'), wt(14, 'thing', end=True), '20111001_1498_south_beach_hotel_victor_dusk_2_jpg.jpg', mode='card')
beat(k='kick', at=wt(13, 'dixon') - .1, until=wt(14, 'thing', end=True) - .1, top='HOTEL VICTOR  →', txt='Hotel Dixon', x=110, y=650, fs=80)
vids(wt(14, 'thing', end=True), st(15), ['hwy_pov', 'boat_dusk', 'jetski'])
photo(st(15), st(16), 'colony_hotel_miami_beach_izzy_jpg.jpg', mode='card')
beat(k='kick', at=wt(15, 'colon', 2), until=st(16) - .15, top='GTA VICE CITY · 2002', txt='Colon Hotel', x=110, y=650, fs=80)
photo(st(16), wt(17, 'but'), 'miami_beach_ocean_drive_hotel_the_colony_hotel_jpg.jpg', mode='card')
beat(k='count', at=wt(16, '24'), until=st(17) - .1, to=24, unit=' YEARS', y=330, fs=170)
beats[-1]['from'] = 0
mu, fl_ = mxy('mia', -80.1395, 25.7695), mxy('mia', -80.1425, 25.7745)
T17 = wt(17, 'but'); E17 = st(19) if L1 >= 19 else DUR
mapshot(T17, E17, 'mia', [[T17 - .5, {'x': sb[0], 'y': sb[1], 'z': 2.4}, .1], [T17, {'x': (mu[0] + fl_[0]) / 2, 'y': (mu[1] + fl_[1]) / 2, 'z': 3.2}, E17 - T17, 'sine.inOut']],
        pin('mia', -80.1395, 25.7695, wt(17, 'towers'), min(E17, st(18) if L1 >= 18 else DUR) - .2, 'MURANO GRANDE', fs=36, dy=58) + pin('mia', -80.1425, 25.7745, wt(17, 'towers') + .25, min(E17, st(18) if L1 >= 18 else DUR) - .2, 'THE FLORIDIAN', fs=36))
STOPS_T = [(st(11), 1)]
def K(at, until, top, txt, fs=None, **kw):
    b = dict(k='kick', at=at, until=until, top=top, txt=txt, x=110, y=650); b.update(kw)
    if fs: b['fs'] = fs
    return beat(**b)
def CNT(at, until, to, unit='', prefix='', y=300, fs=190, dur=1.2):
    return beat(k='count', at=at, until=until, to=to, unit=unit, prefix=prefix, y=y, fs=fs, dur=dur, **{'from': 0})
def CHAP(n, name, at, until):
    beat(k='chap', at=at + .1, until=until, top=f'STOP {n}', txt=name)
eg = mxy('mia', -80.1885, 25.7975)
if L1 >= 24:   # ---------------- STOP 2 · THE TOWERS
    CHAP(2, 'The Towers', st(18), st(19) - .3)
    vids(st(19), wt(19, 'like'), ['towers_up', 'beach_aerial'])
    photo(wt(19, 'like'), st(20), PF('Muranograndeatportofino'), mode='card')
    K(wt(19, 'murano'), st(20) - .15, 'REAL MIAMI BEACH', 'Murano Grande')
    mapshot(st(20), st(21), 'mia', [[st(20) - .5, {'x': mu[0], 'y': mu[1] - 600, 'z': 1.0}, .1], [st(20), {'y': mu[1] - 1600, 'z': 1.15}, st(21) - st(20) + .5, 'sine.inOut']])
    K(wt(20, 'university') , st(21) - .15, 'UNIVERSITY OF MIAMI · 2024', 'Sinking towers', fs=84)
    photo(st(21), st(22), PF('South Beach, Miami22'), zoom=(1.0, 1.06))
    CNT(wt(21, '35'), wt(21, 'two') - .1, 35, unit=' TOWERS')
    K(wt(21, 'two'), st(22) - .15, 'SANK IN JUST 7 YEARS', '2–8 cm')
    mapshot(st(22), st(23), 'mia', [[st(22) - .5, {'x': (mu[0] + fl_[0]) / 2, 'y': (mu[1] + fl_[1]) / 2, 'z': 2.2}, .1], [st(22), {'z': 3.0}, st(23) - st(22) + .5, 'sine.inOut']],
            pin('mia', -80.1395, 25.7695, st(22) + .3, st(23) + .3, 'MURANO GRANDE', fs=36, dy=58) + pin('mia', -80.1425, 25.7745, st(22) + .5, st(23) + .3, 'THE FLORIDIAN', fs=36))
    vids(st(23), wt(23, 'real'), ['night_aerial', 'towers_up', 'port_boat'])
    photo(wt(23, 'real'), wt(24, 'one'), PF('Miami - Skyline from Harbor'), zoom=(1.0, 1.06))
    mapshot(wt(24, 'one'), st(25), 'mia', [[wt(24, 'one') - .5, {'x': eg[0], 'y': eg[1], 'z': 1.3}, .1], [wt(24, 'one'), {'z': 1.9}, st(25) - wt(24, 'one') + 3.5, 'sine.inOut']])
    STOPS_T.append((st(19) - .1, 2))
if L1 >= 31:   # ---------------- STOP 3 · THE APARTMENT
    CHAP(3, 'The Apartment', st(25), st(26) - .3)
    mapshot(st(25), st(26), 'mia', [[st(25) - .5, {'x': eg[0], 'y': eg[1], 'z': 1.9}, .1], [st(25), {'z': 2.6}, st(26) - st(25) + .5, 'sine.inOut']])
    vids(st(26), st(27), ['apt_kitchen', 'apt_living', 'sunset_balcony', 'yacht'])
    K(wt(26, 'pink') - .1, st(27) - .15, 'IN GTA 6', 'Jason & Lucia’s place', fs=80)
    mapshot(st(27), st(28), 'mia', [[st(27) - .5, {'x': eg[0], 'y': eg[1], 'z': 2.0}, .1], [st(27), {'z': 2.8}, st(28) - st(27) + .5, 'sine.inOut']],
            pin('mia', -80.1885, 25.7975, wt(27, 'edgewater'), st(28) + .3, 'EDGEWATER', fs=40))
    K(wt(27, 'belmar'), st(28) - .15, 'BUILT 1973', 'The Belmar')
    mapshot(st(28), st(30), 'mia', [[st(28) - .5, {'x': eg[0], 'y': eg[1], 'z': 2.8}, .1], [st(28), {'z': 3.4}, st(30) - st(28) + .5, 'sine.inOut']])
    CNT(wt(28, '12'), wt(28, 'tore') + .3, 12, prefix='$', unit=' MILLION', fs=170)
    K(wt(29, 'empty'), st(30) - .15, 'TODAY', 'An empty lot')
    vids(st(30), st(31), ['apt_living', 'night_aerial'])
    vids(st(31), st(32), ['mural_drive', 'lowrider_street'])
    STOPS_T.append((st(26) - .1, 3))
if L1 >= 35:   # ---------------- STOP 4 · THE MURALS
    photo(st(32), st(33), PF('Wynwood Walls Miami Florida October 2013'), pos='center 30%')
    CHAP(4, 'Wynwood', st(32), st(33) - .3)
    photo(st(33), wt(33, 'painted'), PF('April 7, 2015 - Wynwood Miami - 03'), mode='card')
    photo(wt(33, 'painted'), st(34), PF('April 7, 2015 - Wynwood Miami - 05'), mode='card')
    vids(st(34), st(35), ['lowrider_street', 'mural_drive'])
    K(wt(34, 'stockyards') - .1, st(35) - .15, 'IN GTA 6 IT\'S', 'The Stockyards')
    vids(st(35), st(36), ['night_drive', 'metromover', 'hwy_pov'])
    STOPS_T.append((st(33) - .1, 4))
if L1 >= 43:   # ---------------- STOP 5 · THE ARENA
    photo(st(36), st(38), PF('Kaseya Center Downtown Miami'), zoom=(1.0, 1.07))
    CHAP(5, 'The Arena', st(36), st(37) - .3)
    K(wt(37, 'kaseya'), st(38) - .15, 'HOME OF THE MIAMI HEAT', 'Kaseya Center')
    vids(st(38), st(39), ['night_aerial', 'neon_drive', 'night_drive'])
    K(wt(38, 'sahara'), st(39) - .15, 'IN GTA 6 IT\'S', 'Sahara Arena')
    photo(st(39), st(41), PF('AAArena Night'), zoom=(1.0, 1.12))
    photo(st(41), st(43), PF('Kaseya Center Downtown Miami'), zoom=(1.08, 1.18))
    K(wt(40, 'welcome') - .1, st(41) - .15, 'ON THE REAL ROOF, 2026', '“Welcome to Vice City”', fs=72)
    CNT(wt(41, '975000'), st(42) - .1, 975000, prefix='$', fs=170)
    K(st(42), st(43) - .15, 'PUBLIC-VOTE LIMIT', '$1,000,000')
    vids(st(43), st(44), ['vice_sign'])
    STOPS_T.append((st(37) - .1, 5))
if L1 >= 49:   # ---------------- STOP 6 · THE AIRPORT
    photo(st(44), st(45), PF('Aerial view of Miami International Airport in 2026'), zoom=(1.0, 1.06))
    CHAP(6, 'The Airport', st(44), st(45) - .3)
    vids(st(45), st(46), ['plane_takeoff', 'vice_sign', 'plane_signs'])
    photo(st(46), st(48), PF('Aerial view of Miami International Airport in 2026'), zoom=(1.08, 1.16))
    K(wt(47, 'miami'), st(48) - .15, 'MOVIE PROP · BAD BOYS', 'MIAMI')
    vids(st(48), st(49), ['vice_sign', 'sunset_pier'])
    vids(st(49), st(50), ['hwy_pov', 'driving_billboard'])
    STOPS_T.append((st(45) - .1, 6))
if L1 >= 57:   # ---------------- STOP 7 · THE SWAMP
    photo(st(50), st(51), PF('Visit the Everglades on a program'), zoom=(1.0, 1.06))
    CHAP(7, 'The Everglades', st(50), st(51) - .3)
    vids(st(51), st(52), ['swamp_gold', 'swamp_heli', 'airboat'])
    K(wt(51, 'grassrivers'), st(52) - .15, 'IN GTA 6 THEY\'RE', 'The Grassrivers')
    photo(st(52), st(53), PF('Cypress Habitat'), zoom=(1.0, 1.08))
    photo(st(53), st(54), PF('Visit the Everglades on a program'), zoom=(1.04, 1.12))
    K(wt(52, 'river'), wt(53, 'same') - .15, 'A 1947 BOOK', '“River of Grass”')
    K(wt(53, 'national'), st(54) - .15, 'SINCE 1947', 'National park', fs=84)
    vids(st(54), wt(54, 'just'), ['flamingos', 'airboat', 'swamp_gold'])
    photo(wt(54, 'just'), st(55), PF('American Alligator in Everglades'), mode='card')
    vids(st(55), st(56), ['swamp_heli', 'swamp_gold'])
    photo(st(56), wt(56, 'pet'), PF('A Burmese python stretched out'), zoom=(1.0, 1.05))
    photo(wt(56, 'pet'), st(57), PF('Burmese Python, NPSPhoto, Rodney Cammauf (8721514008)'), mode='card')
    ok_ = mxy('fl', -80.83, 26.95); evg = mxy('fl', -80.9, 25.6)
    mapshot(st(57), st(58), 'fl', [[st(57) - .5, {'x': evg[0], 'y': evg[1], 'z': 2.2}, .1], [st(57), {'x': ok_[0], 'y': ok_[1], 'z': 2.6}, st(58) - st(57) + 1.5, 'sine.inOut']],
            pin('fl', -80.93, 26.75, st(57) + .8, st(58) - .2, 'CLEWISTON', fs=40))
    STOPS_T.append((st(51) - .1, 7))
if L1 >= 64:   # ---------------- STOP 8 · THE SUGAR TOWN
    mapshot(st(58), st(59), 'fl', [[st(58) - .5, {'x': ok_[0], 'y': ok_[1], 'z': 2.6}, .1], [st(58), {'z': 3.0}, st(59) - st(58) + .5, 'sine.inOut']])
    CHAP(8, 'The Sugar Town', st(58), st(59) - .3)
    photo(st(59), wt(59, 'sugar'), PF('Aerial view of Canal Point, Florida, approaching lock'), zoom=(1.0, 1.06))
    photo(wt(59, 'sugar'), st(60), PF('20210226-PJK-FPAC-0188'), zoom=(1.0, 1.06))
    photo(st(60), st(61), PF('CITY LIMITS OF CLEWISTON'), mode='card')
    K(wt(60, 'americas'), st(61) - .15, 'CLEWISTON, FLORIDA', '“America’s Sweetest Town”', fs=72)
    vids(st(61), st(62), ['desert_car', 'dirt_trail'])
    K(wt(61, 'ambrosia'), wt(61, 'slogan') - .1, 'IN GTA 6 IT\'S', 'Ambrosia')
    K(wt(61, 'keeping'), st(62) - .15, 'ITS SLOGAN', '“Keeping Leonida Sweet”', fs=72)
    photo(st(62), st(63), PF('US Sugar Train II'), mode='card')
    K(wt(62, 'allied'), wt(62, 'lake') - .1, 'IN GTA 6', 'Allied Crystal')
    K(wt(62, 'leonida'), st(63) - .15, 'IN GTA 6', 'Lake Leonida')
    photo(st(63), st(64), PF('Clewiston FL Hoover Dike Memorial02'), mode='card')
    ky = mxy('fl', -81.0, 24.9)
    mapshot(st(64), st(65), 'fl', [[st(64) - .5, {'x': ok_[0], 'y': ok_[1], 'z': 2.2}, .1], [st(64), {'x': ky[0], 'y': ky[1], 'z': 2.4}, st(65) - st(64) + 1.5, 'sine.inOut']])
    STOPS_T.append((st(59) - .1, 8))
if L1 >= 70:   # ---------------- STOP 9 · THE KEYS
    photo(st(65), st(66), PF('Seven Mile Bridge, Florida Keys aerial (2003)'), zoom=(1.0, 1.06))
    CHAP(9, 'The Keys', st(65), st(66) - .3)
    photo(st(66), st(67), PF('Seven-mile Historic Bridge, Florida Keys'), zoom=(1.0, 1.07))
    vids(st(67), st(68), ['keys_sign', 'keys_bridge', 'keys_village'])
    K(wt(67, 'leonida'), st(68) - .15, 'IN GTA 6 THEY\'RE', 'The Leonida Keys')
    mapshot(st(68), st(69), 'fl', [[st(68) - .5, {'x': ky[0], 'y': ky[1], 'z': 2.4}, .1], [st(68), {'x': mxy('fl', -80.63, 24.92)[0], 'y': mxy('fl', -80.63, 24.92)[1], 'z': 3.2}, st(69) - st(68) + .5, 'sine.inOut']],
            pin('fl', -80.63, 24.92, st(68) + .4, st(69) + .3, 'ISLAMORADA', fs=40))
    K(wt(68, 'betsy'), st(69) - .15, '9 METRES TALL', 'Betsy the lobster', fs=84)
    vids(st(69), st(70), ['stilt_house', 'seaplane', 'marina'])
    K(wt(69, 'whale'), st(70) - .15, 'IN GTA 6', 'A giant whale')
    mapshot(st(70), st(71), 'fl', [[st(70) - .5, {'x': ky[0], 'y': ky[1], 'z': 2.0}, .1], [st(70), {'x': cf[0], 'y': cf[1], 'z': .9}, st(71) - st(70) + .5, 'sine.inOut']])
    STOPS_T.append((st(66) - .1, 9))
if L1 >= 78:   # ---------------- STOP 10 · THE MOUNTAINS
    vids(st(71), st(72), ['dirt_trail', 'desert_car'])
    CHAP(10, 'Mount Kalaga', st(71), st(72) - .3)
    photo(st(72), st(73), PF('Britton Hill, Florida'), mode='card')
    CNT(wt(72, '105'), st(73) - .1, 105, unit=' m')
    mapshot(st(73), st(74), 'fl', [[st(73) - .5, {'x': cf[0], 'y': cf[1], 'z': .86}, .1], [st(73), {'z': .9}, st(74) - st(73) + .5, 'none']],
            pin('fl', -86.282, 30.988, st(73) + .2, st(74) + .3, 'BRITTON HILL', fs=40, dy=58))
    photo(st(74), st(75), PF('Miami Night Skyline from across the Biscayne Bay'), zoom=(1.0, 1.06))
    vids(st(75), st(76), ['dirt_trail', 'desert_car'])
    photo(st(76), st(77), PF('View from top of Providence Canyon a'), mode='card')
    K(wt(76, 'providence'), st(77) - .15, 'GEORGIA, USA', 'Providence Canyon')
    vids(st(77), st(78), ['dirt_trail', 'sunset_hwy'])
    vids(st(78), st(79), ['vice_sign'])
    STOPS_T.append((st(72) - .1, 10))
END_STOPS = st(79) if L1 >= 79 else DUR
if L1 >= 86:   # ---------------- FINALE · MIAMI COPIES BACK
    photo(st(79), st(80), PF('Miami Night Skyline from across the Biscayne Bay'), zoom=(1.06, 1.12))
    beat(k='chap', at=st(79) + .1, until=st(80) - .3, top='FINALE', txt='Miami copies back')
    photo(st(80), st(81), PF('Aerial view of Miami International Airport in 2026'), zoom=(1.0, 1.06))
    K(wt(80, 'vice'), st(81) - .15, 'THE COUNTY’S PITCH', '“Vice City Airport”', fs=80)
    photo(st(81), st(82), PF('Miami Dade Transit Metromover 57'), zoom=(1.0, 1.06))
    photo(st(82), st(83), PF('Miami - Skyline from Harbor'), zoom=(1.04, 1.1))
    K(wt(82, 'miamidade', 1) if any('miamidade' in w for w in sw) else wt(82, 'miami'), st(83) - .15, 'MIAMI-DADE SHERIFF', '“Miami-Dade County is not Vice City.”', fs=58)
    photo(st(83), st(84), PF('AAArena Night'), zoom=(1.04, 1.1))
    K(wt(83, 'welcome'), st(84) - .15, 'ON THE ARENA ROOF', '“Welcome to Vice City”', fs=72)
    its = []
    for j_, (lo, la) in enumerate(STOPS):
        p_ = mxy('fl', lo, la); its.append({'k': 'pin', 'p': p_, 'a': [[st(84) + .05 * j_, 1, .35, 'back.out'], [st(85) + .3, 0, .3]]})
    mapshot(st(84), st(85), 'fl', [[st(84) - .5, {'x': cf[0], 'y': cf[1], 'z': .86}, .1], [st(84), {'z': .9}, st(85) - st(84) + .5, 'none']], its)
    REC = [('hotel', 'p', 'art_deco_colony_hotel_boulevard_hotel_miami_beach_.jpg'), ('towers', 'p', PF('Muranograndeatportofino')), ('apartment', 'v', 'apt_living'),
           ('walls', 'p', PF('April 7, 2015 - Wynwood Miami - 03')), ('arena', 'p', PF('Kaseya Center Downtown Miami')), ('sign', 'v', 'vice_sign'),
           ('river', 'p', PF('Cypress Habitat')), ('sweet', 'p', PF('CITY LIMITS OF CLEWISTON')), ('lobster', 'v', 'keys_bridge'), ('mountains', 'v', 'dirt_trail')]
    ts = [wt(85, w_) for w_, _, _ in REC] + [st(86)]
    for (w_, kind, src), a_, b_ in zip(REC, ts, ts[1:]):
        if kind == 'p': photo(a_ - .1, b_ - .1, src, zoom=(1.0, 1.05))
        else: vids(a_ - .1, b_ - .1, [src])
    vids(st(86) - .1, wt(86, 'now'), ['sunset_hwy', 'night_aerial'])
    photo(wt(86, 'now'), st(87), PF('Miami Night Skyline from across the Biscayne Bay'), zoom=(1.0, 1.08))
if L1 >= 90:   # ---------------- ENDING + CTA
    vids(st(87), st(88), ['neon_drive', 'yacht', 'beach_aerial'])
    mapshot(st(88), st(89), 'fl', [[st(88) - .5, {'x': cf[0], 'y': cf[1], 'z': .86}, .1], [st(88), {'z': .92}, st(89) - st(88) + .5, 'none']])
    mapshot(st(89), st(90), 'fl', [[st(89) - .5, {'x': cf[0], 'y': cf[1], 'z': .92}, .1], [st(89), {'z': .98}, st(90) - st(89) + .5, 'none']])
    beat(k='sub', at=wt(89, 'subscribe') - .2, until=st(90) - .1)
    vids(st(90), DUR, ['sunset_hwy', 'vice_sign'])
    K(wt(90, 'november'), DUR, 'LAUNCH DAY', 'Nov <b style="color:#FFD86A">19</b>', fs=110)
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
DATA = {'lang': 'en', 'dur': DUR, 'shots': shots, 'beats': beats, 'caps': CAPS, 'stops': [[a_, b_, n_] for (a_, n_), (b_, _) in zip(sorted(STOPS_T), sorted(STOPS_T)[1:] + [(END_STOPS, 0)])], 'nStops': 10}
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
json.dump({'sfx_dir': ME + '/money-mirage/mm3/library/sfx', 'below_voice_db': 19, 'swell_db': 4, 'sections': [
    *([{'file': MUS + 'eighties_action.mp3', 'from': 0, 'to': DUR, 'gain_db': -18}] if L1 < 79 else [
    {'file': MUS + 'eighties_action.mp3', 'from': 0, 'to': st(36), 'gain_db': -18},
    {'file': MUS + 'cyborg_ninja.mp3', 'from': st(36) - .75, 'to': st(58), 'gain_db': -18},
    {'file': MUS + 'ouroboros.mp3', 'from': st(58) - .75, 'to': st(79), 'gain_db': -18},
    {'file': MUS + 'eighties_action.mp3', 'from': st(79) - .75, 'to': DUR, 'gain_db': -18}])]}, open(f'{B}/music.json', 'w'))
