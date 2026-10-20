import { chromium } from '/opt/npm-tools/node_modules/playwright/index.mjs';
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 2700 } });
await p.goto('file://' + process.argv[2]); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
await (await p.$('#v')).screenshot({ path: 'thumb2_v.png' }); await (await p.$('#w')).screenshot({ path: 'thumb2_w.png' }); await b.close();
