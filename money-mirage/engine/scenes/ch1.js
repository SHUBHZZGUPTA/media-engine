// CHAPTER 1: WHY GOLD? (lines 6-10)
function c1_clock(parent, x, y, r) { const g0 = sv('g', { transform: `translate(${x},${y})` }, parent); const g = sv('g', {}, g0);
  sv('circle', { r, fill: '#F3EBDD', stroke: '#C9CFDA', 'stroke-width': r * .08 }, g);
  for (let k = 0; k < 12; k++) { const a = k / 12 * 6.283; sv('line', { x1: Math.sin(a) * r * .78, y1: -Math.cos(a) * r * .78, x2: Math.sin(a) * r * .9, y2: -Math.cos(a) * r * .9, stroke: '#4B5570', 'stroke-width': r * .04, 'stroke-linecap': 'round' }, g); }
  // hands drawn through the centre (half dashed away) so their bbox centre is the pivot
  const hm = sv('path', { d: `M0,${-r * .72} L0,${r * .72}`, stroke: '#101A2E', 'stroke-width': r * .06, 'stroke-linecap': 'round', 'stroke-dasharray': `${r * .72} ${r * 2}` }, g);
  const hh = sv('path', { d: `M0,${-r * .48} L0,${r * .48}`, stroke: '#E2614B', 'stroke-width': r * .09, 'stroke-linecap': 'round', 'stroke-dasharray': `${r * .48} ${r * 2}` }, g);
  sv('circle', { r: r * .07, fill: '#101A2E' }, g); return { g, hm, hh }; }
function c1_lump(parent, x, y, s) { const g0 = sv('g', { transform: `translate(${x},${y}) scale(${s})` }, parent); const g = sv('g', {}, g0);
  sv('path', { d: 'M-70,-20 Q-60,-62 -10,-58 Q40,-74 66,-34 Q92,6 62,40 Q24,70 -30,56 Q-84,44 -70,-20 Z', fill: '#E6D59A', stroke: '#8A7A3A', 'stroke-width': 6 }, g);
  sv('path', { d: 'M-40,-30 Q-20,-46 10,-40', fill: 'none', stroke: '#FFF6D8', 'stroke-width': 8, 'stroke-linecap': 'round', opacity: .7 }, g); return g; }

