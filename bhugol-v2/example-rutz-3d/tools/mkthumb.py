# New BHUGOL cover (L02) from the video's own GA frame: Russia's 11 zones lit, firework at Kamchatka, sun at Kaliningrad,
# the alarm-clock character as the cut-out joke, 1-4 words with the last word on a yellow box. Usage: mkthumb.py <build_dir> <out_dir> <en|hi>
import sys, os, shutil, re
B, O, L = sys.argv[1:4]; V = sys.argv[4] if len(sys.argv) > 4 else 'q'
if os.path.exists(O): shutil.rmtree(O)
shutil.copytree(B, O, ignore=shutil.ignore_patterns('*.mp4'))
words = {('en', 'q'): ('MIDNIGHT OR', '2 PM?'), ('hi', 'q'): ('आधी रात या', '2 PM?'),
         ('en', 't'): ('RUSSIA GETS<br>NEW YEAR', '11 TIMES?!'), ('hi', 't'): ('रूस में<br>NEW YEAR', '11 बार?!')}[(L, V)]
inj = """
<style>#caps,#titles,#hook,#badgeWrap,#follow,#dim{display:none!important}
.thumbclk{opacity:1!important;transform:none!important}
#thumbtxt{position:absolute;left:0;top:195px;width:1080px;text-align:center;font-family:'BSD','Muk',sans-serif;font-weight:900;line-height:1.02;z-index:50}
#thumbtxt .a{display:inline-block;font-size:__FS__px;color:#fff;paint-order:stroke fill;-webkit-text-stroke:24px #03101A;text-shadow:0 8px 24px rgba(0,0,0,.55)}
#thumbtxt .b{display:inline-block;margin-top:14px;padding:0 34px 6px;font-size:190px;color:#0B0B0B;background:#FFD23F;border:9px solid #fff;border-radius:22px;transform:rotate(-3deg);box-shadow:0 14px 30px rgba(0,0,0,.5)}
.hi #thumbtxt .a{font-size:140px;letter-spacing:0}
#thumbbadge{position:absolute;left:26px;top:26px;width:120px;height:120px;z-index:51}
</style>
<div id="thumbtxt"><div class="a">__A__</div><br><div class="b">__B__</div></div><img id="thumbbadge" src="assets/bhugol_badge.png">
<script>
(function wait(){ if(!(window.__timelines&&window.__timelines.main)) return setTimeout(wait,50);
  for (let i = 1; i < 12; i++) { GA.zA[i].base = 1; GA.zA[i].keys = []; }
  GA.flagA.keys = []; GA.flagA.base = 0; GA.sunLon.keys = []; GA.sunLon.base = 96;
  GA.ck.keys = []; GA.ck.base = __CAM__;
  const fw = GA.fw.find(f => f.o === 12); fw.L.a.keys = []; fw.L.a.base = 1; fw.L.pop.keys = []; fw.L.pop.base = .9;
  const sun = gLabel(GA, '☀️', 21, 54.7, 150); sun.a.base = 1; sun.pop.base = .25;
  const c = GB.cClk; if (__CLK__) GA.chars.appendChild(c.box); c.box.classList.add('thumbclk'); Object.assign(c.box.style, { left: (720 - 390) + 'px', top: (1520 - 390) + 'px' });
  c.box.querySelector('svg').setAttribute('transform', 'rotate(8)');
  document.getElementById('stage').appendChild(document.getElementById('thumbtxt')); document.getElementById('stage').appendChild(document.getElementById('thumbbadge'));
})();
</script>
""".replace('__CAM__', '{ lon: 100, lat: 55, dist: 4.25, tlon: 100, tlat: 52, tr: .3 }').replace('__CLK__', 'false' if V == 't' else 'true').replace('__FS__', '150' if V == 'q' else '128').replace('__A__', words[0]).replace('__B__', words[1])
p = os.path.join(O, 'index.html'); h = open(p).read(); h = h.replace('</body>', inj + '</body>'); open(p, 'w').write(h); print('thumb page', p)
