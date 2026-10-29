import sys
sys.argv = [sys.argv[0], sys.argv[1]]
exec(open("make_thumbs.py").read().split("# A: the loop")[0])
from PIL import ImageEnhance
P = Image.open("putin_cut.png").convert("RGBA")
import numpy as np
_a = np.array(P.split()[3], np.float32); h_, w_ = _a.shape
fy = np.clip((h_ * .97 - np.arange(h_)) / (h_ * .30), 0, 1)[:, None]        # body dissolves towards the bottom
fx = np.clip(np.arange(w_) / (w_ * .14), 0, 1)[None, :] * np.ones((h_, 1))   # soften the cut left edge
fx = np.maximum(fx, (np.arange(h_) < h_ * .55)[:, None])
P.putalpha(Image.fromarray((_a * fy * fx).astype(np.uint8)))
def putin(h):
    p = P.resize((int(P.width * h / P.height), h), Image.LANCZOS)
    a = p.split()[3]; g = Image.new("RGBA", (p.width + 60, p.height + 60), (0, 0, 0, 0))
    m = Image.new("L", g.size, 0); m.paste(a, (30, 30)); m = m.filter(ImageFilter.MaxFilter(11)).filter(ImageFilter.GaussianBlur(10))
    g.paste(Image.new("RGBA", g.size, (230, 40, 40, 255)), (0, 0), m.point(lambda v: int(v * .8))); g.alpha_composite(p, (30, 30)); return g
def base():
    im = bg(f"{S}/th_C_size.jpg", 1.15, .62, .35)
    grad = Image.new("L", (W, H)); gd = ImageDraw.Draw(grad)
    for x in range(W): gd.line([(x, 0), (x, H)], fill=int(max(0, 210 - x * .28)))
    im.paste((0, 0, 0, 255), (0, 0), grad); return im
# A2: SAME STORY, rulers loop into Putin
im = base(); pu = putin(820); im.alpha_composite(pu, (W - pu.width + 140, H - pu.height + 140))
loop(im, (30, 330, 770, 705))
for k, (n, h) in enumerate([("c_rurik", 270), ("c_ivan4", 285), ("c_catherine", 275), ("c_lenin", 290)]):
    c = char(n, h); im.alpha_composite(c, (55 + k * 170, 690 - c.height))
text(im, "SAME", (290, 115), 150); text(im, "STORY", (290, 250), 150, fill=(255, 255, 255))
im.convert("RGB").save("thumb_A2_putin_loop.jpg", quality=92)
# C: 1,100 YEARS, Viking vs Putin
im = base(); pu = putin(860); im.alpha_composite(pu, (W - pu.width + 160, H - pu.height + 160))
c = char("c_rurik", 420); im.alpha_composite(c, (60, H - c.height - 10))
text(im, "1,100", (400, 120), 160); text(im, "YEARS", (400, 265), 120, fill=(255, 255, 255))
d = ImageDraw.Draw(im); d.line([(420, 470), (620, 470)], fill=(230, 40, 40), width=18); d.polygon([(620, 440), (680, 470), (620, 500)], fill=(230, 40, 40))
im.convert("RGB").save("thumb_C_putin_1100.jpg", quality=92)
