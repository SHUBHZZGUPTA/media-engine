# Shot plan: "8 Philippines facts nobody believes" (BHUGOL EN long-form, GTA-video style).
# Exec'd by make.py (st(n) = start of script line n, WT(n, word) = start of a word).
NSTOPS, COUNTDOWN, TRKWORD = 8, True, 'FACT'
MAPSRC = {}
STOPS_T = []
PHN = 'PHILIPPINES'

_EN = {}
for _l in open(PROJ + '/script_en.txt'):
    _m = re.match(r'^(\d+) (.*)', _l.strip())
    if _m: _EN[int(_m.group(1))] = [norm(x) for x in _m.group(2).replace('*', '').replace('$100', 'a hundred dollars').split() if norm(x)]
def WT(n, *words, occ=1, end=False):
    """start (or end) time of a word in line n: exact token match first, then substring; tries each candidate"""
    for word in words:
        w = norm(word)
        for exact in (True, False):
            c = 0
            for k in range(len(sw)):
                if sl[k] == n - L0 and ((sw[k] == w) if exact else (w in sw[k])):
                    c += 1
                    if c == occ: return tt[k][1] if end else tt[k][0]
    en = _EN.get(n, [])
    for word in words:
        w = norm(word)
        for k, t in enumerate(en):
            if t == w or w in t:
                f = k / max(1, len(en)); t0, t1 = st(n), (st(n + 1) if n < L1 else DUR)
                return t0 + f * (t1 - t0) + (.25 if end else 0)
    raise SystemExit(f'none of {words} in line {n}')
def K(at, until, top, txt, fs=None, **kw):
    b = dict(k='kick', at=at, until=until, top=top, txt=txt, x=110, y=650); b.update(kw)
    if fs: b['fs'] = fs
    return beat(**b)
def CNT(at, until, to, unit='', prefix='', y=300, fs=190, dur=1.2, frm=0):
    return beat(k='count', at=at, until=until, to=to, unit=unit, prefix=prefix, y=y, fs=fs, dur=dur, **{'from': frm})
def CHAP(n, name, at, until):
    beat(k='chap', at=at + .1, until=min(until, at + 1.8), top=f'FACT #{n}', txt=name)
    STOPS_T.append((at - .1, n))

HAVE = set(os.path.basename(p)[:-5] for p in _glob.glob(CL + '/*.webm'))
for n_, row in SEL.items():
    CLIPTAG[n_] = ('real', ' '.join(row[5:]).replace('_', ' ') if len(row) > 5 else PHN)
def PX(t0, t1, f, label, **kw): return photo(t0, t1, f, label=label, **kw)
def CL_(name, fb):
    """a clip if we downloaded it, otherwise the fallback photo item"""
    return name if name in HAVE else fb
def MIX(t0, t1, items):
    """fast cuts: split [t0,t1] evenly; item = clip name or (photo, label[, zoom]) tuple"""
    n = len(items); d = (t1 - t0) / n
    for i, it in enumerate(items):
        a, b = t0 + i * d, t0 + (i + 1) * d
        if isinstance(it, str): vids(a, b, [it] + [c for c in items if isinstance(c, str) and c != it])
        elif len(it) > 3: photo(a, b, it[0], label=it[1], mode=it[3])
        else: photo(a, b, it[0], label=it[1], zoom=it[2] if len(it) > 2 and it[2] else (1, 1.08))

# ---------- maps ----------
# phw: whole country (z7, padded 16:9, 2832x1593) · ph: z9 plate 3932x6375 for regional zooms · taal / pina: z13 close plates
PLACES = {'leyte': (124.9, 11.6, 'LEYTE & SAMAR'), 'manila': (120.98, 14.6, 'MANILA'), 'bohol': (124.15, 9.83, 'BOHOL'),
          'trench': (126.6, 9.5, 'PHILIPPINE TRENCH'), 'pinatubo': (120.35, 15.14, 'MT PINATUBO'), 'taal': (121.0, 14.0, 'TAAL')}
