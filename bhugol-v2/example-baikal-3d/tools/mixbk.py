# Baikal mix: voice + light synthesized music bed (voice-first, ducked) + SFX locked to the shot plan.
# The BHUGOL kit's score.py could not be loaded in this session (kit.json is over the 4 MB read limit), so the bed is a
# re-creation in the same spirit: soft pad chords, a gentle pluck arpeggio, light drums in story sections, bass.
# Usage: python3 mixbk.py <build_dir> <audio_dir> [--fx-only]
#   build_dir/times.json : {"dur", "shots":[{t,cut}], "beats":[{kind,t}], "sections":{...}, "story":[[name,t,vol],...]}
#   audio_dir/voice.wav + timing.json  -> audio_dir/mix.wav (or fx_stem.wav)
import json, os, sys, subprocess
import numpy as np, soundfile as sf
sys.path.insert(0, '/home/claude/media-engine/bhugol-v2/motion'); import motion_plan
SR = 48000
BD, AD = [a for a in sys.argv[1:] if not a.startswith('--')][:2]; FXONLY = '--fx-only' in sys.argv
T = json.load(open(os.path.join(BD, 'times.json'))); TIM = json.load(open(os.path.join(AD, 'timing.json')))
DUR = T['dur']; N = int(DUR * SR) + SR
SFX = '/home/claude/media-engine/money-mirage/mm3/library/sfx/'
def load(p, sr=SR):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', p, '-f', 'f32le', '-ac', '1', '-ar', str(sr), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)
CACHE = {}
def S(name, rate=1.0):
    k = (name, rate)
    if k not in CACHE:
        p = SFX + name; x = load(p, int(SR * rate)) if rate != 1 else load(p); CACHE[k] = x / (np.abs(x).max() or 1)
    return CACHE[k]
MAP = {'whoosh': ['whoosh-short.mp3', 'whoosh.mp3'], 'whoosh_down': ['whoosh.mp3'], 'pop': ['pop.mp3', 'click-soft.mp3'], 'thud': ['thump.mp3', 'thud.mp3'],
       'slide': ['whoosh-short.mp3'], 'shot': ['impact-bass-2.mp3'], 'boom': ['impact-bass-1.mp3'], 'crack': ['paper_crumple.mp3'], 'riser': ['riser.mp3'], 'ticks': ['clock.mp3']}
fx = np.zeros(N); rot = {}
def place(buf, x, t, gain, peak_align=False):
    st = int(round(t * SR)) - (int(np.argmax(np.abs(x))) if peak_align else max(0, int(np.argmax(np.abs(x) > .25)) - int(.006 * SR)))
    s0 = max(0, st); x = x[s0 - st:]; n = min(len(x), N - s0)
    if n > 0: buf[s0:s0 + n] += x[:n] * gain
P = [{'t': s['t'], 'cut': s['cut']} for s in T['shots']]
B = [b for b in T['beats'] if b['kind'] in ('slam', 'count', 'punch', 'charslam', 'card', 'grow', 'flap', 'circle', 'arrow')]
cues = motion_plan.sfx(P, [{'kind': b['kind'], 't': b['t']} for b in B])
for c in cues:
    name, t, vol = c[0], c[1], c[2]; takes = MAP.get(name)
    if not takes: continue
    i = rot.get(name, 0); rot[name] = i + 1; f = takes[i % len(takes)]; rate = (1.0, 1.06, .95)[i % 3]
    if name == 'riser':
        x = S(f); end = c[3] if len(c) > 3 else t + 1.6; L = int((end - t) * SR); place(fx, x[-L:] if L < len(x) else x, t, vol * .5); continue
    if name == 'ticks': place(fx, S(f)[:int(1.3 * SR)], t, vol * .5); continue
    if name == 'pop' and len(c) > 4 and c[4] <= .05: place(fx, S('click-soft.mp3'), t, vol * .55); continue   # the quiet on-beat click
    place(fx, S(f, rate), t, vol * (.55 if name in ('whoosh', 'slide', 'whoosh_down') else .7), peak_align=name in ('thud', 'shot', 'boom'))
for p in P[1:]:
    if p['cut'] in ('zoom', 'zoomIn'): place(fx, S('click-soft.mp3'), p['t'], .5)
    if p['cut'] in ('flash', 'burn'): place(fx, S('whoosh-cinematic.mp3'), p['t'] + .05, .28, True); place(fx, S('impact-bass-2.mp3'), p['t'] + .3, .3, True)
for b in T['beats']:
    if b['kind'] == 'charslam': place(fx, S('impact-bass-1.mp3'), b['t'] + .3, .3, True)
for name, t, vol in T.get('story', []): place(fx, S(name), t, vol * .6)
fx *= .5
if FXONLY:
    sf.write(os.path.join(AD, 'fx_stem.wav'), np.stack([fx, fx], 1), SR); print('fx stem'); sys.exit()
