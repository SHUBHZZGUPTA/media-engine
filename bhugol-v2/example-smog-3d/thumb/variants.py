import json, math, random, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
LANG = sys.argv[1] if len(sys.argv) > 1 else 'en'
G = json.load(open('../art/geo.json')); W, H = 1080, 1920
F = 'bsd900.ttf' if LANG == 'en' else 'muk800.ttf'
TXT = {'en': {'v1': ('NO', 'EXIT?'), 'v2': ('AQI', '488?!'), 'v3': ('TRAPPED', 'HERE?'), 'v4': ("CAN'T", 'ESCAPE?')},
       'hi': {'v1': ('कोई', 'रास्ता नहीं'), 'v2': ('AQI', '488?!'), 'v3': ('यहाँ', 'क़ैद'), 'v4': ('निकल', 'नहीं पाता?')}}[LANG]
def pop(im): im = ImageEnhance.Contrast(im).enhance(1.15); im = ImageEnhance.Color(im).enhance(1.35); return ImageEnhance.Brightness(im).enhance(1.05)
def text(img, top, box, y=150):
    dr = ImageDraw.Draw(img); f1 = ImageFont.truetype(F, 170); qf = ImageFont.truetype('bsd900.ttf', 230)
    def font_for(s): return ImageFont.truetype('bsd900.ttf', 230) if all(ord(c) < 128 for c in s) else ImageFont.truetype(F, 190)
    f1 = ImageFont.truetype('bsd900.ttf', 180) if all(ord(c) < 128 for c in top) else ImageFont.truetype(F, 170)
    if top: tw = dr.textlength(top, font=f1); dr.text(((W - tw) / 2, y), top, font=f1, fill=(255, 255, 255), stroke_width=16, stroke_fill=(3, 16, 26))
    q = ''
    if not all(ord(c) < 128 for c in box) and box.endswith('?'): box, q = box[:-1], '?'
    f2 = font_for(box); bb = dr.textbbox((0, 0), box, font=f2); bw = bb[2] - bb[0]; qw = dr.textlength(q, font=qf) if q else 0
    bx = (W - bw - qw) / 2; by = y + 250; pad = 34
    dr.rounded_rectangle((bx - pad, by + bb[1] - pad * .7, bx + bw + qw + pad, by + bb[3] + pad * .7), radius=26, fill=(255, 210, 0), outline=(255, 255, 255), width=8)
    dr.text((bx, by), box, font=f2, fill=(10, 10, 10))
    if q: dr.text((bx + bw + 6, by + bb[1] - 40), q, font=qf, fill=(10, 10, 10))
    badge = Image.open('/home/claude/media-engine/citylapse/engine/assets/bhugol_badge.png').convert('RGBA').resize((120, 120)); img.alpha_composite(badge, (30, 30))
def title_text(img, lines, box, y):
    dr = ImageDraw.Draw(img); asc = lambda t: all(ord(c) < 128 for c in t)
    for ln in lines:
        f = ImageFont.truetype('bsd900.ttf', 150) if asc(ln) else ImageFont.truetype(F, 128)
        if ln.endswith('🇮🇳'):
            ln = ln[:-2].rstrip(); tw = dr.textlength(ln, font=f) + 130
            x = (W - tw) / 2; dr.text((x, y), ln, font=f, fill=(255, 255, 255), stroke_width=14, stroke_fill=(3, 16, 26))
            em = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109); e = Image.new('RGBA', (140, 140), (0, 0, 0, 0))
            ImageDraw.Draw(e).text((0, 0), '🇮🇳', font=em, embedded_color=True); e = e.resize((112, 112)); img.alpha_composite(e, (int(x + tw - 112), int(y + 22)))
        else:
            tw = dr.textlength(ln, font=f); dr.text(((W - tw) / 2, y), ln, font=f, fill=(255, 255, 255), stroke_width=14, stroke_fill=(3, 16, 26))
        y += 158
    text(img, '', box, y=y - 250 + 20)
def outline(img, P, fillcol=None, flag=False):
    if flag:
        m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
        for r in G['india']: d.polygon([P(*c) for c in r], fill=255)
        ys = [P(0, la)[1] for r in G['india'] for _, la in r]; y0, y1 = min(ys), max(ys); h = (y1 - y0) / 3
        fl = Image.new('RGBA', (W, H)); fd = ImageDraw.Draw(fl)
        fd.rectangle((0, y0, W, y0 + h), fill=(255, 153, 51, 255)); fd.rectangle((0, y0 + h, W, y0 + 2 * h), fill=(255, 255, 255, 255)); fd.rectangle((0, y0 + 2 * h, W, H), fill=(19, 136, 8, 255))
        cx, cy = P(79, 22.5); r0 = 40; fd.ellipse((cx - r0, cy - r0, cx + r0, cy + r0), outline=(0, 0, 128, 255), width=7)
        for i in range(24): a = i * math.pi / 12; fd.line((cx, cy, cx + math.cos(a) * r0, cy + math.sin(a) * r0), fill=(0, 0, 128, 255), width=2)
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.paste((0, 0, 0, 170), (14, 22), m); img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
        img.paste(fl, (0, 0), m)
    ol = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ol)
    for r in G['india']: pts = [P(*c) for c in r]; d.line(pts + [pts[0]], fill=(255, 255, 255, 255), width=8, joint='curve')
    img.alpha_composite(ol)
