/* ---------- XS: clay cross-section of the plain, north (left) to south (right); 1 unit = 1 km up ---------- */
function xsec() {
  const { el, push } = newScene(); const G = renderer(push); const ov = mk('div', { class: 'ov' }, push); const chars = mk('div', { class: 'chars' }, push);
  G.R.shadowMap.enabled = true;
  const sc = new T3.Scene(); { const c = document.createElement('canvas'); c.width = 4; c.height = 512; const g = c.getContext('2d'); const gr = g.createLinearGradient(0, 0, 0, 512);
    gr.addColorStop(0, '#163a6b'); gr.addColorStop(.55, '#4f86c2'); gr.addColorStop(.75, '#a9c9e8'); gr.addColorStop(1, '#d8c9a8'); g.fillStyle = gr; g.fillRect(0, 0, 4, 512); sc.background = new T3.CanvasTexture(c); }
  sc.fog = new T3.Fog(0x9ab8d8, 110, 220);
  const cam = new T3.PerspectiveCamera(FOV, ASP, .1, 300);
  sc.add(new T3.HemisphereLight(0xeef6ff, 0x3a2a18, .7));
  const sun = new T3.DirectionalLight(0xfff0d0, 1.1); sun.position.set(6, 18, 14); sun.castShadow = true; sun.shadow.bias = -.003; sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -16, right: 16, top: 12, bottom: -10, near: 1, far: 60 }); sc.add(sun);
  const TH = 3.0;
  const ext = (pts, col, opt, depth) => { const s = new T3.Shape(pts.map(p => new T3.Vector2(p[0], p[1]))); const g = new T3.ExtrudeGeometry(s, { depth: depth || TH, bevelEnabled: true, bevelSize: .05, bevelThickness: .05, bevelSegments: 2 });
    g.translate(0, 0, -(depth || TH) / 2); const m = new T3.MeshStandardMaterial(Object.assign({ color: col, roughness: .85 }, opt || {})); const o = new T3.Mesh(g, m); o.castShadow = o.receiveShadow = true; return o; };
  // ground: plain in the middle, the Himalaya + Tibet block on the left, Aravalli / Vindhya hills on the right
  const BOT = -9;
  const plain = ext([[-4.6, BOT], [-4.6, -.2], [5.4, -.2], [5.4, BOT]], 0x6b4a2e); sc.add(plain); sc.add(ext([[-4.6, -.22], [-4.6, .1], [5.4, .1], [5.4, -.22]], 0x6f8a3c));
  const south = ext([[5.2, BOT], [5.2, .1], [5.9, .45], [6.5, .95], [7.1, .55], [7.8, .9], [8.6, .5], [9.6, .7], [11, .45], [11, BOT]], 0x8a6a3c); sc.add(south);
  const him = new T3.Group(); sc.add(him);
  const HP = [[-15, BOT], [-15, 4.6], [-12.5, 4.8], [-10.6, 5.0], [-9.6, 6.9], [-8.9, 5.7], [-8.1, 7.6], [-7.2, 5.2], [-6.5, 6.1], [-5.7, 3.4], [-5.1, 1.6], [-4.7, .5], [-4.5, .1], [-4.5, BOT]];
  him.add(ext(HP, 0x6e5a4a));
  him.add(ext([[-10.1, 5.9], [-9.6, 6.9], [-9.2, 6.3], [-8.6, 6.6], [-8.1, 7.6], [-7.6, 6.4], [-6.9, 5.8], [-6.5, 6.1], [-6.2, 5.3], [-6.8, 5.5], [-7.2, 5.2], [-7.7, 5.9], [-8.1, 6.6], [-8.6, 6.0], [-8.9, 5.7], [-9.5, 6.1]], 0xf4f8ff, { roughness: .6 }, TH + .12));
  him.position.y = 0; him.scale.y = 1;
  // air: summer mixing line, winter warm lid layer, smoke particles, cold air ribbon, wind streaks, pot lid
  const layerMat = new T3.MeshBasicMaterial({ color: 0xff9a3c, transparent: true, opacity: 0, depthWrite: false });
  const layer = new T3.Mesh(new T3.BoxGeometry(10.2, .32, TH + .2), layerMat); layer.position.set(.4, 1, 0); sc.add(layer);
  const lineMat = new T3.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0, depthWrite: false });
  const mline = new T3.Mesh(new T3.BoxGeometry(10.2, .035, .035), lineMat); mline.position.set(.4, 1, TH / 2 + .05); sc.add(mline);
  const nP = 900, pp = new Float32Array(nP * 3), ps = new Float32Array(nP * 3);
  for (let i = 0; i < nP; i++) { pp.set([-4.3 + ((i * .618) % 1) * 9.5, .1, -TH / 2 + ((i * .754) % 1) * TH], i * 3); ps.set([(i * .3819) % 1, (i * .917) % 1, (i * .123) % 1], i * 3); }
  const pg = new T3.BufferGeometry(); pg.setAttribute('position', new T3.BufferAttribute(pp, 3)); pg.setAttribute('seed', new T3.BufferAttribute(ps, 3));
  const SU = { time: { value: 0 }, alpha: { value: 0 }, ceil: { value: 1 }, rise: { value: 0 }, glow: { value: GLOW } };
  const smoke = new T3.Points(pg, new T3.ShaderMaterial({ uniforms: SU, transparent: true, depthWrite: false,
    vertexShader: `uniform float time, ceil, rise; attribute vec3 seed; varying float vA; void main(){ vec3 p = position;
      float t = fract(seed.x + time * (0.05 + seed.y * 0.05)); float yr = 0.1 + t * 3.2; float yt = 0.12 + seed.y * ceil * 0.92 + sin(time * 0.7 + seed.z * 30.0) * 0.03;
      p.y = mix(yt, yr, rise); p.x += sin(time * 0.3 + seed.z * 20.0) * 0.12 + rise * t * 1.2; vA = mix(1.0, smoothstep(1.0, 0.55, t), rise);
      vec4 mv = modelViewMatrix * vec4(p, 1.0); gl_Position = projectionMatrix * mv; gl_PointSize = (200.0 + seed.z * 260.0) / -mv.z * 6.0; }`,
    fragmentShader: `uniform float alpha; uniform sampler2D glow; varying float vA; void main(){ float a = texture2D(glow, gl_PointCoord).r; gl_FragColor = vec4(0.55, 0.52, 0.48, a * alpha * 0.32 * vA); }` }));
  smoke.frustumCulled = false; smoke.renderOrder = 4; sc.add(smoke);
  // cold air: a blue ribbon sliding down off the plateau
  const cc = new T3.CatmullRomCurve3([new T3.Vector3(-13.5, 5.9, 0), new T3.Vector3(-10, 6.2, 0), new T3.Vector3(-7.2, 4.6, 0), new T3.Vector3(-5.2, 1.4, 0), new T3.Vector3(-3.2, .5, 0), new T3.Vector3(1.5, .35, 0)]);
  const CU = { prog: { value: 0 }, alpha: { value: 0 }, time: { value: 0 } };
  const cold = new T3.Mesh(new T3.TubeGeometry(cc, 160, .22, 12, false), new T3.ShaderMaterial({ uniforms: CU, transparent: true, depthWrite: false,
    vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `uniform float prog, alpha, time; varying vec2 vUv; void main(){ if (vUv.x > prog) discard; float s = 0.65 + 0.35 * sin(vUv.x * 60.0 - time * 8.0); gl_FragColor = vec4(0.45, 0.8, 1.0, alpha * 0.8 * s * smoothstep(prog, prog - 0.05, vUv.x)); }` }));
  cold.position.z = TH / 2 + .25; sc.add(cold);
  // wind streaks moving left to right across the plain (speed track)
  const nW = 24, wp = new Float32Array(nW * 3), wsd = new Float32Array(nW);
  for (let i = 0; i < nW; i++) { wp.set([0, .25 + ((i * .37) % 1) * .9, -TH / 2 + ((i * .61) % 1) * TH], i * 3); wsd[i] = (i * .618) % 1; }
  const wg = new T3.BufferGeometry(); wg.setAttribute('position', new T3.BufferAttribute(wp, 3)); wg.setAttribute('sd', new T3.BufferAttribute(wsd, 1));
  const WU2 = { off: { value: 0 }, alpha: { value: 0 } };
  const wind = new T3.Points(wg, new T3.ShaderMaterial({ uniforms: WU2, transparent: true, depthWrite: false,
    vertexShader: `uniform float off; attribute float sd; void main(){ vec3 p = position; p.x = -4.2 + fract(sd + off) * 9.4; vec4 mv = modelViewMatrix * vec4(p, 1.0); gl_Position = projectionMatrix * mv; gl_PointSize = 900.0 / -mv.z; }`,
    fragmentShader: `uniform float alpha; void main(){ vec2 q = gl_PointCoord - 0.5; float a = smoothstep(0.5, 0.0, abs(q.x)) * smoothstep(0.06, 0.0, abs(q.y)); gl_FragColor = vec4(1.0, 1.0, 1.0, a * alpha * 0.9); }` }));
  wind.frustumCulled = false; sc.add(wind);
  // pot lid: a flattened dome + knob
  const lid = new T3.Group(); sc.add(lid);
  const lidM = new T3.MeshStandardMaterial({ color: 0xb9c2cc, metalness: .8, roughness: .28, transparent: true, opacity: 0 });
  const dome = new T3.Mesh(new T3.SphereGeometry(1, 64, 24, 0, Math.PI * 2, 0, Math.PI / 2), lidM); dome.scale.set(5.6, .55, 2.1); lid.add(dome);
  const rim = new T3.Mesh(new T3.TorusGeometry(1, .03, 12, 96), lidM); rim.rotation.x = Math.PI / 2; rim.scale.set(5.6, 2.1, 1); lid.add(rim);
  const knob = new T3.Mesh(new T3.SphereGeometry(.32, 32, 16), new T3.MeshStandardMaterial({ color: 0x1b1b1b, roughness: .4, transparent: true, opacity: 0 })); knob.position.y = .62; knob.scale.set(1, .6, 1); lid.add(knob);
  lid.position.set(.4, 1.2, 0);
  const S = { el, push, ov, chars, G, sc, cam, labels: [], wins: [], him, layer, mline, lid, lidM, knob, TH,
    ck: TK({ x: 0, y: 2.5, dist: 30, yaw: 8, pitch: 10 }), himS: TK(1), lineA: TK(0), layerA: TK(0), ceil: TK(1), smokeA: TK(0), rise: TK(0), coldP: TK(0), coldA: TK(0), windA: TK(0), windV: TK(0), lidA: TK(0), lidY: TK(6) };
  S.camAt = t => { const k = valAt(S.ck, t); const y = k.yaw * Math.PI / 180, p = k.pitch * Math.PI / 180; const tg = new T3.Vector3(k.x, k.y, 0);
    cam.position.set(tg.x + Math.sin(y) * Math.cos(p) * k.dist, tg.y + Math.sin(p) * k.dist, Math.cos(y) * Math.cos(p) * k.dist); cam.lookAt(tg); cam.updateMatrixWorld(); };
  S.proj = (t, x, y, z) => { S.camAt(t); return toScreen(cam, new T3.Vector3(x, y, z === undefined ? TH / 2 + .2 : z)); };
  // wind offset = integral of speed (pure function of time: speed is piecewise linear, integrate numerically)
  const windOff = t => { let s = 0, dt = 1 / 30; for (let u = 0; u < t; u += dt) s += valAt(S.windV, u) * dt; return s; };
  S.render = t => { S.camAt(t);
    const hs = valAt(S.himS, t); him.scale.y = Math.max(.05, hs);
    const ce = valAt(S.ceil, t); layer.position.y = ce + .16; mline.position.y = ce; layerMat.opacity = valAt(S.layerA, t) * .55; lineMat.opacity = valAt(S.lineA, t) * .9;
    SU.time.value = t; SU.alpha.value = valAt(S.smokeA, t); SU.ceil.value = ce; SU.rise.value = valAt(S.rise, t);
    CU.prog.value = valAt(S.coldP, t); CU.alpha.value = valAt(S.coldA, t); CU.time.value = t;
    WU2.alpha.value = valAt(S.windA, t); WU2.off.value = windOff(t) * .18;
    const la = valAt(S.lidA, t); lidM.opacity = la; knob.material.opacity = la; lid.visible = la > .01; lid.position.y = valAt(S.lidY, t);
    G.R.render(sc, cam);
    for (const L of S.labels) { const a = valAt(L.a, t); L.e.style.opacity = a; if (a <= 0) continue; const yy = typeof L.y === 'function' ? L.y(t) : L.y; const q = toScreen(cam, new T3.Vector3(L.x, yy, L.z === undefined ? TH / 2 + .2 : L.z));
      L.e.style.transform = `translate(${(q.x - L.e.offsetWidth * (L.ax === undefined ? .5 : L.ax)).toFixed(1)}px,${(q.y - L.e.offsetHeight / 2).toFixed(1)}px) scale(${((.6 + .4 * Math.min(1, a * 1.5)) * (1 + valAt(L.pop, t))).toFixed(3)})`; } };
  return S;
}
function xLabel(S, html, x, y, fs, col, ax) { const e = mk('div', { class: 'plbl' }, S.ov); e.innerHTML = html; Object.assign(e.style, { fontSize: fs + 'px', webkitTextStrokeWidth: (fs * .18) + 'px', color: col || '' });
  const rec = { e, x, y, ax, a: TK(0), pop: TK(0) }; S.labels.push(rec); return rec; }

