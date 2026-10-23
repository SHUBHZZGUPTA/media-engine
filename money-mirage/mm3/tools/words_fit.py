# Fit Whisper word timings onto the script's own tokens (any language), so align.py gets exactly one entry per script word.
# Whisper splits, merges and misspells words (names, Hindi spellings, numbers); a character-level match between the
# script and the transcript carries the times across. Tokens with no matched characters are interpolated.
# Usage: python3 words_fit.py <spec.json> <whisper_words.txt> <out_words.txt>   (whisper lines: "start end word", tab or space)
import sys, json, re, unicodedata, difflib
spec_p, ww_p, out_p = sys.argv[1:4]
S = json.load(open(spec_p))
def norm(w): return ''.join(ch for ch in unicodedata.normalize('NFC', w.lower()) if unicodedata.category(ch)[0] in 'LMN')
toks = [w for l in S['lines'] for w in l['text'].split()]
W = []
for ln in open(ww_p, encoding='utf-8'):
    p = ln.strip().split(None, 2)
    if len(p) == 3: W.append((float(p[0]), float(p[1]), norm(p[2])))
# whisper character stream with a time per character
wc, wt = [], []
for a, b, w in W:
    n = max(1, len(w))
    for i, ch in enumerate(w): wc.append(ch); wt.append(a + (b - a) * i / n)
wend = []  # end time of the word each char belongs to
for a, b, w in W: wend += [b] * len(w)
sc, own = [], []
for k, w in enumerate(toks):
    for ch in norm(w): sc.append(ch); own.append(k)
m = difflib.SequenceMatcher(None, ''.join(sc), ''.join(wc), autojunk=False)
s2w = {}
for a, b, n in m.get_matching_blocks():
    for i in range(n): s2w[a + i] = b + i
st = [None] * len(toks); en = [None] * len(toks); pos = 0
for k, w in enumerate(toks):
    idx = [i for i in range(pos, pos + len(norm(w)))]; pos += len(idx)
    hit = [i for i in idx if i in s2w]
    if len(hit) >= max(1, len(idx) // 3):
        f, l = hit[0], hit[-1]
        st[k] = max(0.0, wt[s2w[f]] - .065 * (f - idx[0])); en[k] = wend[s2w[l]] if l == idx[-1] else wt[s2w[l]] + .065 * (idx[-1] - l + 1)
# interpolate gaps
known = [k for k in range(len(toks)) if st[k] is not None]
for k in range(len(toks)):
    if st[k] is None:
        p = max([j for j in known if j < k], default=None); q = min([j for j in known if j > k], default=None)
        a = en[p] if p is not None else 0.0; b = st[q] if q is not None else a + .4 * (k - (p if p is not None else -1))
        lo = p if p is not None else -1; hi = q if q is not None else len(toks)
        f0 = (k - lo - 1) / (hi - lo - 1); f1 = (k - lo) / (hi - lo - 1)
        st[k] = a + (b - a) * f0; en[k] = a + (b - a) * f1
for k in range(1, len(toks)): st[k] = max(st[k], st[k - 1] + .05); en[k] = max(en[k], st[k] + .05)
with open(out_p, 'w', encoding='utf-8') as o:
    for k, w in enumerate(toks): o.write(f'{st[k]:.2f} {en[k]:.2f} {w}\n')
miss = [toks[k] for k in range(len(toks)) if k not in known]
print(f'{len(toks)} tokens, {len(W)} whisper words, {len(miss)} interpolated' + (': ' + ' '.join(miss[:30]) if miss else ''))
