<script>
const D = __DATA__;
if (D.lang === 'hi') document.getElementById('root').classList.add('hi');
const NS = 'http://www.w3.org/2000/svg', T3 = THREE;
const $ = id => document.getElementById(id);
const tr = s => (D.i18n && D.i18n[s]) || s;
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const mk = (tag, attrs, parent, ns) => { const e = ns ? document.createElementNS(NS, tag) : document.createElement(tag); for (const k in attrs || {}) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; };
const markup = (txt, el) => { let key = false; txt.split(' ').forEach((w, i) => { let word = w; if (word.startsWith('*')) { key = true; word = word.slice(1); } const end = word.endsWith('*'); if (end) word = word.slice(0, -1);
  const s = document.createElement('span'); if (key) s.className = 'k'; s.textContent = (i ? ' ' : '') + word; el.appendChild(s); if (end) key = false; }); };
const C = (li, ci, off) => D.C[li + '.' + (ci || 0)] + (off || 0);
const LN = D.LN, PT = D.pt;

/* ---------- keyframe tracks (evaluated from time only) ---------- */
const EZ = {}; const ease = n => EZ[n || 'power2.inOut'] || (EZ[n || 'power2.inOut'] = gsap.parseEase(n || 'power2.inOut'));
function Track(base) { return { base, last: base, keys: [] }; }
function key(T, to, at, dur, e) { const from = (typeof T.last === 'object') ? Object.assign({}, T.last) : T.last;
  const tgt = (typeof to === 'object') ? Object.assign({}, from, to) : to; T.keys.push({ a: at, d: Math.max(.04, dur), from, to: tgt, e: ease(e) }); T.last = tgt; }
function valAt(T, t) { let v = T.base;
  for (const k of T.keys) { if (t < k.a) break; const p = k.e(Math.min(1, (t - k.a) / k.d));
    if (typeof k.to === 'object') { v = {}; for (const q in k.to) v[q] = k.from[q] + (k.to[q] - k.from[q]) * p; } else v = k.from + (k.to - k.from) * p; }
  return v; }

/* ---------- assets ---------- */
const loader = new T3.TextureLoader(); const TX = {};
function tex(n, opt) { if (!TX[n]) TX[n] = new Promise(r => loader.load('assets/' + n, t => { t.anisotropy = 4; if (opt && opt.nearest) { t.minFilter = t.magFilter = T3.LinearFilter; t.generateMipmaps = false; } if (opt && opt.repeat) t.wrapS = t.wrapT = T3.RepeatWrapping; r(t); })); return TX[n]; }
const CPU = {};
function cpuImg(n) { if (!CPU[n]) CPU[n] = new Promise(r => { const im = new Image(); im.onload = () => { const c = document.createElement('canvas'); c.width = im.width; c.height = im.height; const x = c.getContext('2d'); x.drawImage(im, 0, 0); r({ w: im.width, h: im.height, d: x.getImageData(0, 0, im.width, im.height).data }); }; im.src = 'assets/' + n; }); return CPU[n]; }
const sampleCPU = (I, u, v) => { const x = clamp(Math.round(u * (I.w - 1)), 0, I.w - 1), y = clamp(Math.round((1 - v) * (I.h - 1)), 0, I.h - 1); return I.d[(y * I.w + x) * 4] / 255; };
function glowTex() { const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d'); const r = g.createRadialGradient(64, 64, 0, 64, 64, 64);
  r.addColorStop(0, 'rgba(255,255,255,1)'); r.addColorStop(.25, 'rgba(255,255,255,.55)'); r.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = r; g.fillRect(0, 0, 128, 128); return new T3.CanvasTexture(c); }
const GLOW = glowTex();
const READY = [];

