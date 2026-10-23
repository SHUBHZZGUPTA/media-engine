# Money Mirage Short s001 (gold in a crisis): the whole shot plan, native portrait 1080x1920, as data for build.py --port.
# Language-agnostic: anchors are caption chunks (Hindi has the same chunk count per line). Run from the short folder or hi/.
# Anchors: A(li, ci, off) = caption-chunk start; Wd(li, wi, off) = word start. Plate coords are 0..1 of the image (read off grid images).
import json, os
HERE = os.getcwd(); LANG = json.load(open(os.path.join(HERE, 'episode.json'))).get('lang', 'en')
A = lambda li, ci=0, off=0.0: {'@': [li, ci, off]}
Wd = lambda li, wi, off=0.0: {'@w': [li, wi, off]}
SH = []; BT = []
def shot(id, img, look, at, cut='curve', cam0=None, cam1=None, keys=None, dScale=.3, **kw):
    SH.append(dict(id=id, img=img, look=look, at=at, cut=cut, cam0=cam0 or {'x': .5, 'y': .5, 'z': 1.05}, cam1=cam1 or {'z': 1.15}, keys=keys or [], dScale=dScale, **kw))
def beat(kind, at, **kw): BT.append(dict(kind=kind, at=at, **kw))
def key(t, x=None, y=None, z=None, yaw=None, pitch=None, d=.32, e='power3.out'):
    to = {k: v for k, v in dict(x=x, y=y, z=z, yaw=yaw, pitch=pitch).items() if v is not None}; return dict(t=t, to=to, d=d, e=e)
NUM = dict(align='center', y=250, size=170)
SCALE = 'scale' if os.path.exists(os.path.join(HERE, 'art/baked/scale__film.jpg')) else 'central_bank'   # new Codex plate, library fallback
FOLLOW_W = {'en': 4, 'hi': 8}[LANG]   # index of the spoken "Follow" in the sign-off line

# ---- 1 HOOK: safe haven lost 28% ... why is gold falling?
shot('s00', 'gold_cube', 'film', A(0), cam0={'x': .76, 'y': .42, 'z': 1.3, 'yaw': -4}, cam1={'x': .72, 'y': .45, 'z': 1.05, 'yaw': 4})   # aim at the cube's edge so it reads as a block in portrait
beat('card', {'abs': 0.12}, text='$5,608 → *$4,014*', y=280, size=132, blur=True, until={'abs': 2.4})
beat('punch', A(0, 0, .55), shot='s00', level=1.15)
beat('punch', A(0, 0, 1.9), shot='s00', level=1.25)
beat('punch', A(0, 1, .45), shot='s00', level=1.32); beat('shake', A(0, 1, .55), k=.5)
shot('s01', 'bank_vault_1700s', 'film', A(0, 2, -.1), cut='whip', cam0={'x': .25, 'y': .4, 'z': 1.2}, cam1={'x': .27, 'y': .42, 'z': 1.5, 'yaw': 3})
beat('punch', A(0, 2, .5), shot='s01', level=1.4)
# ---- 2 oil $112, stocks sliding
shot('s02', 'oil_tanker', 'film', A(1, 0, -.15), cut='zoom', cam0={'x': .32, 'y': .38, 'z': 1.3}, cam1={'z': 1.4},
     keys=[key(A(1, 2, -.35), x=.82, y=.26, z=1.45, d=.9, e='power2.inOut')])
