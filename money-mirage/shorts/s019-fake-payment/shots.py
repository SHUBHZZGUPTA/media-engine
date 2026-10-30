# Money Mirage Short s019 (fake payment screenshot): whole shot plan, native portrait, data for build.py --port.
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
CTR, APP, RUSH, CHK = P('fp_counter', 'red_phone'), P('fp_app', 'wire_terminal'), P('fp_rush', 'uk_high_street_1991'), P('fp_check', 'wallet_desk')
# 1 HOOK
shot('s00', CTR, 'film', A(0), cam0=PORT(.42, .38, 1.2), cam1=PORT(.42, .38, 1.35))
beat('card', {'abs': 0.12}, text='PAID ✅ *?*', y=280, size=140, blur=True, until={'abs': 2.2})
beat('punch', A(0, 0, .8), shot='s00', level=1.2)
beat('count', Wd(0, 9, -.05), to=200, **dict(NUM, y=560), until=A(0, 2, -.1))
beat('punch', A(0, 2, .3), shot='s00', level=1.35)
# 2 payment successful; Punjab arrests
shot('s01', APP, 'film', A(1, 0, -.15), cut='whip', cam0=PORT(.5, .3, 1.2), cam1=PORT(.5, .27, 1.4))
beat('circle', A(1, 1, .1), shot='s01', c=c('app_tick', [.5, .25]), r=[150, 150], col='#FFC23A', until=A(1, 3, -.1))
beat('punch', A(1, 2, .2), shot='s01', level=1.45)
shot('s02', 'treasury_courtyard', 'film', A(1, 3, -.1), cut='zoom', cam0={'x': .45, 'y': .45, 'z': 1.15}, cam1={'x': .5, 'y': .45, 'z': 1.3})
# 3 Bill
shot('s03', CTR, 'soft', A(2, 0, -.35), cam0=PORT(.5, .5, 1.12), cam1={'z': 1.18})
beat('moment', A(2, 0, -.3), what='char', shot='s03', who='c_bill', side='M', lines=[2], shrink=A(2, 0, .9), leave=A(3, 0, -.25))
# 4 OPEN LOOP 1
shot('s04', CTR, 'film', A(3, 0, -.15), cut='zoomIn', cam0=PORT(.42, .38, 1.4), cam1=PORT(.4, .36, 1.6))
# 5-6 fake app / edited screenshot / fake SMS
shot('s05', APP, 'film', A(4, 0, -.15), cut='zoom', cam0=PORT(.5, .3, 1.1), cam1=PORT(.5, .28, 1.3))
beat('punch', A(4, 1, .2), shot='s05', level=1.3)
shot('s06', APP, 'film', A(5, 0, -.1), cut='whip', cam0=PORT(.55, .35, 1.4), cam1=PORT(.5, .3, 1.55))
beat('punch', A(5, 1, .3), shot='s06', level=1.25)
# 7 Delhi 200
shot('s07', RUSH, 'film', A(6, 0, -.15), cut='zoom', cam0=PORT(.5, .3, 1.1), cam1=PORT(.55, .3, 1.3))
beat('moment', A(6, 1, .5), what='grade', shot='s07', bright=.6, sat=.4, d=.6)
# 8 OPEN LOOP 2
shot('s08', RUSH, 'film', A(7, 0, -.1), cut='flash', cam0=PORT(.6, .25, 1.35), cam1=PORT(.62, .22, 1.55))
beat('shake', A(7, 0, .9), k=.5)
# 9 rush, queue, no time
shot('s09', RUSH, 'film', A(8, 0, -.12), cut='whip', cam0=PORT(.35, .4, 1.2), cam1=PORT(.4, .4, 1.4), handheld=.12)
beat('punch', A(8, 1, .1), shot='s09', level=1.3); beat('shake', A(8, 2, .3), k=.4)
# 10 PAYOFF
shot('MA', 'p_mirage', 'film', A(9, 0, -.15), cut='zoom', cam0={'x': .62, 'y': .35, 'z': 1.1}, cam1={'x': .62, 'y': .3, 'z': 1.3}, shim=[1.0], shimRect=[.3, 0, .75, .55])
shot('MB', 'p_mirage_empty', 'film', A(9, 1, -.05), cut='flash', depthOf='p_mirage', cam0={'x': .58, 'y': .33, 'z': 1.3}, cam1={'x': .5, 'y': .45, 'z': 1.1}, shim=[.6], shimRect=[.3, 0, .75, .55])
# 11 half of real-time payments
shot('s10', 'trading_room', 'film', A(10, 0, -.15), cut='zoom', cam0={'x': .45, 'y': .3, 'z': 1.25}, cam1={'x': .45, 'y': .32, 'z': 1.45})
beat('punch', A(10, 1, .2), shot='s10', level=1.25)
# 12 Goldie
shot('s11', 'vault_full', 'soft', A(11, 0, -.35), cam0={'x': .5, 'y': .5, 'z': 1.12}, cam1={'z': 1.18})
beat('moment', A(11, 0, -.3), what='char', shot='s11', who='c_goldie', side='M', lines=[11], grow=A(11, 1, 0), leave=A(12, 0, -.25))
# 13 check your app, not theirs
shot('s12', CHK, 'film', A(12, 0, -.15), cut='zoomIn', cam0=PORT(.5, .5, 1.1), cam1=PORT(.53, .5, 1.35))
beat('circle', A(12, 1, .2), shot='s12', c=c('own_phone', [.53, .5]), r=[150, 120], col='#FFC23A', until=A(13, 0, -.1))
# 14 comment
shot('s13', CTR, 'film', A(13, 0, -.15), cut='zoom', cam0=PORT(.45, .4, 1.2), cam1=PORT(.45, .4, 1.35))
shot('ZZ', 'wallet_desk', 'soft', A(14, 0, -.15), cut='zoom', cam0={'x': .55, 'y': .58, 'z': 1.15}, cam1={'x': .55, 'y': .58, 'z': 1.3})
beat('moment', A(14, 0, 0), what='follow', btn=A(14, 0, .5), click=Wd(14, 4, .1), y=330)

SH = [{k: v for k, v in s.items() if v is not None} for s in SH]
json.dump({"shots": SH, "beats": BT}, open(os.path.join(HERE, "shots.json"), "w"), ensure_ascii=False, indent=1)
print(LANG, len(SH), "shots", len(BT), "beats")
