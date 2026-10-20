// COLD OPEN (lines 0-5) + logo sting
function ch0() {
  const tA = A('The money in your wallet'), tQ = A('So what is it backed'), tM = A('And it matters'), tR = A('Read the small print');
  const tPW = A('Pay what'), tSun = A('Then, one Sunday'), tG = LA(3) - .5, tIV = A('In this video'), tFr = A('why France'), tNine = A('why almost nine'),
    tBeh = A("and what's really"), tSp = A('Spoiler'), tEnd = LB(5) + .35, tLogo = CH(1).a - 1.3;
  startCh(0);

  // 1. wallet opens, note slides out
  { const S = shot(0, tQ, { tr: 'fade' }); const g = G(S, { opacity: 1 });
    const n = note(g, 960, 470, 520, { num: '100' }); const w = wallet(g, 960, 560, 1.25);
    tl.set(n, { y: 90 }, 0); pop(w.g, .15, { s0: .6 });
    tl.fromTo(w.flap, { scaleY: 1, transformOrigin: '50% 100%', transformBox: 'fill-box' }, { scaleY: -.15, duration: .5, ease: 'power2.inOut', ...IR }, A('in your wallet'));
    sfx('zip', A('in your wallet'), .6);
    tl.fromTo(n, { y: 90, attr: { opacity: 1 } }, { y: -160, duration: .7, ease: 'back.out(1.6)', ...IR }, A('backed'));
    const t = T(S, "Not backed by *gold* since *1971*", 960, 830, 76); kin(t, A('backed'), { times: wordTimes("hasn't been backed by gold since 1971").slice(1) });
    stamp(T(S, '_NO GOLD_', 1370, 300, 70, { color: '#E2614B' }), A('1971'), { r: 10 }); }

  // 2. so what is it backed by?
  { const S = shot(tQ, tM, { tr: 'zoom' }); const g = G(S, { opacity: 1 }); const n = note(g, 700, 470, 560, { num: '100' });
    const q = T(S, '*?*', 1330, 470, 420); kin(q, tQ + .6, { s0: .2, sfx: 'pop' }); pulse(q, tQ + 1.6, 1.1, 2);
    const t = T(S, 'Backed by... *what?*', 960, 830, 84); kin(t, tQ, { times: wordTimes('backed by').concat([A('backed by', .55)]) });
    wiggle(n, tQ + .8, 4, 3); }

  // 3. whatever backs your money can weaken it: pillar cracks
  { const tW = A('weaken'); const S = shot(tM, tR, {}); const g = G(S, { opacity: 1 });
    const pil = sv('g', {}, g); sv('rect', { x: 860, y: 520, width: 200, height: 330, fill: '#C9CFDA', stroke: '#6C7690', 'stroke-width': 6 }, pil);
    sv('rect', { x: 830, y: 500, width: 260, height: 40, rx: 6, fill: '#DDE2EA', stroke: '#6C7690', 'stroke-width': 6 }, pil); svgT(pil, 'BACKING', 960, 700, 34, { c: '#4B5570', font: 'Inter', w: 900, ls: '.18em' });
    const n = note(g, 960, 420, 360, { num: '100' }); slideIn(pil, tM, 0, 300); slideIn(n, tM + .3, 0, -300, { sfx: 'whoosh' });
    const crack = sv('path', { d: 'M960,520 L935,600 L985,650 L940,730 L975,800 L955,850', fill: 'none', stroke: '#E2614B', 'stroke-width': 8, 'stroke-linejoin': 'round', opacity: 0 }, g);
    draw(crack, tW, .35); shake(tW + .1, 1.4); sfx('crack', tW); tl.to(n, { rotation: 9, y: 20, transformOrigin: '50% 50%', duration: .5, ease: 'back.out(3)' }, tW + .15);
    const t = T(S, 'What backs it can *weaken* it', 960, 180, 72); kin(t, A('because whatever', 0)); }

  // 4. the small print: magnifier over the promise line
  { const S = shot(tR, tPW, { tr: 'slide', push: 1.08 }); const g = G(S, { opacity: 1 });
    const n = note(g, 960, 480, 1100, { num: '20', text: 'I PROMISE TO PAY THE BEARER|ON DEMAND THE SUM OF' }); pop(n, tR, { s0: .8, sfx: 'whoosh' });
    const lens = sv('g', { opacity: 0 }, g); sv('circle', { cx: 0, cy: 0, r: 150, fill: 'rgba(243,235,221,.12)', stroke: '#E9B44C', 'stroke-width': 14 }, lens); sv('path', { d: 'M105,105 L210,210', stroke: '#E9B44C', 'stroke-width': 26, 'stroke-linecap': 'round' }, lens);
    tl.fromTo(lens, { opacity: 0, x: 1500, y: 900 }, { opacity: 1, x: 860, y: 440, duration: 1.1, ease: 'power3.inOut', ...IR }, A('small print'));
    const q = T(S, '"I promise to pay the bearer on demand..."', 960, 830, 62, { color: '#E9B44C' }); kin(q, A('"I promise'), { times: wordTimes('I promise to pay the bearer on demand') });
    tl.to(lens, { x: 1000, duration: 2.2, ease: 'sine.inOut' }, A('"I promise')); }

  // 5. pay what? the answer was gold
  { const tGold = A('answer was gold', .55); const S = shot(tPW, tSun, { tr: 'wipe' }); const g = G(S, { opacity: 1 });
    const t = T(S, 'Pay *what?*', 960, 300, 150); kin(t, tPW, { times: wordTimes('Pay what') });
    tl.to(t, { y: -110, scale: .6, duration: .5, ease: 'power3.inOut' }, A('For most of history'));
    const sub = T(S, 'For most of history...', 960, 340, 56, { color: '#8D98B0' }); kin(sub, A('For most of history'));
    const gb = goldBar(g, 960, 650, 2.6); pop(gb, tGold, { s0: 3, sfx: 'clink', ease: 'power4.in', d: .3 }); shake(tGold + .3, .8); flash(tGold + .28, .35);
    bob(gb, tGold + .5, tSun, 8, 2); }

  // 6. one Sunday in 1971 the promise changed: calendar + chain snaps
  { const tCh = A('quietly changed'), tNv = A('never changed back'); const S = shot(tSun, tG, { tr: 'up' }); const g = G(S, { opacity: 1 });
    const cal = P(S, 160, 210, 380, 420, { bg: '#F3EBDD', border: '#C9CFDA' }); const ch = mk('div', {}, cal); ch.innerHTML = '<div style="background:#E2614B;height:90px;border-radius:18px 18px 0 0;color:#fff;font:800 44px Inter;display:flex;align-items:center;justify-content:center;letter-spacing:.12em">SUNDAY</div><div style="font:800 170px Brico;color:#101A2E;text-align:center;line-height:220px">1971</div>';
    slideIn(cal, A('one Sunday'), -300, 0, { sfx: 'flip' });
    const n = note(g, 1000, 430, 300, { num: '1' }); const gb = goldBar(g, 1560, 430, 1.5);
    const chain = sv('g', { opacity: 0 }, g); for (let k = 0; k < 7; k++) sv('ellipse', { cx: 1170 + k * 38, cy: 430, rx: 24, ry: 13, fill: 'none', stroke: '#C9CFDA', 'stroke-width': 7 }, chain);
    pop(n, A('that promise'), { s0: .5 }); pop(gb, A('that promise', .25), { s0: .5, sfx: 'clink' }); fin(chain, A('that promise', .4));
    tl.to(chain, { opacity: 0, scale: 1.4, transformOrigin: '50% 50%', transformBox: 'fill-box', duration: .25 }, tCh); sfx('snap', tCh); shake(tCh, 1.2); flash(tCh, .25);
    tl.to(gb, { x: 90, rotation: 8, transformOrigin: '50% 50%', duration: .7, ease: 'power3.out' }, tCh); tl.to(n, { x: -80, rotation: -8, transformOrigin: '50% 50%', duration: .7, ease: 'power3.out' }, tCh);
    const t = T(S, '...and it *never* changed back', 1180, 790, 70); kin(t, tNv, { times: wordTimes('and it never changed back') }); }

  // 7. Goldie and Bill banter
  { const S = shot(tG, tIV, { tr: 'fade', push: 1.02 }); const spot = sv('ellipse', { cx: 960, cy: 960, rx: 760, ry: 120, fill: 'rgba(233,180,76,.10)' }, S.svg);
    const spot2 = sv('path', { d: 'M700,0 L1220,0 L1560,1000 L360,1000 Z', fill: 'rgba(243,235,221,.05)' }, S.svg);
    charIn('G', tG, 'CL'); charIn('B', tG + .35, 'CR'); idle('G', tG + .6, tIV + .2); idle('B', tG + .9, tIV + .2);
    talk('G', 3); tl.to(CHR.G.M.brow, { y: -8, duration: .2, yoyo: true, repeat: 1 }, LA(3) + .2); tl.to(CHR.G.M.armR, { rotation: -25, svgOrigin: '272 215', duration: .25, yoyo: true, repeat: 1 }, LA(3) + .4);
    talk('B', 4); tl.to(CHR.B.M.sweat, { opacity: 1, duration: .15 }, LA(4)); tl.to(CHR.B.M.sweat, { y: 40, opacity: 0, duration: .8 }, LA(4) + .3);
    tl.to(CHR.B.d, { x: -40, duration: .2, yoyo: true, repeat: 1 }, LA(4) + .1);
    charOut('G', tIV - .1); charOut('B', tIV - .1); }

  // 8. preview montage
  { const S = shot(tIV, A('how paper beat', 1.6), { tr: 'zoom' }); const g = G(S, { opacity: 1 });
    const t = T(S, 'In this video', 960, 200, 64, { color: '#8D98B0' }); kin(t, tIV);
    const sc = scaleProp(g, 960, 600, 1.3); pop(sc.g, A('how paper beat'), { s0: .6 });
    const n = note(sc.L, -200, -70, 150, {}); const gb = goldBar(sc.R, 200, -55, .75); tl.set([n, gb], { opacity: 1 }, 0);
    tl.fromTo(sc.beam, { rotation: 10, transformOrigin: '50% 4%' }, { rotation: -12, transformOrigin: '50% 4%', duration: 1.1, ease: 'elastic.out(1,.5)', ...IR }, A('paper beat', .2));
    const k = T(S, 'Paper *beat* gold', 960, 840, 76); kin(k, A('paper beat')); }
  { const S = shot(A('why France'), tNine, { tr: 'slide' }); const f = E(S, '🇫🇷', 520, 470, 220); pop(f, tFr);
    const d = E(S, '💵', 960, 470, 200); pop(d, A('cash its dollars'));
    const ar = arrowPath(S.svg, 'M1100,470 L1290,470', { w: 14 }); draw(ar, A('in for gold', -.2), .4); const gb = goldBar(S.svg, 1480, 480, 1.4); pop(gb, A('in for gold'), { sfx: 'clink' });
    const k = T(S, 'France cashes in', 960, 830, 76); kin(k, A('why France')); }
  { const S = shot(tNine, tBeh, { tr: 'up' }); const R = 230, C = 2 * Math.PI * R;
    sv('circle', { cx: 760, cy: 470, r: R, fill: 'none', stroke: '#26344F', 'stroke-width': 56 }, S.svg);
    const ring = sv('circle', { cx: 760, cy: 470, r: R, fill: 'none', stroke: '#E9B44C', 'stroke-width': 56, 'stroke-dasharray': C, 'stroke-dashoffset': C, transform: 'rotate(-90 760 470)' }, S.svg);
    tl.fromTo(ring, { attr: { 'stroke-dashoffset': C } }, { attr: { 'stroke-dashoffset': C * .11 }, duration: 1.6, ease: 'power2.out', ...IR }, A('nine in ten'));
    const n = I(S, '0', 760, 470, 130, { weight: 900 }); fin(n, A('nine in ten'), .2); count(n, 0, 89, A('nine in ten'), 1.6, { suf: '%' });
    const k = T(S, '9 in 10 currency trades', 1390, 410, 64, { align: 'center' }); kin(k, A('currency trades'));
    const k2 = T(S, 'involve the *dollar*', 1390, 510, 64); kin(k2, A('involve the dollar')); }
  { const S = shot(tBeh, tSp, { tr: 'zoom' }); const g = G(S, { opacity: 1 }); const glow = sv('circle', { cx: 960, cy: 470, r: 330, fill: 'rgba(233,180,76,.12)' }, g);
    const q = T(S, '*?*', 960, 470, 560, { color: '#26344F' }); kin(q, tBeh, { s0: .3, sfx: 'swoosh' });
    const n = note(g, 960, 470, 520, { num: '?' }); pop(n, A('standing behind', -.2)); bob(n, A('standing behind'), tSp, 12, 2.4);
    const k = T(S, "What's really behind your money?", 960, 840, 66); kin(k, tBeh, { times: wordTimes("what's really standing behind your money").filter((_, i) => i !== 2) }); }
  { const tBut = A("But it isn't nothing"); const S = shot(tSp, tEnd, { tr: 'wipe' }); const g = G(S, { opacity: 1 });
    const gb = goldBar(g, 960, 470, 2.4); pop(gb, tSp, { s0: .5, sfx: 'clink' }); const xm = sv('path', { d: 'M740,280 L1180,660 M1180,280 L740,660', stroke: '#E2614B', 'stroke-width': 34, 'stroke-linecap': 'round', opacity: 0 }, g);
    stamp(xm, A("it isn't gold", .1), { r: 0 }); const k = T(S, "Spoiler: it isn't *gold*", 960, 830, 80); kin(k, tSp);
    tl.to([gb, xm], { opacity: .15, duration: .4 }, tBut); const k2 = T(S, "But it isn't *nothing*", 960, 830, 80); out(k, tBut - .05, .2); kin(k2, tBut, { times: wordTimes("But it isn't nothing") }); }

  // 9. logo sting
  { const S = shot(tEnd, tLogo, { tr: 'fade', push: 1.04 }); const wm = wordmark(S.svg, 220, 520, 3.4); tl.set(wm.g, { opacity: 0 }, 0);
    tl.fromTo(wm.g, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .8, ease: 'power3.out', ...IR }, tEnd + .1); sfx('sting', tEnd + .05, 1);
    tl.fromTo(wm.waves, { x: 0 }, { x: -56, duration: 3.2, ease: 'none', ...IR }, tEnd); tl.fromTo(wm.refl, { opacity: 0 }, { opacity: .28, duration: 1, ...IR }, tEnd + .5);
    const sh = sv('rect', { x: 300, y: 330, width: 120, height: 300, fill: 'rgba(255,246,226,.35)', transform: 'skewX(-20)', style: 'filter: blur(10px)' }, S.svg);
    tl.fromTo(sh, { x: -300 }, { x: 1500, duration: 1.2, ease: 'power2.inOut', ...IR }, tEnd + .9); }
}
