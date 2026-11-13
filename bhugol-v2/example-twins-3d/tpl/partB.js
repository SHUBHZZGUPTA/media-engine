/* ---------- 3D map: globe + terrain (flag fills baked per country) ---------- */
function map3(P, M3, o) {
  const [L0, L1, B0, B1] = M3.bbox; const LC = (L0 + L1) / 2, BC = (B0 + B1) / 2, KX = Math.cos(BC * Math.PI / 180);
  const { el, push } = newScene(); const G = renderer(push), Tn = renderer(push); const ov = mk('div', { class: 'ov' }, push); const chars = mk('div', { class: 'chars' }, push);
  const sg = new T3.Scene(); sg.background = new T3.Color(0x01040A); const cg = new T3.PerspectiveCamera(30, ASP, .01, 100);
  const globe = new T3.Mesh(new T3.SphereGeometry(1, 160, 120), new T3.MeshBasicMaterial({ color: 0xffffff })); sg.add(globe);
  sg.add(new T3.Mesh(new T3.SphereGeometry(1.06, 96, 72), new T3.ShaderMaterial({ side: T3.BackSide, transparent: true, blending: T3.AdditiveBlending, depthWrite: false,
    vertexShader: `varying vec3 vN; varying vec3 vP; void main(){ vN = normalize(normalMatrix * normal); vec4 mv = modelViewMatrix * vec4(position,1.0); vP = mv.xyz; gl_Position = projectionMatrix * mv; }`,
    fragmentShader: `varying vec3 vN; varying vec3 vP; void main(){ float f = pow(clamp(1.0 - abs(dot(normalize(-vP), vN)), 0.0, 1.0), 2.2); gl_FragColor = vec4(0.35, 0.65, 1.0, f * 0.9); }` })));
  { const n = 1400, p = new Float32Array(n * 3); for (let i = 0; i < n; i++) { const a = (i * 2.399963) % (Math.PI * 2), z = 1 - 2 * ((i + .5) / n), r = Math.sqrt(1 - z * z); p.set([Math.cos(a) * r * 30, z * 30, Math.sin(a) * r * 30], i * 3); }
    const g = new T3.BufferGeometry(); g.setAttribute('position', new T3.BufferAttribute(p, 3)); sg.add(new T3.Points(g, new T3.PointsMaterial({ color: 0xffffff, size: 1.6, sizeAttenuation: false, transparent: true, opacity: .7 }))); }
  const ll = (lon, lat, r) => { const ph = (lon + 180) * Math.PI / 180, th = (90 - lat) * Math.PI / 180; return new T3.Vector3(-Math.cos(ph) * Math.sin(th) * r, Math.cos(th) * r, Math.sin(ph) * Math.sin(th) * r); };
  const st = new T3.Scene(); st.background = new T3.Color(0x0A1424); st.fog = new T3.Fog(0x0A1424, o.fog[0], o.fog[1]);
  const ct = new T3.PerspectiveCamera(32, ASP, .005, 400); ct.up.set(0, 0, 1);
  const Wt = (L1 - L0) * KX, Ht = (B1 - B0), EX = .0105;
  const TU = { cl: { value: o.cls === false ? 0 : 1 }, dem: { value: null }, ne: { value: null }, cls: { value: null }, mask: { value: null }, hs: { value: null }, flg: { value: null }, fA: { value: 0 }, fB: { value: 0 }, hl: { value: 0 }, exag: { value: 0 },
    px: { value: new T3.Vector2(2.5 / 4096, 2.5 / 4096 * (M3.bbox[1] - M3.bbox[0]) / (M3.bbox[3] - M3.bbox[2])) },
    crect: { value: new T3.Vector4((M3.pa_close_bbox[0] - L0) / (L1 - L0), (M3.pa_close_bbox[2] - B0) / (B1 - B0), (M3.pa_close_bbox[1] - L0) / (L1 - L0), (M3.pa_close_bbox[3] - B0) / (B1 - B0)) } };
  st.add(new T3.Mesh(new T3.PlaneGeometry(Wt, Ht, 640, 400), new T3.ShaderMaterial({ uniforms: TU,
    vertexShader: `uniform sampler2D dem; uniform float exag; varying vec2 vUv; void main(){ vUv = uv; vec3 p = position; p.z += texture2D(dem, uv).r * exag; gl_Position = projectionMatrix * modelViewMatrix * vec4(p,1.0); }`,
    fragmentShader: `uniform sampler2D ne, cls, mask, hs, flg; uniform float fA, fB, hl, cl; uniform vec4 crect; uniform vec2 px; varying vec2 vUv;
      float idx(vec2 u){ return floor(texture2D(mask, u).r * 255.0 / 40.0 + 0.5); }
      void main(){ vec3 c = texture2D(ne, vUv).rgb;
        vec2 q = (vUv - crect.xy) / (crect.zw - crect.xy); float f = smoothstep(0.0, 0.08, q.x) * smoothstep(1.0, 0.92, q.x) * smoothstep(0.0, 0.08, q.y) * smoothstep(1.0, 0.92, q.y);
        vec3 cc = texture2D(cls, clamp(q, 0.0, 1.0)).rgb; f *= cl * smoothstep(0.03, 0.07, dot(cc, vec3(0.333))); if (f > 0.0) c = mix(c, cc, f);
        float h = texture2D(hs, vUv).r; c *= 0.48 + 0.72 * h; float lu = dot(c, vec3(0.299,0.587,0.114)); c = mix(vec3(lu), c, 0.9);
        float i0 = idx(vUv); float fill = (i0 > 0.5 && i0 < 1.5) ? fA : ((i0 > 1.5 && i0 < 2.5) ? fB : 0.0);
        vec3 fl = texture2D(flg, vUv).rgb * (0.78 + 0.32 * h);
        c = mix(c, fl, fill * 0.9);
        float e = 0.0; for (int k = 0; k < 4; k++) { vec2 d = k == 0 ? vec2(px.x, 0.0) : (k == 1 ? vec2(-px.x, 0.0) : (k == 2 ? vec2(0.0, px.y) : vec2(0.0, -px.y))); float j = idx(vUv + d); if (abs(j - i0) > 0.5) { float fj = (j > 0.5 && j < 1.5) ? fA : ((j > 1.5 && j < 2.5) ? fB : 0.0); e = max(e, max(fill, fj)); } }
        c = mix(c, vec3(1.0), e);
        c *= mix(1.0, 0.55, hl * (fill > 0.01 ? 0.0 : 1.0));
        gl_FragColor = vec4(c, 1.0); }` })));
  const demI = { I: null }; const hAt = (lon, lat) => demI.I ? sampleCPU(demI.I, (lon - L0) / (L1 - L0), (lat - B0) / (B1 - B0)) * EX : 0;
  const wpos = (lon, lat, up) => new T3.Vector3((lon - LC) * KX, lat - BC, hAt(lon, lat) * TU.exag.value / EX + (up || 0));
  const pin = new T3.Group(); st.add(pin);
  const beam = new T3.Mesh(new T3.CylinderGeometry(.03, .03, 1.2, 12, 1, true), new T3.MeshBasicMaterial({ color: 0xFFC23A, transparent: true, opacity: 0, blending: T3.AdditiveBlending, depthWrite: false }));
  beam.rotation.x = Math.PI / 2; beam.position.z = .6; pin.add(beam);
  const head = new T3.Sprite(new T3.SpriteMaterial({ map: GLOW, color: 0xFFC23A, transparent: true, blending: T3.AdditiveBlending, depthWrite: false, opacity: 0 })); head.position.z = 1.2; head.scale.set(.7, .7, 1); pin.add(head);
  // overlay: several rings (true size, already placed in lon/lat), flag texture over their joint bbox; dx/dy offsets in degrees
  const ovs = [];
  function uvGeo(shapes, bb) { const g = new T3.ShapeGeometry(shapes); const p = g.attributes.position; const uvs = [];
    for (let i = 0; i < p.count; i++) uvs.push((p.getX(i) - bb.min.x) / (bb.max.x - bb.min.x), (p.getY(i) - bb.min.y) / (bb.max.y - bb.min.y)); g.setAttribute('uv', new T3.Float32BufferAttribute(uvs, 2)); return g; }
  const toV = ring => ring.map(([lo, la]) => new T3.Vector2((lo - LC) * KX, la - BC));
  function overlay(rings, flagT) { const vs = rings.map(toV); const shapes = vs.map(v => new T3.Shape(v)); const bb = new T3.Box2().setFromPoints(vs.flat());
    const grp = new T3.Group(); st.add(grp);
    const fill = new T3.Mesh(uvGeo(shapes, bb), new T3.MeshBasicMaterial({ map: flagT, transparent: true, opacity: 0, depthWrite: false, depthTest: false })); fill.renderOrder = 6; grp.add(fill);
    const edges = vs.map(v => { const pts = v.map(p => new T3.Vector3(p.x, p.y, 0)); const g = new T3.BufferGeometry().setFromPoints(pts.concat([pts[0]]));
      const m = new T3.Line(g, new T3.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0, depthTest: false })); m.renderOrder = 7; grp.add(m); return m; });
    const sh = new T3.Mesh(new T3.ShapeGeometry(shapes), new T3.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0, depthWrite: false, depthTest: false })); sh.renderOrder = 4; st.add(sh);
    const rec = { grp, fill, edges, sh, bb, a: TK(0), z: TK(2.4), d: TK({ x: 0, y: 0 }), grey: TK(0), cx: (bb.min.x + bb.max.x) / 2, cy: (bb.min.y + bb.max.y) / 2 }; ovs.push(rec); return rec; }
  // morph overlay: ring A -> ring B (same point count), rebuilt when p changes
  function morph(ra, rb, flagT) { const A = toV(ra), B = toV(rb); const bbA = new T3.Box2().setFromPoints(A), bbB = new T3.Box2().setFromPoints(B);
    const mat = new T3.MeshBasicMaterial({ map: flagT, transparent: true, opacity: 0, depthWrite: false, depthTest: false });
    const mesh = new T3.Mesh(new T3.BufferGeometry(), mat); mesh.renderOrder = 6; st.add(mesh);
    const lmat = new T3.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0, depthTest: false }); const line = new T3.Line(new T3.BufferGeometry(), lmat); line.renderOrder = 7; st.add(line);
    const rec = { mesh, line, a: TK(0), p: TK(0), last: -1, z: .05 };
    rec.update = p => { if (Math.abs(p - rec.last) < 1e-4) return; rec.last = p; const pts = A.map((a, i) => new T3.Vector2(a.x + (B[i].x - a.x) * p, a.y + (B[i].y - a.y) * p));
      const bb = new T3.Box2().setFromPoints(pts); mesh.geometry.dispose(); mesh.geometry = uvGeo([new T3.Shape(pts)], bb);
      line.geometry.dispose(); line.geometry = new T3.BufferGeometry().setFromPoints(pts.concat([pts[0]]).map(v => new T3.Vector3(v.x, v.y, 0))); };
    S.morphs.push(rec); return rec; }
  const S = { el, push, ov, chars, G, Tn, sg, cg, st, ct, globe, TU, pin, beam, head, lls: [], cards: [], meas: [], ovs, morphs: [], overlay, morph, wpos, ll, KX, LC, BC,
    gk: TK(Object.assign({ lon: 30, lat: 12, dist: 3.5 }, o.gk0 || {})), tk: TK(Object.assign({ lon: LC, lat: BC, dist: 30, el: 80, yaw: 0 }, o.tk0 || {})), x: TK(o.globe ? 0 : 1), fA: TK(0), fB: TK(0), hl: TK(0), pinA: TK(0), wins: [] };
  READY.push(tex('globe_flags.jpg').then(t => { globe.material.map = t; globe.material.needsUpdate = true; }), tex(P + 'ne.jpg').then(t => TU.ne.value = t), tex(P + 'pa_close.jpg').then(t => TU.cls.value = t),
    tex(P + 'pa_mask.png', { nearest: 1 }).then(t => TU.mask.value = t), tex(P + 'hillshade.png').then(t => TU.hs.value = t), tex(P + 'dem8.png').then(t => TU.dem.value = t), tex(P + 'flags.jpg').then(t => TU.flg.value = t),
    cpuImg(P + 'dem8.png').then(I => { demI.I = I; TU.exag.value = EX * (o.exag || 26); if (o.pin) pin.position.copy(wpos(o.pin[0], o.pin[1])); }));
  S.cam = t => { const k = valAt(S.tk, t); const tg = new T3.Vector3((k.lon - LC) * KX, k.lat - BC, 0); const e = k.el * Math.PI / 180, y = k.yaw * Math.PI / 180;
    ct.position.set(tg.x + Math.sin(y) * Math.cos(e) * k.dist, tg.y - Math.cos(y) * Math.cos(e) * k.dist, Math.sin(e) * k.dist); ct.lookAt(tg); ct.updateMatrixWorld(); };
  S.proj = (t, lon, lat, up) => { S.cam(t); return toScreen(ct, wpos(lon, lat, up || .01)); };
  S.render = t => {
    const x = valAt(S.x, t); G.cv.style.opacity = 1 - x; Tn.cv.style.opacity = x;
    if (x < 1) { const g = valAt(S.gk, t); cg.position.copy(ll(g.lon, g.lat, g.dist)); cg.up.set(0, 1, 0); cg.lookAt(0, 0, 0); G.R.render(sg, cg); }
    if (x > 0) { S.cam(t); TU.fA.value = valAt(S.fA, t); TU.fB.value = valAt(S.fB, t); TU.hl.value = valAt(S.hl, t);
      const pa = valAt(S.pinA, t); beam.material.opacity = pa * .85; head.material.opacity = pa;
      for (const v of ovs) { const a = valAt(v.a, t), z = valAt(v.z, t), d = valAt(v.d, t), gr = valAt(v.grey, t);
        v.fill.material.opacity = a * .95; v.fill.material.color.setRGB(1 - gr * .55, 1 - gr * .55, 1 - gr * .45); v.edges.forEach(e => e.material.opacity = a);
        v.grp.position.set(d.x * KX, d.y, .05 + z * 1.6); v.sh.position.set(d.x * KX + .1 * z + .05, d.y - .14 * z - .07, .02); v.sh.material.opacity = a * .4; }
      for (const m of S.morphs) { const a = valAt(m.a, t); m.mesh.material.opacity = a * .95; m.line.material.opacity = a; m.mesh.position.z = m.line.position.z = .06; if (a > 0) m.update(valAt(m.p, t)); }
      Tn.R.render(st, ct);
      for (const L of S.lls) { const a = valAt(L.a, t); L.e.style.opacity = a * x; if (a <= 0) continue; const dd = L.ov ? valAt(L.ov.d, t) : { x: 0, y: 0 };
        const q = toScreen(ct, wpos(L.lon + dd.x, L.lat + dd.y, .05)); const s = (.6 + .4 * Math.min(1, a * 1.5)) * (1 + valAt(L.pop, t));
        L.e.style.transform = `translate(${(q.x - L.e.offsetWidth / 2).toFixed(1)}px,${(q.y - L.e.offsetHeight / 2 + valAt(L.dy, t)).toFixed(1)}px) scale(${s.toFixed(3)}) rotate(${valAt(L.rot, t).toFixed(1)}deg)`; }
      for (const cd of S.cards) { const a = valAt(cd.a, t); cd.el.style.opacity = a * x; cd.ln.style.opacity = a * x; if (a <= 0) continue;
        const q = toScreen(ct, wpos(cd.lon, cd.lat, .05)); const w = cd.el.offsetWidth, h = cd.el.offsetHeight; const cx = cd.side === 'L' ? 40 : 1040 - w, cy = cd.y + (1 - a) * 40;
        cd.el.style.transform = `translate(${cx}px,${cy.toFixed(1)}px)`; cd.path.setAttribute('d', `M${(cx + w / 2).toFixed(1)} ${(cy + h).toFixed(1)} L${q.x.toFixed(1)} ${q.y.toFixed(1)}`); cd.dot.setAttribute('cx', q.x.toFixed(1)); cd.dot.setAttribute('cy', q.y.toFixed(1)); }
      for (const m of S.meas) { const a = valAt(m.a, t), dr = valAt(m.draw, t); m.svg.style.opacity = a * x; m.lab.style.opacity = a * x; if (a <= 0) continue;
        const p0 = toScreen(ct, wpos(m.p0[0], m.p0[1], .02)), p1 = toScreen(ct, wpos(m.p1[0], m.p1[1], .02)); const ex = p0.x + (p1.x - p0.x) * dr, ey = p0.y + (p1.y - p0.y) * dr;
        m.path.setAttribute('d', `M${p0.x.toFixed(1)} ${p0.y.toFixed(1)} L${ex.toFixed(1)} ${ey.toFixed(1)}`); m.c0.setAttribute('cx', p0.x); m.c0.setAttribute('cy', p0.y); m.c1.setAttribute('cx', ex); m.c1.setAttribute('cy', ey);
        m.lab.style.transform = `translate(${((p0.x + p1.x) / 2 - m.lab.offsetWidth / 2).toFixed(1)}px,${(Math.min(p0.y, p1.y) - m.lab.offsetHeight - 40).toFixed(1)}px)`; } }
  };
  return S;
}
function mapLabel(S, txt, lon, lat, fs, col) { const e = mk('div', { class: 'plbl' }, S.ov); e.innerHTML = txt; Object.assign(e.style, { fontSize: fs + 'px', webkitTextStrokeWidth: (fs * .18) + 'px', color: col || '' });
  const rec = { e, lon, lat, a: TK(0), pop: TK(0), dy: TK(0), rot: TK(0) }; S.lls.push(rec); return rec; }
