// CHAPTER 3: THE GOLD TRAP (lines 17-22) — archival / painted documentary style
const c3_top = S => S.stg.appendChild(S.svg); // keep the SVG layer (highlights, diagrams) above cards
const c3_dim = (S, o) => sv('rect', { x: 0, y: 0, width: 1920, height: 1080, fill: '#080C16', opacity: o == null ? .55 : o }, S.svg);
function ch3() {
  const t0 = CH(3).a - .3, tPanic = A('And in a panic'), tEmerg = A('So in emergencies'), tAm = A('America went further'), tHand = A('Americans had to hand'),
    tHoard = A('Hoard it'), tDin = A('Imagine explaining'), tYear = A('A year later'), tAnd74 = A("And Americans couldn't"), tOrd = A('So ordinary people'), tEnd = LB(22) + .35;
  startCh(3);

  // 1. calm times + the catch: money line capped by the gold line
  { const S = photo(t0, tPanic, 'bank_vault_1700s.jpg', { grade: 'paint', kb: [1.02, 1.12], from: [1, 0], to: [-1, -1], tr: 'fade' }); c3_dim(S, .62);
    const t1 = T(S, 'In calm times, it *worked*', 960, 170, 76); kin(t1, A('In calm times'), { times: wordTimes('In calm times, it worked') }); out(t1, A("But here's the catch", -.1));
    const g = sv('g', {}, S.svg); const X0 = 360, X1 = 1560, Y0 = 760, Y1 = 300;
    const ax = sv('path', { d: `M${X0},${Y1 - 20} L${X0},${Y0} L${X1 + 40},${Y0}`, fill: 'none', stroke: '#5A6782', 'stroke-width': 4, opacity: 0 }, g);
    const gold = sv('path', { d: `M${X0},${Y0 - 230} C${X0 + 400},${Y0 - 250} ${X0 + 800},${Y0 - 270} ${X1},${Y0 - 290}`, fill: 'none', stroke: '#E9B44C', 'stroke-width': 9, 'stroke-linecap': 'round', opacity: 0 }, g);
    const money = sv('path', { d: `M${X0},${Y0 - 40} C${X0 + 260},${Y0 - 70} ${X0 + 420},${Y0 - 210} ${X0 + 640},${Y0 - 252} C${X0 + 820},${Y0 - 268} ${X0 + 1000},${Y0 - 278} ${X1},${Y0 - 286}`, fill: 'none', stroke: '#F3EBDD', 'stroke-width': 7, 'stroke-dasharray': '1 0', 'stroke-linecap': 'round', opacity: 0 }, g);
    const lg = svgT(g, 'GOLD PILE', X1 + 30, Y0 - 300, 30, { anchor: 'start', c: '#E9B44C', font: 'Inter', w: 800, ls: '.14em' }); const lm = svgT(g, 'MONEY', X1 + 30, Y0 - 256, 30, { anchor: 'start', c: '#F3EBDD', font: 'Inter', w: 800, ls: '.14em' });
    const cap = sv('path', { d: `M${X0 + 600},${Y0 - 300} L${X0 + 700},${Y0 - 300}`, stroke: '#E2614B', 'stroke-width': 0, opacity: 0 }, g);
    fin(ax, A("But here's the catch"), .4); draw(gold, A('Money could only'), 1.0); pop(lg, A('Money could only', .8), { sfx: false });
    draw(money, A('grow as fast'), 1.6, { ease: 'power2.out' }); pop(lm, A('the gold pile'), { sfx: false }); sfx('thud', A('the gold pile', .2), .5);
    lower(S, "HERE'S THE CATCH", 'Money can only grow as fast as *gold*', A("But here's the catch", .3), { size: 64, y: 930 - 60 }); }

  // 2. the bank run
  { const S = photo(tPanic, tEmerg, 'bankrun_1931.jpg', { grade: 'mono', kb: [1.04, 1.18], from: [2, 2], to: [-2, -2], tr: 'fade', credit: 'Crowd outside the failed Bank of United States, New York · Library of Congress, NYWT&S · Public domain' });
    lower(S, 'NEW YORK · GREAT DEPRESSION', 'Everyone wants their *gold* back', A('everyone wants their', -.2), { size: 88 });
    const st = I(S, 'NOT ENOUGH FOR EVERYONE', 1440, 260, 46, { weight: 900, color: '#E2614B', ls: '.12em' }); stamp(st, A('never enough'), { r: -6, amp: .6 }); }

  // 3. emergencies, wars; Britain cuts the link in 1931
  { const tBr = A('Britain cut it'); const S = photo(tEmerg, tAm, 'boe_hall_1808.jpg', { grade: 'warm', kb: [1.08, 1.2], from: [0, 2], to: [2, -2], tr: 'slide', credit: 'Bank of England, Rowlandson & Pugin, 1808 · Public domain' });
    const l = lower(S, 'EMERGENCIES · ESPECIALLY WARS', 'Countries kept *suspending* the link', A('So in emergencies', .1), { size: 76 });
    tl.to([l.k, l.h], { autoAlpha: 0, duration: .3 }, tBr - .15); c3_dim(S, 0); const dim = S.svg.lastChild; tl.to(dim, { attr: { opacity: .55 }, duration: .4 }, tBr - .2);
    const k = I(S, 'BRITAIN CUTS THE LINK FOR GOOD', 960, 330, 32, { weight: 800, color: '#E9B44C', ls: '.3em' }); fin(k, tBr, .4);
    const y = T(S, '*1931*', 960, 520, 260); kin(y, A('1931', -.05), { s0: .6, dy: 0 }); sfx('stamp', A('1931', .1), .6); }

  // 4. America went further: Executive Order 6102
  { const S = photo(tAm, tHand, 'central_bank.jpg', { grade: 'paint', kb: [1.0, 1.14], to: [-2, -2], tr: 'fade' }); c3_dim(S, .35);
    const a1 = T(S, 'America went *further*', 960, 200, 88); kin(a1, tAm, { times: wordTimes('America went further') });
    const l = lower(S, 'APRIL 5, 1933 · THE GREAT DEPRESSION', 'Executive Order *6102*', A('On April 5th', .1), { size: 110 });
    const sub = I(S, 'Signed by President Franklin Roosevelt', 124, 900 - 30, 34, { align: 'left', color: '#C9CFDA' }); fin(sub, A('signed'), .4); sfx('typing', A('Executive Order', .2), .4); }

  // 5. the order itself: hand in gold by May 1, at 20.67 an ounce
  { const S = photo(tHand, tHoard, 'eo6102.jpg', { grade: 'mono', kb: [1.3, 1.36], tr: 'slide', credit: 'Executive Order 6102 notice, 1933 · U.S. Government Printing Office · Public domain' }); tl.set(S.img, { filter: GRADES.mono + ' blur(14px) brightness(.6)' }, tHand - .2);
    const c = card(S, 'eo6102.jpg', 1060, 70, 560, { filter: 'sepia(.25) contrast(1.05)' }); c3_top(S);
    slideIn(c, tHand, 0, 120, { d: .7 });
    hl(S, 1100, 242, 488, 60, A('gold coins'), {}); hl(S, 1104, 211, 480, 36, A('by May 1st', -.1), {});
    const l = lower(S, 'HAND IT IN BY MAY 1', 'Gold coins, bars and *certificates*', tHand + .2, { size: 58, x: 110, y: 560 });
    const p = I(S, '20.67', 120, 720, 120, { align: 'left', weight: 900, color: '#E9B44C' }); pop(p, A('at 20 dollars', -.1), { s0: .8, sfx: 'clink' });
    const u = I(S, 'DOLLARS AN OUNCE', 124, 800, 30, { align: 'left', weight: 800, ls: '.24em' }); fin(u, A('at 20 dollars', .3), .4); }

  // 6. the penalties
  { const S = photo(tHoard, tDin, 'eo6102.jpg', { grade: 'mono', kb: [1.3, 1.34], tr: 'fade' }); tl.set(S.img, { filter: GRADES.mono + ' blur(14px) brightness(.55)' }, tHoard - .2);
    const c = card(S, 'eo6102.jpg', 860, -820, 1000, { filter: 'sepia(.25) contrast(1.05)' }); c3_top(S); fin(c, tHoard - .1, .4);
    tl.fromTo(c, { y: 0 }, { y: -40, duration: tDin - tHoard + .5, ease: 'none', ...IR }, tHoard - .1);
    const box = hl(S, 912, 474, 900, 112, A('Hoard it', .4), { sw: 7 }); tl.fromTo(box, { y: 0 }, { y: -40, duration: tDin - tHoard + .5, ease: 'none', ...IR }, tHoard - .1);
    const f = I(S, '10,000-DOLLAR FINE', 110, 420, 64, { align: 'left', weight: 900, color: '#E2614B' }); pop(f, A('10,000-dollar fine', -.05), { s0: .8, sfx: 'stamp' });
    const j = I(S, 'UP TO 10 YEARS IN PRISON', 110, 520, 44, { align: 'left', weight: 900 }); pop(j, A('up to ten years'), { s0: .8, sfx: 'thud' });
    const b = I(S, 'OR BOTH.', 110, 610, 44, { align: 'left', weight: 900, color: '#E9B44C' }); pop(b, A('or both'), { s0: .8, sfx: false }); }

  // 7. dinner-party beat: awkward hold
  { const S = photo(tDin, tYear, 'tv_1971.jpg', { grade: 'paint', kb: [1.0, 1.22], from: [0, 0], to: [-6, 3], tr: 'fade' }); tl.set(S.img, { filter: GRADES.paint + ' sepia(.4) brightness(.7)' }, tDin - .2);
    sfx('crickets', A('dinner party', .4), .8); }

  // 8. a year later: price jumps to 35, each dollar = 41% less gold
  { const S = photo(tYear, tAnd74, 'fortknox_postcard.jpg', { grade: 'mono', kb: [1.06, 1.16], to: [-2, -1], tr: 'slide', credit: 'Fort Knox Bullion Depository, postcard · Tichnor Bros., Boston Public Library · Public domain' }); c3_dim(S, .45);
    const k = I(S, 'A YEAR LATER · OFFICIAL PRICE OF GOLD', 960, 170, 30, { weight: 800, color: '#E9B44C', ls: '.3em' }); fin(k, tYear, .4);
    const p = I(S, '20.67', 960, 320, 170, { weight: 900 }); fin(p, tYear + .2, .3); count(p, 20.67, 35, A('jumped to'), 1.0, { f: '2', ease: 'power3.inOut' });
    const u = I(S, 'DOLLARS AN OUNCE', 960, 430, 32, { weight: 800, ls: '.24em' }); fin(u, tYear + .4, .4);
    const sg = T(S, 'Same *gold.*', 960, 560, 72); kin(sg, A('Same gold'), { times: wordTimes('Same gold') });
    const g = sv('g', {}, S.svg); const bx = 560, bw = 800;
    const lb1 = svgT(g, 'GOLD PER DOLLAR · BEFORE', bx, 690, 24, { anchor: 'start', c: '#C9CFDA', font: 'Inter', w: 800, ls: '.16em' }); const b1 = sv('rect', { x: bx, y: 705, width: bw, height: 30, rx: 6, fill: '#E9B44C' }, g);
    const lb2 = svgT(g, 'AFTER', bx, 790, 24, { anchor: 'start', c: '#C9CFDA', font: 'Inter', w: 800, ls: '.16em' }); const b2 = sv('rect', { x: bx, y: 805, width: bw, height: 30, rx: 6, fill: '#E9B44C' }, g);
    const cut = sv('rect', { x: bx + bw * .59, y: 805, width: bw * .41, height: 30, rx: 6, fill: 'none', stroke: '#E2614B', 'stroke-width': 4, 'stroke-dasharray': '10 7', opacity: 0 }, g);
    const pct = svgT(g, '−41%', bx + bw + 30, 832, 46, { anchor: 'start', c: '#E2614B' });
    [lb1, b1, lb2, b2, pct].forEach(e => gsap.set(e, { autoAlpha: 0 })); tl.to([lb1, b1, lb2, b2], { autoAlpha: 1, duration: .4 }, A('But each dollar', -.1));
    tl.fromTo(b2, { attr: { width: bw } }, { attr: { width: bw * .59 }, duration: .9, ease: 'power2.inOut', ...IR }, A('41 percent', -.2)); fin(cut, A('41 percent', .4), .3); pop(pct, A('41 percent', .3), { sfx: 'thud' }); }

  // 9. the last day of 1974
  { const S = photo(tAnd74, tOrd, 'fortknox_vault.jpg', { grade: 'mono', kb: [1.1, 1.2], tr: 'fade', credit: 'Fort Knox Bullion Depository · Public domain' }); tl.set(S.img, { filter: GRADES.mono + ' blur(5px)' }, tAnd74 - .2); c3_dim(S, .4);
    const l = lower(S, 'PRIVATE GOLD BARS', 'Illegal to own until', tAnd74 + .1, { size: 72, y: 330 });
    const cal = P(S, 1150, 360, 420, 440, { bg: '#F3EBDD', border: '#C9CFDA' }); const inner = mk('div', {}, cal);
    inner.innerHTML = '<div style="background:#E2614B;height:96px;border-radius:18px 18px 0 0;color:#fff;font:800 46px Inter;display:flex;align-items:center;justify-content:center;letter-spacing:.14em">DECEMBER</div><div style="font:800 190px Inter;color:#101A2E;text-align:center;line-height:230px">31</div><div style="font:800 64px Inter;color:#101A2E;text-align:center;letter-spacing:.1em">1974</div>';
    slideIn(cal, A('the last day', -.3), 0, -260, { sfx: 'flip', d: .6 }); }

  // 10. re-hook: people locked out, governments not
  { const tGov = A('But foreign governments'), tLoop = A('And that loophole'); const S = photo(tOrd, tEnd, 'gold_window.jpg', { grade: 'paint', kb: [1.0, 1.12], to: [-1, -2], tr: 'fade' }); c3_dim(S, .3);
    const g = sv('g', {}, S.svg);
    const pp = svgT(g, 'ORDINARY PEOPLE', 520, 300, 40, { c: '#F3EBDD', font: 'Inter', w: 900, ls: '.18em' }); const lk = lock(g, 520, 490, 1.2); const lkx = svgT(g, 'LOCKED OUT', 520, 650, 34, { c: '#E2614B', font: 'Inter', w: 900, ls: '.2em' });
    const gv = svgT(g, 'FOREIGN GOVERNMENTS', 1400, 300, 40, { c: '#F3EBDD', font: 'Inter', w: 900, ls: '.18em' }); const op = svgT(g, 'STILL ALLOWED', 1400, 650, 34, { c: '#E9B44C', font: 'Inter', w: 900, ls: '.2em' });
    const gb = goldBar(g, 1400, 480, 1.3);
    pop(pp, tOrd + .2, { sfx: false }); pop(lk.g, A('locked out', -.1), { sfx: 'clang', vol: .6 }); pop(lkx, A('locked out', .2), { sfx: false });
    pop(gv, tGov, { sfx: false }); pop(gb, A("weren't", -.2), { sfx: 'clink' }); pop(op, A("weren't", .1), { sfx: false });
    tl.to([pp, lk.g, lkx, gv, gb, op], { autoAlpha: 0, duration: .35 }, tLoop - .1);
    const r = T(S, 'That loophole broke the *whole system*', 960, 470, 84); kin(r, tLoop, { times: wordTimes('that loophole is what eventually broke the whole system').filter((_, i) => ![2, 3, 4].includes(i)) }); sfx('crack', A('broke the whole', .1), .6); }
}
