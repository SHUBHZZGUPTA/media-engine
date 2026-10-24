import { rng, fractal, type Ctx, type P } from "./core";
import { INTER900, MUKTA800, LOGO } from "./fontdata";

// MONEY MIRAGE · MIXED-MEDIA KIT for 9:16 Shorts, drawn with anidoodle (Apache-2.0).
// Five looks share one desk: ARCHIVAL SCRAPBOOK (foxed album page, torn cards, tape, ransom tiles,
// red pen, rubber stamp) is the base; MARKER COMIC (cel fill, one hard shadow edge, one heavy
// contour thickening away from the light, streaky marker texture) draws the objects; accents are
// TOY-THEATRE PAPER COLLAGE (proscenium of patterned card, flats with a gap and a shadow, cut-outs
// with a white sticker margin), NEWSPRINT (groundwood paper, column rules, halftone dots, one
// orange spot) and TOY BRICK (anidoodle's toyBrickKit, used by the film directly).
// Text is one face (Inter 900; Mukta 800 carries ₹ and Devanagari). Pure functions of the frame.

// ---------------------------------------------------------------- fonts + logo
export const FONT = "Inter9, Mukta8";
if (typeof FontFace !== "undefined" && typeof document !== "undefined") {
  const faces = [new FontFace("Inter9", `url(data:font/woff2;base64,${INTER900})`), new FontFace("Mukta8", `url(data:font/woff2;base64,${MUKTA800})`)];
  (globalThis as unknown as { __FONTS_READY__: Promise<unknown> }).__FONTS_READY__ = Promise.all(faces.map((f) => f.load().then((l) => { document.fonts.add(l); })));
}
export const LOGO_URL = LOGO;

export const W = 1080, H = 1920, FPS = 30;
export const sec = (s: number) => Math.round(s * FPS);
export const clamp01 = (v: number) => (v <= 0 ? 0 : v >= 1 ? 1 : v);
export const span = (f: number, a: number, b: number) => (b <= a ? (f >= a ? 1 : 0) : clamp01((f - a) / (b - a)));
export const easeOut = (t: number) => 1 - (1 - clamp01(t)) ** 3;
export const easeIO = (t: number) => { const x = clamp01(t); return x < 0.5 ? 4 * x * x * x : 1 - (-2 * x + 2) ** 3 / 2; };
export const back = (t: number) => { const x = clamp01(t), c = 1.9; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2; };

// palette (the scrapbook plate's, plus marker inks)
export const PARCH = "#e8d6b2", INK = "#241b15", NAVY = "#22335a", TEAL = "#4f8f8a", PINK = "#d9a5a0", RED = "#c23a2a", STAMP = "#b8322a", MUSTARD = "#d6a13c", GOLD = "#f2b632", CREAM = "#f6efe0";
export const KEY = "#FF4D3D";

// ---------------------------------------------------------------- geometry helpers
export const path = (c: Ctx, pts: P[], close = true) => { c.beginPath(); pts.forEach(([x, y], i) => (i ? c.lineTo(x, y) : c.moveTo(x, y))); if (close) c.closePath(); };
export const rect = (w: number, h: number, cx = 0, cy = 0): P[] => [[cx - w / 2, cy - h / 2], [cx + w / 2, cy - h / 2], [cx + w / 2, cy + h / 2], [cx - w / 2, cy + h / 2]];
export const rrect = (w: number, h: number, r: number, cx = 0, cy = 0, n = 5): P[] => {
  const out: P[] = []; const cs: [number, number, number][] = [[cx + w / 2 - r, cy - h / 2 + r, -Math.PI / 2], [cx + w / 2 - r, cy + h / 2 - r, 0], [cx - w / 2 + r, cy + h / 2 - r, Math.PI / 2], [cx - w / 2 + r, cy - h / 2 + r, Math.PI]];
  cs.forEach(([x, y, a0]) => { for (let k = 0; k <= n; k++) { const a = a0 + (k / n) * (Math.PI / 2); out.push([x + Math.cos(a) * r, y + Math.sin(a) * r]); } }); return out;
};
export const ellipse = (cx: number, cy: number, rx: number, ry: number, n = 40): P[] => Array.from({ length: n }, (_, i) => { const a = (i / n) * Math.PI * 2; return [cx + Math.cos(a) * rx, cy + Math.sin(a) * ry] as P; });
export const xf = (pts: P[], dx: number, dy: number, rot = 0, sc = 1): P[] => { const c = Math.cos(rot), s = Math.sin(rot); return pts.map(([x, y]) => [dx + (x * c - y * s) * sc, dy + (x * s + y * c) * sc]); };
/** resample a closed ring to roughly one point per `step` px */
export const resampleRing = (pts: P[], step = 6): P[] => {
  const out: P[] = []; const n = pts.length;
  for (let i = 0; i < n; i++) { const a = pts[i], b = pts[(i + 1) % n], L = Math.hypot(b[0] - a[0], b[1] - a[1]), k = Math.max(1, Math.round(L / step)); for (let j = 0; j < k; j++) out.push([a[0] + ((b[0] - a[0]) * j) / k, a[1] + ((b[1] - a[1]) * j) / k]); }
  return out;
};
/** a torn edge: the ring pushed in and out by fractal noise */
export const tear = (pts: P[], amp: number, seed: number): P[] => resampleRing(pts, 5).map(([x, y], i) => { const n = fractal(seed, x * 0.02, y * 0.02, 1, 1, 3) - 0.5, r = rng(seed * 997 + i)(); return [x + n * amp * 2 + (r - 0.5) * amp * 0.6, y + (fractal(seed + 7, x * 0.02, y * 0.02, 1, 1, 3) - 0.5) * amp * 2] as P; });
const bbox = (pts: P[]) => { let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; for (const [x, y] of pts) { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); } return { x0, y0, x1, y1 }; };

// ---------------------------------------------------------------- text (one face)
export type TxtO = { stroke?: number; strokeColor?: string; align?: CanvasTextAlign; sc?: number; alpha?: number; rot?: number; weight?: number };
export const txt = (c: Ctx, s: string, x: number, y: number, size: number, color: string, o: TxtO = {}) => {
  const k = o.sc ?? 1, a = o.alpha ?? 1; if (k <= 0 || a <= 0) return;
  c.save(); c.translate(x, y); if (o.rot) c.rotate(o.rot); c.scale(k, k); c.globalAlpha = a;
  c.font = `${o.weight ?? 900} ${size}px ${FONT}`; c.textAlign = o.align ?? "center"; c.textBaseline = "middle"; c.lineJoin = "round";
  if (o.stroke) { c.strokeStyle = o.strokeColor ?? "rgba(20,14,10,0.94)"; c.lineWidth = o.stroke; c.strokeText(s, 0, 0); }
  c.fillStyle = color; c.fillText(s, 0, 0); c.restore();
};
export const textW = (c: Ctx, s: string, size: number) => { c.save(); c.font = `900 ${size}px ${FONT}`; const w = c.measureText(s).width; c.restore(); return w; };

