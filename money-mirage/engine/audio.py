# Money Mirage audio: synthesized music bed (per chapter), synthesized SFX at cue times, ducking, final mix.
# Usage: python3 audio.py  (reads build/timing.json, build/narration.wav, build/sfx.json) -> build/mix.wav
import json, wave, numpy as np
from scipy.signal import fftconvolve, butter, sosfilt
SR = 48000; B = '/home/claude/mm-work/engine/build'
rng = np.random.default_rng(7)
TIM = json.load(open(f'{B}/timing.json')); DUR = TIM['dur']; N = int(DUR * SR) + SR

def rd(p):
    with wave.open(p) as w: return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
def env_adsr(n, a=.01, d=.1, s=.6, r=.2):
    t = np.arange(n) / SR; e = np.ones(n) * s; L = n / SR
    e[t < a] = t[t < a] / a; m = (t >= a) & (t < a + d); e[m] = 1 - (1 - s) * (t[m] - a) / d
    rr = t > L - r; e[rr] *= np.clip((L - t[rr]) / r, 0, 1); return e
def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
def hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
def bp(x, f1, f2): return sosfilt(butter(2, [f1, f2], 'band', fs=SR, output='sos'), x)
def mtof(m): return 440 * 2 ** ((m - 69) / 12)
IR = rng.standard_normal(int(2.2 * SR)) * np.exp(-np.arange(int(2.2 * SR)) / SR * 3.2); IR = lp(IR, 5000); IR /= np.abs(IR).sum() ** .5 * 6
def verb(x, wet=.3): return x * (1 - wet) + fftconvolve(x, IR)[:len(x)] * wet

# ---------------- SFX ----------------
def noise(n): return rng.standard_normal(n).astype(np.float32)
def S_pop():
    n = int(.12 * SR); t = np.arange(n) / SR; f = 900 * np.exp(-t * 18) + 300
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 30) * .6
def S_whoosh(L=.45):
    n = int(L * SR); x = noise(n); t = np.arange(n) / SR; out = np.zeros(n)
    for k in range(0, n, 2400):
        seg = x[k:k + 2400]; fc = 300 + 2600 * np.sin(np.pi * min(1, k / n)) ; out[k:k + 2400] = bp(seg, fc * .6, fc * 1.4)
    return out * np.sin(np.pi * t / L) ** 2 * .5
def S_swoosh(): return S_whoosh(.6) * .9
def S_stamp():
    n = int(.35 * SR); t = np.arange(n) / SR
    body = np.sin(2 * np.pi * (70 + 80 * np.exp(-t * 25)) * t) * np.exp(-t * 14); click = lp(noise(n), 2500) * np.exp(-t * 60) * .6
    return (body + click) * .9
def S_thud(): return S_stamp() * 1.1
def S_clink():
    n = int(.9 * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for f, a, dk in [(2093, 1, 5), (3140, .6, 7), (4400, .4, 9), (5280, .25, 11)]: x += a * np.sin(2 * np.pi * f * t) * np.exp(-t * dk)
    return x * .22
def S_ping():
    n = int(.6 * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * 1320 * t) + .4 * np.sin(2 * np.pi * 2640 * t)) * np.exp(-t * 7) * .25
def S_tick():
    n = int(.03 * SR); t = np.arange(n) / SR; return hp(noise(n), 3000) * np.exp(-t * 200) * .5
def S_crack():
    n = int(.5 * SR); t = np.arange(n) / SR; x = hp(noise(n), 800) * np.exp(-t * 12)
    x *= (rng.random(n) < .06) * 2.5 + .3; return lp(x, 6000) * .5
def S_snap():
    n = int(.25 * SR); t = np.arange(n) / SR; return (hp(noise(n), 1500) * np.exp(-t * 40) + np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 30) * .4) * .6
def S_flip():
    n = int(.25 * SR); t = np.arange(n) / SR; return bp(noise(n), 1200, 5000) * np.exp(-((t - .06) / .04) ** 2) * .6
def S_zip():
    n = int(.4 * SR); t = np.arange(n) / SR; return bp(noise(n), 2000, 7000) * (np.sin(2 * np.pi * 60 * t) > 0) * np.sin(np.pi * t / .4) * .35
def S_boing():
    n = int(.5 * SR); t = np.arange(n) / SR; f = 220 + 120 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 4)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6) * .35
