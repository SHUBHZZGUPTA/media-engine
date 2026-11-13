# Insert silence before chosen lines and (optionally) slow the take; shifts timing.json to match.
# Usage: python3 pad_lines.py <dir> <tempo> gap_default "i:g,i:g"
import json, sys, subprocess, numpy as np, soundfile as sf
d, tempo, g0, spec = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
G = {int(a): float(b) for a, b in (x.split(':') for x in spec.split(',') if x)}
T = json.load(open(d + '/timing.json')); OFF = T['offset']; x, sr = sf.read(d + '/voice.wav', always_2d=True)
L = T['lines']
cuts = [max(0, L[i]['start'] - OFF - .05) for i in range(1, len(L))]
segs = []; s0 = 0
for c in cuts: segs.append(x[int(s0 * sr):int(c * sr)]); s0 = c
segs.append(x[int(s0 * sr):])
y = [segs[0]]; sh = [0.0]
for i in range(1, len(L)):
    g = G.get(i, g0); y.append(np.zeros((int(g * sr), x.shape[1]))); y.append(segs[i]); sh.append(sh[-1] + g)
y = np.concatenate(y); sf.write(d + '/voice_pad.wav', y, sr)
for i, l in enumerate(L):
    l['start'] = round(l['start'] + sh[i], 3); l['end'] = round(l['end'] + sh[i], 3); l['words'] = [round(w + sh[i], 3) for w in l['words']]
if tempo != 1.0:
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', d + '/voice_pad.wav', '-filter:a', f'atempo={tempo}', d + '/voice.wav'], check=True)
    f = lambda t: round((t - OFF) / tempo + OFF, 3)
    for l in L: l['start'] = f(l['start']); l['end'] = f(l['end']); l['words'] = [f(w) for w in l['words']]
else:
    sf.write(d + '/voice.wav', y, sr)
json.dump(T, open(d + '/timing.json', 'w'), indent=1); print('padded ->', round(len(y) / sr / tempo, 2), 's')
