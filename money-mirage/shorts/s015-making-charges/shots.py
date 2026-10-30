# Money Mirage Short s015 (gold making charges): whole shot plan, native portrait 1080x1920, data for build.py --port.
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
NECK, SHOP, SMITH, SCALE = P('gj_necklace', 'gold_window'), P('gj_shop', 'chengdu_market'), P('gj_goldsmith', 'lydia_mint'), P('gj_scale', 'p_earlymoney')
FOLLOW_W = 4
NW = {'20': 11, '800': 9}
C = json.load(open(os.path.join(HERE, 'coords.json'))) if os.path.exists(os.path.join(HERE, 'coords.json')) else {}
c = lambda k, d: C.get(k, d)

# ---- 1 HOOK: necklace can lose $200 the moment you pay
shot('s00', NECK, 'film', A(0), cam0=PORT(.5, .4, 1.15), cam1=PORT(.5, .4, 1.3))
beat('card', {'abs': 0.12}, text='$1,000 → *$800*', y=280, size=132, blur=True, until={'abs': 2.4})
beat('punch', A(0, 0, .6), shot='s00', level=1.18)
beat('punch', A(0, 1, .3), shot='s00', level=1.3); beat('shake', A(0, 1, .4), k=.5)
shot('s01', 'gold_cube', 'film', A(0, 2, -.1), cut='whip', cam0={'x': .76, 'y': .42, 'z': 1.3, 'yaw': -4}, cam1={'x': .72, 'y': .45, 'z': 1.1, 'yaw': 4})
beat('punch', A(0, 3, .2), shot='s01', level=1.35)
# ---- 2 Dhanteras next week
shot('s02', SHOP, 'film', A(1, 0, -.15), cut='zoom', cam0=PORT(.5, .45, 1.1), cam1=PORT(.5, .5, 1.3))
beat('punch', A(1, 1, .5), shot='s02', level=1.25)
# ---- 3 Goldie joke
shot('s03', SHOP, 'soft', A(2, 0, -.35), cam0=PORT(.5, .5, 1.12), cam1={'z': 1.18})
beat('moment', A(2, 0, -.3), what='char', shot='s03', who='c_goldie', side='M', lines=[2], grow=A(2, 0, 1.0), leave=A(3, 0, -.25))
# ---- 4 a $1,000 necklace isn't $1,000 of gold
shot('s04', NECK, 'film', A(3, 0, -.15), cut='zoomIn', cam0=PORT(.5, .4, 1.1), cam1=PORT(.5, .4, 1.4))
beat('moment', A(3, 0, 1.6), what='grade', shot='s04', bright=.6, sat=.45, d=.6)
# ---- 5 OPEN LOOP 1
shot('s05', NECK, 'film', A(4, 0, -.15), cut='whip', cam0=PORT(.45, .45, 1.45), cam1=PORT(.5, .4, 1.6))
# ---- 6 making charges: design + labour, often 20% or more
shot('s06', SMITH, 'film', A(5, 0, -.15), cut='zoom', cam0=PORT(.5, .5, 1.1), cam1=PORT(.5, .5, 1.3))
beat('circle', A(5, 1, .2), shot='s06', c=c('smith_hands', [.5, .55]), r=[220, 180], col='#FFC23A', until=A(5, 2, -.1))
beat('count', Wd(5, NW['20'], -.05), to=20, suffix='%', **NUM, until=A(6, 0, -.1))
# ---- 7 then tax
shot('s07', SHOP, 'film', A(6, 0, -.1), cut='whip', cam0=PORT(.5, .5, 1.3), cam1=PORT(.5, .5, 1.45))
# ---- 8 when you sell, they pay for the gold inside
shot('s08', SCALE, 'film', A(7, 0, -.15), cut='zoom', cam0=PORT(.5, .5, 1.1), cam1=PORT(.5, .5, 1.3))
beat('circle', A(7, 1, .5), shot='s08', c=c('scale_pan', [.5, .6]), r=[200, 160], until=A(8, 0, -.1))
# ---- 9 OPEN LOOP 2
shot('s09', SCALE, 'film', A(8, 0, -.1), cut='flash', cam0=PORT(.5, .4, 1.35), cam1=PORT(.5, .35, 1.55))
beat('shake', A(8, 0, .9), k=.5)
# ---- 10 making charges gone, tax gone
shot('s10', SCALE, 'film', A(9, 0, -.12), cut='zoomIn', cam0=PORT(*c('crucible_cam', [.5, .3]), 1.25), cam1=PORT(*c('crucible_cam', [.5, .28]), 1.45))
beat('moment', A(9, 1, 0), what='grade', shot='s10', bright=.55, sat=.35, d=.5)
beat('punch', A(9, 1, .9), shot='s10', level=1.3)
# ---- 11 PAYOFF: mirage (hero flash)
shot('s11', 'p_mirage', 'film', A(10, 0, -.15), cut='zoom', cam0={'x': .62, 'y': .35, 'z': 1.1}, cam1={'x': .62, 'y': .3, 'z': 1.3}, shim=[1.0], shimRect=[.3, 0, .75, .55])
shot('s12', SMITH, 'film', A(10, 2, -.05), cut='flash', cam0=PORT(.5, .5, 1.35), cam1=PORT(.5, .5, 1.1))
# ---- 12 $1,000 sells back for around $800
shot('s13', NECK, 'film', A(11, 0, -.15), cut='zoom', cam0=PORT(.5, .4, 1.1), cam1=PORT(.5, .4, 1.3))
beat('slam', Wd(11, NW['800'], -.03), to=800, prefix='$', **NUM, until=A(12, 0, -.1))
beat('moment', Wd(11, NW['800'], .15), what='grade', shot='s13', bright=.6, sat=.4, d=.7)
# ---- 13 savers pick coins or bars
shot('s14', 'vault_full', 'film', A(12, 0, -.15), cut='whip', cam0={'x': .3, 'y': .45, 'z': 1.25}, cam1={'x': .32, 'y': .45, 'z': 1.45})
beat('punch', A(12, 0, 1.0), shot='s14', level=1.25)
# ---- 14 Bill twist
shot('s15', 'coin_spin', 'soft', A(13, 0, -.35), cam0={'x': .55, 'y': .5, 'z': 1.12}, cam1={'z': 1.18})
beat('moment', A(13, 0, -.3), what='char', shot='s15', who='c_bill', side='M', lines=[13], grow=A(13, 1, 0), leave=A(14, 0, -.25))
# ---- 15 comment
shot('s16', NECK, 'film', A(14, 0, -.15), cut='zoom', cam0=PORT(.5, .4, 1.2), cam1=PORT(.5, .4, 1.35))
beat('punch', A(14, 0, 1.0), shot='s16', level=1.25)
# ---- 16 sign-off
shot('s17', 'wallet_desk', 'soft', A(15, 0, -.15), cut='zoom', cam0={'x': .55, 'y': .58, 'z': 1.15}, cam1={'x': .55, 'y': .58, 'z': 1.3})
beat('moment', A(15, 0, 0), what='follow', btn=A(15, 0, .5), click=Wd(15, FOLLOW_W, .1), y=330)

SH = [{k: v for k, v in s.items() if v is not None} for s in SH]
json.dump({'shots': SH, 'beats': BT}, open(os.path.join(HERE, 'shots.json'), 'w'), ensure_ascii=False, indent=1)
print(LANG, len(SH), 'shots', len(BT), 'beats', 'plates:', NECK, SHOP, SMITH, SCALE)