def S_sting():
    n = int(3.0 * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for m, dl in [(50, 0), (57, .0), (62, .08), (65, .16), (69, .24), (74, .32)]:
        tt = np.clip(t - dl, 0, None); x += np.sin(2 * np.pi * mtof(m) * tt) * np.exp(-tt * 1.4) * (t >= dl) * .18
    x += lp(noise(n), 1500) * np.exp(-t * 3) * .08
    return verb(x, .45)
def S_chapter():
    n = int(1.2 * SR); t = np.arange(n) / SR; x = S_whoosh(.7); y = np.zeros(n); y[:len(x)] += x * .7
    y += np.sin(2 * np.pi * 110 * t) * np.exp(-t * 3) * .35 + np.sin(2 * np.pi * mtof(69) * t) * np.exp(-t * 4) * .08
    return verb(y, .35)
def S_clang():
    n = int(1.4 * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for f, a in [(180, 1), (497, .7), (811, .5), (1253, .4), (1771, .3)]: x += a * np.sin(2 * np.pi * f * t) * np.exp(-t * 3.5)
    return (x * .2 + lp(noise(n), 3000) * np.exp(-t * 25) * .5) * .8
def S_static():
    n = int(.8 * SR); t = np.arange(n) / SR; return bp(noise(n), 500, 6000) * np.exp(-t * 2) * .25
def S_crickets():
    n = int(1.8 * SR); t = np.arange(n) / SR; chirp = np.sin(2 * np.pi * 4500 * t) * (np.sin(2 * np.pi * 30 * t) > .3) * (np.sin(2 * np.pi * 1.6 * t) > 0)
    return chirp * .07
def S_register():
    a = S_clink(); b = S_ping(); n = max(len(a), int(.2 * SR) + len(b)); x = np.zeros(n); x[:len(a)] += a; x[int(.2 * SR):int(.2 * SR) + len(b)] += b * 1.4; return x
def S_sparkle():
    n = int(1.0 * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for k, m in enumerate([84, 88, 91, 96, 100]):
        tt = np.clip(t - k * .07, 0, None); x += np.sin(2 * np.pi * mtof(m) * tt) * np.exp(-tt * 9) * (t >= k * .07) * .09
    return verb(x, .4)
def S_typing():
    n = int(1.2 * SR); x = np.zeros(n)
    for k in range(9): s = int((k * .13 + rng.random() * .03) * SR); c = S_tick() * 1.4; x[s:s + len(c)] += c[:len(x) - s]
    return x
def S_splash():
    n = int(.7 * SR); t = np.arange(n) / SR; return lp(noise(n), 3000) * np.exp(-t * 6) * np.sin(np.pi * np.clip(t / .05, 0, .5)) * .4
def S_shimmer():
    n = int(2.0 * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for m in [79, 83, 86, 91]: x += np.sin(2 * np.pi * mtof(m) * t + 3 * np.sin(2 * np.pi * 5 * t)) * .04
    return verb(x * np.sin(np.pi * t / 2.0), .5)
SFX = {k[2:].lower(): v for k, v in globals().items() if k.startswith('S_')}
CACHE = {}

# ---------------- music ----------------
def pluck(f, dur, bright=.5):
    n = int(dur * SR); p = max(2, int(SR / f)); buf = lp(noise(p), 2000 + 6000 * bright); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]; buf[i % p] = .5 * (buf[i % p] + buf[(i + 1) % p]) * .996
    return out
PL = {}
def pl(m, dur, br):
    k = (m, round(dur, 2), br)
    if k not in PL: PL[k] = pluck(mtof(m), dur, br)
    return PL[k]
def pad(freqs, n):
    t = np.arange(n) / SR; x = np.zeros(n)
    for f in freqs:
        for h in range(1, 6): x += np.sin(2 * np.pi * f * h * t * (1 + .0015 * np.sin(2 * np.pi * .2 * t + h))) / h * .5
    return lp(x, 900)
# chord progressions (MIDI roots + quality) per mood
MOODS = {
    'wonder': [(57, 'm'), (53, 'M'), (48, 'M'), (55, 'M')],    # Am F C G
    'tension': [(50, 'm'), (46, 'M'), (45, 'M'), (50, 'm')],   # Dm Bb A Dm
    'drive': [(52, 'm'), (48, 'M'), (55, 'M'), (50, 'M')],     # Em C G D
    'resolve': [(53, 'M'), (55, 'M'), (57, 'm'), (52, 'm')],   # F G Am Em
}
CHMOOD = ['wonder', 'wonder', 'drive', 'tension', 'drive', 'tension', 'drive', 'resolve']
BPM = 92; BEAT = 60 / BPM; BAR = BEAT * 4
def tri(root, q): return [root, root + (3 if q == 'm' else 4), root + 7]
music = np.zeros(N, np.float32)
for c in TIM['chapters']:
    a = c['a'] - (2.2 if c['n'] else .3); b = (TIM['chapters'][c['n'] + 1]['a'] - 2.2) if c['n'] < 7 else DUR
    mood = MOODS[CHMOOD[c['n']]]; n0 = int(max(0, a) * SR); L = int((b - max(0, a)) * SR); seg = np.zeros(L + SR * 3)
    nb = int(np.ceil((b - a) / BAR))
    for k in range(nb):
        root, q = mood[(k // 2) % 4]; s = int(k * BAR * SR); e = min(len(seg), s + int(BAR * SR))
        fr = [mtof(m) for m in tri(root - 12, q)]; pd = pad(fr, e - s) * env_adsr(e - s, .4, .3, .8, .5); seg[s:e] += pd * .05
        bass = np.sin(2 * np.pi * mtof(root - 24) * np.arange(e - s) / SR) * env_adsr(e - s, .02, .4, .5, .3); seg[s:e] += bass * .09
        arp = tri(root, q) + [root + 12]; pat = [0, 2, 1, 3, 2, 1, 3, 2]
        for j in range(8):
            if CHMOOD[c['n']] == 'tension' and j % 2: continue
            st = s + int(j * BEAT / 2 * SR); nt = pl(arp[pat[j]] + (12 if CHMOOD[c['n']] == 'resolve' else 0), .7, .45)
            seg[st:st + len(nt)] += nt[:len(seg) - st] * .07
        if CHMOOD[c['n']] in ('drive', 'tension'):
            for j in range(4):
                st = s + int(j * BEAT * SR); kl = int(.25 * SR); tt = np.arange(kl) / SR
                kick = np.sin(2 * np.pi * (50 + 90 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 12)
                if j % 2 == 0: seg[st:st + kl] += kick[:len(seg) - st] * .12
                hh = hp(noise(int(.05 * SR)), 7000) * np.exp(-np.arange(int(.05 * SR)) / SR * 80) * .025
                st2 = st + int(BEAT / 2 * SR); seg[st2:st2 + len(hh)] += hh[:len(seg) - st2]
    seg = verb(seg, .3)
    fade = np.ones(len(seg)); fi = int(1.2 * SR); fade[:fi] = np.linspace(0, 1, fi); fo = int(2.5 * SR); end = L
    fade[end - fo:end] *= np.linspace(1, 0, fo); fade[end:] = 0
    seg *= fade; e = min(N, n0 + len(seg)); music[n0:e] += seg[:e - n0]
# ---------------- ducking under narration ----------------
nar = rd(f'{B}/narration.wav'); voice = np.zeros(N, np.float32); voice[:len(nar)] = nar
hop = 480; envv = np.array([np.sqrt((voice[i:i + hop] ** 2).mean()) for i in range(0, N, hop)])
act = (envv > .02).astype(float); sm = np.convolve(act, np.ones(40) / 40, 'same')  # ~0.4 s smoothing
gain = 1 - .55 * np.clip(sm * 1.5, 0, 1); gain = np.repeat(gain, hop)[:N]
music *= gain
# ---------------- SFX placement ----------------
fx = np.zeros(N, np.float32); cues = json.load(open(f'{B}/sfx.json'))
last = {}
for name, t, vol in sorted(cues, key=lambda c: c[1]):
    if name not in SFX or t < 0: continue
    if t - last.get(name, -9) < .12: continue
    last[name] = t
    if name not in CACHE: CACHE[name] = SFX[name]().astype(np.float32)
    x = CACHE[name] * vol * {'whoosh': .55, 'swoosh': .6, 'tick': .7, 'pop': .8}.get(name, 1); s = int(t * SR); e = min(N, s + len(x)); fx[s:e] += x[:e - s]
fx = verb(fx, .12)
mix = voice * 1.0 + music * 1.0 + fx * .55
mix = mix[:int((DUR + .5) * SR)]
mix /= max(1e-6, np.abs(mix).max()) / .95
with wave.open(f'{B}/mix.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
print('mix ok', len(mix) / SR, 'cues', len(cues))
