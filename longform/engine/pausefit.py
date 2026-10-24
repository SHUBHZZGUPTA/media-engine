#!/usr/bin/env python3
"""Line timings from pauses alone (no transcription), for languages Whisper aligns poorly.

Usage: python3 pausefit.py tts_job.json audio.wav out.json [--check lines_ref.json]
Finds every pause in the take, then uses dynamic programming to choose one pause per line
boundary so each line's duration best matches its expected duration (character length x
the take's average speed). Character lines (short quips) get their own speed estimate.
"""
import json, re, sys, wave
import numpy as np

def energy(path):
    with wave.open(path) as w:
        sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)
    hop = int(sr * .01); n = len(x) // hop
    return np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)), n * .01

def find_pauses(e, min_len=.22):
    thr = max(np.percentile(e, 25) * 1.6, 60); q = e < thr; out = []; k = 0; n = len(e)
    while k < n:
        if q[k]:
            j = k
            while j < n and q[j]: j += 1
            if (j - k) * .01 >= min_len: out.append((k * .01, j * .01))
            k = j
        else: k += 1
    return out

def clen(s): return max(len(re.sub(r"\[[^\]]*\]", "", s).replace("*", "").strip()), 3)

job = json.load(open(sys.argv[1])); lines = job["items"][0]["lines"]
e, dur = energy(sys.argv[2]); P = find_pauses(e)
start = P[0][1] if P and P[0][0] < .05 else 0.0
end = P[-1][0] if P and P[-1][1] > dur - .05 else dur
P = [p for p in P if start < p[0] and p[1] < end]
N = len(lines); lens = np.array([clen(t) for _, t in lines], float)
# speech time available = total minus pause time between lines (approx: total gaps of chosen pauses)
rate = (end - start) * .88 / lens.sum()
exp = lens * rate
# DP over pauses: state (line index, pause index) = best cost with line i ending at pause j
M = len(P); INF = 1e18
cost = np.full((N, M + 1), INF); back = np.zeros((N, M + 1), int)
bounds_s = [start] + [p[1] for p in P]           # where a line can start (end of pause j-1)
bounds_e = [p[0] for p in P] + [end]             # where a line can end (start of pause j)
ALPHA = float(sys.argv[sys.argv.index("--alpha") + 1]) if "--alpha" in sys.argv else 1.0
plen = [p[1] - p[0] for p in P] + [1.5]          # length of the pause that ends each candidate line
def c(i, s, t, j=None):
    d = t - s; x = exp[i]
    if d <= .15: return INF
    return ((d - x) / max(x, .6)) ** 2 * .35 - ALPHA * min(plen[j], 1.6) if j is not None else ((d - x) / max(x, .6)) ** 2
for j in range(M + 1):                           # line 0 starts at `start`
    cost[0, j] = c(0, start, bounds_e[j], j)
for i in range(1, N):
    best = INF; arg = -1
    for j in range(M + 1):
        # previous line ended at pause k < j; this line runs from end of pause k to start of pause j
        if j == 0: continue
        if cost[i - 1, j - 1] < best: best, arg = cost[i - 1, j - 1], j - 1
        # running min over k <= j-1 is not enough because cost depends on k; do exact search in a window
        lo = max(0, j - 40)
        bk = min(range(lo, j), key=lambda k: cost[i - 1, k] + c(i, bounds_s[k + 1], bounds_e[j], j))
        cost[i, j] = cost[i - 1, bk] + c(i, bounds_s[bk + 1], bounds_e[j], j); back[i, j] = bk
j = M; ends = [0] * N
for i in range(N - 1, -1, -1):
    ends[i] = j; j = back[i, j]
out = []
for i in range(N):
    s = start if i == 0 else bounds_s[ends[i - 1] + 1]
    out.append({"i": i, "who": lines[i][0], "text": lines[i][1], "t0": round(s, 3), "t1": round(bounds_e[ends[i]], 3)})
json.dump(out, open(sys.argv[3], "w"), indent=1, ensure_ascii=False)
print(N, "lines over", round(end - start, 1), "s;", M, "pauses found")
if "--check" in sys.argv:
    ref = json.load(open(sys.argv[sys.argv.index("--check") + 1]))
    err = [abs(a["t0"] - b["t0"]) for a, b in zip(out, ref)]
    print("start error vs reference: median", round(float(np.median(err)), 2), "s; max", round(max(err), 2), "s; >1 s:", sum(x > 1 for x in err))
