# Money Mirage ep01 v2 preview: HyperFrames-native project builder.
# One scene per sub-composition (compositions/sNN.html), one captions composition, audio as placed <audio>.
# Timing comes from build/timing.json (word times per script line, from conform.py --words).
# usage: python3 build.py  -> writes proj/ ; then treat.sh applies HyperFrames media treatments.
import json, os, re, shutil, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from note import note_svg
P = os.path.join(HERE, 'proj'); ARCH = '/home/claude/mm-work/engine/assets/arch'
TIM = json.load(open(os.path.join(HERE, 'build/timing.json')))
LINES = TIM['lines']; DUR = TIM['dur']
W = [(w, a, b, li) for li, L in enumerate(LINES) for (w, a, b) in L['d']]
nrm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())

def A(phrase, off=0.0, nth=0):
    """Start time of the first (nth) occurrence of phrase in the narration."""
    q = [nrm(x) for x in phrase.split()]; hits = []
    for i in range(len(W) - len(q) + 1):
        if all(nrm(W[i + k][0]) == q[k] for k in range(len(q))): hits.append(i)
    if len(hits) <= nth: raise SystemExit(f'anchor not found: {phrase}')
    return round(W[hits[nth]][1] + off, 3)

def AE(phrase, off=0.0, nth=0):
    q = phrase.split(); i0 = None
    qn = [nrm(x) for x in q]; hits = []
    for i in range(len(W) - len(qn) + 1):
        if all(nrm(W[i + k][0]) == qn[k] for k in range(len(qn))): hits.append(i)
    i0 = hits[nth]; return round(W[i0 + len(qn) - 1][2] + off, 3)

def AW(li, word, nth=0):
    hits = [a for (w, a, b) in LINES[li]['d'] if nrm(w) == nrm(word)]
    return round(hits[nth], 3)
LS = lambda li: LINES[li]['a']
LE = lambda li: LINES[li]['b']

# ---------------------------------------------------------------- scene authoring
class Scene:
    def __init__(self, sid, a, b):
        self.id, self.a, self.b = sid, round(a, 3), round(b, 3); self.html = []; self.css = []; self.js = []; self.treat = []
        self.sfx = []
    @property
    def d(self): return round(self.b - self.a, 3)
    def t(self, abs_t): return round(abs_t - self.a, 3)
    def add(self, h): self.html.append(h)
    def tw(self, s): self.js.append(s)

    def plate(self, name, look, kb=(1.0, 1.06), frm=(0, 0), to=(0, 0), pos='50% 50%', origin='50% 50%', key='plate', extra_treat=None):
        """Full-bleed image on a camera wrapper. look: 'print' (archival evidence) | 'film' (paintings) | 'soft' (blurred ground)."""
        iid = f'{self.id}-{key}'; cid = f'{self.id}-{key}cam'
        if look: BAKE.add(f'{name}:{look}'); name = f'baked/{os.path.splitext(name)[0]}__{look}.jpg'
        self.add(f'<div id="{cid}" class="cam" style="transform-origin:{origin}"><img id="{iid}" class="plate" src="assets/img/{name}" style="object-position:{pos}" alt=""></div>')
        self.tw(f'tl.fromTo("#{cid}",{{scale:{kb[0]},xPercent:{frm[0]},yPercent:{frm[1]}}},{{scale:{kb[1]},xPercent:{to[0]},yPercent:{to[1]},duration:{self.d},ease:"none"}},0);')
        copy_img(name); return cid

    def sfx_at(self, name, abs_t, vol=1.0): SFX.append((name, round(abs_t, 3), vol))

    def build(self):
        css = '\n'.join(self.css)
        return f'''<template>
<style>
#root{{position:absolute;inset:0;overflow:hidden;background:#000}}
#{self.id} .cam{{position:absolute;inset:0;will-change:transform}}
#{self.id} .plate{{position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover}}
#{self.id} .num{{position:absolute;font-family:Inter;font-weight:900;font-variant-numeric:tabular-nums;color:#E9B44C;letter-spacing:-.02em;line-height:1;white-space:nowrap;text-shadow:0 6px 0 rgba(0,0,0,.45),0 0 40px rgba(0,0,0,.55)}}
#{self.id} svg.ov{{position:absolute;left:0;top:0;overflow:visible}}
{css}
</style>
<div id="root" data-composition-id="{self.id}" data-width="1920" data-height="1080">
<div id="{self.id}">
{chr(10).join(self.html)}
</div>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(self.js)}
tl.set({{}}, {{}}, {self.d});
window.__timelines["{self.id}"] = tl;
</script>
</template>'''

