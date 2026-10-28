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
# re-voiced tails: {global line idx: (fix job, item, local idx in item)}
FIX = {}
for fj in sorted(f for f in os.listdir(HERE) if f.startswith("ru-full-en-fix") and f.endswith("_map.json")):
    jid = fj[:-9]
    if not os.path.exists(os.path.join(ROOT, "outputs", "align", f"{jid}-fix_a", "words.txt")) and not os.path.exists(os.path.join(ROOT, "outputs", "align", jid + "-" + next(iter(json.load(open(os.path.join(HERE, fj))))), "words.txt")):
        print("fix not aligned yet:", jid); continue
    for item, m in json.load(open(os.path.join(HERE, fj))).items():
        if not os.path.exists(os.path.join(ROOT, "outputs", "align", f"{jid}-{item}", "words.txt")): print("skip (no take yet):", jid, item); continue
        for k, g in enumerate(m["global"]): FIX[g] = (jid, item, k)
FIXDATA = {}
def fixdata(jid, item):
    if (jid, item) in FIXDATA: return FIXDATA[(jid, item)]
    jf = json.load(open(os.path.join(ROOT, "jobs", "tts", jid + ".json"))); it = dict(next(i for i in jf["items"] if i["name"] == item))
    drop = json.load(open(os.path.join(HERE, jid + "_map.json")))[item].get("drop", [])
    it["lines"] = [l for q, l in enumerate(it["lines"]) if q not in drop]      # lines the take skipped
    one = os.path.join(W, f"{jid}_{item}_job.json"); json.dump({"items": [it]}, open(one, "w"))
    wav = os.path.join(ROOT, "outputs", "tts", jid, item + ".wav"); words = os.path.join(ROOT, "outputs", "align", f"{jid}-{item}", "words.txt")
    lj = os.path.join(W, f"{jid}_{item}_lines.json"); run("python3", os.path.join(ENG, "linetimes.py"), one, words, lj, wav)
    spk = json.load(open(os.path.join(HERE, jid + "_map.json")))[item]["speakers"]
    cj = os.path.join(W, f"{jid}_{item}_cast.json"); json.dump({"speakers": spk, "pitch": {k: PITCH.get(k, 0) for k in set(spk.values())}}, open(cj, "w"))
    pv = os.path.join(W, f"{jid}_{item}_pitched.wav"); run("python3", os.path.join(ENG, "charvoices.py"), wav, lj, cj, pv)
    with wave.open(pv) as w: x = np.frombuffer(w.readframes(w.getnframes()), np.int16)
    Wd = [(float(a), float(b), wd.strip()) for a, b, wd in (r.split(None, 2) for r in open(words) if r.strip())]
    FIXDATA[(jid, item)] = (x, json.load(open(lj)), Wd); return FIXDATA[(jid, item)]