/* ---------- 3D plate scenes ---------- */
const PH = 2, FOV = 30, ASP = 1080 / 1920;
const VS = `uniform sampler2D dep; uniform float dScale; varying vec2 vUv;
void main(){ vUv = uv; float d = texture2D(dep, uv).r; vec3 p = position; p.z += (d - 0.5) * dScale; gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0); }`;
const FS = `uniform sampler2D tex, tex2, burn, noiseT; uniform float prog, grassP, bright, sat, time, shim, hasBurn, heat, flk; uniform vec4 grid, shimRect; varying vec2 vUv;
void main(){ vec2 uv = vUv;
  if (shim > 0.0) { float m = smoothstep(shimRect.x, shimRect.x + 0.05, uv.x) * smoothstep(shimRect.z, shimRect.z - 0.05, uv.x) * smoothstep(shimRect.y, shimRect.y + 0.05, uv.y) * smoothstep(shimRect.w, shimRect.w - 0.05, uv.y);
    uv += shim * m * vec2(sin(uv.y * 170.0 + time * 7.0) * 0.0016, sin(uv.x * 120.0 + time * 5.0) * 0.0011); }
  vec3 c = texture2D(tex, uv).rgb;
  if (hasBurn > 0.5) { float b = texture2D(burn, uv).r; float r = 1.0 - smoothstep(prog - 0.07, prog, b);
    float fl = mix(1.0, 0.86 + 0.14 * sin(time * 13.0 + uv.x * 40.0) * sin(time * 7.3 + uv.y * 31.0), flk); /* fire flicker only on plates with flick: 1 (no line comments inside one-line shader strings) */ c = mix(c, texture2D(tex2, uv).rgb * mix(1.0, fl, r), r); }
  if (grassP > 0.0) { float inG = smoothstep(grid.x, grid.x + 0.04, uv.x) * smoothstep(grid.z, grid.z - 0.04, uv.x) * smoothstep(grid.y, grid.y + 0.04, uv.y) * smoothstep(grid.w, grid.w - 0.04, uv.y);
    float n = texture2D(noiseT, uv * vec2(2.0, 3.0)).r; float n2 = texture2D(noiseT, uv * vec2(9.0, 13.0)).r;
    float g = smoothstep(n - 0.06, n + 0.06, grassP) * inG; vec3 gc = mix(vec3(0.30, 0.41, 0.19), vec3(0.46, 0.52, 0.26), n2) * (0.7 + 0.6 * dot(c, vec3(0.299,0.587,0.114))); c = mix(c, gc, g * 0.9); }
  c += heat * vec3(0.20, 0.06, 0.0);
  float l = dot(c, vec3(0.299, 0.587, 0.114)); c = mix(vec3(l), c, sat) * bright;
  gl_FragColor = vec4(c, 1.0); }`;
const PVS = `uniform float time, rise, sizeK, drift; attribute vec3 seed; varying float vA; varying float vS;
void main(){ float t = fract(seed.x + time * seed.y); vec3 p = position; p.y += t * rise; p.x += sin(t * 6.0 + seed.z * 30.0) * drift * t; p.z += t * 0.05;
  vec4 mv = modelViewMatrix * vec4(p, 1.0); gl_Position = projectionMatrix * mv; gl_PointSize = sizeK * (0.5 + t * 1.6) / -mv.z; vA = sin(t * 3.14159); vS = seed.z; }`;
