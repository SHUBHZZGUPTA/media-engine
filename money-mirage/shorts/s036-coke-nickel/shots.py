# Money Mirage Short s036 (Coca-Cola's 5-cent price, 1886-1959): whole shot plan, native portrait, build.py --port. English only.
# No Coca-Cola logo or contour bottle anywhere (plain unlabelled bottles); Eisenhower never drawn (empty office).
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
FOUNT = P('ck_fountain', 'pn_jar'); LAW = P('ck_lawyers', 'pn_ledger'); VEND = P('ck_vending', 'pn_nickel'); OFF = P('ck_office', 'pn_ledger'); BOT = P('ck_bottles', 'pn_press')
NICK = ('pn_nickel', .5, .5); LED = ('pn_ledger', .5, .45); PRESS = ('pn_press', .5, .45); JAR = ('pn_jar', .5, .45)
# 0 HOOK
shot('s00', FOUNT[0], 'film', A(0), **cam(FOUNT, 1.15, 1.3))
beat('card', {'abs': 0.12}, text='Price frozen: *1886–1959*', y=280, size=118, blur=True, until={'abs': 2.4})
beat('punch', A(0, 0, .55), shot='s00', level=1.15)
beat('punch', A(0, 1, .1), shot='s00', level=1.28)
shot('s01', NICK[0], 'film', A(0, 2, -.1), cut='whip', **cam(NICK, 1.2, 1.35))
beat('slam', W(0, '5', -.03), to=5, suffix='¢', **NUM, until=A(0, 3, -.1))
beat('punch', A(0, 3, .1), shot='s01', level=1.4)
# 1 1899: lawyers, syrup price fixed permanently
shot('s02', LAW[0], 'film', A(1, 0, -.15), cut='zoomIn', **cam(LAW, 1.1, 1.3))
beat('punch', A(1, 1, .2), shot='s02', level=1.25)
beat('punch', W(1, 'permanently', .05), shot='s02', level=1.35)
# 2 joke
shot('s03', LED[0], 'film', A(2, 0, -.15), cut='zoom', **cam(LED, 1.15, 1.3))
beat('punch', A(2, 0, .7), shot='s03', level=1.35)
# 3 OPEN LOOP 1
shot('s04', VEND[0], 'film', A(3, 0, -.15), cut='whip', **cam(VEND, 1.15, 1.3))
beat('circle', A(3, 0, .5), shot='s04', c=CIRC_VEND, r=[170, 170], col='#FFC23A', until=A(4, 1, -.1))
# 4 five cents; single nickel; next coin a dime
beat('punch', A(4, 1, .2), shot='s04', level=1.3)
shot('s05', NICK[0], 'film', A(4, 2, -.1), cut='whip', **cam(NICK, 1.15, 1.35))
beat('punch', A(4, 3, .1), shot='s05', level=1.38)
# 5 OPEN LOOP 2
shot('s06', PRESS[0], 'film', A(5, 0, -.1), cut='flash', **cam(PRESS, 1.15, 1.3))
beat('punch', A(5, 0, .9), shot='s06', level=1.35); beat('shake', A(5, 0, .95), k=.4)
# 6 7½-cent coin; Eisenhower; no
beat('slam', W(6, '7½', -.03), text='7½¢', **NUM, until=A(6, 2, -.1))
shot('s07', OFF[0], 'film', A(6, 2, -.1), cut='whip', **cam(OFF, 1.1, 1.3))
beat('punch', A(6, 3, .1), shot='s07', level=1.28)
beat('punch', W(6, 'no', .05), shot='s07', level=1.4); beat('shake', W(6, 'no', .1), k=.35)
# 7 inflation won; 1959
shot('s08', BOT[0], 'film', A(7, 0, -.15), cut='zoom', **cam(BOT, 1.1, 1.3))
beat('slam', W(7, '1959', -.03), to=1959, **NUM, until=A(7, 2, -.1))
beat('moment', W(7, 'gone', .1), what='grade', shot='s08', bright=.65, sat=.45, d=.6)
# 8 PAYOFF (hero flash)
shot('s09', JAR[0], 'film', A(8, 0, -.15), cut='flash', **cam(JAR, 1.1, 1.35))
beat('punch', W(8, 'weaker', .05), shot='s09', level=1.3)
# 9 GOLDIE twist
shot('s10', 'vault_full', 'film', A(9, 0, -.35), cam0={'x': .45, 'y': .5, 'z': 1.12}, cam1={'z': 1.18})
beat('moment', A(9, 0, -.3), what='char', shot='s10', who='c_goldie', side='M', lines=[9], grow=A(9, 0, .9), leave=A(10, 0, -.25))
# 10 comment prompt
shot('s11', FOUNT[0], 'film', A(10, 0, -.15), cut='zoom', **cam(FOUNT, 1.1, 1.3))
beat('punch', A(10, 0, 1.4), shot='s11', level=1.22)
# 11 sign-off
shot('s12', 'wallet_desk', 'soft', A(11, 0, -.15), cut='zoom', cam0={'x': .55, 'y': .58, 'z': 1.15}, cam1={'x': .55, 'y': .58, 'z': 1.3})
beat('moment', A(11, 0, 0), what='follow', btn=A(11, 0, .5), click=Wd(11, FOLLOW_W, .1), y=330)

json.dump({"shots": SH, "beats": BT}, open(os.path.join(HERE, "shots.json"), "w"), ensure_ascii=False, indent=1)
print(LANG, len(SH), "shots", len(BT), "beats")
