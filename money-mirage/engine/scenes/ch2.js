// CHAPTER 2: PAPER ARRIVES (lines 11-16, Bill on 14)
function c2_anvil(parent, x, y, s) { const g0 = sv('g', { transform: `translate(${x},${y}) scale(${s})` }, parent); const g = sv('g', {}, g0);
  sv('path', { d: 'M-120,-50 L110,-50 Q150,-50 170,-80 L170,-30 Q140,0 80,0 L60,0 L60,40 L100,70 L-90,70 L-50,40 L-50,0 L-100,0 Q-120,-10 -120,-50 Z', fill: '#5A6378', stroke: '#1E2433', 'stroke-width': 7, 'stroke-linejoin': 'round' }, g);
  sv('path', { d: 'M-100,-40 L100,-40', stroke: '#8D98B0', 'stroke-width': 6, 'stroke-linecap': 'round' }, g); return g; }
function c2_vault(parent, x, y, s) { const g0 = sv('g', { transform: `translate(${x},${y}) scale(${s})` }, parent); const g = sv('g', {}, g0);
  sv('rect', { x: -170, y: -170, width: 340, height: 340, rx: 24, fill: '#3A4766', stroke: '#1E2433', 'stroke-width': 8 }, g);
  sv('rect', { x: -140, y: -140, width: 280, height: 280, rx: 14, fill: '#26344F', stroke: '#5A6A8E', 'stroke-width': 5 }, g);
  const dial = sv('g', {}, g); sv('circle', { cx: 0, cy: 0, r: 70, fill: '#8D98B0', stroke: '#1E2433', 'stroke-width': 7 }, dial);
  for (let k = 0; k < 4; k++) sv('path', { d: `M0,0 L${Math.cos(k * 1.571) * 60},${Math.sin(k * 1.571) * 60}`, stroke: '#1E2433', 'stroke-width': 10, 'stroke-linecap': 'round' }, dial);
  sv('circle', { cx: 0, cy: 0, r: 16, fill: '#E9B44C' }, dial); return { g, dial }; }
function c2_shimmer(el, a, b) { const o = { t: 0 }; tl.fromTo(o, { t: 0 }, { t: b - a, duration: Math.max(.1, b - a), ease: 'none', ...IR, onUpdate: () => gsap.set(el, { skewX: Math.sin(o.t * 7) * 6, scaleY: 1 + Math.sin(o.t * 5.3) * .04, filter: `blur(${(1.2 + Math.sin(o.t * 4.1) * 1.2).toFixed(2)}px)` }) }, a); }

