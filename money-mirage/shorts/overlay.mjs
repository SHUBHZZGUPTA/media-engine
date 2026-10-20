import { chromium } from 'playwright'; import fs from 'fs';
const S = JSON.parse(fs.readFileSync('/home/claude/mm-work/shorts/shorts.json'));
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell', args: ['--allow-file-access-from-files'] });
const pg = await b.newPage({ viewport: { width: 1080, height: 1920 } });
const k = s => s.replace(/\*([^*]+)\*/g, '<b>$1</b>');
for (const s of S) {
  fs.writeFileSync('/home/claude/mm-work/shorts/_ov.html', `<html><head><style>@font-face{font-family:Brico;font-weight:800;src:url(brico800.woff2)}@font-face{font-family:Inter;font-weight:800;src:url(inter800.woff2)}
  body{margin:0;background:transparent;width:1080px;height:1920px;position:relative;overflow:hidden}
  .t{position:absolute;left:60px;right:60px;top:300px;text-align:center;font:800 92px/1.02 Brico;color:#F3EBDD;text-shadow:0 6px 0 #050A14,0 0 30px rgba(0,0,0,.7)}.t b{color:#E9B44C}
  .s{position:absolute;left:60px;right:60px;top:540px;text-align:center;font:800 40px Inter;color:#E2614B;text-shadow:0 3px 0 #050A14}
  .w{position:absolute;left:0;right:0;bottom:250px;text-align:center;font:800 54px Brico;color:#E9B44C;letter-spacing:1px}.w span{color:#F3EBDD}
  .f{position:absolute;left:0;right:0;bottom:190px;text-align:center;font:800 30px Inter;color:#8D98B0;letter-spacing:.12em}</style></head>
  <body><div class=t>${k(s.t1)}<br>${k(s.t2)}</div><div class=s>${s.t3}</div><div class=w>MONEY <span>MIRAGE</span></div><div class=f>FULL STORY ON THE CHANNEL</div></body></html>`); await pg.goto('file:///home/claude/mm-work/shorts/_ov.html');
  await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(200);
  await pg.screenshot({ path: `/home/claude/mm-work/shorts/ov_${s.id}.png`, omitBackground: true });
}
await b.close(); console.log('ok');
