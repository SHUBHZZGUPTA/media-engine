#!/usr/bin/env python3
"""Chapter cards 1-14 + ending for the India remake (same timeline card style as v1, new titles)."""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "..", "engine"))
import cards
C = os.path.join(HERE, "cards"); os.makedirs(C, exist_ok=True)
CH = ["Indus", "Buddha", "Mauryas", "Ashoka", "Golden Bird", "Sultans", "Tughlaq", "Mughals", "Taj", "Company", "Raj", "Freedom", "1947", "Today"]
SMALL = {"The", "And", "To", "A", "Of", "Who", "In", "Off", "Wasn'T", "Couldn'T"}
def tc(s):
    w = s.title().replace("'T", "'t").replace("'S", "'s").split()
    return " ".join(x if i == 0 or x not in ("The", "And", "To", "A", "Of", "In", "Off") else x.lower() for i, x in enumerate(w))
for r in open(os.path.join(HERE, "script_en.md"), encoding="utf-8"):
    m = re.match(r"# CHAPTER (\d+): (.+)", r.strip())
    if m:
        n = int(m.group(1)); cards.chapter(os.path.join(C, f"chapter{n}.png"), CH, n - 1, f"Chapter {n}: {tc(m.group(2))}", cols=7)
cards.chapter(os.path.join(C, "ending.png"), CH, 13, "The Answer", cols=7)
print(sorted(os.listdir(C)))
