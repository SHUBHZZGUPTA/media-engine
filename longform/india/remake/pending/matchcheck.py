#!/usr/bin/env python3
"""India remake voice matching check (rule agreed 9 Nov, VOICE_NOTES "Matching rule").

Usage: python3 matchcheck.py <job>:<take> [<job>:<take> ...]      (takes in script order)
Per take, narrator lines only (cut from the whisper alignment against the job's script lines):
  pitch median vs the 3.8 reference 114.8 Hz (pass: within +-1.0 st), speaking rate (words per narrator second,
  pass: within +-8% of the 8 kept 3.8 takes' median), narrator loudness (RMS dBFS, pass: within +-1.5 dB of that median),
  and per seam the last 30 s of narrator in take N vs the first 30 s of take N+1 (pass: within 1.0 st).
Timbre/tone: runs longform/engine/voicecheck.py with the kept takes as the reference.
"""
import json, os, re, sys, difflib, subprocess, numpy as np, librosa
ROOT = "/home/claude/media-engine"; sys.path.insert(0, f"{ROOT}/longform/india/full")
from num_in import digits
REF_HZ = 114.8; SR = 16000
KEPT = ["in-rm-en-t38:p01", "in-rm-en-e1:p02", "in-rm-en-t38:p05", "in-rm-en-e1:p06", "in-rm-en-e1:p07",
        "in-rm-en-t38:p09", "in-rm-en-t38:p12", "in-rm-en-t38:p18"]
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())
def toks(s):
    s = re.sub(r"\[[^\]]*\]", " ", s).replace("*", "")
    return [norm(w) for w in re.split(r"[\s\-—–]+", digits(s).replace(",", "")) if norm(w)]

def narr(spec):
    job, n = spec.split(":"); J = json.load(open(f"{ROOT}/jobs/tts/{job}.json")); it = next(i for i in J["items"] if i["name"] == n)
    W = [(float(a), float(b), norm(w)) for a, b, w in (r.split(None, 2) for r in open(f"{ROOT}/outputs/align/{job}-{n}/words.txt") if r.strip())]
    S, own = [], []
    for li, (who, txt) in enumerate(it["lines"]):
        for t in toks(txt): S.append(t); own.append((li, who))
    sm = difflib.SequenceMatcher(None, S, [w[2] for w in W], autojunk=False); span = {}; nw = {}
    for b in sm.get_matching_blocks():
        for k in range(b.size):
            li, who = own[b.a + k]; a0, a1 = W[b.b + k][:2]
            s = span.setdefault(li, [who, a0, a1]); s[1] = min(s[1], a0); s[2] = max(s[2], a1); nw[li] = nw.get(li, 0) + 1
    y, _ = librosa.load(f"{ROOT}/outputs/tts/{job}/{n}.wav", sr=SR)
    segs = sorted((a, b, nw[li]) for li, (who, a, b) in span.items() if who == "Narrator" and b > a)
    return y, segs

def f0(y):
    f, v, _ = librosa.pyin(y, fmin=70, fmax=200, sr=SR, frame_length=1024); return float(np.nanmedian(f[v]))
st = lambda hz, ref: 12 * np.log2(hz / ref)
def stats(spec):
    y, segs = narr(spec); cut = lambda S: np.concatenate([y[int(a * SR):int(b * SR)] for a, b, _ in S])
    allv = cut(segs); dur = sum(b - a for a, b, _ in segs); words = sum(w for *_, w in segs)
    head, acc = [], 0
    for s in segs:
        head.append(s); acc += s[1] - s[0]
        if acc >= 30: break
    tail, acc = [], 0
    for s in reversed(segs):
        tail.append(s); acc += s[1] - s[0]
        if acc >= 30: break
    return dict(hz=f0(allv), rate=words / dur, db=20 * np.log10(np.sqrt(np.mean(allv ** 2)) + 1e-9),
                head=f0(cut(head)), tail=f0(cut(sorted(tail))))

takes = sys.argv[1:]
K = [stats(s) for s in KEPT]; rate0 = float(np.median([k["rate"] for k in K])); db0 = float(np.median([k["db"] for k in K]))
print(f"kept 3.8 takes: rate {rate0:.2f} words/s, narrator loudness {db0:.1f} dBFS, reference pitch {REF_HZ} Hz\n")
T = [(s, stats(s)) for s in takes]; bad = []
for s, t in T:
    p, r, d = st(t["hz"], REF_HZ), t["rate"] / rate0 - 1, t["db"] - db0
    ok = abs(p) <= 1.0 and abs(r) <= 0.08 and abs(d) <= 1.5; bad += [] if ok else [s]
    print(f"{'PASS' if ok else 'FAIL'}  {s:22s} pitch {t['hz']:6.1f} Hz {p:+.1f} st | rate {r:+.0%} | loudness {d:+.1f} dB")
print()
for (s1, a), (s2, b) in zip(T, T[1:]):
    g = st(b["head"], a["tail"]); ok = abs(g) <= 1.0; bad += [] if ok else [f"seam {s1}->{s2}"]
    print(f"{'PASS' if ok else 'FAIL'}  seam {s1.split(':')[1]} -> {s2.split(':')[1]}: end {a['tail']:.1f} Hz -> start {b['head']:.1f} Hz ({g:+.1f} st)")
ref = [f"{ROOT}/outputs/tts/{k.split(':')[0]}/{k.split(':')[1]}.wav" for k in KEPT]
tk = [f"{ROOT}/outputs/tts/{s.split(':')[0]}/{s.split(':')[1]}.wav" for s in takes]
print("\ntimbre/tone vs the kept takes (voicecheck.py, whole mix incl. scene voices, first 70 s):")
subprocess.run([sys.executable, f"{ROOT}/longform/engine/voicecheck.py", *ref, "--", *tk])
print("\nFAILED:", bad if bad else "none")
