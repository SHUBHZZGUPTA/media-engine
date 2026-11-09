
/* ================= BUDAPEST WATER: per-video scenes ================= */
/* Two terrain-map instances (real NASA imagery + AWS terrain) and two views of an engine-drawn cutaway block of the real
   Buda Hills (top = real elevation + Landsat; front = a drawn geological section). No generated art. */
const MP = map3(); MP.cards = []; MP.pre = [];
const MQ = map3(); MQ.cards = []; MQ.pre = [];
for (const S of [MP, MQ]) S.pre.push((t, k) => { S.pin.scale.setScalar(clamp(k.dist / 5, .04, 1.0)); S.ring.visible = S.beam.visible = k.dist > 2; });
function mapDot(S, lon, lat, col, size) { const sp = new T3.Sprite(new T3.SpriteMaterial({ map: GLOW, color: col, transparent: true, blending: T3.AdditiveBlending, depthWrite: false, opacity: 0 }));
  sp.material.depthTest = false; S.st.add(sp); const rec = { sp, lon, lat, a: Track(0), size: size || .05 }; (S.dots = S.dots || []).push(rec);
  S.pre.push((t, k) => { const a = valAt(rec.a, t); sp.material.opacity = a; sp.position.copy(S.wpos(lon, lat, .002)); const s = rec.size * k.dist * (1 + .12 * Math.sin(t * 7 + lon * 50)); sp.scale.set(s, s, 1); });
  return rec; }