ORDER = ['leyte', 'manila', 'manila', 'bohol', 'bohol', 'trench', 'pinatubo', 'taal']
def COV(k): W_, H_ = MAPS[k]['size']; return max(1920 / W_, 1080 / H_)
def wmap(t0, t1, z0=1.0, z1=1.06, items=()):
    WC = _clamp('phw', mxy('phw', 121.8, 12.9), z0)
    cam = [[t0 - .5, {'x': WC[0], 'y': WC[1], 'z': z0}, .1], [t0, {'z': z1}, t1 - t0 + .5, 'none']]
    return mapshot(t0, t1, 'phw', cam, items)
def wpins(a, b, keys=ORDER, step=.08):
    its = []
    for j_, k_ in enumerate(dict.fromkeys(keys)):
        lo, la, _ = PLACES[k_]; its.append({'k': 'pin', 'p': mxy('phw', lo, la), 'a': [[a + step * j_, 1, .35, 'back.out'], [b, 0, .3]]})
    return its
def _clamp(k, p, z):
    W_, H_ = MAPS[k]['size']; sc = z * COV(k); hw, hh = 960 / sc, 540 / sc
    return [min(max(p[0], hw), W_ - hw) if W_ > 2 * hw else W_ / 2, min(max(p[1], hh), H_ - hh) if H_ > 2 * hh else H_ / 2]
def zcam(k, t0, t1, keys, ease='sine.inOut'):
    """camera keys [(t, lon, lat, z), ...] on plate k, clamped inside the plate"""
    cam = []
    for j, (t, lo, la, z) in enumerate(keys):
        c = _clamp(k, mxy(k, lo, la), z)
        if j == 0: cam.append([t - .5, {'x': c[0], 'y': c[1], 'z': z}, .1])
        else: cam.append([keys[j - 1][0], {'x': c[0], 'y': c[1], 'z': z}, max(.3, t - keys[j - 1][0]), ease])
    return cam
def fmap(t0, t1, key, zf=2.0, z0=1.0, dy_lbl=-58):
    """zoom from the whole width of the country into a place on the z9 plate, pin + label it once the chapter card clears"""
    lo, la, nm = PLACES[key]
    cam = zcam('ph', t0, t1, [(t0, lo, la, z0), (t0 + max(.8, t1 - t0) * .8 + .3, lo, la, zf)])
    return mapshot(t0, t1, 'ph', cam, pin('ph', lo, la, min(t0 + 1.9, t1 - .4), t1 + .3, nm, dy=dy_lbl))