function ch2() {
  const c0 = CH(2).a - .3;
  const t2 = A('the local coins'), t3 = A('So merchants left'), t4 = A('When some of those'), t4b = A('the Song government'), t5 = A('Then it discovered'),
    t6 = A("That's the first mirage"), t7 = A('Europe caught on'), t8 = A('Bank of England notes'), t9 = A('Paper was the ticket'), tEnd = LB(16) + .35;
  startCh(2);

  // 1. map flight from Lydia to Chengdu
  { const S = mapShot(c0, t2, { tr: 'fade' });
    camSet(S, 28.5, 38.8, 3.6); camTo(S, 66, 36, 1.1, c0 + .3, 1.3, 'power2.inOut'); camTo(S, 104.07, 30.67, 4.6, A('in Chengdu') - .5, 1.6, 'power3.inOut');
    const y = T(S, 'About *1,000 years* ago', 960, 150, 72); kin(y, A('About a thousand'));
    pin(S, 104.07, 30.67, A('Chengdu'), { r: 10 }); mlabel(S, 'CHENGDU', 104.07, 30.67, A('Chengdu', .1), { fs: 22, c: '#E9B44C' });
    mlabel(S, 'SICHUAN, CHINA', 103.5, 29.6, A('Sichuan'), { fs: 16, dy: 26 }); }

  // 2. iron coins: heavy, not worth much, a small anvil
  { const tA = A('Carrying your savings'), tV = A('small anvil'); const S = shot(t2, t3, { tr: 'zoom' });
    const t = T(S, 'Coins made of *iron*', 960, 150, 70); kin(t, A('the local coins'));
    const cs = []; for (let k = 0; k < 7; k++) { const c = coin(S.svg, 960 + (k % 2 ? 6 : -6), 700 - k * 46, 110, { fill: '#8A8F99' }); pop(c, A('made of iron') + k * .1, { sfx: 'clink', vol: .4, y0: -200, s0: 1 }); cs.push(c); }
    const h = T(S, '_Heavy_', 560, 470, 80); stamp(h, A('Heavy,'), { r: -8, sfx: 'thud' });
    const w = T(S, 'not worth much', 1380, 470, 56, { color: '#8D98B0', font: 'Inter', weight: 800 }); kin(w, A('not worth much'));
    tl.to(cs, { opacity: 0, y: 200, duration: .35, stagger: .03, ease: 'power2.in' }, tA - .2); tl.to([h, w], { opacity: 0, duration: .3 }, tA - .2);
    const pr = E(S, '🚶', 820, 650, 230); pop(pr, tA, { x0: -300 });
    const sv1 = T(S, 'Your *savings...*', 960, 300, 64); kin(sv1, tA);
    const an = c2_anvil(S.svg, 830, 545, .9); tl.set(an, { opacity: 0 }, 0);
    tl.fromTo(an, { opacity: 1, y: -700 }, { y: 0, duration: .4, ease: 'power4.in', ...IR }, tV - .25); sfx('thud', tV + .15, 1); shake(tV + .15, 1.8);
    tl.to(pr, { scaleY: .8, scaleX: 1.12, transformOrigin: '50% 100%', duration: .15 }, tV + .15); const sw = E(S, '😵', 660, 470, 90); pop(sw, tV + .3); }

  // 3. merchants deposit coins, carry paper: jiaozi
  { const S = shot(t3, t4, { tr: 'slide' });
    const m = E(S, '🧑', 420, 520, 220); pop(m, A('merchants'), { y0: 60 }); const sh = E(S, '🏛️', 1500, 500, 240); pop(sh, A('trusted businesses'), { y0: 60 });
    const lb = I(S, 'TRUSTED BUSINESS', 1500, 690, 34, { color: '#8D98B0', ls: '.2em', weight: 800 }); pop(lb, A('trusted businesses', .2), { sfx: false });
    const a1 = arrowPath(S.svg, 'M600,430 Q960,300 1320,430', { w: 10 }); draw(a1, A('left their coins'), .7);
    for (let k = 0; k < 3; k++) { const c = coin(S.svg, 600, 430, 32, { fill: '#8A8F99' }); tl.set(c, { opacity: 0 }, 0); tl.fromTo(c, { opacity: 1, x: 0, y: 0 }, { x: 720, y: 0, opacity: 0, duration: .9, ease: 'power1.inOut', ...IR }, A('left their coins') + .2 + k * .2); }
    const a2 = arrowPath(S.svg, 'M1320,640 Q960,760 600,640', { w: 10, c: '#7FB58A', hc: 's' }); draw(a2, A('carried paper notes'), .7);
    const n = note(S.svg, 960, 700, 170, {}); pop(n, A('paper notes'), { y0: 30 });
    const j = T(S, '*Jiaozi*', 960, 200, 120); kin(j, A('jiaozi'), { s0: .3, sfx: 'pop' }); const js = T(S, 'paper notes', 960, 300, 44, { color: '#8D98B0', font: 'Inter', weight: 800 }); kin(js, A('jiaozi', .2)); }

  // 4a. some businesses went bust
  { const S = shot(t4, t4b, { tr: 'up' });
    const sh = E(S, '🏛️', 960, 470, 280); pop(sh, t4, { y0: 40 });
    tl.to(sh, { rotation: 14, y: 60, transformOrigin: '50% 100%', duration: .4, ease: 'power3.in' }, A('went bust')); sfx('crack', A('went bust'));
    const b = T(S, '_BUST_', 1300, 330, 110); stamp(b, A('went bust'), { r: -10 }); }

  // 4b. timeline 1023 / 1024: first government paper money
  { const S = shot(t4b, t5, { tr: 'wipe' });
    const t = T(S, 'The *Song government* takes over', 960, 170, 64); kin(t, t4b);
    const ln = sv('path', { d: 'M300,520 L1620,520', stroke: '#3A4766', 'stroke-width': 10, 'stroke-linecap': 'round', opacity: 0 }, S.svg); draw(ln, t4b + .2, .9);
    [['1023', 720, A('1023')], ['1024', 1200, A('1024')]].forEach(([y, x, at]) => { const d = sv('circle', { cx: x, cy: 520, r: 26, fill: '#E9B44C', stroke: '#0A1120', 'stroke-width': 8 }, S.svg); pop(d, at, { sfx: 'ping' });
      const l = T(S, `*${y}*`, x, 420, 84); kin(l, at, { s0: .4, sfx: false }); });
    const s1 = I(S, 'takes over', 720, 610, 34, { color: '#8D98B0', weight: 800 }); pop(s1, A('1023', .2), { sfx: false });
    const n = note(S.svg, 1200, 680, 190, {}); pop(n, A('1024', .4));
    const f = T(S, "World's first *government paper money*", 960, 830, 58); kin(f, A("the world's first"), { times: wordTimes("world's first government paper money") }); }

  // 5. printing temptation: notes pile up, prices rise; Bill cameo
  { const tPr = A('Prices kept rising'); const S = shot(t5, t6, { tr: 'zoom' });
    const t = T(S, 'The oldest *temptation*', 960, 150, 70); kin(t, A('the oldest temptation'), { times: wordTimes('the oldest temptation') });
    const press = sv('g', { opacity: 0 }, S.svg); sv('rect', { x: 260, y: 380, width: 360, height: 300, rx: 20, fill: '#3A4766', stroke: '#1E2433', 'stroke-width': 8 }, press);
    sv('rect', { x: 300, y: 330, width: 280, height: 70, rx: 10, fill: '#8D98B0', stroke: '#1E2433', 'stroke-width': 6 }, press); svgT(press, 'PRINT', 440, 560, 54, { c: '#E9B44C', font: 'Inter', w: 900, ls: '.2em' });
    slideIn(press, t5 + .4, -400, 0);
    const q = T(S, 'Why not print a little *more?*', 960, 270, 60); kin(q, A('why not print'), { times: wordTimes('why not print a little more') });
    const ns = []; for (let k = 0; k < 9; k++) { const n = note(S.svg, 820 + (k % 3) * 40, 690 - k * 34, 220, {}); tl.set(n, { opacity: 0 }, 0); ns.push(n);
      tl.fromTo(n, { opacity: 1, x: -260, rotation: -20 }, { x: 0, rotation: (k % 2 ? 4 : -4), duration: .3, ease: 'power2.out', ...IR }, A('why not print', .8) + k * .3); sfx('flip', A('why not print', .8) + k * .3, .3); }
    tl.to(press, { y: 8, duration: .08, yoyo: true, repeat: 15 }, A('why not print', .8)); ev(A('Extra notes'), 'pop');
    const ch = sv('path', { d: 'M1250,700 L1370,660 L1450,600 L1530,480 L1620,330', fill: 'none', stroke: '#E2614B', 'stroke-width': 14, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', opacity: 0 }, S.svg);
    draw(ch, tPr, 1.0); const pl = T(S, '_PRICES_', 1440, 760, 56); kin(pl, tPr, { sfx: 'register' });
    charIn('B', LA(14) - .55, 'R'); idle('B', LA(14) - .1, t6 + .1); talk('B', 14);
    tl.to(CHR.B.M.sweat, { opacity: 1, y: 0, duration: .15 }, LA(14) + .1); tl.to(CHR.B.M.sweat, { y: 40, opacity: 0, duration: .9 }, LA(14) + .5);
    tl.to(CHR.B.body, { rotation: -6, transformOrigin: '50% 100%', duration: .25, yoyo: true, repeat: 1 }, A('they printed me'));
    tl.to([ch, pl], { opacity: .25, duration: .3 }, LA(14) - .5); charOut('B', t6 - .15); }

  // 6. the first mirage
  { const tBl = A('believe'); const S = shot(t6, t7, { tr: 'fade' });
    const t = T(S, 'The first *mirage*', 960, 330, 130); kin(t, A('the first mirage'), { times: wordTimes('the first mirage') }); c2_shimmer(t.ws[2], A('mirage'), t7 + .4);
    const n = note(S.svg, 960, 640, 300, { num: '1' }); pop(n, A('Paper only works'), { s0: .6 }); c2_shimmer(n, A('Paper only works'), t7 + .4);
    const glow = sv('circle', { cx: 960, cy: 640, r: 260, fill: 'rgba(233,180,76,.16)', opacity: 0 }, S.svg); S.svg.insertBefore(glow, S.svg.firstChild);
    fin(glow, tBl, .4); pulse(glow, tBl + .2, 1.15, 2);
    const b = T(S, 'only while people *believe*', 960, 830, 54); kin(b, A('Paper only works'), { times: [A('only'), A('while'), A('people'), A('believe')] }); }

  // 7a. Europe: London, 1694
  { const S = mapShot(t7, t8, { tr: 'slide' });
    camSet(S, 10, 49, 2.2); camTo(S, -0.13, 51.5, 5, t7 + .2, 1.8, 'power2.inOut');
    pin(S, -0.13, 51.5, A('From 1694') - .3, { r: 8 }); mlabel(S, 'LONDON', -0.13, 51.5, A('From 1694'), { fs: 18, c: '#E9B44C' });
    const y = T(S, '*1694*', 960, 170, 130); stamp(y, A('1694'), { r: -4 });
    const t = T(S, 'Europe catches on', 960, 830, 54, { color: '#C9CFDA' }); kin(t, t7); }

  // 7b. Bank of England notes promised to pay ... until 1931, in gold
  { const tG = A('pay out in gold'); const S = shot(t8, t9, { tr: 'up' });
    const n = note(S.svg, 760, 470, 760, { num: '£', text: 'I PROMISE TO PAY|THE BEARER' }); pop(n, t8, { s0: .7, sfx: 'whoosh' });
    const pr = T(S, '"...promised to pay the bearer"', 760, 150, 52, { color: '#E9B44C' }); kin(pr, A('promised to pay'), { times: [A('promised')].concat(wordTimes('to pay the bearer')) });
    const u = T(S, 'until *1931*', 1560, 290, 64); kin(u, A('until 1931'), { times: wordTimes('until 1931') });
    const ar = arrowPath(S.svg, 'M1170,470 L1400,470', { w: 14 }); draw(ar, tG - .4, .4);
    const gb = goldBar(S.svg, 1600, 480, 1.5); pop(gb, tG, { sfx: 'clink' }); const sp = E(S, '✨', 1720, 380, 80); pop(sp, tG + .2, { sfx: 'sparkle' }); }

  // 8. ticket and vault = gold standard
  { const S = shot(t9, tEnd, { tr: 'zoom' });
    const n = note(S.svg, 520, 470, 380, {}); pop(n, t9, { r0: -20 }); const tk = T(S, '*Ticket*', 520, 240, 70); kin(tk, A('the ticket'));
    const v = c2_vault(S.svg, 1400, 470, 1); pop(v.g, A('Gold sat'), { s0: .6, sfx: 'clang' }); tl.fromTo(v.dial, { attr: { transform: 'rotate(0)' } }, { attr: { transform: 'rotate(270)' }, duration: tEnd - A('Gold sat'), ease: 'power1.inOut', ...IR }, A('Gold sat'));
    for (let k = 0; k < 3; k++) { const gb = goldBar(S.svg, 1318 + k * 82, 585, .36, { label: false }); pop(gb, A('in the vault') + k * .12, { sfx: 'clink', vol: .4 }); }
    const vl = T(S, '*Vault*', 1400, 240, 70); kin(vl, A('in the vault'));
    const ar = arrowPath(S.svg, 'M760,470 L1160,470', { w: 10, head: true }); tl.set(ar, { attr: { 'stroke-dasharray': '22 16' } }, 0); fin(ar, A('Gold sat'), .3);
    const gs = T(S, '= a *gold standard*', 960, 790, 72); kin(gs, A("That's a gold standard"), { times: [A("That's"), A('a gold standard')].concat(wordTimes('gold standard')) }); }
}
