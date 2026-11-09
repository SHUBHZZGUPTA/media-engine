
/* ================= DANUBE: per-video scenes ================= */
/* Three terrain-map instances (real NASA imagery + AWS terrain): two wide Europe views (MW, MV) and one close view of the
   sinkhole country (MI); plus an engine-drawn cutaway block of the real ground at Immendingen (top = real elevation +
   Landsat; front = a drawn karst section). No generated art. */
const RV = D.rivers;
const HDP = [{ t: 'hd_vb.jpg', b: D.hd.hd_vb }, { t: 'hd_bu.jpg', b: D.hd.hd_bu }, { t: 'hd_be.jpg', b: D.hd.hd_be }, { t: 'hd_src.jpg', b: D.hd.hd_src }];
const MW = map3({ m3: D.mapW, p: 'w_', ex: .0105, exk: 10, fog0: 45, fog1: 160, far: 220, patches: HDP, noClose: 1, f1: 'w_flag1.png', f2: 'w_flag2.png', f3: 'w_flag1r.png' });
const MV = map3({ m3: D.mapW, p: 'w_', ex: .0105, exk: 10, fog0: 45, fog1: 160, far: 220, patches: HDP, noClose: 1, f1: 'w_flag1.png', f2: 'w_flag2.png' });
const MI = map3({ m3: D.mapI, p: 'i_', ex: .0105, exk: 1.6, fog0: 6, fog1: 16, noClose: 1, f1: 'i_flag1.png', segX: 1024, segY: 600 });
const MAPS = [MW, MV, MI];
for (const S of MAPS) S.pre.push((t, k) => { S.pin.scale.setScalar(clamp(k.dist / 5, .04, 1.0)); S.ring.visible = S.beam.visible = k.dist > 2; });
/* rivers on every map: Danube gold, Rhine blue (incl. Lake Constance), underground route + Aach dashed green */
for (const S of MAPS) {
  S.dan = mapRiver(S, RV.danube, 0xFFC23A, { wk: S === MI ? .003 : .0035 });
  S.rhi = mapRiver(S, RV.lake.concat(RV.rhine.slice(1)), 0x4FB3FF, { wk: S === MI ? .0045 : .0035 });
  S.und = mapRiver(S, RV.under, 0x5CFF8A, { wk: .006, dash: 14 });
  S.aach = mapRiver(S, RV.aach, 0x4FB3FF, { wk: .0045 });
  S.up = mapRiver(S, RV.danube.filter(p => p[0] <= 8.75), 0x4FB3FF, { wk: S === MI ? .006 : .005 });   /* upper Danube, recoloured for the twist */
}
const CAPS4 = [['VIENNA', 16.3738, 48.2082, '🇦🇹'], ['BRATISLAVA', 17.1077, 48.1486, '🇸🇰'], ['BUDAPEST', 19.0402, 47.4979, '🇭🇺'], ['BELGRADE', 20.4489, 44.8125, '🇷🇸']];
const SINK = [8.733, 47.932], SPRING = [8.857, 47.843];

