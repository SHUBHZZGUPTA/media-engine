# sheet.py <dir> <comma labels> <cols> <w> <h> — contact sheet of frame-*.png (sorted by time) with time labels -> <dir>/sheet.jpg
import sys, glob, re
from PIL import Image, ImageDraw
d, ts, cols, w, h = sys.argv[1], sys.argv[2].split(','), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
fs = sorted(glob.glob(d + '/frame-*.png'), key=lambda f: float(re.search(r'at-([\d.]+)s', f).group(1)))
W = Image.new('RGB', (cols * w, ((len(fs) + cols - 1) // cols) * (h + 10)), '#111'); dr = ImageDraw.Draw(W)
for i, f in enumerate(fs):
    x, y = (i % cols) * w, (i // cols) * (h + 10); W.paste(Image.open(f).convert('RGB').resize((w, h)), (x, y)); dr.text((x + 5, y + 4), ts[i] if i < len(ts) else '', fill='#ff0')
W.save(d + '/sheet.jpg', quality=85); print('sheet', len(fs), d + '/sheet.jpg')
