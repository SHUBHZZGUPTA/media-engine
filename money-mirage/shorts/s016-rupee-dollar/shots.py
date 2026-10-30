# Money Mirage Short s016 (1 rupee = 1 dollar myth): whole shot plan, native portrait, data for build.py --port.
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
GP, Y47, STAIRS, PORTP = P('rp_grandpa', 'wallet_desk'), P('rp_1947', 'deposit_shop'), P('rp_stairs', 'note_falling'), P('rp_port', 'p_ship')
# 1 HOOK
shot('s00', GP, 'film', A(0), cam0=PORT(.45, .42, 1.15), cam1=PORT(.5, .4, 1.3))
beat('card', {'abs': 0.12}, text='₹1 = $1 *?*', y=280, size=140, blur=True, until={'abs': 2.4})
beat('punch', A(0, 1, .3), shot='s00', level=1.2)
shot('s01', 'euro_notes_pile', 'film', A(0, 2, -.1), cut='whip', cam0={'x': .45, 'y': .45, 'z': 1.2}, cam1={'x': .5, 'y': .45, 'z': 1.4})
beat('count', Wd(0, 15, -.05), to=95, **NUM, until=A(0, 3, .4))
shot('s02', GP, 'film', A(0, 3, -.1), cut='zoomIn', cam0=PORT(.5, .42, 1.3), cam1=PORT(.5, .42, 1.5))
# 2 Bill
shot('s03', 'euro_notes_pile', 'soft', A(1, 0, -.35), cam0={'x': .5, 'y': .5, 'z': 1.12}, cam1={'z': 1.18})
beat('moment', A(1, 0, -.3), what='char', shot='s03', who='c_bill', side='M', lines=[1], shrink=A(1, 1, .3), leave=A(2, 0, -.25))
# 3 OPEN LOOP 1
shot('s04', GP, 'film', A(2, 0, -.15), cut='whip', cam0=PORT(.35, .4, 1.35), cam1=PORT(.3, .4, 1.55))
# 4 1947: never; 3.3
shot('s05', Y47, 'film', A(3, 0, -.15), cut='zoom', cam0=PORT(.5, .42, 1.1), cam1=PORT(.5, .45, 1.3))
beat('slam', Wd(3, 1, -.03), to=1947, **NUM, until=A(3, 2, -.1))
beat('count', Wd(3, 9, -.05), to=3.3, dec=1, prefix='₹', **NUM, until=A(4, 0, -.1))
# 5 tied to the pound
shot('s06', 'boe_hall_1808', 'film', A(4, 0, -.15), cut='whip', cam0={'x': .45, 'y': .4, 'z': 1.2}, cam1={'x': .5, 'y': .42, 'z': 1.4})
beat('punch', A(4, 1, .2), shot='s06', level=1.25)
# 6 1966 devalued to 7.5
shot('s07', STAIRS, 'film', A(5, 0, -.15), cut='zoom', cam0=PORT(.35, .3, 1.15), cam1=PORT(.5, .55, 1.35))
beat('slam', Wd(5, 1, -.03), to=1966, **NUM, until=A(5, 1, -.1))
beat('punch', A(5, 2, .4), shot='s07', level=1.3)
# 7 1991 crisis; past 30
shot('s08', 'vault_empty', 'film', A(6, 0, -.15), cut='whip', cam0={'x': .3, 'y': .45, 'z': 1.25}, cam1={'x': .3, 'y': .45, 'z': 1.45})
beat('slam', Wd(6, 1, -.03), to=1991, **NUM, until=A(6, 2, -.1))
beat('moment', A(6, 1, .6), what='grade', shot='s08', bright=.55, sat=.35, d=.6)
beat('count', Wd(6, 12, -.05), to=30, prefix='₹', **NUM, until=A(7, 0, -.1))
# 8 OPEN LOOP 2
shot('s09', STAIRS, 'film', A(7, 0, -.1), cut='flash', cam0=PORT(.5, .6, 1.4), cam1=PORT(.5, .7, 1.6))
beat('shake', A(7, 0, .9), k=.5)
# 9 exports cheaper
shot('s10', PORTP, 'film', A(8, 0, -.15), cut='zoom', cam0=PORT(.5, .4, 1.1), cam1=PORT(.55, .4, 1.3))
beat('punch', A(8, 1, .3), shot='s10', level=1.25)
# 10 PAYOFF
shot('MA', 'p_mirage', 'film', A(9, 0, -.15), cut='zoom', cam0={'x': .62, 'y': .35, 'z': 1.1}, cam1={'x': .62, 'y': .3, 'z': 1.3}, shim=[1.0], shimRect=[.3, 0, .75, .55])
shot('MB', 'p_mirage_empty', 'film', A(9, 1, -.05), cut='flash', depthOf='p_mirage', cam0={'x': .58, 'y': .33, 'z': 1.3}, cam1={'x': .5, 'y': .45, 'z': 1.1}, shim=[.6], shimRect=[.3, 0, .75, .55])
# 11 loop: record low, your income vs the dollar
shot('s11', GP, 'film', A(10, 0, -.15), cut='zoomIn', cam0=PORT(.5, .45, 1.1), cam1=PORT(.5, .42, 1.35))
beat('punch', A(10, 2, .5), shot='s11', level=1.25)
# 12 comment
shot('s12', Y47, 'film', A(11, 0, -.15), cut='zoom', cam0=PORT(.5, .45, 1.2), cam1=PORT(.5, .45, 1.35))
beat('punch', A(11, 0, .9), shot='s12', level=1.25)
shot('ZZ', 'wallet_desk', 'soft', A(12, 0, -.15), cut='zoom', cam0={'x': .55, 'y': .58, 'z': 1.15}, cam1={'x': .55, 'y': .58, 'z': 1.3})
beat('moment', A(12, 0, 0), what='follow', btn=A(12, 0, .5), click=Wd(12, 4, .1), y=330)

SH = [{k: v for k, v in s.items() if v is not None} for s in SH]
json.dump({"shots": SH, "beats": BT}, open(os.path.join(HERE, "shots.json"), "w"), ensure_ascii=False, indent=1)
print(LANG, len(SH), "shots", len(BT), "beats")