/* ---------- cutaway block (Immendingen karst) ---------- */
const BKD = D.block; const [K0, K1, KB0, KB1] = BKD.bbox;
const BLW = 2.0, BLD = BLW * (KB1 - KB0) / ((K1 - K0) * Math.cos((KB0 + KB1) / 2 * Math.PI / 180)), HZ = .30, BOT = -1.05;
const WVS = `attribute float fu; attribute float ftop; varying float vU; varying float vY; varying float vTop;
void main(){ vU = fu; vTop = ftop; vY = position.y; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`;
const WFS = `uniform sampler2D noiseT; uniform float time, feat, crackA, sinkP, condP, dyeA, springA, capP, side;
varying float vU; varying float vY; varying float vTop;
float seg(vec2 p, vec2 a, vec2 b, out float h){ vec2 pa = p - a, ba = b - a; h = clamp(dot(pa, ba) / dot(ba, ba), 0.0, 1.0); return length(pa - ba * h); }
void main(){
  vec2 p = vec2(vU * 2.0, vY); float d = vTop - vY;
  float n = texture2D(noiseT, vec2(vU * 3.0 + side * 0.37, vY * 1.3)).r; float n2 = texture2D(noiseT, vec2(vU * 11.0, vY * 7.0)).r;
  float n3 = texture2D(noiseT, vec2(vU * 6.0 + 0.3, vY * 4.0 + 0.7)).r;
  float yy = vY + 0.04 * sin(vU * 7.0 + side) + 0.04 * (n - 0.5);
  vec3 lime = vec3(0.90, 0.84, 0.66), lime2 = vec3(0.80, 0.73, 0.56), marl = vec3(0.52, 0.47, 0.42), soil = vec3(0.30, 0.27, 0.17);
  vec3 c = yy > -0.55 ? mix(lime, lime2, step(0.5, fract(yy * 7.0))) : marl;
  c *= 0.92 + 0.08 * sin(yy * 60.0 + n2 * 2.0);
  c *= 0.86 + 0.26 * n;
  c = mix(c, soil, smoothstep(0.03, 0.004, d));
  float crack = smoothstep(0.035, 0.0, abs(n3 - 0.5)) * step(-0.62, vY) * step(0.03, d);
  c = mix(c, vec3(0.25, 0.20, 0.16), crack * crackA * 0.75);
  if (feat > 0.5) {
    vec3 blue = vec3(0.30, 0.72, 1.0), green = vec3(0.30, 1.0, 0.50);
    vec3 wcol = mix(blue, green, dyeA);
    float sinkZone = smoothstep(0.42, 0.25, vU) * smoothstep(0.02, 0.10, vU);
    float wet = crack * sinkZone * step(-sinkP * 0.7, vY - 0.10);
    c = mix(c, wcol * 1.15, wet * step(0.01, sinkP) * 0.9);
    vec2 A = vec2(0.33, 0.35), B = vec2(0.42, -0.34), Cq = vec2(0.95, -0.58), Dq = vec2(1.40, -0.40), E = vec2(1.57, 0.35);
    float h1, h2, h3, h4; float d1 = seg(p, A, B, h1), d2 = seg(p, B, Cq, h2), d3 = seg(p, Cq, Dq, h3), d4 = seg(p, Dq, E, h4);
    float L1 = length(B - A), L2 = length(Cq - B), L3 = length(Dq - Cq), L4 = length(E - Dq), T = L1 + L2 + L3 + L4;
    float s1 = h1 * L1 / T, s2 = (L1 + h2 * L2) / T, s3 = (L1 + L2 + h3 * L3) / T, s4 = (L1 + L2 + L3 + h4 * L4) / T;
    float w = 0.012 + 0.03 * capP;
    float m = max(max(smoothstep(w, w * 0.4, d1) * step(s1, condP), smoothstep(w, w * 0.4, d2) * step(s2, condP)),
                  max(smoothstep(w, w * 0.4, d3) * step(s3, condP), smoothstep(w, w * 0.4, d4) * step(s4, condP)));
    float sAll = d1 < w ? s1 : (d2 < w ? s2 : (d3 < w ? s3 : s4));
    float dash = step(0.40, fract(sAll * 16.0 - time * 1.2));
    c = mix(c, wcol * 1.3, m * mix(0.6, 1.0, dash));
    c += capP * vec3(0.25, 0.6, 1.0) * smoothstep(0.08, 0.0, min(min(d1, d2), min(d3, d4))) * (0.5 + 0.3 * sin(time * 4.0));
    c += springA * blue * 0.9 * exp(-dot(p - E, p - E) / 0.01) * (0.75 + 0.25 * sin(time * 6.0));
  }
  gl_FragColor = vec4(c, 1.0); }`;
