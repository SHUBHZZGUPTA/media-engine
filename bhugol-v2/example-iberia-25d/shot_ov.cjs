const puppeteer = require('/home/claude/work/node_modules/puppeteer-core');
(async () => { const b = await puppeteer.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell', args: ['--allow-file-access-from-files', '--no-sandbox'] });
  const p = await b.newPage(); await p.setViewport({ width: 1080, height: 1920 }); await p.goto('file:///home/claude/iberia/cover_ov.html'); await p.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 400)); await p.screenshot({ path: '/home/claude/iberia/cover_ov.png', omitBackground: true }); await b.close(); })();
