import { chromium } from 'playwright'; import fs from 'fs';
const [dir, outp] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell', args: ['--allow-file-access-from-files'] });
const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
await pg.addInitScript(() => { window.__timelines = {}; });
await pg.goto('file://' + dir + '/index.html'); await pg.waitForFunction(() => window.__ready, null, { timeout: 60000 });
const r = await pg.evaluate(() => ({ sfx: window.__sfx, events: window.__events }));
fs.writeFileSync(outp, JSON.stringify(r.sfx)); fs.writeFileSync(outp.replace('sfx.json', 'events.json'), JSON.stringify(r.events));
console.log('sfx', r.sfx.length); await b.close(); process.exit(0);