const TVS = `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`;
const TFS = `uniform sampler2D top, hs, riv; uniform float time, sat, riverA, dyeA, springA, upA; uniform vec2 sinkUv, springUv; varying vec2 vUv;
void main(){ vec3 c = texture2D(top, vUv).rgb; float h = texture2D(hs, vUv).r; c *= 0.75 + 0.6 * h;
  float lu = dot(c, vec3(0.299, 0.587, 0.114)); c = mix(vec3(lu), c, sat);
  float r = texture2D(riv, vUv).r; float down = smoothstep(sinkUv.x - 0.02, sinkUv.x + 0.02, vUv.x);
  vec3 wc = mix(vec3(0.25, 0.65, 1.0), vec3(0.30, 1.0, 0.50), dyeA * exp(-dot(vUv - sinkUv, vUv - sinkUv) / 0.004));
  float wa = r * mix(riverA, upA, 1.0 - down);
  c = mix(c, wc * (0.9 + 0.15 * sin(time * 3.0 + vUv.x * 60.0)), wa * 0.85);
  c += springA * vec3(0.3, 0.75, 1.0) * exp(-dot(vUv - springUv, vUv - springUv) / 0.0012) * (0.8 + 0.2 * sin(time * 5.0));
  gl_FragColor = vec4(c, 1.0); }`;
const bx = lon => (lon - K0) / (K1 - K0) * BLW - BLW / 2;
const bz = lat => BLD / 2 - (lat - KB0) / (KB1 - KB0) * BLD;
const buv = (lon, lat) => new T3.Vector2((lon - K0) / (K1 - K0), (lat - KB0) / (KB1 - KB0));
function block3() {
  const el = mk('div', { class: 'scene' }, $('scenes')); const push = mk('div', { class: 'push' }, el);
  const cv = mk('canvas', { width: 1080, height: 1920, class: 'cv' }, push); const ov = mk('div', { class: 'ov' }, push);
  const R = new T3.WebGLRenderer({ canvas: cv, antialias: true, preserveDrawingBuffer: true }); R.setPixelRatio(1); R.setSize(1080, 1920, false);
  const sc = new T3.Scene(); sc.background = new T3.Color(0x0E1C3C);
  const cam = new T3.PerspectiveCamera(30, ASP, .01, 50); sc.add(cam);
  const WU = { noiseT: { value: null }, time: { value: 0 }, feat: { value: 1 }, crackA: { value: 0 }, sinkP: { value: 0 }, condP: { value: 0 }, dyeA: { value: 0 }, springA: { value: 0 }, capP: { value: 0 }, side: { value: 0 } };
  const TU = { top: { value: null }, hs: { value: null }, riv: { value: null }, time: { value: 0 }, sat: { value: 1.12 }, riverA: { value: 1 }, dyeA: { value: 0 }, springA: { value: 0 }, upA: { value: 1 },
    sinkUv: { value: buv(SINK[0], SINK[1]) }, springUv: { value: buv(SPRING[0], SPRING[1]) } };
  const wall = (pts, front, sideK) => { const N = pts.length, M = 40, pos = [], fu = [], ft = [], idx = [];
    for (let i = 0; i < N; i++) for (let j = 0; j <= M; j++) { const [x, ty, z, u] = pts[i]; const y = ty + (BOT - ty) * j / M; pos.push(x, y, z); fu.push(u); ft.push(ty); }
    for (let i = 0; i < N - 1; i++) for (let j = 0; j < M; j++) { const a = i * (M + 1) + j, b = a + M + 1; idx.push(a, b, a + 1, b, b + 1, a + 1); }
    const g = new T3.BufferGeometry(); g.setAttribute('position', new T3.Float32BufferAttribute(pos, 3)); g.setAttribute('fu', new T3.Float32BufferAttribute(fu, 1)); g.setAttribute('ftop', new T3.Float32BufferAttribute(ft, 1)); g.setIndex(idx);
    const U = Object.assign({}, WU, { feat: { value: front ? 1 : 0 }, side: { value: sideK || 0 } });
    const m = new T3.Mesh(g, new T3.ShaderMaterial({ uniforms: U, vertexShader: WVS, fragmentShader: WFS, side: T3.DoubleSide })); sc.add(m); return m; };
  const NX = 300, NZ = 160;
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
  const base = new T3.Mesh(new T3.BoxGeometry(BLW * 1.04, .04, BLD * 1.08), new T3.MeshBasicMaterial({ color: 0x0A1428 })); base.position.y = BOT - .02; sc.add(base);
  const S = { el, push, cv, ov, R, sc, cam, WU, TU, uT: {}, cam0: Track({ x: 0, y: 0, z: 0, dist: 3.4, yaw: 0, pitch: 14 }), parts: [], glows: [], labels: [], hooks: [], emos: [], demI: null };
  READY.push(tex('noise.png', { repeat: 1 }).then(t => WU.noiseT.value = t), tex('blk_top.jpg').then(t => TU.top.value = t), tex('blk_hs.png').then(t => TU.hs.value = t),
    tex('blk_riv.png').then(t => TU.riv.value = t), cpuImg('blk_dem.png').then(I => { S.demI = I; build(I); }));
  return S; }
