# Tighten the Gemini take (cap pauses, gentle tempo) and produce timing.json for the build.
# Usage: python3 retime.py raw.wav words.txt script.json out_dir
import json, re, sys, os, subprocess, difflib
import numpy as np, soundfile as sf
RAW, WORDS, SCRIPT, OUT = sys.argv[1:5]; os.makedirs(OUT, exist_ok=True)
TEMPO, LEAD = 1.05, .12
x, sr = sf.read(RAW); x = x if x.ndim == 1 else x.mean(1)
S = json.load(open(SCRIPT))
W = []
for ln in open(WORDS):
    a, b, w = ln.split(' ', 2); W.append((float(a), float(b), w.strip()))
norm = lambda s: re.sub(r'[\W_]', '', s.lower().replace('[offended, squeaky]', ''))
# TTS tokens with their line/chunk
TOK = []
for li, L in enumerate(S['lines']):
    for ci, c in enumerate(L['tc']):
        for w in c.split(): TOK.append({'li': li, 'ci': ci, 'w': w})
# whisper may merge/split hyphenated numbers: compare on split pieces
def pieces(s): return [p for p in re.split(r'[\s\-]+', s) if norm(p)]
A = [(norm(p), i) for i, t in enumerate(TOK) for p in pieces(t['w'])]
B = [(norm(p), j) for j, w in enumerate(W) for p in pieces(w[2])]
sm = difflib.SequenceMatcher(a=[a for a, _ in A], b=[b for b, _ in B], autojunk=False)
st = [None] * len(TOK); en = [None] * len(TOK); wmap = [None] * len(TOK)
for blk in sm.get_matching_blocks():
    for k in range(blk.size):
        ti = A[blk.a + k][1]; wj = B[blk.b + k][1]
        if st[ti] is None: st[ti] = W[wj][0]; wmap[ti] = wj
        en[ti] = W[wj][1]
# unmatched runs (numbers: Whisper writes digits) -> spread the unmatched Whisper words between the anchors
i = 0
while i < len(TOK):
    if st[i] is not None: i += 1; continue
    j = i
    while j < len(TOK) and st[j] is None: j += 1
    p = i - 1; q = j if j < len(TOK) else None
    w0 = (wmap[p] + 1) if p >= 0 else 0; w1 = wmap[q] if q is not None else len(W)
    if w1 > w0:
        a, b = W[w0][0], W[w1 - 1][1]; n = j - i
        for k in range(n): st[i + k] = a + (b - a) * k / n; en[i + k] = a + (b - a) * (k + 1) / n
    i = j
miss = [TOK[i]['w'] for i in range(len(TOK)) if st[i] is None]
print('unmatched tokens:', len(miss), miss[:20])
# interpolate gaps
idx = [i for i in range(len(TOK)) if st[i] is not None]
for i in range(len(TOK)):
    if st[i] is None:
        p = max([j for j in idx if j < i], default=None); q = min([j for j in idx if j > i], default=None)
        if p is None: st[i], en[i] = 0, st[q]
        elif q is None: st[i] = en[p]; en[i] = en[p] + .3
        else: f = (i - p) / (q - p); st[i] = en[p] + (st[q] - en[p]) * f; en[i] = st[i] + .25
for i in range(len(TOK)): en[i] = max(en[i], st[i] + .05)
# energy for silence detection
hop = int(sr * .005); e = np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, 'same'))
def silent_span(a, b):
    i0, i1 = int(a * sr), int(b * sr)
    if i1 - i0 < int(.06 * sr): return None
    seg = e[i0:i1] < .012
    if not seg.any(): return None
    # longest silent run
    best = (0, 0); s = None
    for k, v in enumerate(np.append(seg, False)):
        if v and s is None: s = k
        if not v and s is not None:
            if k - s > best[1] - best[0]: best = (s, k)
            s = None
    return (i0 + best[0]) / sr, (i0 + best[1]) / sr
