"""Build a HyperFrames project page for a city timelapse.
Usage: python3 build_page.py <plan.json> <scene_dir> <out_proj_dir> [--w 1280 --h 720]
"""
import base64, json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ENG = os.path.join(HERE, '..', 'engine')
plan_p, scene_d, out = sys.argv[1:4]
arg = lambda k, d: int(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
W, H = arg('--w', 1280), arg('--h', 720)
plan = json.load(open(plan_p)); scene = json.load(open(os.path.join(scene_d, 'scene.json')))
os.makedirs(os.path.join(out, 'assets'), exist_ok=True)
nm = os.path.join(ENG, 'node_modules')
shutil.copy(os.path.join(nm, 'three/build/three.min.js'), out); shutil.copy(os.path.join(nm, 'gsap/dist/gsap.min.js'), out)
for wgt in (500, 600, 700): shutil.copy(os.path.join(nm, f'@fontsource/oswald/files/oswald-latin-{wgt}-normal.woff2'), os.path.join(out, 'assets', f'oswald{wgt}.woff2'))
shutil.copy(os.path.join(ENG, 'assets', 'bhugol_badge.png'), os.path.join(out, 'assets', 'bhugol_badge.png'))
for fn in ('land.png', 'roads.png'): shutil.copy(os.path.join(scene_d, fn), os.path.join(out, 'assets', fn))
bld = base64.b64encode(open(os.path.join(scene_d, 'bld.bin'), 'rb').read()).decode()
D = {'dur': plan['dur'], 'plan': plan, 'scene': scene, 'bld': bld}
html = open(os.path.join(ENG, 'city.html')).read()
html = (html.replace('__DATA__', json.dumps(D, separators=(',', ':'))).replace('__W__', str(W)).replace('__H__', str(H))
        .replace('__DUR__', str(plan['dur'])).replace('__S__', f'{W / 1920:.4f}').replace('__TITLE__', plan.get('title', 'city timelapse')))
open(os.path.join(out, 'index.html'), 'w').write(html)
print('built', out, f'{len(html) / 1e6:.1f} MB', W, H, plan['dur'], 's')
