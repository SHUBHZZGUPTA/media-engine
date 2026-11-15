const puppeteer = require('/home/claude/work/node_modules/puppeteer-core');
(async () => {
  const b = await puppeteer.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell', args: ['--allow-file-access-from-files', '--no-sandbox'] });
  const p = await b.newPage(); const errs = [];
  p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.setViewport({ width: 1080, height: 1920 });
  await p.goto('file://' + process.argv[2] + '/index.html');
  await p.waitForFunction('!!(window.__timelines && window.__timelines.main)', { timeout: 60000 }).catch(e => errs.push('timeout ' + e));
  const evs = await p.evaluate(() => window.__EVS || null);
  require('fs').writeFileSync(process.argv[2] + '/evs.json', JSON.stringify(evs));
  console.log('errors:', errs.slice(0, 10)); console.log('evs', evs && evs.length);
  await b.close();
})();
