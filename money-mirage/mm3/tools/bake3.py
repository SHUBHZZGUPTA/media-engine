# Bake HyperFrames media treatments into stills (works around graded media in later-starting scenes
# rendering untreated in hyperframes 0.8.181). Each (image, look) is graded by `hyperframes media-treatment`
# on a 2400x1350 composition and snapshotted, so the look is still the HyperFrames shader's output.
# usage: python3 bake.py name:look [name:look ...]   -> assets/img/baked/<stem>__<look>.jpg
import os, sys, json, shutil, subprocess
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from mmpaths import *
sys.path.insert(0, HERE)
LOOKS = {
    'print': '{"intensity":1,"adjust":{"contrast":0.08,"highlights":-0.06,"shadows":0.04},"effects":{"twoInkPrint":1,"twoInkPrintSize":0.42}}',
    'film': '{"preset":"vintage-wash","intensity":0.6,"details":{"vignette":0.12,"grain":0.12,"grainSize":0.2,"grainRoughness":0.6}}',
    'soft': '{"preset":"vintage-wash","intensity":0.5,"adjust":{"exposure":-0.35},"effects":{"blur":0.55}}',
}
ENV = dict(os.environ, HYPERFRAMES_NO_TELEMETRY='1', DO_NOT_TRACK='1', HYPERFRAMES_NO_UPDATE_CHECK='1', HYPERFRAMES_SKIP_SKILLS='1',
           HYPERFRAMES_BROWSER_PATH=os.environ.get('HYPERFRAMES_BROWSER_PATH', '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'))
OUT = os.path.join(HERE, 'art/baked'); os.makedirs(OUT, exist_ok=True)
for spec in sys.argv[1:]:
    name, look = spec.split(':'); stem = os.path.splitext(name)[0]; dst = os.path.join(OUT, f'{stem}__{look}.jpg')
    if os.path.exists(dst): continue
    if look == 'none':
        p = os.path.join(HERE, 'art', name) if os.path.exists(os.path.join(HERE, 'art', name)) else os.path.join(SRC, name)
        Image.open(p).convert('RGB').save(dst, quality=93); print('copied', dst); continue
    if look == 'soft':  # the film look from HyperFrames, then a still-image defocus + darken for grounds behind a hero object
        subprocess.run([sys.executable, __file__, f'{name}:film'], check=True)
        from PIL import Image, ImageFilter, ImageEnhance
        im = Image.open(os.path.join(OUT, f'{stem}__film.jpg')).filter(ImageFilter.GaussianBlur(16))
        ImageEnhance.Brightness(im).enhance(.62).save(dst, quality=93); print('baked', dst); continue
    d = os.path.join(HERE, 'bake', f'{stem}__{look}'); shutil.rmtree(d, ignore_errors=True); os.makedirs(d + '/assets')
    src = next((os.path.join(DEP, j, stem + '_x2.jpg') for j in DEPTH_JOBS if os.path.exists(os.path.join(DEP, j, stem + '_x2.jpg'))), None)
    if not src: src = os.path.join(HERE, 'art', name) if os.path.exists(os.path.join(HERE, 'art', name)) else os.path.join(SRC, name)
    print('  source', src)
    shutil.copy(src, d + '/assets/' + name); shutil.copy(os.path.join(ENG, 'node_modules/gsap/dist/gsap.min.js'), d)
    w0, h0 = Image.open(src).size; CW, CH = (2560, 1440) if w0 >= h0 else (1440, round(1440 * h0 / w0))   # portrait plates keep their aspect
    open(d + '/index.html', 'w').write(f'''<!doctype html><html><head><meta charset="UTF-8"><script src="./gsap.min.js"></script>
<style>body{{margin:0}}#root{{position:relative;width:{CW}px;height:{CH}px;overflow:hidden;background:#000}}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="1" data-width="{CW}" data-height="{CH}">
<img id="m" src="assets/{name}" style="position:absolute;left:0;top:0;width:{CW}px;height:{CH}px;object-fit:cover" alt=""></div>
<script>window.__timelines={{}};window.__timelines.main=gsap.timeline({{paused:true}}).to({{}},{{duration:1}});</script></body></html>''')
    subprocess.run(['npx', 'hyperframes', 'media-treatment', '--project', d, '--selector', '#m', '--grading', LOOKS[look], '--apply'], env=ENV, check=True, capture_output=True, cwd=ENG)
    subprocess.run(['npx', 'hyperframes', 'snapshot', d, '-o', d + '/snap', '--at', '0.5', '--no-end', '--describe', 'false'], env=ENV, check=True, capture_output=True, cwd=ENG)
    from PIL import Image
    Image.open(d + '/snap/frame-00-at-0.5s.png').convert('RGB').save(dst, quality=93)
    print('baked', dst)
