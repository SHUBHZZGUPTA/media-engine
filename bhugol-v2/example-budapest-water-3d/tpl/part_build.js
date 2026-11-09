
/* ---------- timeline ---------- */
function build() {
  layout();
  const tl = gsap.timeline({ paused: true }); const IR = { immediateRender: false };
  const MO = BhugolMotion(tl, { xfade: false });
  const PL = D.shots.map(s => ({ S: SC[s.scene], el: SC[s.scene].el, at: s.t, cut: s.cut }));
  for (const S of [MP, MQ, XS, CV]) S.wins = [];
  PL.forEach((p, i) => { p.S.wins.push([i ? p.at - .45 : 0, i < PL.length - 1 ? PL[i + 1].at + .1 : D.dur + 1]); });
  MO.shots(PL); tl.set(PL[0].el, { opacity: 1 }, 0);
  for (const b of D.beats || []) if (b.kind === 'punch') MO.punch(SC[b.scene].push, b.t, b.level, b.back);
  const on = (T, at, d, v, e) => key(T, v === undefined ? 1 : v, at, d || .4, e || 'power1.inOut');
  const bcam = (S, to, at, dur, e) => key(S.cam0, to, at, dur, e || 'sine.inOut');
  const bset = (S, s) => { S.cam0.base = S.cam0.last = Object.assign({ x: 0, y: 0, z: 0, dist: 3.4, yaw: 0, pitch: 14 }, s); };
  const U = (S, k, base) => (S.uT[k] = S.uT[k] || Track(base === undefined ? 0 : base));
  const both = (k, v, at, d, e) => { for (const S of BLOCKS) key(U(S, k), v, at, d, e || 'power1.inOut'); };
  const popD = (el, at) => tl.fromTo(el, { opacity: 0, scale: .3, y: 80 }, { opacity: 1, scale: 1, y: 0, duration: .4, ease: 'back.out(2.2)', ...IR }, at);
  const fade = (el, at, d) => tl.to(el, { opacity: 0, duration: d || .3 }, at);
  const shake = (at, k) => MO.shake(at, .6, 'rig-6d-wobble', k || .75);
  const nextChunk = t => { const c = D.chunks.find(c => c.sn > t + .5); return c ? c.sn - .12 : t + 2; };
  const tk = (S, v, at, d, e) => key(S.tk, v, at, d, e || 'power2.inOut');
  const end = D.end.start;

  /* ===== MP: globe -> Hungary -> Budapest (hook), card (L4), outro (L17) ===== */
  MP.gk.base = MP.gk.last = { lon: 8, lat: 33, dist: 3.3 };
  key(MP.gk, { lon: 19.0, lat: 47.4, dist: 1.55 }, .05, C(0, 1, .1) - .05, 'power2.inOut');
  key(MP.x, 1, C(0, 1, -.15), .45, 'power1.inOut');
  MP.tk.base = MP.tk.last = { lon: 19.3, lat: 47.0, dist: 8.5, el: 76, yaw: 0 };
  tk(MP, { lon: 19.2, lat: 47.1, dist: 6.6, el: 66, yaw: 6 }, C(0, 1, -.15), 1.2, 'power2.out');
  tk(MP, { lon: 19.04, lat: 47.47, dist: 1.25, el: 52, yaw: 14 }, C(0, 2, -.2), C(0, 4) - C(0, 2, -.2), 'power2.inOut');
  tk(MP, { lon: 19.04, lat: 47.49, dist: .62, el: 46, yaw: 22 }, C(0, 4), C(1, 0) - C(0, 4) + .3, 'power1.inOut');
  key(MP.hl, 1, C(0, 1), .6); key(MP.rise, 1, C(0, 1, .1), .9, 'power2.out'); key(MP.flagA, .75, C(0, 1, .2), .5, 'power2.out'); key(MP.flagA, 0, C(0, 3), .8);
  key(MP.rise, 0, C(0, 4), .6); key(MP.pinA, 1, C(0, 2, .2), .4);
  MP.labels.push({ e: (() => { const e = mk('div', { class: 'plbl' }, MP.ov); e.textContent = 'BUDAPEST'; Object.assign(e.style, { fontSize: '70px', webkitTextStrokeWidth: '13px' }); return e; })(), a: Track(0) });
  key(MP.labels[0].a, 1, C(0, 2, .3), .3); key(MP.labels[0].a, 0, C(0, 3, .2), .2);
  /* L4: back over Budapest for the 123 card */
  tk(MP, { lon: 19.06, lat: 47.47, dist: .95, el: 50, yaw: -12 }, C(4, 0, -.2), .01);
  tk(MP, { lon: 19.04, lat: 47.49, dist: .72, el: 46, yaw: -4 }, C(4, 0, -.15), C(5, 0) - C(4, 0, -.15), 'sine.inOut');
  /* L17: pull back to Hungary for the outro */
  tk(MP, { lon: 19.04, lat: 47.49, dist: .8, el: 50, yaw: 10 }, C(16, 3, .4), .01);
  tk(MP, { lon: 19.3, lat: 47.1, dist: 7.5, el: 70, yaw: 0 }, C(16, 3, .45), end - C(16, 3, .45) + 1.5, 'power2.inOut');
  key(MP.flagA, .7, C(17, 0, .6), .8); key(MP.rise, 1, C(17, 0, .5), .9);

  /* ===== MQ: low flight over Budapest (Romans/Ottomans), Rozsadomb, then landlocked Hungary ===== */
  MQ.x.base = MQ.x.last = 1; MQ.hl.base = MQ.hl.last = 0;
  MQ.tk.base = MQ.tk.last = { lon: 19.05, lat: 47.545, dist: .5, el: 42, yaw: -28 };
  tk(MQ, { lon: 19.045, lat: 47.515, dist: .44, el: 46, yaw: -14 }, C(5, 0, -.15), C(5, 1) - C(5, 0, -.15), 'sine.inOut');
  tk(MQ, { lon: 19.04, lat: 47.50, dist: .40, el: 50, yaw: -4 }, C(5, 1), C(7, 0) - C(5, 1), 'sine.inOut');
  const dA = mapDot(MQ, 19.0494, 47.5636, 0xFFC23A, .06), dR = mapDot(MQ, 19.0469, 47.4888, 0xFF7A1A, .06), dK = mapDot(MQ, 19.0369, 47.5115, 0xFF7A1A, .06);
  const lA = mapLabel(MQ, 'AQUINCUM', 19.0494, 47.5636 + .005, 58, '#FFC23A'), lR = mapLabel(MQ, 'RUDAS', 19.0469, 47.4888 + .005, 58), lK = mapLabel(MQ, 'KIRÁLY', 19.0369, 47.5115 + .005, 58);
  on(dA.a, C(5, 0, .1), .3); on(lA.a, C(5, 0, .2), .3); on(dR.a, C(5, 1, .05), .3); on(lR.a, C(5, 1, .15), .3); on(dK.a, C(5, 1, .25), .3); on(lK.a, C(5, 1, .35), .3);
  for (const r of [dA, lA, dR, lR, dK, lK]) key(r.a, 0, C(7, 0, -.3), .3);
  popD(eSpa, C(6, 0, .05)); tl.to(eSpa, { y: -14, duration: .5, yoyo: true, repeat: 2, ease: 'sine.inOut' }, C(6, 0, .5)); fade(eSpa, C(7, 0, -.35), .2);
  /* L11: Rozsadomb, a hill full of houses */
  tk(MQ, { lon: 19.03, lat: 47.512, dist: .26, el: 50, yaw: -12 }, C(11, 2, -.2), .01);
  tk(MQ, { lon: 19.03, lat: 47.516, dist: .21, el: 54, yaw: -4 }, C(11, 2, -.15), C(12, 0) - C(11, 2, -.15), 'sine.inOut');
  const dM = mapDot(MQ, 19.0359, 47.5181, 0x5FE0F0, .06); const lM = mapLabel(MQ, 'MOLNÁR JÁNOS CAVE', 19.0359 + .014, 47.5181 - .004, 50, '#7FE9F5');
  on(dM.a, C(11, 2, .05), .3); on(lM.a, C(11, 2, .2), .3); key(dM.a, 0, C(12, 0, -.3), .2); key(lM.a, 0, C(12, 0, -.3), .2);
  /* L13: pull back to landlocked Hungary */
  tk(MQ, { lon: 19.04, lat: 47.49, dist: .9, el: 52, yaw: 0 }, C(13, 1, -.2), .01);
  tk(MQ, { lon: 19.4, lat: 47.1, dist: 7.2, el: 72, yaw: 0 }, C(13, 1, -.15), C(14, 0) - C(13, 1, -.15) + .2, 'power2.inOut');
  key(MQ.hl, 1, C(13, 1, 1.2), .6); key(MQ.flagA, .7, C(13, 1, 1.7), .6); key(MQ.rise, 1, C(13, 1, 1.4), .8, 'power2.out');

  /* ===== blocks: shared geology state ===== */
  both('heatA', .55, C(1, 0, .2), 1.6); both('rainP', 1, C(3, 0, .1), C(3, 2) - C(3, 0, .1), 'power1.inOut');
  both('hotP', 1, C(3, 2, .1), C(4, 0) - C(3, 2, .1), 'power1.inOut'); both('faultA', 1, C(3, 2), .5);
  both('caveP', .45, C(7, 1, -.2), 1.6, 'power2.out'); both('caveP', .72, C(8, 2), 1.2, 'power2.out');
  both('waterA', 1, C(10, 1, -.05), 1.0, 'power2.out'); both('rainP', 0, C(7, 0, -.2), .01); both('hotP', 0, C(7, 0, -.2), .01);
  both('rainP', 1, C(8, 0, .1), .9); both('hotP', 1, C(8, 2, -.05), .9); both('rainP', 0, C(9, 0, -.3), .01); both('hotP', 0, C(9, 0, -.3), .01);
  both('resA', 1, C(14, 0), .6, 'power2.out'); both('glowCity', 1, C(14, 1, -.1), .6); both('heatA', .9, C(14, 0), .6);
  both('resA', .35, C(15, 0), .5); both('glowCity', 0, C(15, 0), .5);
  both('growA', 1, C(15, 1, -.1), .5); both('caveP', .9, C(15, 1, -.1), end - C(15, 1), 'power1.inOut');
  /* steam over the springs */
  for (const S of BLOCKS) { on(S.steam.a, C(3, 2), .6, .35); }
  /* XS: wide section */
  bset(XS, { x: .05, y: -.30, z: .1, dist: 4.4, yaw: -10, pitch: 22 });
  bcam(XS, { x: 0, y: -.38, dist: 3.9, yaw: -4, pitch: 21 }, C(1, 0, -.15), C(2, 0) - C(1, 0, -.15));
  bcam(XS, { x: -.15, y: -.35, dist: 4.3, yaw: -14, pitch: 24 }, C(3, 0, -.3), .01);
  bcam(XS, { x: .05, y: -.38, dist: 3.9, yaw: -6, pitch: 22 }, C(3, 0, -.15), C(3, 2) - C(3, 0, -.15));
  bcam(XS, { x: .05, y: -.3, dist: 4.4, yaw: 8, pitch: 24 }, C(8, 0, -.3), .01);
  bcam(XS, { x: .1, y: -.34, dist: 3.8, yaw: -2, pitch: 22 }, C(8, 0, -.15), C(10, 0) - C(8, 0, -.15));
  bcam(XS, { x: .2, y: -.25, dist: 2.6, yaw: -12, pitch: 24 }, C(9, 0, -.3), .01);
  bcam(XS, { x: .24, y: -.2, dist: 2.2, yaw: -4, pitch: 23 }, C(9, 0, -.15), C(10, 0) - C(9, 0, -.15));
  bcam(XS, { x: .15, y: -.35, dist: 3.0, yaw: -16, pitch: 26 }, C(14, 0, -.3), .01);
  bcam(XS, { x: .05, y: -.42, dist: 5.4, yaw: 6, pitch: 32 }, C(14, 0, -.15), C(15, 0) - C(14, 0, -.15), 'power2.out');
  bcam(XS, { x: .2, y: -.3, dist: 3.4, yaw: -12, pitch: 24 }, C(16, 0, 1.1), .01);
  bcam(XS, { x: .25, y: -.25, dist: 2.7, yaw: -4, pitch: 22 }, C(16, 0, 1.25), end - C(16, 0, 1.25) + .3);
  const lRain = bLabel(XS, 'RAIN', { u: .32, y: .40 }, 76, '#7CC4FF'); on(lRain.a, C(3, 0, .3), .3); key(lRain.a, 0, C(3, 2, -.3), .2);
  /* CV: close views */
  bset(CV, { x: -.25, y: -.22, z: .15, dist: 2.5, yaw: -16, pitch: 24 });
  bcam(CV, { x: -.15, y: -.3, dist: 2.2, yaw: -8 }, C(2, 0, -.15), C(3, 0) - C(2, 0, -.15));
  bcam(CV, { x: .32, y: -.30, dist: 2.0, yaw: -20, pitch: 24 }, C(3, 2, -.3), .01);
  bcam(CV, { x: .34, y: -.22, dist: 1.6, yaw: -10, pitch: 22 }, C(3, 2, -.15), C(4, 0) - C(3, 2, -.15));
  bcam(CV, { x: .26, y: -.14, dist: 1.7, yaw: -22, pitch: 28 }, C(7, 0, -.3), .01);
  bcam(CV, { x: .27, y: -.15, dist: 1.35, yaw: -12, pitch: 24 }, C(7, 0, -.15), C(8, 0) - C(7, 0, -.15));
  bcam(CV, { x: .26, y: -.28, dist: 1.8, yaw: 14, pitch: 20 }, C(8, 1, -.3), .01);
  bcam(CV, { x: .27, y: -.24, dist: 1.5, yaw: 4, pitch: 21 }, C(8, 1, -.15), C(9, 0) - C(8, 1, -.15));
  bcam(CV, { x: .36, y: .0, dist: 2.16, yaw: -28, pitch: 38 }, C(10, 0, -.3), .01);
  bcam(CV, { x: .34, y: -.05, dist: 1.69, yaw: -18, pitch: 30 }, C(10, 0, -.15), C(10, 2) - C(10, 0, -.15));
  bcam(CV, { x: .28, y: -.15, dist: 2.03, yaw: -8, pitch: 22 }, C(10, 2), C(11, 2) - C(10, 2));
  bcam(CV, { x: .30, y: -.17, dist: 1.42, yaw: 10, pitch: 20 }, C(12, 0, -.3), .01);
  bcam(CV, { x: .26, y: -.14, dist: 1.55, yaw: -6, pitch: 22 }, C(12, 0, -.15), C(13, 1) - C(12, 0, -.15));
  bcam(CV, { x: .28, y: -.16, dist: 1.5, yaw: -18, pitch: 24 }, C(15, 0, -.3), .01);
  bcam(CV, { x: .28, y: -.17, dist: 1.1, yaw: -6, pitch: 22 }, C(15, 0, -.15), C(16, 0) - C(15, 0, -.15));
  /* thermometer on CV: crust heats ~1 degree per 20 m */
  const th = CV.thermo, tl0 = CV.thermoLbl;
  key(th.a, 1, C(2, 1, -.1), .35, 'back.out(2)'); key(th.lvl, .85, C(2, 1), 1.6, 'power2.in'); key(th.spin, .25, C(2, 1, -.1), 1.8, 'power2.out');
  key(CV.lblA, 1, C(2, 1), .2); key(th.a, 0, C(3, 0, -.3), .25); key(CV.lblA, 0, C(3, 0, -.3), .2);
  { const sp = tl0.querySelector('span'); MO.countUp(sp, 20, C(2, 2, -.05), { dur: .9, noScale: true }); }
  const lFault = bLabel(CV, 'FAULT LINE', { u: .735, y: -.36 }, 66, '#FF9A3A'); on(lFault.a, C(3, 2, .3), .3); key(lFault.a, 0, C(4, 0, -.3), .2);
  key(CV.diver.a, 1, C(11, 0, -.05), .4); key(CV.diver.a, 0, C(11, 2, -.3), .2); key(CV.diver.a, 1, C(12, 0), .3); key(CV.diver.a, 0, C(13, 1, -.3), .2);
  const eDoor = bEmo(CV, '🚪', { lon: 19.0359, lat: 47.5181 }, 120, -70), eDiv = bEmo(CV, '🤿', { u: .70, y: -.04 }, 120), eDiv2 = bEmo(CV, '🤿', { u: .70, y: -.06 }, 120), eShark = bEmo(CV, '🦈', { u: .52, y: -.12 }, 130);
  key(eDoor.a, 1, C(10, 0, .1), .4, 'back.out(2)'); key(eDoor.a, 0, C(10, 2, -.2), .25);
  key(eDiv.a, 1, C(11, 0, .05), .05); key(eDiv.a, 0, C(11, 2, -.3), .2);
  key(eDiv2.a, 1, C(12, 0, .05), .4, 'back.out(2)'); key(eDiv2.a, 0, C(13, 0, -.1), .2);
  key(eShark.a, 1, C(13, 0, .25), .05); key(eShark.a, 0, C(13, 1, -.3), .2);
  /* snail gag + slam */
  const EMO = { diver: eDiv, shark: eShark };
  for (const sl of (D.beats || []).filter(b => b.kind === 'slam')) {
    if (sl.emo === 'snail') { tl.set(eSnail, { opacity: 1 }, sl.t); MO.slam(eSnail, sl.t); fade(eSnail, end - .2, .25); }
    else if (EMO[sl.emo]) MO.slam(EMO[sl.emo].inner, sl.t); }

  /* ===== beats from the spec: circles, arrows, grows, cards ===== */
  const beat = k => (D.beats || []).filter(b => b.kind === k);
  const projQ = (S, q, t) => (S === MP || S === MQ) ? mapProj(S, t, q.lon, q.lat, .01) : bProj(S, q, t);
  for (const b of beat('circle')) { const S = SC[b.scene];
    MO.hwCircle(S.ov, t => projQ(S, b.q, t), (b.r || [200, 110])[0], (b.r || [200, 110])[1], b.t, b.u || nextChunk(b.t), { seed: 3 + b.t, col: b.col }); }
  for (const b of beat('arrow')) { const S = SC[b.scene];
    MO.hwArrow(S.ov, t => { const p0 = projQ(S, b.qf, t), p1 = projQ(S, b.qt, t); return { x0: p0.x, y0: p0.y, x1: p1.x, y1: p1.y }; }, b.t, b.u || nextChunk(b.t), { seed: 7 + b.t, col: b.col }); }
  const wordTime = (b, needle) => { const ch = D.chunks.find(c => Math.abs(c.sn - b.t) < .02); const wi = ch ? ch.txt.replace(/\|/g, ' ').split(' ').findIndex(w => w.includes(needle)) : -1; return wi >= 0 ? ch.wt[wi] : null; };
  for (const b of beat('grow')) { const el = mk('div', { class: 'kbox', style: `top:${b.y || 150}px` }, $('hook'));
    el.innerHTML = `<span class="knum">0</span><span class="ksuf">${b.unit || ''}</span>`; if (b.fs) el.style.fontSize = b.fs + 'px';
    const wt = wordTime(b, String(b.to).slice(0, 2)); const dur = wt ? Math.max(.6, wt - b.t + .15) : 1.2; tl.set(el, { opacity: 1 }, b.t);
    MO.countGrow(el.querySelector('.knum'), b.to, b.t, { dur, from: b.from || 0, prefix: b.prefix, startScale: .35, suffixEl: el.querySelector('.ksuf') }); MO.textOut(el, b.u || nextChunk(b.t)); }
  for (const b of beat('card')) { const Cd = mkCard(SC[b.scene] || MP, b); key(Cd.a, 1, b.t, .35, 'power3.out'); key(Cd.a, 0, b.u || nextChunk(b.t), .25); key(MP.labels[0].a, 0, b.t - .1, .2);
    if (b.to) MO.countGrow(Cd.num, b.to, b.t + .1, { dur: 1.1, startScale: .5, suffixEl: Cd.suf }); else Cd.num.textContent = ''; }
  MO.shake(0, C(1, 0, -.15), 'handheld-normal-mild', .1, { decay: false });
  shake(C(14, 0, .05), .6);
  /* titles: hook charslam + above/below */
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
  for (const S of [MP, MQ]) allT.push(S.gk, S.tk, S.x, S.hl, S.rise, S.pinA, S.flagA, ...S.cards.map(c => c.a), ...S.labels.map(l => l.a), ...S.lls.map(l => l.a));
  allT.push(CV.thermo.a, CV.thermo.lvl, CV.thermo.spin, CV.lblA);
  for (const T of allT) T.keys.sort((a, b) => a.a - b.a);
  /* dots registered via mapDot live in closures: sort their tracks too */
  for (const S of [MP, MQ]) for (const d of (S.dots || [])) d.a.keys.sort((a, b) => a.a - b.a);
  const clk = { t: 0 };
  tl.fromTo(clk, { t: 0 }, { t: D.dur, duration: D.dur, ease: 'none', ...IR, onUpdate: () => { const t = clk.t;
    const live = S => S.wins.some(w => t >= w[0] - .05 && t <= w[1] + .45);
    for (const S of BLOCKS) if (live(S)) renderBlock(S, t);
    for (const S of [MP, MQ]) if (live(S)) renderMap(S, t); } }, 0);
  return tl;
}
window.__timelines = window.__timelines || {};
document.fonts.ready.then(() => Promise.all(READY)).then(() => { window.__timelines['main'] = build(); });
</script>
</body>
</html>
