// CHAPTER 5: THE SUNDAY IT CHANGED (lines 29-34)
function c5_tv(parent, x, y, s) { const g0 = sv('g', { transform: `translate(${x},${y}) scale(${s})` }, parent); const g = sv('g', {}, g0);
  sv('path', { d: 'M-60,-190 L-120,-280 M60,-190 L120,-280', stroke: '#C9CFDA', 'stroke-width': 7, 'stroke-linecap': 'round' }, g);
  sv('circle', { cx: -120, cy: -280, r: 9, fill: '#E9B44C' }, g); sv('circle', { cx: 120, cy: -280, r: 9, fill: '#E9B44C' }, g);
  sv('rect', { x: -300, y: -195, width: 600, height: 400, rx: 40, fill: '#7A4A28', stroke: '#2E190C', 'stroke-width': 8 }, g);
  sv('rect', { x: -265, y: -160, width: 420, height: 330, rx: 34, fill: '#0B1222', stroke: '#2E190C', 'stroke-width': 7 }, g);
  for (const ky of [-90, 10]) sv('circle', { cx: 225, cy: ky, r: 26, fill: '#C9CFDA', stroke: '#2E190C', 'stroke-width': 5 }, g);
  for (let k = 0; k < 4; k++) sv('rect', { x: 200, y: 70 + k * 18, width: 50, height: 8, rx: 4, fill: '#2E190C' }, g);
  sv('path', { d: 'M-230,205 L-250,250 M230,205 L250,250', stroke: '#2E190C', 'stroke-width': 10, 'stroke-linecap': 'round' }, g);
  const scr = sv('g', {}, g); const stat = sv('g', {}, scr);
  for (let k = 0; k < 16; k++) sv('rect', { x: -255 + ((k * 97) % 300), y: -150 + k * 20, width: 60 + ((k * 53) % 200), height: 6, fill: '#C9CFDA', opacity: .25 + ((k * 7) % 5) / 10 }, stat);
  const show = sv('g', { opacity: 0 }, scr);
  sv('rect', { x: -255, y: -150, width: 400, height: 310, rx: 26, fill: '#1B2C4D' }, show);
  svgT(show, 'SUNDAY', -55, -60, 40, { c: '#E2614B', font: 'Inter', w: 900, ls: '.2em' });
  svgT(show, 'AUG 15', -55, 30, 96, { c: '#F3EBDD' }); svgT(show, '1971', -55, 120, 70, { c: '#E9B44C' });
  return { g, stat, show }; }

