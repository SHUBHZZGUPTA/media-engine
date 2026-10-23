# every cut and visual beat needs a sound onset within 100 ms (BHUGOL v2 sfx_check, on this project's times.json)
import json, subprocess, os
MMENG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'engine'); EPD = os.getcwd(); os.chdir(MMENG)
env = dict(os.environ, HYPERFRAMES_NO_TELEMETRY='1', HYPERFRAMES_NO_UPDATE_CHECK='1', HYPERFRAMES_SKIP_SKILLS='1')
out = subprocess.run(['npx', 'hyperframes', 'audio', os.path.join(EPD, 'audio/fx_stem.wav'), '--quality', 'fast', '--json', '--only', 'onsets'], capture_output=True, text=True, env=env).stdout
open(os.path.join(EPD, 'audio/onsets.json'), 'w').write(out); A = json.loads(out)
ts = [e['t'] for e in A['items'][0]['onsets']['events'] if e['strength'] > .15]
T = json.load(open(os.path.join(EPD, 'proj/times.json'))); END = T['end_start']
ev = [('cut:' + s['cut'], s['t']) for s in T['shots'][1:] if s['t'] < END] + [(b['kind'], b['t'] + (.3 if b['kind'] == 'charslam' else 0)) for b in T['beats'] if b['kind'] in ('slam', 'count', 'punch', 'charslam', 'grow', 'flap', 'circle', 'arrow') and b['t'] < END]
hit = 0; miss = []
for k, t in sorted(ev, key=lambda x: x[1]):
    d = min((abs(o - t) for o in ts), default=9); ok = d <= .1; hit += ok
    if not ok: miss.append(f'  MISS {k:12s} {t:7.2f}  nearest onset {d * 1000:.0f} ms')
print('\n'.join(miss)); print(f'{"PASS" if hit == len(ev) else "CHECK"}  sfx on beat: {hit}/{len(ev)}')
