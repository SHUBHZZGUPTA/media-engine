// Pre-render each country's flag clipped to its border, in world coordinates at half resolution (transparent PNG).
const puppeteer = require('/home/claude/work/node_modules/puppeteer-core'); const fs = require('fs');
const M = JSON.parse(fs.readFileSync('/home/claude/iberia/assets/map.json'));
const tpl = fs.readFileSync('/home/claude/iberia/template.html', 'utf8'); const fsrc = tpl.slice(tpl.indexOf('function flagSVG'), tpl.indexOf('/* ================= camera'));
(async () => { const b = await puppeteer.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell', args: ['--no-sandbox'] });
  for (const k of ['ESP', 'PRT']) {
    const [x0, y0, x1, y1] = M.bbox[k]; const W = x1 - x0 + 8, H = y1 - y0 + 8, s = 1.0, pw = Math.ceil(W * s), ph = Math.ceil(H * s);
    const p = await b.newPage(); await p.setViewport({ width: pw, height: ph });
    await p.setContent(`<html><body style="margin:0;background:transparent"><script>${fsrc}</script><div id="c"></div><script>
      document.getElementById('c').innerHTML = '<svg width="${pw}" height="${ph}" viewBox="${x0 - 4} ${y0 - 4} ${W} ${H}"><defs><clipPath id="cp"><path d="${M.paths[k]}"/></clipPath></defs>' +
      '<g clip-path="url(#cp)"><svg x="${x0 - 4}" y="${y0 - 4}" width="${W}" height="${H}" viewBox="0 0 1000 500" preserveAspectRatio="none">' + flagSVG('${k}', 1000, 500, true) + '</svg></g></svg>';
    </script></body></html>`);
    await p.screenshot({ path: `/home/claude/iberia/assets/flag_${k}.png`, omitBackground: true }); console.log(k, pw, ph); await p.close(); }
  await b.close(); })();
