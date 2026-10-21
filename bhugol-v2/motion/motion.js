/* BHUGOL motion library (v1, 21 Oct 2026) — shared by the 2D and 3D templates.
   Built from the HyperFrames motion doctrine (faceless-explainer motion-language + cut-catalog, hyperframes-animation
   transitions/rules, embedded-captions motion). Every effect is a GSAP tween on the paused main timeline, so every frame
   is a pure function of time (seek-safe, render-safe).

   const M = BhugolMotion(tl);
   M.shots(list)            list = [{el, at, cut}] in order; at = cut time (s); cut = 'curve' | 'zoom' | 'zoomIn' | 'whip' | 'flash' | 'hard'
                            the first shot is shown at 0. Scenes are full-frame elements (class .scene), hidden by default.
   M.karaoke(words, times, isKey)   per-word reveal: keywords pop 1.15 with a glow, others 1.03; power3.out, no bounce
   M.countUp(el, to, at, {from, dur, prefix, suffix, decimals, noScale})   1.2-2.5 s, power3.out, grows from 55% (noScale for
                            elements whose transform is written elsewhere, e.g. 3D-projected labels)
   M.slam(el, at, {shake})  kinetic slam for a number/title: scale 1.5 -> 1 + blur 10 -> 0, expo.out 0.3 s
   M.punch(el, at, level, back)  quick push-in on a stressed word (hook beats); back = time to ease out
   M.jitter(el, a, b)       finite hold-aliveness: scale 0.012, y 2.5 px, period ~2 s (never on text being read)
   M.textIn(el, at) / M.textOut(el, at)   titles/labels: power3.out / power2.in (no back/elastic on reading text)
   M.cues                   [{t, kind}] one per cut, for the sound pass (the build passes the same plan to mkscore)

   Grammar (from the docs): one primary cut type for ~60-70% of cuts ('curve'), 1-2 accents ('zoom' for a new chapter,
   'zoomIn' for an arrival/payoff, 'whip' for time jumps), 'flash' at most twice (hero beats: the payoff and/or the twist),
   'hard' for rapid-fire lists. Every shot change gets a cut. */
