# Money Mirage Short s018 (Mansa Musa): whole shot plan, native portrait, data for build.py --port.
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
CAR, KING, CAI, SCL = P('mm_caravan', 'barter_market'), P('mm_king', 'barter_market'), P('mm_cairo', 'chengdu_market'), P('mm_scale', 'p_earlymoney')
C = json.load(open(os.path.join(HERE, 'coords.json'))) if os.path.exists(os.path.join(HERE, 'coords.json')) else {}
c = lambda k, d: C.get(k, d)
# 1 HOOK
shot('s00', CAR, 'film', A(0), cam0=PORT(.4, .4, 1.15), cam1=PORT(.45, .4, 1.3))
beat('card', {'abs': 0.12}, text='TOO MUCH *GOLD*', y=280, size=132, blur=True, until={'abs': 2.4})
beat('punch', A(0, 1, .3), shot='s00', level=1.25)
shot('s01', 'gold_cube', 'film', A(0, 2, -.1), cut='whip', cam0={'x': .76, 'y': .42, 'z': 1.3, 'yaw': -4}, cam1={'x': .72, 'y': .45, 'z': 1.1, 'yaw': 4})
# 2 1324 Mansa Musa
shot('s02', KING, 'film', A(1, 0, -.15), cut='zoom', cam0=PORT(.45, .4, 1.1), cam1=PORT(.45, .38, 1.3))
beat('slam', Wd(1, 1, -.03), to=1324, **NUM, until=A(1, 2, -.1))
beat('punch', A(1, 3, .3), shot='s02', level=1.25)
# 3 tons of gold (the story goes)
shot('s03', CAR, 'film', A(2, 0, -.15), cut='whip', cam0=PORT(.3, .4, 1.25), cam1=PORT(.35, .45, 1.45))
# 4 Goldie
shot('s04', CAR, 'soft', A(3, 0, -.35), cam0=PORT(.5, .5, 1.12), cam1={'z': 1.18})
beat('moment', A(3, 0, -.3), what='char', shot='s04', who='c_goldie', side='M', lines=[3], grow=A(3, 0, 1.0), leave=A(4, 0, -.25))
# 5 OPEN LOOP 1
shot('s05', KING, 'film', A(4, 0, -.15), cut='zoomIn', cam0=PORT(.45, .35, 1.3), cam1=PORT(.45, .32, 1.55))
# 6 gave it away, spent everywhere
shot('s06', CAI, 'film', A(5, 0, -.15), cut='zoom', cam0=PORT(.35, .45, 1.1), cam1=PORT(.4, .45, 1.3))
beat('punch', A(5, 3, .2), shot='s06', level=1.25)
beat('circle', A(5, 4, .3), shot='s06', c=c('cairo_gold', [.3, .5]), r=[170, 140], col='#FFC23A', until=A(6, 0, -.1))
# 7 more gold than it knew what to do with
shot('s07', 'gold_cube', 'film', A(6, 0, -.15), cut='whip', cam0={'x': .3, 'y': .45, 'z': 1.08}, cam1={'x': .33, 'y': .45, 'z': 1.18})
# 8 OPEN LOOP 2
shot('s08', SCL, 'film', A(7, 0, -.1), cut='flash', cam0=PORT(.4, .35, 1.4), cam1=PORT(.4, .38, 1.6))
beat('shake', A(7, 0, .8), k=.5)
# 9 25 -> 22
shot('s09', SCL, 'film', A(8, 0, -.15), cut='zoom', cam0=PORT(.35, .45, 1.1), cam1=PORT(.36, .47, 1.2))
beat('count', Wd(8, 4, -.05), to=25, **NUM, until=A(8, 1, -.1))
beat('slam', Wd(8, 9, -.03), to=22, **NUM, until=A(9, 0, -.1))
beat('moment', Wd(8, 9, .2), what='grade', shot='s09', bright=.6, sat=.4, d=.6)
beat('circle', Wd(8, 9, .35), shot='s09', c=c('gold_pan', [.25, .45]), r=[150, 120], until=A(9, 0, -.1))
# 10 12 years
shot('s10', CAI, 'film', A(9, 0, -.15), cut='whip', cam0=PORT(.6, .4, 1.15), cam1=PORT(.6, .38, 1.35))
beat('count', Wd(9, 9, -.05), to=12, suffix=' YRS', **NUM, until=A(10, 0, -.1))
# 11 PAYOFF
shot('MA', 'p_mirage', 'film', A(10, 0, -.15), cut='zoom', cam0={'x': .62, 'y': .35, 'z': 1.1}, cam1={'x': .62, 'y': .3, 'z': 1.3}, shim=[1.0], shimRect=[.3, 0, .75, .55])
shot('MB', 'p_mirage_empty', 'film', A(10, 1, -.05), cut='flash', depthOf='p_mirage', cam0={'x': .58, 'y': .33, 'z': 1.3}, cam1={'x': .5, 'y': .45, 'z': 1.1}, shim=[.6], shimRect=[.3, 0, .75, .55])
# 12 Bill twist
shot('s11', 'coin_spin', 'soft', A(11, 0, -.35), cam0={'x': .55, 'y': .5, 'z': 1.12}, cam1={'z': 1.18})
beat('moment', A(11, 0, -.3), what='char', shot='s11', who='c_bill', side='M', lines=[11], grow=A(11, 0, .6), leave=A(12, 0, -.25))
# 13 loop: king's gold becomes ordinary
shot('s12', CAI, 'film', A(12, 0, -.15), cut='zoomIn', cam0=PORT(.4, .45, 1.1), cam1=PORT(.4, .45, 1.35))
beat('moment', A(12, 1, .5), what='grade', shot='s12', bright=.6, sat=.4, d=.6)
# 14 comment
shot('s13', CAR, 'film', A(13, 0, -.15), cut='zoom', cam0=PORT(.45, .4, 1.2), cam1=PORT(.45, .4, 1.35))
beat('punch', A(13, 1, .3), shot='s13', level=1.25)
shot('ZZ', 'wallet_desk', 'soft', A(14, 0, -.15), cut='zoom', cam0={'x': .55, 'y': .58, 'z': 1.15}, cam1={'x': .55, 'y': .58, 'z': 1.3})
beat('moment', A(14, 0, 0), what='follow', btn=A(14, 0, .5), click=Wd(14, 4, .1), y=330)

SH = [{k: v for k, v in s.items() if v is not None} for s in SH]
json.dump({"shots": SH, "beats": BT}, open(os.path.join(HERE, "shots.json"), "w"), ensure_ascii=False, indent=1)
print(LANG, len(SH), "shots", len(BT), "beats")