# ---------- photos (file, label) ----------
P_ISL = ('elnido2.jpg', 'EL NIDO · PALAWAN'); P_ISL2 = ('elnido3.jpg', 'EL NIDO · PALAWAN'); P_ISL3 = ('elnido.jpg', 'PALAWAN'); P_ISL4 = ('elnido4.jpg', 'EL NIDO · PALAWAN')
P_PHIL = ('philip.jpg', 'PHILIP II OF SPAIN'); P_PHY = ('philip_young.jpg', 'PRINCE PHILIP · 1550s'); P_VIL = ('villa.jpg', 'VILLALOBOS EXPEDITION ACCOUNT')
P_MALL = ('mall_sep.jpg', 'MALL OF ASIA · SEPTEMBER 2025'); P_GLF = ('glf3.jpg', 'GIANT LANTERN · SAN FERNANDO'); P_PAR = ('parols.jpg', 'PAROLS · PAMPANGA'); P_LAN = ('lanterns.jpg', 'PAROLS · PHILIPPINES')
P_MSKY = ('manila_sky.jpg', 'MANILA'); P_MDR = ('manila_drone.jpg', 'MANILA'); P_BIN = ('binondo.jpg', 'BINONDO · MANILA'); P_J1 = ('jeep1.jpg', 'JEEPNEY · METRO MANILA'); P_J2 = ('jeep2.jpg', 'JEEPNEY · QUIAPO, MANILA')
P_CRW = ('crowd.jpg', 'MANILA BAYWALK'); P_NYC = ('manhattan.jpg', 'MANHATTAN · NEW YORK'); P_NYC2 = ('manh2.jpg', 'MANHATTAN · NEW YORK')
P_T1 = ('tarsier_real.jpg', 'PHILIPPINE TARSIER · BOHOL'); P_T2 = ('tars2.jpg', 'PHILIPPINE TARSIER'); P_T3 = ('tars4.jpg', 'PHILIPPINE TARSIER · BOHOL'); P_T4 = ('tars3.jpg', 'PHILIPPINE TARSIER')
P_C1 = ('choc1.jpg', 'CHOCOLATE HILLS · BOHOL'); P_C2 = ('choc2.jpg', 'CHOCOLATE HILLS · BOHOL'); P_C3 = ('choc3.jpg', 'CHOCOLATE HILLS · CARMEN, BOHOL'); P_C4 = ('choc4.jpg', 'CHOCOLATE HILLS · BOHOL'); P_C5 = ('choc5.jpg', 'CHOCOLATE HILLS · BOHOL')
P_EV = ('everest.jpg', 'MOUNT EVEREST · 8,849 m'); P_SUB = ('sub.jpg', 'DEEP-SEA SUBMERSIBLE')
P_PN1 = ('pina1.jpg', 'MT PINATUBO · 12 JUNE 1991'); P_PN0 = ('pinatubo91.jpg', 'MT PINATUBO · 1991'); P_PN2 = ('pina2.jpg', 'MT PINATUBO · 15 JUNE 1991'); P_PN3 = ('pina3.jpg', 'ASHFALL · CUBI POINT, 1991')
P_PL = ('pinalake.jpg', 'LAKE PINATUBO'); P_PL2 = ('pina_lake2.jpg', 'MT PINATUBO')
P_TA = ('taal13.jpg', 'TAAL VOLCANO ISLAND'); P_TA2 = ('taal_air.jpg', 'TAAL VOLCANO ISLAND'); P_TA3 = ('taal05.jpg', 'TAAL LAKE'); P_TG = ('taal_tagaytay.jpg', 'TAAL LAKE · FROM TAGAYTAY')
P_CR1 = ('taal_crater.jpg', 'TAAL MAIN CRATER LAKE'); P_CR2 = ('taal_cl.jpg', 'TAAL MAIN CRATER LAKE'); P_CR3 = ('taal_lakelake.jpg', 'TAAL MAIN CRATER LAKE'); P_TW = ('tawilis.jpg', 'TAWILIS · TAAL LAKE')

# ================= HOOK (1-8) =================
MIX(0, st(2), [CL_('isl_a', P_ISL), CL_('isl_b', P_ISL2)])
K(WT(1, 'hundred') - .1, st(2) - .1, 'THE BET', '$100', fs=120)
wmap(st(2), st(3), 1.0, 1.08)
CNT(WT(2, 'seven') + .1, WT(2, 'more') - .1, 7641, unit=' ISLANDS', y=150, fs=130, dur=1.6, frm=1000)
K(WT(2, 'more'), st(3) - .1, 'ADDED BY SATELLITE', '+534 islands', fs=100)
MIX(st(3), st(4), [CL_('isl_c', P_ISL3), CL_('isl_d', P_ISL4)])
PX(st(4), st(5), *P_TW, zoom=(1.0, 1.1))
MIX(st(5), st(6), [P_PN1, P_PN2])
PX(st(6), st(7), *P_TA, zoom=(1.0, 1.12))
MIX(st(7), st(8), [CL_('choc_a', P_C1), CL_('tars_a', P_T1), CL_('man_a', P_MSKY)])
wmap(st(8), st(9) + .2, 1.0, 1.05, items=wpins(WT(8, 'eight'), st(9) + .3))