/* ---------- GA: real NASA satellite plate (DOM) with slow camera, AQI gauge ---------- */
function plate(img, k0) {
  const { el, push } = newScene(); const im = mk('img', { src: 'assets/' + img, style: 'position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;transform-origin:540px 900px' }, push);
  const ov = mk('div', { class: 'ov' }, push); const chars = mk('div', { class: 'chars' }, push);
  const S = { el, push, ov, chars, im, wins: [], k: TK(Object.assign({ s: 1.0, x: 0, y: 0 }, k0 || {})) };
  S.render = t => { const k = valAt(S.k, t); im.style.transform = `translate(${k.x.toFixed(1)}px,${k.y.toFixed(1)}px) scale(${k.s.toFixed(4)})`; };
  S.proj = (t, x, y) => { const k = valAt(S.k, t); return { x: 540 + (x - 540) * k.s + k.x, y: 900 + (y - 900) * k.s + k.y }; };
  return S;
}
function gauge(S) { const g = mk('div', { style: 'position:absolute;left:90px;top:330px;width:900px;height:620px;opacity:0' }, S.ov);
  g.innerHTML = `<svg width="900" height="620" viewBox="0 0 900 620" style="overflow:visible">
    <defs><linearGradient id="gg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2ec27e"/><stop offset=".2" stop-color="#f5d33c"/><stop offset=".4" stop-color="#ff9a1f"/><stop offset=".6" stop-color="#ff4b2b"/><stop offset=".8" stop-color="#b3124a"/><stop offset="1" stop-color="#5a0b3a"/></linearGradient>
    <filter id="gs"><feDropShadow dx="0" dy="14" stdDeviation="12" flood-opacity=".55"/></filter></defs>
    <rect x="20" y="10" width="860" height="760" rx="46" fill="rgba(6,10,18,.86)" stroke="#fff" stroke-opacity=".9" stroke-width="5" filter="url(#gs)"/>
    <path d="M110,470 A340,340 0 0 1 790,470" fill="none" stroke="#1b2433" stroke-width="64" stroke-linecap="round"/>
    <path id="garc" d="M110,470 A340,340 0 0 1 790,470" fill="none" stroke="url(#gg)" stroke-width="64" stroke-linecap="round" stroke-dasharray="1068" stroke-dashoffset="1068"/>
    <g id="gneedle" transform="rotate(-90 450 470)"><path d="M441,470 L450,200 L459,470Z" fill="#fff" stroke="#03101A" stroke-width="5"/><circle cx="450" cy="470" r="30" fill="#fff" stroke="#03101A" stroke-width="6"/></g>
    <text x="96" y="560" font-family="Arch" font-weight="800" font-size="38" fill="#c9d6e6" text-anchor="middle">0</text>
    <g id="gmax"><text x="804" y="560" font-family="BSD" font-weight="900" font-size="64" fill="#FFC23A" text-anchor="middle" stroke="#03101A" stroke-width="10" paint-order="stroke fill">${tr('MAX 500')}</text></g>
    <text x="450" y="120" font-family="Arch" font-weight="800" font-size="40" letter-spacing="6" fill="#c9d6e6" text-anchor="middle">${tr('DELHI · AQI')}</text>
  </svg><div class="gnum" style="position:absolute;left:0;top:540px;width:900px;text-align:center;font-family:BSD;font-weight:900;font-size:190px;color:#fff;paint-order:stroke fill;-webkit-text-stroke:24px #03101A;line-height:1">0</div>`;
  return { g, arc: g.querySelector('#garc'), nd: g.querySelector('#gneedle'), num: g.querySelector('.gnum'), mx: g.querySelector('#gmax') }; }

