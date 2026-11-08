# s031 thumbnail options: vertical 1080x1920 only, colour-popping. Renders opt_*.jpg + a contact sheet.
import os, asyncio
from playwright.async_api import async_playwright
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(H, '../../../..'))
B = os.path.join(H, '../art/baked'); F = f'file://{R}/money-mirage/mm3/library/fonts/'
LOGO = f'file://{R}/money-mirage/logo/MoneyMirage_logo_transparent.png'
W, Hh = 1080, 1920
def plate(name, x):   # 16:9 plate scaled to 1920 tall, subject at plate x centred
    pw = Hh * 16 / 9; return f'<img class="bg" src="file://{os.path.realpath(os.path.join(B, name + "__film.jpg"))}" style="height:{Hh}px;width:{pw:.0f}px;left:{540 - x * pw:.0f}px;top:0">'
def ring(cx, cy, rx, ry, col='#FF2D2D'):
    return (f'<svg width="{W}" height="{Hh}"><defs><filter id="gl"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{col}" stroke-width="16" stroke-linecap="round" transform="rotate(-6 {cx} {cy})" filter="url(#gl)" stroke-dasharray="{int(6.1*max(rx,ry))} 60"/>'
            f'<ellipse cx="{cx+8}" cy="{cy-6}" rx="{rx*1.04}" ry="{ry*.97}" fill="none" stroke="{col}" stroke-width="10" stroke-linecap="round" transform="rotate(4 {cx} {cy})" opacity=".85" stroke-dasharray="{int(4.8*max(rx,ry))} 400"/></svg>')
OPTS = {
 'A': dict(p=plate('p_mirage', .55), body='<div class="dk"></div><div class="w" style="top:1040px">STAMPED <s>$1M</s></div><div class="n" style="top:1220px;font-size:260px">$13M<b>?</b></div>',
           ring=(470, 365, 300, 290), note='mirage sun-coin; $1M struck out, $13M?'),
 'B': dict(p=plate('gold_cube', .73), body='<div class="w" style="top:270px">100 KG GOLD</div><div class="n" style="top:430px;font-size:250px">$13M<b>?</b></div>',
           ring=None, note='giant gold block; 100 KG GOLD $13M?'),
 'C': dict(p=plate('coin_spin', .54), body='<div class="w" style="top:300px;font-size:128px">REALLY WORTH</div><div class="n" style="top:470px;font-size:215px">$13M<b>?</b></div>',
           ring=(545, 975, 235, 265), note='current design, brightened'),
 'D': dict(p=plate('vault_full', .4), body='<div class="w" style="top:260px;font-size:120px">SAYS <s>$1M</s></div><div class="w" style="top:420px;font-size:120px">WORTH</div><div class="n" style="top:560px;font-size:250px">$13M<b>?</b></div>',
           ring=None, note='gold vault; SAYS $1M / WORTH $13M?'),
 'E': dict(p=plate('coin_spin', .54), body='<div class="n" style="top:250px;font-size:140px;color:#F7F1E3">$1,000,000</div><div class="w" style="top:440px;font-size:130px;color:#FF3B30">COIN?</div><div class="n" style="top:1380px;font-size:200px">LIES<b>!</b></div>',
           ring=(545, 975, 235, 265), note='$1,000,000 COIN? ... LIES!'),
}
CSS = f'''@font-face{{font-family:Inter;font-weight:900;src:url({F}inter900.woff2)}}
body{{margin:0}}#r{{position:relative;width:{W}px;height:{Hh}px;overflow:hidden;background:#05080F}}
.bg{{position:absolute;filter:contrast(1.12) saturate(1.55) brightness(1.18)}}
.sh{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,8,15,.7) 0%,rgba(5,8,15,.35) 28%,rgba(5,8,15,0) 42%)}}
.w,.n{{position:absolute;left:0;width:{W}px;text-align:center;font-family:Inter,sans-serif;font-weight:900;line-height:1;paint-order:stroke fill}}
.w{{font-size:140px;color:#F7F1E3;-webkit-text-stroke:16px #0A0F1A;transform:rotate(-2.5deg)}}
.n{{color:#FFC43A;-webkit-text-stroke:20px #0A0F1A;text-shadow:0 0 60px rgba(255,180,40,.7),0 12px 0 rgba(0,0,0,.6)}}
.n b{{color:#FF2D2D;font-size:.7em;vertical-align:.12em;margin-left:.06em}}
.s,s{{text-decoration:line-through;text-decoration-color:#FF2D2D;text-decoration-thickness:22px}} .s{{color:#F7F1E3}}
.dk{{position:absolute;left:0;right:0;top:960px;height:700px;background:radial-gradient(ellipse at center,rgba(5,8,15,.6) 0%,rgba(5,8,15,0) 70%)}}
.lg{{position:absolute;left:36px;top:40px;width:230px}} svg{{position:absolute;left:0;top:0}}'''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get('HYPERFRAMES_BROWSER_PATH'))
        for k, o in OPTS.items():
            html = f'<!doctype html><html><head><meta charset="UTF-8"><style>{CSS}</style></head><body><div id="r">{o["p"]}<div class="sh"></div>{ring(*o["ring"]) if o["ring"] else ""}{o["body"]}<img class="lg" src="{LOGO}"></div></body></html>'
            f = os.path.join(H, 'options', f'opt_{k}.html'); open(f, 'w').write(html)
            pg = await b.new_page(viewport={'width': W, 'height': Hh}); await pg.goto('file://' + f); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
            await pg.screenshot(path=f.replace('.html', '.png')); await pg.close()
        await b.close()
asyncio.run(main())
from PIL import Image, ImageDraw
ims = []
for k in OPTS:
    im = Image.open(os.path.join(H, 'options', f'opt_{k}.png')).convert('RGB'); im.save(os.path.join(H, 'options', f'opt_{k}.jpg'), quality=90); ims.append((k, im))
S = Image.new('RGB', (len(ims) * 370 + 10, 680), '#222'); d = ImageDraw.Draw(S)
for i, (k, im) in enumerate(ims):
    t = im.resize((360, 640)); S.paste(t, (10 + i * 370, 30)); d.text((14 + i * 370, 8), k, fill='white')
S.save(os.path.join(H, 'options', 'options_sheet.jpg'), quality=88)
# 140 px feed test row
F2 = Image.new('RGB', (len(ims) * 150, 250), '#222')
for i, (k, im) in enumerate(ims): F2.paste(im.resize((140, 249)), (i * 150, 0))
F2.save(os.path.join(H, 'options', 'feed_test.jpg'))
print('ok')
