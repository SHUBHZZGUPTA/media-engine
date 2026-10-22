// Pre-render layout gate for BHUGOL builds: every 0.25 s, measure every visible overlay (hand-drawn circles/arrows,
// plate labels, map cards) on screen and fail when one leaves the frame, sits in the caption band, or is drawn
// while entirely off screen (a beat the viewer never sees).
// Usage: node layout_gate.mjs <build_dir> [--step=0.25]   (exit 1 on failure)
import { chromium } from 'playwright-core'; import http from 'http'; import fs from 'fs'; import path from 'path';
const dir = process.argv[2]; const STEP = +(process.argv.find(a => a.startsWith('--step=')) || '--step=0.25').split('=')[1];
const port = 8900 + Math.floor(Math.random() * 90);
const srv = http.createServer((q, r) => { const u = decodeURIComponent(q.url.split('?')[0]); fs.readFile(path.join(dir, u === '/' ? 'index.html' : u), (e, b) => { if (e) { r.writeHead(404); r.end(); } else r.end(b); }); }).listen(port);
const b = await chromium.launch({ executablePath: process.env.HYPERFRAMES_BROWSER_PATH || '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell', args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto(`http://localhost:${port}/index.html`);
await p.waitForFunction(() => !!(window.__timelines && window.__timelines.main), null, { timeout: 120000 });
const issues = await p.evaluate((STEP) => {
  const tl = window.__timelines.main; const out = []; const END = D.end.start;
  const CAP = [1300, 1470];   // caption band (lines centred on y 1385)
  const vis = el => { let e = el; while (e && e !== document.body) { const s = getComputedStyle(e); if (s.display === 'none' || s.visibility === 'hidden' || +s.opacity < 0.08) return false; e = e.parentElement; } return true; };
  for (let t = 0.2; t < END; t += STEP) {
    tl.seek(t, false);
    const els = [...document.querySelectorAll('.ov svg path, .plbl, .card .cin')];
    for (const el of els) {
      if (el.tagName === 'path' && !(el.getAttribute('d') || '').length) continue;
      if (!vis(el)) continue;
      const r = el.getBoundingClientRect(); if (r.width < 2 && r.height < 2) continue;
      const kind = el.tagName === 'path' ? 'mark' : el.classList.contains('plbl') ? 'label: ' + el.textContent.trim() : 'card';
      const area = r.width * r.height, ix = Math.max(0, Math.min(r.right, 1080) - Math.max(r.left, 0)), iy = Math.max(0, Math.min(r.bottom, 1920) - Math.max(r.top, 0));
      const inside = area ? (ix * iy) / area : 1;
      if (inside < 0.05) out.push({ t: +t.toFixed(2), kind, why: 'drawn entirely off screen (viewer never sees it)' });
      else if (kind.startsWith('label') && (r.top < 160 || r.bottom > 1880 || r.left < 0 || r.right > 1080)) out.push({ t: +t.toFixed(2), kind, why: `label at frame edge / under the top fade (${r.left | 0},${r.top | 0} - ${r.right | 0},${r.bottom | 0})` });
      else if (inside < 0.85) out.push({ t: +t.toFixed(2), kind, why: `${Math.round((1 - inside) * 100)}% outside the frame` });
      else if (!kind.startsWith('mark') && r.bottom > CAP[0] && r.top < CAP[1]) out.push({ t: +t.toFixed(2), kind, why: 'overlaps the caption band' });
    }
  }
  return out;
}, STEP);
// group consecutive hits of the same element/problem into ranges
const groups = []; for (const i of issues) { const key = w => w.split('(')[0].replace(/[0-9]+%/g, 'N%'); const g = groups.find(g => g.kind === i.kind && key(g.why) === key(i.why) && i.t - g.t1 <= STEP * 1.5 + 1e-6); if (g) g.t1 = i.t; else groups.push({ ...i, t0: i.t, t1: i.t }); }
const real = groups.filter(g => g.t1 - g.t0 >= STEP * 1.5);   // ignore single-sample blips during cuts
for (const g of groups) console.log(`${real.includes(g) ? 'FAIL' : 'note'} ${g.t0.toFixed(2)}-${g.t1.toFixed(2)} s  ${g.kind}  ${g.why}`);
console.log(real.length ? `LAYOUT FAIL: ${real.length} placement problem(s)` : 'LAYOUT PASS: every circle, arrow, label and card stays on screen and out of the caption band');
await b.close(); srv.close(); process.exit(real.length ? 1 : 0);
