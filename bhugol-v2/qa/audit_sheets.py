"""Full visual audit before ANY delivery (22 Oct 2026): frames every 0.5 s of the exact file being delivered, as labelled
contact sheets. Every sheet must be looked at; numbers alone (jitter, cadence) do not prove a picture is there.
Usage: python3 audit_sheets.py <video.mp4> <out_dir>      -> <out_dir>/sheet_00.jpg ... (8 x 3 frames per sheet)"""
import glob, os, subprocess, sys
from PIL import Image, ImageDraw
v, out = sys.argv[1:3]; os.makedirs(out, exist_ok=True)
for f in glob.glob(os.path.join(out, 'f_*.png')) + glob.glob(os.path.join(out, 'sheet_*.jpg')): os.remove(f)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', v, '-vf', 'fps=2,scale=216:384', os.path.join(out, 'f_%04d.png')], check=True)
fs = sorted(glob.glob(os.path.join(out, 'f_*.png'))); C, R = 8, 3; per = C * R
for s in range(0, len(fs), per):
    sh = Image.new('RGB', (C * 216, R * 402), 'white'); d = ImageDraw.Draw(sh)
    for k, f in enumerate(fs[s:s + per]):
        x, y = (k % C) * 216, (k // C) * 402; sh.paste(Image.open(f), (x, y + 18)); d.text((x + 4, y + 3), f'{(s + k) * .5:.1f}s', fill='black')
    sh.save(os.path.join(out, f'sheet_{s // per:02d}.jpg'), quality=80)
for f in fs: os.remove(f)
print(f'{(len(fs) + per - 1) // per} sheets in {out}: view every one before delivering')
