import { chromium } from "/home/claude/japan/node_modules/playwright/index.mjs";
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell' });
const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
await p.goto('file:///home/claude/ph/thumb/' + process.argv[2]); await p.waitForTimeout(800);
await p.screenshot({ path: '/home/claude/ph/thumb/' + process.argv[3], type: 'jpeg', quality: 92 }); await b.close();
