"""Turn depth/upscale job outputs into 3D-scene assets for a BHUGOL v2 build.
Usage: python3 prep3d.py <outputs/depth/<id>> <art_dir> [--chars c_a,c_b] [--soft 3]
For every <stem>_x2.jpg/png with a matching <stem>_depth.png: writes plate_<stem>.jpg (2x art) and depth_<stem>.png
(8-bit, 512x768, edge-grown then softened so foreground edges don't tear). Characters (<name>_x2.png) are trimmed to
their alpha box at <=1400 px. Also writes noise.png (used by the grass/reveal shader).
"""
import argparse, glob, os
import numpy as np
from PIL import Image, ImageFilter
ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('art'); ap.add_argument('--chars', default=''); ap.add_argument('--soft', type=float, default=3)
a = ap.parse_args(); S = a.src.rstrip('/') + '/'; A = a.art.rstrip('/') + '/'; os.makedirs(A, exist_ok=True)
for dp in glob.glob(S + '*_depth.png'):
    stem = os.path.basename(dp)[:-10]; up = next((S + stem + '_x2' + e for e in ('.jpg', '.png') if os.path.exists(S + stem + '_x2' + e)), None)
    if not up: continue
    Image.open(up).convert('RGB').save(A + f'plate_{stem}.jpg', quality=93)
    d = np.array(Image.open(dp)).astype(np.float32); d = d / max(1.0, d.max())
    Image.fromarray((d * 255).astype(np.uint8)).resize((512, 768), Image.BILINEAR).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(a.soft)).save(A + f'depth_{stem}.png')
    print('scene', stem)
for n in filter(None, a.chars.split(',')):
    im = Image.open(S + n + '_x2.png').convert('RGBA'); im = im.crop(im.getbbox()); im.thumbnail((1400, 1400)); im.save(A + n + '.png', optimize=True); print('char', n)
rng = np.random.default_rng(3); n = np.zeros((256, 256))
for s, w in ((8, .5), (16, .3), (32, .2)):
    n += w * np.array(Image.fromarray((rng.random((s, s)) * 255).astype(np.uint8)).resize((256, 256), Image.BICUBIC)) / 255
Image.fromarray(((n - n.min()) / (n.max() - n.min()) * 255).astype(np.uint8)).save(A + 'noise.png')
