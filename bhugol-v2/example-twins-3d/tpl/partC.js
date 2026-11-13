/* ---------- build scenes ---------- */
const FT = iso => { const t = new T3.Texture(); READY.push(tex('flag_' + iso + '.png').then(x => { t.image = x.image; t.needsUpdate = true; })); return t; };
const SA = map3('sa/', D.maps.sa, { globe: true, fog: [60, 170], pin: [86.925, 27.988], exag: 30, tk0: { lon: 86.6, lat: 25.6, dist: 46, el: 88, yaw: 0 }, gk0: D.loopPose });
const WA = map3('wa/', D.maps.wa, { cls: false, fog: [50, 140], exag: 8, tk0: { lon: -11.2, lat: 10.2, dist: 22, el: 88, yaw: 0 } });
const ZC = map3('zc/', D.maps.zc, { cls: false, fog: [120, 320], exag: 10, tk0: { lon: 25.5, lat: -13, dist: 34, el: 88, yaw: 0 } });
const IT = map3('it/', D.maps.it, { cls: false, fog: [80, 240], exag: 12, tk0: { lon: 12.5, lat: 42, dist: 30, el: 88, yaw: 0 } });
const SEA = map3('sea/', D.maps.sea, { cls: false, globe: true, fog: [80, 240], exag: 12, tk0: { lon: 109.4, lat: 9.6, dist: 74, el: 88, yaw: 0 }, gk0: { lon: 109.4, lat: 9.6, dist: 2.3 } });
const REG = { SA, WA, ZC, IT, SEA }; const SCENES = [SA, WA, ZC, IT, SEA];
const XF = BhugolXfade(T3, $('cshake'));
const GEO = D.geo;
WA.uk = WA.overlay(GEO.gb_on_gn, FT('GB'));
ZC.cl = ZC.overlay(GEO.cl_side, FT('CL')); ZC.mo = ZC.morph(GEO.morph_a, GEO.morph_b, FT('ZM'));
IT.ph = IT.overlay(GEO.ph_top, FT('PH'));
const OVR = { 'WA.uk': WA.uk, 'ZC.cl': ZC.cl, 'IT.ph': IT.ph };
SA.meas22 = measure(SA, [88.111, 26.586], [88.346, 26.505]);
const LBL = (D.labels || []).map(b => { const S = REG[b.scene]; const L = mapLabel(S, b.txt, b.lon, b.lat, b.fs || 64, b.col); if (b.ov) L.ov = OVR[b.ov]; return Object.assign(L, { b }); });
// characters
WA.cGb = character(WA, 'gb', 540, 900, 1.25); SEA.cMy = character(SEA, 'my', 330, 900, 1.05); SEA.cVn = character(SEA, 'vn', 780, 780, 1.1);
const heart = mk('div', { class: 'emo', style: 'left:470px;top:560px;font-size:170px' }, SEA.chars); heart.textContent = '❤️';
// rank badges
const RK = {}; for (const n of [5, 4, 3, 2, 1]) { const el = mk('div', { class: 'rank' + (n === 1 ? ' one' : '') }, $('ranks'));
  el.innerHTML = (n === 1 ? '<div class="rays"></div><div class="crown">👑</div>' : '') + `<div class="rnum">#${n}</div>`; RK[n] = el; }
const CONF = []; { const cols = ['#FFC23A', '#FF3B30', '#38D6FF', '#7CFF6B', '#FF6BD5', '#FFFFFF']; for (let i = 0; i < 70; i++) { const e = mk('div', { class: 'conf' }, $('ranks'));
  const h = k => { const s = Math.sin((i + 1) * 91.7 + k * 13.3) * 43758.5; return s - Math.floor(s); };
  e.style.background = cols[i % cols.length]; CONF.push({ e, a: h(1) * Math.PI * 2, v: 700 + h(2) * 900, sp: (h(3) - .5) * 900, w: 14 + h(4) * 14 }); e.style.width = CONF[i].w + 'px'; e.style.height = (CONF[i].w * .55) + 'px'; } }

