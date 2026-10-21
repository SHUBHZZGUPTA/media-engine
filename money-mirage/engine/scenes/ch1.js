// CHAPTER 1: WHY GOLD? (lines 6-10) — archival/painted documentary style
const c1_sh = el => { el.style.textShadow = '0 4px 26px rgba(0,0,0,.85), 0 2px 4px rgba(0,0,0,.6)'; return el; };
function ch1() {
  const t0 = CH(1).a - .3, tEc = A('Economists'), tSo = A('So people tried'), tRust = A("It doesn't rust"), tAround = A('Around 600 BC'),
    tSomeone = A('someone stamped'), tThey = A("They're among"), tBut = A('But gold had'), tEnd = LB(10) + .35;
  startCh(1);

  // 1. the barter problem
  { const S = photo(t0, tEc, 'barter_market.jpg', { grade: 'paint', kb: [1.02, 1.2], from: [0, 0], to: [-3, -2], tr: 'fade' });
    lower(S, 'BEFORE MONEY', 'Trading was a *nightmare*', A('Trading without money', -.1));
    const a = c1_sh(I(S, 'YOU HAVE: CHICKENS', 140, 170, 34, { align: 'left', weight: 800, ls: '.18em' })); fin(a, A('You have chickens'), .4);
    const b = c1_sh(I(S, 'YOU WANT: A GOAT', 140, 225, 34, { align: 'left', weight: 800, ls: '.18em', color: '#E9B44C' })); fin(b, A('You want a goat'), .4);
    const c = c1_sh(T(S, 'The goat owner _hates_ chickens', 140, 300, 54, { align: 'left' })); kin(c, A('The goat owner'), { times: wordTimes('The goat owner hates chickens') });
    sfx('stamp', A('hates'), .35); }

  // 2. double coincidence of wants + wasted afternoon
  { const tW = A('wasted afternoon'); const S = photo(tEc, tSo, 'barter_market.jpg', { grade: 'warm', kb: [1.35, 1.5], from: [6, 4], to: [4, 2], tr: 'zoom' });
    const k = c1_sh(I(S, 'ECONOMISTS CALL THIS', 960, 360, 30, { weight: 800, ls: '.3em', color: '#E9B44C' })); fin(k, tEc, .5);
    const h = c1_sh(T(S, 'The double coincidence of *wants*', 960, 450, 92)); kin(h, A('the double coincidence'), { times: wordTimes('the double coincidence of wants') });
    // clock: a whole afternoon sweeping past
    const g = G(S); const cx = 1620, cy = 690;
    sv('circle', { cx, cy, r: 92, fill: 'rgba(10,17,32,.55)', stroke: '#F3EBDD', 'stroke-width': 5 }, g);
    for (let i = 0; i < 12; i++) { const an = i * Math.PI / 6; sv('line', { x1: cx + Math.sin(an) * 76, y1: cy - Math.cos(an) * 76, x2: cx + Math.sin(an) * 86, y2: cy - Math.cos(an) * 86, stroke: '#F3EBDD', 'stroke-width': 4 }, g); }
    const hh = sv('line', { x1: cx, y1: cy, x2: cx, y2: cy - 48, stroke: '#E9B44C', 'stroke-width': 8, 'stroke-linecap': 'round' }, g);
    const mm = sv('line', { x1: cx, y1: cy, x2: cx, y2: cy - 72, stroke: '#F3EBDD', 'stroke-width': 5, 'stroke-linecap': 'round' }, g);
    sv('circle', { cx, cy, r: 8, fill: '#E9B44C' }, g);
    fin(g, A('Everyone else', -.2), .4);
    tl.fromTo(mm, { rotation: 0, transformOrigin: '50% 100%' }, { rotation: 1440, duration: 1.8, ease: 'power2.inOut', ...IR }, tW - .2);
    tl.fromTo(hh, { rotation: 0, transformOrigin: '50% 100%' }, { rotation: 120, duration: 1.8, ease: 'power2.inOut', ...IR }, tW - .2);
    for (let i = 0; i < 6; i++) sfx('tick', tW - .2 + i * .3, .3);
    const w = c1_sh(I(S, 'a.k.a. a wasted afternoon', 1620, 830, 30, { weight: 600, color: '#C9CFDA' })); fin(w, tW, .4); }

  // 3. shells, cattle, metal... gold
  { const tGold = A('Gold', -.05); const S = photo(tSo, tRust, 'lydia_mint.jpg', { grade: 'soft', kb: [1.08, 1.18], tr: 'fade' }); tl.set(S.img, { filter: GRADES.soft + ' blur(5px)' }, tSo);
    const k = c1_sh(I(S, 'PEOPLE TRIED', 960, 250, 30, { weight: 800, ls: '.32em', color: '#E9B44C' })); fin(k, tSo, .4);
    const words = [['Shells', 540, A('shells')], ['Cattle', 960, A('cattle')], ['Metal', 1380, A('metal')]]; const els = [];
    words.forEach(([w, x, t]) => { const e = c1_sh(T(S, w, x, 400, 86)); kin(e, t, { sfx: 'swoosh', vol: .25 }); els.push([e, x]); });
    els.forEach(([e, x], i) => { const ln = sv('line', { x1: x - 150, y1: 400, x2: x + 150, y2: 400, stroke: '#E2614B', 'stroke-width': 8, 'stroke-linecap': 'round', opacity: 0 }, S.svg);
      draw(ln, A('and one material', .1 + i * .18), .3); tl.to(e, { opacity: .45, duration: .3 }, A('and one material', .15 + i * .18)); });
    const g = c1_sh(T(S, '*GOLD*', 960, 640, 210)); kin(g, tGold, { s0: .5, sfx: 'clink', vol: .7 }); flash(tGold + .05, .2); }

  // 4. the four properties
  { const tW = A('everyone, everywhere'); const S = photo(tRust, tAround, 'bank_vault_1700s.jpg', { grade: 'paint', kb: [1.04, 1.16], from: [-2, 0], to: [-5, -2], tr: 'slide' });
    const items = [["Doesn't rust", A("doesn't rust")], ["Doesn't rot", A("doesn't rot")], ['Rare, but not too rare', A("It's rare")], ['Melt it · split it · stamp it', A('You can melt')]];
    items.forEach(([txt, t], i) => { const y = 250 + i * 110; const tick = sv('path', { d: `M1040,${y - 8} l18,18 l34,-38`, fill: 'none', stroke: '#E9B44C', 'stroke-width': 9, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', opacity: 0 }, S.svg);
      draw(tick, t, .35); const e = c1_sh(T(S, txt, 1110, y, 56, { align: 'left' })); kin(e, t + .05, { st: .05, sfx: 'swoosh', vol: .2 }); });
    const w = c1_sh(T(S, 'Wanted *everywhere*', 1110, 720, 72, { align: 'left' })); kin(w, tW, { times: wordTimes('everyone everywhere') }); }

  // 5. Lydia on the map
  { const S = mapShot(tAround, tSomeone, { tr: 'fade' }); camSet(S, 20, 38, 1.1); camTo(S, 28.5, 38.8, 4.2, tAround, 3.4, 'power2.inOut');
    pin(S, 28.04, 38.49, A('in Lydia'), { r: 12 }); mlabel(S, 'LYDIA', 28.04, 38.49, A('in Lydia', .2), { fs: 26 });
    mlabel(S, 'today: western Turkey', 28.04, 38.49, A('western Turkey'), { fs: 14, c: '#E9B44C', dy: 44 });
    lower(S, 'AROUND 600 BC', 'Lydia', tAround, { size: 110 }); }

  // 6. stamping electrum
  { const tSt = A('stamped lumps'); const S = photo(tSomeone, tThey, 'lydia_mint.jpg', { grade: 'paint', kb: [1.1, 1.32], from: [0, 0], to: [-8, -6], tr: 'zoom' });
    sfx('stamp', tSt + .1, .6); flash(tSt + .12, .15); shake(tSt + .12, .5);
    lower(S, 'ELECTRUM', 'Gold + silver, *stamped*', A('lumps of electrum', -.1));
    const m = c1_sh(I(S, 'WITH AN OFFICIAL MARK', 124, 900, 28, { align: 'left', weight: 800, ls: '.28em', color: '#C9CFDA' })); fin(m, A('an official mark'), .4); }

  // 7. the earliest coins — just count
  { const tCount = A('You could just count'); const S = photo(tThey, tBut, 'lydia_trite_bm.jpg', { grade: 'warm', kb: [1.0, 1.18], tr: 'fade', credit: 'Lydian electrum trite, British Museum · ArchaiOptix, CC BY-SA 4.0' });
    const k = c1_sh(I(S, 'AMONG THE EARLIEST COINS WE KNOW OF', 960, 150, 32, { weight: 800, ls: '.28em', color: '#E9B44C' })); fin(k, A('earliest coins', -.2), .5);
    const n = c1_sh(T(S, 'No more _weighing_', 140, 700, 80, { align: 'left' })); kin(n, A('No more weighing'), { times: wordTimes('No more weighing') });
    const c = c1_sh(T(S, 'Just *count*', 140, 800, 80, { align: 'left' })); kin(c, tCount + .3, { sfx: 'clink', vol: .5 });
    ['1', '2', '3'].forEach((d, i) => { const e = c1_sh(T(S, d, 1500 + i * 110, 800, 90, { color: '#E9B44C' })); kin(e, tCount + .5 + i * .22, { sfx: 'clink', vol: .35 }); }); }

  // 8. gold is heavy — and paper slips in through the back door
  { const tHv = A("It's heavy"); const S = photo(tBut, tEnd, 'bank_vault_1700s.jpg', { grade: 'warm', kb: [1.3, 1.45], from: [16, 6], to: [12, 4], tr: 'wipe' });
    const l = lower(S, 'ONE BIG PROBLEM', 'Gold is *heavy*', A('one big problem', -.1));
    tl.to(l.h, { y: 22, duration: .14, ease: 'power3.in', yoyo: true, repeat: 1 }, tHv + .2); sfx('thud', tHv + .25, .8); shake(tHv + .3, .6);
    const b = c1_sh(T(S, 'A house? With a *backpack* of coins?', 1800, 200, 54, { align: 'right' })); kin(b, A('Try buying'), { st: .07 });
    // a door opening: a sliver of light with paper drifting in
    const g = G(S, { opacity: 1 }); const door = sv('rect', { x: 1450, y: 330, width: 0, height: 330, fill: 'rgba(243,235,221,.85)', style: 'filter: drop-shadow(0 0 30px rgba(233,180,76,.8))' }, g);
    tl.fromTo(door, { attr: { width: 0, x: 1550 } }, { attr: { width: 150, x: 1475 }, duration: .8, ease: 'power2.out', ...IR }, A('let paper', -.1)); sfx('swoosh', A('let paper'), .4);
    const p = c1_sh(T(S, 'Enter: *paper*', 1550, 720, 64)); kin(p, A('paper in through'), { sfx: false }); }
}
