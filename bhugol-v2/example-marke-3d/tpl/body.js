
/* ---------- extra styles (cover headline, clocks, stamp) ---------- */
{ const st = document.createElement('style'); st.textContent = `
#cover { position: absolute; inset: 0; opacity: 0; }
.cvl { position: absolute; left: 40px; width: 1000px; text-align: center; white-space: nowrap; font-family: 'BSD', 'Muk', 'Emo', sans-serif; font-weight: 900; color: #fff; paint-order: stroke fill; -webkit-text-stroke: 26px #03101A; line-height: 1; font-size: 170px; }
.cvl .yb { display: inline-block; background: #FFD21F; color: #03101A; -webkit-text-stroke: 0; padding: 4px 26px 0; border-radius: 14px; box-shadow: 0 0 0 8px #03101A, 0 14px 30px rgba(0,0,0,.45); }
.clk { position: absolute; left: 0; top: 0; opacity: 0; white-space: nowrap; padding: 10px 26px 12px; border-radius: 26px; background: rgba(6,12,22,.86); border: 5px solid #FFFFFF; box-shadow: 0 14px 30px rgba(0,0,0,.5); text-align: center; }
.clk .cf { font-family: 'Emo', sans-serif; font-size: 58px; vertical-align: middle; margin-right: 12px; }
.clk .ct { font-family: 'BSD', sans-serif; font-weight: 900; font-size: 104px; color: #FFD21F; vertical-align: middle; letter-spacing: .02em; }
.stamp { position: absolute; left: 0; width: 1080px; top: 330px; text-align: center; opacity: 0; }
.stamp span { display: inline-block; font-family: 'BSD', 'Muk', 'Emo', sans-serif; font-weight: 900; font-size: 120px; color: #fff; background: #12B76A; padding: 10px 36px 4px; border-radius: 22px; box-shadow: 0 0 0 8px #03101A, 0 16px 34px rgba(0,0,0,.5); transform: rotate(-4deg); }
`; document.head.appendChild(st); }

/* ---------- 3D map: globe + terrain flyover, Sweden/Finland flag fills from pa_cov (R = SE, G = FI) ---------- */
function map3(P, M3, o) {
  const [L0, L1, B0, B1] = M3.bbox; const LC = (L0 + L1) / 2, BC = (B0 + B1) / 2, KX = Math.cos(BC * Math.PI / 180);
  const { el, push } = newScene(); const G = renderer(push), Tn = renderer(push); const ov = mk('div', { class: 'ov' }, push);
  const sg = new T3.Scene(); sg.background = new T3.Color(0x01040A); const cg = new T3.PerspectiveCamera(30, ASP, .01, 100);
  const globe = new T3.Mesh(new T3.SphereGeometry(1, 160, 120), new T3.MeshBasicMaterial({ color: 0xffffff })); sg.add(globe);
  sg.add(new T3.Mesh(new T3.SphereGeometry(1.06, 96, 72), new T3.ShaderMaterial({ side: T3.BackSide, transparent: true, blending: T3.AdditiveBlending, depthWrite: false,
    vertexShader: `varying vec3 vN; varying vec3 vP; void main(){ vN = normalize(normalMatrix * normal); vec4 mv = modelViewMatrix * vec4(position,1.0); vP = mv.xyz; gl_Position = projectionMatrix * mv; }`,
    fragmentShader: `varying vec3 vN; varying vec3 vP; void main(){ float f = pow(clamp(1.0 - abs(dot(normalize(-vP), vN)), 0.0, 1.0), 2.2); gl_FragColor = vec4(0.35, 0.65, 1.0, f * 0.9); }` })));
  { const n = 1400, p = new Float32Array(n * 3); for (let i = 0; i < n; i++) { const a = (i * 2.399963) % (Math.PI * 2), z = 1 - 2 * ((i + .5) / n), r = Math.sqrt(1 - z * z); p.set([Math.cos(a) * r * 30, z * 30, Math.sin(a) * r * 30], i * 3); }
    const g = new T3.BufferGeometry(); g.setAttribute('position', new T3.BufferAttribute(p, 3)); sg.add(new T3.Points(g, new T3.PointsMaterial({ color: 0xffffff, size: 1.6, sizeAttenuation: false, transparent: true, opacity: .7 }))); }
  const ll = (lon, lat, r) => { const ph = (lon + 180) * Math.PI / 180, th = (90 - lat) * Math.PI / 180; return new T3.Vector3(-Math.cos(ph) * Math.sin(th) * r, Math.cos(th) * r, Math.sin(ph) * Math.sin(th) * r); };
  const st = new T3.Scene(); st.background = new T3.Color(0x0A1424); st.fog = new T3.Fog(0x0A1424, o.fog ? o.fog[0] : 30, o.fog ? o.fog[1] : 70);
  const ct = new T3.PerspectiveCamera(32, ASP, .005, 200); ct.up.set(0, 0, 1);
  const Wt = (L1 - L0) * KX, Ht = (B1 - B0), EX = .0105;
  const R4 = r => new T3.Vector4((r[0] - L0) / (L1 - L0), (r[2] - B0) / (B1 - B0), (r[1] - L0) / (L1 - L0), (r[3] - B0) / (B1 - B0));
  const TU = { dem: { value: null }, ne: { value: null }, cls: { value: null }, cov: { value: null }, hs: { value: null }, exag: { value: 0 }, flagA: { value: 0 }, flagB: { value: 0 }, empA: { value: 0 }, sepia: { value: 0 }, edgeA: { value: 0 },
    frS: { value: R4(D.geo.flagS) }, frF: { value: R4(D.geo.flagF) }, crect: { value: R4(M3.pa_close_bbox) } };
  st.add(new T3.Mesh(new T3.PlaneGeometry(Wt, Ht, 640, 320), new T3.ShaderMaterial({ uniforms: TU,
    vertexShader: `uniform sampler2D dem; uniform float exag; varying vec2 vUv; void main(){ vUv = uv; vec3 p = position; p.z += texture2D(dem, uv).r * exag; gl_Position = projectionMatrix * modelViewMatrix * vec4(p,1.0); }`,
    fragmentShader: `uniform sampler2D ne, cls, cov, hs; uniform float flagA, flagB, empA, sepia, edgeA; uniform vec4 crect, frS, frF; varying vec2 vUv;
      void main(){ vec3 c = texture2D(ne, vUv).rgb;
        vec2 q = (vUv - crect.xy) / (crect.zw - crect.xy); float f = smoothstep(0.0, 0.05, q.x) * smoothstep(1.0, 0.95, q.x) * smoothstep(0.0, 0.05, q.y) * smoothstep(1.0, 0.95, q.y);
        vec3 cl = texture2D(cls, clamp(q, 0.0, 1.0)).rgb; float cll = dot(cl, vec3(0.333)); f *= smoothstep(0.03, 0.09, cll);
        f = 0.0;
        float h = texture2D(hs, vUv).r; c *= 0.45 + 0.75 * h; float lu = dot(c, vec3(0.299,0.587,0.114)); c = mix(vec3(lu), c, 0.9); c *= 1.14;
        vec3 cv = texture2D(cov, vUv).rgb; float ms = cv.r, mf = cv.g;
        c = pow(max(c, vec3(0.0)), vec3(0.8)) * 1.12;
        float ld = cv.b; vec3 sea = vec3(0.03, 0.20, 0.38); sea = mix(sea, vec3(0.30, 0.34, 0.33), sepia * 0.8); c = mix(sea, c, ld);
        c = mix(c, vec3(0.72,0.62,0.42) * (0.75 + 0.4 * h), sepia * 0.8 * ld);
        vec2 us = (vUv - frS.xy) / (frS.zw - frS.xy); float cs = max(step(0.3125, us.x) * step(us.x, 0.4375), step(0.4, us.y) * step(us.y, 0.6));
        vec3 fs = mix(vec3(0.0, 0.42, 0.67), vec3(1.0, 0.80, 0.0), cs);
        vec2 uf = (vUv - frF.xy) / (frF.zw - frF.xy); float cf = max(step(0.2778, uf.x) * step(uf.x, 0.4444), step(0.3636, uf.y) * step(uf.y, 0.6364));
        vec3 ff = mix(vec3(0.97), vec3(0.0, 0.21, 0.50), cf);
        c = mix(c, fs * (0.85 + 0.22 * h), ms * flagA * 0.92);
        c = mix(c, ff * (0.85 + 0.22 * h), mf * flagB * 0.92);
        c = mix(c, vec3(0.30, 0.56, 0.36) * (0.8 + 0.3 * h), mf * empA * 0.9);
        float e = max(max(ms * (1.0 - ms), mf * (1.0 - mf)), ld * (1.0 - ld)) * 4.0; c = mix(c, vec3(1.0), clamp(e * 1.6, 0.0, 1.0) * max(edgeA, 0.55));
        gl_FragColor = vec4(c, 1.0); }` })));
  const demI = { I: null }; const hAt = (lon, lat) => demI.I ? sampleCPU(demI.I, (lon - L0) / (L1 - L0), (lat - B0) / (B1 - B0)) * EX : 0;
  const wpos = (lon, lat, up) => new T3.Vector3((lon - LC) * KX, lat - BC, hAt(lon, lat) * TU.exag.value / EX + (up || 0));
  const pin = new T3.Group(); st.add(pin);
  const beam = new T3.Mesh(new T3.CylinderGeometry(.006, .006, .2, 12, 1, true), new T3.MeshBasicMaterial({ color: 0xFF3B30, transparent: true, opacity: 0, blending: T3.AdditiveBlending, depthWrite: false }));
  beam.rotation.x = Math.PI / 2; beam.position.z = .1; pin.add(beam);
  const head = new T3.Sprite(new T3.SpriteMaterial({ map: GLOW, color: 0xFF5A3C, transparent: true, blending: T3.AdditiveBlending, depthWrite: false, opacity: 0 })); head.position.z = .2; head.scale.set(.14, .14, 1); pin.add(head);
  const S = { el, push, ov, G, Tn, sg, cg, st, ct, globe, TU, pin, beam, head, lls: [], cards: [], wpos, ll, KX, LC, BC, wins: [],
    gk: TK({ lon: 20, lat: 30, dist: 3.4 }), tk: TK(Object.assign({ lon: LC, lat: BC, dist: 11, el: 80, yaw: 0 }, o.tk0 || {})), x: TK(o.globe ? 0 : 1),
    pinA: TK(0), flagA: TK(0), flagB: TK(0), empA: TK(0), sepia: TK(0), edgeA: TK(0) };
  READY.push(tex(P + 'globe.jpg').then(t => { globe.material.map = t; globe.material.needsUpdate = true; }), tex(P + 'ne.jpg').then(t => TU.ne.value = t), tex(P + 'pa_close.jpg').then(t => TU.cls.value = t),
    tex(P + 'pa_cov.png').then(t => TU.cov.value = t), tex(P + 'hillshade.png').then(t => TU.hs.value = t), tex(P + 'dem8.png').then(t => TU.dem.value = t),
    cpuImg(P + 'dem8.png').then(I => { demI.I = I; TU.exag.value = EX * 18; pin.position.copy(wpos(M3.pin[0], M3.pin[1])); }));
  S.cam = t => { const k = valAt(S.tk, t); const tg = new T3.Vector3((k.lon - LC) * KX, k.lat - BC, 0); const e = k.el * Math.PI / 180, y = k.yaw * Math.PI / 180;
    ct.position.set(tg.x + Math.sin(y) * Math.cos(e) * k.dist, tg.y - Math.cos(y) * Math.cos(e) * k.dist, Math.sin(e) * k.dist); ct.lookAt(tg); ct.updateMatrixWorld(); };
  S.proj = (t, lon, lat, up) => { S.cam(t); return toScreen(ct, wpos(lon, lat, up || .01)); };
  S.render = t => {
    const x = valAt(S.x, t); G.cv.style.opacity = 1 - x; Tn.cv.style.opacity = x;
    if (x < 1) { const g = valAt(S.gk, t); cg.position.copy(ll(g.lon, g.lat, g.dist)); cg.lookAt(0, 0, 0); G.R.render(sg, cg); }
    if (x > 0) { S.cam(t); for (const k of ['flagA', 'flagB', 'empA', 'sepia', 'edgeA']) TU[k].value = valAt(S[k], t);
      const pa = valAt(S.pinA, t); beam.material.opacity = pa * .85; head.material.opacity = pa; head.scale.setScalar(.12 + .04 * Math.sin(t * 7));
      Tn.R.render(st, ct);
      for (const L of S.lls) { const a = valAt(L.a, t); L.e.style.opacity = a * x; if (a <= 0) continue; const q = toScreen(ct, wpos(L.lon, L.lat, .03));
        L.e.style.transform = `translate(${(q.x - L.e.offsetWidth / 2).toFixed(1)}px,${(q.y - L.e.offsetHeight / 2).toFixed(1)}px) scale(${((.6 + .4 * Math.min(1, a * 1.5)) * (1 + valAt(L.pop, t))).toFixed(3)})`; }
      for (const cd of S.cards) { const a = valAt(cd.a, t); cd.el.style.opacity = a * x; cd.ln.style.opacity = a * x; if (a > 0) { const q = toScreen(ct, pin.position.clone().add(new T3.Vector3(0, 0, .003)));
        const w = cd.el.offsetWidth, h = cd.el.offsetHeight, cx = clamp(q.x - w / 2, 40, 1040 - w), cy = clamp(q.y - h - 190, 300, 1150 - h);
        cd.el.style.transform = `translate(${cx.toFixed(1)}px,${(cy + (1 - a) * 40).toFixed(1)}px)`; cd.path.setAttribute('d', `M${(cx + w / 2).toFixed(1)} ${(cy + h).toFixed(1)} L${q.x.toFixed(1)} ${q.y.toFixed(1)}`); } } }
  };
  return S;
}
function mapLabel(S, txt, lon, lat, fs, col) { const e = mk('div', { class: 'plbl' }, S.ov); e.innerHTML = tr(txt); Object.assign(e.style, { fontSize: fs + 'px', webkitTextStrokeWidth: (fs * .18) + 'px', color: col || '' });
  const rec = { e, lon, lat, a: TK(0), pop: TK(0) }; S.lls.push(rec); return rec; }
