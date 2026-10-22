"""Write a SEGMENTED Whisper align job for a Hindi take (default for every Hindi video since 22 Oct 2026).
Whisper 'small' drops or garbles whole stretches of long Hindi takes (Bengaluru lost lines 17-19); cutting the audio at
pauses into 6-10 s pieces fixes it. Usage (from the repo root):
  python3 bhugol-v2/hindi_align_job.py <id> outputs/tts/<job>/narration_hi.wav     -> jobs/align/<id>.json (push it)
Then check words_fit's 'interpolated' list: any proper noun in it needs its timing patched from words.txt by hand."""
import json, sys
import numpy as np, soundfile as sf
jid, wav = sys.argv[1:3]
x, sr = sf.read(wav, always_2d=True); x = x.mean(1); h = int(sr * .01); n = len(x) // h
db = 20 * np.log10(np.sqrt((x[:n * h].reshape(n, h) ** 2).mean(1)) + 1e-9); sp = db > db.max() - 38
cuts = [0.0]; i = 0
while i < n:
    if not sp[i]:
        j = i
        while j < n and not sp[j]: j += 1
        if j - i >= 30 and (i + j) // 2 * .01 - cuts[-1] > 6: cuts.append((i + j) // 2 * .01)
        i = j
    else: i += 1
cuts.append(n * .01)
seg = [[round(a, 2), round(b, 2)] for a, b in zip(cuts[:-1], cuts[1:])]
json.dump({'id': jid, 'audio': wav, 'lang': 'hi', 'model': 'small', 'segments': seg}, open(f'jobs/align/{jid}.json', 'w'))
print(f'jobs/align/{jid}.json: {len(seg)} segments')
