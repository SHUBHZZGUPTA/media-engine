// CHAPTER 3: THE GOLD TRAP (lines 17-22)
function c3_type(el, txt, at, dur) { const p = { v: 0 }; el.textContent = ''; gsap.set(el, { autoAlpha: 0 }); tl.set(el, { autoAlpha: 1 }, at);
  tl.fromTo(p, { v: 0 }, { v: txt.length, duration: dur, ease: 'none', ...IR, onUpdate: () => { el.textContent = txt.slice(0, Math.round(p.v)); } }, at); sfx('typing', at, .5); ev(at, 'type'); }
function ch3() {
  const t0 = CH(3).a - .3, tPanic = A('And in a panic'), tEm = A('So in emergencies'), tAm = A('America went further'), tHand = A('Americans had to hand'),
    tHoard = A('Hoard it'), tDin = A('Imagine explaining'), tYear = A('A year later'), tLeg = A("And Americans couldn't"), tOrd = A('So ordinary people'), tEnd = LB(22) + .35;
  startCh(3);

  // 1. money line capped by the gold pile
  { const S = shot(t0, tPanic, { tr: 'fade' }); const g = G(S, { opacity: 1 });
    const ax = sv('path', { d: 'M360,820 L360,230 M360,820 L1560,820', stroke: '#3B5384', 'stroke-width': 6, fill: 'none', 'stroke-linecap': 'round', opacity: 0 }, g); draw(ax, t0 + .2, .6);
    const t1 = T(S, 'In calm times, it *worked*', 960, 150, 70); kin(t1, A('In calm times'));
    const gl = sv('path', { d: 'M360,620 C700,600 1100,585 1560,560', stroke: '#E9B44C', 'stroke-width': 12, fill: 'none', 'stroke-linecap': 'round', 'stroke-dasharray': '26 16', opacity: 0 }, g);
    const ml = sv('path', { d: 'M360,800 C560,760 700,660 860,640 C1050,622 1250,604 1560,580', stroke: '#7FB58A', 'stroke-width': 12, fill: 'none', 'stroke-linecap': 'round', opacity: 0 }, g);
    const lm = svgT(g, 'MONEY', 1580, 600, 34, { c: '#7FB58A', anchor: 'start', font: 'Inter', w: 900 }); const lg = svgT(g, 'GOLD', 1580, 545, 34, { c: '#E9B44C', anchor: 'start', font: 'Inter', w: 900 });
    tl.set([lm, lg], { opacity: 0 }, 0);
    out(t1, A("But here's the catch"), .2); const t2 = T(S, "But here's the *catch*", 960, 150, 70); kin(t2, A("But here's the catch"), { times: wordTimes("But here's the catch") });
    draw(gl, A('Money could only'), 1.0); fin(lg, A('Money could only', .9));
    draw(ml, A('grow as fast'), 1.3); fin(lm, A('grow as fast', 1.2));
    const stack = G(S, {}); for (let k = 0; k < 3; k++) goldBar(stack, 1460 - k * 10, 500 - k * 44, .55, { label: false }); pop(stack, A('gold pile'), { sfx: 'clink' });
    const cap = sv('circle', { cx: 860, cy: 640, r: 22, fill: '#E2614B', opacity: 0 }, g); pop(cap, A('gold pile', .4), { sfx: 'thud' }); pulse(cap, A('gold pile', .8), 1.4, 2); }

  // 2. bank run: the queue grows, the vault is too small
  { const tNE = A("There's never enough"); const S = shot(tPanic, tEm, { tr: 'slide' }); const g = G(S, { opacity: 1 });
    const bank = G(S, {}); sv('path', { d: 'M1380,300 L1640,220 L1900,300 Z', fill: '#C9CFDA', stroke: '#6C7690', 'stroke-width': 6 }, bank);
    sv('rect', { x: 1390, y: 300, width: 500, height: 420, fill: '#DDE2EA', stroke: '#6C7690', 'stroke-width': 6 }, bank);
    for (let k = 0; k < 4; k++) sv('rect', { x: 1425 + k * 120, y: 330, width: 40, height: 300, fill: '#B5BDCC' }, bank);
    sv('rect', { x: 1560, y: 560, width: 160, height: 160, fill: '#4B5570' }, bank); svgT(bank, 'BANK', 1640, 285, 34, { c: '#4B5570', font: 'Inter', w: 900, ls: '.2em' });
    slideIn(bank, tPanic, 400, 0);
    const vg = G(S, { opacity: 1 }); const vault = goldBar(vg, 1640, 690, .6); pop(vault, tPanic + .4, { sfx: 'clink' });
    const t = T(S, 'Everyone wants their *gold* back', 760, 160, 64); kin(t, A('everyone wants'));
    const ppl = ['🧍', '🧍‍♀️', '🧍‍♂️', '🧍', '🧍‍♀️', '🧍‍♂️', '🧍', '🧍‍♀️', '🧍‍♂️', '🧍'];
    ppl.forEach((p, k) => { const e = E(S, p, 1270 - k * 115, 640, 150); pop(e, A('everyone wants', k * .38), { y0: -60, sfx: k % 3 ? false : 'pop', vol: .4 }); bob(e, A('everyone wants', k * .38 + .5), tEm + .3, 5, .5 + k * .03); });
    stamp(T(S, '_NOT ENOUGH GOLD_', 1000, 420, 88, { color: '#E2614B' }), tNE, { r: -6 }); }

  // 3. emergencies, wars: the link keeps getting cut; Britain 1931
  { const t31 = A('Britain cut it'); const S = shot(tEm, tAm, { tr: 'zoom' }); const g = G(S, { opacity: 1 });
    const n = note(g, 640, 430, 320, { num: '1' }); const gb = goldBar(g, 1300, 440, 1.3);
    const chain = G(S, {}); for (let k = 0; k < 6; k++) sv('ellipse', { cx: 840 + k * 50, cy: 435, rx: 30, ry: 15, fill: 'none', stroke: '#C9CFDA', 'stroke-width': 8 }, chain);
    pop(n, tEm, { s0: .6 }); pop(gb, tEm + .2, { s0: .6, sfx: 'clink' }); fin(chain, tEm + .3);
    const war = E(S, '⚔️', 960, 230, 130); pop(war, A('especially wars'), { sfx: 'clang' }); wiggle(war, A('especially wars', .4), 12, 3);
    tl.to(chain, { opacity: .15, duration: .15, yoyo: true, repeat: 3 }, A('kept suspending')); sfx('snap', A('kept suspending', .1), .7);
    const t = T(S, 'Countries kept *suspending* the link', 960, 690, 62); kin(t, A('countries kept'));
    out([n, gb, chain, war, t], t31 - .15, .25);
    const card = P(S, 610, 230, 700, 420, { bg: '#F3EBDD', border: '#C9CFDA' }); const ci = mk('div', {}, card);
    ci.innerHTML = '<div style="font:800 44px Inter;color:#4B5570;text-align:center;margin-top:44px;letter-spacing:.2em">BRITAIN</div><div style="font:800 190px Brico;color:#101A2E;text-align:center;line-height:220px">1931</div>';
    slideIn(card, t31, 0, 300, { sfx: 'flip' }); const fl = E(S, '🇬🇧', 1310, 250, 130); pop(fl, t31 + .3);
    stamp(T(S, '_LINK CUT_', 1180, 600, 80, { color: '#E2614B' }), A('for good'), { r: -10 }); }

  // 4. Executive Order 6102 types itself
  { const S = shot(tAm, tHand, { tr: 'up', push: 1.04 }); const t = T(S, 'America went *further*', 960, 140, 72); kin(t, tAm, { times: wordTimes('America went further') });
    const doc = P(S, 560, 230, 800, 600, { bg: '#F3EBDD', border: '#C9CFDA' }); slideIn(doc, A('On April'), 0, 400, { sfx: 'flip' });
    const l1 = mk('div', {}, doc), l2 = mk('div', {}, doc), l3 = mk('div', {}, doc), l4 = mk('div', {}, doc);
    Object.assign(l1.style, { position: 'absolute', left: '60px', top: '60px', font: '800 50px Brico', color: '#101A2E' });
    Object.assign(l2.style, { position: 'absolute', left: '60px', top: '140px', font: '800 40px Inter', color: '#E2614B' });
    Object.assign(l3.style, { position: 'absolute', left: '60px', top: '230px', width: '680px', height: '14px', background: '#C9CFDA', borderRadius: '7px' });
    Object.assign(l4.style, { position: 'absolute', left: '60px', top: '270px', width: '540px', height: '14px', background: '#C9CFDA', borderRadius: '7px' });
    c3_type(l2, 'April 5, 1933', A('April 5th'), .9);
    fin(l3, A('Great Depression'), .3); fin(l4, A('Great Depression', .3), .3);
    const dep = I(S, 'THE GREAT DEPRESSION', 960, 700, 36, { color: '#8D98B0', ls: '.2em', weight: 800 }); fin(dep, A('Great Depression'), .4);
    c3_type(l1, 'EXECUTIVE ORDER 6102', A('signed Executive'), 1.2);
    const sig = sv('path', { d: 'M760,640 q40,-60 70,0 t70,0 q30,-50 60,-10 t60,0', stroke: '#101A2E', 'stroke-width': 6, fill: 'none', 'stroke-linecap': 'round', opacity: 0 }, S.svg); draw(sig, A('signed'), .7);
    stamp(T(S, '_ORDER_', 1240, 330, 70, { color: '#E2614B' }), A('6102', .2), { r: 12 }); }

  // 5. hand in your gold by May 1st, at 20.67 an ounce
  { const S = shot(tHand, tHoard, { tr: 'slide' }); const g = G(S, { opacity: 1 });
    const t = T(S, 'Hand in your *gold* by May 1', 960, 140, 68); kin(t, A('hand most'));
    const items = [coin(g, 380, 470, 70), goldBar(g, 620, 480, .9), coin(g, 860, 470, 70, { mark: '$' })];
    items.forEach((it, k) => pop(it, A(['gold coins', 'bars and', 'gold certificates'][k]), { sfx: k === 2 ? 'pop' : 'clink' }));
    const bank = E(S, '🏦', 1480, 470, 260); pop(bank, A('banking system'));
    items.forEach((it, k) => tl.to(it, { x: 1100 - k * 240, scale: .2, opacity: 0, duration: .6, ease: 'power2.in' }, A('by May', k * .15)));
    sfx('whoosh', A('by May'), .6); pulse(bank, A('by May', .6), 1.12, 1);
    const tag = P(S, 660, 640, 600, 150, { bg: '#E9B44C', border: '#7A4E0E' }); const tt = mk('div', {}, tag);
    Object.assign(tt.style, { font: '800 64px Brico', color: '#101A2E', textAlign: 'center', lineHeight: '150px' }); tt.textContent = '20.67 dollars / oz';
    pop(tag, A('at 20 dollars'), { sfx: 'register', r0: -8 }); }

  // 6. the penalty
  { const S = shot(tHoard, tDin, { tr: 'zoom' }); const t = T(S, 'Hoard it?', 960, 160, 90); kin(t, tHoard, { times: wordTimes('Hoard it') });
    const c1 = P(S, 300, 330, 600, 330, { bg: '#16233D' }), c2 = P(S, 1020, 330, 600, 330, { bg: '#16233D' });
    const a1 = mk('div', {}, c1), a2 = mk('div', {}, c2);
    a1.innerHTML = '<div style="font:900 40px Inter;color:#8D98B0;text-align:center;margin-top:46px;letter-spacing:.2em">FINE</div><div class="n1" style="font:800 110px Brico;color:#E9B44C;text-align:center">10,000</div><div style="font:800 36px Inter;color:#F3EBDD;text-align:center">dollars</div>';
    a2.innerHTML = '<div style="font:900 40px Inter;color:#8D98B0;text-align:center;margin-top:46px;letter-spacing:.2em">PRISON</div><div class="n2" style="font:800 110px Brico;color:#E2614B;text-align:center">10</div><div style="font:800 36px Inter;color:#F3EBDD;text-align:center">up to 10 years</div>';
    slideIn(c1, A('10,000'), -300, 0); count(c1.querySelector('.n1'), 0, 10000, A('10,000'), .9);
    slideIn(c2, A('up to ten'), 300, 0); count(c2.querySelector('.n2'), 0, 10, A('up to ten'), .8);
    const both = T(S, '...or *both*', 960, 780, 74); kin(both, A('or both')); shake(A('or both', .3), .8); sfx('stamp', A('or both', .3)); }

  // 7. dinner party gag
  { const S = shot(tDin, tYear, { tr: 'fade', push: 1.02 }); const g = G(S, { opacity: 1 });
    sv('ellipse', { cx: 960, cy: 640, rx: 560, ry: 90, fill: '#6B3E22', stroke: '#2E190C', 'stroke-width': 6 }, g);
    sv('rect', { x: 640, y: 660, width: 24, height: 160, fill: '#4A2A16' }, g); sv('rect', { x: 1256, y: 660, width: 24, height: 160, fill: '#4A2A16' }, g);
    const faces = ['😬', '😐', '🫢', '😶']; faces.forEach((f, k) => { const e = E(S, f, 560 + k * 270, 460, 170); pop(e, tDin + k * .12, { sfx: k ? false : 'pop' }); });
    const props = ['🍷', '🍽️', '🍷']; props.forEach((p, k) => { const e = E(S, p, 720 + k * 240, 610, 80); fin(e, tDin); });
    const b = T(S, '...', 1600, 260, 120, { color: '#8D98B0' }); kin(b, A('dinner party'), { sfx: 'pop' }); sfx('crickets', A('dinner party', .2), .8); }

  // 8. a year later: price tag 20.67 -> 35, 41% less gold per dollar
  { const S = shot(tYear, tLeg, { tr: 'wipe' }); const t = T(S, 'Official price of gold', 960, 140, 60, { color: '#8D98B0' }); kin(t, tYear);
    const tag = P(S, 560, 210, 800, 220, { bg: '#E9B44C', border: '#7A4E0E' }); const n = mk('div', {}, tag);
    Object.assign(n.style, { font: '800 120px Brico', color: '#101A2E', textAlign: 'center', lineHeight: '220px' });
    pop(tag, tYear + .2, { sfx: 'register' }); count(n, 20.67, 35, A('jumped to'), 1.0, { f: '2', suf: ' / oz' }); sfx('register', A('35 dollars'), .8);
    const same = T(S, 'Same *gold.*', 960, 500, 62); kin(same, A('Same gold'));
    const r1 = P(S, 480, 590, 960, 70, { bg: '#E9B44C', border: '#7A4E0E' }), r2 = P(S, 480, 700, 960, 70, { bg: '#E9B44C', border: '#7A4E0E' });
    const l1 = I(S, 'Gold per dollar: before', 470, 625, 30, { align: 'right', color: '#8D98B0' }), l2 = I(S, 'after', 470, 735, 30, { align: 'right', color: '#8D98B0' });
    fin(r1, A('But each dollar')); fin(l1, A('But each dollar')); fin(r2, A('But each dollar', .3)); fin(l2, A('But each dollar', .3));
    tl.fromTo(r2, { width: 960 }, { width: 566, duration: .9, ease: 'power3.inOut', ...IR }, A('41 percent', -.2));
    const pct = T(S, '_-41%_', 1560, 735, 70, { color: '#E2614B' }); stamp(pct, A('41 percent', .4), { r: 0 }); }

  // 9. legal again: Dec 31, 1974
  { const S = shot(tLeg, tOrd, { tr: 'up' }); const g = G(S, { opacity: 1 });
    const cal = P(S, 1080, 220, 420, 460, { bg: '#F3EBDD', border: '#C9CFDA' }); const ci = mk('div', {}, cal);
    ci.innerHTML = '<div style="background:#E2614B;height:100px;border-radius:18px 18px 0 0;color:#fff;font:800 50px Inter;display:flex;align-items:center;justify-content:center;letter-spacing:.12em">DEC 31</div><div style="font:800 170px Brico;color:#101A2E;text-align:center;line-height:250px">1974</div>';
    const gb = goldBar(g, 620, 450, 1.8); pop(gb, tLeg, { s0: .6, sfx: 'clink' }); const lk = lock(g, 620, 360, .8); pop(lk.g, tLeg + .3, { sfx: 'clang' });
    const t = T(S, 'Gold bars: *illegal* to own', 620, 720, 54); kin(t, A('legally own'));
    slideIn(cal, A('until the last day'), 300, 0, { sfx: 'flip' });
    tl.to(lk.g, { y: -60, opacity: 0, rotation: 20, transformOrigin: '50% 50%', duration: .5, ease: 'power2.in' }, A('1974', .2)); sfx('snap', A('1974', .2), .6); }

  // 10. re-hook: people locked out, governments not
  { const tGov = A('But foreign governments'), tLoop = A('that loophole'); const S = shot(tOrd, tEnd, { tr: 'zoom' }); const g = G(S, { opacity: 1 });
    const door = (x, label, col) => { const d = G(S, {}); sv('rect', { x: x - 170, y: 230, width: 340, height: 500, rx: 14, fill: '#16233D', stroke: '#3B5384', 'stroke-width': 8 }, d);
      const leaf = sv('rect', { x: x - 150, y: 250, width: 300, height: 480, rx: 8, fill: col, stroke: '#2A3A5C', 'stroke-width': 5 }, d); svgT(d, label, x, 790, 40, { font: 'Inter', w: 900, ls: '.14em' }); return { d, leaf }; };
    const D1 = door(620, 'PEOPLE', '#4B5570'), D2 = door(1300, 'GOVERNMENTS', '#4B5570');
    const top = G(S, { opacity: 1 }); pop(D1.d, tOrd, { s0: .8 }); const lk = lock(top, 620, 470, 1.1); pop(lk.g, A('locked out'), { s0: 2, sfx: 'clang', ease: 'power4.in', d: .25 }); shake(A('locked out', .25), .8);
    pop(D2.d, tGov, { s0: .8 }); const glow = sv('rect', { x: 1150, y: 250, width: 300, height: 480, fill: '#E9B44C', opacity: 0 }, top);
    tl.to(D2.leaf, { attr: { width: 40 }, duration: .6, ease: 'power3.inOut' }, A("governments weren't", .2)); tl.to(glow, { opacity: .55, duration: .5 }, A("governments weren't", .3)); sfx('sparkle', A("governments weren't", .3), .7);
    const gb = goldBar(top, 1300, 520, .8); pop(gb, A("governments weren't", .6), { sfx: 'clink' });
    const t = T(S, 'That *loophole* broke the system', 960, 130, 70); kin(t, tLoop);
    const crack = sv('path', { d: 'M960,160 L930,330 L990,480 L940,640 L975,800', stroke: '#E2614B', 'stroke-width': 10, fill: 'none', 'stroke-linejoin': 'round', opacity: 0 }, top);
    draw(crack, A('broke the whole'), .35); shake(A('broke the whole', .1), 1.4); sfx('crack', A('broke the whole')); flash(A('broke the whole', .1), .3); }
}
