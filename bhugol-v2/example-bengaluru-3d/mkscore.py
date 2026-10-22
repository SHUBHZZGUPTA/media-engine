# Bengaluru lakes: nominal timings (o = aligned starts), music sections + story SFX in real seconds, then score.py.
# Usage: python3 mkscore.py <spec.json> <out_dir> [--fx-only]   (reads <out_dir>/voice.wav + timing.json; writes mix_norm.wav, mix_final.wav)
import json, sys, subprocess
spec_p, od = [a for a in sys.argv[1:] if not a.startswith('--')][:2]; FXONLY = '--fx-only' in sys.argv
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
S['music'] = {'bpm': 84, 'level': 0 if FXONLY else .3,
  'chords': [[62, 66, 69, 74], [59, 62, 66, 71], [55, 59, 62, 67], [57, 61, 64, 69]], 'roots': [50, 47, 43, 45],
  'sections': {'pad': [[0, C(0, 2), 1], [C(2, 0), C(4, 0), .8], [C(6, 0), C(8, 0, .5), 1], [C(11, 0), C(12, 0), .9], [C(15, 0, -.3), C(16, 0, .8), 1.2], [ES - .4, 'end', 1]],
               'drone': [[C(12, 0), C(15, 0, -.2), .9]], 'drums': [[C(8, 0), C(10, 0, -.2), .7], [C(16, 0), C(21, 0, -.2), .8]],
               'bass': [[C(3, 0), C(6, 0, -.3), .8], [C(10, 0), C(12, 0), .8], [C(16, 0), ES, .7]], 'arp': [[C(8, 0), C(9, 0, .5), .8], [ES - .2, 'end', 1]],
               'muffle': [[C(15, 0, -.2), C(16, 0, -.2), 1]]}}
sys.path.insert(0, '/home/claude/media-engine/bhugol-v2/motion'); import motion_plan
P = motion_plan.plan(S, C); BEATS = [{'kind': b['kind'], 't': C(*b['at'])} for b in S.get('beats', [])]
fx = motion_plan.sfx(P, BEATS)   # whooshes / impacts / risers locked to the shot plan's cuts and beats
fx += [['stream_dur', .05, .14, 3.6],                                              # the lake at golden hour
       ['sparkles', C(3, 2, -.1), .3, 10, .14],                                     # 920 m card
       ['boing', C(4, 2, .1), .5, 170, .6],                                         # "Bengaluru IS the hill"
       ['rumble', C(6, 0, .25), .35, C(6, 0, 1.9)], ['stream', C(6, 0), .16, C(8, 0, -.2)],   # monsoon: thunder + rain
       ['gloop', C(8, 0, .3), .55], ['gloop', C(8, 1, .05), .55], ['gloop', C(8, 2, .05), .6], ['stream', C(8, 0, .2), .15, C(9, 0)],
       ['pop', C(9, 0, -.35), .6, 600], ['slide', C(9, 0, 0), .55, 1600, 500, .55],            # Drop slides in
       ['rumble', C(12, 0, .1), .35, C(13, 1)],                                     # the city grows
       ['stream', C(14, 0, .2), .15, C(15, 0, -.3)], ['riser', C(14, 2, -.1), .22, C(14, 2, 1.0)],   # pumped + lifted 300 m
       ['pop', C(17, 1, .2), .5, 820], ['pop', C(18, 1, .2), .5, 860], ['pop', C(19, 1, .2), .5, 900],
       ['pop', C(20, 0, -.35), .6, 600], ['horn', C(20, 0, -.3), .35, .6],          # the bus rolls in
       ['chime', ES, .6, [587.33, 739.99, 880.0], 1.6, .5], ['pop', ES + .8, .6, 900], ['plink', ES + 2.0, .6, 1800, .5]]
# (on-beat clicks and soft pen-swish marks now come from motion_plan.sfx itself)
S['fx'] = fx
motion_plan.unwarp(S, TIM)   # score.py re-maps times through W(); ours are real seconds already
out = spec_p.replace('.json', '.fxonly.json' if FXONLY else '.scored.json'); json.dump(S, open(out, 'w'), ensure_ascii=False, indent=1)
subprocess.run(['python3', '/home/claude/bhugol-kit/tools/score.py', out, od + '/voice.wav', od + '/timing.json', od], check=True)
cues = []
for b in S.get('beats', []):
    if b['kind'] == 'charslam': cues.append({'file': 'impact-bass-1.mp3', 't': C(*b['at']) + .3, 'gain_db': -10, 'what': 'hook title lands'})
for p in P[1:]:
    if p['cut'] in ('burn', 'flash'): cues += [{'file': 'whoosh-cinematic.mp3', 't': p['t'] + .05, 'gain_db': -9, 'what': 'hero cut'}, {'file': 'impact-bass-2.mp3', 't': p['t'] + .3, 'gain_db': -12, 'what': 'hero landing'}]
json.dump(cues, open(od + '/sfx_cues.json', 'w'), indent=1)
subprocess.run(['python3', '/home/claude/media-engine/bhugol-v2/motion/sfxlayer.py', od + '/mix_norm.wav', od + '/mix_final.wav', od + '/sfx_stem.wav', od + '/sfx_cues.json'], check=True)
