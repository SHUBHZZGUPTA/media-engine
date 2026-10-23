# Word timings from the transcript, corrected with the audio's own pauses, then long pauses trimmed.
# Usage: python3 align.py <spec.json> <vo.wav> <words.txt> <out_dir>
# Writes <out_dir>/voice.wav (long pauses trimmed, optional tempo) and <out_dir>/timing.json.
import sys, json, re, difflib
import numpy as np, soundfile as sf

import os, subprocess
spec_p, vo_p, ww_p, out_dir = sys.argv[1:5]
SPEC = json.load(open(spec_p)); A = SPEC.get('align', {})
LINES = [l['text'] for l in SPEC['lines']]
LONG_BEFORE = {int(k): v for k, v in A.get('long_before', {}).items()}
CAP = A.get('cap', .42); OFF = A.get('offset', .3); TEMPO = A.get('tempo', 1.0)
os.makedirs(out_dir, exist_ok=True)
out_wav = os.path.join(out_dir, 'voice_tight.wav'); out_json = os.path.join(out_dir, 'timing.json')
x, sr = sf.read(vo_p, always_2d=True)
mono = x.mean(axis=1); hop = int(sr * .01); n = len(mono) // hop
db = 20 * np.log10(np.sqrt(np.mean(mono[:n * hop].reshape(n, hop) ** 2, axis=1)) + 1e-12)
db = np.convolve(db, np.ones(3) / 3, mode='same'); sp = db > max(np.percentile(db, 98) - 36, -55)
sil = []; i = 0
while i < n:
    if not sp[i]:
        j = i
        while j < n and not sp[j]: j += 1
        if j - i >= 12: sil.append((i * .01, j * .01))
        i = j
    else: i += 1
first_speech = next(k for k in range(n) if sp[k]) * .01
import unicodedata  # letters, marks and digits of any script (Hindi matras are marks)
norm = lambda w: ''.join(ch for ch in unicodedata.normalize('NFC', w.lower()) if unicodedata.category(ch)[0] in 'LMN')
Wt = [(float(a), float(b), norm(w)) for a, b, w in (ln.strip().split(' ', 2) for ln in open(ww_p) if ln.strip())]
wi = 0; lines_raw = []
for li, L in enumerate(LINES):
    toks = L.split(); st = []; en = []; prev_end = None
    for k, w in enumerate(toks):
        T = norm(w); got = Wt[wi][2]; ws, we = Wt[wi][0], Wt[wi][1]; wi += 1
        while wi < len(Wt) and abs(len(got + Wt[wi][2]) - len(T)) < abs(len(got) - len(T)):
            got += Wt[wi][2]; we = Wt[wi][1]; wi += 1
        if difflib.SequenceMatcher(None, got, T).ratio() < .5: print('WARN match', w, got)
        s = ws
        lo = (prev_end if prev_end is not None else (first_speech if li == 0 else ws - 1.5)) - .05
        for a, b in sil:  # audible start: after any pause that sits inside the transcript's stretched word
            if a >= lo and b <= we - .03: s = max(s, b)
        for a, b in sil:  # a word never starts inside a pause
            if a - .02 <= s < b - .05 and b < we + .6: s = b
        for a, b in sil:  # audible end: a pause that starts inside the transcript's word and runs past its end
            if s + .1 < a < we + .02 and b > we - .02: we = a + .03; break
        if li == 0 and k == 0: s = max(s, first_speech)
        st.append(s); en.append(we); prev_end = we
    for k in range(1, len(st)): st[k] = max(st[k], st[k - 1] + .08)
    lines_raw.append((st, en))
# pauses to trim: every silence longer than the cap (a longer breath before some lines)
line_starts = [ls[0][0] for ls in lines_raw]
cuts = []
if first_speech > .15: cuts.append((0.0, first_speech - .15))
for a, b in sil:
    if b <= first_speech: continue
    nxt = next((li for li, s0 in enumerate(line_starts) if s0 >= b - .15 and s0 <= b + .4), None)
    cap = LONG_BEFORE.get(nxt, CAP) if nxt is not None else CAP
    if b - a > cap: m = (a + b) / 2; r = (b - a) - cap; cuts.append((m - r / 2, m + r / 2))
cuts.sort()
end_t = lines_raw[-1][1][-1] + .45
def mapt(t):
    r = 0
    for c0, c1 in cuts:
        if t >= c1: r += c1 - c0
        elif t > c0: r += t - c0
    return t - r