/* ---------- cutaway block ---------- */
const BKD = D.block; const [K0, K1, KB0, KB1] = BKD.bbox;
const BLW = 2.0, BLD = BLW * (KB1 - KB0) / ((K1 - K0) * Math.cos((KB0 + KB1) / 2 * Math.PI / 180)), HZ = .30, BOT = -1.05;
const WVS = `attribute float fu; attribute float ftop; varying float vU; varying float vY; varying float vTop;
void main(){ vU = fu; vTop = ftop; vY = position.y; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`;
const WFS = `uniform sampler2D noiseT; uniform float time, feat, faultA, rainP, hotP, caveP, waterA, growA, resA, heatA, side;
varying float vU; varying float vY; varying float vTop;
float seg(vec2 p, vec2 a, vec2 b, out float h){ vec2 pa = p - a, ba = b - a; h = clamp(dot(pa, ba) / dot(ba, ba), 0.0, 1.0); return length(pa - ba * h); }
float cavef(vec2 p){ float f = 0.0;
  f += exp(-dot(p - vec2(1.24, -0.03), p - vec2(1.24, -0.03)) / 0.0031);
  f += exp(-dot(p - vec2(1.32, -0.11), p - vec2(1.32, -0.11)) / 0.0029);
  f += exp(-dot(p - vec2(1.20, -0.18), p - vec2(1.20, -0.18)) / 0.0031);
  f += exp(-dot(p - vec2(1.36, -0.21), p - vec2(1.36, -0.21)) / 0.0029);
  f += exp(-dot(p - vec2(1.28, -0.27), p - vec2(1.28, -0.27)) / 0.0026);
  f += exp(-dot(p - vec2(1.14, -0.07), p - vec2(1.14, -0.07)) / 0.0020);
  f += exp(-dot(p - vec2(1.40, -0.09), p - vec2(1.40, -0.09)) / 0.0016);
  return f; }
void main(){
  vec2 p = vec2(vU * 2.0, vY); float d = vTop - vY;
  float n = texture2D(noiseT, vec2(vU * 3.0 + side * 0.37, vY * 1.3)).r; float n2 = texture2D(noiseT, vec2(vU * 11.0, vY * 7.0)).r;
  float yy = vY + 0.05 * sin(vU * 9.0 + side) + 0.05 * (n - 0.5);
  vec3 lime = vec3(0.88, 0.80, 0.62), dolo = vec3(0.70, 0.63, 0.54), deep = vec3(0.42, 0.34, 0.30), soil = vec3(0.34, 0.30, 0.19);
  vec3 c = yy > -0.30 ? lime : (yy > -0.64 ? dolo : deep);
  c = mix(c, mix(lime, dolo, 0.5), smoothstep(0.03, 0.0, abs(yy + 0.30)) * 0.6);
  c *= 0.93 + 0.07 * sin(yy * 70.0 + n2 * 2.0);
  c *= 0.86 + 0.28 * n;
  c = mix(c, soil, smoothstep(0.028, 0.004, d));
  c = mix(c, vec3(1.0, 0.42, 0.10), heatA * smoothstep(-0.25, -1.05, vY) * 0.85);
  c += resA * vec3(1.0, 0.48, 0.12) * smoothstep(-0.50, -1.0, vY) * (0.75 + 0.25 * sin(time * 3.0 + vU * 12.0));
  if (feat > 0.5) {
    float fx = 0.68 + vY * 0.06; float fd = abs(vU - fx) * 2.0;
    c = mix(c, vec3(0.22, 0.10, 0.07), smoothstep(0.010, 0.004, fd) * 0.85);
    c += faultA * vec3(0.9, 0.36, 0.06) * smoothstep(0.014, 0.0, fd) * (0.55 + 0.30 * sin(time * 6.0 - vY * 24.0));
    float f = cavef(p) + (n2 - 0.5) * 0.18; float th = 1.25 - caveP * 0.95;
    float cv = smoothstep(th, th + 0.05, f) * step(0.02, caveP);
    float wl = smoothstep(-0.035, -0.06, vY);
    vec3 wat = vec3(0.10, 0.72, 0.86) * (0.85 + 0.15 * sin(time * 2.2 + vY * 50.0 + vU * 30.0));
    float deepIn = smoothstep(th, th + 0.45, f);
    vec3 voidC = mix(vec3(0.36, 0.27, 0.19), vec3(0.10, 0.075, 0.06), deepIn);
    vec3 cc = mix(voidC, wat * mix(1.15, 0.8, deepIn), waterA * wl);
    c = mix(c, cc, cv);
    c = mix(c, vec3(0.97, 0.90, 0.74), smoothstep(0.035, 0.0, abs(f - th)) * step(0.02, caveP) * 0.55);
    c += growA * vec3(1.0, 0.62, 0.20) * smoothstep(0.06, 0.0, abs(f - th)) * step(0.02, caveP) * (0.55 + 0.45 * sin(time * 5.0));
    for (int k = 0; k < 3; k++) { float o = float(k);
      vec2 A = vec2(0.56 + o * 0.08, 0.20 - o * 0.02), B = vec2(0.70 + o * 0.08, -0.80 - o * 0.05), Cq = vec2(1.24 - o * 0.03, -0.92 - o * 0.04), Dq = vec2(1.36 - o * 0.02, 0.04);
      float h1, h2, h3; float d1 = seg(p, A, B, h1), d2 = seg(p, B, Cq, h2), d3 = seg(p, Cq, Dq, h3);
      float L1 = length(B - A), L2 = length(Cq - B), L3 = length(Dq - Cq);
      float s1 = h1 * L1, s2 = L1 + h2 * L2, s3 = L1 + L2 + h3 * L3; float tot12 = L1 + L2;
      float w = 0.007;
      float m1 = smoothstep(w, w * 0.4, d1) * step(s1, rainP * tot12);
      float m2 = smoothstep(w, w * 0.4, d2) * step(s2, rainP * tot12);
      float m3 = smoothstep(w, w * 0.4, d3) * step(h3, hotP);
      float dash1 = step(0.45, fract(s1 * 7.0 - time * 1.1)), dash2 = step(0.45, fract(s2 * 7.0 - time * 1.1)), dash3 = step(0.45, fract(s3 * 7.0 - time * 1.4));
      vec3 blue = vec3(0.30, 0.70, 1.0), hot = vec3(1.0, 0.50, 0.12);
      c = mix(c, blue * 1.25, m1 * mix(0.55, 1.0, dash1));
      c = mix(c, mix(blue, hot, h2) * 1.25, m2 * mix(0.55, 1.0, dash2));
      c = mix(c, hot * 1.35, m3 * mix(0.55, 1.0, dash3)); }
  }
  gl_FragColor = vec4(c, 1.0); }`;
const TVS = `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`;
const TFS = `uniform sampler2D top, hs; uniform float glowCity, time, sat; varying vec2 vUv;
void main(){ vec3 c = texture2D(top, vUv).rgb; float h = texture2D(hs, vUv).r; c *= 0.75 + 0.6 * h;
  float lu = dot(c, vec3(0.299, 0.587, 0.114)); c = mix(vec3(lu), c, sat);
  c += glowCity * vec3(1.0, 0.55, 0.18) * (0.35 + 0.15 * sin(time * 3.0 + vUv.x * 20.0));
  gl_FragColor = vec4(c, 1.0); }`;
