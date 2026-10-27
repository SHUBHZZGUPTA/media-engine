# Money Mirage ep02 thumbnails (same recipe as ep01 v3) — built from study findings (person/document + one puzzle, <=3 words,
# number not in title, red hand-drawn circle, desaturated base + gold/red accent). One font: Inter.
import os, math, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))

def scribble(cx, cy, rx, ry, rot=-8, seed=1, turns=1.12, w=16, color='#E8322A'):
    """Hand-drawn marker loop: jittered ellipse that overshoots its start, like a quick pen circle."""
    R = random.Random(seed); pts = []; n = 90; a0 = R.uniform(0, 6.28)
    for i in range(int(n * turns) + 1):
        t = a0 + 2 * math.pi * i / n; k = 1 + .045 * math.sin(3 * t + seed) + R.uniform(-.012, .012) + .05 * i / n
        x, y = rx * k * math.cos(t), ry * k * math.sin(t); r = math.radians(rot)
        pts.append((cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r)))
    d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    return (f'<path d="{d}" fill="none" stroke="rgba(0,0,0,.35)" stroke-width="{w+6}" stroke-linecap="round" stroke-linejoin="round" transform="translate(4,6)"/>'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')

HEAD = '''<!doctype html><html><head><meta charset="UTF-8"><script src="./gsap.min.js"></script><style>
@font-face{font-family:Inter;font-weight:900;src:url(assets/inter900.woff2)}
@font-face{font-family:Inter;font-weight:800;src:url(assets/inter800.woff2)}
body{margin:0;background:#000}#root{position:relative;width:1920px;height:1080px;overflow:hidden;background:#0B1324;font-family:Inter}
svg.ov{position:absolute;left:0;top:0;pointer-events:none}
.grain{position:absolute;inset:0;opacity:.09;mix-blend-mode:overlay;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/></filter><rect width='300' height='300' filter='url(%23n)'/></svg>")}
%CSS%
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-width="1920" data-height="1080" data-duration="1">
%BODY%
<div class="grain"></div></div>
<script>document.fonts.ready.then(()=>{window.__timelines=window.__timelines||{};window.__timelines.main=gsap.timeline({paused:true}).to({},{duration:1});});</script></body></html>'''



def marker_arrow(x0, y0, x1, y1, bend=-120, w=24, color='#FF2A2A'):
    """Hand-drawn marker arrow: a curved shaft from (x0,y0) to (x1,y1) with a two-stroke head."""
    import math
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2; dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy)
    cx, cy = mx - dy / L * bend, my + dx / L * bend
    ang = math.atan2(y1 - cy, x1 - cx); h = 140
    p1 = (x1 - h * math.cos(ang - .5), y1 - h * math.sin(ang - .5)); p2 = (x1 - h * math.cos(ang + .5), y1 - h * math.sin(ang + .5))
    d = f'M{x0},{y0} Q{cx:.0f},{cy:.0f} {x1},{y1} M{p1[0]:.0f},{p1[1]:.0f} L{x1},{y1} L{p2[0]:.0f},{p2[1]:.0f}'
    return (f'<path d="{d}" fill="none" stroke="rgba(0,0,0,.45)" stroke-width="{w+8}" stroke-linecap="round" stroke-linejoin="round" transform="translate(5,8)"/>'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(0 0 18px rgba(255,40,40,.6))"/>')

V = {}
SIDE = '''
#hero{position:absolute;left:560px;top:0;width:1360px;height:1080px;object-fit:cover;object-position:%POS%}
.fade{position:absolute;left:520px;top:0;width:480px;height:1080px;background:linear-gradient(90deg,#0B1324 0%,rgba(11,19,36,.85) 35%,rgba(11,19,36,0) 100%)}
.big{position:absolute;left:90px;top:170px;font-weight:900;font-size:%BS%px;line-height:.86;letter-spacing:-14px;color:#F3EBDD;text-shadow:0 12px 0 rgba(0,0,0,.5)}
.sub{position:absolute;left:96px;top:%ST%px;font-weight:900;font-size:%SS%px;line-height:.86;letter-spacing:-6px;color:#E9B44C;text-shadow:0 10px 0 rgba(0,0,0,.5)}
.tag{position:absolute;left:80px;top:%ST%px;padding:6px 30px 18px;background:#E8322A;font-weight:900;font-size:%SS%px;line-height:.9;letter-spacing:-6px;color:#fff;transform:rotate(-3deg);box-shadow:0 12px 0 rgba(0,0,0,.45)}
'''
def mk(img, pos, big, sub, bs, ss, st, tag=False, circ=None):
    css = SIDE.replace('%POS%', pos).replace('%BS%', str(bs)).replace('%SS%', str(ss)).replace('%ST%', str(st))
    body = f'<img id="hero" src="assets/{img}"><div class="fade"></div><div class="big">{big}</div><div class="{"tag" if tag else "sub"}">{sub}</div><svg class="ov" width="1920" height="1080">%C%</svg>'
    return dict(css=css, body=body, svg=scribble(*circ) if circ else '', treat=[], assets=[img])
V['a'] = mk('boe_photo__print.jpg', '60% 40%', '15%', 'FAILED', 470, 250, 600, circ=(470, 370, 430, 235, -4, 3, 1.12, 18))
V['b'] = mk('vault_empty__film.jpg', '45% 50%', '£3.3BN', 'LOST', 300, 250, 470, tag=True, circ=(560, 300, 540, 175, -3, 5, 1.12, 16))
POP = '''
#hero{position:absolute;left:560px;top:0;width:1360px;height:1080px;object-fit:cover;object-position:45% 50%}
.glow{position:absolute;left:1180px;top:120px;width:760px;height:760px;border-radius:50%;background:radial-gradient(circle,rgba(255,196,80,.55) 0%,rgba(255,170,50,.18) 40%,rgba(255,170,50,0) 70%);mix-blend-mode:screen}
.fade{position:absolute;left:520px;top:0;width:520px;height:1080px;background:linear-gradient(90deg,#0A1430 0%,rgba(10,20,48,.8) 40%,rgba(10,20,48,0) 100%)}
.bgl{position:absolute;left:0;top:0;width:600px;height:1080px;background:radial-gradient(ellipse 120% 70% at 30% 35%,#1B2E63 0%,#0A1430 70%)}
.big{position:absolute;left:84px;top:150px;font-weight:900;font-size:310px;line-height:.86;letter-spacing:-14px;color:#FFD34D;-webkit-text-stroke:6px #2A1600;text-shadow:0 0 60px rgba(255,200,60,.55),0 14px 0 rgba(0,0,0,.7)}
.tag{position:absolute;left:74px;top:470px;padding:6px 34px 20px;background:#FF1F1F;font-weight:900;font-size:260px;line-height:.9;letter-spacing:-6px;color:#fff;transform:rotate(-3deg);box-shadow:0 14px 0 rgba(0,0,0,.55),0 0 60px rgba(255,40,40,.5)}
.vig{position:absolute;inset:0;background:radial-gradient(ellipse 85% 85% at 55% 50%,rgba(0,0,0,0) 55%,rgba(0,0,0,.45) 100%)}
'''
V['b2'] = dict(css=POP, body='<div class="bgl"></div><img id="hero" src="assets/vault_pop.jpg"><div class="glow"></div><div class="fade"></div><div class="vig"></div><div class="big">£3.3BN</div><div class="tag">LOST</div><svg class="ov" width="1920" height="1080">%C%</svg>',
    svg=scribble(570, 290, 560, 180, -3, 5, 1.12, 20, '#FF2A2A') + marker_arrow(1720, 960, 1165, 405, bend=-110, w=28), treat=[], assets=['vault_pop.jpg'])
V['c'] = mk('treasury_courtyard__film.jpg', '55% 50%', 'BROKEN', 'IN HOURS', 250, 170, 420, tag=False, circ=(1500, 690, 130, 210, 4, 7, 1.12, 14))
for k, v in V.items():
    d = os.path.join(HERE, 'v' + k); os.makedirs(d + '/assets', exist_ok=True)
    shutil.copy(HERE + '/gsap.min.js', d)
    for f in ['inter900.woff2', 'inter800.woff2'] + v['assets']: shutil.copy(HERE + '/assets/' + f, d + '/assets/')
    open(d + '/index.html', 'w').write(HEAD.replace('%CSS%', v['css']).replace('%BODY%', v['body'].replace('%C%', v['svg'])))
print('ok')
