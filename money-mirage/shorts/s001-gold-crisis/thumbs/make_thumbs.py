# Money Mirage Short thumbnails: vertical 1080x1920 (also frame 0) + 16:9 1280x720, EN + HI. Hero plate + 1-3 words + a number, red hand-drawn circle, logo top-left.
import os, asyncio
from playwright.async_api import async_playwright
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(H, '../../../..'))
PLATE = f'file://{R}/money-mirage/episodes/ep01/art/baked/gold_window__film.jpg'; LOGO = f'file://{R}/money-mirage/logo/MoneyMirage_logo_transparent.png'
F = f'file://{R}/money-mirage/mm3/library/fonts/'
WORDS = {'en': 'SAFE HAVEN?', 'hi': 'सोना सुरक्षित?'}
def circle(cx, cy, rx, ry):   # two overlapping hand-drawn ellipses with a glow
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#FF2D2D" stroke-width="16" stroke-linecap="round" transform="rotate(-6 {cx} {cy})" filter="url(#gl)" stroke-dasharray="{int(6.1*max(rx,ry))} 60"/>'
            f'<ellipse cx="{cx+8}" cy="{cy-6}" rx="{rx*1.04}" ry="{ry*.97}" fill="none" stroke="#FF2D2D" stroke-width="10" stroke-linecap="round" transform="rotate(4 {cx} {cy})" opacity=".85" stroke-dasharray="{int(4.8*max(rx,ry))} 400"/>')
def page(lang, W, Hh):
    v = Hh > W
    img = (f'<img class="bg" src="{PLATE}" style="width:auto;height:{Hh}px;left:-1235px;top:0">' if v else
           f'<img class="bg" src="{PLATE}" style="width:1920px;height:1080px;left:-60px;top:-180px">')
    cx, cy, rx, ry = (540, 925, 270, 205) if v else (960, 338, 170, 135)
    word_css = f'left:0;width:{W}px;text-align:center;top:300px;font-size:{150 if lang=="en" else 140}px' if v else f'left:48px;width:700px;top:170px;font-size:{88 if lang=="en" else 86}px;white-space:nowrap'
    num_css = f'left:0;width:{W}px;text-align:center;top:480px;font-size:215px' if v else 'left:40px;width:600px;top:330px;font-size:150px'
    return f'''<!doctype html><html><head><meta charset="UTF-8"><style>
@font-face{{font-family:Inter;font-weight:900;src:url({F}inter900.woff2)}}@font-face{{font-family:Mukta;font-weight:800;src:url({F}mukta800.woff2)}}
body{{margin:0}}#r{{position:relative;width:{W}px;height:{Hh}px;overflow:hidden;background:#05080F}}
.bg{{position:absolute;filter:contrast(1.15) saturate(1.35) brightness(1.02)}}
.sh{{position:absolute;inset:0;background:{'linear-gradient(180deg,rgba(5,8,15,.92) 0%,rgba(5,8,15,.6) 30%,rgba(5,8,15,0) 45%,rgba(5,8,15,0) 75%,rgba(5,8,15,.5) 100%)' if v else 'linear-gradient(90deg,rgba(5,8,15,.95) 0%,rgba(5,8,15,.8) 40%,rgba(5,8,15,0) 62%)'}}}
.w,.n{{position:absolute;font-family:Inter,Mukta,sans-serif;font-weight:900;line-height:1;paint-order:stroke fill;letter-spacing:0}}
.w{{color:#F7F1E3;-webkit-text-stroke:{16 if v else 11}px #0A0F1A;transform:rotate(-2.5deg)}}
.n{{color:#FFC43A;-webkit-text-stroke:{20 if v else 14}px #0A0F1A;text-shadow:0 0 50px rgba(255,180,40,.55),0 12px 0 rgba(0,0,0,.6)}}
.n b{{color:#FF2D2D;font-size:.7em;vertical-align:.12em;margin-left:.08em}}
.lg{{position:absolute;left:{36 if v else 26}px;top:{40 if v else 24}px;width:{230 if v else 150}px}}
svg{{position:absolute;left:0;top:0}}</style></head><body><div id="r">{img}<div class="sh"></div>
<svg width="{W}" height="{Hh}"><defs><filter id="gl"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>{circle(cx, cy, rx, ry)}</svg>
<div class="w" style="{word_css}">{WORDS[lang]}</div><div class="n" style="{num_css}">$4,000<b>↓</b></div>
<img class="lg" src="{LOGO}"></div></body></html>'''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get('HYPERFRAMES_BROWSER_PATH'))
        for lang in ('en', 'hi'):
            for W, Hh, tag in ((1080, 1920, 'v'), (1280, 720, 'h')):
                f = os.path.join(H, f'thumb_{lang}_{tag}.html'); open(f, 'w').write(page(lang, W, Hh))
                pg = await b.new_page(viewport={'width': W, 'height': Hh}); await pg.goto('file://' + f); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
                out = os.path.join(H, f'MoneyMirage_s001_thumb_{lang}_{tag}.png'); await pg.screenshot(path=out); await pg.close()
        await b.close()
asyncio.run(main())
from PIL import Image
for lang in ('en', 'hi'):
    for tag in ('v', 'h'):
        im = Image.open(os.path.join(H, f'MoneyMirage_s001_thumb_{lang}_{tag}.png')).convert('RGB'); im.save(os.path.join(H, f'MoneyMirage_s001_thumb_{lang}_{tag}.jpg'), quality=92)
    # 140 px feed test
    a = Image.open(os.path.join(H, f'MoneyMirage_s001_thumb_{lang}_v.jpg')); b = Image.open(os.path.join(H, f'MoneyMirage_s001_thumb_{lang}_h.jpg'))
    a = a.resize((140, int(140 * a.height / a.width))); b = b.resize((140, int(140 * b.height / b.width)))
    s = Image.new('RGB', (300, max(a.height, b.height)), '#222'); s.paste(a, (0, 0)); s.paste(b, (150, 0)); s.save(os.path.join(H, f'feed_test_{lang}.jpg'))
print('ok')
