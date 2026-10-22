# Shorts v3 mix: hook line + pieces of the main narration, one ducked YouTube Audio Library bed, real SFX locked to the
# Short's own cuts and beats (same cue rules as mix.py). Usage: python3 mix_short.py <id>  -> audio/shorts/<id>_mix.wav
import json, os, sys, subprocess
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); SR = 48000
sys.dont_write_bytecode = True; sys.path.insert(0, '/home/claude/media-engine/bhugol-v2/motion'); import motion_plan
SID = sys.argv[1]; SS = next(x for x in json.load(open(os.path.join(HERE, 'shorts_v3.json')))['shorts'] if x['id'] == SID)
T = json.load(open(os.path.join(HERE, 'proj/times.json'))); SPEC = json.load(open(os.path.join(HERE, 'spec.json'))); TIM = json.load(open(os.path.join(HERE, 'audio/timing.json')))
H = SS['hook']['dur']; P = SS['pieces']; DUR = H + sum(b - a for a, b in P); N = int((DUR + .5) * SR)
BUN = '/root/.claude/skills/media-use/audio/assets/sfx/'; OV = '/home/claude/mm-work/v2/assets/sfx/'
def load(p, sr=SR): return np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', p, '-f', 'f32le', '-ac', '1', '-ar', str(sr), '-'], capture_output=True, check=True).stdout, np.float32).astype(np.float64)
CACHE = {}
def S(p, rate=1.0):
    if (p, rate) not in CACHE: x = load(p, int(SR * rate)); CACHE[(p, rate)] = x / (np.abs(x).max() or 1)
    return CACHE[(p, rate)]
def mapt(t):  # main time -> Short time (None if outside every piece)
    cur = H
    for a, b in P:
        if a <= t < b: return cur + t - a
        cur += b - a
    return None
fx = np.zeros(N)
def place(buf, x, t, gain, peak=False):
    st = int(round(t * SR)) - (int(np.argmax(np.abs(x))) if peak else int(np.argmax(np.abs(x) > .25)) - int(.006 * SR)); s0 = max(0, st); x = x[s0 - st:]; n = min(len(x), N - s0)
    if n > 0: buf[s0:s0 + n] += x[:n] * gain
MAP = {'whoosh': [BUN + 'whoosh-short.mp3', BUN + 'whoosh.mp3'], 'whoosh_down': [BUN + 'whoosh.mp3'], 'pop': [BUN + 'pop.mp3', BUN + 'click-soft.mp3'],
       'thud': [OV + 'thump.mp3', OV + 'thud.mp3'], 'slide': [BUN + 'whoosh-short.mp3'], 'shot': [BUN + 'impact-bass-2.mp3'], 'boom': [BUN + 'impact-bass-1.mp3'],
       'crack': [OV + 'paper_crumple.mp3'], 'riser': [BUN + 'riser.mp3'], 'ticks': [OV + 'clock.mp3']}
# the Short's own cut list: the hook card, then every main shot inside the pieces (+ a hard cut at each piece start)
shots = [{'scene': 'hook', 't': 0.0, 'cut': 'hard'}]
for k, (a, b) in enumerate(P):
    live = [s for s in T['shots'] if s['t'] <= a]; first = live[-1] if live else T['shots'][0]
    shots.append({'scene': first['id'] + f'@{k}', 't': mapt(a), 'cut': 'whip' if k == 0 else 'hard'})
    shots += [{'scene': s['id'], 't': mapt(s['t']), 'cut': s['cut']} for s in T['shots'] if a < s['t'] < b]
beats = [{'kind': 'charslam', 't': .05}] + [{'kind': b['kind'], 't': mapt(b['t'])} for b in T['beats'] if b['kind'] in ('slam', 'count', 'punch', 'charslam', 'grow', 'flap', 'circle', 'arrow') and mapt(b['t']) is not None]
shots.sort(key=lambda s: s['t'])
rot = {}
for c in motion_plan.sfx(shots, beats):
    name, t, vol = c[0], c[1], c[2]; takes = MAP.get(name)
    if not takes: continue
    i = rot.get(name, 0); rot[name] = i + 1; path = takes[i % len(takes)]
    if name == 'riser': end = c[3] if len(c) > 3 else t + 1.6; x = S(path); place(fx, x[-int((end - t) * SR):] if (end - t) * SR < len(x) else x, t, vol * .5); continue
    if name == 'ticks': place(fx, S(path)[:int(1.3 * SR)], t, vol * .5); continue
    place(fx, S(path, (1.0, 1.06, .95)[i % 3]), t, vol * (.55 if name in ('whoosh', 'slide', 'whoosh_down') else .7), peak=name in ('thud', 'shot', 'boom'))
