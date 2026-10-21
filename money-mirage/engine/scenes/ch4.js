// CHAPTER 4: THE DOLLAR BECOMES THE WORLD'S GOLD (lines 23-28) — archival / painted documentary style
const c4_top = S => S.stg.appendChild(S.svg);
const c4_dim = (S, o) => sv('rect', { x: 0, y: 0, width: 1920, height: 1080, fill: '#080C16', opacity: o == null ? .55 : o }, S.svg);
const c4_circ = (g, x, y, r, txt, fill, tc) => { const c = sv('g', {}, g); sv('circle', { cx: x, cy: y, r, fill: fill || '#16233D', stroke: '#E9B44C', 'stroke-width': 5 }, c); svgT(c, txt, x, y + r * .36, r * 1.0, { c: tc || '#F3EBDD' }); return c; };
function ch4() {
  const t0 = CH(4).a - .3, tHotel = A('check into a hotel'), tPlan = A('The plan'), tWhy = A('Why the dollar'), tSud = A('Suddenly the dollar'), tTrap = A('But there was a trap'),
    tMore = A('And the more dollars'), tFr = A('France noticed'), tMin = A('Its finance minister'), tPlug = A('America plugged'), tEnd = LB(28) + .35;
  startCh(4);

  // 1. July 1944: the war, 44 countries, a map to Bretton Woods
  { const S = mapShot(t0, tHotel, { tr: 'fade' }); camSet(S, -30, 35, .5); camTo(S, -71.44, 44.26, 3.2, A('44 countries', -.3), tHotel - A('44 countries', -.3) + .4, 'power2.inOut');
    const l = lower(S, 'JULY 1944', 'The Second World War is still *raging*', A('July 1944', -.1), { size: 76, y: 300 });
    tl.to([l.k, l.h], { autoAlpha: 0, duration: .3 }, A('and delegates', -.2));
    const n = I(S, '0', 960, 360, 200, { weight: 900, color: '#E9B44C' }); fin(n, A('44 countries', -.1), .2); count(n, 0, 44, A('44 countries', -.1), 1.1);
    const nl = I(S, 'COUNTRIES SEND DELEGATES', 960, 480, 32, { weight: 800, ls: '.28em' }); fin(nl, A('44 countries', .2), .4);
    tl.to([n, nl], { autoAlpha: 0, duration: .3 }, tHotel - .5); pin(S, -71.44, 44.26, tHotel - .6, { r: 6, rep: 2 }); }

  // 2. the hotel at Bretton Woods: not for a holiday
  { const S = photo(tHotel, tPlan, 'mtwashington.jpg', { grade: 'warm', kb: [1.15, 1.2], tr: 'fade', credit: 'Mount Washington Hotel, Bretton Woods, historic postcard · Public domain' }); tl.set(S.img, { filter: GRADES.warm + ' blur(10px) brightness(.6)' }, tHotel - .2);
    const c = card(S, 'mtwashington.jpg', 980, 170, 820, { rot: 3, filter: 'sepia(.35) contrast(1.05)' }); c4_top(S); slideIn(c, tHotel + .1, 120, 0, { d: .7 });
    tl.to(c, { scale: 1.05, duration: tPlan - tHotel, ease: 'none' }, tHotel + .8);
    lower(S, 'BRETTON WOODS, NEW HAMPSHIRE', 'A hotel in the *mountains*', tHotel + .2, { size: 66, y: 560, x: 110 });
    const nh = T(S, 'Not for a *holiday.*', 120, 700, 66, { align: 'left' }); kin(nh, A('Not for a holiday'), { times: wordTimes('Not for a holiday') }); }

  // 3. the plan: currencies -> dollar -> gold
  { const S = photo(tPlan, tWhy, 'bw_room.jpg', { grade: 'warm', kb: [1.04, 1.12], from: [2, 0], to: [-2, 0], tr: 'slide', credit: 'Bretton Woods conference room · Pi3.124, CC BY-SA 4.0' }); c4_dim(S, .66);
    const k = I(S, 'THE PLAN', 960, 150, 30, { weight: 800, color: '#E9B44C', ls: '.32em' }); fin(k, tPlan, .4);
    const g = sv('g', {}, S.svg); const cur = [['£', 260], ['₣', 470], ['…', 680]].map(([s, y]) => c4_circ(g, 420, y, 70, s));
    const usd = c4_circ(g, 960, 470, 115, '$', '#E9B44C', '#101A2E'); const gb = goldBar(g, 1530, 470, 1.6);
    const arrs = cur.map((c, i) => arrowPath(g, `M500,${[260, 470, 680][i]} L835,470`, { w: 6 })); const ar2 = arrowPath(g, 'M1085,470 L1340,470', { w: 8 });
    const lp = svgT(g, '35 DOLLARS AN OUNCE', 1530, 600, 28, { c: '#F3EBDD', font: 'Inter', w: 800, ls: '.1em' }); const ls = svgT(g, 'SWAPPABLE BY FOREIGN GOVERNMENTS', 1530, 642, 22, { c: '#C9CFDA', font: 'Inter', w: 800, ls: '.08em' });
    cur.forEach((c, i) => pop(c, A('other currencies', i * .15), { sfx: i ? false : 'pop' })); arrs.forEach((a, i) => draw(a, A('peg to the dollar', -.1 + i * .1), .5));
    pop(usd, A('the dollar,', -.1), { sfx: 'clink' }); pop(gb, A('pegs to gold', -.1), { sfx: 'clink' }); draw(ar2, A('pegs to gold', -.2), .5);
    pop(lp, A('at 35 dollars'), { sfx: false }); pop(ls, A('swappable'), { sfx: false });
    tl.to(usd, { scale: 1.08, transformOrigin: '50% 50%', transformBox: 'fill-box', yoyo: true, repeat: 1, duration: .3 }, A('peg to the dollar', .4)); }

  // 4. why the dollar? ~3/4 of the world's official gold
  { const S = photo(tWhy, tSud, 'fortknox_postcard.jpg', { grade: 'mono', kb: [1.04, 1.14], to: [-2, -1], tr: 'fade', credit: 'Fort Knox Bullion Depository, postcard · Tichnor Bros., Boston Public Library · Public domain' }); c4_dim(S, .5);
    const l = lower(S, 'WHY THE DOLLAR?', 'America held about *three quarters*', tWhy, { size: 70, x: 110, y: 330 });
    const sub = I(S, "OF THE WORLD'S OFFICIAL GOLD", 116, 400, 32, { align: 'left', weight: 800, ls: '.2em' }); fin(sub, A("of the world's", -.2), .4);
    const g = sv('g', {}, S.svg); const R = 190, cx = 1420, cy = 560, C = 2 * Math.PI * R;
    sv('circle', { cx, cy, r: R, fill: 'rgba(16,26,46,.75)', stroke: '#26344F', 'stroke-width': 4 }, g);
    const arc = sv('circle', { cx, cy, r: R / 2, fill: 'none', stroke: '#E9B44C', 'stroke-width': R, 'stroke-dasharray': `0 ${Math.PI * R}`, transform: `rotate(-90 ${cx} ${cy})` }, g);
    tl.fromTo(arc, { attr: { 'stroke-dasharray': `0 ${Math.PI * R}` } }, { attr: { 'stroke-dasharray': `${Math.PI * R * .75} ${Math.PI * R}` }, duration: 1.2, ease: 'power2.out', ...IR }, A('three quarters', -.2));
    const pl = svgT(g, '~¾', cx, cy + 30, 90, { c: '#101A2E' }); gsap.set(pl, { autoAlpha: 0 }); tl.to(pl, { autoAlpha: 1, duration: .3 }, A('three quarters', .8)); sfx('swoosh', A('three quarters', -.2), .4); }

  // 5. as good as gold... looking expensive
  { const tSits = A('Gold just sits'); const S = photo(tSud, tTrap, 'bank_vault_1700s.jpg', { grade: 'paint', kb: [1.0, 1.16], from: [0, 0], to: [-3, -2], tr: 'zoom' }); c4_dim(S, .25);
    const a = T(S, 'The dollar: *as good as gold*', 960, 220, 84); kin(a, A('Suddenly the dollar', .3)); out(a, tSits - .2);
    const b = T(S, '...and you could *invest* it', 960, 330, 56, { color: '#C9CFDA' }); kin(b, A('You could invest')); out(b, tSits - .2);
    const c = T(S, 'Gold just sits there,', 120, 700, 70, { align: 'left' }); kin(c, tSits, { times: wordTimes('Gold just sits there') });
    const d = T(S, '*looking expensive.*', 120, 790, 70, { align: 'left' }); kin(d, A('looking expensive'), { times: wordTimes('looking expensive') });
    const glint = sv('rect', { x: 0, y: -200, width: 140, height: 1500, fill: 'rgba(255,240,200,.28)', transform: 'rotate(18 960 540)', style: 'filter: blur(18px)' }, S.svg);
    tl.fromTo(glint, { x: -400 }, { x: 2300, duration: 1.1, ease: 'power2.inOut', ...IR }, A('looking expensive', .1)); sfx('sparkle', A('looking expensive', .2), .7); }

  // 6. the trap: dollars sent abroad
  { const S = mapShot(tTrap, tMore, { tr: 'slide' }); camSet(S, -20, 30, .55); camTo(S, 0, 28, .62, tTrap, tMore - tTrap + .4, 'sine.inOut');
    lower(S, 'A TRAP BUILT IN', 'Dollars had to keep going *abroad*', tTrap + .1, { size: 70, y: 860 });
    const us = [-90, 39]; pin(S, us[0], us[1], A('To give the world', -.2), { r: 16, rep: 1 });
    [[2.35, 48.86], [-0.13, 51.5], [13.4, 52.5], [139.7, 35.7], [-46.6, -23.5], [28, -26], [77.2, 28.6]].forEach(([lo, la], i) => marc(S, us[0], us[1], lo, la, A('keep sending', -.3 + i * .22), .9, { c: '#7FB58A', w: 7, bend: .2 })); }

  // 7. Triffin: dollars pile up overseas, the gold stays fixed
  { const tTr = A('Economists call this'); const S = photo(tMore, tFr, 'central_bank.jpg', { grade: 'paint', kb: [1.08, 1.14], tr: 'fade' }); tl.set(S.img, { filter: GRADES.paint + ' blur(6px) brightness(.55)' }, tMore - .2);
    const g = sv('g', {}, S.svg);
    const lv = svgT(g, 'GOLD IN AMERICAN VAULTS', 560, 250, 28, { c: '#E9B44C', font: 'Inter', w: 900, ls: '.16em' }); const lo = svgT(g, 'DOLLARS OVERSEAS', 1360, 250, 28, { c: '#7FB58A', font: 'Inter', w: 900, ls: '.16em' });
    const bars = []; for (let k = 0; k < 4; k++) bars.push(goldBar(g, 560, 700 - k * 62, 1.1));
    const notes = []; for (let k = 0; k < 9; k++) { const n = note(g, 1360 + (k % 2 ? 26 : -26), 730 - k * 48, 260, { fill: '#E6EEDF' }); notes.push(n); }
    [lv, lo].forEach(e => pop(e, tMore, { sfx: false })); bars.forEach((b, k) => pop(b, tMore + .1 + k * .08, { sfx: k ? false : 'clink' }));
    notes.forEach((n, k) => pop(n, A('piled up overseas', -.3 + k * .22), { s0: .6, y0: -80, sfx: k % 3 ? false : 'flip' }));
    const cov = svgT(g, 'NOT ENOUGH GOLD TO COVER THEM', 960, 860, 34, { c: '#E2614B', font: 'Inter', w: 900, ls: '.14em' }); pop(cov, A('could cover them', -.2), { sfx: 'thud' });
    tl.to([lv, lo, cov, ...bars, ...notes], { autoAlpha: .15, duration: .4 }, tTr - .2);
    const t = T(S, 'The *Triffin dilemma*', 960, 480, 120); kin(t, tTr, { st: .12 }); }

  // 8. France noticed: January 1965, at least 300 million dollars for gold
  { const S = mapShot(tFr, tMin, { tr: 'fade' }); camSet(S, -37, 42, .82); camTo(S, -37, 43, .9, tFr, tMin - tFr + .4, 'sine.inOut');
    const l = lower(S, 'FRANCE · JANUARY 1965', 'France *noticed*', tFr, { size: 84, y: 300 });
    pin(S, 2.35, 48.86, tFr + .3, { rep: 1 }); mlabel(S, 'PARIS', 2.35, 48.86, tFr + .4, { fs: 34 }); pin(S, -77.04, 38.9, A('it announced'), { c: '#F3EBDD', rep: 1 }); mlabel(S, 'WASHINGTON', -77.04, 38.9, A('it announced', .1), { fs: 34 });
    marc(S, 2.35, 48.86, -77.04, 38.9, A('would swap', -.1), 1.0, { c: '#7FB58A', w: 9, bend: .12 });
    marc(S, -77.04, 38.9, 2.35, 48.86, A('for American gold', -.2), 1.0, { c: '#E9B44C', w: 9, bend: .22 });
    const n = I(S, '0', 960, 640, 120, { weight: 900, color: '#E9B44C' }); fin(n, A('at least 300', -.1), .2); count(n, 0, 300, A('at least 300', -.1), 1.2, { pre: 'AT LEAST ', suf: ' MILLION' });
    const u = I(S, 'OF ITS DOLLARS, SWAPPED FOR AMERICAN GOLD', 960, 735, 30, { weight: 800, ls: '.18em' }); fin(u, A('of its dollars'), .4); }

  // 9. exorbitant privilege
  { const S = photo(tMin, tPlug, 'trading_room.jpg', { grade: 'paint', kb: [1.06, 1.14], tr: 'zoom' }); tl.set(S.img, { filter: GRADES.paint + ' blur(8px) brightness(.45)' }, tMin - .2);
    const k = I(S, "FRANCE'S FINANCE MINISTER, VALÉRY GISCARD D'ESTAING", 960, 300, 30, { weight: 800, color: '#E9B44C', ls: '.18em' }); fin(k, tMin, .5);
    const q = T(S, '"Exorbitant *privilege."*', 960, 520, 150, { font: 'Brico' }); kin(q, A('"exorbitant', -.15), { times: wordTimes('exorbitant privilege'), s0: .8 });
    const sub = I(S, "— HIS NAME FOR AMERICA'S POSITION", 960, 680, 30, { weight: 800, ls: '.18em', color: '#C9CFDA' }); fin(sub, A("called America's", -.1), .4); }

  // 10. London gold pool collapses, 1968
  { const tCol = A('the gold pool collapsed'); const S = mapShot(tPlug, tEnd, { tr: 'slide' }); camSet(S, -0.13, 51.5, 2.2); camTo(S, -0.13, 51.5, 3.6, tPlug, tEnd - tPlug + .3, 'sine.inOut');
    pin(S, -0.13, 51.5, A('shared gold pool', -.2), { r: 10, rep: 2 }); mlabel(S, 'LONDON', -0.13, 51.5, A('in London', -.1), { fs: 22 });
    lower(S, 'PLUGGING THE LEAKS', 'A shared gold pool in *London*', tPlug + .1, { size: 70, y: 300 });
    const sw = I(S, '+ EMERGENCY SWAPS BETWEEN CENTRAL BANKS', 124, 860, 28, { align: 'left', weight: 800, ls: '.14em', color: '#C9CFDA' }); fin(sw, A('emergency swaps'), .4);
    const y = I(S, '1968', 1440, 640, 200, { weight: 900, color: '#E2614B' }); stamp(y, A('In 1968', -.05), { r: -6 });
    const crack = sv('path', { d: 'M960,120 L930,260 L990,360 L940,480 L1000,600 L955,720 L985,900', fill: 'none', stroke: '#E2614B', 'stroke-width': 7, 'stroke-linejoin': 'round', opacity: 0 }, S.svg);
    draw(crack, tCol, .35); sfx('crack', tCol + .1, .8); shake(tCol + .2, 1.2); flash(tCol + .2, .2); }
}
