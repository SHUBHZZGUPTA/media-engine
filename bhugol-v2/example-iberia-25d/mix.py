# Mix: Gemini voice + light synthesized BHUGOL bed (voice-first, ducked, no fades at the loop seam) + SFX locked to every move/beat.
# Usage: python3 mix.py <build_dir> <audio_dir> [--fx-only]
import json, os, sys, subprocess
import numpy as np, soundfile as sf
SR = 48000
BD, AD = [a for a in sys.argv[1:] if not a.startswith('--')][:2]; FXONLY = '--fx-only' in sys.argv
T = json.load(open(os.path.join(BD, 'times.json'))); EV = json.load(open(os.path.join(BD, 'evs.json'))); TIM = json.load(open(os.path.join(AD, 'timing.json')))
DUR = T['dur']; N0 = int(round(DUR * SR)); N = N0
LIB = '/home/claude/media-engine/money-mirage/mm3/library/sfx/'
def load(p):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', p, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32).astype(np.float64); return x / (np.abs(x).max() or 1)
CACHE = {}
def S(n):
    if n not in CACHE: CACHE[n] = load(LIB + n)
    return CACHE[n]
fx = np.zeros(N)
def place(x, t, gain, peak=False, maxlen=None):
    if maxlen: x = x[:int(maxlen * SR)] * np.r_[np.ones(max(0, int(maxlen * SR) - 2400)), np.linspace(1, 0, min(2400, int(maxlen * SR)))][:len(x[:int(maxlen * SR)])]
    st = int(round(t * SR)) - (int(np.argmax(np.abs(x))) if peak else max(0, int(np.argmax(np.abs(x) > .25)) - int(.006 * SR)))
    s0 = max(0, st); x = x[s0 - st:]; n = min(len(x), N - s0 - int(.25 * SR))   # nothing rings into the loop seam
    if n > 0: fx[s0:s0 + n] += x[:n] * gain
rot = {}
def pick(names):
    i = rot.get(names[0], 0); rot[names[0]] = i + 1; return names[i % len(names)]
MAP = {'card': (['whoosh-short.mp3'], .3, False),   # no pop/click/tick sounds (Shubham, 16 Nov 2026)
       'slam': (['thump.mp3'], .8, True), 'stamp': (['stamp.mp3', 'office_stamp.mp3'], .8, True), 'chime': (['chime.mp3'], .5, False), 'sparkle': (['sparkle.mp3'], .55, False),
       'coins': (['coin_drop.mp3', 'coins_plate.mp3'], .6, False), 'thud': (['thud.mp3'], .8, True), 'whoosh': (['whoosh-short.mp3', 'whoosh.mp3'], .45, False),
       'boom': (['impact-bass-1.mp3'], .55, True)}
for e in EV:
    k, t = e['kind'], e['t']
    if k == 'flash': place(S('whoosh-cinematic.mp3'), t + .05, .5, True); place(S('impact-bass-2.mp3'), t + .15, .55, True); continue
    if k not in MAP: continue
    names, g, pk = MAP[k]; place(S(pick(names)), t, g, pk, maxlen=1.3 if k == 'count' else None)
for k in T['cam'][1:]:   # every camera glide gets an airy whoosh
    if k['at'] > DUR - 1: g = .22
    else: g = .32 if k.get('ease') != 'snap' else .45
    place(S(pick(['whoosh.mp3', 'whoosh-short.mp3'])), k['at'] + .02, g)
rng = np.random.default_rng(3); C = T['C']
fx *= .55
if FXONLY:
    sf.write(os.path.join(AD, 'fx_stem.wav'), np.stack([fx, fx], 1), SR); print('fx stem'); sys.exit()
# voice

raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', os.path.join(AD, 'voice.wav'), '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
v = np.frombuffer(raw, np.float32).astype(np.float64)
voice = np.zeros(N); s0 = int(TIM['offset'] * SR); m = min(len(v), N - s0); voice[s0:s0 + m] = v[:m]
voice *= .7 / (np.abs(voice).max() or 1)
# light bed (same spirit as the BHUGOL kit: soft pads, gentle pluck, light drums), constant level so the loop seam is invisible
LW = int(.8 * SR); N = N0 + LW; voice = np.r_[voice, np.zeros(LW)]
BPM = 100; beat = 60 / BPM; bar = beat * 4; hz = lambda mm: 440 * 2 ** ((mm - 69) / 12)
CH = [[57, 60, 64, 69], [53, 57, 60, 65], [48, 52, 55, 60], [55, 59, 62, 67]]
pad = np.zeros(N); arp = np.zeros(N); bass = np.zeros(N); drums = np.zeros(N)
def env(n, a, r):
    e = np.ones(n); A = min(n, int(a * SR)); R = min(n - A, int(r * SR))
    if A: e[:A] = np.linspace(0, 1, A)
    if R: e[-R:] = np.linspace(1, 0, R)
    return e