// ---------------------------------------------------------------- shadows
export const dropShadow = (c: Ctx, pts: P[], off: P, blur: number, alpha: number, color = "#3b2a14") => {
  c.save(); c.shadowColor = color; c.shadowBlur = blur; c.shadowOffsetX = off[0]; c.shadowOffsetY = off[1]; c.globalAlpha = alpha; c.fillStyle = color; path(c, pts); c.fill(); c.restore();
};

// ---------------------------------------------------------------- BACKGROUNDS
/** archival scrapbook page: parchment, age clouds, handled edges, a fold, foxing */
export const scrapPage = (c: Ctx, seed = 301) => {
  const r = rng(seed); c.fillStyle = PARCH; c.fillRect(0, 0, W, H);
  for (let i = 0; i < 22; i++) { const x = r() * W, y = r() * H, R = 180 + r() * 380, g = c.createRadialGradient(x, y, 0, x, y, R), col = r() < 0.55 ? "#f4e7c9" : "#c9a671"; g.addColorStop(0, col); g.addColorStop(1, col + "00"); c.globalAlpha = 0.3; c.fillStyle = g; c.fillRect(x - R, y - R, R * 2, R * 2); }
  const eg = (x0: number, y0: number, x1: number, y1: number) => { const g = c.createLinearGradient(x0, y0, x1, y1); g.addColorStop(0, "rgba(120,78,30,0.36)"); g.addColorStop(1, "rgba(120,78,30,0)"); c.globalAlpha = 1; c.fillStyle = g; c.fillRect(0, 0, W, H); };
  eg(0, 0, 90, 0); eg(W, 0, W - 100, 0); eg(0, 0, 0, 90); eg(0, H, 0, H - 120);
  const fy = 820 + r() * 260; c.globalAlpha = 0.22; c.strokeStyle = "#fff6df"; c.lineWidth = 4; c.beginPath(); c.moveTo(0, fy); c.bezierCurveTo(360, fy - 6, 720, fy + 8, W, fy - 2); c.stroke();
  c.globalAlpha = 0.16; c.strokeStyle = "#7a5424"; c.lineWidth = 1.6; c.beginPath(); c.moveTo(0, fy + 3); c.bezierCurveTo(360, fy - 3, 720, fy + 11, W, fy + 1); c.stroke();
  const drift = (cx: number, cy: number, sx: number, sy: number, n: number, big: number) => { for (let i = 0; i < n; i++) { const x = cx + (r() + r() - 1) * sx, y = cy + (r() + r() - 1) * sy, s = (0.6 + r() * r() * big) * 2.6; c.globalAlpha = 0.16 + r() * 0.24; c.fillStyle = "#a4652a"; c.beginPath(); c.arc(x, y, s, 0, 6.283); c.fill(); if (s > 4) { c.globalAlpha *= 0.45; c.beginPath(); c.arc(x, y, s * 2.3, 0, 6.283); c.fill(); } } };
  drift(1040, 300 + r() * 600, 40, 260, 40, 3); drift(60, 1500 + r() * 200, 70, 90, 34, 4); drift(540, fy, 220, 14, 18, 1.5); drift(900 + r() * 100, 80, 80, 40, 12, 2);
  c.globalAlpha = 1;
};
/** the paper's tooth + a warm vignette, laid over everything at the end */
export const grain = (c: Ctx, f: number, warm = true) => {
  const r = rng(7700 + (f % 6)); c.save(); c.globalAlpha = 0.05; c.fillStyle = "#3a2a1a";
  for (let i = 0; i < 1400; i++) { const x = r() * W, y = r() * H; c.fillRect(x, y, 1.6, 1.6); }
  c.globalAlpha = 1; const g = c.createRadialGradient(W / 2, H * 0.45, H * 0.32, W / 2, H * 0.5, H * 0.78); g.addColorStop(0, "rgba(0,0,0,0)"); g.addColorStop(1, warm ? "rgba(70,40,14,0.38)" : "rgba(0,0,0,0.42)"); c.fillStyle = g; c.fillRect(0, 0, W, H); c.restore();
};
/** marker-comic panel: bleedproof marker paper, a ruled panel, blue pencil ghosts, speed lines */
export const comicPage = (c: Ctx, seed = 41, tint = "#f7f1e4") => {
  const r = rng(seed); c.fillStyle = "#efe6d3"; c.fillRect(0, 0, W, H);
  c.fillStyle = tint; c.fillRect(46, 120, W - 92, H - 240);
  // the pencil ghosts: non-photo blue construction lines
  c.strokeStyle = "rgba(110,160,210,0.28)"; c.lineWidth = 1.4; for (let i = 0; i < 9; i++) { c.beginPath(); const y = 200 + r() * (H - 400); c.moveTo(60, y); c.lineTo(W - 60, y + (r() - 0.5) * 60); c.stroke(); }
  // warm-grey marker wash in the lower panel corner
  // ben-day dots fading in from two corners (printed comic tone)
  c.save(); path(c, rect(W - 92, H - 240, W / 2, H / 2)); c.clip(); c.fillStyle = "rgba(222,120,96,0.30)";
  for (let y = 130; y < H - 120; y += 22) for (let x = 56 + ((y / 22) % 2) * 11; x < W - 46; x += 22) { const t = Math.max(1 - Math.hypot(x - (W - 46), y - 120) / 620, 1 - Math.hypot(x - 46, y - (H - 120)) / 680); if (t > 0) { c.beginPath(); c.arc(x, y, 7.5 * Math.sqrt(t), 0, 6.283); c.fill(); } }
  c.restore();
  // the panel border: one heavy brush-pen line, thicker at the bottom and right (away from the light)
  c.strokeStyle = INK; c.lineJoin = "round"; c.lineWidth = 9; path(c, rect(W - 92, H - 240, W / 2, H / 2)); c.stroke();
  c.lineWidth = 6; c.beginPath(); c.moveTo(W - 40, 126); c.lineTo(W - 40, H - 114); c.lineTo(52, H - 114); c.stroke();
};
/** comic speed lines radiating from a point (a "pow" behind a beat) */
export const burst = (c: Ctx, cx: number, cy: number, r0: number, r1: number, n: number, seed: number, p: number, color = INK) => {
  if (p <= 0) return; const r = rng(seed); c.save(); c.fillStyle = color; c.globalAlpha = 0.85 * clamp01(p * 2);
  for (let i = 0; i < n; i++) { const a = (i / n) * Math.PI * 2 + r() * 0.08, w = 0.012 + r() * 0.02, a0 = r0 * (1 + r() * 0.2), a1 = r0 + (r1 - r0) * easeOut(p) * (0.7 + r() * 0.3);
    c.beginPath(); c.moveTo(cx + Math.cos(a - w) * a0, cy + Math.sin(a - w) * a0); c.lineTo(cx + Math.cos(a) * a1, cy + Math.sin(a) * a1); c.lineTo(cx + Math.cos(a + w) * a0, cy + Math.sin(a + w) * a0); c.fill(); }
  c.restore();
};
/** comic starburst "pow" shape (a jagged balloon) behind a hero number */
export const pow = (c: Ctx, cx: number, cy: number, rx: number, ry: number, fill: string, seed: number, p: number) => {
  if (p <= 0) return; const r = rng(seed), n = 18, k = back(p), pts: P[] = [];
  for (let i = 0; i < n * 2; i++) { const a = (i / (n * 2)) * Math.PI * 2, rr = i % 2 ? 0.72 + r() * 0.1 : 1 + r() * 0.12; pts.push([cx + Math.cos(a) * rx * rr * k, cy + Math.sin(a) * ry * rr * k]); }
  marker(c, pts, fill, { shadow: shade(fill, -0.25), contour: 7, seed });
};
/** toy theatre: proscenium of patterned card, a painted backdrop flat, wings, a floor of boards */
export const theatre = (c: Ctx, f: number, seed = 77, back = "#3d5a73", backB = "#2b4256") => {
  const r = rng(seed); c.fillStyle = "#1e1612"; c.fillRect(0, 0, W, H);
  // backdrop flat: sugar paper, a sun-faded gradient, painted gouache clouds with card edges
  const g = c.createLinearGradient(0, 260, 0, 1500); g.addColorStop(0, back); g.addColorStop(1, backB); c.fillStyle = g; c.fillRect(90, 240, W - 180, 1300);
  fibresFill(c, rect(W - 180, 1300, W / 2, 890), "#ffffff", seed + 1, 0.05);
  for (let i = 0; i < 3; i++) { const cx = 200 + r() * 680, cy = 380 + r() * 360, sh: P[] = []; for (let k = 0; k < 9; k++) { const a = Math.PI + (k / 8) * Math.PI; sh.push([cx + Math.cos(a) * (90 + r() * 40), cy + Math.sin(a) * (50 + r() * 20)]); } sh.push([cx + 120, cy + 8], [cx - 120, cy + 8]); cutout(c, sh, "#e9e2d0", seed + 10 + i, 0, 1, 0.55); }
  // floor: boards in perspective
  c.fillStyle = "#6b4a2c"; c.beginPath(); c.moveTo(90, 1470); c.lineTo(W - 90, 1470); c.lineTo(W, 1700); c.lineTo(0, 1700); c.fill();
  c.strokeStyle = "rgba(30,18,10,0.6)"; c.lineWidth = 2.4; for (let i = -6; i <= 6; i++) { c.beginPath(); c.moveTo(540 + i * 74, 1470); c.lineTo(540 + i * 104, 1700); c.stroke(); }
  // wings: two flats each side, cut card with a white sticker edge, a gap and a shadow on the flat behind
  const wing = (x: number, sgn: number, col: string, s: number) => { const pts: P[] = sgn < 0 ? [[x - 140, 220], [x + 40, 260], [x + 70, 600], [x + 20, 900], [x + 60, 1280], [x - 140, 1520]] : [[x + 140, 220], [x - 40, 260], [x - 70, 600], [x - 20, 900], [x - 60, 1280], [x + 140, 1520]]; cutout(c, pts, col, s, 4, 1, 0.7); };
  wing(90, -1, "#7d2e2e", seed + 20); wing(W - 90, 1, "#7d2e2e", seed + 21); wing(30, -1, "#a03a32", seed + 22); wing(W - 30, 1, "#a03a32", seed + 23);
  // proscenium: patterned card arch (stripes), a scalloped pelmet, gilt edge
  c.save(); const arch: P[] = []; arch.push([0, 0], [W, 0], [W, H], [0, H], [0, 0]); arch.push([70, 1720]); for (let k = 0; k <= 24; k++) { const a = Math.PI + (k / 24) * Math.PI; arch.push([540 + Math.cos(a) * 470, 330 + Math.sin(a) * 150]); } arch.push([1010, 1720], [70, 1720]);
  c.beginPath(); arch.forEach(([x, y], i) => (i ? c.lineTo(x, y) : c.moveTo(x, y))); c.closePath();
  c.shadowColor = "rgba(0,0,0,0.6)"; c.shadowBlur = 30; c.shadowOffsetY = 14; c.fillStyle = "#24343f"; c.fill("evenodd"); c.restore();
  c.save(); c.beginPath(); arch.forEach(([x, y], i) => (i ? c.lineTo(x, y) : c.moveTo(x, y))); c.closePath(); c.clip("evenodd");
  for (let x = -40; x < W + 40; x += 46) { c.fillStyle = (x / 46) % 2 ? "#2f4a5a" : "#20323d"; c.fillRect(x, 0, 23, H); }
  c.fillStyle = "rgba(240,200,120,0.18)"; for (let y = 40; y < H; y += 120) for (let x = 20; x < W; x += 120) { c.beginPath(); c.arc(x + ((y / 120) % 2) * 60, y, 9, 0, 6.283); c.fill(); }
  c.restore();
  c.strokeStyle = "#d7b25c"; c.lineWidth = 7; c.beginPath(); c.moveTo(70, 1720); c.lineTo(70, 330); for (let k = 0; k <= 24; k++) { const a = Math.PI + (k / 24) * Math.PI; c.lineTo(540 + Math.cos(a) * 470, 330 + Math.sin(a) * 150); } c.lineTo(1010, 1720); c.stroke();
  // pelmet scallops
  for (let i = 0; i < 9; i++) { const x = 120 + i * 105, pts: P[] = [[x - 52, 175], [x + 52, 175]]; for (let k = 0; k <= 10; k++) { const a = (k / 10) * Math.PI; pts.push([x + 52 - (k / 10) * 104, 175 + Math.sin(a) * 44]); } cutout(c, pts, i % 2 ? "#a03a32" : "#c4573c", seed + 40 + i, 3, 1, 0.5); }
  // footlights: a warm glow on the floor that breathes
  const fl = c.createRadialGradient(540, 1700, 40, 540, 1500, 900); fl.addColorStop(0, `rgba(255,200,120,${0.32 + 0.04 * Math.sin(f * 0.21)})`); fl.addColorStop(1, "rgba(255,200,120,0)"); c.fillStyle = fl; c.fillRect(0, 0, W, H);
};
/** newsprint: unbleached groundwood, mottled, with column rules and grey text lines */
export const NEWSPRINT = "#e3dcc8";
export const newsPage = (c: Ctx, seed = 91) => {
  const r = rng(seed); c.fillStyle = NEWSPRINT; c.fillRect(0, 0, W, H);
  for (let i = 0; i < 30; i++) { const x = r() * W, y = r() * H, R = 120 + r() * 260, g = c.createRadialGradient(x, y, 0, x, y, R); g.addColorStop(0, "rgba(170,150,110,0.14)"); g.addColorStop(1, "rgba(170,150,110,0)"); c.fillStyle = g; c.fillRect(x - R, y - R, R * 2, R * 2); }
  // masthead rules
  c.fillStyle = "#1d1a17"; c.fillRect(60, 150, W - 120, 8); c.fillRect(60, 166, W - 120, 2.5);
  // the columns of type, as grey lines that break at word ends
  textColumns(c, 60, 210, W - 120, H - 300, 4, seed + 2, 0.32);
};
export const textColumns = (c: Ctx, x0: number, y0: number, w: number, h: number, cols: number, seed: number, alpha = 0.3) => {
  const r = rng(seed), gut = 26, cw = (w - gut * (cols - 1)) / cols; c.save(); c.fillStyle = "#1d1a17"; c.globalAlpha = alpha;
  for (let k = 0; k < cols; k++) { const cx = x0 + k * (cw + gut); for (let y = y0; y < y0 + h; y += 17) { let x = cx; const end = r() < 0.08 ? cx + cw * (0.3 + r() * 0.5) : cx + cw; while (x < end - 6) { const l = Math.min(end - x, 14 + r() * 46); c.fillRect(x, y, l, 6); x += l + 7; } } if (k < cols - 1) { c.globalAlpha = alpha * 0.8; c.fillRect(cx + cw + gut / 2 - 0.8, y0, 1.6, h); c.globalAlpha = alpha; } }
  c.restore();
};
/** fill a shape with an AM halftone screen: black dots sized by tone(x,y) 0..1, at 45 degrees */
export const halftoneFill = (c: Ctx, pts: P[], tone: (x: number, y: number) => number, pitch = 11, color = "#1d1a17", ang = Math.PI / 4) => {
  const b = bbox(pts), cx = (b.x0 + b.x1) / 2, cy = (b.y0 + b.y1) / 2, R = Math.hypot(b.x1 - b.x0, b.y1 - b.y0) / 2 + pitch, ca = Math.cos(ang), sa = Math.sin(ang);
  c.save(); path(c, pts); c.clip(); c.fillStyle = color;
  for (let u = -R; u <= R; u += pitch) for (let v = -R; v <= R; v += pitch) { const x = cx + u * ca - v * sa, y = cy + u * sa + v * ca; if (x < b.x0 - pitch || x > b.x1 + pitch || y < b.y0 - pitch || y > b.y1 + pitch) continue; const t = clamp01(tone(x, y)); if (t < 0.03) continue; c.beginPath(); c.arc(x, y, pitch * 0.62 * Math.sqrt(t), 0, 6.283); c.fill(); }
  c.restore();
};
/** a newspaper clipping: a torn sheet of newsprint carrying a headline area, a halftone picture box and columns */
export const clipping = (c: Ctx, cx: number, cy: number, w: number, h: number, rot: number, seed: number, p: number, from: P = [0, 160]) => {
  if (p <= 0) return null; const e = easeOut(p), dx = from[0] * (1 - e), dy = from[1] * (1 - e), lift = 1 + 5 * (1 - e) ** 2;
  const sh = xf(tear(rect(w, h), 4, seed), cx + dx, cy + dy, rot + 0.12 * (1 - e));
  dropShadow(c, sh, [4 * lift, 8 * lift], 8 + 6 * lift, 0.45 / Math.sqrt(lift));
  c.fillStyle = NEWSPRINT; path(c, sh); c.fill();
  c.save(); path(c, sh); c.clip(); c.translate(cx + dx, cy + dy); c.rotate(rot + 0.12 * (1 - e));
  textColumns(c, -w / 2 + 30, h * 0.06, w - 60, h * 0.42, 3, seed + 5, 0.33);
  c.fillStyle = "#1d1a17"; c.fillRect(-w / 2 + 30, -h / 2 + 34, w - 60, 5); c.fillRect(-w / 2 + 30, -h / 2 + 46, w - 60, 1.6);
  c.restore(); return { cx: cx + dx, cy: cy + dy, rot: rot + 0.12 * (1 - e) };
};

