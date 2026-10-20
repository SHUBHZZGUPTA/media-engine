# Conform the 3 narration parts into one track: even pacing, breathing room between lines,
# chapter gaps, pitch-shifted character voices. Writes narration.wav + timing.json.
import json, re, difflib, subprocess, wave, os, numpy as np
ME = '/home/claude/media-engine'; OUT = '/home/claude/mm-work/engine/build'; os.makedirs(OUT, exist_ok=True)
job = json.load(open(f'{ME}/jobs/tts/mm-pilot-sadaltager.json'))
src = open('/home/claude/mm-work/script_v2.md').read()
secs = re.split(r'^# ', src, flags=re.M)[1:]
# script lines with chapter index and speaker (display text = script text, not TTS spelling)
SL = []
for ci, s in enumerate(secs):
    for l in s.split('\n')[1:]:
        l = l.strip()
        if not l: continue
        who, _, txt = l.partition(': ')
        tag = ''
        m = re.match(r'\[([^\]]*)\] (.*)', txt)
        if m: tag, txt = m.group(1), m.group(2)
        SL.append({'ch': ci, 'spk': {'N': 'N', 'GOLDIE': 'G', 'BILL': 'B'}[who], 'text': txt})
TEMPO = {'a': 0.9, 'b': 1.0, 'c': 1.0}
SR = 48000
norm = lambda s: re.sub(r"[^a-z0-9' ]", " ", s.lower().replace('-', ' ')).split()

