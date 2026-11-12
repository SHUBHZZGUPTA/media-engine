# Shot plan + beats for the Russia time zones Short (same for EN and HI: chunk counts match per line).
import json, sys
p = sys.argv[1] if len(sys.argv) > 1 else 'rutz.base.json'; out = sys.argv[2] if len(sys.argv) > 2 else 'rutz.json'
S = json.load(open(p))
S['shots'] = [
 {'scene': 'GA', 'at': [0, 0, 0]},
 {'scene': 'GB', 'at': [1, 0, -.15], 'cut': 'curve'},     # Kamchatka midnight vs Kaliningrad 2 PM
 {'scene': 'GA', 'at': [2, 0, -.15], 'cut': 'curve'},     # eleven clocks: zones light up
 {'scene': 'GB', 'at': [3, 0, -.15], 'cut': 'whip'},      # rewind to 2010
 {'scene': 'KM', 'at': [4, 0, -.15], 'cut': 'zoomIn'},    # dive onto Kamchatka
 {'scene': 'GA', 'at': [5, 0, -.15], 'cut': 'whip'},      # 2014
 {'scene': 'GB', 'at': [6, 0, -.15], 'cut': 'curve'},     # trains
 {'scene': 'GA', 'at': [8, 0, -.15], 'cut': 'curve'},     # world record, right?
 {'scene': 'WM', 'at': [9, 0, -.15], 'cut': 'flash'},     # nope: France
 {'scene': 'GA', 'at': [11, 0, -.15], 'cut': 'zoomIn'},   # sign-off / end card
]
B = [
 {'kind': 'charslam', 'at': [0, 0, 0]},
 {'kind': 'punch', 'scene': 'GA', 'at': [0, 0, 0], 'word': 'ONE', 'level': 1.15, 'back': [0, 1, -.1]},
 {'kind': 'moment', 'what': 'midnight sweeps west, fireworks pop zone by zone', 'at': [0, 1, 0]},
 {'kind': 'punch', 'scene': 'GA', 'at': [0, 1, 0], 'word': 'ELEVEN', 'level': 1.3, 'back': [1, 0, -.25]},
 {'kind': 'card', 'scene': 'GB', 'at': [1, 0, .1], 'pin': 'kam', 'flag': '🌙', 'name': 'KAMCHATKA', 'to': 0, 'unit': ':00', 'pad': 2, 'tag': 'MIDNIGHT', 'until': [2, 0, -.2]},
 {'kind': 'card', 'scene': 'GB', 'at': [1, 1, 0], 'pin': 'kal', 'flag': '☀️', 'name': 'KALININGRAD', 'to': 14, 'unit': ':00', 'tag': '2 PM', 'until': [2, 0, -.2]},
 {'kind': 'punch', 'scene': 'GB', 'at': [1, 1, 0], 'word': '2', 'level': 1.2, 'back': [2, 0, -.25]},
 {'kind': 'moment', 'what': 'zones light up west to east', 'at': [2, 0, .2]},
 {'kind': 'grow', 'at': [2, 1, 0], 'from': 1, 'to': 11, 'unit': 'ZONES', 'dur': 1.0, 'until': [3, 0, -.2]},
 {'kind': 'circle', 'scene': 'GB', 'at': [3, 1, 0], 'c': [50.5, 53.2], 'r': [120, 90], 'col': '#FF3B30', 'until': [4, 0, -.2]},
 {'kind': 'circle', 'scene': 'GB', 'at': [3, 1, .3], 'c': [162, 61], 'r': [150, 130], 'col': '#FF3B30', 'until': [4, 0, -.2]},
 {'kind': 'grow', 'at': [3, 1, 0], 'from': 11, 'to': 9, 'unit': 'ZONES', 'word': 'TWO', 'dur': .6, 'until': [4, 0, -.2], 'lang': 'en'},
 {'kind': 'grow', 'at': [3, 1, 0], 'from': 11, 'to': 9, 'unit': 'ZONES', 'word': 'हटा', 'dur': .6, 'until': [4, 0, -.2], 'lang': 'hi'},
 {'kind': 'slam', 'what': 'merge', 'at': [3, 1, 0], 'word': 'TWO', 'lang': 'en'},
 {'kind': 'slam', 'what': 'merge', 'at': [3, 1, 0], 'word': 'हटा', 'lang': 'hi'},
 {'kind': 'punch', 'scene': 'KM', 'at': [4, 1, 0], 'level': 1.2, 'back': [5, 0, -.25]},
 {'kind': 'slam', 'what': 'protest', 'at': [4, 1, .05]},
 {'kind': 'grow', 'at': [5, 1, 0], 'from': 9, 'to': 11, 'unit': 'ZONES', 'word': 'BACK', 'dur': .6, 'until': [6, 0, -.2], 'lang': 'en'},
 {'kind': 'grow', 'at': [5, 1, 0], 'from': 9, 'to': 11, 'unit': 'ZONES', 'word': 'वापस', 'dur': .6, 'until': [6, 0, -.2], 'lang': 'hi'},
 {'kind': 'slam', 'what': 'restore', 'at': [5, 1, 0], 'word': 'BACK', 'lang': 'en'},
 {'kind': 'slam', 'what': 'restore', 'at': [5, 1, 0], 'word': 'वापस', 'lang': 'hi'},
 {'kind': 'punch', 'scene': 'GB', 'at': [6, 1, 0], 'level': 1.15, 'back': [6, 2, -.1], 'lang': 'hi'},
 {'kind': 'punch', 'scene': 'GB', 'at': [7, 0, .15], 'level': 1.14, 'back': [7, 1, .3], 'lang': 'hi'},
 {'kind': 'moment', 'what': 'Trans-Siberian line draws Moscow to Vladivostok, train rides it', 'at': [6, 0, .1]},
 {'kind': 'card', 'scene': 'GB', 'at': [6, 2, 0], 'pin': 'vla', 'flag': '🎫', 'name': 'TICKET', 'to': 19, 'unit': ':00', 'tag': 'MSK', 'until': [7, 1, -.1]},
 {'kind': 'moment', 'what': 'alarm clock character pops in', 'at': [7, 0, -.3]},
 {'kind': 'circle', 'scene': 'GB', 'screen': [760, 1010], 'at': [7, 1, 0], 'word': '2', 'r': [170, 90], 'col': '#FF3B30', 'until': [8, 0, -.2]},
 {'kind': 'slam', 'what': 'jolt', 'char': 'clock', 'at': [7, 0, .45]},
 {'kind': 'slam', 'what': 'jolt', 'char': 'clock', 'at': [7, 1, 0], 'word': '2'},
 {'kind': 'punch', 'scene': 'GA', 'at': [8, 0, .1], 'level': 1.2, 'back': [9, 0, -.2]},
 {'kind': 'moment', 'what': 'France fills with its flag, island pins pop worldwide', 'at': [9, 1, 0]},
 {'kind': 'grow', 'at': [9, 1, 0], 'from': 11, 'to': 12, 'unit': 'ZONES', 'word': 'TWELVE', 'dur': .45, 'until': [10, 0, -.2]},
 {'kind': 'impact', 'at': [9, 1, .25]},
 {'kind': 'slam', 'what': 'pins', 'at': [9, 2, 0], 'word': 'ISLANDS', 'lang': 'en'},
 {'kind': 'slam', 'what': 'pins', 'at': [9, 2, 0], 'word': 'द्वीपों', 'lang': 'hi'},
 {'kind': 'moment', 'what': 'France character enters', 'at': [10, 0, -.3]},
 {'kind': 'arrow', 'scene': 'WM', 'at': [10, 1, 0], 'from': [2.35, 46.8], 'to': [-149.4, -17.6], 'col': '#FFC23A'},
 {'kind': 'arrow', 'scene': 'WM', 'at': [10, 1, .15], 'from': [2.35, 46.8], 'to': [165.6, -21.3], 'col': '#FFC23A'},
 {'kind': 'slam', 'what': 'jolt', 'char': 'france', 'at': [10, 1, 0]},
]
S['beats'] = B
S['music_sections'] = {
 'pad': [[[0, 0, -.5], 'end', .85]],
 'arp': [[[0, 0, 0], [3, 0, -.2], .8], [[6, 0, 0], [8, 0, 0], .7], [[9, 0, 0], 'end', .9]],
 'drums': [[[0, 1, 0], [3, 0, -.3], .6], [[6, 0, 0], [8, 0, -.2], .6], [[9, 1, 0], 'end', .55]],
 'bass': [[[1, 0, 0], [4, 0, -.2], .8], [[5, 0, 0], 'end', .75]]}
S['hand'] = [[[4, 0, 0], [5, 0, -.2]]]
S['impacts'] = [[3, 1, .1], [9, 1, .25]]
S['story'] = [['sparkle.mp3', [0, 1, 0], .55], ['crowd.mp3', [4, 1, -.1], .45], ['clock.mp3', [7, 0, -.3], .45], ['chime.mp3', [9, 1, 0], .4]]
json.dump(S, open(out, 'w'), ensure_ascii=False, indent=1); print('plan ->', out, len(S['shots']), 'shots', len(B), 'beats')