LOOKS = {
    'print': '{"intensity":1,"adjust":{"contrast":0.08,"highlights":-0.06,"shadows":0.04},"effects":{"twoInkPrint":1,"twoInkPrintSize":0.42}}',
    'film': '{"preset":"vintage-wash","intensity":0.6,"details":{"vignette":0.12,"grain":0.12,"grainSize":0.2,"grainRoughness":0.6}}',
    'soft': '{"preset":"vintage-wash","intensity":0.5,"adjust":{"exposure":-0.35},"effects":{"blur":0.55}}',
    None: None,
}
COPIED = set(); BAKE = set()
def copy_img(name):
    if name in COPIED: return
    src = os.path.join(HERE, 'assets/img', name)
    if not os.path.exists(src): src = os.path.join(ARCH, name)
    if not os.path.exists(src): MISSING.append(name); return
    os.makedirs(os.path.dirname(os.path.join(P, 'assets/img', name)), exist_ok=True)
    shutil.copy(src, os.path.join(P, 'assets/img', name)); COPIED.add(name)
MISSING = []

SFX = []

def scribble(cx, cy, rx, ry, rot=-6, seed=1, turns=1.12):
    R = random.Random(seed); pts = []; n = 90; a0 = R.uniform(0, 6.28)
    for i in range(int(n * turns) + 1):
        t = a0 + 2 * math.pi * i / n; k = 1 + .045 * math.sin(3 * t + seed) + R.uniform(-.012, .012) + .05 * i / n
        x, y = rx * k * math.cos(t), ry * k * math.sin(t); r = math.radians(rot)
        pts.append((cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r)))
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)

def draw_on(S, el, at_abs, dur=.55):
    S.tw(f'(()=>{{const p=document.querySelector("{el}");const L=p.getTotalLength()||3000;tl.fromTo(p,{{strokeDasharray:L,strokeDashoffset:L,opacity:1}},{{strokeDashoffset:0,duration:{dur},ease:"power2.inOut"}},{S.t(at_abs)});}})();')

def blur_in(S, el, at_abs, d=.18):
    S.tw(f'tl.fromTo("{el}",{{opacity:0,filter:"blur(8px)"}},{{opacity:1,filter:"blur(0px)",duration:{d},ease:"power4.out"}},{S.t(at_abs)});')

def blur_out(S, el, at_abs, d=.18):
    S.tw(f'tl.to("{el}",{{opacity:0,filter:"blur(8px)",duration:{d},ease:"power3.in"}},{S.t(at_abs)});')

def dip_out(S, d=0.1):
    """Dip cut: the outgoing frame darkens ~40% for 3 frames before the hard cut."""
    S.add(f'<div id="{S.id}-dip" style="position:absolute;inset:0;background:#000;opacity:0"></div>')
    S.tw(f'tl.fromTo("#{S.id}-dip",{{opacity:0}},{{opacity:.42,duration:.04}},{S.d - d});')

# ---------------------------------------------------------------- the shots
os.makedirs(os.path.join(P, 'compositions'), exist_ok=True); os.makedirs(os.path.join(P, 'assets/img'), exist_ok=True)
os.makedirs(os.path.join(P, 'assets/audio'), exist_ok=True)
SC = []
NOTE = note_svg('nt'); NOTE_NP = note_svg('nt', promise=False)

