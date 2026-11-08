# Money Mirage Short s031 (the $1M Big Maple Leaf coin, Berlin 2017): whole shot plan, native portrait 1080x1920, for build.py --port.
# English only (Shubham, 8 Nov 2026). Anchors: A(li, ci, off) = caption-chunk start; Wd(li, wi, off) = word start.
# New Codex plates are 1024x1536 portrait (cam x .5); each has a library fallback so the build never waits on Codex.
import json, os
HERE = os.getcwd(); LANG = json.load(open(os.path.join(HERE, 'episode.json'))).get('lang', 'en')
A = lambda li, ci=0, off=0.0: {'@': [li, ci, off]}
Wd = lambda li, wi, off=0.0: {'@w': [li, wi, off]}
SH = []; BT = []
def shot(id, img, look, at, cut='curve', cam0=None, cam1=None, keys=None, dScale=.3, **kw):
    SH.append(dict(id=id, img=img, look=look, at=at, cut=cut, cam0=cam0 or {'x': .5, 'y': .5, 'z': 1.05}, cam1=cam1 or {'z': 1.15}, keys=keys or [], dScale=dScale, **kw))
def beat(kind, at, **kw): BT.append(dict(kind=kind, at=at, **kw))
NUM = dict(align='center', y=250, size=170)
have = lambda p: os.path.exists(os.path.join(HERE, f'art/baked/{p}__film.jpg'))
# new plate -> (plate, cam x, cam y) with library fallback
def P(new, fb, fx, fy=.5): return (new, .5, .5) if have(new) else (fb, fx, fy)
COIN = P('coin_case', 'coin_spin', .5, .5)
MUSEUM = P('museum_tracks', 'bank_vault_1700s', .25, .42)
BARROW = P('wheelbarrow', 'gold_window', .5, .48)
FURNACE = P('furnace', 'lydia_mint', .64, .58)
JAIL = P('jail_bars', 'gold_window', .5, .45)
FOLLOW_W = 4
NW = {'100kilo': 13, 'barrow': 19, '4': 8, 'jailed': 10, '100kilos': 9, '13': 15, 'thirteen': 8}

