# Money Mirage Short s022 (Black Friday deals): whole shot plan, native portrait, data for build.py --port.
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
shot('s00', TV, 'film', A(0), cam0=PORT(.6, .3, 1.15), cam1=PORT(.62, .28, 1.3))
beat('card', {'abs': 0.12}, text='SALE *?*', y=280, size=150, blur=True, until={'abs': 2.2})
beat('punch', A(0, 0, .9), shot='s00', level=1.2)
beat('count', Wd(0, 14, -.05), to=134, suffix=' days', **dict(NUM, y=560), until=A(0, 2, -.1))
beat('circle', A(0, 2, .1), shot='s00', c=c('sticker', [.83, .2]), r=[120, 120], until=A(1, 0, -.1))
# 2-3 Which? 175 products, 83%
shot('s01', CRD, 'film', A(1, 0, -.15), cut='whip', cam0=PORT(.5, .25, 1.1), cam1=PORT(.5, .22, 1.3))
beat('count', Wd(1, 4, -.05), to=175, **NUM, until=A(2, 0, -.1))
shot('s02', TV, 'film', A(2, 0, -.15), cut='zoom', cam0=PORT(.6, .3, 1.2), cam1=PORT(.6, .3, 1.4))
beat('slam', Wd(2, 0, -.03), to=83, suffix='%', **NUM, until=A(3, 0, -.4))
# 4 Goldie
shot('s03', TV, 'soft', A(3, 0, -.35), cam0=PORT(.5, .5, 1.12), cam1={'z': 1.18})
beat('moment', A(3, 0, -.3), what='char', shot='s03', who='c_goldie', side='M', lines=[3], shrink=A(3, 1, .1), leave=A(4, 0, -.25))
# 5 OPEN LOOP 1
shot('s04', CRD, 'film', A(4, 0, -.15), cut='zoomIn', cam0=PORT(.5, .3, 1.3), cam1=PORT(.5, .25, 1.55))
# 6 the "was" price
shot('s05', TV, 'film', A(5, 0, -.15), cut='whip', cam0=PORT(.8, .22, 1.3), cam1=PORT(.82, .2, 1.5))
beat('punch', A(5, 1, .3), shot='s05', level=1.3)
# 7 countdown clock
shot('s06', CLK, 'film', A(6, 0, -.15), cut='zoom', cam0=PORT(.42, .15, 1.15), cam1=PORT(.42, .2, 1.35), handheld=.1)
beat('circle', A(6, 0, .5), shot='s06', c=c('clock', [.42, .12]), r=[260, 110], until=A(7, 0, -.1))
# 8 OPEN LOOP 2
shot('s07', CLK, 'film', A(7, 0, -.1), cut='flash', cam0=PORT(.4, .5, 1.35), cam1=PORT(.4, .5, 1.55))
beat('shake', A(7, 0, .8), k=.5)
# 9 drop again, 27% less
shot('s08', RCP, 'film', A(8, 0, -.15), cut='zoom', cam0=PORT(.5, .4, 1.1), cam1=PORT(.6, .35, 1.3))
beat('count', Wd(8, 12, -.05), to=27, prefix='-', suffix='%', **NUM, until=A(9, 0, -.1))
beat('moment', A(8, 1, .2), what='grade', shot='s08', bright=.6, sat=.4, d=.6)
# 10 PAYOFF
shot('MA', 'p_mirage', 'film', A(9, 0, -.15), cut='zoom', cam0={'x': .62, 'y': .35, 'z': 1.1}, cam1={'x': .62, 'y': .3, 'z': 1.3}, shim=[1.0], shimRect=[.3, 0, .75, .55])
shot('MB', 'p_mirage_empty', 'film', A(9, 1, -.05), cut='flash', depthOf='p_mirage', cam0={'x': .58, 'y': .33, 'z': 1.3}, cam1={'x': .5, 'y': .45, 'z': 1.1}, shim=[.6], shimRect=[.3, 0, .75, .55])
beat('punch', A(9, 1, 1.0), shot='MB', level=1.2)
# 11 price history, not percent off
shot('s09', RCP, 'film', A(10, 0, -.15), cut='whip', cam0=PORT(.68, .3, 1.25), cam1=PORT(.68, .32, 1.45))
beat('circle', A(10, 0, .5), shot='s09', c=c('calendar', [.68, .3]), r=[150, 130], col='#FFC23A', until=A(11, 0, -.4))
# 12 Bill
shot('s10', TV, 'soft', A(11, 0, -.35), cam0=PORT(.5, .5, 1.12), cam1={'z': 1.18})
beat('moment', A(11, 0, -.3), what='char', shot='s10', who='c_bill', side='M', lines=[11], grow=A(11, 0, .8), leave=A(12, 0, -.25))
# 13 comment
shot('s11', CRD, 'film', A(12, 0, -.15), cut='zoom', cam0=PORT(.5, .3, 1.2), cam1=PORT(.5, .3, 1.35))
beat('punch', A(12, 0, 1.0), shot='s11', level=1.25)
shot('ZZ', 'wallet_desk', 'soft', A(13, 0, -.15), cut='zoom', cam0={'x': .55, 'y': .58, 'z': 1.15}, cam1={'x': .55, 'y': .58, 'z': 1.3})
beat('moment', A(13, 0, 0), what='follow', btn=A(13, 0, .5), click=Wd(13, 4, .1), y=330)

SH = [{k: v for k, v in s.items() if v is not None} for s in SH]
json.dump({"shots": SH, "beats": BT}, open(os.path.join(HERE, "shots.json"), "w"), ensure_ascii=False, indent=1)
print(LANG, len(SH), "shots", len(BT), "beats")
