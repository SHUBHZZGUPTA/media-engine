/* ---------- 3D map: globe + terrain flyover (parametric: several bboxes per video) ---------- */
/* cfg: { m3: map3d.json data, p: asset prefix, flag: flag png or null } */
function map3(cfg) {
  const M3 = cfg.m3, P = cfg.p || ''; const [L0, L1, B0, B1] = M3.bbox; const LC = (L0 + L1) / 2, BC = (B0 + B1) / 2, KX = Math.cos(BC * Math.PI / 180);
  const el = mk('div', { class: 'scene' }, $('scenes')); const push = mk('div', { class: 'push' }, el);
  const cvG = mk('canvas', { width: 1080, height: 1920, class: 'cv' }, push); const cvT = mk('canvas', { width: 1080, height: 1920, class: 'cv' }, push);
  const ov = mk('div', { class: 'ov' }, push);
  const RG = new T3.WebGLRenderer({ canvas: cvG, antialias: true, preserveDrawingBuffer: true }); RG.setPixelRatio(1); RG.setSize(1080, 1920, false);
  const RT = new T3.WebGLRenderer({ canvas: cvT, antialias: true, preserveDrawingBuffer: true }); RT.setPixelRatio(1); RT.setSize(1080, 1920, false);
  // globe
  const sg = new T3.Scene(); sg.background = new T3.Color(0x01040A); const cg = new T3.PerspectiveCamera(30, ASP, .01, 100);
  const globe = new T3.Mesh(new T3.SphereGeometry(1, 160, 120), new T3.MeshBasicMaterial({ color: 0xffffff })); sg.add(globe);
  const atm = new T3.Mesh(new T3.SphereGeometry(1.06, 96, 72), new T3.ShaderMaterial({ side: T3.BackSide, transparent: true, blending: T3.AdditiveBlending, depthWrite: false,
    vertexShader: `varying vec3 vN; varying vec3 vP; void main(){ vN = normalize(normalMatrix * normal); vec4 mv = modelViewMatrix * vec4(position,1.0); vP = mv.xyz; gl_Position = projectionMatrix * mv; }`,
    fragmentShader: `varying vec3 vN; varying vec3 vP; void main(){ float f = pow(clamp(1.0 - abs(dot(normalize(-vP), vN)), 0.0, 1.0), 2.2); gl_FragColor = vec4(0.35, 0.65, 1.0, f * 0.9); }` })); sg.add(atm);
  { const n = 1400, p = new Float32Array(n * 3); for (let i = 0; i < n; i++) { const a = (i * 2.399963) % (Math.PI * 2), z = 1 - 2 * ((i + .5) / n), r = Math.sqrt(1 - z * z); p.set([Math.cos(a) * r * 30, z * 30, Math.sin(a) * r * 30], i * 3); }
    const g = new T3.BufferGeometry(); g.setAttribute('position', new T3.BufferAttribute(p, 3)); sg.add(new T3.Points(g, new T3.PointsMaterial({ color: 0xffffff, size: 1.6, sizeAttenuation: false, transparent: true, opacity: .7 }))); }
  const ll = (lon, lat, r) => { const ph = (lon + 180) * Math.PI / 180, th = (90 - lat) * Math.PI / 180; return new T3.Vector3(-Math.cos(ph) * Math.sin(th) * r, Math.cos(th) * r, Math.sin(ph) * Math.sin(th) * r); };
  // terrain
  const st = new T3.Scene(); st.background = new T3.Color(0x0A1424); st.fog = new T3.Fog(0x0A1424, cfg.fog0 || 9, cfg.fog1 || 20);
  const ct = new T3.PerspectiveCamera(32, ASP, .005, cfg.far || 60); ct.up.set(0, 0, 1);
  const Wt = (L1 - L0) * KX, Ht = (B1 - B0), EX = cfg.ex || .0105;
  const FR = (() => { const lo = M3.pa.map(p => p[0]), la = M3.pa.map(p => p[1]); return new T3.Vector4((Math.min(...lo) - L0) / (L1 - L0), (Math.min(...la) - B0) / (B1 - B0), (Math.max(...lo) - L0) / (L1 - L0), (Math.max(...la) - B0) / (B1 - B0)); })();
  const PR = (b) => new T3.Vector4((b[0] - L0) / (L1 - L0), (b[2] - B0) / (B1 - B0), (b[1] - L0) / (L1 - L0), (b[3] - B0) / (B1 - B0));
  const PT = (cfg.patches || []).slice(0, 4); while (PT.length < 4) PT.push(null);
  const TU = { dem: { value: null }, ne: { value: null }, cls: { value: null }, mask: { value: null }, hs: { value: null }, hl: { value: 0 }, exag: { value: 0 }, flag: { value: null }, flagA: { value: 0 }, frect: { value: FR },
    f1: { value: null }, f2: { value: null }, f3: { value: null }, fA1: { value: 0 }, fA2: { value: 0 }, fA3: { value: 0 }, useC: { value: cfg.noClose ? 0 : 1 },
    p1: { value: null }, p2: { value: null }, p3: { value: null }, p4: { value: null },
    r1: { value: PT[0] ? PR(PT[0].b) : new T3.Vector4(2, 2, 3, 3) }, r2: { value: PT[1] ? PR(PT[1].b) : new T3.Vector4(2, 2, 3, 3) },
    r3: { value: PT[2] ? PR(PT[2].b) : new T3.Vector4(2, 2, 3, 3) }, r4: { value: PT[3] ? PR(PT[3].b) : new T3.Vector4(2, 2, 3, 3) },
    crect: { value: new T3.Vector4((M3.pa_close_bbox[0] - L0) / (L1 - L0), (M3.pa_close_bbox[2] - B0) / (B1 - B0), (M3.pa_close_bbox[1] - L0) / (L1 - L0), (M3.pa_close_bbox[3] - B0) / (B1 - B0)) } };
  const terr = new T3.Mesh(new T3.PlaneGeometry(Wt, Ht, cfg.segX || 640, cfg.segY || 320), new T3.ShaderMaterial({ uniforms: TU,
    vertexShader: `uniform sampler2D dem; uniform float exag; varying vec2 vUv; void main(){ vUv = uv; vec3 p = position; p.z += texture2D(dem, uv).r * exag; gl_Position = projectionMatrix * modelViewMatrix * vec4(p,1.0); }`,
    fragmentShader: `uniform sampler2D ne, cls, mask, hs, flag, f1, f2, f3, p1, p2, p3, p4; uniform float hl, flagA, fA1, fA2, fA3, useC; uniform vec4 crect, frect, r1, r2, r3, r4; varying vec2 vUv;
      float pf(vec2 q){ return smoothstep(0.0, 0.06, q.x) * smoothstep(1.0, 0.94, q.x) * smoothstep(0.0, 0.06, q.y) * smoothstep(1.0, 0.94, q.y); }
      vec3 patchMix(vec3 c, sampler2D t, vec4 r){ vec2 q = (vUv - r.xy) / (r.zw - r.xy); float f = pf(q); return f > 0.0 ? mix(c, texture2D(t, clamp(q, 0.0, 1.0)).rgb, f) : c; }
      void main(){ vec3 c = texture2D(ne, vUv).rgb;
        vec2 q = (vUv - crect.xy) / (crect.zw - crect.xy); float f = pf(q) * useC;
        if (f > 0.0) c = mix(c, texture2D(cls, clamp(q, 0.0, 1.0)).rgb, f);
        c = patchMix(c, p1, r1); c = patchMix(c, p2, r2); c = patchMix(c, p3, r3); c = patchMix(c, p4, r4);
        float h = texture2D(hs, vUv).r; c *= 0.42 + 0.78 * h; float lu = dot(c, vec3(0.299,0.587,0.114)); c = mix(vec3(lu), c, 0.78);
        float m = texture2D(mask, vUv).r; c = mix(c, c * vec3(1.15, 1.02, 0.7) + vec3(0.07, 0.045, 0.0), m * hl * 0.6); c *= mix(1.0, 0.62, hl * (1.0 - m));
        if (flagA > 0.0) { vec2 fq = clamp((vUv - frect.xy) / (frect.zw - frect.xy), 0.0, 1.0); vec3 fc = texture2D(flag, fq).rgb; float lu2 = dot(c, vec3(0.299,0.587,0.114));
          c = mix(c, fc * (0.62 + 0.75 * lu2), m * flagA * 0.8); }
        float lu3 = dot(c, vec3(0.299,0.587,0.114));
        if (fA1 > 0.0) { vec4 o = texture2D(f1, vUv); c = mix(c, o.rgb * (0.6 + 0.7 * lu3), o.a * fA1 * 0.85); }
        if (fA2 > 0.0) { vec4 o = texture2D(f2, vUv); c = mix(c, o.rgb * (0.6 + 0.7 * lu3), o.a * fA2 * 0.85); }
        if (fA3 > 0.0) { vec4 o = texture2D(f3, vUv); c = mix(c, o.rgb * (0.6 + 0.7 * lu3), o.a * fA3 * 0.85); }
        gl_FragColor = vec4(c, 1.0); }` }));
  st.add(terr);
  const demI = { I: null }; const hAt = (lon, lat) => demI.I ? sampleCPU(demI.I, (lon - L0) / (L1 - L0), (lat - B0) / (B1 - B0)) * EX * 1.0 : 0;
  const wpos = (lon, lat, up) => new T3.Vector3((lon - LC) * KX, lat - BC, hAt(lon, lat) * TU.exag.value / EX + (up || 0));
  const WU = { rise: { value: 0 }, wh: { value: cfg.wh || .28 } };
  const wallMat = new T3.ShaderMaterial({ uniforms: WU, transparent: true, depthWrite: false, side: T3.DoubleSide, blending: T3.AdditiveBlending,
    vertexShader: `uniform float rise, wh; attribute float k; varying float vK; void main(){ vK = k; vec3 p = position; p.z += k * wh * rise; gl_Position = projectionMatrix * modelViewMatrix * vec4(p,1.0); }`,
    fragmentShader: `uniform float rise; varying float vK; void main(){ float a = (1.0 - vK) * (1.0 - vK) * rise; gl_FragColor = vec4(1.0, 0.68, 0.18, a * 0.95); }` });
  const pin = new T3.Group(); st.add(pin);
  const beam = new T3.Mesh(new T3.CylinderGeometry(.008, .008, .24, 12, 1, true), new T3.MeshBasicMaterial({ color: 0xFF7A1A, transparent: true, opacity: .0, blending: T3.AdditiveBlending, depthWrite: false }));
  beam.rotation.x = Math.PI / 2; beam.position.z = .12; pin.add(beam);
  const head = new T3.Sprite(new T3.SpriteMaterial({ map: GLOW, color: 0xFF5A1A, transparent: true, blending: T3.AdditiveBlending, depthWrite: false, opacity: 0 })); head.position.z = .24; head.scale.set(.16, .16, 1); pin.add(head);
  const ring = new T3.Mesh(new T3.RingGeometry(.02, .03, 48), new T3.MeshBasicMaterial({ color: 0xFF7A1A, transparent: true, opacity: 0, blending: T3.AdditiveBlending, depthWrite: false, side: T3.DoubleSide })); ring.position.z = .004; pin.add(ring);
  const S = { el, push, ov, cvG, cvT, RG, RT, sg, cg, st, ct, globe, TU, WU, pin, beam, head, ring, labels: [], lls: [], cards: [], pre: [], post: [], dots: [], rivers: [], onDem: [],
    gk: Track({ lon: 10, lat: 30, dist: 3.4 }), tk: Track({ lon: LC, lat: BC, dist: 5, el: 74, yaw: 0 }),
    x: Track(0), hl: Track(0), rise: Track(0), pinA: Track(0), flagA: Track(0), fA1: Track(0), fA2: Track(0), fA3: Track(0), wpos, ll, L0, L1, B0, B1, LC, BC, KX, EX, M3 };
  READY.push(tex(P + 'globe.jpg').then(t => { globe.material.map = t; globe.material.needsUpdate = true; }), tex(P + 'ne.jpg').then(t => TU.ne.value = t), tex(P + 'pa_close.jpg').then(t => TU.cls.value = t),
    tex(P + 'pa_mask.png').then(t => TU.mask.value = t), cfg.flag ? tex(cfg.flag).then(t => TU.flag.value = t) : 0, tex(P + 'hillshade.png').then(t => TU.hs.value = t),
    ...PT.map((p, i) => p ? tex(p.t).then(t => TU['p' + (i + 1)].value = t) : 0), cfg.f1 ? tex(cfg.f1).then(t => TU.f1.value = t) : 0, cfg.f2 ? tex(cfg.f2).then(t => TU.f2.value = t) : 0, cfg.f3 ? tex(cfg.f3).then(t => TU.f3.value = t) : 0, tex(P + 'dem8.png', { nearest: 1 }).then(t => TU.dem.value = t),
    cpuImg(P + 'dem8.png').then(I => { demI.I = I; TU.exag.value = EX * (cfg.exk || 26);
      const pts = M3.pa.map(([lo, la]) => wpos(lo, la, .002)); const pos = [], kk = [];
      for (let i = 0; i < pts.length; i++) { const a = pts[i], b = pts[(i + 1) % pts.length]; pos.push(a.x, a.y, a.z, b.x, b.y, b.z, b.x, b.y, b.z, a.x, a.y, a.z, b.x, b.y, b.z, a.x, a.y, a.z); kk.push(0, 0, 1, 0, 1, 1); }
      const g = new T3.BufferGeometry(); g.setAttribute('position', new T3.Float32BufferAttribute(pos, 3)); g.setAttribute('k', new T3.Float32BufferAttribute(kk, 1)); st.add(new T3.Mesh(g, wallMat));
      const cp = wpos(M3.pin[0], M3.pin[1]); pin.position.copy(cp); for (const f of S.onDem) f(); }));
  return S;
}
function camOf(S, k) { const tg = new T3.Vector3((k.lon - S.LC) * S.KX, k.lat - S.BC, 0); const e = k.el * Math.PI / 180, y = k.yaw * Math.PI / 180;
  S.ct.position.set(tg.x + Math.sin(y) * Math.cos(e) * k.dist, tg.y - Math.cos(y) * Math.cos(e) * k.dist, Math.sin(e) * k.dist); S.ct.lookAt(tg); S.ct.updateMatrixWorld(); }
