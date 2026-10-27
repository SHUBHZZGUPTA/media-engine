#!/usr/bin/env python3
"""Globe overlay textures for the Russia full video (built once into ../map3d_art). Import and use O[...] names."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "..", "engine", "map3d"))
import overlays as OVL
A = os.path.join(HERE, "..", "map3d_art")
CRIMEA = [34.1, 45.0]
RU = {"admin0": "Russia", "drop": [CRIMEA]}                      # internationally recognised borders
UA = {"admin0": "Ukraine", "add": [[{"admin0": "Russia"}, CRIMEA]]}
CR = {"poly": [[32.5, 45.4], [33.6, 46.2], [34.6, 46.1], [35.5, 45.4], [36.6, 45.4], [35.3, 44.5], [33.9, 44.4], [33.4, 44.6], [32.5, 45.3]]}
GDR = {"poly": [[10.9, 54.1], [11.6, 54.2], [13.0, 54.6], [14.2, 53.9], [14.4, 53.3], [14.6, 52.6], [14.8, 51.6], [15.0, 51.0], [14.3, 51.0], [12.2, 50.3], [11.9, 50.4], [10.1, 50.6], [10.4, 51.4], [10.6, 52.1], [11.0, 53.0], [10.6, 53.5]]}
HORDE = {"poly": [[27.5, 47.0], [30.5, 48.5], [34.0, 49.5], [38.5, 51.5], [42.0, 52.8], [46.0, 55.2], [50.0, 56.2], [53.0, 55.6], [56.0, 56.5], [60.0, 56.2], [66.0, 55.0],
                  [72.0, 54.2], [78.0, 52.0], [80.0, 48.0], [77.0, 44.5], [70.0, 42.5], [64.0, 40.5], [60.0, 41.0], [55.0, 41.8], [51.0, 42.5], [47.5, 42.6],
                  [44.5, 43.2], [40.0, 43.8], [37.0, 44.8], [34.0, 44.5], [32.5, 45.6], [30.0, 46.0]]}
USSR = [RU, UA, {"admin0": "Belarus"}, {"admin0": "Moldova"}, {"admin0": "Lithuania"}, {"admin0": "Latvia"}, {"admin0": "Estonia"}, {"admin0": "Georgia"},
        {"admin0": "Armenia"}, {"admin0": "Azerbaijan"}, {"admin0": "Kazakhstan"}, {"admin0": "Uzbekistan"}, {"admin0": "Turkmenistan"}, {"admin0": "Kyrgyzstan"}, {"admin0": "Tajikistan"}]
EAST = [{"admin0": n} for n in ("Poland", "Czechia", "Slovakia", "Hungary", "Romania", "Bulgaria", "Albania", "Mongolia", "Cuba")] + [GDR]
WEST = [{"admin0": n} for n in ("United States of America", "Canada", "United Kingdom", "France", "Italy", "Norway", "Denmark", "Netherlands", "Belgium",
                                "Luxembourg", "Portugal", "Iceland", "Greece", "Turkey", "Spain", "Germany")]
COL15 = [(214, 66, 58), (240, 196, 25), (120, 120, 120), (230, 126, 34), (52, 152, 219), (155, 89, 182), (26, 188, 156), (231, 76, 60), (46, 204, 113),
         (243, 156, 18), (52, 73, 94), (22, 160, 133), (241, 90, 36), (142, 68, 173), (39, 174, 96)]
O = {}
def once(name, fn):
    p = os.path.join(A, name)
    if not os.path.exists(p): fn(p)
    O[name[:-4]] = name
def build():
    once("flag_ru.png", OVL.flag_ru)
    once("ov_rudj_flag.png", lambda p: OVL.fill(p, [RU], flag=os.path.join(A, "flag_ru.png"), alpha=180, box=[27, 180, 41, 78]))
    once("ov_rudj_edge.png", lambda p: OVL.edge(p, [RU], (255, 230, 160), 4, 9))
    once("ov_rudj_red.png", lambda p: OVL.fill(p, [RU], color=(200, 30, 30), alpha=200))
    once("ov_horde.png", lambda p: OVL.fill(p, [HORDE], color=(150, 20, 20), alpha=190))
    once("ov_horde_edge.png", lambda p: OVL.edge(p, [HORDE], (255, 90, 60), 4, 10))
    once("ov_fr_blue.png", lambda p: OVL.fill(p, [{"admin0": "France"}], color=(30, 70, 200), alpha=210, box=None) if False else OVL.fill(p, [{"poly": [[-4.8, 48.5], [-1.5, 43.4], [3.2, 42.4], [7.6, 43.8], [6.2, 46.3], [8.2, 49.0], [2.5, 51.1], [-1.6, 49.7]]}], color=(30, 70, 200), alpha=210))
    once("ov_pl.png", lambda p: OVL.fill(p, [{"admin0": "Poland"}], color=(220, 40, 60), alpha=200))
    once("ov_se.png", lambda p: OVL.fill(p, [{"admin0": "Sweden"}], color=(30, 100, 200), alpha=200))
    once("ov_jp.png", lambda p: OVL.fill(p, [{"admin0": "Japan"}], color=(230, 230, 230), alpha=210))
    once("ov_ussr_red.png", lambda p: OVL.fill(p, USSR, color=(200, 25, 25), alpha=205))
    once("ov_ussr_edge.png", lambda p: OVL.edge(p, USSR, (255, 120, 90), 4, 10))
    once("ov_east_red.png", lambda p: OVL.fill(p, EAST, color=(200, 25, 25), alpha=190))
    once("ov_west_blue.png", lambda p: OVL.fill(p, WEST, color=(30, 90, 220), alpha=190))
    once("ov_cuba.png", lambda p: OVL.fill(p, [{"admin0": "Cuba"}], color=(220, 30, 30), alpha=230))
    once("ov_us.png", lambda p: OVL.fill(p, [{"admin0": "United States of America"}], color=(30, 90, 220), alpha=170))
    import numpy as np; from PIL import Image
    def ussr15(p):
        acc = None
        for k, r in enumerate(USSR):
            tmp = p + f".{k}.png"; OVL.fill(tmp, [r], color=COL15[k], alpha=225); im = Image.open(tmp); os.remove(tmp)
            acc = im if acc is None else Image.alpha_composite(acc, im)
        acc.save(p)
    once("ov_ussr15.png", ussr15)
    once("ov_ussr15_edge.png", lambda p: OVL.edge(p, USSR, (255, 255, 255), 3, 6))
    once("ov_ua.png", lambda p: OVL.fill(p, [UA], color=(255, 213, 0), alpha=150))
    once("ov_ua_edge.png", lambda p: OVL.edge(p, [UA], (120, 190, 255), 4, 10))
    once("ov_crimea.png", lambda p: OVL.fill(p, [{"admin0": "Russia", "drop": []}], color=(0, 0, 0), alpha=0) if False else OVL.fill(p, [{"admin1": "Crimea"}, {"admin1": "Sevastopol"}], color=(230, 40, 40), alpha=230))
    once("ov_crimea_edge.png", lambda p: OVL.edge(p, [{"admin1": "Crimea"}, {"admin1": "Sevastopol"}], (255, 120, 90), 4, 9))
    once("ov_ak_us.png", lambda p: None)   # built for the pilot
    once("ov_ak_edge.png", lambda p: None)
    once("ov_mn_fill.png", lambda p: None); once("ov_mn_edge.png", lambda p: None)
    return O
if __name__ == "__main__":
    import time; t = time.time(); build(); print(sorted(O), round(time.time() - t, 1), "s")
