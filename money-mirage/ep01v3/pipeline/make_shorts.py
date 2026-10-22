# Shorts v3 spec: hook line (spoken + on-screen), pieces of the main timeline, hook card plate. Hook timings come from
# audio/shorts/<id>_words.txt when present (Whisper), otherwise an estimate so pages can be previewed before voicing.
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, 'spec.json'))); T = json.load(open(os.path.join(HERE, 'audio/timing.json')))['lines']
st = lambda i, d=-.3: round(T[i]['start'] + d, 3); en = lambda i, d=.55: round(T[i]['end'] + d, 3); wd = lambda i, w, d=-.3: round(T[i]['words'][w] + d, 3)
SH = [
 ('01_what_broke', "Your $100 bill used to buy almost 5 ounces of gold. Now it buys a fortieth. What broke?", "4.84 OZ → *0.024 OZ*", 'wallet_desk__film.jpg', '45% 50%', [[st(1), en(1, .3)], [st(3), en(5)]]),
 ('02_why_gold', "Before coins, you could lose a whole day trading chickens for one goat. Why did gold end up as money?", "WHY *GOLD* WON", 'barter_market__film.jpg', '50% 50%', [[st(8), en(10)]]),
 ('03_first_paper_money', "1,000 years ago, your savings in China cost you a backpack of iron. So why did paper win, and what broke?", "FIRST *PAPER MONEY*", 'chengdu_market__film.jpg', '50% 50%', [[st(14), en(18)]]),
 ('04_gold_prison', "You could risk 10 years in prison for keeping gold in 1933. But why?", "ORDER *6102*", 'p_bank1933__film.jpg', '50% 50%', [[st(23), en(27)]]),
 ('05_france_gold', "Your dollar's gold promise started cracking in 1965. Why did France want 300 million dollars in gold?", "$300,000,000 → *GOLD*", 'p_ship__film.jpg', '40% 50%', [[st(33), en(35)]]),
 ('06_sunday_1971', "Your money lost its last link to gold on August 15th, 1971. What happened that Sunday?", "SUN AUG 15 *1971*", 'tv_1971__film.jpg', '60% 50%', [[st(37), en(41)]]),
 ('07_dollar_network', "Why do you still pay in dollars, 50 years after gold left? Blame your family group chat.", "*89%* OF TRADES", 'trading_room__film.jpg', '50% 50%', [[st(44), en(45)]]),
 ('08_gold_cube', "Why can't you just go back to gold? All 222,600 tonnes would cost you more than you think.", "*22.6 m* OF GOLD", 'gold_cube__film.jpg', '35% 50%', [[wd(49, 8), en(50)]]),
]
def chunks(line, times):
    ws = line.split(); out = []; cur = []
    for i, w in enumerate(ws):
        cur.append(i)
        if w[-1] in '.,?!' or len(cur) >= 5: out.append(cur); cur = []
    if cur: out.append(cur)
    C = []
    for k, c in enumerate(out):
        sn = times[c[0]] - .06; C.append({'txt': ' '.join(ws[i] for i in c), 'sn': round(sn, 3), 'wt': [round(times[i] - .03, 3) for i in c]})
    for k, c in enumerate(C): c['en'] = round(C[k + 1]['sn'] if k + 1 < len(C) else c['wt'][-1] + 1.2, 3)
    return C
out = []
for sid, line, onscreen, img, pos, pieces in SH:
    wf = os.path.join(HERE, 'audio/shorts', sid + '_words.txt'); lead = .15
    if os.path.exists(wf):
        times = [float(l.split()[0]) + lead for l in open(wf) if l.strip()]
        assert len(times) == len(line.split()), (sid, len(times), len(line.split()))
        dur = round(float(open(wf).read().strip().split('\n')[-1].split()[1]) + lead + .45, 3)
    else:
        times = []; t = lead
        for w in line.split(): times.append(round(t, 3)); t += .36 + (.22 if w[-1] in '.,?!' else 0)
        dur = round(t + .4, 3)
    # keywords: numbers and the question word get the red sweep
    marked = ' '.join(f'*{w}*' if any(ch.isdigit() for ch in w) else w for w in line.split())
    out.append({'id': sid, 'line': line, 'pieces': pieces, 'hook': {'img': img, 'pos': pos, 'dur': dur, 'text': onscreen, 'textOut': 2.2, 'chunks': chunks(marked, times)},
                'dur': round(dur + sum(b - a for a, b in pieces), 2)})
json.dump({'shorts': out}, open(os.path.join(HERE, 'shorts_v3.json'), 'w'), ensure_ascii=False, indent=1)
for s in out: print(s['id'], s['dur'], 's', s['pieces'])
