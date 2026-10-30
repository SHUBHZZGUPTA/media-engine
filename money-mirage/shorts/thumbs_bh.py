# Money Mirage Short vertical thumbnail in the BHUGOL Shorts style (Shubham's reference: BhuGol Shorts 4-6, 30 Oct 2026).
# Full-frame vivid picture; a full-statement headline top-left in Big Shoulders Display 900 (white, black stroke) with the key
# phrase in a yellow box; red hand-drawn circle on the subject + a red curved arrow from the headline; small in-picture tags;
# emoji stickers; round logo top-left. 1080x1920, also burned as frame 0. Colour-popping (saturation/brightness boosted).
# Usage (from the Short folder): python3 ../thumbs_bh.py   -> reads thumbs/thumb.json
import os, json, asyncio
from playwright.async_api import async_playwright
HERE = os.getcwd(); R = os.path.abspath(os.path.join(HERE, '../../..'))
C = json.load(open(os.path.join(HERE, 'thumbs/thumb.json')))
PLATE = f'file://{R}/money-mirage/ep01v3/src/{C["plate"]}.jpg'; LOGO = f'file://{R}/money-mirage/logo/MoneyMirage_channel_icon_800.png'
F = f'file://{R}/money-mirage/mm3/library/fonts/'
W, H = 1080, 1920; Z = C.get('zoom', 1.0); PW, PH = int(1280 * Z), int(H * Z)
left, top = int((PW - W) * C.get('fx', .5)), int((PH - H) * C.get('fy', .5))
px = lambda x, y: (int(PW * x - left), int(PH * y - top))
cx, cy = px(*C['circle'][:2]); rx, ry = C['circle'][2:]
G1, G2 = C.get('glow', ['#FF2D55', '#1E7BFF'])
lines = ''.join(f'<div class="hl">{l}</div>' for l in C['lines'])
box = f'<div class="bx">{C["box"]}</div>'
ax0, ay0 = C.get('arrow_from', [760, 640]); ax1, ay1 = cx + C.get('arrow_dx', 40), cy - ry - 30
arrow = (f'<path d="M{ax0},{ay0} Q{ax0 + 120},{(ay0 + ay1) // 2} {ax1},{ay1}" fill="none" stroke="#FF1A1A" stroke-width="16" stroke-linecap="round"/>'
         f'<path d="M{ax1 - 42},{ay1 - 40} L{ax1},{ay1} L{ax1 + 34},{ay1 - 52}" fill="none" stroke="#FF1A1A" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>') if C.get('arrow', True) else ''
circ = (f'<g fill="none" stroke="#FF1A1A" stroke-linecap="round" style="filter:drop-shadow(0 0 10px rgba(255,30,30,.9))">'
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" stroke-width="18" transform="rotate(-8 {cx} {cy})" stroke-dasharray="{int(6.2*max(rx,ry))} 50"/>'
        f'<ellipse cx="{cx+6}" cy="{cy-4}" rx="{rx*1.05}" ry="{ry*.96}" stroke-width="10" transform="rotate(5 {cx} {cy})" opacity=".85" stroke-dasharray="{int(4.6*max(rx,ry))} 500"/></g>')
def tag(t):
    x, y = t['at']
    if t.get('kind') == 'num':   # big yellow number with a small caption under it (like "47% OF THE LAND")
        return f'<div class="tn" style="left:{x}px;top:{y}px">{t["text"]}<small>{t.get("sub", "")}</small></div>'
    return f'<div class="tg" style="left:{x}px;top:{y}px;transform:rotate({t.get("rot", -4)}deg)">{t["text"]}</div>'
tags = ''.join(tag(t) for t in C.get('tags', []))
emo = ''.join(f'<div class="em" style="left:{x}px;top:{y}px;font-size:{s}px">{e}</div>' for e, x, y, s in C.get('emoji', []))
html = f'''<!doctype html><html><head><meta charset="UTF-8"><style>
@font-face{{font-family:BSD;font-weight:900;src:url({F}bsd900.woff2)}}@font-face{{font-family:Emo;src:url({F}emoji.ttf)}}
body{{margin:0}}#r{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:#07101E}}
.bg{{position:absolute;left:-{left}px;top:-{top}px;width:{PW}px;height:{PH}px;filter:contrast(1.2) saturate(1.9) brightness(1.35)}}
.gl{{position:absolute;inset:0;mix-blend-mode:screen;background:radial-gradient(circle 520px at {cx-260}px {cy-60}px,{G1}88,transparent 70%),radial-gradient(circle 560px at {cx+300}px {cy+160}px,{G2}88,transparent 70%)}}
.sh{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,8,18,.85) 0%,rgba(4,8,18,.55) 22%,rgba(4,8,18,0) 38%)}}
.head{{position:absolute;left:40px;top:{C.get('head_top', 250)}px;font-family:BSD;font-weight:900;line-height:.92;text-transform:uppercase}}
.hl{{font-size:{C.get('hsize', 150)}px;color:#fff;paint-order:stroke fill;-webkit-text-stroke:16px #000;filter:drop-shadow(0 8px 8px rgba(0,0,0,.6));white-space:nowrap}}
.bx{{display:inline-block;margin-top:14px;font-size:{C.get('bsize', 150)}px;color:#0A0A0A;background:#FFE01A;padding:6px 22px 0;border:8px solid #000;box-shadow:10px 12px 0 #000;transform:rotate(-2deg);white-space:nowrap}}
.tg{{position:absolute;font-family:BSD;font-weight:900;font-size:64px;color:#E8102E;background:#fff;padding:6px 18px 2px;border:6px solid #E8102E;border-radius:10px;box-shadow:0 8px 16px rgba(0,0,0,.5);white-space:nowrap}}
.tn{{position:absolute;font-family:BSD;font-weight:900;font-size:120px;line-height:.9;color:#FFE01A;paint-order:stroke fill;-webkit-text-stroke:12px #000;text-align:center}}
.tn small{{display:block;font-size:34px;color:#fff;-webkit-text-stroke:6px #000;letter-spacing:1px}}
.em{{position:absolute;font-family:Emo;line-height:1;filter:drop-shadow(0 8px 10px rgba(0,0,0,.6))}}
.lg{{position:absolute;left:34px;top:30px;width:190px;height:190px;border-radius:50%;border:7px solid #fff;box-shadow:0 0 0 5px #FFE01A,0 10px 24px rgba(0,0,0,.6)}}svg{{position:absolute;left:0;top:0;overflow:visible}}</style></head><body><div id="r">
<img class="bg" src="{PLATE}"><div class="gl"></div><div class="sh"></div>
<svg width="{W}" height="{H}">{circ}{arrow}</svg>{tags}{emo}
<div class="head">{lines}{box}</div><img class="lg" src="{LOGO}"></div></body></html>'''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get('HYPERFRAMES_BROWSER_PATH'))
        f = os.path.join(HERE, 'thumbs/thumb_v.html'); open(f, 'w').write(html)
        pg = await b.new_page(viewport={'width': W, 'height': H}); await pg.goto('file://' + f); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(500)
        await pg.screenshot(path=os.path.join(HERE, 'thumbs/thumb_v.png')); await b.close()
asyncio.run(main())
from PIL import Image
im = Image.open(os.path.join(HERE, 'thumbs/thumb_v.png')).convert('RGB'); out = os.path.join(HERE, f'thumbs/MoneyMirage_{C["id"]}_thumb_v.jpg'); im.save(out, quality=93)
im.resize((140, int(140 * im.height / im.width))).save(os.path.join(HERE, 'thumbs/feed_test_en.jpg')); print(out)
