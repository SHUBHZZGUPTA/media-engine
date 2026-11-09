# s032 thumbnails (copied from s031 make_bhstyle.py) in the BHUGOL thumbnail style (bhugol-v2/thumbnail_rules.md + thumbnail_template.html + thumb_split):
# condensed BSD 900 caps, white text with a heavy black outline for the set-up line, the key words black on a yellow
# bar (black border, hard black shadow, -3 deg), 1-2 emoji stickers, red hand-drawn circle on the payoff, small badge
# top-left; or the split recipe (two halves, white divider, one yellow-bar label each). Vertical 1080x1920 only.
import os, asyncio
from playwright.async_api import async_playwright
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(H, '../../../..'))
B = os.path.join(H, '../art/baked'); F = f'file://{R}/money-mirage/mm3/library/fonts/'
LOGO = f'file://{R}/money-mirage/logo/MoneyMirage_logo_transparent.png'
W, Hh = 1080, 1920
src = lambda n: 'file://' + os.path.realpath(os.path.join(B, n + '__film.jpg'))
img = lambda n, w, l, t, extra='': f'<img class="bg" src="{src(n)}" style="width:{w}px;left:{l}px;top:{t}px;{extra}">'
def ring(cx, cy, rx, ry):
    return (f'<svg class="sv" width="{W}" height="{Hh}"><defs><filter id="gl"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
            f'<g fill="none" stroke="#FF1F1F" stroke-linecap="round" filter="url(#gl)"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" stroke-width="16" transform="rotate(-6 {cx} {cy})"/>'
            f'<ellipse cx="{cx+7}" cy="{cy+6}" rx="{rx*.97}" ry="{ry*1.02}" stroke-width="9" opacity=".9" transform="rotate(4 {cx} {cy})"/></g></svg>')
emo = lambda e, x, y, s=150: f'<div class="emo" style="left:{x}px;top:{y}px;font-size:{s}px">{e}</div>'
SID = 's032'
OPTS = {
 'V1': (img('rs_kitchen', 1280, -100, 0), ring(924, 825, 150, 120) +
        '<div class="t" style="top:1060px;font-size:175px">FBI REFUND?</div>'
        '<div class="h" style="top:1290px;font-size:190px">$5,000</div>' + emo('🚨', 820, 1600, 150) + emo('📞', 80, 1620, 130)),
 'V2': (img('fc_phone', 1280, -100, 0), ring(693, 1017, 150, 120) +
        '<div class="t" style="top:1060px;font-size:175px">FBI REFUND?</div>'
        '<div class="h" style="top:1290px;font-size:190px">$5,000</div>' + emo('🚨', 820, 1600, 150) + emo('📞', 80, 1620, 130)),
}
CSS = f'''@font-face{{font-family:BSD;font-weight:900;src:url({F}bsd900.woff2)}}@font-face{{font-family:Emo;src:url({F}emoji.ttf)}}
body{{margin:0}}#r{{position:relative;width:{W}px;height:{Hh}px;overflow:hidden;background:#05080F}}
.bg{{position:absolute;filter:contrast(1.1) saturate(1.55) brightness(1.25)}}
.t{{position:absolute;left:0;width:{W}px;text-align:center;font-family:BSD;font-weight:900;color:#fff;line-height:1;white-space:nowrap;-webkit-text-stroke:22px #000;paint-order:stroke fill;letter-spacing:.01em;transform:rotate(-2deg)}}
.h{{position:absolute;left:50%;font-family:BSD;font-weight:900;color:#000;line-height:1;white-space:nowrap;background:#FFE81A;border:9px solid #000;padding:6px 26px 12px;box-shadow:14px 14px 0 #000,0 0 44px rgba(255,232,26,.7);transform:translateX(-50%) rotate(-3deg)}}
.lb{{position:absolute;transform:translate(-50%,-50%) rotate(-3deg);font-family:BSD;font-weight:900;font-size:96px;color:#000;background:#FFE81A;padding:4px 20px 8px;border:7px solid #000;box-shadow:10px 10px 0 #000;white-space:nowrap;line-height:1}}
.tag{{position:absolute;font-family:BSD;font-weight:900;font-size:78px;color:#FFE81A;background:#000;padding:6px 18px 10px;border:5px solid #fff;transform:rotate(4deg);white-space:nowrap;line-height:1}}
.half{{position:absolute;top:0;width:540px;height:{Hh}px;overflow:hidden}}
.div{{position:absolute;left:532px;top:0;width:16px;height:{Hh}px;background:#fff;box-shadow:0 0 30px rgba(0,0,0,.6)}}
.emo{{position:absolute;font-family:Emo;line-height:1;filter:drop-shadow(0 8px 10px rgba(0,0,0,.6))}}
.lg{{position:absolute;left:30px;top:34px;width:170px}} .sv{{position:absolute;left:0;top:0}}'''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get('HYPERFRAMES_BROWSER_PATH'))
        for k, body in OPTS.items():
            f = os.path.join(H, 'options', f'{k}.html')
            open(f, 'w').write(f'<!doctype html><html><head><meta charset="UTF-8"><style>{CSS}</style></head><body><div id="r">{body}<img class="lg" src="{LOGO}"></div></body></html>')
            pg = await b.new_page(viewport={'width': W, 'height': Hh}); await pg.goto('file://' + f); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(500)
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
S.save(os.path.join(H, 'options', 'bhstyle_sheet.jpg'), quality=88)
F2 = Image.new('RGB', (len(ims) * 150, 250), '#222')
for i, (k, im) in enumerate(ims): F2.paste(im.resize((140, 249)), (i * 150, 0))
F2.save(os.path.join(H, 'options', 'bhstyle_feed.jpg'))
print('ok')

import shutil, sys
pick = sys.argv[1] if len(sys.argv) > 1 else list(OPTS)[0]
shutil.copy(os.path.join(H, 'options', f'{pick}.jpg'), os.path.join(H, f'MoneyMirage_{SID}_thumb_en_v.jpg'))
Image.open(os.path.join(H, 'options', f'{pick}.jpg')).resize((140, 249)).save(os.path.join(H, 'feed_test_en.jpg'))
