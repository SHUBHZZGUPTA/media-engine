#!/usr/bin/env python3
"""mix_mixed.py <narration.wav> <timing.ts> <music.mp3> <sfx dir> <duration s> <out.wav>

Voice + one library music track + sound effects on the chalkboard's beats, for any Money Mirage mixed-media Short (automatic cues) (scrapbook / marker comic / toy theatre / newsprint / toy brick).
Music sits ~10 dB under the voice between lines and 18 dB under while he speaks (smoothed gain);
effects land on the scene wipes, hero numbers, the strike, the gavel and the follow tap.
Prints the cue list and the measured voice-vs-bed gap per line."""
import json, subprocess, sys
import numpy as np

nar, timing, music, sfxdir, dur, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5]), sys.argv[6]
SR = 48000
def load(path):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()
db = lambda x: 20 * np.log10(max(x, 1e-9))
rms = lambda x: float(np.sqrt(np.mean(x ** 2))) if len(x) else 0.0

L = json.loads(open(timing).read().split("[] = ", 1)[1].rstrip().rstrip(";"))
N = int(dur * SR)
voice = np.zeros(N, np.float32); v = load(nar); voice[:min(N, len(v))] = v[:N]
# voice to a fixed speech level (~ -18 dBFS RMS over speech)
speech = np.concatenate([voice[int(l["s"] * SR):int(l["e"] * SR)] for l in L])
voice *= 10 ** ((-18 - db(rms(speech))) / 20)

m = load(music); m = np.tile(m, int(np.ceil(N / len(m))) + 1)[:N]
m *= 10 ** ((-18 - db(rms(m[: SR * 20]))) / 20)              # bed at the voice's level, then ducked below
# gain curve: -18 dB while a line is spoken, -10 dB between lines, smoothed 250 ms
g = np.full(N, -11.0)
for l in L: g[int((l["s"] - 0.15) * SR):int((l["e"] + 0.2) * SR)] = -22.0
k = int(0.25 * SR); g = np.convolve(g, np.ones(k) / k, mode="same")
g[-int(0.8 * SR):] += np.linspace(0, -30, int(0.8 * SR))       # fade out the tail
bed = m * 10 ** (g / 20)
# fade the music in over the hook card
bed[: int(0.5 * SR)] *= np.linspace(0, 1, int(0.5 * SR))

# ---- sound effects on beats (times in seconds, matched to shrink.ts)
W = 10 / 30
def at(li, word=None, off=0.0):
    ws = L[li]["words"]
    if word is None: return ws[0]["s"] + off
    for w in ws:
        if w["t"].upper().strip("\"").rstrip(",.?:!\"").replace(".","").replace(",","").startswith(word.upper().replace(".","")): return w["s"] + off
    raise SystemExit(f"no word {word} in line {li}")
# automatic cues: a page turn on every scene change, a sound on each keyword (spaced >= 0.7 s),
# a big impact on numbers, a click on "Follow"
import re as _re
cues = [(0.12, "paper_flip1.mp3", -16), (1.0, "stamp.mp3", -14), (2.4, "page_turn.mp3", -14)]
last = -9.0; kinds = ["pop.mp3", "stamp.mp3", "paper_flip2.mp3", "ping.mp3"]
for li, ln in enumerate(L):
    if li > 0: cues.append((ln["s"] - W, "page_turn.mp3", -14))
    for wi, w in enumerate(ln["words"]):
        t = w["s"]
        if w["t"].upper().startswith("FOLLOW"): cues.append((t, "click.mp3", -8)); continue
        if not w["key"] or t - last < 0.7 or t < 2.6: continue
        if wi > 0 and ln["words"][wi - 1]["key"] and t - ln["words"][wi - 1]["s"] < 0.5: continue
        num = bool(_re.search(r"\d", w["t"]))
        cues.append((t, ("impact-bass-1.mp3" if num and li % 2 == 0 else "impact-bass-2.mp3") if num else kinds[(li + wi) % len(kinds)], -11 if num else -16)); last = t
fx = np.zeros(N, np.float32)
for t, name, level in cues:
    s = load(f"{sfxdir}/{name}"); s = s[: int(2.5 * SR)]
    pk = float(np.max(np.abs(s))) or 1; s = s / pk * 10 ** (level / 20) * 0.5
    i = int(t * SR); e = min(N, i + len(s)); fx[i:e] += s[: e - i]
mix = voice + bed + fx
pk = float(np.max(np.abs(mix)))
if pk > 0.95: mix *= 0.95 / pk
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", out], input=mix.astype(np.float32).tobytes(), check=True)
gaps = [db(rms(voice[int(l["s"] * SR):int(l["e"] * SR)])) - db(rms(bed[int(l["s"] * SR):int(l["e"] * SR)])) for l in L]
print(f"{len(cues)} sound cues; voice over bed while speaking: min {min(gaps):.1f} dB, median {np.median(gaps):.1f} dB")
print("cues:", ", ".join(f"{t:.2f}s {n.split('.')[0]}" for t, n, _ in cues))
