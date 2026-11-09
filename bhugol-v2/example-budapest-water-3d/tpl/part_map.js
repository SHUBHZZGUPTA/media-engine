/* ---------- 3D map: globe + terrain flyover ---------- */
const M3 = D.map3; const [L0, L1, B0, B1] = M3.bbox; const LC = (L0 + L1) / 2, BC = (B0 + B1) / 2, KX = Math.cos(BC * Math.PI / 180);
function map3() {
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
  const st = new T3.Scene(); st.background = new T3.Color(0x0A1424); st.fog = new T3.Fog(0x0A1424, 9, 20);
  const ct = new T3.PerspectiveCamera(32, ASP, .005, 60); ct.up.set(0, 0, 1);
  const Wt = (L1 - L0) * KX, Ht = (B1 - B0), EX = .0105;
  const FR = (() => { const lo = M3.pa.map(p => p[0]), la = M3.pa.map(p => p[1]); return new T3.Vector4((Math.min(...lo) - L0) / (L1 - L0), (Math.min(...la) - B0) / (B1 - B0), (Math.max(...lo) - L0) / (L1 - L0), (Math.max(...la) - B0) / (B1 - B0)); })();
  const TU = { dem: { value: null }, ne: { value: null }, cls: { value: null }, mask: { value: null }, hs: { value: null }, hl: { value: 0 }, exag: { value: 0 }, flag: { value: null }, flagA: { value: 0 }, frect: { value: FR },
    crect: { value: new T3.Vector4((M3.pa_close_bbox[0] - L0) / (L1 - L0), (M3.pa_close_bbox[2] - B0) / (B1 - B0), (M3.pa_close_bbox[1] - L0) / (L1 - L0), (M3.pa_close_bbox[3] - B0) / (B1 - B0)) } };
  const terr = new T3.Mesh(new T3.PlaneGeometry(Wt, Ht, 640, 320), new T3.ShaderMaterial({ uniforms: TU,
    vertexShader: `uniform sampler2D dem; uniform float exag; varying vec2 vUv; void main(){ vUv = uv; vec3 p = position; p.z += texture2D(dem, uv).r * exag; gl_Position = projectionMatrix * modelViewMatrix * vec4(p,1.0); }`,
    fragmentShader: `uniform sampler2D ne, cls, mask, hs, flag; uniform float hl, flagA; uniform vec4 crect, frect; varying vec2 vUv;
      void main(){ vec3 c = texture2D(ne, vUv).rgb;
        vec2 q = (vUv - crect.xy) / (crect.zw - crect.xy); float f = smoothstep(0.0, 0.08, q.x) * smoothstep(1.0, 0.92, q.x) * smoothstep(0.0, 0.08, q.y) * smoothstep(1.0, 0.92, q.y);
        if (f > 0.0) c = mix(c, texture2D(cls, clamp(q, 0.0, 1.0)).rgb, f);
        float h = texture2D(hs, vUv).r; c *= 0.42 + 0.78 * h; float lu = dot(c, vec3(0.299,0.587,0.114)); c = mix(vec3(lu), c, 0.78);
        float m = texture2D(mask, vUv).r; c = mix(c, c * vec3(1.15, 1.02, 0.7) + vec3(0.07, 0.045, 0.0), m * hl * 0.6); c *= mix(1.0, 0.62, hl * (1.0 - m));
        if (flagA > 0.0) { vec2 fq = clamp((vUv - frect.xy) / (frect.zw - frect.xy), 0.0, 1.0); vec3 fc = texture2D(flag, fq).rgb; float lu2 = dot(c, vec3(0.299,0.587,0.114));
          c = mix(c, fc * (0.62 + 0.75 * lu2), m * flagA * 0.8); }
        gl_FragColor = vec4(c, 1.0); }` }));
  st.add(terr);
  const demI = { I: null }; const hAt = (lon, lat) => demI.I ? sampleCPU(demI.I, (lon - L0) / (L1 - L0), (lat - B0) / (B1 - B0)) * EX * 1.0 : 0;
  const wpos = (lon, lat, up) => new T3.Vector3((lon - LC) * KX, lat - BC, hAt(lon, lat) * TU.exag.value / EX + (up || 0));
  // wall ribbon along the PA outline (built after DEM loads)
  const WU = { rise: { value: 0 }, wh: { value: .28 } };
  const wallMat = new T3.ShaderMaterial({ uniforms: WU, transparent: true, depthWrite: false, side: T3.DoubleSide, blending: T3.AdditiveBlending,
    vertexShader: `uniform float rise, wh; attribute float k; varying float vK; void main(){ vK = k; vec3 p = position; p.z += k * wh * rise; gl_Position = projectionMatrix * modelViewMatrix * vec4(p,1.0); }`,
    fragmentShader: `uniform float rise; varying float vK; void main(){ float a = (1.0 - vK) * (1.0 - vK) * rise; gl_FragColor = vec4(1.0, 0.68, 0.18, a * 0.95); }` });
  const pin = new T3.Group(); st.add(pin);
  const beam = new T3.Mesh(new T3.CylinderGeometry(.008, .008, .24, 12, 1, true), new T3.MeshBasicMaterial({ color: 0xFF7A1A, transparent: true, opacity: .0, blending: T3.AdditiveBlending, depthWrite: false }));
  beam.rotation.x = Math.PI / 2; beam.position.z = .12; pin.add(beam);
  const head = new T3.Sprite(new T3.SpriteMaterial({ map: GLOW, color: 0xFF5A1A, transparent: true, blending: T3.AdditiveBlending, depthWrite: false, opacity: 0 })); head.position.z = .24; head.scale.set(.16, .16, 1); pin.add(head);
  const ring = new T3.Mesh(new T3.RingGeometry(.02, .03, 48), new T3.MeshBasicMaterial({ color: 0xFF7A1A, transparent: true, opacity: 0, blending: T3.AdditiveBlending, depthWrite: false, side: T3.DoubleSide })); ring.position.z = .004; pin.add(ring);
  const S = { el, push, ov, cvG, cvT, RG, RT, sg, cg, st, ct, globe, TU, WU, pin, beam, head, ring, labels: [], lls: [], gk: Track({ lon: -92, lat: 34, dist: 3.4 }), tk: Track({ lon: -77.6, lat: 40.9, dist: 5, el: 74, yaw: 0 }),
    x: Track(0), hl: Track(0), rise: Track(0), pinA: Track(0), flagA: Track(0), wpos, ll, lab: null };
  READY.push(tex('globe.jpg').then(t => { globe.material.map = t; globe.material.needsUpdate = true; }), tex('ne.jpg').then(t => TU.ne.value = t), tex('pa_close.jpg').then(t => TU.cls.value = t),
    tex('pa_mask.png').then(t => TU.mask.value = t), tex('flag_hu.png').then(t => TU.flag.value = t), tex('hillshade.png').then(t => TU.hs.value = t), tex('dem8.png', { nearest: 1 }).then(t => TU.dem.value = t),
    cpuImg('dem8.png').then(I => { demI.I = I; TU.exag.value = EX * 26;
      const pts = M3.pa.map(([lo, la]) => wpos(lo, la, .002)); const pos = [], kk = [];
      for (let i = 0; i < pts.length; i++) { const a = pts[i], b = pts[(i + 1) % pts.length]; pos.push(a.x, a.y, a.z, b.x, b.y, b.z, b.x, b.y, b.z, a.x, a.y, a.z, b.x, b.y, b.z, a.x, a.y, a.z); kk.push(0, 0, 1, 0, 1, 1); }
      const g = new T3.BufferGeometry(); g.setAttribute('position', new T3.Float32BufferAttribute(pos, 3)); g.setAttribute('k', new T3.Float32BufferAttribute(kk, 1)); st.add(new T3.Mesh(g, wallMat));
      const cp = wpos(M3.centralia[0], M3.centralia[1]); pin.position.copy(cp); }));
  return S;
}
function renderMap(S, t) {
  const x = valAt(S.x, t); S.cvG.style.opacity = 1 - x; S.cvT.style.opacity = x;
  if (x < 1) { const g = valAt(S.gk, t); const p = S.ll(g.lon, g.lat, g.dist); S.cg.position.copy(p); S.cg.lookAt(0, 0, 0); S.globe.rotation.y = 0; S.RG.render(S.sg, S.cg); }
  if (x > 0) { const k = valAt(S.tk, t); S.TU.hl.value = valAt(S.hl, t); S.TU.flagA.value = valAt(S.flagA, t); S.WU.rise.value = valAt(S.rise, t);
    const tg = new T3.Vector3((k.lon - LC) * KX, k.lat - BC, 0); const e = k.el * Math.PI / 180, y = k.yaw * Math.PI / 180;
    S.ct.position.set(tg.x + Math.sin(y) * Math.cos(e) * k.dist, tg.y - Math.cos(y) * Math.cos(e) * k.dist, Math.sin(e) * k.dist); S.ct.lookAt(tg); S.ct.updateMatrixWorld();
    const pa = valAt(S.pinA, t); S.beam.material.opacity = pa * .8; S.head.material.opacity = pa; const rs = 1 + ((t * .9) % 1) * 5; S.ring.scale.set(rs, rs, 1); S.ring.material.opacity = pa * (1 - (t * .9) % 1);
    for (const h of (S.pre || [])) h(t, k);
    S.RT.render(S.st, S.ct);
    for (const L of S.labels) { const a = valAt(L.a, t); L.e.style.opacity = a * x; if (a <= 0) continue; const q = toScreen(S.ct, S.pin.position.clone().add(new T3.Vector3(0, 0, .34)));
      L.e.style.transform = `translate(${(q.x - L.e.offsetWidth / 2).toFixed(1)}px,${(q.y - L.e.offsetHeight).toFixed(1)}px)`; }
    for (const cd of S.cards) { const a = valAt(cd.a, t); cd.el.style.opacity = a * x; cd.ln.style.opacity = a * x; if (a > 0) { const q = toScreen(S.ct, S.pin.position.clone().add(new T3.Vector3(0, 0, .26)));
      const w = cd.el.offsetWidth, h = cd.el.offsetHeight, cx = clamp(q.x - w / 2, 40, 1040 - w), cy = clamp(q.y - h - 170, 300, 1150 - h);
      cd.el.style.transform = `translate(${cx.toFixed(1)}px,${(cy + (1 - a) * 40).toFixed(1)}px)`; cd.path.setAttribute('d', `M${(cx + w / 2).toFixed(1)} ${(cy + h).toFixed(1)} L${q.x.toFixed(1)} ${q.y.toFixed(1)}`); } }
    for (const L of S.lls) { const a = valAt(L.a, t); L.e.style.opacity = a * x; if (a <= 0) continue; const q = toScreen(S.ct, S.wpos(L.lon, L.lat, .03));
      L.e.style.transform = `translate(${(q.x - L.e.offsetWidth / 2).toFixed(1)}px,${(q.y - L.e.offsetHeight / 2).toFixed(1)}px) scale(${(.6 + .4 * Math.min(1, a * 1.5)).toFixed(3)})`; } } 
}

/* camera of the terrain flyover at time t (pure function of time), for beats pinned to a lon/lat; and lon/lat labels */
function mapProj(S, t, lon, lat, up) { const k = valAt(S.tk, t); const tg = new T3.Vector3((k.lon - LC) * KX, k.lat - BC, 0); const e = k.el * Math.PI / 180, y = k.yaw * Math.PI / 180;
  S.ct.position.set(tg.x + Math.sin(y) * Math.cos(e) * k.dist, tg.y - Math.cos(y) * Math.cos(e) * k.dist, Math.sin(e) * k.dist); S.ct.lookAt(tg); S.ct.updateMatrixWorld();
  return toScreen(S.ct, S.wpos(lon, lat, up || .01)); }
function mapLabel(S, txt, lon, lat, fs, col) { const e = mk('div', { class: 'plbl' }, S.ov); e.textContent = tr(txt); Object.assign(e.style, { fontSize: fs + 'px', webkitTextStrokeWidth: (fs * .18) + 'px', color: col || '' });
  const rec = { e, lon, lat, a: Track(0) }; S.lls.push(rec); return rec; }

