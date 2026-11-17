# Shot plan: "8 Romania facts nobody believes" (BHUGOL EN long-form, GTA-video style).
# Exec'd by make.py (st(n) = start of script line n, WT(n, word) = start of a word).
NSTOPS, COUNTDOWN, TRKWORD = 8, True, 'FACT'
MAPSRC = {'ro': 'eox'}
STOPS_T = []
RO = 'ROMANIA'

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
    CLIPTAG[n_] = ('real', ' '.join(row[5:]).replace('_', ' ') if len(row) > 5 else RO)
def V(t0, t1, names, fallback, label=None, **kw):
    """clips if we have them, otherwise the fallback photo"""
    got = [n for n in names if n in HAVE]
    if got: vids(t0, t1, got)
    else: photo(t0, t1, fallback, label=label, **kw)
def PX(t0, t1, f, label, **kw): return photo(t0, t1, f, label=label, **kw)
def MIX(t0, t1, items):
    """fast cuts: split [t0,t1] evenly; item = clip name or (photo, label[, zoom]) tuple"""
    n = len(items); d = (t1 - t0) / n
    for i, it in enumerate(items):
        a, b = t0 + i * d, t0 + (i + 1) * d
        if isinstance(it, str): vids(a, b, [it])
        elif len(it) > 3: photo(a, b, it[0], label=it[1], mode=it[3])
        else: photo(a, b, it[0], label=it[1], zoom=it[2] if len(it) > 2 else (1, 1.08))

# Romania plate: 3531 x 2516 px (EOX z9). Whole country at z .5, regional zoom up to ~1.15.
C0 = [1765, 1250]
PLACES = {'bucharest': (26.10, 44.43, 'BUCHAREST'), 'sapanta': (23.69, 47.97, 'SĂPÂNȚA'), 'bran': (25.367, 45.515, 'BRAN'),
          'transf': (24.617, 45.604, 'TRANSFĂGĂRĂȘAN'), 'brasov': (25.59, 45.65, 'BRAȘOV'), 'turda': (23.79, 46.587, 'TURDA'),
          'movile': (28.58, 43.82, 'MOVILE CAVE')}
ORDER = ['bucharest', 'sapanta', 'bran', 'transf', 'brasov', 'bucharest', 'turda', 'movile']
def romap(t0, t1, z0=.56, z1=.6, focus=None, items=(), zf=1.0):
    if focus:
        lo, la, _ = PLACES[focus]; p = mxy('ro', lo, la)
        cam = [[t0 - .5, {'x': C0[0], 'y': C0[1], 'z': z0}, .1], [t0, {'x': p[0], 'y': p[1], 'z': zf}, max(.8, t1 - t0) * .8 + .3, 'sine.inOut']]
    else:
        cam = [[t0 - .5, {'x': C0[0], 'y': C0[1], 'z': z0}, .1], [t0, {'z': z1}, t1 - t0 + .5, 'none']]
    return mapshot(t0, t1, 'ro', cam, items)
def place_pin(key, a0, a1, fs=40, dy=-58):
    lo, la, nm = PLACES[key]; return pin('ro', lo, la, a0, a1, nm, fs=fs, dy=dy)