(function (G) {
  G.BhugolMotion = function (tl) {
    const IR = { immediateRender: false }; const cues = [];
    let flashEl = document.getElementById('mFlash');
    if (!flashEl) { flashEl = document.createElement('div'); flashEl.id = 'mFlash';
      Object.assign(flashEl.style, { position: 'absolute', inset: '0', background: '#FFF6E0', opacity: '0', pointerEvents: 'none', zIndex: '40' });
      (document.getElementById('stage') || document.body).appendChild(flashEl); }
    const BLUR0 = 'blur(0px)';
    function show(el, at) { tl.set(el, { opacity: 1, x: 0, y: 0, scale: 1, filter: BLUR0 }, at); }
    function hide(el, at) { tl.set(el, { opacity: 0, x: 0, scale: 1, filter: BLUR0 }, at); }
    const CUT = {
      // primary: cut at peak velocity — power4 in/out, ~0.33 s each side, entry fades up from 0.35.
      // Full-bleed plates: the outgoing shot keeps travelling under the incoming one (no exit fade), so no edge strip ever shows.
      curve(a, b, t) {
        tl.fromTo(a, { x: 0, scale: 1 }, { x: -60, scale: 1.12, duration: .32, ease: 'power4.in', ...IR }, t - .32);  // push-in keeps the frame filled
        tl.to(a, { x: -420, duration: .34, ease: 'power2.out' }, t);
        hide(a, t + .36);
        tl.fromTo(b, { opacity: .35, x: 230, scale: 1.04, filter: BLUR0 }, { opacity: 1, x: 0, scale: 1, duration: .34, ease: 'power4.out', ...IR }, t);
        tl.set(b, { opacity: .35 }, t);
      },
      // accent: new chapter (forward zoom-through) — exit 1 -> 1.2 + blur 18, power3.in 0.2 s; entry settles 1.3 -> 1, expo.out 0.5 s.
      // inverse (zoomIn = arrival/payoff): softer exit 1 -> 1.08, entry 1.18 -> 1 over 0.7 s power3.out.
      // Full-bleed scenes never go below scale 1 (the doc's 0.75/0.8 values are for text; on a full-frame plate they expose the edges).
      zoom(a, b, t, inv) {
        tl.fromTo(a, { scale: 1, filter: BLUR0 }, { scale: inv ? 1.08 : 1.2, filter: 'blur(18px)', duration: .2, ease: 'power3.in', ...IR }, t - .2);
        hide(a, t + .13);
        tl.fromTo(b, { opacity: 0, scale: inv ? 1.18 : 1.3, filter: 'blur(18px)' }, { opacity: 1, scale: 1, filter: BLUR0, duration: inv ? .7 : .5, ease: inv ? 'power3.out' : 'expo.out', ...IR }, t);
        tl.fromTo(b, { opacity: 0 }, { opacity: 1, duration: .12, ease: 'none', ...IR }, t);
      },
      // accent: time jump / rewind — blurred whip-push: both shots travel together (no gap), blur peaks ~22 px at the swap
      whip(a, b, t) {
        const d1 = .2, d2 = .34;
        tl.fromTo(a, { x: 0, filter: BLUR0 }, { x: -540, filter: 'blur(22px)', duration: d1, ease: 'power3.in', ...IR }, t - d1);
        tl.to(a, { x: -1080, duration: d2, ease: 'power3.out' }, t);
        hide(a, t + d2 + .01);
        tl.fromTo(b, { opacity: 1, x: 540, filter: 'blur(22px)' }, { x: 0, filter: BLUR0, duration: d2, ease: 'power3.out', ...IR }, t);
        tl.set(b, { opacity: 1, x: 1080, filter: BLUR0 }, t - d1 - .01);
        tl.fromTo(b, { x: 1080, filter: BLUR0 }, { x: 540, filter: 'blur(22px)', duration: d1, ease: 'power3.in', ...IR }, t - d1);
      },
      // hero: flash-through-white — rise 0.045 s, hard swap at the peak, recover 0.32 s (max twice per video)
      flash(a, b, t) {
        tl.fromTo(flashEl, { opacity: 0 }, { keyframes: [{ opacity: .92, duration: .045 }, { opacity: 0, duration: .32, ease: 'power2.out' }], ...IR }, t - .045);
        hide(a, t); show(b, t);
        tl.fromTo(b, { scale: 1.08 }, { scale: 1, duration: .6, ease: 'expo.out', ...IR }, t);
      },
      hard(a, b, t) { hide(a, t); show(b, t); }
    };
    const SND = { curve: 'curve', zoom: 'zoom', zoomIn: 'zoomIn', whip: 'whip', flash: 'flash', hard: 'hard' };
    function shots(list) {
      list.forEach((s, i) => {
        if (i === 0) { show(s.el, 0); return; }
        const a = list[i - 1].el, b = s.el, t = s.at, k = s.cut || 'curve';
        tl.set(b, { opacity: 0 }, 0);
        (k === 'zoomIn') ? CUT.zoom(a, b, t, true) : (CUT[k] || CUT.curve)(a, b, t);
        cues.push({ t, kind: SND[k] || 'curve' });
      });
    }
    function karaoke(words, times, isKey) {
      words.forEach((w, i) => { const t = times[Math.min(i, times.length - 1)]; const key = isKey(w);
        tl.fromTo(w, { opacity: 0, scale: key ? 1.15 : 1.03, display: 'inline-block' },
          { opacity: 1, scale: 1, duration: key ? .26 : .16, ease: 'power3.out', ...IR }, t);
        if (key) tl.fromTo(w, { textShadow: '0 0 26px rgba(255,194,58,.95)' }, { textShadow: '0 0 0px rgba(255,194,58,0)', duration: .6, ease: 'power2.out', ...IR }, t); });
    }
    function countUp(el, to, at, o) { o = o || {}; const from = o.from || 0, dur = o.dur || 1.6, dec = o.decimals || 0; const st = { v: from };
      const fmt = v => (o.prefix || '') + Number(v.toFixed(dec)).toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec }) + (o.suffix || '');
      tl.fromTo(st, { v: from }, { v: to, duration: dur, ease: 'power3.out', ...IR, onUpdate: () => { el.textContent = fmt(st.v); } }, at);
      if (!o.noScale) tl.fromTo(el, { scale: .55 }, { scale: 1, duration: dur, ease: 'power3.out', transformOrigin: '50% 50%', ...IR }, at);
      tl.set(el, { textContent: fmt(from) }, Math.max(0, at - .01)); }
    function slam(el, at, o) { o = o || {};
      tl.fromTo(el, { opacity: 0, scale: 1.5, filter: 'blur(10px)' }, { opacity: 1, scale: 1, filter: BLUR0, duration: .3, ease: 'expo.out', transformOrigin: '50% 50%', ...IR }, at);
      if (o.shake !== false) { const sh = document.getElementById('shake'); if (sh) tl.fromTo(sh, { x: 0, y: 0 }, { keyframes: [{ x: -14, y: 9, duration: .05 }, { x: 10, y: -7, duration: .05 }, { x: -5, y: 3, duration: .06 }, { x: 0, y: 0, duration: .08 }], ...IR }, at + .12); }
      cues.push({ t: at + .1, kind: 'slam' }); }
    function jitter(el, a, b) { const n = Math.max(1, Math.floor((b - a - .2) / 2));
      tl.fromTo(el, { scale: 1, y: 0 }, { keyframes: Array.from({ length: n }, (_, i) => ({ scale: i % 2 ? 1 : 1.012, y: i % 2 ? 0 : -2.5, duration: 2, ease: 'sine.inOut' })), ...IR }, a + .2); }
    // punch-in: a quick push on a stressed word (a visual beat without new on-screen content). level = target scale (1.08-1.25)
    function punch(el, at, level, back) { tl.to(el, { scale: level || 1.12, duration: .26, ease: 'power3.out', transformOrigin: '50% 45%' }, at);
      if (back) tl.to(el, { scale: 1, duration: .45, ease: 'power2.inOut' }, back);
      cues.push({ t: at, kind: 'punch' }); }
    const textIn = (el, at, d) => tl.fromTo(el, { opacity: 0, scale: .9, y: 18 }, { opacity: 1, scale: 1, y: 0, duration: d || .34, ease: 'power3.out', ...IR }, at);
    const textOut = (el, at, d) => tl.to(el, { opacity: 0, y: -10, duration: d || .22, ease: 'power2.in' }, at);
    return { shots, karaoke, countUp, slam, jitter, punch, textIn, textOut, cues, CUT };
  };
})(window);