def note_block(S, key, x, y, scale, rot=0, coin=True, promise=False):
    """The carrier note as inline SVG at (x,y) top-left in px, 1440x640 units scaled."""
    w, h = 1440 * scale, 640 * scale
    nid = f'{S.id}-{key}'
    coin_el = (f'<image id="{nid}-coin" href="assets/img/coin_lion.png" x="560" y="160" width="320" height="317" style="transform-origin:720px 318px;transform-box:view-box"/>' if coin else '')
    S.add(f'<div id="{nid}" data-layout-ignore style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform-origin:50% 50%">'
          f'<svg viewBox="0 0 1440 640" width="{w}" height="{h}" style="overflow:visible;filter:drop-shadow(0 30px 40px rgba(0,0,0,.6))">{(NOTE if promise else NOTE_NP).replace("nt-", nid + "-")}{coin_el}</svg></div>')
    copy_img('coin_lion.png'); return nid

# s01: hook. Wallet plate on screen from frame 0; "1971" lands on the word.
S = Scene('s01', 0, A('So why hasn\'t it died') - .05); SC.append(S)
S.plate('wallet_desk.jpg', 'film', kb=(1.0, 1.05), origin='35% 60%')
S.add('<div id="s01-y" class="num" style="left:1180px;top:300px;font-size:220px;opacity:0">1971</div>')
blur_in(S, '#s01-y', A('1971') - .05, .2); S.sfx_at('thud', A('1971') - .02, .55)
dip_out(S)

# s02: so why hasn't it died? Fort Knox, evidence (print)
S = Scene('s02', SC[-1].b, A('Look at the small print') - .05); SC.append(S)
S.plate('fortknox_postcard.jpg', 'print', kb=(1.04, 1.14), origin='50% 45%')

# s03: the note slides out of the wallet world; camera pushes into the promise line
S = Scene('s03', SC[-1].b, A('In early 1933') - .05); SC.append(S)
S.plate('wallet_desk.jpg', 'soft', kb=(1.08, 1.12), key='bg')
S.add('<div id="s03-cam2" class="cam" style="transform-origin:50% 50%">'); n = note_block(S, 'note', 192, 250, 1.0, coin=True, promise=True); S.add('</div>')
S.tw(f'tl.fromTo("#{n}",{{x:-500,y:420,rotation:-18,opacity:0}},{{x:0,y:0,rotation:-4,opacity:1,duration:.85,ease:"expo.out"}},0.05);')
S.sfx_at('paper_flip2', S.a + .08, .8)
tp = A('small print'); tq = A('I promise'); tw_ = A('Pay you what')
# promise line sits at note-local (720,590) -> page (192+720, 250+590) = (912, 840); push there
S.tw(f'tl.fromTo("#s03-cam2",{{scale:1,x:0,y:0}},{{scale:2.35,x:{(960-912)*2.35:.0f},y:{(540-840)*2.35:.0f},duration:1.1,ease:"power2.inOut"}},{S.t(tp)});')
S.add(f'<svg class="ov" width="1920" height="1080" viewBox="0 0 1920 1080"><path id="s03-circ" d="{scribble(960, 540, 610, 70, rot=-3, seed=4)}" fill="none" stroke="#E8322A" stroke-width="12" stroke-linecap="round" opacity="0"/></svg>')
draw_on(S, '#s03-circ', tw_ - .05, .5)

