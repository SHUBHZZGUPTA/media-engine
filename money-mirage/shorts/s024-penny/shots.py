# Money Mirage Short s024 (the penny): whole shot plan, native portrait, data for build.py --port.
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
PRESS, JAR, LED, NIC = P('pn_press', 'lydia_mint'), P('pn_jar', 'coin_spin'), P('pn_ledger', 'p_earlymoney'), P('pn_nickel', 'coin_spin')
# 1 HOOK
shot('s00', JAR, 'film', A(0), cam0=PORT(.55, .38, 1.2), cam1=PORT(.55, .38, 1.35))
beat('card', {'abs': 0.12}, text='1¢ = *4¢?*', y=280, size=150, blur=True, until={'abs': 2.2})
beat('count', Wd(0, 8, -.05), to=4, suffix='¢', **dict(NUM, y=560), until=A(0, 2, -.1))
beat('punch', A(0, 2, .3), shot='s00', level=1.3)
# 2 2024: 3.7 cents, loss on every one
shot('s01', PRESS, 'film', A(1, 0, -.15), cut='whip', cam0=PORT(.45, .45, 1.1), cam1=PORT(.45, .5, 1.3))
beat('slam', Wd(1, 1, -.03), to=2024, **NUM, until=A(1, 1, -.1))
beat('count', Wd(1, 6, -.05), to=3.7, dec=1, suffix='¢', **NUM, until=A(1, 3, -.1))
shot('s02', LED, 'film', A(1, 3, -.1), cut='zoom', cam0=PORT(.7, .35, 1.2), cam1=PORT(.7, .35, 1.4))
beat('circle', A(1, 3, .4), shot='s02', c=c('scale', [.7, .35]), r=[220, 180], col='#FFC23A', until=A(2, 0, -.4))
# 3 Goldie
shot('s03', PRESS, 'soft', A(2, 0, -.35), cam0=PORT(.5, .5, 1.12), cam1={'z': 1.18})
beat('moment', A(2, 0, -.3), what='char', shot='s03', who='c_goldie', side='M', lines=[2], grow=A(2, 0, 1.0), leave=A(3, 0, -.25))
# 4 OPEN LOOP 1
shot('s04', JAR, 'film', A(3, 0, -.15), cut='zoomIn', cam0=PORT(.55, .38, 1.35), cam1=PORT(.55, .38, 1.6))
# 5 1793, habit, rounding fear
shot('s05', 'p_earlymoney', 'film', A(4, 0, -.15), cut='zoom', cam0={'x': .5, 'y': .5, 'z': 1.1}, cam1={'x': .5, 'y': .5, 'z': 1.3})
beat('slam', Wd(4, 4, -.03), to=1793, **NUM, until=A(4, 1, -.1))
beat('punch', A(4, 3, .2), shot='s05', level=1.25)
# 6-7 final order; last struck Philadelphia 2025
shot('s06', PRESS, 'film', A(5, 0, -.15), cut='whip', cam0=PORT(.45, .55, 1.15), cam1=PORT(.45, .55, 1.35))
beat('moment', A(6, 0, .3), what='grade', shot='s06', bright=.55, sat=.35, d=.6)
beat('slam', Wd(6, 9, -.03), to=2025, **NUM, until=A(7, 0, -.1))
# 8 OPEN LOOP 2
shot('s07', NIC, 'film', A(7, 0, -.1), cut='flash', cam0=PORT(.33, .33, 1.35), cam1=PORT(.33, .33, 1.55))
beat('shake', A(7, 0, .8), k=.5)
# 9 nickel costs more than 5 cents
shot('s08', NIC, 'film', A(8, 0, -.15), cut='zoom', cam0=PORT(.33, .35, 1.1), cam1=PORT(.33, .35, 1.3))
beat('circle', A(8, 1, .1), shot='s08', c=c('nickel', [.33, .33]), r=[170, 210], until=A(9, 0, -.1))
# 10 PAYOFF
shot('MA', 'p_mirage', 'film', A(9, 0, -.15), cut='zoom', cam0={'x': .62, 'y': .35, 'z': 1.1}, cam1={'x': .62, 'y': .3, 'z': 1.3}, shim=[1.0], shimRect=[.3, 0, .75, .55])
shot('MB', 'p_mirage_empty', 'film', A(9, 1, -.05), cut='flash', depthOf='p_mirage', cam0={'x': .58, 'y': .33, 'z': 1.3}, cam1={'x': .5, 'y': .45, 'z': 1.1}, shim=[.6], shimRect=[.3, 0, .75, .55])
beat('punch', A(9, 1, 1.0), shot='MB', level=1.2)
# 11 114 billion pennies
shot('s09', JAR, 'film', A(10, 0, -.15), cut='whip', cam0=PORT(.55, .4, 1.1), cam1=PORT(.55, .4, 1.3))
beat('count', Wd(10, 1, -.05), to=114, suffix='B', **NUM, until=A(11, 0, -.4))
# 12 Bill
shot('s10', JAR, 'soft', A(11, 0, -.35), cam0=PORT(.5, .5, 1.12), cam1={'z': 1.18})
beat('moment', A(11, 0, -.3), what='char', shot='s10', who='c_bill', side='M', lines=[11], grow=A(11, 0, .8), leave=A(12, 0, -.25))
# 13 comment
shot('s11', LED, 'film', A(12, 0, -.15), cut='zoom', cam0=PORT(.7, .35, 1.2), cam1=PORT(.7, .35, 1.35))
beat('punch', A(12, 0, .8), shot='s11', level=1.25)
shot('ZZ', 'wallet_desk', 'soft', A(13, 0, -.15), cut='zoom', cam0={'x': .55, 'y': .58, 'z': 1.15}, cam1={'x': .55, 'y': .58, 'z': 1.3})
beat('moment', A(13, 0, 0), what='follow', btn=A(13, 0, .5), click=Wd(13, 4, .1), y=330)

SH = [{k: v for k, v in s.items() if v is not None} for s in SH]
json.dump({"shots": SH, "beats": BT}, open(os.path.join(HERE, "shots.json"), "w"), ensure_ascii=False, indent=1)
print(LANG, len(SH), "shots", len(BT), "beats")
