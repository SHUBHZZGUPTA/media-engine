#!/usr/bin/env python3
"""Map script lines to narration times using Whisper word timings.

Usage: python3 linetimes.py tts_job.json words.txt out.json
words.txt lines: "start end word". Output: [{"i", "who", "text", "t0", "t1"}...]
Lines whose words were not heard (e.g. stage tags) get times interpolated
from their neighbours. Works for English and Hindi (Unicode-aware tokens).
"""
import json, re, sys, difflib

def toks(s):
    s = re.sub(r"\[[^\]]*\]", " ", s)              # drop [style tags]
    return [w for w in re.findall(r"[\w']+", s.lower())]

job = json.load(open(sys.argv[1])); lines = job["items"][0]["lines"]
words = [l.split(None, 2) for l in open(sys.argv[2]) if l.strip()]
W = [(float(a), float(b), re.sub(r"[^\w']", "", w.lower())) for a, b, w in words]

script, owner = [], []
for i, (who, text) in enumerate(lines):
    for t in toks(text): script.append(t); owner.append(i)

sm = difflib.SequenceMatcher(None, script, [w[2] for w in W], autojunk=False)
first, last = {}, {}
for a, b, n in sm.get_matching_blocks():
    for k in range(n):
        i = owner[a + k]; t0, t1, _ = W[b + k]
        first.setdefault(i, t0); last[i] = t1

out = []
for i, (who, text) in enumerate(lines):
    out.append({"i": i, "who": who, "text": text, "t0": first.get(i), "t1": last.get(i)})
# interpolate gaps
for i, L in enumerate(out):
    if L["t0"] is None:
        prev = next((out[j]["t1"] for j in range(i - 1, -1, -1) if out[j]["t1"] is not None), 0.0)
        nxt = next((out[j]["t0"] for j in range(i + 1, len(out)) if out[j]["t0"] is not None), prev + 1.0)
        L["t0"], L["t1"], L["guess"] = prev + 0.05, max(nxt - 0.05, prev + 0.3), True
json.dump(out, open(sys.argv[3], "w"), indent=1, ensure_ascii=False)
miss = [L["i"] for L in out if L.get("guess")]
print(len(out), "lines; guessed:", miss)
