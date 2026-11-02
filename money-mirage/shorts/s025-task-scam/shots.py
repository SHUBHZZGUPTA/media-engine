# Money Mirage Short s025 (task scams): whole shot plan, native portrait, data for build.py --port.
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
TXT, LIK, LAD, WAL = P('ts_text', 'wallet_desk'), P('ts_likes', 'wallet_desk'), P('ts_ladder', 'coin_spin'), P('ts_wallet', 'wallet_desk')
# 1 HOOK
shot('s00', TXT, 'film', A(0), cam0=PORT(.58, .4, 1.15), cam1=PORT(.6, .42, 1.35))
beat('card', {'abs': 0.12}, text='$ PER *LIKE?*', y=280, size=140, blur=True, until={'abs': 2.2})
beat('circle', A(0, 0, .3), shot='s00', c=c('bubble', [.6, .43]), r=[170, 90], col='#FFC23A', until=A(0, 1, -.1))
shot('s01', LIK, 'film', A(0, 1, -.1), cut='whip', cam0=PORT(.52, .32, 1.15), cam1=PORT(.52, .3, 1.35))
beat('punch', A(0, 2, .3), shot='s01', level=1.3)
# 2 FTC: task scam
shot('s02', 'fc_badge', 'film', A(1, 0, -.15), cut='zoom', cam0=PORT(.5, .4, 1.1), cam1=PORT(.5, .38, 1.3))
beat('punch', A(1, 2, .3), shot='s02', level=1.25)
# 3 sets of forty, earnings climbing
shot('s03', LIK, 'film', A(2, 0, -.15), cut='zoomIn', cam0=PORT(.5, .35, 1.3), cam1=PORT(.53, .3, 1.55))
beat('count', Wd(2, 9, -.05), to=40, **NUM, until=A(2, 2, -.1))
beat('circle', A(2, 2, .2), shot='s03', c=c('phone', [.53, .3]), r=[230, 300], until=A(3, 0, -.1))
# 4 withdraw, it works
shot('s04', 'coin_spin', 'film', A(3, 0, -.15), cut='whip', cam0=PORT(.5, .45, 1.15), cam1=PORT(.5, .45, 1.35))
beat('punch', A(3, 1, .1), shot='s04', level=1.3)
# 5 Goldie
shot('s05', 'coin_spin', 'soft', A(4, 0, -.35), cam0=PORT(.5, .5, 1.12), cam1={'z': 1.18})
beat('moment', A(4, 0, -.3), what='char', shot='s05', who='c_goldie', side='M', lines=[4], shrink=A(4, 1, .4), leave=A(5, 0, -.25))
# 6 double task, deposit, crypto
shot('s06', LAD, 'film', A(5, 0, -.15), cut='zoom', cam0=PORT(.3, .55, 1.15), cam1=PORT(.35, .4, 1.35))
beat('punch', A(5, 2, .4), shot='s06', level=1.25)
beat('circle', A(5, 3, .1), shot='s06', c=c('climber', [.25, .45]), r=[150, 230], col='#FFC23A', until=A(6, 0, -.1))
# 7 each level more; never real (OPEN LOOP 2 feel)
shot('s07', LAD, 'film', A(6, 0, -.1), cut='flash', cam0=PORT(.5, .5, 1.2), cam1=PORT(.5, .2, 1.5))
beat('moment', A(6, 2, .1), what='grade', shot='s07', bright=.55, sat=.4, d=.6)
# 8 5,000 -> 20,000 reports
shot('s08', TXT, 'film', A(7, 0, -.15), cut='whip', cam0=PORT(.55, .4, 1.2), cam1=PORT(.6, .42, 1.45))
beat('count', Wd(7, 4, -.05), to=5000, **NUM, until=A(7, 2, -.1))
beat('slam', Wd(7, 11, -.03), to=20000, **NUM, until=A(8, 0, -.2))
beat('shake', Wd(7, 11, .05), k=.4)
# 9 BBB: typical loss $2,300
shot('s09', WAL, 'film', A(8, 0, -.15), cut='zoom', cam0=PORT(.4, .4, 1.1), cam1=PORT(.38, .4, 1.3))
beat('count', Wd(8, 11, -.05), to=2300, prefix='$', **NUM, until=A(9, 0, -.1))
beat('circle', A(8, 2, .5), shot='s09', c=c('wallet', [.33, .4]), r=[260, 170], until=A(9, 0, -.1))
# 10 PAYOFF
shot('MA', 'p_mirage', 'film', A(9, 0, -.15), cut='zoom', cam0={'x': .62, 'y': .35, 'z': 1.1}, cam1={'x': .62, 'y': .3, 'z': 1.3}, shim=[1.0], shimRect=[.3, 0, .75, .55])
shot('MB', 'p_mirage_empty', 'film', A(9, 1, -.05), cut='flash', depthOf='p_mirage', cam0={'x': .58, 'y': .33, 'z': 1.3}, cam1={'x': .5, 'y': .45, 'z': 1.1}, shim=[.6], shimRect=[.3, 0, .75, .55])
beat('punch', A(9, 1, 1.0), shot='MB', level=1.2)
# 11 never pay to get paid
shot('s10', TXT, 'film', A(10, 0, -.15), cut='whip', cam0=PORT(.6, .43, 1.3), cam1=PORT(.6, .43, 1.55))
beat('punch', A(10, 1, .05), shot='s10', level=1.3)
# 12 Bill
shot('s11', WAL, 'soft', A(11, 0, -.35), cam0=PORT(.5, .5, 1.12), cam1={'z': 1.18})
beat('moment', A(11, 0, -.3), what='char', shot='s11', who='c_bill', side='M', lines=[11], grow=A(11, 1, .2), leave=A(12, 0, -.25))
# 13 comment
shot('s12', LIK, 'film', A(12, 0, -.15), cut='zoom', cam0=PORT(.5, .32, 1.2), cam1=PORT(.5, .32, 1.35))
beat('punch', A(12, 0, 1.0), shot='s12', level=1.25)
shot('ZZ', 'wallet_desk', 'soft', A(13, 0, -.15), cut='zoom', cam0={'x': .55, 'y': .58, 'z': 1.15}, cam1={'x': .55, 'y': .58, 'z': 1.3})
beat('moment', A(13, 0, 0), what='follow', btn=A(13, 0, .5), click=Wd(13, 4, .1), y=330)

SH = [{k: v for k, v in s.items() if v is not None} for s in SH]
json.dump({"shots": SH, "beats": BT}, open(os.path.join(HERE, "shots.json"), "w"), ensure_ascii=False, indent=1)
print(LANG, len(SH), "shots", len(BT), "beats")