P_ATH = ('bucharest_romanian_athenaeum_29141749601_jpg.jpg', 'ROMANIAN ATHENAEUM · BUCHAREST')
P_CEC = ('palacio_cec_bucarest_ruman_a_2016_05_29_dd_65_jpg.jpg', 'CEC PALACE · BUCHAREST')
P_ARC = ('arcul_de_triumf_jpg.jpg', 'ARCUL DE TRIUMF · BUCHAREST')
P_M1 = ('merry_cemetery_s_p_n_a_2017_jpg.jpg', 'MERRY CEMETERY · SĂPÂNȚA')
P_M2 = ('ro_mm_sapanta_merry_cemetery_2_jpg.jpg', 'MERRY CEMETERY · SĂPÂNȚA')
P_M3 = ('merry_cemetery_sapanta_romania_01_jpg.jpg', 'MERRY CEMETERY · SĂPÂNȚA')
P_MD = ('merry_cemetery_sapanta_romania_detail_jpg.jpg', 'MERRY CEMETERY · SĂPÂNȚA', (1.04, 1.14))
P_MC = ('crosses_at_merry_cemetery_sapanta_village_romania_.jpg', 'MERRY CEMETERY · SĂPÂNȚA')
P_B1 = ('bran_castle_28535731471_jpg.jpg', 'BRAN CASTLE')
P_B2 = ('bran_castle_toerzburg_or_castelul_bran_05asd_jpg.jpg', 'BRAN CASTLE')
P_B3 = ('bran_seen_from_bran_castle_jpg.jpg', 'BRAN')
P_TR = ('transfagarasan_road_unsplash_jpg.jpg', 'TRANSFĂGĂRĂȘAN')
P_TL = ('lake_b_lea_and_the_transf_g_r_an_road_jpg.jpg', 'BÂLEA LAKE · TRANSFĂGĂRĂȘAN')
P_TC = ('transfagarasan_road_from_balea_lake_to_c_r_i_oara_.jpg', 'TRANSFĂGĂRĂȘAN')
P_FG = ('f_g_ra_mountains_romania_view_from_sibiu_04_jpg.jpg', 'FĂGĂRAȘ MOUNTAINS')
P_BR = ('carpathian_brown_bear_232367505_jpeg.jpg', 'CARPATHIANS · ROMANIA')
P_W1 = ('romania_bear_warning_jpg.jpg', 'ROMANIA')
P_W2 = ('bear_warning_jpg.jpg', 'ROMANIA')
P_PA = ('palace_of_the_parliament_in_bucharest_51878975552_.jpg', 'PALACE OF THE PARLIAMENT')
P_PB = ('bucharest_palace_of_parliament_may_2016_001_jpg.jpg', 'PALACE OF THE PARLIAMENT')
P_27 = ('bucharest_in_1927_jpg.jpg', 'BUCHAREST · 1927')
P_ST = ('salina_turda_romania_jpg.jpg', 'SALINA TURDA')
P_S5 = ('salina_turda_5_jpg.jpg', 'SALINA TURDA')
P_SZ = ('tereziamijn_salina_turda_jpg.jpg', 'TEREZIA MINE · SALINA TURDA')
P_S3 = ('salina_turda_3_jpg.jpg', 'TEREZIA MINE · SALINA TURDA')
P_SL = ('unterirdischer_see_in_der_alten_mine_von_turda_jpg.jpg', 'TEREZIA MINE · SALINA TURDA')
P_MV = 'movile_cave_schematic_illustration_jpg.jpg'
P_TG = 'various_aquatic_troglobites_from_movile_cave_png.jpg'
P_CR = 'cryptops_speleorex_holotype_jpg.jpg'
P_MG = ('09_09_21_mangalia_641025_51490333746_jpg.jpg', 'MANGALIA')
P_MP = ('portul_turistic_mangalia_marea_neagr_rom_nia_jpg.jpg', 'MANGALIA · BLACK SEA')
P_M19 = ('mangalia_2019_jpg.jpg', 'MANGALIA')
P_MB = ('mangalia_2015_2_jpg.jpg', 'MANGALIA · BLACK SEA')
P_MB2 = ('mangalia_2015_3_jpg.jpg', 'MANGALIA')
P_XS = 'movile_cave_x_section_png.jpg'
P_NP = 'image_of_the_troglofaunal_water_scorpion_nepa_anop.jpg'
P_CALEA = ('149_calea_victoriei_bucharest_01_jpg.jpg', 'CALEA VICTORIEI · BUCHAREST')

