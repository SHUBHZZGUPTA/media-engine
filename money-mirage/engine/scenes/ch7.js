// CHAPTER 7: So what is your money, really? (lines 41-46) + end card
function c7_cubeLayer(parent, x0, base, S, i, h) { // one slab of the gold cube (front + side), bottom-up
  const g = sv('g', {}, parent); const y1 = base - (i + 1) * h, y0 = base - i * h, dx = S * .42, dy = -S * .28;
  sv('rect', { x: x0, y: y1, width: S, height: h, fill: i % 2 ? '#E2AA40' : '#E9B44C', stroke: '#7A4E0E', 'stroke-width': 4 }, g);
  sv('path', { d: `M${x0 + S},${y1} L${x0 + S + dx},${y1 + dy} L${x0 + S + dx},${y0 + dy} L${x0 + S},${y0} Z`, fill: i % 2 ? '#B8862B' : '#C4912F', stroke: '#7A4E0E', 'stroke-width': 4, 'stroke-linejoin': 'round' }, g);
  return g; }

// wordmark with measured spacing between MONEY and MIRAGE, centred at x=960
function c7_wordmark(parent, y, s) { const g0 = sv('g', {}, parent); const g = sv('g', {}, g0);
  const t1 = svgT(g, 'MONEY', 0, 0, 52, { c: '#E9B44C', anchor: 'start' }); const w1 = t1.getComputedTextLength() + 14;
  const t2 = svgT(g, 'MIRAGE', w1, 0, 52, { c: '#F3EBDD', anchor: 'start' }); const wt = w1 + t2.getComputedTextLength();
  const refl = sv('g', { transform: 'translate(0,14) scale(1,-1)', opacity: .28 }, g); svgT(refl, 'MONEY', 0, 0, 52, { c: '#E9B44C', anchor: 'start' }); svgT(refl, 'MIRAGE', w1, 0, 52, { c: '#F3EBDD', anchor: 'start' });
  const waves = sv('g', {}, g); const segs = Math.ceil((wt + 80) / 28); for (let k = 0; k < 4; k++) sv('path', { d: `M-6,${20 + k * 9}` + ' t28,0'.repeat(0) + Array.from({ length: segs }, (_, i) => i ? ' t28,0' : ' q14,-4 28,0').join(''), fill: 'none', stroke: '#101A2E', 'stroke-width': 3.2 }, waves);
  g0.setAttribute('transform', `translate(${(960 - wt * s / 2).toFixed(1)},${y}) scale(${s})`); return { g, refl, waves }; }

