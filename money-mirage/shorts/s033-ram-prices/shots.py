# Money Mirage Short s033 (AI ate your RAM: memory prices ~3x in 2026): whole shot plan, native portrait, build.py --port. English only.
import json, os, re
HERE = os.getcwd(); LANG = json.load(open(os.path.join(HERE, 'episode.json'))).get('lang', 'en')
A = lambda li, ci=0, off=0.0: {'@': [li, ci, off]}
Wd = lambda li, wi, off=0.0: {'@w': [li, wi, off]}
SH = []; BT = []
def shot(id, img, look, at, cut='curve', cam0=None, cam1=None, keys=None, dScale=.3, **kw):
    SH.append(dict(id=id, img=img, look=look, at=at, cut=cut, cam0=cam0 or {'x': .5, 'y': .5, 'z': 1.05}, cam1=cam1 or {'z': 1.15}, keys=keys or [], dScale=dScale, **kw))
def beat(kind, at, **kw): BT.append(dict(kind=kind, at=at, **kw))
NUM = dict(align='center', y=250, size=170)
have = lambda p: os.path.exists(os.path.join(HERE, f'art/baked/{p}__film.jpg'))
def P(new, fb, fx=.5, fy=.5, nx=.5, ny=.5): return (new, nx, ny) if have(new) else (fb, fx, fy)
# word index by token, read from this folder's script (caption words, *keywords* stripped)
LINES = [re.sub(r'\[.*?\]', '', l.split(':', 1)[1]).replace('*', '').split() for l in open(os.path.join(HERE, 'script_marked.md')).read().split('\n')[1:] if ':' in l]
def W(li, tok, off=0.0, n=1):
    hits = [i for i, w in enumerate(LINES[li]) if w.lower().strip('.,?!:;"\'').startswith(tok.lower())]
    assert len(hits) >= n, (li, tok, LINES[li]); return Wd(li, hits[n - 1], off)
def cam(p, z0, z1, dx=0, dy=0): return dict(cam0={'x': p[1], 'y': p[2], 'z': z0}, cam1={'x': p[1] + dx, 'y': p[2] + dy, 'z': z1})
FOLLOW_W = 4
SHOP = P('ram_shop', 'bf_receipt'); CHIP = P('ram_chip', 'dp_tag', ny=.4); DC = P('ram_datacenter', 'ts_text'); FAB = P('ram_fab', 'dp_tag')
TAG = ('dp_tag', .5, .45); REC = ('bf_receipt', .5, .5); PHN = ('ts_text', .5, .5)
# 0 HOOK
shot('s00', SHOP[0], 'film', A(0), **cam(SHOP, 1.15, 1.3))
beat('card', {'abs': 0.12}, text='AI ate your *RAM*', y=280, size=132, blur=True, until={'abs': 2.4})
beat('punch', A(0, 0, .55), shot='s00', level=1.15)
beat('punch', A(0, 1, .2), shot='s00', level=1.28)
shot('s01', CHIP[0], 'film', A(0, 2, -.1), cut='whip', **cam(CHIP, 1.2, 1.35))
beat('slam', W(0, 'three', -.03), to=3, suffix='×', **NUM, until=A(0, 3, -.1))
shot('s02', TAG[0], 'film', A(0, 3, -.1), cut='zoom', **cam(TAG, 1.3, 1.4))
# 1 RAM; TrendForce +80% / +40% / +20%
shot('s03', CHIP[0], 'film', A(1, 0, -.15), cut='zoomIn', **cam(CHIP, 1.2, 1.35))
beat('punch', A(1, 1, .2), shot='s03', level=1.25)
beat('count', W(1, '80%', -.05), to=80, prefix='+', suffix='%', **NUM, until=A(1, 3, -.1))
beat('punch', A(1, 3, .05), shot='s03', level=1.35)
shot('s04', TAG[0], 'film', A(1, 4, -.1), cut='whip', **cam(TAG, 1.15, 1.3))
# 2 joke: not exactly a clearance sale
beat('punch', A(2, 0, .5), shot='s04', level=1.4); beat('shake', A(2, 0, .55), k=.35)
# 3 OPEN LOOP 1
shot('s05', REC[0], 'film', A(3, 0, -.15), cut='zoom', **cam(REC, 1.15, 1.35))
beat('punch', A(3, 0, 1.0), shot='s05', level=1.3)
# 4 AI. data centres
shot('s06', DC[0], 'film', A(4, 0, -.15), cut='zoomIn', **cam(DC, 1.1, 1.4), handheld=.1)
beat('punch', A(4, 1, .2), shot='s06', level=1.3)
# 5 chipmakers shift factories
shot('s07', FAB[0], 'film', A(5, 0, -.15), cut='whip', **cam(FAB, 1.15, 1.3))
beat('punch', A(5, 1, .2), shot='s07', level=1.3)
# 6 OPEN LOOP 2
shot('s08', PHN[0], 'film', A(6, 0, -.1), cut='flash', **cam(PHN, 1.15, 1.3))
beat('punch', A(6, 0, .9), shot='s08', level=1.35); beat('shake', A(6, 0, .95), k=.4)
# 7 the free chatbot pushes up the price of your phone
beat('punch', A(7, 1, .2), shot='s08', level=1.25)
shot('s09', DC[0], 'film', A(7, 2, -.1), cut='whip', **cam(DC, 1.3, 1.45))
# 8 PAYOFF (hero flash)
shot('s10', SHOP[0], 'film', A(8, 0, -.15), cut='flash', **cam(SHOP, 1.1, 1.35))
beat('punch', W(8, 'checkout', .05), shot='s10', level=1.3)
beat('moment', W(8, 'checkout', .2), what='grade', shot='s10', bright=.7, sat=.5, d=.6)
# 9 BILL: can I pay in gigabytes?
shot('s11', 'wallet_desk', 'soft', A(9, 0, -.35), cam0={'x': .5, 'y': .5, 'z': 1.12}, cam1={'z': 1.18})
beat('moment', A(9, 0, -.3), what='char', shot='s11', who='c_bill', side='M', lines=[9], shrink=A(9, 0, 1.0), leave=A(10, 0, -.25))
# 10 comment prompt
shot('s12', PHN[0], 'film', A(10, 0, -.15), cut='zoom', **cam(PHN, 1.1, 1.3))
beat('punch', A(10, 1, .1), shot='s12', level=1.22)
# 11 sign-off
shot('s13', 'wallet_desk', 'soft', A(11, 0, -.15), cut='zoom', cam0={'x': .55, 'y': .58, 'z': 1.15}, cam1={'x': .55, 'y': .58, 'z': 1.3})
beat('moment', A(11, 0, 0), what='follow', btn=A(11, 0, .5), click=Wd(11, FOLLOW_W, .1), y=330)

json.dump({"shots": SH, "beats": BT}, open(os.path.join(HERE, "shots.json"), "w"), ensure_ascii=False, indent=1)
print(LANG, len(SH), "shots", len(BT), "beats")
