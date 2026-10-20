import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell', args: ['--allow-file-access-from-files'] });
const pg = await b.newPage({ viewport: { width: 1280, height: 720 } }); await pg.goto('file:///home/claude/mm-work/thumb/thumb.html'); await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(300);
await pg.locator('#t').screenshot({ path: '/home/claude/mm-work/thumb/MoneyMirage_thumbnail.png' }); await b.close();
