# Assemble the Money Mirage HyperFrames project: python3 build.py [out_dir]
import json, os, sys, shutil, glob
HERE = os.path.dirname(os.path.abspath(__file__)); MM = '/home/claude/mm-work'
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'proj')
os.makedirs(os.path.join(out, 'assets'), exist_ok=True)
TIM = json.load(open(os.path.join(HERE, 'build/timing.json')))
D = {'dur': TIM['dur'], 'lines': TIM['lines'], 'chapters': TIM['chapters'], 'env': TIM['env']}
files = sorted(glob.glob(os.path.join(HERE, 'scenes', 'ch*.js')))
if os.environ.get('ONLY'): files = [f for f in files if os.path.basename(f)[:-3] in os.environ['ONLY'].split(',')]
code = '\n'.join(open(f).read() for f in files)
names = [os.path.basename(f)[:-3] for f in files]
code += '\nfunction SCENES() {\n' + ''.join(f'  startCh({int(n[2:])}); {n}();\n' for n in names) + '}\n'
fonts = {'brico800.woff2': '@fontsource/bricolage-grotesque/files/bricolage-grotesque-latin-800-normal.woff2',
         'brico700.woff2': '@fontsource/bricolage-grotesque/files/bricolage-grotesque-latin-700-normal.woff2',
         'inter600.woff2': '@fontsource/inter/files/inter-latin-600-normal.woff2',
         'inter800.woff2': '@fontsource/inter/files/inter-latin-800-normal.woff2',
         'inter900.woff2': '@fontsource/inter/files/inter-latin-900-normal.woff2'}
for d, s in fonts.items():
    p = os.path.join(out, 'assets', d)
    if not os.path.exists(p): shutil.copy(os.path.join(MM, 'node_modules', s), p)
for src, dst in [('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 'assets/emoji.ttf'), (os.path.join(HERE, 'assets/world.jpg'), 'assets/world.jpg'),
                 (os.path.join(MM, 'node_modules/gsap/dist/gsap.min.js'), 'gsap.min.js')]:
    if not os.path.exists(os.path.join(out, dst)): shutil.copy(src, os.path.join(out, dst))
shutil.copytree(os.path.join(HERE, 'assets/arch'), os.path.join(out, 'assets/arch'), dirs_exist_ok=True)
tpl = open(os.path.join(HERE, 'template.html')).read().replace('__SCENES__', code).replace('__DATA__', json.dumps(D, ensure_ascii=False))
segs = json.loads(sys.argv[2]) if len(sys.argv) > 2 else None
open(os.path.join(out, 'index.html'), 'w').write(tpl.replace('__SEG__', 'null').replace('__DUR__', '%.3f' % D['dur']))
if segs:
    for i, (a, b) in enumerate(segs):
        open(os.path.join(out, f'seg{i:02d}.html'), 'w').write(tpl.replace('__SEG__', json.dumps([a, b])).replace('__DUR__', '%.3f' % (b - a)))
print('built', out, 'dur', D['dur'], 'chapters', names)