# s04: the shrinking claim. Same world: camera pulls back, the note moves left; the coin in its oval shrinks with the numbers.
t33, t60, t26 = A('In early 1933'), A('By the 1960s'), A('Today, spend it')
S = Scene('s04', SC[-1].b, A('Somewhere between') - .05); SC.append(S)
S.plate('wallet_desk.jpg', 'soft', kb=(1.12, 1.16), key='bg')
n = note_block(S, 'note', 60, 300, .78, rot=-4)
S.tw(f'tl.fromTo("#{n}",{{x:180,y:-40,scale:1.15,rotation:-4}},{{x:0,y:0,scale:1,rotation:-3,duration:.9,ease:"expo.out"}},0);')
for k, (txt, yr, at) in enumerate([('4.84 oz', '1933', t33), ('2.86 oz', '1960s', t60), ('0.024 oz', '2026', t26)]):
    S.add(f'<div id="s04-yr{k}" class="num" style="left:1290px;top:330px;font-size:64px;color:#F3EBDD;opacity:0">{yr}</div>')
    S.add(f'<div id="s04-oz{k}" class="num" style="left:1280px;top:410px;font-size:150px;opacity:0">{txt}</div>')
    blur_in(S, f'#s04-yr{k}', at + .1); blur_in(S, f'#s04-oz{k}', at + .25)
    if k < 2:
        nxt = [t60, t26][k]; blur_out(S, f'#s04-yr{k}', nxt - .2, .15); blur_out(S, f'#s04-oz{k}', nxt - .2, .15)
scales = [1.0, math.sqrt(2.86 / 4.84), math.sqrt(0.0243 / 4.84)]
S.tw(f'tl.fromTo("#{n}-coin",{{scale:1,transformOrigin:"50% 50%"}},{{scale:{scales[1]:.3f},transformOrigin:"50% 50%",duration:.7,ease:"power3.inOut"}},{S.t(t60 + .2)});')
S.tw(f'tl.fromTo("#{n}-coin",{{scale:{scales[1]:.3f},transformOrigin:"50% 50%"}},{{scale:{scales[2]:.3f},transformOrigin:"50% 50%",immediateRender:false,duration:.9,ease:"power3.inOut"}},{S.t(t26 + .2)});')
S.sfx_at('coins_plate', t33 + .2, .7); S.sfx_at('coin_drop', t60 + .25, .7); S.sfx_at('coin_drop', t26 + .5, .35)
dip_out(S)

# s05: one Sunday night in 1971. Nixon at Camp David (evidence, print), then the living-room TV (painting) on "quietly changed"
tq5 = A('when that promise')
S = Scene('s05', SC[-1].b, tq5 - .05); SC.append(S)
S.plate('nixon_campdavid.jpg', 'print', kb=(1.02, 1.16), origin='48% 42%')
S.sfx_at('thud', A('night in 1971') + .35, .5)
S = Scene('s05b', SC[-1].b, A("So let's follow") - .05); SC.append(S)
S.plate('tv_1971.jpg', 'film', kb=(1.0, 1.1), origin='72% 45%')

# s06: follow one note through 26 centuries: the note recedes as the year runs back, then the camera dives into its oval
S = Scene('s06', SC[-1].b, LS(5) - .02); SC.append(S)
S.plate('wallet_desk.jpg', 'soft', kb=(1.16, 1.2), key='bg')
n = note_block(S, 'note', 240, 230, .1 + .9 * 1.0, coin=False)
S.add('<div id="s06-yr" class="num" style="left:0;width:1920px;text-align:center;top:90px;font-size:130px;opacity:0">2026</div>')
tf = S.a + .1; tc = A('twenty-six centuries')
S.tw(f'tl.fromTo("#{n}",{{scale:.8,rotation:-3}},{{scale:.62,rotation:2,duration:{max(.5, S.d - 1.0):.2f},ease:"sine.inOut"}},0);')
blur_in(S, '#s06-yr', tc - .1)
S.tw(f'(()=>{{const e=document.querySelector("#s06-yr");const o={{v:2026}};tl.fromTo(o,{{v:2026}},{{v:-600,duration:1.6,ease:"power2.inOut",onUpdate:()=>{{const v=Math.round(o.v);e.textContent=v>0?String(v):(v===0?"1":(-v)+" BC");}}}},{S.t(tc + .1)});}})();')
S.sfx_at('clock', tc + .1, .35)
# dive into the empty oval: the note scales up hugely around the oval centre
S.tw(f'tl.to("#{n}",{{scale:7,duration:.7,ease:"power3.in"}},{S.d - .7});')
S.tw(f'tl.to("#s06-yr",{{opacity:0,duration:.15}},{S.d - .7});')
S.sfx_at('whoosh-cinematic', S.b - 3.6, .35)