function mkCard(S, b) { const el = mk('div', { class: 'card' }, S.ov);
  el.innerHTML = `<div class="cin"><div class="crow"><span class="cflag">${b.flag || ''}</span><span>${b.name || ''}</span></div><div class="cbig"><span class="cnum">0</span><span class="csuf">${b.unit || ''}</span></div>${b.tag ? `<div class="ctag">${b.tag}</div>` : ''}</div>`;
  const svg = mk('svg', { width: 1080, height: 1920, style: 'position:absolute;left:0;top:0;overflow:visible;opacity:0' }, S.ov, true); S.ov.insertBefore(svg, el);
  const path = mk('path', { stroke: '#FF5A3C', 'stroke-width': 6, 'stroke-dasharray': '14 10', fill: 'none' }, svg, true);
  const c = { el, ln: svg, path, a: TK(0), num: el.querySelector('.cnum'), suf: el.querySelector('.csuf') }; S.cards.push(c); return c; }

/* ---------- shared 3D helpers ---------- */
function skyDome(sc, top, hor) { const m = new T3.Mesh(new T3.SphereGeometry(900, 32, 16), new T3.ShaderMaterial({ side: T3.BackSide, depthWrite: false, fog: false,
  uniforms: { top: { value: new T3.Color(top) }, hor: { value: new T3.Color(hor) }, dk: { value: 0 } },
  vertexShader: `varying vec3 vP; void main(){ vP = position; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }`,
  fragmentShader: `uniform vec3 top, hor; uniform float dk; varying vec3 vP; void main(){ float k = clamp(normalize(vP).y * 2.2, 0.0, 1.0); vec3 c = mix(hor, top, pow(k, 0.7)); c = mix(c, vec3(0.03,0.06,0.16) + 0.1 * vec3(0.2,0.3,0.6) * (1.0 - k), dk); gl_FragColor = vec4(c, 1.0); }` })); sc.add(m); return m; }
function camRig(S, cam, ck) { S.camAt = t => { const k = valAt(ck, t); const y = k.yaw * Math.PI / 180, p = k.pitch * Math.PI / 180; const tg = new T3.Vector3(k.x, k.y, k.z || 0);
    cam.position.set(tg.x + Math.sin(y) * Math.cos(p) * k.dist, tg.y + Math.sin(p) * k.dist, tg.z + Math.cos(y) * Math.cos(p) * k.dist); cam.lookAt(tg); cam.updateMatrixWorld(); };
  S.proj = (t, x, y, z) => { S.camAt(t); return toScreen(cam, new T3.Vector3(x, y, z || 0)); }; }
