/* ---------- build scenes ---------- */
const MP = map3('mp/', D.maps.mp, { globe: true, fog: [60, 140], flagCanvas: indiaFlagCanvas() });
const MP2 = map3('mp/', D.maps.mp, { globe: false, fog: [60, 140], exagK: 40, tk0: { lon: 80.5, lat: 25.0, dist: 20, el: 52, yaw: 0 } });
const GA = plate('ga_delhi.jpg', { s: 1.08 }); const GB = plate('ga_wide.jpg', { s: 1.0 });
const REG = { MP, MP2, GA, GB }; const SCENES = [MP, MP2, GA, GB];
const XF = BhugolXfade(T3, $('cshake'));
// map labels (lon/lat)
const L = D.lab;
MP.lPun = mapLabel(MP, tr('PUNJAB'), 75.4, 30.9, 60, '#FFFFFF'); MP.lBen = mapLabel(MP, tr('BENGAL'), 87.9, 23.4, 60, '#FFFFFF');
MP.lDel = mapLabel(MP, tr('DELHI'), 77.1, 29.05, 64, '#38D6FF'); MP.lInd = mapLabel(MP, '🇮🇳 ' + tr('INDIA'), 80.5, 25.0, 70, '#FFFFFF');
MP.lHim = mapLabel(MP, tr('HIMALAYAS'), 80.6, 30.2, 58, '#FFFFFF');
MP.iFarm = mapLabel(MP, '🌾', 75.6, 30.3, 120); MP.iRoad = mapLabel(MP, '🚗', 80.9, 26.8, 120); MP.iFac = mapLabel(MP, '🏭', 83.2, 25.4, 120);
MP.iFarm2 = mapLabel(MP, '🌾', 83.5, 26.2, 100); MP.iRoad2 = mapLabel(MP, '🚗', 77.8, 28.0, 100); MP.iFac2 = mapLabel(MP, '🏭', 78.6, 27.3, 100);
// terrain-scene labels (MP2: the plain, the wall, the lid)
MP2.lPlain = mapLabel(MP2, 'THE PLAIN', 80.6, 26.3, 62, '#f1e7b5'); MP2.lHim = mapLabel(MP2, 'HIMALAYAS', 82.6, 29.7, 70, '#FFFFFF');
MP2.lTib = mapLabel(MP2, 'TIBETAN PLATEAU', 84.0, 32.0, 54, '#ffffff');
MP2.lAra = mapLabel(MP2, 'ARAVALLI', 75.3, 25.6, 58, '#FFFFFF'); MP2.lVin = mapLabel(MP2, 'VINDHYA', 78.8, 23.3, 58, '#FFFFFF');
MP2.lSum = mapLabel(MP2, 'SUMMER', 80.2, 27.6, 92, '#FFC23A'); MP2.lSum.up = () => .9;
MP2.lNov = mapLabel(MP2, 'NOVEMBER', 83.2, 29.6, 92, '#8fd8ff'); MP2.lNov.up = () => .9;
MP2.lid = MP2.layer(0xFF8A2A, 0xFFD27A, 7, false); MP2.cold = MP2.layer(0x4FB8FF, 0xBFE8FF, 6, true);
MP2.lKm = mapLabel(MP2, '', 82.8, 25.6, 80, '#FFC23A'); MP2.lKm.e.innerHTML = `<span class="n">0</span> ${tr('KM')}`; MP2.lKm.up = t => valAt(MP2.smogH, t) + .08;
MP2.lFew = mapLabel(MP2, 'A FEW HUNDRED M', 80.4, 25.2, 66, '#FFC23A'); MP2.lFew.up = t => valAt(MP2.lid.z, t) + .05;
// characters + DOM widgets
MP2.cHim = himChar(MP2, 600, 820, .95); MP.cHim = himChar(MP, 560, 800, .95);
const GAU = gauge(GA); const GRID = cityGrid();
MP.del = MP.overlay(D.geo.states['Delhi'], null, 0x38D6FF); MP.del.zBase = .03;