# s07: barter market (painting). Iris opens from the centre, as if through the oval.
S = Scene('s07', SC[-1].b, A('So people tried') - .05); SC.append(S)
cid = S.plate('barter_market.jpg', 'film', kb=(1.0, 1.08), frm=(0, 0), to=(-2, 0), origin='40% 50%')
S.tw(f'tl.fromTo("#{cid}",{{clipPath:"ellipse(10% 18% at 50% 50%)"}},{{clipPath:"ellipse(80% 95% at 50% 50%)",duration:.55,ease:"power3.out"}},0);')
for at, sc, ox, oy in [(A('You have chickens'), 1.7, 33, 52), (A('You want a goat'), 1.8, 60, 66), (A('The goat owner'), 1.15, 50, 50), (A('Economists call this'), 1.0, 50, 50)]:
    S.tw(f'tl.set("#s07-plate",{{scale:{sc},transformOrigin:"{ox}% {oy}%"}},{S.t(at)});')
S.sfx_at('chicken', A('You have chickens') + .25, .45); S.sfx_at('goat', A('want a goat') + .25, .5)

# s08: shells, cattle, metal... gold. Mint painting, then the coin lands
S = Scene('s08', SC[-1].b, A("It doesn't rust") - .05); SC.append(S)
S.plate('lydia_mint.jpg', 'film', kb=(1.08, 1.0), origin='50% 50%')
S.add('<img id="s08-coin" src="assets/img/coin_lion.png" style="position:absolute;left:660px;top:240px;width:600px;opacity:0;filter:drop-shadow(0 30px 50px rgba(0,0,0,.7))" alt="">')
tg = AW(6, 'Gold.')
S.tw(f'tl.fromTo("#s08-coin",{{opacity:0,scale:1.25,filter:"blur(10px) drop-shadow(0 30px 50px rgba(0,0,0,.7))"}},{{opacity:1,scale:1,filter:"blur(0px) drop-shadow(0 30px 50px rgba(0,0,0,.7))",duration:.35,ease:"expo.out"}},{S.t(tg)});')
S.sfx_at('coin_drop', tg + .05, .8)

# s09: properties of gold: punch-ins on the real coin, hard cuts inside the scene
S = Scene('s09', SC[-1].b, A('More than twenty-five') - .05); SC.append(S)
S.plate('gold_window.jpg', 'soft', kb=(1.1, 1.14), key='bg')
S.add('<div id="s09-cw" class="cam"><img id="s09-coin" src="assets/img/coin_lion.png" style="position:absolute;left:560px;top:140px;width:800px" alt=""></div>')
cuts = [(S.a, 1.0, 0, 0), (A("It doesn't rot"), 1.45, -120, 60), (A("It's rare"), 1.9, 200, -120), (A('You can melt'), 1.2, 0, 0), (A('stamp it'), 2.4, -60, 180), (A('And everyone'), 1.0, 0, 0)]
for at, sc, dx, dy in cuts:
    S.tw(f'tl.set("#s09-cw",{{scale:{sc},x:{dx},y:{dy},transformOrigin:"50% 50%"}},{S.t(at)});')
S.tw(f'tl.fromTo("#s09-coin",{{rotation:-4}},{{rotation:4,duration:{S.d},ease:"none"}},0);')
S.sfx_at('stamp', A('stamp it') + .15, .8)

