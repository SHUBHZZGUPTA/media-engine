# The carrier object: an invented engraved banknote (never a real currency design).
# note_svg() returns inline SVG markup (1440 x 640 units) with an empty portrait oval at (720, 318);
# the scene places the gold coin (and its shrinking) in that oval as its own element.
import math

INK, INK2, PAPER = '#2F4A37', '#3E5B45', '#E6E9D6'


def guilloche(cx, cy, R, r, k, n=720, col=INK2, sw=1.3, op=.5):
    pts = []
    for i in range(n + 1):
        t = 2 * math.pi * i / n
        rr = R + r * math.sin(k * t)
        pts.append((cx + rr * math.cos(t), cy + rr * math.sin(t)))
    d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + 'Z'
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" opacity="{op}"/>'


def rose(cx, cy, s):
    return ''.join(guilloche(cx, cy, s * (0.55 + .09 * j), s * .16, 18 + 2 * j) for j in range(5))


def note_svg(pid='nt', promise=True, serial='MM 1971 000100'):
    border = ''.join(
        f'<rect x="{30+i*7}" y="{30+i*7}" width="{1440-2*(30+i*7)}" height="{640-2*(30+i*7)}" rx="{26-i*2}" fill="none" '
        f'stroke="{INK2}" stroke-width="{2.4 if i in (0, 4) else 1}" opacity=".7"/>' for i in range(5))
    waves = ''
    for base in (112, 512):
        for j in range(4):
            y = base + j * 6
            seg = ' '.join(f'Q{80+x+15},{y+(8 if (x//30)%2 else -8)} {80+x+30},{y}' for x in range(0, 1260, 30))
            waves += f'<path d="M80,{y} {seg}" fill="none" stroke="{INK2}" stroke-width=".9" opacity=".35"/>'
    corners = ''.join(
        f'<text x="{x}" y="{y}" font-family="Inter" font-weight="900" font-size="104" fill="{INK}" text-anchor="{a}">100</text>'
        for x, y, a in ((112, 176, 'start'), (1328, 176, 'end'), (112, 588, 'start'), (1328, 588, 'end')))
    promise_txt = (f'<text id="{pid}-promise" x="720" y="590" font-family="Inter" font-weight="800" font-size="22" '
                   f'letter-spacing="3" fill="{INK}" text-anchor="middle">I PROMISE TO PAY THE BEARER ON DEMAND</text>') if promise else ''
    return f'''<defs>
<linearGradient id="{pid}-paper" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ECEFDD"/><stop offset=".55" stop-color="#D9E0C7"/><stop offset="1" stop-color="#C5CFB0"/></linearGradient>
<filter id="{pid}-fib"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="11"/><feColorMatrix values="0 0 0 0 .18  0 0 0 0 .29  0 0 0 0 .22  0 0 0 .10 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>
</defs>
<rect x="0" y="0" width="1440" height="640" rx="30" fill="url(#{pid}-paper)"/>
<rect x="0" y="0" width="1440" height="640" rx="30" fill="#000" filter="url(#{pid}-fib)"/>
{border}{waves}
<g>{rose(250, 330, 170)}{rose(1190, 330, 170)}</g>
<g>{''.join(guilloche(720, 318, 250 + 8 * j, 22, 40, col=INK, op=.32) for j in range(3))}</g>
<ellipse cx="720" cy="318" rx="190" ry="222" fill="{PAPER}" stroke="{INK}" stroke-width="5"/>
<ellipse cx="720" cy="318" rx="176" ry="208" fill="none" stroke="{INK}" stroke-width="1.5" opacity=".6"/>
{corners}
<text x="720" y="78" font-family="Inter" font-weight="800" font-size="26" letter-spacing="10" fill="{INK}" text-anchor="middle">ONE HUNDRED</text>
{promise_txt}'''
