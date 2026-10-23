import { Gfx, rng, type Ctx, type Medium, type P } from "./core";
import { G, letter, width as textWidth } from "./drafting";
import { blob, fillShape, hatchRuns, inside } from "./gallery";

// CHALK KIT, portrait. The moonPhases chalkboard hand (side-of-chalk scumble, every stroke broken by
// the board's tooth and shedding dust, felt-eraser ghosts) rebuilt for a 1080 x 1920 Short.
// Everything here is a pure function of its arguments and a progress value 0..1: a mark is written
// stroke by stroke, never faded in.

export const W = 1080, H = 1920;
export const CHALK_M: Medium = { nib: 2.1, taper: 0.55, pressure: 0.95, retrace: true, wobble: 1.4, rough: 1.2 };
export const CHALK = "#f4f0e6", YEL = "#f6e6a4", BLUE = "#a9d3e8", PINK = "#f3c1cf", RED = "#ff8b7b", BROWN = "#b98a63", DKBROWN = "#8a5e3c";
export const B0 = 26, B1 = W - 26, TOP = 26, LEDGE = 1862;

// the rupee sign, drawn the way a hand writes it: two bars, the bowl, the diagonal leg
G["₹"] = { l: [[[0.2, 0], [3.8, 0]], [[0.2, 1.6], [3.8, 1.6]], [[0.9, 3.3], [3.7, 6]]], c: [[[0.6, 0], [2.3, 0], [3.1, 0.8], [3.1, 2.4], [2.2, 3.3], [0.4, 3.3]]], w: 4 };

export const clamp01 = (v: number) => Math.max(0, Math.min(1, v));
/** progress of a mark that is written between frames a and b */
export const span = (f: number, a: number, b: number) => (b <= a ? (f >= a ? 1 : 0) : clamp01((f - a) / (b - a)));

export const chalk = (g: Gfx, draw: (dust: boolean) => void, dustAlpha = 0.2) => {
  g.group("plain", () => draw(true), { blur: 3.2, alpha: dustAlpha });
  g.group("plain", () => draw(false), { textures: ["pencilTooth", "risoSpeck"] });
};
export const line = (g: Gfx, dust: boolean, pts: P[], w: number, color: string, seed: number, op = 0.92, wob = 1, progress = 1) => {
  if (progress <= 0) return;
  g.pen(pts, { w: dust ? w * 2.6 : w, color, seed, wobble: wob, boil: 0, opacity: op, retrace: !dust, taper: 1, progress });
};
export const scumble = (g: Gfx, dust: boolean, region: P[], color: string, o: { angle: number; gap: number; w: number; alpha: number; seed: number; keep?: (x: number, y: number) => boolean; progress?: number }) => {
  const { angle, gap, w, alpha, seed, keep = () => true, progress = 1 } = o, r = rng(seed);
  if (progress <= 0) return;
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; region.forEach(([x, y]) => { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); });
  const c = g.cur; g.touch(x0 - 12, y0 - 12, x1 + 12, y1 + 12);
  c.save(); c.lineCap = "round"; c.lineJoin = "round"; c.strokeStyle = color; c.lineWidth = dust ? w * 2.2 : w;
  const runs = hatchRuns({ x0, y0, x1, y1 }, angle, gap, (x, y) => inside(region, x, y) && keep(x, y), 4, seed);
  const upto = progress * runs.length;
  runs.forEach((run, i) => {
    if (i > upto) return;
    const pts = run.filter((_, k, a) => k % 2 === 0 || k === a.length - 1), m = i + 1 > upto ? Math.max(2, Math.ceil(pts.length * (upto - i))) : pts.length;
    c.globalAlpha = alpha * (0.86 + r() * 0.2); c.beginPath();
    pts.slice(0, m).forEach(([x, y], k) => (k ? c.lineTo(x + (r() - 0.5) * 1.5, y + (r() - 0.5) * 1.5) : c.moveTo(x, y)));
    c.stroke();
  });
  c.restore();
};
/** chalk lettering; `progress` writes it stroke by stroke */
export const write = (g: Gfx, text: string, x: number, y: number, cap: number, color: string, seed: number, progress = 1, align: "left" | "center" | "right" = "center", op = 0.95) =>
  letter(g, text, x, y, { cap, color, seed, align, w: Math.max(1.6, cap * 0.07), opacity: op, progress, slant: 0.08 });
