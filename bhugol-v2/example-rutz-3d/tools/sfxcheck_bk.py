# SFX-on-beat check against the build's own times.json (beats already in real seconds, word-timed).
import json, sys
A = json.load(open(sys.argv[1])); ts = [e['t'] for e in A['items'][0]['onsets']['events'] if e['strength'] > .15]
T = json.load(open(sys.argv[2])); END = T['end']
ev = [('cut:' + s['cut'], s['t']) for s in T['shots'][1:]] + [(b['kind'], b['t'] + (.3 if b['kind'] == 'charslam' else 0)) for b in T['beats'] if b['kind'] not in ('impact', 'moment', 'flashfx')]
ev = [e for e in ev if e[1] < END]
miss = [(k, round(t, 2), round(min(abs(t - x) for x in ts), 3)) for k, t in ev if min(abs(t - x) for x in ts) > .1]
print(f'sound-on-beat: {len(ev) - len(miss)}/{len(ev)} within 100 ms'); [print('  miss', m) for m in miss]