# ---------- voice ----------
v, vsr = sf.read(os.path.join(AD, 'voice.wav'), always_2d=True); v = v.mean(1)
if vsr != SR: v = load(os.path.join(AD, 'voice.wav'))
off = TIM.get('offset', .3); voice = np.zeros(N); s0 = int(off * SR); voice[s0:s0 + len(v)] = v[:N - s0]
pk = np.abs(voice).max() or 1; voice *= .5 / pk * 1.4
# ---------- light synthesized bed ----------
BPM = 92; beat = 60 / BPM; t = np.arange(N) / SR
CH = [[57, 60, 64, 69], [53, 57, 60, 65], [48, 52, 55, 60], [55, 59, 62, 67]]   # Am F C G (curious, light)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def env(n, a, r):
    e = np.ones(n); A = min(n, int(a * SR)); R = min(n - A, int(r * SR))
    if A: e[:A] = np.linspace(0, 1, A)
    if R: e[-R:] = np.linspace(1, 0, R)
    return e
def sec(name):  # multiplier curve for one part from T['sections'][name] = [[a, b, level], ...]
    m = np.zeros(N)
    for a, b, lv in T['sections'].get(name, []):
        b = DUR if b == 'end' else b; i0, i1 = int(a * SR), min(N, int(b * SR)); f = int(.6 * SR)
        if i1 <= i0: continue
        seg = np.full(i1 - i0, float(lv)); k = min(f, len(seg) // 2); seg[:k] *= np.linspace(0, 1, k); seg[-k:] *= np.linspace(1, 0, k); m[i0:i1] = np.maximum(m[i0:i1], seg)
    return m
bar = beat * 4; nb = int(DUR / bar) + 2
pad = np.zeros(N); arp = np.zeros(N); bass = np.zeros(N); drums = np.zeros(N)
rng = np.random.default_rng(7)
for k in range(nb):
    c = CH[k % 4]; a = int(k * bar * SR); n = min(int(bar * 1.15 * SR), N - a)
    if n <= 0: break
    tt = np.arange(n) / SR; e = env(n, .5, .6)
    for m in c: pad[a:a + n] += (np.sin(2 * np.pi * hz(m) * tt) * .6 + np.sin(2 * np.pi * hz(m) * 2.002 * tt) * .12) * e / 4
    bn = min(int(bar * SR), N - a); tb = np.arange(bn) / SR; bass[a:a + bn] += np.sin(2 * np.pi * hz(c[0] - 12) * tb) * np.exp(-tb * 1.4) * .7
    for j in range(8):  # pluck arpeggio, 8ths
        s = a + int(j * beat / 2 * SR); pn = min(int(.5 * SR), N - s)
        if pn <= 0: continue
        m = c[[0, 1, 2, 3, 2, 1, 3, 2][j]] + 12; tp = np.arange(pn) / SR
        arp[s:s + pn] += (np.sin(2 * np.pi * hz(m) * tp) + .3 * np.sin(2 * np.pi * hz(m) * 3 * tp) * np.exp(-tp * 9)) * np.exp(-tp * 6) * .35
    for j in range(4):  # light kick + hat
        s = a + int(j * beat * SR); kn = min(int(.25 * SR), N - s)
        if kn <= 0: continue
        tk = np.arange(kn) / SR
        if j in (0, 2): drums[s:s + kn] += np.sin(2 * np.pi * (55 + 90 * np.exp(-tk * 30)) * tk) * np.exp(-tk * 14) * .8
        else: drums[s:s + kn] += np.sin(2 * np.pi * 180 * tk) * np.exp(-tk * 30) * .25 + rng.normal(0, 1, kn) * np.exp(-tk * 40) * .12
        h = s + int(beat / 2 * SR); hn = min(int(.06 * SR), N - h)
        if hn > 0: drums[h:h + hn] += rng.normal(0, 1, hn) * np.exp(-np.arange(hn) / SR * 70) * .1
music = pad * sec('pad') * .9 + arp * sec('arp') * .55 + bass * sec('bass') * .5 + drums * sec('drums') * .55
# soft low-pass-ish smoothing of the bed (one-pole) so it stays under the voice
music =np.convolve(music, np.ones(6) / 6, 'same')
rms = np.sqrt((music[music != 0] ** 2).mean()) if np.any(music) else 1; music = music / rms * .03
hop = SR // 100; e = np.sqrt(np.convolve(voice ** 2, np.ones(hop) / hop, 'same'))[::hop]
act = (e > .01).astype(float); sm = np.zeros_like(act); g = 0
for i, x in enumerate(act): g = g + (x - g) * (.3 if x > g else .012); sm[i] = g
duck = np.interp(np.arange(N) / SR, np.arange(len(sm)) * hop / SR, 1 - .65 * sm)
mix = voice + music * duck + fx * .8
pk = np.abs(mix).max(); mix = mix / pk * .89 if pk > .89 else mix
sf.write(os.path.join(AD, 'mix_raw.wav'), np.stack([mix, mix], 1), SR)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', os.path.join(AD, 'mix_raw.wav'), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', os.path.join(AD, 'mix_final.wav')], check=True)
print('mix', round(len(mix) / SR, 1), 's; fx cues', len(cues))