const PFS = `uniform vec3 col; uniform float alpha, time, flick; varying float vA; varying float vS;
void main(){ float d = length(gl_PointCoord - 0.5); float a = exp(-d * d * 14.0) * vA * alpha; a *= 1.0 - flick + flick * (0.5 + 0.5 * sin(time * 20.0 + vS * 60.0)); gl_FragColor = vec4(col, a); }`;
const SHOTS = [];
function plate3(o) {
  const el = mk('div', { class: 'scene' }, $('scenes')); const push = mk('div', { class: 'push' }, el);
  const cv = mk('canvas', { width: 1080, height: 1920, class: 'cv' }, push);
  const ov = mk('div', { class: 'ov' }, push); const chars = mk('div', { class: 'chars' }, push);
  const R = new T3.WebGLRenderer({ canvas: cv, antialias: true, preserveDrawingBuffer: true }); R.setPixelRatio(1); R.setSize(1080, 1920, false);
  const sc = new T3.Scene(); sc.background = new T3.Color(o.bg || 0x02070D);
  const cam = new T3.PerspectiveCamera(FOV, ASP, .02, 100); sc.add(cam);
  const W = PH * 1024 / 1536;
  const U = { tex: { value: null }, tex2: { value: null }, dep: { value: null }, burn: { value: null }, noiseT: { value: null }, dScale: { value: o.dScale || .32 },
    prog: { value: -.2 }, grassP: { value: 0 }, grid: { value: new T3.Vector4(0, 0, 1, 1) }, bright: { value: 1 }, sat: { value: 1 }, time: { value: 0 },
    shim: { value: 0 }, shimRect: { value: new T3.Vector4(0, 0, 1, 1) }, hasBurn: { value: o.burn ? 1 : 0 }, heat: { value: 0 }, flk: { value: o.flick ? 1 : 0 } };
  if (o.shim) U.shimRect.value.set(o.shim[0] / 1024, 1 - o.shim[3] / 1536, o.shim[2] / 1024, 1 - o.shim[1] / 1536);
  if (o.grid) U.grid.value.set(o.grid[0] / 1024, 1 - o.grid[3] / 1536, o.grid[2] / 1024, 1 - o.grid[1] / 1536);
  sc.add(new T3.Mesh(new T3.PlaneGeometry(W, PH, 256, 384), new T3.ShaderMaterial({ uniforms: U, vertexShader: VS, fragmentShader: FS })));
  const S = { el, push, cv, ov, chars, R, sc, cam, U, W, o, cam0: Track({ x: 512, y: 768, z: 1, yaw: 0, pitch: 0 }), uT: {}, parts: [], glows: [], labels: [], hooks: [] };
  READY.push(tex(o.tex).then(t => U.tex.value = t), tex(o.dep, { nearest: 1 }).then(t => U.dep.value = t), cpuImg(o.dep).then(I => S.depI = I),
    tex('noise.png', { repeat: 1 }).then(t => U.noiseT.value = t), o.tex2 ? tex(o.tex2).then(t => U.tex2.value = t) : 0, o.burn ? tex(o.burn).then(t => U.burn.value = t) : 0);
  return S;
}
const world = (S, ix, iy, lift) => { const u = ix / 1024, v = 1 - iy / 1536; const d = S.depI ? sampleCPU(S.depI, u, v) : .5;
  return new T3.Vector3((u - .5) * S.W, (v - .5) * PH, (d - .5) * S.U.dScale.value + (lift || 0)); };
const toScreen = (cam, p) => { const v = p.clone().project(cam); return { x: (v.x + 1) / 2 * 1080, y: (1 - v.y) / 2 * 1920, z: v.z }; };
/* 10% overscan: camera yaw/pitch never reveals the plate edge */
function setCam(S, s) { const Z = Math.max(1.1, s.z); const hv = PH / 2 / Z / 1.1; const dist = hv / Math.tan(FOV * Math.PI / 360); const hw = hv * ASP;
  let tx = (s.x / 1024 - .5) * S.W, ty = (.5 - s.y / 1536) * PH; const mx = Math.max(0, S.W / 2 - hw), my = Math.max(0, PH / 2 - hv);
  tx = clamp(tx, -mx, mx); ty = clamp(ty, -my, my);
  const yw = s.yaw * Math.PI / 180, pt = s.pitch * Math.PI / 180;
  S.cam.position.set(tx + Math.sin(yw) * Math.cos(pt) * dist, ty + Math.sin(pt) * dist, Math.cos(yw) * Math.cos(pt) * dist); S.cam.lookAt(tx, ty, 0); S.cam.updateMatrixWorld(); }