# ---- 0 HOOK: would you risk prison for a $1M coin? three men did, in 2017. the million was never the point. why?
shot('s00', COIN[0], 'film', A(0), cam0={'x': COIN[1], 'y': COIN[2], 'z': 1.15}, cam1={'x': COIN[1], 'y': COIN[2], 'z': 1.3})
beat('card', {'abs': 0.12}, text='$1M → *$13M?*', y=280, size=132, blur=True, until={'abs': 2.4})
beat('punch', A(0, 0, .55), shot='s00', level=1.15)
beat('punch', A(0, 0, 1.6), shot='s00', level=1.25)
shot('s01', JAIL[0], 'film', A(0, 1, -.1), cut='whip', cam0={'x': JAIL[1], 'y': JAIL[2], 'z': 1.2}, cam1={'x': JAIL[1], 'y': JAIL[2], 'z': 1.35})
beat('punch', A(0, 2, .1), shot='s01', level=1.32); beat('shake', A(0, 2, .2), k=.5)
shot('s02', 'coin_spin', 'film', A(0, 3, -.1), cut='zoom', cam0={'x': .5, 'y': .5, 'z': 1.25}, cam1={'x': .5, 'y': .52, 'z': 1.4})
beat('punch', A(0, 3, 1.2), shot='s02', level=1.4)
# ---- 1 Berlin 3:30 a.m., train tracks, 100-kilo coin, wheelbarrow
shot('s03', MUSEUM[0], 'film', A(1, 0, -.15), cut='zoomIn', cam0={'x': MUSEUM[1], 'y': MUSEUM[2], 'z': 1.1}, cam1={'x': MUSEUM[1], 'y': MUSEUM[2] - .04, 'z': 1.35})
beat('punch', A(1, 1, .3), shot='s03', level=1.25)
beat('count', Wd(1, NW['100kilo'], -.05), to=100, suffix=' KG', **NUM, until=A(1, 3, -.1))
shot('s04', BARROW[0], 'film', A(1, 3, -.15), cut='whip', cam0={'x': BARROW[1], 'y': BARROW[2], 'z': 1.2}, cam1={'x': BARROW[1], 'y': BARROW[2], 'z': 1.32}, handheld=.1)
# ---- 2 not exactly pickpockets (joke)
beat('punch', A(2, 0, .2), shot='s04', level=1.4)
# ---- 3 OPEN LOOP 1: so why call it a million-dollar coin?
shot('s05', COIN[0], 'film', A(3, 0, -.15), cut='zoom', cam0={'x': COIN[1], 'y': COIN[2], 'z': 1.3}, cam1={'x': COIN[1], 'y': COIN[2], 'z': 1.45})
beat('circle', A(3, 0, .6), shot='s05', c=[COIN[1], COIN[2]], r=[230, 230], col='#FFC23A', until=A(4, 0, -.2))
# ---- 4 face value, in Canadian dollars
shot('s06', 'coin_spin', 'film', A(4, 0, -.15), cut='whip', cam0={'x': .45, 'y': .5, 'z': 1.2}, cam1={'x': .52, 'y': .52, 'z': 1.5})
beat('punch', A(4, 1, .2), shot='s06', level=1.3)
# ---- 5 BILL: mine's just printed on, too
shot('s07', 'wallet_desk', 'soft', A(5, 0, -.35), cam0={'x': .5, 'y': .5, 'z': 1.12}, cam1={'z': 1.18})
beat('moment', A(5, 0, -.3), what='char', shot='s07', who='c_bill', side='M', lines=[5], shrink=A(5, 0, 1.0), leave=A(6, 0, -.25))
# ---- 6 the gold inside: over $4 million
shot('s08', 'vault_full', 'film', A(6, 0, -.15), cut='zoomIn', cam0={'x': .38, 'y': .45, 'z': 1.2}, cam1={'x': .36, 'y': .45, 'z': 1.45})
beat('count', Wd(6, NW['4'], -.05), to=4, prefix='$', suffix='M', **NUM, until=A(7, 0, -.1))
# ---- 7 OPEN LOOP 2: and that's not even the strangest part
shot('s09', FURNACE[0], 'film', A(7, 0, -.1), cut='flash', cam0={'x': FURNACE[1], 'y': FURNACE[2], 'z': 1.15}, cam1={'x': FURNACE[1], 'y': FURNACE[2], 'z': 1.3})
beat('punch', A(7, 0, 1.0), shot='s09', level=1.35); beat('shake', A(7, 0, 1.05), k=.4)
# ---- 8 melted and sold, three men jailed, never found
beat('punch', A(8, 0, .4), shot='s09', level=1.25)
shot('s10', JAIL[0], 'film', Wd(8, NW['jailed'], -.25), cut='whip', cam0={'x': JAIL[1], 'y': JAIL[2], 'z': 1.25}, cam1={'x': JAIL[1], 'y': JAIL[2], 'z': 1.4})
shot('s11', 'vault_empty', 'film', A(8, 2, -.15), cut='zoom', cam0={'x': .36, 'y': .45, 'z': 1.25}, cam1={'x': .36, 'y': .45, 'z': 1.5})
beat('moment', A(8, 2, .6), what='grade', shot='s11', bright=.6, sat=.35, d=.7)
# ---- 9 gold tripled; 100 kilos now ~$13 million (climax)
shot('s12', 'gold_cube', 'film', A(9, 0, -.15), cut='zoomIn', cam0={'x': .76, 'y': .42, 'z': 1.3, 'yaw': -4}, cam1={'x': .72, 'y': .45, 'z': 1.08, 'yaw': 4})
beat('arrow', A(9, 1, .3), shot='s12', **{'from': [.73, .72], 'to': [.73, .3]}, col='#FFC23A', until=A(9, 2, -.1))
beat('punch', A(9, 2, .2), shot='s12', level=1.25)
beat('slam', Wd(9, NW['13'], -.03), to=13, prefix='$', suffix='M', **NUM, until=A(10, 0, -.15))
beat('moment', Wd(9, NW['13'], .15), what='grade', shot='s12', bright=1.15, sat=1.25, d=.6)
# ---- 10 PAYOFF: the coin said one million, the gold says thirteen (hero flash)
shot('s13', 'p_mirage', 'film', A(10, 0, -.15), cut='zoom', cam0={'x': .62, 'y': .35, 'z': 1.1}, cam1={'x': .62, 'y': .3, 'z': 1.35}, shim=[1.0], shimRect=[.3, 0, .75, .55])
shot('s14', 'p_mirage_empty', 'film', A(10, 1, -.05), cut='flash', depthOf='p_mirage', cam0={'x': .58, 'y': .33, 'z': 1.3}, cam1={'x': .5, 'y': .45, 'z': 1.1}, shim=[.6], shimRect=[.3, 0, .75, .55])
beat('punch', Wd(10, NW['thirteen'], .05), shot='s14', level=1.3)
# ---- 11 twist: GOLDIE finally feels valued
shot('s15', 'vault_full', 'film', A(11, 0, -.35), cam0={'x': .45, 'y': .5, 'z': 1.12}, cam1={'z': 1.18})
beat('moment', A(11, 0, -.3), what='char', shot='s15', who='c_goldie', side='M', lines=[11], grow=A(11, 0, 1.0), leave=A(12, 0, -.25))
# ---- 12 comment prompt
shot('s16', COIN[0], 'film', A(12, 0, -.15), cut='zoom', cam0={'x': COIN[1], 'y': COIN[2], 'z': 1.1}, cam1={'x': COIN[1], 'y': COIN[2], 'z': 1.3})
beat('punch', A(12, 0, 1.3), shot='s16', level=1.22)
# ---- 13 sign-off: logo + FOLLOW tapped on the spoken word
shot('s17', 'wallet_desk', 'soft', A(13, 0, -.15), cut='zoom', cam0={'x': .55, 'y': .58, 'z': 1.15}, cam1={'x': .55, 'y': .58, 'z': 1.3})
beat('moment', A(13, 0, 0), what='follow', btn=A(13, 0, .5), click=Wd(13, FOLLOW_W, .1), y=330)

json.dump({'shots': SH, 'beats': BT}, open(os.path.join(HERE, 'shots.json'), 'w'), ensure_ascii=False, indent=1)
print(LANG, len(SH), 'shots', len(BT), 'beats', 'new plates:', [p[0] for p in (COIN, MUSEUM, BARROW, FURNACE, JAIL)])
