#!/usr/bin/env python3
"""Chapter cards for the Mariana Trench long-form."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "engine"))
import cards
C = os.path.join(HERE, "cards"); os.makedirs(C, exist_ok=True)
CH = ["Where", "Darkness", "Pressure", "1960", "Life", "Drinking", "Plastic"]
TITLES = ["The Hole at the Bottom of the World", "Where the Light Dies", "The Weight of the Ocean", "The First Two Men",
          "Something Is Alive Down Here", "The Trench That Drinks the Ocean", "We Got There First"]
for n, t in enumerate(TITLES, 1):
    cards.chapter(os.path.join(C, f"chapter{n}.png"), CH, n - 1, f"Chapter {n}: {t}", cols=7)
print(sorted(os.listdir(C)))
