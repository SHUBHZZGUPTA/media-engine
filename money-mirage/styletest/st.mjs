import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell', args: ['--allow-file-access-from-files'] });
const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } }); await pg.goto('file:///home/claude/mm-work/styletest/st.html'); await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(500);
for (const id of ['a', 'b']) await pg.locator('#' + id).screenshot({ path: `/home/claude/mm-work/styletest/style_archival_${id}.jpg`, type: 'jpeg', quality: 88 });
await b.close();
