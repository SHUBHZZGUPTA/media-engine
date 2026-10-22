// Pre-render gate for BHUGOL 3D builds: seek into every shot of the plan and fail on
//  (1) any WebGL / shader / page error in the console, and
//  (2) any shot whose scene canvas is blank (mean brightness below a floor) at its midpoint.
// Usage: node scene_gate.mjs <build_dir>   (exit 1 on failure). Needs playwright-core in the work folder (npm i playwright-core).
// 2D builds (plates are DOM images, no canvas) are checked for visibility only. Added 22 Oct 2026 after a GLSL syntax
// error ('//' comment inside a one-line shader string) blanked 3 scenes in the delivered Bengaluru video.
import { chromium } from 'playwright-core'; import http from 'http'; import fs from 'fs'; import path from 'path';
const dir = process.argv[2]; const port = 8800 + Math.floor(Math.random() * 100);
const srv = http.createServer((q, r) => { const u = decodeURIComponent(q.url.split('?')[0]); fs.readFile(path.join(dir, u === '/' ? 'index.html' : u), (e, b) => { if (e) { r.writeHead(404); r.end(); } else r.end(b); }); }).listen(port);
const b = await chromium.launch({ executablePath: process.env.HYPERFRAMES_BROWSER_PATH || '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell', args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
const errs = [];
p.on('console', m => { const t = m.text(); if (/GPU stall/.test(t)) return; if (m.type() === 'error' || /WebGL|shader|Shader|INVALID_|CONTEXT_LOST/.test(t)) errs.push(m.type() + ': ' + t.slice(0, 200)); });
p.on('pageerror', e => errs.push('pageerror: ' + e.message));
await p.goto(`http://localhost:${port}/index.html`);
await p.waitForFunction(() => !!(window.__timelines && window.__timelines.main), null, { timeout: 120000 });
const res = await p.evaluate(() => {
  const tl = window.__timelines.main; const out = [];
  D.shots.forEach((s, i) => { const t1 = i < D.shots.length - 1 ? D.shots[i + 1].t : D.end.start; const t = s.t + (t1 - s.t) * 0.5;
    tl.seek(t, false); const el = (() => { try { return eval(s.scene).el; } catch (e) { return null; } })(); const cvs = el ? [...el.querySelectorAll('canvas')] : [];
    let best = cvs.length ? 0 : 255; for (const c of cvs) { if (getComputedStyle(c).opacity === '0') continue; const g = document.createElement('canvas'); g.width = 54; g.height = 96; const x = g.getContext('2d'); x.drawImage(c, 0, 0, 54, 96);
      const d = x.getImageData(0, 0, 54, 96).data; let m = 0; for (let k = 0; k < d.length; k += 4) m += d[k] + d[k + 1] + d[k + 2]; best = Math.max(best, m / (d.length / 4) / 3); }
    out.push({ scene: s.scene, t: +t.toFixed(2), opacity: el ? getComputedStyle(el).opacity : 'missing', mean: +best.toFixed(1) }); });
  return out; });
let bad = 0;
for (const r of res) { const ok = r.mean > 12 && r.opacity !== '0' && r.opacity !== 'missing'; if (!ok) bad++; console.log(`${ok ? 'ok  ' : 'FAIL'} ${r.scene.padEnd(4)} t=${r.t} opacity=${r.opacity} brightness=${r.mean}`); }
const uniq = [...new Set(errs)]; for (const e of uniq.slice(0, 12)) console.log('ERR ' + e);
console.log(bad || uniq.length ? `GATE FAIL: ${bad} blank/hidden shot(s), ${uniq.length} console error(s)` : `GATE PASS: ${res.length} shots drawn, 0 console errors`);
await b.close(); srv.close(); process.exit(bad || uniq.length ? 1 : 0);
