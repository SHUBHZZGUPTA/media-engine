/* BHUGOL motion library (v2, 22 Oct 2026) — shared by the 2D and 3D templates.
   v2 adds ports of HyperFrames library items (registry / rules, Apache-2.0 / MIT): measured camera-shake profiles, hand-drawn
   circles and arrows (hw-*), char-slam + kinetic word beats, counting with dynamic scale, split-flap board, caption highlight
   sweep, and the 'burn' hero cut (WebGL overlay in shader_xfade.js for 3D; warm flash in 2D).
   const MO = BhugolMotion(tl, { xfade: true });   (xfade: true only in 3D, with shader_xfade.js)
   MO.shake(at, dur, profile, k, {decay}) ... MO.shakeOn(wrapperEl, totalDur)   one driver sums every shake event (call once, last)
   MO.hwCircle(parent, pos(t)->{x,y}, rx, ry, at, until, {col, w, seed})  /  MO.hwArrow(parent, ends(t)->{x0,y0,x1,y1}, at, until, o)
   MO.charSlam(lineEl, at, {wordGap, spread, blur})   MO.countGrow(numEl, to, at, {dur, from, prefix, startScale, suffixEl})
   MO.flap(rowEl, 'TEXT', at, {stagger})              MO.sweep(wordSpan, at, col)   (keywords: bar behind the word, no outline)
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
  G.BhugolMotion = function (tl, opts) { opts = opts || {};
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
        tl.fromTo(a, { x: 0, scale: 1 }, { x: -100, scale: 1.12, duration: .32, ease: 'power4.in', ...IR }, t - .32);  // push-in keeps the frame filled
        tl.to(a, { x: -740, duration: .34, ease: 'power2.out' }, t);
        hide(a, t + .36);
        tl.fromTo(b, { opacity: .35, x: 400, scale: 1.04, filter: BLUR0 }, { opacity: 1, x: 0, scale: 1, duration: .34, ease: 'power4.out', ...IR }, t);
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
        tl.fromTo(a, { x: 0, filter: BLUR0 }, { x: -960, filter: 'blur(22px)', duration: d1, ease: 'power3.in', ...IR }, t - d1);
        tl.to(a, { x: -1920, duration: d2, ease: 'power3.out' }, t);
        hide(a, t + d2 + .01);
        tl.fromTo(b, { opacity: 1, x: 960, filter: 'blur(22px)' }, { x: 0, filter: BLUR0, duration: d2, ease: 'power3.out', ...IR }, t);
        tl.set(b, { opacity: 1, x: 1920, filter: BLUR0 }, t - d1 - .01);
        tl.fromTo(b, { x: 1920, filter: BLUR0 }, { x: 960, filter: 'blur(22px)', duration: d1, ease: 'power3.in', ...IR }, t - d1);
      },
      // hero: flash-through-white — rise 0.045 s, hard swap at the peak, recover 0.32 s (max twice per video)
      flash(a, b, t) {
        tl.fromTo(flashEl, { opacity: 0 }, { keyframes: [{ opacity: .92, duration: .045 }, { opacity: 0, duration: .32, ease: 'power2.out' }], ...IR }, t - .045);
        hide(a, t); show(b, t);
        tl.fromTo(b, { scale: 1.08 }, { scale: 1, duration: .6, ease: 'expo.out', ...IR }, t);
      },
      hard(a, b, t) { hide(a, t); show(b, t); },
      // hero: shader transition drawn by the template's WebGL overlay (e.g. ridged fire burn) over [t, t + dur];
      // the scenes themselves swap under the overlay at the end, so this side is a hard swap at t + dur.
      burn(a, b, t) { if (opts.xfade) { hide(a, t + BURN_DUR); show(b, t + BURN_DUR); return; }  // 3D: the shader overlay draws the cut
        flashEl.style.background = '#FFB060'; CUT.flash(a, b, t); }  // 2D (no WebGL overlay): a warm fire flash instead
    };
    const BURN_DUR = .8;
    const SND = { curve: 'curve', zoom: 'zoom', zoomIn: 'zoomIn', whip: 'whip', flash: 'flash', hard: 'hard', burn: 'burn' };
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
        if (key) tl.fromTo(w, { textShadow: '0 0 22px rgba(255,214,120,.85)' }, { textShadow: '0 0 0px rgba(255,214,120,0)', duration: .6, ease: 'power2.out', ...IR }, t); });
    }
    function countUp(el, to, at, o) { o = o || {}; const from = o.from || 0, dur = o.dur || 1.6, dec = o.decimals || 0; const st = { v: from };
      const fmt = v => (o.prefix || '') + Number(v.toFixed(dec)).toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec, useGrouping: !o.plain }) + (o.suffix || '');
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

    /* ===================== v2: ports of HyperFrames library items (registry, MIT/Apache) =====================
       Every effect below is driven by a property-setter "driver" tween (not onUpdate), so it renders correctly on
       seek, on HyperFrames' sub-frame motion-blur seeks, and in any order. */
    const HASH = (n, s) => { const x = Math.sin(n * 127.1 + (s || 1) * 311.7) * 43758.5453; return (x - Math.floor(x)) * 2 - 1; };
    const clamp01 = v => Math.max(0, Math.min(1, v));
    function driver(a, b, fn) { const d = {}; let v = a; Object.defineProperty(d, 't', { get: () => v, set: n => { v = n; fn(n); } });
      tl.fromTo(d, { t: a }, { t: b, duration: Math.max(.001, b - a), ease: 'none', ...IR }, a); return d; }

    // ---- camera shake (reg:camera-shake profiles: measured amplitudes in degrees / frequencies in Hz, 3 octaves) ----
    const CSP = {
      'handheld-normal-mild': { lens: 50, rot: [[[7, .15], [5, .1], null], [[4, .8], [2, .75], null], [[1, 1.2], [.8, 1.5], null]] },
      'handheld-normal-strong': { lens: 50, rot: [[[10, .4], [10, .06], null], [[5, 1.44], [3, .73], null], [[3, 2.49], [1, 2], null]] },
      'handheld-tele-strong': { lens: 85, rot: [[[6.19, .39], [4, .15], [1, .1]], [[1.84, 1.75], [.5, .9], null], [[2.3, 2], [.5, 1.4], null]] },
      'rig-6d-wobble': { lens: 50, rot: [[[.987, 5.2], [1.34, 5.39], [2, 2.23]], [[.73, 9.17], [.86, 11.35], [.51, 8.31]], [[.78, 13.52], [.55, 27.66], [.28, 18.91]]] } };
    function csHash(i, seed) { let h = Math.imul(i | 0, 374761393) + Math.imul(seed | 0, 668265263); h = (h ^ (h >>> 13)) >>> 0; h = Math.imul(h, 1274126177) >>> 0; return ((h ^ (h >>> 16)) >>> 0) / 4294967296; }
    function csNoise(x, seed) { const i = Math.floor(x), f = x - i, u = f * f * f * (f * (f * 6 - 15) + 10); return csHash(i, seed) * (1 - u) + csHash(i + 1, seed) * u; }
    function csSample(P, t, k) { const r = [0, 0, 0]; P.rot.forEach((oct, o) => oct.forEach((ch, a) => { if (ch) r[a] += (csNoise(ch[1] * t + (o * 3 + a) * 7.13, o * 3 + a) - .5) * ch[0] * k; })); return r; }
    const SHK = []; let shkEl = null;
    // add a shake event: profile, peak intensity, attack/decay envelope. One driver sums all events (no tween fights).
    function shake(at, dur, profile, k, o) { o = o || {}; SHK.push({ at, dur, P: CSP[profile] || CSP['handheld-normal-mild'], k, att: o.attack || .03, decay: o.decay !== false }); }
    function shakeOn(el, total) { shkEl = el; const RAD = Math.PI / 180;
      driver(0, total, t => { let x = 0, y = 0, roll = 0;
        for (const e of SHK) { if (t < e.at || t > e.at + e.dur) continue; const u = t - e.at;
          const env = Math.min(1, u / e.att) * (e.decay ? Math.pow(1 - u / e.dur, 2) : Math.min(1, (e.dur - u) / .25));
          const r = csSample(e.P, t, e.k * env); const D = 1663 * e.P.lens / 50 * 1.0;
          x += -D * Math.tan(r[1] * RAD); y += D * Math.tan(r[0] * RAD); roll += r[2] * .6 + r[1] * .15; }
        const rr = Math.abs(roll) * RAD, os = (Math.cos(rr) + 1.78 * Math.sin(rr)) * Math.max(1 + 2 * Math.abs(x) / 1920, 1 + 2 * Math.abs(y) / 1080) * 1.01;
        shkEl.style.transform = `translate(${x.toFixed(2)}px,${y.toFixed(2)}px) rotate(${roll.toFixed(3)}deg) scale(${(x || y || roll ? os : 1).toFixed(4)})`; }); }

    // ---- hand-drawn marks (reg:hw-callout-circle / hw-arrow: wobble ellipse, draw-on, 3-frame boil) ----
    const NS = 'http://www.w3.org/2000/svg';
    function hwSvg(parent) { const s = document.createElementNS(NS, 'svg'); s.setAttribute('width', 1920); s.setAttribute('height', 1080);
      Object.assign(s.style, { position: 'absolute', left: 0, top: 0, overflow: 'visible', pointerEvents: 'none', opacity: 0 }); parent.appendChild(s); return s; }
    function hwPath(svg, col, w) { const p = document.createElementNS(NS, 'path'); p.setAttribute('fill', 'none'); p.setAttribute('stroke', col); p.setAttribute('stroke-width', w);
      p.setAttribute('stroke-linecap', 'round'); p.setAttribute('stroke-linejoin', 'round'); p.style.filter = 'drop-shadow(0 3px 0 rgba(0,0,0,.55))'; svg.appendChild(p); return p; }
    const ez = gsap.parseEase('power2.inOut'), ez3 = gsap.parseEase('power3.out');
    function boil(t, seed) { const st = Math.floor(t * 10); return [HASH(st * 3, seed) * 1.8, HASH(st * 3 + 1, seed) * 1.8, HASH(st * 3 + 2, seed) * .6]; }
    // circle around a moving target. pos(t) -> {x, y}; rx, ry in px. Overshoots ~12% of a turn like a real marker loop.
    function hwCircle(parent, pos, rx, ry, at, until, o) { o = o || {}; const seed = o.seed || 3, dur = o.dur || .5, svg = hwSvg(parent), p = hwPath(svg, o.col || '#FF3B30', o.w || 13);
      const N = 18, turns = 1.12, a0 = -2.2;
      driver(at - .02, until + .3, t => { const u = t - at; svg.style.opacity = u < 0 ? 0 : clamp01((until + .25 - t) / .25);
        if (u < 0) return; const c = pos(t), b = boil(t, seed); let d = '';
        for (let i = 0; i <= N; i++) { const a = a0 + i / N * Math.PI * 2 * turns, wr = 1 + HASH(i * 13 + 5, seed) * .05 + i / N * .07;
          const X = c.x + Math.cos(a) * rx * wr, Y = c.y + Math.sin(a) * ry * wr; d += (i ? ' L' : 'M') + X.toFixed(1) + ' ' + Y.toFixed(1); }
        p.setAttribute('d', d); const L = p.getTotalLength(), pr = ez(clamp01(u / dur)); p.setAttribute('stroke-dasharray', L + ' ' + L); p.setAttribute('stroke-dashoffset', (L * (1 - pr)).toFixed(1));
        svg.style.transform = `translate(${b[0].toFixed(1)}px,${b[1].toFixed(1)}px) rotate(${b[2].toFixed(2)}deg)`; svg.style.transformOrigin = `${c.x}px ${c.y}px`; });
      cues.push({ t: at, kind: 'draw' }); return svg; }
    // arrow from p0 to p1 (ends(t) -> {x0, y0, x1, y1}); shaft draws, then the two head strokes
    function hwArrow(parent, ends, at, until, o) { o = o || {}; const seed = o.seed || 7, dur = o.dur || .42, svg = hwSvg(parent), sh = hwPath(svg, o.col || '#FF3B30', o.w || 13), hd = hwPath(svg, o.col || '#FF3B30', o.w || 13);
      const bend = o.bend === undefined ? .16 : o.bend;
      driver(at - .02, until + .3, t => { const u = t - at; svg.style.opacity = u < 0 ? 0 : clamp01((until + .25 - t) / .25); if (u < 0) return;
        const e = ends(t), b = boil(t, seed), dx = e.x1 - e.x0, dy = e.y1 - e.y0, len = Math.hypot(dx, dy) || 1, nx = -dy / len, ny = dx / len;
        const cx = (e.x0 + e.x1) / 2 + nx * len * bend + HASH(1, seed) * 8, cy = (e.y0 + e.y1) / 2 + ny * len * bend + HASH(2, seed) * 8;
        sh.setAttribute('d', `M${e.x0.toFixed(1)} ${e.y0.toFixed(1)} Q${cx.toFixed(1)} ${cy.toFixed(1)} ${e.x1.toFixed(1)} ${e.y1.toFixed(1)}`);
        const L = sh.getTotalLength(), pr = ez(clamp01(u / dur)); sh.setAttribute('stroke-dasharray', L + ' ' + L); sh.setAttribute('stroke-dashoffset', (L * (1 - pr)).toFixed(1));
        const ang = Math.atan2(e.y1 - cy, e.x1 - cx), hl = o.head || 62, hp = clamp01((u - dur * .9) / .12);
        const h = s => [e.x1 - Math.cos(ang + s * .5) * hl * hp, e.y1 - Math.sin(ang + s * .5) * hl * hp];
        const [ax, ay] = h(1), [bx, by] = h(-1); hd.setAttribute('d', hp > 0 ? `M${ax.toFixed(1)} ${ay.toFixed(1)} L${e.x1.toFixed(1)} ${e.y1.toFixed(1)} L${bx.toFixed(1)} ${by.toFixed(1)}` : '');
        svg.style.transform = `translate(${b[0].toFixed(1)}px,${b[1].toFixed(1)}px)`; });
      cues.push({ t: at, kind: 'draw' }); return svg; }

    // ---- char-slam + kinetic word beats (reg:char-slam-explode, rules/kinetic-beat-slam) ----
    const SCAT = [[-.9, -.038, .677], [.61, .716, -.967], [.418, .575, .822], [-.76, -.451, .944], [-.621, .579, -.215], [.714, .437, -.824], [.577, .567, .464], [.902, .346, .016],
      [-.526, .743, -.275], [-.571, -.353, .954], [-.666, .61, -.075], [-.122, .875, -.783], [-.141, .726, -.659], [.606, -.665, -.713], [-.962, .131, .307], [.227, .813, -.979]];
    // el holds word spans (from markup); each word lands on its own beat (wordGap), its letters fly in from a scatter and slam.
    function charSlam(el, at, o) { o = o || {}; const gap = o.wordGap || .14, sp = o.spread || 1; let gi = 0;
      [...el.children].forEach((w, wi) => { const txt = w.textContent; w.textContent = '';
        [...txt].forEach(ch => { const g = document.createElement('span'); g.textContent = ch; g.style.display = 'inline-block'; g.style.whiteSpace = 'pre'; w.appendChild(g);
          if (o.blur === true) g.setAttribute('data-hf-motion-blur', '{"samplesPerFrame": 8}');   // blur:'css' = cheap filter smear (true sub-frame sampling costs ~40 s/frame on 14 glyphs)
          const r = SCAT[gi++ % SCAT.length], t0 = at + wi * gap + (gi % 3) * .012;
          gsap.set(g, { opacity: 0 }); tl.set(g, { opacity: 0 }, 0);  // hidden until its own beat (fromTo without immediateRender shows the landed glyph early)
          tl.fromTo(g, Object.assign({ opacity: 0, x: r[0] * 150 * sp, y: r[1] * 190 * sp, rotation: r[2] * 28, scale: .55 }, o.blur === 'css' ? { filter: 'blur(14px)' } : {}), Object.assign({ opacity: 1, x: 0, y: 0, rotation: 0, scale: 1, duration: .34, ease: 'power4.out', ...IR }, o.blur === 'css' ? { filter: 'blur(0px)' } : {}), t0); });
        const land = at + wi * gap + .3; tl.fromTo(w, { x: 0 }, { keyframes: [{ x: -7, duration: 1 / 30 }, { x: 5, duration: 1 / 30 }, { x: -2, duration: 1 / 30 }, { x: 0, duration: 1 / 30 }], ...IR }, land); });
      cues.push({ t: at + .3, kind: 'slam' }); }

    // ---- counting with dynamic scale (rules/counting-dynamic-scale): number grows while counting; suffix lands after ----
    function countGrow(numEl, to, at, o) { o = o || {}; const dur = o.dur || 1.2, st = { v: o.from || 0 };
      const fmt = v => (o.prefix || '') + Math.round(v).toLocaleString('en-US', { useGrouping: !o.plain });
      tl.fromTo(st, { v: o.from || 0 }, { v: to, duration: dur, ease: o.ease || 'power3.out', ...IR, onUpdate: () => { numEl.textContent = fmt(st.v); } }, at);
      tl.set(numEl, { textContent: fmt(o.from || 0) }, Math.max(0, at - .01));
      tl.fromTo(numEl, { scale: o.startScale || .4, opacity: 0 }, { scale: 1, opacity: 1, duration: dur, ease: 'power3.out', transformOrigin: '50% 60%', ...IR }, at);
      if (o.suffixEl) tl.fromTo(o.suffixEl, { opacity: 0, x: 60, scale: 1.25 }, { opacity: 1, x: 0, scale: 1, duration: .26, ease: 'power4.out', ...IR }, at + dur - .05);
      cues.push({ t: at, kind: 'count' }); }

    // ---- split-flap board (reg:split-flap-board): each cell walks a drum of characters to its target, left to right ----
    function flap(box, text, at, o) { o = o || {}; const step = 1 / 15, set = o.charset || 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
      const cells = [...text].map((ch, i) => { const c = document.createElement('span'); c.className = 'flap'; c.textContent = ' '; box.appendChild(c);
        const n = ch === ' ' ? 0 : 5 + (i * 7) % 6; return { c, ch, n, t0: at + i * (o.stagger || .045) }; });
      driver(at - .02, at + 3, t => { for (const k of cells) { const u = t - k.t0; if (u < 0) { k.c.textContent = ' '; k.c.style.transform = 'scaleY(1)'; continue; }
        const s = Math.floor(u / step), f = (u / step) - s; if (s >= k.n) { k.c.textContent = k.ch; k.c.style.transform = 'scaleY(1)'; continue; }
        k.c.textContent = set[(s * 11 + k.ch.charCodeAt(0) * 3) % set.length]; k.c.style.transform = `scaleY(${(.35 + .65 * Math.abs(Math.cos(f * Math.PI))).toFixed(3)})`; } });
      cues.push({ t: at, kind: 'flap' }); }

    // ---- caption highlight sweep (reg:caption-highlight): a colour bar wipes in behind the keyword as it is spoken ----
    function sweep(w, at, col) { w.style.backgroundImage = `linear-gradient(${col || '#E8321C'},${col || '#E8321C'})`; w.style.backgroundRepeat = 'no-repeat';
      w.style.backgroundPosition = '0 50%'; w.style.borderRadius = '12px'; w.style.padding = '0 .14em'; w.style.margin = '0 .02em';
      w.style.webkitTextStrokeWidth = '0px'; w.style.color = '#FFFFFF'; if (w.textContent.startsWith(' ')) { w.textContent = w.textContent.slice(1); w.style.marginLeft = '.3em'; }  // TikTok-style: no outline on the bar; the bar sits on the word, not the space before it
      tl.fromTo(w, { backgroundSize: '0% 78%' }, { backgroundSize: '100% 78%', duration: .16, ease: 'power2.out', ...IR }, at); }
    return { shots, karaoke, countUp, slam, jitter, punch, textIn, textOut, cues, CUT, BURN_DUR, driver, shake, shakeOn, hwCircle, hwArrow, charSlam, countGrow, flap, sweep };
  };
})(window);
