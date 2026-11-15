// Camera footprint of every 3D map shot (15 Nov 2026, after the Gibraltar Short's blocky edges).
// Plays a built HyperFrames page frame by frame (no GPU needed: the map is rendered on CPU but only the camera matters),
// and records, per map, the ground each visible frame shows and the finest metres per screen pixel any frame needs.
// The sharp imagery patch is then sized from this (map3d_prep.py job --footprint ...), so no shot can leave it.
//
// Usage: NODE_PATH=<dir with node_modules/puppeteer-core> node footprint.cjs <build_dir> <out.json> [--step 0.2] [--dur 82.6] [--maxmag 2.5]
// QA gate: exits 1 when any frame stretches its imagery more than --maxmag x ("soft" list = time, stretch, place). Run it on the final build.
//   build_dir: a HyperFrames build whose template has the map3 footprint probe (window.__FP / __FPD) and window.__seek
//   out.json:  { "<map prefix>": { "bbox": [lon0, lon1, lat0, lat1], "mpp_min": m, "mpp_p10": m, "frames": n, "horizon": bool,
//                 "close": bbox + 15% margin, "worst_t": s, "base_mpp": m/px of the regional plate,
//                 "zones": {lt100, lt300, lt750}: bbox (+15%) of the frames needing finer than 100/300/750 m per screen pixel,
//                 "patch": zones.lt300 -> fetch the sharp patch for this (null = no shot needs one), "soft": frames stretching imagery > maxmag },
//            "preview_frames": [closest frame of each map shot] -> gpu/hf3d_render.py only_frames for a GPU stills preview }
// Env: CHROME (browser path; default: the headless shell from example-twins-3d/tools/env.sh).
const fs = require('fs'), path = require('path'), http = require('http');
const puppeteer = require('puppeteer-core');
const [dir, outp] = process.argv.slice(2);
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > 0 ? Number(process.argv[i + 1]) : d; };
const STEP = arg('--step', 0.2), MAXMAG = arg('--maxmag', 2.5), NATIVE = arg('--native', 500);   // NATIVE: true resolution of the regional plate (Blue Marble ~500 m)
let DUR = arg('--dur', 0);
if (!DUR) { try { DUR = JSON.parse(fs.readFileSync(path.join(dir, 'times.json'))).dur; } catch (e) { console.error('pass --dur'); process.exit(2); } }
function imgW(f) { const b = fs.readFileSync(f); for (let i = 2; i < b.length;) { if (b[i] !== 0xFF) return 0; const m = b[i + 1], L = b.readUInt16BE(i + 2); if (m >= 0xC0 && m <= 0xC3) return b.readUInt16BE(i + 7); i += 2 + L; } return 0; }   // JPEG width
const CHROME = process.env.CHROME || '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell';
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.mp3': 'audio/mpeg', '.wav': 'audio/wav', '.svg': 'image/svg+xml' };
const srv = http.createServer((q, r) => { const f = path.join(dir, decodeURIComponent(q.url.split('?')[0])); fs.readFile(f, (e, b) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' }); r.end(b); }); });
srv.listen(0, async () => {
  const port = srv.address().port;
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'shell', protocolTimeout: 600000, args: ['--no-sandbox', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage(); await p.setViewport({ width: 1080, height: 1920 });
  p.on('pageerror', e => console.log('PAGEERR', e.message));
  await p.goto(`http://127.0.0.1:${port}/index.html`); await p.waitForFunction(() => !!window.__seek, { timeout: 600000 });
  // outside the HyperFrames runtime the page has no size: give it the video frame (otherwise every layer is 0 px tall)
  await p.addStyleTag({ content: 'html,body{width:1080px;height:1920px;margin:0;overflow:hidden}' });
  await p.evaluate(() => { window.__seek(0.5); window.__FP = 1; window.__FPD = []; });
  for (let t = 0; t <= DUR; t += STEP) await p.evaluate(t => { window.__FPT = t; window.__seek(Math.max(t, 0.001)); }, t);   // never return the timeline: it hangs puppeteer
  const D = await p.evaluate(() => window.__FPD);
  await b.close(); srv.close();
  const by = {};
  for (const s of D) { (by[s.map] = by[s.map] || []).push(s); }
  const out = {};
  for (const [m, S] of Object.entries(by)) {
    const pts = S.flatMap(s => s.pts); if (!pts.length) continue;
    const lo = pts.map(q => q.lon), la = pts.map(q => q.lat), mp = S.map(s => s.mpp).filter(x => x < 1e8).sort((a, b) => a - b);
    const bb = [Math.min(...lo), Math.max(...lo), Math.min(...la), Math.max(...la)], mx = (bb[1] - bb[0]) * .075, my = (bb[3] - bb[2]) * .075;
    const worst = S.reduce((a, s) => s.mpp < a.mpp ? s : a, S[0]);
    // frames that need more detail than the regional base plate (ne.jpg) can give: these alone decide the sharp patch
    let base = null; try { const M = { bbox: S[0].bb }; const W = imgW(path.join(dir, 'assets', m, 'ne.jpg'));
      base = (M.bbox[1] - M.bbox[0]) * 111320 * Math.cos((M.bbox[2] + M.bbox[3]) / 2 * Math.PI / 180) / W; } catch (e) {}
    // magnification gate: imagery under each sampled pixel vs. that pixel's ground size. Sharp patch (if on and covering the point):
    // max(texture m/px, 30 m Landsat); otherwise the regional plate: max(texture m/px, NATIVE m Blue Marble). > MAXMAG = soft/blocky.
    let soft = [];
    try { const cw = imgW(path.join(dir, 'assets', m, 'pa_close.jpg')), nw = imgW(path.join(dir, 'assets', m, 'ne.jpg')), bb = S[0].bb;
      const kx = Math.cos((bb[2] + bb[3]) / 2 * Math.PI / 180) * 111320, baseSrc = Math.max((bb[1] - bb[0]) * kx / nw, NATIVE);
      for (const s of S) { let w = 0, at = null;
        const cb = s.cb, patchSrc = cb ? Math.max((cb[1] - cb[0]) * kx / cw, 30) : 1e9;
        for (const q of s.pts) { if (!q.m) continue; const inP = s.cl && cb && q.lon > cb[0] && q.lon < cb[1] && q.lat > cb[2] && q.lat < cb[3];
          const mag = (inP ? patchSrc : baseSrc) / q.m; if (mag > w) { w = mag; at = q; } }
        if (w > MAXMAG) soft.push({ t: +s.t.toFixed(2), mag: +w.toFixed(1), lon: +at.lon.toFixed(3), lat: +at.lat.toFixed(3) }); } } catch (e) { soft = [{ error: String(e) }]; }
    // zones: bbox (+15%) of only the frames that need finer than N metres per screen pixel.
    // The sharp Landsat patch (~30 m) is fetched for zone 300; frames needing 300-750 m are served by the regional plate.
    const zone = th => { const P = S.filter(s => s.mpp < th).flatMap(s => s.pts); if (!P.length) return null;
      const a0 = Math.min(...P.map(q => q.lon)), a1 = Math.max(...P.map(q => q.lon)), b0 = Math.min(...P.map(q => q.lat)), b1 = Math.max(...P.map(q => q.lat)), ex = (a1 - a0) * .075, ey = (b1 - b0) * .075;
      return [a0 - ex, a1 + ex, b0 - ey, b1 + ey].map(v => +v.toFixed(3)); };
    const zones = { lt100: zone(100), lt300: zone(300), lt750: zone(750) }, fine = zones.lt300;
    out[m] = { bbox: bb.map(v => +v.toFixed(4)), close: [bb[0] - mx, bb[1] + mx, bb[2] - my, bb[3] + my].map(v => +v.toFixed(3)), mpp_min: Math.round(mp[0]), mpp_p10: Math.round(mp[Math.floor(mp.length * .1)]),
      frames: S.length, horizon: S.some(s => s.hz), worst_t: +worst.t.toFixed(2),
      base_mpp: base && Math.round(base), zones, patch: fine, soft_frames: soft.length, soft: soft.slice(0, 40) };   // patch = zone lt300: fetch the sharp patch for it; null = no shot gets close enough to need one
  }
  // preview_frames: the closest frame of every continuous map shot (30 fps frame numbers) -> hf3d_render.py "only_frames"
  const prev = new Set();
  for (const S of Object.values(by)) { S.sort((a, b) => a.t - b.t); let run = [];
    const flush = () => { if (run.length) { const w = run.reduce((a, s) => s.mpp < a.mpp ? s : a, run[0]); prev.add(Math.round(w.t * 30)); } run = []; };
    for (const s of S) { if (run.length && s.t - run[run.length - 1].t > STEP * 1.5) flush(); run.push(s); } flush(); }
  out.preview_frames = [...prev].sort((a, b) => a - b);
  fs.writeFileSync(outp, JSON.stringify(out, null, 1)); console.log(JSON.stringify(out, null, 1));
  const bad = Object.entries(out).filter(([k, v]) => v && v.soft_frames); for (const [k, v] of bad) console.log(`SOFT ${k}: ${v.soft_frames} frames, worst ${JSON.stringify(v.soft.reduce((a, b) => (b.mag || 0) > (a.mag || 0) ? b : a, {}))}`);
  process.exit(bad.length ? 1 : 0);
});