function ch1() {
  const c0 = CH(1).a - .3;
  const t2 = A('Economists call this'), t3 = A('So people tried'), t4 = A("It doesn't rust"), t5 = A('Around 600 BC'), t6 = A('someone stamped'),
    t7 = A('No more weighing'), t8 = A('But gold had one'), tEnd = LB(10) + .35;
  startCh(1);

  // 1. barter skit: chickens vs goat
  { const S = shot(c0, t2, { tr: 'fade' });
    const t = T(S, 'Trading without money is a *nightmare*', 960, 150, 70); kin(t, A('Trading without money'));
    const ck = E(S, '🐔', 470, 520, 230); pop(ck, A('You have chickens'), { y0: 60 }); bob(ck, A('You have chickens', .5), t2, 8, 1.1);
    const lb1 = I(S, 'YOU', 470, 720, 40, { color: '#8D98B0', ls: '.2em' }); pop(lb1, A('You have chickens'), { sfx: false });
    const gt = E(S, '🐐', 1450, 520, 230); pop(gt, A('You want a goat'), { y0: 60 });
    const ar = arrowPath(S.svg, 'M650,520 Q960,380 1270,520', { w: 12 }); draw(ar, A('want a goat'), .6);
    const ow = E(S, '🧑‍🌾', 1650, 360, 130); pop(ow, A('The goat owner'), { x0: 120 });
    const no = E(S, '😤', 1720, 230, 90); pop(no, A('hates chickens'));
    wiggle(gt, A('hates chickens'), 9, 4); sfx('boing', A('hates chickens'), .5);
    const x = sv('path', { d: 'M900,400 L1020,520 M1020,400 L900,520', stroke: '#E2614B', 'stroke-width': 26, 'stroke-linecap': 'round', opacity: 0 }, S.svg);
    stamp(x, A('hates chickens', .45), { r: 0 }); }

  // 2. double coincidence of wants + wasted afternoon clock
  { const tW = A('Everyone else calls'); const S = shot(t2, t3, { tr: 'zoom' });
    const pn = P(S, 460, 200, 1000, 300); pop(pn, t2, { s0: .8, sfx: 'whoosh' });
    const lb = I(S, 'ECONOMISTS CALL IT', 960, 270, 34, { color: '#8D98B0', ls: '.24em' }); pop(lb, t2, { sfx: false });
    const t = T(S, 'the *double coincidence* of wants', 960, 390, 64); kin(t, A('the double coincidence'), { times: wordTimes('the double coincidence of wants') });
    const ck = c1_clock(S.svg, 960, 690, 120); pop(ck.g, tW, { s0: .3 });
    spin(ck.hm, tW + .2, t3 + .4, 360 * 9); spin(ck.hh, tW + .2, t3 + .4, 360 * .75);
    for (let k = 0; k < 6; k++) sfx('tick', tW + .4 + k * .4, .4);
    tl.to(pn, { y: -60, duration: .5, ease: 'power2.inOut' }, tW - .2); tl.to([lb, t], { y: -60, duration: .5, ease: 'power2.inOut' }, tW - .2);
    const w = T(S, 'a *wasted afternoon*', 1430, 690, 56); kin(w, A('a wasted afternoon')); }

  // 3. shells, cattle, metal... gold wins
  { const tG = A('Gold.'); const S = shot(t3, t4, { tr: 'slide' });
    const t = T(S, 'People tried...', 960, 150, 64, { color: '#8D98B0' }); kin(t, A('So people tried'));
    const items = [['🐚', 'SHELLS', 'shells', 520], ['🐄', 'CATTLE', 'cattle', 960], ['🔩', 'METAL', 'metal', 1400]].map(([e, l, w, x]) => {
      const em = E(S, e, x, 420, 200); pop(em, A(w), { y0: 50 }); const lb = I(S, l, x, 590, 38, { color: '#F3EBDD', ls: '.2em', weight: 800 }); pop(lb, A(w, .1), { sfx: false }); return [em, lb]; });
    tl.to(items.flat(), { opacity: .18, scale: .8, duration: .5 }, A('one material kept'));
    const k = T(S, 'One kept *winning*', 960, 150, 64); out(t, A('one material kept') - .05, .2); kin(k, A('one material kept'));
    const gb = goldBar(S.svg, 960, 470, 2.6); pop(gb, tG, { s0: 3, sfx: 'clink', ease: 'power4.in', d: .3 }); shake(tG + .3, .9); flash(tG + .28, .4);
    const sp = E(S, '✨', 1240, 330, 110); pop(sp, tG + .35, { sfx: 'sparkle' }); spin(sp, tG + .4, t4 + .5, 90); }

  // 4. four badges: why gold
  { const tE = A('And everyone, everywhere'); const S = shot(t4, t5, { tr: 'up' });
    const gb = goldBar(S.svg, 960, 240, 1.3); pop(gb, t4, { s0: .5, sfx: 'clink' }); bob(gb, t4 + .5, t5, 6, 2.2);
    const B = [["Doesn't rust", "It doesn't rust", '🛡️'], ["Doesn't rot", "It doesn't rot", '⏳'], ['Rare, not too rare', "It's rare", '💎'], ['Melt, split, stamp', 'You can melt', '🔨']];
    B.forEach(([lbl, ph, em], i) => { const x = 270 + i * 460; const at = A(ph); const p = P(S, x - 200, 420, 400, 250); stamp(p, at, { r: i % 2 ? 3 : -3, amp: .5, sfx: 'stamp' });
      const e = E(S, em, x, 505, 100); pop(e, at + .25, { sfx: false }); const l = I(S, lbl, x, 625, 36, { weight: 800 }); pop(l, at + .3, { sfx: false }); });
    const em = E(S, '🌍', 640, 790, 90); pop(em, tE, { sfx: 'ping' }); spin(em, tE, t5 + .5, 40);
    const w = T(S, 'Wanted *everywhere*', 1050, 790, 64); kin(w, tE, { times: [A('everyone'), A('everywhere')] }); }

  // 5. map: Lydia, ~600 BC
  { const S = mapShot(t5, t6, { tr: 'wipe' });
    camSet(S, 30, 39, 1.3); camTo(S, 28.5, 38.8, 4.4, A('Around 600 BC'), 2.6, 'power2.inOut'); camTo(S, 29.5, 39.2, 3.6, A('western Turkey'), 1.4, 'sine.inOut');
    const y = T(S, 'Around *600 BC*', 960, 150, 96); kin(y, A('600 BC'), { s0: .4, sfx: 'pop' });
    pin(S, 28.04, 38.49, A('Lydia'), { r: 10 }); mlabel(S, 'LYDIA', 28.04, 38.49, A('Lydia', .1), { fs: 22, c: '#E9B44C' });
    mlabel(S, 'today: TURKEY', 33, 39.8, A('western Turkey'), { fs: 16, c: '#F3EBDD' }); }

  // 6. electrum lump stamped into a coin
  { const tM = A('official mark'), tE2 = A("They're among the earliest"); const S = shot(t6, t7, { tr: 'zoom' });
    const lump = c1_lump(S.svg, 700, 560, 1.6); pop(lump, A('lumps of electrum'), { s0: .5 });
    const lb = T(S, '*Electrum*', 700, 220, 72); kin(lb, A('electrum'));
    const mx = T(S, 'gold + silver', 700, 330, 48, { color: '#C9CFDA', font: 'Inter', weight: 800 }); kin(mx, A('natural mix'));
    const ham = sv('g', { opacity: 0 }, S.svg); sv('rect', { x: 1120, y: 180, width: 60, height: 260, rx: 10, fill: '#8A5530', stroke: '#2E190C', 'stroke-width': 6 }, ham);
    sv('rect', { x: 1040, y: 420, width: 220, height: 90, rx: 12, fill: '#8D98B0', stroke: '#3A4766', 'stroke-width': 6 }, ham);
    fin(ham, tM - .9, .3); tl.fromTo(ham, { x: 0, y: -60 }, { x: -450, y: -60, duration: .5, ease: 'power2.inOut', ...IR }, tM - .7);
    tl.to(ham, { y: 30, duration: .14, ease: 'power4.in' }, tM - .14); tl.to(ham, { y: -200, opacity: 0, duration: .4, ease: 'power2.out' }, tM + .1);
    sfx('clang', tM, .9); shake(tM, 1.3); flash(tM, .45); out(lump, tM + .02, .05);
    const cn = coin(S.svg, 700, 560, 120, { mark: '★' }); pop(cn, tM + .02, { s0: 1.4, sfx: 'clink', d: .3 });
    const sp = E(S, '✨', 860, 430, 100); pop(sp, tM + .2, { sfx: 'sparkle' });
    tl.to([lb, mx], { opacity: 0, duration: .3 }, tE2 - .3);
    const t = T(S, 'Among the *earliest coins*', 1300, 560, 62); kin(t, tE2, { times: wordTimes("among the earliest coins") });
    bob(cn, tM + .5, t7 + .3, 8, 2); }

  // 7. no more weighing - just count
  { const tC = A('You could just count'); const S = shot(t7, t8, { tr: 'slide' });
    const sc = scaleProp(S.svg, 560, 560, 1.1); pop(sc.g, t7, { s0: .6 });
    const lp = c1_lump(sc.L, -200, -80, .55); tl.set(lp, { opacity: 1 }, 0);
    const x = sv('path', { d: 'M380,360 L740,720 M740,360 L380,720', stroke: '#E2614B', 'stroke-width': 28, 'stroke-linecap': 'round', opacity: 0 }, S.svg); stamp(x, A('weighing metal'), { r: 0 });
    for (let k = 0; k < 3; k++) { const c = coin(S.svg, 1180 + k * 170, 560, 70, { mark: String(k + 1) }); pop(c, tC + k * .22, { sfx: 'clink', y0: -80 }); }
    const t = T(S, 'Just *count*', 1350, 330, 76); kin(t, tC, { times: wordTimes('just count') }); }

  // 8. gold is heavy; backpack; paper sneaks in the back door
  { const tH = A("It's heavy"), tB = A('Try buying'), tD = A('And that problem'), tP = A('let paper in'); const S = shot(t8, tEnd, { tr: 'wipe' });
    const t = T(S, 'One big *problem*', 960, 150, 72); kin(t, A('one big problem'), { times: wordTimes('one big problem') });
    const gb = goldBar(S.svg, 960, 260, 2.2); pop(gb, tH - .2, { s0: .5 });
    tl.to(gb, { y: 150, duration: .35, ease: 'power4.in' }, tH); sfx('thud', tH + .33); shake(tH + .35, 1.5);
    const hv = T(S, '_HEAVY_', 1380, 560, 90); stamp(hv, tH + .3, { r: 8, sfx: false });
    tl.to([gb, hv, t], { opacity: 0, duration: .3 }, A('a house') - .3);
    const hs = E(S, '🏠', 520, 470, 220); pop(hs, A('a house'));
    const bp = E(S, '🎒', 1280, 470, 240); pop(bp, A('a backpack'), { y0: 60 });
    for (let k = 0; k < 5; k++) { const c = coin(S.svg, 1180 + (k % 3) * 90, 300 - Math.floor(k / 3) * 60, 34); pop(c, A('full of coins') + k * .12, { sfx: 'clink', vol: .5, y0: -120 }); tl.to(c, { y: 140, opacity: 0, duration: .3, ease: 'power2.in' }, A('full of coins') + .8 + k * .05); }
    tl.to(bp, { scaleY: .72, scaleX: 1.18, y: 40, transformOrigin: '50% 100%', duration: .3, ease: 'power2.in' }, A('full of coins') + .9); sfx('thud', A('full of coins') + 1.1, .7);
    const sw = E(S, '😩', 1400, 300, 80); pop(sw, A('full of coins') + 1.2);
    tl.to([hs, bp, sw], { opacity: 0, duration: .3 }, tD - .1);
    const door = P(S, 760, 200, 400, 600, { bg: '#2A1F17', border: '#6B3E22' }); fin(door, tD, .3);
    const leaf = P(S, 760, 200, 400, 600, { bg: '#8A5530', border: '#2E190C' }); fin(leaf, tD, .3);
    tl.to(leaf, { rotationY: -75, transformOrigin: '0% 50%', transformPerspective: 1200, duration: .6, ease: 'power2.inOut' }, tP - .3); sfx('flip', tP - .3, .6);
    const n = note(S.svg, 960, 500, 300, { num: '1' }); tl.set(n, { opacity: 0 }, 0);
    tl.fromTo(n, { opacity: 1, x: 900, rotation: 20 }, { x: 0, rotation: -6, duration: .7, ease: 'back.out(1.5)', ...IR }, tP); sfx('whoosh', tP, .6);
    const bd = T(S, 'through the *back door*', 960, 150, 64); kin(bd, A('through the back door'), { times: wordTimes('through the back door') }); }
}
