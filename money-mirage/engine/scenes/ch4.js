// CHAPTER 4: THE DOLLAR BECOMES THE WORLD'S GOLD (lines 23-28)
function ch4() {
  const t0 = CH(4).a - .3, tPlan = A('The plan'), tWhy = A('Why the dollar'), tSud = A('Suddenly the dollar'), tTrap = A('But there was a trap'),
    tFr = A('France noticed'), tMin = A('Its finance minister'), tPl = A('America plugged'), tEnd = LB(28) + .35;
  startCh(4);

  // 1. July 1944, 44 countries, Bretton Woods (map)
  { const S = mapShot(t0, tPlan, { tr: 'fade' }); camSet(S, -30, 30, 1.0);
    camTo(S, -45, 38, 1.15, t0, A('and delegates') - t0, 'sine.inOut');
    const t = T(S, 'July *1944*', 960, 170, 110); kin(t, t0 + .2, { times: wordTimes('July 1944').map((x, i) => Math.max(t0 + .2, x)) });
    const sub = T(S, 'The Second World War is still raging', 960, 280, 48, { color: '#8D98B0' }); kin(sub, A('The Second World War'));
    out([t, sub], A('and delegates', -.1), .3);
    const fl = G(S, {}); tl.set(fl, { opacity: 1 }, 0); const COLS = [['#E2614B', '#F3EBDD', '#3B5384'], ['#7FB58A', '#F3EBDD', '#E9B44C'], ['#3B5384', '#E9B44C', '#E2614B'], ['#F3EBDD', '#E2614B', '#7FB58A']];
    const tD = A('delegates from 44');
    for (let k = 0; k < 44; k++) { const c = k % 11, r = Math.floor(k / 11); const x = 440 + c * 96, y = 300 + r * 74; const f = sv('g', {}, fl);
      const cs = COLS[(k * 7 + r) % 4]; for (let s = 0; s < 3; s++) sv('rect', k % 2 ? { x: x + s * 26, y, width: 26, height: 54, fill: cs[s] } : { x, y: y + s * 18, width: 78, height: 18, fill: cs[s] }, f);
      sv('rect', { x, y, width: 78, height: 54, fill: 'none', stroke: '#0A1120', 'stroke-width': 3 }, f);
      gsap.set(f, { autoAlpha: 0 }); tl.fromTo(f, { autoAlpha: 0, y: -40, rotation: -30, transformOrigin: '50% 100%' }, { autoAlpha: 1, y: 0, rotation: 0, duration: .3, ease: 'back.out(2)', ...IR }, tD + k * .035); }
    sfx('flip', tD, .5); sfx('flip', tD + .6, .5); sfx('flip', tD + 1.2, .5); ev(tD, 'flags');
    const n = I(S, '0', 960, 650, 110, { weight: 900, color: '#E9B44C' }); fin(n, A('44 countries'), .2); count(n, 0, 44, A('44 countries'), 1.0);
    const nl = I(S, 'COUNTRIES', 960, 730, 34, { weight: 800, ls: '.3em', color: '#F3EBDD' }); fin(nl, A('44 countries', .2));
    const tH = A('hotel in'); out([fl, n, nl], tH, .3); camTo(S, -71.44, 44.26, 4.5, tH, 1.4, 'power3.inOut');
    pin(S, -71.44, 44.26, A('Bretton Woods'), { r: 7 }); mlabel(S, 'BRETTON WOODS', -71.44, 44.26, A('Bretton Woods', .2), { fs: 9, dy: -9 });
    const ht = E(S, '🏨', 1300, 640, 150); pop(ht, A('hotel in', .4));
    const hol = E(S, '🏖️', 620, 640, 150); pop(hol, A('Not for a holiday'));
    const x = sv('path', { d: 'M530,550 L710,730 M710,550 L530,730', stroke: '#E2614B', 'stroke-width': 22, 'stroke-linecap': 'round', opacity: 0 }, S.svg); stamp(x, A('holiday', .1), { r: 0 }); }

  // 2. the peg diagram
  { const tSw = A('swappable by'); const S = shot(tPlan, tWhy, { tr: 'slide' }); const g = G(S, { opacity: 1 });
    const t = T(S, 'The *plan*', 960, 130, 76); kin(t, tPlan);
    const cur = [['£', 360, 300], ['₣', 300, 520], ['…', 360, 740]]; const cg = [];
    cur.forEach(([m, x, y], k) => { const c = coin(g, x, y, 70, { mark: m, fill: '#C9CFDA' }); cg.push(c); pop(c, A('other currencies', k * .2), { sfx: k ? false : 'pop' }); });
    const usd = coin(g, 960, 520, 120, { mark: '$' }); const gb = goldBar(g, 1560, 530, 1.6);
    const links = cur.map(([, x, y]) => arrowPath(g, `M${x + 80},${y} Q${(x + 830) / 2},${(y + 520) / 2 + (y < 520 ? -40 : y > 520 ? 40 : 0)} 830,520`, { w: 8 }));
    links.forEach((l, k) => draw(l, A('peg to the dollar', -.3 + k * .15), .5)); pop(usd, A('peg to the dollar'), { sfx: 'clink' });
    tl.to(cg, { x: 30, duration: .18, yoyo: true, repeat: 3, ease: 'sine.inOut' }, A('peg to the dollar', .5)); sfx('boing', A('peg to the dollar', .5), .5);
    const l2 = arrowPath(g, 'M1090,520 L1400,525', { w: 12 }); draw(l2, A('pegs to gold'), .5); pop(gb, A('pegs to gold', .3), { sfx: 'clink' });
    const tag = I(S, '35 dollars / oz', 1250, 430, 42, { weight: 800, color: '#E9B44C' }); pop(tag, A('at 35'));
    const sw = E(S, '🏛️', 1250, 760, 100); pop(sw, tSw); const swl = T(S, 'swappable by foreign governments', 1250, 850, 34, { color: '#8D98B0' }); kin(swl, tSw);
    const loop = arrowPath(g, 'M1080,620 Q1250,720 1420,630', { w: 6, hc: 'l', c: '#F3EBDD' }); draw(loop, tSw + .2, .5); }

  // 3. why the dollar? ~3/4 of official gold
  { const S = shot(tWhy, tSud, { tr: 'zoom' }); const g = G(S, { opacity: 1 });
    const t = T(S, 'Why the *dollar?*', 960, 130, 80); kin(t, tWhy, { times: wordTimes('Why the dollar') });
    const R = 230, C = 2 * Math.PI * (R / 2); sv('circle', { cx: 760, cy: 520, r: R, fill: '#26344F' }, g);
    const pie = sv('circle', { cx: 760, cy: 520, r: R / 2, fill: 'none', stroke: '#E9B44C', 'stroke-width': R, 'stroke-dasharray': C, 'stroke-dashoffset': C, transform: 'rotate(-90 760 520)' }, g);
    tl.fromTo(pie, { attr: { 'stroke-dashoffset': C } }, { attr: { 'stroke-dashoffset': C * .25 }, duration: 1.4, ease: 'power2.out', ...IR }, A('held about'));
    const us = E(S, '🇺🇸', 1300, 420, 120); pop(us, A('America held'));
    const l1 = T(S, '*~3/4* of the world\'s', 1340, 560, 58); kin(l1, A('three quarters')); const l2 = T(S, 'official gold', 1340, 640, 58); kin(l2, A('official gold'));
    sfx('sparkle', A('official gold'), .6); }

  // 4. as good as gold, and you could invest it; gold just sits there
  { const tSits = A('Gold just sits'); const S = shot(tSud, tTrap, { tr: 'up' }); const g = G(S, { opacity: 1 });
    const n = note(g, 560, 470, 380, { num: '1' }); pop(n, tSud); const eq = T(S, '=', 960, 470, 160, { color: '#E9B44C' }); kin(eq, A('as good as gold'), { sfx: 'pop' });
    const gb = goldBar(g, 1360, 480, 1.7); pop(gb, A('as good as gold', .3), { sfx: 'clink' });
    const t = T(S, 'As good as *gold...*', 960, 160, 70); kin(t, A('as good as gold'));
    out(t, A('and better'), .2); const t2 = T(S, '...and *better* in one way', 960, 160, 70); kin(t2, A('and better'));
    const up = E(S, '📈', 560, 730, 130); pop(up, A('invest dollars')); const il = I(S, 'invest it', 560, 830, 38, { weight: 800, color: '#7FB58A' }); pop(il, A('invest dollars', .2), { sfx: false });
    const sun = E(S, '😎', 1360, 330, 150); pop(sun, A('looking expensive'), { y0: -120, sfx: 'boing' });
    const gl = sv('rect', { x: 1150, y: 380, width: 70, height: 220, fill: 'rgba(255,246,226,.75)', transform: 'skewX(-20)', style: 'filter: blur(6px)', opacity: 0 }, g);
    tl.fromTo(gl, { opacity: 0, x: 0 }, { keyframes: [{ opacity: 1, x: 150, duration: .3 }, { opacity: 0, x: 380, duration: .3 }], ...IR }, A('expensive', .1)); sfx('sparkle', A('expensive', .1));
    const sl = T(S, 'Gold just *sits* there', 1360, 790, 46, { color: '#8D98B0' }); kin(sl, tSits); }

  // 5. the trap: dollars pile up overseas, the gold stays fixed; Triffin dilemma
  { const tTr = A('Economists call this'); const S = shot(tTrap, tFr, { tr: 'wipe' }); const g = G(S, { opacity: 1 });
    const t = T(S, 'A *trap* built in', 960, 120, 72); kin(t, tTrap);
    const vt = sv('rect', { x: 200, y: 300, width: 500, height: 420, rx: 22, fill: '#16233D', stroke: '#2A3A5C', 'stroke-width': 3 }, g); fin(vt, A('To give the world')); const vl = I(S, 'AMERICAN VAULTS', 450, 760, 34, { weight: 800, ls: '.2em', color: '#8D98B0' }); fin(vl, A('To give the world'));
    const st = G(S, {}); for (let k = 0; k < 4; k++) goldBar(st, 450, 650 - k * 72, .95, { label: false }); fin(st, A('To give the world', .2));
    const ov = I(S, 'OVERSEAS', 1450, 760, 34, { weight: 800, ls: '.2em', color: '#8D98B0' }); fin(ov, A('sending them abroad'));
    const arr = arrowPath(g, 'M720,450 Q960,330 1200,450', { w: 10, hc: 's', c: '#7FB58A' }); draw(arr, A('sending them abroad', -.3), .6);
    for (let k = 0; k < 12; k++) { const c = k % 3, r = Math.floor(k / 3); const nn = note(g, 1330 + c * 120 + (r % 2) * 30, 690 - r * 70, 150, {}); pop(nn, A('piled up', -.6 + k * .2), { s0: .3, y0: -80, sfx: k % 3 ? false : 'pop', vol: .4 }); }
    const cov = I(S, 'gold per dollar abroad ↓', 960, 230, 40, { weight: 800, color: '#E2614B' }); pop(cov, A('the less the gold'));
    tl.to(st, { opacity: .45, duration: .6 }, A('could cover them'));
    const card = P(S, 560, 380, 800, 200, { bg: '#F3EBDD', border: '#E2614B' }); const ci = mk('div', {}, card);
    ci.innerHTML = '<div style="font:900 30px Inter;color:#E2614B;text-align:center;margin-top:34px;letter-spacing:.3em">ECONOMISTS CALL IT</div><div style="font:800 76px Brico;color:#101A2E;text-align:center;white-space:nowrap">The Triffin dilemma</div>';
    stamp(card, A('Triffin', -.3), { r: -3, amp: .8 }); }

  // 6. France noticed: January 1965, 300 million dollars -> gold (map)
  { const S = mapShot(tFr, tMin, { tr: 'zoom' }); camSet(S, -38.5, 40, .85); camTo(S, -38.5, 40, .88, tFr, tMin - tFr, 'sine.inOut');
    pin(S, 2.35, 48.86, tFr, { r: 18 }); mlabel(S, 'FRANCE', 2.35, 48.86, tFr + .2, { fs: 40, dy: -36 });
    pin(S, -77.04, 38.9, A('swap at least', -.4), { r: 18, c: '#F3EBDD' }); mlabel(S, 'USA', -77.04, 38.9, A('swap at least', -.2), { fs: 40, dy: -36 });
    const t = T(S, 'France *noticed*', 960, 150, 76); kin(t, tFr, { times: wordTimes('France noticed') });
    const jd = I(S, 'JANUARY 1965', 960, 250, 40, { weight: 800, ls: '.25em', color: '#E9B44C' }); pop(jd, A('January 1965'));
    marc(S, 2.35, 48.86, -77.04, 38.9, A('300 million'), 1.0, { c: '#7FB58A', w: 12, bend: .03 });
    const amt = T(S, 'At least *300 million* dollars', 960, 700, 64); kin(amt, A('at least 300'));
    const back = marc(S, -77.04, 38.9, 2.35, 48.86, A('for American gold'), 1.0, { c: '#E9B44C', w: 12, bend: .09 });
    const gb = goldBar(S.svg, 1500, 560, .9); pop(gb, A('American gold', .5), { sfx: 'clink' }); }

  // 7. "exorbitant privilege" quote card
  { const S = shot(tMin, tPl, { tr: 'fade', push: 1.04 });
    const q = T(S, '“', 420, 330, 300, { color: '#E9B44C' }); pop(q, tMin, { sfx: 'whoosh' });
    const who = I(S, "France's finance minister", 960, 330, 40, { weight: 600, color: '#8D98B0' }); fin(who, A('finance minister'));
    const nm = T(S, "Valéry Giscard d'Estaing", 960, 410, 58); kin(nm, A('Valéry'));
    const qt = T(S, '*"Exorbitant privilege"*', 960, 600, 120); kin(qt, A('exorbitant'), { times: wordTimes('exorbitant privilege'), sfx: 'sting', vol: .5 });
    const line = sv('path', { d: 'M520,690 L1400,690', stroke: '#E2614B', 'stroke-width': 8, 'stroke-linecap': 'round', opacity: 0 }, S.svg); draw(line, A('privilege', .2), .5); }

  // 8. the London gold pool cracks (1968)
  { const t68 = A('In 1968'); const S = shot(tPl, tEnd, { tr: 'slide' }); const g = G(S, { opacity: 1 });
    const t = T(S, 'Plugging the *leaks*', 960, 120, 70); kin(t, tPl);
    const pool = G(S, {}); sv('ellipse', { cx: 960, cy: 520, rx: 420, ry: 130, fill: '#16233D', stroke: '#C9CFDA', 'stroke-width': 10 }, pool);
    const gold = sv('ellipse', { cx: 960, cy: 525, rx: 390, ry: 110, fill: '#E9B44C' }, pool); svgT(pool, 'LONDON GOLD POOL', 960, 540, 44, { c: '#7A4E0E', font: 'Inter', w: 900, ls: '.14em' });
    pop(pool, A('shared gold pool'), { s0: .6, sfx: 'clink' }); const uk = E(S, '🇬🇧', 960, 300, 100); pop(uk, A('London'));
    const b1 = E(S, '🏦', 300, 760, 120), b2 = E(S, '🏦', 1620, 760, 120); pop(b1, A('emergency swaps')); pop(b2, A('emergency swaps', .2), { sfx: false });
    const sw1 = arrowPath(g, 'M400,740 Q960,640 1520,740', { w: 8, hc: 'l', c: '#F3EBDD' }), sw2 = arrowPath(g, 'M1520,800 Q960,900 400,800', { w: 8, hc: 'l', c: '#F3EBDD' });
    draw(sw1, A('central banks', -.4), .6); draw(sw2, A('central banks', -.1), .6);
    stamp(T(S, '_1968_', 1500, 300, 110, { color: '#E2614B' }), t68, { r: 8 });
    const crack = sv('path', { d: 'M700,420 L780,500 L740,560 L860,620 M1180,420 L1120,520 L1200,580 L1140,640', stroke: '#0A1120', 'stroke-width': 10, fill: 'none', 'stroke-linejoin': 'round', opacity: 0 }, G(S, { opacity: 1 }));
    const tC = A('the gold pool collapsed'); draw(crack, tC, .3); shake(tC + .1, 1.6); sfx('crack', tC); flash(tC + .1, .3);
    tl.to(gold, { attr: { ry: 6, rx: 120 }, duration: .6, ease: 'power2.in' }, tC + .2); }
}
