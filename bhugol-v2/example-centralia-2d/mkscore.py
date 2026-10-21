# Adds nominal timings (o = aligned starts), music sections and sound effects in real seconds, then runs score.py.
# Usage: python3 mkscore.py <spec.json> <out_dir>   (reads <out_dir>/voice.wav + timing.json)
import json, sys, subprocess
spec_p, od = sys.argv[1:3]
S = json.load(open(spec_p)); TIM = json.load(open(od + '/timing.json'))
for L, T in zip(S['lines'], TIM['lines']): L['o'] = T['start']
DUR = round((TIM['lines'][-1]['end'] + S.get('tail', 2.3)) * 30) / 30
S['old_end'] = DUR
Cd = {}
for li, L in enumerate(S['lines']):
    w0 = 0; ws = TIM['lines'][li]['words']
    for ci, c in enumerate(L['chunks']):
        Cd[(li, ci)] = ws[min(w0, len(ws) - 1)] - .06; w0 += len(c.replace('|', ' ').split(' '))
C = lambda li, ci=0, off=0.0: round(Cd[(li, ci)] + off, 3)
ES = round(TIM['lines'][-1]['start'] - .25, 3)
shots = [C(1, 0, -.15), C(2, 0, -.15), C(3, 0, -.15), C(7, 0, -.15), C(9, 0, -.15), C(11, 0, -.15), C(15, 0, -.15)]
S['music'] = {'bpm': 78, 'level': .3,
  'chords': [[57, 60, 64, 69], [53, 57, 60, 65], [52, 56, 59, 64], [57, 60, 63, 69]], 'roots': [45, 41, 40, 45],
  'sections': {'pad': [[0, C(0, 1), 1], [C(3, 0, -.5), C(3, 1, .5), .8], [C(6, 0), C(7, 0, .5), 1], [C(13, 0, -.3), C(14, 0, .8), 1.2], [ES - .4, 'end', 1]],
               'drone': [[0, C(9, 0, -.2), .9], [C(11, 0), 'end', .9]], 'drums': [[C(7, 0), C(9, 0, -.3), .7], [C(11, 0), C(13, 0, -.2), .8]],
               'bass': [[C(3, 0), C(9, 0, -.3), .8], [C(11, 0), C(13, 1), .9], [C(15, 0), ES, .7]], 'arp': [[ES - .2, 'end', 1]],
               'muffle': [[C(9, 0, -.2), C(11, 0, -.2), 1]]}}
fx = [['rumble_dur', .05, .9, 2.2], ['crack', C(0, 1, .1), .8]]
import sys as _s; _s.path.insert(0, '/home/claude/media-engine/bhugol-v2/motion'); import motion_plan
CC = lambda li, ci=0, off=0.0: C(li, ci, off)
P = motion_plan.plan(S, CC); BEATS = [{'kind': b['kind'], 't': CC(*b['at'])} for b in S.get('beats', [])]
fx += motion_plan.sfx(P, BEATS)   # whooshes / impacts / risers locked to the shot plan's cuts, slams and count-ups
fx += [['pop', C(1, 1, .5), .6, 900], ['pop', C(1, 1, .6), .5, 700],
       ['crack', C(3, 1, .05), .8], ['rumble', C(3, 1, .05), .6, C(3, 1, 1.4)], ['pop', C(3, 0, .7), .5, 760],
       ['pop', C(4, 0, -.35), .6, 600], ['slide', C(4, 1), .5, 500, 1400, .4],
       ['thud', C(5, 0, .3), .7], ['thud', C(5, 0, .6), .7], ['gloop', C(5, 1, .05), .7], ['pop', C(5, 2), .6, 900],
       ['slide', C(5, 3, .35), .6, 1500, 380, .7], ['crack', C(5, 4, .1), .9], ['rumble', C(5, 4, .1), .7, C(5, 4, 1.6)],
       ['riser', C(6, 0), .5, C(7, 0, -.1)], ['pop', C(7, 1, .05), .5, 700],
       ['riser', C(7, 2, -.2), .6, C(7, 2, .6)], ['pop', C(7, 2, .5), .7, 1000], ['boing', C(8, 1), .6, 170, .6],
       ['pop', C(9, 0), .5, 760], ['whoosh_down', C(9, 2, -.05), .5, .8, 2400, 300],
       ['plink', C(10, 1, .1), .5, 2600, .3], ['plink', C(10, 1, .38), .5, 2900, .3], ['plink', C(10, 1, .72), .5, 2400, .3],
       ['riser', C(11, 2, -.1), .6, C(11, 2, .9)], ['boom', C(11, 2, .8), .7, 1.4, 48], ['pop', C(12, 0, .1), .5, 700],
       ['slide', C(12, 1, -.1), .6, 1400, 420, .5], ['scratch', C(12, 2, .25), .6, .45],
       ['shot', C(13, 1, .25), 1.0], ['sparkles', C(14, 0, .3), .35, 12, .17], ['pop', C(14, 2), .6, 820], ['thud', C(14, 2, .1), .6],
       ['boom', C(16, 2, .1), .7, 1.6, 44], ['pop', C(16, 2), .6, 900], ['pop', C(17, 0, -.35), .6, 600],
       ['chime', ES, .6, [523.25, 659.25, 783.99], 1.6, .5], ['pop', ES + .8, .6, 900], ['plink', ES + 2.0, .6, 1800, .5]]
S['fx'] = fx
motion_plan.unwarp(S, TIM)   # score.py re-maps times through W(); our times are already real seconds (bug fixed 22 Oct)
out = spec_p.replace('.json', '.scored.json'); json.dump(S, open(out, 'w'), ensure_ascii=False, indent=1)
subprocess.run(['python3', '/home/claude/bhugol-kit/tools/score.py', out, od + '/voice.wav', od + '/timing.json', od], check=True)
cues = [{'file': 'impact-bass-1.mp3', 't': CC(*b['at']) + .3, 'gain_db': -10, 'what': 'hook title lands'} for b in S.get('beats', []) if b['kind'] == 'charslam']
for p in P[1:]:
    if p['cut'] in ('burn', 'flash'): cues += [{'file': 'whoosh-cinematic.mp3', 't': p['t'] + .05, 'gain_db': -9, 'what': 'hero cut'}, {'file': 'impact-bass-2.mp3', 't': p['t'] + .3, 'gain_db': -12, 'what': 'hero landing'}]
json.dump(cues, open(od + '/sfx_cues.json', 'w'), indent=1)
subprocess.run(['python3', '/home/claude/media-engine/bhugol-v2/motion/sfxlayer.py', od + '/mix_norm.wav', od + '/mix_final.wav', od + '/sfx_stem.wav', od + '/sfx_cues.json'], check=True)
