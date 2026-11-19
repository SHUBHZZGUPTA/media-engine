# Shot plan + beats for the Märket Short (same chunk counts EN/HI). Usage: python3 plan.py <base.json> <out.json>
import json, sys
S = json.load(open(sys.argv[1]))
S['shots'] = [
 {'scene': 'MK', 'at': [0, 0, 0]},                         # cover pose: the island, two halves, the S border
 {'scene': 'MW', 'at': [3, 0, -.15], 'cut': 'zoom'},       # this is Märket: Baltic map, Sweden + Finland, pin
 {'scene': 'MK2', 'at': [3, 2, -.15], 'cut': 'zoom'},    # no trees, no people, just seals
 {'scene': 'MK', 'at': [4, 0, -.15], 'cut': 'curve'},      # who drew this mess?
 {'scene': 'MH', 'at': [5, 0, -.15], 'cut': 'whip'},       # rewind to 1809
 {'scene': 'MK', 'at': [6, 1, -.15], 'cut': 'zoom'},       # a straight line through the rock; the lighthouse
 {'scene': 'MK2', 'at': [9, 0, -.15], 'cut': 'curve'},     # Sweden not thrilled; the view
 {'scene': 'MK', 'at': [11, 0, -.15], 'cut': 'curve'},     # 100 years in the wrong country
 {'scene': 'MW', 'at': [12, 0, -.15], 'cut': 'curve'},     # rehook: the fix
 {'scene': 'MK2', 'at': [13, 0, -.15], 'cut': 'flash'},    # 1985: they moved the border
 {'scene': 'MK', 'at': [16, 0, -.15], 'cut': 'curve'},     # one hour behind; hop back and forth; loop
]
B = [
 {'kind': 'charslam', 'at': [0, 0, 0]},
 {'kind': 'punch', 'scene': 'MK', 'at': [0, 0, 0], 'word': 'ROCK', 'level': 1.15, 'back': [0, 1, -.1]},
 {'kind': 'punch', 'scene': 'MK', 'at': [0, 2, 0], 'word': 'TIME', 'level': 1.25, 'back': [1, 0, -.1]},
 {'kind': 'punch', 'scene': 'MK', 'at': [1, 1, 0], 'word': 'HOUR', 'level': 1.4, 'back': [2, 0, -.2]},
 {'kind': 'slam', 'what': 'clock', 'at': [1, 1, .1]},
 {'kind': 'moment', 'what': 'Sweden half fills', 'at': [2, 0, 0]},
 {'kind': 'slam', 'what': 'pop', 'at': [2, 1, 0]},
 {'kind': 'moment', 'what': 'the S border draws', 'at': [2, 2, 0]},
 {'kind': 'circle', 'scene': 'MK', 'at': [2, 3, 0], 'c': [4.8, -1.2, .2], 'r': [330, 250], 'col': '#FF3B30', 'until': [2, 4, .6]},
 {'kind': 'slam', 'what': 'pop', 'at': [2, 4, 0]},
 {'kind': 'card', 'scene': 'MW', 'at': [3, 1, 0], 'flag': '🇸🇪🇫🇮', 'name': 'MÄRKET', 'to': 350, 'unit': 'M', 'until': [3, 2, -.2]},
 {'kind': 'slam', 'what': 'pop', 'at': [3, 3, 0]},
 {'kind': 'punch', 'scene': 'MK', 'at': [4, 0, 0], 'word': 'MESS', 'level': 1.2, 'back': [5, 0, -.2]},
 {'kind': 'grow', 'at': [5, 0, 0], 'word': '1809', 'from': 1700, 'to': 1809, 'unit': '', 'dur': .8, 'until': [5, 2, .3]},
 {'kind': 'slam', 'what': 'num', 'at': [5, 0, .85]},
 {'kind': 'moment', 'what': 'Finland turns Russian-Empire green', 'at': [5, 2, 0]},
 {'kind': 'slam', 'what': 'pop', 'at': [5, 2, .15]},
 {'kind': 'moment', 'what': 'pin pulses on Märket', 'at': [6, 0, 0]},
 {'kind': 'moment', 'what': 'straight line draws through the rock', 'at': [6, 1, 0]},
 {'kind': 'grow', 'at': [7, 0, 0], 'word': '1885', 'from': 1809, 'to': 1885, 'unit': '', 'dur': .8, 'until': [7, 2, -.1]},
 {'kind': 'slam', 'what': 'num', 'at': [7, 0, .85]},
 {'kind': 'slam', 'what': 'rise', 'at': [7, 1, .1]},
 {'kind': 'arrow', 'scene': 'MK', 'at': [7, 2, 0], 'from': [-3.0, 3.5, 2.6], 'to': [-.3, .5, 1.2], 'col': '#FFC23A', 'until': [7, 3, -.05]},
 {'kind': 'grow', 'at': [7, 3, 0], 'word': 'TWO', 'to': 2, 'unit': 'M', 'dur': .6, 'until': [8, 0, -.1]},
 {'kind': 'slam', 'what': 'num', 'at': [7, 3, .65]},
 {'kind': 'punch', 'scene': 'MK', 'at': [8, 0, 0], 'word': 'PROBLEM', 'level': 1.15, 'back': [8, 1, -.05]},
 {'kind': 'circle', 'scene': 'MK', 'at': [8, 1, 0], 'c': [0, 0, .9], 'r': [150, 230], 'col': '#FF3B30', 'until': [9, 0, -.2]},
 {'kind': 'slam', 'what': 'pop', 'at': [9, 0, .55]},
 {'kind': 'slam', 'what': 'pop', 'at': [10, 1, .1]},
 {'kind': 'grow', 'at': [11, 2, 0], 'word': '100', 'from': 1885, 'to': 1985, 'unit': '', 'dur': 1.4, 'until': [12, 0, -.1]},
 {'kind': 'moment', 'what': 'day-night cycles', 'at': [11, 0, .2]},
 {'kind': 'punch', 'scene': 'MW', 'at': [12, 0, 0], 'word': 'WEIRDER', 'level': 1.2, 'back': [13, 0, -.2]},
 {'kind': 'grow', 'at': [13, 0, 0], 'word': '1985', 'from': 1950, 'to': 1985, 'unit': '', 'dur': .7, 'until': [13, 2, -.1]},
 {'kind': 'slam', 'what': 'num', 'at': [13, 0, .75]},
 {'kind': 'slam', 'what': 'morph', 'at': [13, 2, .25]},
 {'kind': 'moment', 'what': 'pulse runs along the S', 'at': [14, 0, 0]},
 {'kind': 'slam', 'what': 'pop', 'at': [15, 0, .15]},
 {'kind': 'grow', 'at': [14, 2, 0], 'word': '480', 'to': 480, 'unit': 'M', 'dur': 1.0, 'until': [15, 0, -.1]},
 {'kind': 'slam', 'what': 'num', 'at': [14, 2, 1.05]},
 {'kind': 'moment', 'what': 'lighthouse patch pulses gold', 'at': [15, 0, .1]},
 {'kind': 'slam', 'what': 'stamp', 'at': [15, 1, .25], 'until': [16, 0, -.2]},
 {'kind': 'slam', 'what': 'clock', 'at': [16, 1, 0]},
 {'kind': 'moment', 'what': 'walker hops across the S, his clock flips', 'at': [17, 0, .1]},
 {'kind': 'slam', 'what': 'pop', 'at': [17, 0, .15]},
 {'kind': 'slam', 'what': 'clock', 'at': [17, 1, 0]},
 {'kind': 'slam', 'what': 'clock', 'at': [17, 2, 0]},
 {'kind': 'slam', 'what': 'pop', 'at': [18, 1, 0]},
 {'kind': 'punch', 'scene': 'MK', 'at': [18, 1, 0], 'word': 'EXTRA', 'level': 1.15, 'back': [19, 0, -.1]},
 {'kind': 'moment', 'what': 'camera glides back to the cover', 'at': [19, 0, 0]},
 {'kind': 'slam', 'what': 'pop', 'at': [19, 1, .1]},
]
S['beats'] = B
S['impacts'] = []
S['cover_cam'] = {'x': -1.5, 'y': 0, 'z': 2.0, 'dist': 70, 'yaw': 68, 'pitch': 62}
S['cover_en'] = ['WHY THE', '[ZIGZAG?]']
S['cover_hi'] = ['बॉर्डर', '[ZIGZAG] क्यों?']
S['music_sections'] = {'pad': [[[0, 0, -.5], 'end', .85]], 'arp': [[[0, 0, 0], [5, 0, -.2], .8], [[13, 0, 0], 'end', .85]],
                       'drums': [[[0, 1, 0], [4, 0, -.3], .6], [[6, 1, 0], [11, 0, -.3], .55], [[13, 2, 0], 'end', .55]],
                       'bass': [[[1, 0, 0], [5, 0, -.2], .8], [[6, 0, 0], 'end', .75]]}
S['story'] = [['sparkle.mp3', [2, 0, 0], .4], ['chime.mp3', [10, 1, .1], .35], ['stamp.mp3', [15, 1, .25], .6], ['clock.mp3', [16, 1, 0], .35]]
json.dump(S, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
print('plan ->', sys.argv[2], len(B), 'beats')