/* ---------- character drawn in code: the Himalayas (snow-capped range with a face) ---------- */
function himChar(S, cx, cy, sc) {
  const box = mk('div', { class: 'char' }, S.chars); Object.assign(box.style, { left: (cx - 390) + 'px', top: (cy - 390) + 'px', width: '780px', height: '780px' });
  const svg = mk('svg', { width: 780, height: 780, viewBox: '0 0 780 780', style: 'overflow:visible' }, box, true);
  const d = 'M20,560 L95,395 L140,430 L215,240 L265,300 L330,110 L392,265 L440,205 L520,355 L560,330 L640,560 Z';
  const id = 'him' + Math.round(cx);
  const defs = mk('defs', {}, svg, true);
  defs.innerHTML = `<clipPath id="c${id}"><path d="${d}"/></clipPath><linearGradient id="g${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fa3c2"/><stop offset="1" stop-color="#3d4f6e"/></linearGradient>
    <filter id="s${id}" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="22" stdDeviation="14" flood-color="#000" flood-opacity=".5"/></filter>`;
  const body = mk('g', { transform: `translate(${390 - 330 * sc},${390 - 340 * sc}) scale(${sc})`, filter: `url(#s${id})` }, svg, true);
  body.innerHTML = `<path d="${d}" fill="none" stroke="#0b0b0b" stroke-width="34" stroke-linejoin="round"/><path d="${d}" fill="none" stroke="#fff" stroke-width="20" stroke-linejoin="round"/>
    <g clip-path="url(#c${id})"><rect x="0" y="0" width="700" height="700" fill="url(#g${id})"/>
    <path d="M180,320 L215,240 L248,286 L226,300 L262,326 L265,300 L300,190 L330,110 L372,215 L350,226 L384,258 L392,265 L425,225 L440,205 L470,262 L446,256 L430,290 L405,282 L380,300 L355,280 L330,300 L300,282 L275,318 L250,305 L225,330 L205,316Z" fill="#f6fbff"/></g>`;
  const face = mk('g', { transform: 'translate(335,420) scale(.95)' }, body, true);
  const eyes = mk('g', {}, face, true), brows = mk('g', {}, face, true);
  eyes.innerHTML = `<ellipse cx="-62" cy="0" rx="40" ry="34" fill="#fff" stroke="#14203a" stroke-width="7"/><ellipse cx="62" cy="0" rx="40" ry="34" fill="#fff" stroke="#14203a" stroke-width="7"/>
    <circle cx="-56" cy="10" r="16" fill="#14203a"/><circle cx="68" cy="10" r="16" fill="#14203a"/>
    <path d="M-104,-4 Q-62,-22 -20,-4 L-20,-38 L-104,-38Z" fill="#5d6f8f" stroke="#14203a" stroke-width="7"/><path d="M20,-4 Q62,-22 104,-4 L104,-38 L20,-38Z" fill="#5d6f8f" stroke="#14203a" stroke-width="7"/>`;
  brows.innerHTML = `<path d="M-108,-52 Q-62,-70 -18,-48" stroke="#14203a" stroke-width="14" fill="none" stroke-linecap="round"/><path d="M18,-48 Q62,-70 108,-52" stroke="#14203a" stroke-width="14" fill="none" stroke-linecap="round"/>`;
  const mouthO = mk('g', {}, face, true); mouthO.innerHTML = `<path d="M-34,70 Q0,60 34,70 Q28,104 0,106 Q-28,104 -34,70Z" fill="#3a0a10" stroke="#14203a" stroke-width="7"/>`;
  const mouthC = mk('g', {}, face, true); mouthC.innerHTML = `<path d="M-38,80 Q0,96 38,76" stroke="#14203a" stroke-width="12" fill="none" stroke-linecap="round"/>`;
  return { box, eyes, brows, mouthO, mouthC, cx, cy };
}
// 100-city icon grid (illustrative): 10 x 10 dots, n of them turn red
function cityGrid() { const g = mk('div', { style: 'position:absolute;left:190px;top:470px;width:700px;height:700px;opacity:0' }, $('hook'));
  g.innerHTML = `<div style="position:absolute;inset:0;border-radius:40px;background:rgba(6,10,18,.84);border:5px solid #fff;box-shadow:0 18px 40px rgba(0,0,0,.6)"></div>`;
  const dots = []; for (let i = 0; i < 100; i++) { const d = mk('div', {}, g); Object.assign(d.style, { position: 'absolute', left: (62 + (i % 10) * 60) + 'px', top: (150 + Math.floor(i / 10) * 52) + 'px', width: '40px', height: '40px', borderRadius: '50%', background: '#5b6b80', border: '4px solid #03101A' }); dots.push(d); }
  const lab = mk('div', {}, g); Object.assign(lab.style, { position: 'absolute', left: 0, top: '28px', width: '700px', textAlign: 'center', fontFamily: 'BSD', fontWeight: 900, fontSize: '96px', color: '#fff', lineHeight: 1 });
  lab.innerHTML = `<span class="gn" style="color:#FF3B30">0</span> / 100`;
  return { g, dots, n: lab.querySelector('.gn') }; }
