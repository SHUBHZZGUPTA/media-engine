# Money Mirage Short s020 (Newton and the South Sea Bubble): whole shot plan, native portrait, data for build.py --port.
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
STARS, ALLEY, DESK, CRASH = P('nb_stars', 'ny_office_window'), P('nb_alley', 'election_night_1997'), P('nb_desk', 'strict_friend'), P('nb_crash', 'note_falling')
# 1 HOOK
shot('s00', STARS, 'film', A(0), cam0=PORT(.5, .3, 1.15), cam1=PORT(.5, .22, 1.3))
beat('card', {'abs': 0.12}, text='GENIUS vs *BUBBLE*', y=280, size=120, blur=True, until={'abs': 2.2})
beat('count', Wd(0, 8, -.05), to=20000, prefix='£', **dict(NUM, y=560), until=A(0, 2, -.1))
beat('punch', A(0, 2, .3), shot='s00', level=1.3)
# 2 1720 London wants shares
shot('s01', ALLEY, 'film', A(1, 0, -.15), cut='whip', cam0=PORT(.5, .35, 1.1), cam1=PORT(.5, .35, 1.3), handheld=.1)
beat('slam', Wd(1, 1, -.03), to=1720, **NUM, until=A(1, 1, -.1))
# 3 £130 -> £1,000
shot('s02', ALLEY, 'film', A(2, 0, -.12), cut='zoomIn', cam0=PORT(.45, .3, 1.3), cam1=PORT(.4, .25, 1.55))
beat('count', Wd(2, 11, -.05), from_=130, to=1000, prefix='£', **NUM, until=A(3, 0, -.4))
# 4 Goldie
shot('s03', ALLEY, 'soft', A(3, 0, -.35), cam0=PORT(.5, .5, 1.12), cam1={'z': 1.18})
beat('moment', A(3, 0, -.3), what='char', shot='s03', who='c_goldie', side='M', lines=[3], shrink=A(3, 0, 1.0), leave=A(4, 0, -.25))
# 5 OPEN LOOP 1
shot('s04', STARS, 'film', A(4, 0, -.15), cut='whip', cam0=PORT(.5, .35, 1.3), cam1=PORT(.5, .32, 1.5))
# 6 sold early, tidy profit
shot('s05', DESK, 'film', A(5, 0, -.15), cut='zoom', cam0=PORT(.55, .4, 1.1), cam1=PORT(.6, .45, 1.3))
beat('punch', A(5, 2, .2), shot='s05', level=1.25)
# 7 prices climbing, friends richer
shot('s06', ALLEY, 'film', A(6, 0, -.15), cut='whip', cam0=PORT(.6, .3, 1.15), cam1=PORT(.65, .25, 1.35), handheld=.12)
beat('punch', A(6, 1, .4), shot='s06', level=1.3)
# 8 OPEN LOOP 2
shot('s07', DESK, 'film', A(7, 0, -.1), cut='flash', cam0=PORT(.3, .3, 1.35), cam1=PORT(.3, .28, 1.55))
beat('shake', A(7, 0, .9), k=.5)
# 9 bought back at double; burst
shot('s08', ALLEY, 'film', A(8, 0, -.15), cut='zoom', cam0=PORT(.5, .35, 1.2), cam1=PORT(.5, .3, 1.4))
shot('s09', CRASH, 'film', A(8, 2, -.1), cut='flash', cam0=PORT(.45, .45, 1.3), cam1=PORT(.45, .5, 1.1))
beat('shake', A(8, 2, .3), k=.6)
beat('moment', A(8, 2, .5), what='grade', shot='s09', bright=.55, sat=.3, d=.6)
# 10 lost a fortune; debate
shot('s10', DESK, 'film', A(9, 0, -.15), cut='zoomIn', cam0=PORT(.55, .45, 1.15), cam1=PORT(.6, .5, 1.35))
beat('moment', A(9, 0, .4), what='grade', shot='s10', bright=.6, sat=.4, d=.6)
# 11 PAYOFF
shot('MA', 'p_mirage', 'film', A(10, 0, -.15), cut='zoom', cam0={'x': .62, 'y': .35, 'z': 1.1}, cam1={'x': .62, 'y': .3, 'z': 1.3}, shim=[1.0], shimRect=[.3, 0, .75, .55])
shot('MB', 'p_mirage_empty', 'film', A(10, 1, -.05), cut='flash', depthOf='p_mirage', cam0={'x': .58, 'y': .33, 'z': 1.3}, cam1={'x': .5, 'y': .45, 'z': 1.1}, shim=[.6], shimRect=[.3, 0, .75, .55])
# 12 stars vs madness
shot('s11', STARS, 'film', A(11, 0, -.15), cut='zoom', cam0=PORT(.5, .2, 1.2), cam1=PORT(.5, .35, 1.05))
shot('s12', CRASH, 'film', A(11, 1, -.1), cut='whip', cam0=PORT(.45, .4, 1.2), cam1=PORT(.45, .42, 1.35))
# 13 Bill
shot('s13', CRASH, 'soft', A(12, 0, -.35), cam0=PORT(.5, .5, 1.12), cam1={'z': 1.18})
beat('moment', A(12, 0, -.3), what='char', shot='s13', who='c_bill', side='M', lines=[12], grow=A(12, 0, .5), leave=A(13, 0, -.25))
# 14 comment
shot('s14', ALLEY, 'film', A(13, 0, -.15), cut='zoom', cam0=PORT(.5, .35, 1.2), cam1=PORT(.5, .35, 1.35))
beat('punch', A(13, 0, 1.0), shot='s14', level=1.25)
shot('ZZ', 'wallet_desk', 'soft', A(14, 0, -.15), cut='zoom', cam0={'x': .55, 'y': .58, 'z': 1.15}, cam1={'x': .55, 'y': .58, 'z': 1.3})
beat('moment', A(14, 0, 0), what='follow', btn=A(14, 0, .5), click=Wd(14, 4, .1), y=330)

SH = [{k: v for k, v in s.items() if v is not None} for s in SH]
json.dump({"shots": SH, "beats": BT}, open(os.path.join(HERE, "shots.json"), "w"), ensure_ascii=False, indent=1)
print(LANG, len(SH), "shots", len(BT), "beats")
