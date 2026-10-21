"""Shared shot plan for the BHUGOL motion pass: one source of truth for cut times/types (the composition) and the sound
locked to them (mkscore). The spec carries:
  "shots": [{"scene": "R1", "at": [0, 0, 0]}, {"scene": "MP", "at": [1, 0, -0.15], "cut": "zoom"}, ...]
     at = [line, chunk, offset] -> the cut time = caption-chunk start + offset (the first shot is at 0)
     cut = curve (primary, default) | zoom (new chapter) | zoomIn (arrival/payoff) | whip (time jump) | flash (hero, <=2) | hard
  "beats": [{"kind": "slam" | "count", "at": [line, chunk, offset]}]   optional, for SFX on number slams / count-ups
Usage from Python:  from motion_plan import plan, sfx;  P = plan(spec, chunk_times);  fx += sfx(P)
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
        if cuts.count('flash') > 2: w.append('flash used more than twice; keep hero transitions to 1-2 per video')
    gaps = [b['t'] - a['t'] for a, b in zip(P, P[1:])]
    for (a, g) in zip(P, gaps):
        if g > 12: print(f'motion note: shot {a["scene"]} runs {g:.1f} s; it needs in-shot beats every 2-4 s (retention_qa.py measures this as change cadence)')
    return w


def sfx(P, beats=()):
    """Sound cues locked to the cuts, in the kit score.py fx format."""
    fx = []
    for p in P[1:]:
        t, k = p['t'], p['cut']
        if k == 'curve': fx += [['whoosh', t - .2, .5, .38, 700, 2600]]
        elif k == 'zoom': fx += [['whoosh', t - .25, .65, .5, 400, 3000], ['thud', t + .05, .55]]
        elif k == 'zoomIn': fx += [['whoosh_down', t - .25, .6, .5, 2800, 400], ['thud', t + .05, .6]]
        elif k == 'whip': fx += [['whoosh', t - .26, .75, .45, 300, 3400], ['pop', t + .02, .4, 520]]
        elif k == 'flash': fx += [['riser', t - 1.6, .45, t - .05], ['shot', t, 1.0]]
        elif k == 'hard': fx += [['pop', t, .45, 900]]
    for b in beats:
        if b['kind'] == 'slam': fx += [['thud', b['t'] + .1, .7], ['pop', b['t'] + .08, .5, 760]]
        elif b['kind'] == 'count': fx += [['ticks', b['t'], .35, b['t'] + 1.4, 14]]
        elif b['kind'] == 'punch': fx += [['thud', b['t'], .4], ['whoosh', b['t'] - .12, .25, .25, 900, 2400]]
    return fx