function particles(S, o) { // o: rect [x0,y0,x1,y1] image px, n, rise, size, col, alpha, add, flick, drift, speed, lift
  const n = o.n, pos = new Float32Array(n * 3), sd = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) { const fx = ((i * 0.6180339) % 1), fy = ((i * 0.7548776) % 1); const ix = o.rect[0] + fx * (o.rect[2] - o.rect[0]), iy = o.rect[1] + fy * (o.rect[3] - o.rect[1]);
    const u = ix / 1024, v = 1 - iy / 1536; pos.set([(u - .5) * S.W, (v - .5) * PH, .5 * S.U.dScale.value * .0 + (o.lift || .18)], i * 3);
    sd.set([(i * 0.3819) % 1, (o.speed || .25) * (.7 + ((i * 0.917) % 1) * .6), (i * 0.1234) % 1], i * 3); }
  const g = new T3.BufferGeometry(); g.setAttribute('position', new T3.BufferAttribute(pos, 3)); g.setAttribute('seed', new T3.BufferAttribute(sd, 3));
  const U = { time: { value: 0 }, rise: { value: o.rise || .5 }, sizeK: { value: o.size || 300 }, drift: { value: o.drift || .05 }, col: { value: new T3.Color(o.col || 0xEEF2F6) }, alpha: { value: 0 }, flick: { value: o.flick || 0 } };
  const m = new T3.ShaderMaterial({ uniforms: U, vertexShader: PVS, fragmentShader: PFS, transparent: true, depthWrite: false, blending: o.add ? T3.AdditiveBlending : T3.NormalBlending });
  const P = new T3.Points(g, m); P.frustumCulled = false; S.sc.add(P); const rec = { P, U, a: Track(0) }; S.parts.push(rec); return rec; }
function glow(S, ix, iy, size, col, lift) { const sp = new T3.Sprite(new T3.SpriteMaterial({ map: GLOW, color: col, transparent: true, blending: T3.AdditiveBlending, depthWrite: false, opacity: 0 }));
  S.sc.add(sp); const rec = { sp, ix, iy, size, lift: lift || .08, a: Track(0), seed: S.glows.length * 1.7 }; S.glows.push(rec); return rec; }
function label(S, txt, ix, iy, fs, col) { const e = mk('div', { class: 'plbl' }, S.ov); e.textContent = tr(txt); Object.assign(e.style, { fontSize: fs + 'px', webkitTextStrokeWidth: (fs * .18) + 'px', color: col || '' });
  const rec = { e, ix, iy, a: Track(0) }; S.labels.push(rec); return rec; }
function lights(S) { S.sc.add(new T3.HemisphereLight(0xffffff, 0x2a3240, 1.0)); const d = new T3.DirectionalLight(0xffffff, 1.1); d.position.set(-2, 3, 4); S.sc.add(d); }
const viewPos = (sx, sy, dist) => { const hv = dist * Math.tan(FOV * Math.PI / 360); return new T3.Vector3((sx / 540 - 1) * hv * ASP, (1 - sy / 960) * hv, -dist); };

function renderPlate(S, t) {
  setCam(S, valAt(S.cam0, t)); S.U.time.value = t;
  for (const k in S.uT) S.U[k].value = valAt(S.uT[k], t);
  for (const p of S.parts) { p.U.time.value = t; p.U.alpha.value = valAt(p.a, t); }
  for (const g of S.glows) { const a = valAt(g.a, t); g.sp.material.opacity = a * (.8 + .2 * Math.sin(t * 11 + g.seed) * Math.sin(t * 6.3 + g.seed * 2));
    g.sp.position.copy(world(S, g.ix, g.iy, g.lift)); const s = g.size * (1 + .06 * Math.sin(t * 9 + g.seed)); g.sp.scale.set(s, s, 1); }
  for (const h of S.hooks) h(t);
  S.R.render(S.sc, S.cam);
  for (const L of S.labels) { const a = valAt(L.a, t); L.e.style.opacity = a; if (a <= 0) continue; const q = toScreen(S.cam, world(S, L.ix, L.iy, .03));
    L.e.style.transform = `translate(${(q.x - L.e.offsetWidth / 2).toFixed(1)}px,${(q.y - L.e.offsetHeight / 2).toFixed(1)}px) scale(${(.6 + .4 * Math.min(1, a * 1.5)).toFixed(3)})`; }
}

