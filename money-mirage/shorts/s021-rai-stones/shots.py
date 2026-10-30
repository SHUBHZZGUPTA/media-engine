# Money Mirage Short s021 (Rai stones of Yap): whole shot plan, native portrait, data for build.py --port.
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
SEA, PATH, VIL, RAFT = P('ry_seafloor', 'canal_buoys'), P('ry_path', 'barter_market'), P('ry_village', 'barter_market'), P('ry_raft', 'p_ship')
# 1 HOOK
shot('s00', SEA, 'film', A(0), cam0=PORT(.5, .3, 1.2), cam1=PORT(.5, .35, 1.35))
beat('card', {'abs': 0.12}, text='SUNK… *STILL MONEY?*', y=280, size=112, blur=True, until={'abs': 2.4})
beat('punch', A(0, 2, .2), shot='s00', level=1.3)
beat('circle', A(0, 3, .1), shot='s00', c=c('sea_stone', [.5, .35]), r=[260, 260], col='#FFC23A', until=A(1, 0, -.1))
# 2 Yap, rai
shot('s01', PATH, 'film', A(1, 0, -.15), cut='whip', cam0=PORT(.4, .35, 1.1), cam1=PORT(.35, .35, 1.3))
beat('punch', A(1, 3, .2), shot='s01', level=1.25)
# 3 3.6 m
shot('s02', PATH, 'film', A(2, 0, -.12), cut='zoomIn', cam0=PORT(.25, .35, 1.3), cam1=PORT(.25, .38, 1.5))
beat('count', Wd(2, 3, -.05), to=3.6, dec=1, suffix=' m', **NUM, until=A(3, 0, -.4))
# 4 Bill
shot('s03', PATH, 'soft', A(3, 0, -.35), cam0=PORT(.5, .5, 1.12), cam1={'z': 1.18})
beat('moment', A(3, 0, -.3), what='char', shot='s03', who='c_bill', side='M', lines=[3], shrink=A(3, 0, .9), leave=A(4, 0, -.25))
# 5 OPEN LOOP 1
shot('s04', VIL, 'film', A(4, 0, -.15), cut='whip', cam0=PORT(.6, .3, 1.3), cam1=PORT(.62, .27, 1.5))
# 6 everyone agrees who owns it
shot('s05', VIL, 'film', A(5, 0, -.15), cut='zoom', cam0=PORT(.5, .4, 1.1), cam1=PORT(.45, .45, 1.3))
beat('punch', A(5, 1, .3), shot='s05', level=1.25)
# 7 Palau 400 km by sea
shot('s06', RAFT, 'film', A(6, 0, -.15), cut='whip', cam0=PORT(.45, .3, 1.15), cam1=PORT(.5, .32, 1.3))
beat('count', Wd(6, 5, -.05), to=400, suffix=' km', **NUM, until=A(7, 0, -.1))
# 8 OPEN LOOP 2
shot('s07', RAFT, 'film', A(7, 0, -.1), cut='flash', cam0=PORT(.45, .3, 1.4), cam1=PORT(.45, .35, 1.6))
beat('shake', A(7, 0, .8), k=.6)
# 9 it sank, still traded
shot('s08', SEA, 'film', A(8, 0, -.15), cut='zoom', cam0=PORT(.5, .2, 1.1), cam1=PORT(.5, .35, 1.3))
beat('punch', A(8, 1, .3), shot='s08', level=1.25)
shot('s09', VIL, 'film', A(8, 2, -.1), cut='whip', cam0=PORT(.6, .3, 1.2), cam1=PORT(.62, .3, 1.35))
# 10 PAYOFF
shot('MA', 'p_mirage', 'film', A(9, 0, -.15), cut='zoom', cam0={'x': .62, 'y': .35, 'z': 1.1}, cam1={'x': .62, 'y': .3, 'z': 1.3}, shim=[1.0], shimRect=[.3, 0, .75, .55])
shot('MB', 'p_mirage_empty', 'film', A(9, 1, -.05), cut='flash', depthOf='p_mirage', cam0={'x': .58, 'y': .33, 'z': 1.3}, cam1={'x': .5, 'y': .45, 'z': 1.1}, shim=[.6], shimRect=[.3, 0, .75, .55])
# 11 your money is numbers
shot('s10', 'wire_terminal', 'film', A(10, 0, -.15), cut='zoom', cam0={'x': .55, 'y': .35, 'z': 1.25}, cam1={'x': .55, 'y': .35, 'z': 1.45})
# 12 Goldie
shot('s11', 'vault_full', 'soft', A(11, 0, -.35), cam0={'x': .5, 'y': .5, 'z': 1.12}, cam1={'z': 1.18})
beat('moment', A(11, 0, -.3), what='char', shot='s11', who='c_goldie', side='M', lines=[11], grow=A(11, 1, 0), leave=A(12, 0, -.25))
# 13 loop: account or agreement
shot('s12', SEA, 'film', A(12, 0, -.15), cut='zoomIn', cam0=PORT(.5, .35, 1.1), cam1=PORT(.5, .35, 1.35))
beat('moment', A(12, 1, .2), what='grade', shot='s12', bright=.6, sat=.4, d=.6)
# 14 comment
shot('s13', VIL, 'film', A(13, 0, -.15), cut='zoom', cam0=PORT(.6, .3, 1.2), cam1=PORT(.6, .3, 1.35))
beat('punch', A(13, 0, .9), shot='s13', level=1.25)
shot('ZZ', 'wallet_desk', 'soft', A(14, 0, -.15), cut='zoom', cam0={'x': .55, 'y': .58, 'z': 1.15}, cam1={'x': .55, 'y': .58, 'z': 1.3})
beat('moment', A(14, 0, 0), what='follow', btn=A(14, 0, .5), click=Wd(14, 4, .1), y=330)

SH = [{k: v for k, v in s.items() if v is not None} for s in SH]
json.dump({"shots": SH, "beats": BT}, open(os.path.join(HERE, "shots.json"), "w"), ensure_ascii=False, indent=1)
print(LANG, len(SH), "shots", len(BT), "beats")