function renderMap(S, t) {
  const x = valAt(S.x, t); S.cvG.style.opacity = 1 - x; S.cvT.style.opacity = x;
  if (x < 1) { const g = valAt(S.gk, t); const p = S.ll(g.lon, g.lat, g.dist); S.cg.position.copy(p); S.cg.lookAt(0, 0, 0); S.globe.rotation.y = 0; S.RG.render(S.sg, S.cg); }
  if (x > 0) { const k = valAt(S.tk, t); S.TU.hl.value = valAt(S.hl, t); S.TU.flagA.value = valAt(S.flagA, t); S.TU.fA1.value = valAt(S.fA1, t); S.TU.fA2.value = valAt(S.fA2, t); S.TU.fA3.value = valAt(S.fA3, t); S.WU.rise.value = valAt(S.rise, t);
    camOf(S, k);
    const pa = valAt(S.pinA, t); S.beam.material.opacity = pa * .8; S.head.material.opacity = pa; const rs = 1 + ((t * .9) % 1) * 5; S.ring.scale.set(rs, rs, 1); S.ring.material.opacity = pa * (1 - (t * .9) % 1);
    for (const h of S.pre) h(t, k);
    S.RT.render(S.st, S.ct);
    for (const cd of S.cards) { const a = valAt(cd.a, t); cd.el.style.opacity = a * x; cd.ln.style.opacity = a * x; if (a > 0) { const q = toScreen(S.ct, S.wpos(cd.lon, cd.lat, .004));
      const w = cd.el.offsetWidth, h = cd.el.offsetHeight, cx = clamp(q.x - w / 2 + (cd.dx || 0), 40, 1040 - w), cy = clamp(q.y - h - (cd.dy === undefined ? 170 : cd.dy), 260, 1150 - h);
      cd.el.style.transform = `translate(${cx.toFixed(1)}px,${(cy + (1 - a) * 40).toFixed(1)}px)`; cd.path.setAttribute('d', `M${(cx + w / 2).toFixed(1)} ${(cy + h).toFixed(1)} L${q.x.toFixed(1)} ${q.y.toFixed(1)}`); } }
    for (const L of S.lls) { const a = valAt(L.a, t); L.e.style.opacity = a * x; if (a <= 0) continue; const q = toScreen(S.ct, S.wpos(L.lon, L.lat, .003));
      L.e.style.transform = `translate(${(q.x - L.e.offsetWidth / 2 + (L.dx || 0)).toFixed(1)}px,${(q.y - L.e.offsetHeight / 2 + (L.dy || 0)).toFixed(1)}px) scale(${(.6 + .4 * Math.min(1, a * 1.5)).toFixed(3)})`; }
    for (const h of S.post) h(t, k, x); }
}
/* screen point of lon/lat at time t (pure function of time) */
function mapProj(S, t, lon, lat, up) { camOf(S, valAt(S.tk, t)); return toScreen(S.ct, S.wpos(lon, lat, up || .003)); }
function mapLabel(S, txt, lon, lat, fs, col, dx, dy) { const e = mk('div', { class: 'plbl' }, S.ov); e.textContent = tr(txt); Object.assign(e.style, { fontSize: fs + 'px', webkitTextStrokeWidth: (fs * .18) + 'px', color: col || '' });
  const rec = { e, lon, lat, a: Track(0), dx: dx || 0, dy: dy || 0 }; S.lls.push(rec); return rec; }
