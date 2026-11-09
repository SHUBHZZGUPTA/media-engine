
/* ---------- timeline ---------- */
function build() {
  layout();
  const tl = gsap.timeline({ paused: true }); const IR = { immediateRender: false };
  const MO = BhugolMotion(tl, { xfade: false });
  const PL = D.shots.map(s => ({ S: SC[s.scene], el: SC[s.scene].el, at: s.t, cut: s.cut }));
  for (const S of [MW, MV, MI, XS]) S.wins = [];
  PL.forEach((p, i) => { p.S.wins.push([i ? p.at - .45 : 0, i < PL.length - 1 ? PL[i + 1].at + .1 : D.dur + 1]); });
  MO.shots(PL); tl.set(PL[0].el, { opacity: 1 }, 0);
  for (const b of D.beats || []) if (b.kind === 'punch') MO.punch(SC[b.scene].push, b.t, b.level, b.back);
  const on = (T, at, d, v, e) => key(T, v === undefined ? 1 : v, at, d || .4, e || 'power1.inOut');
  const off = (T, at, d) => key(T, 0, at, d || .3, 'power1.inOut');
  const bcam = (S, to, at, dur, e) => key(S.cam0, to, at, dur, e || 'sine.inOut');
  const bset = (S, s) => { S.cam0.base = S.cam0.last = Object.assign({ x: 0, y: 0, z: 0, dist: 3.4, yaw: 0, pitch: 14 }, s); };
  const U = (S, k, base) => (S.uT[k] = S.uT[k] || Track(base === undefined ? 0 : base));
  const popD = (el, at) => tl.fromTo(el, { opacity: 0, scale: .3, y: 80 }, { opacity: 1, scale: 1, y: 0, duration: .4, ease: 'back.out(2.2)', ...IR }, at);
  const fade = (el, at, d) => tl.to(el, { opacity: 0, duration: d || .3 }, at);
  const shake = (at, k) => MO.shake(at, .6, 'rig-6d-wobble', k || .75);
  const nextChunk = t => { const c = D.chunks.find(c => c.sn > t + .5); return c ? c.sn - .12 : t + 2; };
  const tk = (S, v, at, d, e) => key(S.tk, v, at, d || .01, e || 'power2.inOut');
  const setTk = (S, v) => { S.tk.base = S.tk.last = v; };
  const end = D.end.start;
  const allOn = (S, a) => { for (const r of [S.dan, S.rhi]) { r.a.base = r.a.last = a; r.prog.base = r.prog.last = 1; } };

  /* ===== MW: globe -> Europe, Danube draws (hook); Vienna/Bratislava (L2-3); four capitals (L5); Rhine payoff (L12); outro (L15) ===== */
  MW.gk.base = MW.gk.last = { lon: -12, lat: 32, dist: 3.3 };
  key(MW.gk, { lon: 15, lat: 47, dist: 1.5 }, .05, C(0, 1, -.15) - .05, 'power2.inOut');
  key(MW.x, 1, C(0, 1, -.45), .6, 'power1.inOut');
  setTk(MW, { lon: 17.5, lat: 46.6, dist: 34, el: 72, yaw: -55 });
  tk(MW, { lon: 18.6, lat: 46.4, dist: 27, el: 68, yaw: -90 }, C(0, 1, -.3), C(0, 3) - C(0, 1, -.3), 'power2.out');
  tk(MW, { lon: 11.0, lat: 47.6, dist: 13, el: 62, yaw: -70 }, C(0, 3), C(1, 0) - C(0, 3) + .3, 'power2.inOut');
  MW.dan.a.base = MW.dan.a.last = 0; on(MW.dan.a, C(0, 0, .2), .3); key(MW.dan.prog, 1, C(0, 0, .25), C(0, 2) - C(0, 0, .25), 'power1.inOut');
  const capDots = S => CAPS4.map(c => mapDot(S, c[1], c[2], 0xFF7A1A, .022));
  const dW = capDots(MW), dV = capDots(MV);
  dW.forEach((d, i) => on(d.a, C(0, 1, .05 + i * .12), .25));
  /* hook teaser: the upper Danube blinks near its start */
  key(MW.up.prog, 1, C(0, 4), .01); on(MW.up.a, C(0, 4, .05), .2); off(MW.up.a, C(0, 4, .45), .2); on(MW.up.a, C(0, 4, .7), .2); off(MW.up.a, C(1, 0, -.2), .2);
  /* L2: Vienna -> Bratislava */
  tk(MW, { lon: 16.6, lat: 48.0, dist: 4.4, el: 62, yaw: -10 }, C(2, 0, -.3), .01);
  tk(MW, { lon: 16.7, lat: 48.1, dist: 3.5, el: 64, yaw: -4 }, C(2, 0, -.15), C(2, 2) - C(2, 0, -.15), 'sine.inOut');
  tk(MW, { lon: 16.85, lat: 48.1, dist: 3.2, el: 64, yaw: 4 }, C(2, 2), C(4, 0) - C(2, 2), 'sine.inOut');
  /* L5: pull back over all four capitals */
  tk(MW, { lon: 18.5, lat: 46.6, dist: 12, el: 62, yaw: -6 }, C(5, 0, -.3));
  tk(MW, { lon: 18.5, lat: 46.4, dist: 15.5, el: 64, yaw: 2 }, C(5, 0, -.15), C(6, 0) - C(5, 0, -.15), 'power2.out');
  dW.forEach((d, i) => { key(d.a, 1.6, C(5, 1, i * .1), .15); key(d.a, 1, C(5, 1, .25 + i * .1), .3); });
  /* L12: Rhine to the North Sea (payoff) */
  tk(MW, { lon: 8.6, lat: 48.6, dist: 6, el: 58, yaw: 0 }, C(12, 0, -.3));
  tk(MW, { lon: 6.6, lat: 50.4, dist: 14, el: 64, yaw: 0 }, C(12, 0, -.15), C(12, 2) - C(12, 0, -.15), 'power2.inOut');
  key(MW.rhi.a, 0, C(12, 0, -.3), .01); key(MW.rhi.prog, 0, C(12, 0, -.3), .01);
  on(MW.rhi.a, C(12, 0, -.1), .3); key(MW.rhi.prog, 1, C(12, 0, .1), C(12, 1, .4) - C(12, 0, .1), 'power1.inOut');
  key(MW.dan.a, .45, C(12, 0, -.3), .01);
  /* L15: outro, everything on */
  tk(MW, { lon: 15, lat: 47.0, dist: 16, el: 64, yaw: -60 }, C(15, 0, -.3));
  tk(MW, { lon: 18.6, lat: 46.4, dist: 27, el: 70, yaw: -90 }, C(15, 0, -.15), end - C(15, 0, -.15) + 2, 'power2.out');
  key(MW.dan.a, 1, C(15, 0, -.2), .3); key(MW.rhi.a, 1, C(15, 2), .5);
  dW.forEach((d, i) => { key(d.a, 1.6, C(15, 0, i * .1), .15); key(d.a, 1, C(15, 0, .25 + i * .1), .3); });
  key(MW.up.prog, 1, C(15, 3), .01); on(MW.up.a, C(15, 3, .1), .2); off(MW.up.a, C(15, 3, .5), .2); on(MW.up.a, C(15, 3, .8), .2); off(MW.up.a, end - .3, .3);
  const lNS = mapLabel(MW, 'NORTH SEA', 4.9, 53.7, 70, '#7CC4FF'), lRh = mapLabel(MW, 'RHINE', 7.0, 50.6, 64, '#7CC4FF', 70, 0);
  on(lRh.a, C(12, 0, .6), .3); on(lNS.a, C(12, 1, .1), .3); off(lRh.a, C(13, 0, -.3)); off(lNS.a, C(13, 0, -.3));
  const lDanW = mapLabel(MW, 'DANUBE', 23.5, 44.2, 70, '#FFD36A'); on(lDanW.a, C(0, 1, .4), .3); off(lDanW.a, C(0, 3, .2));

  /* ===== MV: source -> Black Sea (L1); Budapest/Belgrade (L4); back to the source (L6); German states (L13) ===== */
  MV.x.base = MV.x.last = 1; allOn(MV, 1); MV.dan.prog.base = MV.dan.prog.last = 0;
  setTk(MV, { lon: 8.55, lat: 47.85, dist: 4.0, el: 62, yaw: -14 });
  tk(MV, { lon: 8.55, lat: 47.98, dist: 3.2, el: 64, yaw: -6 }, C(1, 0, -.15), C(1, 2) - C(1, 0, -.15), 'sine.inOut');
  tk(MV, { lon: 22.5, lat: 45.6, dist: 22, el: 64, yaw: -90 }, C(1, 2), C(2, 0) - C(1, 2) + .2, 'power2.inOut');
  key(MV.dan.prog, .06, C(1, 0, -.15), C(1, 2) - C(1, 0, -.15), 'sine.inOut'); key(MV.dan.prog, 1, C(1, 2), C(2, 0) - C(1, 2) + .1, 'power2.inOut');
  key(MV.rhi.a, 0, 0, .01);
  const lBF = mapLabel(MV, 'BLACK FOREST', 8.15, 48.25, 66, '#FFFFFF'); on(lBF.a, C(1, 1, .05), .3); off(lBF.a, C(1, 2, .3));
  const dSrc = mapDot(MV, 8.18, 48.09, 0xFFC23A, .06); on(dSrc.a, C(1, 1), .3); off(dSrc.a, C(1, 2, .4));
  const lBS = mapLabel(MV, 'BLACK SEA', 29.4, 44.4, 76, '#7CC4FF'); on(lBS.a, C(1, 2, .6), .3); off(lBS.a, C(2, 0, -.2));
  /* L4 */
  tk(MV, { lon: 19.0, lat: 47.4, dist: 3.8, el: 62, yaw: -8 }, C(4, 0, -.3));
  tk(MV, { lon: 19.05, lat: 47.5, dist: 3.1, el: 64, yaw: 0 }, C(4, 0, -.15), C(4, 2) - C(4, 0, -.15), 'sine.inOut');
  tk(MV, { lon: 20.42, lat: 44.82, dist: 3.2, el: 64, yaw: 6 }, C(4, 2, -.1), C(5, 0) - C(4, 2, -.1) + .2, 'power2.inOut');
  key(MV.dan.prog, 1, C(4, 0, -.3), .01); dV.forEach(d => { key(d.a, 1, C(4, 0, -.3), .01); });
  /* L6: back toward the source; Germany flag; the river near the start flickers out */
  tk(MV, { lon: 10.5, lat: 48.0, dist: 9, el: 60, yaw: -8 }, C(6, 0, -.3));
  tk(MV, { lon: 8.7, lat: 47.95, dist: 3.0, el: 62, yaw: -4 }, C(6, 0, -.15), C(6, 1, .2) - C(6, 0, -.15), 'power2.out');
  tk(MV, { lon: 8.72, lat: 47.95, dist: 2.6, el: 62, yaw: 0 }, C(6, 1, .2), C(7, 0) - C(6, 1, .2) + .2, 'sine.inOut');
  dV.forEach(d => off(d.a, C(6, 0, -.3), .01));
  
  key(MV.up.prog, 1, C(6, 3), .01); key(MV.up.a, 0, C(6, 3), .01);
  for (let i = 0; i < 4; i++) key(MV.dan.a, i % 2 ? 1 : .15, C(6, 3, .05 + i * .14), .07);
  key(MV.dan.a, .25, C(6, 3, .7), .2);
  /* L13: the German states */
  tk(MV, { lon: 8.7, lat: 47.98, dist: 3.2, el: 62, yaw: -6 }, C(13, 0, -.3));
  tk(MV, { lon: 8.65, lat: 47.95, dist: 2.7, el: 62, yaw: 4 }, C(13, 0, -.15), C(14, 0) - C(13, 0, -.15) + .2, 'sine.inOut');
  key(MV.dan.a, 1, C(13, 0, -.3), .01); 
  const dSinkV = mapDot(MV, SINK[0], SINK[1], 0x5CFF8A, .07); on(dSinkV.a, C(13, 0, .2), .3);
  popD(eLaw, C(13, 0, .05)); fade(eLaw, C(14, 0, -.3), .2);

  /* ===== flags laid on each country's land (+ country names) ===== */
  key(MW.fA3, .75, C(0, 1), .5, 'power2.out'); key(MW.fA3, 0, C(2, 0, -.3), .01); key(MW.fA1, .75, C(2, 0, -.3), .01); key(MW.fA1, 0, C(12, 0, -.3), .01); key(MW.fA2, .6, C(12, 0, -.3), .01); key(MW.fA2, 0, C(15, 0, -.3), .01); key(MW.fA3, .75, C(15, 0, -.3), .01);
  key(MV.fA2, .55, 0, .01); key(MV.fA2, 0, C(1, 2, .4), .6);
  key(MV.fA1, .75, C(4, 0, -.3), .01); key(MV.fA1, 0, C(6, 0, -.3), .01); key(MV.fA2, .5, C(6, 0, -.3), .01);
  MI.fA1.base = MI.fA1.last = .38;
  const cl = (S, txt, lo, la, a, z, fs, dy) => { const L = mapLabel(S, txt, lo, la, fs || 54, '#FFFFFF', 0, dy || 0); on(L.a, a, .3); off(L.a, Math.max(z, a + .9), .3); return L; };
  cl(MW, 'AUSTRIA', 16.5, 47.95, C(2, 1, .2), C(4, 0, -.3), 54, -330); cl(MW, 'SLOVAKIA', 17.12, 48.42, C(3, 0, .05), C(4, 0, -.3));
  cl(MV, 'HUNGARY', 19.35, 47.3, C(4, 0, .3), C(4, 2, .2), 54, -220); cl(MV, 'SERBIA', 20.75, 44.55, C(4, 2, .8), C(5, 0, -.3));
  cl(MV, 'GERMANY', 8.9, 48.14, C(1, 0, .1), C(1, 2, .2));
  cl(MV, 'GERMANY', 9.2, 48.2, C(6, 1, .3), C(7, 0, -.3)); cl(MV, 'GERMANY', 8.95, 48.12, C(13, 0, .3), C(14, 0, -.3));
  cl(MI, 'GERMANY', 8.68, 47.985, C(7, 0, .2), C(8, 0, -.3));
  cl(MI, 'GERMANY', 8.62, 48.06, C(14, 0, .2), C(15, 0, -.3));
  /* ===== MI: Immendingen (L7); 60 hours / spring / Lake Constance (L11); twist (L14) ===== */
  MI.x.base = MI.x.last = 1; allOn(MI, 1); MI.rhi.a.base = MI.rhi.a.last = .9;
  setTk(MI, { lon: 8.62, lat: 47.98, dist: .62, el: 46, yaw: -24 });
  tk(MI, { lon: 8.70, lat: 47.95, dist: .42, el: 44, yaw: -12 }, C(7, 0, -.15), C(7, 2) - C(7, 0, -.15), 'sine.inOut');
  tk(MI, { lon: 8.73, lat: 47.935, dist: .26, el: 48, yaw: -4 }, C(7, 2), C(8, 0) - C(7, 2) + .2, 'power2.inOut');
  const dSink = mapDot(MI, SINK[0], SINK[1], 0x5CFF8A, .07), dSpr = mapDot(MI, SPRING[0], SPRING[1], 0x4FB3FF, .08);
  on(dSink.a, C(7, 1, .05), .3);
  /* L11 */
  tk(MI, { lon: 8.80, lat: 47.89, dist: .62, el: 52, yaw: -6 }, C(11, 0, -.3));
  tk(MI, { lon: 8.84, lat: 47.86, dist: .5, el: 50, yaw: 2 }, C(11, 0, -.15), C(11, 2) - C(11, 0, -.15), 'sine.inOut');
  tk(MI, { lon: 8.92, lat: 47.77, dist: .78, el: 52, yaw: 6 }, C(11, 2), C(12, 0) - C(11, 2) + .2, 'power2.inOut');
  key(MI.und.prog, 0, C(11, 0, -.3), .01); on(MI.und.a, C(11, 1, -.1), .2); key(MI.und.prog, 1, C(11, 1), C(11, 2) - C(11, 1), 'power1.inOut');
  key(MI.aach.prog, 0, 0, .01); on(MI.aach.a, C(11, 2), .2); key(MI.aach.prog, 1, C(11, 2, .05), C(11, 3) - C(11, 2), 'power1.inOut');
  on(dSpr.a, C(11, 2), .3);
  /* L14 twist: upper Danube turns blue, route glows */
  tk(MI, { lon: 8.62, lat: 47.95, dist: .8, el: 56, yaw: -10 }, C(14, 0, -.3));
  tk(MI, { lon: 8.80, lat: 47.875, dist: .78, el: 56, yaw: 0 }, C(14, 0, -.15), end - C(14, 0, -.15), 'sine.inOut');
  key(MI.und.prog, 1, C(14, 0, -.3), .01); key(MI.aach.prog, 1, C(14, 0, -.3), .01); key(MI.und.a, 1, C(14, 0, -.3), .01); key(MI.aach.a, 1, C(14, 0, -.3), .01);
  key(MI.und.a, 1.8, C(14, 1), .5); key(MI.dan.a, .35, C(14, 2), .4);
  key(MI.up.prog, 0, C(14, 2, -.1), .01); on(MI.up.a, C(14, 2), .2); key(MI.up.prog, 1, C(14, 2, .05), C(14, 3, .3) - C(14, 2), 'power1.inOut');

  /* ===== XS: the karst block (L8-L10) ===== */
  bset(XS, { x: -.35, y: -.15, z: .1, dist: 3.4, yaw: -18, pitch: 26 });
  bcam(XS, { x: -.45, y: -.25, dist: 2.7, yaw: -8, pitch: 22 }, C(8, 0, -.15), C(8, 2) - C(8, 0, -.15));
  bcam(XS, { x: 0, y: -.3, dist: 3.6, yaw: 6, pitch: 30 }, C(8, 2), C(9, 0) - C(8, 2), 'power2.inOut');
  bcam(XS, { x: -.3, y: -.25, dist: 2.4, yaw: -14, pitch: 24 }, C(9, 0, -.05), C(10, 0) - C(9, 0, -.05));
  bcam(XS, { x: -.45, y: -.2, dist: 2.2, yaw: -6, pitch: 24 }, C(10, 0), C(10, 2) - C(10, 0));
  bcam(XS, { x: .1, y: -.3, dist: 3.4, yaw: 8, pitch: 24 }, C(10, 2), C(11, 0) - C(10, 2) + .2, 'power2.inOut');
  const XU = k => U(XS, k);
  key(XU('crackA'), 1, C(8, 0, .1), .8, 'power2.out'); key(XU('sinkP'), 1, C(8, 0, .2), C(8, 2) - C(8, 0, .2), 'power1.inOut');
  key(XU('riverA'), 1, 0, .01); key(XU('upA'), 1, 0, .01); key(XU('riverA'), .05, C(8, 3), .9, 'power2.inOut');
  key(XU('dyeA'), 1, C(10, 1), .6); key(XU('condP'), 1, C(10, 2), C(11, 0) - C(10, 2), 'power1.inOut'); key(XU('springA'), 1, C(10, 3, .3), .5);
  const gDye = bGlow(XS, { lon: SINK[0], lat: SINK[1] }, .28, 0x5CFF8A); on(gDye.a, C(10, 1), .3);
  /* SPRING label: English build only (Hindi timing puts it off screen) */
  if (D.lang !== 'hi') { const lSpr = bLabel(XS, 'SPRING', { lon: SPRING[0], lat: SPRING[1] }, 60, '#7CC4FF'); on(lSpr.a, C(10, 3, .4), .3); }

  /* ===== emoji ===== */
  popD(eBus, C(3, 1, .05)); tl.to(eBus, { x: -30, duration: .5, yoyo: true, repeat: 1, ease: 'sine.inOut' }, C(3, 1, .5)); fade(eBus, C(4, 0, -.3), .2);
  const EMO = { trophy: eTrophy, timer: eTimer, salt: eSalt, swap: eSwap };
  for (const sl of (D.beats || []).filter(b => b.kind === 'slam')) { const e = EMO[sl.emo]; if (!e) continue; tl.set(e, { opacity: 1 }, sl.t); MO.slam(e.inner, sl.t); fade(e, nextChunk(sl.t) + .6, .25); }

  /* ===== beats from the spec: circles, arrows, grows, cards, flap ===== */
  const beat = k => (D.beats || []).filter(b => b.kind === k);
  const isMap = S => S === MW || S === MV || S === MI;
  const projQ = (S, q, t) => isMap(S) ? mapProj(S, t, q.lon, q.lat, .003) : bProj(S, q, t);
  for (const b of beat('circle')) { const S = SC[b.scene];
    MO.hwCircle(S.ov, t => projQ(S, b.q, t), (b.r || [200, 110])[0], (b.r || [200, 110])[1], b.t, b.u || nextChunk(b.t), { seed: 3 + b.t, col: b.col }); }
  for (const b of beat('arrow')) { const S = SC[b.scene];
    MO.hwArrow(S.ov, t => { const p0 = projQ(S, b.qf, t), p1 = projQ(S, b.qt, t); return { x0: p0.x, y0: p0.y, x1: p1.x, y1: p1.y }; }, b.t, b.u || nextChunk(b.t), { seed: 7 + b.t, col: b.col }); }
  const wordTime = (b, needle) => { const ch = D.chunks.find(c => Math.abs(c.sn - b.t) < .02); const wi = ch ? ch.txt.replace(/\|/g, ' ').split(' ').findIndex(w => w.includes(needle)) : -1; return wi >= 0 ? ch.wt[wi] : null; };
  for (const b of beat('grow')) { const el = mk('div', { class: 'kbox', style: `top:${b.y || 150}px` }, $('hook'));
    el.innerHTML = `<span class="knum">0</span><span class="ksuf">${b.unit || ''}</span>`; if (b.fs) el.style.fontSize = b.fs + 'px';
    const wt = wordTime(b, String(b.to).slice(0, 2)); const dur = wt ? Math.max(.6, wt - b.t + .15) : 1.0; tl.set(el, { opacity: 1 }, b.t);
    MO.countGrow(el.querySelector('.knum'), b.to, b.t, { dur, from: b.from || 0, prefix: b.prefix, startScale: .35, suffixEl: el.querySelector('.ksuf') }); MO.textOut(el, b.u || nextChunk(b.t)); }
  for (const b of beat('card')) { const S = SC[b.scene]; const Cd = mkCard(S, b); key(Cd.a, 1, b.t, .35, 'power3.out'); key(Cd.a, 0, b.u || nextChunk(b.t), .25);
    if (b.to) MO.countGrow(Cd.num, b.to, b.t + .1, { dur: 1.0, startScale: .5, suffixEl: Cd.suf }); }
  for (const b of beat('flap')) { const box = mk('div', { class: 'kbox', style: `top:${b.y || 260}px` }, $('hook')); const row = mk('div', { class: 'flapRow' }, box);
    tl.set(box, { opacity: 1 }, b.t - .02); MO.flap(row, b.text, b.t); MO.textOut(box, b.u || nextChunk(b.t)); }
  MO.shake(0, C(1, 0, -.15), 'handheld-normal-mild', .1, { decay: false });
  shake(C(12, 2, .05), .6);
  /* titles: hook charslam */
  const cs = beat('charslam')[0];
  for (const id in TT) { const { g, t } = TT[id];
    if (id === 'tHook' && cs) { tl.set(g, { opacity: 1 }, cs.t); MO.charSlam(TT.tHook.lines[0], cs.t, { blur: true }); } else MO.textIn(g, t.a);
    MO.textOut(g, t.b); }
  /* captions */
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
  const allT = [];
  for (const S of BLOCKS) allT.push(S.cam0, ...Object.values(S.uT), ...S.parts.map(p => p.a), ...S.glows.map(g => g.a), ...S.labels.map(l => l.a), ...S.emos.map(e => e.a));
  for (const S of MAPS) allT.push(S.gk, S.tk, S.x, S.hl, S.rise, S.pinA, S.flagA, S.fA1, S.fA2, S.fA3, ...S.cards.map(c => c.a), ...S.lls.map(l => l.a), ...S.dots.map(d => d.a), ...S.rivers.flatMap(r => [r.a, r.prog, r.from]));
  for (const T of allT) T.keys.sort((a, b) => a.a - b.a);
  const clk = { t: 0 };
  tl.fromTo(clk, { t: 0 }, { t: D.dur, duration: D.dur, ease: 'none', ...IR, onUpdate: () => { const t = clk.t;
    const live = S => S.wins.some(w => t >= w[0] - .05 && t <= w[1] + .45);
    for (const S of BLOCKS) if (live(S)) renderBlock(S, t);
    for (const S of MAPS) if (live(S)) renderMap(S, t); } }, 0);
  return tl;
}
window.__timelines = window.__timelines || {};
document.fonts.ready.then(() => Promise.all(READY)).then(() => { window.__timelines['main'] = build(); });
</script>
</body>
</html>
