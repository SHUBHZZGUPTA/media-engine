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
  layout();  // re-fit captions after the keyword bars changed their widths
  MO.shakeOn($('cshake'), D.dur);
  // sort keyframes, then one render driver (reads time only)
  const allT = []; for (const S of PLATES) { allT.push(S.cam0, ...Object.values(S.uT), ...S.parts.map(p => p.a), ...S.glows.map(g => g.a), ...S.labels.map(l => l.a)); }
  allT.push(MP.gk, MP.tk, MP.x, MP.hl, MP.rise, MP.pinA, MP.flagA, ...MP.cards.map(c => c.a), MP.labels[0].a, ...MP.lls.map(l => l.a), HO.dl, TW1.thermo.a, TW1.thermo.lvl, TW1.thermo.spin, TW1.lblA, ...Object.values(TW2.bars).filter(v => v && v.keys));
  for (const T of allT) T.keys.sort((a, b) => a.a - b.a);
  const clk = { t: 0 };
  tl.fromTo(clk, { t: 0 }, { t: D.dur, duration: D.dur, ease: 'none', ...IR, onUpdate: () => { const t = clk.t;
    const live = S => S.wins.some(w => t >= w[0] - .05 && t <= w[1] + .45);
    for (const S of PLATES) if (live(S)) renderPlate(S, t);
    if (live(MP)) renderMap(MP, t);
    XF.render(t); } }, 0);
  return tl;
}
window.__timelines = window.__timelines || {};
document.fonts.ready.then(() => Promise.all(READY)).then(() => { window.__timelines['main'] = build(); });
</script>
</body>
</html>
