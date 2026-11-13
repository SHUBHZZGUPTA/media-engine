# Shot plan + beats + map labels for the same-size countries Short (EN and HI share chunk indices per line).
import json, sys
src, out = sys.argv[1], sys.argv[2]
S = json.load(open(src)); HI = 'hi' in S['slug']
S['shots'] = [{'scene': 'SA', 'at': [0, 0, 0]}, {'scene': 'WA', 'at': [3, 0, -.15], 'cut': 'curve'}, {'scene': 'ZC', 'at': [6, 0, -.15], 'cut': 'zoom'},
              {'scene': 'IT', 'at': [8, 0, -.15], 'cut': 'curve'}, {'scene': 'SEA', 'at': [11, 0, -.15], 'cut': 'burn'}]
W = lambda en, hi: {'word': hi if HI else en}
B = [
 {'kind': 'charslam', 'at': [0, 0, .25]},
 {'kind': 'punch', 'scene': 'SA', 'at': [0, 0, .2], 'level': 1.15, 'back': [0, 1, -.1], **W('$100', '$100')},
 {'kind': 'punch', 'scene': 'SA', 'at': [0, 2, 0], 'level': 1.25, 'back': [0, 3, -.1], **W('COMPLETELY', 'बिल्कुल')},
 {'kind': 'punch', 'scene': 'SA', 'at': [0, 3, 0], 'level': 1.38, 'back': [1, 0, -.4], **W('SAME', 'एक')},
 {'kind': 'slam', 'what': 'rank', 'n': 5, 'at': [1, 0, 0], **W('FIVE', 'फाइव'), 'until': [1, 1, .2], 'off': [3, 0, -.2]},
 {'kind': 'count', 'at': [2, 0, .4]},
 {'kind': 'circle', 'scene': 'SA', 'at': [2, 2, 0], 'c': [86.93, 27.99], 'r': [150, 110], 'col': '#FF3B30', 'until': [2, 3, -.2]},
 {'kind': 'arrow', 'scene': 'SA', 'at': [2, 4, 0], 'from': [90.55, 23.5], 'to': [90.9, 21.5], 'col': '#FFC23A', 'until': [2, 4, .9]},
 {'kind': 'card', 'scene': 'SA', 'at': [2, 4, .45], 'until': [3, 0, -.3], 'side': 'L', 'flag': '🇳🇵', 'name': 'NEPAL', 'to': 147181, 'lon': 84.0, 'lat': 28.2},
 {'kind': 'card', 'scene': 'SA', 'at': [2, 4, .6], 'until': [3, 0, -.3], 'side': 'R', 'flag': '🇧🇩', 'name': 'BANGLADESH', 'to': 148460, 'lon': 90.3, 'lat': 23.8},
 {'kind': 'slam', 'what': 'rank', 'n': 4, 'at': [3, 0, 0], **W('FOUR', 'फोर'), 'until': [3, 1, .1], 'off': [6, 0, -.2]},
 {'kind': 'slam', 'what': 'land', 'at': [3, 1, .65], **W('UNITED', 'यूनाइटेड')},
 {'kind': 'punch', 'scene': 'WA', 'at': [4, 0, 0], 'level': 1.18, 'back': [4, 1, -.1]},
 {'kind': 'slam', 'what': 'crown', 'at': [4, 1, 0], **W('BIGGEST', 'सबसे')},
 {'kind': 'card', 'scene': 'WA', 'at': [4, 2, .1], 'until': [5, 0, -.45], 'side': 'L', 'flag': '🇬🇳', 'name': 'GUINEA', 'to': 245857, 'lon': -12.5, 'lat': 9.6},
 {'kind': 'card', 'scene': 'WA', 'at': [4, 2, .25], 'until': [5, 0, -.45], 'side': 'R', 'flag': '🇬🇧', 'name': 'UNITED KINGDOM', 'to': 243610, 'lon': -10.0, 'lat': 11.2},
 {'kind': 'moment', 'what': 'UK character sobs', 'at': [5, 0, -.3]},
 {'kind': 'slam', 'what': 'rank', 'n': 3, 'at': [6, 0, 0], **W('THREE', 'थ्री'), 'until': [6, 1, .1], 'off': [8, 0, -.2]},
 {'kind': 'moment', 'what': 'Chile slides in', 'at': [6, 1, 0], **W('CHILE', 'चिली')},
 {'kind': 'moment', 'what': 'Zambia lifts off the map', 'at': [7, 0, .25]},
 {'kind': 'punch', 'scene': 'ZC', 'at': [7, 1, 0], 'level': 1.16, 'back': [7, 2, .2]},
 {'kind': 'circle', 'scene': 'ZC', 'at': [7, 2, .2], 'c': [12.6, -13.2], 'r': [120, 520], 'col': '#FF3B30', 'until': [7, 3, .2], **W('CHILE', 'चिली')},
 {'kind': 'card', 'scene': 'ZC', 'at': [7, 3, 0], 'until': [8, 0, -.3], 'side': 'R', 'flag': '🇿🇲', 'name': 'ZAMBIA', 'to': 752618, 'lon': 28.0, 'lat': -6},
 {'kind': 'card', 'scene': 'ZC', 'at': [7, 3, .15], 'until': [8, 0, -.3], 'side': 'L', 'flag': '🇨🇱', 'name': 'CHILE', 'to': 756102, 'lon': 12.6, 'lat': -6},
 {'kind': 'slam', 'what': 'rank', 'n': 2, 'at': [8, 0, 0], **W('TWO', 'टू'), 'until': [8, 1, .1], 'off': [11, 0, -.2]},
 {'kind': 'moment', 'what': 'Philippines flies in', 'at': [8, 1, 0], **W('PHILIPPINES', 'फिलीपींस')},
 {'kind': 'circle', 'scene': 'IT', 'at': [9, 0, 0], 'c': [16.2, 39.6], 'r': [120, 150], 'col': '#FF3B30', 'until': [9, 1, -.05], **W('BOOT', 'जूते')},
 {'kind': 'circle', 'scene': 'IT', 'at': [9, 1, 0], 'c': [31.0, 52.0], 'r': [230, 420], 'col': '#FF3B30', 'until': [10, 0, -.1], **W('SITTING', 'बैठे')},
 {'kind': 'slam', 'what': 'land', 'at': [10, 0, .45], **W('TOGETHER', 'जोड़')},
 {'kind': 'flashfx', 'at': [10, 0, .45], **W('TOGETHER', 'जोड़')},
 {'kind': 'punch', 'scene': 'IT', 'at': [10, 1, 0], 'level': 1.14, 'back': [10, 1, 1.2], **W('BODY', 'इंसान')},
 {'kind': 'card', 'scene': 'IT', 'at': [10, 1, .3], 'until': [11, 0, -.3], 'side': 'L', 'flag': '🇮🇹', 'name': 'ITALY', 'to': 301340, 'y': 1560, 'lon': 12.8, 'lat': 43.0},
 {'kind': 'card', 'scene': 'IT', 'at': [10, 1, .45], 'until': [11, 0, -.3], 'side': 'R', 'flag': '🇵🇭', 'name': 'PHILIPPINES', 'to': 300000, 'y': 1560, 'lon': 14.0, 'lat': 56.0},
 {'kind': 'slam', 'what': 'rank', 'n': 1, 'at': [11, 0, 0], **W('ONE', 'वन'), 'until': [11, 1, .5], 'off': [14, 0, -.1]},
 {'kind': 'arrow', 'scene': 'SEA', 'at': [12, 1, 0], 'from': [109.6, 11.6], 'to': [107.4, 19.8], 'col': '#FFC23A', 'until': [12, 2, -.05]},
 {'kind': 'arrow', 'scene': 'SEA', 'at': [12, 1, .15], 'from': [110.2, 1.2], 'to': [117.8, 7.2], 'col': '#FFC23A', 'until': [12, 2, -.05]},
 {'kind': 'card', 'scene': 'SEA', 'at': [12, 2, 0], 'until': [13, 0, -.4], 'side': 'L', 'flag': '🇲🇾', 'name': 'MALAYSIA', 'to': 329847, 'y': 1560, 'lon': 102.3, 'lat': 4.2},
 {'kind': 'card', 'scene': 'SEA', 'at': [12, 2, .15], 'until': [13, 0, -.4], 'side': 'R', 'flag': '🇻🇳', 'name': 'VIETNAM', 'to': 331210, 'y': 1560, 'lon': 106.4, 'lat': 15.5},
 {'kind': 'punch', 'scene': 'SEA', 'at': [13, 0, .2], 'level': 1.12, 'back': [13, 0, 1.4]},
 {'kind': 'moment', 'what': 'heart pops', 'at': [13, 0, .6]},
 {'kind': 'moment', 'what': 'pull back to the globe (loop)', 'at': [14, 0, .05]},
 {'kind': 'slam', 'what': 'lpop', 'at': [2, 1, .35]},
 {'kind': 'slam', 'what': 'lpop', 'at': [2, 1 if HI else 2, 0], **W('EVEREST', 'एवरेस्ट')},
 {'kind': 'slam', 'what': 'lpop', 'at': [9, 1, 0], **W('SITTING', 'बैठे')},
 {'kind': 'slam', 'what': 'jolt', 'at': [5, 0, 0]},
 {'kind': 'slam', 'what': 'lpop', 'at': [8, 1, .5], **W('PHILIPPINES', 'फिलीपींस')},
 {'kind': 'slam', 'what': 'lpop', 'at': [9, 0, .1], **W('BOOT', 'जूते')},
 {'kind': 'slam', 'what': 'lpop', 'at': [11, 1, 0], **W('VIETNAM', 'वियतनाम')},
 {'kind': 'slam', 'what': 'lpop', 'at': [12, 0, 0], **W('SOUTHEAST', 'साउथईस्ट')},
 {'kind': 'slam', 'what': 'lpop', 'at': [13, 0, .6]},
 {'kind': 'slam', 'what': 'lpop', 'at': [14, 0, .05]},
]
S['beats'] = B
L = lambda sc, txt, lon, lat, at, until, fs=62, col='#FFFFFF', **k: dict(scene=sc, txt=txt, lon=lon, lat=lat, at=at, until=until, fs=fs, col=col, **k)
S['labels'] = [
 L('SA', '🇳🇵 NEPAL', 84.2, 28.6, [1, 1, 0], [2, 0, -.2], word=('नेपाल' if HI else 'NEPAL')),
 L('SA', '🇧🇩 BANGLADESH', 90.2, 23.4, [1, 1, 0], [2, 0, -.2], word=('बांग्लादेश' if HI else 'BANGLADESH')),
 L('SA', 'EVEREST', 86.93, 28.25, [2, 1 if HI else 2, 0], [2, 3, -.2], fs=84, col='#FFC23A', word=('एवरेस्ट' if HI else 'EVEREST')),
 L('WA', '🇬🇳 GUINEA', -13.3, 11.7, [3, 1, 0], [4, 2, 0], word=('गिनी' if HI else 'GUINEA')),
 L('WA', '🇬🇧 UK', -10.0, 12.2, [3, 1, .7], [4, 2, 0], ov='WA.uk', word=('यूनाइटेड' if HI else 'UNITED')),
 L('WA', '👑', -10.4, 13.2, [4, 1, 0], [5, 0, -.3], fs=150, ov='WA.uk', word=('सबसे' if HI else 'BIGGEST'), fall=[4, 3, 0], fallword=('गिनी' if HI else 'GUINEA')),
 L('ZC', '🇨🇱 CHILE', 12.6, 4.0, [6, 1, .3], [7, 3, -.1], ov='ZC.cl', word=('चिली' if HI else 'CHILE')),
 L('ZC', '🇿🇲 ZAMBIA', 27.8, -10.4, [6, 1, 0], [7, 0, .2], word=('ज़ाम्बिया' if HI else 'ZAMBIA')),
 L('IT', '🇮🇹 ITALY', 12.4, 44.2, [8, 1, 0], [9, 0, -.05], word=('इटली' if HI else 'ITALY')),
 L('IT', '🇵🇭 PHILIPPINES', 31.0, 43.6, [8, 1, .5], [9, 1, -.05], fs=56, word=('फिलीपींस' if HI else 'PHILIPPINES')),
 L('IT', '👢', 18.6, 38.2, [9, 0, .1], [10, 0, -.1], fs=120, word=('जूते' if HI else 'BOOT')),
 L('IT', '🧍', 22.5, 52.0, [10, 1, .1], [11, 0, -.3], fs=170, word=('इंसान' if HI else 'BODY')),
 L('SEA', '🇲🇾 MALAYSIA', 101.4, 8.4, [11, 1, 0], [12, 2, -.1], word=('मलेशिया' if HI else 'MALAYSIA')),
 L('SEA', '🇻🇳 VIETNAM', 105.2, 16.8, [11, 1, 0], [12, 2, -.1], word=('वियतनाम' if HI else 'VIETNAM')),
 L('SEA', 'SOUTHEAST ASIA', 112.0, 15.0, [12, 0, 0], [12, 1, .3], fs=58, col='#FFC23A', word=('साउथईस्ट' if HI else 'SOUTHEAST')),
]
S['impacts'] = []
S['music_sections'] = {'pad': [[[0, 0, -.5], 'end', .9]], 'arp': [[[0, 0, 0], [11, 0, -.2], .7], [[11, 0, 0], 'end', 1]],
                       'drums': [[[1, 0, 0], [5, 0, -.2], .6], [[6, 0, 0], [13, 0, -.2], .65]], 'bass': [[[1, 0, 0], 'end', .8]]}
S['hand'] = []
json.dump(S, open(out, 'w'), ensure_ascii=False, indent=1); print('plan ->', out, len(S['shots']), 'shots', len(B), 'beats', len(S['labels']), 'labels')
