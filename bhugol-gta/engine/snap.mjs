const { chromium } = await import(process.env.PW || '/home/claude/japan/node_modules/playwright/index.mjs');
const [url, times, out] = [process.argv[2], JSON.parse(process.argv[3]), process.argv[4]];
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell', args: ['--autoplay-policy=no-user-gesture-required'] });
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
await p.goto(url);
await p.waitForFunction(() => !!window.__seek, null, { timeout: 180000 });
for (const t of times) {
  await p.evaluate(async t => { window.__seek(t);
    const vs = [...document.querySelectorAll('video')];
    await Promise.all(vs.map(v => { const a = +v.dataset.start, d = +v.dataset.duration, ms = +(v.dataset.mediaStart || 0), r = +(v.dataset.rate || 1);
      if (!(t >= a - .05 && t <= a + d + .05)) return null; const tt = (Math.round(Math.max(0, Math.min(d, t - a)) * r * 30) + 0.5) / 30 + ms;
      if (Math.abs(v.currentTime - tt) < 1e-3 && v.readyState >= 2) return null;
      return new Promise(res => { let fin = false; const done = () => { if (!fin) { fin = true; res(); } }; v.addEventListener('seeked', () => { if (v.requestVideoFrameCallback) { v.requestVideoFrameCallback(() => done()); setTimeout(done, 600); } else done(); }, { once: true }); v.currentTime = tt; setTimeout(done, 4000); }); }));
    await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
  }, t);
  await p.evaluate(async () => { if (window.__ready) await window.__ready(); });
  await p.waitForTimeout(60);
  await p.screenshot({ path: `${out}/t${String(t.toFixed(2)).padStart(7, '0')}.jpg`, type: 'jpeg', quality: 70 });
}
console.log('ERRS', JSON.stringify(errs.slice(0, 8)));
await b.close();
