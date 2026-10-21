# Money Mirage ep01 thumbnails v3 — built from study findings (person/document + one puzzle, <=3 words,
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

V = {}
# ---------- A: the man + the number ----------
V['a'] = dict(css='''
#hero{position:absolute;left:640px;top:0;width:1280px;height:1080px;object-fit:cover;object-position:50% 40%}
.fade{position:absolute;left:600px;top:0;width:420px;height:1080px;background:linear-gradient(90deg,#0B1324 0%,rgba(11,19,36,.85) 35%,rgba(11,19,36,0) 100%)}
.big{position:absolute;left:110px;top:150px;font-weight:900;font-size:470px;line-height:.86;letter-spacing:-22px;color:#F3EBDD;text-shadow:0 12px 0 rgba(0,0,0,.5)}
.sub{position:absolute;left:124px;top:600px;font-weight:900;font-size:250px;line-height:.86;letter-spacing:-6px;color:#E9B44C;text-shadow:0 10px 0 rgba(0,0,0,.5)}
''', body='''<img id="hero" src="assets/nixon_tight.png"><div class="fade"></div>
<div class="big">0%</div><div class="sub">GOLD</div>
<svg class="ov" width="1920" height="1080">%C%</svg>''',
    svg=scribble(430, 385, 370, 265, rot=-5, seed=3, w=18),
    treat=[('#hero', '{"intensity":1,"adjust":{"contrast":0.08,"highlights":-0.06,"shadows":0.04},"effects":{"twoInkPrint":1,"twoInkPrintSize":0.36}}')],
    assets=['nixon_tight.png'])

# ---------- B: the document nobody remembers ----------
V['b'] = dict(css='''
#doc{position:absolute;left:900px;top:-20px;width:1120px;transform:rotate(4deg);transform-origin:50% 0;box-shadow:-30px 40px 80px rgba(0,0,0,.7)}
.bgdoc{position:absolute;inset:0;background:radial-gradient(ellipse 70% 80% at 70% 40%,#1A2742 0%,#0B1324 60%,#060A14 100%)}
.l1{position:absolute;left:70px;top:110px;font-weight:900;font-size:200px;line-height:.9;letter-spacing:-6px;color:#E9B44C;text-shadow:0 10px 0 rgba(0,0,0,.5)}
.l2{position:absolute;left:70px;top:300px;font-weight:900;font-size:200px;line-height:.9;letter-spacing:-6px;color:#F3EBDD;text-shadow:0 10px 0 rgba(0,0,0,.5)}
.l3{position:absolute;left:62px;top:500px;padding:6px 30px 18px;background:#E8322A;font-weight:900;font-size:200px;line-height:.9;letter-spacing:-6px;color:#fff;transform:rotate(-3deg);box-shadow:0 12px 0 rgba(0,0,0,.45)}
''', body='''<div class="bgdoc"></div><img id="doc" src="assets/eo6102.jpg">
<div class="l1">GOLD</div><div class="l2">WAS</div><div class="l3">ILLEGAL</div>
<svg class="ov" width="1920" height="1080">%C%</svg>''',
    svg=scribble(1435, 378, 445, 58, rot=5, seed=5, w=14), treat=[('#doc', '{"intensity":1,"adjust":{"contrast":0.12,"temperature":0.05}}')],
    assets=['eo6102.jpg'])

# ---------- C: the IOU ----------
def guilloche(cx, cy, R, r, k, n=900, col='#3E5B45', sw=1.4, op=.55):
    pts = []
    for i in range(n + 1):
        t = 2 * math.pi * i / n * 1
        rr = R + r * math.sin(k * t)
        pts.append((cx + rr * math.cos(t), cy + rr * math.sin(t)))
    return f'<path d="M{" L".join(f"{x:.1f},{y:.1f}" for x,y in pts)}Z" fill="none" stroke="{col}" stroke-width="{sw}" opacity="{op}"/>'