function mkCard(S, b) { const el = mk('div', { class: 'card' }, S.ov);
  el.innerHTML = `<div class="cin"><div class="crow"><span class="cflag">${b.flag || ''}</span><span>${b.name || ''}</span></div><div class="cbig"><span class="cnum">0</span><span class="csuf">km²</span></div></div>`;
  const svg = mk('svg', { width: 1080, height: 1920, style: 'position:absolute;left:0;top:0;overflow:visible;opacity:0' }, S.ov, true); S.ov.insertBefore(svg, el);
  const path = mk('path', { stroke: '#FFFFFF', 'stroke-width': 6, 'stroke-dasharray': '14 10', fill: 'none' }, svg, true); const dot = mk('circle', { r: 11, fill: '#FFC23A', stroke: '#03101A', 'stroke-width': 4 }, svg, true);
  const c = { el, ln: svg, path, dot, a: TK(0), side: b.side, y: b.y || 250, lon: b.lon, lat: b.lat, num: el.querySelector('.cnum') }; S.cards.push(c); return c; }
function measure(S, p0, p1) { const svg = mk('svg', { width: 1080, height: 1920, style: 'position:absolute;left:0;top:0;overflow:visible;opacity:0' }, S.ov, true);
  const path = mk('path', { stroke: '#FFC23A', 'stroke-width': 10, 'stroke-dasharray': '22 14', 'stroke-linecap': 'round', fill: 'none' }, svg, true);
  const c0 = mk('circle', { r: 16, fill: '#fff', stroke: '#03101A', 'stroke-width': 5 }, svg, true), c1 = mk('circle', { r: 16, fill: '#fff', stroke: '#03101A', 'stroke-width': 5 }, svg, true);
  const lab = mk('div', { class: 'plbl', style: 'font-size:120px;-webkit-text-stroke-width:20px;color:#FFC23A' }, S.ov); lab.innerHTML = '<span class="n">0</span> km';
  const m = { svg, path, c0, c1, lab, p0, p1, a: TK(0), draw: TK(0) }; S.meas.push(m); return m; }
