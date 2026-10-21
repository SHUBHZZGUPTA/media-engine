// CHAPTER 7: SO WHAT IS YOUR MONEY, REALLY? (lines 41-46) + end card — archival/painted style
function c7_note(parent, x, y, w, fill) { const g0 = sv('g', { transform: `translate(${x},${y})` }, parent); const g = sv('g', {}, g0); const h = w * .5;
  sv('rect', { x: -w / 2, y: -h / 2, width: w, height: h, rx: 10, fill: fill || '#EFE6D2', stroke: '#E9B44C', 'stroke-width': 4 }, g);
  sv('rect', { x: -w / 2 + 14, y: -h / 2 + 14, width: w - 28, height: h - 28, rx: 6, fill: 'none', stroke: '#8D7A52', 'stroke-width': 2, 'stroke-dasharray': '8 5' }, g);
  sv('ellipse', { cx: w * .2, cy: 0, rx: w * .12, ry: h * .28, fill: 'none', stroke: '#8D7A52', 'stroke-width': 3 }, g);
  svgT(g, '£', -w * .32, -h * .12, w * .14, { c: '#6E5A35' }); return g; }

function ch7() {
  const t0 = CH(7).a - .3, tProb = A("Here's the problem"), tAll = A('All the gold ever mined'), tTie = A("Tie the world's money"),
    tCri = A('In a crisis'), tMany = A('Many economists'), tBack = A('So, back to the question'), tRead = A('Read that British note'),
    tSwap = A('you can swap the note'), tWhat = A('What really stands behind it'), tPay = A('Gold was a promise'), tSub = LA(46) - .25, tEndAll = D.dur + .5;
  startCh(7);

  // 1. why not go back to gold?
  { const S = photo(t0, tAll - .2, 'fortknox_vault.jpg', { grade: 'mono', kb: [1.14, 1.04], tr: 'fade', credit: 'Fort Knox Bullion Depository · Public domain' });
    lower(S, null, 'Why not go back to *gold?*', A('So why not just', -.05), { kin: { times: wordTimes('why not just go back to gold').filter((_, i) => i !== 2) } });
    const p = I(S, "HERE'S THE PROBLEM", 124, 650, 30, { align: 'left', color: '#E2614B', ls: '.3em', weight: 800 }); fin(p, tProb, .35); sfx('swoosh', tProb, .35); }

  // 2. all the gold ever mined -> one cube
  { const S = photo(tAll - .2, tTie - .2, 'gold_cube.jpg', { grade: 'paint', kb: [1.0, 1.05], from: [0, 0], to: [0, -1], tr: 'zoom' });
    const k = I(S, 'ALL THE GOLD EVER MINED', 124, 170, 28, { align: 'left', color: '#E9B44C', ls: '.3em', weight: 800 }); fin(k, tAll, .4);
    const n = I(S, '0', 118, 270, 120, { align: 'left', weight: 900 }); fin(n, A('222,600'), .2); count(n, 0, 222600, A('222,600'), 2.0);
    const u = I(S, 'TONNES', 124, 360, 34, { align: 'left', color: '#C9CFDA', ls: '.25em', weight: 800 }); fin(u, A('tonnes'), .3);
    const tM = A('22.6 metres'); const g = G(S, { opacity: 1 });
    const ln = sv('path', { d: 'M700,205 L700,730', stroke: '#E9B44C', 'stroke-width': 5, fill: 'none', opacity: 0 }, g); draw(ln, A('roughly', -.1), .9);
    const tk = sv('path', { d: 'M675,205 L725,205 M675,730 L725,730', stroke: '#E9B44C', 'stroke-width': 5, opacity: 0 }, g); fin(tk, A('roughly', .6), .3);
    const m = I(S, '22.6 m', 670, 600, 64, { align: 'right', color: '#E9B44C', weight: 900 }); pop(m, tM, { s0: .6, sfx: 'tick' });
    const s2 = I(S, 'PER SIDE', 670, 655, 24, { align: 'right', color: '#F3EBDD', ls: '.3em', weight: 800 }); fin(s2, A('on each side'), .3);
    const c = T(S, 'One *single* cube', 1800, 860, 70, { align: 'right' }); kin(c, A('single cube', -.15)); sfx('clink', A('cube'), .5);
    const il = I(S, 'ILLUSTRATION', 1880, 1050, 13, { align: 'right', color: 'rgba(243,235,221,.45)', ls: '.2em', weight: 600 }); fin(il, tAll, .3); }

  // 3. money grows only as fast as miners can dig
  { const S = photo(tTie - .2, tCri - .15, 'miners_1850.jpg', { grade: 'warm', kb: [1.32, 1.42], pos: '50% 45%', from: [0, 1], to: [-2, -1], tr: 'slide', credit: 'G. H. Johnson, c.1850s · Public domain' });
    const k = lower(S, 'CALIFORNIA GOLD MINERS · 1850s', 'Money grows only as fast as *miners dig*', A('and money can only', -.1), { size: 76, y: 800 });
    const g = G(S, { opacity: 1 }); const ax = sv('path', { d: 'M1170,420 L1170,180 M1170,420 L1680,420', stroke: 'rgba(243,235,221,.6)', 'stroke-width': 3, fill: 'none', opacity: 0 }, g); fin(ax, tTie + .2, .3);
    const mine = sv('path', { d: 'M1170,400 C1330,385 1500,350 1680,330', stroke: '#E9B44C', 'stroke-width': 7, fill: 'none', opacity: 0, 'stroke-linecap': 'round' }, g); draw(mine, A('that cube', -.2), 1.0);
    const mon = sv('path', { d: 'M1170,405 C1300,395 1480,345 1680,335', stroke: '#E2614B', 'stroke-width': 5, fill: 'none', opacity: 0, 'stroke-dasharray': '1 0', 'stroke-linecap': 'round' }, g); draw(mon, A('can only grow', -.1), 1.1);
    const l1 = svgT(g, 'GOLD MINED', 1690, 322, 20, { anchor: 'start', c: '#E9B44C', font: 'Inter', w: 800, ls: '.15em' }); const l2 = svgT(g, 'MONEY', 1690, 352, 20, { anchor: 'start', c: '#E2614B', font: 'Inter', w: 800, ls: '.15em' });
    gsap.set([l1, l2], { opacity: 0 }); tl.to(l1, { opacity: 1, duration: .3 }, A('that cube', .7)); tl.to(l2, { opacity: 1, duration: .3 }, A('can only grow', .9)); }

  // 4. in a crisis, central banks' hands are tied
  { const S = photo(tCri - .15, tMany - .15, 'central_bank.jpg', { grade: 'paint', kb: [1.18, 1.06], from: [0, -2], to: [0, 0], tr: 'fade' });
    lower(S, 'IN A CRISIS', "Central banks' hands are *tied*", tCri + .1, { size: 88 }); sfx('clang', A('tied', -.05), .5); shake(A('tied'), .5); }

  // 5. the Great Depression
  { const S = photo(tMany - .15, tBack - .2, 'bankrun_1931.jpg', { grade: 'mono', kb: [1.04, 1.18], from: [2, 0], to: [-2, -3], tr: 'slide', credit: 'Library of Congress, NYWT&S Collection · Public domain' });
    lower(S, 'NEW YORK · GREAT DEPRESSION', 'Part of what made it *so brutal*', A('Many economists', .3), { size: 84 }); sfx('thud', A('brutal'), .35); }

  // 6. back to the question (wallet callback)
  { const S = photo(tBack - .2, tRead - .2, 'wallet_desk.jpg', { grade: 'paint', kb: [1.1, 1.24], from: [-1, -2], to: [-3, -5], tr: 'fade' });
    const k = I(S, 'BACK TO THE QUESTION', 960, 360, 28, { color: '#E9B44C', ls: '.32em', weight: 800 }); fin(k, tBack, .4);
    const h = T(S, 'What is your money *backed by?*', 960, 460, 100); kin(h, A('What is your money'), { times: wordTimes('What is your money backed by') }); }

  // 7. read that British note again: the promise, and what it means today
  { const S = photo(tRead - .2, tSwap - .2, 'boe_hall_1808.jpg', { grade: 'warm', kb: [1.2, 1.06], from: [0, -2], to: [0, 1], tr: 'zoom', credit: 'Rowlandson & Pugin, 1808 · Public domain' });
    const q = T(S, '"I promise to pay the bearer on demand..."', 960, 300, 66, { color: '#E9B44C' }); kin(q, tRead + .2, { st: .12 });
    const k = lower(S, 'THE BANK OF ENGLAND SAYS', 'It means *one thing*', A('Today, the Bank'), { size: 90 }); sfx('typing', tRead + .2, .4); }

  // 8. swap the note... for another note (loop)
  { const S = photo(tSwap - .2, tWhat - .2, 'bank_vault_1700s.jpg', { grade: 'soft', kb: [1.12, 1.18], tr: 'fade' }); tl.set(S.img, { filter: GRADES.soft + ' blur(6px) brightness(.6)' }, tSwap - .25);
    const g = G(S, { opacity: 1 }); const nA = c7_note(g, 700, 430, 300), nB = c7_note(g, 1220, 430, 300, '#E6DCC4');
    gsap.set([nA, nB], { autoAlpha: 0 }); tl.to(nA, { autoAlpha: 1, duration: .3 }, tSwap); tl.to(nB, { autoAlpha: 1, duration: .3 }, A('another Bank', -.2));
    const arcT = sv('path', { d: 'M760,300 Q960,170 1160,300', stroke: '#E9B44C', 'stroke-width': 6, fill: 'none', 'marker-end': 'url(#ahg)', opacity: 0 }, g);
    const arcB = sv('path', { d: 'M1160,560 Q960,690 760,560', stroke: '#E9B44C', 'stroke-width': 6, fill: 'none', 'marker-end': 'url(#ahg)', opacity: 0 }, g);
    draw(arcT, A('swap the note'), .5); draw(arcB, A('swap the note', .4), .5); sfx('swoosh', A('swap the note'), .4);
    for (let k = 0; k < 3; k++) { const at = A('another Bank', -.1) + k * 1.05;
      tl.to(nA, { x: 520, y: 0, duration: .5, ease: 'power2.inOut' }, at); tl.to(nB, { x: -520, duration: .5, ease: 'power2.inOut' }, at);
      tl.to(nA, { x: 0, duration: .5, ease: 'power2.inOut' }, at + .52); tl.to(nB, { x: 0, duration: .5, ease: 'power2.inOut' }, at + .52); sfx('flip', at, .35); }
    const h = T(S, 'Swap it... for *another note*', 960, 820, 78); kin(h, A('swap the note', -.1), { times: wordTimes('swap the note').slice(0, 2).concat(wordTimes('for another Bank of England note').slice(0, 3)) }); }

  // 9. trust: three pillars rising
  { const tT1 = A('Trust that the central bank'), tT2 = A('Trust in a government'), tT3 = A('And trust that everyone'), tTom = A('tomorrow');
    const S = photo(tWhat - .2, tPay - .3, 'central_bank.jpg', { grade: 'paint', kb: [1.06, 1.14], tr: 'fade' }); tl.set(S.img, { filter: GRADES.paint + ' blur(5px) brightness(.45)' }, tWhat - .25);
    const tr = T(S, '*TRUST*', 960, 130, 110, { ls: '.18em' }); kin(tr, A('is trust', .2), { s0: 1.6, dy: 0, sfx: 'stamp' }); shake(A('is trust', .45), .5);
    const g = G(S, { opacity: 1 }); const base = sv('rect', { x: 430, y: 760, width: 1060, height: 22, rx: 4, fill: '#C9CFDA', opacity: 0 }, g); fin(base, tWhat + .4, .4);
    const lab = [['Stable', 'prices', tT1, 610], ['Taxes paid', 'in it', tT2, 960], ['Everyone', 'accepts it', tT3, 1310]];
    lab.forEach(([a1, a2, at, x]) => { const p = sv('g', {}, g);
      sv('rect', { x: x - 80, y: 380, width: 160, height: 380, fill: '#DDE2EA', stroke: '#8D98B0', 'stroke-width': 4 }, p);
      for (let k = 0; k < 3; k++) sv('line', { x1: x - 45 + k * 45, y1: 410, x2: x - 45 + k * 45, y2: 740, stroke: '#A9B1C2', 'stroke-width': 4 }, p);
      sv('rect', { x: x - 100, y: 360, width: 200, height: 26, rx: 4, fill: '#F3EBDD', stroke: '#8D98B0', 'stroke-width': 4 }, p);
      const t1 = svgT(p, a1, x, 540, 30, { c: '#101A2E', font: 'Inter', w: 800 }); const t2 = svgT(p, a2, x, 578, 30, { c: '#101A2E', font: 'Inter', w: 800 });
      gsap.set(p, { autoAlpha: 0 }); tl.fromTo(p, { autoAlpha: 1, scaleY: 0, transformOrigin: '50% 100%' }, { scaleY: 1, duration: .6, ease: 'back.out(1.4)', ...IR }, at); sfx('thud', at + .2, .4); ev(at, 'pillar'); });
    const top = c7_note(g, 960, 300, 340); gsap.set(top, { autoAlpha: 0 }); tl.fromTo(top, { autoAlpha: 0, y: -160 }, { autoAlpha: 1, y: 0, duration: .6, ease: 'bounce.out', ...IR }, tTom - .3); sfx('clink', tTom, .4); ev(tTom, 'note'); }

  // 10. payoff, typed slowly, then the mirage dissolves
  { const tStop = A('stop believing'), tMir = A("that's when the mirage"), tDis = A('disappears');
    const S = photo(tPay - .3, tSub, 'wallet_desk.jpg', { grade: 'paint', kb: [1.0, 1.1], from: [0, 0], to: [-1, -2], tr: 'fade' });
    const fid = 'c7wob'; const defs = sv('defs', {}, S.svg); const flt = sv('filter', { id: fid, x: '-5%', y: '-5%', width: '110%', height: '110%' }, defs);
    const turb = sv('feTurbulence', { type: 'fractalNoise', baseFrequency: '0.008 0.03', numOctaves: 2, seed: 3, result: 'n' }, flt);
    const disp = sv('feDisplacementMap', { in: 'SourceGraphic', in2: 'n', scale: 0, xChannelSelector: 'R', yChannelSelector: 'G' }, flt);
    const l1 = T(S, 'Gold was a promise you could *hold.*', 960, 330, 84); kin(l1, A('Gold was a promise'), { times: wordTimes('Gold was a promise you could hold'), dy: 10, s0: 1 });
    const l2 = T(S, 'Paper is a promise you have to *believe.*', 960, 450, 84); kin(l2, A('Paper is a promise'), { times: wordTimes('Paper is a promise you have to believe'), dy: 10, s0: 1 });
    tl.to([l1, l2], { opacity: .35, duration: .8 }, tStop - .6);
    const l3 = T(S, "...that's when the *mirage* disappears", 960, 640, 76); kin(l3, tMir, { times: wordTimes("that's when the mirage disappears"), dy: 10, s0: 1 });
    S.wrap.style.filter = `url(#${fid})`; [l1, l2, l3].forEach(e => { e.style.filter = `url(#${fid})`; });
    const w = { s: 0, f: 0 }; tl.fromTo(w, { s: 0, f: 0 }, { s: 70, f: 1, duration: tSub - tDis + .2, ease: 'power2.in', ...IR, onUpdate: () => { disp.setAttribute('scale', w.s.toFixed(1)); turb.setAttribute('baseFrequency', `${(0.008 + w.f * 0.01).toFixed(4)} ${(0.03 + w.f * 0.03).toFixed(4)}`); } }, tDis - .2);
    tl.to([S.wrap, l1, l2, l3], { opacity: 0, duration: tSub - tDis + .1, ease: 'power1.in' }, tDis); sfx('shimmer', tDis - .3, .7); ev(tDis, 'dissolve'); }

  // 11. end card
  { const S = shot(tSub, tEndAll, { tr: 'fade', push: 1.03, bg: 'radial-gradient(ellipse 70% 60% at 50% 45%, #16243F 0%, #0A1120 70%)' });
    const s = 2.4, wmw = 435 * s; const wm = wordmark(S.svg, (1920 - wmw) / 2, 460, s); tl.set(wm.g, { opacity: 0 }, 0);
    tl.fromTo(wm.g, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .8, ease: 'power3.out', ...IR }, tSub + .1); sfx('sting', tSub + .05, .7);
    tl.fromTo(wm.waves, { x: 0 }, { x: -56, duration: 5, ease: 'none', ...IR }, tSub); tl.fromTo(wm.refl, { opacity: 0 }, { opacity: .28, duration: 1, ...IR }, tSub + .5);
    const btn = mk('div', {}, S.stg); Object.assign(btn.style, { position: 'absolute', left: '810px', top: '600px', width: '300px', height: '84px', borderRadius: '42px', background: '#E9B44C', color: '#101A2E', font: "800 36px Inter", display: 'flex', alignItems: 'center', justifyContent: 'center', letterSpacing: '.04em', boxSizing: 'border-box' }); btn.textContent = 'Subscribe';
    pop(btn, A('Subscribe to Money'), { s0: .5, sfx: false }); const tp = A('Money Mirage', .4);
    tl.to(btn, { keyframes: [{ scale: .9, duration: .1 }, { scale: 1, duration: .14 }] }, tp); sfx('pop', tp, .8);
    tl.to(btn, { backgroundColor: '#101A2E', color: '#E9B44C', border: '4px solid #E9B44C', duration: .2 }, tp + .05);
    const tg = T(S, "See through money's *illusions*", 960, 790, 46, { color: '#C9CFDA' }); kin(tg, A('we\'ll see through', -.1), { st: .1 }); sfx('sparkle', A("we'll see through"), .5); }
}
