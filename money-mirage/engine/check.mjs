// node check.mjs <projdir> : prints missing anchors, JS errors, and the longest gaps between visual events per chapter
import { chromium } from 'playwright';
const dir = process.argv[2];
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell', args: ['--allow-file-access-from-files'] });
const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } }); const errs = [];
pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
await pg.addInitScript(() => { window.__timelines = {}; });
await pg.goto('file://' + dir + '/index.html'); await pg.waitForFunction(() => window.__ready, null, { timeout: 60000 }).catch(e => errs.push('not ready ' + e.message));
const r = await pg.evaluate(() => { const ev = window.__events.filter(e => e[1] !== 'chapter').map(e => e[0]).sort((a, b) => a - b); const gaps = [];
  for (let i = 1; i < ev.length; i++) gaps.push([+(ev[i] - ev[i - 1]).toFixed(2), ev[i - 1]]); gaps.sort((a, b) => b[0] - a[0]);
  return { missing: window.__missing, events: ev.length, sfx: window.__sfx.length, top_gaps: gaps.slice(0, 6) }; });
console.log(JSON.stringify(r)); if (errs.length) console.log('ERRORS', errs.slice(0, 10)); await b.close(); process.exit(0);
