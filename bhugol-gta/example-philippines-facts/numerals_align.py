#!/usr/bin/env python3
"""Expand ASR numerals ('7,641', '20th', '12' ',000') into words so make.py can match a script that spells numbers out.
usage: python3 numerals_align.py outputs/align/<id>/words.txt outputs/align/<id>x/words.txt   (then build with ALIGN=<id>x)
Years 1500-2039 stay as digits (scripts write years in digits)."""
import re, sys, os
from num2words import num2words
src, dst = sys.argv[1], sys.argv[2]; out = []
L = [l.rstrip('\n').split(None, 2) for l in open(src)]; i = 0
while i < len(L):
    p = L[i]
    if len(p) < 3: i += 1; continue
    a, b, w = float(p[0]), float(p[1]), p[2]
    core = re.sub(r'[^\w.,]', '', w).strip('.,')
    if i + 1 < len(L) and len(L[i + 1]) >= 3 and re.fullmatch(r',\d{3}[.,!?]*', L[i + 1][2].strip()):
        core += L[i + 1][2].strip().rstrip('.,!?'); b = float(L[i + 1][1]); i += 1
    m = re.fullmatch(r'(\d[\d,]*)(st|nd|rd|th)?', core)
    if m and not re.fullmatch(r'1[5-9]\d\d|20[0-3]\d', core):
        n = int(m.group(1).replace(',', '')); ws = (num2words(n, to='ordinal') if m.group(2) else num2words(n)).replace(',', '').split(); d = (b - a) / len(ws)
        out += [f'{a + k * d:.3f} {a + (k + 1) * d:.3f} {x}' for k, x in enumerate(ws)]
    else: out.append(f'{a:.3f} {b:.3f} {w}')
    i += 1
os.makedirs(os.path.dirname(dst), exist_ok=True); open(dst, 'w').write('\n'.join(out) + '\n')
