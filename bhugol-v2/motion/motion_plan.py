"""Shared shot plan for the BHUGOL motion pass: one source of truth for cut times/types (the composition) and the sound
locked to them (mkscore). The spec carries:
  "shots": [{"scene": "R1", "at": [0, 0, 0]}, {"scene": "MP", "at": [1, 0, -0.15], "cut": "zoom"}, ...]
     at = [line, chunk, offset] -> the cut time = caption-chunk start + offset (the first shot is at 0)
     cut = curve (primary, default) | zoom (new chapter) | zoomIn (arrival/payoff) | whip (time jump) | flash / burn (hero, <=2 together) | hard
  "beats": [{"kind": ..., "at": [line, chunk, offset], "until": [...], "scene": ...}]   visual beats; the template places them and
     sfx() gives each its sound. kinds: slam, count, punch, charslam, grow, flap, card, circle, arrow (impact = sound-less marker)
Usage from Python:  from motion_plan import plan, sfx, unwarp;  P = plan(spec, chunk_times);  fx += sfx(P, beats);  ... unwarp(S, TIM)
"""


def plan(spec, C):
    """C(li, ci, off) -> seconds. Returns [{'scene', 't', 'cut'}]."""
    out = []
    for i, s in enumerate(spec.get('shots', [])):
        li, ci, off = (s.get('at') or [0, 0, 0]) + [0] * (3 - len(s.get('at') or []))
        out.append({'scene': s['scene'], 't': 0.0 if i == 0 else round(C(li, ci, off), 3), 'cut': s.get('cut', 'curve')})
    return out


def check(P):
    """Grammar check from the HyperFrames doctrine; returns warnings."""
    cuts = [p['cut'] for p in P[1:]]; w = []
    if cuts:
        prim = max(set(cuts), key=cuts.count); share = cuts.count(prim) / len(cuts)
        if share > .8: w.append(f'one cut type is {share:.0%} of cuts; add 1-2 accents (zoom for chapters, whip for time jumps)')
        if len(set(cuts) - {'hard'}) > 4: w.append('more than 3 transition types plus hard cuts; keep 1 primary + 1-2 accents')
        if cuts.count('flash') + cuts.count('burn') > 2: w.append('flash used more than twice; keep hero transitions to 1-2 per video')
    gaps = [b['t'] - a['t'] for a, b in zip(P, P[1:])]
    for (a, g) in zip(P, gaps):
        if g > 12: print(f'motion note: shot {a["scene"]} runs {g:.1f} s; it needs in-shot beats every 2-4 s (retention_qa.py measures this as change cadence)')
    return w


def sfx(P, beats=()):
    """Sound cues locked to the cuts, in the kit score.py fx format."""
    fx = []
    for p in P[1:]:
        t, k = p['t'], p['cut']
        if k == 'curve': fx += [['whoosh', t - .2, .5, .38, 700, 2600], ['pop', t, .4, 640]]
        elif k == 'zoom': fx += [['whoosh', t - .25, .65, .5, 400, 3000], ['thud', t + .05, .55]]
        elif k == 'zoomIn': fx += [['whoosh_down', t - .25, .6, .5, 2800, 400], ['thud', t + .05, .6]]
        elif k == 'whip': fx += [['whoosh', t - .26, .75, .45, 300, 3400], ['pop', t + .02, .4, 520]]
        elif k == 'flash': fx += [['riser', t - 1.6, .45, t - .05], ['shot', t, 1.0]]
        elif k == 'hard': fx += [['pop', t, .45, 900]]
        elif k == 'burn': fx += [['riser', t - 1.1, .4, t + .05], ['crack', t, .6], ['boom', t + .08, .75, 1.5, 44], ['crack', t + .12, .7], ['rumble', t + .1, .5, t + .9]]
    for b in beats:
        if b['kind'] == 'slam': fx += [['thud', b['t'] + .1, .7], ['pop', b['t'] + .08, .5, 760]]
        elif b['kind'] == 'count': fx += [['ticks', b['t'], .35, b['t'] + 1.4, 14]]
        elif b['kind'] == 'punch': fx += [['thud', b['t'], .4], ['pop', b['t'], .3, 520], ['whoosh', b['t'] - .12, .25, .25, 900, 2400]]  # pop = sharp transient so the hit reads on the beat
        elif b['kind'] == 'charslam': fx += [['whoosh', b['t'] - .05, .35, .35, 600, 3000], ['thud', b['t'] + .3, .75], ['pop', b['t'] + .3, .5, 700]]
        elif b['kind'] == 'grow': fx += [['ticks', b['t'], .3, b['t'] + 1.1, 18]]
        elif b['kind'] == 'flap': fx += [['pop', b['t'], .4, 1800], ['ticks', b['t'], .6, b['t'] + .9, 30]]
        elif b['kind'] == 'card': fx += [['pop', b['t'], .55, 820], ['whoosh', b['t'] - .1, .3, .3, 900, 2600]]
        elif b['kind'] in ('circle', 'arrow'): fx += [['pop', b['t'], .25, 1500], ['slide', b['t'], .35, 1800, 2600, .45]]
    return fx


def unwarp(S, TIM):
    """score.py maps every fx / music time through W() (nominal chunk positions -> aligned chunk starts). mkscore scripts
    already write real (aligned) seconds, so pre-apply the inverse here or anything on a mid-line chunk lands up to ~1 s
    off. Call once, after S['fx'] and S['music'] are filled and every line has 'o' and S['old_end'] is set."""
    anc = [(0.0, 0.0)]
    for li, L in enumerate(S['lines']):
        o, chs = L['o'], L['chunks']; nW = sum(len(c.replace('|', ' ').split(' ')) for c in chs)
        end = S['lines'][li + 1]['o'] if li < len(S['lines']) - 1 else S['old_end']; w0 = 0
        for c in chs: anc.append((TIM['lines'][li]['words'][w0] - .06, o + (w0 / nW) * (end - o))); w0 += len(c.replace('|', ' ').split(' '))
    anc.append((round((TIM['lines'][-1]['end'] + S.get('tail', 2.3)) * 30) / 30, S['old_end']))
    def inv(new):
        for (n0, o0), (n1, o1) in zip(anc, anc[1:]):
            if new <= n1: return o0 + (o1 - o0) * (new - n0) / max(1e-6, n1 - n0)
        return S['old_end']
    for f in S.get('fx', []):
        f[1] = inv(f[1])
        if f[0] in ('riser', 'stream', 'wind', 'rumble', 'ticks') and isinstance(f[3], (int, float)): f[3] = inv(f[3])
    for v in S.get('music', {}).get('sections', {}).values():
        for seg in v:
            for k in (0, 1):
                if isinstance(seg[k], (int, float)): seg[k] = inv(seg[k])
    return S
