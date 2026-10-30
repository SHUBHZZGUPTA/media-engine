# Money Mirage Short s017 (pig butchering): whole shot plan, native portrait, data for build.py --port.
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
TXT, CHAT, PIG, APP, CMP = P('pb_text', 'red_phone'), P('pb_chat', 'tv_1971'), P('pb_pig', 'coin_spin'), P('pb_app', 'trading_room'), P('pb_compound', 'dealing_room_1992')
C = json.load(open(os.path.join(HERE, 'coords.json'))) if os.path.exists(os.path.join(HERE, 'coords.json')) else {}
c = lambda k, d: C.get(k, d)
# 1 HOOK
shot('s00', TXT, 'film', A(0), cam0=PORT(.6, .48, 1.2), cam1=PORT(.62, .5, 1.35))
beat('card', {'abs': 0.12}, text='"Hi… *wrong number*"', y=280, size=118, blur=True, until={'abs': 2.2})
beat('count', Wd(0, 3, -.05), to=7, prefix='$', suffix='B', align='center', y=560, size=170, until=A(0, 2, -.1))
beat('punch', A(0, 2, .3), shot='s00', level=1.3)
beat('circle', A(0, 2, .6), shot='s00', c=c('text_phone', [.45, .5]), r=[150, 110], col='#FFC23A', until=A(1, 0, -.1))
# 2 stranger, chats, savings gone
shot('s01', CHAT, 'film', A(1, 0, -.15), cut='whip', cam0=PORT(.5, .35, 1.1), cam1=PORT(.55, .35, 1.3))
beat('moment', A(1, 2, .1), what='grade', shot='s01', bright=.55, sat=.35, d=.6)
# 3 pig butchering
shot('s02', PIG, 'film', A(2, 0, -.15), cut='zoom', cam0=PORT(.4, .45, 1.1), cam1=PORT(.38, .5, 1.35))
beat('punch', A(2, 1, .3), shot='s02', level=1.3); beat('shake', A(2, 1, .4), k=.4)
# 4 Goldie
shot('s03', PIG, 'soft', A(3, 0, -.35), cam0=PORT(.5, .5, 1.12), cam1={'z': 1.18})
beat('moment', A(3, 0, -.3), what='char', shot='s03', who='c_goldie', side='M', lines=[3], grow=A(3, 1, 0), leave=A(4, 0, -.25))
# 5 OPEN LOOP 1
shot('s04', PIG, 'film', A(4, 0, -.15), cut='zoomIn', cam0=PORT(.38, .5, 1.3), cam1=PORT(.38, .52, 1.55))
# 6 patient, chats, friendship, romance
shot('s05', CHAT, 'film', A(5, 0, -.15), cut='whip', cam0=PORT(.55, .35, 1.2), cam1=PORT(.6, .3, 1.4))
beat('punch', A(5, 3, .2), shot='s05', level=1.35)
# 7 crypto app tip
shot('s06', APP, 'film', A(6, 0, -.15), cut='zoom', cam0=PORT(.55, .4, 1.1), cam1=PORT(.58, .35, 1.3))
beat('circle', A(6, 1, .4), shot='s06', c=c('app_chart', [.6, .33]), r=[160, 240], col='#FFC23A', until=A(7, 0, -.1))
# 8 invest a little, huge profits, withdraw some
shot('s07', APP, 'film', A(7, 0, -.12), cut='zoomIn', cam0=PORT(.58, .35, 1.3), cam1=PORT(.6, .32, 1.5))
beat('punch', A(7, 1, .3), shot='s07', level=1.35)
# 9 OPEN LOOP 2
shot('s08', PIG, 'film', A(8, 0, -.1), cut='flash', cam0=PORT(.6, .25, 1.3), cam1=PORT(.6, .2, 1.5))
beat('shake', A(8, 0, .8), k=.6)
# 10 invest more, tax to cash out
shot('s09', APP, 'film', A(9, 0, -.15), cut='whip', cam0=PORT(.55, .4, 1.2), cam1=PORT(.55, .38, 1.35))
beat('moment', A(9, 2, .3), what='grade', shot='s09', bright=.5, sat=.3, d=.6)
# 11 PAYOFF
shot('MA', 'p_mirage', 'film', A(10, 0, -.15), cut='zoom', cam0={'x': .62, 'y': .35, 'z': 1.1}, cam1={'x': .62, 'y': .3, 'z': 1.3}, shim=[1.0], shimRect=[.3, 0, .75, .55])
shot('MB', 'p_mirage_empty', 'film', A(10, 1, -.05), cut='flash', depthOf='p_mirage', cam0={'x': .58, 'y': .33, 'z': 1.3}, cam1={'x': .5, 'y': .45, 'z': 1.1}, shim=[.6], shimRect=[.3, 0, .75, .55])
# 12 prosecutors charged a ring with bonuses
shot('s10', CMP, 'film', A(11, 0, -.15), cut='zoom', cam0=PORT(.5, .45, 1.1), cam1=PORT(.5, .45, 1.3))
beat('punch', A(11, 2, .3), shot='s10', level=1.25)
# 13 Bill twist
shot('s11', CMP, 'soft', A(12, 0, -.35), cam0=PORT(.5, .5, 1.12), cam1={'z': 1.18})
beat('moment', A(12, 0, -.3), what='char', shot='s11', who='c_bill', side='M', lines=[12], shrink=A(12, 0, .9), leave=A(13, 0, -.25))
# 14 loop: you're the pig
shot('s12', PIG, 'film', A(13, 0, -.15), cut='zoomIn', cam0=PORT(.4, .45, 1.1), cam1=PORT(.38, .5, 1.4))
beat('punch', A(13, 2, .2), shot='s12', level=1.4); beat('shake', A(13, 2, .3), k=.5)
# 15 comment
shot('s13', TXT, 'film', A(14, 0, -.15), cut='zoom', cam0=PORT(.45, .5, 1.2), cam1=PORT(.45, .5, 1.35))
shot('ZZ', 'wallet_desk', 'soft', A(15, 0, -.15), cut='zoom', cam0={'x': .55, 'y': .58, 'z': 1.15}, cam1={'x': .55, 'y': .58, 'z': 1.3})
beat('moment', A(15, 0, 0), what='follow', btn=A(15, 0, .5), click=Wd(15, 4, .1), y=330)

SH = [{k: v for k, v in s.items() if v is not None} for s in SH]
json.dump({"shots": SH, "beats": BT}, open(os.path.join(HERE, "shots.json"), "w"), ensure_ascii=False, indent=1)
print(LANG, len(SH), "shots", len(BT), "beats")
