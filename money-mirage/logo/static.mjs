import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell', args: ['--allow-file-access-from-files'] });
const pg = await b.newPage({ viewport: { width: 2400, height: 2400 } }); await pg.goto('file:///home/claude/mm-work/logo/static.html'); await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(500);
await pg.locator('#lockup').screenshot({ path: '/home/claude/mm-work/logo/MoneyMirage_logo_transparent.png', omitBackground: true });
await pg.locator('#icon').screenshot({ path: '/home/claude/mm-work/logo/MoneyMirage_channel_icon_800.png' });
await b.close();