# ================= HOOK (1-8) =================
MIX(0, st(2), ['transf_a', 'bran_a', 'palace_a'])
K(WT(1, 'hundred', '100') - .1, st(2) - .1, 'THE BET', '$100', fs=120)
MIX(st(2), st(3), [(P_MV, 'MOVILE CAVE · ROMANIA', None, 'card'), (P_NP, 'MOVILE CAVE · ROMANIA', None, 'card')])
CNT(WT(2, 'five') + .1, st(3) - .1, 5500000, unit=' YEARS', y=150, fs=120, dur=1.4)
MIX(st(3), st(4), ['turda_wheel', 'turda_crowd'])
vids(st(4), st(5), ['palace_b'])
MIX(st(5), st(6), ['transf_c', 'transf_f'])
MIX(st(6), st(7), ['bran_b2', 'bran_d'])
MIX(st(7), st(8), ['merry_walk', 'bear_road', 'turda_wheel2'])
its = []
for j_, k_ in enumerate(ORDER):
    lo, la, _ = PLACES[k_]; its.append({'k': 'pin', 'p': mxy('ro', lo, la), 'a': [[WT(8, 'eight') + .08 * j_, 1, .35, 'back.out'], [st(9) + .3, 0, .3]]})
romap(st(8), st(9) + .2, .56, .6, items=its)

# ================= #8 LITTLE PARIS (9-14) =================
romap(st(9), WT(9, 'once'), focus='bucharest', items=place_pin('bucharest', WT(9, 'once') - .6, WT(9, 'once') + .3), zf=1.1)
CHAP(8, 'Little Paris', st(9), WT(9, 'once') - .2)
MIX(WT(9, 'once'), st(10), [P_ATH, 'palace_d'])
MIX(st(10), st(11), [P_CEC, (P_ATH[0], P_ATH[1], (1.12, 1.2)), 'arc_night'])
K(WT(10, 'little'), WT(10, 'grand') - .1, 'NICKNAME', 'Little Paris')
MIX(st(11), st(12), ['arc_a', 'arc_b'])
K(WT(11, 'arc'), st(12) - .15, 'BUCHAREST', 'Arc de Triomphe')
MIX(st(12), st(13), [P_ARC, 'arc_night'])
K(WT(12, 'wood'), st(13) - .15, 'FIRST VERSION · 1878', 'Made of wood')
MIX(st(13), st(14), ['arc_b', (P_ARC[0], P_ARC[1], (1.0, 1.1))])
CNT(WT(13, 'twentyseven', '27', 'twenty'), WT(13, 'paris') - .1, 27, unit=' m', y=260)
K(WT(13, 'paris'), st(14) - .15, 'PARIS HAS THE ORIGINAL', 'Bucharest has the copy', fs=70)
MIX(st(14), st(15), ['merry_church', 'merry_cross'])

# ================= #7 MERRY CEMETERY (15-20) =================
romap(st(15), WT(15, 'village'), focus='sapanta', items=place_pin('sapanta', WT(15, 'village') - .6, st(16) + .3), zf=1.1)
CHAP(7, 'Merry Cemetery', st(15), WT(15, 'village') - .2)
vids(WT(15, 'village'), st(16), ['merry_wide'])
MIX(st(16), st(17), ['merry_walk', P_M1])
K(WT(16, '1935'), st(17) - .15, 'STAN IOAN PĂTRAȘ', 'Since 1935', fs=90)
MIX(st(17), st(18), ['merry_cross', P_M3])
MIX(st(18), st(19), [P_M2, P_MD])
K(WT(18, 'mother') - .05, st(19) - .15, 'TARGET', 'The mother-in-law', fs=80)
MIX(st(19), st(20), ['merry_crosses', P_MC])
CNT(WT(19, 'eight'), st(20) - .1, 800, unit='+ CROSSES', y=240, fs=150)
MIX(st(20), st(21), ['merry_close', 'merry_tower'])

