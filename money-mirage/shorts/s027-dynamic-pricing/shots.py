# Money Mirage Short s027 (dynamic pricing): whole shot plan, native portrait, data for build.py --port.
import json, os
HERE = os.getcwd(); LANG = json.load(open(os.path.join(HERE, 'episode.json'))).get('lang', 'en')
A = lambda li, ci=0, off=0.0: {'@': [li, ci, off]}
Wd = lambda li, wi, off=0.0: {'@w': [li, wi, off]}
SH = []; BT = []
def shot(id, img, look, at, cut='curve', cam0=None, cam1=None, keys=None, dScale=.3, **kw):
    SH.append(dict(id=id, img=img, look=look, at=at, cut=cut, cam0=cam0 or {'x': .5, 'y': .5, 'z': 1.05}, cam1=cam1 or {'z': 1.15}, keys=keys or [], dScale=dScale, **kw))
def beat(kind, at, **kw): BT.append(dict(kind=kind, at=at, **kw))
NUM = dict(align='center', y=250, size=170)
P = lambda n, fb: n if os.path.exists(os.path.join(HERE, f'art/baked/{n}__film.jpg')) else fb   # new Codex plate, library fallback
PORT = lambda x=.5, y=.5, z=1.05: {'x': x, 'y': y, 'z': z}
C = json.load(open(os.path.join(HERE, "coords.json"))) if os.path.exists(os.path.join(HERE, "coords.json")) else {}
c = lambda k, d: C.get(k, d)
TV, CLK, RCP, CRD = P('bf_tv', 'trading_room'), P('bf_clock', 'trading_room'), P('bf_receipt', 'wallet_desk'), P('bf_crowd', 'uk_high_street_1991')
# 1 HOOK
EGG, SHP, BRD, TAG = P('dp_eggs', 'chengdu_market'), P('dp_shoppers', 'chengdu_market'), P('dp_board', 'trading_room'), P('dp_tag', 'wallet_desk')
# 1 HOOK
shot('s00', EGG, 'film', A(0), cam0=PORT(.5, .35, 1.15), cam1=PORT(.5, .4, 1.35))
beat('card', {'abs': 0.12}, text='$3.99 *or* $4.79?', y=280, size=120, blur=True, until={'abs': 2.2})
beat('punch', A(0, 1, .1), shot='s00', level=1.2)
beat('circle', A(0, 2, .1), shot='s00', c=c('tags', [.5, .6]), r=[300, 140], until=A(1, 0, -.1))
# 2 Instacart, five prices
shot('s01', SHP, 'film', A(1, 0, -.15), cut='whip', cam0=PORT(.5, .45, 1.1), cam1=PORT(.55, .45, 1.3))
shot('s02', EGG, 'film', A(1, 2, -.1), cut='zoom', cam0=PORT(.5, .55, 1.25), cam1=PORT(.5, .6, 1.5))
beat('count', Wd(1, 13, -.05), to=3.99, dec=2, prefix='$', **NUM, until=Wd(1, 18, -.1))
beat('punch', A(1, 3, .1), shot='s02', level=1.3)
beat('slam', Wd(1, 18, -.03), to=4.79, dec=2, prefix='$', **NUM, until=A(2, 0, -.2))
# 3 3 in 4 items
shot('s03', SHP, 'film', A(2, 0, -.15), cut='zoomIn', cam0=PORT(.55, .45, 1.25), cam1=PORT(.55, .45, 1.5))
beat('circle', A(2, 0, .6), shot='s03', c=c('phones', [.55, .45]), r=[330, 200], col='#FFC23A', until=A(3, 0, -.4))
# 4 Goldie
shot('s04', EGG, 'soft', A(3, 0, -.35), cam0=PORT(.5, .5, 1.12), cam1={'z': 1.18})
beat('moment', A(3, 0, -.3), what='char', shot='s04', who='c_goldie', side='M', lines=[3], shrink=A(3, 1, .2), leave=A(4, 0, -.25))
# 5 dynamic pricing (OPEN LOOP 1: who's looking)
shot('s05', TAG, 'film', A(4, 0, -.15), cut='whip', cam0=PORT(.5, .4, 1.1), cam1=PORT(.5, .4, 1.35))
beat('punch', A(4, 1, .2), shot='s05', level=1.2)
beat('punch', A(4, 3, .1), shot='s05', level=1.35)
beat('shake', A(4, 3, .3), k=.4)
# 6 airlines: Delta 3% -> 20%
shot('s06', BRD, 'film', A(5, 0, -.15), cut='zoom', cam0=PORT(.5, .35, 1.1), cam1=PORT(.5, .3, 1.3))
beat('count', Wd(5, 11, -.05), to=3, suffix='%', **NUM, until=Wd(5, 21, -.1))
beat('slam', Wd(5, 21, -.03), to=20, suffix='%', **NUM, until=A(6, 1, -.2))
# 7 Instacart ended tests Dec 2025
shot('s07', SHP, 'film', A(6, 0, -.15), cut='whip', cam0=PORT(.45, .4, 1.2), cam1=PORT(.45, .4, 1.4))
beat('punch', Wd(6, 6, .1), shot='s07', level=1.3)
# 8 PAYOFF
shot('MA', 'p_mirage', 'film', A(7, 0, -.15), cut='zoom', cam0={'x': .62, 'y': .35, 'z': 1.1}, cam1={'x': .62, 'y': .3, 'z': 1.3}, shim=[1.0], shimRect=[.3, 0, .75, .55])
shot('MB', 'p_mirage_empty', 'film', A(7, 2, -.1), cut='flash', depthOf='p_mirage', cam0={'x': .58, 'y': .33, 'z': 1.3}, cam1={'x': .5, 'y': .45, 'z': 1.1}, shim=[.6], shimRect=[.3, 0, .75, .55])
beat('punch', A(7, 2, .5), shot='MB', level=1.2)
# 9 compare
shot('s08', TAG, 'film', A(8, 0, -.15), cut='whip', cam0=PORT(.5, .45, 1.25), cam1=PORT(.5, .45, 1.45))
beat('punch', A(8, 1, .3), shot='s08', level=1.25)
shot('s09', EGG, 'film', A(8, 3, -.1), cut='zoom', cam0=PORT(.5, .35, 1.2), cam1=PORT(.5, .35, 1.35))
# 10 Bill
shot('s10', SHP, 'soft', A(9, 0, -.35), cam0=PORT(.5, .5, 1.12), cam1={'z': 1.18})
beat('moment', A(9, 0, -.3), what='char', shot='s10', who='c_bill', side='M', lines=[9], grow=A(9, 0, .8), leave=A(10, 0, -.25))
# 11 comment
shot('s11', TAG, 'film', A(10, 0, -.15), cut='zoom', cam0=PORT(.5, .4, 1.2), cam1=PORT(.5, .4, 1.35))
beat('punch', A(10, 1, .3), shot='s11', level=1.25)
shot('ZZ', 'wallet_desk', 'soft', A(11, 0, -.15), cut='zoom', cam0={'x': .55, 'y': .58, 'z': 1.15}, cam1={'x': .55, 'y': .58, 'z': 1.3})
beat('moment', A(11, 0, 0), what='follow', btn=A(11, 0, .5), click=Wd(11, 4, .1), y=330)

SH = [{k: v for k, v in s.items() if v is not None} for s in SH]
json.dump({"shots": SH, "beats": BT}, open(os.path.join(HERE, "shots.json"), "w"), ensure_ascii=False, indent=1)
print(LANG, len(SH), "shots", len(BT), "beats")
