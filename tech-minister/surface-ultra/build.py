# Builds the HyperFrames project for the Tech Minister Surface Laptop Ultra reel.
# Usage: python3 build.py <timing_final.json> <out_dir>
import json, os, sys, shutil

tim_p, out = sys.argv[1:3]
HERE = os.path.dirname(os.path.abspath(__file__))
TIM = json.load(open(tim_p)); DUR = TIM['dur']
os.makedirs(os.path.join(out, 'assets'), exist_ok=True)

# Caption chunks: [spoken segment (matches the TTS text tokens), display text ('|' = line break, *key*)]
CH = [
 [["You can now carry", "YOU CAN NOW CARRY"], ["a petaflop in your backpack.", "A *PETAFLOP* IN|YOUR *BACKPACK.*"],
  ["In two thousand eight, it filled a room...", "IN *2008,* IT FILLED|A *ROOM...*"], ["and cost over a hundred million dollars.", "AND COST OVER|*$100 MILLION.*"],
  ["So what changed?", "SO WHAT *CHANGED?*"]],
 [["Rewind to two thousand eight.", "REWIND TO *2008.*"], ["IBM's Roadrunner became", "IBM'S *ROADRUNNER*|BECAME"],
  ["the first computer to break a petaflop.", "THE FIRST COMPUTER|TO BREAK A *PETAFLOP.*"]],
 [["Nearly three hundred racks.", "NEARLY *300 RACKS.*"], ["Two point three five megawatts of power.", "*2.35 MEGAWATTS*|OF POWER."]],
 [["Now Microsoft's Surface Laptop Ultra", "NOW MICROSOFT'S|*SURFACE LAPTOP ULTRA*"], ["claims... up to one petaflop.", "CLAIMS... UP TO|*ONE PETAFLOP.*"]],
 [["So did a supercomputer", "SO DID A|*SUPERCOMPUTER*"], ["just shrink into a backpack?", "JUST SHRINK INTO|A *BACKPACK?*"]],
 [["Here's the catch.", "HERE'S THE *CATCH.*"]],
 [["Roadrunner counted in big,", "ROADRUNNER COUNTED|IN BIG,"], ["precise, sixty-four-bit numbers.", "PRECISE, *64-BIT*|NUMBERS."]],
 [["Nvidia's R T X Spark chip", "NVIDIA'S *RTX SPARK*|CHIP"], ["hits its petaflop with tiny four-bit numbers...", "HITS ITS PETAFLOP WITH|TINY *4-BIT* NUMBERS..."],
  ["plus a shortcut called sparsity.", "PLUS A SHORTCUT|CALLED *SPARSITY.*"]],
 [["Same word.", "SAME *WORD.*"], ["Very different math.", "VERY DIFFERENT *MATH.*"]],
 [["So why care? Memory.", "SO WHY CARE?|*MEMORY.*"]],
 [["Most laptops give the graphics chip", "MOST LAPTOPS GIVE|THE *GRAPHICS CHIP*"], ["its own small memory.", "ITS OWN|*SMALL* MEMORY."]],
 [["This one shares a single pool.", "THIS ONE SHARES|A *SINGLE POOL.*"], ["Up to one hundred and twenty-eight gigabytes.", "UP TO|*128 GIGABYTES.*"]],
 [["Not all of it goes to graphics.", "NOT ALL OF IT|GOES TO *GRAPHICS.*"], ["In one test, the G P U", "IN ONE TEST,|THE *GPU*"],
  ["could reach about one hundred and ten.", "COULD REACH|ABOUT *110.*"]],
 [["Enough to fit an A I model", "ENOUGH TO FIT|AN *AI MODEL*"], ["with a hundred and twenty billion parameters.", "WITH *120 BILLION*|PARAMETERS."]],
 [["On your lap.", "ON YOUR *LAP.*"], ["No cloud. No server room.", "NO *CLOUD.* NO|*SERVER ROOM.*"]],
 [["The bill?", "THE *BILL?*"], ["From two thousand five hundred and ninety-nine dollars.", "FROM *$2,599.*"],
  ["The one-twenty-eight-gig version?", "THE *128-GIG*|VERSION?"], ["Five thousand, eight hundred and ninety-nine.", "*$5,899.*"]],
 [["So no, it's not a", "SO NO, IT'S NOT A"], ["two-thousand-eight supercomputer.", "*2008*|SUPERCOMPUTER."],
  ["It's an A I lab... in a backpack.", "IT'S AN *AI LAB...*|IN A *BACKPACK.*"]],
 [["Roadrunner drew two point three five megawatts.", "ROADRUNNER DREW|*2.35 MEGAWATTS.*"],
  ["This one charges from a hundred-and-forty-watt brick.", "THIS ONE CHARGES|FROM A *140-WATT* BRICK."]],
 [["This is Tech Minister.", "THIS IS|*TECH MINISTER.*"], ["Follow for tech, minus the hype.", "*FOLLOW* FOR TECH,|MINUS THE *HYPE.*"]],
]
assert len(CH) == len(TIM['lines']), (len(CH), len(TIM['lines']))
flat = []
for li, row in enumerate(CH):
    W = TIM['lines'][li]['words']; w0 = 0
    for spoken, disp in row:
        n = len(spoken.split())
        wt = W[w0:w0 + n]; assert len(wt) == n, (li, spoken)
        flat.append({'li': li, 'txt': disp, 'sn': round(wt[0] - .06, 3), 'wt': [round(x - .03, 3) for x in wt]}); w0 += n
    assert w0 == len(W), (li, w0, len(W))
for i, c in enumerate(flat): c['en'] = flat[i + 1]['sn'] if i < len(flat) - 1 else DUR + 1
S = [round(l['start'], 3) for l in TIM['lines']]; E = [round(l['end'], 3) for l in TIM['lines']]
# chunk start lookup C[li][ci]
CS = {}
for c in flat: CS.setdefault(c['li'], []).append(c['sn'])
D = {'dur': DUR, 'S': S, 'E': E, 'CS': CS, 'chunks': flat}

FONTS = {'bodoni800.woff2': '/tmp/claude-0/-home-claude/c09a985c-a081-5cf5-b813-df1fcadd3047/scratchpad/brand/node_modules/@fontsource/bodoni-moda/files/bodoni-moda-latin-800-normal.woff2',
         'inter800.woff2': '/home/claude/tm-work/node_modules/@fontsource/inter/files/inter-latin-800-normal.woff2',
         'inter600.woff2': '/home/claude/tm-work/node_modules/@fontsource/inter/files/inter-latin-600-normal.woff2'}
for dst, src in FONTS.items(): shutil.copy(src, os.path.join(out, 'assets', dst))
for f in os.listdir(os.path.join(HERE, 'assets')):
    shutil.copy(os.path.join(HERE, 'assets', f), os.path.join(out, 'assets', f))
shutil.copy('/home/claude/tm-work/node_modules/gsap/dist/gsap.min.js', os.path.join(out, 'gsap.min.js'))
tpl = open(os.path.join(HERE, 'template.html')).read()
html = tpl.replace('__DATA__', json.dumps(D)).replace('__DUR__', '%.3f' % DUR)
# media clip timing placeholders: __S3__ etc. resolved here so the <video> tags carry literal numbers
import re
def sub(m):
    expr = m.group(1)
    return '%.3f' % eval(expr, {'S': S, 'E': E, 'DUR': DUR, 'min': min, 'max': max})
html = re.sub(r'\{\{(.+?)\}\}', sub, html)
open(os.path.join(out, 'index.html'), 'w').write(html)
print('built', out, 'dur', DUR, 'chunks', len(flat))
