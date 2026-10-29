#!/usr/bin/env python3
"""Board cards for the India pilot (cycle loop, wealth bars, chapter map)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "..", "engine"))
import cards
C = os.path.join(HERE, "cards"); os.makedirs(C, exist_ok=True)
STEPS = ["STITCH", "SHINE", "SHATTER", "ABSORB"]
for n in range(1, 5): cards.cycle(os.path.join(C, f"cycle{n}.png"), STEPS, n)
cards.cycle(os.path.join(C, "cycle_shine.png"), STEPS, 2, highlight=1)
cards.cycle(os.path.join(C, "cycle_shatter.png"), STEPS, 3, highlight=2)
cards.bars(os.path.join(C, "bars.png"), "India's share of the world economy (est.)",
           [("1700", 24.4, "~24%", "#f0ba32"), ("1950", 4.2, "~4%", "#d6423a")])
CH = ["Indus", "Vedic", "Buddha", "Mauryas", "Golden Age", "Sultans", "Mughals I", "Mughals II", "Company", "1857 & Raj", "Freedom", "1947", "Today"]
cards.chapter(os.path.join(C, "chapter1.png"), CH, 0, "Chapter 1: The City Nobody Can Read")
print(sorted(os.listdir(C)))
