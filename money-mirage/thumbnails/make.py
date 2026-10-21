import os
V={
 'a':dict(bg='wallet_desk.jpg',pos='62% 50%',filt='contrast(1.12) brightness(.92) saturate(1.05)',extra='<circle cx="990" cy="330" r="235" fill="none" stroke="#E2614B" stroke-width="16"/>'),
 'b':dict(bg='gold_window.jpg',pos='65% 45%',filt='contrast(1.15) brightness(.95) saturate(1.1)',extra=''),
 'c':dict(bg='bank_vault_1700s.jpg',pos='50% 50%',filt='contrast(1.1) brightness(.55) saturate(.9) blur(2px)',extra='COIN'),
}
COIN='''<defs><radialGradient id="cg" cx="42%" cy="36%" r="70%"><stop offset="0" stop-color="#FFE7A6"/><stop offset=".45" stop-color="#EDBB52"/><stop offset="1" stop-color="#B07A1E"/></radialGradient>
<radialGradient id="hl" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#E9B44C" stop-opacity=".6"/><stop offset="1" stop-color="#E9B44C" stop-opacity="0"/></radialGradient>
<linearGradient id="fd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".7"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="mk" maskUnits="userSpaceOnUse" x="0" y="560" width="1920" height="520"><rect x="0" y="560" width="1920" height="420" fill="url(#fd)"/></mask>
<filter id="mr"><feTurbulence type="fractalNoise" baseFrequency="0.004 0.05" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="30" xChannelSelector="R" yChannelSelector="G"/></filter></defs>
<circle cx="1370" cy="400" r="420" fill="url(#hl)"/>
<clipPath id="ab"><rect x="0" y="0" width="1920" height="560"/></clipPath><clipPath id="be"><rect x="0" y="560" width="1920" height="520"/></clipPath>
<g clip-path="url(#ab)"><circle cx="1370" cy="400" r="230" fill="url(#cg)"/><circle cx="1370" cy="400" r="196" fill="none" stroke="#A8711A" stroke-width="6" opacity=".55"/></g>
<g clip-path="url(#be)"><g mask="url(#mk)"><g filter="url(#mr)"><g transform="translate(0,1120) scale(1,-1)"><circle cx="1370" cy="400" r="230" fill="url(#cg)"/></g></g></g>
<rect x="1130" y="590" width="480" height="5" fill="#0B1324"/><rect x="1130" y="640" width="480" height="7" fill="#0B1324"/><rect x="1130" y="700" width="480" height="9" fill="#0B1324"/><rect x="1130" y="770" width="480" height="11" fill="#0B1324"/></g>
<rect x="960" y="558" width="820" height="4" fill="#F3EBDD" opacity=".8"/>'''
for k,v in V.items():
    extra=COIN if v['extra']=='COIN' else v['extra']
    html=f'''<!doctype html><html><head><meta charset="UTF-8"><script src="./gsap.min.js"></script><style>
@font-face{{font-family:Brico;font-weight:800;src:url(assets/brico800.woff2)}}
body{{margin:0;background:#000}}#root{{position:relative;width:1920px;height:1080px;overflow:hidden;background:#0A1120}}
.bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{v['pos']};filter:{v['filt']}}}
.shade{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(6,10,20,.92) 0%,rgba(6,10,20,.75) 34%,rgba(6,10,20,.1) 62%,rgba(6,10,20,0) 100%),linear-gradient(0deg,rgba(6,10,20,.55),rgba(6,10,20,0) 40%)}}
.t{{position:absolute;left:96px;top:150px;font:800 230px/0.9 Brico;letter-spacing:-4px;color:#F3EBDD;text-shadow:0 10px 0 rgba(0,0,0,.55),0 0 60px rgba(0,0,0,.6)}}
.t .g{{color:#E9B44C;font-size:300px}}
.bug{{position:absolute;right:56px;bottom:40px;font:800 44px Brico;letter-spacing:4px;color:#E9B44C;opacity:.9}}.bug span{{color:#F3EBDD}}
svg{{position:absolute;left:0;top:0}}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-width="1920" data-height="1080" data-duration="1">
<img class="bg" src="assets/{v['bg']}"><div class="shade"></div>
<svg width="1920" height="1080" viewBox="0 0 1920 1080">{extra}</svg>
<div class="t">IT'S<br><span class="g">NOT</span><br>GOLD</div>
<div class="bug">MONEY <span>MIRAGE</span></div></div>
<script>document.fonts.ready.then(()=>{{window.__timelines=window.__timelines||{{}};window.__timelines.main=gsap.timeline({{paused:true}}).to({{}},{{duration:1}});}});</script></body></html>'''
    open(f'v{k}/index.html','w').write(html)
print('ok')
