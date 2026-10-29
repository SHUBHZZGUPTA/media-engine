import sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
S, A1, A2 = sys.argv[1], "../../art", "../../art2"
F = "/usr/share/fonts/truetype/google-fonts/Poppins-Black.ttf"
import os
if not os.path.exists(F): F = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
W, H = 1280, 720
def bg(path, zoom=1.0, cx=.5, cy=.5, dark=.0):
    im = Image.open(path).convert("RGB"); w, h = im.size; s = max(W / w, H / h) * zoom
    im = im.resize((int(w * s), int(h * s)), Image.LANCZOS); x = int((im.width - W) * cx); y = int((im.height - H) * cy)
    im = im.crop((x, y, x + W, y + H))
    if dark: im = ImageEnhance.Brightness(im).enhance(1 - dark)
    return im.convert("RGBA")
def char(name, h, flip=False):
    p = f"{A2}/{name}.png" if os.path.exists(f"{A2}/{name}.png") else f"{A1}/{name}.png"
    im = Image.open(p).convert("RGBA"); im = im.crop(im.getbbox()); s = h / im.height
    im = im.resize((int(im.width * s), h), Image.LANCZOS)
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    a = im.split()[3]; glow = Image.new("RGBA", (im.width + 40, im.height + 40), (0, 0, 0, 0))
    m = Image.new("L", glow.size, 0); m.paste(a, (20, 20)); m = m.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(4))
    glow.paste(Image.new("RGBA", glow.size, (255, 255, 255, 255)), (0, 0), m); glow.alpha_composite(im, (20, 20)); return glow
def text(img, s, xy, size, fill=(255, 214, 0), stroke=10, anchor="mm", rot=0):
    f = ImageFont.truetype(F, size); L = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.text(xy, s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(10, 10, 10), anchor=anchor)
    sh = L.filter(ImageFilter.GaussianBlur(8)); sh2 = Image.new("RGBA", img.size, (0, 0, 0, 0)); sh2.paste((0, 0, 0, 160), (0, 0), sh.split()[3])
    if rot: L = L.rotate(rot, center=xy, resample=Image.BICUBIC); sh2 = sh2.rotate(rot, center=xy, resample=Image.BICUBIC)
    img.alpha_composite(sh2, (6, 8)); img.alpha_composite(L)
def loop(img, box, col=(230, 40, 40), w=16):
    L = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.arc(box, 200, 515, fill=col, width=w)
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2; rx, ry = (box[2] - box[0]) / 2, (box[3] - box[1]) / 2
    a = math.radians(515); ex, ey = cx + rx * math.cos(a), cy + ry * math.sin(a); t = a + math.pi / 2
    d.polygon([(ex + 34 * math.cos(t), ey + 34 * math.sin(t)), (ex + 22 * math.cos(t + 2.2), ey + 22 * math.sin(t + 2.2)), (ex + 22 * math.cos(t - 2.2), ey + 22 * math.sin(t - 2.2))], fill=col)
    img.alpha_composite(L)
# A: the loop
im = bg(f"{S}/th_C_size.jpg", 1.15, .62, .35)
grad = Image.new("L", (W, H)); gd = ImageDraw.Draw(grad)
for x in range(W): gd.line([(x, 0), (x, H)], fill=int(max(0, 200 - x * .32)))
im.paste((0, 0, 0, 255), (0, 0), grad)
loop(im, (40, 300, 860, 700))
for k, (n, h) in enumerate([("c_rurik", 330), ("c_ivan4", 350), ("c_catherine", 340), ("c_lenin", 360)]):
    c = char(n, h); im.alpha_composite(c, (70 + k * 195, 690 - c.height))
text(im, "SAME", (300, 120), 150); text(im, "STORY", (300, 255), 150, fill=(255, 255, 255))
im.convert("RGB").save("thumb_A_loop.jpg", quality=92)
# B: Alaska 2 cents
im = bg(f"{S}/th_B_america.jpg", 1.0, .5, .5)
grad = Image.new("L", (W, H)); gd = ImageDraw.Draw(grad)
for x in range(W): gd.line([(x, 0), (x, H)], fill=int(max(0, min(180, (x - 650) * .6))))
im.paste((0, 0, 0, 255), (0, 0), grad)
c = char("c_traveller", 400, flip=True); im.alpha_composite(c, (W - c.width - 10, H - c.height + 10))
text(im, "2¢", (900, 140), 220, fill=(255, 214, 0), rot=6)
text(im, "AN ACRE", (860, 300), 92, fill=(255, 255, 255), rot=6)
im.convert("RGB").save("thumb_B_alaska.jpg", quality=92)
