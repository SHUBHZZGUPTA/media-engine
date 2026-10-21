"""Layer HyperFrames' bundled SFX (Pixabay licence: commercial use, no attribution) onto the synth mix, PEAK-aligned to beats.
Usage: python3 sfxlayer.py <mix_norm.wav> <out.wav> <sfx_stem.wav> <cues.json>
cues.json = [{"file": "whoosh-cinematic.mp3", "t": <seconds where the sound's peak lands>, "gain_db": -9, "what": "..."}]
Files (in node_modules/hyperframes/dist/skills/media-use/audio/assets/sfx/, see manifest.json there): whoosh, whoosh-short,
whoosh-cinematic, impact-bass-1/2, riser (10 s, peak at the end), glitch-1/2/3, typing, key-press, click, click-soft, pop, ping,
chime, sparkle, notification, error. Typical: impact-bass-1 on the hook's title landing, whoosh-cinematic + impact-bass-2 on a
hero (burn/flash) cut. Keep 2-4 per Short; the synth score carries the rest. Env SFX_DIR overrides the folder."""
import json, os, sys, subprocess, numpy as np, soundfile as sf
SFX = os.environ.get('SFX_DIR', '/home/claude/work/node_modules/hyperframes/dist/skills/media-use/audio/assets/sfx/')
mix_p, out_p, stem_p, cues_p = sys.argv[1:5]
mix, sr = sf.read(mix_p, always_2d=True); cues = json.load(open(cues_p))
def load(n):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', os.path.join(SFX, n), '-f', 'f32le', '-ac', '2', '-ar', str(sr), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
stem = np.zeros_like(mix)
for c in cues:
    a = load(c['file']); pk = int(np.argmax(np.abs(a).sum(1))); st = int(round(c['t'] * sr)) - pk
    a = a * 10 ** (c['gain_db'] / 20); s0 = max(0, st); a = a[s0 - st:]; n = min(len(a), len(stem) - s0); stem[s0:s0 + n] += a[:n]
out = mix + stem; pk = float(np.max(np.abs(out)))
if pk > .97: out = np.tanh(out / pk * 1.4) / np.tanh(1.4) * .97   # soft-limit only when the layer pushed past full scale
sf.write(out_p, out, sr); sf.write(stem_p, stem, sr); print('layered', len(cues), 'cues; peak before limit', round(pk, 3))