// ---------------------------------------------------------------- PAPER PIECES
const fibresFill = (c: Ctx, pts: P[], color: string, seed: number, alpha: number) => { const r = rng(seed), b = bbox(pts); c.save(); path(c, pts); c.clip(); c.strokeStyle = color; c.globalAlpha = alpha; c.lineWidth = 1; for (let i = 0; i < (b.x1 - b.x0) * (b.y1 - b.y0) / 900; i++) { const x = b.x0 + r() * (b.x1 - b.x0), y = b.y0 + r() * (b.y1 - b.y0), a = r() * 6.28, l = 3 + r() * 9; c.beginPath(); c.moveTo(x, y); c.quadraticCurveTo(x + Math.cos(a + 1) * l * 0.5, y + Math.sin(a + 1) * l * 0.5, x + Math.cos(a) * l, y + Math.sin(a) * l); c.stroke(); } c.restore(); };
export type CardSpec = { cx: number; cy: number; w: number; h: number; rot: number; color: string; seed: number; from?: P; torn?: number };
/** a torn card laid down on the page at p (0 → 1): it slides in, lifted, and settles with its shadow */
export const card = (c: Ctx, cd: CardSpec, p: number) => {
  if (p <= 0) return; const e = easeOut(p), fr = cd.from ?? [0, 120], dx = fr[0] * (1 - e), dy = fr[1] * (1 - e), lift = 1 + 6 * (1 - e) ** 2;
  const sh = xf(tear(rect(cd.w, cd.h), cd.torn ?? 3, cd.seed), cd.cx + dx, cd.cy + dy, cd.rot + 0.1 * (1 - e));
  dropShadow(c, sh, [4 * lift, 7 * lift], 6 + 5 * lift, 0.36 / Math.sqrt(lift));
  c.fillStyle = cd.color; path(c, sh); c.fill(); fibresFill(c, sh, shade(cd.color, -0.25), cd.seed + 3, 0.18);
  c.strokeStyle = shade(cd.color, -0.35); c.globalAlpha = 0.4; c.lineWidth = 1.6; path(c, sh); c.stroke(); c.globalAlpha = 1;
};
/** the card's local frame, so things drawn on it ride with it */
export const onCard = (c: Ctx, cd: CardSpec, p: number, draw: () => void) => {
  if (p <= 0) return; const e = easeOut(p), fr = cd.from ?? [0, 120]; c.save(); c.translate(cd.cx + fr[0] * (1 - e), cd.cy + fr[1] * (1 - e)); c.rotate(cd.rot + 0.1 * (1 - e)); draw(); c.restore();
};
/** yellowed cellulose tape, laid from one end */
export const tape = (c: Ctx, x: number, y: number, ang: number, len: number, p: number, seed: number) => {
  if (p <= 0) return; const L = len * easeOut(p), h = 44, r = rng(seed); c.save(); c.translate(x, y); c.rotate(ang);
  const pts: P[] = [[-len / 2, -h / 2], [-len / 2 + L, -h / 2], [-len / 2 + L + 3, -h / 4], [-len / 2 + L - 2, 0], [-len / 2 + L + 3, h / 4], [-len / 2 + L, h / 2], [-len / 2, h / 2], [-len / 2 - 3, h / 4], [-len / 2 + 2, 0], [-len / 2 - 3, -h / 4]];
  c.globalAlpha = 0.5; c.fillStyle = "#efe0a8"; path(c, pts); c.fill(); c.globalAlpha = 0.3; c.fillStyle = "#fffbe8"; c.fillRect(-len / 2 + 4, -h / 2 + 4, L - 8, 6);
  c.globalAlpha = 0.18; c.strokeStyle = "#8a6a2a"; c.lineWidth = 1; for (let k = 0; k < 3; k++) { const xx = -len / 2 + 12 + r() * (L - 20); c.beginPath(); c.moveTo(xx, -h / 2 + 3); c.lineTo(xx + (r() - 0.5) * 12, h / 2 - 3); c.stroke(); }
  c.restore();
};
/** a toy-theatre cut-out: gouache shape with a white sticker margin, a card edge, a gap and a shadow */
export const cutout = (c: Ctx, pts: P[], fill: string, seed: number, gap = 6, p = 1, shadowA = 0.55) => {
  if (p <= 0) return; c.save(); c.lineJoin = "round";
  c.shadowColor = "rgba(10,6,2,0.85)"; c.shadowBlur = 10 + gap * 2; c.shadowOffsetX = gap; c.shadowOffsetY = gap * 1.6; c.globalAlpha = shadowA; c.strokeStyle = "#000"; c.lineWidth = 16; path(c, pts); c.stroke(); c.fillStyle = "#000"; c.fill(); c.restore();
  c.save(); c.lineJoin = "round"; c.strokeStyle = "#fbf7ee"; c.lineWidth = 16; path(c, pts); c.stroke(); c.fillStyle = fill; path(c, pts); c.fill();
  // gouache: a soft light on the upper-left, brush streaks
  const b = bbox(pts), g = c.createLinearGradient(b.x0, b.y0, b.x1, b.y1); g.addColorStop(0, "rgba(255,255,255,0.18)"); g.addColorStop(0.6, "rgba(255,255,255,0)"); g.addColorStop(1, "rgba(0,0,0,0.16)"); c.fillStyle = g; c.fill();
  path(c, pts); c.clip(); markerStreaks(c, pts, shade(fill, -0.12), 18, 0.25, seed);
  c.restore();
  c.save(); c.strokeStyle = "rgba(80,60,40,0.5)"; c.lineWidth = 1.4; c.lineJoin = "round"; path(c, xf(pts, 0, 0)); c.restore();
};