def cloud(img, cx, cy, s, face=True):
    random.seed(7); c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    blobs = [(-1.0, .15, .55), (-.55, -.25, .62), (0, -.42, .72), (.55, -.22, .62), (1.0, .15, .52), (-.4, .3, .55), (.4, .3, .55), (0, .25, .6)]
    for x, y, r in blobs: d.ellipse((cx + (x - r) * s, cy + (y - r) * s, cx + (x + r) * s, cy + (y + r) * s), fill=(20, 20, 24, 255))
    inner = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d2 = ImageDraw.Draw(inner)
    for x, y, r in blobs: d2.ellipse((cx + (x - r) * s + 14, cy + (y - r) * s + 14, cx + (x + r) * s - 14, cy + (y + r) * s - 14), fill=(150, 140, 128, 255))
    for x, y, r in blobs: d2.ellipse((cx + (x - r * .7) * s, cy + (y - r * .9) * s, cx + (x + r * .3) * s, cy + (y - r * .2) * s), fill=(190, 182, 170, 255))
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.paste((0, 0, 0, 150), (0, 30), c.split()[3]); img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    img.alpha_composite(c); img.alpha_composite(inner)
    if face:
        d = ImageDraw.Draw(img); e = s * .16
        for sx in (-1, 1):
            d.ellipse((cx + sx * s * .3 - e, cy - s * .1 - e, cx + sx * s * .3 + e, cy - s * .1 + e), fill=(255, 255, 255), outline=(20, 20, 24), width=8)
            d.ellipse((cx + sx * s * .26 - e * .45, cy - s * .06 - e * .45, cx + sx * s * .26 + e * .45, cy - s * .06 + e * .45), fill=(20, 20, 24))
            d.line((cx + sx * s * .12, cy - s * .32, cx + sx * s * .48, cy - s * .24), fill=(20, 20, 24), width=14)
        d.arc((cx - s * .25, cy + s * .08, cx + s * .25, cy + s * .38), 200, 340, fill=(20, 20, 24), width=12)
# --- V1: India in its flag (official boundary), a grumpy smog cloud parked on the north ---
gl = Image.open('/home/claude/work/smog/art/mp/globe.jpg').convert('RGB'); GW, GH = gl.size
lo0, lo1 = 65.0, 100.5; la1 = 21.0 + (lo1 - lo0) * 16 / 9 / 2 * .78; la0 = 21.0 - (lo1 - lo0) * 16 / 9 / 2 * 1.22
x0 = (lo0 + 180) / 360 * GW; x1 = (lo1 + 180) / 360 * GW; y0 = (90 - la1) / 180 * GH; y1 = (90 - la0) / 180 * GH
b1 = pop(gl.crop((int(x0), int(y0), int(x1), int(y1))).resize((W, H), Image.LANCZOS)).convert('RGBA')
P1 = lambda lo, la: ((lo - lo0) / (lo1 - lo0) * W, (la1 - la) / (la1 - la0) * H)
outline(b1, P1, flag=True); cloud(b1, *P1(82.5, 26.6), 150); text(b1, *TXT['v1'], y=1330); b1.convert('RGB').save(f'v1_{LANG}.jpg', quality=92)
# --- V2: real haze + a giant AQI gauge pinned in the red ---
hz = Image.open('/home/claude/work/smog/art/ga_wide.jpg').convert('RGB'); b2 = pop(hz).convert('RGBA')
g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(g); cx, cy, R = 540, 1260, 420
d.rounded_rectangle((cx - 500, cy - 520, cx + 500, cy + 180), radius=60, fill=(8, 12, 22, 225), outline=(255, 255, 255), width=10)
cols = [(46, 194, 126), (245, 211, 60), (255, 154, 31), (255, 75, 43), (179, 18, 74), (90, 11, 58)]
for i in range(180):
    t = i / 179; k = t * 5; a0 = math.radians(180 + t * 180); c0 = cols[min(4, int(k))]; c1 = cols[min(5, int(k) + 1)]; f = k - int(k)
    col = tuple(int(c0[j] + (c1[j] - c0[j]) * f) for j in range(3))
    d.arc((cx - R, cy - R, cx + R, cy + R), 180 + t * 180 - 1, 180 + t * 180 + 1.2, fill=col + (255,), width=90)
