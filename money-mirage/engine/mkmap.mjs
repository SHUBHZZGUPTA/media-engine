// Equirectangular world plate, Desert Night colours. x=(lon+180)/360*W, y=(90-lat)/180*H
import fs from 'fs'; import { geoPath, geoEquirectangular, geoGraticule10 } from 'd3-geo'; import { feature, mesh } from 'topojson-client';
import { chromium } from 'playwright';
const W = 8192, H = 4096;
const topo = JSON.parse(fs.readFileSync('node_modules/world-atlas/countries-50m.json'));
const proj = geoEquirectangular().scale(W / (2 * Math.PI)).translate([W / 2, H / 2]);
const p = geoPath(proj);
const land = p(feature(topo, topo.objects.land)), borders = p(mesh(topo, topo.objects.countries, (a, b) => a !== b)), grat = p(geoGraticule10());
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
<defs><radialGradient id="o" cx="50%" cy="45%" r="75%"><stop offset="0" stop-color="#13213A"/><stop offset="1" stop-color="#0A1222"/></radialGradient></defs>
<rect width="${W}" height="${H}" fill="url(#o)"/><path d="${grat}" fill="none" stroke="#1A2A45" stroke-width="2"/>
<path d="${land}" fill="#25365A" stroke="#3B5384" stroke-width="3"/><path d="${borders}" fill="none" stroke="#3E5687" stroke-width="2" stroke-opacity=".8"/></svg>`;
fs.writeFileSync('engine/assets/world.svg', svg);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell' });
const pg = await b.newPage({ viewport: { width: W, height: H } });
await pg.setContent(`<html><body style="margin:0">${svg}</body></html>`);
await pg.screenshot({ path: 'engine/assets/world.jpg', type: 'jpeg', quality: 88 });
await b.close(); console.log('ok');