# s10: Lydia, late 600s BC. Mint painting with the date, then the lion
tl_ = A("lion's")
S = Scene('s10', SC[-1].b, A('But gold had') - .05); SC.append(S)
S.plate('lydia_mint.jpg', 'film', kb=(1.0, 1.07), frm=(0, 0), to=(2, -1), origin='60% 50%')
S.add('<div id="s10-d" class="num" style="left:120px;top:150px;font-size:150px;opacity:0">600s BC</div>')
blur_in(S, '#s10-d', A('More than twenty-five') + .1); blur_out(S, '#s10-d', tl_ - .5)
S.tw(f'tl.set("#s10-plate",{{scale:1.45,transformOrigin:"62% 70%"}},{S.t(A('a natural mix'))});')
S.tw(f'tl.set("#s10-plate",{{scale:1,transformOrigin:"50% 50%"}},{S.t(A('were stamped'))});')
S.add('<div id="s10-lw" style="position:absolute;inset:0;opacity:0"><img id="s10-lg" class="plate" src="assets/img/baked/lydia_mint__soft.jpg" alt=""><img id="s10-lion" src="assets/img/coin_lion.png" style="position:absolute;left:510px;top:60px;width:900px;filter:drop-shadow(0 40px 60px rgba(0,0,0,.75))" alt=""></div>')
BAKE.add('lydia_mint.jpg:soft'); copy_img('baked/lydia_mint__soft.jpg')
S.tw(f'tl.set("#s10-lw",{{opacity:1}},{S.t(tl_ - .25)});')
S.tw(f'tl.fromTo("#s10-lion",{{scale:1.0,rotation:-3}},{{scale:1.12,rotation:2,duration:{S.b - tl_:.2f},ease:"none",transformOrigin:"45% 45%"}},{S.t(tl_ - .25)});')
S.add(f'<svg class="ov" width="1920" height="1080" viewBox="0 0 1920 1080"><path id="s10-circ" d="{scribble(800, 320, 300, 245, rot=-8, seed=7)}" fill="none" stroke="#E8322A" stroke-width="14" stroke-linecap="round" opacity="0"/></svg>')
draw_on(S, '#s10-circ', tl_ + .25, .5)
S.sfx_at('coins_count', A('You could just count') + .2, .6)

# s11: gold is heavy. Vault painting; paper slides in on "back door"
S = Scene('s11', SC[-1].b, LS(len(LINES) - 1) - .05); SC.append(S)
S.plate('bank_vault_1700s.jpg', 'film', kb=(1.0, 1.08), origin='50% 60%')
S.sfx_at('coins_plate', A('backpack full of coins') + .4, .6)
tb = A('let paper in')
n = note_block(S, 'note', 1180, 640, .42, coin=False)
S.tw(f'tl.fromTo("#{n}",{{x:900,rotation:20,opacity:1}},{{x:0,rotation:-6,duration:.7,ease:"expo.out"}},{S.t(tb + .2)});')
S.sfx_at('paper_flip1', tb + .22, .8)

# s12: Goldie (the coin) and Bill (the note) bicker
S = Scene('s12', SC[-1].b, DUR); SC.append(S)
S.plate('bank_vault_1700s.jpg', 'soft', kb=(1.08, 1.1), key='bg')
S.add('<img id="s12-g" src="assets/img/coin_lion.png" style="position:absolute;left:300px;top:300px;width:520px" alt="">')
n = note_block(S, 'note', 980, 380, .56, coin=False)
L = LINES[-1]; gw = [w for w in L['d']]; ta = L['a']
# split the two character lines by the word "I'm"
tbill = next(a for (w, a, b) in L['d'] if nrm(w) == 'im')
S.tw(f'tl.fromTo("#s12-g",{{y:420,rotation:-10}},{{y:0,rotation:0,duration:.6,ease:"back.out(1.6)"}},0);')
S.tw(f'tl.fromTo("#{n}",{{y:420,rotation:12}},{{y:0,rotation:-4,duration:.6,ease:"back.out(1.6)"}},.12);')
S.tw(f'tl.to("#s12-g",{{keyframes:[{{scaleY:.9,scaleX:1.06,duration:.12}},{{scaleY:1.04,scaleX:.98,duration:.14}},{{scaleY:1,scaleX:1,duration:.14}}],transformOrigin:"50% 100%"}},{S.t(ta + .05)});')
S.tw(f'tl.to("#{n}",{{keyframes:[{{y:-30,rotation:-10,duration:.14}},{{y:0,rotation:-4,duration:.2}}],transformOrigin:"50% 100%"}},{S.t(tbill)});')
S.tw(f'tl.to("#s12-g",{{x:-40,duration:.4,ease:"power2.out"}},{S.t(tbill + .3)});')

