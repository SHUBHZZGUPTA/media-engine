"""Retention QA gate for a rendered BHUGOL Short (run on the silent render before finishing).
Usage: python3 retention_qa.py <video.mp4> [--end <end_card_start_s>] [--spec spec.json --timing timing_final.json]
Checks (thresholds from the HyperFrames motion doctrine + the kit's attention benchmark):
  - frozen stretches: no window > 2.0 s with near-zero motion (HyperFrames `motion_frozen`)
  - change cadence: a visual event at least every 2.7 s on average, longest gap <= 6 s (in-shot beats count)
  - moving share: >= 85% of 0.25 s steps moving
  - black frames: none (blackdetect)
  - plate missing: no stretch >= 0.5 s where the picture area (above the captions) is near-flat while captions still run;
    blackdetect misses this because captions, badge and particles keep the frame from being 'black' (Bengaluru, 22 Oct)
  - first second: motion within the first 0.5 s (the hook frame must already move)
  - transition grammar (with --spec/--timing): 1 primary cut type ~60-70%, 1-2 accents, <= 2 hero flashes, no shot > 12 s without a cut
Prints PASS/CHECK per item and an overall verdict. CHECK items are fixed before finishing unless deliberate (say why).
"""
import argparse, json, os, subprocess, sys
import numpy as np

ap = argparse.ArgumentParser(); ap.add_argument('video'); ap.add_argument('--end', type=float); ap.add_argument('--spec'); ap.add_argument('--timing')
a = ap.parse_args()
raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', a.video, '-vf', 'fps=4,scale=64:114,format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, 114, 64).astype(float); d = np.abs(np.diff(fr, axis=0)).mean((1, 2)); t = np.arange(len(d)) / 4 + .25
if a.end: keep = t < a.end; d, t = d[keep], t[keep]
res = []
def rep(name, ok, detail): res.append((name, ok)); print(f"  {'PASS ' if ok else 'CHECK'}  {name:<22} {detail}")
# frozen windows > 2 s
low = d < .6; runs = []; c = 0
for i, s in enumerate(low):
    if s: c += 1
    else:
        if c >= 8: runs.append((round(t[i - c], 1), c / 4))
        c = 0
rep('frozen > 2 s', not runs, 'none' if not runs else f'{runs[:5]}')
moving = 1 - low.mean(); rep('moving share', moving >= .85, f'{moving:.0%} (target >= 85%)')
# change events: local peaks in motion (cuts, slams, reveals)
rm = np.array([np.median(d[max(0, i - 8):i + 9]) for i in range(len(d))])   # +-2 s local baseline (steam/particles raise it)
ev = [t[i] for i in range(1, len(d) - 1) if d[i] > max(3.0, 1.8 * rm[i]) and d[i] >= d[i - 1] and d[i] >= d[i + 1]]
ev2 = [];
for e in ev:
    if not ev2 or e - ev2[-1] > .5: ev2.append(e)
gaps = np.diff([0] + ev2 + [t[-1]]) if len(t) else [0]
avg = (t[-1] / max(1, len(ev2))) if len(t) else 0
rep('change cadence', avg <= 2.7 and max(gaps) <= 6, f'one every {avg:.1f} s, longest gap {max(gaps):.1f} s ({len(ev2)} events)')
rep('hook frame moving', bool(len(d)) and d[:2].max() > .6, f'motion in first 0.5 s = {d[:2].max():.2f}' if len(d) else 'n/a')
# plate missing: picture region (rows above the caption band) almost flat for >= 0.5 s
pic = fr[1:, 10:75, :] if len(fr) > 1 else fr[:, 10:75, :]
flat = pic.std((1, 2)) < 6.0
if a.end: flat = flat[:len(t)]
runs2 = []; c = 0
for i, f in enumerate(list(flat) + [False]):
    if f: c += 1
    else:
        if c >= 2: runs2.append((round(float(t[i - c]), 2), round(c / 4, 2)))
        c = 0
rep('plate missing', not runs2, 'none' if not runs2 else f'flat picture area at {runs2[:6]} (start s, length s) - a scene did not draw')
bd = subprocess.run(['ffmpeg', '-hide_banner', '-i', a.video, '-vf', 'blackdetect=d=0.03:pix_th=0.08', '-an', '-f', 'null', '-'], capture_output=True, text=True).stderr
blk = [l.split('black_start:')[1].split()[0] for l in bd.splitlines() if 'black_start:' in l]
rep('black frames', not blk, 'none' if not blk else f'at {blk[:5]} s')
if a.spec and a.timing:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import motion_plan
    S = json.load(open(a.spec)); T = json.load(open(a.timing)); Cd = {}
    for li, L in enumerate(S['lines']):
        w0 = 0; ws = T['lines'][li]['words']
        for ci, ch in enumerate(L['chunks']): Cd[(li, ci)] = ws[min(w0, len(ws) - 1)] - .06; w0 += len(ch.replace('|', ' ').split(' '))
    P = motion_plan.plan(S, lambda li, ci=0, off=0.0: Cd[(li, ci)] + off); W = motion_plan.check(P)
    kinds = [p['cut'] for p in P[1:]]
    rep('transition grammar', not W, f"{dict((k, kinds.count(k)) for k in sorted(set(kinds)))}" + ('' if not W else ' | ' + '; '.join(W)))
ok = all(r[1] for r in res)
print('  RESULT:', 'PASS' if ok else 'CHECK (fix, or note why it is deliberate)')