# ================= #6 FAKE DRACULA (21-27) =================
romap(st(21), WT(21, 'sold'), focus='bran', items=place_pin('bran', WT(21, 'sold') - .6, WT(21, 'sold') + .3), zf=1.1)
CHAP(6, 'Fake Dracula', st(21), WT(21, 'sold') - .2)
vids(WT(21, 'sold'), st(22), ['bran_a'])
K(WT(21, 'dracula'), st(22) - .15, 'SOLD AS', 'Dracula’s Castle', fs=90)
MIX(st(22), st(23), ['bran_c', P_B1])
K(WT(22, 'never'), st(23) - .15, 'BRAM STOKER', 'Never visited Romania', fs=80)
MIX(st(23), st(24), ['bran_d', P_B3])
MIX(st(24), st(25), ['bran_e', P_B2])
K(WT(24, 'lived'), st(25) - .15, 'VLAD THE IMPALER', 'Never lived here', fs=86)
MIX(st(25), st(26), ['bran_b2', 'bran_c'])
MIX(st(26), st(27), ['bran_v', P_B1])
K(WT(26, 'archduke') - .1, st(27) - .15, 'OWNER', 'An Austrian archduke', fs=84)
MIX(st(27), st(28), ['transf_e', P_FG])

# ================= #5 ROAD OF FEAR (28-34) =================
romap(st(28), st(29), focus='transf', items=place_pin('transf', st(29) - .6, st(29) + .3), zf=1.1)
CHAP(5, 'Road of fear', st(28), st(29) - .2)
MIX(st(29), st(30), [P_FG, 'transf_e'])
K(WT(29, '1968'), st(30) - .15, 'AUGUST 1968', 'Soviets invade Czechoslovakia', fs=64)
MIX(st(30), st(31), ['transf_b', 'transf_lake'])
MIX(st(31), st(32), ['transf_a', 'transf_c', 'transf_d'])
CNT(WT(31, '2042', 'two'), st(32) - .1, 2042, unit=' m', y=240, fs=170)
MIX(st(32), st(33), ['transf_f', P_TR])
K(WT(32, 'best'), st(33) - .15, 'TOP GEAR · 2009', '“The best road in the world”', fs=66)
MIX(st(33), st(34), ['transf_cabins', P_TL])
K(WT(33, 'october'), st(34) - .15, 'CLOSED BY SNOW', 'Late Oct → late June', fs=80)
MIX(st(34), st(35), ['transf_d', 'bear_hill'])

# ================= #4 BEAR COUNTRY (35-41) =================
romap(st(35), WT(35, 'europe'), focus='brasov', items=place_pin('brasov', WT(35, 'brown') + .1, st(36) + .3), zf=1.0)
CHAP(4, 'Bear country', st(35), WT(35, 'brown') - .1)
MIX(WT(35, 'europe'), st(36), [P_BR, 'bear_hill2'])
MIX(st(36), st(37), ['bear_walk', 'bear_close2'])
K(WT(36, 'twentyfour', '24', 'twenty'), st(37) - .15, 'DNA SAMPLES', '24,000+', fs=110)
MIX(st(37), st(38), ['bear_hill', 'bear_close'])
K(WT(37, 'ten'), st(38) - .15, 'BROWN BEARS IN ROMANIA', '10,600 – 12,800', fs=100)
romap(st(38), WT(38, 'thirteen') + .4, focus='brasov', items=place_pin('brasov', st(38) + .2, WT(38, 'thirteen') + .6), zf=1.15)
MIX(WT(38, 'thirteen') + .4, st(39), ['bear_gold', 'bear_close2'])
CNT(WT(38, 'thirteen'), st(39) - .1, 1300, unit=' BEARS', y=240, fs=150)
MIX(st(39), st(40), ['bear_road', 'bear_road2'])
MIX(st(40), st(41), [P_W1, P_W2])
K(WT(40, 'bear'), st(41) - .15, 'ATENȚIE!', 'Bear zone', fs=100)
MIX(st(41), st(42), ['palace_c', P_PB])

