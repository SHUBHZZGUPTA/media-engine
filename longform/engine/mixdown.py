#!/usr/bin/env python3
"""Long-form audio mix: narration + ducked music bed + sound on every cut/pop, mastered to -14 LUFS.

Usage: python3 mixdown.py spec.json voice.wav music.json out.wav
music.json: {"sfx_dir": path, "sections": [{"file": mp3, "from": t, "to": t, "gain_db": -18}]}
- music sections crossfade (1.5 s) and sit ~18 dB below the voice, ducked further while speaking
- a short whoosh on every shot cut, a soft pop on every layer that pops in (capped per second)
"""
import json, subprocess, sys
import numpy as np

SR = 48000
def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()
def db(x): return 10 ** (x / 20)
def place(buf, clip, t, gain):
    a = int(t * SR)
    if a >= len(buf) or a < 0: return
    b = min(a + len(clip), len(buf)); buf[a:b] += clip[:b - a] * gain

spec = json.load(open(sys.argv[1])); voice = decode(sys.argv[2]); cfg = json.load(open(sys.argv[3]))
dur = max(spec["shots"][-1]["t1"], len(voice) / SR) + .5; N = int(dur * SR)
v = np.zeros(N, np.float32); v[:len(voice)] = voice[:N]

# --- music bed with crossfades
music = np.zeros(N, np.float32); xf = int(1.5 * SR)
for sec in cfg["sections"]:
    m = decode(sec["file"]); a, b = int(sec["from"] * SR), min(int(sec["to"] * SR), N)
    need = b - a
    if need <= 0: continue
    reps = int(np.ceil(need / len(m))) + 1; m = np.tile(m, reps)[:need + xf]
    env = np.ones(len(m), np.float32); env[:xf] = np.linspace(0, 1, xf); env[-xf:] = np.linspace(1, 0, xf)
    seg = m * env * db(sec.get("gain_db", -18)); end = min(a + len(seg), N); music[a:end] += seg[:end - a]
# duck: envelope of the voice (fast attack, ~0.8 s release)
hop = int(SR * .01); n = N // hop
rms = np.sqrt((v[:n * hop].reshape(n, hop) ** 2).mean(1)); speaking = rms > max(np.percentile(rms, 40), 1e-4)
duck = np.ones(n, np.float32); level = 1.0; rel = 1 - np.exp(-1 / 80)
for k in range(n):
    target = db(-7) if speaking[k] else 1.0
    level = target if target < level else level + (target - level) * rel
    duck[k] = level
music[:n * hop] *= np.repeat(duck, hop)

# --- sound on cuts and pops
sfx = np.zeros(N, np.float32); d = cfg["sfx_dir"]
whoosh = decode(f"{d}/whoosh-short.mp3"); pop = decode(f"{d}/pop.mp3")
for s in spec["shots"][1:]: place(sfx, whoosh, s["t0"] - .08, db(-16))
last = -1
for s in spec["shots"]:
    for L in s.get("layers", []):
        t = L.get("in")
        if t is None or L.get("enter", "pop") != "pop" or t < s["t0"]: continue
        if t - last < .35: continue
        place(sfx, pop, t, db(-20)); last = t

mix = v + music + sfx
tmp = sys.argv[4] + ".raw.wav"
import wave
with wave.open(tmp, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes())
# two-pass loudness normalisation to -14 LUFS / -1.5 dBTP
meas = subprocess.run(["ffmpeg", "-hide_banner", "-i", tmp, "-af", "loudnorm=I=-14:TP=-1.5:LRA=7:print_format=json", "-f", "null", "-"],
                      capture_output=True, text=True).stderr
j = json.loads(meas[meas.rindex("{"):meas.rindex("}") + 1])
af = (f"loudnorm=I=-14:TP=-1.5:LRA=7:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
      f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", af, "-ar", str(SR), "-ac", "2", sys.argv[4]], check=True)
import os; os.remove(tmp)
print("mixed", round(dur, 1), "s ->", sys.argv[4])