function ch7() {
  const t0 = CH(7).a - .3, tTie = A("Tie the world's money"), tCri = A('In a crisis'), tBack = A('So, back to the question'), tToday = A('Today, the Bank'),
    tTrust = A('What really stands behind'), tGold = A('Gold was a promise'), tEndC = LA(46) - 1.0;
  startCh(7);

  // 1. all the gold ever mined = one cube, 22.6 m a side
  { const S = shot(t0, tTie, { tr: 'fade' }); const g = G(S, { opacity: 1 });
    const h1 = T(S, 'Why not go back to *gold?*', 960, 150, 84); kin(h1, A('why not just go back', -.2), { times: wordTimes('why not just go back to gold').filter((_, i) => i !== 2) });
    tl.to(h1, { autoAlpha: 0, y: -30, duration: .3 }, A('All the gold ever mined', -.3));
    const h2 = T(S, "Here's the _problem._", 960, 150, 84); kin(h2, A("Here's the problem"), { times: wordTimes("Here's the problem") }); out(h2, A('All the gold ever mined', -.25), .25);
    const X0 = 520, BASE = 860, SZ = 400, N = 8, H = SZ / N;
    const shadow = sv('ellipse', { cx: X0 + SZ * .7, cy: BASE + 18, rx: SZ * .85, ry: 34, fill: 'rgba(0,0,0,.35)', opacity: 0 }, g); fin(shadow, A('All the gold ever mined'));
    const tMined = A('All the gold ever mined'), tCube = A('single cube');
    for (let i = 0; i < N; i++) { const L = c7_cubeLayer(g, X0, BASE, SZ, i, H); const at = tMined + i * (tCube - tMined) / N;
      gsap.set(L, { autoAlpha: 0 }); tl.fromTo(L, { autoAlpha: 0, y: -260 }, { autoAlpha: 1, y: 0, duration: .32, ease: 'bounce.out', ...IR }, at); sfx('thud', at + .2, .35); ev(at, 'layer'); }
    const dx = SZ * .42, dy = -SZ * .28; const top = sv('path', { d: `M${X0},${BASE - SZ} L${X0 + dx},${BASE - SZ + dy} L${X0 + SZ + dx},${BASE - SZ + dy} L${X0 + SZ},${BASE - SZ} Z`, fill: '#F7D88A', stroke: '#7A4E0E', 'stroke-width': 4, 'stroke-linejoin': 'round' }, g);
    pop(top, tCube, { s0: .8, sfx: 'clink' }); const shine = sv('path', { d: `M${X0 + 40},${BASE - SZ + 30} L${X0 + 110},${BASE - SZ + 30} L${X0 + 60},${BASE - 30} L${X0 - 10},${BASE - 30} Z`, fill: '#FFF3C9', opacity: 0 }, g);
    tl.fromTo(shine, { opacity: 0 }, { opacity: .3, duration: .4, ...IR }, tCube + .2);
    const ml = sv('path', { d: `M${X0 - 60},${BASE} L${X0 - 60},${BASE - SZ} M${X0 - 82},${BASE} L${X0 - 38},${BASE} M${X0 - 82},${BASE - SZ} L${X0 - 38},${BASE - SZ}`, fill: 'none', stroke: '#F3EBDD', 'stroke-width': 6, 'stroke-linecap': 'round', opacity: 0 }, g);
    const tM = A('22.6 metres'); draw(ml, tM - .3, .7, { len: 600 });
    const mlab = T(S, '*22.6 m*', X0 - 95, BASE - SZ / 2, 60, { align: 'right' }); pop(mlab, tM + .1, { sfx: 'stamp' });
    const cnt = I(S, '0', 1460, 470, 120, { weight: 900, color: '#E9B44C' }); fin(cnt, A('222,600', -.2), .2); count(cnt, 0, 222600, A('222,600'), 1.8, { f: 'int' });
    const tl1 = I(S, 'tonnes of gold', 1460, 570, 44, { color: '#8D98B0' }); fin(tl1, A('222,600', .2));
    const tl2 = T(S, 'All the gold *ever mined*', 1460, 360, 52); kin(tl2, A('All the gold ever mined'), { times: wordTimes('All the gold ever mined') });
    const tl3 = I(S, 'fits in one cube', 1460, 660, 44, { color: '#F3EBDD' }); fin(tl3, A('fit in a single cube')); }

  // 2. money capped by the mining line
  { const S = shot(tTie, tCri, { tr: 'slide' }); const g = G(S, { opacity: 1 }); const OX = 360, OY = 790, W = 1200;
    const ax = sv('path', { d: `M${OX},${OY - 470} L${OX},${OY} L${OX + W},${OY}`, fill: 'none', stroke: '#3B4A6A', 'stroke-width': 6, 'stroke-linecap': 'round', opacity: 0 }, g); draw(ax, tTie, .5, { len: 1700 });
    const gl = sv('path', { d: `M${OX},${OY - 40} C${OX + 400},${OY - 90} ${OX + 800},${OY - 170} ${OX + W},${OY - 280}`, fill: 'none', stroke: '#E9B44C', 'stroke-width': 14, 'stroke-linecap': 'round', opacity: 0 }, g);
    draw(gl, A('that cube'), 1.4); const glab = T(S, '*Gold mined*', OX + W - 10, OY - 175, 40, { align: 'right' }); pop(glab, A('that cube', .9), { sfx: false });
    const mlLine = sv('path', { d: `M${OX},${OY - 54} C${OX + 400},${OY - 106} ${OX + 800},${OY - 188} ${OX + W},${OY - 298}`, fill: 'none', stroke: '#F3EBDD', 'stroke-width': 8, 'stroke-linecap': 'round', 'stroke-dasharray': '1 0', opacity: 0 }, g);
    const tGrow = A('and money can only grow'); draw(mlLine, tGrow, 1.8, { ease: 'none' });
    const mlab = T(S, 'Money', OX + W - 10, OY - 360, 40, { align: 'right' }); pop(mlab, tGrow + 1.6, { sfx: false });
    const pick = E(S, '⛏️', OX + W + 80, OY - 300, 110); pop(pick, A('miners can dig'), { sfx: 'thud' }); wiggle(pick, A('miners can dig', .45), 18, 3);
    const h = T(S, 'Money can only grow as fast as *miners can dig*', 960, 170, 58); kin(h, tGrow, { times: wordTimes('money can only grow as fast as miners can dig') }); }

  // 3. central banks' hands are tied
  { const S = shot(tCri, tBack, { tr: 'zoom' }); const g = G(S, { opacity: 1 }); const bk = sv('g', {}, g);
    sv('path', { d: 'M640,380 L960,250 L1280,380 Z', fill: '#C9CFDA', stroke: '#6C7690', 'stroke-width': 6, 'stroke-linejoin': 'round' }, bk);
    sv('rect', { x: 660, y: 380, width: 600, height: 34, fill: '#DDE2EA', stroke: '#6C7690', 'stroke-width': 6 }, bk);
    for (let k = 0; k < 5; k++) sv('rect', { x: 700 + k * 120, y: 414, width: 52, height: 286, fill: '#DDE2EA', stroke: '#6C7690', 'stroke-width': 5 }, bk);
    sv('rect', { x: 630, y: 700, width: 660, height: 44, rx: 4, fill: '#C9CFDA', stroke: '#6C7690', 'stroke-width': 6 }, bk);
    svgT(bk, 'CENTRAL BANK', 960, 404, 26, { c: '#4B5570', font: 'Inter', w: 900, ls: '.2em' });
    slideIn(bk, tCri, 0, 260, { sfx: 'whoosh' });
    const tTied = A('hands are tied'); const cuffs = sv('g', {}, g);
    for (const cx of [800, 1120]) { sv('circle', { cx, cy: 600, r: 74, fill: 'none', stroke: '#0A1120', 'stroke-width': 34 }, cuffs); sv('circle', { cx, cy: 600, r: 74, fill: 'none', stroke: '#C9CFDA', 'stroke-width': 22 }, cuffs); }
    for (let k = 0; k < 4; k++) sv('ellipse', { cx: 905 + k * 37, cy: 600, rx: 22, ry: 12, fill: 'none', stroke: '#C9CFDA', 'stroke-width': 8 }, cuffs);
    stamp(cuffs, tTied - .1, { r: 0, sfx: 'clang', amp: 1.3 });
    const k1 = T(S, "In a crisis, central banks' *hands are tied*", 960, 150, 64); kin(k1, tCri, { times: wordTimes("In a crisis central banks' hands are tied") });
    tl.to(k1, { autoAlpha: 0, duration: .3 }, A('Many economists', -.3));
    const k2 = T(S, 'Many economists argue it made the', 960, 130, 50, { color: '#8D98B0' }); kin(k2, A('Many economists'));
    const k3 = T(S, '_Great Depression_ so brutal', 960, 205, 74); kin(k3, A('Great Depression'), { times: wordTimes('Great Depression so brutal') });
    tl.to(bk, { y: 14, duration: .4, ease: 'power2.in' }, A('so brutal')); shake(A('so brutal', .1), .7); sfx('thud', A('so brutal', .1), .6); }

  // 4. back to the question: the opening note returns, magnifier on the promise
  { const S = shot(tBack, tToday, { tr: 'wipe', push: 1.06 }); const g = G(S, { opacity: 1 });
    const q = T(S, 'What is your money *backed by?*', 960, 150, 76); kin(q, A('So, back to the question'), { st: .12 });
    tl.to(q, { scale: 1.08, duration: .25, yoyo: true, repeat: 1, ease: 'sine.inOut' }, A('What is your money backed by'));
    const n = note(g, 960, 540, 1000, { num: '20', text: 'I PROMISE TO PAY THE BEARER|ON DEMAND THE SUM OF' }); pop(n, A('question we started', -.2), { s0: .7, sfx: 'whoosh' });
    const lens = sv('g', { opacity: 0 }, g); sv('circle', { cx: 0, cy: 0, r: 140, fill: 'rgba(243,235,221,.12)', stroke: '#E9B44C', 'stroke-width': 14 }, lens); sv('path', { d: 'M100,100 L200,200', stroke: '#E9B44C', 'stroke-width': 26, 'stroke-linecap': 'round' }, lens);
    const tRead = A('Read that British note'); tl.fromTo(lens, { opacity: 0, x: 1550, y: 950 }, { opacity: 1, x: 880, y: 500, duration: .9, ease: 'power3.inOut', ...IR }, tRead); ev(tRead, 'lens'); sfx('whoosh', tRead, .4);
    tl.to(lens, { x: 1050, duration: 1.4, ease: 'sine.inOut' }, tRead + .9); }

  // 5. today the promise means: swap the note... for another note (endless loop)
  { const S = shot(tToday, tTrust, { tr: 'up' }); const g = G(S, { opacity: 1 });
    const k1 = T(S, 'Today the promise means...', 960, 140, 64, { color: '#8D98B0' }); kin(k1, tToday, { st: .12 });
    const CX = 960, CY = 500, RX = 340, RY = 150;
    const nA = note(g, CX - RX, CY, 330, { num: '20' }), nB = note(g, CX + RX, CY, 330, { num: '20' });
    pop(nA, A('its promise'), { s0: .6 });
    const tSwap = A('swap the note'), tAnother = A('for another'); pop(nB, tAnother, { s0: .4, sfx: 'pop' });
    const arc1 = arrowPath(g, `M${CX - 200},${CY - 170} Q${CX},${CY - 300} ${CX + 200},${CY - 170}`, { w: 12 }), arc2 = arrowPath(g, `M${CX + 200},${CY + 170} Q${CX},${CY + 300} ${CX - 200},${CY + 170}`, { w: 12 });
    draw(arc1, tSwap, .5); draw(arc2, tAnother + .2, .5); sfx('swoosh', tSwap, .5);
    const p = { a: 0 }; tl.fromTo(p, { a: 0 }, { a: Math.PI * 2 * 1.25, duration: tTrust - (tAnother + .5) + .4, ease: 'none', ...IR, onUpdate: () => {
      gsap.set(nA, { x: (Math.cos(p.a + Math.PI) + 1) * RX, y: Math.sin(p.a + Math.PI) * RY * -1 }); gsap.set(nB, { x: (Math.cos(p.a) - 1) * RX, y: -Math.sin(p.a) * RY }); } }, tAnother + .5);
    ev(tAnother + 3, 'loop'); ev(tAnother + 6, 'loop');
    const k2 = T(S, 'Swap it... for *another note*', 960, 820, 66); kin(k2, tSwap, { times: wordTimes('swap the note for another').filter((_, i) => i !== 1).concat([A('England note', .25)]) }); }

  // 6. what really stands behind it is trust: three pillars
  { const S = shot(tTrust, tGold, { tr: 'fade' }); const g = G(S, { opacity: 1 });
    const tw = T(S, '*TRUST*', 960, 155, 130, { ls: '.06em' }); kin(tw, A('is trust', .2), { s0: .3, sfx: 'stamp' }); shake(A('is trust', .45), .6);
    const lead = T(S, 'What really stands behind it?', 960, 170, 64, { color: '#8D98B0' }); kin(lead, tTrust); out(lead, A('is trust'), .2);
    const pil = [['Stable', 'prices', A('keeps prices stable')], ['Taxes', 'paid in it', A('collects taxes')], ['Everyone', 'accepts it', A('will still accept')]];
    pil.forEach(([l1, l2, at], i) => { const x = 560 + i * 400; const pg = sv('g', {}, g);
      sv('rect', { x: x - 80, y: 440, width: 160, height: 380, fill: '#C9CFDA', stroke: '#6C7690', 'stroke-width': 6 }, pg);
      sv('rect', { x: x - 105, y: 418, width: 210, height: 34, rx: 6, fill: '#DDE2EA', stroke: '#6C7690', 'stroke-width': 6 }, pg);
      sv('rect', { x: x - 110, y: 812, width: 220, height: 30, rx: 6, fill: '#DDE2EA', stroke: '#6C7690', 'stroke-width': 6 }, pg);
      for (const fx of [-40, 0, 40]) sv('path', { d: `M${x + fx},470 L${x + fx},800`, stroke: '#AEB6C5', 'stroke-width': 5 }, pg);
      svgT(pg, l1, x, 600, 29, { c: '#2B3550', font: 'Brico' }); svgT(pg, l2, x, 645, 30, { c: '#4B5570', font: 'Inter', w: 800 });
      gsap.set(pg, { autoAlpha: 0 }); tl.fromTo(pg, { autoAlpha: 0, y: 460 }, { autoAlpha: 1, y: 0, duration: .6, ease: 'back.out(1.4)', ...IR }, at - .4); sfx('thud', at, .6); ev(at - .4, 'pillar'); });
    const roof = sv('g', {}, g); sv('rect', { x: 430, y: 384, width: 1060, height: 36, rx: 8, fill: '#E9B44C', stroke: '#7A4E0E', 'stroke-width': 5 }, roof);
    const rn = note(roof, 960, 318, 260, { num: '20' }); pop(roof, A('accept it tomorrow', .2), { s0: .6, sfx: 'clink' }); }

  // 7. the payoff, typed slowly, then the mirage dissolves
  { const S = shot(tGold, tEndC, { tr: 'fade', push: 1.04 }); const g = G(S, { opacity: 1 });
    const glow = sv('ellipse', { cx: 960, cy: 470, rx: 900, ry: 360, fill: 'rgba(233,180,76,.045)', style: 'filter: blur(40px)' }, g);
    const gb = goldBar(g, 250, 330, 1.0), nt = note(g, 250, 500, 200, { num: '1' });
    const l1 = T(S, 'Gold was a promise you could *hold.*', 1110, 330, 80); kin(l1, tGold, { times: wordTimes('Gold was a promise you could hold'), sfx: 'typing', vol: .6 }); pop(gb, tGold, { s0: .5, sfx: 'clink', vol: .5 });
    const tPap = A('Paper is a promise'); const l2 = T(S, 'Paper is a promise you have to *believe.*', 1110, 500, 80); kin(l2, tPap, { times: wordTimes('Paper is a promise you have to believe'), sfx: 'typing', vol: .6 }); pop(nt, tPap, { s0: .5, sfx: false });
    const tMom = A('And the moment'); const l3 = T(S, 'And the moment enough people _stop believing..._', 960, 690, 58, { color: '#8D98B0' }); kin(l3, tMom, { times: wordTimes('And the moment enough people stop believing') });
    tl.to(nt, { rotation: -6, duration: .25, yoyo: true, repeat: 3, transformOrigin: '50% 50%' }, A('stop believing'));
    const tMir = A('the mirage disappears'); sfx('shimmer', tMir - .3, 1);
    tl.to(S.stg, { keyframes: [{ skewX: 3, duration: .25 }, { skewX: -3, duration: .25 }, { skewX: 2, duration: .25 }, { skewX: -2, duration: .25 }, { skewX: 0, duration: .25 }] }, tMir - .2);
    tl.to(S.stg, { filter: 'blur(16px)', opacity: 0, scaleY: 1.06, duration: 1.4, ease: 'power2.in' }, tMir); ev(tMir, 'dissolve');
    const band = sv('rect', { x: -200, y: 300, width: 2400, height: 420, fill: 'rgba(233,180,76,.10)', opacity: 0, style: 'filter: blur(30px)' }, S.svg);
    tl.fromTo(band, { opacity: 0, y: 200 }, { opacity: 1, y: -200, duration: 1.6, ease: 'sine.inOut', ...IR }, tMir - .4); }

  // 8. end card: wordmark + subscribe
  { const S = shot(tEndC, D.dur + 1, { tr: 'fade', push: 1.03 }); const wm = c7_wordmark(S.svg, 420, 2.8); gsap.set(wm.g, { opacity: 0 });
    tl.fromTo(wm.g, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .8, ease: 'power3.out', ...IR }, tEndC + .2); sfx('sting', tEndC + .15, .9); ev(tEndC + .2, 'logo');
    tl.fromTo(wm.waves, { x: 0 }, { x: -56, duration: D.dur - tEndC + 1, ease: 'none', ...IR }, tEndC); tl.fromTo(wm.refl, { opacity: 0 }, { opacity: .28, duration: 1, ...IR }, tEndC + .6);
    const btn = mk('div', {}, S.stg); Object.assign(btn.style, { position: 'absolute', left: '760px', top: '600px', width: '400px', height: '104px', borderRadius: '52px', background: '#E9B44C', color: '#101A2E', font: "800 46px 'Brico'", display: 'flex', alignItems: 'center', justifyContent: 'center', letterSpacing: '.02em', boxShadow: '0 14px 40px rgba(0,0,0,.45)' });
    btn.textContent = 'Subscribe'; const tSub = A('Subscribe to Money Mirage'); pop(btn, tSub, { s0: .3 });
    const tPress = A('and next time'); tl.to(btn, { keyframes: [{ scale: .9, duration: .1 }, { scale: 1.06, duration: .14 }, { scale: 1, duration: .12 }] }, tPress); sfx('pop', tPress, .9); ev(tPress, 'press');
    tl.to(btn, { backgroundColor: '#26344F', color: '#E9B44C', duration: .15 }, tPress + .1);
    const tg = T(S, "See through money's *illusions*", 960, 800, 48, { color: '#8D98B0' }); kin(tg, A("we'll see through"), { st: .1 }); }
}