# ================= #3 HEAVIEST BUILDING (42-49) =================
romap(st(42), WT(42, 'bucharest'), focus='bucharest', items=place_pin('bucharest', WT(42, 'bucharest') - .6, st(43) + .3), zf=1.1)
CHAP(3, 'Heaviest building', st(42), WT(42, 'bucharest') - .1)
vids(WT(42, 'bucharest'), st(43), ['palace_a'])
MIX(st(43), st(44), ['palace_b', P_PA, 'palace_c'])
CNT(WT(43, 'four'), st(44) - .1, 4000000, unit=' TONNES', y=240, fs=150, dur=1.5)
K(WT(43, 'guinness') - .1, WT(43, 'four') - .15, 'GUINNESS WORLD RECORDS', 'Heaviest building', fs=86)
MIX(st(44), st(45), [P_PA, P_PB])
CNT(WT(44, 'eleven'), WT(44, 'in') - .1, 1100, unit=' ROOMS', y=240, fs=160)
K(WT(44, 'four'), st(45) - .15, 'IN USE (2013)', '~400 rooms', fs=100)
MIX(st(45), st(46), [P_27, P_CALEA, (P_27[0], P_27[1], (1.14, 1.24))])
K(WT(45, 'seven'), st(46) - .15, 'DEMOLISHED', '7 km² of old Bucharest', fs=76)
MIX(st(46), st(47), [(P_27[0], P_27[1], (1.1, 1.2)), 'palace_c'])
CNT(WT(46, 'forty'), st(47) - .1, 40000, unit=' PEOPLE', y=240, fs=160)
MIX(st(47), st(48), ['palace_d', 'palace_b'])
CNT(WT(47, 'six'), st(48) - .1, 6, prefix='$', unit='M+ / YEAR', y=240, fs=170, dur=.8)
MIX(st(48), st(49), ['palace_a', P_PA])
K(WT(48, '1989'), st(49) - .15, 'DECEMBER 1989', 'Overthrown', fs=100)
MIX(st(49), st(50), ['turda_shaft', P_S5])

# ================= #2 SALT THEME PARK (50-58) =================
romap(st(50), WT(50, 'salt'), focus='turda', items=place_pin('turda', WT(50, 'salt') - .6, st(51) + .3), zf=1.1)
CHAP(2, 'Salt theme park', st(50), WT(50, 'salt') - .1)
vids(WT(50, 'salt'), st(51), ['turda_lights'])
MIX(st(51), st(52), [P_SZ, 'turda_shaft'])
CNT(WT(51, '1271'), st(52) - .1, 1271, prefix='SINCE ', y=240, fs=170, frm=1000)
MIX(st(52), st(53), [P_S5, ('rudolfmijn_salina_turda_jpg.jpg', 'RUDOLF MINE · SALINA TURDA', (1.0, 1.08))])
K(WT(52, 'hundred'), st(53) - .15, 'DUG BY HAND', '~90 m tall halls', fs=96)
MIX(st(53), st(54), ['turda_dome', P_ST])
MIX(st(54), st(55), ['turda_wheel', 'turda_lights', 'turda_dome'])
MIX(st(55), st(56), ['turda_wheel2', 'turda_crowd'])
K(WT(55, 'ferris'), st(56) - .15, 'UNDERGROUND', 'Ferris wheel · bowling · mini golf', fs=60)
MIX(st(56), st(57), [P_S3, P_SL])
MIX(st(57), st(58), ['turda_crowd', (P_ST[0], P_ST[1], (1.1, 1.2))])
romap(st(58), st(59), .56, .62)