// ---------------------------------------------------------------- MARKER COMIC
export const shade = (hx: string, t: number) => {
  const m = hx.replace("#", ""), v = [0, 2, 4].map((i) => parseInt(m.slice(i, i + 2), 16)), o = v.map((x) => Math.round(t >= 0 ? x + (255 - x) * t : x * (1 + t)));
  return `rgb(${o[0]},${o[1]},${o[2]})`;
};
/** marker streaks: parallel strokes laid at an angle inside the current clip, the overlaps darker */
export const markerStreaks = (c: Ctx, pts: P[], color: string, width: number, alpha: number, seed: number, ang = -0.5) => {
  const b = bbox(pts), r = rng(seed), cx = (b.x0 + b.x1) / 2, cy = (b.y0 + b.y1) / 2, R = Math.hypot(b.x1 - b.x0, b.y1 - b.y0) / 2 + width;
  c.save(); c.strokeStyle = color; c.lineCap = "round"; c.globalAlpha = alpha; const ca = Math.cos(ang), sa = Math.sin(ang);
  for (let v = -R; v <= R; v += width * 0.8) { c.lineWidth = width * (0.8 + r() * 0.35); c.beginPath(); const u0 = -R + r() * 20, u1 = R - r() * 20; c.moveTo(cx + u0 * ca - v * sa, cy + u0 * sa + v * ca); c.lineTo(cx + u1 * ca - v * sa, cy + u1 * sa + v * ca); c.stroke(); }
  c.restore();
};
export type MarkerO = { shadow?: string; contour?: number; seed?: number; light?: P; hi?: boolean; streak?: boolean; ink?: string };
/** one marker-comic shape: cel fill, a hard shadow edge away from the light, streaky marker, a heavy contour */
export const marker = (c: Ctx, pts: P[], fill: string, o: MarkerO = {}) => {
  const seed = o.seed ?? 1, [lx, ly] = o.light ?? [-1, -1], b = bbox(pts), size = Math.max(b.x1 - b.x0, b.y1 - b.y0), off = Math.max(8, size * 0.09), cw = o.contour ?? Math.max(4, Math.min(10, size * 0.022));
  c.save(); path(c, pts); c.fillStyle = o.shadow ?? shade(fill, -0.3); c.fill();
  c.save(); path(c, pts); c.clip();
  path(c, xf(pts, lx * off, ly * off)); c.fillStyle = fill; c.fill();
  if (o.streak !== false) markerStreaks(c, pts, shade(fill, -0.08), Math.max(10, size * 0.05), 0.35, seed);
  if (o.hi !== false) { c.globalAlpha = 0.55; c.fillStyle = "#ffffff"; const hx = b.x0 + (b.x1 - b.x0) * 0.22, hy = b.y0 + (b.y1 - b.y0) * 0.2; c.beginPath(); c.ellipse(hx, hy, size * 0.06, size * 0.025, -0.6, 0, 6.283); c.fill(); }
  c.restore();
  // contour: thin on the lit side, heavy on the shadow side (a second pass offset away from the light)
  c.strokeStyle = o.ink ?? INK; c.lineJoin = "round"; c.lineCap = "round"; c.lineWidth = cw; path(c, pts); c.stroke();
  c.save(); c.translate(-lx * cw * 0.45, -ly * cw * 0.45); c.lineWidth = cw * 0.9; path(c, pts); c.stroke(); c.restore();
  c.restore();
};
/** a marker line (brush pen): a tapered stroke along pts */
export const brushLine = (c: Ctx, pts: P[], w: number, color: string, p = 1) => {
  if (p <= 0) return; const n = Math.max(2, Math.floor(pts.length * clamp01(p))); c.save(); c.strokeStyle = color; c.lineCap = "round"; c.lineJoin = "round";
  for (let i = 1; i < n; i++) { const t = i / (pts.length - 1), k = Math.sin(Math.PI * Math.min(1, t * 1.1)) * 0.75 + 0.25; c.lineWidth = w * k; c.beginPath(); c.moveTo(pts[i - 1][0], pts[i - 1][1]); c.lineTo(pts[i][0], pts[i][1]); c.stroke(); }
  c.restore();
};