# ---------------------------------------------------------------- captions: groups of 3-5 words, one at a time
groups = []
for li, L in enumerate(LINES):
    cur = []
    for k, (w, a, b) in enumerate(L['d']):
        cur.append((w, a, b))
        nxt = L['d'][k + 1][1] if k + 1 < len(L['d']) else None
        brk = w.endswith(('.', '?', '!', ',', ':', ';', '...')) and len(cur) >= 2
        if len(cur) >= 5 or brk or nxt is None or (nxt - b) > .15 and len(cur) >= 3:
            groups.append(cur); cur = []
    if cur: groups.append(cur)
cap_html, cap_js = [], []
for gi, g in enumerate(groups):
    a = max(.15, g[0][1] - .05); b = g[-1][2] + .12
    if gi + 1 < len(groups): b = min(b + .25, groups[gi + 1][0][1] - .05)
    txt = ' '.join(w for w, _, _ in g).replace('"', '&quot;')
    txt = re.sub(r'(\b\d[\d,.]*\b)', r'<b>\1</b>', txt)
    cap_html.append(f'<div id="cap{gi}" class="cg">{txt}</div>')
    cap_js.append(f'tl.set("#cap{gi}",{{opacity:1,visibility:"visible"}},{a:.3f});tl.set("#cap{gi}",{{opacity:0,visibility:"hidden"}},{b:.3f});')
open(os.path.join(P, 'compositions/captions.html'), 'w').write(f'''<template>
<style>
#root{{position:absolute;inset:0;pointer-events:none}}
#captions-wrap .cg{{position:absolute;left:0;right:0;bottom:96px;text-align:center;font-family:Inter;font-weight:800;font-size:54px;line-height:1.15;color:#F7F1E3;opacity:0;visibility:hidden;padding:0 240px;
  text-shadow:0 3px 0 rgba(0,0,0,.6),0 0 18px rgba(0,0,0,.85),0 0 4px rgba(0,0,0,.9)}}
#captions-wrap .cg b{{color:#E9B44C;font-weight:900}}
</style>
<div id="root" data-composition-id="captions" data-width="1920" data-height="1080">
<div id="captions-wrap">
{chr(10).join(cap_html)}
</div>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(cap_js)}
tl.set({{}}, {{}}, {DUR:.3f});
window.__timelines["captions"] = tl;
</script>
</template>''')

# ---------------------------------------------------------------- audio
AUD = []
shutil.copy(os.path.join(HERE, 'build/narration.wav'), os.path.join(P, 'assets/audio/narration.wav'))
AUD.append(f'<audio id="vo" class="clip" src="assets/audio/narration.wav" data-start="0" data-duration="{DUR:.3f}" data-track-index="10" data-volume="1"></audio>')
# music: Keys To Unravel under the cold open, Never Dont Stop from chapter 1; ducked under the voice
ch1 = LS(5)
MUS = [('keys', '1_keys.mp3', 0, ch1 + 1.2, json.load(open(os.path.join(HERE, 'build/music_offsets.json')))['keys'] if os.path.exists(os.path.join(HERE, 'build/music_offsets.json')) else 0),
       ('never', '2_never.mp3', ch1 - 1.0, DUR - (ch1 - 1.0), json.load(open(os.path.join(HERE, 'build/music_offsets.json')))['never'] if os.path.exists(os.path.join(HERE, 'build/music_offsets.json')) else 0)]
