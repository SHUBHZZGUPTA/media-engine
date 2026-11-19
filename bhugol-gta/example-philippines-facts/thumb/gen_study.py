import sys; sys.argv=['x']
exec(open('/home/claude/ph/thumb/gen_thumbs.py').read().split("# 1 ·")[0])
CSS2 = CSS + ".lab{font-size:40px;padding:6px 14px 8px}\n"
def page2(name, base, body):
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS2}</style></head><body><div class="bg" style="background-image:url({base})"></div>{body}</body></html>'
    open(D + f's_{name}.html', 'w').write(html)
def TAGS(P): return callouts(P, [
    ('pina', 'COOLED EARTH', 330, 175, 24),
    ('taal', 'IMPOSSIBLE!', 330, 330, 24),
    ('bohol', 'CHOCOLATE?!', 420, 520, 28),
    ]) + trench(P)
def trench(P):
    x, y = P(127.25, 9.7); r = 30
    ring = f'<div class="ring" style="left:{x - r:.0f}px;top:{y - r * .8:.0f}px;width:{2 * r - 14:.0f}px;height:{1.6 * r - 14:.0f}px"></div>'
    lab = '<div class="lab" style="left:1010px;top:250px">10 KM DEEP</div>'
    svg = '<svg style="position:absolute;inset:0" width="1280" height="720">' + arrow(1150, 312, x + 2, y - r * .8 - 6, curve=-.2) + '</svg>'
    return svg + ring + lab
# A: Coggnize / Unmapped formula: red country, black bar, yellow rings + short tags
PA = proj('base_red.jpg'); page2('A_red_tags', 'base_red.jpg', bar('PHILIPPINES IS', 'INSANE') + TAGS(PA))
# B: Navigating Geography formula: lit country, white outline glow, few markers
PB = proj('base_lit.jpg'); page2('B_lit', 'base_lit.jpg', bar('PHILIPPINES IS', 'INSANE') + TAGS(PB))
# C: Borderline Wonders formula: flag-filled country + same tags
PC = proj('base_flag.jpg'); page2('C_flag_tags', 'base_flag.jpg', bar('PHILIPPINES IS', 'INSANE') + TAGS(PC))
print('ok')
