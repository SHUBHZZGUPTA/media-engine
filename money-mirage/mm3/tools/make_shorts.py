# Shorts (v3): portrait Shorts cut from the long-form, each with a NEW spoken hook, a tailored CTA teaser and the plug.
# Everything episode-specific lives in episode.json -> "shorts". Run from the episode folder.
#   python3 make_shorts.py            -> shorts_v3.json (hook/CTA timings from audio/shorts/* when voiced, estimates before)
#   python3 make_shorts.py --tts-job  -> <repo>/jobs/tts/<slug>-shorts.json (2 requests: all hooks, all CTAs; narrator model only)
#   python3 make_shorts.py --split <hooks_ctas.wav> <whisper words.txt>  -> audio/shorts/<id>.wav, <id>_cta.wav + word timings
import json, os, sys, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from mmpaths import *
PLUG = "The full story's on Money Mirage. Follow for more."
SHS = EPC['shorts']
lines_of = lambda: [s['hook'] for s in SHS] + [s['cta'] + ' ' + PLUG for s in SHS]
if '--tts-job' in sys.argv:
    D = ("Narrate for a premium documentary YouTube channel about money and history. The narrator is a deep, warm, confident storyteller with a hint of mystery, "
         "energetic and punchy, never slow, never announcer-like. These are separate short lines for YouTube Shorts: read each one as its own complete take, "
         "with the same voice, energy and loudness every time, and leave a clear one-second pause between lines. Natural emphasis on dates and numbers; "
         "questions end with a curious lift.")
    nar = {'Narrator': EPC.get('tts_speakers', {}).get('Narrator', 'Sadaltager')}
    job = {'id': EPC['slug'] + '-shorts', 'models': ['gemini-3.1-flash-tts-preview'],
           'items': [{'name': 'hooks', 'direction': D, 'speakers': nar, 'lines': [['Narrator', s['hook']] for s in SHS]},
                     {'name': 'ctas', 'direction': D, 'speakers': nar, 'lines': [['Narrator', s['cta'] + ' ' + PLUG] for s in SHS]}]}
    p = os.path.join(REPO, 'jobs/tts', job['id'] + '.json'); json.dump(job, open(p, 'w'), indent=1, ensure_ascii=False); print('wrote', p); sys.exit()
if '--split' in sys.argv:
    import numpy as np, soundfile as sf
    wav, words = sys.argv[sys.argv.index('--split') + 1:sys.argv.index('--split') + 3]
    os.makedirs('audio/shorts', exist_ok=True); L = lines_of(); names = [s['id'] for s in SHS] + [s['id'] + '_cta' for s in SHS]
    json.dump({'lines': [{'text': t} for t in L]}, open('audio/shorts/_spec.json', 'w'))
    subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'words_fit.py'), 'audio/shorts/_spec.json', words, 'audio/shorts/_fit.txt'], check=True)
    x, sr = sf.read(wav); F = [l.split() for l in open('audio/shorts/_fit.txt') if l.strip()]; k = 0
    for nm, t in zip(names, L):
        n = len(t.split()); ws = F[k:k + n]; k += n; a = max(0, float(ws[0][0]) - .08); b = float(ws[-1][1]) + .3
        seg = x[int(a * sr):int(b * sr)].copy(); f = int(.015 * sr); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        sf.write(f'audio/shorts/{nm}.wav', seg, sr)
        wf = f'audio/shorts/{nm}_words.txt' if not nm.endswith('_cta') else f'audio/shorts/{nm[:-4]}_cta_words.txt'
        open(wf, 'w').write(''.join(f'{float(w[0]) - a:.3f} {float(w[1]) - a:.3f} {w[2] if len(w) > 2 else ""}\n' for w in ws)); print(nm, round(b - a, 2), 's')
    sys.exit()

S = json.load(open('spec.json')); T = json.load(open('audio/timing.json'))['lines']
CUTS = [x['t'] for x in json.load(open('proj/times.json'))['shots']]
def en(i, d=.55):   # end a piece after its last word, but before the next shot's transition starts (no flash of the next scene)
    e = T[i]['end']; b = e + d; c = [x for x in CUTS if e < x < b + .6]
    return round(max(e + .12, min(b, c[0] - .45)) if c else b, 3)
def st(f):          # piece start: a line number, or [line, word] to start mid-line
    return round((T[f[0]]['words'][f[1]] if isinstance(f, list) else T[f]['start']) - .3, 3)
def chunks(line, times):
    ws = line.split(); out = []; cur = []
    for i, w in enumerate(ws):
        cur.append(i)
        if w[-1] in '.,?!' or len(cur) >= 5: out.append(cur); cur = []
    if cur: out.append(cur)
    C = [{'txt': ' '.join(ws[i] for i in c), 'sn': round(times[c[0]] - .06, 3), 'wt': [round(times[i] - .03, 3) for i in c]} for c in out]
    for k, c in enumerate(C): c['en'] = round(C[k + 1]['sn'] if k + 1 < len(C) else c['wt'][-1] + 1.2, 3)
    return C
def timed(path, words, lead, tail):
    if os.path.exists(path):
        t = [float(l.split()[0]) + lead for l in open(path) if l.strip()]; assert len(t) == len(words), (path, len(t), len(words))
        return t, round(float(open(path).read().strip().split('\n')[-1].split()[1]) + lead + tail, 3)
    t, x = [], lead
    for w in words: t.append(round(x, 3)); x += .36 + (.22 if w[-1] in '.,?!' else 0)
    return t, round(x + tail, 3)
out = []
for s in SHS:
    sid, line = s['id'], s['hook']; pieces = [[st(p[0]), en(p[1], p[2] if len(p) > 2 else .55)] for p in s['pieces']]
    times, dur = timed(os.path.join('audio/shorts', sid + '_words.txt'), line.split(), .15, .45)
    marked = ' '.join(f'*{w}*' if any(ch.isdigit() for ch in w) else w for w in line.split())   # numbers get the red sweep
    cta = s['cta'] + ' ' + PLUG; cw = cta.split()
    ct, cdur = timed(os.path.join('audio/shorts', sid + '_cta_words.txt'), cw, .2, .9)
    ix = lambda w, after=0: next(i for i, x in enumerate(cw) if i >= after and x.strip('.,?!').lower() == w)
    cmarked = ' '.join(f'*{w}*' if w.strip('.,') in ('Money', 'Mirage', 'Follow') else w for w in cw)
    outro = {'img': EPC.get('outro_img', 'wallet_desk__soft.jpg'), 'dur': cdur, 'plug': round(ct[ix('full')] - .1, 3),
             'btn': round(ct[ix('money', ix('full'))] - .1, 3), 'click': round(ct[ix('follow', ix('full'))] + .1, 3), 'chunks': chunks(cmarked, ct)}
    out.append({'id': sid, 'line': line, 'cta': cta, 'pcam': s.get('pcam', {}), 'pieces': pieces,
                'hook': {'img': s['img'], 'pos': s.get('pos', '50% 50%'), 'dur': dur, 'text': s['onscreen'], 'textOut': 2.2, 'chunks': chunks(marked, times)},
                'outro': outro, 'dur': round(dur + sum(b - a for a, b in pieces) + cdur, 2)})
json.dump({'shorts': out}, open('shorts_v3.json', 'w'), ensure_ascii=False, indent=1)
for s in out: print(s['id'], s['dur'], 's', s['pieces'])
