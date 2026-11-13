import json, sys, math
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance, ImageChops
LANG = sys.argv[1]; OUT = sys.argv[2]
G = json.load(open('../art/geo.json')); W, H = 1080, 1920
src = Image.open('/home/claude/media-engine/outputs/fetch/smog-map/haze_VIIRS_NOAA20_2026-11-12.jpg').convert('RGB')
SW, SH = src.size; cx, wdeg = 81.0, 8.0; cw = wdeg / 26 * SW; ch = SH; x0 = (cx - 68) / 26 * SW - cw / 2
base = src.crop((int(x0), 0, int(x0 + cw), ch)).resize((W, H), Image.LANCZOS)
base = ImageEnhance.Contrast(base).enhance(1.18); base = ImageEnhance.Color(base).enhance(1.35); base = ImageEnhance.Brightness(base).enhance(1.06)
P = lambda lo, la: (((lo - 68) / 26 * SW - x0) * W / cw, (34 - la) / 14 * H)
img = base.convert('RGBA')
# plain states: saturated warm fill so the trapped region reads at feed size
fill = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(fill)
for n in ['Punjab', 'Chandigarh', 'Haryana', 'Delhi', 'Uttar Pradesh', 'Bihar', 'West Bengal']:
    d.polygon([P(*c) for c in G['states'][n]], fill=(255, 110, 30, 120))
img = Image.alpha_composite(img, fill)
# India official outline (Kashmir fully inside): white line with saffron glow
ol = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ol)
for r in G['india']:
    pts = [P(*c) for c in r]; d.line(pts + [pts[0]], fill=(255, 153, 51, 255), width=22, joint='curve')
ol = ol.filter(ImageFilter.GaussianBlur(9)); img = Image.alpha_composite(img, ol)
ol2 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ol2)
for r in G['india']:
    pts = [P(*c) for c in r]; d.line(pts + [pts[0]], fill=(255, 255, 255, 255), width=7, joint='curve')
img = Image.alpha_composite(img, ol2)
# the lid (visual joke): a giant shiny pot lid sitting on the plain, smoke leaking from under the rim
LX, LY, LW, LH = 540, 1120, 940, 250
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((LX - LW / 2 + 20, LY - 40, LX + LW / 2 + 40, LY + 90), fill=(0, 0, 0, 150)); img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(26)))
smoke = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(smoke)
import random; random.seed(4)
for i in range(70):
    a = random.uniform(0, math.pi * 2); rx = LX + math.cos(a) * LW / 2 * random.uniform(.85, 1.1); ry = LY + 20 + math.sin(a) * 55 * random.uniform(.6, 1.2) - random.uniform(0, 50)
    r = random.uniform(30, 75); g = random.randint(170, 215); d.ellipse((rx - r, ry - r, rx + r, ry + r), fill=(g, g - 6, g - 14, 120))
img = Image.alpha_composite(img, smoke.filter(ImageFilter.GaussianBlur(14)))
lid = Image.new('RGBA', (W, H), (0, 0, 0, 0))
dome = Image.new('L', (W, H), 0); ImageDraw.Draw(dome).ellipse((LX - LW / 2, LY - LH, LX + LW / 2, LY + LH), fill=255); ImageDraw.Draw(dome).rectangle((0, LY + 2, W, H), fill=0)
grad = Image.new('RGBA', (W, H)); gd = ImageDraw.Draw(grad)
for y in range(int(LY - LH), int(LY) + 3):
    t = (y - (LY - LH)) / LH; v = int(250 - 120 * t + 30 * math.sin(t * 6)); gd.line((0, y, W, y), fill=(v, min(255, v + 6), min(255, v + 14), 255))
lid.paste(grad, (0, 0), dome)
hl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(hl).ellipse((LX - 330, LY - LH + 40, LX - 40, LY - LH + 150), fill=(255, 255, 255, 170)); lid = Image.alpha_composite(lid, Image.composite(hl.filter(ImageFilter.GaussianBlur(18)), Image.new('RGBA', (W, H), (0, 0, 0, 0)), dome))
d = ImageDraw.Draw(lid)
d.ellipse((LX - LW / 2 - 14, LY - 34, LX + LW / 2 + 14, LY + 34), outline=(40, 44, 52, 255), width=16)
d.ellipse((LX - LW / 2 - 6, LY - 26, LX + LW / 2 + 6, LY + 26), outline=(225, 230, 238, 255), width=8)
d.arc((LX - LW / 2, LY - LH, LX + LW / 2, LY + LH), 180, 360, fill=(30, 32, 38, 255), width=12)
d.ellipse((LX - 85, LY - LH - 70, LX + 85, LY - LH + 30), fill=(22, 22, 24, 255), outline=(8, 8, 8, 255), width=8)
d.ellipse((LX - 50, LY - LH - 58, LX + 10, LY - LH - 30), fill=(120, 120, 128, 255))
img = Image.alpha_composite(img, lid)
# text: 1-3 words, last word in a yellow box (black text, thin white border)
dr = ImageDraw.Draw(img)
if LANG == 'en': top, box, F = 'UNDER A', 'LID?', 'bsd900.ttf'
else: top, box, F = 'बंद', 'ढक्कन', 'muk800.ttf'
f1 = ImageFont.truetype(F, 190 if LANG == 'en' else 170); f2 = ImageFont.truetype(F, 230 if LANG == 'en' else 190)
tw = dr.textlength(top, font=f1); dr.text(((W - tw) / 2, 150), top, font=f1, fill=(255, 255, 255), stroke_width=16, stroke_fill=(3, 16, 26))
bb = dr.textbbox((0, 0), box, font=f2); bw, bh = bb[2] - bb[0], bb[3] - bb[1]; bx = (W - bw) / 2; by = 400
q = '' if LANG == 'en' else '?'; fq = ImageFont.truetype('bsd900.ttf', 230); qw = dr.textlength(q, font=fq) if q else 0
bx -= qw / 2
pad = 34; dr.rounded_rectangle((bx - pad, by + bb[1] - pad * .7, bx + bw + qw + pad, by + bb[3] + pad * .7), radius=26, fill=(255, 210, 0), outline=(255, 255, 255), width=8)
dr.text((bx, by), box, font=f2, fill=(10, 10, 10))
if q: dr.text((bx + bw + 6, by + bb[1] - 40), q, font=fq, fill=(10, 10, 10))
badge = Image.open('/home/claude/media-engine/citylapse/engine/assets/bhugol_badge.png').convert('RGBA').resize((130, 130)); img.alpha_composite(badge, (34, 34))
img.convert('RGB').save(OUT, quality=93)
img.convert('RGB').resize((140, 249), Image.LANCZOS).save(OUT.replace('.jpg', '_feed.jpg'))
print(OUT)
