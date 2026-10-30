#!/usr/bin/env python3
"""Narrator consistency check: does each TTS take sound like the channel's narrator?

Usage: python3 voicecheck.py ref.wav [ref2.wav ...] -- take1.wav take2.wav ...
Reference = one or more approved narrator takes. For each take prints median pitch, tone (5-band EQ difference vs the reference)
and an MFCC timbre distance, then PASS/FAIL. Fail if pitch is > 1.5 semitones off, any tone band > 3 dB off, or timbre distance > 14.
Only the first 70 s of each file are measured (enough for a stable profile).
"""
import sys, numpy as np, librosa
SR = 16000; BANDS = [(80, 250), (250, 600), (600, 1500), (1500, 3000), (3000, 6000)]
def profile(path):
    y, _ = librosa.load(path, sr=SR, duration=70)
    f0, vf, _ = librosa.pyin(y, fmin=60, fmax=300, sr=SR, frame_length=1024)
    spec = 10 * np.log10((np.abs(librosa.stft(y, n_fft=1024)) ** 2).mean(1) + 1e-12)
    return float(np.nanmedian(f0[vf])), spec, librosa.feature.mfcc(y=y, sr=SR, n_mfcc=20).mean(1)
a = sys.argv[1:]; k = a.index("--"); refs, takes = a[:k], a[k + 1:]
R = [profile(r) for r in refs]; f0r = float(np.median([r[0] for r in R])); specr = np.mean([r[1] for r in R], 0); mfr = np.mean([r[2] for r in R], 0)
fr = librosa.fft_frequencies(sr=SR, n_fft=1024); mid = (fr > 250) & (fr < 3000)
print(f"reference pitch {f0r:.1f} Hz")
ok_all = True
for t in takes:
    f0, spec, mf = profile(t); st = 12 * np.log2(f0 / f0r); d = spec - specr; d -= d[mid].mean()
    tone = [float(np.mean(d[(fr >= x) & (fr < y)])) for x, y in BANDS]; tim = float(np.linalg.norm(mf[1:] - mfr[1:]))
    ok = abs(st) <= 1.5 and max(abs(v) for v in tone) <= 3 and tim <= 14; ok_all &= ok
    print(f"{'PASS' if ok else 'FAIL'}  {t.split('/')[-2]}/{t.split('/')[-1]:10s} pitch {f0:6.1f} Hz ({st:+.1f} st)  tone {[round(v, 1) for v in tone]}  timbre {tim:.1f}")
sys.exit(0 if ok_all else 1)
