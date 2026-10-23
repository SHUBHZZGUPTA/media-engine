# Pick review frames per segment: every circle/arrow/moment/number beat (+0.9 s) and every shot start (+0.6 s), max 16 per segment.
import json, sys
T = json.load(open('proj/times.json'))   # run from the episode folder
kinds = set(sys.argv[1].split(',')) if len(sys.argv) > 1 else {'circle', 'arrow', 'moment', 'slam', 'grow', 'count', 'flap', 'charslam'}
for i, (a, b) in enumerate(T['segs']):
    ts = sorted({round(x['t'] + .9, 2) for x in T['beats'] if x['kind'] in kinds and a + .2 <= x['t'] + .9 < b - .05})
    if len(ts) > 16: ts = ts[::max(1, len(ts) // 16 + 1)]
    print(i, ','.join(map(str, ts)))
