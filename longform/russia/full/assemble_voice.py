#!/usr/bin/env python3
"""Assemble the full narration (chapters 2-11) from the TTS parts.
For each part: line timings (linetimes.py), character pitches (charvoices.py). Then concatenate with a short gap,
speed up (atempo), and write voice_full.wav, lines_full.json (sped-up times) and words_full.txt (raw times; plan divides by speed).
Usage: python3 assemble_voice.py [speed]
"""
import json, os, subprocess, sys, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..", "..", ".."); ENG = os.path.join(HERE, "..", "..", "engine")
SPEED = float(sys.argv[1]) if len(sys.argv) > 1 else 1.12
PARTS = [("ru-full-en-a", "ch2"), ("ru-full-en-a", "ch3_4"), ("ru-full-en-a", "ch5_6"), ("ru-full-en-b", "ch7"), ("ru-full-en-b", "ch8"), ("ru-full-en-b", "ch9"), ("ru-full-en-b", "ch10_11")]
GAP = 0.9
PITCH = {"TRAVELLER": 2, "PRINCE": 1, "KHAN": -4, "SERVANT": 3, "IVAN": -5, "DMITRY": 2, "NOBLE": -2, "FOREMAN": -1, "PETER": -3, "OFFICER": -2, "CATHERINE": 4,
         "NAPOLEON": 0, "AIDE": 3, "SAILOR": 4, "ADMIRAL": -4, "COMRADE": 3, "LENIN": -1, "OFFICIAL": -4, "EDITOR": 3, "GUARD ONE": 1, "GUARD TWO": -2,
         "CAPTAIN": -1, "ARKHIPOV": -4}
W = os.path.join(HERE, "voice_work"); os.makedirs(W, exist_ok=True)
def run(*a): subprocess.run(list(a), check=True)
allL, allW, chunks, off = [], [], [], 0.0
for job, name in PARTS:
    jf = json.load(open(os.path.join(ROOT, "jobs", "tts", job + ".json"))); item = next(i for i in jf["items"] if i["name"] == name)
    one = os.path.join(W, name + "_job.json"); json.dump({"items": [item]}, open(one, "w"))
    wav = os.path.join(ROOT, "outputs", "tts", job, name + ".wav"); words = os.path.join(ROOT, "outputs", "align", f"ru-full-en-{name}", "words.txt")
    lj = os.path.join(W, name + "_lines.json")
    run("python3", os.path.join(ENG, "linetimes.py"), one, words, lj, wav)
    spk = json.load(open(os.path.join(HERE, job + "_speakers.json")))[name]
    cast = {"speakers": spk, "pitch": {k: PITCH.get(k, 0) for k in set(spk.values())}}
    cj = os.path.join(W, name + "_cast.json"); json.dump(cast, open(cj, "w"))
    pv = os.path.join(W, name + "_pitched.wav"); run("python3", os.path.join(ENG, "charvoices.py"), wav, lj, cj, pv)
    with wave.open(pv) as w: sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16)
    dur = len(x) / sr
    for l in json.load(open(lj)): allL.append(dict(l, t0=l["t0"] + off, t1=l["t1"] + off))
    for r in open(words):
        if r.strip(): a, b, wd = r.split(None, 2); allW.append(f"{float(a) + off:.3f} {float(b) + off:.3f} {wd.strip()}")
    chunks.append(x); chunks.append(np.zeros(int(GAP * sr), np.int16)); off += dur + GAP
    print(name, round(dur, 1), "s; lines", len(json.load(open(lj))), flush=True)
raw = os.path.join(W, "voice_raw.wav")
with wave.open(raw, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(np.concatenate(chunks).tobytes())
run("ffmpeg", "-v", "error", "-y", "-i", raw, "-af", f"atempo={SPEED}", os.path.join(HERE, "voice_full.wav"))
for i, l in enumerate(allL): l["i"] = i; l["t0"] = round(l["t0"] / SPEED, 3); l["t1"] = round(l["t1"] / SPEED, 3)
json.dump(allL, open(os.path.join(HERE, "lines_full.json"), "w"), indent=0)
open(os.path.join(HERE, "words_full.txt"), "w").write("\n".join(allW) + "\n")
print("total", round(off / SPEED, 1), "s sped;", len(allL), "lines")
