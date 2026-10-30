# Money Mirage Short s014 (no-cost EMI): whole shot plan, native portrait 1080x1920, data for build.py --port.
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
CTR, ENV, CUPS, BUY = P('emi_counter', 'wallet_desk'), P('emi_envelopes', 'coin_spin'), P('emi_cups', 'chess_queen'), P('emi_buyers', 'uk_high_street_1991')
FOLLOW_W = 4
NW = {'300': 3, '255': 7, '21': 6}
C = json.load(open(os.path.join(HERE, 'coords.json'))) if os.path.exists(os.path.join(HERE, 'coords.json')) else {}
c = lambda k, d: C.get(k, d)

# ---- 1 HOOK: no-cost EMI can cost ~20% more
shot('s00', CTR, 'film', A(0), cam0=PORT(.5, .5, 1.15), cam1=PORT(.5, .48, 1.3))
beat('card', {'abs': 0.12}, text='0% INTEREST*?*', y=280, size=132, blur=True, until={'abs': 2.4})
beat('punch', A(0, 0, .6), shot='s00', level=1.15)
beat('punch', A(0, 1, .2), shot='s00', level=1.3); beat('shake', A(0, 1, .3), k=.5)
shot('s01', CUPS, 'film', A(0, 2, -.1), cut='whip', cam0=PORT(.5, .5, 1.2), cam1=PORT(.5, .52, 1.4))
# ---- 2 the deal: $300, six payments, zero interest
shot('s02', ENV, 'film', A(1, 0, -.15), cut='zoom', cam0=PORT(.5, .5, 1.1), cam1=PORT(.5, .5, 1.3))
beat('count', Wd(1, NW['300'], -.05), to=300, prefix='$', **NUM, until=A(1, 2, -.1))
beat('punch', A(1, 2, .2), shot='s02', level=1.25)
# ---- 3 bank still charges interest; store hides it
shot('s03', CUPS, 'film', A(2, 0, -.15), cut='whip', cam0=PORT(.5, .55, 1.15), cam1=PORT(.5, .55, 1.35))
beat('circle', A(2, 1, .3), shot='s03', c=c('cup_coin', [.5, .6]), r=[170, 140], col='#FFC23A', until=A(3, 0, -.4))
# ---- 4 Goldie joke
shot('s04', CTR, 'soft', A(3, 0, -.35), cam0=PORT(.5, .5, 1.12), cam1={'z': 1.18})
beat('moment', A(3, 0, -.3), what='char', shot='s04', who='c_goldie', side='M', lines=[3], shrink=A(3, 1, .2), leave=A(4, 0, -.25))
# ---- 5 OPEN LOOP 1: where does the interest go?
shot('s05', CUPS, 'film', A(4, 0, -.15), cut='zoomIn', cam0=PORT(.5, .55, 1.3), cam1=PORT(.5, .58, 1.55))
# ---- 6 into the discount: cash $255 vs you $300
shot('s06', BUY, 'film', A(5, 0, -.15), cut='whip', cam0=PORT(.5, .5, 1.1), cam1=PORT(.5, .5, 1.25))
beat('slam', Wd(5, NW['255'], -.03), to=255, prefix='$', **NUM, until=A(5, 2, -.1))
beat('circle', A(5, 2, .4), shot='s06', c=c('long_receipt', [.65, .75]), r=[180, 260], until=A(6, 0, -.1))
# ---- 7 tax on hidden interest + processing fee
shot('s07', BUY, 'film', A(6, 0, -.12), cut='zoomIn', cam0=PORT(*c('long_receipt_cam', [.62, .7]), 1.45), cam1=PORT(*c('long_receipt_cam', [.62, .78]), 1.6))
beat('punch', A(6, 1, .3), shot='s07', level=1.3)
# ---- 8 OPEN LOOP 2: the part almost nobody reads
shot('s08', 'note_falling', 'film', A(7, 0, -.1), cut='flash', cam0={'x': .5, 'y': .4, 'z': 1.25}, cam1={'x': .5, 'y': .45, 'z': 1.5})
beat('shake', A(7, 0, 1.0), k=.5)
# ---- 9 2013: RBI said zero percent interest doesn't exist
shot('s09', 'central_bank', 'film', A(8, 0, -.15), cut='whip', cam0={'x': .45, 'y': .4, 'z': 1.2}, cam1={'x': .5, 'y': .4, 'z': 1.4})
beat('slam', Wd(8, 1, -.03), to=2013, **NUM, until=A(8, 1, -.1))
beat('punch', A(8, 1, 1.2), shot='s09', level=1.3)
# ---- 10 PAYOFF: mirage (hero flash)
shot('s10', 'p_mirage', 'film', A(9, 0, -.15), cut='zoom', cam0={'x': .62, 'y': .35, 'z': 1.1}, cam1={'x': .62, 'y': .3, 'z': 1.3}, shim=[1.0], shimRect=[.3, 0, .75, .55])
shot('s11', 'p_mirage_empty', 'film', A(9, 1, -.05), cut='flash', depthOf='p_mirage', cam0={'x': .58, 'y': .33, 'z': 1.3}, cam1={'x': .5, 'y': .45, 'z': 1.1}, shim=[.6], shimRect=[.3, 0, .75, .55])
shot('s12', CTR, 'film', A(9, 2, -.1), cut='whip', cam0=PORT(.5, .5, 1.35), cam1=PORT(.5, .5, 1.15))
# ---- 11 21% more for the same phone
shot('s13', BUY, 'film', A(10, 0, -.15), cut='zoom', cam0=PORT(.5, .45, 1.2), cam1=PORT(.5, .5, 1.35))
beat('count', Wd(10, NW['21'], -.05), to=21, prefix='+', suffix='%', **NUM, until=A(11, 0, -.4))
# ---- 12 Bill twist: cash is the discount?
shot('s14', ENV, 'soft', A(11, 0, -.35), cam0=PORT(.5, .5, 1.12), cam1={'z': 1.18})
beat('moment', A(11, 0, -.3), what='char', shot='s14', who='c_bill', side='M', lines=[11], grow=A(11, 0, .8), leave=A(12, 0, -.25))
# ---- 13 loop to hook: no cost... for the store
shot('s15', CUPS, 'film', A(12, 0, -.15), cut='zoomIn', cam0=PORT(.5, .5, 1.1), cam1=PORT(.5, .55, 1.35))
beat('moment', A(12, 1, 0), what='grade', shot='s15', bright=.6, sat=.4, d=.6)
# ---- 14 comment
shot('s16', CTR, 'film', A(13, 0, -.15), cut='zoom', cam0=PORT(.5, .5, 1.2), cam1=PORT(.5, .5, 1.35))
beat('punch', A(13, 0, .8), shot='s16', level=1.25)
# ---- 15 sign-off
shot('s17', 'wallet_desk', 'soft', A(14, 0, -.15), cut='zoom', cam0={'x': .55, 'y': .58, 'z': 1.15}, cam1={'x': .55, 'y': .58, 'z': 1.3})
beat('moment', A(14, 0, 0), what='follow', btn=A(14, 0, .5), click=Wd(14, FOLLOW_W, .1), y=330)

SH = [{k: v for k, v in s.items() if v is not None} for s in SH]
json.dump({'shots': SH, 'beats': BT}, open(os.path.join(HERE, 'shots.json'), 'w'), ensure_ascii=False, indent=1)
print(LANG, len(SH), 'shots', len(BT), 'beats', 'plates:', CTR, ENV, CUPS, BUY)
