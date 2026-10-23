# Free character voices: re-pitches the narrator on lines spoken by characters (spec.lines[].speaker),
# so one Holden narration can carry a cast. Line timing is unchanged (pitch only, duration kept).
# Usage: python3 voices.py <spec.json> <out_dir>    (reads/writes <out_dir>/voice.wav, uses <out_dir>/timing.json)
# spec.voices: {"bolivia": {"semitones": 5, "formant": "shifted", "gain_db": 0, "eq": "highpass=f=180"}}
#   semitones: + higher / - lower. formant: "shifted" = cartoon (chipmunk / giant), "preserved" = a different-sounding person.
#   eq: optional extra ffmpeg filter chain (e.g. "highpass=f=250,lowpass=f=5000" for a tiny radio-ish voice).
import sys, os, json, shutil, subprocess
import numpy as np, soundfile as sf

spec_p, out_dir = sys.argv[1:3]
SPEC = json.load(open(spec_p)); V = SPEC.get('voices', {})
vo_p = os.path.join(out_dir, 'voice.wav'); tim = json.load(open(os.path.join(out_dir, 'timing.json')))
OFF = tim['offset']
todo = [(li, L, SPEC['lines'][li].get('speaker')) for li, L in enumerate(tim['lines'])]
todo = [(li, L, who) for li, L, who in todo if who and who in V]
if not todo:
    print('voices: no character lines with a voice preset; narration unchanged'); sys.exit(0)
shutil.copy(vo_p, os.path.join(out_dir, 'voice_plain.wav'))
x, sr = sf.read(vo_p, always_2d=True)
tmp = os.path.join(out_dir, '_voices'); os.makedirs(tmp, exist_ok=True)
fz = int(.02 * sr)
for li, L, who in todo:
    v = V[who]
    a = max(0.0, L['start'] - OFF - .05)
    nxt = tim['lines'][li + 1]['start'] - OFF - .03 if li + 1 < len(tim['lines']) else len(x) / sr
    b = min(len(x) / sr, L['end'] - OFF + .35, nxt)
    i0, i1 = int(a * sr), int(b * sr)
    if i1 - i0 < 4 * fz: continue
    pi, po = os.path.join(tmp, f'{li}.wav'), os.path.join(tmp, f'{li}_v.wav')
    sf.write(pi, x[i0:i1], sr)
    ratio = 2 ** (float(v.get('semitones', 0)) / 12)
    chain = f"rubberband=pitch={ratio:.5f}:formant={v.get('formant', 'shifted')}:pitchq=quality"
    if v.get('eq'): chain += ',' + v['eq']
    if v.get('gain_db'): chain += f",volume={v['gain_db']}dB"
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', pi, '-af', chain, '-ar', str(sr), po], check=True)
    y, _ = sf.read(po, always_2d=True)
    n = i1 - i0
    y = y[:n] if len(y) >= n else np.vstack([y, np.zeros((n - len(y), y.shape[1]))])
    if y.shape[1] != x.shape[1]: y = np.repeat(y.mean(axis=1, keepdims=True), x.shape[1], axis=1)
    w = np.ones(n); w[:fz] = np.linspace(0, 1, fz); w[-fz:] = np.linspace(1, 0, fz); w = w[:, None]
    x[i0:i1] = x[i0:i1] * (1 - w) + y * w
    print(f"voices: line {li} '{L['text'][:40]}' -> {who} ({v.get('semitones', 0):+} st, {v.get('formant', 'shifted')})")
sf.write(vo_p, x, sr)
shutil.rmtree(tmp, ignore_errors=True)
print('voices ->', vo_p, '(plain narration kept as voice_plain.wav)')
