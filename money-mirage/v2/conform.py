# v2 narration from per-line Gemini files (no time-stretch, no pitch-shift).
# Pass 1: trim each line, shorten pauses inside a line longer than 0.6 s to 0.45 s (yt-edit dead-air rule),
#         level to -17 dB, join with fixed gaps -> build/narration.wav + build/lines_raw.json
# Pass 2 (--words <words.txt>): map Whisper words onto script words -> build/timing.json
import json, re, sys, subprocess, wave, difflib, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'build'); SR = 48000
os.makedirs(OUT, exist_ok=True)
SRC = os.environ.get('TTS_DIR', '/home/claude/media-engine/outputs/tts/mm2-preview-gemini')
script = open(os.path.join(HERE, os.environ.get('SCRIPT', 'SCRIPT_preview.md'))).read()
secs = re.split(r'^# ', script, flags=re.M)[1:]
SL = []; chars = []
for ci, s in enumerate(secs):
    for l in s.split('\n')[1:]:
        l = l.strip()
        if not l: continue
        who, _, txt = l.partition(': ')
        txt = re.sub(r'^\[[^\]]*\] ', '', txt)
        if who == 'N': SL.append({'ch': ci, 'spk': 'N', 'text': txt})
        else: chars.append((ci, who, txt))
if chars:  # all character lines of a section are one dialogue file
    SL.append({'ch': chars[0][0], 'spk': 'C', 'text': ' '.join(t for _, _, t in chars)})
norm = lambda s: re.sub(r"[^a-z0-9' ]", " ", s.lower().replace('-', ' ').replace('’', "'")).split()

def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768

def tighten(x, thr=.012, maxgap=.5, keep=.38):
    hop = 480; r = np.array([np.sqrt((x[i:i + hop] ** 2).mean()) for i in range(0, len(x) - hop, hop)]); act = r > thr
    idx = np.where(act)[0]
    a = max(0, idx[0] * hop - int(.04 * SR)); b = min(len(x), (idx[-1] + 1) * hop + int(.12 * SR))
    out = []; i = idx[0]; seg_start = a; k = idx[0]
    # walk silent runs inside the speech and shorten long ones from their middle
    runs = []; j = idx[0]
    while j < idx[-1]:
        if not act[j]:
            s0 = j
            while j < idx[-1] and not act[j]: j += 1
            if (j - s0) * hop / SR > maxgap: runs.append((s0 * hop, j * hop))
        j += 1
    pieces = []; cur = a; cut = 0.0
    for s0, s1 in runs:
        mid = (s0 + s1) // 2; half = int(keep * SR / 2)
        pieces.append(x[cur:mid - half]); cur = mid + half; cut += (s1 - s0) / SR - keep
    pieces.append(x[cur:b])
    return np.concatenate(pieces), cut

if '--words' not in sys.argv:
    files = sorted(f for f in os.listdir(SRC) if f.startswith('line_') and f.endswith('.wav'))
    assert len(files) == len(SL), (len(files), len(SL), files)
    pieces = []; T = 0.0; lines = []; tot_cut = 0
    sil = lambda s: np.zeros(int(s * SR), np.float32)
    for i, (L, f) in enumerate(zip(SL, files)):
        x, cut = tighten(load(os.path.join(SRC, f))); tot_cut += cut
        fr = x[:len(x) // 480 * 480].reshape(-1, 480); r = np.sqrt((fr ** 2).mean(1)); act = r[r > .02]
        x = x * min(3, max(.33, 10 ** (-17 / 20) / np.sqrt((act ** 2).mean())))
        prev = lines[-1] if lines else None
        pre = .12 if prev is None else (1.6 if prev['ch'] != L['ch'] else (.35 if 'C' in (L['spk'], prev['spk']) else .45))
        pieces.append(sil(pre)); T += pre
        lines.append(dict(L, a=round(T, 3), b=round(T + len(x) / SR, 3))); pieces.append(x); T += len(x) / SR
    pieces.append(sil(1.0)); T += 1.0
    mix = np.concatenate(pieces); mix = mix / np.abs(mix).max() * .89
    with wave.open(os.path.join(OUT, 'narration.wav'), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    json.dump({'dur': round(T, 3), 'lines': lines}, open(os.path.join(OUT, 'lines_raw.json'), 'w'), indent=1)
    print('narration %.1f s, %d lines, %.1f s of long pauses trimmed' % (T, len(lines), tot_cut))
else:
    R = json.load(open(os.path.join(OUT, 'lines_raw.json'))); lines = R['lines']
    Wd = []
    for row in open(sys.argv[sys.argv.index('--words') + 1]).read().strip().split('\n'):
        a, b, w = row.split(' ', 2); Wd.append((float(a), float(b), w))
    for L in lines:
        hw = [(x, a, b) for a, b, w in Wd if a >= L['a'] - .15 and a < L['b'] + .05 for x in norm(w)]
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
    json.dump({'dur': R['dur'], 'lines': lines}, open(os.path.join(OUT, 'timing.json'), 'w'), indent=1)
    print('timing ok; unmatched words per line:', [(i, l['miss']) for i, l in enumerate(lines) if l['miss']])