G0 = 0
LEAD = 2.0 * SPEED   # silence before chapter 2 (its chapter card)
allL, allW, chunks, off = [], [], [], LEAD
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
    PL = json.load(open(lj)); PW = [(float(a), float(b), wd.strip()) for a, b, wd in (r.split(None, 2) for r in open(words) if r.strip())]
    # splice re-voiced runs (contiguous global lines from the same fix item)
    runs, k = [], 0
    while k < len(PL):
        g = G0 + k
        if g in FIX:
            j = k
            while j + 1 < len(PL) and G0 + j + 1 in FIX and FIX[G0 + j + 1][:2] == FIX[g][:2]: j += 1
            runs.append((k, j)); k = j + 1
        else: k += 1
    for k0, k1 in reversed(runs):
        jid, item, f0 = FIX[G0 + k0]; f1 = FIX[G0 + k1][2]; fx, fl, fw = fixdata(jid, item)
        a0 = max(0.0, PL[k0]["t0"] - .12); a1 = PL[k1]["t1"] + .25 if k1 + 1 < len(PL) else len(x) / sr
        if k1 + 1 < len(PL): a1 = min(a1, PL[k1 + 1]["t0"] - .05)
        b0 = max(0.0, fl[f0]["t0"] - .12); b1 = fl[f1]["t1"] + .25 if f1 + 1 < len(fl) else len(fx) / sr
        if f1 + 1 < len(fl): b1 = min(b1, fl[f1 + 1]["t0"] - .05)
        piece = fx[int(b0 * sr):int(b1 * sr)]; delta = (b1 - b0) - (a1 - a0)
        x = np.concatenate([x[:int(a0 * sr)], piece, x[int(a1 * sr):]])
        for q in range(k0, k1 + 1): PL[q] = dict(PL[q], t0=fl[f0 + q - k0]["t0"] - b0 + a0, t1=fl[f0 + q - k0]["t1"] - b0 + a0)
        for q in range(k1 + 1, len(PL)): PL[q] = dict(PL[q], t0=PL[q]["t0"] + delta, t1=PL[q]["t1"] + delta)
        PW = [w_ for w_ in PW if w_[0] < a0] + [(a_ - b0 + a0, b_ - b0 + a0, w_) for a_, b_, w_ in fw if b0 <= a_ < b1] + \
             [(a_ + delta, b_ + delta, w_) for a_, b_, w_ in PW if a_ >= a1]
        print(f"  spliced {item} lines {G0 + k0}-{G0 + k1}: {a1 - a0:.1f}s -> {b1 - b0:.1f}s", flush=True)
    # the TTS sometimes reads a [style tag] aloud ("Whispering, he hasn't..."): cut those words out
    import re as _re, difflib as _dl
    nz = lambda w: _re.sub(r"[^a-z]", "", w.lower())
    for q in range(len(PL) - 1, -1, -1):
        m = _re.match(r"\s*\[([^\]]*)\]", PL[q]["text"])
        if not m: continue
        tagw = {nz(w) for w in m.group(1).split()} - {""}
        lo = PL[q - 1]["t1"] - .05 if q else max(0.0, PL[q]["t0"] - 2.5)
        ws = [w_ for w_ in PW if max(lo, PL[q]["t0"] - 2.5) <= w_[0] < PL[q]["t1"]]
        n = 0
        while n < len(ws) and any(_dl.SequenceMatcher(None, nz(ws[n][2]), t_).ratio() > .75 for t_ in tagw): n += 1
        if n == 0 or n >= len(ws) or not any(len(nz(w_[2])) >= 4 for w_ in ws[:n]): continue
        c0, c1 = max(0.0, ws[0][0] - .04), ws[n][0] - .06
        if c1 <= c0: continue
        x = np.concatenate([x[:int(c0 * sr)], x[int(c1 * sr):]]); d = c1 - c0
        PL[q] = dict(PL[q], t0=min(PL[q]["t0"], c0 + .04) if PL[q]["t0"] > c1 else PL[q]["t0"], t1=PL[q]["t1"] - d)
        if PL[q]["t0"] > c0: PL[q]["t0"] = max(c0, PL[q]["t0"] - d)
        for r_ in range(q + 1, len(PL)): PL[r_] = dict(PL[r_], t0=PL[r_]["t0"] - d, t1=PL[r_]["t1"] - d)
        PW = [w_ for w_ in PW if w_[0] < c0] + [(a_ - d, b_ - d, w_) for a_, b_, w_ in PW if a_ >= c1]
        print(f"  cut spoken tag in line {G0 + q}: {' '.join(w_[2] for w_ in ws[:n])!r} ({d:.2f}s)", flush=True)
    dur = len(x) / sr; G0 += len(PL)
    for l in PL: allL.append(dict(l, t0=l["t0"] + off, t1=l["t1"] + off))
    for a_, b_, wd in PW: allW.append(f"{a_ + off:.3f} {b_ + off:.3f} {wd}")
    chunks.append(x); chunks.append(np.zeros(int(GAP * sr), np.int16)); off += dur + GAP
    print(name, round(dur, 1), "s; lines", len(PL), flush=True)
raw = os.path.join(W, "voice_raw.wav")
with wave.open(raw, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(np.concatenate([np.zeros(int(LEAD * sr), np.int16)] + chunks).tobytes())
run("ffmpeg", "-v", "error", "-y", "-i", raw, "-af", f"atempo={SPEED}", os.path.join(HERE, "voice_full.wav"))
for i, l in enumerate(allL): l["i"] = i; l["t0"] = round(l["t0"] / SPEED, 3); l["t1"] = round(l["t1"] / SPEED, 3)
json.dump(allL, open(os.path.join(HERE, "lines_full.json"), "w"), indent=0)
open(os.path.join(HERE, "words_full.txt"), "w").write("\n".join(allW) + "\n")
print("total", round(off / SPEED, 1), "s sped;", len(allL), "lines")
