#!/usr/bin/env python3
"""Chapter cards 2-13 for the India full video (same map card as the pilot's chapter 1)."""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "..", "engine"))
import cards
C = os.path.join(HERE, "cards"); os.makedirs(C, exist_ok=True)
CH = ["Indus", "Vedic", "Buddha", "Mauryas", "Golden Age", "Sultans", "Mughals I", "Mughals II", "Company", "1857 & Raj", "Freedom", "1947", "Today"]
for r in open(os.path.join(HERE, "script_ch2-13.md"), encoding="utf-8"):
    m = re.match(r"# CHAPTER (\d+): (.+)", r.strip())
    if m:
        n = int(m.group(1)); title = m.group(2).title().replace("And The", "and the").replace("The ", "The ")
        cards.chapter(os.path.join(C, f"chapter{n}.png"), CH, n - 1, f"Chapter {n}: {title}", cols=7)
print(sorted(os.listdir(C)))