# ================= #1 SEALED CAVE (59-68) =================
romap(st(59), WT(59, 'black'), focus='movile', items=place_pin('movile', WT(59, 'black') - .6, st(60) + .3), zf=1.1)
CHAP(1, 'Sealed cave', st(59), WT(59, 'black') - .1)
PX(WT(59, 'black'), st(60), P_MP[0], P_MP[1])
MIX(st(60), st(61), [P_M19, (P_XS, 'MOVILE CAVE · CROSS-SECTION', None, 'card')])
K(WT(60, '1986'), st(61) - .15, 'DISCOVERED', '1986', fs=110)
MIX(st(61), st(62), [(P_MV, 'MOVILE CAVE', None, 'card'), (P_TG, 'MOVILE CAVE', (1.0, 1.1))])
CNT(WT(61, 'five'), st(62) - .1, 5500000, unit=' YEARS', y=220, fs=150, dur=1.4)
romap(st(62), WT(62, 'ours'), focus='movile', items=place_pin('movile', st(62) + .1, WT(62, 'ours') + .3), zf=1.15)
PX(WT(62, 'ours'), st(63), P_MB[0], P_MB[1])
K(WT(62, 'seven'), WT(62, 'ours') - .1, 'OXYGEN INSIDE', '7–10%', fs=120)
K(WT(62, 'ours'), st(63) - .15, 'OXYGEN OUT HERE', '21%', fs=120)
PX(st(63), st(64), P_TG, 'MOVILE CAVE', mode='card')
MIX(st(64), st(65), [(P_CR, 'MOVILE CAVE', None, 'card'), (P_NP, 'NEPA ANOPHTHALMA · MOVILE CAVE', None, 'card')])
CNT(WT(64, 'thirtyseven', '37', 'thirty'), st(65) - .1, 37, unit=' FOUND NOWHERE ELSE', y=200, fs=110)
MIX(st(65), st(66), [(P_TG, 'MOVILE CAVE', (1.12, 1.24)), (P_NP, 'WATER SCORPION · MOVILE CAVE', (1.0, 1.12)), (P_CR, 'MOVILE CAVE', (1.05, 1.15))])
PX(st(66), st(67), P_MV, 'MOVILE CAVE', zoom=(1.0, 1.08))
romap(st(67), WT(67, 'scientists'), focus='movile', items=place_pin('movile', st(67) + .1, WT(67, 'scientists') + .3), zf=1.15)
PX(WT(67, 'scientists'), st(68), P_XS, 'MOVILE CAVE · CROSS-SECTION', mode='card')
K(WT(67, 'few'), st(68) - .15, 'ACCESS', 'A few scientists a year', fs=84)
vids(st(68), WT(68, 'cave'), ['palace_a', 'palace_b'])
PX(WT(68, 'cave'), st(69), P_MV, 'MOVILE CAVE', mode='card')

# ================= ENDING + CTA (69-73) =================
its = []
for j_, k_ in enumerate(ORDER):
    lo, la, _ = PLACES[k_]; its.append({'k': 'pin', 'p': mxy('ro', lo, la), 'a': [[st(69) + .06 * j_, 1, .35, 'back.out'], [WT(69, 'owe') + .3, 0, .3]]})
romap(st(69), WT(69, 'owe'), .56, .62, items=its)
MIX(WT(69, 'owe'), st(70), ['bran_a', 'turda_crowd'])
MIX(st(70), st(71), ['merry_crosses', 'bear_walk'])
K(WT(69, 'owe'), st(70) - .15, 'THE BET', '$100', fs=120)
MIX(st(71), st(72), ['transf_a', 'bran_b2', 'turda_wheel'])
MIX(st(72), st(73), ['transf_cabins', 'turda_lights'])
beat(k='sub', at=WT(72, 'subscribe') - .2, until=st(73) - .1)
MIX(st(73), DUR, ['merry_aerial', 'transf_lake'])
END_STOPS = st(69)

MUS = ME + '/outputs/fetch/gta6-music/'
MUSIC_SECTIONS = [
    {'file': MUS + 'eighties_action.mp3', 'from': 0, 'to': st(28), 'gain_db': -18},
    {'file': MUS + 'cyborg_ninja.mp3', 'from': st(28) - .75, 'to': st(50), 'gain_db': -18},
    {'file': MUS + 'ouroboros.mp3', 'from': st(50) - .75, 'to': st(69), 'gain_db': -18},
    {'file': MUS + 'eighties_action.mp3', 'from': st(69) - .75, 'to': DUR, 'gain_db': -18}]