beat('count', A(1, 2, .1), to=112, prefix='$', **NUM, until=A(1, 3, -.1))
shot('s03', 'trading_room', 'film', A(1, 3, -.15), cut='whip', cam0={'x': .45, 'y': .3, 'z': 1.3}, cam1={'x': .45, 'y': .32, 'z': 1.45, 'yaw': -3}, handheld=.1)
beat('arrow', A(1, 3, .2), shot='s03', **{'from': [.4, .2], 'to': [.5, .42]}, col='#FF3B30', until=A(2, 0, -.3))
# ---- 3-4 Goldie brags, gold dips below $4,000
shot('s04', 'gold_cube', 'film', A(2, 0, -.35), cam0={'x': .3, 'y': .45, 'z': 1.08}, cam1={'x': .33, 'y': .45, 'z': 1.18})
beat('moment', A(2, 0, -.3), what='char', shot='s04', who='c_goldie', side='M', lines=[2], shrink=A(3, 0, .9), leave=A(4, 0, -.25))
beat('slam', A(3, 0, .7), to=4000, prefix='$', **NUM, until=A(4, 0, -.2))
beat('moment', A(3, 0, .8), what='grade', shot='s04', bright=.62, sat=.35, d=.7)
# ---- 5 why does the shield crack?
shot('s05', 'p_dam', 'film', A(4, 0, -.15), cam0={'x': .5, 'y': .4, 'z': 1.15}, cam1={'x': .55, 'y': .47, 'z': 1.5})
beat('moment', A(4, 0, .4), what='cracks', shot='s05', lines=[[[.56, .28], [.54, .4], [.57, .5], [.55, .62]], [[.6, .3], [.63, .42], [.61, .55]]], until=A(5, 0, -.2))
beat('shake', A(4, 0, .9), k=.6)
beat('circle', A(4, 1, .1), shot='s05', c=[.555, .47], r=[170, 230], until=A(5, 0, -.2))
# ---- 6 gold pays nothing, a bond pays 5%
shot('s06', 'bank_vault_1700s', 'film', A(5, 0, -.15), cut='zoomIn', cam0={'x': .2, 'y': .38, 'z': 1.25}, cam1={'x': .22, 'y': .38, 'z': 1.55})
beat('punch', A(5, 0, .7), shot='s06', level=1.3)
shot('s07', SCALE, 'film', A(5, 1, -.15), cam0={'x': .5, 'y': .45, 'z': 1.1}, cam1={'x': .5, 'y': .45, 'z': 1.3})
beat('count', A(5, 1, 1.1), to=5, suffix='%', **NUM, until=A(6, 0, -.1))
# ---- 7 oil -> inflation -> rates high -> nothing gets expensive
shot('s08', 'central_bank', 'film', A(6, 0, -.15), cut='whip', cam0={'x': .6, 'y': .4, 'z': 1.2}, cam1={'x': .66, 'y': .4, 'z': 1.4})
beat('arrow', A(6, 1, .2), shot='s08', **{'from': [.62, .62], 'to': [.62, .22]}, col='#FFC23A', until=A(6, 2, -.1))
beat('punch', A(6, 2, .7), shot='s08', level=1.25)
# ---- 8 Bill: paper wins
shot('s09', SCALE, 'film', A(7, 0, -.35), cam0={'x': .5, 'y': .5, 'z': 1.12}, cam1={'z': 1.18})
beat('moment', A(7, 0, -.3), what='char', shot='s09', who='c_bill', side='M', lines=[7], grow=A(7, 1, 0), leave=A(8, 0, -.25))
# ---- 9 forced selling: gold is the cash machine
shot('s10', 'trading_room', 'soft', A(8, 0, -.15), cut='zoom', cam0={'x': .5, 'y': .32, 'z': 1.2}, cam1={'x': .5, 'y': .34, 'z': 1.35}, handheld=.1)
beat('punch', A(8, 1, .3), shot='s10', level=1.2)
shot('s11', 'gold_window', 'film', A(8, 2, -.15), cut='whip', cam0={'x': .5, 'y': .45, 'z': 1.15}, cam1={'x': .5, 'y': .48, 'z': 1.4})
beat('circle', A(8, 3, .2), shot='s11', c=[.52, .48], r=[180, 140], col='#FFC23A', until=A(9, 0, -.2))
# ---- 10 PAYOFF: the mirage (hero flash)
shot('s12', 'p_mirage', 'film', A(9, 0, -.15), cut='zoom', cam0={'x': .62, 'y': .35, 'z': 1.1}, cam1={'x': .62, 'y': .3, 'z': 1.35}, shim=[1.0], shimRect=[.3, 0, .75, .55])
shot('s13', 'p_mirage_empty', 'film', A(9, 1, -.05), cut='flash', depthOf='p_mirage', cam0={'x': .58, 'y': .33, 'z': 1.3}, cam1={'x': .5, 'y': .45, 'z': 1.1}, shim=[.6], shimRect=[.3, 0, .75, .55])
beat('punch', A(9, 2, .8), shot='s13', level=1.22)
# ---- 11 loop back to the hook: your safe haven isn't
shot('s14', 'gold_cube', 'film', A(10, 0, -.15), cut='zoomIn', cam0={'x': .74, 'y': .42, 'z': 1.1}, cam1={'x': .72, 'y': .42, 'z': 1.35})
beat('moment', A(10, 1, 0), what='grade', shot='s14', bright=.55, sat=.3, d=.6)
beat('punch', A(10, 1, .45), shot='s14', level=1.3)
# ---- 12 twist: Goldie is just resting
shot('s15', 'p_mirage_empty', 'film', A(11, 0, -.35), depthOf='p_mirage', cam0={'x': .5, 'y': .5, 'z': 1.12}, cam1={'z': 1.18})
beat('moment', A(11, 0, -.3), what='char', shot='s15', who='c_goldie', side='M', lines=[11], shrink=A(11, 1, 0))
# ---- 13 sign-off: logo + FOLLOW tapped on the spoken word
shot('s16', 'wallet_desk', 'soft', A(12, 0, -.15), cut='zoom', cam0={'x': .55, 'y': .58, 'z': 1.15}, cam1={'x': .55, 'y': .58, 'z': 1.3})
beat('moment', A(12, 0, 0), what='follow', btn=A(12, 0, .5), click=Wd(12, FOLLOW_W, .1), y=330)

json.dump({'shots': SH, 'beats': BT}, open(os.path.join(HERE, 'shots.json'), 'w'), ensure_ascii=False, indent=1)
print(LANG, len(SH), 'shots', len(BT), 'beats', 'scale plate:', SCALE)