function indiaFlagCanvas() { const c = document.createElement('canvas'); c.width = 4096; c.height = 2048; const x = c.getContext('2d');
  const P = (lon, lat) => [(lon + 180) / 360 * 4096, (90 - lat) / 180 * 2048];
  const path = () => { x.beginPath(); for (const r of D.geo.india) r.forEach(([lo, la], i) => { const [px, py] = P(lo, la); i ? x.lineTo(px, py) : x.moveTo(px, py); }); x.closePath(); };
  let y0 = 1e9, y1 = -1e9; for (const r of D.geo.india) for (const [, la] of r) { const py = P(0, la)[1]; y0 = Math.min(y0, py); y1 = Math.max(y1, py); }
  x.save(); path(); x.clip('evenodd'); const h = (y1 - y0) / 3; x.fillStyle = '#FF9933'; x.fillRect(0, y0, 4096, h + 1); x.fillStyle = '#FFFFFF'; x.fillRect(0, y0 + h, 4096, h + 1); x.fillStyle = '#138808'; x.fillRect(0, y0 + 2 * h, 4096, h + 1);
  const [cx, cy] = P(79.5, 22.8); x.strokeStyle = '#000080'; x.lineWidth = 3; x.beginPath(); x.arc(cx, cy, 13, 0, Math.PI * 2); x.stroke(); for (let i = 0; i < 24; i++) { const a = i * Math.PI / 12; x.beginPath(); x.moveTo(cx, cy); x.lineTo(cx + Math.cos(a) * 13, cy + Math.sin(a) * 13); x.lineWidth = 1.2; x.stroke(); }
  x.restore(); path(); x.strokeStyle = '#FFFFFF'; x.lineWidth = 3; x.stroke(); return c; }