// ---------------------------------------------------------------- RED PEN + STAMP + RANSOM
/** red pen ellipse drawn on, slightly overshooting its start (hand-drawn) */
export const penLoop = (c: Ctx, cx: number, cy: number, rx: number, ry: number, p: number, seed: number, color = RED, w = 9) => {
  if (p <= 0) return; const r = rng(seed), pts: P[] = [], n = 60, turns = 1.12;
  for (let k = 0; k <= n; k++) { const t = k / n, a = -2.2 + t * Math.PI * 2 * turns, j = 1 + (r() - 0.5) * 0.03 + t * 0.06; pts.push([cx + Math.cos(a) * rx * j, cy + Math.sin(a) * ry * j]); }
  c.save(); c.shadowColor = "rgba(194,58,42,0.35)"; c.shadowBlur = 6; brushLine(c, pts, w, color, easeOut(p)); c.restore();
};
export const penStrike = (c: Ctx, x0: number, y0: number, x1: number, y1: number, p: number, color = RED, w = 10) => { if (p <= 0) return; const e = easeOut(p); brushLine(c, [[x0, y0], [x0 + (x1 - x0) * 0.5 * e, y0 + (y1 - y0) * 0.5 * e - 4], [x0 + (x1 - x0) * e, y0 + (y1 - y0) * e]], w, color, 1); };
export const penArrow = (c: Ctx, a: P, b: P, p: number, color = RED, w = 9) => {
  if (p <= 0) return; const e = easeOut(p), mx = (a[0] + b[0]) / 2 + (b[1] - a[1]) * 0.18, my = (a[1] + b[1]) / 2 - (b[0] - a[0]) * 0.18, pts: P[] = [];
  for (let k = 0; k <= 20; k++) { const t = (k / 20) * e; pts.push([(1 - t) ** 2 * a[0] + 2 * (1 - t) * t * mx + t * t * b[0], (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * my + t * t * b[1]]); }
  brushLine(c, pts, w, color, 1);
  if (e >= 0.98) { const [px, py] = pts[pts.length - 2], [qx, qy] = pts[pts.length - 1], ang = Math.atan2(qy - py, qx - px); brushLine(c, [[qx - Math.cos(ang - 0.5) * 40, qy - Math.sin(ang - 0.5) * 40], [qx, qy]], w, color); brushLine(c, [[qx - Math.cos(ang + 0.5) * 40, qy - Math.sin(ang + 0.5) * 40], [qx, qy]], w, color); }
};
/** a rubber stamp, rocked on from one end: double border, text in the one face, ink starved in spots */
export const stamp = (c: Ctx, text: string, x: number, y: number, size: number, rot: number, p: number, color = STAMP, seed = 5) => {
  if (p <= 0) return; const w = textW(c, text, size) + size * 0.9, h = size * 1.55, reach = -w / 2 - 10 + (w + 20) * easeOut(clamp01(p * 1.4)), k = 1 + 0.25 * (1 - easeOut(clamp01(p * 3)));
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k); c.beginPath(); c.rect(-w / 2 - 14, -h / 2 - 14, reach + w / 2 + 14, h + 28); c.clip();
  c.globalAlpha = 0.9; c.strokeStyle = color; c.lineWidth = size * 0.09; c.strokeRect(-w / 2, -h / 2, w, h); c.lineWidth = size * 0.035; c.strokeRect(-w / 2 + size * 0.14, -h / 2 + size * 0.14, w - size * 0.28, h - size * 0.28);
  c.font = `900 ${size}px ${FONT}`; c.textAlign = "center"; c.textBaseline = "middle"; c.fillStyle = color; c.fillText(text, 0, size * 0.04);
  // starved ink: knock out specks with the paper colour
  const r = rng(seed); c.globalCompositeOperation = "destination-out"; c.globalAlpha = 0.6; for (let i = 0; i < w * h / 160; i++) { c.beginPath(); c.arc(-w / 2 + r() * w, -h / 2 + r() * h, 0.8 + r() * 2.4, 0, 6.283); c.fill(); }
  c.restore();
};
/** ransom-note tiles: each character cut from a different printed page, pasted with a little lift */
const TILE_PAIRS: [string, string][] = [[NAVY, "#f3ead6"], [TEAL, "#1c1a18"], ["#f1e9d8", "#1c1a18"], [PINK, NAVY], [STAMP, "#f6ecd9"], [MUSTARD, "#1c1a18"], ["#d8d2c4", "#1c1a18"], ["#1d1b19", "#efe6d0"], ["#e9c9b4", STAMP]];
export const ransom = (c: Ctx, word: string, cx: number, cy: number, cap: number, seed: number, p: number, stepF = 0.08) => {
  const r = rng(seed), chars = [...word], ws: number[] = chars.map((ch) => (ch === " " ? cap * 0.35 : textW(c, ch, cap) + cap * 0.42)), tot = ws.reduce((a, b) => a + b + 6, -6); let x = cx - tot / 2, last = -1;
  chars.forEach((ch, i) => {
    const w = ws[i], q = clamp01((p - i * stepF) / 0.25); let pi = Math.floor(r() * TILE_PAIRS.length); if (pi === last) pi = (pi + 3) % TILE_PAIRS.length; last = pi; const jy = (r() - 0.5) * cap * 0.2, rot = (r() - 0.5) * 0.22, sc = 0.88 + r() * 0.24, news = r() < 0.4;
    if (ch !== " " && q > 0) {
      const e = easeOut(q), lift = 1 + 4 * (1 - e) ** 2, tx = x + w / 2 - 6 * (1 - e), ty = cy + jy - 16 * (1 - e), rr = rot + 0.3 * (1 - e) * (i % 2 ? 1 : -1), [bg, fg] = TILE_PAIRS[pi];
      const sh = xf(tear(rect(w, cap * 1.45 * sc), 1.6, seed * 31 + i), tx, ty, rr);
      dropShadow(c, sh, [2 * lift, 4 * lift], 2 + 2 * lift, 0.42 / Math.sqrt(lift)); c.fillStyle = bg; path(c, sh); c.fill();
      if (news) { c.save(); path(c, sh); c.clip(); c.globalAlpha = 0.22; c.fillStyle = fg; for (let yy = ty - cap; yy < ty + cap; yy += 7) c.fillRect(tx - w, yy, w * 2, 2); c.restore(); }
      txt(c, ch, tx, ty + cap * 0.04, cap * sc, fg, { rot: rr });
    }
    x += w + 6;
  });
};
/** a paper sticker label (scrapbook tag / price sticker) */
export const label = (c: Ctx, s: string, x: number, y: number, size: number, p: number, fg = INK, bg = CREAM, rot = 0, seed = 3) => {
  if (p <= 0) return; const k = back(p), w = textW(c, s, size) + size * 0.8, h = size * 1.45;
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k); const sh = tear(rect(w, h), 1.4, seed);
  dropShadow(c, sh, [3, 6], 6, 0.4); c.fillStyle = bg; path(c, sh); c.fill(); fibresFill(c, sh, shade(bg.startsWith("#") ? bg : "#f6efe0", -0.3), seed, 0.15);
  c.restore(); txt(c, s, x, y + size * 0.03, size, fg, { sc: k, rot });
};
/** a hero number: Inter 900, big, ink-stroked, slammed in on its word with a short shake */
export const hero = (c: Ctx, s: string, x: number, y: number, f: number, t: number, color = KEY, size = 170, rot = 0) => {
  if (f < t) return; const p = span(f, t, t + 6), sc = 1.6 - 0.6 * easeOut(p), sh = f < t + 8 ? (rng(f * 7 + 3)() - 0.5) * 16 * (1 - span(f, t + 4, t + 8)) : 0;
  txt(c, s, x + sh, y, size, color, { stroke: size * 0.11, sc, alpha: clamp01(p * 3), rot });
};

