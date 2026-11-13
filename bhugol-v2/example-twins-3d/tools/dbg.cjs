const puppeteer = require('/home/claude/hf/node_modules/puppeteer-core');
(async () => {
  const b = await puppeteer.launch({ executablePath: process.env.HYPERFRAMES_BROWSER_PATH, args: ['--use-angle=swiftshader', '--allow-file-access-from-files', '--no-sandbox'] });
  const p = await b.newPage(); p.on('console', m => console.log('console:', m.text())); p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto('file://' + process.argv[2] + '/index.html'); await new Promise(r => setTimeout(r, 15000));
  const r = await p.evaluate(src => { try { return String(eval(src)); } catch (e) { return 'E:' + e.message; } }, process.argv[3]);
  console.log(r); await b.close();
})();
