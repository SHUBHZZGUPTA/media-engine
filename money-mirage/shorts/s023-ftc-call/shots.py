# Money Mirage Short s023 (fake-FTC deactivation call): whole shot plan, native portrait, data for build.py --port.
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
PH, BADGE, COP, DEP = P('fc_phone', 'red_phone'), P('fc_badge', 'red_phone'), P('fc_cop', 'phones_offhook'), P('fc_deposit', 'wallet_desk')
# 1 HOOK
shot('s00', PH, 'film', A(0), cam0=PORT(.55, .48, 1.2), cam1=PORT(.55, .5, 1.4))
beat('card', {'abs': 0.12}, text='"FTC" *CALLING*', y=280, size=130, blur=True, until={'abs': 2.2})
beat('punch', A(0, 1, .3), shot='s00', level=1.25)
shot('s01', BADGE, 'film', A(0, 2, -.1), cut='whip', cam0=PORT(.32, .3, 1.2), cam1=PORT(.3, .3, 1.4))
beat('punch', A(0, 3, .3), shot='s01', level=1.35)
# 2 FTC warned Oct 22
shot('s02', 'treasury_courtyard', 'film', A(1, 0, -.15), cut='zoom', cam0={'x': .45, 'y': .45, 'z': 1.15}, cam1={'x': .5, 'y': .45, 'z': 1.3})
beat('slam', Wd(1, 9, -.03), to=22, prefix='OCT ', **NUM, until=A(2, 0, -.1))
# 3 phone in your name, deactivated
shot('s03', PH, 'film', A(2, 0, -.15), cut='whip', cam0=PORT(.55, .45, 1.1), cam1=PORT(.55, .5, 1.3))
beat('circle', A(2, 1, .2), shot='s03', c=c('phone', [.55, .5]), r=[200, 150], col='#FFC23A', until=A(2, 2, -.1))
beat('moment', A(2, 2, .6), what='grade', shot='s03', bright=.5, sat=.3, d=.5)
# 4 Bill
shot('s04', PH, 'soft', A(3, 0, -.35), cam0=PORT(.5, .5, 1.12), cam1={'z': 1.18})
beat('moment', A(3, 0, -.3), what='char', shot='s04', who='c_bill', side='M', lines=[3], shrink=A(3, 1, .1), leave=A(4, 0, -.25))
# 5 OPEN LOOP 1
shot('s05', BADGE, 'film', A(4, 0, -.15), cut='zoomIn', cam0=PORT(.3, .3, 1.35), cam1=PORT(.3, .3, 1.6))
# 6 fake police, arrest
shot('s06', COP, 'film', A(5, 0, -.15), cut='zoom', cam0=PORT(.5, .4, 1.1), cam1=PORT(.55, .4, 1.3))
beat('circle', A(5, 0, 1.0), shot='s06', c=c('cop', [.55, .3]), r=[200, 220], until=A(5, 1, -.1))
beat('punch', A(5, 1, .4), shot='s06', level=1.3)
# 7 OPEN LOOP 2
shot('s07', DEP, 'film', A(6, 0, -.1), cut='flash', cam0=PORT(.45, .4, 1.35), cam1=PORT(.5, .45, 1.55))
beat('shake', A(6, 0, .8), k=.5)
# 8 security deposit
shot('s08', DEP, 'film', A(7, 0, -.15), cut='zoom', cam0=PORT(.55, .5, 1.1), cam1=PORT(.55, .5, 1.3))
beat('circle', A(7, 1, .3), shot='s08', c=c('notes', [.55, .5]), r=[180, 150], col='#FFC23A', until=A(8, 0, -.1))
# 9 PAYOFF
shot('MA', 'p_mirage', 'film', A(8, 0, -.15), cut='zoom', cam0={'x': .62, 'y': .35, 'z': 1.1}, cam1={'x': .62, 'y': .3, 'z': 1.3}, shim=[1.0], shimRect=[.3, 0, .75, .55])
shot('MB', 'p_mirage_empty', 'film', A(8, 1, -.05), cut='flash', depthOf='p_mirage', cam0={'x': .58, 'y': .33, 'z': 1.3}, cam1={'x': .5, 'y': .45, 'z': 1.1}, shim=[.6], shimRect=[.3, 0, .75, .55])
beat('punch', A(8, 1, 1.0), shot='MB', level=1.2)
# 10 FTC says: never money, phone, secrecy
shot('s09', 'treasury_courtyard', 'film', A(9, 0, -.15), cut='whip', cam0={'x': .5, 'y': .4, 'z': 1.2}, cam1={'x': .5, 'y': .4, 'z': 1.35})
beat('punch', A(9, 1, .2), shot='s09', level=1.2)
beat('punch', A(9, 2, .2), shot='s09', level=1.35)
# 11 loop: deactivate the call
shot('s10', PH, 'film', A(10, 0, -.15), cut='zoomIn', cam0=PORT(.55, .5, 1.1), cam1=PORT(.55, .5, 1.4))
beat('moment', A(10, 1, .1), what='grade', shot='s10', bright=.4, sat=.3, d=.4)
# 12 comment
shot('s11', COP, 'film', A(11, 0, -.15), cut='zoom', cam0=PORT(.5, .4, 1.2), cam1=PORT(.5, .4, 1.35))
beat('punch', A(11, 0, 1.0), shot='s11', level=1.25)
shot('ZZ', 'wallet_desk', 'soft', A(12, 0, -.15), cut='zoom', cam0={'x': .55, 'y': .58, 'z': 1.15}, cam1={'x': .55, 'y': .58, 'z': 1.3})
beat('moment', A(12, 0, 0), what='follow', btn=A(12, 0, .5), click=Wd(12, 4, .1), y=330)

SH = [{k: v for k, v in s.items() if v is not None} for s in SH]
json.dump({"shots": SH, "beats": BT}, open(os.path.join(HERE, "shots.json"), "w"), ensure_ascii=False, indent=1)
print(LANG, len(SH), "shots", len(BT), "beats")
