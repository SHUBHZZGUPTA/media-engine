# Music + story SFX in real seconds, the shot-plan sound (motion_plan.sfx), unwarp fix, then score.py + bundled SFX layer.
# Usage: python3 mkscore_bp.py <spec.json> <out_dir> [--fx-only]   (reads <out_dir>/voice.wav + timing.json)
import json, sys, subprocess, shutil
spec_p, od = sys.argv[1:3]; FXONLY = '--fx-only' in sys.argv
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
# light, voice-first bed: pad windows at act changes; a soft drone under the underground scenes; drums only mid-story
S['music'] = {'bpm': 92, 'level': 0 if FXONLY else .28,
  'chords': [[57, 60, 64, 69], [53, 57, 60, 65], [55, 59, 62, 67], [52, 56, 59, 64]], 'roots': [45, 41, 43, 40],
  'sections': {'pad': [[0, C(1, 0), 1], [C(6, 0, -.3), C(7, 1), .9], [C(12, 0, -.3), C(13, 1), 1.2], [ES - .4, 'end', 1]],
               'drone': [[C(7, 0), C(11, 0, -.2), .8], [C(14, 0), ES, .7]],
               'drums': [[C(1, 0), C(6, 0, -.2), .7], [C(11, 0), C(12, 2, -.2), .6]],
               'bass': [[C(1, 0), C(6, 0, -.2), .7], [C(11, 0), ES, .7]], 'arp': [[ES - .2, 'end', 1]],
               'muffle': [[C(8, 0), C(10, 3), .6]]}}
fx = [['rumble_dur', .05, .6, 1.6]]
sys.path.insert(0, '/home/claude/media-engine/bhugol-v2/motion'); import motion_plan
P = motion_plan.plan(S, C); BEATS = [{'kind': b['kind'], 't': C(*b['at'])} for b in S.get('beats', [])]
fx += motion_plan.sfx(P, BEATS)
fx += [['stream', C(0, 0, .2), .1, C(0, 2)],                          # the river drawing across Europe
       ['sparkles', C(0, 1, .05), .25, 8, .17],                          # capital dots
       ['stream', C(1, 2), .1, C(2, 0, -.2)],                            # flying with the river
       ['boing', C(3, 1, .9), .3, 260, .4],                              # commute joke
       ['sparkles', C(5, 1, .05), .25, 8, .17],
       ['slide', C(6, 3, -.05), .35, 1200, 300, .7],                      # disappear?
       ['gloop', C(8, 1, .05), .45], ['stream', C(8, 0, .2), .1, C(8, 3)],  # leaking into the ground
       ['plink', C(10, 1, .1), .35, 1900, .3], ['stream', C(10, 2), .1, C(11, 0, -.2)],  # dye poured, conduit
       ['plink', C(11, 2, .1), .4, 2200, .3],                            # spring
       ['stream', C(12, 0, .1), .1, C(12, 2)],                           # the Rhine
       ['riser', C(14, 1, -.1), .3, C(14, 3, .3)], ['plink', C(14, 4, .05), .4, 2400, .3],
       ['chime', ES, .6, [523.25, 659.25, 783.99], 1.6, .5], ['pop', ES + .8, .6, 900], ['plink', ES + 2.0, .6, 1800, .5]]
S['fx'] = fx
motion_plan.unwarp(S, TIM)
out = spec_p.replace('.json', '.scored.json' if not FXONLY else '.fxonly.json'); json.dump(S, open(out, 'w'), ensure_ascii=False, indent=1)
voice = od + '/voice.wav'
if FXONLY:   # silent voice for the sound-on-beat stem
    import soundfile as sf, numpy as np; x, sr = sf.read(voice); sf.write(od + '/voice_silent.wav', np.zeros_like(x), sr); voice = od + '/voice_silent.wav'
subprocess.run(['python3', '/home/claude/bhugol-kit/tools/score.py', out, voice, od + '/timing.json', od], check=True)
cues = []
for b in S.get('beats', []):
    if b['kind'] == 'charslam': cues.append({'file': 'impact-bass-1.mp3', 't': C(*b['at']) + .3, 'gain_db': -10, 'what': 'hook title lands'})
for p in P[1:]:
    if p['cut'] in ('burn', 'flash'): cues += [{'file': 'whoosh-cinematic.mp3', 't': p['t'] + .05, 'gain_db': -9, 'what': 'hero cut'}, {'file': 'impact-bass-2.mp3', 't': p['t'] + .3, 'gain_db': -12, 'what': 'hero landing'}]
json.dump(cues, open(od + '/sfx_cues.json', 'w'), indent=1)
sfx_out = od + ('/fx_stem.wav' if FXONLY else '/mix_final.wav')
subprocess.run(['python3', '/home/claude/media-engine/bhugol-v2/motion/sfxlayer.py', od + '/mix_norm.wav', sfx_out, od + '/sfx_stem.wav', od + '/sfx_cues.json'], check=True)
if FXONLY: shutil.copy(od + '/mix_norm.wav', od + '/fx_mix_norm.wav')
