# Shot plan + beats for the Baikal Short, written into the spec (same for EN and HI: chunk counts match per line).
import json, sys
p = sys.argv[1] if len(sys.argv) > 1 else 'baikal.base.json'; out = sys.argv[2] if len(sys.argv) > 2 else 'baikal.json'
S = json.load(open(p))
S['shots'] = [
 {'scene': 'MP', 'at': [0, 0, 0]},
 {'scene': 'GL', 'at': [0, 1, -.15], 'cut': 'curve'},
 {'scene': 'MP', 'at': [1, 0, -.15], 'cut': 'curve'},
 {'scene': 'GL', 'at': [2, 2, -.15], 'cut': 'curve'},
 {'scene': 'MP', 'at': [4, 1, -.15], 'cut': 'curve'},
 {'scene': 'XS', 'at': [5, 0, -.15], 'cut': 'zoom'},
 {'scene': 'MP', 'at': [10, 0, -.15], 'cut': 'curve'},
 {'scene': 'XS', 'at': [11, 0, -.15], 'cut': 'whip'},
 {'scene': 'GL', 'at': [12, 0, -.15], 'cut': 'whip'},
 {'scene': 'MP', 'at': [14, 0, -.15], 'cut': 'curve'},
 {'scene': 'XS', 'at': [15, 0, -.15], 'cut': 'flash'},
 {'scene': 'MP', 'at': [18, 0, -.15], 'cut': 'zoomIn'},
]
B = [
 {'kind': 'charslam', 'at': [0, 0, 0]},
 {'kind': 'punch', 'scene': 'MP', 'at': [0, 0, .3], 'level': 1.15, 'back': [0, 1, -.2]},
 {'kind': 'count', 'at': [0, 1, .1]},
 {'kind': 'punch', 'scene': 'GL', 'at': [0, 1, .5], 'level': 1.22, 'back': [1, 0, -.2]},
 {'kind': 'punch', 'scene': 'MP', 'at': [1, 0, .25], 'level': 1.15, 'back': [1, 1, -.1]},
 {'kind': 'moment', 'what': 'belgium drops onto the lake', 'at': [1, 1, 0]},
 {'kind': 'slam', 'what': 'drop', 'at': [1, 1, .45]},
 {'kind': 'card', 'scene': 'MP', 'at': [2, 0, .1], 'flag': '🇷🇺', 'name': 'LAKE BAIKAL', 'to': 636, 'unit': 'km long', 'tag': 'SIBERIA', 'until': [2, 2, -.25]},
 {'kind': 'moment', 'what': 'Superior enters', 'at': [3, 0, -.3]},
 {'kind': 'moment', 'what': 'Baikal outline drops beside the Great Lakes', 'at': [4, 0, 0]},
 {'kind': 'grow', 'at': [4, 0, .35], 'to': 8, 'prefix': '×', 'unit': 'AREA', 'until': [4, 1, -.2], 'dur': .8},
 {'kind': 'circle', 'scene': 'MP', 'at': [4, 2, 0], 'c': [107.9, 53.4], 'r': [150, 280], 'col': '#FFC23A'},
 {'kind': 'impact', 'at': [5, 0, .1]},
 {'kind': 'slam', 'what': 'depth', 'at': [6, 0, 0], 'word': '1,642'},
 {'kind': 'grow', 'at': [6, 1, 0], 'to': 4, 'prefix': '×', 'unit': 'DEEPER', 'word': 'FOUR', 'y': 150},
 {'kind': 'circle', 'scene': 'XS', 'at': [6, 2, 0], 'c': [0, 4.4], 'r': [300, 90], 'col': '#FFC23A', 'until': [7, 0, -.3]},
 {'kind': 'moment', 'what': 'Superior pops in on the section', 'at': [7, 0, -.3]},
 {'kind': 'count', 'at': [8, 0, .1]},
 {'kind': 'moment', 'what': 'five Eiffel Towers stack up', 'at': [8, 1, 0]},
 {'kind': 'punch', 'scene': 'XS', 'at': [9, 0, .1], 'level': 1.14, 'back': [9, 1, -.05]},
 {'kind': 'circle', 'scene': 'XS', 'at': [9, 2, .1], 'c': [.1, -4.8], 'r': [110, 300], 'col': '#FFC23A', 'until': [10, 0, -.25]},
 {'kind': 'arrow', 'scene': 'MP', 'at': [10, 1, 0], 'from': [107.45, 53.25], 'to': [106.4, 54.05], 'col': '#FFC23A'},
 {'kind': 'arrow', 'scene': 'MP', 'at': [10, 1, .15], 'from': [107.55, 53.15], 'to': [108.6, 52.45], 'col': '#FFC23A'},
 {'kind': 'grow', 'at': [11, 1, 0], 'from': 25, 'to': 30, 'unit': 'MILLION YRS', 'dur': 1.0},
 {'kind': 'grow', 'at': [12, 1, 0], 'to': 14000, 'unit': 'YEARS AGO', 'word': '14,000'},
 {'kind': 'moment', 'what': 'Superior, embarrassed', 'at': [13, 0, -.3]},
 {'kind': 'arrow', 'scene': 'MP', 'at': [14, 1, 0], 'from': [107.45, 53.25], 'to': [106.6, 53.9], 'col': '#FFC23A'},
 {'kind': 'arrow', 'scene': 'MP', 'at': [14, 1, .15], 'from': [107.55, 53.15], 'to': [108.4, 52.55], 'col': '#FFC23A'},
 {'kind': 'grow', 'at': [14, 2, 0], 'to': 4, 'unit': 'MM / YEAR', 'dur': .8},
 {'kind': 'punch', 'scene': 'XS', 'at': [15, 1, 0], 'level': 1.12, 'back': [16, 0, -.3]},
 {'kind': 'punch', 'scene': 'XS', 'at': [16, 0, .1], 'level': 1.18, 'back': [16, 1, 0]},
 {'kind': 'flashfx', 'at': [16, 0, 0]},
 {'kind': 'impact', 'at': [16, 1, .2]},
 {'kind': 'slam', 'what': 'mud', 'at': [17, 1, 0], 'word': 'SEVEN'},
 {'kind': 'circle', 'scene': 'XS', 'at': [17, 3, 0], 'c': [.1, -4.6], 'r': [180, 400], 'col': '#FFC23A', 'until': [18, 0, -.25]},
 {'kind': 'punch', 'scene': 'XS', 'at': [17, 2, 0], 'level': 1.1, 'back': [17, 3, .3]},
 {'kind': 'moment', 'what': 'Belgium drops onto the lake again', 'at': [18, 1, 0]},
 {'kind': 'slam', 'what': 'drop', 'at': [18, 1, .5]},
 {'kind': 'moment', 'what': 'Belgium speaks', 'at': [19, 0, -.3]},
 {'kind': 'slam', 'what': 'title', 'at': [11, 3, 0]},
 {'kind': 'slam', 'what': 'jolt', 'char': 'MP.cBel', 'at': [19, 1, 0]},
 {'kind': 'slam', 'what': 'jolt', 'char': 'GL.cSup', 'at': [3, 0, 0], 'word': 'EIGHT'},
]
B += [
 {'kind': 'slam', 'what': 'pop', 'lab': 'GL.lab', 'show': 1, 'at': [2, 2, .25], 'until': [3, 0, -.4]},
 {'kind': 'slam', 'what': 'pop', 'lab': 'XS.lBk', 'at': [5, 0, .45]},
 {'kind': 'slam', 'what': 'jolt', 'char': 'XS.cSup', 'at': [7, 0, 0], 'word': 'MEASURE'},
 {'kind': 'slam', 'what': 'pop', 'lab': 'XS.lCrack', 'show': 1, 'at': [9, 2, .35], 'until': [10, 0, -.2]},
 {'kind': 'slam', 'what': 'mudlit', 'at': [16, 1, .4]},
 {'kind': 'slam', 'what': 'pop', 'lab': 'XS.lSup', 'at': [6, 2, .15]},
 {'kind': 'slam', 'what': 'pop', 'lab': 'XS.lDep', 'at': [6, 0, .2]},
]
S['beats'] = B
S['music_sections'] = {
 'pad': [[[0, 0, -.5], [16, 0, -.2], .9], [[16, 0, -.2], [18, 0, -.2], .55], [[18, 0, -.2], 'end', .9]],
 'arp': [[[0, 0, 0], [5, 0, -.2], .8], [[10, 0, 0], [15, 0, 0], .7], [[18, 0, 0], 'end', 1]],
 'drums': [[[0, 1, 0], [5, 0, -.3], .6], [[10, 0, 0], [12, 0, -.2], .7], [[14, 0, 0], [16, 0, -.3], .7], [[18, 1, 0], 'end', .5]],
 'bass': [[[2, 0, 0], [5, 0, -.2], .8], [[9, 0, 0], [16, 0, -.2], .7], [[17, 0, 0], 'end', .8]]}
S['hand'] = [[[10, 0, 0], [11, 0, -.2]], [[14, 0, 0], [15, 0, -.2]]]
S['impacts'] = [[5, 0, .1], [16, 1, .2]]
json.dump(S, open(out, 'w'), ensure_ascii=False, indent=1); print('plan ->', out, len(S['shots']), 'shots', len(B), 'beats')
