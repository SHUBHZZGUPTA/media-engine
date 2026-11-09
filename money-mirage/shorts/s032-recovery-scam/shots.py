# Money Mirage Short s032 (the recovery scam: fake FBI/IC3 "refund" calls): whole shot plan, native portrait 1080x1920, build.py --port. English only.
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
KIT = P('rs_kitchen', 'fc_phone'); LIST = P('rs_list', 'pn_ledger'); FAKE = P('rs_deepfake', 'da_fakeset'); BUOY = P('rs_rescue', 'fc_deposit')
CIRC_PH = [.62, .53]; CIRC_LIST = [.75, .27] if LIST[0] == 'rs_list' else [.5, .4]
PH = ('fc_phone', .55, .55); BADGE = ('fc_badge', .45, .45); COP = ('fc_cop', .5, .45); DEP = ('fc_deposit', .5, .5); VC = ('da_videocall', .5, .45); SET = ('da_fakeset', .5, .45)
# 0 HOOK
shot('s00', KIT[0], 'film', A(0), **cam(KIT, 1.15, 1.3))
beat('card', {'abs': 0.12}, text='Scammed *twice?*', y=280, size=132, blur=True, until={'abs': 2.4})
beat('punch', A(0, 0, .55), shot='s00', level=1.15)
beat('count', W(0, '$5,000', -.05), to=5000, prefix='$', **dict(NUM, y=640, size=150), until=A(0, 1, -.1))
shot('s01', PH[0], 'film', A(0, 1, -.1), cut='whip', **cam(PH, 1.2, 1.35))
beat('punch', A(0, 2, .1), shot='s01', level=1.3); beat('shake', A(0, 2, .2), k=.4)
beat('punch', A(0, 3, .1), shot='s01', level=1.4)
shot('s02', KIT[0], 'film', A(0, 4, -.1), cut='zoom', **cam(KIT, 1.3, 1.4))
# 1 agent sounds real / badge / knows
shot('s03', VC[0], 'film', A(1, 0, -.15), cut='zoomIn', **cam(VC, 1.1, 1.3))
shot('s04', BADGE[0], 'film', A(1, 1, -.1), cut='whip', **cam(BADGE, 1.15, 1.3))
beat('punch', A(1, 2, .2), shot='s04', level=1.3)
# 2 small recovery fee. Upfront.
shot('s05', DEP[0], 'film', A(2, 0, -.15), cut='zoom', **cam(DEP, 1.1, 1.3))
beat('punch', W(2, 'Upfront', .05), shot='s05', level=1.38)
# 3 BILL: oh no. not again.
shot('s06', 'wallet_desk', 'soft', A(3, 0, -.35), cam0={'x': .5, 'y': .5, 'z': 1.12}, cam1={'z': 1.18})
beat('moment', A(3, 0, -.3), what='char', shot='s06', who='c_bill', side='M', lines=[3], shrink=A(3, 1, .2), leave=A(4, 0, -.25))
# 4 OPEN LOOP 1
shot('s07', PH[0], 'film', A(4, 0, -.15), cut='zoom', **cam(PH, 1.3, 1.45))
beat('circle', A(4, 0, .6), shot='s07', c=CIRC_PH, r=[230, 230], col='#FFC23A', until=A(5, 0, -.2))
# 5 FTC: they buy lists
shot('s08', LIST[0], 'film', A(5, 0, -.15), cut='zoomIn', cam0={'x': .6, 'y': .37, 'z': 1.12}, cam1={'x': .68, 'y': .33, 'z': 1.25})
beat('punch', A(5, 1, .2), shot='s08', level=1.15)
beat('circle', A(5, 2, .05), shot='s08', c=CIRC_LIST, r=[170, 120], col='#FF3B30', until=A(6, 0, -.1))
# 6 OPEN LOOP 2
shot('s09', FAKE[0], 'film', A(6, 0, -.1), cut='flash', **cam(FAKE, 1.15, 1.3))
beat('punch', A(6, 0, .9), shot='s09', level=1.35); beat('shake', A(6, 0, .95), k=.4)
# 7 deepfakes, fake complaint site
beat('punch', A(7, 0, .3), shot='s09', level=1.25)
shot('s10', SET[0], 'film', A(7, 1, -.1), cut='whip', **cam(SET, 1.15, 1.3))
beat('punch', A(7, 2, .3), shot='s10', level=1.3)
# 8 real IC3 never calls first, never charges. Zero.
shot('s11', COP[0], 'film', A(8, 0, -.15), cut='zoom', **cam(COP, 1.1, 1.3))
beat('punch', A(8, 1, .2), shot='s11', level=1.25)
beat('slam', W(8, 'Zero', -.03), to=0, prefix='$', **NUM, until=A(9, 0, -.15))
beat('moment', W(8, 'Zero', .15), what='grade', shot='s11', bright=1.15, sat=1.2, d=.6)
# 9 PAYOFF: the rescue is the scam (hero flash)
shot('s12', BUOY[0], 'film', A(9, 0, -.15), cut='flash', **cam(BUOY, 1.1, 1.35))
beat('punch', W(9, 'scam', .05), shot='s12', level=1.3)
# 10 GOLDIE twist
shot('s13', 'vault_full', 'film', A(10, 0, -.35), cam0={'x': .45, 'y': .5, 'z': 1.12}, cam1={'z': 1.18})
beat('moment', A(10, 0, -.3), what='char', shot='s13', who='c_goldie', side='M', lines=[10], grow=A(10, 1, .3), leave=A(11, 0, -.25))
# 11 comment prompt
shot('s14', PH[0], 'film', A(11, 0, -.15), cut='zoom', **cam(PH, 1.1, 1.3))
beat('punch', A(11, 0, 1.3), shot='s14', level=1.22)
# 12 sign-off
shot('s15', 'wallet_desk', 'soft', A(12, 0, -.15), cut='zoom', cam0={'x': .55, 'y': .58, 'z': 1.15}, cam1={'x': .55, 'y': .58, 'z': 1.3})
beat('moment', A(12, 0, 0), what='follow', btn=A(12, 0, .5), click=Wd(12, FOLLOW_W, .1), y=330)

json.dump({"shots": SH, "beats": BT}, open(os.path.join(HERE, "shots.json"), "w"), ensure_ascii=False, indent=1)
print(LANG, len(SH), "shots", len(BT), "beats")