function ch5() {
  const c0 = CH(5).a - .3, end = LB(34) + .35;
  const t2 = A('President Richard', -.4), t3 = A('And on Sunday', -.3), t4 = A('A 90-day', -.3), t5 = A('And the big one', -.2), t6 = A('Nixon pitched', -.3),
    t7 = A('It never came back', -.25), t8 = A('By 1973', -.2), t9 = A('Which leaves a puzzle', -.3);
  startCh(5);

  // 1. August 1971: the dam is cracking
  { const tc = A('cracking'); const S = shot(c0, t2, { tr: 'fade' }); const g = G(S, { opacity: 1 });
    const water = sv('rect', { x: 260, y: 330, width: 640, height: 470, fill: '#2C6E9E', opacity: .85 }, g);
    for (let k = 0; k < 8; k++) svgT(g, '$', 330 + (k % 4) * 150, 430 + Math.floor(k / 4) * 170, 70, { c: '#9FD3F2' });
    const wall = sv('g', {}, g);
    for (let r = 0; r < 8; r++) for (let c = 0; c < 4; c++) sv('rect', { x: 900 + c * 70 + (r % 2 ? 35 : 0) - 35, y: 240 + r * 70, width: 66, height: 66, rx: 6, fill: '#8D98B0', stroke: '#4B5570', 'stroke-width': 4 }, wall);
    sv('rect', { x: 860, y: 200, width: 290, height: 46, fill: '#6C7690' }, wall);
    slideIn(wall, c0 + .2, 0, 400, { sfx: 'thud' });
    const t = T(S, 'August *1971*', 960, 140, 92); kin(t, A('By August'));
    const cr = sv('path', { d: 'M900,300 L960,380 L930,450 L1010,520 L970,600 L1040,690 L1010,790', fill: 'none', stroke: '#E2614B', 'stroke-width': 9, 'stroke-linejoin': 'round', opacity: 0 }, g);
    draw(cr, tc - .1, .5); sfx('crack', tc); shake(tc + .2, 1.1);
    const sp = []; for (let k = 0; k < 3; k++) { const p = sv('path', { d: `M${1150},${400 + k * 140} Q${1320 + k * 40},${360 + k * 140} ${1420 + k * 60},${560 + k * 140}`, fill: 'none', stroke: '#9FD3F2', 'stroke-width': 18, 'stroke-linecap': 'round', opacity: 0 }, g); sp.push(p); draw(p, tc + .3 + k * .25, .6); }
    sfx('splash', tc + .35, .7);
    const k2 = T(S, 'The dam was *cracking*', 1500, 330, 56, { align: 'center' }); kin(k2, A('the dam'));
    tl.to(water, { attr: { y: 360, height: 440 }, duration: 1.5, ease: 'sine.inOut', yoyo: true, repeat: 1 }, tc + .2); }

  // 2. Camp David, the weekend
  { const S = mapShot(t2, t3, { tr: 'zoom' }); camSet(S, -77.2, 39.2, 2.2); camTo(S, -77.3, 39.4, 4.5, t2 + .1, 3.4, 'power2.inOut');
    pin(S, -77.04, 38.9, A('President Richard'), { r: 6, c: '#F3EBDD', rep: 1 }); mlabel(S, 'WASHINGTON', -77.04, 38.9, A('President Richard', .2), { fs: 15, dy: 26 });
    pin(S, -77.46, 39.65, A('Camp David', -.3), { r: 7 }); mlabel(S, 'CAMP DAVID', -77.46, 39.65, A('Camp David'), { fs: 13, c: '#E9B44C' });
    const t = T(S, 'Economic team · *the weekend*', 960, 150, 64); kin(t, A('economic team'));
    const cal = P(S, 1430, 640, 360, 180); const ch = mk('div', {}, cal); ch.innerHTML = '<div style="display:flex;gap:14px;padding:24px;justify-content:center">' + ['FRI', 'SAT', 'SUN'].map((d, i) => `<div style="width:92px;height:120px;border-radius:14px;background:${i === 2 ? '#E2614B' : '#26344F'};color:#F3EBDD;font:800 30px Inter;display:flex;align-items:center;justify-content:center">${d}</div>`).join('') + '</div>';
    slideIn(cal, A('for the weekend', -.2), 300, 0, { sfx: 'flip' }); }

  // 3. Sunday, August 15th: he went on television
  { const tTv = A('went on television'); const S = shot(t3, t4, { tr: 'wipe' }); const tv = c5_tv(S.svg, 960, 520, 1.15); pop(tv.g, t3 + .1, { s0: .6, sfx: 'thud' });
    tl.fromTo(tv.stat, { opacity: 0 }, { keyframes: [{ opacity: .9, duration: .08 }, { opacity: .3, duration: .08 }, { opacity: .9, duration: .08 }, { opacity: .5, duration: .1 }], ...IR }, A('Sunday, August', -.2)); sfx('static', A('Sunday, August', -.2), .6);
    tl.to(tv.stat, { y: 14, duration: .1, repeat: 12, yoyo: true, ease: 'none' }, A('Sunday, August', -.2));
    tl.to(tv.stat, { opacity: 0, duration: .15 }, tTv - .1); tl.fromTo(tv.show, { opacity: 0, scaleY: .02, transformOrigin: '50% 50%' }, { opacity: 1, scaleY: 1, duration: .3, ease: 'power3.out', ...IR }, tTv - .1); flash(tTv, .3); ev(tTv, 'tv');
    const t = T(S, 'On *television*', 960, 120, 70); kin(t, tTv - .2); }

  // 4. three announcements
  { const S = shot(t4, t5 + 1.3, { tr: 'up' });
    const cards = [['🧊', '90-DAY FREEZE', 'on wages & prices', A('90-day'), '#26344F'], ['🚢', '10% SURCHARGE', 'on imports', A('10 percent'), '#26344F'], ['🪟', 'GOLD WINDOW', 'closed', A('the big one', .3), '#5A2430']];
    cards.forEach(([em, h, sub, at, bgc], i) => { const x = 140 + i * 570; const p = P(S, x, 300, 500, 420, { bg: bgc, border: i === 2 ? '#E2614B' : '#3A4A6C' });
      const e = mk('div', { class: 'e' }, p); e.textContent = em; Object.assign(e.style, { fontSize: '120px', left: '190px', top: '50px' });
      const hd = mk('div', { class: 't' }, p); hd.textContent = h; Object.assign(hd.style, { fontSize: '50px', left: '0', right: '0', top: '220px', textAlign: 'center', color: i === 2 ? '#E2614B' : '#E9B44C' });
      const sb = mk('div', { class: 'i' }, p); sb.textContent = sub; Object.assign(sb.style, { fontSize: '36px', left: '0', right: '0', top: '300px', textAlign: 'center' });
      stamp(p, at - .25, { r: i === 1 ? 2 : -3, amp: i === 2 ? 1.5 : .8, sfx: i === 2 ? 'clang' : 'stamp' }); });
    const t = T(S, 'Three announcements', 960, 170, 60, { color: '#8D98B0' }); kin(t, t4 + .1);
    const big = T(S, '_The big one_', 1420, 820, 56); kin(big, A('the big one')); }

  // 5. the gold window shutter slams
  { const tCl = A('was closed', .1); const sA = t5 + 1.3; const S = shot(sA, t6, { tr: 'fade' }); const g = G(S, { opacity: 1 });
    sv('rect', { x: 560, y: 200, width: 800, height: 470, rx: 18, fill: '#16233D', stroke: '#C9CFDA', 'stroke-width': 10 }, g);
    for (let k = 0; k < 6; k++) goldBar(g, 700 + (k % 3) * 260, 470 + Math.floor(k / 3) * 110, .9, { label: false });
    const sign = svgT(g, 'GOLD WINDOW', 960, 175, 46, { c: '#E9B44C', font: 'Inter', w: 900, ls: '.2em' });
    const shw = sv('g', { 'clip-path': 'url(#c5clip)' }, g); const sh = sv('g', {}, shw); for (let k = 0; k < 9; k++) sv('rect', { x: 560, y: 200 + k * 52, width: 800, height: 50, fill: '#8D98B0', stroke: '#4B5570', 'stroke-width': 4 }, sh);
    tl.set(sh, { y: -470, opacity: 1 }, sA); gsap.set(sh, { y: -470 });
    const clip = sv('clipPath', { id: 'c5clip' }, g); sv('rect', { x: 560, y: 200, width: 800, height: 470 }, clip);
    tl.fromTo(sh, { y: -470 }, { y: 0, duration: .35, ease: 'bounce.out', ...IR }, Math.max(sA + .6, tCl - .25)); sfx('clang', Math.max(sA + .6, tCl - .25) + .2); shake(Math.max(sA + .6, tCl - .25) + .2, 1.6);
    const cl = T(S, '_CLOSED_', 960, 440, 120, { color: '#E2614B' }); stamp(cl, Math.max(sA + .9, tCl + .2), { r: -6 });
    const govs = []; for (let k = 0; k < 4; k++) { const e = E(S, '🏛️', 250 + k * 470, 850, 80); govs.push(e); }
    const tF = A('Foreign governments');
    govs.forEach((e, k) => { pop(e, tF + k * .15, { y0: 80, sfx: k ? false : 'pop' }); });
    const ds = []; for (let k = 0; k < 4; k++) { const e = E(S, '💵', 330 + k * 470, 760, 60); ds.push(e); pop(e, A('swap their dollars') + k * .1, { sfx: false }); tl.to(e, { y: -60, duration: .3, yoyo: true, repeat: 1, ease: 'power2.out' }, A('for American gold') + k * .08); }
    sfx('boing', A('for American gold'), .5); }

  // 6. "a pause" + Bill hopeful
  { const S = shot(t6, t7, { tr: 'slide' }); const g = G(S, { opacity: 1 });
    const pb = sv('g', {}, g); sv('circle', { cx: 620, cy: 440, r: 200, fill: '#26344F', stroke: '#E9B44C', 'stroke-width': 12 }, pb);
    sv('rect', { x: 555, y: 350, width: 45, height: 180, rx: 10, fill: '#E9B44C' }, pb); sv('rect', { x: 640, y: 350, width: 45, height: 180, rx: 10, fill: '#E9B44C' }, pb);
    pop(pb, A('as a pause', .2), { s0: .3 }); pulse(pb, A('as a pause', .8), 1.06, 2);
    const t = T(S, 'Pitched as a *pause*', 620, 150, 70); kin(t, t6 + .1);
    const loop = arrowPath(g, 'M840,330 Q1000,250 1000,440 Q1000,620 840,560', { w: 10 }); draw(loop, A('with gold to return'), .8);
    const gb = goldBar(g, 1120, 450, .8); pop(gb, A('to return', .1), { sfx: 'clink' });
    const k = T(S, 'Gold to return once *fixed*', 620, 760, 50, { color: '#8D98B0' }); kin(k, A('with gold to return'));
    const bIn = LA(32) - .8; charIn('B', bIn, 'R'); idle('B', bIn + .5, t7 + 1.2);
    tl.to(CHR.B.M.brow, { y: -10, duration: .25 }, LA(32) - .2); talk('B', 32); }

  // 7. it never came back: TEMPORARY stamp cracks, Bill's face falls
  { const tN = A('It never came back'); const S = shot(t7, t8, { tr: 'zoom' }); const g = G(S, { opacity: 1 });
    const st = T(S, '_TEMPORARY_', 800, 470, 150, { color: '#E2614B' }); stamp(st, t7 + .05, { r: -8, amp: 1.2 });
    const cr = sv('path', { d: 'M500,380 L640,470 L590,520 L760,560 L700,600 L900,660', fill: 'none', stroke: '#F3EBDD', 'stroke-width': 10, 'stroke-linejoin': 'round', opacity: 0 }, g);
    draw(cr, A('never came', .1), .35); sfx('crack', A('never came', .1));
    tl.to(st, { y: 120, rotation: 14, opacity: .25, duration: .7, ease: 'power2.in' }, AE('came back', .1));
    const k = T(S, 'It never came back', 800, 200, 66); kin(k, tN);
    tl.to(CHR.B.M.brow, { y: 6, rotation: 0, duration: .25 }, tN + .2); tl.to(CHR.B.body, { scaleY: .86, transformOrigin: '50% 100%', duration: .5, ease: 'power2.out' }, tN + .3);
    tl.to(CHR.B.M.sweat, { opacity: 1, y: 0, duration: .15 }, tN + .4); tl.to(CHR.B.M.sweat, { y: 50, opacity: 0, duration: .9 }, tN + .6); sfx('boing', tN + .3, .3);
    charOut('B', t8 + .4); tl.set(CHR.B.body, { scaleY: 1 }, t8 + 1); tl.set(CHR.B.M.brow, { y: 0 }, t8 + 1); }

  // 8. 1973: currencies floating on the waves
  { const S = shot(t8, t9, { tr: 'up' }); const g = G(S, { opacity: 1 });
    const t = T(S, '*1973:* currencies float', 960, 150, 84); kin(t, A('By 1973'));
    const boats = []; [['$', '#E9B44C'], ['€', '#7FB58A'], ['£', '#E2614B'], ['¥', '#C9CFDA']].forEach(([sym, c], k) => {
      const b = sv('g', { transform: `translate(${420 + k * 360},${560 + (k % 2) * 40})` }, g); const bi = sv('g', {}, b);
      sv('path', { d: 'M-110,20 L110,20 L80,80 L-80,80 Z', fill: '#6B3E22', stroke: '#2E190C', 'stroke-width': 6 }, bi);
      sv('circle', { cx: 0, cy: -50, r: 70, fill: c, stroke: '#0A1120', 'stroke-width': 6 }, bi); svgT(bi, sym, 0, -22, 84, { c: '#0A1120' });
      boats.push(bi); pop(bi, A('the major currencies') + k * .25, { y0: 120, sfx: k ? false : 'splash' }); bob(bi, A('the major currencies') + k * .25 + .5, t9 + .4, 16, 1.8 + k * .3); });
    const waves = sv('g', {}, g); for (let k = 0; k < 3; k++) { let d = `M-200,${660 + k * 60}`; for (let x = 0; x < 30; x++) d += ` q60,-28 120,0 t120,0`; sv('path', { d, fill: 'none', stroke: ['#3B7CB0', '#2C6E9E', '#1F5580'][k], 'stroke-width': 26 - k * 4, 'stroke-linecap': 'round' }, waves); }
    fin(waves, t8, .4); tl.fromTo(waves, { x: 0 }, { x: -240, duration: t9 - t8 + .5, ease: 'none', ...IR }, t8);
    const k = T(S, 'Priced by *markets,* not metal', 960, 960 - 120, 56); kin(k, A('priced by markets')); }

  // 9. re-hook: the puzzle
  { const S = shot(t9, end, { tr: 'wipe', push: 1.06 }); const g = G(S, { opacity: 1 });
    const c = coin(g, 960, 470, 170, { mark: '$' }); pop(c, t9 + .2, { s0: .3, sfx: 'clink' });
    const q = T(S, '*?*', 960, 200, 200); kin(q, A('a puzzle'), { s0: .2, sfx: 'pop' }); pulse(q, A('a puzzle', .5), 1.12, 2);
    const gb = goldBar(g, 1460, 470, 1.2); pop(gb, A('The dollar lost'), { sfx: false });
    const link = sv('path', { d: 'M1150,470 L1330,470', stroke: '#C9CFDA', 'stroke-width': 14, 'stroke-dasharray': '22 14', opacity: 0 }, g); fin(link, A('The dollar lost'), .2);
    tl.to(link, { opacity: 0, scaleX: .2, transformOrigin: '50% 50%', duration: .25 }, A('last link', .3)); sfx('snap', A('last link', .3));
    tl.to(gb, { x: 200, opacity: 0, duration: .6, ease: 'power2.in' }, A('more than fifty'));
    const yrs = I(S, '0', 1480, 470, 96, { weight: 900, color: '#E9B44C' }); fin(yrs, A('more than fifty'), .2); count(yrs, 0, 50, A('more than fifty'), 1.1, { suf: '+ yrs' });
    out(yrs, A("You'd expect"), .3);
    const bin = E(S, '🗑️', 480, 720, 150); pop(bin, A("You'd expect", .2));
    tl.to(c, { x: -380, y: 160, rotation: -30, scale: .5, duration: .7, ease: 'power2.in' }, A('to dump it', -.2)); sfx('whoosh', A('to dump it', -.2), .5);
    tl.to(c, { x: 0, y: 0, rotation: 0, scale: 1.15, duration: .7, ease: 'back.out(2)' }, A('Instead', .1)); out(bin, A('Instead', .2), .3); sfx('swoosh', A('Instead', .1), .6);
    const rings = []; for (let k = 0; k < 3; k++) { const r = sv('circle', { cx: 960, cy: 470, r: 180, fill: 'none', stroke: '#E9B44C', 'stroke-width': 6, opacity: 0 }, g); tl.fromTo(r, { opacity: .8, attr: { r: 180 } }, { opacity: 0, attr: { r: 520 }, duration: 1.2, ease: 'power2.out', ...IR }, A('even more central') + k * .3); }
    const k = T(S, 'Even more *central*', 960, 780, 70); kin(k, A('even more central'));
    out(k, A('Why?', -.15), .15); const w = T(S, '*Why?*', 960, 780, 120); stamp(w, A('Why?', -.2), { r: 0 }); }
}
