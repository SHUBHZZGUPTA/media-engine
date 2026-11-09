# Money Mirage Short s035 (De Beers, "A Diamond Is Forever", lab-grown collapse): whole shot plan, native portrait, build.py --port. English only.
import json, os, re
HERE = os.getcwd(); LANG = json.load(open(os.path.join(HERE, 'episode.json'))).get('lang', 'en')
A = lambda li, ci=0, off=0.0: {'@': [li, ci, off]}
Wd = lambda li, wi, off=0.0: {'@w': [li, wi, off]}
SH = []; BT = []
def shot(id, img, look, at, cut='curve', cam0=None, cam1=None, keys=None, dScale=.3, **kw):
    SH.append(dict(id=id, img=img, look=look, at=at, cut=cut, cam0=cam0 or {'x': .5, 'y': .5, 'z': 1.05}, cam1=cam1 or {'z': 1.15}, keys=keys or [], dScale=dScale, **kw))
def beat(kind, at, **kw): BT.append(dict(kind=kind, at=at, **kw))
NUM = dict(align='center', y=250, size=170)
have = lambda p: os.path.exists(os.path.join(HERE, f'art/baked/{p}__film.jpg'))
def P(new, fb, fx=.5, fy=.5, nx=.5, ny=.5): return (new, nx, ny) if have(new) else (fb, fx, fy)
# word index by token, read from this folder's script (caption words, *keywords* stripped)
LINES = [re.sub(r'\[.*?\]', '', l.split(':', 1)[1]).replace('*', '').split() for l in open(os.path.join(HERE, 'script_marked.md')).read().split('\n')[1:] if ':' in l]
def W(li, tok, off=0.0, n=1):
    hits = [i for i, w in enumerate(LINES[li]) if w.lower().strip('.,?!:;"\'').startswith(tok.lower())]
    assert len(hits) >= n, (li, tok, LINES[li]); return Wd(li, hits[n - 1], off)