function drawLabels(S, cam, t) { for (const L of S.labels) { const a = valAt(L.a, t); L.e.style.opacity = a; if (a <= 0) continue; const P = L.fn ? L.fn(t) : [L.x, L.y, L.z || 0];
    const q = toScreen(cam, new T3.Vector3(P[0], P[1], P[2])); L.e.style.transform = `translate(${(q.x - L.e.offsetWidth * (L.ax === undefined ? .5 : L.ax)).toFixed(1)}px,${(q.y - L.e.offsetHeight * (L.ay === undefined ? .5 : L.ay)).toFixed(1)}px) scale(${((.6 + .4 * Math.min(1, a * 1.5)) * (1 + valAt(L.pop, t))).toFixed(3)})`; } }
function xLabel(S, html, x, y, z, fs, col, cls) { const e = mk('div', { class: cls || 'plbl' }, S.ov); e.innerHTML = html; Object.assign(e.style, { fontSize: fs + 'px', webkitTextStrokeWidth: (fs * .18) + 'px', color: col || '' });
  const rec = { e, x, y, z, a: TK(0), pop: TK(0) }; S.labels.push(rec); return rec; }

/* ---------- Märket island in code (1 unit = 10 m; world x = east, z = -north, y = up) ---------- */
const MG = D.mk;                          // {ext:[x0,x1,y0,y1], border:[[x,y]...], buildings, lighthouse}
const VH = 1.7;                           // vertical exaggeration
function islH(sd) { return sd > 0 ? (.05 + .2 * Math.min(1, sd / 22) * (2 - Math.min(1, sd / 22))) * VH / 1 : -.4; }
function island3d() {
  const { el, push } = newScene(); const Gr = renderer(push); const ov = mk('div', { class: 'ov' }, push);
  const sc = new T3.Scene(); const sky = skyDome(sc, 0x2F8BFF, 0xD8F1FF); sc.fog = new T3.Fog(0xCBEBFF, 140, 420);
  const cam = new T3.PerspectiveCamera(FOV, ASP, .1, 2000);
  const hemi = new T3.HemisphereLight(0xE8F6FF, 0x405060, .95); sc.add(hemi);
  const sun = new T3.DirectionalLight(0xFFF2DC, 1.15); sun.position.set(-40, 60, 30); sc.add(sun);
  const [x0, x1, y0, y1] = MG.ext; const wx = x1 - x0, wy = y1 - y0, cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
  const IU = { isl: { value: null }, noiseT: { value: NOISE }, tintOld: { value: 0 }, tintNew: { value: 0 }, fiA: { value: 1 }, swapA: { value: 0 }, swapB: { value: 0 }, vh: { value: VH }, dk: { value: 0 },
    sunD: { value: new T3.Vector3(-.5, .75, .4).normalize() }, time: { value: 0 } };
  const rockG = new T3.PlaneGeometry(wx, wy, 440, 290);
  const rock = new T3.Mesh(rockG, new T3.ShaderMaterial({ uniforms: IU,
    vertexShader: `uniform sampler2D isl, noiseT; uniform float vh; varying vec2 vUv; varying float vH; varying float vSd; varying vec3 vW;
      void main(){ vUv = uv; vec3 p = position; float sd = (texture2D(isl, uv).r * 255.0 - 128.0) * 0.5; vSd = sd;
        float n = texture2D(noiseT, uv * vec2(9.0, 6.0)).r * 0.6 + texture2D(noiseT, uv * vec2(31.0, 21.0)).r * 0.4;
        float k = clamp(sd / 22.0, 0.0, 1.0); float h = sd > 0.0 ? (0.05 + 0.2 * k * (2.0 - k)) * vh * (0.75 + 0.5 * n) : -0.4 + 0.3 * clamp(1.0 + sd / 4.0, 0.0, 1.0);
        p.z += h; vH = h; vec4 w = modelMatrix * vec4(p, 1.0); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`,
    fragmentShader: `uniform sampler2D isl, noiseT; uniform float tintOld, tintNew, fiA, swapA, swapB, time, dk; uniform vec3 sunD; varying vec2 vUv; varying float vH; varying float vSd; varying vec3 vW;
      void main(){ vec3 N = normalize(cross(dFdx(vW), dFdy(vW))); if (N.y < 0.0) N = -N; float di = clamp(dot(N, sunD), 0.0, 1.0);
        float n1 = texture2D(noiseT, vUv * vec2(24.0, 16.0)).r, n2 = texture2D(noiseT, vUv * vec2(70.0, 46.0)).r;
        vec3 gr = mix(vec3(0.62, 0.52, 0.50), vec3(0.80, 0.72, 0.68), n1); gr = mix(gr, vec3(0.45, 0.40, 0.40), smoothstep(0.62, 0.8, n2) * 0.6);
        float wet = 1.0 - smoothstep(0.0, 2.5, vSd); gr = mix(gr, gr * 0.55, wet);
        vec3 c = gr * (0.42 + 0.75 * di);
        vec4 m = texture2D(isl, vUv); float so = m.g, sn = m.b;
        vec2 gw = vec2(vW.x, -vW.z); float crS = max(step(abs(gw.x + 5.5), 1.15), step(abs(gw.y + 2.0), 1.15)); float crF = max(step(abs(gw.x - 13.0), 1.25), step(abs(gw.y + 2.6), 1.25));
        vec3 seC = mix(vec3(0.0, 0.33, 0.62), vec3(1.0, 0.80, 0.0), crS), fiC = mix(vec3(0.98, 0.99, 1.0), vec3(0.0, 0.21, 0.52), crF);
        float land = smoothstep(0.0, 0.8, vSd);
        c = mix(c, mix(fiC, seC, so) * (0.7 + 0.4 * di), tintOld * land * 0.86);
        c = mix(c, mix(fiC, seC, sn) * (0.7 + 0.4 * di), tintNew * land * 0.86 * mix(fiA, 1.0, sn));
        float ga = (1.0 - so) * sn, gb = so * (1.0 - sn);     // ga: became Swedish, gb: became Finnish
        float pu = 0.6 + 0.4 * sin(time * 9.0);
        c = mix(c, vec3(1.0, 0.82, 0.10), gb * swapA * land * pu);
        c = mix(c, vec3(1.0, 0.82, 0.10), ga * swapB * land * pu);
        c *= 1.0 - dk * 0.62; c = mix(c, c * vec3(0.55, 0.7, 1.2), dk * 0.5);
        if (vSd < -0.2) discard;
        gl_FragColor = vec4(c, 1.0); }` }));
  rock.material.extensions = { derivatives: true };
  rock.rotation.x = -Math.PI / 2; rock.position.set(cx, 0, -cy); sc.add(rock);
  // sea
  const WU = { time: { value: 0 }, isl: { value: null }, ext: { value: new T3.Vector4(x0, x1, y0, y1) }, noiseT: { value: NOISE }, dk: { value: 0 } };
  const sea = new T3.Mesh(new T3.PlaneGeometry(1600, 1600, 1, 1), new T3.ShaderMaterial({ uniforms: WU, fog: false,
    vertexShader: `varying vec3 vW; void main(){ vec4 w = modelMatrix * vec4(position,1.0); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`,
    fragmentShader: `uniform float time, dk; uniform sampler2D isl, noiseT; uniform vec4 ext; varying vec3 vW;
      void main(){ vec2 g = vec2(vW.x, -vW.z); vec2 u = (g - ext.xy * vec2(1.0, 0.0) - vec2(0.0, ext.z)) ; vec2 uv = vec2((g.x - ext.x) / (ext.y - ext.x), (g.y - ext.z) / (ext.w - ext.z));
        float sd = -60.0; if (uv.x > 0.0 && uv.x < 1.0 && uv.y > 0.0 && uv.y < 1.0) sd = (texture2D(isl, uv).r * 255.0 - 128.0) * 0.5;
        float n = texture2D(noiseT, g * 0.045 + vec2(time * 0.02, time * 0.013)).r * 0.6 + texture2D(noiseT, g * 0.13 - vec2(time * 0.03, -time * 0.02)).r * 0.4;
        vec3 deep = vec3(0.02, 0.42, 0.58), shal = vec3(0.12, 0.74, 0.80);
        vec3 c = mix(deep, shal, smoothstep(-25.0, 0.0, sd) * 0.8); c += (n - 0.5) * 0.10; c += smoothstep(0.78, 0.92, n) * 0.18;
        float fo = smoothstep(-6.0, -0.4, sd) * (1.0 - smoothstep(-0.4, 0.4, sd)); float fl = 0.6 + 0.4 * sin(sd * 2.4 - time * 3.2 + n * 6.0);
        c = mix(c, vec3(0.96, 0.99, 1.0), fo * fl * 0.85);
        float dist = length(vW.xz - cameraPosition.xz); c = mix(c, vec3(0.70, 0.86, 0.96), smoothstep(160.0, 480.0, dist) * 0.65);
        c *= 1.0 - dk * 0.65; gl_FragColor = vec4(c, 1.0); }` }));
  sea.rotation.x = -Math.PI / 2; sea.position.y = .0; sc.add(sea);
  // CPU height for objects
  const isI = { I: null };
  const sdAt = (x, y) => { if (!isI.I) return 1; const u = (x - x0) / wx, v = (y - y0) / wy; const I = isI.I; const px = clamp(Math.round(u * (I.w - 1)), 0, I.w - 1), py = clamp(Math.round((1 - v) * (I.h - 1)), 0, I.h - 1); return (I.d[(py * I.w + px) * 4] - 128) * .5; };
  const sideAt = (x, y, ch) => { if (!isI.I) return 0; const u = (x - x0) / wx, v = (y - y0) / wy; const I = isI.I; const px = clamp(Math.round(u * (I.w - 1)), 0, I.w - 1), py = clamp(Math.round((1 - v) * (I.h - 1)), 0, I.h - 1); return I.d[(py * I.w + px) * 4 + ch] / 255; };
  const hAt = (x, y) => { const sd = sdAt(x, y); const k = clamp(sd / 22, 0, 1); return sd > 0 ? (.05 + .2 * k * (2 - k)) * VH : 0; };
  const W3 = (x, y, up) => new T3.Vector3(x, hAt(x, y) + (up || 0), -y);
  // border ribbon (morph: straight 1809 line -> 1985 S)
  const Bn = []; { const B = MG.border; for (let i = 0; i < B.length - 1; i++) { const a = B[i], b = B[i + 1]; const n = Math.max(2, Math.ceil(Math.hypot(b[0] - a[0], b[1] - a[1]) / .12)); for (let k = 0; k < n; k++) Bn.push([a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n]); } Bn.push(B[B.length - 1]); }
  const cum = [0]; for (let i = 1; i < Bn.length; i++) cum.push(cum[i - 1] + Math.hypot(Bn[i][0] - Bn[i - 1][0], Bn[i][1] - Bn[i - 1][1])); const TOT = cum[cum.length - 1];
  const A0 = Bn[0], A1 = Bn[Bn.length - 1]; const Bo = Bn.map((p, i) => [A0[0] + (A1[0] - A0[0]) * cum[i] / TOT, A0[1] + (A1[1] - A0[1]) * cum[i] / TOT]);
  const NP = Bn.length; const rpos = new Float32Array(NP * 2 * 3), ru = new Float32Array(NP * 2), rs = new Float32Array(NP * 2), ridx = [];
  for (let i = 0; i < NP; i++) { ru[i * 2] = ru[i * 2 + 1] = cum[i] / TOT; rs[i * 2] = -1; rs[i * 2 + 1] = 1; if (i < NP - 1) { const a = i * 2; ridx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2); } }
  const mkRib = (w, core) => { const g = new T3.BufferGeometry(); g.setAttribute('position', new T3.BufferAttribute(rpos, 3)); g.setAttribute('u', new T3.BufferAttribute(ru, 1)); g.setAttribute('s', new T3.BufferAttribute(rs, 1)); g.setIndex(ridx);
    const U = { prog: { value: 0 }, alpha: { value: 0 }, time: { value: 0 }, pulse: { value: -1 } };
    const m = new T3.Mesh(g, new T3.ShaderMaterial({ uniforms: U, transparent: true, depthTest: false, depthWrite: false, blending: core ? T3.NormalBlending : T3.AdditiveBlending,
      vertexShader: `attribute float u, s; varying float vU, vS; void main(){ vU = u; vS = s; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }`,
      fragmentShader: core ? `uniform float prog, alpha, pulse; varying float vU, vS; void main(){ if (vU > prog) discard; float e = 1.0 - smoothstep(0.55, 1.0, abs(vS)); float p = exp(-pow((vU - pulse) * 14.0, 2.0)); gl_FragColor = vec4(mix(vec3(1.0, 0.25, 0.18), vec3(1.0, 0.95, 0.6), p), alpha * e); }`
        : `uniform float prog, alpha, time; varying float vU, vS; void main(){ if (vU > prog) discard; float e = pow(1.0 - abs(vS), 2.0); gl_FragColor = vec4(1.0, 0.3, 0.15, alpha * e * (0.55 + 0.15 * sin(time * 6.0 + vU * 30.0))); }` }));
    m.renderOrder = core ? 11 : 10; m.frustumCulled = false; sc.add(m); return { m, U, w }; };
  const ribG = mkRib(.75, false), ribC = mkRib(.26, true);
  let lastMorph = -1;
  const setRibbon = mo => { if (Math.abs(mo - lastMorph) < 1e-4 || !isI.I) return; lastMorph = mo; const P = Bn.map((p, i) => [Bo[i][0] + (p[0] - Bo[i][0]) * mo, Bo[i][1] + (p[1] - Bo[i][1]) * mo]);
    for (const R of [ribG, ribC]) { const pa = R.m.geometry.attributes.position.array;
      for (let i = 0; i < NP; i++) { const a = P[Math.max(0, i - 1)], b = P[Math.min(NP - 1, i + 1)]; let dx = b[0] - a[0], dy = b[1] - a[1]; const l = Math.hypot(dx, dy) || 1; dx /= l; dy /= l;
        const nx = -dy * R.w / 2, ny = dx * R.w / 2; const h = Math.max(hAt(P[i][0], P[i][1]), .05) + .09;
        pa.set([P[i][0] + nx, h, -(P[i][1] + ny)], i * 6); pa.set([P[i][0] - nx, h, -(P[i][1] - ny)], i * 6 + 3); }
      R.m.geometry.attributes.position.needsUpdate = true; } };
  // lighthouse + keeper buildings
  const LH = new T3.Group(); sc.add(LH);
  const stoneM = new T3.MeshStandardMaterial({ color: 0xF2EEE6, roughness: .8 }), redM = new T3.MeshStandardMaterial({ color: 0xD8261B, roughness: .55 }), roofM = new T3.MeshStandardMaterial({ color: 0x4A4F57, roughness: .7 });
  const glassM = new T3.MeshStandardMaterial({ color: 0xFFE9A0, emissive: 0xFFC94A, emissiveIntensity: .9, roughness: .2 });
  for (const q of MG.buildings) { if (q.length < 3) continue; const sh = new T3.Shape(q.map(([x, y]) => new T3.Vector2(x, y)));
    const g = new T3.ExtrudeGeometry(sh, { depth: .5, bevelEnabled: false }); g.rotateX(-Math.PI / 2); const m = new T3.Mesh(g, stoneM); LH.add(m);
    const r = new T3.Mesh(new T3.ExtrudeGeometry(sh, { depth: .07, bevelEnabled: false }).rotateX(-Math.PI / 2), roofM); r.position.y = .5; LH.add(r); }
  const twr = new T3.Group(); LH.add(twr);
  const t1 = new T3.Mesh(new T3.CylinderGeometry(.27, .36, 1.15, 6), stoneM); t1.position.y = .575; twr.add(t1);
  const t2 = new T3.Mesh(new T3.CylinderGeometry(.29, .29, .16, 6), redM); t2.position.y = 1.2; twr.add(t2);
  const t3 = new T3.Mesh(new T3.CylinderGeometry(.2, .2, .26, 12), glassM); t3.position.y = 1.41; twr.add(t3);
  const t4 = new T3.Mesh(new T3.ConeGeometry(.25, .24, 12), redM); t4.position.y = 1.66; twr.add(t4);
  const BEAM = new T3.Group(); BEAM.position.y = 1.41; twr.add(BEAM);
  const bU = { a: { value: 0 } };
  for (const s of [1, -1]) { const g = new T3.ConeGeometry(2.6, 26, 32, 1, true); g.translate(0, -13, 0); g.rotateZ(s * Math.PI / 2);
    const m = new T3.Mesh(g, new T3.ShaderMaterial({ uniforms: bU, transparent: true, depthWrite: false, blending: T3.AdditiveBlending, side: T3.DoubleSide,
      vertexShader: `varying float vL; void main(){ vL = length(position) / 26.0; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }`,
      fragmentShader: `uniform float a; varying float vL; void main(){ gl_FragColor = vec4(1.0, 0.92, 0.6, a * 0.28 * (1.0 - vL)); }` })); BEAM.add(m); }
  const S = { el, push, ov, G: Gr, sc, cam, sky, IU, WU, labels: [], wins: [], W3, hAt, sideAt, LH, twr, BEAM, setRibbon, ribG, ribC, Bn, cum, TOT,
    ck: TK({ x: 5.5, y: 0, z: 2, dist: 80, yaw: 70, pitch: 58 }), tintOld: TK(0), tintNew: TK(0), fiA: TK(1), swapA: TK(0), swapB: TK(0), morph: TK(1), prog: TK(1), ribA: TK(0), pulse: TK(-1),
    lhRise: TK(1), beamA: TK(0), beamSpin: TK(0), dk: TK(0) };
  camRig(S, cam, S.ck);
  READY.push(tex('isl.png').then(t => { t.flipY = true; t.needsUpdate = true; IU.isl.value = t; WU.isl.value = t; }), cpuImg('isl.png').then(I => { isI.I = I; LH.position.y = 0; S.setRibbon(1.0001); }));
  S.render = t => { S.camAt(t); IU.time.value = WU.time.value = t;
    for (const k of ['tintOld', 'tintNew', 'fiA', 'swapA', 'swapB']) IU[k].value = valAt(S[k], t);
    const dk = valAt(S.dk, t); IU.dk.value = WU.dk.value = dk; sky.material.uniforms.dk.value = dk; sun.intensity = 1.15 * (1 - dk * .7); hemi.intensity = .95 * (1 - dk * .55);
    S.setRibbon(valAt(S.morph, t)); const pr = valAt(S.prog, t), ra = valAt(S.ribA, t);
    ribG.U.prog.value = ribC.U.prog.value = pr; ribG.U.alpha.value = ribC.U.alpha.value = ra; ribG.U.time.value = t; ribC.U.pulse.value = valAt(S.pulse, t);
    const lr = valAt(S.lhRise, t); LH.scale.set(1, Math.max(.001, lr), 1); LH.visible = lr > .002;
    bU.a.value = valAt(S.beamA, t) * Math.min(1, lr); BEAM.rotation.y = t * 1.6 + valAt(S.beamSpin, t);
    glassM.emissiveIntensity = .9 + dk * 1.2;
    Gr.R.render(sc, cam); drawLabels(S, cam, t);
    for (const K of S.clocks || []) K.draw(t); if (S.walker) S.walker.draw(t); };
  return S;
}