export const textW = (text: string, cap: number) => textWidth(text, cap, 1.25);

export const rect = (x0: number, y0: number, x1: number, y1: number): P[] => [[x0, y0], [x1, y0], [x1, y1], [x0, y1]];
export const loop = (cx: number, cy: number, rx: number, ry: number, a0 = -0.4, turns = 1.08, n = 14): P[] => Array.from({ length: n + 1 }, (_, k) => { const a = a0 + (k / n) * Math.PI * 2 * turns; return [cx + Math.cos(a) * rx, cy + Math.sin(a) * ry] as P; });
/** an arrow written in two strokes: the shaft, then the head */
export const arrow = (g: Gfx, dust: boolean, a: P, b: P, color: string, seed: number, p: number, w = 3) => {
  line(g, dust, [a, [(a[0] + b[0]) / 2 + (b[1] - a[1]) * 0.06, (a[1] + b[1]) / 2 - (b[0] - a[0]) * 0.06], b], w, color, seed, 0.92, 1, clamp01(p * 1.4));
  const ang = Math.atan2(b[1] - a[1], b[0] - a[0]), hl = 30;
  line(g, dust, [[b[0] - Math.cos(ang - 0.5) * hl, b[1] - Math.sin(ang - 0.5) * hl], b, [b[0] - Math.cos(ang + 0.5) * hl, b[1] - Math.sin(ang + 0.5) * hl]], w, color, seed + 1, 0.92, 0.3, clamp01(p * 1.4 - 0.4) / 0.6);
};
/** a strike-through, scrubbed twice */
export const strike = (g: Gfx, dust: boolean, x0: number, y: number, x1: number, color: string, seed: number, p: number) => {
  line(g, dust, [[x0, y + 6], [(x0 + x1) / 2, y - 2], [x1, y - 8]], 4, color, seed, 0.95, 1, clamp01(p * 2));
  line(g, dust, [[x0 + 6, y + 18], [(x0 + x1) / 2, y + 10], [x1 - 4, y + 2]], 3, color, seed + 1, 0.85, 1, clamp01(p * 2 - 1));
};