function character(S, kind, cx, cy, sc) {
  const box = mk('div', { class: 'char' }, S.chars); Object.assign(box.style, { left: (cx - 390) + 'px', top: (cy - 390) + 'px', width: '780px', height: '780px' });
  const svg = mk('svg', { width: 780, height: 780, viewBox: '0 0 780 780', style: 'overflow:visible' }, box, true);
  const d = D.shapes[kind]; const id = 'cp_' + kind + '_' + Math.round(cx);
  const defs = mk('defs', {}, svg, true);
  defs.innerHTML = `<clipPath id="${id}"><path d="${d}"/></clipPath><linearGradient id="h${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".45"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <filter id="s${id}" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="22" stdDeviation="14" flood-color="#000" flood-opacity=".5"/></filter>`;
  const body = mk('g', { transform: `translate(${390 - 300 * sc},${390 - 300 * sc}) scale(${sc})`, filter: `url(#s${id})` }, svg, true);
  body.innerHTML = `<path d="${d}" fill="none" stroke="#0b0b0b" stroke-width="30" stroke-linejoin="round"/><path d="${d}" fill="none" stroke="#fff" stroke-width="16" stroke-linejoin="round"/>
    <g clip-path="url(#${id})"><image href="assets/flag_${kind}.png" x="0" y="0" width="600" height="600" preserveAspectRatio="none"/><rect x="0" y="0" width="600" height="270" fill="url(#h${id})"/></g>`;
  const F = D.face[kind]; const face = mk('g', { transform: `translate(${F[0]},${F[1]}) scale(${F[2]})` }, body, true);
  const eyes = mk('g', {}, face, true), extra = mk('g', {}, face, true);
  eyes.innerHTML = `<ellipse cx="-50" cy="0" rx="34" ry="42" fill="#fff" stroke="#111" stroke-width="7"/><ellipse cx="50" cy="0" rx="34" ry="42" fill="#fff" stroke="#111" stroke-width="7"/>
    <circle cx="-44" cy="${kind === 'gb' ? 14 : 6}" r="17" fill="#111"/><circle cx="56" cy="${kind === 'gb' ? 14 : 6}" r="17" fill="#111"/><circle cx="-38" cy="0" r="6" fill="#fff"/><circle cx="62" cy="0" r="6" fill="#fff"/>`;
  let mouthO, mouthC;
  if (kind === 'gb') {
    extra.innerHTML = `<path d="M-88,-58 L-20,-40" stroke="#111" stroke-width="13" stroke-linecap="round"/><path d="M88,-58 L20,-40" stroke="#111" stroke-width="13" stroke-linecap="round" transform="scale(-1,1) rotate(180) scale(-1,-1)"/>
      <path class="tear" d="M-58,40 q-12,26 0,34 q12,-8 0,-34z" fill="#7fd4ff" stroke="#1b5c8a" stroke-width="4"/><path class="tear" d="M58,40 q-12,26 0,34 q12,-8 0,-34z" fill="#7fd4ff" stroke="#1b5c8a" stroke-width="4"/>`;
    mouthO = mk('g', {}, face, true); mouthO.innerHTML = `<path d="M-34,104 Q0,62 34,104 Q0,96 -34,104Z" fill="#3a0a10" stroke="#111" stroke-width="7"/>`;
    mouthC = mk('g', {}, face, true); mouthC.innerHTML = `<path d="M-32,100 Q0,72 32,100" stroke="#111" stroke-width="11" fill="none" stroke-linecap="round"/>`;
  } else {
    extra.innerHTML = `<ellipse cx="-78" cy="52" rx="26" ry="14" fill="#ff6b9a" opacity=".75"/><ellipse cx="78" cy="52" rx="26" ry="14" fill="#ff6b9a" opacity=".75"/>`;
    mouthO = mk('g', {}, face, true); mouthO.innerHTML = `<path d="M-30,70 Q0,112 30,70Z" fill="#5a0f1e" stroke="#111" stroke-width="7"/>`;
    mouthC = mk('g', {}, face, true); mouthC.innerHTML = `<path d="M-30,72 Q0,100 30,72" stroke="#111" stroke-width="11" fill="none" stroke-linecap="round"/>`;
  }
  return { box, eyes, extra, mouthO, mouthC, cx, cy, tears: [...extra.querySelectorAll('.tear')] };
}