/* ---------- build scenes ---------- */
const MK = island3d(), MK2 = island3d();
const MW = map3('mk/', D.maps.mk, { globe: true, fog: [30, 70] });
const MH = map3('mk/', D.maps.mk, { globe: false, fog: [30, 70], tk0: { lon: 19.4, lat: 60.4, dist: 7.0, el: 72, yaw: 0 } });
const REG = { MK, MK2, MW, MH }; const SCENES = [MK, MK2, MW, MH];
const XF = BhugolXfade(T3, $('cshake'));
const G = D.geo, PIN = D.maps.mk.pin;
// map labels
MW.lSE = mapLabel(MW, 'SWEDEN', 16.0, 61.2, 96, '#FFFFFF'); MW.lFI = mapLabel(MW, 'FINLAND', 23.2, 61.6, 96, '#FFFFFF');
MW.lMK = mapLabel(MW, 'MÄRKET', PIN[0] + .05, PIN[1] - .28, 62, '#FFD21F');
MH.lSE = mapLabel(MH, 'SWEDEN', 18.05, 60.75, 74, '#FFFFFF'); MH.lRU = mapLabel(MH, 'RUSSIAN<br>EMPIRE', 21.85, 61.05, 78, '#FFFFFF');
// island labels (positions in units: x east, y north -> world [x, h, -y])
const P3 = (S, x, y, up) => { const v = S.W3(x, y, up || 0); return [v.x, v.y, v.z]; };
for (const S of [MK, MK2]) {
  S.seals = [[-9.6, -4.2], [-6.5, -10.2], [16.5, -8.6], [1.6, -10.6]].map(([x, y]) => { const L = xLabel(S, '🦭', 0, 0, 0, 92, '', 'emo'); L.fn = () => P3(S, x, y, .25); return L; });
  S.coffee = xLabel(S, '☕', 0, 0, 0, 130, '', 'emo'); S.coffee.fn = () => P3(S, 9.5, 4.5, 1.6);
  S.angry = xLabel(S, '😠', 0, 0, 0, 150, '', 'emo'); S.angry.fn = () => P3(S, -7.5, -1.5, 1.8);
  S.cool = xLabel(S, '😎', 0, 0, 0, 120, '', 'emo'); S.cool.fn = () => [0, 2.25, 0];
  S.sleep = xLabel(S, '😴', 0, 0, 0, 160, '', 'emo'); S.sleep.fn = () => P3(S, -7.0, -2.5, 1.6);
  S.lSE = xLabel(S, '🇸🇪', 0, 0, 0, 120, '', 'emo'); S.lSE.fn = () => P3(S, -4.0, 4.5, 1.0);
  S.lFI = xLabel(S, '🇫🇮', 0, 0, 0, 120, '', 'emo'); S.lFI.fn = () => P3(S, 15.5, -1.5, 1.0);
  // clocks over each half
  const mkClock = (flag, x, y) => { const e = mk('div', { class: 'clk' }, S.ov); e.innerHTML = `<span class="cf">${flag}</span><span class="ct">12:00</span>`; const ct = e.querySelector('.ct');
    const K = { e, ct, a: TK(0), val: null, x, y, txt: t => '12:00', draw: t => { const a = valAt(K.a, t); e.style.opacity = a; if (a <= 0) return; const v = K.txt(t); if (v !== K.val) { ct.textContent = v; K.val = v; }
      const qx = K.sx === 'L' ? 70 : 1010 - e.offsetWidth; e.style.transform = `translate(${qx}px,${K.sy}px) scale(${(.7 + .3 * Math.min(1, a * 1.4)).toFixed(3)})`; } };
    return K; };
  S.ckSE = mkClock('🇸🇪', -7.5, -3.0); S.ckFI = mkClock('🇫🇮', 16.0, -2.5); S.ckSE.sx = 'L'; S.ckSE.sy = 560; S.ckFI.sx = 'R'; S.ckFI.sy = 1010; S.ckFI.txt = () => '13:00';
  S.clocks = [S.ckSE, S.ckFI];
}
/* ---------- titles, cover, captions ---------- */
const TT = {};
for (const t of D.titles) { const g = mk('div', { class: 'ttl', id: t.id }, $('titles')); const lines = [];
  t.lines.forEach((ln0, i) => { const size = 132; const d = mk('div', { class: 'tl big' }, g); Object.assign(d.style, { fontSize: size + 'px', top: (300 + i * 124 - size * .8) + 'px', webkitTextStrokeWidth: (size * .14) + 'px' }); markup(ln0, d); lines.push(d); });
  TT[t.id] = { g, t, lines }; }