/* ---------- titles + captions ---------- */
const TT = {};
for (const t of D.titles) { const g = mk('div', { class: 'ttl', id: t.id }, $('titles')); const lines = [];
  t.lines.forEach((ln0, i) => { const small = ln0.startsWith('~'); const ln = small ? ln0.slice(1) : ln0; const size = small ? 64 : 124;
    const d = mk('div', { class: 'tl ' + (small ? 'small' : 'big') }, g); const base = 330 + (i === 0 ? 0 : (small ? 80 : 124));
    Object.assign(d.style, { fontSize: size + 'px', top: (base - size * .8) + 'px', webkitTextStrokeWidth: (size * .14) + 'px' }); markup(ln, d); lines.push(d); });
  TT[t.id] = { g, t, lines }; }
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
}

/* ---------- timeline ---------- */
function build() {
  layout();
  const tl = gsap.timeline({ paused: true }); const IR = { immediateRender: false };
  const MO = BhugolMotion(tl, { xfade: true });
  const PL = D.shots.map(s => ({ S: REG[s.scene], el: REG[s.scene].el, at: s.t, cut: s.cut }));
  PL.forEach((p, i) => { p.S.wins.push([i ? p.at - .45 : 0, i < PL.length - 1 ? PL[i + 1].at + .1 + (PL[i + 1].cut === 'burn' ? MO.BURN_DUR : 0) : D.dur + 1]); });
  PL.forEach((p, i) => { if (p.cut === 'burn') { const A = PL[i - 1].S; XF.add(p.at, MO.BURN_DUR, { cv: A.Tn.cv, push: A.push }, { cv: p.S.Tn.cv, push: p.S.push }, 'burn'); } });
  MO.shots(PL); tl.set(PL[0].el, { opacity: 1 }, 0);
  for (const b of D.beats || []) if (b.kind === 'punch') MO.punch(REG[b.scene].push, b.t, b.level, b.back);
  const on = (T, at, d, v, e) => key(T, v === undefined ? 1 : v, at, d || .4, e || 'power1.inOut');
  const WT = (li, ci, en, hi, off) => { const ch = D.chunks.find(c => c.li === li && c.ci === ci); const nd = (D.lang === 'hi' ? hi : en);
    const toks = ch.txt.replace(/\|/g, ' ').replace(/\*/g, '').split(' '); const k = nd ? toks.findIndex(w => w.toUpperCase().includes(nd.toUpperCase())) : -1; return (k >= 0 ? ch.wt[k] : ch.sn) + (off || 0); };
  const flash = at => tl.to($('flash'), { keyframes: [{ opacity: .5, duration: .08 }, { opacity: 0, duration: .45 }] }, at);
  const chIn = (ch, at) => { tl.fromTo(ch.box, { opacity: 0, y: 420, scale: .6, rotation: -8 }, { opacity: 1, y: 0, scale: 1, rotation: 0, duration: .55, ease: 'back.out(1.8)', ...IR }, at); };
  const chOut = (ch, at) => tl.to(ch.box, { y: 460, opacity: 0, scale: .7, duration: .35, ease: 'power3.in' }, at);
  const mouth = (ch, a, b, step) => { tl.set(ch.mouthO, { opacity: 0 }, 0); tl.set(ch.mouthC, { opacity: 1 }, 0);
    for (let t = a; t < b - .05; t += step) { tl.set(ch.mouthO, { opacity: 1 }, t); tl.set(ch.mouthC, { opacity: 0 }, t); tl.set(ch.mouthO, { opacity: 0 }, t + step * .55); tl.set(ch.mouthC, { opacity: 1 }, t + step * .55); } };
  const bob = (ch, a, b) => { const n = Math.max(2, Math.floor((b - a) / .32));
    tl.fromTo(ch.box, { scaleY: 1, rotation: 0, transformOrigin: '50% 80%' }, { keyframes: Array.from({ length: n }, (_, i) => [{ scaleY: 1.04, rotation: i % 2 ? 2 : -2, duration: .16 }, { scaleY: 1, rotation: 0, duration: .16 }]).flat(), ...IR }, a); };
  const shake = (at, k) => MO.shake(at, .6, 'rig-6d-wobble', k || .75);
  const LNe = i => LN[i].b;

  // ===== SA: hook globe spin -> dive onto Nepal & Bangladesh (pair #5) =====
  key(SA.gk, D.loopPose, 0, .01); key(SA.gk, { lon: 84, lat: 24, dist: 2.5 }, .05, C(1, 0, -.35) - .05, 'sine.inOut');
  key(SA.gk, { lon: 86.6, lat: 25.6, dist: 1.75 }, C(1, 0, -.35), .45, 'power3.in'); key(SA.x, 1, C(1, 0, -.05), .35, 'power1.inOut');
  key(SA.tk, { lon: 86.5, lat: 25.6, dist: 41, el: 86, yaw: 2 }, C(1, 0, -.05), C(2, 0, -.25) - C(1, 0, -.05), 'power2.out');
  on(SA.fA, WT(1, 1, 'NEPAL', 'नेपाल', -.05), .35); on(SA.fB, WT(1, 1, 'BANGLADESH', 'बांग्लादेश', -.05), .35);
  key(SA.tk, { lon: 88.23, lat: 26.4, dist: 6.5, el: 74, yaw: 0 }, C(2, 0, -.25), 1.0, 'power3.inOut');
  key(SA.tk, { lon: 88.24, lat: 26.42, dist: 5.8, el: 70, yaw: 4 }, C(2, 0, .75), C(2, 1, -.2) - C(2, 0, .75), 'sine.inOut');
  { const m = SA.meas22; on(m.a, C(2, 0, .35), .2); key(m.draw, 1, C(2, 0, .4), .6, 'power3.out'); key(m.a, 0, C(2, 1, -.25), .2);
    MO.countUp(m.lab.querySelector('.n'), 22, C(2, 0, .4), { dur: .7, noScale: true }); }
  key(SA.tk, { lon: 86.93, lat: 27.75, dist: 3.6, el: 34, yaw: 0 }, C(2, 1, -.2), 1.1, 'power3.inOut'); on(SA.pinA, C(2, 1, .3), .5); key(SA.fA, 0, C(2, 1, -.1), .6); key(SA.fB, 0, C(2, 1, -.1), .6);
  key(SA.tk, { lon: 86.95, lat: 27.8, dist: 3.2, el: 28, yaw: -7 }, C(2, 1, .9), C(2, 3, -.2) - C(2, 1, .9), 'sine.inOut'); key(SA.pinA, 0, C(2, 3, 0), .3);
  key(SA.tk, { lon: 90.4, lat: 23.1, dist: 8, el: 62, yaw: 6 }, C(2, 3, -.2), 1.0, 'power3.inOut');
  key(SA.tk, { lon: 86.5, lat: 25.6, dist: 44, el: 88, yaw: 0 }, C(2, 4, .3), .9, 'power3.inOut'); key(SA.fA, 1, C(2, 4, .3), .5); key(SA.fB, 1, C(2, 4, .3), .5);
  key(SA.tk, { lon: 86.5, lat: 25.6, dist: 42, el: 87, yaw: -2 }, C(2, 4, 1.2), Math.max(.3, C(3, 0) - C(2, 4, 1.2)), 'sine.inOut');

  // ===== WA: Guinea + the UK (pair #4) =====
  key(WA.tk, { lon: -11.0, lat: 10.6, dist: 20, el: 87, yaw: 2 }, C(3, 0, -.15), C(3, 1, .2) - C(3, 0, -.15), 'sine.inOut'); key(WA.tk, { lon: -10.9, lat: 11.0, dist: 26, el: 88, yaw: 0 }, C(3, 1, .25), .8, 'power3.inOut'); key(WA.tk, { lon: -10.9, lat: 11.0, dist: 24.5, el: 87, yaw: 2 }, C(3, 1, 1.1), C(4, 1) - C(3, 1, 1.1), 'sine.inOut');
  on(WA.fA, WT(3, 1, 'GUINEA', 'गिनी', -.05), .35);
  { const tu = WT(3, 1, 'UNITED', 'यूनाइटेड', .05); on(WA.uk.a, tu, .25); key(WA.uk.z, 0, tu, .6, 'bounce.out'); }
  key(WA.tk, { lon: -10.9, lat: 11.0, dist: 23.5, el: 86, yaw: -2 }, C(4, 1), C(6, 0) - C(4, 1), 'sine.inOut');
  key(WA.uk.grey, 1, C(5, 0, -.3), .5, 'power2.inOut');
  chIn(WA.cGb, C(5, 0, -.4)); mouth(WA.cGb, LN[5].a, LN[5].b, .22); bob(WA.cGb, LN[5].a, LN[5].b + .2);
  WA.cGb.tears.forEach((tr, i) => tl.fromTo(tr, { y: 0, opacity: 0 }, { keyframes: [{ opacity: 1, duration: .1 }, { y: 120, duration: .7, ease: 'power2.in' }, { opacity: 0, duration: .1 }], repeat: 1, ...IR }, LN[5].a + i * .15));
  chOut(WA.cGb, C(6, 0, -.3));

  // ===== ZC: Zambia stretched into Chile (pair #3) =====
  key(ZC.tk, { lon: 25.5, lat: -13, dist: 32, el: 87, yaw: 2 }, C(6, 0, -.15), C(7, 0) - C(6, 0, -.15), 'sine.inOut');
  { const tc = WT(6, 1, 'CHILE', 'चिली', -.05); key(ZC.cl.d, { x: -30, y: 0 }, 0, .01); on(ZC.cl.a, tc, .2); key(ZC.cl.z, 0, tc, .01); key(ZC.cl.d, { x: 0, y: 0 }, tc, .7, 'power3.out'); }
  on(ZC.fA, WT(6, 1, 'ZAMBIA', 'ज़ाम्बिया', -.05), .35);
  key(ZC.tk, { lon: 20.3, lat: -13.2, dist: 88, el: 89, yaw: 0 }, C(7, 0, -.1), 1.0, 'power3.inOut');
  on(ZC.mo.a, C(7, 0, .25), .15); key(ZC.fA, 0, C(7, 0, .3), .15);
  key(ZC.mo.p, 1, C(7, 1, -.05), Math.max(1.2, C(7, 2, .2) - C(7, 1, -.05)), 'power2.inOut');
  key(ZC.tk, { lon: 20.3, lat: -13.3, dist: 85, el: 88, yaw: -1 }, C(7, 1, .9), C(8, 0) - C(7, 1, .9), 'sine.inOut');

  // ===== IT: Italy + the Philippines = a body (pair #2) =====
  key(IT.tk, { lon: 12.6, lat: 42.2, dist: 28, el: 86, yaw: 3 }, C(8, 0, -.15), C(8, 1) - C(8, 0, -.15), 'sine.inOut');
  on(IT.fA, WT(8, 1, 'ITALY', 'इटली', -.05), .35);
  { const tp = WT(8, 1, 'PHILIPPINES', 'फिलीपींस', -.1); key(IT.ph.d, { x: 46, y: -3.2 }, 0, .01); key(IT.ph.z, 0, 0, .01); on(IT.ph.a, tp, .2); key(IT.ph.d, { x: 18.6, y: -3.2 }, tp, .8, 'power3.out');
    key(IT.tk, { lon: 21.5, lat: 48.5, dist: 64, el: 89, yaw: 0 }, tp - .1, .9, 'power3.inOut'); }
  key(IT.tk, { lon: 21.3, lat: 48.6, dist: 62, el: 88, yaw: -1 }, C(9, 0), C(10, 0) - C(9, 0), 'sine.inOut');
  { const tt = WT(10, 0, 'TOGETHER', 'जोड़', -.25); key(IT.ph.d, { x: 0, y: 0 }, tt, .7, 'power3.inOut'); key(IT.tk, { lon: 12.6, lat: 49.8, dist: 56, el: 89, yaw: 0 }, tt, .8, 'power3.inOut'); }
  key(IT.tk, { lon: 12.6, lat: 49.8, dist: 54, el: 87, yaw: 2 }, C(10, 1), C(11, 0) - C(10, 1), 'sine.inOut');

  // ===== SEA: number one, Malaysia + Vietnam, then back out to the globe (loop) =====
  key(SEA.x, 1, 0, .01);
  key(SEA.tk, { lon: 109.4, lat: 9.6, dist: 72, el: 87, yaw: 1 }, C(11, 0), C(12, 0) - C(11, 0), 'sine.inOut');
  on(SEA.fA, WT(11, 1, 'MALAYSIA', 'मलेशिया', -.05), .35); on(SEA.fB, WT(11, 1, 'VIETNAM', 'वियतनाम', -.05), .35);
  on(SEA.hl, WT(11, 0, 'ONE', 'वन', 0), .5); key(SEA.hl, 0, C(12, 0), .6);
  key(SEA.tk, { lon: 109.4, lat: 9.7, dist: 70, el: 86, yaw: -1 }, C(12, 0), C(13, 0) - C(12, 0), 'sine.inOut');
  key(SEA.tk, { lon: 109.4, lat: 9.8, dist: 71, el: 87, yaw: 1 }, C(13, 0, -.2), C(14, 0) - C(13, 0, -.2), 'sine.inOut');
  chIn(SEA.cMy, C(13, 0, -.4)); chIn(SEA.cVn, C(13, 0, -.25)); bob(SEA.cMy, LN[13].a, LN[13].b); bob(SEA.cVn, LN[13].a + .1, LN[13].b);
  tl.fromTo(heart, { opacity: 0, scale: .2 }, { opacity: 1, scale: 1, duration: .45, ease: 'back.out(2.4)', ...IR }, WT(13, 0, 'MADE', 'एक-दूसरे', 0));
  tl.to(heart, { keyframes: [{ scale: 1.18, duration: .15 }, { scale: 1, duration: .2 }, { scale: 1.18, duration: .15 }, { scale: 1, duration: .2 }] }, WT(13, 0, 'MADE', 'एक-दूसरे', .5));
  tl.to(heart, { opacity: 0, scale: .4, duration: .3 }, C(14, 0, -.15));
  chOut(SEA.cMy, C(14, 0, -.15)); chOut(SEA.cVn, C(14, 0, -.1));
  { const a = C(14, 0, .05); key(SEA.gk, { lon: 109.4, lat: 9.6, dist: 2.3 }, 0, .01); key(SEA.x, 0, a, .5, 'power1.inOut'); key(SEA.tk, { lon: 109.4, lat: 9.8, dist: 80, el: 88, yaw: 0 }, a - .2, .7, 'power2.in');
    key(SEA.fA, 0, a, .4); key(SEA.fB, 0, a, .4); key(SEA.gk, D.loopPose, a + .05, D.dur - a - .05, 'power2.inOut'); }

  // ===== spec-driven beats =====
  const beat = k => (D.beats || []).filter(b => b.kind === k);
  const nextChunk = t => { const c = D.chunks.find(c => c.sn > t + .5); return c ? c.sn - .12 : t + 2; };
  for (const L of LBL) { const b = L.b; key(L.a, 1, b.t, .25, 'power3.out'); key(L.pop, .3, b.t, .1, 'power2.out'); key(L.pop, 0, b.t + .1, .3, 'power2.inOut'); key(L.a, 0, b.u, .25);
    if (b.fall) { key(L.dy, 340, b.fall, .7, 'power2.in'); key(L.rot, 50, b.fall, .7, 'power2.in'); key(L.a, 0, b.fall + .45, .25); } }
  for (const b of beat('circle')) { const S = REG[b.scene]; const r = b.r || [200, 110];
    MO.hwCircle(S.ov, t => S.proj(t, b.c[0], b.c[1]), r[0], r[1], b.t, b.u || nextChunk(b.t), { seed: 3 + b.t, col: b.col }); }
  for (const b of beat('arrow')) { const S = REG[b.scene];
    MO.hwArrow(S.ov, t => { const p0 = S.proj(t, b.from[0], b.from[1]), p1 = S.proj(t, b.to[0], b.to[1]); return { x0: p0.x, y0: p0.y, x1: p1.x, y1: p1.y }; }, b.t, b.u || nextChunk(b.t), { seed: 7 + b.t, col: b.col }); }
  for (const b of beat('card')) { const S = REG[b.scene]; const Cd = mkCard(S, b); key(Cd.a, 1, b.t, .35, 'power3.out'); key(Cd.a, 0, b.u || nextChunk(b.t), .25);
    MO.countGrow(Cd.num, b.to, b.t + .1, { dur: 1.1, startScale: .5 }); }
  for (const b of beat('slam')) if (b.what === 'rank') { const el = RK[b.n];
    tl.fromTo(el, { opacity: 0, scale: 2.6, x: 0, y: 0 }, { opacity: 1, scale: 1, duration: .32, ease: 'power4.out', ...IR }, b.t);
    if (b.n === 1) { shake(b.t + .1, .9); flash(b.t + .05); tl.fromTo(el.querySelector('.crown'), { y: -260, opacity: 0, rotation: -30 }, { y: 0, opacity: 1, rotation: -12, duration: .5, ease: 'back.out(2)', ...IR }, b.t + .2);
      tl.fromTo(el.querySelector('.rays'), { opacity: 0, scale: .3 }, { opacity: .9, scale: 1, duration: .5, ease: 'power3.out', ...IR }, b.t);
      tl.to(el, { scale: 1.07, duration: .5, yoyo: true, repeat: 3, ease: 'sine.inOut' }, b.t + .4); window.__CONF = b.t + .05; }
    else shake(b.t + .08, .45);
    tl.to(el, { x: -330, y: -150, scale: .42, duration: .5, ease: 'power3.inOut' }, b.u); if (b.n === 1) tl.to(el.querySelector('.rays'), { opacity: 0, duration: .4 }, b.u);
    tl.to(el, { opacity: 0, duration: .25 }, b.off); }
  else if (b.what === 'land') { shake(b.t, .5); }
  for (const b of beat('flashfx')) flash(b.t);
  for (const s of D.impacts || []) shake(s, .75);
  for (const s of D.hand || []) MO.shake(s[0], s[1] - s[0], 'handheld-normal-mild', .1, { decay: false });
  const cs = beat('charslam')[0];
  for (const id in TT) { const { g, t } = TT[id];
    if (id === 'tHook' && cs && D.lang !== 'hi') { tl.set(g, { opacity: 1 }, cs.t); MO.charSlam(TT.tHook.lines[0], cs.t, { blur: false }); if (TT.tHook.lines[1]) MO.textIn(TT.tHook.lines[1], cs.t + .6); }
    else MO.textIn(g, t.a);
    MO.textOut(g, t.b); }
  for (const K of CAPS) { const c = K.c;
    tl.set(K.g, { opacity: 1 }, c.sn); tl.set(K.g, { opacity: 0 }, c.en);
    tl.fromTo(K.g, { scale: .9, transformOrigin: '565px 1385px' }, { scale: 1, duration: .2, ease: 'power3.out', ...IR }, c.sn);
    MO.karaoke(K.words, c.wt, w => w.classList.contains('k'));
    K.words.forEach((w, i) => { if (w.classList.contains('k')) MO.sweep(w, c.wt[Math.min(i, c.wt.length - 1)]); }); }
  const BW = $('badgeWrap'); const bs = 108 / 620; tl.set(BW, { opacity: 1, x: 44 - 230, y: 1332 - 450, scale: bs }, 0);
  layout();
  MO.shakeOn($('cshake'), D.dur);
  for (const T of ALLT) T.keys.sort((a, b) => a.a - b.a);
  const clk = { t: 0 };
  tl.fromTo(clk, { t: 0 }, { t: D.dur, duration: D.dur, ease: 'none', ...IR, onUpdate: () => { const t = clk.t;
    const live = S => S.wins.some(w => t >= w[0] - .05 && t <= w[1] + .45);
    for (const S of SCENES) if (live(S)) S.render(t);
    XF.render(t);
    const r1 = RK[1].querySelector('.rays'); r1.style.transform = `rotate(${(t * 40).toFixed(1)}deg)`;
    const t0 = window.__CONF; for (const p of CONF) { const u = t - (t0 || 1e9); if (u < 0 || u > 2.6) { p.e.style.opacity = 0; continue; }
      const x = 540 + Math.cos(p.a) * p.v * u * .55, y = 300 - Math.abs(Math.sin(p.a)) * p.v * u * .9 + 1100 * u * u;
      p.e.style.opacity = Math.max(0, 1 - u / 2.6); p.e.style.transform = `translate(${x.toFixed(1)}px,${y.toFixed(1)}px) rotate(${(p.sp * u).toFixed(1)}deg)`; } } }, 0);
  window.__C = {}; if (D.thumb) ['caps', 'ranks', 'titles', 'hook', 'badgeWrap'].forEach(i => $(i).style.display = 'none');
  if (D.t1) { const outer = gsap.timeline({ paused: true }); outer.add(tl.tweenFromTo(D.t0, D.t1, { ease: 'none' }), 0); return outer; }
  return tl;
}
window.__timelines = window.__timelines || {};
document.fonts.ready.then(() => Promise.all(READY)).then(() => { window.__timelines['main'] = build(); });
