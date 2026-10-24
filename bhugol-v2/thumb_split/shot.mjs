// Screenshots #v and #w from a split_<lang>.html page. Usage (cwd with playwright-core): node shot.mjs <page.html> <out_base>; needs HYPERFRAMES_BROWSER_PATH
import { chromium } from 'playwright-core';
const [html, out] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: process.env.HYPERFRAMES_BROWSER_PATH }); const p = await b.newPage({ viewport: { width: 1280, height: 2700 } });
await p.goto('file://' + html); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(800);
await (await p.$('#v')).screenshot({ path: out + '_v.png' }); await (await p.$('#w')).screenshot({ path: out + '_w.png' }); await b.close();