rose = lambda cx, cy, s: ''.join(guilloche(cx, cy, s * (0.55 + .09 * j), s * .16, 18 + 2 * j) for j in range(5))
border = ''.join(f'<rect x="{30+i*7}" y="{30+i*7}" width="{1440-2*(30+i*7)}" height="{640-2*(30+i*7)}" rx="{26-i*2}" fill="none" stroke="#3E5B45" stroke-width="{2.4 if i in (0,4) else 1}" opacity=".7"/>' for i in range(5))
wave = ''.join(f'<path d="M80,{110+j*6} ' + ' '.join(f'Q{80+x+15},{110+j*6+(8 if (x//30)%2 else -8)} {80+x+30},{110+j*6}' for x in range(0, 1260, 30)) + '" fill="none" stroke="#3E5B45" stroke-width=".9" opacity=".35"/>' for j in range(4))
wave2 = wave.replace('110+', '510+')
NOTE = f'''<g transform="translate(160,180) scale(1.11) rotate(-7 720 320)">
<rect x="18" y="26" width="1440" height="640" rx="30" fill="rgba(0,0,0,.55)" filter="url(#blur)"/>
<rect x="0" y="0" width="1440" height="640" rx="30" fill="url(#paper)"/>
{border}
<g>{rose(250,330,170)}{rose(1190,330,170)}</g>
<g>{''.join(guilloche(720,330,250+8*j,22,40,col='#2F4A37',op=.35) for j in range(3))}</g>
<ellipse cx="720" cy="318" rx="190" ry="222" fill="#E6E9D6" stroke="#2F4A37" stroke-width="5"/>
<clipPath id="ov"><ellipse cx="720" cy="318" rx="180" ry="212"/></clipPath>
<image id="face" href="assets/nixon_face_engraved.png" x="520" y="96" width="400" height="444" preserveAspectRatio="xMidYMid slice" clip-path="url(#ov)"/>
<text x="120" y="170" font-family="Inter" font-weight="900" font-size="120" fill="#2F4A37">1</text>
<text x="1320" y="170" font-family="Inter" font-weight="900" font-size="120" fill="#2F4A37" text-anchor="end">1</text>
<text x="120" y="590" font-family="Inter" font-weight="900" font-size="120" fill="#2F4A37">1</text>
<text x="1320" y="590" font-family="Inter" font-weight="900" font-size="120" fill="#2F4A37" text-anchor="end">1</text>
<text x="720" y="80" font-family="Inter" font-weight="800" font-size="30" letter-spacing="10" fill="#2F4A37" text-anchor="middle">PAYABLE TO THE BEARER</text>
<text x="720" y="604" font-family="Inter" font-weight="800" font-size="26" letter-spacing="8" fill="#2F4A37" text-anchor="middle">NOT REDEEMABLE IN GOLD</text>
</g>'''
STAMP = '''<g transform="translate(1400,700) rotate(-14) scale(.88)" filter="url(#ink)">
<rect x="-430" y="-200" width="860" height="400" rx="34" fill="none" stroke="#E8322A" stroke-width="30"/>
<rect x="-392" y="-162" width="784" height="324" rx="20" fill="none" stroke="#E8322A" stroke-width="8"/>
<text x="0" y="118" font-family="Inter" font-weight="900" font-size="330" letter-spacing="-6" fill="#E8322A" text-anchor="middle">IOU</text></g>'''
DEFS = '''<defs><linearGradient id="paper" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E9ECD9"/><stop offset=".55" stop-color="#D6DEC4"/><stop offset="1" stop-color="#C3CDAE"/></linearGradient>
<filter id="blur"><feGaussianBlur stdDeviation="18"/></filter>
<filter id="ink" x="-20%" y="-20%" width="140%" height="140%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4" result="n"/>
<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.4 1.55" result="m"/><feComposite in="SourceGraphic" in2="m" operator="in" result="c"/>
<feTurbulence type="fractalNoise" baseFrequency=".012" numOctaves="2" seed="9" result="w"/><feDisplacementMap in="c" in2="w" scale="10"/></filter>
<radialGradient id="halo" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#E9B44C" stop-opacity=".35"/><stop offset="1" stop-color="#E9B44C" stop-opacity="0"/></radialGradient></defs>'''
V['c'] = dict(css='''.bgc{position:absolute;inset:0;background:radial-gradient(ellipse 65% 70% at 50% 50%,#1A2742 0%,#0B1324 60%,#05080F 100%)}
#facesrc{position:absolute;left:-2000px;top:0;width:1008px;height:1008px}''',
    body='<div class="bgc"></div><svg class="ov" width="1920" height="1080">' + DEFS + '<ellipse cx="960" cy="560" rx="900" ry="520" fill="url(#halo)"/>' + NOTE + STAMP + '</svg>',
    svg='', treat=[], assets=['nixon_face_engraved.png'])

for k, v in V.items():
    d = os.path.join(HERE, 'v' + k); os.makedirs(d + '/assets', exist_ok=True)
    shutil.copy(HERE + '/gsap.min.js', d)
    for f in ['inter900.woff2', 'inter800.woff2'] + v['assets']:
        if os.path.exists(HERE + '/assets/' + f): shutil.copy(HERE + '/assets/' + f, d + '/assets/')
    html = HEAD.replace('%CSS%', v['css']).replace('%BODY%', v['body'].replace('%C%', v['svg']))
    open(d + '/index.html', 'w').write(html)
    open(d + '/treat.txt', 'w').write('\n'.join(f'{s}\t{g}' for s, g in v['treat']))
print('ok')
