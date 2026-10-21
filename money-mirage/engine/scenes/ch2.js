// CHAPTER 2: PAPER ARRIVES (lines 11-16, Bill = 14) — archival/painted documentary style
const c2_sh = el => { el.style.textShadow = '0 4px 26px rgba(0,0,0,.85), 0 2px 4px rgba(0,0,0,.6)'; return el; };
function ch2() {
  const t0 = CH(2).a - .3, tLocal = A('the local coins'), tSo = A('So merchants'), tWhen = A('When some of those'), tAnd24 = A('and in 1024'),
    tThen = A('Then it discovered'), tBill = LA(14) - .55, tFirst = A("That's the first mirage"), tEu = A('Europe caught on'), tTicket = A('Paper was the ticket'),
    tEnd = LB(16) + .35;
  startCh(2);

  // 1. map flight to Chengdu
  { const S = mapShot(t0, tLocal, { tr: 'fade' }); camSet(S, 75, 32, 1.0); camTo(S, 104.07, 30.67, 4.4, t0 + .2, 3.6, 'power2.inOut');
    pin(S, 104.07, 30.67, A('in Chengdu'), { r: 11 }); mlabel(S, 'CHENGDU', 104.07, 30.67, A('in Chengdu', .2), { fs: 24 });
    mlabel(S, 'SICHUAN', 102.2, 31.9, A('Sichuan'), { fs: 16, c: '#E9B44C' });
    lower(S, 'ABOUT A THOUSAND YEARS AGO', 'Chengdu, *China*', A('About a thousand', -.1), { size: 100 }); }

  // 2. iron coins — and a small anvil
  { const tAnv = A('small anvil'); const S = photo(tLocal, tSo, 'chengdu_market.jpg', { grade: 'paint', kb: [1.02, 1.16], from: [0, 0], to: [-2, -3], tr: 'slide' });
    lower(S, 'SICHUAN', 'Coins made of *iron*', A('made of iron', -.2));
    const h = c2_sh(I(S, 'HEAVY · NOT WORTH MUCH', 1800, 170, 32, { align: 'right', weight: 800, ls: '.24em', color: '#E9B44C' })); fin(h, A('Heavy, and not'), .4);
    tl.to(S.stg, { scale: 1.07, duration: .12, ease: 'power4.in' }, tAnv + .25); sfx('thud', tAnv + .3, .9); shake(tAnv + .32, .8);
    const a = c2_sh(T(S, 'Savings = a small *anvil*', 1800, 250, 54, { align: 'right' })); kin(a, A('Carrying your savings'), { st: .07 }); }

  // 3. coins in, paper out — jiaozi
  { const S = photo(tSo, tWhen, 'deposit_shop.jpg', { grade: 'paint', kb: [1.04, 1.2], from: [0, 0], to: [-4, -2], tr: 'fade' });
    lower(S, 'TRUSTED BUSINESSES', 'Coins in. *Paper* out.', A('left their coins', -.2));
    const j = c2_sh(T(S, '*Jiaozi*', 1750, 230, 120, { align: 'right' })); kin(j, A('called jiaozi'), { sfx: 'swoosh', vol: .4 });
    const s = c2_sh(I(S, 'PAPER NOTES', 1750, 320, 28, { align: 'right', weight: 800, ls: '.3em', color: '#C9CFDA' })); fin(s, A('called jiaozi', .4), .4); }

  // 4. shops go bust, the Song government takes over (printing plate)
  { const S = photo(tWhen, tAnd24, 'song_plate.jpg', { grade: 'warm', pos: 'center 38%', kb: [1.0, 1.14], to: [0, -3], tr: 'zoom', credit: 'Northern Song paper-money printing plate · Popolon, CC BY-SA 4.0' });
    const k = c2_sh(I(S, 'SOME BUSINESSES WENT BUST', 960, 170, 30, { weight: 800, ls: '.3em', color: '#E2614B' })); fin(k, A('went bust', -.3), .4); sfx('crack', A('went bust'), .35);
    lower(S, 'THE SONG GOVERNMENT', 'Took over in *1023*', A('the Song government'), { kin: { times: wordTimes('took over in 1023') } }); }

  // 5. 1024 — the world's first government paper money
  { const S = photo(tAnd24, tThen, 'yuan_note.jpg', { grade: 'warm', pos: 'center center', kb: [1.0, 1.12], from: [0, 0], to: [-2, -1], tr: 'fade', credit: 'Yuan banknote and plate, 1287 · PHGCOM, CC BY-SA 3.0' });
    const y = c2_sh(T(S, '*1024*', 1790, 210, 150, { align: 'right' })); kin(y, A('1024', -.05), { s0: .6, sfx: 'stamp', vol: .5 });
    lower(S, "OFTEN CALLED THE WORLD'S FIRST", 'Government *paper money*', A("what's often called"));
    const p = c2_sh(I(S, 'PICTURED: A LATER YUAN-DYNASTY NOTE, 1287', 124, 905, 22, { align: 'left', weight: 800, ls: '.2em', color: '#C9CFDA' })); fin(p, tAnd24 + .6, .5); }

  // 6. the oldest temptation: print more, prices rise
  { const tExtra = A('Extra notes'), tPr = A('Prices kept'); const S = photo(tThen, tBill, 'song_printing.jpg', { grade: 'paint', kb: [1.02, 1.18], from: [0, 0], to: [-3, -3], tr: 'slide' });
    lower(S, 'THE OLDEST TEMPTATION', 'Why not print a little *more?*', A('why not print', -.25), { size: 84, kin: { times: wordTimes('why not print a little more') } });
    const g = G(S, { opacity: 1 }); const ox = 1180, oy = 470, w = 600, h = 300;
    const ax = sv('path', { d: `M${ox},${oy - h} L${ox},${oy} L${ox + w},${oy}`, fill: 'none', stroke: 'rgba(243,235,221,.6)', 'stroke-width': 3, opacity: 0 }, g); fin(ax, tExtra - .4, .4);
    const nl = sv('path', { d: `M${ox},${oy - 30} C${ox + 200},${oy - 50} ${ox + 380},${oy - 120} ${ox + w},${oy - 260}`, fill: 'none', stroke: '#E9B44C', 'stroke-width': 8, 'stroke-linecap': 'round', opacity: 0 }, g); draw(nl, tExtra, 1.4);
    const pl = sv('path', { d: `M${ox},${oy - 15} C${ox + 220},${oy - 25} ${ox + 400},${oy - 90} ${ox + w},${oy - 230}`, fill: 'none', stroke: '#E2614B', 'stroke-width': 8, 'stroke-linecap': 'round', 'stroke-dasharray': '1 0', opacity: 0 }, g); draw(pl, tPr, 1.2);
    const l1 = c2_sh(I(S, 'NOTES', ox + w + 20, oy - 270, 26, { align: 'left', weight: 800, ls: '.2em', color: '#E9B44C' })); fin(l1, tExtra + 1.0, .3);
    const l2 = c2_sh(I(S, 'PRICES', ox + w + 20, oy - 225, 26, { align: 'left', weight: 800, ls: '.2em', color: '#E2614B' })); fin(l2, tPr + .9, .3); sfx('swoosh', tPr, .3); }

  // 7. Bill's cameo — "they printed me"
  { const S = photo(tBill, tFirst, 'song_printing.jpg', { grade: 'soft', kb: [1.25, 1.3], from: [-6, -4], to: [-6, -5], tr: 'fade' }); tl.set(S.img, { filter: GRADES.soft + ' blur(5px)' }, tBill);
    charIn('B', tBill, 'CR'); idle('B', tBill + .5, tFirst + .1); talk('B', 14);
    tl.to(CHR.B.M.sweat, { opacity: 1, duration: .15 }, LA(14) + .1); tl.to(CHR.B.M.sweat, { y: 40, opacity: 0, duration: .9 }, LA(14) + .5);
    tl.to(CHR.B.d, { rotation: -6, duration: .25, yoyo: true, repeat: 1, transformOrigin: '50% 100%' }, A('they printed me', -.1));
    charOut('B', tFirst - .15); }

  // 8. the first mirage
  { const tB = A('Paper only works'); const S = photo(tFirst, tEu, 'deposit_shop.jpg', { grade: 'soft', kb: [1.15, 1.05], tr: 'fade' }); tl.set(S.img, { filter: GRADES.soft + ' blur(3px)' }, tFirst);
    const m = c2_sh(T(S, 'The first *mirage*', 960, 420, 120)); kin(m, A('the first mirage'), { times: [A('the first mirage'), A('first mirage'), A('mirage')] });
    // heat-shimmer wobble on the headline
    tl.fromTo(m, { skewX: 0 }, { keyframes: Array.from({ length: 10 }, (_, i) => ({ skewX: i % 2 ? -3 : 3, duration: .28, ease: 'sine.inOut' })).concat([{ skewX: 0, duration: .3 }]), ...IR }, A('mirage') + .4);
    tl.to(m, { opacity: .55, duration: .5, yoyo: true, repeat: 3, ease: 'sine.inOut' }, A('mirage') + .5); sfx('shimmer', A('mirage'), .5);
    const b = c2_sh(T(S, 'Paper works only while people *believe* it', 960, 600, 56)); kin(b, tB, { st: .1 }); }

  // 9. Europe: Bank of England, 1694 -> 1931
  { const t94 = A('1694'), t31 = A('until 1931'); const S = photo(tEu, tTicket, 'boe_hall_1808.jpg', { grade: 'warm', kb: [1.04, 1.18], from: [0, 2], to: [-2, -3], tr: 'slide', credit: 'Rowlandson & Pugin, Bank of England, 1808 · Public domain' });
    lower(S, 'EUROPE CAUGHT ON', 'Bank of *England* notes', A('Bank of England notes', -.3));
    const q = c2_sh(T(S, '"...promised to pay the bearer"', 960, 300, 58, { color: '#E9B44C' })); kin(q, A('promised to pay'), { st: .1 });
    const g = G(S, { opacity: 1 }); const bar = sv('line', { x1: 560, y1: 170, x2: 1360, y2: 170, stroke: 'rgba(243,235,221,.7)', 'stroke-width': 4, opacity: 0 }, g); draw(bar, t94 + .2, 1.0, { len: 800 });
    const d1 = sv('circle', { cx: 560, cy: 170, r: 12, fill: '#E9B44C' }, g); pop(d1, t94 - .05, { sfx: false }); const y1 = c2_sh(I(S, '1694', 560, 120, 40, { weight: 800, color: '#E9B44C' })); fin(y1, t94, .3);
    const d2 = sv('circle', { cx: 1360, cy: 170, r: 12, fill: '#E2614B' }, g); pop(d2, t31, { sfx: false }); const y2 = c2_sh(I(S, '1931', 1360, 120, 40, { weight: 800, color: '#E2614B' })); fin(y2, t31 + .1, .3);
    const m = c2_sh(I(S, 'PAYABLE IN GOLD (MUCH OF THE TIME)', 960, 215, 22, { weight: 800, ls: '.24em', color: '#C9CFDA' })); fin(m, A('pay out in gold', -.2), .4); }

  // 10. ticket and vault = the gold standard
  { const tGs = A('gold standard'); const S = photo(tTicket, tEnd, 'bank_vault_1700s.jpg', { grade: 'soft', kb: [1.1, 1.2], from: [0, 0], to: [-2, -2], tr: 'zoom' }); tl.set(S.img, { filter: GRADES.soft + ' blur(4px) brightness(.7)' }, tTicket);
    const g = G(S, { opacity: 1 }); const n = note(g, 620, 430, 420, {}); pop(n, A('Paper was the ticket', .2), { s0: .7, sfx: 'swoosh', vol: .3 });
    const b = goldBar(g, 1300, 440, 2.2, { label: false }); pop(b, A('Gold sat', -.05), { s0: .7, sfx: 'clink', vol: .5 });
    const ar = arrowPath(S.svg, 'M860,435 L1030,435', { w: 10 }); tl.set(ar, { attr: { 'stroke-dasharray': '18 14' } }, 0); fin(ar, A('Gold sat'), .4);
    const l1 = c2_sh(I(S, 'THE TICKET', 620, 620, 34, { weight: 800, ls: '.3em' })); fin(l1, A('Paper was the ticket', .3), .3);
    const l2 = c2_sh(I(S, 'IN THE VAULT', 1300, 620, 34, { weight: 800, ls: '.3em', color: '#E9B44C' })); fin(l2, A('in the vault', -.1), .3);
    const s = c2_sh(T(S, '= a *gold standard*', 960, 790, 96)); kin(s, A("That's a gold standard"), { times: [A("That's a gold standard"), A("That's a gold standard", .15)].concat(wordTimes('gold standard')) }); }
}
