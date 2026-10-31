#!/usr/bin/env python3
"""Reusable explainer-board graphics (transparent PNGs) for long-form videos.

  bars(path, title, rows)             rows = [(label, value, display, "#hex")]
  cycle(path, steps, upto, highlight) the repeating-story loop, revealed up to step `upto`
  chapter(path, labels, current, title, cols=6) parchment chapter map, current chapter highlighted (cols=7 for 13-14 chapters)
"""
import math
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
INK, MUTED, RED, GOLD, PAPER, PAPER_EDGE = (34, 34, 34), (120, 120, 120), (214, 66, 58), (240, 186, 50), (236, 214, 170), (150, 110, 60)
def F(s): return ImageFont.truetype(FONT, s)

def bars(path, title, rows, w=1100, h=700):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((0, 0), title, font=F(52), fill=INK)
    vmax = max(r[1] for r in rows); top = 110; bh = (h - top) // len(rows) - 24
    for k, (lab, v, disp, col) in enumerate(rows):
        y = top + k * (bh + 24)
        d.text((0, y + bh // 2), lab, font=F(40), fill=INK, anchor="lm")
        x0 = 260; x1 = x0 + int((w - x0 - 230) * v / vmax)
        d.rounded_rectangle([x0, y, x1, y + bh], radius=14, fill=col)
        d.text((x1 + 18, y + bh // 2), disp, font=F(38), fill=INK, anchor="lm")
    im.save(path)

def cycle(path, steps, upto, highlight=None, w=1100, h=820):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx, cy, R = w // 2, h // 2 + 10, 300; n = len(steps); pts = []
    for k in range(n):
        a = -math.pi / 2 + 2 * math.pi * k / n; pts.append((cx + R * math.cos(a), cy + R * math.sin(a)))
    for k in range(min(upto, n)):            # arrows between revealed steps
        if k + 1 < upto or (upto == n and k == n - 1):
            a0 = -math.pi / 2 + 2 * math.pi * (k + .22) / n; a1 = -math.pi / 2 + 2 * math.pi * (k + .78) / n
            arc = [(cx + R * math.cos(a0 + (a1 - a0) * u / 20), cy + R * math.sin(a0 + (a1 - a0) * u / 20)) for u in range(21)]
            d.line(arc, fill=MUTED, width=8)
            ex, ey = arc[-1]; px, py = arc[-3]; ang = math.atan2(ey - py, ex - px)
            d.polygon([(ex + 20 * math.cos(ang), ey + 20 * math.sin(ang)), (ex + 18 * math.cos(ang + 2.4), ey + 18 * math.sin(ang + 2.4)), (ex + 18 * math.cos(ang - 2.4), ey + 18 * math.sin(ang - 2.4))], fill=MUTED)
    for k in range(min(upto, n)):
        x, y = pts[k]; hot = (highlight == k) if highlight is not None else (k == upto - 1)
        col = RED if hot else (255, 255, 255)
        tw = d.textlength(steps[k], font=F(40))
        d.rounded_rectangle([x - tw / 2 - 26, y - 40, x + tw / 2 + 26, y + 40], radius=40, fill=col, outline=INK, width=4)
        d.text((x, y), steps[k], font=F(40), fill=(255, 255, 255) if hot else INK, anchor="mm")
    if upto >= n: d.text((cx, cy), "AGAIN", font=F(72), fill=RED, anchor="mm")
    im.save(path)

def chapter(path, labels, current, title, w=1700, h=900, cols=6):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([40, 40, w - 40, h - 40], radius=30, fill=PAPER, outline=PAPER_EDGE, width=10)
    for x in (40, w - 70):                    # scroll rollers
        d.rounded_rectangle([x, 20, x + 30, h - 20], radius=15, fill=PAPER_EDGE)
    rows = math.ceil(len(labels) / cols); r = 92 if cols <= 6 else 84
    for k, lab in enumerate(labels):
        gx, gy = k % cols, k // cols
        x = 240 + gx * ((w - 480) / (cols - 1)); y = 230 + gy * 260
        if k + 1 < len(labels) and gx < cols - 1: d.line([(x + r, y), (x + (w - 480) / (cols - 1) - r, y)], fill=PAPER_EDGE, width=6)
        done, now = k < current, k == current
        fill = RED if now else ((214, 190, 140) if done else (246, 232, 200))
        d.ellipse([x - r, y - r, x + r, y + r], fill=fill, outline=PAPER_EDGE, width=6)
        d.text((x, y), lab, font=F(30 if len(lab) < (9 if r >= 92 else 7) else 24), fill=(255, 255, 255) if now else INK, anchor="mm")
    d.text((w // 2, h - 120), title, font=F(64), fill=INK, anchor="mm")
    im.save(path)
