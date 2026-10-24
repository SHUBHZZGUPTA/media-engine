#!/usr/bin/env python3
"""Line timings by fuzzy phonetic alignment of the script to Whisper words.

Usage: python3 phonalign.py tts_job.json words.txt out.json
For mixed Hindi/English scripts: both the script and Whisper's output (which writes English
words in Devanagari, with varying spellings) are reduced to coarse consonant-class strings,
then aligned with a global DP (Needleman-Wunsch) using edit-distance similarity per token.
Each line takes the times of its aligned words; lines with no aligned word are interpolated.
"""
import json, re, sys
import numpy as np

# coarse consonant classes, shared by Latin and Devanagari
LAT = {**{c: "K" for c in "kcqx"}, **{c: "G" for c in "gjz"}, **{c: "T" for c in "td"}, **{c: "P" for c in "pbf"},
       **{c: "S" for c in "s"}, **{c: "M" for c in "mn"}, **{c: "L" for c in "lr"}, **{c: "V" for c in "vwy"}, "h": "H"}
DEV = {}
for chars, k in [("कखक़ख़", "K"), ("गघजझज़ग़", "G"), ("चछ", "K"), ("टठडढतथदधड़ढ़", "T"), ("पफबभफ़", "P"),
                 ("सशष", "S"), ("मनणङञ", "M"), ("लर", "L"), ("वय", "V"), ("ह", "H")]:
    for c in chars: DEV[c] = k
NUKTA = "़"

def skel(word):
    w = word.lower().replace(NUKTA, "")
    out = []
    for i, c in enumerate(w):
        if c in DEV: k = DEV[c]
        elif "a" <= c <= "z": k = LAT.get(c, "")
        elif c in "aeiou": k = ""
        else: k = ""
        if c == "h" and i and w[i - 1] in "cstpkgbdj": continue      # digraphs: sh, th, ph, kh...
        if k and (not out or out[-1] != k): out.append(k)
    return "".join(out)

def lev(a, b):
    if not a or not b: return max(len(a), len(b))
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1): cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]

def sim(a, b):
    if not a or not b: return 0.0
    return 1 - lev(a, b) / max(len(a), len(b))

NUM = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}
def toks(s):
    s = re.sub(r"\[[^\]]*\]", " ", s).replace("*", "")
    return [w for w in re.findall(r"[^\s.,!?।\"…:;()\-—]+", s)]

job = json.load(open(sys.argv[1])); lines = job["items"][0]["lines"]
W = [(float(a), float(b), w) for a, b, w in (l.split(None, 2) for l in open(sys.argv[2]) if l.strip())]
S, owner = [], []
for i, (_, text) in enumerate(lines):
    for t in toks(text): S.append(skel(t)); owner.append(i)
H = [skel(re.sub(r"[\s.,!?।\"…:;()\-—]", "", w)) for _, _, w in W]
n, m = len(S), len(H)
GAP = -0.35
score = np.zeros((n + 1, m + 1), np.float32); move = np.zeros((n + 1, m + 1), np.int8)
score[1:, 0] = GAP * np.arange(1, n + 1); score[0, 1:] = GAP * np.arange(1, m + 1); move[1:, 0] = 1; move[0, 1:] = 2
for i in range(1, n + 1):
    si = S[i - 1]
    for j in range(1, m + 1):
        s = sim(si, H[j - 1]); d = score[i - 1, j - 1] + (s * 2 - 0.8)
        u = score[i - 1, j] + GAP; l = score[i, j - 1] + GAP
        if d >= u and d >= l: score[i, j], move[i, j] = d, 0
        elif u >= l: score[i, j], move[i, j] = u, 1
        else: score[i, j], move[i, j] = l, 2
i, j = n, m; pairs = []
while i > 0 and j > 0:
    mv = move[i, j]
    if mv == 0:
        if sim(S[i - 1], H[j - 1]) >= .5: pairs.append((i - 1, j - 1))
        i, j = i - 1, j - 1
    elif mv == 1: i -= 1
    else: j -= 1
first, last = {}, {}
for a, b in sorted(pairs):
    k = owner[a]; first.setdefault(k, W[b][0]); last[k] = W[b][1]
out = [{"i": i, "who": w, "text": t, "t0": first.get(i), "t1": last.get(i)} for i, (w, t) in enumerate(lines)]
for k, L in enumerate(out):
    if L["t0"] is None:
        prev = next((out[j]["t1"] for j in range(k - 1, -1, -1) if out[j]["t1"] is not None), 0.0)
        nxt = next((out[j]["t0"] for j in range(k + 1, len(out)) if out[j]["t0"] is not None), prev + 1.0)
        L.update(t0=prev + .05, t1=max(nxt - .05, prev + .35), guess=True)
# implausible spans (far shorter/longer than their text) are re-spread by length between solid neighbours
clen = lambda s: max(len(re.sub(r"\[[^\]]*\]", "", s).replace("*", "").strip()), 3)
rate = (out[-1]["t1"] - out[0]["t0"]) / sum(clen(L["text"]) for L in out)
bad = [not (0.35 < (L["t1"] - L["t0"]) / (clen(L["text"]) * rate) < 2.6) or L.get("guess") for L in out]
for q in range(1, len(bad) - 1):            # a lone good line between bad ones is not trustworthy either
    if bad[q - 1] and bad[q + 1]: bad[q] = True
k = 0
while k < len(out):
    if not bad[k]: k += 1; continue
    j = k
    while j < len(out) and bad[j]: j += 1
    lo = out[k - 1]["t1"] + .1 if k > 0 else out[k]["t0"]
    hi = out[j]["t0"] - .1 if j < len(out) else out[j - 1]["t1"]
    lens = [clen(out[q]["text"]) for q in range(k, j)]; tot = sum(lens); t0 = lo
    for q, ln in zip(range(k, j), lens):
        d = (hi - lo) * ln / tot; out[q].update(t0=round(t0, 3), t1=round(t0 + d * .9, 3), guess=True); t0 += d
    k = j
json.dump(out, open(sys.argv[3], "w"), indent=1, ensure_ascii=False)
print(len(out), "lines;", len(pairs), "aligned words of", n, "; re-spread lines:", [L["i"] for L in out if L.get("guess")])
