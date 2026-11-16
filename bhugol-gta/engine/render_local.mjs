const { chromium } = await import(process.env.PW || '/home/claude/japan/node_modules/playwright/index.mjs');
import { spawn } from 'node:child_process';
const [url, f0s, f1s, out] = process.argv.slice(2); const f0 = +f0s, f1 = +f1s;
const b = await chromium.launch({ executablePath: process.env.CHROME || '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell', args: ['--autoplay-policy=no-user-gesture-required'] });
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
p.on('pageerror', e => console.log('PAGEERR', e.message));
await p.goto(url); await p.waitForFunction(() => !!window.__seek, null, { timeout: 300000 });
const enc = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
const t0 = Date.now();
for (let f = f0; f < f1; f++) {
  await p.evaluate(async t => { window.__seek(t);
    const vs = [...document.querySelectorAll('video')];
    await Promise.all(vs.map(v => { const a = +v.dataset.start, d = +v.dataset.duration, ms = +(v.dataset.mediaStart || 0), r = +(v.dataset.rate || 1);
      if (!(t >= a - .05 && t <= a + d + .05)) return null; const tt = (Math.round(Math.max(0, Math.min(d, t - a)) * r * 30) + 0.5) / 30 + ms;
      if (Math.abs(v.currentTime - tt) < 1e-3 && v.readyState >= 2) return null;
      return new Promise(res => { let fin = false; const done = () => { if (!fin) { fin = true; res(); } }; v.addEventListener('seeked', () => { if (v.requestVideoFrameCallback) { v.requestVideoFrameCallback(() => done()); setTimeout(done, 600); } else done(); }, { once: true }); v.currentTime = tt; setTimeout(done, 4000); }); }));
    await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
  }, f / 30);
  await p.evaluate(async () => { if (window.__ready) await window.__ready(); await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); });
  const buf = await p.screenshot({ type: 'jpeg', quality: 92 });
  if (!enc.stdin.write(buf)) await new Promise(r => enc.stdin.once('drain', r));
  if ((f - f0) % 300 === 0) console.log('PROGRESS', f, ((Date.now() - t0) / 1000).toFixed(0) + 's');
}
enc.stdin.end(); await new Promise(r => enc.on('close', r)); console.log('DONE', f0, f1, ((Date.now() - t0) / 1000).toFixed(0) + 's'); await b.close();