const COV = mk('div', { id: 'cover' }, $('titles'));
D.cover.forEach((ln, i) => { const d = mk('div', { class: 'cvl' }, COV); d.style.top = (250 + i * 200) + 'px'; d.innerHTML = ln.replace(/\[(.+?)\]/g, '<span class="yb">$1</span>'); });
const STAMP = mk('div', { class: 'stamp' }, $('titles')); STAMP.innerHTML = `<span>${tr('SAME AREA ✓')}</span>`;
const CAPS = D.chunks.map(c => { const g = mk('div', { class: 'cap' }, $('caps'));
  const lines = c.txt.split('|').map(ln => { const d = mk('div', { class: 'cl' }, g); markup(ln, d); return d; });
  return { c, g, lines, words: [...g.querySelectorAll('span')] }; });
function layout() {
  for (const K of CAPS) { let fs = 92; K.g.style.opacity = 1;
    for (const d of K.lines) { d.style.fontSize = '92px'; const w = d.scrollWidth; if (w > 740) fs = Math.min(fs, 92 * 740 / w); }
    K.g.style.opacity = 0; const n = K.lines.length;
    K.lines.forEach((d, i) => Object.assign(d.style, { fontSize: fs.toFixed(1) + 'px', webkitTextStrokeWidth: (fs * .17).toFixed(1) + 'px', top: (1385 + (i - (n - 1) / 2) * fs - fs * .5).toFixed(1) + 'px' })); }
  for (const id in TT) { const { g, lines } = TT[id]; g.style.opacity = 1;
    for (const d of lines) { const w = d.scrollWidth, fs = parseFloat(d.style.fontSize); if (w > 960) d.style.fontSize = (fs * 960 / w).toFixed(1) + 'px'; }
    g.style.opacity = 0; }
  COV.style.opacity = 1; for (const d of COV.children) { d.style.fontSize = '170px'; const w = d.scrollWidth; if (w > 1000) d.style.fontSize = (170 * 1000 / w).toFixed(1) + 'px'; } COV.style.opacity = 0;
}