// ---------------------------------------------------------------- MARKER-COMIC PROPS
/** a price tag (marker comic): rounded card, punched hole, string loop; text drawn by the caller */
export const priceTagShape = (w: number, h: number): P[] => { const pts: P[] = [[-w / 2 + h * 0.35, -h / 2], [w / 2, -h / 2], [w / 2, h / 2], [-w / 2 + h * 0.35, h / 2], [-w / 2, 0]]; return resampleRing(pts, 8); };
export const priceTag = (c: Ctx, x: number, y: number, w: number, h: number, rot: number, text: string, p: number, seed = 9, fill = "#f3e9cf") => {
  if (p <= 0) return; const k = back(p); c.save(); c.translate(x, y); c.rotate(rot + 0.3 * (1 - easeOut(p))); c.scale(k, k);
  brushLine(c, [[-w / 2 + h * 0.18, 0], [-w / 2 - 40, -h * 0.5], [-w / 2 - 70, -h * 0.9]], 5, INK);
  marker(c, priceTagShape(w, h), fill, { seed, shadow: "#d1c19c" });
  c.fillStyle = INK; c.beginPath(); c.arc(-w / 2 + h * 0.18, 0, h * 0.07, 0, 6.283); c.fill();
  c.restore(); txt(c, text, x + Math.cos(rot) * w * 0.08, y + Math.sin(rot) * w * 0.08, h * 0.5, INK, { sc: k, rot });
};
/** a chocolate bar in a wrapper (marker comic), cols x rows squares; `gone` columns torn off on the right */
export const chocBar = (c: Ctx, x: number, y: number, cell: number, cols: number, rows: number, rot: number, gone: number, seed = 13, wrap = "#6a4c9c") => {
  c.save(); c.translate(x, y); c.rotate(rot); const bw = cols * cell, bh = rows * cell;
  // the wrapper sleeve stays full size (same wrapper): the foil end peeks out
  marker(c, rrect(bw + cell * 0.9, bh + cell * 0.7, 18), wrap, { seed: seed + 1, contour: 7 });
  c.fillStyle = "rgba(255,255,255,0.22)"; c.fillRect(-bw / 2 - cell * 0.45, -bh * 0.05, bw + cell * 0.9, bh * 0.1);
  for (let i = 0; i < cols; i++) for (let j = 0; j < rows; j++) {
    const g = clamp01(gone - (cols - 1 - i)); if (g >= 1) continue;
    const cx = -bw / 2 + cell * (i + 0.5) + g * 60, cy = -bh / 2 + cell * (j + 0.5) - g * 220 + g * g * 90, rr = g * (i % 2 ? 0.9 : -0.7);
    marker(c, xf(rrect(cell * 0.86, cell * 0.86, cell * 0.14), cx, cy, rr), "#7a4424", { seed: seed + i * 7 + j, contour: 4, shadow: "#55301a", streak: false });
    c.globalAlpha = 0.5 * (1 - g); c.strokeStyle = "#a8683e"; c.lineWidth = 3; path(c, xf(rrect(cell * 0.56, cell * 0.56, cell * 0.1), cx, cy, rr)); c.stroke(); c.globalAlpha = 1;
  }
  c.restore();
};
/** a cartoon brain: two lobes and folds (marker comic) */
export const brain = (c: Ctx, x: number, y: number, s: number, p: number, seed = 31) => {
  if (p <= 0) return; const k = back(p); c.save(); c.translate(x, y); c.scale(k * s, k * s);
  const pts: P[] = []; for (let i = 0; i < 36; i++) { const a = (i / 36) * Math.PI * 2, bump = 1 + 0.07 * Math.sin(a * 9); pts.push([Math.cos(a) * 150 * bump, Math.sin(a) * 108 * bump * (a > 0 && a < Math.PI ? 0.92 : 1)]); }
  marker(c, pts, "#f0a3b4", { seed, contour: 8, shadow: "#c97a8c" });
  const folds: P[][] = [[[0, -100], [-14, -40], [10, 20], [-8, 96]], [[-120, -20], [-80, -54], [-46, -14], [-90, 30]], [[46, -64], [96, -30], [66, 10], [116, 40]], [[-104, 54], [-54, 74], [-24, 44]], [[30, 60], [84, 82]]];
  folds.forEach((f) => brushLine(c, f, 7, "#8a3f52"));
  c.restore();
};
/** a cartoon eye (marker comic), pupil looking toward (lx, ly) */
export const eye = (c: Ctx, x: number, y: number, s: number, look: P, p: number, blink = 0, seed = 51) => {
  if (p <= 0) return; const k = back(p); c.save(); c.translate(x, y); c.scale(k * s, k * s);
  const open = 1 - blink, shape: P[] = []; for (let i = 0; i < 40; i++) { const a = (i / 40) * Math.PI * 2; shape.push([Math.cos(a) * 200, Math.sin(a) * 120 * Math.max(0.05, open) * (Math.abs(Math.cos(a)) ** 0.25)]); }
  marker(c, shape, "#fbf6ea", { seed, contour: 10, shadow: "#d8cdb6" });
  c.save(); path(c, shape); c.clip(); const [lx, ly] = look; marker(c, ellipse(lx * 50, ly * 30, 82, 82), "#3f7fa0", { seed: seed + 1, contour: 6 }); c.fillStyle = INK; c.beginPath(); c.arc(lx * 56, ly * 34, 38, 0, 6.283); c.fill(); c.fillStyle = "#fff"; c.beginPath(); c.arc(lx * 56 - 18, ly * 34 - 18, 13, 0, 6.283); c.fill(); c.restore();
  // lashes
  for (let i = 0; i < 5; i++) { const a = -Math.PI * 0.85 + i * (Math.PI * 0.7 / 4); brushLine(c, [[Math.cos(a) * 200, Math.sin(a) * 122 * open], [Math.cos(a) * 250, Math.sin(a) * 175 * open - 10]], 9, INK); }
  c.restore();
};
/** a judge's gavel (marker comic), swung by angle `a` (radians), on a sound block */
export const gavel = (c: Ctx, x: number, y: number, s: number, a: number, seed = 61) => {
  c.save(); c.translate(x, y); c.scale(s, s);
  marker(c, rrect(260, 60, 14, 0, 130), "#7a4a26", { seed, contour: 7, shadow: "#55331a" });
  c.save(); c.translate(130, 40); c.rotate(-a);
  marker(c, rrect(340, 34, 14, -200, 0), "#b07a45", { seed: seed + 1, contour: 6, shadow: "#87592f" });
  marker(c, rrect(90, 170, 18, -370, 0), "#7a4a26", { seed: seed + 2, contour: 7, shadow: "#55331a" });
  c.fillStyle = "#d7b25c"; c.fillRect(-418, -30, 8, 60); c.fillRect(-330, -30, 8, 60);
  c.restore(); c.restore();
};
/** a triangular-peaks bar (generic, no brand marks): n peaks; peaks where gone(i) > 0 lift away */
export const peaks = (c: Ctx, x: number, y: number, pw: number, ph: number, n: number, gone: (i: number) => number, seed = 71) => {
  c.save(); c.translate(x, y); const tot = n * pw;
  marker(c, rrect(tot + 40, 60, 14, 0, ph / 2 + 10), "#d9b25a", { seed, contour: 7, shadow: "#b38a3a" });
  for (let i = 0; i < n; i++) {
    const g = clamp01(gone(i)), cx = -tot / 2 + pw * (i + 0.5), dy = -g * 320, rr = g * (i % 4 === 1 ? -0.8 : 0.8), a = 1 - g * 0.9; if (a <= 0.05) continue;
    c.globalAlpha = a; marker(c, xf([[-pw / 2 + 6, ph / 2], [0, -ph / 2], [pw / 2 - 6, ph / 2]], cx, dy, rr), "#e2b85e", { seed: seed + i, contour: 6, shadow: "#b38a3a" }); c.globalAlpha = 1;
  }
  c.restore();
};
/** a cereal-style box (marker comic) */
export const box = (c: Ctx, x: number, y: number, w: number, h: number, fill: string, seed = 81, rot = 0) => {
  c.save(); c.translate(x, y); c.rotate(rot); const d = w * 0.22;
  marker(c, [[-w / 2 + d, -h / 2 - d * 0.6], [w / 2 + d, -h / 2 - d * 0.6], [w / 2 + d, h / 2 - d * 0.6], [w / 2, h / 2], [w / 2, -h / 2]], shade(fill, -0.3), { seed: seed + 9, contour: 6, streak: false, hi: false });
  marker(c, rect(w, h), fill, { seed, contour: 7 });
  marker(c, ellipse(0, -h * 0.05, w * 0.3, w * 0.3), "#fff2c4", { seed: seed + 2, contour: 5, streak: false });
  c.restore();
};
/** a shopping cart (marker comic line art) */
export const cart = (c: Ctx, x: number, y: number, s: number, seed = 91) => {
  c.save(); c.translate(x, y); c.scale(s, s);
  marker(c, [[-150, -100], [150, -100], [120, 30], [-120, 30]], "#9bb7c6", { seed, contour: 8 });
  c.strokeStyle = INK; c.lineWidth = 5; for (let i = -3; i <= 3; i++) { c.beginPath(); c.moveTo(i * 38, -100); c.lineTo(i * 32, 30); c.stroke(); }
  brushLine(c, [[-150, -100], [-200, -170], [-250, -175]], 12, INK); brushLine(c, [[-120, 30], [-110, 80], [130, 80]], 10, INK);
  [[-90, 110], [100, 110]].forEach(([cx, cy], i) => marker(c, ellipse(cx, cy, 28, 28), "#3a3a3a", { seed: seed + i, contour: 6, streak: false }));
  c.restore();
};