# ================= #8 THE BORROWED NAME (9-15) =================
fmap(st(9), WT(9, 'named'), 'leyte', zf=1.8)
CHAP(8, 'Borrowed name', st(9), WT(9, 'named') - .2)
MIX(WT(9, 'named'), st(10), [(P_PHIL[0], P_PHIL[1], None, 'card')])
mapshot(st(10), st(11), 'ph', zcam('ph', st(10), st(11), [(st(10), 125.0, 11.6, 1.3), (st(11) + .3, 125.0, 11.6, 1.7)]),
        pin('ph', 125.0, 12.0, WT(10, 'two') - .1, st(11) + .2, 'SAMAR') + pin('ph', 124.85, 10.95, WT(10, 'two') + .1, st(11) + .2, 'LEYTE'))
K(WT(10, '1543'), st(11) - .15, 'RUY LÓPEZ DE VILLALOBOS', '1543 · “Las Islas Filipinas”', fs=70)
MIX(st(11), st(12), [(P_PHY[0], P_PHY[1], None, 'card'), (P_PHIL[0], P_PHIL[1], None, 'card')])
K(WT(11, 'king'), st(12) - .15, 'LATER', 'King Philip II', fs=90)
wmap(st(12), st(13), 1.0, 1.08, items=wpins(WT(12, 'spread'), st(13) + .2, keys=['leyte', 'manila', 'bohol', 'pinatubo', 'taal'], step=.12))
MIX(st(13), st(14), [(P_PHIL[0], P_PHIL[1], None, 'card'), CL_('isl_b', P_ISL2)])
K(WT(13, 'never'), st(14) - .15, 'PHILIP II', 'Never visited', fs=110)
MIX(st(14), st(15), [CL_('isl_d', P_ISL3), CL_('isl_e', P_ISL4)])
CNT(WT(14, 'seven'), st(15) - .1, 7641, unit=' ISLANDS', y=240, fs=140, frm=1000)
MIX(st(15), st(16), [P_LAN, P_PAR])

# ================= #7 CHRISTMAS IN SEPTEMBER (16-22) =================
MIX(st(16), WT(16, 'september'), [P_PAR])
CHAP(7, 'Early Christmas', st(16), WT(16, 'september') - .1)
MIX(WT(16, 'september'), st(17), [CL_('mall_a', P_MALL)])
K(WT(16, 'september'), st(17) - .15, 'CHRISTMAS STARTS', 'September 1', fs=100)
MIX(st(17), st(18), [P_MALL, CL_('mall_a', P_LAN)])
MIX(st(18), st(19), [CL_('lant_b', P_LAN), (P_MALL[0], P_MALL[1], (1.1, 1.2))])
K(WT(18, 'four'), st(19) - .15, 'SEPT · OCT · NOV · DEC', '4 months of jingle bells', fs=70)
MIX(st(19), st(20), [P_PAR, CL_('lant_c', P_LAN)])
K(WT(19, 'january'), st(20) - .15, 'AND THEN', 'Into January', fs=100)
MIX(st(20), st(21), [(P_GLF[0], P_GLF[1], None, 'card'), CL_('lant_a', P_PAR)])
CNT(WT(20, 'twelve'), st(21) - .1, 12000, unit=' BULBS', y=240, fs=150)
K(WT(20, 'six'), WT(20, 'twelve') - .1, 'GIANT PAROLS', '6 m wide', fs=110)
MIX(st(21), st(22), [CL_('isl_e', P_ISL2), (P_MALL[0], P_MALL[1], (1.08, 1.16))])
MIX(st(22), st(23), [CL_('man_e', P_MSKY), P_BIN])

# ================= #6 THE CROWDED CAPITAL (23-29) =================
fmap(st(23), WT(23, 'capital'), 'manila', zf=2.2)
CHAP(6, 'Crowded capital', st(23), WT(23, 'capital') - .1)
MIX(WT(23, 'capital'), st(24), [CL_('man_a', P_MDR)])
MIX(st(24), st(25), [CL_('man_b', P_MDR), P_CRW])
K(WT(24, 'one'), st(25) - .15, 'CITY OF MANILA', '1.8 million people', fs=100)
MIX(st(25), st(26), [CL_('man_c', P_BIN), CL_('man_d', P_J2)])
CNT(WT(25, 'forty'), st(26) - .1, 42, unit=' km²', y=240, fs=170)
MIX(st(26), st(27), [P_NYC, P_MSKY])
K(WT(26, 'manhattan'), st(27) - .15, 'MANILA vs MANHATTAN', 'More people · less space', fs=76)
MIX(st(27), st(28), [CL_('man_g', P_J1), CL_('man_b', P_CRW)])
CNT(WT(27, 'forty'), st(28) - .1, 40000, unit='+ / km²', y=240, fs=150)
MIX(st(28), st(29), [CL_('man_f', P_BIN), P_J2])
MIX(st(29), st(30), [CL_('tars_b', P_T2), P_T3])