KEEP = {}   # token index -> max pause before it
for i, t in enumerate(TOK):
    if i and TOK[i - 1]['li'] != t['li']: KEEP[i] = .34
for i, t in enumerate(TOK):
    if t['li'] == 12 and t['ci'] == 2 and TOK[i - 1]['ci'] == 1: KEEP[i] = .55
    if t['li'] == 3 and t['ci'] == 1 and TOK[i - 1]['ci'] == 0: KEEP[i] = .45   # after "Well..."
    if t['li'] == 8 and i and TOK[i - 1]['li'] == 7: KEEP[i] = .45
    if t['li'] == 16 and TOK[i - 1]['li'] == 15: KEEP[i] = .30
cuts = []
GLOBAL = os.environ.get('GLOBAL_SIL') == '1'
if GLOBAL:   # trim every silent run (token boundaries are approximate for transliterated Whisper output)
    sil = e < .012; s0 = None; runs = []
    for k2, v in enumerate(np.append(sil, False)):
        if v and s0 is None: s0 = k2
        if not v and s0 is not None:
            runs.append((s0 / sr, k2 / sr)); s0 = None
    keep_at = {st[i]: c for i, c in KEEP.items() if c > .34}
    for a0, b0 in runs:
        if a0 < .05 or b0 > len(x) / sr - .05: continue
        cap = .30
        for tt, c in keep_at.items():
            if a0 - .3 <= tt <= b0 + .3: cap = c
        extra = (b0 - a0) - cap
        if extra > .02: m = (a0 + b0) / 2; cuts.append((m - extra / 2, m + extra / 2))
for i in (range(1, len(TOK)) if not GLOBAL else []):
    cap = KEEP.get(i, .26)
    sp = silent_span(en[i - 1], st[i] + .02)
    if not sp: continue
    a, b = sp; extra = (b - a) - cap
    if extra > .02: m = (a + b) / 2; cuts.append((m - extra / 2, m + extra / 2))
# build edited audio with 12 ms crossfades
segs = []; pos = 0; fade = int(.012 * sr)
for a, b in cuts: segs.append((pos, int(a * sr))); pos = int(b * sr)
segs.append((pos, len(x)))
outa = np.zeros(0)
for s0, s1 in segs:
    piece = x[s0:s1].copy()
    if len(outa) and len(piece) > fade:
        r = np.linspace(0, 1, fade); outa[-fade:] = outa[-fade:] * (1 - r) + piece[:fade] * r; piece = piece[fade:]
    outa = np.concatenate([outa, piece])
def warp(t):  # raw time -> edited time
    removed = 0
    for a, b in cuts:
        if t >= b: removed += (b - a) - .012
        elif t > a: removed += (t - a); break
    return t - removed
sf.write(os.path.join(OUT, 'voice_cut.wav'), outa, sr)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', os.path.join(OUT, 'voice_cut.wav'), '-af', f'atempo={TEMPO}', '-ar', '48000', os.path.join(OUT, 'voice.wav')], check=True)
T = lambda t: round(LEAD + warp(t) / TEMPO, 3)
lines = []
for li, L in enumerate(S['lines']):
    ix = [i for i, t in enumerate(TOK) if t['li'] == li]
    chunks = []
    for ci in range(len(L['tc'])):
        jx = [i for i in ix if TOK[i]['ci'] == ci]
        chunks.append({'start': T(st[jx[0]]), 'tok': [T(st[i]) for i in jx], 'end': T(en[jx[-1]])})
    lines.append({'start': T(st[ix[0]]), 'end': T(en[ix[-1]]), 'chunks': chunks})
dur_v = len(outa) / sr / TEMPO
json.dump({'offset': LEAD, 'voice_dur': round(dur_v, 3), 'lines': lines}, open(os.path.join(OUT, 'timing.json'), 'w'), indent=1)
print('cuts', len(cuts), 'removed %.2f s' % sum(b - a for a, b in cuts), 'voice %.2f s' % dur_v, 'last word end', lines[-1]['end'])
