# Money Mirage Short s013 (digital arrest): whole shot plan, native portrait 1080x1920, data for build.py --port. Copied from s001's grammar.
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
CALL, PARCEL, XFER, FAKESET, COURT = P('da_videocall', 'red_phone'), P('da_parcel', 'medicine_bottle'), P('da_transfer', 'wallet_desk'), P('da_fakeset', 'tv_1971'), P('da_court', 'central_bank')
PORT = lambda x=.5, y=.5, z=1.05: {'x': x, 'y': y, 'z': z}
FOLLOW_W = 4
NW = {'260000': 11, '200': 5}
C = json.load(open(os.path.join(HERE, 'coords.json'))) if os.path.exists(os.path.join(HERE, 'coords.json')) else {}
c = lambda k, d: C.get(k, d)

# ---- 1 HOOK: police on a video call, would you pay $260,000?
shot('s00', CALL, 'film', A(0), cam0=PORT(.5, .42, 1.15), cam1=PORT(.5, .38, 1.3))
beat('card', {'abs': 0.12}, text='VIDEO CALL → *ARRESTED?*', y=280, size=120, blur=True, until={'abs': 2.4})
beat('punch', A(0, 0, .5), shot='s00', level=1.15)
beat('punch', A(0, 1, .35), shot='s00', level=1.28); beat('shake', A(0, 1, .9), k=.5)
beat('count', Wd(0, NW['260000'], -.05), to=260000, prefix='$', **NUM, until=A(1, 0, -.1))
beat('punch', A(0, 2, 1.2), shot='s00', level=1.4)
# ---- 2 one woman did, in a single week
shot('s01', XFER, 'film', A(1, 0, -.15), cut='whip', cam0=PORT(.5, .45, 1.2), cam1=PORT(.5, .5, 1.45))
beat('punch', A(1, 1, .3), shot='s01', level=1.3)
# ---- 3 no such thing as digital arrest; the officer was a scammer
shot('s02', 'phones_offhook', 'film', A(2, 0, -.15), cut='zoom', cam0={'x': .45, 'y': .4, 'z': 1.3}, cam1={'x': .5, 'y': .42, 'z': 1.45}, handheld=.1)
beat('punch', A(2, 1, .4), shot='s02', level=1.3)
# ---- 4 Bill: I'd have paid too
shot('s03', XFER, 'soft', A(3, 0, -.35), cam0=PORT(.5, .5, 1.12), cam1={'z': 1.18})
beat('moment', A(3, 0, -.3), what='char', shot='s03', who='c_bill', side='M', lines=[3], shrink=A(3, 0, .7), leave=A(4, 0, -.25))
# ---- 5 OPEN LOOP 1: so why do smart people pay?
shot('s04', CALL, 'film', A(4, 0, -.15), cut='zoomIn', cam0=PORT(.5, .4, 1.25), cam1=PORT(.5, .36, 1.5))
beat('punch', A(4, 0, .8), shot='s04', level=1.35)
# ---- 6 parcel, drugs, uniform, fake station
shot('s05', PARCEL, 'film', A(5, 0, -.15), cut='whip', cam0=PORT(.5, .5, 1.1), cam1=PORT(.5, .55, 1.3))
beat('circle', A(5, 1, .1), shot='s05', c=c('parcel_packets', [.5, .5]), r=[200, 160], col='#FFC23A', until=A(5, 2, -.1))
shot('s06', FAKESET, 'film', A(5, 2, -.15), cut='zoom', cam0=PORT(.5, .45, 1.3), cam1=PORT(.5, .42, 1.15), depthOf=None)
beat('punch', A(5, 3, .3), shot='s06', level=1.25)
# ---- 7 don't hang up, tell no one
shot('s07', CALL, 'film', A(6, 0, -.15), cut='whip', cam0=PORT(.5, .38, 1.35), cam1=PORT(.5, .36, 1.55))
beat('moment', A(6, 1, 0), what='grade', shot='s07', bright=.6, sat=.4, d=.6)
# ---- 8 $200 million lost in 2024
shot('s08', 'vault_empty', 'film', A(7, 0, -.15), cut='zoom', cam0={'x': .3, 'y': .45, 'z': 1.25}, cam1={'x': .3, 'y': .45, 'z': 1.45})
beat('count', Wd(7, NW['200'], -.05), to=200, prefix='$', suffix='M', **NUM, until=A(8, 0, -.1))
# ---- 9 OPEN LOOP 2: the part that empties accounts
shot('s09', XFER, 'film', A(8, 0, -.12), cut='flash', cam0=PORT(.5, .42, 1.4), cam1=PORT(.5, .4, 1.6))
beat('shake', A(8, 0, .9), k=.6)
# ---- 10 move savings to a "safe" account
shot('s10', XFER, 'film', A(9, 0, -.15), cut='zoom', cam0=PORT(.5, .5, 1.1), cam1=PORT(.5, .4, 1.35))
beat('arrow', A(9, 1, .2), shot='s10', **{'from': c('xfer_from', [.3, .7]), 'to': c('xfer_to', [.5, .4])}, col='#FFC23A', until=A(10, 0, -.2))
# ---- 11 PAYOFF: the mirage - the set behind the camera (hero flash)
shot('s11', 'p_mirage', 'film', A(10, 0, -.15), cut='zoom', cam0={'x': .62, 'y': .35, 'z': 1.1}, cam1={'x': .62, 'y': .3, 'z': 1.3}, shim=[1.0], shimRect=[.3, 0, .75, .55])
shot('s12', FAKESET, 'film', A(10, 1, -.05), cut='flash', cam0=PORT(.5, .45, 1.35), cam1=PORT(.5, .45, 1.05))
beat('punch', A(10, 1, 1.4), shot='s12', level=1.2)
# ---- 12 Supreme Court: banks that miss red flags should pay back
shot('s13', COURT, 'film', A(11, 0, -.15), cut='whip', cam0=PORT(.5, .4, 1.1), cam1=PORT(.5, .38, 1.3))
beat('punch', A(11, 1, .5), shot='s13', level=1.25)
# ---- 13 loop to hook: real police never arrest you on a video call
shot('s14', CALL, 'film', A(12, 0, -.15), cut='zoomIn', cam0=PORT(.5, .4, 1.4), cam1=PORT(.5, .45, 1.05))
beat('circle', A(12, 0, .9), shot='s14', c=c('call_screen', [.5, .4]), r=[230, 300], until=A(12, 1, -.1))
beat('moment', A(12, 1, .1), what='grade', shot='s14', bright=.55, sat=.3, d=.6)
# ---- 14 comment prompt
shot('s15', 'phones_offhook', 'film', A(13, 0, -.15), cut='zoom', cam0={'x': .5, 'y': .45, 'z': 1.2}, cam1={'x': .5, 'y': .45, 'z': 1.35})
beat('punch', A(13, 0, .7), shot='s15', level=1.25)
# ---- 15 sign-off
shot('s16', 'wallet_desk', 'soft', A(14, 0, -.15), cut='zoom', cam0={'x': .55, 'y': .58, 'z': 1.15}, cam1={'x': .55, 'y': .58, 'z': 1.3})
beat('moment', A(14, 0, 0), what='follow', btn=A(14, 0, .5), click=Wd(14, FOLLOW_W, .1), y=330)

SH = [{k: v for k, v in s.items() if v is not None} for s in SH]
json.dump({'shots': SH, 'beats': BT}, open(os.path.join(HERE, 'shots.json'), 'w'), ensure_ascii=False, indent=1)
print(LANG, len(SH), 'shots', len(BT), 'beats', 'plates:', CALL, PARCEL, XFER, FAKESET, COURT)