const bTop = (S, lon, lat) => S.demI ? sampleCPU(S.demI, (lon - K0) / (K1 - K0), (lat - KB0) / (KB1 - KB0)) * HZ : 0;
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
  sp.material.depthTest = false; S.sc.add(sp); const rec = { sp, q, size, a: Track(0), path: null }; S.glows.push(rec); return rec; }
function bLabel(S, txt, q, fs, col) { const e = mk('div', { class: 'plbl' }, S.ov); e.textContent = tr(txt); Object.assign(e.style, { fontSize: fs + 'px', webkitTextStrokeWidth: (fs * .18) + 'px', color: col || '' });
  const rec = { e, q, a: Track(0) }; S.labels.push(rec); return rec; }
function bEmo(S, ch, q, fs, dy) { const e = mk('div', { class: 'emo' }, S.ov); const inner = mk('span', { style: 'display:inline-block' }, e); inner.textContent = ch; e.style.fontSize = (fs || 150) + 'px'; const rec = { e, inner, q, a: Track(0), dy: dy || 0 }; S.emos.push(rec); return rec; }
function renderBlock(S, t) {
  const s = valAt(S.cam0, t); setBCam(S, s); S.WU.time.value = t; S.TU.time.value = t;
  for (const k in S.uT) { const v = valAt(S.uT[k], t); if (k in S.WU) S.WU[k].value = v; if (k in S.TU) S.TU[k].value = v; }
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
const XS = block3();
const BLOCKS = [XS];

/* emoji in screen space */
const emo = (ch, x, y, fs) => { const e = mk('div', { class: 'emo' }, $('fx')); const inner = mk('span', { style: 'display:inline-block' }, e); inner.textContent = ch; Object.assign(e.style, { left: x + 'px', top: y + 'px', fontSize: (fs || 200) + 'px' }); e.inner = inner; return e; };
const eBus = emo('🚌', 700, 520, 190), eTimer = emo('⏳', 760, 520, 180), eLaw = emo('⚖️', 720, 520, 190), eTrophy = emo('🏆', 760, 600, 190), eSalt = emo('🧂', 740, 560, 180), eSwap = emo('🔄', 760, 560, 180);
const SC = { MW, MV, MI, XS };
function mkCard(S, b) { const el = mk('div', { class: 'card' }, S.ov);
  el.innerHTML = `<div class="cin"><div class="crow"><span class="cflag">${b.flag || ''}</span><span>${b.name || ''}</span></div>${b.to || b.big ? `<div class="cbig"><span class="cnum">${b.big || 0}</span><span class="csuf">${b.unit || ''}</span></div>` : ''}${b.tag ? `<div class="ctag">${b.tag}</div>` : ''}</div>`;
  const svg = mk('svg', { width: 1080, height: 1920, style: 'position:absolute;left:0;top:0;overflow:visible;opacity:0' }, S.ov, true); S.ov.insertBefore(svg, el);
  const path = mk('path', { stroke: '#FF7A1A', 'stroke-width': 6, 'stroke-dasharray': '14 10', fill: 'none' }, svg, true);
  const c = { el, ln: svg, path, a: Track(0), num: el.querySelector('.cnum'), suf: el.querySelector('.csuf'), lon: b.lon, lat: b.lat, dx: b.dx || 0, dy: b.dy }; S.cards.push(c); return c; }