const bx = lon => (lon - K0) / (K1 - K0) * BLW - BLW / 2;
const bz = lat => BLD / 2 - (lat - KB0) / (KB1 - KB0) * BLD;
function block3() {
  const el = mk('div', { class: 'scene' }, $('scenes')); const push = mk('div', { class: 'push' }, el);
  const cv = mk('canvas', { width: 1080, height: 1920, class: 'cv' }, push); const ov = mk('div', { class: 'ov' }, push);
  const R = new T3.WebGLRenderer({ canvas: cv, antialias: true, preserveDrawingBuffer: true }); R.setPixelRatio(1); R.setSize(1080, 1920, false);
  const sc = new T3.Scene(); sc.background = new T3.Color(0x0E1C3C);
  const cam = new T3.PerspectiveCamera(30, ASP, .01, 50); sc.add(cam);
  const WU = { noiseT: { value: null }, time: { value: 0 }, feat: { value: 1 }, faultA: { value: 0 }, rainP: { value: 0 }, hotP: { value: 0 }, caveP: { value: 0 }, waterA: { value: 0 },
    growA: { value: 0 }, resA: { value: 0 }, heatA: { value: 0 }, side: { value: 0 } };
  const TU = { top: { value: null }, hs: { value: null }, dem: { value: null }, glowCity: { value: 0 }, time: { value: 0 }, sat: { value: 1.1 } };
  /* walls: an edge polyline (x, z, top-y, u) down to BOT */
  const wall = (pts, front, sideK) => { const N = pts.length, M = 40, pos = [], fu = [], ft = [], idx = [];
    for (let i = 0; i < N; i++) for (let j = 0; j <= M; j++) { const [x, ty, z, u] = pts[i]; const y = ty + (BOT - ty) * j / M; pos.push(x, y, z); fu.push(u); ft.push(ty); }
    for (let i = 0; i < N - 1; i++) for (let j = 0; j < M; j++) { const a = i * (M + 1) + j, b = a + M + 1; idx.push(a, b, a + 1, b, b + 1, a + 1); }
    const g = new T3.BufferGeometry(); g.setAttribute('position', new T3.Float32BufferAttribute(pos, 3)); g.setAttribute('fu', new T3.Float32BufferAttribute(fu, 1)); g.setAttribute('ftop', new T3.Float32BufferAttribute(ft, 1)); g.setIndex(idx);
    const U = Object.assign({}, WU, { feat: { value: front ? 1 : 0 }, side: { value: sideK || 0 } });
    const m = new T3.Mesh(g, new T3.ShaderMaterial({ uniforms: U, vertexShader: WVS, fragmentShader: WFS, side: T3.DoubleSide })); sc.add(m); return m; };
  /* one consistent solid: heights for the top grid AND the four walls come from the same CPU-sampled DEM */
  const NX = 300, NZ = 66;
  const build = I => { const H = (u, v) => sampleCPU(I, u, v) * HZ;
    const edge = (n, f) => Array.from({ length: n }, (_, i) => f(i / (n - 1)));
    wall(edge(NX, u => [u * BLW - BLW / 2, H(u, 0), BLD / 2, u]), true);
    wall(edge(NZ, v => [-BLW / 2, H(0, v), BLD / 2 - v * BLD, v * .3]), false, 1);
    wall(edge(NZ, v => [BLW / 2, H(1, v), BLD / 2 - v * BLD, .7 + v * .3]), false, 2);
    wall(edge(NX, u => [u * BLW - BLW / 2, H(u, 1), -BLD / 2, u]), false, 3);
    const pos = [], uv = [], idx = [];
    for (let j = 0; j < NZ; j++) for (let i = 0; i < NX; i++) { const u = i / (NX - 1), v = j / (NZ - 1); pos.push(u * BLW - BLW / 2, H(u, v), BLD / 2 - v * BLD); uv.push(u, v); }
    for (let j = 0; j < NZ - 1; j++) for (let i = 0; i < NX - 1; i++) { const a = j * NX + i, b2 = a + NX; idx.push(a, a + 1, b2, a + 1, b2 + 1, b2); }
    const tg = new T3.BufferGeometry(); tg.setAttribute('position', new T3.Float32BufferAttribute(pos, 3)); tg.setAttribute('uv', new T3.Float32BufferAttribute(uv, 2)); tg.setIndex(idx);
    sc.add(new T3.Mesh(tg, new T3.ShaderMaterial({ uniforms: TU, vertexShader: TVS, fragmentShader: TFS, side: T3.DoubleSide }))); };
  /* a thin dark base slab so the block reads as a model */
  const base = new T3.Mesh(new T3.BoxGeometry(BLW * 1.04, .04, BLD * 1.12), new T3.MeshBasicMaterial({ color: 0x0A1428 })); base.position.y = BOT - .02; sc.add(base);
  const S = { el, push, cv, ov, R, sc, cam, WU, TU, uT: {}, cam0: Track({ x: 0, y: 0, z: 0, dist: 3.4, yaw: 0, pitch: 14 }), parts: [], glows: [], labels: [], hooks: [], emos: [], demI: null };
  READY.push(tex('noise.png', { repeat: 1 }).then(t => WU.noiseT.value = t), tex('blk_top.jpg').then(t => TU.top.value = t), tex('blk_hs.png').then(t => TU.hs.value = t),
    cpuImg('blk_dem.png').then(I => { S.demI = I; build(I); }));
  return S; }
