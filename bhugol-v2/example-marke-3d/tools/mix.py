# Märket mix: voice + Kevin MacLeod "Carefree" bed (ducked, wrapped across the loop seam) + SFX locked to the shot plan.
# Usage: python3 mix.py <build_dir> <audio_dir> [--fx-only]   -> audio_dir/mix_final.wav (or fx_stem.wav)
import json, os, sys, subprocess
import numpy as np, soundfile as sf
sys.path.insert(0, '/home/claude/media-engine/bhugol-v2/motion'); import motion_plan
SR = 48000
BD, AD = [a for a in sys.argv[1:] if not a.startswith('--')][:2]; FXONLY = '--fx-only' in sys.argv
T = json.load(open(os.path.join(BD, 'times.json'))); TIM = json.load(open(os.path.join(AD, 'timing.json')))
DUR = T['dur']; N = int(round(DUR * SR))
SFX = '/home/claude/media-engine/money-mirage/mm3/library/sfx/'
def load(p):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', p, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)
CACHE = {}
def S(name):
    if name not in CACHE: x = load(SFX + name); CACHE[name] = x / (np.abs(x).max() or 1)
    return CACHE[name]
fx = np.zeros(N)
def place(x, t, gain, peak=False):
    st = int(round(t * SR)) - (int(np.argmax(np.abs(x))) if peak else max(0, int(np.argmax(np.abs(x) > .25)) - int(.006 * SR)))
    s0 = max(0, st); x = x[s0 - st:]; n = min(len(x), N - s0)
    if n > 0: fx[s0:s0 + n] += x[:n] * gain
MAP = {'whoosh': 'whoosh-short.mp3', 'whoosh_down': 'whoosh.mp3', 'pop': 'pop.mp3', 'thud': 'thump.mp3', 'slide': 'whoosh-short.mp3', 'shot': 'impact-bass-2.mp3',
       'boom': 'impact-bass-1.mp3', 'riser': 'riser.mp3', 'ticks': 'clock.mp3'}
P = [{'t': s['t'], 'cut': s['cut']} for s in T['shots']]
B = [b for b in T['beats'] if b['kind'] in ('slam', 'count', 'punch', 'charslam', 'card', 'grow', 'flap', 'circle', 'arrow')]
cues = motion_plan.sfx(P, [{'kind': b['kind'], 't': b['t']} for b in B])
for c in cues:
    name, t, vol = c[0], c[1], c[2]; f = MAP.get(name)
    if not f or t > DUR - .45: continue          # nothing lands on the seam
    if name == 'riser': x = S(f); end = c[3] if len(c) > 3 else t + 1.6; L = int((end - t) * SR); place(x[-L:] if L < len(x) else x, t, vol * .45); continue
    if name == 'ticks': place(S(f)[:int(1.1 * SR)], t, vol * .4); continue
    if name == 'pop' and len(c) > 4 and c[4] <= .05: place(S('click-soft.mp3'), t, vol * 1.6); continue   # quiet on-beat click
    place(S(f), t, vol * (.5 if name in ('whoosh', 'slide', 'whoosh_down') else .6), peak=name in ('thud', 'shot', 'boom'))
for p in P[1:]:
    if p['cut'] == 'flash': place(S('whoosh-cinematic.mp3'), p['t'] + .05, .28, True); place(S('impact-bass-2.mp3'), p['t'] + .3, .3, True)
for b in T['beats']:
    if b['kind'] == 'charslam': place(S('impact-bass-1.mp3'), b['t'] + .3, .28, True)
for name, t, vol in T.get('story', []): place(S(name), t, vol * .6)
fx *= .5
if FXONLY:
    sf.write(os.path.join(AD, 'fx_stem.wav'), np.stack([fx, fx], 1), SR); print('fx stem'); sys.exit()
v = load(os.path.join(AD, 'voice.wav')); off = TIM.get('offset', .3); voice = np.zeros(N); s0 = int(off * SR); n = min(len(v), N - s0); voice[s0:s0 + n] = v[:n]
voice *= .5 / (np.abs(voice).max() or 1) * 1.4
# music bed: track[o : o+DUR]; the last L s crossfade into track[o-L : o] so the end flows straight into frame 0
trk = load('/home/claude/work/marke/music/carefree.mp3'); o = int(4.0 * SR); L = int(.6 * SR)
bed = trk[o:o + N].copy(); pre = trk[o - L:o]; w = np.linspace(0, np.pi / 2, L)
bed[-L:] = bed[-L:] * np.cos(w) + pre * np.sin(w)
bed = bed / (np.sqrt((bed ** 2).mean()) or 1) * .045
hop = SR // 100; e = np.sqrt(np.convolve(voice ** 2, np.ones(hop) / hop, 'same'))[::hop]
act = (e > .01).astype(float); sm = np.zeros_like(act); g = 0
for i, x in enumerate(np.concatenate([act[-150:], act])):   # warm up on the tail so the duck matches across the seam
    g = g + (x - g) * (.3 if x > g else .012)
    if i >= 150: sm[i - 150] = g
duck = np.interp(np.arange(N) / SR, np.arange(len(sm)) * hop / SR, 1 - .6 * sm)
mix = voice + bed * duck + fx * .8
pk = np.abs(mix).max(); mix = mix / pk * .89 if pk > .89 else mix
sf.write(os.path.join(AD, 'mix_raw.wav'), np.stack([mix, mix], 1), SR)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', os.path.join(AD, 'mix_raw.wav'), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', os.path.join(AD, 'mix_final.wav')], check=True)
y, _ = sf.read(os.path.join(AD, 'mix_final.wav')); y = y.mean(1); q = int(.5 * SR)
r = lambda a: 20 * np.log10(np.sqrt((a ** 2).mean()) + 1e-9)
print('mix', round(len(y) / SR, 2), 's; cues', len(cues), '| seam RMS last/first 0.5 s:', round(r(y[-q:]), 1), round(r(y[:q]), 1))
