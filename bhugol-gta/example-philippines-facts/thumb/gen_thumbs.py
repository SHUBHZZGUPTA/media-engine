#!/usr/bin/env python3
"""Philippines long-form thumbnails in the competitor-winning style: bright relief map, country filled, callouts."""
import json, math
D = '/home/claude/ph/thumb/'
def proj(base):
    p = json.load(open(D + base[:-4] + '.json')); N = 2 ** p['z'] * 256
    def merc(lo, la):
        s = math.sin(math.radians(la)); return (lo + 180) / 360 * N, (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * N
    cx, cy = merc(p['lonc'], p['latc'])
    return lambda lo, la: ((merc(lo, la)[0] - cx) * p['sc'] + 640, (merc(lo, la)[1] - cy) * p['sc'] + 360)
PL = {'taal': (121.0, 14.0), 'pina': (120.35, 15.14), 'manila': (120.98, 14.6), 'bohol': (124.15, 9.85), 'trench': (126.75, 10.2),
      'leyte': (125.0, 11.6), 'palawan': (118.7, 9.6), 'mindanao': (125.2, 7.6), 'luzon': (121.3, 16.8)}
CSS = """@font-face{font-family:BSD;font-weight:900;src:url(bsd900.woff2)}
html,body{margin:0;width:1280px;height:720px;overflow:hidden;font-family:BSD;background:#000}
.bg{position:absolute;inset:0;background-size:cover}
.bar{position:absolute;left:34px;top:30px;background:#0B0B0B;color:#fff;font-size:86px;line-height:1;padding:12px 22px 14px;border-radius:10px;white-space:nowrap;box-shadow:0 8px 0 rgba(0,0,0,.35)}
.ybar{background:#FFD21A;color:#0B0B0B;border:6px solid #0B0B0B}
.hl{display:inline-block;background:#FFD21A;color:#0B0B0B;padding:0 14px 2px;border-radius:8px;margin-left:6px}
.ybar .hl{background:#E8221B;color:#fff}
.t2{position:absolute;color:#fff;-webkit-text-stroke:13px #0B0B0B;paint-order:stroke fill;font-size:96px;line-height:1.02;white-space:nowrap}
.lab{position:absolute;background:#FFD21A;color:#0B0B0B;font-size:34px;line-height:1.05;padding:6px 12px 7px;border:4px solid #0B0B0B;border-radius:7px;white-space:nowrap;box-shadow:0 5px 0 #0B0B0B}
.ring{position:absolute;border:7px solid #FFD21A;border-radius:50%;box-shadow:0 0 0 4px #0B0B0B,inset 0 0 0 4px #0B0B0B}
.num{position:absolute;width:58px;height:58px;border-radius:50%;background:#FFD21A;border:5px solid #0B0B0B;color:#0B0B0B;font-size:40px;line-height:58px;text-align:center}
.cut{position:absolute;filter:drop-shadow(0 0 0 #0B0B0B) drop-shadow(8px 0 0 #0B0B0B) drop-shadow(-8px 0 0 #0B0B0B) drop-shadow(0 -8px 0 #0B0B0B) drop-shadow(0 8px 0 #0B0B0B)}
.inset{position:absolute;border-radius:50%;border:10px solid #fff;box-shadow:0 0 0 7px #0B0B0B,0 12px 0 7px #0B0B0B;background-size:cover}
"""
def arrow(x1, y1, x2, y2, col='#fff', curve=.25):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2; dx, dy = x2 - x1, y2 - y1
    cx, cy = mx - dy * curve, my + dx * curve
    ang = math.atan2(y2 - cy, x2 - cx); L = 24
    p1 = (x2 - L * math.cos(ang - .5), y2 - L * math.sin(ang - .5)); p2 = (x2 - L * math.cos(ang + .5), y2 - L * math.sin(ang + .5))
    path = f'M{x1:.0f},{y1:.0f} Q{cx:.0f},{cy:.0f} {x2:.0f},{y2:.0f}'
    head = f'M{p1[0]:.0f},{p1[1]:.0f} L{x2:.0f},{y2:.0f} L{p2[0]:.0f},{p2[1]:.0f}'
    return (f'<path d="{path}" stroke="#0B0B0B" stroke-width="15" fill="none" stroke-linecap="round"/><path d="{head}" stroke="#0B0B0B" stroke-width="15" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{path}" stroke="{col}" stroke-width="7" fill="none" stroke-linecap="round"/><path d="{head}" stroke="{col}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
def callouts(P, items):
    """items: (place, label, label_x, label_y, ring_r)"""
    svg, html = [], []
    for pl, txt, lx, ly, r in items:
        x, y = P(*PL[pl])
        html.append(f'<div class="ring" style="left:{x - r:.0f}px;top:{y - r * .8:.0f}px;width:{2 * r - 14:.0f}px;height:{1.6 * r - 14:.0f}px"></div>')
        html.append(f'<div class="lab" style="left:{lx}px;top:{ly}px">{txt}</div>')
        # arrow from label edge toward the ring
        ax = lx + (0 if lx > x else 10 + 17 * len(txt.split("<br>")[0])); ay = ly + 24
        ex, ey = x + (r + 6 if lx > x else -(r + 6)) * .9, y
        svg.append(arrow(ax, ay, ex, ey))
    return '<svg style="position:absolute;inset:0" width="1280" height="720">' + ''.join(svg) + '</svg>' + ''.join(html)
def page(name, base, body):
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="bg" style="background-image:url({base})"></div>{body}</body></html>'
    open(D + f'v_{name}.html', 'w').write(html)
def bar(words, hl, cls='bar', fs=86, left=34, top=30):
    return f'<div class="{cls}" style="font-size:{fs}px;left:{left}px;top:{top}px">{words} <span class="hl">{hl}</span></div>'

# 1 · "PHILIPPINES IS INSANE" + real fact callouts (GeoByJames / Coggnize formula)
P = proj('base_red.jpg')
page('1_insane_facts', 'base_red.jpg', bar('PHILIPPINES IS', 'INSANE') + callouts(P, [
    ('taal', 'ISLAND IN A LAKE<br>IN A VOLCANO', 380, 300, 22), ('pina', 'COOLED THE<br>PLANET', 470, 130, 22),
    ('bohol', 'CHOCOLATE<br>HILLS', 470, 520, 28), ('trench', 'DEEPER THAN<br>EVEREST', 1050, 560, 30)]))
# 2 · same, curiosity labels only
page('2_insane_lie', 'base_red.jpg', bar('PHILIPPINES IS', 'INSANE') + callouts(P, [
    ('taal', 'IMPOSSIBLE!', 440, 290, 26), ('pina', 'TRUE!', 560, 170, 26), ('bohol', 'LIE?', 560, 540, 28), ('trench', 'DEEPEST!', 1060, 600, 30), ('palawan', 'WRONG!', 420, 430, 24)]))
# 3 · flag fill + LIE labels (Borderline Wonders 149× formula)
Pf = proj('base_flag.jpg')
page('3_flag_nobody', 'base_flag.jpg', bar('NOBODY', 'BELIEVES') + callouts(Pf, [
    ('luzon', 'FAKE?', 560, 190, 30), ('taal', 'REAL!', 520, 330, 22), ('bohol', 'FAKE?', 1040, 470, 26), ('palawan', 'REAL!', 450, 520, 26)]))
# 4 · Taal inset: the #1 fact as the whole thumbnail
x, y = P(*PL['taal'])
page('4_taal_inset', 'base_red.jpg',
     f'<div class="inset" style="left:250px;top:250px;width:380px;height:380px;background-image:url(taal13.jpg);background-position:50% 50%;background-size:170%;filter:saturate(1.7) contrast(1.2) brightness(1.08)"></div>'
     f'<div class="ring" style="left:{x - 22:.0f}px;top:{y - 18:.0f}px;width:30px;height:24px"></div>'
     '<svg style="position:absolute;inset:0" width="1280" height="720">' + arrow(x - 26, y + 4, 640, 420, curve=-.15) + '</svg>'
     + bar('AN ISLAND IN A LAKE IN A', 'VOLCANO?!', fs=66))
# 5 · trench glow (Borderline "IT'S MOVING" formula)
Pt = proj('base_flag_tr.jpg'); tx, ty = Pt(*PL['trench'])
page('5_trench_everest', 'base_flag_tr.jpg', bar('DEEPER THAN', 'EVEREST?!') +
     '<svg style="position:absolute;inset:0" width="1280" height="720">' + arrow(560, 500, tx - 18, ty + 40, col='#fff', curve=.3) + '</svg>'
     f'<div class="lab" style="left:300px;top:470px;font-size:44px">10,540 m DEEP</div>')
# 6 · numbered countdown pins
nums = [('leyte', 8), ('manila', 6), ('bohol', 5), ('trench', 3), ('pina', 2), ('taal', 1), ('palawan', 7), ('mindanao', 4)]
OFF = {'pina': (-55, -30), 'manila': (-70, 20), 'taal': (30, 30), 'leyte': (10, -20)}
pins = ''.join(f'<div class="num" style="left:{P(*PL[k])[0] - 34 + OFF.get(k, (0, 0))[0]:.0f}px;top:{P(*PL[k])[1] - 34 + OFF.get(k, (0, 0))[1]:.0f}px">{n}</div>' for k, n in nums)
page('6_eight_pins', 'base_red.jpg', bar('8 FACTS NOBODY', 'BELIEVES', fs=78) + pins)
# 7 · "makes no sense" with ?! callouts on the trench version
Pr = proj('base_red_tr.jpg')
page('7_no_sense', 'base_red_tr.jpg', bar('PHILIPPINES MAKES NO', 'SENSE', fs=70) + callouts(Pr, [
    ('taal', '?!', 520, 290, 24), ('bohol', '?!', 600, 560, 28), ('trench', '?!', 1110, 330, 30), ('pina', '?!', 540, 170, 24)]))
# 8 · map + cartoon tarsier (character + map hybrid)
Pl = proj('base_red_l.jpg')
page('8_tarsier_map', 'base_red_l.jpg', bar('PHILIPPINES IS', 'INSANE') +
     '<img class="cut" src="tarsier_toon_cut.png" style="right:-10px;bottom:-40px;height:560px">' + callouts(Pl, [
    ('taal', 'ISLAND IN A LAKE<br>IN A VOLCANO', 110, 300, 24), ('bohol', 'CHOCOLATE<br>HILLS', 130, 520, 26)]))
# 9 · flag + real fact callouts, "SECRETS" headline (Borderline 38×)
page('9_flag_secrets', 'base_flag.jpg', bar('PHILIPPINES', 'SECRETS') + callouts(Pf, [
    ('taal', 'ISLAND IN A LAKE<br>IN A VOLCANO', 380, 300, 22), ('pina', 'COOLED THE<br>PLANET', 470, 130, 22),
    ('bohol', 'CHOCOLATE HILLS', 1000, 400, 26), ('trench', 'DEEPER THAN<br>EVEREST', 1040, 590, 28)]))
# 10 · Christmas: Santa on the map
page('10_christmas', 'base_red_l.jpg', bar('CHRISTMAS IN', 'SEPTEMBER?!', fs=80) +
     '<img class="cut" src="santa_cut.png" style="right:10px;bottom:-30px;height:600px">')
print('ok')
