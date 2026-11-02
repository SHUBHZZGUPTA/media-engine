# Money Mirage Short s026 (free trial auto-renew): whole shot plan, native portrait, data for build.py --port.
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
GIF, CAL, MAZ, CRD = P('ft_gift', 'wallet_desk'), P('ft_calendar', 'wallet_desk'), P('ft_maze', 'bank_vault_1700s'), P('ft_card', 'wallet_desk')
# 1 HOOK
shot('s00', GIF, 'film', A(0), cam0=PORT(.5, .4, 1.1), cam1=PORT(.55, .42, 1.3))
beat('card', {'abs': 0.12}, text='FREE*?*', y=280, size=170, blur=True, until={'abs': 2.0})
beat('count', Wd(0, 2, -.05), to=30, suffix=' days', **dict(NUM, y=560), until=A(0, 1, -.1))
beat('circle', A(0, 1, .2), shot='s00', c=c('card', [.8, .53]), r=[170, 110], until=A(0, 2, -.1))
beat('punch', A(0, 3, .1), shot='s00', level=1.3)
# 2 the day you forget
shot('s01', CAL, 'film', A(1, 0, -.15), cut='whip', cam0=PORT(.5, .3, 1.15), cam1=PORT(.47, .32, 1.4))
beat('circle', A(1, 1, .2), shot='s01', c=c('mark', [.46, .32]), r=[120, 120], until=A(2, 0, -.1))
# 3 trial ends, charged, renews
shot('s02', CRD, 'film', A(2, 0, -.15), cut='zoom', cam0=PORT(.5, .45, 1.1), cam1=PORT(.5, .43, 1.3))
beat('shake', A(2, 1, .1), k=.4)
beat('punch', A(2, 2, .3), shot='s02', level=1.3)
# 4 Goldie
shot('s03', GIF, 'soft', A(3, 0, -.35), cam0=PORT(.5, .5, 1.12), cam1={'z': 1.18})
beat('moment', A(3, 0, -.3), what='char', shot='s03', who='c_goldie', side='M', lines=[3], shrink=A(3, 1, .6), leave=A(4, 0, -.25))
# 5 FTC accused Amazon
shot('s04', 'fc_badge', 'film', A(4, 0, -.15), cut='zoomIn', cam0=PORT(.5, .4, 1.1), cam1=PORT(.5, .38, 1.35))
beat('punch', A(4, 1, .2), shot='s04', level=1.25)
shot('s05', CRD, 'film', A(4, 3, -.1), cut='whip', cam0=PORT(.4, .4, 1.25), cam1=PORT(.4, .45, 1.45))
# 6 "Iliad" (OPEN LOOP-ish)
shot('s06', MAZ, 'film', A(5, 0, -.15), cut='zoom', cam0=PORT(.35, .75, 1.15), cam1=PORT(.65, .25, 1.45))
beat('punch', A(5, 1, .3), shot='s06', level=1.3)
beat('circle', A(5, 2, .2), shot='s06', c=c('door', [.68, .21]), r=[120, 110], col='#FFC23A', until=A(6, 0, -.1))
# 7 $2.5B settlement, $1.5B refunds
shot('s07', 'bank_vault_1700s', 'film', A(6, 0, -.15), cut='whip', cam0=PORT(.5, .5, 1.15), cam1=PORT(.5, .45, 1.35))
beat('count', Wd(6, 8, -.05), to=2.5, dec=1, prefix='$', suffix='B', **NUM, until=A(6, 2, -.1))
beat('count', Wd(6, 12, -.05), to=1.5, dec=1, prefix='$', suffix='B', **NUM, until=A(7, 0, -.2))
beat('punch', A(6, 2, .2), shot='s07', level=1.25)
# 8 PAYOFF
shot('MA', 'p_mirage', 'film', A(7, 0, -.15), cut='zoom', cam0={'x': .62, 'y': .35, 'z': 1.1}, cam1={'x': .62, 'y': .3, 'z': 1.3}, shim=[1.0], shimRect=[.3, 0, .75, .55])
shot('MB', 'p_mirage_empty', 'film', A(7, 2, -.1), cut='flash', depthOf='p_mirage', cam0={'x': .58, 'y': .33, 'z': 1.3}, cam1={'x': .5, 'y': .45, 'z': 1.1}, shim=[.6], shimRect=[.3, 0, .75, .55])
beat('punch', A(7, 2, .5), shot='MB', level=1.2)
# 9 the fix
shot('s08', CAL, 'film', A(8, 0, -.15), cut='whip', cam0=PORT(.75, .2, 1.2), cam1=PORT(.6, .28, 1.4))
beat('circle', A(8, 1, .2), shot='s08', c=c('mark', [.46, .32]), r=[120, 120], col='#FFC23A', until=A(8, 2, -.1))
beat('punch', A(8, 2, .4), shot='s08', level=1.25)
# 10 Bill
shot('s09', CRD, 'soft', A(9, 0, -.35), cam0=PORT(.5, .5, 1.12), cam1={'z': 1.18})
beat('moment', A(9, 0, -.3), what='char', shot='s09', who='c_bill', side='M', lines=[9], grow=A(9, 0, .8), leave=A(10, 0, -.25))
# 11 comment
shot('s10', GIF, 'film', A(10, 0, -.15), cut='zoom', cam0=PORT(.55, .4, 1.2), cam1=PORT(.55, .4, 1.35))
beat('punch', A(10, 0, 1.0), shot='s10', level=1.25)
shot('ZZ', 'wallet_desk', 'soft', A(11, 0, -.15), cut='zoom', cam0={'x': .55, 'y': .58, 'z': 1.15}, cam1={'x': .55, 'y': .58, 'z': 1.3})
beat('moment', A(11, 0, 0), what='follow', btn=A(11, 0, .5), click=Wd(11, 4, .1), y=330)

SH = [{k: v for k, v in s.items() if v is not None} for s in SH]
json.dump({"shots": SH, "beats": BT}, open(os.path.join(HERE, "shots.json"), "w"), ensure_ascii=False, indent=1)
print(LANG, len(SH), "shots", len(BT), "beats")