for mid, f, st, du, off in MUS:
    shutil.copy(os.path.join('/home/claude/mm-work/engine/build/music', f), os.path.join(P, 'assets/audio', f))
    pts = [{"t": 0, "v": 0.32}]
    for L in LINES:
        a, b = L['a'] - st, L['b'] - st
        if b < 0 or a > du: continue
        pts += [{"t": round(max(0, a - .25), 2), "v": 0.32}, {"t": round(max(0, a), 2), "v": 0.14}, {"t": round(b, 2), "v": 0.14}, {"t": round(b + .35, 2), "v": 0.32}]
    pts = sorted({p['t']: p for p in pts}.values(), key=lambda p: p['t'])[:500]
    auto = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": pts}]}).replace('"', '&quot;')
    AUD.append(f'<audio id="mus-{mid}" class="clip" src="assets/audio/{f}" data-start="{st:.3f}" data-duration="{du:.3f}" data-media-start="{off:.2f}" data-track-index="{11 if mid == 'keys' else 9}" data-volume="1" data-fade-in="0.6" data-fade-out="1.5" data-automation="{auto}"></audio>')
SFXDIR = '/home/claude/mm-work/v2/assets/sfx'
for i, (name, t, vol) in enumerate(sorted(SFX, key=lambda x: x[1])):
    fn = name + '.mp3'
    shutil.copy(os.path.join(SFXDIR, fn), os.path.join(P, 'assets/audio', fn))
    import subprocess
    du = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(SFXDIR, fn)], capture_output=True, text=True).stdout)
    du = min(du - .06, 4.0, DUR - t)
    AUD.append(f'<audio id="fx{i:02d}" class="clip" src="assets/audio/{fn}" data-start="{t:.3f}" data-duration="{du:.2f}" data-track-index="{12 + i % 4}" data-volume="{vol * .55:.2f}" data-fade-out="0.3"></audio>')

# ---------------------------------------------------------------- scenes + root
hosts = []
for k, S in enumerate(SC):
    open(os.path.join(P, f'compositions/{S.id}.html'), 'w').write(S.build())
    hosts.append(f'<div id="{S.id}" data-composition-id="{S.id}" data-composition-src="compositions/{S.id}.html" data-start="{S.a:.3f}" data-duration="{S.d:.3f}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index:1"></div>')
hosts.append(f'<div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{DUR:.3f}" data-track-index="2" data-track-kind="captions" data-width="1920" data-height="1080" style="z-index:5"></div>')
shutil.copy('/home/claude/mm-work/node_modules/gsap/dist/gsap.min.js', os.path.join(P, 'gsap.min.js'))
os.makedirs(os.path.join(P, 'assets/fonts'), exist_ok=True)
open(os.path.join(P, 'index.html'), 'w').write(f'''<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=1920, height=1080">
<title>Money Mirage ep01 v2 preview</title>
<script src="./gsap.min.js"></script>
<style>html,body{{margin:0;background:#000}}#root{{position:relative;width:1920px;height:1080px;overflow:hidden;background:#000}}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.3f}" data-width="1920" data-height="1080">
{chr(10).join(hosts)}
{chr(10).join(AUD)}
</div>
<script>window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
</body>
</html>''')
json.dump([{'file': f'compositions/{S.id}.html', 'treat': S.treat} for S in SC if S.treat], open(os.path.join(P, 'treat.json'), 'w'), indent=1)
json.dump(sorted(SFX, key=lambda x: x[1]), open(os.path.join(P, 'sfx.json'), 'w'))
if MISSING: print('NEED BAKE:', ' '.join(sorted(BAKE)))
print('built', P, 'dur', DUR, 'scenes', [(S.id, S.a, S.b) for S in SC], 'sfx', len(SFX), 'captions', len(groups))
