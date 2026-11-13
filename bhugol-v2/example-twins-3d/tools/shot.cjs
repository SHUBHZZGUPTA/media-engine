const puppeteer = require('/home/claude/hf/node_modules/puppeteer-core');
(async () => { const b = await puppeteer.launch({ executablePath: process.env.HYPERFRAMES_BROWSER_PATH, args: ['--allow-file-access-from-files', '--no-sandbox'] });
  const p = await b.newPage(); await p.setViewport({ width: 1080, height: 1920 });
  for (const [out, q] of JSON.parse(process.argv[2])) { await p.goto('file://' + __dirname + '/make.html?' + q); await p.evaluate(() => document.fonts.ready); await new Promise(r => setTimeout(r, 600));
    await (await p.$('#c')).screenshot({ path: __dirname + '/' + out }); }
  await b.close(); })();