segs = []; pos = 0.0
for c0, c1 in cuts: segs.append((pos, c0)); pos = c1
segs.append((pos, min(end_t, len(x) / sr))); segs = [s for s in segs if s[1] - s[0] > .03]
fx = int(.02 * sr); out = []
for k, (s0, s1) in enumerate(segs):
    piece = x[int(s0 * sr):int(s1 * sr)].copy()
    if k > 0: piece[:fx] *= np.linspace(0, 1, fx)[:, None]
    if k < len(segs) - 1: piece[-fx:] *= np.linspace(1, 0, fx)[:, None]
    out.append(piece)
y = np.concatenate(out); sf.write(out_wav, y, sr)
lines = [{'start': round(mapt(st[0]) + OFF, 3), 'end': round(mapt(en[-1]) + OFF, 3), 'words': [round(mapt(s) + OFF, 3) for s in st], 'text': LINES[li]} for li, (st, en) in enumerate(lines_raw)]
json.dump({'offset': OFF, 'lines': lines, 'removed': round(sum(c1 - c0 for c0, c1 in cuts), 2), 'audio_len': round(len(y) / sr, 3)}, open(out_json, 'w'), indent=1)
print('raw %.2fs -> %.2fs (removed %.2fs)' % (len(x) / sr, len(y) / sr, sum(c1 - c0 for c0, c1 in cuts)))
for L in lines: print(f"{L['start']:6.2f}-{L['end']:6.2f}  {L['text'][:50]}")
# optional pitch-preserving speed-up, timings scaled to match
final = os.path.join(out_dir, 'voice.wav')
LT = {int(k): float(v) for k, v in A.get('line_tempo', {}).items()}   # per-line pace, e.g. {"7": 1.0} keeps a punchline slower
if LT:
    # piecewise: each stretch from one line's start to the next gets that line's tempo (default TEMPO)
    d = json.load(open(out_json)); n_total = len(y) / sr
    bounds = [0.0] + [max(0.0, L['start'] - OFF - .06) for L in d['lines'][1:]] + [n_total]
    for i in range(1, len(bounds)): bounds[i] = max(bounds[i], bounds[i - 1])
    pieces, newb = [], [0.0]
    tmpd = os.path.join(out_dir, '_tempo'); os.makedirs(tmpd, exist_ok=True)
    for i in range(len(bounds) - 1):
        a, b = bounds[i], bounds[i + 1]; seg_ = y[int(a * sr):int(b * sr)]
        tp = LT.get(i, TEMPO)
        if len(seg_) < int(.02 * sr): pieces.append(seg_); newb.append(newb[-1] + len(seg_) / sr); continue
        if abs(tp - 1) > 1e-3:
            pi, po = os.path.join(tmpd, f'{i}.wav'), os.path.join(tmpd, f'{i}_t.wav'); sf.write(pi, seg_, sr)
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', pi, '-af', f'atempo={tp}', '-ar', str(sr), po], check=True)
            seg_, _ = sf.read(po, always_2d=True)
        pieces.append(seg_); newb.append(newb[-1] + len(seg_) / sr)
    fz = int(.008 * sr)
    for k in range(len(pieces)):
        if len(pieces[k]) > 2 * fz:
            if k > 0: pieces[k][:fz] *= np.linspace(0, 1, fz)[:, None]
            if k < len(pieces) - 1: pieces[k][-fz:] *= np.linspace(1, 0, fz)[:, None]
    yy = np.concatenate(pieces); tmpw = os.path.join(tmpd, 'all.wav'); sf.write(tmpw, yy, sr)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmpw, '-ar', '48000', final], check=True)
    def sc(t):
        u = t - OFF
        for i in range(len(bounds) - 1):
            if u <= bounds[i + 1] or i == len(bounds) - 2:
                span = max(1e-6, bounds[i + 1] - bounds[i]); return round(newb[i] + (u - bounds[i]) * (newb[i + 1] - newb[i]) / span + OFF, 3)
    for L in d['lines']: L['start'] = sc(L['start']); L['end'] = sc(L['end']); L['words'] = [sc(w) for w in L['words']]
    d['tempo'] = TEMPO; d['line_tempo'] = LT; json.dump(d, open(out_json, 'w'), indent=1)
    print('per-line tempo:', len(y) / sr, '->', round(len(yy) / sr, 2), 's', LT)
elif abs(TEMPO - 1) > 1e-3:
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', out_wav, '-af', f'atempo={TEMPO}', '-ar', '48000', final], check=True)
    d = json.load(open(out_json)); sc = lambda t: round((t - OFF) / TEMPO + OFF, 3)
    for L in d['lines']: L['start'] = sc(L['start']); L['end'] = sc(L['end']); L['words'] = [sc(w) for w in L['words']]
    d['tempo'] = TEMPO; json.dump(d, open(out_json, 'w'), indent=1)
else:
    import shutil; shutil.copy(out_wav, final)
print('voice ->', final, '| timing ->', out_json)
