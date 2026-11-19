# Replace frames [a, b) of a silent 30 fps master with PNG snapshots (sorted by time). Usage: patch.py <silent.mp4> <png_dir> <a> <b> <out.mp4>
import sys, os, subprocess, glob, tempfile, re
src, pd, a, b, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
pngs = sorted(glob.glob(pd + '/frame-*.png'), key=lambda f: float(re.search(r'at-([\d.]+)s', f).group(1)))
assert len(pngs) == b - a, (len(pngs), b - a)
T = tempfile.mkdtemp(); run = lambda c: subprocess.run(c, check=True)
for i, f in enumerate(pngs): os.symlink(os.path.abspath(f), f'{T}/p{i:05d}.png')
enc = ['-c:v', 'libx264', '-preset', 'fast', '-crf', '10', '-pix_fmt', 'yuv420p', '-r', '30']
run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf', f'trim=start_frame=0:end_frame={a},setpts=PTS-STARTPTS', '-an'] + enc + [f'{T}/h.mp4'])
run(['ffmpeg', '-v', 'error', '-y', '-framerate', '30', '-i', f'{T}/p%05d.png', '-vf', 'scale=1080:1920'] + enc + [f'{T}/m.mp4'])
run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf', f'trim=start_frame={b},setpts=PTS-STARTPTS', '-an'] + enc + [f'{T}/t.mp4'])
open(f'{T}/l.txt', 'w').write(f"file '{T}/h.mp4'\nfile '{T}/m.mp4'\nfile '{T}/t.mp4'\n")
run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{T}/l.txt', '-c', 'copy', out])
print(subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', out], capture_output=True, text=True).stdout.strip(), 'frames ->', out)