// ---------------------------------------------------------------- the board
/** the slate, its ghosts, and (optionally) the felt eraser sweeping a region clean */
export const board = (g: Gfx, ctx: Ctx, seed: number) => {
  const gr = ctx.createRadialGradient(540, 820, 80, 540, 900, 1250);
  gr.addColorStop(0, "#36493f"); gr.addColorStop(0.6, "#27352f"); gr.addColorStop(1, "#19231f");
  ctx.fillStyle = gr; ctx.fillRect(0, 0, W, H);
  g.paper("coldpress", 0.3);
  g.group("plain", () => {
    const r = rng(seed);
    for (let i = 0; i < 12; i++) {
      const cx = 120 + r() * 840, cy = 140 + r() * 1600, rr = 140 + r() * 200, a0 = r() * 6; const pts: P[] = [];
      for (let k = 0; k <= 12; k++) { const a = a0 + (k / 12) * 2.2; pts.push([cx + Math.cos(a) * rr, cy + Math.sin(a) * rr * 0.55]); }
      g.pen(pts, { w: 44 + r() * 30, color: CHALK, seed: seed + 6 + i, wobble: 3, boil: 0, opacity: 0.05, retrace: false, taper: 0.4 });
    }
  }, { blur: 9 });
};
/** the eraser passing left to right at x (0..1 progress): everything right of it is still yesterday's board */
export const eraserWipe = (g: Gfx, p: number, y0: number, y1: number, drawOld: () => void) => {
  if (p >= 1) return;
  const wx = B0 + p * (B1 - B0), c = g.cur;
  c.save(); c.beginPath(); c.rect(wx, y0, W - wx, y1 - y0); c.clip(); drawOld(); c.restore();
  // the felt block itself, mid-sweep
  if (p > 0) {
    const ey = (y0 + y1) / 2 + Math.sin(p * 12) * 40;
    g.group("plain", () => { fillShape(g, [[wx - 70, ey - 110], [wx + 20, ey - 104], [wx + 26, ey + 110], [wx - 64, ey + 116]], "#2a1a0e", 0.45); fillShape(g, [[wx - 78, ey - 118], [wx + 12, ey - 112], [wx + 18, ey + 102], [wx - 72, ey + 108]], "#a0714a"); fillShape(g, [[wx - 30, ey - 114], [wx + 12, ey - 112], [wx + 18, ey + 102], [wx - 24, ey + 104]], "#8e8a86"); });
  }
};
export const frame = (g: Gfx) => {
  g.group("plain", () => {
    const wood = "#7b5231", dark = "#553620", r = rng(70);
    fillShape(g, rect(0, 0, W, TOP), wood); fillShape(g, rect(0, 0, B0, H), wood); fillShape(g, rect(B1, 0, W, H), wood);
    fillShape(g, rect(0, LEDGE, W, H), "#6a4526");
    fillShape(g, [[B0 - 8, LEDGE - 4], [B1 + 8, LEDGE - 4], [B1 + 18, LEDGE + 22], [B0 - 18, LEDGE + 22]], "#8c6139");
    for (let i = 0; i < 40; i++) { const y = r() * H, x = r() < 0.5 ? r() * B0 : B1 + r() * B0; g.pen([[x, y], [x + (r() - 0.5) * 3, y + 50 + r() * 70]], { w: 0.9, color: dark, seed: 71 + i, wobble: 0.6, boil: 0, opacity: 0.45, retrace: false }); }
    fillShape(g, [[B0, TOP], [B1, TOP], [B1 - 6, TOP + 8], [B0 + 8, TOP + 8], [B0 + 8, LEDGE - 4], [B0, LEDGE - 4]], "#0e1512", 0.55);
    for (let i = 0; i < 160; i++) { const x = B0 + r() * (B1 - B0), y = LEDGE + 2 + r() * 18; fillShape(g, blob(x, y, 0.8 + r() * 1.8, 0.6 + r(), 110 + i, 0.3, 6), CHALK, 0.25 + r() * 0.45); }
    fillShape(g, [[700, LEDGE + 2], [800, LEDGE - 6], [804, LEDGE + 10], [704, LEDGE + 18]], CHALK);
    fillShape(g, [[700, LEDGE + 11], [804, LEDGE + 3], [804, LEDGE + 10], [704, LEDGE + 18]], "#d9d3c6");
  });
};

// ---------------------------------------------------------------- props
/** a chocolate bar in brown chalk: the slab scumbled in, then the segment grooves, then the rim.
 *  `gone` columns at the right end are missing: an eraser smudge and a dashed ghost where they were. */
