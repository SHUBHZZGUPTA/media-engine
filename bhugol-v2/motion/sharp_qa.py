"""Sharpness QA for map shots (15 Nov 2026, after the Gibraltar Short's blocky map edges slipped past a contact-sheet review).

Scores every part of a frame for real fine detail and saves the worst full-resolution 1:1 crops to look at.
Blocky or blurry imagery (a texture stretched past its resolution) has almost no detail finer than ~3 px,
so each 360x360 tile is scored by how much of its texture survives a 3x down-and-up resample.
Flat tiles (open sea, solid colour, caption boxes) are skipped.

Usage: python3 sharp_qa.py <video.mp4 | frame.png ...> [--every 2] [--times 8,46,76] [--out qa_sharp] [--min 0.12]
Writes <out>/sheet.jpg (worst crops at 1:1 with time + score) and <out>/report.json; exit 1 when a tile fails.
Always LOOK at sheet.jpg too: the score catches stretched imagery, the eye catches everything else.
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

args = sys.argv[1:]
def opt(k, d=None):
    if k in args: i = args.index(k); v = args[i + 1]; del args[i:i + 2]; return v
    return d
EVERY = float(opt('--every', 2)); TIMES = opt('--times'); OUT = opt('--out', 'qa_sharp'); MIN = float(opt('--min', 0.12))
os.makedirs(OUT, exist_ok=True)
T = 360

def frames():
    if args[0].lower().endswith(('.png', '.jpg', '.jpeg')):
        for f in args: yield os.path.basename(f), Image.open(f).convert('RGB')
        return
    v = args[0]; dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', v], capture_output=True, text=True).stdout)
    ts = [float(x) for x in TIMES.split(',')] if TIMES else list(np.arange(.5, dur - .3, EVERY))
    for t in ts:
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', v, '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
        yield f'{t:.1f}s', Image.frombytes('RGB', (1080, 1920), raw)

def score(tile):
    g = np.asarray(tile.convert('L'), np.float32)
    if g.std() < 6: return None                                   # flat: sea, sky, a solid card
    lo = np.asarray(tile.convert('L').resize((T // 3, T // 3), Image.BOX).resize((T, T), Image.BICUBIC), np.float32)
    hf = np.abs(g - lo).mean(); tex = np.abs(g - np.asarray(tile.convert('L').filter(ImageFilter.GaussianBlur(12)), np.float32)).mean()
    return float(hf / (tex + 1e-6))                                # share of the tile's texture that is finer than ~3 px

rows = []
for name, im in frames():
    for y in range(0, 1920 - T + 1, T):
        for x in range(0, 1080 - T + 1, T):
            c = im.crop((x, y, x + T, y + T)); s = score(c)
            if s is not None: rows.append({'at': name, 'x': x, 'y': y, 'score': round(s, 3), 'crop': c})
rows.sort(key=lambda r: r['score']); worst = rows[:12]
sheet = Image.new('RGB', (4 * (T + 8), 3 * (T + 34)), 'white'); d = ImageDraw.Draw(sheet)
for i, r in enumerate(worst):
    X, Y = (i % 4) * (T + 8), (i // 4) * (T + 34); sheet.paste(r['crop'], (X, Y + 30))
    d.text((X + 4, Y + 6), f"{r['at']} x{r['x']} y{r['y']}  score {r['score']}{'  FAIL' if r['score'] < MIN else ''}", fill=(200, 0, 0) if r['score'] < MIN else (0, 0, 0))
sheet.save(os.path.join(OUT, 'sheet.jpg'), quality=90)
fails = [r for r in rows if r['score'] < MIN]
json.dump({'min': MIN, 'tiles': len(rows), 'fails': [{k: v for k, v in r.items() if k != 'crop'} for r in fails],
           'worst': [{k: v for k, v in r.items() if k != 'crop'} for r in worst]}, open(os.path.join(OUT, 'report.json'), 'w'), indent=1)
print(f"{len(rows)} textured tiles, {len(fails)} below {MIN}; worst {worst[0]['score'] if worst else '-'} at {worst[0]['at'] if worst else '-'} -> {OUT}/sheet.jpg")
sys.exit(1 if fails else 0)
