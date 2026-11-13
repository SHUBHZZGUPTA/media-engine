# Shot plan + beats for the Denmark desert Short (same for EN and HI: chunk counts match per line, except line 18).
import json, sys
p = sys.argv[1]; out = sys.argv[2]
S = json.load(open(p))
S['shots'] = [
 {'scene': 'MW', 'at': [0, 0, 0]},                         # globe -> Denmark in its flag
 {'scene': 'DU', 'at': [1, 0, -.15], 'cut': 'zoom'},       # dive onto the dune: 40 m, walking
 {'scene': 'MW', 'at': [3, 0, -.15], 'cut': 'curve'},      # green, rainy Denmark
 {'scene': 'MC', 'at': [4, 0, -.15], 'cut': 'whip'},       # rewind: the forests
 {'scene': 'MW', 'at': [7, 0, -.15], 'cut': 'curve'},      # North Jutland coast: trees held the sand
 {'scene': 'CH', 'at': [9, 0, -.15], 'cut': 'zoom'},       # Skagen church
 {'scene': 'MC', 'at': [15, 0, -.15], 'cut': 'curve'},     # Denmark fights back with trees
 {'scene': 'MW', 'at': [16, 0, -.15], 'cut': 'zoom'},      # rehook: one bare patch
 {'scene': 'DU', 'at': [18, 0, -.15], 'cut': 'curve'},     # bought in 1900, roams free
 {'scene': 'MC', 'at': [19, 0, -.1], 'cut': 'flash'},      # the twist
 {'scene': 'DU', 'at': [21, 0, -.15], 'cut': 'curve'},     # the main road
]
L = lambda lang, b: dict(b, lang=lang)
B = [
 {'kind': 'charslam', 'at': [0, 0, 0]},
 {'kind': 'punch', 'scene': 'MW', 'at': [0, 1, 0], 'level': 1.15, 'back': [1, 0, -.25]},
 {'kind': 'moment', 'what': 'Denmark fills with its flag', 'at': [0, 1, .1]},
 {'kind': 'grow', 'at': [1, 0, 0], 'word': '40', 'to': 40, 'unit': 'M TALL', 'dur': .8, 'until': [2, 0, -.15]},
 {'kind': 'punch', 'scene': 'DU', 'at': [1, 1, 0], 'level': 1.3, 'back': [2, 0, -.2]},
 {'kind': 'grow', 'at': [2, 0, 0], 'word': '18', 'to': 18, 'unit': 'M / YEAR', 'dur': .7, 'until': [3, 0, -.15]},
 {'kind': 'arrow', 'scene': 'DU', 'at': [2, 0, .3], 'from': [0.4, 5.7, 0], 'to': [2.4, 5.7, 0], 'col': '#FF3B30', 'until': [2, 1, -.05]},
 L('en', {'kind': 'slam', 'what': 'pitch', 'at': [2, 1, 0], 'word': 'CRICKET'}),
 L('hi', {'kind': 'slam', 'what': 'pitch', 'at': [2, 1, 0], 'word': 'CRICKET'}),
 {'kind': 'moment', 'what': 'rain over green Denmark', 'at': [3, 0, .2]},
 {'kind': 'circle', 'scene': 'MW', 'at': [3, 1, 0], 'c': [10.41, 57.648], 'r': [110, 80], 'col': '#FF3B30', 'until': [4, 0, -.2]},
 {'kind': 'flap', 'at': [4, 0, .1], 'text': '1500S', 'y': 170, 'until': [5, 0, .2]},
 {'kind': 'moment', 'what': 'forests shrink', 'at': [5, 0, 0]},
 L('en', {'kind': 'slam', 'what': 'axe', 'at': [5, 0, 0], 'word': 'CUT'}),
 L('hi', {'kind': 'slam', 'what': 'axe', 'at': [5, 0, 0], 'word': 'काट'}),
 {'kind': 'slam', 'what': 'lbl', 'lab': 'y1800', 'at': [6, 0, 0], 'word': '1800'},
 {'kind': 'grow', 'at': [6, 1, 0], 'prefix': '2–', 'to': 4, 'unit': '% FOREST', 'dur': .7, 'until': [7, 0, -.15]},
 {'kind': 'slam', 'what': 'num', 'at': [6, 2, .05]},
 {'kind': 'moment', 'what': 'trees along the coast', 'at': [7, 0, .1]},
 {'kind': 'slam', 'what': 'trees', 'at': [7, 1, 0]},
 {'kind': 'circle', 'scene': 'MW', 'at': [7, 1, 0], 'c': [10.20, 57.56], 'r': [170, 110], 'col': '#FF3B30', 'until': [8, 0, .2]},
 {'kind': 'moment', 'what': 'sand spreads inland', 'at': [8, 0, .1]},
 L('en', {'kind': 'slam', 'what': 'bury', 'at': [8, 1, 0], 'word': 'FARMS'}),
 L('hi', {'kind': 'slam', 'what': 'bury', 'at': [8, 2, 0], 'word': 'खेत'}),
 L('en', {'kind': 'grow', 'at': [8, 2, 0], 'word': '7', 'to': 7, 'unit': 'KM INLAND', 'dur': .7, 'until': [9, 0, -.15]}),
 L('hi', {'kind': 'grow', 'at': [8, 1, 0], 'word': '7', 'to': 7, 'unit': 'KM INLAND', 'dur': .7, 'until': [9, 0, -.15]}),
 {'kind': 'slam', 'what': 'lbl', 'lab': 'skagen', 'at': [9, 0, .3]},
 {'kind': 'slam', 'what': 'lbl', 'lab': 'towerA', 'at': [9, 1, .05]},
 {'kind': 'circle', 'scene': 'CH', 'at': [9, 1, 0], 'c': [-2.7, 1.6, 0], 'r': [150, 230], 'col': '#FF3B30', 'until': [10, 0, -.1]},
 {'kind': 'grow', 'at': [10, 0, 0], 'word': '20', 'to': 20, 'unit': 'YEARS', 'dur': .7, 'until': [11, 0, -.3]},
 {'kind': 'moment', 'what': 'shovel digs the door free', 'at': [10, 1, 0]},
 {'kind': 'punch', 'scene': 'CH', 'at': [10, 2, 0], 'level': 1.15, 'back': [11, 0, -.3]},
 {'kind': 'moment', 'what': 'dune character enters, knocks', 'at': [11, 0, -.3]},
 {'kind': 'moment', 'what': 'church character protests', 'at': [12, 0, -.3]},
 {'kind': 'slam', 'what': 'knock', 'at': [11, 0, 0]},
 {'kind': 'slam', 'what': 'jolt', 'at': [12, 1, 0]},
 {'kind': 'punch', 'scene': 'CH', 'at': [13, 0, 0], 'level': 1.2, 'back': [14, 0, -.3]},
 {'kind': 'grow', 'at': [14, 0, 0], 'word': '1795', 'from': 1700, 'to': 1795, 'unit': '', 'dur': .8, 'until': [15, 0, -.15]},
 {'kind': 'moment', 'what': 'the nave sinks, the tower stays', 'at': [14, 0, .9]},
 {'kind': 'slam', 'what': 'lbl', 'lab': 'tower', 'at': [14, 1, 0]},
 {'kind': 'moment', 'what': 'forests grow back over the sand', 'at': [15, 0, .2]},
 {'kind': 'grow', 'at': [15, 1, 0], 'word': '1950', 'from': 1800, 'to': 1950, 'unit': 'S', 'dur': .8, 'until': [16, 0, -.15]},
 {'kind': 'circle', 'scene': 'MW', 'at': [16, 1, 0], 'c': [10.404, 57.6485], 'r': [150, 120], 'col': '#FF3B30', 'until': [17, 0, .3]},
 {'kind': 'punch', 'scene': 'MW', 'at': [16, 1, 0], 'level': 1.2, 'back': [17, 0, -.2]},
 {'kind': 'card', 'scene': 'MW', 'at': [17, 0, .15], 'flag': '🇩🇰', 'name': 'RÅBJERG MILE', 'tag': 'PROTECTED', 'until': [18, 0, -.2]},
 L('en', {'kind': 'grow', 'at': [18, 1, 0], 'word': '1900', 'from': 1850, 'to': 1900, 'unit': '', 'dur': .7, 'until': [19, 0, -.2]}),
 L('hi', {'kind': 'grow', 'at': [18, 0, 0], 'word': '1900', 'from': 1850, 'to': 1900, 'unit': '', 'dur': .7, 'until': [19, 0, -.2]}),
 {'kind': 'moment', 'what': 'the dune walks (time-lapse)', 'at': [18, 2, 0]},
 L('hi', {'kind': 'slam', 'what': 'num', 'at': [18, 2, 0]}),
 {'kind': 'arrow', 'scene': 'MC', 'at': [20, 1, 0], 'from': [10.41, 57.652], 'to': [10.545, 57.711], 'col': '#FFC23A', 'until': [21, 0, -.2]},
 {'kind': 'circle', 'scene': 'MC', 'at': [20, 2, 0], 'c': [10.5503, 57.7137], 'r': [110, 90], 'col': '#FF3B30', 'until': [21, 0, -.2]},
 {'kind': 'slam', 'what': 'lbl', 'lab': 'church', 'at': [20, 2, .05]},
 {'kind': 'grow', 'at': [21, 0, .05], 'prefix': '100–', 'from': 150, 'to': 200, 'unit': 'YEARS', 'dur': .8, 'until': [22, 0, -.2]},
 {'kind': 'moment', 'what': 'dune slides toward the road', 'at': [21, 1, 0]},
 {'kind': 'slam', 'what': 'lbl', 'lab': 'road', 'at': [21, 2, 0]},
 {'kind': 'moment', 'what': 'dune character on the road', 'at': [22, 0, -.3]},
 {'kind': 'punch', 'scene': 'DU', 'at': [22, 1, 0], 'level': 1.2, 'back': [23, 0, -.1]},
]
S['beats'] = B
S['hand'] = []
S['impacts'] = []
S['music_sections'] = {'pad': [[[0, 0, -.5], 'end', .85]], 'arp': [[[0, 0, 0], [4, 0, -.2], .8], [[7, 0, 0], [9, 0, -.2], .7], [[15, 0, 0], 'end', .85]],
                       'drums': [[[0, 1, 0], [4, 0, -.3], .6], [[7, 0, 0], [11, 0, -.3], .55], [[16, 0, 0], 'end', .55]],
                       'bass': [[[1, 0, 0], [4, 0, -.2], .8], [[5, 0, 0], 'end', .75]]}
S['story'] = [['sparkle.mp3', [0, 1, .1], .5], ['thump.mp3', [11, 0, 0], .7], ['thump.mp3', [11, 0, .32], .7], ['chime.mp3', [17, 0, .2], .4]]
json.dump(S, open(out, 'w'), ensure_ascii=False, indent=1)
print('plan ->', out, len(B), 'beats')