# ================= #5 THE TARSIER'S EYES (30-36) =================
fmap(st(30), WT(30, 'tarsier'), 'bohol', zf=2.2)
CHAP(5, 'Tarsier eyes', st(30), WT(30, 'tarsier') - .1)
MIX(WT(30, 'tarsier'), st(31), [CL_('tars_a', P_T1)])
MIX(st(31), st(32), [CL_('tars_d', P_T3), CL_('tars_b', P_T4)])
K(WT(31, 'hand'), st(32) - .15, 'SIZE', 'Fits in your hand', fs=100)
MIX(st(32), st(33), [(P_T2[0], P_T2[1], (1.15, 1.3))])
CNT(WT(32, 'sixteen'), st(33) - .1, 16, unit=' mm', y=240, fs=180)
MIX(st(33), st(34), [CL_('tars_c', P_T1), (P_T2[0], P_T2[1], (1.25, 1.4))])
K(WT(33, 'entire'), st(34) - .15, 'EACH EYE', 'As big as its brain', fs=100)
MIX(st(34), st(35), [CL_('tars_b', P_T4), CL_('tars_c', P_T3), (P_T1[0], P_T1[1], (1.1, 1.2))])
K(WT(34, 'backwards'), st(35) - .15, 'EYES STUCK IN PLACE', 'So the head turns ~180°', fs=80)
MIX(st(35), st(36), [CL_('tars_c', P_T2), CL_('tars_d', P_T3)])
MIX(st(36), st(37), [CL_('choc_a', P_C1), P_C3])

# ================= #4 THE CHOCOLATE HILLS (37-43) =================
fmap(st(37), WT(37, 'chocolate'), 'bohol', zf=2.2)
CHAP(4, 'Chocolate Hills', st(37), WT(37, 'chocolate') - .1)
MIX(WT(37, 'chocolate'), st(38), [CL_('choc_a', P_C2)])
MIX(st(38), st(39), [CL_('choc_b', P_C3), P_C4])
CNT(WT(38, 'twelve'), WT(38, 'maybe') - .1, 1200, unit='+ HILLS', y=240, fs=160)
K(WT(38, 'maybe'), st(39) - .15, 'MAYBE', 'Up to ~1,776', fs=110)
MIX(st(39), st(40), [CL_('choc_c', P_C1), CL_('choc_d', P_C5), CL_('choc_e', P_C3)])
MIX(st(40), st(41), [P_C2, CL_('choc_b', P_C4)])
K(WT(40, 'dry'), st(41) - .15, 'DRY SEASON', 'Green → chocolate brown', fs=86)
MIX(st(41), st(42), [CL_('choc_b', P_C5), P_C1])
K(WT(41, 'limestone'), st(42) - .15, 'SADLY', 'Limestone, not chocolate', fs=86)
MIX(st(42), st(43), [CL_('choc_e', P_C3), CL_('choc_a', P_C2)])
MIX(st(43), st(44), [CL_('sea_a', P_SUB)])

