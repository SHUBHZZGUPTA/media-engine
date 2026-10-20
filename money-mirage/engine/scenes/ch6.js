// CHAPTER 6: WHY THE WORLD STILL RUNS ON DOLLARS (lines 35-40)
function c6_bubble(S, x, y, w, html, o) { o = o || {}; const p = P(S, x, y, w, o.h || 86, { bg: o.bg || '#26344F', border: o.border || '#3A4A6C' });
  p.style.borderRadius = o.me ? '30px 30px 6px 30px' : '30px 30px 30px 6px'; const t = mk('div', { class: 'i' }, p); t.innerHTML = html;
  Object.assign(t.style, { fontSize: (o.fs || 34) + 'px', left: '28px', top: '22px', color: o.c || '#F3EBDD' }); t.style.visibility = 'inherit'; return p; }

function ch6() {
  const c0 = CH(6).a - .3, end = LB(40) + .35;
  const t2 = A('In 1974', -.3), t3 = A('No formal treaty', -.3), t4 = A('The bigger reason', -.3), t5 = A('If every bank', -.4), t6 = A('The numbers are wild', -.3),
    t7 = A('Central banks keep', -.3), t8 = A('Behind that sits', -.3), t9 = A('But gold never', -.3);
  startCh(6);

  // 1. part of it is oil: barrel rolls in
  { const S = shot(c0, t2, { tr: 'fade' }); const b = E(S, '🛢️', 960, 470, 300);
    tl.fromTo(b, { autoAlpha: 0, x: -1100, rotation: -540 }, { autoAlpha: 1, x: 0, rotation: 0, duration: 1.1, ease: 'power3.out', ...IR }, c0 + .1); sfx('thud', c0 + 1.1); gsap.set(b, { autoAlpha: 0 }); ev(c0 + .1, 'roll');
    const t = T(S, 'Part of it: *oil*', 960, 160, 90); kin(t, A('Part of it'));
    wiggle(b, A('oil', .1), 5, 2); }

  // 2. 1974: US and Saudi Arabia, informal understanding
  { const S = mapShot(t2, t3, { tr: 'zoom' }); camSet(S, -16, 33, .42); camTo(S, -16, 33, .5, t2, t3 - t2 + .5, 'sine.inOut');
    pin(S, -77.04, 38.9, A('the US'), { r: 30 }); mlabel(S, 'USA', -77.04, 38.9, A('the US', .1), { fs: 80, dy: -70 });
    pin(S, 46.7, 24.7, A('Saudi Arabia'), { r: 30 }); mlabel(S, 'SAUDI ARABIA', 46.7, 24.7, A('Saudi Arabia', .1), { fs: 80, dy: -70 });
    const yr = T(S, '*1974* · an informal understanding', 960, 130, 64); kin(yr, A('In 1974'));
    marc(S, 46.7, 24.7, -77.04, 38.9, A('Saudi oil money'), 1.3, { c: '#E9B44C', w: 22, bend: .28 });
    const l1 = T(S, '🛢️ Oil money → *US bonds*', 960, 760, 54); kin(l1, A('Saudi oil money'));
    marc(S, -77.04, 38.9, 46.7, 24.7, A('America offered'), 1.3, { c: '#E2614B', w: 22, bend: .12 });
    const l2 = T(S, '_Military support_ → Saudi Arabia', 960, 840, 54); kin(l2, A('America offered')); }

  // 3. no formal treaty, but oil trades in dollars
  { const S = shot(t3, t4, { tr: 'slide' }); const doc = P(S, 330, 190, 560, 600, { bg: '#F3EBDD', border: '#C9CFDA' });
    const h = mk('div', { class: 't' }, doc); h.textContent = 'TREATY'; Object.assign(h.style, { fontSize: '64px', left: '0', right: '0', top: '50px', textAlign: 'center', color: '#101A2E' });
    for (let k = 0; k < 7; k++) { const ln = mk('div', {}, doc); Object.assign(ln.style, { position: 'absolute', left: '60px', top: (170 + k * 50) + 'px', width: (420 - (k % 3) * 70) + 'px', height: '12px', borderRadius: '6px', background: '#C9CFDA' }); }
    slideIn(doc, t3 + .05, 0, 300, { sfx: 'flip' });
    const st = T(S, '_NO FORMAL TREATY_', 610, 500, 70, { color: '#E2614B' }); stamp(st, A('treaty', .1), { r: -12, amp: 1.2 });
    const b = E(S, '🛢️', 1260, 450, 190); pop(b, A('but oil has'));
    const eq = T(S, '= *$*', 1560, 460, 170); kin(eq, A('traded in dollars'), { sfx: 'register' });
    const k = T(S, 'Traded in *dollars* ever since', 1400, 760, 52); kin(k, A('traded in dollars')); }

  // 4. network effect: the family group chat
  { const S = shot(t4, t5, { tr: 'up' }); const ph = P(S, 1060, 120, 560, 740, { bg: '#0D1628', border: '#C9CFDA' }); ph.style.borderRadius = '56px'; ph.style.borderWidth = '8px';
    const hd = mk('div', { class: 'i' }, ph); hd.innerHTML = '👨‍👩‍👧‍👦 <b>Family</b>'; Object.assign(hd.style, { fontSize: '36px', left: '40px', top: '40px', visibility: 'inherit' });
    slideIn(ph, t4 + .1, 0, 600, { sfx: 'whoosh' });
    const t = T(S, 'Network *effect*', 520, 330, 104); kin(t, A('network effect'));
    const sub = T(S, 'Everyone ends up on the same app', 520, 460, 44, { color: '#8D98B0' }); kin(sub, A('whole family'));
    const bs = [[1100, 210, 380, 'Dinner on Sunday? 🍲', A('your whole family'), {}], [1240, 320, 300, '👍👍', A('ends up', .1), { me: true, bg: '#2C5B3C' }],
      [1100, 430, 420, 'Who has the charger?', A('messaging app'), {}],
      [1100, 550, 460, 'Good morning! 🌞🌻🌼', A('good-morning memes', -.2), { bg: '#E9B44C', c: '#101A2E', h: 150, fs: 42 }]];
    bs.forEach(([x, y, w, html, at, o]) => { const b = c6_bubble(S, x, y, w, html, o); pop(b, at, { s0: .5, y0: 30, sfx: 'pop' }); });
    const last = ph.parentNode.lastChild; wiggle(last, A('memes', .2), 5, 3); sfx('boing', A('memes', .2), .5);
    const ww = T(S, '...every single day', 1340, 770, 40, { color: '#E9B44C' }); kin(ww, A('memes', .3)); }

  // 5. every bank, exporter, central bank -> dollars -> you
  { const S = shot(t5, t6, { tr: 'zoom' }); const g = G(S, { opacity: 1 }); const cx = 960, cy = 470;
    const hub = coin(g, cx, cy, 120, { mark: '$' }); pop(hub, t5 + .1, { s0: .3, sfx: 'clink' });
    const nodes = [['🏦', 'Every bank', 420, 230, A('every bank')], ['🚢', 'Every exporter', 1500, 230, A('every exporter')], ['🏛️', 'Every central bank', 420, 720, A('every central bank')], ['🙋', 'You', 1500, 720, A('the easiest thing')]];
    nodes.forEach(([em, lab, x, y, at], k) => { const ln = sv('path', { d: `M${x},${y} L${cx},${cy}`, stroke: k === 3 ? '#E2614B' : '#E9B44C', 'stroke-width': 8, 'stroke-dasharray': '18 12', opacity: 0 }, g);
      const e = E(S, em, x, y - 20, 130); pop(e, at, { sfx: 'pop' }); const l = I(S, lab, x, y + 80, 36, { weight: 800 }); fin(l, at + .1, .3);
      tl.fromTo(ln, { opacity: 0 }, { opacity: 1, duration: .3, ...IR }, at + .25); tl.fromTo(ln, { attr: { 'stroke-dashoffset': 0 } }, { attr: { 'stroke-dashoffset': -300 }, duration: t6 - at + .5, ease: 'none', ...IR }, at + .25); });
    tl.to(hub, { scale: 1.25, transformOrigin: '50% 50%', duration: .3, yoyo: true, repeat: 1 }, A('use dollars too')); sfx('register', A('use dollars too'), .7);
    const k = T(S, '...use *dollars* too', 960, 140, 64); kin(k, A('use dollars too', -.3)); }

  // 6. 89% of trades, 9.6 trillion a day
  { const S = shot(t6, t7, { tr: 'wipe' }); const R = 210, C = 2 * Math.PI * R;
    const t = T(S, 'The numbers are *wild*', 960, 130, 74); kin(t, t6 + .1);
    const tag = P(S, 820, 220, 280, 70, { bg: '#E2614B', border: '#E2614B' }); const tt = mk('div', { class: 'i' }, tag); tt.textContent = 'APRIL 2025'; Object.assign(tt.style, { fontSize: '34px', left: '0', right: '0', top: '14px', textAlign: 'center', fontWeight: 900, letterSpacing: '.12em', visibility: 'inherit' });
    stamp(tag, A('April 2025', -.2), { r: -3, amp: .5 });
    sv('circle', { cx: 560, cy: 570, r: R, fill: 'none', stroke: '#26344F', 'stroke-width': 52 }, S.svg);
    const ring = sv('circle', { cx: 560, cy: 570, r: R, fill: 'none', stroke: '#E9B44C', 'stroke-width': 52, 'stroke-dasharray': C, 'stroke-dashoffset': C, transform: 'rotate(-90 560 570)' }, S.svg);
    const ap = A('89 percent', -.3); tl.fromTo(ring, { attr: { 'stroke-dashoffset': C } }, { attr: { 'stroke-dashoffset': C * .11 }, duration: 1.4, ease: 'power2.out', ...IR }, ap);
    const n = I(S, '0%', 560, 570, 110, { weight: 900 }); fin(n, ap, .2); count(n, 0, 89, ap, 1.4, { suf: '%' });
    const l1 = I(S, 'of all currency trades', 560, 850, 36, { color: '#8D98B0' }); fin(l1, A('all currency trades'), .3);
    const big = I(S, '0', 1380, 540, 150, { weight: 900, color: '#E9B44C' }); const at = A('9.6 trillion', -.3); fin(big, at, .2); count(big, 0, 9.6, at, 1.6, { f: '1', pre: '$', suf: 'T' });
    const l2 = I(S, 'a day in currency markets', 1380, 660, 44, { weight: 800 }); fin(l2, A('dollars a day'), .3);
    const ds = []; for (let k = 0; k < 6; k++) { const e = E(S, '💵', 1150 + k * 95, 800, 64); ds.push(e); pop(e, A('dollars a day') + k * .1, { y0: -200, sfx: false }); } sfx('register', A('dollars a day'), .6); }

  // 7. reserves leaderboard
  { const S = shot(t7, t8, { tr: 'slide' }); const t = T(S, "Central banks' known *reserves*", 960, 150, 70); kin(t, t7 + .1);
    const rows = [['🇺🇸', 'US DOLLAR', 57, '#E9B44C', A('57 percent', -.3)], ['🇪🇺', 'EURO', 20, '#7FB58A', A('The euro')]];
    rows.forEach(([fl, nm, v, c, at], k) => { const y = 330 + k * 230;
      const f = E(S, fl, 230, y + 50, 100); pop(f, at - .1, { sfx: false }); const lab = I(S, nm, 310, y - 20, 40, { align: 'left', weight: 900, ls: '.12em' }); fin(lab, at - .1, .3);
      const bar = mk('div', {}, S.stg); Object.assign(bar.style, { position: 'absolute', left: '310px', top: (y + 20) + 'px', width: (v / 60 * 1150) + 'px', height: '80px', borderRadius: '14px', background: c, transformOrigin: '0 50%', visibility: 'hidden' });
      tl.fromTo(bar, { autoAlpha: 1, scaleX: 0 }, { scaleX: 1, duration: 1.3, ease: 'power3.out', ...IR }, at); ev(at, 'bar'); sfx('swoosh', at, .5);
      const n = I(S, '0%', 330 + v / 60 * 1150 + 40, y + 60, 64, { align: 'left', weight: 900, color: c }); fin(n, at, .2); count(n, 0, v, at, 1.3, { suf: '%' }); });
    const two = T(S, '_2nd place_', 1350, 610, 48); kin(two, A('in second place')); }

  // 8. the bond market: a safe harbour
  { const S = shot(t8, t9, { tr: 'up' }); const g = G(S, { opacity: 1 });
    const waves = sv('g', {}, g); for (let k = 0; k < 3; k++) { let d = `M-200,${700 + k * 55}`; for (let x = 0; x < 30; x++) d += ' q60,-24 120,0 t120,0'; sv('path', { d, fill: 'none', stroke: ['#3B7CB0', '#2C6E9E', '#1F5580'][k], 'stroke-width': 24 - k * 4 }, waves); }
    fin(waves, t8, .3); tl.fromTo(waves, { x: 0 }, { x: -240, duration: t9 - t8 + .5, ease: 'none', ...IR }, t8);
    const pier = sv('g', {}, g); sv('rect', { x: 1180, y: 540, width: 620, height: 50, fill: '#8A5530', stroke: '#2E190C', 'stroke-width': 5 }, pier);
    for (let k = 0; k < 5; k++) sv('rect', { x: 1200 + k * 140, y: 590, width: 22, height: 170, fill: '#6B3E22' }, pier);
    slideIn(pier, t8 + .1, 400, 0, { sfx: 'thud' }); const anc = E(S, '⚓', 1490, 430, 140); pop(anc, A('market for US'));
    const lb = T(S, 'US government *bonds*', 1490, 300, 56); kin(lb, A('market for US'));
    const t = T(S, 'A huge, easy-to-trade market', 600, 160, 58); kin(t, A('a huge'));
    const storm = E(S, '⛈️', 260, 330, 170); pop(storm, A('gets scared', -.2), { sfx: 'crack' }); shake(A('gets scared'), .7); flash(A('gets scared'), .2);
    for (let k = 0; k < 5; k++) { const m = E(S, '💵', 300 + k * 70, 600 - (k % 2) * 60, 70); pop(m, A("that's where") + k * .08, { sfx: false }); tl.to(m, { x: 1000 - k * 40, y: -120 + k * 10, duration: 1.2, ease: 'power2.inOut' }, A("that's where") + .3 + k * .1); }
    sfx('whoosh', A("that's where", .3), .6);
    const sh = T(S, '*Safe harbour*', 600, 260, 70); kin(sh, A('traditionally run', -.4)); }

  // 9. gold never left: central-bank gold stacks + Goldie returns
  { const S = shot(t9, end, { tr: 'zoom', push: 1.03 }); const g = G(S, { opacity: 1 });
    const t = T(S, 'Gold never really *left*', 700, 130, 80); kin(t, t9 + .1);
    const big = goldBar(g, 700, 520, 2.6); pop(big, A('gold never', .1), { s0: 3, ease: 'power4.in', d: .3, sfx: 'clink' }); shake(A('gold never', .4), .7);
    tl.to(big, { scale: .2, opacity: 0, y: 200, transformOrigin: '50% 50%', duration: .45, ease: 'power3.in' }, A('Central banks bought', -.3));
    sv('path', { d: 'M150,800 L1250,800', stroke: '#3A4A6C', 'stroke-width': 6 }, g);
    const cols = [['2022', 5, '1,000+ t', A('2022', -.2)], ['2023', 5, '1,000+ t', A('2023', -.2)], ['2024', 5, '1,000+ t', A('2024', -.2)], ['2025', 4.3, '863 t', A('863', -.2)]];
    cols.forEach(([yr, n, lab, at], k) => { const x = 300 + k * 270; const yl = svgT(g, yr, x, 860, 44, { c: '#8D98B0', font: 'Inter', w: 800 }); pop(yl, at - .1, { sfx: false });
      const nb = Math.round(n); for (let j = 0; j < nb; j++) { const scl = j === nb - 1 && n % 1 ? .3 : 1; const bar = goldBar(g, x, 770 - j * 86, .95, { label: false }); if (scl !== 1) bar.outer.setAttribute('transform', `translate(${x},${770 - j * 86 + 28}) scale(.95,.33)`);
        tl.fromTo(bar, { autoAlpha: 0, y: -300 }, { autoAlpha: 1, y: 0, duration: .3, ease: 'bounce.out', ...IR }, at + j * .11); gsap.set(bar, { autoAlpha: 0 }); sfx('clink', at + j * .11 + .2, .35); }
      ev(at, 'stack'); const l = svgT(g, lab, x, 770 - nb * 86 - 20, 40, { c: '#E9B44C' }); pop(l, at + nb * .11 + .1, { sfx: false }); });
    const sub = T(S, 'Central banks bought', 700, 230, 46, { color: '#8D98B0' }); kin(sub, A('Central banks bought'));
    const gIn = LA(40) - .8; charIn('G', gIn, 'R'); idle('G', gIn + .5, LB(40) + 1.4); talk('G', 40);
    tl.fromTo(CHR.G.M.spark, { opacity: 0, scale: .4, transformOrigin: '50% 50%' }, { opacity: 1, scale: 1.1, duration: .35, ease: 'back.out(3)', ...IR }, LA(40)); sfx('sparkle', LA(40));
    tl.to(CHR.G.M.spark, { opacity: 0, duration: .4 }, LB(40) + .9); tl.to(CHR.G.M.brow, { y: -10, duration: .2, yoyo: true, repeat: 1 }, LA(40));
    charOut('G', LB(40) + 1.2); }
}
