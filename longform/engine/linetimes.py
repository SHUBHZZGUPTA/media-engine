#!/usr/bin/env python3
"""Map script lines to narration times using Whisper word timings.

Usage: python3 linetimes.py tts_job.json words.txt out.json [audio.wav]
words.txt lines: "start end word". Output: [{"i", "who", "text", "t0", "t1", "guess"?}...]

Matching is done on normalised tokens; Devanagari is reduced to a consonant skeleton
(no vowel signs, nukta, anusvara or virama) so spelling variants still match. Lines
with no matched words (common for English words inside Hindi lines) are placed by
character length between their matched neighbours, then snapped to the nearest
pause in the audio when a wav is given.
"""
import json, re, sys, difflib, wave
import numpy as np

DROP = set(range(0x093A, 0x0950)) | {0x0901, 0x0902, 0x0903, 0x0962, 0x0963, 0x0971}
def norm(w):
    w = w.lower()
    return "".join(c for c in w if ord(c) not in DROP)

def toks(s):
    s = re.sub(r"\[[^\]]*\]", " ", s)
    return [t for t in (norm(w) for w in re.findall(r"[\w']+", s)) if t]

def pauses(path, min_len=.28):
    with wave.open(path) as w:
        sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)
    hop = int(sr * .02); n = len(x) // hop
    e = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)); thr = max(np.percentile(e, 20) * 1.5, 80)
    quiet = e < thr; out = []; k = 0
    while k < n:
        if quiet[k]:
            j = k
            while j < n and quiet[j]: j += 1
            if (j - k) * .02 >= min_len: out.append(((k + j) / 2) * .02)
            k = j
        else: k += 1
    return out

def raw_pauses(path, min_len=.22):
    with wave.open(path) as w:
        sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)
    hop = int(sr * .01); n = len(x) // hop
    e = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)); thr = max(np.percentile(e, 25) * 1.6, 60)
    q = e < thr; out = []; k = 0
    while k < n:
        if q[k]:
            j = k
            while j < n and q[j]: j += 1
            if (j - k) * .01 >= min_len: out.append((k * .01, j * .01))
            k = j
        else: k += 1
    return out
PAUSES = raw_pauses(sys.argv[4]) if len(sys.argv) > 4 else None

def fit_gap(lo, hi, lens, alpha=1.0):
    """Split [lo, hi] into len(lens) lines at pauses: durations follow text length, long pauses preferred."""
    n = len(lens); P = [p for p in PAUSES if lo + .2 < p[0] and p[1] < hi - .2]
    if n == 1: return [(lo, hi)]
    if len(P) < n - 1: return None
    exp = np.array(lens, float) / sum(lens) * (hi - lo) * .9
    S = [lo] + [p[1] for p in P]; E = [p[0] for p in P] + [hi]; pl = [p[1] - p[0] for p in P] + [1.5]; M = len(P)
    INF = 1e18; cost = np.full((n, M + 1), INF); back = np.zeros((n, M + 1), int)
    def c(i, s, e, j):
        d = e - s
        return INF if d <= .15 else ((d - exp[i]) / max(exp[i], .6)) ** 2 * .35 - alpha * min(pl[j], 1.6)
    for j in range(M + 1): cost[0, j] = c(0, lo, E[j], j)
    for i in range(1, n):
        for j in range(1, M + 1):
            k = min(range(j), key=lambda k: cost[i - 1, k] + c(i, S[k + 1], E[j], j))
            cost[i, j] = cost[i - 1, k] + c(i, S[k + 1], E[j], j); back[i, j] = k
    j = M; ends = [0] * n
    for i in range(n - 1, -1, -1): ends[i] = j; j = back[i, j]
    return [((lo if i == 0 else S[ends[i - 1] + 1]), E[ends[i]]) for i in range(n)]

job = json.load(open(sys.argv[1])); lines = job["items"][0]["lines"]
W = [(float(a), float(b), norm(re.sub(r"[^\w']", "", w))) for a, b, w in (l.split(None, 2) for l in open(sys.argv[2]) if l.strip())]
script, owner = [], []
for i, (who, text) in enumerate(lines):
    for t in toks(text): script.append(t); owner.append(i)
sm = difflib.SequenceMatcher(None, script, [w[2] for w in W], autojunk=False)
first, last, hits = {}, {}, {}
for a, b, n in sm.get_matching_blocks():
    for k in range(n):
        i = owner[a + k]; t0, t1, _ = W[b + k]
        first.setdefault(i, t0); last[i] = t1; hits[i] = hits.get(i, 0) + 1
out = [{"i": i, "who": who, "text": text, "t0": first.get(i), "t1": last.get(i)} for i, (who, text) in enumerate(lines)]
# a line with a single stray hit is unreliable: treat as unmatched
for L in out:
    if hits.get(L["i"], 0) < 2 and len(toks(L["text"])) > 3: L["t0"] = L["t1"] = None
end = W[-1][1] if W else 0.0
# a matched span far longer than the line's length implies a stray match: drop it
clen = lambda s: max(len(re.sub(r"\[[^\]]*\]", "", s)), 4)
spc = end / sum(clen(L["text"]) for L in out)
for L in out:
    if L["t0"] is not None and (L["t1"] - L["t0"]) > 2.2 * clen(L["text"]) * spc + 1.5: L["t0"] = L["t1"] = None
# an anchor must sit near where its cumulative text length puts it
cum = 0.0
for L in out:
    est = cum * spc; cum += clen(L["text"])
    if L["t0"] is not None and abs(L["t0"] - est) > max(12.0, .08 * end): L["t0"] = L["t1"] = None
# enforce order: a line may not start before the previous matched line ends
prev = 0.0
for L in out:
    if L["t0"] is None: continue
    if L["t0"] < prev - .05: L["t0"] = L["t1"] = None; continue
    prev = L["t1"]
# fill runs of unmatched lines by character length between anchors
i = 0
while i < len(out):
    if out[i]["t0"] is not None: i += 1; continue
    j = i
    while j < len(out) and out[j]["t0"] is None: j += 1
    lo = out[i - 1]["t1"] + .15 if i > 0 else 0.0
    hi = out[j]["t0"] - .15 if j < len(out) else end
    lens = [max(len(re.sub(r"\[[^\]]*\]", "", out[k]["text"])), 4) for k in range(i, j)]; tot = sum(lens); t = lo
    spans = fit_gap(lo, hi, lens) if PAUSES is not None else None
    for n, (k, ln) in enumerate(zip(range(i, j), lens)):
        if spans: out[k].update(t0=spans[n][0], t1=spans[n][1], guess=True)
        else:
            d = (hi - lo) * ln / tot; out[k].update(t0=t, t1=t + d * .92, guess=True); t += d
    i = j
if False:                                  # (old snapping step, replaced by fit_gap)
    P = pauses(sys.argv[4])
    for k, L in enumerate(out):
        if not L.get("guess"): continue
        for key, sgn in (("t0", 1), ("t1", -1)):
            near = min(P, key=lambda p: abs(p - L[key]), default=None)
            if near is not None and abs(near - L[key]) < 1.2: L[key] = near + sgn * .1
        if L["t1"] <= L["t0"] + .3: L["t1"] = L["t0"] + .3
json.dump(out, open(sys.argv[3], "w"), indent=1, ensure_ascii=False)
print(len(out), "lines; placed by length:", [L["i"] for L in out if L.get("guess")])
