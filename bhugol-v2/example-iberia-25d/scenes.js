  // ===== L0 hook: Spain + Portugal = ? ... AGAIN? =====
  const h1 = mk('div', { class: 'ttl' }, $('titles')); h1.style.top = '175px'; h1.innerHTML = '<div style="font-size:160px;-webkit-text-stroke-width:22px">🇪🇸 + 🇵🇹 = <span class="k">?</span></div>';
  tl.fromTo(h1, { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: .3, ease: 'expo.out', ...IR }, .32); ev(.32, 'slam'); out(h1, C(0, 2, .25));
  PUN(C(0, 0, .3), 1.08, C(0, 1)); PUN(C(0, 1, .05), 1.12, C(0, 2));
  tl.fromTo(FL.ESP, { opacity: .82 }, { keyframes: [{ opacity: 1, duration: .15 }, { opacity: .82, duration: .35 }] }, C(0, 0, .2));
  tl.fromTo(FL.PRT, { opacity: .82 }, { keyframes: [{ opacity: 1, duration: .15 }, { opacity: .82, duration: .35 }] }, C(0, 1));
  const ag = mk('div', { class: 'stamp' }, hud); ag.textContent = 'AGAIN?! 🔁'; place(ag, 250, 330);
  tl.fromTo(ag, { opacity: 0, scale: 2.2, rotation: -14 }, { opacity: 1, scale: 1, rotation: -7, duration: .26, ease: 'power4.in', ...IR }, C(0, 2, .45)); ev(C(0, 2, .69), 'stamp');
  PUN(C(0, 2, .7), 1.2, C(1, 0, .1)); out(ag, C(1, 1, -.05));

  // ===== L1 they've already done it once =====
  const doc = mk('div', { class: 'card' }, hud); doc.innerHTML = '<div class="big" style="font-size:110px">📜</div><div class="lbl">IT ALREADY HAPPENED</div><div class="chip">1580 – 1640</div>';
  place(doc, 300, 290); doc.style.textAlign = 'center'; pop(doc, C(1, 1, -.05)); ev(C(1, 1, -.05), 'card');
  const tr = mk('div', { class: 'stamp' }, hud); tr.textContent = 'TRUE STORY ✅'; place(tr, 150, 700);
  tl.fromTo(tr, { opacity: 0, scale: 2.2, rotation: -14 }, { opacity: 1, scale: 1, rotation: -8, duration: .26, ease: 'power4.in', ...IR }, C(1, 2)); ev(C(1, 2, .24), 'stamp');
  out(doc, C(2, 0, -.05)); out(tr, C(2, 0, -.05));

  // ===== L2 1580: Portugal's royal family ran out of heirs (flashback) =====
  const tT = C(2, 0, -.05);
  tl.to($('flash'), { keyframes: [{ opacity: .9, duration: .07 }, { opacity: 0, duration: .5 }] }, tT); ev(tT, 'flash');
  tl.to($('sepia'), { opacity: .2, duration: .5 }, tT + .05); tl.to($('warm'), { opacity: .22, duration: .5 }, tT + .05);
  const yr = mk('div', { class: 'ttl' }, $('titles')); yr.style.top = '230px'; yr.innerHTML = '<div style="font-size:190px;-webkit-text-stroke-width:26px">⏪ <span class="k n">2026</span></div>';
  MO.textIn(yr, tT); { const n = yr.querySelector('.n'); const st = { v: 2026 }; tl.fromTo(st, { v: 2026 }, { v: 1580, duration: .9, ease: 'power3.out', ...IR, onUpdate: () => { n.textContent = Math.round(st.v); } }, C(2, 0)); }
  ev(C(2, 0), 'count'); out(yr, C(2, 1, .2));
  const crP = emo('👑', 170); ride(crP, 'lisbon', -85, -260); pop(crP, C(2, 1)); ev(C(2, 1), 'pop');
  const nh = mk('div', { class: 'card' }, hud); nh.innerHTML = '<div class="lbl">PORTUGAL\'S NEXT KING</div><div class="big" style="font-size:100px">NO HEIR <span style="font-family:Emo">❌</span></div>';
  place(nh, 200, 300); pop(nh, C(2, 2, -.05)); ev(C(2, 2, -.05), 'card');
  tl.to(crP, { keyframes: [{ rotation: -12, duration: .12 }, { rotation: 10, duration: .12 }, { rotation: 0, duration: .12 }] }, C(2, 2, .2)); out(nh, C(3, 0, -.05));

  // ===== L3 Spain's king took the crown... for sixty years =====
  const mp = pin('madrid', 'MADRID', '🇪🇸'); ride(mp, 'madrid'); tl.fromTo(mp, { opacity: 0, y: -50 }, { opacity: 1, y: 0, duration: .35, ease: 'back.out(2)', ...IR }, C(3, 0)); ev(C(3, 0), 'pop');
  { const A = ANCH.find(a => a.el === crP); const t0 = C(3, 1, -.05), t1 = t0 + .8; A.key = null;
    A.fn = t => { const u = EASE.soft(Math.min(1, Math.max(0, (t - t0) / (t1 - t0)))); const a = P.lisbon, b = P.madrid; return [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u - Math.sin(Math.PI * u) * 260]; }; }
  ev(C(3, 1, -.05), 'whoosh'); ev(C(3, 1, .75), 'thud');
  const tG0 = C(3, 2, -.1);
  for (const k in FL) tl.to(FL[k], { opacity: 0, duration: .45 }, tG0);
  fadeA(goldG, 1, tG0, .5); fadeA(rim, 1, tG0, .4);
  const s60 = mk('div', { class: 'stamp' }, hud); s60.textContent = '60 YEARS'; place(s60, 270, 300);
  tl.fromTo(s60, { opacity: 0, scale: 2.2, rotation: 10 }, { opacity: 1, scale: 1, rotation: 6, duration: .26, ease: 'power4.in', ...IR }, C(3, 2)); ev(C(3, 2, .24), 'stamp');
  out(s60, C(4, 0, -.05)); out(crP, C(4, 0, -.05)); out(mp, C(4, 0, -.05));

  // ===== L4 OL1: so what would this country get TODAY? =====
  const tN = C(4, 0, -.1);
  tl.to($('sepia'), { opacity: 0, duration: .4 }, tN); tl.to($('warm'), { opacity: 0, duration: .4 }, tN);
  tl.to($('flash'), { keyframes: [{ opacity: .35, duration: .06 }, { opacity: 0, duration: .45 }] }, tN); ev(tN, 'boom');
  for (const k in OUT) tl.to(OUT[k], { attr: { opacity: 0 }, duration: .4, ...IR }, tN);
  fadeA(rimW, .35, tN, .4); fadeA(lights, .9, tN + .3, .6);
  tl.set(shineR, { attr: { opacity: 1 } }, tN + .1);
  MO.driver(tN + .1, tN + 1.3, t => { const u = Math.min(1, Math.max(0, (t - tN - .1) / 1.1)); const x = P.atl[0] - 600 + u * 3200; shine.setAttribute('x1', x - 500); shine.setAttribute('x2', x + 500); shineR.setAttribute('opacity', u < 1 ? 1 : 0); });
  const nm = mk('div', { class: 'ttl' }, $('titles')); nm.style.top = '230px'; nm.innerHTML = '<div style="font-size:120px;-webkit-text-stroke-width:19px">🇪🇸🤝🇵🇹</div><div style="font-size:110px;-webkit-text-stroke-width:18px"><span class="k">TODAY?</span></div>';
  MO.textIn(nm, C(4, 0)); PUN(C(4, 1, .1), 1.12, C(5, 0)); out(nm, C(5, 0, -.05));

  // ===== L5 61 million people, more than Italy =====
  const cP = mk('div', { class: 'card' }, hud); cP.innerHTML = '<div class="lbl">PEOPLE</div><div class="big"><span class="n">0</span><span class="u">MILLION 👥</span></div><div class="chip">MORE THAN 🇮🇹 ITALY ✅</div>';
  place(cP, 190, 280); pop(cP, C(5, 0, -.05)); MO.countUp(cP.querySelector('.n'), 61, C(5, 0), { dur: 1.0, noScale: true }); ev(C(5, 0), 'count');
  const chP = cP.querySelector('.chip'); tl.set(chP, { opacity: 0 }, 0); tl.fromTo(chP, { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .35, ease: 'back.out(2)', ...IR }, C(5, 1, .1)); ev(C(5, 1, .1), 'pop');
  out(cP, C(6, 0, -.05));

  // ===== L6 two languages, 800 million speakers =====
  const cL = mk('div', { class: 'card' }, hud); cL.innerHTML = '<div class="lbl">ESPAÑOL + PORTUGUÊS</div><div class="big"><span class="n">0</span><span class="u">MILLION 🗣️</span></div>';
  place(cL, 170, 280); pop(cL, C(6, 0, -.05)); ev(C(6, 0, -.05), 'card');
  MO.countUp(cL.querySelector('.n'), 800, C(6, 1, -.05), { suffix: '+', dur: 1.4, noScale: true }); ev(C(6, 1, -.05), 'count');
  const BUB = []; for (let i = 0; i < 12; i++) { const c = mk('div', { class: 'coin' }, fx); c.textContent = i % 2 ? '💬' : '🗨️'; c.style.fontSize = (80 + (i * 23) % 50) + 'px'; BUB.push(c); }
  BUB.forEach((c, i) => { const x = 80 + (i * 233) % 880, y1 = 1080 - (i * 61) % 380; tl.fromTo(c, { opacity: 0, x, y: y1 + 260, scale: .4 }, { opacity: 1, y: y1, scale: 1, duration: .5, ease: 'back.out(1.8)', ...IR }, C(6, 1, i * .05));
    out(c, C(7, 0, -.1 + i * .02), .15); });
  ev(C(6, 1, .1), 'pop'); out(cL, C(7, 0, -.05));

  // ===== L7 a Nobel-winning writer picked its name: IBERIA =====
  const cN = mk('div', { class: 'card' }, hud); cN.innerHTML = '<div class="big" style="font-size:100px">🏅 NOBEL</div><div class="lbl">PORTUGUESE WRITER · 2007 IDEA</div>';
  place(cN, 230, 290); cN.style.textAlign = 'center'; pop(cN, C(7, 0, -.05)); ev(C(7, 0, -.05), 'card'); out(cN, C(7, 2, -.1));
  const ib = mk('div', { class: 'ttl' }, $('titles')); ib.style.top = '300px'; ib.innerHTML = '<div style="font-size:200px;-webkit-text-stroke-width:28px"><span class="k">IBERIA</span></div>';
  MO.slam(ib, C(7, 2), { shake: false }); ev(C(7, 2), 'slam'); PUN(C(7, 2, .05), 1.14, C(8, 0, -.1)); out(ib, C(8, 0, -.05));

  // ===== L8 so why did Portugal walk away? =====
  const tB = C(8, 0, -.1);
  for (const k in FL) tl.to(FL[k], { opacity: .82, duration: .4 }, tB);
  for (const k in OUT) tl.to(OUT[k], { attr: { opacity: .95 }, duration: .4, ...IR }, tB);
  fadeA(goldG, 0, tB, .4); fadeA(rim, 0, tB, .3); fadeA(rimW, 0, tB, .3); fadeA(lights, 0, tB, .3);
  const q = mk('div', { class: 'ttl' }, $('titles')); q.style.top = '250px'; q.innerHTML = '<div style="font-size:130px;-webkit-text-stroke-width:21px">WHY <span class="k">LEAVE?!</span> 🤨</div>';
  MO.slam(q, C(8, 1, -.05), { shake: false }); ev(C(8, 1, -.05), 'slam'); out(q, C(9, 0, -.05));
  const walk = emo('🚶', 170); ride(walk, 'atl', -85, -120); tl.fromTo(walk, { opacity: 0, x: 120 }, { opacity: 1, x: -60, duration: .7, ease: 'power2.out', ...IR }, C(8, 1)); out(walk, C(9, 0, -.05));

  // ===== L9 Spain kept dragging Portugal into its wars =====
  const tW = C(9, 0, -.05);
  tl.to($('sepia'), { opacity: .2, duration: .4 }, tW); tl.to($('warm'), { opacity: .22, duration: .4 }, tW); ev(tW, 'whoosh');
  const SW = []; [[-260, -340], [120, -420], [-40, -160]].forEach(([dx, dy], i) => { const s = emo('⚔️', 150); ride(s, 'es_c', dx - 75, dy); SW.push(s);
    tl.fromTo(s, { opacity: 0, scale: 2, rotation: -20 }, { opacity: 1, scale: 1, rotation: 0, duration: .28, ease: 'power4.in', ...IR }, C(9, 2, -.1 + i * .16)); ev(C(9, 2, .15 + i * .16), 'thud'); });
  const rope = emo('🪢', 130); ride(rope, 'border', -65, -170); pop(rope, C(9, 0, .1)); ev(C(9, 0, .1), 'pop');
  tl.to(rope, { keyframes: [{ x: 30, duration: .15 }, { x: -10, duration: .15 }, { x: 30, duration: .15 }, { x: 0, duration: .15 }] }, C(9, 1));
  SW.forEach(s => out(s, C(10, 0, -.05))); out(rope, C(10, 0, -.05));

  // ===== L10 December 1st 1640: Portugal took its crown back =====
  const d1 = mk('div', { class: 'stamp' }, hud); d1.textContent = '1 DEC 1640'; place(d1, 200, 300);
  tl.fromTo(d1, { opacity: 0, scale: 2.2, rotation: -12 }, { opacity: 1, scale: 1, rotation: -6, duration: .26, ease: 'power4.in', ...IR }, C(10, 0, .1)); ev(C(10, 0, .34), 'stamp');
  const crB = emo('👑', 170); ride(crB, 'lisbon', -85, -260);
  tl.fromTo(crB, { opacity: 0, y: -300, rotation: -30 }, { opacity: 1, y: 0, rotation: 0, duration: .5, ease: 'bounce.out', ...IR }, C(10, 2)); ev(C(10, 2, .35), 'thud');
  tl.to(FL.PRT, { keyframes: [{ opacity: 1, duration: .2 }] }, C(10, 2)); tl.to(FL.ESP, { opacity: .5, duration: .3 }, C(10, 2));
  tl.to($('flash'), { keyframes: [{ opacity: .3, duration: .06 }, { opacity: 0, duration: .4 }] }, C(10, 2, .05)); ev(C(10, 2, .05), 'boom');
  out(d1, C(11, 0, -.05));

  // ===== L11 ...and it still gets a day off =====
  tl.to($('sepia'), { opacity: 0, duration: .4 }, C(11, 0, -.1)); tl.to($('warm'), { opacity: 0, duration: .4 }, C(11, 0, -.1));
  const cal = mk('div', { class: 'card' }, hud); cal.innerHTML = '<div class="lbl">EVERY YEAR 🇵🇹</div><div class="big" style="font-size:110px">📅 1 DEC</div><div class="chip">DAY OFF 🎉</div>';
  place(cal, 260, 290); pop(cal, C(11, 0)); ev(C(11, 0), 'card');
  const chC = cal.querySelector('.chip'); tl.set(chC, { opacity: 0 }, 0); tl.fromTo(chC, { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .35, ease: 'back.out(2)', ...IR }, C(11, 1, .15)); ev(C(11, 1, .15), 'pop');
  const beach = emo('🏖️', 140); place(beach, 820, 640); pop(beach, C(11, 1, .3)); ev(C(11, 1, .3), 'pop');
  out(cal, C(12, 0, -.05)); out(beach, C(12, 0, -.05)); out(crB, C(12, 0, -.05)); tl.to(FL.ESP, { opacity: .82, duration: .3 }, C(12, 0, -.1));

  // ===== L12 OL2 =====
  PUN(C(12, 1, .05), 1.16, C(13, 0, -.05));
  const pc = emo('🍿', 150); place(pc, 860, 380); pop(pc, C(12, 1)); ev(C(12, 1), 'pop'); out(pc, C(13, 0));

  // ===== L13 cross the border... and travel back in time =====
  for (const k in FL) tl.to(FL[k], { opacity: .3, duration: .4 }, C(13, 0, -.15));
  tl.to(STB, { attr: { opacity: .95 }, duration: .4, ...IR }, C(13, 0, -.1)); tl.to(BGLOW, { attr: { opacity: .55 }, duration: .4, ...IR }, C(13, 0, -.1));
  const car = emo('🚗', 120); ride(car, null, -60, -90); const cA = ANCH[ANCH.length - 1];
  { const t0 = C(13, 0, .2), t1 = C(13, 2, .3); const a = [P.border[0] + 380, P.border[1] + 10], b = [P.border[0] - 380, P.border[1] - 10];
    cA.fn = t => { const u = Math.min(1, Math.max(0, (t - t0) / (t1 - t0))); return [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u]; }; }
  tl.fromTo(car, { opacity: 0, scaleX: -1 }, { opacity: 1, scaleX: -1, duration: .25, ...IR }, C(13, 0, .2)); ev(C(13, 0, .2), 'whoosh');
  const tt = mk('div', { class: 'ttl' }, $('titles')); tt.style.top = '250px'; tt.innerHTML = '<div style="font-size:130px;-webkit-text-stroke-width:21px">⏪ <span class="k">TIME TRAVEL</span></div>';
  MO.slam(tt, C(13, 2), { shake: false }); ev(C(13, 2), 'slam'); out(tt, C(14, 0, -.05));
  tl.to($('flash'), { keyframes: [{ opacity: .4, duration: .06 }, { opacity: 0, duration: .4 }] }, C(13, 2, .05));
  out(car, C(14, 0, .1));

  // ===== L14 Spain's clocks run an hour ahead. Since 1940 =====
  const ckE = lab('🇪🇸 13:00'), ckP = lab('🇵🇹 12:00'); [ckE, ckP].forEach(e => { e.style.fontSize = '78px'; e.style.transform = 'translate(-50%,-50%)'; });
  ride(ckE, null, 230, -60); ANCH[ANCH.length - 1].xy = P.border; ride(ckP, null, -230, -60); ANCH[ANCH.length - 1].xy = P.border;
  pop(ckP, C(14, 0, -.05)); ev(C(14, 0, -.05), 'pop');
  tl.fromTo(ckE, { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .4, ease: 'back.out(2)', ...IR }, C(14, 1)); ev(C(14, 1), 'pop');
  const ar = emo('⏩', 110); ride(ar, 'border', -55, -190); pop(ar, C(14, 1, .2)); ev(C(14, 1, .2), 'pop');
  const s40 = mk('div', { class: 'stamp' }, hud); s40.textContent = 'SINCE 1940'; place(s40, 230, 300);
  tl.fromTo(s40, { opacity: 0, scale: 2.2, rotation: -12 }, { opacity: 1, scale: 1, rotation: -6, duration: .26, ease: 'power4.in', ...IR }, C(14, 2)); ev(C(14, 2, .24), 'stamp');
  [ckE, ckP, ar, s40].forEach(e => out(e, C(15, 0, -.05)));
  tl.to(STB, { attr: { opacity: 0 }, duration: .3, ...IR }, C(15, 0, -.05)); tl.to(BGLOW, { attr: { opacity: 0 }, duration: .3, ...IR }, C(15, 0, -.05));

  // ===== L15 capital fight =====
  for (const k in FL) tl.to(FL[k], { opacity: .82, duration: .4 }, C(15, 0, -.1));
  const cq = mk('div', { class: 'ttl' }, $('titles')); cq.style.top = '250px'; cq.innerHTML = '<div style="font-size:130px;-webkit-text-stroke-width:21px">🏛️ <span class="k">CAPITAL?</span></div>';
  MO.textIn(cq, C(15, 0)); ev(C(15, 0), 'pop'); out(cq, C(15, 1, -.05));
  PUN(C(15, 0, .1), 1.08, C(15, 1, -.1));
  const md = pin('madrid', 'MADRID', '🇪🇸'); ride(md, 'madrid'); tl.fromTo(md, { opacity: 0, y: -50 }, { opacity: 1, y: 0, duration: .35, ease: 'back.out(2)', ...IR }, C(15, 1)); ev(C(15, 1), 'pop');
  const lb = pin('lisbon', 'LISBON', '🇵🇹'); ride(lb, 'lisbon'); tl.fromTo(lb, { opacity: 0, y: -50 }, { opacity: 1, y: 0, duration: .35, ease: 'back.out(2)', ...IR }, C(15, 2)); ev(C(15, 2), 'pop');
  const vs = emo('⚔️', 140); ride(vs, null, -70, -70); ANCH[ANCH.length - 1].xy = mid('madrid', 'lisbon'); pop(vs, C(15, 2, .3)); ev(C(15, 2, .3), 'thud');
  out(md, C(16, 0, -.1)); out(lb, C(17, 0, -.1)); out(vs, C(16, 0, -.1));

  // ===== L16 Portugal's one demand: NATA > CHURROS =====
  const ball = mk('div', { class: 'ball' }, hud);
  ball.innerHTML = `<svg width="300" height="300" viewBox="0 0 300 300"><defs><clipPath id="bc"><circle cx="150" cy="160" r="120"/></clipPath></defs>
   <g clip-path="url(#bc)"><svg x="0" y="40" width="300" height="240" viewBox="0 0 480 240" preserveAspectRatio="xMidYMid slice">${flagSVG('PRT', 480, 240, true)}</svg></g>
   <circle cx="150" cy="160" r="120" fill="none" stroke="#03101A" stroke-width="9"/>
   <ellipse cx="112" cy="150" rx="30" ry="26" fill="#fff" stroke="#03101A" stroke-width="6"/><ellipse cx="190" cy="150" rx="30" ry="26" fill="#fff" stroke="#03101A" stroke-width="6"/>
   <circle cx="120" cy="156" r="10" fill="#03101A"/><circle cx="198" cy="156" r="10" fill="#03101A"/>
   <path d="M84 116 L140 130" stroke="#03101A" stroke-width="11" stroke-linecap="round"/><path d="M220 116 L164 130" stroke="#03101A" stroke-width="11" stroke-linecap="round"/></svg>`;
  Object.assign(ball.style, { left: '70px', top: '990px' }); tl.fromTo(ball, { opacity: 0, y: 400, scaleY: .7 }, { opacity: 1, y: 0, scaleY: 1, duration: .45, ease: 'back.out(1.8)', ...IR }, C(16, 0, -.15)); ev(C(16, 0, -.15), 'pop');
  tl.to(ball, { keyframes: [{ scaleY: .9, duration: .1 }, { scaleY: 1.05, duration: .12 }, { scaleY: 1, duration: .1 }] }, C(16, 1));
  const bub = mk('div', { class: 'bubble' }, hud); bub.textContent = D.bubble; Object.assign(bub.style, { left: '250px', top: '850px' }); pop(bub, C(16, 1)); ev(C(16, 1), 'pop');
  const tart = emo('🥧', 150); place(tart, 780, 700); pop(tart, C(16, 1, .25)); ev(C(16, 1, .25), 'pop');
  out(ball, C(17, 0, .05)); out(bub, C(17, 0, .05)); out(tart, C(17, 0, .05));

  // ===== L17 vote, back to the opening frame =====
  const v1 = mk('div', { class: 'vote' }, hud); v1.style.left = '90px'; v1.style.background = 'linear-gradient(#FFE27A,#F6B630)'; v1.innerHTML = '<div class="vt">ONE COUNTRY</div><div class="vf">🟡</div>';
  const v2 = mk('div', { class: 'vote' }, hud); v2.style.left = '560px'; v2.style.background = '#fff'; v2.innerHTML = '<div class="vt">STAY TWO</div><div class="vf">🇪🇸🇵🇹</div>';
  v1.querySelector('.vt').style.fontSize = '58px';
  if (D.lang === 'hi') { v1.querySelector('.vt').textContent = 'एक देश'; v2.querySelector('.vt').textContent = 'दो देश'; [v1, v2].forEach(v => v.querySelector('.vt').style.fontFamily = 'Muk, BSD, sans-serif'); }
  pop(v1, C(17, 0, .05)); pop(v2, C(17, 1, -.05)); ev(C(17, 0, .05), 'pop'); ev(C(17, 1, -.05), 'pop');
  tl.to(v1, { keyframes: [{ scale: 1.08, duration: .15 }, { scale: 1, duration: .2 }] }, C(17, 1, .3)); tl.to(v2, { keyframes: [{ scale: 1.08, duration: .15 }, { scale: 1, duration: .2 }] }, C(17, 2, -.05));
  out(v1, D.dur - .55); out(v2, D.dur - .55);