// ---------------------------------------------------------------- CAPTIONS (word-by-word karaoke, key words red)
export type TWordIn = { t: string; key: boolean; s: number; e: number };
type Chunk = { words: { t: string; key: boolean; s: number }[]; from: number; to: number };
export const makeChunks = (lines: { words: TWordIn[] }[]): Chunk[] => {
  const out: Chunk[] = [];
  lines.forEach((ln) => {
    let cur: Chunk["words"] = []; const flush = () => { if (cur.length) out.push({ words: cur, from: 0, to: 0 }); cur = []; };
    ln.words.forEach((w, i) => { cur.push({ t: w.t.toUpperCase(), key: w.key, s: sec(w.s) }); const left = ln.words.length - 1 - i; if (left < 2) return; if (cur.length >= 4 || (/[.?!:]$/.test(w.t) && cur.length >= 2) || (/,$/.test(w.t) && cur.length >= 3)) flush(); });
    flush();
  });
  out.forEach((ch, i) => { ch.from = ch.words[0].s - 2; ch.to = i + 1 < out.length ? out[i + 1].words[0].s - 2 : 1e9; });
  return out;
};
export const CAP = 74, CAP_Y = 1540;
export const captions = (c: Ctx, f: number, chunks: Chunk[]) => {
  const ch = chunks.find((k) => f >= k.from && f < k.to); if (!ch) return;
  c.save(); c.font = `900 ${CAP}px ${FONT}`; const sp = CAP * 0.28, ws = ch.words.map((w) => c.measureText(w.t).width);
  const lines: number[][] = [[]]; let lw = 0; ws.forEach((w, i) => { if (lw && lw + sp + w > 940) { lines.push([]); lw = 0; } lines[lines.length - 1].push(i); lw += (lw ? sp : 0) + w; });
  lines.forEach((ln, li) => {
    const tot = ln.reduce((a, i, k) => a + ws[i] + (k ? sp : 0), 0); let x = 540 - tot / 2; const y = CAP_Y + (li - (lines.length - 1) / 2) * CAP * 1.2;
    ln.forEach((i) => { const w = ch.words[i], p = span(f, w.s - 1, w.s + 3), live = f >= w.s; if (p > 0) txt(c, w.t, x + ws[i] / 2, y, CAP, w.key && live ? KEY : "#ffffff", { stroke: 15, sc: 0.85 + 0.15 * easeOut(p), alpha: clamp01(p * 2) }); x += ws[i] + sp; });
  });
  c.restore();
};
