import sys, subprocess, numpy as np, soundfile as sf, tempfile, os
v = sys.argv[1]; T = tempfile.mkdtemp()
n = int(subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', v], capture_output=True, text=True).stdout.strip())
for k, f in (('first', 0), ('last', n - 1)): subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', v, '-vf', f'select=eq(n\\,{f})', '-frames:v', '1', f'{T}/{k}.png'], check=True)
from PIL import Image
a = np.asarray(Image.open(f'{T}/first.png').convert('RGB'), float); b = np.asarray(Image.open(f'{T}/last.png').convert('RGB'), float)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', v, '-ac', '1', '-ar', '48000', f'{T}/a.wav'], check=True)
y, sr = sf.read(f'{T}/a.wav'); r = lambda x: 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9); q = int(.15 * sr)
print(f'frames {n} | last vs first frame mean abs diff {np.abs(a - b).mean():.2f}/255 | audio RMS last/first 0.15 s: {r(y[-q:]):.1f} / {r(y[:q]):.1f} dB')
Image.fromarray(np.hstack([a, b]).astype(np.uint8)).resize((1080, 960)).save(sys.argv[2])
