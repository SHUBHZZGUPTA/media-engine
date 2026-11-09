# Money Mirage Short s034 (Victor Lustig sells the Eiffel Tower, 1925): whole shot plan, native portrait, build.py --port. English only.
# Lustig and Poisson are never drawn: anonymous figures from behind / hands only.
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
TOWER = P('et_tower', 'nb_alley'); HOTEL = P('et_hotel', 'nb_alley'); LET = P('et_letter', 'wallet_desk'); CASH = P('et_cash', 'wallet_desk')
COP = ('fc_cop', .5, .45); ALLEY = ('nb_alley', .5, .45); JAIL = ('jail_bars', .5, .45)
# 0 HOOK
shot('s00', TOWER[0], 'film', A(0), **cam(TOWER, 1.1, 1.25, dy=-.04))
beat('card', {'abs': 0.12}, text='*SOLD:* the Eiffel Tower', y=280, size=124, blur=True, until={'abs': 2.4})
beat('punch', A(0, 0, .55), shot='s00', level=1.15)
beat('slam', W(0, '1925', -.03), to=1925, **dict(NUM, y=640, size=150), until=A(0, 2, -.1))
shot('s01', CASH[0], 'film', A(0, 2, -.1), cut='whip', **cam(CASH, 1.2, 1.35))
beat('punch', A(0, 3, .1), shot='s01', level=1.4)
# 1 only meant to stand 20 years; rusting
shot('s02', TOWER[0], 'film', A(1, 0, -.15), cut='zoomIn', cam0={'x': TOWER[1], 'y': .35, 'z': 1.3}, cam1={'x': TOWER[1], 'y': .3, 'z': 1.55})
beat('count', W(1, '20', -.05), to=20, suffix=' YRS', **NUM, until=A(1, 1, -.1))
beat('punch', A(1, 2, .1), shot='s02', level=1.3)
# 2 fake letterhead; luxury hotel
shot('s03', LET[0], 'film', A(2, 0, -.15), cut='whip', **cam(LET, 1.15, 1.3))
beat('punch', W(2, 'letterhead', .05), shot='s03', level=1.3)
shot('s04', HOTEL[0], 'film', A(2, 1, -.1), cut='zoom', **cam(HOTEL, 1.1, 1.3))
# 3 pitch: sell for scrap. Top secret.
beat('punch', A(3, 1, .2), shot='s04', level=1.25)
beat('punch', A(3, 2, .1), shot='s04', level=1.38); beat('shake', A(3, 2, .15), k=.35)
# 4 joke: not exactly a garage sale
shot('s05', TOWER[0], 'film', A(4, 0, -.15), cut='zoom', cam0={'x': TOWER[1], 'y': .3, 'z': 1.2}, cam1={'x': TOWER[1], 'y': .3, 'z': 1.4})
beat('punch', A(4, 0, .7), shot='s05', level=1.35)
# 5 OPEN LOOP 1
shot('s06', COP[0], 'film', A(5, 0, -.15), cut='whip', **cam(COP, 1.15, 1.35))
beat('punch', W(5, 'police', .05), shot='s06', level=1.3)
# 6 Poisson paid, plus a bribe; Lustig vanished
shot('s07', CASH[0], 'film', A(6, 0, -.15), cut='zoom', **cam(CASH, 1.1, 1.3))
beat('punch', A(6, 1, .1), shot='s07', level=1.3)
beat('punch', A(6, 2, .2), shot='s07', level=1.4)
# 7 OPEN LOOP 2
shot('s08', TOWER[0], 'film', A(7, 0, -.1), cut='flash', cam0={'x': .45, 'y': .66, 'z': 1.25}, cam1={'x': .45, 'y': .62, 'z': 1.4})
beat('punch', A(7, 0, .9), shot='s08', level=1.35); beat('shake', A(7, 0, .95), k=.4)
# 8 too embarrassed; came back; tried again
shot('s09', LET[0], 'film', A(8, 0, -.15), cut='zoom', **cam(LET, 1.25, 1.4))
shot('s10', HOTEL[0], 'film', A(8, 1, -.1), cut='whip', **cam(HOTEL, 1.2, 1.35))
beat('moment', W(8, 'again', .1), what='grade', shot='s10', bright=.65, sat=.45, d=.6)
# 9 PAYOFF (hero flash)
shot('s11', TOWER[0], 'film', A(9, 0, -.15), cut='flash', **cam(TOWER, 1.05, 1.3))
beat('punch', W(9, 'silence', .05), shot='s11', level=1.3)
# 10 BILL twist
shot('s12', 'wallet_desk', 'soft', A(10, 0, -.35), cam0={'x': .5, 'y': .5, 'z': 1.12}, cam1={'z': 1.18})
beat('moment', A(10, 0, -.3), what='char', shot='s12', who='c_bill', side='M', lines=[10], shrink=A(10, 0, 1.2), leave=A(11, 0, -.25))
# 11 comment prompt
shot('s13', JAIL[0], 'film', A(11, 0, -.15), cut='zoom', **cam(JAIL, 1.1, 1.3))
beat('punch', A(11, 0, 1.3), shot='s13', level=1.22)
# 12 sign-off
shot('s14', 'wallet_desk', 'soft', A(12, 0, -.15), cut='zoom', cam0={'x': .55, 'y': .58, 'z': 1.15}, cam1={'x': .55, 'y': .58, 'z': 1.3})
beat('moment', A(12, 0, 0), what='follow', btn=A(12, 0, .5), click=Wd(12, FOLLOW_W, .1), y=330)

json.dump({"shots": SH, "beats": BT}, open(os.path.join(HERE, "shots.json"), "w"), ensure_ascii=False, indent=1)
print(LANG, len(SH), "shots", len(BT), "beats")
