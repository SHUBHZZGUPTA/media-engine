# Money Mirage Short vertical thumbnail (1080x1920, also burned as frame 0), English. Shubham: Shorts get vertical thumbnails only.
# Usage (from the Short folder): python3 ../thumbs_v.py  -> reads thumbs/thumb.json {id, plate, fx, words, num, arrow, circle:[cx,cy,rx,ry] in plate 0..1 / px, pos:"top"|"bottom"}
import os, json, asyncio
from playwright.async_api import async_playwright
HERE = os.getcwd(); R = os.path.abspath(os.path.join(HERE, '../../..'))
cfg = json.load(open(os.path.join(HERE, 'thumbs/thumb.json')))
PLATE = f'file://{R}/money-mirage/ep01v3/src/{cfg["plate"]}.jpg'; LOGO = f'file://{R}/money-mirage/logo/MoneyMirage_logo_transparent.png'
F = f'file://{R}/money-mirage/mm3/library/fonts/'
W, Hh = 1080, 1920; Z = cfg.get('zoom', 1.0); PW = int(1280 * Z); PH = int(Hh * Z); left = int((PW - W) * cfg.get('fx', .5)); top = int((PH - Hh) * cfg.get('fy', .5))
G1, G2 = cfg.get('glow', ['#FF2D55', '#1E7BFF'])
def circle(cx, cy, rx, ry):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#FF1E3C" stroke-width="20" stroke-linecap="round" transform="rotate(-6 {cx} {cy})" filter="url(#gl)" stroke-dasharray="{int(6.1*max(rx,ry))} 60"/>'
            f'<ellipse cx="{cx+8}" cy="{cy-6}" rx="{rx*1.04}" ry="{ry*.97}" fill="none" stroke="#FF2D2D" stroke-width="10" stroke-linecap="round" transform="rotate(4 {cx} {cy})" opacity=".85" stroke-dasharray="{int(4.8*max(rx,ry))} 400"/>')
cx, cy, rx, ry = cfg['circle']; cx = int(PW * cx - left); cy = int(PH * cy - top)
bot = cfg.get('pos', 'bottom') == 'bottom'
wt, nt = (1270, 1440) if bot else (300, 480)
grad = (f'radial-gradient(ellipse 70% 40% at {cx}px {cy}px, transparent 55%, rgba(0,0,0,0) 100%), linear-gradient(180deg,rgba(0,0,0,0) 0%,rgba(0,0,0,0) 58%,{G2}cc 74%,{G2} 100%)' if bot else
        'linear-gradient(180deg,rgba(5,8,15,.92) 0%,rgba(5,8,15,.6) 30%,rgba(5,8,15,0) 45%,rgba(5,8,15,0) 75%,rgba(5,8,15,.5) 100%)')
arrow = {'down': '<b>↓</b>', 'up': '<b>↑</b>'}.get(cfg.get('arrow'), '')
html = f'''<!doctype html><html><head><meta charset="UTF-8"><style>
@font-face{{font-family:Inter;font-weight:900;src:url({F}inter900.woff2)}}
body{{margin:0}}#r{{position:relative;width:{W}px;height:{Hh}px;overflow:hidden;background:#05080F}}
.bg{{position:absolute;left:-{left}px;top:-{top}px;width:{PW}px;height:{PH}px;filter:contrast(1.22) saturate(1.95) brightness(1.38)}}
.gl{{position:absolute;inset:0;mix-blend-mode:screen;background:radial-gradient(circle 520px at {cx-260}px {cy-120}px,{G1}aa,transparent 70%),radial-gradient(circle 560px at {cx+300}px {cy+80}px,{G2}aa,transparent 70%)}}
.sh{{position:absolute;inset:0;background:{grad}}}
.w,.n{{position:absolute;left:0;width:{W}px;text-align:center;font-family:Inter,sans-serif;font-weight:900;line-height:1;paint-order:stroke fill}}
.w{{top:{wt}px;left:50%;width:auto;transform:translateX(-50%) rotate(-3deg);font-size:{cfg.get('wsize',130)}px;color:#0A0A0A;background:#FFE11A;padding:22px 40px 18px;border-radius:14px;box-shadow:0 14px 0 #0A0A0A,0 0 60px rgba(255,225,26,.6);white-space:nowrap}}
.n{{top:{nt+40}px;font-size:{cfg.get('nsize',235)}px;color:#FFFFFF;-webkit-text-stroke:22px #0A0A0A;text-shadow:0 0 70px {G1},10px 14px 0 #FF1E3C}}
.n b{{color:#FF2D2D;font-size:.7em;vertical-align:.12em;margin-left:.08em}}
.lg{{position:absolute;left:36px;top:40px;width:230px}}svg{{position:absolute;left:0;top:0}}</style></head><body><div id="r">
<img class="bg" src="{PLATE}"><div class="gl"></div><div class="sh"></div>
<svg width="{W}" height="{Hh}"><defs><filter id="gl"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>{circle(cx, cy, rx, ry)}</svg>
<div class="w">{cfg["words"]}</div><div class="n">{cfg["num"]}{arrow}</div><img class="lg" src="{LOGO}"></div></body></html>'''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get('HYPERFRAMES_BROWSER_PATH'))
        f = os.path.join(HERE, 'thumbs/thumb_v.html'); open(f, 'w').write(html)
        pg = await b.new_page(viewport={'width': W, 'height': Hh}); await pg.goto('file://' + f); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
        await pg.screenshot(path=os.path.join(HERE, 'thumbs/thumb_v.png')); await b.close()
asyncio.run(main())
from PIL import Image
im = Image.open(os.path.join(HERE, 'thumbs/thumb_v.png')).convert('RGB'); out = os.path.join(HERE, f'thumbs/MoneyMirage_{cfg["id"]}_thumb_v.jpg'); im.save(out, quality=92)
im.resize((140, int(140 * im.height / im.width))).save(os.path.join(HERE, 'thumbs/feed_test_en.jpg')); print(out)
