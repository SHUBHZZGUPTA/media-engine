  // badge + end card
  const BW = $('badgeWrap'); const E = D.end; const bs = 108 / 620;
  tl.fromTo(BW, { opacity: 0, x: 44 - 230, y: 1332 - 450, scale: bs }, { opacity: 1, x: 44 - 230, y: 1332 - 450, scale: bs, duration: .5 }, .2);
  tl.fromTo(BW, { x: 44 - 230, y: 1332 - 450, scale: bs }, { x: 0, y: 0, scale: 1, duration: .9, ease: 'power2.inOut', ...IR }, E.start);
  tl.to($('dim'), { opacity: .55, duration: .5 }, E.start);
  const F = $('follow');
  tl.fromTo(F, { opacity: 0, scale: .2 }, { opacity: 1, scale: 1, duration: .45, ease: 'back.out(2)', ...IR }, E.btn);
  const TD = $('tapDot');
  tl.fromTo(TD, { opacity: 0, x: 470, y: 120 }, { opacity: 1, x: 430, y: 50, duration: .6, ease: 'power2.out', ...IR }, E.tap - .6);
  tl.to(F, { keyframes: [{ scale: .94, duration: .1 }, { scale: 1, duration: .1 }] }, E.tap);
  tl.fromTo($('ripple'), { opacity: .5, scale: .05 }, { opacity: 0, scale: 1, duration: .8, ease: 'power2.out', ...IR }, E.tap + .1);
  tl.set($('folBtn'), { backgroundColor: '#2A1206', border: '5px solid #FF7A1A' }, E.tap + .2);
  tl.set($('folTxt'), { opacity: 0 }, E.tap + .2); tl.set($('folTxt2'), { opacity: 1 }, E.tap + .2);
  tl.to(TD, { opacity: 0, duration: .3 }, E.tap + .5);