const bTop = (S, lon, lat) => S.demI ? sampleCPU(S.demI, (lon - K0) / (K1 - K0), (lat - KB0) / (KB1 - KB0)) * HZ : 0;
/* surface point (lon, lat) or front-face point {u, y} -> world */
const bWorld = (S, q, lift) => q.u !== undefined ? new T3.Vector3(q.u * BLW - BLW / 2, q.y, BLD / 2 + .004) : new T3.Vector3(bx(q.lon), bTop(S, q.lon, q.lat) + (lift || .01), bz(q.lat));
function setBCam(S, s) { const yw = s.yaw * Math.PI / 180, pt = s.pitch * Math.PI / 180; const T = new T3.Vector3(s.x, s.y, s.z);
  S.cam.position.set(T.x + Math.sin(yw) * Math.cos(pt) * s.dist, T.y + Math.sin(pt) * s.dist, T.z + Math.cos(yw) * Math.cos(pt) * s.dist); S.cam.lookAt(T); S.cam.updateMatrixWorld(); }
const PWV = `uniform float time, rise, sizeK, drift; attribute vec3 seed; varying float vA; varying float vS;
void main(){ float t = fract(seed.x + time * seed.y); vec3 p = position; p.y += t * rise; p.x += sin(t * 6.0 + seed.z * 30.0) * drift * t;
  vec4 mv = modelViewMatrix * vec4(p, 1.0); gl_Position = projectionMatrix * mv; gl_PointSize = sizeK * (0.5 + t * 1.6) / -mv.z; vA = sin(t * 3.14159); vS = seed.z; }`;
function wparts(S, pts, o) { const n = pts.length, pos = new Float32Array(n * 3), sd = new Float32Array(n * 3);
  pts.forEach((q, i) => { pos.set([q.x, q.y, q.z], i * 3); sd.set([(i * 0.3819) % 1, (o.speed || .2) * (.7 + ((i * 0.917) % 1) * .6), (i * 0.1234) % 1], i * 3); });
  const g = new T3.BufferGeometry(); g.setAttribute('position', new T3.BufferAttribute(pos, 3)); g.setAttribute('seed', new T3.BufferAttribute(sd, 3));
  const U = { time: { value: 0 }, rise: { value: o.rise || .3 }, sizeK: { value: o.size || 200 }, drift: { value: o.drift || .03 }, col: { value: new T3.Color(o.col || 0xEEF2F6) }, alpha: { value: 0 }, flick: { value: o.flick || 0 } };
  const Pp = new T3.Points(g, new T3.ShaderMaterial({ uniforms: U, vertexShader: PWV, fragmentShader: PFS, transparent: true, depthWrite: false, blending: o.add ? T3.AdditiveBlending : T3.NormalBlending }));
  Pp.frustumCulled = false; S.sc.add(Pp); const rec = { U, a: Track(0) }; S.parts.push(rec); return rec; }
