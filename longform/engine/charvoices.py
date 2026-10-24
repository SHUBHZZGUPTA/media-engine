#!/usr/bin/env python3
"""Give each skit character its own pitch inside a single narration take.

Usage: python3 charvoices.py in.wav lines.json cast.json out.wav
cast.json: {"speakers": {"<line index>": "<character>"}, "pitch": {"<character>": semitones}}
Each character line (from linetimes.py) is cut out with small margins, pitch-shifted
with ffmpeg's rubberband (duration kept), and spliced back with 10 ms crossfades.
"""
import json, subprocess, sys, wave
import numpy as np

def read(p):
    with wave.open(p) as w: sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)
    return x, sr

def shift(seg, sr, st):
    cmd = ["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", "-",
           "-af", f"rubberband=pitch={2 ** (st / 12):.5f}:formant=preserved", "-f", "f32le", "-"]
    out = np.frombuffer(subprocess.run(cmd, input=seg.astype(np.float32).tobytes(), capture_output=True, check=True).stdout, np.float32)
    return np.pad(out, (0, max(0, len(seg) - len(out))))[:len(seg)]

x, sr = read(sys.argv[1]); lines = json.load(open(sys.argv[2])); cast = json.load(open(sys.argv[3]))
y = x.copy(); fade = int(sr * .01)
for idx, who in cast["speakers"].items():
    L = lines[int(idx)]; st = cast["pitch"].get(who, 0)
    if not st: continue
    a = max(int((L["t0"] - .08) * sr), 0); b = min(int((L["t1"] + .12) * sr), len(x))
    s = shift(x[a:b], sr, st)
    ramp = np.linspace(0, 1, fade)
    s[:fade] = s[:fade] * ramp + y[a:a + fade] * (1 - ramp); s[-fade:] = s[-fade:] * ramp[::-1] + y[b - fade:b] * (1 - ramp[::-1])
    y[a:b] = s
with wave.open(sys.argv[4], "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(np.clip(y, -32768, 32767).astype(np.int16).tobytes())
print("re-pitched", len(cast["speakers"]), "lines")