# ================= #3 THE BOTTOMLESS TRENCH (44-50) =================
wmap(st(44), WT(44, 'trench') + .6, 1.0, 1.1, items=pin('phw', *PLACES['trench'][:2], st(44) + 1.9, st(45) + .3, 'PHILIPPINE TRENCH'))
CHAP(3, 'The deep trench', st(44), WT(44, 'trench') - .1)
MIX(WT(44, 'trench') + .6, st(45), [CL_('sea_a', P_SUB)])
MIX(st(45), st(46), [CL_('sea_b', P_SUB), (P_SUB[0], P_SUB[1], (1.1, 1.22))])
CNT(WT(45, 'ten'), st(46) - .1, 10540, unit=' m DEEP', y=240, fs=150, dur=1.5)
MIX(st(46), st(47), [P_EV, (P_EV[0], P_EV[1], (1.12, 1.25))])
K(WT(46, 'two'), st(47) - .15, 'EVEREST IN THE TRENCH', '~1.7 km of water on top', fs=74)
MIX(st(47), st(48), [CL_('sea_a', P_SUB), (P_EV[0], P_EV[1], (1.0, 1.1))])
K(WT(47, 'deepest'), st(48) - .15, 'IN 1951', 'Deepest spot ever measured', fs=80)
MIX(st(48), st(49), [(P_SUB[0], P_SUB[1], (1.05, 1.15)), CL_('sea_b', P_SUB)])
K(WT(48, '2021'), st(49) - .15, 'MARCH 2021', 'First crewed dive · 10,045 m', fs=74)
MIX(st(49), st(50), [CL_('sea_b', (P_SUB[0], P_SUB[1], (1.2, 1.3)))])
K(WT(49, 'trash'), st(50) - .15, 'FOUND AT THE BOTTOM', 'Trash', fs=120)
MIX(st(50), st(51), [P_PN0, P_PL])

# ================= #2 THE VOLCANO THAT COOLED THE PLANET (51-59) =================
fmap(st(51), WT(51, 'pinatubo'), 'pinatubo', zf=2.2)
CHAP(2, 'Cooling volcano', st(51), WT(51, 'pinatubo') - .1)
MIX(WT(51, 'pinatubo'), st(52), [P_PN0])
MIX(st(52), st(53), [P_PN1, P_PN2])
K(WT(52, 'second'), st(53) - .15, 'JUNE 1991', '2nd-biggest eruption of the 1900s', fs=66)
MIX(st(53), st(54), [(P_PN1[0], P_PN1[1], (1.1, 1.22))])
CNT(WT(53, 'forty'), st(54) - .1, 40, unit=' km HIGH', y=240, fs=170)
MIX(st(54), st(55), [P_PN3, P_PN2])
K(WT(54, 'typhoon'), st(55) - .15, 'SAME DAY', 'Typhoon Yunya', fs=100)
wmap(st(55), st(56), 1.12, 1.0)
MIX(st(56), st(57), [(P_PN0[0], P_PN0[1], (1.12, 1.24)), P_PN1])
K(WT(56, 'half'), st(57) - .15, 'THE WHOLE PLANET', '−0.5 °C', fs=130)
MIX(st(57), st(58), [P_PN3, (P_PN2[0], P_PN2[1], (1.1, 1.2))])
mapshot(st(58), WT(58, 'today'), 'pinaw', zcam('pinaw', st(58), WT(58, 'today'), [(st(58), 120.35, 15.14, 1.0), (WT(58, 'today') + .3, 120.35, 15.14, 1.55)]),
        pin('pinaw', 120.35, 15.14, st(58) + .4, WT(58, 'today') + .3, 'MT PINATUBO'))
CNT(WT(58, 'two'), WT(58, 'today') - .1, 260, prefix='−', unit=' m', y=240, fs=170)
MIX(WT(58, 'today'), st(59), [CL_('pina_a', P_PL), CL_('pina_c', P_PL2)])
MIX(st(59), st(60), [CL_('pina_b', P_TA), CL_('taal_c', P_TA2)])

# ================= #1 THE ISLAND INCEPTION (60-69) =================
fmap(st(60), WT(60, 'volcano'), 'taal', zf=2.2)
CHAP(1, 'Island-ception', st(60), WT(60, 'volcano') - .1)
MIX(WT(60, 'volcano'), st(61), [P_TA, CL_('taal_a', P_TA2)])
# the nesting: one continuous zoom down the levels, each named as the narrator says it
mapshot(st(61), st(62), 'ph', zcam('ph', st(61), st(62), [(st(61), 121.0, 15.0, 1.0), (st(62) + .3, 121.0, 14.1, 1.7)]),
        pin('ph', 121.2, 15.7, WT(61, 'luzon'), st(62) + .2, 'LUZON'))