/* ---------- timeline ---------- */
function build() {
  layout();
  const tl = gsap.timeline({ paused: true }); const IR = { immediateRender: false };
  const MO = BhugolMotion(tl, { xfade: true });
  const PL = D.shots.map(s => ({ S: REG[s.scene], el: REG[s.scene].el, at: s.t, cut: s.cut }));
  PL.forEach((p, i) => { p.S.wins.push([i ? p.at - .45 : 0, i < PL.length - 1 ? PL[i + 1].at + .1 : D.dur + 1]); });
  MO.shots(PL); tl.set(PL[0].el, { opacity: 1 }, 0);
  for (const b of D.beats || []) if (b.kind === 'punch') MO.punch(REG[b.scene].push, b.t, b.level, b.back);
  const on = (T, at, d, v, e) => key(T, v === undefined ? 1 : v, at, d || .4, e || 'power1.inOut');
  const off = (T, at, d) => key(T, 0, at, d || .25, 'power1.inOut');
  const set = (T, v, at) => key(T, v, at, .01, 'none');
  const shake = (at, k) => MO.shake(at, .6, 'rig-6d-wobble', k || .75);
  const pop = (L, at) => { key(L.pop, .35, at, .09, 'power2.out'); key(L.pop, 0, at + .09, .32, 'power2.inOut'); };
  const emo = (L, at, until) => { on(L.a, at - .05, .18, 1, 'back.out(2)'); pop(L, at + .05); off(L.a, until); };
  const COVER = D.cover_cam, DUR = D.dur;
  const camK = (S, v, at, d, e) => key(S.ck, v, at, d, e || 'power2.inOut');
  // present-day island state for both instances (frame 0)
  for (const S of [MK, MK2]) { set(S.tintNew, 1, -1); set(S.ribA, 1, -1); set(S.morph, 1, -1); set(S.prog, 1, -1); set(S.lhRise, 1, -1); }

  // ===== MK: hook — cover pose (frame 0 = loop seam), push in; two countries, two clocks (L0-L2) =====
  set(MK.ck, COVER, -1); camK(MK, Object.assign({}, COVER, { dist: COVER.dist * .86, yaw: COVER.yaw - 8 }), .05, C(2, 0) - .05, 'power2.out');
  on(MK.lSE.a, C(0, 1, 0), .25, 1, 'back.out(2)'); on(MK.lFI.a, C(0, 1, .25), .25, 1, 'back.out(2)'); off(MK.lSE.a, C(1, 0, -.1)); off(MK.lFI.a, C(1, 0, -.1));
  on(MK.ckSE.a, C(0, 2, 0), .3, 1, 'back.out(1.6)'); on(MK.ckFI.a, C(0, 2, .12), .3, 1, 'back.out(1.6)');
  MK.ckFI.txt = t => t < C(1, 1, .1) ? '12:00' : '13:00';   // one step -> the clock jumps
  off(MK.ckSE.a, C(2, 0, -.15)); off(MK.ckFI.a, C(2, 0, -.15));
  // L2: Sweden half, Finland half, the zigzag border, coffee
  set(MK.tintNew, 0, C(2, 0, -.2)); set(MK.fiA, 0, C(2, 0, -.2)); key(MK.tintNew, 1, C(2, 0, 0), .1, 'power3.out'); key(MK.fiA, 1, C(2, 1, 0), .1, 'power3.out');
  key(MK.ribA, .25, C(2, 0, -.2), .2); key(MK.ribA, 1, C(2, 2, 0), .3); set(MK.prog, 0, C(2, 2, -.05)); key(MK.prog, 1, C(2, 2, 0), C(2, 4) - C(2, 2, 0), 'power2.inOut');
  camK(MK, { x: 5.0, y: 0, z: 1.5, dist: COVER.dist * .62, yaw: COVER.yaw + 6, pitch: 66 }, C(2, 0), C(3, 0) - C(2, 0) + .2, 'sine.inOut');
  emo(MK.coffee, C(2, 4, 0), C(3, 0, -.2));
  // ===== MW: this is Märket — the Baltic, Sweden + Finland, pin (L3 chunks 0-1) =====
  set(MW.x, 1, -1); set(MW.flagA, 1, -1); set(MW.flagB, 1, -1); set(MW.edgeA, 1, -1);
  set(MW.tk, { lon: 19.2, lat: 60.0, dist: 3.0, el: 78, yaw: 0 }, -1); key(MW.tk, { lon: 19.4, lat: 60.25, dist: 7.6, el: 70, yaw: -6 }, C(3, 0, -.15), C(3, 2) - C(3, 0, -.15) + .1, 'power3.out');
  on(MW.pinA, C(3, 0, .1), .3); on(MW.lMK.a, C(3, 0, .2), .3); pop(MW.lMK, C(3, 0, .25)); on(MW.lSE.a, C(3, 0, .35), .3); on(MW.lFI.a, C(3, 0, .5), .3);
  // ===== MK2: no trees, no people, just seals (L3 chunks 2-3) =====
  set(MK2.ck, { x: 4, y: 0, z: 3, dist: 30, yaw: 40, pitch: 34 }, 0); camK(MK2, { x: 2, y: 0, z: 4, dist: 24, yaw: 30, pitch: 28 }, C(3, 2, -.1), C(4, 0) - C(3, 2, -.1) + .2, 'sine.inOut');
  set(MK2.tintNew, 0, 0); set(MK2.ribA, 0, 0);
  MK2.seals.forEach((L, i) => { on(L.a, C(3, 3, -.05 + i * .12), .2, 1, 'back.out(2)'); pop(L, C(3, 3, i * .12)); off(L.a, C(4, 0, -.2)); });
  // ===== MK: who drew this mess? (L4) =====
  set(MK.tintNew, .55, C(4, 0, -.4)); set(MK.ribA, 1, C(4, 0, -.4)); set(MK.prog, 1, C(4, 0, -.4));
  set(MK.ck, { x: 5.5, y: 0, z: 1.5, dist: COVER.dist * .58, yaw: COVER.yaw - 4, pitch: 70 }, C(4, 0, -.4)); camK(MK, { x: 5.5, y: 0, z: 1.5, dist: COVER.dist * .52, yaw: COVER.yaw + 2, pitch: 72 }, C(4, 0, -.1), C(5, 0) - C(4, 0, -.1) + .2, 'sine.inOut');
  key(MK.pulse, 1.3, C(4, 0, .1), 1.1, 'power1.inOut');
  // ===== MH: 1809 — sepia map, Finland to the Russian Empire (L5) =====
  set(MH.sepia, 1, 0); set(MH.flagA, .0, 0); set(MH.edgeA, .6, 0);
  key(MH.tk, { lon: 20.4, lat: 60.7, dist: 12.0, el: 82, yaw: 4 }, C(5, 0, -.15), C(6, 1) - C(5, 0, -.15), 'sine.inOut');
  on(MH.lSE.a, C(5, 1, 0), .3); on(MH.flagA, C(5, 1, 0), .35, .55); on(MH.empA, C(5, 2, -.05), .45); on(MH.lRU.a, C(5, 2, .1), .3); pop(MH.lRU, C(5, 2, .15));
  on(MH.pinA, C(6, 0, 0), .3);
  // ===== MK: the new border — a straight line through the rock; 1885 lighthouse (L6 c1 - L8) =====
  set(MK.tintNew, 0, C(6, 1, -.5)); set(MK.morph, 0, C(6, 1, -.5)); set(MK.prog, 0, C(6, 1, -.5)); set(MK.ribA, 1, C(6, 1, -.5)); set(MK.lhRise, 0, C(6, 1, -.5));
  set(MK.ck, { x: 6, y: 0, z: 2, dist: COVER.dist * .78, yaw: COVER.yaw - 20, pitch: 64 }, C(6, 1, -.5)); camK(MK, { x: 4, y: 0, z: 1.5, dist: COVER.dist * .66, yaw: COVER.yaw - 10, pitch: 58 }, C(6, 1, -.1), C(7, 1) - C(6, 1, -.1), 'sine.inOut');
  key(MK.prog, 1, C(6, 1, 0), C(6, 2, .5) - C(6, 1, 0), 'power2.inOut');
  camK(MK, { x: 3.5, y: 0, z: 1, dist: COVER.dist * .5, yaw: COVER.yaw - 4, pitch: 62 }, C(6, 2, 0), .5, 'power3.out');
  key(MK.lhRise, 1, C(7, 1, 0), .9, 'back.out(1.3)');
  camK(MK, { x: 1.5, y: .6, z: 0, dist: 19, yaw: COVER.yaw - 30, pitch: 24 }, C(7, 1, .2), .55, 'power3.out');
  camK(MK, { x: 1.2, y: .7, z: 0, dist: 13, yaw: COVER.yaw - 38, pitch: 18 }, C(7, 3, 0), .45, 'power3.out');
  // L8: small problem — that point was in Sweden (old Swedish half lights up)
  key(MK.tintOld, 1, C(8, 1, 0), .3);
  camK(MK, { x: 2.5, y: .5, z: 0, dist: 21, yaw: COVER.yaw - 50, pitch: 30 }, C(8, 1, 0), .5, 'power3.out');
  // ===== MK2: Sweden not thrilled; the lighthouse liked the view (L9-L10) =====
  set(MK2.tintOld, 1, C(9, 0, -.5)); set(MK2.tintNew, 0, C(9, 0, -.5)); set(MK2.morph, 0, C(9, 0, -.5)); set(MK2.ribA, 1, C(9, 0, -.5)); set(MK2.prog, 1, C(9, 0, -.5));
  set(MK2.ck, { x: -3, y: .8, z: 1, dist: 17, yaw: -70, pitch: 20 }, C(9, 0, -.5)); camK(MK2, { x: -2, y: .8, z: .5, dist: 14, yaw: -60, pitch: 18 }, C(9, 0, -.1), C(10, 0) - C(9, 0, -.1), 'sine.inOut');
  emo(MK2.angry, C(9, 0, .55), C(10, 0, -.15)); emo(MK2.lSE, C(9, 0, .1), C(10, 0, -.15));
  camK(MK2, { x: 0, y: 1.4, z: 0, dist: 7.5, yaw: -35, pitch: 6 }, C(10, 0, -.2), .9, 'power3.out');
  on(MK2.beamA, C(10, 0, 0), .4); camK(MK2, { x: 0, y: 1.5, z: 0, dist: 7.0, yaw: -10, pitch: 4 }, C(10, 0, .7), C(11, 0) - C(10, 0, .7) + .2, 'sine.inOut');
  emo(MK2.cool, C(10, 1, .1), C(11, 0, -.15));
  // ===== MK: there it stood, in the wrong country, for 100 years (L11) =====
  set(MK.tintOld, 1, C(11, 0, -.5)); set(MK.beamA, 1, C(11, 0, -.5));
  set(MK.ck, { x: 5, y: 0, z: 2, dist: COVER.dist * .8, yaw: COVER.yaw + 25, pitch: 40 }, C(11, 0, -.5)); camK(MK, { x: 5, y: 0, z: 2, dist: COVER.dist * .72, yaw: COVER.yaw + 70, pitch: 44 }, C(11, 0, -.1), C(12, 0) - C(11, 0, -.1) + .2, 'none');
  { const a = C(11, 0, 0), b = C(12, 0, -.2), n = 5; for (let i = 0; i < n; i++) { const s = a + (b - a) * i / n, d = (b - a) / n; key(MK.dk, .85, s, d * .45, 'sine.inOut'); key(MK.dk, 0, s + d * .5, d * .45, 'sine.inOut'); } }
  // ===== MW: the fix is even weirder (L12) =====
  set(MW.tk, { lon: 19.15, lat: 60.25, dist: 4.4, el: 74, yaw: 10 }, C(12, 0, -.5)); key(MW.tk, { lon: 19.13, lat: 60.29, dist: 2.6, el: 80, yaw: 2 }, C(12, 0, -.15), C(13, 0) - C(12, 0, -.15) + .2, 'power2.in');
  set(MW.pinA, 1, C(12, 0, -.5)); set(MW.lMK.a, 0, C(12, 0, -.5)); set(MW.lSE.a, 0, C(12, 0, -.5)); set(MW.lFI.a, 0, C(12, 0, -.5));
  // ===== MK2: 1985 — they moved the border (L13-L15) =====
  set(MK2.tintOld, 0, C(13, 0, -.5)); set(MK2.tintNew, 0, C(13, 0, -.5)); set(MK2.morph, 0, C(13, 0, -.5)); set(MK2.prog, 1, C(13, 0, -.5)); set(MK2.ribA, 1, C(13, 0, -.5)); set(MK2.beamA, .6, C(13, 0, -.5));
  set(MK2.ck, { x: 5, y: 0, z: 1.5, dist: COVER.dist * .74, yaw: COVER.yaw, pitch: 84 }, C(13, 0, -.5)); camK(MK2, { x: 5, y: 0, z: 1.5, dist: COVER.dist * .68, yaw: COVER.yaw - 6, pitch: 84 }, C(13, 0, -.1), C(13, 2, -.1) - C(13, 0, -.1), 'sine.inOut');
  set(MK2.tintOld, 0, C(13, 0, -.5)); key(MK2.morph, 1, C(13, 2, -.05), .9, 'power3.inOut');
  camK(MK2, { x: 4.5, y: 0, z: 1.2, dist: COVER.dist * .58, yaw: COVER.yaw - 10, pitch: 84 }, C(13, 2, -.05), .45, 'power3.out');
  camK(MK2, { x: 4.5, y: 0, z: 1.2, dist: COVER.dist * .64, yaw: COVER.yaw + 8, pitch: 80 }, C(14, 0, 0), .5, 'power3.out');
  camK(MK2, { x: 4.0, y: 0, z: 1.5, dist: COVER.dist * .56, yaw: COVER.yaw + 4, pitch: 78 }, C(14, 2, 0), .45, 'power3.out');
  key(MK2.pulse, -.2, C(14, 0, -.2), .01); key(MK2.pulse, 1.2, C(14, 0, 0), C(14, 2) - C(14, 0) + .3, 'power1.inOut');
  key(MK2.tintNew, 1, C(15, 0, -.1), .35);
  key(MK2.swapA, 1, C(15, 0, .1), .3); key(MK2.swapA, 0, C(15, 1, -.05), .25); key(MK2.swapB, 1, C(15, 1, .1), .3); key(MK2.swapB, 0, C(16, 0, -.2), .25);
  camK(MK2, { x: 3, y: 0, z: 1.0, dist: COVER.dist * .5, yaw: COVER.yaw + 10, pitch: 74 }, C(15, 0, -.1), .5, 'power3.out');
  camK(MK2, { x: 6, y: 0, z: 2.5, dist: COVER.dist * .56, yaw: COVER.yaw + 16, pitch: 72 }, C(15, 1, 0), .5, 'power3.out');
  // ===== MK: Sweden runs an hour behind; hop back and forth (L16-L18) =====
  for (const k of ['tintOld', 'swapA', 'swapB']) set(MK[k], 0, C(16, 0, -.5)); set(MK.tintNew, 1, C(16, 0, -.5)); set(MK.morph, 1, C(16, 0, -.5)); set(MK.prog, 1, C(16, 0, -.5)); set(MK.ribA, 1, C(16, 0, -.5)); set(MK.beamA, 0, C(16, 0, -.5)); set(MK.dk, 0, C(16, 0, -.5));
  set(MK.ck, { x: 4.5, y: 0, z: 2, dist: COVER.dist * .7, yaw: COVER.yaw - 15, pitch: 48 }, C(16, 0, -.5)); camK(MK, { x: 4.5, y: 0, z: 2, dist: COVER.dist * .64, yaw: COVER.yaw - 5, pitch: 52 }, C(16, 0, -.1), C(17, 0) - C(16, 0, -.1) + .2, 'sine.inOut');
    on(MK.ckSE.a, C(16, 1, 0), .3, 1, 'back.out(1.6)'); on(MK.ckFI.a, C(16, 1, .15), .3, 1, 'back.out(1.6)'); off(MK.ckSE.a, C(17, 0, .1)); off(MK.ckFI.a, C(17, 0, .1));
  // walker hops across the S three times; his own clock flips on each crossing
  { const S = MK; const wk = mk('div', { class: 'emo', style: 'font-size:120px' }, S.ov); wk.textContent = '🚶'; const wc = mk('div', { class: 'clk' }, S.ov); wc.innerHTML = '<span class="ct">12:00</span>'; const wct = wc.querySelector('.ct');
    const a = C(17, 0, .1), b = LN[17].b + .3, A = TK(0); on(A, a - .1, .2); off(A, C(18, 0, -.1));
    const path = t => { const p = clamp((t - a) / (b - a), 0, 1); const x = -5 + 17.6 * p, y = -2 + .8 * Math.sin(p * Math.PI * 6); return [x, y, Math.abs(Math.sin(p * Math.PI * 14)) * .5]; };
    let last = null;
    S.walker = { draw: t => { const al = valAt(A, t); wk.style.opacity = al; wc.style.opacity = al; if (al <= 0) return; const [x, y, hop] = path(t); const v = S.W3(x, y, .15 + hop);
      const q = toScreen(S.cam, v); wk.style.transform = `translate(${(q.x - 55).toFixed(1)}px,${(q.y - 115).toFixed(1)}px)`;
      const se = S.sideAt(x, y, 2) > .5; const txt = se ? '12:00' : '13:00'; if (txt !== last) { wct.textContent = txt; last = txt; }
      wc.style.transform = `translate(${clamp(q.x - wc.offsetWidth / 2, 40, 1040 - wc.offsetWidth).toFixed(1)}px,${Math.min(q.y - 330, 1020).toFixed(1)}px)`; } };
    S.walkT = []; for (let k = 0; k <= 200; k++) { const t = a + (b - a) * k / 200; S.walkT.push(t); } }
  camK(MK, { x: 4.5, y: 0, z: 2.5, dist: COVER.dist * .6, yaw: COVER.yaw + 4, pitch: 56 }, C(17, 0, -.1), C(18, 0) - C(17, 0, -.1), 'sine.inOut');
  emo(MK.sleep, C(18, 1, 0), C(19, 0, .2));
  set(MK.lSE.a, 1, -1); set(MK.lFI.a, 1, -1); off(MK.lSE.a, .12, .2); off(MK.lFI.a, .12, .2);
  on(MK.lSE.a, C(19, 1, .1) - .05, .18, 1, 'back.out(2)'); pop(MK.lSE, C(19, 1, .15)); on(MK.lFI.a, C(19, 1, .25) - .05, .18, 1, 'back.out(2)'); pop(MK.lFI, C(19, 1, .3));
  // ===== MK: back to the cover pose (L19 loop line; last ~0.4 s eases into the cover) =====
  camK(MK, COVER, C(19, 0, -.1), DUR - .02 - C(19, 0, -.1), 'power2.inOut');
  { MK.camAt(0); const q = toScreen(MK.cam, MK.W3(0, 0, .85)); const svg = mk('svg', { width: 1080, height: 1920, style: 'position:absolute;left:0;top:0;overflow:visible' }, COV, true);
    const rx = 105, ry = 135, pts = []; for (let i = 0; i <= 64; i++) { const a = -1.9 + i / 64 * Math.PI * 2.15, k = 1 + .06 * Math.sin(i * .9); pts.push(`${(q.x + Math.cos(a) * rx * k).toFixed(1)},${(q.y + Math.sin(a) * ry * k).toFixed(1)}`); }
    mk('polyline', { points: pts.join(' '), fill: 'none', stroke: '#03101A', 'stroke-width': 24, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, svg, true);
    mk('polyline', { points: pts.join(' '), fill: 'none', stroke: '#FF3B30', 'stroke-width': 14, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, svg, true);
    COV.insertBefore(svg, COV.firstChild); }
  tl.set(COV, { opacity: 1 }, 0); tl.to(COV, { opacity: 0, y: -16, duration: .22, ease: 'power2.in' }, .1);
  tl.fromTo(COV, { opacity: 0, y: 14, scale: .96 }, { opacity: 1, y: 0, scale: 1, duration: .38, ease: 'power2.out', ...IR }, DUR - .42);

  // ===== beats from the spec =====
  const beat = k => (D.beats || []).filter(b => b.kind === k);
  const nextChunk = t => { const c = D.chunks.find(c => c.sn > t + .5); return c ? c.sn - .12 : t + 2; };
  const posFn = (S, pt) => (S === MK || S === MK2) ? (t => { S.camAt(t); return toScreen(S.cam, S.W3(pt[0], pt[1], pt[2] || .1)); }) : (t => S.proj(t, pt[0], pt[1]));
  for (const b of beat('circle')) { const S = REG[b.scene]; const r = b.r || [200, 110];
    MO.hwCircle(S.ov, posFn(S, b.c), r[0], r[1], b.t, b.u || nextChunk(b.t), { seed: 3 + b.t, col: b.col }); }
  for (const b of beat('arrow')) { const S = REG[b.scene]; const f0 = posFn(S, b.from), f1 = posFn(S, b.to);
    MO.hwArrow(S.ov, t => { const p0 = f0(t), p1 = f1(t); return { x0: p0.x, y0: p0.y, x1: p1.x, y1: p1.y }; }, b.t, b.u || nextChunk(b.t), { seed: 7 + b.t, col: b.col }); }
  const GROWS = [];
  for (const b of beat('grow')) { const el = mk('div', { class: 'kbox', style: `top:${b.y || 160}px` }, $('hook'));
    el.innerHTML = `<span class="knum">0</span><span class="ksuf">${tr(b.unit || '')}</span>`;
    tl.set(el, { opacity: 1 }, b.t); MO.countGrow(el.querySelector('.knum'), b.to, b.t, { raw: b.to >= 1000, dur: b.dur || 1.0, from: b.from || 0, prefix: b.prefix, startScale: .35, suffixEl: el.querySelector('.ksuf') }); MO.textOut(el, b.u || nextChunk(b.t)); GROWS.push({ el, t: b.t }); }
  for (const b of beat('card')) { const S = REG[b.scene || 'MW']; const Cd = mkCard(S, b); key(Cd.a, 1, b.t, .35, 'power3.out'); key(Cd.a, 0, b.u || nextChunk(b.t), .25);
    if (b.to) MO.countGrow(Cd.num, b.to, b.t + .1, { dur: 1.1, startScale: .5, suffixEl: Cd.suf }); else { Cd.num.textContent = ''; Cd.num.style.display = 'none'; } }
  for (const b of beat('slam')) {
    if (b.what === 'num') { const g = GROWS.filter(x => x.t <= b.t).pop(); if (g) tl.fromTo(g.el, { scale: 1 }, { keyframes: [{ scale: 1.25, duration: .08 }, { scale: 1, duration: .28 }], transformOrigin: '50% 60%', ...IR }, b.t); shake(b.t + .08, .6); }
    else if (b.what === 'stamp') { tl.fromTo(STAMP, { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: .22, ease: 'power3.in', ...IR }, b.t - .2); MO.textOut(STAMP, b.u || nextChunk(b.t)); shake(b.t + .02, .55); }
    else if (b.what === 'morph') { shake(b.t, .8); }
    else if (b.what === 'clock') { shake(b.t, .5); }
    else if (b.what === 'pop') { shake(b.t + .03, .32); }
    else if (b.what === 'rise') { shake(b.t + .55, .65); }
  }
  for (const s of D.impacts || []) shake(s, .75);
  const cs = beat('charslam')[0];
  for (const id in TT) { const { g, t } = TT[id];
    if (id === 'tHook' && cs && D.lang !== 'hi') { tl.set(g, { opacity: 1 }, cs.t); MO.charSlam(TT.tHook.lines[0], cs.t, { blur: true }); }
    else MO.textIn(g, t.a);
    MO.textOut(g, t.b); }
  for (const K of CAPS) { const c = K.c;
    tl.set(K.g, { opacity: 1 }, c.sn); tl.set(K.g, { opacity: 0 }, Math.min(c.en, D.dur - .42));
    tl.fromTo(K.g, { scale: .9, transformOrigin: '565px 1385px' }, { scale: 1, duration: .2, ease: 'power3.out', ...IR }, c.sn);
    MO.karaoke(K.words, c.wt, w => w.classList.contains('k'));
    K.words.forEach((w, i) => { if (w.classList.contains('k')) MO.sweep(w, c.wt[Math.min(i, c.wt.length - 1)]); }); }
  // badge: stays on screen the whole video (no end card)
  const BW = $('badgeWrap'); const bs = 108 / 620;
  tl.set(BW, { opacity: 1, x: 44 - 230, y: 1332 - 450, scale: bs }, 0);
  layout();
  MO.shakeOn($('cshake'), D.dur);
  for (const T of ALLT) T.keys.sort((a, b) => a.a - b.a);
  const clk = { t: 0 };
  tl.fromTo(clk, { t: 0 }, { t: D.dur, duration: D.dur, ease: 'none', ...IR, onUpdate: () => { const t = clk.t;
    const live = S => S.wins.some(w => t >= w[0] - .05 && t <= w[1] + .45);
    for (const S of SCENES) if (live(S)) S.render(t);
    XF.render(t); } }, 0);
  window.__C = {};
  window.__seek = t => { tl.seek(t, false); };
  return tl;
}
window.__timelines = window.__timelines || {};
document.fonts.ready.then(() => Promise.all(READY)).then(() => { window.__timelines['main'] = build(); });
</script>
</body>
</html>
