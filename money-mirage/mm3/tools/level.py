# Even out the narration: (1) match each TTS part's tone (long-term spectrum) to the whole narration's average,
# (2) bring every line to the same speech loudness. Timing is untouched, so the rendered video still lines up.
# in: audio/voice.wav (+ timing.json, spec.json)  out: audio/voice_lev.wav
import json, os, sys, numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from mmpaths import *
from scipy.signal import stft, istft
S = json.load(open('spec.json')); T = json.load(open('audio/timing.json')); off = T['offset']
x, sr = sf.read('audio/voice.wav'); x = x if x.ndim == 1 else x.mean(1)
L = [(t['start'] - off, t['end'] - off, s['ch'], s.get('speaker')) for s, t in zip(S['lines'], T['lines'])]
PARTS = EPC.get('tts_parts', [[0, 1], [2, 3], [4, 5], [6, 7]])
part = lambda ch: next(k for k, (a, b) in enumerate(PARTS) if a <= ch <= b)     # which Gemini request the line came from
# --- 1) tone match per part (narrator lines only), 1/3-octave smoothed, clamped to +-5 dB
nper = 2048; f, tt, Z = stft(x, sr, nperseg=nper, noverlap=nper * 3 // 4)
P = np.abs(Z) ** 2; e = P.sum(0); act = e > np.percentile(e, 40)
fr_part = np.full(len(tt), -1); fr_nar = np.zeros(len(tt), bool)
for a, b, ch, sp in L:
    m = (tt >= a) & (tt <= b); fr_part[m] = part(ch); fr_nar[m] |= sp is None
ref = P[:, act & fr_nar].mean(1)
def smooth(curve):
    out = np.empty_like(curve)
    for i, fc in enumerate(f):
        lo, hi = fc / 2 ** (1 / 6), fc * 2 ** (1 / 6); m = (f >= lo) & (f <= hi); out[i] = curve[m].mean() if m.any() else curve[i]
    return out
G = np.ones((len(PARTS), len(f)))
for k in range(len(PARTS)):
    m = act & fr_nar & (fr_part == k)
    if m.sum() < 50: continue
    db = 10 * np.log10(smooth(ref) / smooth(P[:, m].mean(1)))
    db = np.clip(db - np.median(db[(f > 200) & (f < 4000)]), -5, 5); db[f < 70] = 0; db[f > 12000] *= .5   # tone only; level is step 2
    G[k] = 10 ** (db / 20); print(f'part {k + 1}: tone correction low {db[(f>80)&(f<300)].mean():+.1f} dB, presence {db[(f>2000)&(f<5000)].mean():+.1f} dB, air {db[(f>6000)&(f<10000)].mean():+.1f} dB')
gain = np.ones((len(f), len(tt)))
fp = fr_part.copy()   # frames between lines take the last part
for i in range(1, len(fp)):
    if fp[i] < 0: fp[i] = fp[i - 1]
fp[fp < 0] = 0
gain = G[fp].T
_, y = istft(Z * gain, sr, nperseg=nper, noverlap=nper * 3 // 4); y = y[:len(x)]
# --- 2) per-line loudness: active-speech RMS to the narration median, gains glide between lines
hop = int(.01 * sr)
def act_db(seg):
    r = np.sqrt(np.convolve(seg ** 2, np.ones(hop) / hop, 'valid')[::hop]); r = r[r > .01]
    return 20 * np.log10(np.sqrt((r ** 2).mean())) if len(r) else None
lv = [act_db(y[int(a * sr):int(b * sr)]) for a, b, _, _ in L]
target = np.median([v for v, (_, _, _, sp) in zip(lv, L) if v is not None and sp is None])
pts_t, pts_g = [0.0], []
for (a, b, ch, sp), v in zip(L, lv):
    g = 0 if v is None else float(np.clip(target - v + (1.0 if sp else 0), -6, 9))
    pts_t += [a + .02, b - .02]; pts_g += [g, g]
pts_g = [pts_g[0]] + pts_g; pts_t.append(len(y) / sr); pts_g.append(pts_g[-1])
env = 10 ** (np.interp(np.arange(len(y)) / sr, pts_t, pts_g) / 20)
y = y * env
pk = np.abs(y).max(); y = y / pk * .95 if pk > .95 else y
sf.write('audio/voice_lev.wav', y, sr)
after = [act_db(y[int(a * sr):int(b * sr)]) for a, b, _, _ in L]
print('line loudness spread before: %.1f dB  after: %.1f dB (target %.1f dBFS)' % (np.ptp([v for v in lv if v]), np.ptp([v for v in after if v]), target))
