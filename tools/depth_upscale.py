"""Depth maps + 2x upscaling for scene art, on GitHub Actions (CPU).
Usage: python3 tools/depth_upscale.py jobs/depth/<id>.json
Job: {"id": "...", "images": ["library/scenes/x.jpg", ...], "depth": ["library/scenes/x.jpg"], "upscale": ["..."]}
  images   default list for both steps; "depth" / "upscale" override per step
Writes outputs/depth/<id>/<stem>_depth.png (16-bit, bright = near) and <stem>_x2.jpg (or .png when the source has alpha).
Models: Depth-Anything-V2-Small (Hugging Face), Real-ESRGAN x2plus (GitHub release), loaded with spandrel.
"""
import json, os, sys, time, urllib.request
import numpy as np, torch
from PIL import Image

job = json.load(open(sys.argv[1])); out = os.path.join('outputs', 'depth', job['id']); os.makedirs(out, exist_ok=True)
imgs = job.get('images', []); rep = {'depth': [], 'upscale': []}
torch.set_num_threads(os.cpu_count() or 4)

dl = job.get('depth', imgs)
if dl:
    from transformers import pipeline
    pipe = pipeline('depth-estimation', model='depth-anything/Depth-Anything-V2-Small-hf', device=-1)
    for p in dl:
        t0 = time.time(); im = Image.open(p).convert('RGB')
        r = pipe(im); d = r['predicted_depth']
        d = torch.nn.functional.interpolate(d[None] if d.dim() == 3 else d[None, None], size=(im.height, im.width), mode='bicubic', align_corners=False)[0, 0].numpy()
        d = (d - d.min()) / max(1e-6, d.max() - d.min())
        stem = os.path.splitext(os.path.basename(p))[0]
        Image.fromarray((d * 65535).astype(np.uint16)).save(os.path.join(out, stem + '_depth.png'))
        rep['depth'].append({'src': p, 'secs': round(time.time() - t0, 1)}); print('depth', p, flush=True)

ul = job.get('upscale', imgs)
if ul:
    from spandrel import ModelLoader
    w = '/tmp/RealESRGAN_x2plus.pth'
    if not os.path.exists(w):
        urllib.request.urlretrieve('https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth', w)
    model = ModelLoader().load_from_file(w).eval(); S = model.scale
    def up(rgb):  # rgb uint8 HxWx3 -> upscaled, tiled with overlap
        H, W, _ = rgb.shape; T, O = 256, 16; outa = np.zeros((H * S, W * S, 3), np.float32)
        x = torch.from_numpy(rgb.astype(np.float32) / 255).permute(2, 0, 1)[None]
        for y0 in range(0, H, T):
            for x0 in range(0, W, T):
                ya, yb, xa, xb = max(0, y0 - O), min(H, y0 + T + O), max(0, x0 - O), min(W, x0 + T + O)
                with torch.no_grad(): o = model(x[:, :, ya:yb, xa:xb])[0].permute(1, 2, 0).clamp(0, 1).numpy()
                cy, cx = (y0 - ya) * S, (x0 - xa) * S; h, w_ = min(T, H - y0) * S, min(T, W - x0) * S
                outa[y0 * S:y0 * S + h, x0 * S:x0 * S + w_] = o[cy:cy + h, cx:cx + w_]
        return (outa * 255 + .5).astype(np.uint8)
    for p in ul:
        t0 = time.time(); im = Image.open(p); stem = os.path.splitext(os.path.basename(p))[0]
        if im.mode in ('RGBA', 'LA', 'P'):
            im = im.convert('RGBA'); a = im.getchannel('A')
            rgb = up(np.array(im.convert('RGB')))
            res = Image.fromarray(rgb).convert('RGBA'); res.putalpha(a.resize(res.size, Image.LANCZOS))
            res.save(os.path.join(out, stem + '_x2.png'), optimize=True)
        else:
            Image.fromarray(up(np.array(im.convert('RGB')))).save(os.path.join(out, stem + '_x2.jpg'), quality=94)
        rep['upscale'].append({'src': p, 'secs': round(time.time() - t0, 1)}); print('upscale', p, flush=True)
json.dump(rep, open(os.path.join(out, 'report.json'), 'w'), indent=1); print(rep)