mapshot(st(62), st(65), 'taalw', zcam('taalw', st(62), st(65), [(st(62), 121.0, 13.97, 1.0), (st(63), 121.0, 13.97, 1.05),
                                                               (st(64), 120.995, 14.0, 1.35), (st(65), 120.999, 14.009, 1.75)]),
        pin('taalw', 121.08, 13.93, WT(62, 'taal') - .1, st(63) + .2, 'TAAL LAKE') +
        pin('taalw', 120.985, 13.985, WT(63, 'volcano') - .1, st(64) + .2, 'VOLCANO ISLAND', dy=-70) +
        pin('taalw', 120.999, 14.009, WT(64, 'crater') - .1, st(65) + .3, 'CRATER LAKE'))
MIX(st(65), st(66), [(P_CR2[0], P_CR2[1], (1.0, 1.12))])
K(WT(65, 'vulcan') - .05, st(66) - .1, 'THE INNERMOST ISLAND', 'Vulcan Point', fs=100)
MIX(st(66), st(67), [P_CR1, P_CR3, P_TA])
K(st(66) + .2, st(67) - .15, 'ISLAND · LAKE · ISLAND · LAKE · ISLAND', 'Five layers deep', fs=84)
MIX(st(67), st(68), [CL_('taal_b', P_TG), CL_('taal_d', P_TA3)])
K(WT(67, '1754'), st(68) - .15, 'AFTER 1754', 'Sea water → fresh water', fs=84)
MIX(st(68), st(69), [(P_TW[0], P_TW[1], (1.0, 1.1))])
K(WT(68, 'only'), st(69) - .15, 'TAWILIS', 'The only freshwater sardine', fs=80)
MIX(st(69), st(70), [P_TW, CL_('taal_c', P_TA)])

# ================= ENDING + CTA (70-74) =================
wmap(st(70), WT(70, 'owe'), 1.0, 1.05, items=wpins(st(70), WT(70, 'owe') + .3))
MIX(WT(70, 'owe'), st(71), [CL_('choc_a', P_C1), CL_('tars_a', P_T1)])
K(WT(70, 'owe'), st(71) - .15, 'THE BET', '$100', fs=120)
MIX(st(71), st(72), [CL_('isl_a', P_ISL), CL_('man_a', P_MSKY)])
MIX(st(72), st(73), [CL_('taal_a', P_TA), CL_('pina_d', P_PL), CL_('isl_d', P_ISL2)])
MIX(st(73), st(74), [CL_('choc_b', P_C3), CL_('man_a', P_GLF)])
beat(k='sub', at=WT(73, 'subscribe') - .2, until=st(74) - .1)
MIX(st(74), DUR, [CL_('isl_c', P_ISL3), CL_('isl_a', P_ISL4)])
END_STOPS = st(70)

KM = ME + '/outputs/fetch/bhugol-music/'; YT = ME + '/music-library/ytal/'
_ms = [(None, 9, KM + 'vivacity.mp3'), (9, 16, KM + 'gaslamp_funworks.mp3'), (16, 23, KM + 'wholesome.mp3'),
       (23, 30, KM + 'meatball_parade.mp3'), (30, 37, KM + 'sneaky_snitch.mp3'), (37, 44, KM + 'carefree.mp3'),
       (44, 51, YT + 'event_horizon.mp3'), (51, 60, YT + 'rapid_unscheduled_disassembly.mp3'), (60, 70, KM + 'mystery_bazaar.mp3'), (70, None, KM + 'ave_marimba.mp3')]
MUSIC_SECTIONS = [{'file': f, 'from': 0 if a is None else st(a) - .75, 'to': DUR if b is None else st(b), 'gain_db': -18} for a, b, f in _ms]