function bGlow(S, q, size, col) { const sp = new T3.Sprite(new T3.SpriteMaterial({ map: GLOW, color: col, transparent: true, blending: T3.AdditiveBlending, depthWrite: false, opacity: 0 }));
  S.sc.add(sp); const rec = { sp, q, size, a: Track(0), path: null }; S.glows.push(rec); return rec; }
function bLabel(S, txt, q, fs, col) { const e = mk('div', { class: 'plbl' }, S.ov); e.textContent = tr(txt); Object.assign(e.style, { fontSize: fs + 'px', webkitTextStrokeWidth: (fs * .18) + 'px', color: col || '' });
  const rec = { e, q, a: Track(0) }; S.labels.push(rec); return rec; }
function bEmo(S, ch, q, fs, dy) { const e = mk('div', { class: 'emo' }, S.ov); const inner = mk('span', { style: 'display:inline-block' }, e); inner.textContent = ch; e.style.fontSize = (fs || 150) + 'px'; const rec = { e, inner, q, a: Track(0), dy: dy || 0 }; S.emos.push(rec); return rec; }
function renderBlock(S, t) {
  const s = valAt(S.cam0, t); setBCam(S, s); S.WU.time.value = t; S.TU.time.value = t;
  for (const k in S.uT) { const v = valAt(S.uT[k], t); if (k in S.WU) S.WU[k].value = v; else if (k in S.TU) S.TU[k].value = v; }
  S.sc.traverse(o => { if (o.material && o.material.uniforms && o.material.uniforms.feat) for (const k in S.WU) if (k !== 'feat' && k !== 'side') o.material.uniforms[k].value = S.WU[k].value; });
  for (const p of S.parts) { p.U.time.value = t; p.U.alpha.value = valAt(p.a, t); }
  for (const g of S.glows) { const a = valAt(g.a, t); g.sp.material.opacity = a; g.sp.position.copy(g.path ? g.path(t) : bWorld(S, g.q, .02)); const z = g.size * (1 + .08 * Math.sin(t * 8 + g.size * 40)); g.sp.scale.set(z, z, 1); }
  for (const h of S.hooks) h(t);
  S.R.render(S.sc, S.cam);
  for (const L of S.labels) { const a = valAt(L.a, t); L.e.style.opacity = a; if (a <= 0) continue; const q = toScreen(S.cam, bWorld(S, L.q, .03));
    L.e.style.transform = `translate(${(q.x - L.e.offsetWidth / 2).toFixed(1)}px,${(q.y - L.e.offsetHeight / 2).toFixed(1)}px) scale(${(.6 + .4 * Math.min(1, a * 1.5)).toFixed(3)})`; }
  for (const E of S.emos) { const a = valAt(E.a, t); E.e.style.opacity = Math.min(1, a); if (a <= 0) continue; const q = toScreen(S.cam, bWorld(S, E.q, .03));
    E.e.style.transform = `translate(${(q.x - E.e.offsetWidth / 2).toFixed(1)}px,${(q.y - E.e.offsetHeight / 2 + E.dy).toFixed(1)}px) scale(${(.3 + .7 * Math.min(1, a)).toFixed(3)})`; } }
const bProj = (S, q, t) => { setBCam(S, valAt(S.cam0, t)); return toScreen(S.cam, bWorld(S, q, .02)); };

const XS = block3();   /* the section: rain, heat, fault, caves forming, payoff glow */
const CV = block3();   /* close on Rozsadomb: door, flooded cave, divers, fossils, growing edge */
const BLOCKS = [XS, CV];
/* steam over the springs line (hill foot by the Danube) */
for (const S of BLOCKS) { const pts = []; for (let i = 0; i < 26; i++) { const u = .66 + ((i * .618) % 1) * .1, z = BLD / 2 - ((i * .7548) % 1) * BLD * .8; pts.push({ x: u * BLW - BLW / 2, y: .06, z }); }
  S.steam = wparts(S, pts, { rise: .22, size: 150, col: 0xEEF2F6, speed: .12, drift: .04 }); }
