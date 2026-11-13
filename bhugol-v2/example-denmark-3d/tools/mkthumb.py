# New BHUGOL cover (L02) as a frame of the video, two concepts:
#   b = the joke: Skagen's tower poking out of the sand, the deadpan dune beside it, "WHERE'S THE CHURCH?"
#   a = map-led (thumbnail study): Denmark in its flag on the satellite map, a cactus cut-out on Skagen ringed in red, "IN EUROPE?!"
# Usage: mkthumb.py <build_dir> <out_dir> <en|hi> <a|b>   -> then `hyperframes snapshot <out_dir> --at T`
import sys, os, shutil
B, O, L, V = sys.argv[1:5]
if os.path.exists(O): shutil.rmtree(O)
shutil.copytree(B, O, ignore=shutil.ignore_patterns('*.mp4', '.hyperframes', 'node_modules'))
words = {('en', 'b'): ('A DESERT IN', 'EUROPE?!'), ('hi', 'b'): ('EUROPE में', 'रेगिस्तान?!'),
         ('en', 'a'): ('A DESERT IN', 'EUROPE?!'), ('hi', 'a'): ('EUROPE में', 'रेगिस्तान?!')}[(L, V)]
css = """
<style>#caps,#titles,#hook,#badgeWrap,#follow,#dim,#flash{display:none!important}
.thumbchar{opacity:1!important;transform:none!important}
#thumbtxt{position:absolute;left:0;top:150px;width:1080px;text-align:center;font-family:'BSD','Muk',sans-serif;font-weight:900;line-height:1.02;z-index:50}
#thumbtxt .a{display:inline-block;font-size:150px;color:#fff;paint-order:stroke fill;-webkit-text-stroke:24px #03101A;text-shadow:0 8px 24px rgba(0,0,0,.55)}
#thumbtxt .b{display:inline-block;margin-top:14px;padding:0 34px 6px;font-size:200px;color:#0B0B0B;background:#FFD23F;border:9px solid #fff;border-radius:22px;transform:rotate(-3deg);box-shadow:0 14px 30px rgba(0,0,0,.5)}
.hi #thumbtxt .a{letter-spacing:0}
#thumbbadge{position:absolute;left:26px;top:26px;width:120px;height:120px;z-index:51}
#stage .push{transform:none!important}
#scenes{filter:saturate(1.35) contrast(1.06) brightness(1.05)}
#thumbring{position:absolute;left:0;top:0;z-index:40;overflow:visible}
</style>
<div id="thumbtxt"><div class="a">__A__</div><br><div class="b">__B__</div></div><img id="thumbbadge" src="assets/bhugol_badge.png">
<svg id="thumbring" width="1080" height="1920"></svg>
"""
js_b = """
  const fix = (T, v) => { T.keys = []; T.base = v; T.last = v; };
  fix(CH.lvl, .66); fix(CH.sink, 1); fix(CH.pit, 0); fix(CH.ck, { x: -2.1, y: 2.05, z: 0, dist: 13.5, yaw: 20, pitch: 6 });
  for (const L of CH.labels) { fix(L.a, 0); }
  const c = CH.cDune; c.box.classList.add('thumbchar'); Object.assign(c.box.style, { left: (730 - 390) + 'px', top: (1480 - 390) + 'px' }); c.box.querySelector('svg').setAttribute('transform', 'scale(1.1)');
  const q = CH.proj(0, -2.55, 2.45, 0); ring(q.x, q.y, 200, 250);
  window.__THUMB_T = 0;
"""
js_a = """
  const fix = (T, v) => { T.keys = []; T.base = v; T.last = v; };
  fix(MW.flagA, 1); fix(MW.x, 1); fix(MW.rise, 1); fix(MW.pinA, 0); fix(MW.sandA, 0); fix(MW.rainA, 0);
  fix(MW.tk, { lon: 10.3, lat: 56.75, dist: 8.0, el: 84, yaw: 0 });
  for (const L of MW.lls) fix(L.a, 0);
  const cac = mapLabel(MW, '🌵', 10.42, 57.62, 270); fix(cac.a, 1); fix(cac.pop, .15);
  const q = MW.proj(1, 10.42, 57.62); ring(q.x, q.y, 190, 210);
  window.__THUMB_T = 2.9;
"""
inj = css.replace('__A__', words[0]).replace('__B__', words[1]) + """
<script>
function ring(cx, cy, rx, ry) { const s = document.getElementById('thumbring'); let d = '';
  for (let i = 0; i <= 64; i++) { const a = -2.2 + i / 64 * Math.PI * 2.15, r = 1 + .04 * Math.sin(i * .9); d += (i ? 'L' : 'M') + (cx + Math.cos(a) * rx * r).toFixed(1) + ' ' + (cy + Math.sin(a) * ry * r).toFixed(1); }
  s.innerHTML = `<path d="${d}" fill="none" stroke="#03101A" stroke-width="30" stroke-linecap="round" stroke-linejoin="round" opacity=".35"/><path d="${d}" fill="none" stroke="#FF2D2D" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>`; }
(function wait(){ if(!(window.__timelines&&window.__timelines.main)) return setTimeout(wait,50);
""" + (js_b if V == 'b' else js_a) + """
  document.getElementById('stage').appendChild(document.getElementById('thumbring'));
  document.getElementById('stage').appendChild(document.getElementById('thumbtxt')); document.getElementById('stage').appendChild(document.getElementById('thumbbadge'));
})();
</script>
"""
p = os.path.join(O, 'index.html'); h = open(p).read(); h = h.replace('</body>', inj + '</body>'); open(p, 'w').write(h); print('thumb page', p, 'snapshot at', 54.5 if V == 'b' else 2.9)
