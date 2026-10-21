// CHAPTER 5: THE SUNDAY IT CHANGED (lines 29-34) — archival/painted style
function c5_panel(S, x, y, w, h) { const d = mk('div', { class: 'panel' }, S.stg); Object.assign(d.style, { left: x + 'px', top: y + 'px', width: w + 'px', height: h + 'px', background: 'rgba(10,17,32,.82)', borderColor: 'rgba(233,180,76,.45)', backdropFilter: 'blur(4px)' }); d.style.visibility = 'hidden'; return d; }
function ch5() {
  const c = CH(5); const t0 = c.a - .3;
  const tCamp = A('President Richard Nixon'), tTV = A('he went on television'), tFz = A('A 90-day freeze'), tGW = A('And the big one'),
    tPause = A('Nixon pitched it'), tBill = LA(32) - .6, tNever = A('It never came back'), tFloat = A('By 1973'), tPuz = A('Which leaves a puzzle'),
    tExp = A("You'd expect"), tEnd = LB(34) + .35;
  startCh(5);

  // 1. the dam was cracking
  { const tCr = A('the dam was cracking'); const S = photo(t0, tCamp, 'central_bank.jpg', { grade: 'paint', kb: [1.12, 1.02], from: [0, -2], to: [0, 1] });
    lower(S, 'AUGUST 1971', 'The dam was *cracking*', A('By August 1971'));
    const crack = sv('path', { d: 'M1240,90 L1210,190 L1265,250 L1220,350 L1275,430 L1235,520 L1260,600', fill: 'none', stroke: '#E2614B', 'stroke-width': 7, 'stroke-linejoin': 'round', opacity: 0 }, S.svg);
    draw(crack, tCr + .3, .5); sfx('crack', tCr + .3, .7); shake(tCr + .5, .7); }
  // 2. Camp David weekend
  { const S = photo(tCamp, tTV, 'camp_david.jpg', { grade: 'mono', kb: [1.04, 1.16], to: [-2, -1], credit: 'Camp David · White House Photo Office · Public domain' });
    lower(S, 'CAMP DAVID', 'His economic team, *for the weekend*', A('took his economic team'), { size: 80 });
    const days = ['FRI', 'SAT', 'SUN']; days.forEach((d, i) => { const e = I(S, d, 1480 + i * 120, 200, 30, { weight: 800, ls: '.2em', color: i === 2 ? '#E2614B' : '#F3EBDD' }); fin(e, A('for the weekend', i * .25), .3); });
    sfx('tick', A('for the weekend'), .4); }
  // 3. Sunday, August 15th — on television
  { const S = photo(tTV, tFz, 'tv_1971.jpg', { grade: 'paint', kb: [1.0, 1.15], to: [-3, -2], tr: 'fade' });
    lower(S, 'SUNDAY, AUGUST 15TH', 'He went on *television*', A('And on Sunday', -.1)); sfx('static', tTV, .5); flash(tTV + .3, .15); }
  // 4. three announcements
  { const S = photo(tFz, tGW, 'tv_1971.jpg', { grade: 'paint', kb: [1.2, 1.28], from: [-4, -3], to: [-5, -4], tr: 'zoom' }); tl.set(S.img, { filter: GRADES.paint + ' blur(7px) brightness(.6)' }, tFz - .1);
    const items = [['01', '90-day freeze', 'on wages and prices', A('A 90-day freeze')], ['02', '10% surcharge', 'on imports', A('A 10 percent surcharge')]];
    items.forEach(([n, h, s, at], i) => { const x = 220 + i * 760; const p = c5_panel(S, x, 300, 680, 360); slideIn(p, at, 0, 80, { sfx: 'swoosh' });
      const nn = I(S, n, x + 50, 380, 40, { align: 'left', color: '#E9B44C', weight: 900, ls: '.1em' }); fin(nn, at + .2);
      const hh = T(S, h, x + 46, 480, 78, { align: 'left' }); kin(hh, at + .25, { st: .06 }); const ss = I(S, s, x + 50, 580, 38, { align: 'left', color: '#C9CFDA' }); fin(ss, at + .5); }); }
  // 5. the big one: gold window closed
  { const tCl = A('the gold window was closed'); const S = photo(tGW, tPause, 'gold_window.jpg', { grade: 'paint', kb: [1.0, 1.12], to: [0, -2], tr: 'slide' });
    lower(S, '03 · THE BIG ONE', 'The gold window: *closed*', tGW, { size: 88 });
    const st = T(S, 'CLOSED', 1440, 300, 120, { color: '#E2614B' }); stamp(st, A('was closed', .1), { r: -6, sfx: 'clang' });
    const sub = I(S, 'Foreign governments: no more dollars for gold', 1440, 420, 34, { weight: 800, ls: '.04em' }); fin(sub, A('Foreign governments could no longer'), .5); }
  // 6. pitched as a pause + Bill
  { const S = photo(tPause, tNever, 'nixon_campdavid.jpg', { grade: 'mono', kb: [1.05, 1.15], to: [1, -1], tr: 'fade', credit: 'Richard Nixon at Camp David, 1971 · White House Photo Office · Public domain' });
    lower(S, null, 'Pitched as a *pause*', tPause, { size: 90, y: 300 });
    const sub = T(S, 'Gold to return once the system was fixed', 120, 420, 48, { align: 'left', color: '#C9CFDA' }); kin(sub, A('with gold to return'), { st: .05 });
    tl.to(S.img, { filter: GRADES.mono + ' blur(6px) brightness(.7)', duration: .5 }, tBill - .2);
    charIn('B', tBill, 'R'); idle('B', tBill + .5, tNever + .9); talk('B', 32);
    tl.to(CHR.B.M.brow, { y: -10, duration: .25 }, LA(32)); tl.to(CHR.B.M.brow, { y: 6, duration: .3 }, tNever + .1);
    tl.to(CHR.B.body, { scaleY: .9, transformOrigin: '50% 100%', transformBox: 'fill-box', duration: .4, ease: 'power2.out' }, tNever + .15); }
  // 7. it never came back; 1973 floating currencies
  { const S = photo(tNever, tPuz, 'trading_room.jpg', { grade: 'paint', kb: [1.02, 1.14], to: [-2, -1], tr: 'fade' }); tl.set(S.img, { filter: GRADES.paint + ' brightness(.55)' }, tNever - .1);
    charOut('B', tNever + 1.0);
    const h = T(S, 'It *never* came back', 960, 220, 104); kin(h, tNever, { times: wordTimes('It never came back') }); tl.to(h, { autoAlpha: 0, duration: .3 }, tFloat - .2);
    lower(S, '1973', 'Currencies *float*', tFloat, { y: 230, size: 96 });
    const cols = ['#E9B44C', '#F3EBDD', '#7FB58A', '#E2614B'], labs = ['DOLLAR', 'POUND', 'MARK', 'YEN'];
    cols.forEach((col, k) => { let d = ''; for (let x = 0; x <= 1680; x += 24) { const y = 520 + k * 70 + Math.sin(x / (90 + k * 23) + k) * (18 + k * 6) + Math.sin(x / 41 + k * 2) * 8; d += (x ? ' L' : 'M') + (120 + x) + ',' + y.toFixed(1); }
      const p = sv('path', { d, fill: 'none', stroke: col, 'stroke-width': 5, opacity: 0, 'stroke-linecap': 'round' }, S.svg); draw(p, tFloat + .3 + k * .2, 2.4, { ease: 'none' });
      const l = sv('text', { x: 1810, y: 520 + k * 70 + 8, 'font-size': 22, 'font-family': 'Inter', 'font-weight': 800, fill: col, 'text-anchor': 'end', opacity: 0, 'letter-spacing': '.12em' }, S.svg); l.textContent = labs[k]; fin(l, tFloat + 2.4 + k * .1, .4); });
    const m = I(S, 'Priced by markets, not metal', 960, 860, 40, { weight: 800, color: '#E9B44C' }); fin(m, A('priced by markets'), .5); }
  // 8. re-hook: a puzzle
  { const S = photo(tPuz, tExp, 'fortknox_postcard.jpg', { grade: 'mono', kb: [1.08, 1.0], tr: 'wipe', credit: 'Tichnor Bros., Boston Public Library · Public domain' });
    lower(S, 'A PUZZLE', 'No link to gold for *50+ years*', A('The dollar lost its last link'), { size: 84 });
    const ln = sv('path', { d: 'M520,330 L1400,330', stroke: '#E2614B', 'stroke-width': 10, 'stroke-dasharray': '26 18', opacity: 0 }, S.svg); draw(ln, A('lost its last link'), .6); tl.to(ln, { attr: { 'stroke-dashoffset': 200 }, opacity: .3, duration: 1 }, A('fifty years ago')); }
  { const S = photo(tExp, tEnd, 'trading_room.jpg', { grade: 'paint', kb: [1.15, 1.3], from: [-2, -2], to: [-3, -4], tr: 'zoom' }); tl.set(S.img, { filter: GRADES.paint + ' brightness(.5) blur(2px)' }, tExp - .1);
    const a1 = T(S, "You'd expect the world to *dump it*", 960, 320, 76); kin(a1, tExp, { st: .07 });
    const a2 = T(S, 'Instead, it became *even more central*', 960, 470, 76); kin(a2, A('Instead'), { st: .07 });
    const w = T(S, '_Why?_', 960, 680, 190); stamp(w, A('Why', -.05), { r: 0, sfx: 'thud' }); pulse(w, A('Why', .5), 1.06, 1); }
}
