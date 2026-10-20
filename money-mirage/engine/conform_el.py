# Build the narration track from per-line ElevenLabs files (no time-stretch, no pitch-shift).
# Pass 1 (no args): trims, levels and spaces the lines -> build/narration.wav + build/lines_raw.json
# Pass 2 (--words): maps Whisper words (outputs/align/mm-el/words.txt) onto script words -> build/timing.json
import json, re, sys, subprocess, wave, difflib, os, numpy as np
ME = '/home/claude/media-engine'; OUT = '/home/claude/mm-work/engine/build'; SR = 48000
LD = f'{ME}/outputs/fetch/mm-el-lines'
src = open('/home/claude/mm-work/script_v2.md').read(); secs = re.split(r'^# ', src, flags=re.M)[1:]
SL = []
for ci, s in enumerate(secs):
    for l in s.split('\n')[1:]:
        l = l.strip()
        if not l: continue
        who, _, txt = l.partition(': ')
        m = re.match(r'\[([^\]]*)\] (.*)', txt)
        if m: txt = m.group(2)
        SL.append({'ch': ci, 'spk': {'N': 'N', 'GOLDIE': 'G', 'BILL': 'B'}[who], 'text': txt})
norm = lambda s: re.sub(r"[^a-z0-9' ]", " ", s.lower().replace('-', ' ').replace('’', "'")).split()
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
def trim(x):
    hop = 480; r = np.array([np.sqrt((x[i:i + hop] ** 2).mean()) for i in range(0, len(x) - hop, hop)]); act = np.where(r > .01)[0]
    a = max(0, act[0] * hop - int(.04 * SR)); b = min(len(x), (act[-1] + 1) * hop + int(.12 * SR)); return x[a:b]
if '--words' not in sys.argv:
    pieces = []; T = 0.0; lines = []
    sil = lambda s: np.zeros(int(s * SR), np.float32)
    for i, L in enumerate(SL):
        x = trim(load(f'{LD}/line_{i:02d}.mp3'))
        fr = x[:len(x) // 480 * 480].reshape(-1, 480); r = np.sqrt((fr ** 2).mean(1)); act = r[r > .02]
        x = x * min(3, max(.33, 10 ** (-17 / 20) / np.sqrt((act ** 2).mean())))
        prev = lines[-1] if lines else None
        if prev is None: pre = .35
        elif prev['ch'] != L['ch']: pre = 3.0 if prev['ch'] == 0 else 2.2
        elif L['spk'] != 'N' or prev['spk'] != 'N': pre = .45
        else: pre = .55
        pieces.append(sil(pre)); T += pre
        lines.append(dict(L, a=round(T, 3), b=round(T + len(x) / SR, 3))); pieces.append(x); T += len(x) / SR
    pieces.append(sil(1.2)); T += 1.2
    mix = np.concatenate(pieces); mix = mix / np.abs(mix).max() * .9
    with wave.open(f'{OUT}/narration.wav', 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    json.dump({'dur': round(T, 3), 'lines': lines}, open(f'{OUT}/lines_raw.json', 'w'))
    print('narration %.1f s (%.2f min), %d lines' % (T, T / 60, len(lines)))
else:
    R = json.load(open(f'{OUT}/lines_raw.json')); lines = R['lines']
    W = []
    for row in open(f'{ME}/outputs/align/mm-el/words.txt').read().strip().split('\n'):
        a, b, w = row.split(' ', 2); W.append((float(a), float(b), w))
    with wave.open(f'{OUT}/narration.wav') as w: mix = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    for L in lines:
        hw = [(x, a, b) for a, b, w in W if a >= L['a'] - .15 and a < L['b'] + .05 for x in norm(w)]
        dws = L['text'].split(); dtok, downer = [], []
        for di, dw in enumerate(dws):
            for x in norm(dw): dtok.append(x); downer.append(di)
        ta = [None] * len(dws); tb = [None] * len(dws)
        for op, a1, b1, c1, d1 in difflib.SequenceMatcher(None, dtok, [h[0] for h in hw], autojunk=False).get_opcodes():
            if op == 'equal':
                for k in range(b1 - a1):
                    di = downer[a1 + k]; h = hw[c1 + k]; ta[di] = h[1] if ta[di] is None else ta[di]; tb[di] = h[2]
        known = [i for i in range(len(dws)) if ta[i] is not None]
        for i in range(len(dws)):
            if ta[i] is None:
                lo = max([k for k in known if k < i], default=None); hi = min([k for k in known if k > i], default=None)
                t0 = tb[lo] if lo is not None else L['a']; t1 = ta[hi] if hi is not None else L['b']
                nl = (hi if hi is not None else len(dws)) - (lo if lo is not None else -1); pos = i - (lo if lo is not None else -1)
                ta[i] = t0 + (t1 - t0) * (pos - 1) / nl; tb[i] = t0 + (t1 - t0) * pos / nl
        L['d'] = [[w, round(ta[i], 3), round(tb[i], 3)] for i, w in enumerate(dws)]
        L['miss'] = len(dws) - len(known)
    env = {}
    for i, L in enumerate(lines):
        if L['spk'] == 'N': continue
        a, b = int(L['a'] * SR), int(L['b'] * SR); hop = SR // 30
        e = [float(np.sqrt((mix[x:x + hop] ** 2).mean())) for x in range(a, b, hop)]; mx = max(e) or 1
        env[str(i)] = [round(min(1, v / mx * 1.3), 2) for v in e]
    chs = []
    for c in range(len(secs)):
        ls = [l for l in lines if l['ch'] == c]; chs.append({'n': c, 'title': secs[c].split('\n')[0].strip(), 'a': ls[0]['a'], 'b': ls[-1]['b']})
    json.dump({'dur': R['dur'], 'lines': lines, 'chapters': chs, 'env': env}, open(f'{OUT}/timing.json', 'w'))
    print('timing ok; unmatched words per line:', [(i, l['miss']) for i, l in enumerate(lines) if l['miss'] > 2])
    for c in chs: print('  ch%d %6.1f-%6.1f' % (c['n'], c['a'], c['b']))
