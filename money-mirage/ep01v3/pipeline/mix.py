# Money Mirage ep01 v3 mix: voice + YouTube Audio Library music (per chapter, ducked) + REAL recorded SFX locked to the
# shot plan (motion_plan.sfx gives the cue list; each synth cue name is mapped to a recorded file, takes rotated).
# Usage: python3 mix.py [--fx-only]   -> audio/mix.wav (or audio/fx_stem.wav)
import json, os, sys, subprocess
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); SR = 48000
sys.path.insert(0, '/home/claude/media-engine/bhugol-v2/motion'); import motion_plan
T = json.load(open(os.path.join(HERE, 'proj/times.json'))); TIM = json.load(open(os.path.join(HERE, 'audio/timing.json')))
SPEC = json.load(open(os.path.join(HERE, 'spec.json'))); DUR = T['dur']; N = int(DUR * SR) + SR
FXONLY = '--fx-only' in sys.argv
BUN = '/root/.claude/skills/media-use/audio/assets/sfx/'; OV = '/home/claude/mm-work/v2/assets/sfx/'
def load(p, sr=SR):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', p, '-f', 'f32le', '-ac', '1', '-ar', str(sr), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)
CACHE = {}
def S(path, rate=1.0):
    k = (path, rate)
    if k not in CACHE:
        x = load(path, int(SR * rate)) if rate != 1 else load(path); pk = np.abs(x).max() or 1; CACHE[k] = x / pk
    return CACHE[k]
# synth cue name -> recorded takes (rotated so no two neighbours repeat)
MAP = {'whoosh': [BUN + 'whoosh-short.mp3', BUN + 'whoosh.mp3'], 'whoosh_down': [BUN + 'whoosh.mp3'], 'pop': [BUN + 'pop.mp3', BUN + 'click-soft.mp3'],
       'thud': [OV + 'thump.mp3', OV + 'thud.mp3'], 'slide': [BUN + 'whoosh-short.mp3'], 'shot': [BUN + 'impact-bass-2.mp3'], 'boom': [BUN + 'impact-bass-1.mp3'],
       'crack': [OV + 'paper_crumple.mp3'], 'riser': [BUN + 'riser.mp3'], 'ticks': [OV + 'clock.mp3']}
fx = np.zeros(N); rot = {}
def place(x, t, gain, peak_align=False):
    st = int(round(t * SR)) - (int(np.argmax(np.abs(x))) if peak_align else int(np.argmax(np.abs(x) > .25)) - int(.006 * SR)); s0 = max(0, st); x = x[s0 - st:]; n = min(len(x), N - s0)   # attack lands on the beat
    if n > 0: fx[s0:s0 + n] += x[:n] * gain
P = [{'scene': s['id'], 't': s['t'], 'cut': s['cut']} for s in T['shots']]
B = [b for b in T['beats'] if b['kind'] in ('slam', 'count', 'punch', 'charslam', 'grow', 'flap', 'circle', 'arrow')]
cues = motion_plan.sfx(P, [{'kind': b['kind'], 't': b['t']} for b in B])
# auto punch-ins (gap fillers) get only a soft whoosh, not the full punch kit
auto = {round(b['t'], 3) for b in T['beats'] if b.get('auto')}
for c in cues:
    name, t, vol = c[0], c[1], c[2]
    if any(abs(t - a) < .13 for a in auto) and name in ('thud', 'pop'): continue
    takes = MAP.get(name);
    if not takes: continue
    i = rot.get(name, 0); rot[name] = i + 1; path = takes[i % len(takes)]; rate = (1.0, 1.06, .95)[i % 3]
    if name == 'riser':  # end-aligned: peaks at the cut
        x = S(path); end = c[3] if len(c) > 3 else t + 1.6; place(x[-int((end - t) * SR):] if (end - t) * SR < len(x) else x, t, vol * .5); continue
    if name == 'ticks':
        x = S(path)[:int(1.3 * SR)]; place(x, t, vol * .5); continue
    place(S(path, rate), t, vol * (.55 if name in ('whoosh', 'slide', 'whoosh_down') else .7), peak_align=name in ('thud', 'shot', 'boom'))