for s in shots[1:]:
    if s['cut'] in ('zoom', 'zoomIn'): place(fx, S(BUN + 'click-soft.mp3'), s['t'], .5)
    if s['cut'] == 'flash': place(fx, S(BUN + 'whoosh-cinematic.mp3'), s['t'] + .05, .45, True); place(fx, S(BUN + 'impact-bass-2.mp3'), s['t'] + .3, .45, True)
for b in T['beats']:
    if b['kind'] == 'sfx' and mapt(b['t']) is not None: place(fx, S(OV + b['name'] + '.mp3'), mapt(b['t']), b.get('vol', 1) * .6)
place(fx, S(BUN + 'impact-bass-1.mp3'), .35, .45, True)
fx *= .5
# voice: hook line, then the matching stretches of the main narration (voice.wav starts at main time = offset)
voice = np.zeros(N); off = TIM.get('offset', .3)
hk = load(os.path.join(HERE, 'audio/shorts', SID + '.wav')) if os.path.exists(os.path.join(HERE, 'audio/shorts', SID + '.wav')) else np.zeros(int(H * SR))
s0 = int(.15 * SR); voice[s0:s0 + len(hk)] += hk[:N - s0]
v = load(os.path.join(HERE, 'audio/voice.wav')); cur = H
for a, b in P:
    seg = v[max(0, int((a - off) * SR)):int((b - off) * SR)].copy(); f = int(.02 * SR); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    i0 = int(cur * SR); n = min(len(seg), N - i0); voice[i0:i0 + n] += seg[:n]; cur += b - a
# music: the chapter's YouTube Audio Library track, ducked under speech
TRACKS = ['1_keys', '2_never', '3_something', '4_standoff', '5_rapid', '6_system', '5b_shadows', '7_fact']; OFFS = {'2_never': 7.7}
li = next(i for i, L in enumerate(TIM['lines']) if L['end'] > P[0][0] + .5); tr = TRACKS[SPEC['lines'][li]['ch']]
m = load(f'/home/claude/mm-work/engine/build/music/{tr}.mp3')[int(OFFS.get(tr, 0) * SR):]
while len(m) < N: m = np.concatenate([m, m])
m = m[:N]; m = m / (np.sqrt((m ** 2).mean()) or 1) * .065; fi, fo = int(.4 * SR), int(1.2 * SR); m[:fi] *= np.linspace(0, 1, fi); m[-fo:] *= np.linspace(1, 0, fo)
hop = SR // 100; e = np.sqrt(np.convolve(voice ** 2, np.ones(hop) / hop, 'same'))[::hop]; act = (e > .01).astype(float); sm = np.zeros_like(act); g = 0
for i, a in enumerate(act): g = g + (a - g) * (.25 if a > g else .04); sm[i] = g
duck = np.interp(np.arange(N) / SR, np.arange(len(sm)) * hop / SR, 1 - .62 * sm)
mix = voice + m * duck * 2.2 + fx; pk = np.abs(mix).max(); mix = mix / pk * .89 if pk > .89 else mix
os.makedirs(os.path.join(HERE, 'audio/shorts'), exist_ok=True)
sf.write(os.path.join(HERE, 'audio/shorts', SID + '_mix.wav'), np.stack([mix, mix], 1), SR)
sf.write(os.path.join(HERE, 'audio/shorts', SID + '_fx.wav'), np.stack([fx, fx], 1), SR)
json.dump({'shots': [{'id': s['scene'], 't': s['t'], 'cut': s['cut']} for s in shots], 'beats': beats, 'dur': DUR}, open(os.path.join(HERE, 'audio/shorts', SID + '_times.json'), 'w'))
print(SID, 'mix', round(DUR, 1), 's; music', tr, '; peak', round(pk, 3))