ang = math.radians(180 + 488 / 500 * 180); d.line((cx, cy, cx + math.cos(ang) * (R - 40), cy + math.sin(ang) * (R - 40)), fill=(255, 255, 255), width=26)
d.ellipse((cx - 44, cy - 44, cx + 44, cy + 44), fill=(255, 255, 255), outline=(3, 16, 26), width=10)
fM = ImageFont.truetype('bsd900.ttf', 74); d.text((cx + R - 40, cy + 40), 'MAX 500', font=fM, fill=(255, 194, 58), stroke_width=8, stroke_fill=(3, 16, 26), anchor='mt')
b2.alpha_composite(g); text(b2, *TXT['v2']); b2.convert('RGB').save(f'v2_{LANG}.jpg', quality=92)
# --- V3: haze piled against the Himalaya, India outline, red circle on the plain ---
b3 = pop(hz).convert('RGBA'); SW = 4096; x0w = 1506.61; cw = 1240.31
P3 = lambda lo, la: (((lo - 68) / 26 * SW - x0w) * W / cw, (34 - la) / 14 * H)
outline(b3, P3); fill = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fill)
for n in ['Punjab', 'Chandigarh', 'Haryana', 'Delhi', 'Uttar Pradesh', 'Bihar', 'West Bengal']: fd.polygon([P3(*c) for c in G['states'][n]], fill=(255, 60, 40, 95))
b3.alpha_composite(fill)
d = ImageDraw.Draw(b3); cx, cy = P3(80.6, 27.2)
for k in range(3): d.ellipse((cx - 470 + k * 3, cy - 300 - k * 2, cx + 470 - k * 2, cy + 300 + k * 3), outline=(255, 59, 48), width=12)
cloud(b3, *P3(81.0, 27.6), 190, face=True); text(b3, *TXT['v3']); b3.convert('RGB').save(f'v3_{LANG}.jpg', quality=92)
b4 = pop(hz).convert('RGBA'); outline(b4, P3)
d = ImageDraw.Draw(b4); cx, cy = P3(80.4, 26.0)
cloud(b4, cx, cy, 230, face=True); d = ImageDraw.Draw(b4)
ax0, ay0, ax1, ay1 = cx + 30, cy - 250, cx + 110, cy - 640
d.line((ax0, ay0, ax1, ay1), fill=(255, 59, 48), width=26); hd = math.atan2(ay1 - ay0, ax1 - ax0)
d.polygon([(ax1 + math.cos(hd) * 40, ay1 + math.sin(hd) * 40), (ax1 + math.cos(hd + 2.4) * 70, ay1 + math.sin(hd + 2.4) * 70), (ax1 + math.cos(hd - 2.4) * 70, ay1 + math.sin(hd - 2.4) * 70)], fill=(255, 59, 48))
bx, by = (ax0 + ax1) / 2 + 10, (ay0 + ay1) / 2 + 30; r = 95
d.ellipse((bx - r, by - r, bx + r, by + r), fill=(255, 255, 255), outline=(200, 20, 20), width=22); d.line((bx - r * .62, by - r * .62, bx + r * .62, by + r * .62), fill=(200, 20, 20), width=24)
text(b4, *TXT['v4'], y=1330); b4.convert('RGB').save(f'v4_{LANG}.jpg', quality=92)
b5 = pop(hz).convert('RGBA'); outline(b5, P3); cloud(b5, cx, cy - 60, 210, face=True); d = ImageDraw.Draw(b5)
ax0, ay0, ax1, ay1 = cx + 30, cy - 290, cx + 110, cy - 640
d.line((ax0, ay0, ax1, ay1), fill=(255, 59, 48), width=26); hd = math.atan2(ay1 - ay0, ax1 - ax0)
d.polygon([(ax1 + math.cos(hd) * 40, ay1 + math.sin(hd) * 40), (ax1 + math.cos(hd + 2.4) * 70, ay1 + math.sin(hd + 2.4) * 70), (ax1 + math.cos(hd - 2.4) * 70, ay1 + math.sin(hd - 2.4) * 70)], fill=(255, 59, 48))
bx, by = (ax0 + ax1) / 2 + 10, (ay0 + ay1) / 2 + 30; r = 95
d.ellipse((bx - r, by - r, bx + r, by + r), fill=(255, 255, 255), outline=(200, 20, 20), width=22); d.line((bx - r * .62, by - r * .62, bx + r * .62, by + r * .62), fill=(200, 20, 20), width=24)
if LANG == 'en': title_text(b5, ["WHY CAN'T", "DELHI'S SMOG 🇮🇳"], 'ESCAPE?', 1180)
else: title_text(b5, ['दिल्ली का स्मॉग', 'निकल क्यों 🇮🇳'], 'नहीं पाता?', 1180)
b5.convert('RGB').save(f'v5_{LANG}.jpg', quality=92)
for v in ('v1', 'v2', 'v3', 'v4', 'v5'): Image.open(f'{v}_{LANG}.jpg').resize((140, 249), Image.LANCZOS).save(f'{v}_{LANG}_feed.jpg')
print('ok')
