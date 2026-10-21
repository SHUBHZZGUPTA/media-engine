// CHAPTER 6: WHY THE WORLD STILL RUNS ON DOLLARS (lines 35-40) — archival/painted style
function c6_panel(S, x, y, w, h, o) { o = o || {}; const d = mk('div', { class: 'panel' }, S.stg); Object.assign(d.style, { left: x + 'px', top: y + 'px', width: w + 'px', height: h + 'px', background: o.bg || 'rgba(10,17,32,.84)', borderColor: o.border || 'rgba(233,180,76,.45)' }); if (o.radius) d.style.borderRadius = o.radius; d.style.visibility = 'hidden'; return d; }
function c6_txt(parent, txt, css) { const d = mk('div', {}, parent); d.textContent = txt; Object.assign(d.style, Object.assign({ position: 'absolute', fontFamily: 'Inter', fontWeight: 800, color: '#F3EBDD', whiteSpace: 'nowrap' }, css)); return d; }
function ch6() {
  const c = CH(6); const t0 = c.a - .3;
  const t74 = A('In 1974'), tSaudi = A('Saudi oil money'), tNoT = A('No formal treaty'), tNet = A('The bigger reason'), tEvery = A('If every bank'),
    tWild = A('The numbers are wild'), tRes = A('Central banks keep'), tBeh = A('Behind that sits'), tGold = A('But gold never really left'), tG = LA(40), tEnd = LB(40) + .35;
  startCh(6);

  // 1. oil
  { const S = photo(t0, t74, 'oil_tanker.jpg', { grade: 'paint', kb: [1.0, 1.14], to: [-2, -1] });
    lower(S, 'PART OF THE ANSWER', '*Oil*', A('Part of it is oil'), { size: 130 }); sfx('splash', A('Part of it is oil'), .4); }
  // 2. 1974 informal understanding: US <-> Saudi Arabia
  { const S = mapShot(t74, tSaudi, { tr: 'fade' }); camSet(S, -18, 33, .52); camTo(S, -15, 31, .6, t74, tSaudi - t74, 'sine.inOut');
    pin(S, -77.04, 38.9, t74 + .3, { rep: 1 }); mlabel(S, 'UNITED STATES', -77.04, 38.9, t74 + .4, { fs: 60 });
    pin(S, 46.7, 24.7, A('Saudi Arabia', -.1), { c: '#F3EBDD', rep: 1 }); mlabel(S, 'SAUDI ARABIA', 46.7, 24.7, A('Saudi Arabia'), { fs: 60, dy: 110 });
    marc(S, -77.04, 38.9, 46.7, 24.7, A('reached an informal'), 1.2, { w: 14, bend: .22 });
    lower(S, '1974', 'An informal *understanding*', A('reached an informal'), { size: 88 }); }
  // 3. the flows
  { const S = photo(tSaudi, tNoT, 'supertanker.jpg', { grade: 'mono', kb: [1.1, 1.2], to: [-3, 0], tr: 'slide', credit: 'Public domain' });
    const rows = [['Saudi oil money', 'US government bonds', '#E9B44C', A('Saudi oil money')], ['US military support', 'Saudi Arabia', '#E2614B', A('and America offered')]];
    rows.forEach(([l, r, col, at], i) => { const y = 250 + i * 190; const p = c6_panel(S, 160, y, 1600, 140); slideIn(p, at, -120, 0, { sfx: 'swoosh', vol: .4 });
      c6_txt(p, l, { left: '50px', top: '42px', fontSize: '50px', fontFamily: 'Inter' }); c6_txt(p, r, { right: '50px', top: '42px', fontSize: '50px', fontFamily: 'Inter', color: col });
      const ar = sv('path', { d: `M760,${y + 70} L1060,${y + 70}`, stroke: col, 'stroke-width': 8, 'stroke-linecap': 'round', 'marker-end': 'url(#ah' + (i ? 'r' : 'g') + ')', opacity: 0 }, S.svg); draw(ar, at + .4, .6); }); }
  // 4. no formal treaty
  { const S = photo(tNoT, tNet, 'oil_tanker.jpg', { grade: 'paint', kb: [1.25, 1.32], from: [-3, -2], to: [-4, -3], tr: 'fade' }); tl.set(S.img, { filter: GRADES.paint + ' blur(6px) brightness(.55)' }, tNoT - .1);
    const doc = c6_panel(S, 660, 120, 600, 560, { bg: '#EFE6D2', border: '#C9B98F', radius: '6px' }); doc.style.rotate = '-3deg'; slideIn(doc, tNoT - .1, 0, 120, { sfx: 'flip' });
    c6_txt(doc, 'TREATY', { left: '0', right: '0', textAlign: 'center', top: '50px', fontSize: '54px', fontFamily: 'Inter', color: '#3A3326', letterSpacing: '.2em' });
    for (let k = 0; k < 9; k++) { const ln = mk('div', {}, doc); Object.assign(ln.style, { position: 'absolute', left: '60px', width: (k % 3 === 2 ? 300 : 480) + 'px', top: 150 + k * 38 + 'px', height: '10px', borderRadius: '5px', background: 'rgba(58,51,38,.22)' }); }
    const st = T(S, 'NO FORMAL TREATY', 960, 400, 84, { color: '#E2614B' }); st.style.border = '8px solid #E2614B'; st.style.padding = '10px 26px'; st.style.borderRadius = '10px'; stamp(st, A('forced oil into dollars', -.2), { r: -10 });
    lower(S, null, 'Oil has mostly traded in *dollars* ever since', A('but oil has mostly'), { size: 70, y: 840 }); }
  // 5. network effect: the family group chat
  { const S = photo(tNet, tEvery, 'tv_1971.jpg', { grade: 'paint', kb: [1.1, 1.18], to: [-2, 0], tr: 'zoom' }); tl.set(S.img, { filter: GRADES.paint + ' blur(5px) brightness(.55)' }, tNet - .1);
    lower(S, 'THE BIGGER REASON', 'A network *effect*', tNet, { size: 92, y: 330 });
    const ph = c6_panel(S, 1180, 110, 520, 760, { bg: '#0E1626', border: 'rgba(243,235,221,.25)', radius: '46px' }); slideIn(ph, A("It's why your whole family"), 0, 300, { sfx: 'swoosh' });
    c6_txt(ph, 'Family', { left: '0', right: '0', textAlign: 'center', top: '34px', fontSize: '30px' }); c6_txt(ph, '14 members', { left: '0', right: '0', textAlign: 'center', top: '72px', fontSize: '18px', color: '#8D98B0', fontWeight: 600 });
    const B = [['Dinner at 8?', 0, A('same messaging app')], ['On my way', 1, A('same messaging app', .9)], ['Who has the charger', 0, A('including the relative', -.4)]];
    B.forEach(([t, me, at], i) => { const b = mk('div', {}, ph); b.textContent = t; Object.assign(b.style, { position: 'absolute', top: 140 + i * 92 + 'px', [me ? 'right' : 'left']: '30px', padding: '16px 24px', borderRadius: '24px', fontFamily: 'Inter', fontWeight: 600, fontSize: '26px', background: me ? '#E9B44C' : '#22314E', color: me ? '#101A2E' : '#F3EBDD', visibility: 'hidden' }); pop(b, at, { s0: .6, sfx: 'pop', vol: .35 }); });
    const meme = mk('div', {}, ph); Object.assign(meme.style, { position: 'absolute', left: '30px', top: '430px', width: '360px', height: '250px', borderRadius: '22px', background: 'linear-gradient(135deg,#F7C66B,#E2614B 55%,#7A3FB0)', visibility: 'hidden', overflow: 'hidden' });
    c6_txt(meme, 'GOOD', { left: '30px', top: '40px', fontSize: '64px', fontFamily: 'Inter', color: '#FFF6E2', textShadow: '0 4px 0 rgba(0,0,0,.25)' }); c6_txt(meme, 'MORNING!', { left: '30px', top: '110px', fontSize: '64px', fontFamily: 'Inter', color: '#FFF6E2', textShadow: '0 4px 0 rgba(0,0,0,.25)' });
    c6_txt(meme, 'have a blessed day', { left: '32px', top: '196px', fontSize: '24px', fontStyle: 'italic', fontWeight: 600, color: '#FFF6E2' });
    pop(meme, A('good-morning memes', -.1), { s0: .3, sfx: 'pop', vol: .5 }); wiggle(meme, A('good-morning memes', .5), 3, 2); }
  // 6. every bank, exporter and central bank -> dollars
  { const S = photo(tEvery, tWild, 'central_bank.jpg', { grade: 'paint', kb: [1.06, 1.16], to: [0, -2], tr: 'fade' }); tl.set(S.img, { filter: GRADES.paint + ' blur(4px) brightness(.45)' }, tEvery - .1);
    const cx = 960, cy = 460; const ring = sv('circle', { cx, cy, r: 110, fill: '#E9B44C', stroke: '#7A4E0E', 'stroke-width': 10, opacity: 0 }, S.svg); const dl = sv('text', { x: cx, y: cy + 42, 'font-size': 130, 'text-anchor': 'middle', fill: '#5A3A0A', 'font-family': 'Inter', 'font-weight': 800, opacity: 0 }, S.svg); dl.textContent = '$';
    const nodes = [['BANKS', 470, 220, A('every bank')], ['EXPORTERS', 1450, 220, A('every exporter')], ['CENTRAL BANKS', 470, 720, A('every central bank')], ['YOU', 1450, 720, A('the easiest thing for you')]];
    nodes.forEach(([n, x, y, at]) => { const ln = sv('path', { d: `M${x},${y} L${cx},${cy}`, stroke: '#E9B44C', 'stroke-width': 4, 'stroke-dasharray': '14 10', opacity: 0 }, S.svg); fin(ln, at + .2, .4);
      const g = sv('g', {}, S.svg); sv('circle', { cx: x, cy: y, r: 62, fill: '#101A2E', stroke: '#F3EBDD', 'stroke-width': 4 }, g); const tx = sv('text', { x, y: y + 100, 'font-size': 30, 'text-anchor': 'middle', fill: '#F3EBDD', 'font-family': 'Inter', 'font-weight': 800, 'letter-spacing': '.14em' }, g); tx.textContent = n;
      sv('circle', { cx: x, cy: y, r: 16, fill: n === 'YOU' ? '#E2614B' : '#E9B44C' }, g); pop(g, at, { s0: .5, sfx: 'ping', vol: .3 }); });
    pop(ring, tEvery + .2, { s0: .3, sfx: 'clink' }); pop(dl, tEvery + .3, { sfx: false }); pulse(ring, A('is use dollars too'), 1.15, 2);
    const k = T(S, '...is use *dollars* too', 960, 860, 64); kin(k, A('is use dollars too')); }
  // 7. the numbers: 89% and 9.6 trillion a day
  { const S = photo(tWild, tRes, 'trading_room.jpg', { grade: 'paint', kb: [1.0, 1.12], to: [-2, -2], tr: 'slide' }); tl.set(S.img, { filter: GRADES.paint + ' brightness(.5)' }, tWild - .1);
    lower(S, 'APRIL 2025', 'The numbers are *wild*', tWild, { size: 84, y: 230 });
    const R = 190, C = 2 * Math.PI * R, cx = 560, cy = 560; sv('circle', { cx, cy, r: R, fill: 'none', stroke: 'rgba(243,235,221,.15)', 'stroke-width': 44 }, S.svg);
    const ring = sv('circle', { cx, cy, r: R, fill: 'none', stroke: '#E9B44C', 'stroke-width': 44, 'stroke-dasharray': C, 'stroke-dashoffset': C, transform: `rotate(-90 ${cx} ${cy})`, 'stroke-linecap': 'round' }, S.svg);
    const tA = A('about 89 percent'); tl.fromTo(ring, { attr: { 'stroke-dashoffset': C } }, { attr: { 'stroke-dashoffset': C * .11 }, duration: 1.6, ease: 'power2.out', ...IR }, tA);
    const n = I(S, '0', cx, cy, 120, { weight: 900, color: '#F3EBDD' }); fin(n, tA, .2); count(n, 0, 89, tA, 1.6, { suf: '%' });
    const l = I(S, 'of all currency trades involve the dollar', cx, cy + 270, 30, { weight: 800, color: '#C9CFDA' }); fin(l, A('of all currency trades'), .4);
    const tT = A('9.6 trillion'); const m = I(S, '0', 1360, 520, 150, { weight: 900, color: '#E9B44C' }); fin(m, tT - .1, .2); count(m, 0, 9.6, tT, 1.6, { f: '1', pre: '$', suf: 'T' });
    const ml = I(S, 'moved every day', 1360, 640, 40, { weight: 800 }); fin(ml, A('dollars a day'), .4); }
  // 8. reserves: dollar 57% vs euro 20%
  { const S = photo(tRes, tBeh, 'bank_vault_1700s.jpg', { grade: 'paint', kb: [1.05, 1.15], to: [2, -1], tr: 'fade' }); tl.set(S.img, { filter: GRADES.paint + ' blur(5px) brightness(.45)' }, tRes - .1);
    lower(S, 'CENTRAL BANK RESERVES', 'Who holds what', tRes, { size: 80, y: 250 });
    const bars = [['US DOLLAR', 57, '#E9B44C', A('about 57 percent')], ['EURO', 20, '#8D98B0', A('sits around 20')]];
    bars.forEach(([lab, v, col, at], i) => { const y = 430 + i * 190, W = 1300 * v / 60; const bg = sv('rect', { x: 320, y, width: 1300, height: 100, rx: 14, fill: 'rgba(243,235,221,.08)', opacity: 0 }, S.svg); fin(bg, tRes + .3, .4);
      const r = sv('rect', { x: 320, y, width: 0, height: 100, rx: 14, fill: col }, S.svg); tl.fromTo(r, { attr: { width: 0 } }, { attr: { width: W }, duration: 1.3, ease: 'power3.out', ...IR }, at);
      const t = sv('text', { x: 300, y: y + 64, 'font-size': 34, 'text-anchor': 'end', fill: '#F3EBDD', 'font-family': 'Inter', 'font-weight': 800, 'letter-spacing': '.1em', opacity: 0 }, S.svg); t.textContent = lab; fin(t, at - .3, .3);
      const pc = I(S, '0', 340 + W + 90, y + 52, 64, { weight: 900, color: col }); fin(pc, at, .2); count(pc, 0, v, at, 1.3, { pre: '~', suf: '%' }); });
    const k = I(S, 'of known foreign-currency reserves', 960, 860, 34, { weight: 600, color: '#C9CFDA' }); fin(k, A('known foreign-currency reserves'), .4); }
  // 9. US government bonds: where scared money runs
  { const S = photo(tBeh, tGold, 'central_bank.jpg', { grade: 'paint', kb: [1.15, 1.0], to: [0, 1], tr: 'zoom' });
    lower(S, 'US GOVERNMENT BONDS', 'Where scared money *runs*', tBeh, { size: 88 });
    for (let k = 0; k < 10; k++) { const sx = k % 2 ? 1900 : 20, sy = 120 + (k * 97) % 600; const d = sv('circle', { cx: sx, cy: sy, r: 10, fill: '#E9B44C', opacity: 0 }, S.svg);
      const at = A('When the world gets scared', k * .12); tl.fromTo(d, { opacity: 0, attr: { cx: sx, cy: sy } }, { opacity: 1, attr: { cx: 960 + (k % 5 - 2) * 30, cy: 420 + (k % 3) * 20 }, duration: 1.1, ease: 'power2.in', ...IR }, at); tl.to(d, { opacity: 0, duration: .3 }, at + 1.1); }
    sfx('swoosh', A('When the world gets scared'), .4);
    const big = I(S, 'A huge, easy-to-trade market', 960, 300, 44, { weight: 800, color: '#C9CFDA' }); fin(big, A('a huge, easy-to-trade market'), .4);
    const sc = T(S, 'When the world gets *scared...*', 960, 420, 70); kin(sc, A('When the world gets scared')); tl.to(sc, { autoAlpha: 0, duration: .3 }, A('traditionally run', -.3)); }
  // 10. gold never left: central-bank buying + Goldie
  { const S = photo(tGold, tEnd, 'fortknox_vault.jpg', { grade: 'mono', kb: [1.04, 1.14], to: [-2, -1], tr: 'fade', credit: 'Fort Knox Bullion Depository · Kevyn Jacobs · Public domain' }); tl.set(S.img, { filter: GRADES.mono + ' brightness(.55)' }, tGold - .1);
    lower(S, 'CENTRAL BANKS BOUGHT', 'Gold never really *left*', tGold, { size: 84, y: 240 });
    const yrs = [['2022', 1000, '1,000+ t', A('2022')], ['2023', 1000, '1,000+ t', A('2023')], ['2024', 1000, '1,000+ t', A('2024')], ['2025', 863, '863 t', A('another 863')]];
    yrs.forEach(([y, v, lab, at], i) => { const x = 420 + i * 300, H = 420 * v / 1000, base = 800; const r = sv('rect', { x, y: base, width: 180, height: 0, rx: 8, fill: i === 3 ? '#C9963A' : '#E9B44C' }, S.svg);
      tl.fromTo(r, { attr: { y: base, height: 0 } }, { attr: { y: base - H, height: H }, duration: .9, ease: 'power3.out', ...IR }, at); sfx('clink', at + .2, .4);
      const t = sv('text', { x: x + 90, y: base + 46, 'font-size': 34, 'text-anchor': 'middle', fill: '#F3EBDD', 'font-family': 'Inter', 'font-weight': 800, opacity: 0 }, S.svg); t.textContent = y; fin(t, at, .3);
      const lv = sv('text', { x: x + 90, y: base - H - 20, 'font-size': 32, 'text-anchor': 'middle', fill: '#E9B44C', 'font-family': 'Inter', 'font-weight': 800, opacity: 0 }, S.svg); lv.textContent = lab; fin(lv, at + .6, .3); });
    const gIn = tG - .8; charIn('G', gIn, 'R'); idle('G', gIn + .5, tEnd); talk('G', 40);
    tl.to(CHR.G.M.spark, { opacity: 1, duration: .15 }, tG); tl.to(CHR.G.M.spark, { opacity: 0, duration: .4 }, tG + .9); sfx('sparkle', tG, .7);
    tl.to(CHR.G.M.brow, { y: -8, duration: .2, yoyo: true, repeat: 1 }, tG); charOut('G', tEnd - .35); }
}