/* camera-attached 3D thermometer (CV) */
lights(CV);
{ const g = new T3.Group(); CV.cam.add(g); g.position.copy(viewPos(880, 700, 1.3)); g.rotation.y = -.35;
  const glass = new T3.Mesh(new T3.CylinderGeometry(.075, .075, 1.3, 40), new T3.MeshStandardMaterial({ color: 0xF4F8FB, roughness: .15, metalness: .05, transparent: true, opacity: .3, depthWrite: false }));
  const cap = new T3.Mesh(new T3.SphereGeometry(.075, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2), glass.material); cap.position.y = .65;
  const bulb = new T3.Mesh(new T3.SphereGeometry(.16, 40, 24), new T3.MeshStandardMaterial({ color: 0xFF3B30, emissive: 0x8A1408, roughness: .3 })); bulb.position.y = -.72;
  const mg = new T3.CylinderGeometry(.045, .045, 1, 24); mg.translate(0, .5, 0); const merc = new T3.Mesh(mg, bulb.material); merc.position.y = -.68;
  const ticks = new T3.Group(); for (let i = 0; i < 9; i++) { const tk = new T3.Mesh(new T3.BoxGeometry(i % 2 ? .05 : .09, .012, .01), new T3.MeshStandardMaterial({ color: 0x03101A })); tk.position.set(.1, -.5 + i * .13, .02); ticks.add(tk); }
  g.add(glass, cap, bulb, merc, ticks); g.visible = false; CV.thermo = { g, merc, a: Track(0), lvl: Track(.05), spin: Track(-.35) };
  const e = mk('div', { class: 'plbl' }, CV.ov); e.innerHTML = '+1°C / <span>0</span> m'; Object.assign(e.style, { fontSize: '120px', webkitTextStrokeWidth: '20px', color: '#FFC23A' }); CV.thermoLbl = e; CV.lblA = Track(0);
  CV.hooks.push(t => { const a = valAt(CV.thermo.a, t); g.visible = a > 0; g.scale.setScalar(.15 * (.6 + .4 * Math.min(1, a))); CV.thermo.merc.scale.y = Math.max(.02, valAt(CV.thermo.lvl, t) * 1.25); g.rotation.y = valAt(CV.thermo.spin, t) + Math.sin(t * .8) * .06;
    const la = valAt(CV.lblA, t); e.style.opacity = la; if (la > 0) { const tp = new T3.Vector3(0, 1.0, 0); g.localToWorld(tp); const q = toScreen(CV.cam, tp);
      e.style.transform = `translate(${(540 - e.offsetWidth / 2).toFixed(1)}px,250px) scale(${(.6 + .4 * la).toFixed(3)})`; } }); }
/* the diver's torch: a light moving through the flooded passages (front face) */
CV.diver = bGlow(CV, { u: .66, y: -.12 }, .07, 0xBFF6FF);
CV.diver.path = t => { const k = (t * .16) % 1, pts = [[.60, -.17], [.66, -.11], [.68, -.20], [.64, -.27], [.60, -.17]]; const s = k * 4, i = Math.floor(s), f = s - i, a = pts[i], b = pts[i + 1];
  return new T3.Vector3((a[0] + (b[0] - a[0]) * f) * BLW - BLW / 2, a[1] + (b[1] - a[1]) * f, BLD / 2 + .01); };

/* emoji */
const emo = (ch, x, y, fs) => { const e = mk('div', { class: 'emo' }, $('fx')); e.textContent = ch; Object.assign(e.style, { left: x + 'px', top: y + 'px', fontSize: (fs || 200) + 'px' }); return e; };
const eSpa = emo('♨️', 760, 560, 190), eSnail = emo('🐌', 700, 640, 200);
const SC = { MP, MQ, XS, CV };
function mkCard(S, b) { const el = mk('div', { class: 'card' }, S.ov);
  el.innerHTML = `<div class="cin"><div class="crow"><span class="cflag">${b.flag || ''}</span><span>${b.name || ''}</span></div><div class="cbig"><span class="cnum">0</span><span class="csuf">${b.unit || ''}</span></div>${b.tag ? `<div class="ctag">${b.tag}</div>` : ''}</div>`;
  const svg = mk('svg', { width: 1080, height: 1920, style: 'position:absolute;left:0;top:0;overflow:visible;opacity:0' }, S.ov, true); S.ov.insertBefore(svg, el);
  const path = mk('path', { stroke: '#FF7A1A', 'stroke-width': 6, 'stroke-dasharray': '14 10', fill: 'none' }, svg, true);
  const c = { el, ln: svg, path, a: Track(0), num: el.querySelector('.cnum'), suf: el.querySelector('.csuf') }; S.cards.push(c); return c; }