# zoom cuts carry only soft whooshes/risers: give each a short click on the cut so the cut has an attack
for p in P[1:]:
    if p['cut'] in ('zoom', 'zoomIn'): place(S(BUN + 'click-soft.mp3'), p['t'], .5)
# story sounds from the spec (chicken, goat, stamp, coins, clock ...)
for b in T['beats']:
    if b['kind'] == 'sfx': place(S(OV + b['name'] + '.mp3'), b['t'], b.get('vol', 1) * .6)
# hero moments: bundled cinematic layer (peak-aligned), as sfxlayer.py does
for p in P[1:]:
    if p['cut'] == 'flash': place(S(BUN + 'whoosh-cinematic.mp3'), p['t'] + .05, .45, True); place(S(BUN + 'impact-bass-2.mp3'), p['t'] + .3, .45, True)
cs = [b for b in T['beats'] if b['kind'] == 'charslam']
for b in cs: place(S(BUN + 'impact-bass-1.mp3'), b['t'] + .3, .45, True)
fx *= .5
if FXONLY:
    sf.write(os.path.join(HERE, 'audio/fx_stem.wav'), np.stack([fx, fx], 1), SR); print('fx stem'); sys.exit()
# voice (align.py timings include its 0.3 s lead-in offset)
v, vsr = sf.read(os.path.join(HERE, 'audio/voice.wav'), always_2d=True); v = v.mean(1)
if vsr != SR: v = load(os.path.join(HERE, 'audio/voice.wav'))
off = TIM.get('offset', .3); voice = np.zeros(N); s0 = int(off * SR); voice[s0:s0 + len(v)] = v[:N - s0]
# music: one YouTube Audio Library track per chapter, 1.5 s crossfades, bed under the voice, ducked
TRACKS = ['1_keys', '2_never', '3_something', '4_standoff', '5_rapid', '6_system', '5b_shadows', '7_fact']   # cold open, ch1..ch7
OFFS = {'2_never': 7.7}
chs = sorted({L['ch'] for L in SPEC['lines']}); starts = []
for c in chs: li = next(i for i, L in enumerate(SPEC['lines']) if L['ch'] == c); starts.append(max(0, TIM['lines'][li]['start'] - 1.2))
starts[0] = 0.0; bounds = starts[1:] + [DUR]
music = np.zeros(N)
for k, (a, b) in enumerate(zip(starts, bounds)):
    tr = load(f'/home/claude/mm-work/engine/build/music/{TRACKS[k]}.mp3'); o = int(OFFS.get(TRACKS[k], 0) * SR); tr = tr[o:]
    L = int((b - a + 1.5) * SR)
    while len(tr) < L: tr = np.concatenate([tr, tr])
    tr = tr[:L]; rms = np.sqrt((tr ** 2).mean()) or 1; tr = tr / rms * .065
    fi, fo = int(.8 * SR), int(1.5 * SR); tr[:fi] *= np.linspace(0, 1, fi); tr[-fo:] *= np.linspace(1, 0, fo)
    s = int(a * SR); n = min(len(tr), N - s); music[s:s + n] += tr[:n]
# duck under speech (envelope follower on the voice), 0.32 -> 1.0 gain with smooth attack/release
hop = SR // 100; e = np.sqrt(np.convolve(voice ** 2, np.ones(hop) / hop, 'same'))[::hop]
act = (e > .01).astype(float); sm = np.zeros_like(act); g = 0
for i, a in enumerate(act): g = g + (a - g) * (.25 if a > g else .04); sm[i] = g
duck = np.interp(np.arange(N) / SR, np.arange(len(sm)) * hop / SR, 1 - .62 * sm)
mix = voice * 1.0 + music * duck * 2.2 + fx
pk = np.abs(mix).max(); mix = mix / pk * .89 if pk > .89 else mix
sf.write(os.path.join(HERE, 'audio/mix.wav'), np.stack([mix, mix], 1), SR); print('mix', round(len(mix) / SR, 1), 's; peak', round(pk, 3), '; fx cues', len(cues))