/* ---------- titles + captions ---------- */
const TT = {};
for (const t of D.titles) { const g = mk('div', { class: 'ttl', id: t.id }, $('titles')); const lines = [];
  t.lines.forEach((ln0, i) => { const small = ln0.startsWith('~'); const ln = small ? ln0.slice(1) : ln0; const size = small ? 58 : (t.size || 132);
    const d = mk('div', { class: 'tl ' + (small ? 'small' : 'big') }, g); const base = (t.top || 300) + (i === 0 ? 0 : (small ? 74 : 124));
    Object.assign(d.style, { fontSize: size + 'px', top: (base - size * .8) + 'px', webkitTextStrokeWidth: (size * .14) + 'px' }); markup(ln, d); lines.push(d); });
  TT[t.id] = { g, t, lines }; }
const CAPS = D.chunks.map(c => { const g = mk('div', { class: 'cap' }, $('caps'));
  const lines = c.txt.split('|').map(ln => { const d = mk('div', { class: 'cl' }, g); markup(ln, d); return d; });
  return { c, g, lines, words: [...g.querySelectorAll('span')] }; });
$('folTxt').textContent = D.end.button; $('folTxt2').textContent = '✓ ' + D.end.following;
function layout() {
  for (const K of CAPS) { let fs = 92; K.g.style.opacity = 1;
    for (const d of K.lines) { d.style.fontSize = '92px'; const w = d.scrollWidth; if (w > 740) fs = Math.min(fs, 92 * 740 / w); }
    K.g.style.opacity = 0; const n = K.lines.length;
    K.lines.forEach((d, i) => Object.assign(d.style, { fontSize: fs.toFixed(1) + 'px', webkitTextStrokeWidth: (fs * .17).toFixed(1) + 'px', top: (1385 + (i - (n - 1) / 2) * fs - fs * .5).toFixed(1) + 'px' })); }
  for (const id in TT) { const { g, lines } = TT[id]; g.style.opacity = 1;
    for (const d of lines) { const w = d.scrollWidth, fs = parseFloat(d.style.fontSize); if (w > 960) d.style.fontSize = (fs * 960 / w).toFixed(1) + 'px'; }
    g.style.opacity = 0; }
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
  const flash = at => tl.to($('flash'), { keyframes: [{ opacity: .45, duration: .08 }, { opacity: 0, duration: .45 }] }, at);
  const chIn = (ch, at) => { tl.fromTo(ch.box, { opacity: 0, y: 420, scale: .6, rotation: -8 }, { opacity: 1, y: 0, scale: 1, rotation: 0, duration: .55, ease: 'back.out(1.8)', ...IR }, at); };
  const chOut = (ch, at) => tl.to(ch.box, { y: 460, opacity: 0, scale: .7, duration: .35, ease: 'power3.in' }, at);
  const talk = (ch, li) => { const ws = D.chunks.filter(c => c.li === li).flatMap(c => c.wt); const a = LN[li].a, b = LN[li].b;
    tl.set(ch.mouthO, { opacity: 0 }, 0); tl.set(ch.mouthC, { opacity: 1 }, 0);
    ws.forEach((w, i) => { const nx = i < ws.length - 1 ? ws[i + 1] : b; tl.set(ch.mouthO, { opacity: 1 }, w); tl.set(ch.mouthC, { opacity: 0 }, w);
      tl.set(ch.mouthO, { opacity: 0 }, Math.min(nx - .03, w + .16)); tl.set(ch.mouthC, { opacity: 1 }, Math.min(nx - .03, w + .16)); });
    const n = Math.max(2, Math.floor((b - a) / .32));
    tl.fromTo(ch.box, { scaleY: 1, rotation: 0, transformOrigin: '50% 80%' }, { keyframes: Array.from({ length: n }, (_, i) => [{ scaleY: 1.03, rotation: i % 2 ? 1.5 : -1.5, duration: .16 }, { scaleY: 1, rotation: 0, duration: .16 }]).flat(), ...IR }, a);
    tl.to(ch.eyes, { keyframes: [{ scaleY: .1, duration: .06 }, { scaleY: 1, duration: .08 }], transformOrigin: '0px 0px' }, a + (b - a) * .55); };
  const zoomTo = (S, ch, a, b) => { tl.to(S.push, { scale: 1.12, x: (540 - ch.cx) * .4, y: -30, duration: .28, ease: 'power3.out', transformOrigin: '540px 900px' }, a - .18);
    tl.to(S.push, { scale: 1, x: 0, y: 0, duration: .35, ease: 'power2.inOut' }, b + .1); };
  const shake = (at, k) => MO.shake(at, .6, 'rig-6d-wobble', k || .75);
  const lbl = (Lb, a, b) => { key(Lb.a, 1, a, .3, 'power3.out'); key(Lb.a, 0, b, .25); };
  const NX = li => C(li + 1, 0);

  // ===== L0 (MP globe): 86 of 100 — India in its flag (official boundary) =====
  key(MP.gk, { lon: 40, lat: 18, dist: 3.4 }, 0, .01); key(MP.gk, { lon: 79, lat: 22, dist: 2.75 }, .05, NX(0) - .3, 'power2.inOut');
  key(MP.flagA, .95, C(0, 2, -.1), .45, 'power2.out');
  tl.fromTo(GRID.g, { opacity: 0, y: 60, scale: .9 }, { opacity: 1, y: 0, scale: 1, duration: .4, ease: 'power3.out', ...IR }, C(0, 0, .25));
  { const t86 = D.w86; const st = { v: 0 }; tl.fromTo(st, { v: 0 }, { v: 86, duration: Math.max(.6, t86 - C(0, 0, .3) + .2), ease: 'power3.out', ...IR, onUpdate: () => { const n = Math.round(st.v); GRID.n.textContent = n; GRID.dots.forEach((d, i) => d.style.background = i < n ? '#FF3B30' : '#5b6b80'); } }, C(0, 0, .3)); }
  MO.textOut(GRID.g, C(0, 2, .05));
  // ===== L1 (GA): Delhi AQI gauge 488 / MAX 500 =====
  key(GA.k, { s: 1.08, x: 0, y: 0 }, 0, .01); key(GA.k, { s: 1.22, x: -20, y: 30 }, C(1, 0, -.2), NX(1) - C(1, 0, -.2) + .3, 'sine.inOut');
  tl.fromTo(GAU.g, { opacity: 0, y: 50, scale: .92 }, { opacity: 1, y: 0, scale: 1, duration: .35, ease: 'power3.out', ...IR }, C(1, 0, .0));
  { const t488 = D.w488; const st = { v: 0 }; const a = C(1, 0, .15), d = Math.max(.7, t488 - a + .15);
    tl.fromTo(st, { v: 0 }, { v: 488, duration: d, ease: 'power3.out', ...IR, onUpdate: () => { const v = st.v; GAU.num.textContent = Math.round(v); GAU.arc.setAttribute('stroke-dashoffset', (1068 * (1 - v / 500)).toFixed(1)); GAU.nd.setAttribute('transform', `rotate(${(-90 + 180 * v / 500).toFixed(2)} 450 470)`); } }, a);
    tl.fromTo(GAU.num, { scale: 1 }, { keyframes: [{ scale: 1.3, duration: .08 }, { scale: 1, duration: .25 }], transformOrigin: '50% 50%', ...IR }, a + d); shake(a + d + .05, .6); }
  tl.fromTo(GAU.mx, { scale: 1 }, { keyframes: [{ scale: 1.25, duration: .1 }, { scale: 1, duration: .3 }], transformOrigin: '804px 540px', ...IR }, D.w500);
  // ===== L2-L3 (MP terrain): the grey river from space; 4 in 10 Indians =====
  key(MP.x, 1, C(2, 0, -.2), .01);
  key(MP.tk, { lon: 81.5, lat: 26.6, dist: 33, el: 88, yaw: 0 }, C(2, 0, -.2), .01); key(MP.tk, { lon: 81.0, lat: 26.9, dist: 29, el: 82, yaw: -2 }, C(2, 0, -.1), C(4, 0) - C(2, 0, -.1), 'sine.inOut');
  key(MP.hazeA, 0, 0, .01); key(MP.hazeA, 1, C(2, 1, -.05), .7, 'power2.out'); key(MP.flagA, 0, C(1, 0), .01);
  lbl(MP.lPun, C(2, 2, -.05), C(3, 0, -.1)); lbl(MP.lBen, C(2, 2, .35), C(3, 0, -.1));
  on(MP.hl, C(3, 0, -.1), .3); { const a = C(3, 0, .0), b = LN[3].b - .1; for (let i = 1; i <= 7; i++) key(MP.lit, i, a + (b - a) * (i - 1) / 7, .06, 'none'); }
  off(MP.hl, C(4, 0, -.1), .3);
  // ===== L4-L7 (MP2 terrain): the bowl, the wall, the hills =====
  key(MP2.tk, { lon: 80.5, lat: 24.8, dist: 21, el: 54, yaw: 0 }, 0, .01); key(MP2.tk, { lon: 80.8, lat: 25.6, dist: 18.5, el: 49, yaw: -4 }, C(4, 0, -.15), C(5, 0) - C(4, 0, -.15), 'sine.inOut');
  key(MP2.x, 1, 0, .01); key(MP2.exK, 34, 0, .01); key(MP2.hazeA, .5, 0, .01); key(MP2.smogA, .55, 0, .01); key(MP2.smogH, .3, 0, .01); key(MP2.smogF, .4, 0, .01);
  on(MP2.rise, C(4, 0, .2), .6); lbl(MP2.lPlain, C(4, 0, .3), C(5, 0, .3));
  key(MP2.exK, 62, C(5, 0, .05), .9, 'power3.out'); lbl(MP2.lHim, C(5, 0, .45), C(6, 0, -.2)); key(MP2.rise, .45, C(5, 0, .1), .5);
  key(MP2.tk, { lon: 81.8, lat: 27.9, dist: 13.5, el: 43, yaw: 4 }, C(5, 0, -.05), C(6, 0) - C(5, 0, -.05), 'power2.inOut');
  key(MP2.tk, { lon: 82.2, lat: 28.1, dist: 12.5, el: 42, yaw: 8 }, C(6, 0, -.05), C(7, 0, -.25) - C(6, 0, -.05), 'sine.inOut');
  chIn(MP2.cHim, C(6, 0, -.35)); talk(MP2.cHim, 6); zoomTo(MP2, MP2.cHim, LN[6].a, LN[6].b); chOut(MP2.cHim, C(7, 0, -.25));
  key(MP2.tk, { lon: 77.0, lat: 24.6, dist: 15, el: 55, yaw: -8 }, C(7, 0, -.25), .7, 'power3.inOut'); key(MP2.tk, { lon: 77.3, lat: 24.9, dist: 16.5, el: 53, yaw: -3 }, C(7, 0, .45), NX(7) - C(7, 0, .45), 'sine.inOut');
  lbl(MP2.lAra, C(7, 0, .25), NX(7) - .2); lbl(MP2.lVin, C(7, 0, .6), NX(7) - .2);
  // ===== L8 (MP oblique): millions of years — so why only in winter? =====
  key(MP.tk, { lon: 79.5, lat: 24.5, dist: 22, el: 54, yaw: 0 }, C(8, 0, -.3), .01); key(MP.tk, { lon: 80.2, lat: 26.2, dist: 18, el: 47, yaw: 6 }, C(8, 0, -.1), NX(8) - C(8, 0, -.1) + .3, 'power2.inOut');
  key(MP.hazeA, 0, C(8, 0, -.3), .01); lbl(MP.lHim, C(8, 0, .3), NX(8) - .2); key(MP.rise, 1, C(8, 0, .1), .8);
  // ===== L9-L12 (MP2 terrain): summer vs November, the lid =====
  key(MP2.tk, { lon: 80.6, lat: 25.9, dist: 18, el: 46, yaw: 3 }, C(9, 0, -.3), .01); key(MP2.tk, { lon: 80.8, lat: 26.3, dist: 16.5, el: 44, yaw: -4 }, C(9, 0, -.1), C(10, 0, -.15) - C(9, 0, -.1), 'sine.inOut');
  key(MP2.rise, 0, C(9, 0, -.3), .01); key(MP2.exK, 62, C(9, 0, -.3), .01); key(MP2.hazeA, .3, C(9, 0, -.3), .01);
  key(MP2.smogA, 1, C(9, 0, -.3), .01); key(MP2.smogH, .3, C(9, 0, -.3), .01); key(MP2.smogF, 1, C(9, 0, -.3), .01);
  lbl(MP2.lSum, C(9, 0, 0), C(10, 0, -.2));
  key(MP2.smogH, 1.5, C(9, 1, -.2), C(10, 0, -.2) - C(9, 1, -.2), 'power1.in'); key(MP2.smogA, .12, C(9, 1, .3), C(10, 0, -.2) - C(9, 1, .3), 'power1.in');
  lbl(MP2.lKm, C(9, 1, -.05), C(10, 0, -.2)); { const n = MP2.lKm.e.querySelector('.n'); MO.countUp(n, 1, C(9, 1, .0), { dur: .6, noScale: true }); }
  // November: smoke back, cold air slides off the plateau, warm layer on top
  key(MP2.smogH, .5, C(10, 0, -.15), .01); key(MP2.smogA, .9, C(10, 0, -.15), .4); key(MP2.hazeA, .6, C(10, 0, -.15), .5);
  lbl(MP2.lNov, C(10, 0, 0), C(10, 2, -.25));
  key(MP2.tk, { lon: 83.4, lat: 28.6, dist: 15, el: 50, yaw: 6 }, C(10, 0, -.15), .8, 'power2.inOut');
  key(MP2.cold.z, .07, 0, .01); key(MP2.cold.sw, 0, 0, .01); on(MP2.cold.a, C(10, 0, .2), .3, .75); key(MP2.cold.sw, 1, C(10, 0, .2), C(10, 2) - C(10, 0, .2) + .2, 'power1.inOut'); lbl(MP2.lTib, C(10, 1, -.05), C(10, 2, -.25));
  key(MP2.tk, { lon: 80.7, lat: 26.2, dist: 16.5, el: 46, yaw: -3 }, C(10, 2, -.2), .8, 'power2.inOut');
  key(MP2.lid.z, 1.1, 0, .01); on(MP2.lid.a, C(10, 2, .0), .4, .55);
  on(MP2.lid.a, C(11, 0, -.1), .15); key(MP2.lid.z, .46, C(11, 0, -.05), .55, 'bounce.out'); off(MP2.cold.a, C(11, 0, .3), .5);
  key(MP2.tk, { lon: 80.7, lat: 26.3, dist: 15, el: 44, yaw: 2 }, C(11, 0, .5), C(12, 0) - C(11, 0, .5), 'sine.inOut');
  // ceiling drops ~1 km -> a few hundred m, the lid rides down, the wind dies
  key(MP2.lid.z, .17, C(12, 0, .1), C(12, 1, .3) - C(12, 0, .1), 'power2.inOut'); key(MP2.smogH, .15, C(12, 0, .1), C(12, 1, .3) - C(12, 0, .1), 'power2.inOut');
  key(MP2.smogA, 1, C(12, 0, .1), .6); key(MP2.hazeA, .9, C(12, 0, .1), .8);
  lbl(MP2.lFew, C(12, 1, -.05), NX(12) - .1);
  key(MP2.smogF, 0, C(12, 2, -.05), .7, 'power2.out');
  key(MP2.tk, { lon: 80.6, lat: 26.2, dist: 12, el: 40, yaw: -3 }, C(12, 1, -.1), NX(12) - C(12, 1, -.1), 'sine.inOut');
  // ===== L13-L16 (MP): strangest part — Delhi at zero, the plain still fills =====
  key(MP.tk, { lon: 80.0, lat: 27.0, dist: 30, el: 84, yaw: 0 }, C(13, 0, -.3), .01); key(MP.tk, { lon: 79.4, lat: 27.6, dist: 26, el: 78, yaw: -4 }, C(13, 0, -.1), C(14, 0) - C(13, 0, -.1), 'sine.inOut');
  key(MP.rise, 0, C(13, 0, -.3), .01); key(MP.hazeA, .85, C(13, 0, -.3), .01); on(MP.smogA, C(13, 0, -.2), .6, .9);
  key(MP.tk, { lon: 77.2, lat: 28.6, dist: 7.5, el: 66, yaw: 8 }, C(14, 0, -.15), .9, 'power3.inOut'); key(MP.tk, { lon: 77.15, lat: 28.62, dist: 6.6, el: 60, yaw: 14 }, C(14, 0, .8), C(16, 0) - C(14, 0, .8), 'sine.inOut');
  on(MP.del.a, C(14, 0, .5), .3); key(MP.del.z, 0, C(14, 0, .5), .5, 'bounce.out'); on(MP.dl, C(14, 0, .5), .3); lbl(MP.lDel, C(14, 0, .6), C(16, 0, -.1));
  key(MP.hazeA, .2, C(14, 0, .7), .35); key(MP.smogA, .15, C(14, 0, .7), .35);   // Delhi's own smoke switched off
  key(MP.smogF, 1, C(15, 0, .0), 1.2, 'power1.inOut'); key(MP.smogA, 1, C(15, 0, .1), 1.4, 'power1.inOut'); key(MP.hazeA, .9, C(15, 0, .1), 1.4, 'power1.inOut');   // ...and the plain's smoke rolls back in
  key(MP.tk, { lon: 80.6, lat: 27.0, dist: 30, el: 76, yaw: -6 }, C(16, 0, -.2), .9, 'power3.inOut'); key(MP.tk, { lon: 80.9, lat: 26.9, dist: 28, el: 72, yaw: -2 }, C(16, 0, .7), C(17, 0) - C(16, 0, .7) + .3, 'sine.inOut');
  off(MP.del.a, C(16, 0, -.1)); off(MP.dl, C(16, 0, -.1));
  for (const [ic, at] of [[MP.iFarm, C(16, 0, .4)], [MP.iFarm2, C(16, 0, .65)], [MP.iRoad, C(16, 0, .9)], [MP.iRoad2, C(16, 1, -.2)], [MP.iFac, C(16, 1, .2)], [MP.iFac2, C(16, 1, .45)]]) {
    key(ic.a, 1, at, .25, 'back.out(2)'); key(ic.pop, .3, at, .08); key(ic.pop, 0, at + .08, .3); key(ic.a, 0, NX(16) - .1, .2); }
  // ===== L17 (GB): one sky =====
  key(GB.k, { s: 1.04, x: 0, y: 0 }, 0, .01); key(GB.k, { s: 1.16, x: 0, y: -20 }, C(17, 0, -.2), NX(17) - C(17, 0, -.2) + .3, 'sine.inOut');
  // ===== L18 (MP2 terrain): the Himalayas' twist =====
  key(MP2.tk, { lon: 81.8, lat: 27.9, dist: 13.5, el: 43, yaw: 6 }, C(18, 0, -.3), .01); key(MP2.tk, { lon: 82.0, lat: 28.0, dist: 12.5, el: 42, yaw: 2 }, C(18, 0, -.1), NX(18) - C(18, 0, -.1) + .3, 'sine.inOut');
  key(MP2.lid.a, 0, C(18, 0, -.3), .01); key(MP2.smogA, .9, C(18, 0, -.3), .01); key(MP2.smogH, .3, C(18, 0, -.3), .01); key(MP2.smogF, .3, C(18, 0, -.3), .01); key(MP2.hazeA, .8, C(18, 0, -.3), .01);
  chIn(MP2.cHim, C(18, 0, -.35)); talk(MP2.cHim, 18); zoomTo(MP2, MP2.cHim, LN[18].a, LN[18].b); chOut(MP2.cHim, NX(18) - .2);
  // ===== L19-20 (MP wide): your city's AQI? then the end card =====
  key(MP.tk, { lon: 80.0, lat: 25.5, dist: 36, el: 86, yaw: 0 }, C(19, 0, -.3), .01); key(MP.tk, { lon: 79.8, lat: 25.6, dist: 33, el: 80, yaw: -3 }, C(19, 0, -.1), D.dur - C(19, 0, -.1), 'sine.inOut');
  key(MP.smogA, .5, C(19, 0, -.3), .01); key(MP.hazeA, .7, C(19, 0, -.3), .01); key(MP.rise, 1, C(19, 0, -.3), .01); lbl(MP.lInd, C(19, 0, .2), D.end.start);

  // ===== beats from the spec (same list drives the sound) =====
  const beat = k => (D.beats || []).filter(b => b.kind === k);
  const nextChunk = t => { const c = D.chunks.find(c => c.sn > t + .5); return c ? c.sn - .12 : t + 2; };
  const posFn = (S, pt) => (t => S.proj(t, pt[0], pt[1]));
  for (const b of beat('circle')) { const S = REG[b.scene]; const r = b.r || [200, 110];
    MO.hwCircle(S.ov, posFn(S, b.c), r[0], r[1], b.t, b.u || nextChunk(b.t), { seed: 3 + b.t, col: b.col }); }
  for (const b of beat('arrow')) { const S = REG[b.scene]; const f0 = posFn(S, b.from), f1 = posFn(S, b.to);
    MO.hwArrow(S.ov, t => { const p0 = f0(t), p1 = f1(t); return { x0: p0.x, y0: p0.y, x1: p1.x, y1: p1.y }; }, b.t, b.u || nextChunk(b.t), { seed: 7 + b.t, col: b.col }); }
  for (const b of beat('grow')) { const el = mk('div', { class: 'kbox', style: `top:${b.y || 160}px` }, $('hook'));
    el.innerHTML = `${b.prefix ? `<span class="ksuf" style="margin:0 20px 0 0">${tr(b.prefix)}</span>` : ''}<span class="knum">0</span><span class="ksuf">${tr(b.unit || '')}</span>`;
    const dur = b.dur || 1.0; tl.set(el, { opacity: 1 }, b.t);
    MO.countGrow(el.querySelector('.knum'), b.to, b.t, { dur, from: b.from || 0, startScale: .35, suffixEl: el.querySelectorAll('.ksuf')[el.querySelectorAll('.ksuf').length - 1] }); MO.textOut(el, b.u || nextChunk(b.t)); }
  const LBL = { 'MP2.lHim': MP2.lHim, 'MP2.lAra': MP2.lAra, 'MP2.lVin': MP2.lVin, 'MP2.lTib': MP2.lTib, 'MP2.lKm': MP2.lKm, 'MP2.lFew': MP2.lFew, 'MP2.lNov': MP2.lNov, 'MP2.lSum': MP2.lSum, 'MP.lDel': MP.lDel, 'MP.lPun': MP.lPun, 'MP.lBen': MP.lBen, 'MP.lHim': MP.lHim, 'MP.lInd': MP.lInd, 'MP2.lPlain': MP2.lPlain };
  for (const b of beat('slam')) {
    if (b.what === 'pop') { const Lb = LBL[b.lab]; key(Lb.pop, .32, b.t, .09, 'power2.out'); key(Lb.pop, 0, b.t + .09, .32, 'power2.inOut'); }
    else if (b.what === 'jolt') tl.to(MP2.cHim.box, { keyframes: [{ rotation: -7, y: 16, duration: .1 }, { rotation: 0, y: 0, duration: .3, ease: 'power2.out' }] }, b.t);
    else if (b.what === 'lid') shake(b.t, .7);
    else if (b.what === 'grid') tl.fromTo(GRID.n, { scale: 1 }, { keyframes: [{ scale: 1.35, duration: .08 }, { scale: 1, duration: .25 }], ...IR }, b.t);
    else if (b.what === 'flag') tl.fromTo($('flash'), { opacity: 0 }, { keyframes: [{ opacity: .14, duration: .06 }, { opacity: 0, duration: .3 }], ...IR }, b.t); }
  for (const s of D.hand || []) MO.shake(s[0], s[1] - s[0], 'handheld-normal-mild', .1, { decay: false });
  for (const s of D.impacts || []) shake(s, .6);
  for (const b of beat('flashfx')) flash(b.t);
  const cs = beat('charslam')[0];
  for (const id in TT) { const { g, t } = TT[id];
    if (id === 'tHook' && cs && D.lang !== 'hi') { tl.set(g, { opacity: 1 }, cs.t); MO.charSlam(TT.tHook.lines[0], cs.t, { blur: true }); }
    else if (t.slam) { MO.slam(g, t.a, { shake: !!t.shake }); g.setAttribute('data-hf-motion-blur', '{"samplesPerFrame": 8}'); } else MO.textIn(g, t.a);
    MO.textOut(g, t.b); }
  // captions
  for (const K of CAPS) { const c = K.c;
    tl.set(K.g, { opacity: 1 }, c.sn); tl.set(K.g, { opacity: 0 }, c.en);
    tl.fromTo(K.g, { scale: .9, transformOrigin: '565px 1385px' }, { scale: 1, duration: .2, ease: 'power3.out', ...IR }, c.sn);
    MO.karaoke(K.words, c.wt, w => w.classList.contains('k'));
    K.words.forEach((w, i) => { if (w.classList.contains('k')) MO.sweep(w, c.wt[Math.min(i, c.wt.length - 1)]); }); }
  // badge + end card
  const BW = $('badgeWrap'); const E = D.end; const bs = 108 / 620;
  tl.fromTo(BW, { opacity: 0, x: 44 - 230, y: 1332 - 450, scale: bs }, { opacity: 1, x: 44 - 230, y: 1332 - 450, scale: bs, duration: .5 }, .2);
  tl.fromTo(BW, { x: 44 - 230, y: 1332 - 450, scale: bs }, { x: 0, y: 0, scale: 1, duration: .9, ease: 'power2.inOut', ...IR }, E.start);
  tl.to($('dim'), { opacity: .55, duration: .5 }, E.start);
  const F = $('follow');
  tl.fromTo(F, { opacity: 0, scale: .2 }, { opacity: 1, scale: 1, duration: .45, ease: 'back.out(2)', ...IR }, E.btn);
  const TD = $('tapDot');
  tl.fromTo(TD, { opacity: 0, x: 470, y: 120 }, { opacity: 1, x: 430, y: 50, duration: .6, ease: 'power2.out', ...IR }, E.tap - .6);
  tl.to(F, { keyframes: [{ scale: .94, duration: .1 }, { scale: 1, duration: .1 }] }, E.tap);
  tl.fromTo($('ripple'), { opacity: .5, scale: .05 }, { opacity: 0, scale: 1, duration: .8, ease: 'power2.out', ...IR }, E.tap + .1);
  tl.set($('folBtn'), { backgroundColor: '#2A1206', border: '5px solid #FF7A1A' }, E.tap + .2);
  tl.set($('folTxt'), { opacity: 0 }, E.tap + .2); tl.set($('folTxt2'), { opacity: 1 }, E.tap + .2);
  tl.to(TD, { opacity: 0, duration: .3 }, E.tap + .5);
  layout();
  MO.shakeOn($('cshake'), D.dur);
  for (const T of ALLT) T.keys.sort((a, b) => a.a - b.a);
  const clk = { t: 0 };
  tl.fromTo(clk, { t: 0 }, { t: D.dur, duration: D.dur, ease: 'none', ...IR, onUpdate: () => { const t = clk.t;
    const live = S => S.wins.some(w => t >= w[0] - .05 && t <= w[1] + .45);
    for (const S of SCENES) if (live(S)) S.render(t);
    XF.render(t); } }, 0);
  window.__C = {};
  return tl;
}
window.__timelines = window.__timelines || {};
document.fonts.ready.then(() => Promise.all(READY)).then(() => { window.__timelines['main'] = build(); });
