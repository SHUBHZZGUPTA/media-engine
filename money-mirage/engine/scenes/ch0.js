// COLD OPEN (lines 0-5) + logo sting — archival/painted documentary style
function ch0() {
  const tQ = A('So what is it backed'), tM = A('And it matters'), tR = A('Read the small print'), tPW = A('Pay what'),
    tSun = A('Then, one Sunday'), tG = LA(3) - .6, tIV = A('In this video'), tFr = A('why France'), tNine = A('why almost nine'),
    tBeh = A("and what's really"), tSp = A('Spoiler'), tEnd = LB(5) + .4, tLogo = CH(1).a - 1.3;
  startCh(0);

  // 1. wallet on a desk, push in
  { const S = photo(0, tQ, 'wallet_desk.jpg', { grade: 'paint', kb: [1.0, 1.22], from: [0, 0], to: [-3, -4], tr: 'fade' });
    const l = lower(S, 'SINCE 1971', 'Not backed by *gold*', A('backed by gold', -.1)); sfx('sting', .1, .5); }
  // 2. so what is it backed by?
  { const S = photo(tQ, tM, 'fortknox_vault.jpg', { grade: 'mono', kb: [1.12, 1.02], tr: 'fade', credit: 'Fort Knox Bullion Depository · Public domain' });
    const h = T(S, 'So what is it *backed by?*', 960, 470, 110); kin(h, tQ + .1, { times: wordTimes('So what is it backed by') }); }
  // 3. whatever backs it can weaken it
  { const S = photo(tM, tR, 'central_bank.jpg', { grade: 'paint', kb: [1.04, 1.16], from: [2, 0], to: [-2, -2] });
    lower(S, null, 'What backs it can *weaken* it', A('because whatever', 0), { size: 88 }); sfx('clang', A('weaken'), .5); }
  // 4. the small print: Bank of England hall + the promise
  { const S = photo(tR, tPW, 'boe_hall_1808.jpg', { grade: 'warm', kb: [1.05, 1.2], from: [0, 2], to: [0, -3], credit: 'Rowlandson & Pugin, Bank of England, 1808 · Public domain' });
    lower(S, 'A BRITISH BANKNOTE', 'Read the small print', tR, { size: 84, y: 300 });
    const q = T(S, '"I promise to pay the bearer on demand..."', 960, 760, 64, { color: '#E9B44C', font: 'Brico' }); kin(q, A('"I promise'), { times: wordTimes('I promise to pay the bearer on demand') }); }
  // 5. pay what? gold
  { const tGold = A('answer was gold', .5); const S = photo(tPW, tSun, 'lydia_trite_bm.jpg', { grade: 'warm', kb: [1.3, 1.05], tr: 'zoom', credit: 'Lydian electrum trite, British Museum · ArchaiOptix, CC BY-SA 4.0' });
    const t = T(S, 'Pay *what?*', 960, 300, 140); kin(t, tPW, { times: wordTimes('Pay what') }); tl.to(t, { autoAlpha: 0, duration: .3 }, A('For most of history', -.1));
    lower(S, 'FOR MOST OF HISTORY', 'The answer was *gold*', A('For most of history')); sfx('clink', tGold); flash(tGold, .18); }
  // 6. one Sunday in 1971
  { const tCh = A('quietly changed'), tNv = A('never changed back'); const S = photo(tSun, tG, 'tv_1971.jpg', { grade: 'paint', kb: [1.02, 1.18], to: [-2, -1] });
    lower(S, 'ONE SUNDAY · 1971', 'That promise *changed*', A('one Sunday')); sfx('static', tCh, .4);
    const t2 = T(S, '...and it _never_ changed back', 1800, 300, 64, { align: 'right' }); kin(t2, tNv, { times: wordTimes('and it never changed back') }); }
  // 7. Goldie and Bill banter in the vault
  { const S = photo(tG, tIV, 'bank_vault_1700s.jpg', { grade: 'soft', kb: [1.1, 1.14], tr: 'fade' }); tl.set(S.img, { filter: GRADES.soft + ' blur(4px)' }, tG);
    charIn('G', tG, 'CL'); charIn('B', tG + .35, 'CR'); idle('G', tG + .6, tIV + .2); idle('B', tG + .9, tIV + .2);
    talk('G', 3); tl.to(CHR.G.M.brow, { y: -8, duration: .2, yoyo: true, repeat: 1 }, LA(3) + .2);
    talk('B', 4); tl.to(CHR.B.M.sweat, { opacity: 1, duration: .15 }, LA(4)); tl.to(CHR.B.M.sweat, { y: 40, opacity: 0, duration: .8 }, LA(4) + .3);
    charOut('G', tIV - .1); charOut('B', tIV - .1); }
  // 8. preview montage (fast cuts)
  { const S = photo(tIV, tFr, 'song_printing.jpg', { grade: 'paint', kb: [1.0, 1.15], tr: 'slide' });
    lower(S, 'IN THIS VIDEO', 'How paper beat *gold*', A('how paper beat', -.2)); }
  { const S = mapShot(tFr, tNine, { tr: 'slide' }); camSet(S, -35, 44, .55); camTo(S, -35, 44, .68, tFr, tNine - tFr, 'sine.inOut');
    pin(S, 2.35, 48.86, tFr + .2, { rep: 1 }); pin(S, -77.04, 38.9, tFr + .4, { c: '#F3EBDD', rep: 1 }); marc(S, 2.35, 48.86, -77.04, 38.9, A('cash its dollars'), 1.0);
    lower(S, 'FRANCE', 'Cashing in its *dollars*', tFr + .1, { size: 84 }); }
  { const S = photo(tNine, tBeh, 'trading_room.jpg', { grade: 'paint', kb: [1.0, 1.14], tr: 'zoom' });
    const n = I(S, '0', 960, 420, 220, { weight: 900, color: '#E9B44C' }); fin(n, A('nine in ten'), .2); count(n, 0, 89, A('nine in ten'), 1.6, { suf: '%' });
    const k = I(S, 'OF ALL CURRENCY TRADES INVOLVE THE DOLLAR', 960, 590, 34, { weight: 800, ls: '.2em' }); fin(k, A('currency trades'), .4); }
  { const S = photo(tBeh, tSp, 'wallet_desk.jpg', { grade: 'paint', kb: [1.25, 1.45], from: [-2, -4], to: [-4, -8], tr: 'fade' });
    lower(S, null, "What's *really* behind your money?", tBeh, { size: 84, kin: { times: wordTimes("what's really standing behind your money").filter((_, i) => i !== 2) } }); }
  { const tBut = A("But it isn't nothing"); const S = photo(tSp, tEnd, 'fortknox_postcard.jpg', { grade: 'mono', kb: [1.02, 1.12], tr: 'wipe', credit: 'Tichnor Bros., Boston Public Library · Public domain' });
    const a1 = T(S, "Spoiler: it isn't *gold*", 960, 430, 104); kin(a1, tSp);
    tl.to(a1, { autoAlpha: 0, duration: .25 }, tBut - .1); tl.to(S.img, { filter: GRADES.mono + ' blur(6px)', duration: .6 }, tBut - .1);
    const a2 = T(S, "But it isn't *nothing*", 960, 430, 104); kin(a2, tBut, { times: wordTimes("But it isn't nothing") }); }

  // 9. logo sting
  { const S = shot(tEnd, tLogo, { tr: 'fade', push: 1.04 }); const wm = wordmark(S.svg, 220, 520, 3.4); tl.set(wm.g, { opacity: 0 }, 0);
    tl.fromTo(wm.g, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .8, ease: 'power3.out', ...IR }, tEnd + .1); sfx('sting', tEnd + .05, 1);
    tl.fromTo(wm.waves, { x: 0 }, { x: -56, duration: 3.2, ease: 'none', ...IR }, tEnd); tl.fromTo(wm.refl, { opacity: 0 }, { opacity: .28, duration: 1, ...IR }, tEnd + .5);
    const sh = sv('rect', { x: 300, y: 330, width: 120, height: 300, fill: 'rgba(255,246,226,.35)', transform: 'skewX(-20)', style: 'filter: blur(10px)' }, S.svg);
    tl.fromTo(sh, { x: -300 }, { x: 1500, duration: 1.2, ease: 'power2.inOut', ...IR }, tEnd + .9); }
}
