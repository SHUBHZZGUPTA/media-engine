"""BHUGOL thumbnail recipe A: 3D satellite map + flag-coloured region + fire/glow at the payoff spot + zoom bubble
of the story's key scene + giant glowing number + 1-3 words. Chosen 21 Oct 2026 from the yt-viral thumbnail study
(top outliers = satellite map + one bold-coloured region + a big date/number; scene/photo thumbnails underperform)
while still showing the story moment (the user's ask). See ../thumbnail_rules.md.

Usage: python3 thumb_a.py <config.json>
config: {
  "art": "/path/art",                 # dir with map3d.json + ne.jpg, pa_close.jpg, pa_mask.png, hillshade.png, dem8.png
  "out": "/path/thumbs", "name": "BHUGOL_Title",
  "words": {"en": "STILL BURNING", "hi": "अब भी जल रहा"},   # <= 3 words, never repeating the title
  "number": "1962",                   # a number/date NOT already in the title
  "bubble": "/path/scene.jpg", "bubble_v": [-70, -70, 760], "bubble_w": [-34, -34, 368],   # img left, top, width inside the bubble
  "emoji": ["😱", "🔥", "🇺🇸"],
  "vcam": "-0.41,0.15,9.6,66,4", "wcam": "-0.61,0.1,8.4,62,0",  # optional camera framing (see thumb3d.html)
  "flag": "/path/flag_xx.png",        # optional: fill the region with this flag (else flat blue)
  "glow": "fire" | "water"            # optional: what glows at the payoff spot (default fire)
}
Writes <name>_FINAL_thumb_v.jpg / _16x9.jpg and <name>_HI_FINAL_thumb_v.jpg / _16x9.jpg, plus a 140 px feed test sheet.
"""
import json, os, shutil, subprocess, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = '/home/claude/bhugol-kit'
C = json.load(open(sys.argv[1])); W = os.path.join(C['out'], '_work'); os.makedirs(os.path.join(W, 'assets'), exist_ok=True)
for f in ('ne.jpg', 'pa_close.jpg', 'pa_mask.png', 'hillshade.png', 'dem8.png'): shutil.copy(os.path.join(C['art'], f), os.path.join(W, 'assets', f))
shutil.copy(C['bubble'], os.path.join(W, 'assets', 'bubble.jpg'))
if C.get('flag'): shutil.copy(C['flag'], os.path.join(W, 'assets', 'flag.png'))
FONTS = {'bsd900.woff2': 'big-shoulders-display/files/big-shoulders-display-latin-900-normal.woff2', 'muk800.woff2': 'mukta/files/mukta-devanagari-800-normal.woff2'}
for d, s in FONTS.items(): shutil.copy(os.path.join(KIT, 'node_modules/@fontsource', s), os.path.join(W, 'assets', d))
shutil.copy('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', os.path.join(W, 'assets', 'emoji.ttf')); shutil.copy(os.path.join(KIT, 'assets/bhugol_badge.png'), os.path.join(W, 'assets', 'bhugol_badge.png'))
shutil.copy(os.path.join(HERE, 'thumb3d.html'), W)
three = next(p for p in ('/home/claude/work/node_modules/three/build/three.min.js', os.path.join(HERE, 'three.min.js')) if os.path.exists(p)); shutil.copy(three, W)
open(os.path.join(W, 'map3d.js'), 'w').write('const M3=' + open(os.path.join(C['art'], 'map3d.json')).read() + ';')
q = f"&vcam={C.get('vcam', '-0.41,0.15,9.6,66,4')}&wcam={C.get('wcam', '-0.61,0.1,8.4,62,0')}&glow={C.get('glow', 'fire')}" + ('&flag=flag.png' if C.get('flag') else '')
open(os.path.join(W, 'bare.mjs'), 'w').write("""import { chromium } from '/opt/npm-tools/node_modules/playwright/index.mjs';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell', args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--allow-file-access-from-files'] });
const out = {};
for (const [m, w, h] of [['v', 1080, 1920], ['w', 1280, 720]]) { const p = await b.newPage({ viewport: { width: w, height: h } });
  await p.goto(`file://${process.cwd()}/thumb3d.html?m=${m}&bare=1&big=1""" + q + """`); await p.waitForFunction(() => document.title === 'READY', null, { timeout: 240000 }); await p.waitForTimeout(300);
  await p.screenshot({ path: `bare_${m}.png` }); out[m] = await p.evaluate(() => window.__C); await p.close(); }
console.log(JSON.stringify(out)); await b.close();
""")
P = json.loads(subprocess.run(['node', 'bare.mjs'], cwd=W, capture_output=True, text=True, check=True).stdout.strip().splitlines()[-1]); vx, vy = P['v']; wx, wy = P['w']
CSS = """@font-face{font-family:BSD;font-weight:900;src:url(assets/bsd900.woff2)}@font-face{font-family:Muk;font-weight:800;src:url(assets/muk800.woff2)}@font-face{font-family:Emo;src:url(assets/emoji.ttf)}
body{margin:0} .f{position:relative;overflow:hidden;background:#07101E;margin-bottom:20px}
.t{position:absolute;font-family:BSD,Muk;font-weight:900;line-height:1;white-space:nowrap} .w{color:#fff;paint-order:stroke fill;-webkit-text-stroke:18px #000;filter:drop-shadow(0 8px 10px rgba(0,0,0,.6))}
.emo{position:absolute;font-family:Emo;line-height:1;filter:drop-shadow(0 8px 10px rgba(0,0,0,.6))} .badge{position:absolute;filter:drop-shadow(0 4px 8px rgba(0,0,0,.6))}
.num{position:absolute;font-family:BSD;font-weight:900;line-height:1;color:#FFD23A;-webkit-text-stroke:14px #2A0800;paint-order:stroke fill;text-shadow:0 0 30px rgba(255,90,0,.95),0 0 60px rgba(255,60,0,.8)}
.bub{position:absolute;border-radius:50%;overflow:hidden;border:12px solid #fff;box-shadow:0 0 0 8px #FF1A1A,0 18px 40px rgba(0,0,0,.6)} .bub img{position:absolute}"""
def circ(x, y, rx, ry, sw=18): return f'<g fill="none" stroke="#FF1A1A" stroke-width="{sw}" stroke-linecap="round" style="filter:drop-shadow(0 0 10px rgba(255,30,30,.9))"><ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" transform="rotate(-8 {x} {y})"/><ellipse cx="{x+5}" cy="{y+4}" rx="{rx-9}" ry="{ry-8}" transform="rotate(5 {x} {y})"/></g>'
E = C.get('emoji', ['😱', '🔥', '🌍']); bv, bw = C.get('bubble_v', [-70, -70, 760]), C.get('bubble_w', [-34, -34, 368]); N = C['number']
for L in ('en', 'hi'):
    w1 = C['words'][L]
    v = f'''<div class="f" id="v" style="width:1080px;height:1920px"><img src="bare_v.png" style="position:absolute;left:0;top:0;width:1080px;height:1920px">
 <div style="position:absolute;inset:0;background:linear-gradient(rgba(0,0,0,.55),rgba(0,0,0,0) 26%)"></div>
 <svg width="1080" height="1920" style="position:absolute;left:0;top:0;overflow:visible"><path d="M{vx},{vy} L540,1300" stroke="#fff" stroke-width="10" stroke-dasharray="4 18" stroke-linecap="round"/>{circ(vx, vy, 120, 100)}</svg>
 <div class="bub" style="left:250px;top:1230px;width:580px;height:580px"><img src="assets/bubble.jpg" style="left:{bv[0]}px;top:{bv[1]}px;width:{bv[2]}px"></div>
 <img class="badge" src="assets/bhugol_badge.png" style="left:36px;top:36px;width:140px"><div class="t w" style="left:0;width:1080px;text-align:center;top:120px;font-size:{130 if L == 'en' else 120}px">{w1}</div>
 <div class="num" style="left:0;width:1080px;text-align:center;top:300px;font-size:300px">{N}</div>
 <div class="emo" style="left:60px;top:1050px;font-size:150px">{E[0]}</div><div class="emo" style="left:860px;top:1080px;font-size:150px">{E[1]}</div><div class="emo" style="left:860px;top:1700px;font-size:140px">{E[2]}</div></div>'''
    w = f'''<div class="f" id="w" style="width:1280px;height:720px"><img src="bare_w.png" style="position:absolute;left:0;top:0;width:1280px;height:720px">
 <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.7),rgba(0,0,0,0) 46%)"></div>
 <svg width="1280" height="720" style="position:absolute;left:0;top:0;overflow:visible"><path d="M{wx},{wy} L1000,520" stroke="#fff" stroke-width="8" stroke-dasharray="3 14" stroke-linecap="round"/>{circ(wx, wy, 90, 72, 13)}</svg>
 <div class="bub" style="left:860px;top:420px;width:280px;height:280px;border-width:8px"><img src="assets/bubble.jpg" style="left:{bw[0]}px;top:{bw[1]}px;width:{bw[2]}px"></div>
 <img class="badge" src="assets/bhugol_badge.png" style="left:22px;top:22px;width:96px"><div class="t w" style="left:40px;top:120px;font-size:{96 if L == 'en' else 90}px;-webkit-text-stroke:13px #000">{w1}</div>
 <div class="num" style="left:40px;top:260px;font-size:230px;-webkit-text-stroke:11px #2A0800">{N}</div>
 <div class="emo" style="left:560px;top:40px;font-size:96px">{E[0]}</div><div class="emo" style="left:1150px;top:300px;font-size:90px">{E[2]}</div></div>'''
    open(os.path.join(W, f'a_{L}.html'), 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{v}{w}</body></html>')
open(os.path.join(W, 'shot.mjs'), 'w').write("""import { chromium } from '/opt/npm-tools/node_modules/playwright/index.mjs';
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 2700 } });
for (const L of ['en', 'hi']) { await p.goto(`file://${process.cwd()}/a_${L}.html`); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(600);
  await (await p.$('#v')).screenshot({ path: `v_${L}.png` }); await (await p.$('#w')).screenshot({ path: `w_${L}.png` }); }
await b.close();
""")
subprocess.run(['node', 'shot.mjs'], cwd=W, check=True)
for L, suf in (('en', ''), ('hi', '_HI')):
    Image.open(os.path.join(W, f'v_{L}.png')).convert('RGB').save(os.path.join(C['out'], f"{C['name']}{suf}_FINAL_thumb_v.jpg"), quality=95)
    Image.open(os.path.join(W, f'w_{L}.png')).convert('RGB').save(os.path.join(C['out'], f"{C['name']}{suf}_FINAL_thumb_16x9.jpg"), quality=95)
a = Image.open(os.path.join(W, 'v_en.png')).convert('RGB'); b = Image.open(os.path.join(W, 'w_en.png')).convert('RGB')
s = Image.new('RGB', (1080 + 1280 + 20, 1920), (24, 24, 24)); s.paste(a, (0, 0)); s.paste(b, (1100, 0)); s.paste(a.resize((140, 249), Image.LANCZOS), (1100, 800)); s.paste(b.resize((246, 138), Image.LANCZOS), (1300, 800))
s.resize((s.width // 2, s.height // 2), Image.LANCZOS).save(os.path.join(C['out'], 'feed_test.jpg'), quality=88)
print('thumbnails ->', C['out'])
