#!/usr/bin/env python3
"""Line-by-line check of a TTS take against its script lines (catches skipped, repeated or garbled lines, spoken stage tags,
and the late-take breakdown seen on Russia, which length/pace checks miss).

Usage: python3 takecheck.py <job_id> <item> [<item> ...]
For each script line: % of its words found in order in the Whisper transcript, and where in the take it falls.
FLAG = under 80% matched, extra words spoken (ad-lib / repeat / tag read aloud), or matched words out of order.
"""
import json, os, re, sys, difflib
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_in import digits
def norm(w): return re.sub(r"[^a-z0-9]", "", w.lower())
def toks(s):
    s = re.sub(r"\[[^\]]*\]", " ", s).replace("*", "")
    return [norm(w) for w in re.split(r"[\s\-—–]+", digits(s).replace(",", "")) if norm(w)]

job_id, items = sys.argv[1], sys.argv[2:]
J = json.load(open(os.path.join(ROOT, "jobs", "tts", job_id + ".json")))
bad_all = 0
for name in items:
    it = next(i for i in J["items"] if i["name"] == name)
    W = [(float(a), w.strip()) for a, b, w in (r.split(None, 2) for r in open(os.path.join(ROOT, "outputs", "align", f"{job_id}-{name}", "words.txt")) if r.strip())]
    hyp = []
    for t, w in W:
        for p in re.split(r"[\s\-—–]+", digits(w).replace(",", "")):
            if norm(p): hyp.append((t, norm(p)))
    ref, owner = [], []
    for k, (who, text) in enumerate(it["lines"]):
        for w in toks(text): ref.append(w); owner.append(k)
    sm = difflib.SequenceMatcher(None, ref, [h[1] for h in hyp], autojunk=False)
    hit = [None] * len(ref); extra = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for q in range(i2 - i1): hit[i1 + q] = j1 + q
        elif tag in ("insert", "replace") and j2 - j1 > (i2 - i1) + 2:     # notably more spoken than written here
            k = owner[min(i1, len(owner) - 1)]; extra[k] = extra.get(k, 0) + (j2 - j1) - (i2 - i1)
    total = len(ref); bad = []
    print(f"## {job_id} {name}: {len(it['lines'])} lines, {total} script words, {len(hyp)} heard")
    for k, (who, text) in enumerate(it["lines"]):
        idx = [i for i in range(total) if owner[i] == k]
        got = [hit[i] for i in idx if hit[i] is not None]
        pct = len(got) / max(len(idx), 1); pos = (idx[0] / total) if idx else 0
        order_ok = got == sorted(got)
        flag = pct < .8 or extra.get(k, 0) >= 3 or not order_ok
        tagw = set(toks(re.match(r"\s*\[([^\]]*)\]", text).group(1))) if re.match(r"\s*\[([^\]]*)\]", text) else set()
        if flag and pct >= .8 and order_ok and tagw and extra.get(k, 0) <= len(tagw) + 1:
            print(f"  tag   line {k:2d} [{who}] stage tag read aloud (assemble_voice.py cuts it): {sorted(tagw)}"); continue
        if flag:
            bad.append(k)
            print(f"  FLAG line {k:2d} at {pos:4.0%} of take [{who}] matched {pct:4.0%}" + (f", +{extra[k]} extra words" if extra.get(k) else "") +
                  ("" if order_ok else ", out of order") + f" | {re.sub(r'[*]', '', text)[:80]}")
    tail = [k for k in bad if k >= .75 * len(it["lines"])]
    print(f"  => {len(it['lines']) - len(bad)}/{len(it['lines'])} lines clean" + (f"; {len(tail)} flagged in the last 25%" if tail else "") + "\n")
    bad_all += len(bad)
sys.exit(1 if bad_all else 0)
