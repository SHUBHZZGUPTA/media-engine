// Resumable frame renderer: node render_frames.js <projdir> <framesdir> <fps> <t0> <t1>
// Writes f%05d.png for frame indices in [t0*fps, t1*fps); skips frames that already exist.
const { chromium } = require('playwright'); const http = require('http'), fs = require('fs'), path = require('path');
const [root, outd, fpsS, t0S, t1S] = process.argv.slice(2); const fps = +fpsS, a = Math.round(+t0S * fps), b = Math.round(+t1S * fps);
fs.mkdirSync(outd, { recursive: true });
const types = { '.js': 'text/javascript', '.html': 'text/html', '.png': 'image/png', '.woff2': 'font/woff2' };
const srv = http.createServer((q, r) => { const f = path.join(root, decodeURIComponent(q.url.split('?')[0])); if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r); }).listen(0, async () => {
  const port = srv.address().port;
  const br = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await br.newPage({ viewport: { width: 1280, height: 720 } }); p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto(`http://localhost:${port}/index.html`); await p.waitForFunction('window.__ready === true', null, { timeout: 300000 });
  const W = await p.evaluate(() => [document.getElementById('root').offsetWidth, document.getElementById('root').offsetHeight]);
  await p.setViewportSize({ width: W[0], height: W[1] });
  let n = 0; const st = Date.now();
  for (let i = a; i < b; i++) { const f = path.join(outd, `f${String(i).padStart(5, '0')}.png`); if (fs.existsSync(f)) continue;
    await p.evaluate(t => window.__frame(t), i / fps); await p.screenshot({ path: f + '.tmp.png' }); fs.renameSync(f + '.tmp.png', f); n++;
    if (n % 60 === 0) console.log(`frame ${i} (${n} done, ${((Date.now() - st) / n / 1000).toFixed(2)} s/frame)`); }
  console.log('DONE', a, b); await br.close(); srv.close(); });
