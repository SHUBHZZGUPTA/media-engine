# s031 thumbnails rebuilt on the money-Shorts thumbnail study (outputs/viral/mms-thumb-study-1, 8 Nov 2026):
# one subject filling the frame, 1-3 words led by a number, text centred in the middle third, bright natural colour,
# no logo, no circles/arrows. Vertical 1080x1920 only.
import os, asyncio
from playwright.async_api import async_playwright
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(H, '../../../..'))
B = os.path.join(H, '../art/baked'); F = f'file://{R}/money-mirage/mm3/library/fonts/'
W, Hh = 1080, 1920
img = lambda n, w, l, t: f'<img class="bg" src="file://{os.path.realpath(os.path.join(B, n + "__film.jpg"))}" style="width:{w}px;left:{l}px;top:{t}px">'
OPTS = {
 'R1': (img('coin_case', 2190, -533, -285), '<div class="w" style="top:1130px">WORTH</div><div class="n" style="top:1270px">$13M</div>'),
 'R1q': (img('coin_case', 2190, -533, -285), '<div class="w" style="top:1130px">WORTH</div><div class="n" style="top:1270px">$13M<b>?</b></div>'),
 'R4': (img('coin_case', 2190, -533, -285), '<div class="w" style="top:1010px;font-size:170px">$1M COIN</div><div class="w" style="top:1210px;font-size:130px">WORTH</div><div class="n" style="top:1360px;font-size:270px">$13M<b>?</b></div>'),
 'R5': (img('coin_case', 2190, -533, -285), '<div class="n" style="top:1190px;font-size:148px"><span style="color:#F7F1E3">$1M</span> → $13M<b>?</b></div>'),
 'R2': (img('coin_case', 2190, -533, -285), '<div class="n" style="top:1110px;font-size:230px;color:#F7F1E3">$1M<b>?</b></div><div class="n" style="top:1330px;font-size:200px">NO. $13M</div>'),
 'R3': (img('wheelbarrow', 1700, -560, -230), '<div class="n" style="top:1120px">100 KG</div><div class="w" style="top:1420px">OF GOLD</div>'),
}
CSS = f'''@font-face{{font-family:Inter;font-weight:900;src:url({F}inter900.woff2)}}
body{{margin:0}}#r{{position:relative;width:{W}px;height:{Hh}px;overflow:hidden;background:#05080F}}
.bg{{position:absolute;filter:contrast(1.1) saturate(1.6) brightness(1.3)}}
.w,.n{{position:absolute;left:0;width:{W}px;text-align:center;font-family:Inter,sans-serif;font-weight:900;line-height:1;paint-order:stroke fill;white-space:nowrap}}
.w{{font-size:150px;color:#FFFFFF;-webkit-text-stroke:18px #000}}
.n{{font-size:290px;color:#FFD23A;-webkit-text-stroke:24px #000;text-shadow:0 14px 0 rgba(0,0,0,.55)}}
.n b{{color:#FF2D2D}}'''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get('HYPERFRAMES_BROWSER_PATH'))
        for k, (bg, body) in OPTS.items():
            f = os.path.join(H, 'options', f'{k}.html')
            open(f, 'w').write(f'<!doctype html><html><head><meta charset="UTF-8"><style>{CSS}</style></head><body><div id="r">{bg}{body}</div></body></html>')
            pg = await b.new_page(viewport={'width': W, 'height': Hh}); await pg.goto('file://' + f); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
            await pg.screenshot(path=f.replace('.html', '.png')); await pg.close()
        await b.close()
asyncio.run(main())
from PIL import Image, ImageDraw
ims = []
for k in OPTS:
    p = os.path.join(H, 'options', f'{k}.png'); im = Image.open(p).convert('RGB'); im.save(p.replace('.png', '.jpg'), quality=90); ims.append((k, im))
    os.remove(p); os.remove(p.replace('.png', '.html'))
S = Image.new('RGB', (len(ims) * 370 + 10, 680), '#222'); d = ImageDraw.Draw(S)
for i, (k, im) in enumerate(ims): S.paste(im.resize((360, 640)), (10 + i * 370, 30)); d.text((14 + i * 370, 8), k, fill='white')
S.save(os.path.join(H, 'options', 'research_sheet.jpg'), quality=88)
print('ok')
