#!/usr/bin/env python3
"""Long-form audio mix: narration + ducked music bed + sound on every cut/pop, mastered to -14 LUFS.

Usage: python3 mixdown.py spec.json voice.wav music.json out.wav
music.json: {"sfx_dir": path, "sections": [{"file": mp3, "from": t, "to": t, "gain_db": -18}]}
- music sections crossfade (1.5 s) and sit ~18 dB below the voice, ducked further while speaking
- a short whoosh on every shot cut, a soft pop on every layer that pops in (capped per second)
Optional (opt-in, e.g. India): "below_voice_db": 21, "swell_db": 3 -> each music section is levelled (3 s RMS, so a track that
builds stays flat) to sit `below_voice_db` under the narration while it speaks, and rises only `swell_db` in pauses.
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
BELOW = cfg.get("below_voice_db"); DUCK = -cfg.get("swell_db", 3) if BELOW is not None else -7
if BELOW is not None:
    # level the bed: target = (voice RMS while speaking) - BELOW + swell, measured on 3 s windows, gain smoothed
    vr = 20 * np.log10(np.sqrt(np.mean(rms[speaking] ** 2)) + 1e-9); tgt = vr - BELOW - DUCK
    mr = np.sqrt((music[:n * hop].reshape(n, hop) ** 2).mean(1)); w = 300
    mr = np.sqrt(np.convolve(mr ** 2, np.ones(w) / w, "same")) + 1e-9
    g = tgt - 20 * np.log10(mr); g = np.clip(g, np.median(g) - 6, np.median(g) + 6)   # cap boosts/cuts at +-6 dB around the typical gain
    g = np.convolve(g, np.ones(w) / w, "same")
    music[:n * hop] *= np.repeat(db(g).astype(np.float32), hop)
    print(f"music levelled: voice {vr:.1f} dBFS, bed {tgt + DUCK:.1f} under speech, {tgt:.1f} in pauses", flush=True)
duck = np.ones(n, np.float32); level = 1.0; rel = 1 - np.exp(-1 / 80)
for k in range(n):
    target = db(DUCK) if speaking[k] else 1.0
    level = target if target < level else level + (target - level) * rel
    duck[k] = level
music[:n * hop] *= np.repeat(duck, hop)

# --- sound on cuts and pops
sfx = np.zeros(N, np.float32); d = cfg["sfx_dir"]
S = {k: decode(f"{d}/{f}") for k, f in {"whoosh": "whoosh-short.mp3", "whip": "whoosh.mp3", "zoom": "whoosh-cinematic.mp3",
     "pop": "pop.mp3", "impact": "impact-bass-1.mp3", "impact2": "impact-bass-2.mp3", "riser": "riser.mp3", "thud": "thud.mp3",
     "tick": "click-soft.mp3", "mark": "click.mp3", "thump": "thump.mp3"}.items()}
pop = S["pop"]
for s in spec["shots"][1:]:                       # a designed sound for every cut type
    c = s.get("cut", "curve")
    if c == "flash":
        place(sfx, S["riser"], s["t0"] - len(S["riser"]) / SR, db(-20)); place(sfx, S["impact2"], s["t0"], db(-12))
    elif c == "whip": place(sfx, S["whip"], s["t0"] - .12, db(-14))
    elif c == "zoom": place(sfx, S["zoom"], s["t0"] - .2, db(-14))
    else: place(sfx, S["whoosh"], s["t0"] - .08, db(-17 if c == "curve" else -15))
for kind, t0, g in spec.get("fx", []):            # beats: slams, counts, marks, punch-ins
    if kind == "ticks":
        k = 0.0
        while k < g: place(sfx, S["tick"], t0 + k, db(-24)); k += .075
    elif kind == "impact-bass-1": place(sfx, S["impact"], t0, db(g))
    elif kind == "thud": place(sfx, S["thud"], t0, db(g))
    elif kind == "mark": place(sfx, S["mark"], t0, db(g))
    elif kind == "punch": place(sfx, S["thump"], t0, db(g))
last = -1
for s in spec["shots"]:
    for L in s.get("layers", []):
        t = L.get("in")
        if t is None or "circle" in L or L.get("enter", "pop") != "pop" or t < s["t0"]: continue
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