for kk in range(int(DUR / bar) + 2):
    c = CH[kk % 4]; a = int(kk * bar * SR); n = min(int(bar * 1.15 * SR), N - a)
    if n <= 0: break
    tt = np.arange(n) / SR; e = env(n, .3 if kk else 0, .6)
    for mm in c: pad[a:a + n] += (np.sin(2 * np.pi * hz(mm) * tt) * .6 + np.sin(2 * np.pi * hz(mm) * 2.002 * tt) * .12) * e / 4
    bn = min(int(bar * SR), N - a); tb = np.arange(bn) / SR; bass[a:a + bn] += np.sin(2 * np.pi * hz(c[0] - 12) * tb) * np.exp(-tb * 1.4) * .7
    for j in range(8):
        s = a + int(j * beat / 2 * SR); pn = min(int(.5 * SR), N - s)
        if pn <= 0: continue
        mm = c[[0, 1, 2, 3, 2, 1, 3, 2][j]] + 12; tp = np.arange(pn) / SR
        arp[s:s + pn] += (np.sin(2 * np.pi * hz(mm) * tp) + .3 * np.sin(2 * np.pi * hz(mm) * 3 * tp) * np.exp(-tp * 9)) * np.exp(-tp * 6) * .35
    for j in range(4):
        s = a + int(j * beat * SR); kn = min(int(.25 * SR), N - s)
        if kn <= 0: continue
        tk = np.arange(kn) / SR
        if j in (0, 2): drums[s:s + kn] += np.sin(2 * np.pi * (55 + 90 * np.exp(-tk * 30)) * tk) * np.exp(-tk * 14) * .8
        else: drums[s:s + kn] += np.sin(2 * np.pi * 180 * tk) * np.exp(-tk * 30) * .25 + rng.normal(0, 1, kn) * np.exp(-tk * 40) * .12
        h = s + int(beat / 2 * SR); hn = min(int(.06 * SR), N - h)
        if hn > 0: drums[h:h + hn] += rng.normal(0, 1, hn) * np.exp(-np.arange(hn) / SR * 70) * .1
# one dropout for the twist ("Here's the twist" -> back in on "In 1397")
dip = np.ones(N); ta, tb = int((C['12.1'] - .05) * SR), int((C['13.0'] - .05) * SR); dip[ta:tb] = .25
dip = np.convolve(dip, np.ones(4800) / 4800, 'same'); dip[:4800] = 1; dip[-4800:] = 1
music = (pad * .9 + arp * .5 + bass * .5 + drums * dip * .5) * np.r_[np.ones(N)]
music = np.convolve(music, np.ones(6) / 6, 'same'); music *= dip ** .5
music = music / (np.sqrt((music ** 2).mean()) or 1) * .03
fi = np.linspace(0, 1, LW); music[:LW] = music[:LW] * fi + music[N0:N0 + LW] * (1 - fi); music = music[:N0]; voice = voice[:N0]; N = N0
hop = SR // 100; PRE = 4 * SR; vv = np.r_[voice[-PRE:], voice]; e = np.sqrt(np.convolve(vv ** 2, np.ones(hop) / hop, 'same'))[::hop]
act = (e > .01).astype(float); sm = np.zeros_like(act); g = 0
for i, x in enumerate(act): g = g + (x - g) * (.3 if x > g else .012); sm[i] = g
sm = sm[PRE // hop:]; duck = np.interp(np.arange(N) / SR, np.arange(len(sm)) * hop / SR, 1 - .6 * sm)
mix = voice + music * duck + fx
pk = np.abs(mix).max(); mix = mix / pk * .89 if pk > .89 else mix
sf.write(os.path.join(AD, 'mix_raw.wav'), np.stack([mix, mix], 1), SR)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', os.path.join(AD, 'mix_raw.wav'), '-af', 'volume=1.0', '-ar', '48000', os.path.join(AD, 'mix_final.wav')], check=True)
print('mix', round(len(mix) / SR, 2), 's; events', len(EV), 'cam', len(T['cam']) - 1)