/* glowing dot at lon/lat (always on top), size scales with camera distance */
function mapDot(S, lon, lat, col, size) { const sp = new T3.Sprite(new T3.SpriteMaterial({ map: GLOW, color: col, transparent: true, blending: T3.AdditiveBlending, depthWrite: false, opacity: 0 }));
  sp.material.depthTest = false; S.st.add(sp); const rec = { sp, lon, lat, a: Track(0), size: size || .05 }; S.dots.push(rec);
  S.pre.push((t, k) => { const a = valAt(rec.a, t); sp.material.opacity = a; sp.position.copy(S.wpos(lon, lat, .002)); const s = rec.size * k.dist * (1 + .12 * Math.sin(t * 7 + lon * 50)); sp.scale.set(s, s, 1); });
  return rec; }
/* a glowing river ribbon drawn along a lon/lat polyline; width follows the camera distance; prog draws it along its length */
function mapRiver(S, pts, col, o) { o = o || {};
  const U = { prog: { value: 0 }, alpha: { value: 0 }, w: { value: .01 }, col: { value: new T3.Color(col) }, time: { value: 0 }, dash: { value: o.dash || 0 }, from: { value: 0 } };
  const mat = new T3.ShaderMaterial({ uniforms: U, transparent: true, depthWrite: false, depthTest: false, blending: T3.AdditiveBlending, side: T3.DoubleSide,
    vertexShader: `uniform float w; attribute vec2 nrm; attribute float side; attribute float s; varying float vS; varying float vSide;
      void main(){ vS = s; vSide = side; vec3 p = position; p.xy += nrm * side * w; gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0); }`,
    fragmentShader: `uniform float prog, alpha, time, dash, from; uniform vec3 col; varying float vS; varying float vSide;
      void main(){ if (vS > prog || vS < from) discard; float e = 1.0 - abs(vSide); float core = smoothstep(0.35, 0.9, e); float glow = e * e;
        float d = dash > 0.0 ? step(0.42, fract(vS * dash - time * 0.9)) : 1.0; float head = smoothstep(prog - 0.02, prog, vS) * 0.8;
        vec3 c = col * (0.55 * glow + 1.1 * core) + vec3(1.0) * core * (0.25 + head);
        gl_FragColor = vec4(c, alpha * (0.35 * glow + 0.85 * core) * d); }` });
  const rec = { U, a: Track(0), prog: Track(o.prog0 || 0), from: Track(0), mesh: null, wk: o.wk || .006, pts };
  S.onDem.push(() => { const P3 = pts.map(([lo, la]) => S.wpos(lo, la, o.up || .003)); let L = 0; const acc = [0];
    for (let i = 1; i < P3.length; i++) { L += P3[i].distanceTo(P3[i - 1]); acc.push(L); }
    const pos = [], nrm = [], sd = [], ss = [], idx = [];
    P3.forEach((p, i) => { const a = P3[Math.max(0, i - 1)], b = P3[Math.min(P3.length - 1, i + 1)]; let nx = -(b.y - a.y), ny = b.x - a.x; const n = Math.hypot(nx, ny) || 1; nx /= n; ny /= n;
      for (const sdv of [-1, 1]) { pos.push(p.x, p.y, p.z); nrm.push(nx, ny); sd.push(sdv); ss.push(acc[i] / L); } });
    for (let i = 0; i < P3.length - 1; i++) { const q = i * 2; idx.push(q, q + 1, q + 2, q + 1, q + 3, q + 2); }
    const g = new T3.BufferGeometry(); g.setAttribute('position', new T3.Float32BufferAttribute(pos, 3)); g.setAttribute('nrm', new T3.Float32BufferAttribute(nrm, 2));
    g.setAttribute('side', new T3.Float32BufferAttribute(sd, 1)); g.setAttribute('s', new T3.Float32BufferAttribute(ss, 1)); g.setIndex(idx);
    rec.mesh = new T3.Mesh(g, mat); rec.mesh.frustumCulled = false; rec.mesh.renderOrder = 5; S.st.add(rec.mesh); });
  S.pre.push((t, k) => { U.alpha.value = valAt(rec.a, t); U.prog.value = valAt(rec.prog, t); U.from.value = valAt(rec.from, t); U.time.value = t; U.w.value = rec.wk * k.dist; });
  S.rivers.push(rec); return rec; }