def cam(p, z0, z1, dx=0, dy=0): return dict(cam0={'x': p[1], 'y': p[2], 'z': z0}, cam1={'x': p[1] + dx, 'y': p[2] + dy, 'z': z1})
FOLLOW_W = 4
RING = P('dm_ring', 'gj_shop'); LAB = P('dm_lab', 'gj_scale'); VAULT = P('dm_vault', 'vault_full', .4, .45); AD = P('dm_ad', 'gj_shop')
CIRC_RING = [.53, .32] if RING[0] == 'dm_ring' else [.5, .4]
SHOPJ = ('gj_shop', .5, .45); SCALE = ('gj_scale', .5, .45); CTR = ('emi_counter', .5, .45)
# 0 HOOK
shot('s00', RING[0], 'film', A(0), **cam(RING, 1.15, 1.3))
beat('card', {'abs': 0.12}, text="A diamond's *real* price?", y=280, size=124, blur=True, until={'abs': 2.4})
beat('punch', A(0, 1, .2), shot='s00', level=1.28)
shot('s01', LAB[0], 'film', A(0, 2, -.1), cut='whip', **cam(LAB, 1.2, 1.35))
beat('count', W(0, '90%', -.05), to=90, prefix='−', suffix='%', **NUM, until=A(0, 3, -.1))
shot('s02', RING[0], 'film', A(0, 3, -.1), cut='zoom', **cam(RING, 1.3, 1.45))
# 1 De Beers controlled most of the world's diamonds
shot('s03', VAULT[0], 'film', A(1, 0, -.15), cut='zoomIn', **cam(VAULT, 1.1, 1.35))
beat('punch', W(1, 'diamonds', .05), shot='s03', level=1.3)
# 2 1947: four words
shot('s04', AD[0], 'film', A(2, 0, -.15), cut='whip', **cam(AD, 1.1, 1.3))
beat('slam', W(2, '1947', -.03), to=1947, **NUM, until=A(2, 2, -.1))
beat('punch', A(2, 2, .1), shot='s04', level=1.35)
# 3 OPEN LOOP 1
shot('s05', RING[0], 'film', A(3, 0, -.15), cut='zoom', **cam(RING, 1.3, 1.45))
beat('circle', A(3, 0, .6), shot='s05', c=CIRC_RING, r=[200, 200], col='#FFC23A', until=A(4, 0, -.2))
# 4 forever means never resell
shot('s06', SHOPJ[0], 'film', A(4, 0, -.15), cut='zoom', **cam(SHOPJ, 1.1, 1.3))
beat('moment', W(4, 'resell', .1), what='grade', shot='s06', bright=.7, sat=.5, d=.6)
beat('punch', A(4, 2, .2), shot='s06', level=1.3)
# 5 joke: romantic, and good for business
shot('s07', AD[0], 'film', A(5, 0, -.15), cut='zoom', **cam(AD, 1.2, 1.35))
beat('punch', W(5, 'business', .05), shot='s07', level=1.38)
# 6 OPEN LOOP 2
shot('s08', CTR[0], 'film', A(6, 0, -.1), cut='flash', **cam(CTR, 1.15, 1.3))
beat('punch', A(6, 0, .9), shot='s08', level=1.35); beat('shake', A(6, 0, .95), k=.4)
# 7 two months' salary; 10% -> 80%
shot('s09', SCALE[0], 'film', A(7, 0, -.15), cut='zoomIn', **cam(SCALE, 1.1, 1.3))
beat('punch', A(7, 1, .1), shot='s09', level=1.3)
shot('s10', AD[0], 'film', A(7, 2, -.1), cut='whip', **cam(AD, 1.3, 1.45))
beat('punch', A(7, 3, .1), shot='s10', level=1.38)
# 8 labs grow the same stone; $6.8B written down
shot('s11', LAB[0], 'film', A(8, 0, -.15), cut='whip', **cam(LAB, 1.1, 1.3))
beat('count', W(8, '$6.8', -.05), to=6.8, dec=1, prefix='$', suffix='B', **NUM, until=A(9, 0, -.15))
beat('moment', W(8, '$6.8', .3), what='grade', shot='s11', bright=.7, sat=.5, d=.6)
# 9 PAYOFF: the rarity was in the story (hero flash, mirage plates)
shot('s12', 'p_mirage', 'film', A(9, 0, -.15), cut='flash', cam0={'x': .62, 'y': .35, 'z': 1.1}, cam1={'x': .62, 'y': .3, 'z': 1.35}, shim=[1.0], shimRect=[.3, 0, .75, .55])
shot('s13', 'p_mirage_empty', 'film', A(9, 1, -.05), cut='flash', depthOf='p_mirage', cam0={'x': .58, 'y': .33, 'z': 1.3}, cam1={'x': .5, 'y': .45, 'z': 1.1}, shim=[.6], shimRect=[.3, 0, .75, .55])
beat('punch', W(9, 'story', .05), shot='s13', level=1.3)
# 10 GOLDIE twist
shot('s14', 'vault_full', 'film', A(10, 0, -.35), cam0={'x': .45, 'y': .5, 'z': 1.12}, cam1={'z': 1.18})
beat('moment', A(10, 0, -.3), what='char', shot='s14', who='c_goldie', side='M', lines=[10], grow=A(10, 0, 1.0), leave=A(11, 0, -.25))
# 11 comment prompt
shot('s15', RING[0], 'film', A(11, 0, -.15), cut='zoom', **cam(RING, 1.1, 1.3))
beat('punch', A(11, 1, .1), shot='s15', level=1.22)
# 12 sign-off
shot('s16', 'wallet_desk', 'soft', A(12, 0, -.15), cut='zoom', cam0={'x': .55, 'y': .58, 'z': 1.15}, cam1={'x': .55, 'y': .58, 'z': 1.3})
beat('moment', A(12, 0, 0), what='follow', btn=A(12, 0, .5), click=Wd(12, FOLLOW_W, .1), y=330)

json.dump({"shots": SH, "beats": BT}, open(os.path.join(HERE, "shots.json"), "w"), ensure_ascii=False, indent=1)
print(LANG, len(SH), "shots", len(BT), "beats")