export const chocBar = (g: Gfx, cx: number, cy: number, w: number, h: number, cols: number, rows: number, seed: number, p: { slab: number; grid: number; rim: number; gone?: number; ghost?: number }) => {
  const x0 = cx - w / 2, y0 = cy - h / 2, cw = w / cols, gone = p.gone ?? 0, xe = x0 + w - gone * cw;
  if (gone > 0 && (p.ghost ?? 0) > 0) g.group("plain", () => scumble(g, false, rect(xe, y0, x0 + w, y0 + h), CHALK, { angle: 0.3, gap: 7, w: 12, alpha: 0.14, seed: seed + 50 }), { blur: 5 });   // where the eraser took it
  chalk(g, (dust) => {
    scumble(g, dust, rect(x0, y0, xe, y0 + h), BROWN, { angle: -0.8, gap: 3.6, w: 4.4, alpha: 0.4, seed: seed + 1, progress: p.slab });
    scumble(g, dust, rect(x0, y0, xe, y0 + h), DKBROWN, { angle: 0.7, gap: 4.4, w: 4, alpha: 0.4, seed: seed + 2, progress: p.slab, keep: (x, y) => ((x - x0) % cw) > cw * 0.62 || ((y - y0) % (h / rows)) > (h / rows) * 0.62 });   // the shaded side of each square
    const gp = p.grid, nl = cols - 1 - gone + rows - 1; let k = 0;
    for (let i = 1; i < cols - gone; i++) { const x = x0 + i * cw; line(g, dust, [[x, y0 + 6], [x + 1, y0 + h - 6]], 2, "#4c3020", seed + 10 + i, 0.85, 0.6, clamp01(gp * nl - k++)); }
    for (let j = 1; j < rows; j++) { const y = y0 + (j * h) / rows; line(g, dust, [[x0 + 6, y], [xe - 6, y + 1]], 2, "#4c3020", seed + 30 + j, 0.85, 0.6, clamp01(gp * nl - k++)); }
    const sides: [P, P][] = [[[x0, y0], [xe, y0]], [[xe, y0], [xe, y0 + h]], [[xe, y0 + h], [x0, y0 + h]], [[x0, y0 + h], [x0, y0]]];
    sides.forEach((sd, i) => line(g, dust, sd, 3, CHALK, seed + 40 + i, 0.9, 0.8, clamp01(p.rim * 4 - i)));   // four strokes, so the corners stay corners
    if (gone > 0 && (p.ghost ?? 0) > 0) {   // the missing squares, outlined in dashes
      const q = p.ghost!, segs: [P, P][] = [];
      for (let x = xe + 10; x < x0 + w; x += 34) { segs.push([[x, y0], [Math.min(x + 18, x0 + w), y0]]); segs.push([[x, y0 + h], [Math.min(x + 18, x0 + w), y0 + h]]); }
      for (let y = y0 + 10; y < y0 + h; y += 34) segs.push([[x0 + w, y], [x0 + w, Math.min(y + 18, y0 + h)]]);
      segs.forEach((s, i) => line(g, dust, s, 2.6, CHALK, seed + 60 + i, 0.8, 0.4, clamp01(q * segs.length - i)));
    }
  });
};
/** a shop's price tag on a string: the tag outline, the hole, the string, then the price */
export const priceTag = (g: Gfx, x: number, y: number, text: string, seed: number, p: number, color = CHALK, ang = -0.12) => {
  const c = Math.cos(ang), s = Math.sin(ang), T = ([px, py]: P): P => [x + px * c - py * s, y + px * s + py * c];
  const body: P[] = [[0, 0], [70, -70], [330, -70], [330, 70], [70, 70], [0, 0]].map((q) => T(q as P));
  chalk(g, (dust) => {
    line(g, dust, body, 3, color, seed, 0.92, 1, clamp01(p * 3));
    line(g, dust, Array.from({ length: 11 }, (_, k) => T([60 + Math.cos(k / 10 * 6.4) * 13, Math.sin(k / 10 * 6.4) * 13])), 2, color, seed + 1, 0.85, 0.4, clamp01(p * 3 - 1));
    line(g, dust, [T([47, 0]), T([-30, -40]), T([-90, -30])], 2, color, seed + 2, 0.7, 1.2, clamp01(p * 3 - 1));
    write(g, text, T([205, 0])[0], T([205, -32])[1], 56, color, seed + 3, clamp01(p * 3 - 2));
  });
};

// ---------------------------------------------------------------- captions
/** word-by-word captions written in chalk on the lower board; key words in red chalk.
 *  words: [text, isKey, startFrame]. Each word is written over its first 6 frames. */
export const CAP_Y = 1500, CAP_CAP = 66;
export const captions = (g: Gfx, f: number, words: [string, boolean, number][], seed: number) => {
  if (!words.length) return;
  // lay out in up to 2 lines of <= 940 px
  const space = CAP_CAP * 0.65, lines: [string, boolean, number, number][][] = [[]]; let lw = 0;
  for (const [t, k, s] of words) { const w = textW(t, CAP_CAP); if (lw > 0 && lw + space + w > 940) { lines.push([]); lw = 0; } lines[lines.length - 1].push([t, k, s, w]); lw += (lw ? space : 0) + w; }
  chalk(g, (dust) => {
    lines.forEach((ln, li) => {
      const tot = ln.reduce((a, q, i) => a + q[3] + (i ? space : 0), 0); let x = 540 - tot / 2;
      const y = CAP_Y + (li - (lines.length - 1) / 2) * CAP_CAP * 1.55;
      ln.forEach(([t, k, s, w], wi) => {
        const p = span(f, s, s + 6);
        if (!dust) write(g, t, x, y, CAP_CAP, k ? RED : CHALK, seed + li * 50 + wi * 7, p, "left", 0.97);
        if (k && p >= 1 && !dust) line(g, false, [[x - 4, y + CAP_CAP + 14], [x + w / 2, y + CAP_CAP + 10], [x + w + 4, y + CAP_CAP + 15]], 3, RED, seed + 900 + wi, 0.8, 1, span(f, s + 6, s + 12));
        x += w + space;
      });
    });
  }, 0.12);
};