def load(path, tempo, pitch=None):
    af = []
    if tempo != 1.0: af.append(f'rubberband=tempo={tempo}')
    if pitch: af.append(f'rubberband=pitch={pitch}:formant=preserved')
    cmd = ['ffmpeg', '-v', 'error', '-i', path] + (['-af', ','.join(af)] if af else []) + ['-ac', '1', '-ar', str(SR), '-f', 's16le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.int16).astype(np.float32) / 32768

li = 0; pieces = []; T = 0.0; words_out = []; lines_out = []
def sil(sec): return np.zeros(int(sec * SR), np.float32)
for it, p in zip(job['items'], 'abc'):
    tts_lines = it['lines']; n = len(tts_lines)
    mine = SL[li:li + n]; li += n
    audio = load(f'{ME}/outputs/tts/mm-pilot-sadaltager/{it["name"]}.wav', TEMPO[p])
    W = []
    for row in open(f'{ME}/outputs/align/mm-pilot-{p}/words.txt').read().strip().split('\n'):
        a, b, w = row.split(' ', 2); W.append((float(a) / TEMPO[p], float(b) / TEMPO[p], w))
    # map each TTS line's word span onto whisper words
    ref, ref_line = [], []
    for k, (_, t) in enumerate(tts_lines):
        ws = norm(re.sub(r'^\[[^\]]*\] ', '', t)); ref += ws; ref_line += [k] * len(ws)
    hyp, hyp_idx = [], []
    for j, (_, _, w) in enumerate(W):
        for x in norm(w): hyp.append(x); hyp_idx.append(j)
    sm = difflib.SequenceMatcher(None, ref, hyp, autojunk=False)
    line_w = [[] for _ in range(n)]
    for op, a, b, c, d in sm.get_opcodes():
        if op == 'equal':
            for k in range(b - a): line_w[ref_line[a + k]].append(hyp_idx[c + k])
        elif op == 'replace':
            for k in range(a, b): line_w[ref_line[k]].extend(hyp_idx[c:d])
    span = []
    for k in range(n):
        js = sorted(set(line_w[k])); assert js, (p, k)
        span.append((W[js[0]][0], W[js[-1]][1], js))
    # cut points: midpoints of inter-line gaps
    cuts = [0.0] + [(span[k][1] + span[k + 1][0]) / 2 for k in range(n - 1)] + [len(audio) / SR]
    for k in range(n):
        L = mine[k]; a0, a1 = cuts[k], cuts[k + 1]
        seg = audio[int(a0 * SR):int(a1 * SR)]
        if L['spk'] != 'N':  # pitch the character line (Puck) into Goldie (lower) or Bill (higher)
            tmp = f'{OUT}/_c.wav'
            with wave.open(tmp, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(seg, -1, 1) * 32767).astype(np.int16).tobytes())
            seg = load(tmp, 1.0, 0.8 if L['spk'] == 'G' else 1.22)
            seg = seg * (1.15 if L['spk'] == 'G' else 1.0)
        # even loudness line to line (TTS drifts louder over long takes)
        fr = seg[:len(seg) // 480 * 480].reshape(-1, 480); r = np.sqrt((fr ** 2).mean(1)); act = r[r > .02]
        if len(act): seg = seg * min(2.5, max(.4, 10 ** (-16 / 20) / np.sqrt((act ** 2).mean())))
        # breathing room before this line
        prev = lines_out[-1] if lines_out else None
        if prev is None: pre = 0.3
        elif prev['ch'] != L['ch']: pre = 2.6 if prev['ch'] == 0 else 2.0   # chapter card (logo sting after cold open)
        elif L['spk'] != 'N' or prev['spk'] != 'N': pre = 0.35
        else: pre = 0.28
        pieces.append(sil(pre)); T += pre
        off = T - a0
        st, en, js = span[k]
        for j in js: words_out.append({'w': W[j][2], 'a': round(W[j][0] + off, 3), 'b': round(W[j][1] + off, 3), 'l': len(lines_out)})
        # display words (script spelling) timed against whisper words of this line
        hw = [(x, W[j][0] + off, W[j][1] + off) for j in js for x in norm(W[j][2])]
        dws = L['text'].split(); dtok, downer = [], []
        for di, dw in enumerate(dws):
            for x in norm(dw): dtok.append(x); downer.append(di)
        sm2 = difflib.SequenceMatcher(None, dtok, [h[0] for h in hw], autojunk=False)
        ta = [None] * len(dws); tb = [None] * len(dws)
        for op, a1, b1, c1, d1 in sm2.get_opcodes():
            if op == 'equal':
                for k in range(b1 - a1):
                    di = downer[a1 + k]; h = hw[c1 + k]
                    ta[di] = h[1] if ta[di] is None else ta[di]; tb[di] = h[2]
        known = [i for i in range(len(dws)) if ta[i] is not None]
        for i in range(len(dws)):
            if ta[i] is None:
                lo = max([k for k in known if k < i], default=None); hi = min([k for k in known if k > i], default=None)
                t0 = tb[lo] if lo is not None else st + off; t1 = ta[hi] if hi is not None else en + off
                nl = (hi if hi is not None else len(dws)) - (lo if lo is not None else -1)
                pos = i - (lo if lo is not None else -1)
                ta[i] = t0 + (t1 - t0) * (pos - 1) / nl; tb[i] = t0 + (t1 - t0) * pos / nl
        lines_out.append({'ch': L['ch'], 'spk': L['spk'], 'text': L['text'], 'a': round(st + off, 3), 'b': round(en + off, 3),
                          'd': [[w, round(ta[i], 3), round(tb[i], 3)] for i, w in enumerate(dws)]})
        pieces.append(seg); T += len(seg) / SR
pieces.append(sil(1.0)); T += 1.0
mix = np.concatenate(pieces)
mix = mix / max(1e-6, np.abs(mix).max()) * 0.89
with wave.open(f'{OUT}/narration.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
# mouth envelopes for character lines (30 fps, 0..1)
env = {}
for i, L in enumerate(lines_out):
    if L['spk'] == 'N': continue
    a, b = int(L['a'] * SR), int(L['b'] * SR); hop = SR // 30
    e = [float(np.sqrt((mix[x:x + hop] ** 2).mean())) for x in range(a, b, hop)]
    mx = max(e) or 1; env[i] = [round(min(1, v / mx * 1.3), 2) for v in e]
chs = []
for c in range(len(secs)):
    ls = [l for l in lines_out if l['ch'] == c]
    chs.append({'n': c, 'title': secs[c].split('\n')[0].strip(), 'a': ls[0]['a'], 'b': ls[-1]['b']})
json.dump({'dur': round(T, 3), 'words': words_out, 'lines': lines_out, 'chapters': chs, 'env': env}, open(f'{OUT}/timing.json', 'w'))
print('duration %.1f s = %.2f min, lines %d, words %d' % (T, T / 60, len(lines_out), len(words_out)))
for c in chs: print('  ch%d %6.1f-%6.1f %s' % (c['n'], c['a'], c['b'], c['title']))
