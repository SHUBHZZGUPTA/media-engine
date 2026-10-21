"""SFX-on-beat QA: every cut and visual beat in the spec must have a sound-effect onset within 100 ms.
1) Render an FX-only stem: run your mkscore with music 'level' 0 and a silent voice.wav (same length), then sfxlayer.py on it.
2) npx hyperframes audio <fx_stem.wav> --quality fast --json --only onsets > onsets.json
3) python3 sfx_check.py onsets.json <spec.json> <build>/times.json [end_s]
Soft sounds (long whooshes, risers) have no sharp onset; give each cut a short pop/crack at the cut time (motion_plan.sfx does)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import motion_plan
A = json.load(open(sys.argv[1])); ts = [e['t'] for e in A['items'][0]['onsets']['events'] if e['strength'] > .15]
S = json.load(open(sys.argv[2])); C = json.load(open(sys.argv[3]))['C']; END = float(sys.argv[4]) if len(sys.argv) > 4 else 1e9
Cf = lambda li, ci=0, off=0: C[f'{li}.{ci}'] + off
P = motion_plan.plan(S, Cf)
ev = [('cut:' + p['cut'], p['t']) for p in P[1:] if p['t'] < END] + [(b['kind'], Cf(*b['at']) + (.3 if b['kind'] == 'charslam' else 0)) for b in S.get('beats', []) if Cf(*b['at']) < END and b['kind'] != 'impact']
hit = 0
for k, t in sorted(ev, key=lambda x: x[1]):
    d = min((abs(o - t) for o in ts), default=9); ok = d <= .1; hit += ok
    if not ok: print(f'  MISS {k:12s} {t:6.2f}  nearest onset {d * 1000:.0f} ms')
print(f'  {"PASS " if hit == len(ev) else "CHECK"}  sfx on beat: {hit}/{len(ev)} events have a sound effect within 100 ms')
