import { Gfx, rng, type Ctx, type Env, type P } from "./core";
import type { Film } from "./film";
import { blob, fillShape } from "./gallery";
import {
  CHALK, CHALK_M, YEL, RED, BLUE, PINK, B0, B1, H, W,
  arrow, board, captions, chalk, chocBar, clamp01, frame, line, loop, priceTag, rect, scumble, span, strike, write, textW,
} from "./chalkkit";
import { LINES } from "./s002timing";

// MONEY MIRAGE · SHRINKFLATION. A 9:16 Short taught on one chalkboard. Every mark is written on
// the word it belongs to (word times come from the narration via s002timing.ts); each new idea
// starts with the felt eraser sweeping the board. Captions are chalked word by word low on the
// board, key words in red. One pure function of the frame.

const FPS = 30, BPM = 60;
const sec = (s: number) => s * FPS;
const END_HOLD = 1.6;                                            // seconds the follow card holds after the last word
export const DURATION = Math.ceil(sec(LINES[LINES.length - 1].e + END_HOLD) / 30) * 30;
/** frame at which line li, word wi starts (+ offset seconds) */
const at = (li: number, wi = 0, off = 0) => sec(LINES[li].words[Math.min(wi, LINES[li].words.length - 1)].s + off);
const endOf = (li: number) => sec(LINES[li].e);
/** the word index in line li whose text starts with `w` (case-insensitive), for anchoring */
const wix = (li: number, w: string) => { const i = LINES[li].words.findIndex((x) => x.t.toUpperCase().replace(/[^A-Z0-9%.]/g, "").startsWith(w.toUpperCase())); if (i < 0) throw new Error(`shrink: no word '${w}' in line ${li}`); return i; };
const AT = (li: number, w: string, off = 0) => at(li, wix(li, w), off);

// ---------------------------------------------------------------- the scene table
// Each scene owns a board from `from` (when the eraser starts) until the next scene's eraser.
type Scene = { id: string; from: number; draw: (g: Gfx, f: number) => void };
const WIPE = 14;                                                 // frames the felt eraser takes to cross

// ---- 1 · hook: the card, then the tag, the +12%, the brain
const HOOK_CARD_END = sec(2.4);
const sHook = (g: Gfx, f: number) => {
  if (f < HOOK_CARD_END + WIPE) {   // the hook card, written fast, in words the narrator does not say
    chalk(g, (dust) => {
      write(g, "₹100", 540, 560, 150, CHALK, 11, span(f, sec(0.12), sec(0.9)));
      write(g, "=", 540, 790, 150, YEL, 12, span(f, sec(0.9), sec(1.2)));
      write(g, "₹112?", 540, 1010, 150, RED, 13, span(f, sec(1.2), sec(2.1)));
      if (!dust) line(g, false, [[300, 1220], [540, 1212], [790, 1224]], 5, RED, 14, 0.85, 1, span(f, sec(2.0), sec(2.3)));
    });
    if (f < HOOK_CARD_END) return;
  }
  const t0 = Math.max(HOOK_CARD_END + WIPE, AT(0, "PRICE"));
  priceTag(g, 260, 760, "₹100", 21, span(f, t0, t0 + 16));
  const n12 = AT(0, "12%");
  if (f >= n12) {   // the hero number slams in on the spoken "twelve percent"
    const p = span(f, n12, n12 + 5), sc = 1.5 - 0.5 * p, s = f < n12 + 8 ? (rng(f)() - 0.5) * 10 * (1 - span(f, n12 + 5, n12 + 8)) : 0;
    g.push(540 + s, 300, sc); chalk(g, () => write(g, "+12%", 0, -85, 170, RED, 22, clamp01(p * 3))); g.pop();
  }
  const bt = AT(0, "BRAIN");   // the brain, two lobes and its folds, and a question mark over it
  chalk(g, (dust) => {
    const bx = 790, by = 1080, q = span(f, bt - 4, bt + 14);
    line(g, dust, loop(bx, by, 150, 105, 3.6, 0.98, 18), 3.2, PINK, 23, 0.9, 1.6, clamp01(q * 2));
    line(g, dust, [[bx, by - 100], [bx - 10, by - 40], [bx + 8, by + 20], [bx - 6, by + 98]], 2.4, PINK, 24, 0.8, 1.2, clamp01(q * 3 - 1));
    [[[bx - 110, by - 20], [bx - 70, by - 50], [bx - 40, by - 10], [bx - 80, by + 30]], [[bx + 40, by - 60], [bx + 90, by - 30], [bx + 60, by + 10], [bx + 110, by + 40]], [[bx - 100, by + 50], [bx - 50, by + 70], [bx - 20, by + 40]], [[bx + 30, by + 60], [bx + 80, by + 80]]]
      .forEach((pts, i) => line(g, dust, pts as P[], 2, PINK, 25 + i, 0.7, 1.4, clamp01(q * 3 - 1.6 - i * 0.2)));
    write(g, "?", bx + 170, by - 210, 120, YEL, 29, span(f, AT(0, "MISS"), AT(0, "MISS") + 8));
  });
};

// ---- 2 · the bar loses a column (lines 1-2)
const sBar = (g: Gfx, f: number) => {
  const a = at(1), gm = AT(1, "100"), n90 = AT(1, "90"), wr = AT(1, "WRAPPER");
  const tiny = AT(2, "TINY"), chg = AT(2, "CHANGED"), shr = AT(2, "SHRINKFLATION");
  const eraseP = span(f, chg - 2, chg + 14);                       // the eraser takes the tenth column
  chocBar(g, 540, 660, 760, 300, 10, 3, 200, { slab: span(f, a, a + 28), grid: span(f, a + 24, a + 40), rim: span(f, a + 36, a + 48), gone: f >= chg + 6 ? 1 : 0, ghost: span(f, chg + 6, chg + 22) });
  if (eraseP > 0 && eraseP < 1) {   // the felt block rubbing out the last column
    const ex = 880, ey = 560 + eraseP * 200 + Math.sin(eraseP * 18) * 30;
    g.group("plain", () => { fillShape(g, rect(ex - 50, ey - 60, ex + 60, ey + 60), "#a0714a"); fillShape(g, rect(ex - 50, ey + 20, ex + 60, ey + 60), "#8e8a86"); });
  }
  chalk(g, (dust) => {
    write(g, "100G", 330, 410, 92, CHALK, 300, span(f, gm, gm + 12));
    if (!dust) strike(g, false, 225, 456, 440, RED, 310, span(f, tiny, tiny + 10));
    arrow(g, dust, [450, 460], [600, 460], YEL, 330, span(f, n90 - 2, n90 + 6));
    write(g, "90G", 700, 400, 120, YEL, 320, span(f, n90, n90 + 12));
  });
  priceTag(g, 380, 1120, "₹100", 400, span(f, wr - 2, wr + 18));
  chalk(g, (dust) => { write(g, "SAME", 860, 1090, 54, YEL, 410, span(f, shr - 4, shr + 10)); arrow(g, dust, [790, 1120], [740, 1125], YEL, 420, span(f, shr + 6, shr + 14)); });
};

// ---- 3 · how you shop: the basket, then the two drops (lines 3-4)
const sShop = (g: Gfx, f: number) => {
  const a = at(3), bx = 540, by = 300;
  chalk(g, (dust) => {   // a wire basket: rim, tapered body, the weave, the handle
    const q = span(f, a, a + 26);
    line(g, dust, [[bx - 170, by - 40], [bx + 170, by - 40]], 3.2, CHALK, 501, 0.92, 0.6, clamp01(q * 4));
    line(g, dust, [[bx - 160, by - 40], [bx - 120, by + 110], [bx + 120, by + 110], [bx + 160, by - 40]], 3, CHALK, 502, 0.92, 0.6, clamp01(q * 4 - 1));
    for (let i = 1; i < 6; i++) { const x = bx - 160 + i * 53; line(g, dust, [[x, by - 36], [bx + (x - bx) * 0.76, by + 106]], 1.6, CHALK, 510 + i, 0.6, 0.4, clamp01(q * 4 - 2 - i * 0.1)); }
    line(g, dust, [[bx - 145, by + 10], [bx + 145, by + 10]], 1.6, CHALK, 520, 0.6, 0.4, clamp01(q * 4 - 2.5)); line(g, dust, [[bx - 132, by + 60], [bx + 132, by + 60]], 1.6, CHALK, 521, 0.6, 0.4, clamp01(q * 4 - 2.7));
    line(g, dust, loop(bx, by - 40, 120, 110, Math.PI, 0.5, 10), 3, CHALK, 522, 0.9, 0.8, clamp01(q * 4 - 3));
  });
  // the two drops: price up 1% → a long fall; pack 1% smaller → half as far
  const base = 640, unit = 300, p1 = AT(4, "RAISE"), d1 = AT(4, "DROP"), n12 = AT(4, "1.2%"), p2 = AT(4, "SHRINK"), hf = AT(4, "HALF");
  chalk(g, (dust) => {
    line(g, dust, [[B0 + 70, base], [B1 - 70, base]], 2.6, CHALK, 530, 0.85, 0.5, span(f, p1 - 10, p1 + 4));
    write(g, "₹ +1%", 330, base - 120, 70, YEL, 531, span(f, p1, p1 + 14));
    write(g, "G -1%", 750, base - 120, 70, BLUE, 532, span(f, p2, p2 + 14));
  });
  const bar = (x: number, len: number, col: string, a0: number, seed: number) => {
    const q = span(f, a0, a0 + 16), y1 = base + 10 + len * unit * q;
    if (q <= 0) return;
    chalk(g, (dust) => { scumble(g, dust, rect(x - 70, base + 10, x + 70, y1), col, { angle: -0.9, gap: 4, w: 4.2, alpha: 0.42, seed }); line(g, dust, [[x - 70, y1], [x + 70, y1]], 3, col, seed + 1, 0.9, 0.5, 1); });
    if (q >= 1) chalk(g, (dust) => arrow(g, dust, [x, base + 40], [x, base + 10 + len * unit - 30], CHALK, seed + 2, span(f, a0 + 16, a0 + 22), 3.4));
  };
  bar(330, 1.2, RED, d1 - 4, 540);
  bar(750, 0.6, BLUE, hf - 6, 550);
  chalk(g, () => { const s = span(f, n12, n12 + 5); if (s > 0) { g.push(330, base + 10 + 1.2 * unit + 30, 1.4 - 0.4 * s); write(g, "1.2%", 0, 0, 96, RED, 560, clamp01(s * 3)); g.pop(); } write(g, "½", 750, base + 10 + 0.6 * unit + 30, 96, BLUE, 561, 0); });
  chalk(g, () => write(g, "HALF", 750, base + 10 + 0.6 * unit + 34, 80, BLUE, 562, span(f, hf + 4, hf + 16)));
};

// ---- 4 · the eye watches the price, never the grams (line 5)
const sEye = (g: Gfx, f: number) => {
  const a = at(5), pr = AT(5, "PRICE"), gr = AT(5, "GRAMS");
  priceTag(g, 160, 820, "₹100", 610, span(f, pr - 4, pr + 16));
  chalk(g, (dust) => {   // the eye: lids, iris looking left at the tag, pupil, lashes
    const ex = 640, ey = 470, q = span(f, a, a + 24);
    const top: P[] = Array.from({ length: 13 }, (_, k) => [ex - 260 + k * 43.3, ey - Math.sin((k / 12) * Math.PI) * 150] as P);
    const bot: P[] = Array.from({ length: 13 }, (_, k) => [ex - 260 + k * 43.3, ey + Math.sin((k / 12) * Math.PI) * 120] as P);
    line(g, dust, top, 3.4, CHALK, 620, 0.92, 0.7, clamp01(q * 3)); line(g, dust, bot, 3, CHALK, 621, 0.9, 0.7, clamp01(q * 3 - 0.6));
    const ix = ex - 90, iy = ey;
    line(g, dust, loop(ix, iy, 92, 92, -0.4, 1.05, 16), 3, BLUE, 622, 0.9, 0.8, clamp01(q * 3 - 1.2));
    scumble(g, dust, loop(ix, iy, 44, 44, 0, 1, 16), CHALK, { angle: 0.8, gap: 3, w: 4, alpha: 0.55, seed: 623, progress: clamp01(q * 3 - 1.8) });
    for (let k = 0; k < 7; k++) { const t = (k + 2.5) / 12, x = ex - 260 + t * 520, y = ey - Math.sin(t * Math.PI) * 150; line(g, dust, [[x, y], [x + (x - ex) * 0.12, y - 44]], 2.2, CHALK, 630 + k, 0.8, 0.5, clamp01(q * 3 - 2 - k * 0.1)); }
    // the sight line to the tag
    if (!dust) for (let k = 0; k < 7; k++) line(g, false, [[ix - 110 - k * 44, iy + 70 + k * 40], [ix - 130 - k * 44, iy + 82 + k * 40]], 2, YEL, 640 + k, 0.8, 0.3, span(f, pr + k * 2, pr + k * 2 + 4));
    // the tiny G, far from the eye's line, with its question mark
    write(g, "G", 880, 1110, 60, CHALK, 650, span(f, gr - 2, gr + 6));
    write(g, "?", 940, 1060, 70, RED, 651, span(f, gr + 6, gr + 14));
  });
};

// ---- 5 · brands shrink the pack; +12% per unit (line 6)
const sSqueeze = (g: Gfx, f: number) => {
  const a = at(6), sq = AT(6, "SHRINK"), dn = AT(6, "DOWNSIZE"), n12 = AT(6, "12%");
  const shrinkP = span(f, dn, dn + 20), w0 = 520, w1 = w0 * 0.82, w = w0 + (w1 - w0) * shrinkP, h = 420 - 60 * shrinkP, cx = 540, cy = 620;
  chalk(g, (dust) => {   // a cereal-style box, drawn as a front and a side
    const q = span(f, a, a + 20), x0 = cx - w / 2, x1 = cx + w / 2, y0 = cy - h / 2, y1 = cy + h / 2;
    [[[x0, y0], [x1, y0]], [[x1, y0], [x1, y1]], [[x1, y1], [x0, y1]], [[x0, y1], [x0, y0]], [[x1, y0], [x1 + 60, y0 - 50]], [[x1 + 60, y0 - 50], [x1 + 60, y1 - 50]], [[x1 + 60, y1 - 50], [x1, y1]], [[x0, y0], [x0 + 60, y0 - 50]], [[x0 + 60, y0 - 50], [x1 + 60, y0 - 50]]]
      .forEach((s, i) => line(g, dust, s as P[], 3.2, CHALK, 700 + i, 0.92, 0.6, clamp01(q * 9 - i)));
    scumble(g, dust, rect(x0 + 8, y0 + 8, x1 - 8, y1 - 8), YEL, { angle: -0.7, gap: 4, w: 4.4, alpha: 0.4, seed: 710, progress: q });
    if (shrinkP > 0 && !dust) { const p = clamp01(shrinkP * 1.4); arrow(g, false, [x0 - 170, cy], [x0 - 30, cy], RED, 720, p, 4); arrow(g, false, [x1 + 230, cy], [x1 + 90, cy], RED, 722, p, 4); }
    if (f >= sq && f < dn) write(g, "", cx, cy, 10, CHALK, 1, 0);
  });
  if (f >= n12) { const p = span(f, n12, n12 + 5); g.push(540, 1060, 1.5 - 0.5 * p); chalk(g, () => { write(g, "+12%", 0, -85, 170, RED, 730, clamp01(p * 3)); }); g.pop(); chalk(g, () => write(g, "PER UNIT", 540, 1215, 56, YEL, 731, span(f, n12 + 6, n12 + 18))); }
};

// ---- 6 · the peaks get gaps; then the gavel (lines 7-8)
const sPeaks = (g: Gfx, f: number) => {
  const a = at(7), gp = AT(7, "WIDENED"), sp = AT(7, "SAME"), mis = AT(8, "MISLED"), crt = AT(8, "COURT");
  const n = 9, x0 = 120, step = 93, base = 640, ph = 150;
  for (let i = 0; i < n; i++) {   // a triangular bar of peaks; alternate peaks rubbed out on "widened the gaps"
    const gone = i % 2 === 1, er = gone ? span(f, gp + i * 1.5, gp + i * 1.5 + 10) : 0;
    const q = span(f, a + i * 3, a + i * 3 + 10);
    if (q <= 0 || er >= 1) { if (er >= 1) g.group("plain", () => scumble(g, false, [[x0 + i * step, base], [x0 + i * step + step / 2, base - ph], [x0 + (i + 1) * step, base]], CHALK, { angle: 0.4, gap: 8, w: 12, alpha: 0.1, seed: 800 + i }), { blur: 5 }); continue; }
    const tri: P[] = [[x0 + i * step, base], [x0 + i * step + step / 2, base - ph], [x0 + (i + 1) * step, base]];
    chalk(g, (dust) => {
      scumble(g, dust, tri, "#c9a173", { angle: -0.7, gap: 3.6, w: 4.2, alpha: 0.42 * (1 - er), seed: 810 + i, progress: q });
      line(g, dust, [tri[0], tri[1]], 2.6, CHALK, 820 + i, 0.9 * (1 - er), 0.5, q); line(g, dust, [tri[1], tri[2]], 2.6, CHALK, 830 + i, 0.9 * (1 - er), 0.5, q);
    });
  }
  chalk(g, (dust) => {
    line(g, dust, [[x0, base], [x0 + n * step, base]], 3, CHALK, 840, 0.9, 0.5, span(f, a + 20, a + 30));
    write(g, "2016", 540, 790, 80, BLUE, 841, span(f, AT(7, "2016"), AT(7, "2016") + 10));
  });
  priceTag(g, 110, 1010, "SAME ₹", 850, span(f, sp - 4, sp + 14));
  // the gavel: handle, head, the strike block; it comes down on "misled"
  const down = span(f, mis - 6, mis), ang = -0.9 + 0.9 * down, hx = 840, hy = 1150, shake = f >= mis && f < mis + 6 ? (rng(f + 9)() - 0.5) * 12 : 0;
  if (f >= crt - 10) {
    const vis = span(f, crt - 10, crt + 6);
    chalk(g, (dust) => {
      line(g, dust, [[hx - 110, hy + 120 + shake], [hx + 110, hy + 120 + shake]], 4, CHALK, 860, 0.9, 0.5, vis);
      g.push(hx + 100, hy + 40 + shake, 1, ang);
      line(g, dust, [[0, 0], [-230, -10]], 6, "#c9a173", 861, 0.95, 0.3, vis);
      scumble(g, dust, rect(-300, -55, -200, 45), "#c9a173", { angle: 0.8, gap: 3.6, w: 4, alpha: 0.5, seed: 862, progress: vis });
      line(g, dust, [[-300, -55], [-200, -55], [-200, 45], [-300, 45], [-300, -55]], 2.6, CHALK, 863, 0.9, 0.5, vis);
      g.pop();
    });
    if (f >= mis) chalk(g, () => write(g, "MISLED", 780, 960, 80, RED, 864, span(f, mis, mis + 12)));
  }
};

// ---- 7 · the mirage: the tag stays, the rise is inside the pack (line 9)
const sMirage = (g: Gfx, f: number) => {
  const a = at(9), tg = AT(9, "TAG"), ins = AT(9, "INSIDE");
  priceTag(g, 120, 480, "₹100", 900, span(f, a, a + 18));
  chalk(g, (dust) => {
    write(g, "MIRAGE", 540, 200, 96, YEL, 901, span(f, AT(9, "MIRAGE") - 2, AT(9, "MIRAGE") + 14));
    if (f >= tg && !dust) { const s = span(f, tg, tg + 8); line(g, false, loop(300, 470, 210, 110, -0.5, 1.1, 16), 3, YEL, 902, 0.85, 1, s); }
    const x0 = 360, y0 = 760, x1 = 900, y1 = 1260, q = span(f, a + 10, a + 30);
    [[[x0, y0], [x1, y0]], [[x1, y0], [x1, y1]], [[x1, y1], [x0, y1]], [[x0, y1], [x0, y0]]].forEach((s, i) => line(g, dust, s as P[], 3.2, CHALK, 910 + i, 0.92, 0.6, clamp01(q * 4 - i)));
    arrow(g, dust, [260, 600], [560, 920], RED, 920, span(f, ins - 6, ins + 6), 4.4);
  });
  if (f >= ins + 4) {   // the hero flash: the rise glowing inside the pack
    const p = span(f, ins + 4, ins + 9);
    g.group("plain", () => g.glow(630, 1010, 230, "#ffb3a6", 0.32 * p));
    g.push(630, 1010, 1.4 - 0.4 * p); chalk(g, () => write(g, "+12%", 0, -85, 170, RED, 930, clamp01(p * 3))); g.pop();
  }
};

// ---- 8 · the shelf label: check the price per kilo (line 10)
const sShelf = (g: Gfx, f: number) => {
  const a = at(10), big = AT(10, "BIG"), kilo = AT(10, "KILO"), x0 = 140, y0 = 380, x1 = 940, y1 = 1000;
  chalk(g, (dust) => {
    const q = span(f, a, a + 16);
    [[[x0, y0], [x1, y0]], [[x1, y0], [x1, y1]], [[x1, y1], [x0, y1]], [[x0, y1], [x0, y0]]].forEach((s, i) => line(g, dust, s as P[], 3.4, CHALK, 1000 + i, 0.92, 0.6, clamp01(q * 4 - i)));
    line(g, dust, [[x0 + 30, 520], [x1 - 30, 520]], 2, CHALK, 1005, 0.6, 0.4, q);
    write(g, "CHOCOLATE 90G", 540, 430, 50, CHALK, 1006, span(f, a + 8, a + 24));
    write(g, "₹100", 540, 600, 190, CHALK, 1007, span(f, a + 14, big + 8));
    if (!dust) strike(g, false, 300, 720, 790, CHALK, 1008, 0);   // (kept unwritten: the big number stays clean)
    write(g, "₹1,111 / KG", 700, 900, 52, YEL, 1009, span(f, big + 6, kilo));
    if (!dust) line(g, false, loop(700, 928, 230, 62, -0.3, 1.12, 18), 4.2, RED, 1010, 0.95, 1.4, span(f, kilo - 2, kilo + 12));
  });
};

// ---- 9 · the same tag, twice (line 11)
const sSame = (g: Gfx, f: number) => {
  const a = at(11), ex = AT(11, "EXACTLY");
  priceTag(g, 90, 560, "₹100", 1100, span(f, a, a + 16));
  priceTag(g, 90, 1000, "₹100", 1101, span(f, a + 8, a + 24));
  chalk(g, () => { write(g, "=", 300, 700, 150, YEL, 1102, span(f, ex - 2, ex + 8)); write(g, "100G", 760, 500, 80, CHALK, 1104, span(f, ex + 4, ex + 16)); write(g, "90G", 760, 940, 80, RED, 1103, span(f, ex + 10, ex + 22)); });
};

// ---- 10 · follow (line 12)
const sFollow = (g: Gfx, f: number) => {
  const a = at(12), mm = AT(12, "MONEY"), fo = AT(12, "FOLLOW");
  chalk(g, () => { write(g, "MONEY", 540, 470, 150, CHALK, 1200, span(f, mm - 4, mm + 14)); write(g, "MIRAGE", 540, 680, 150, YEL, 1201, span(f, mm + 6, mm + 24)); });
  const bx = 540, by = 1060, press = f >= fo && f < fo + 8 ? 0.94 : 1, q = span(f, a + 4, a + 22);
  g.push(bx, by, press);
  chalk(g, (dust) => {
    scumble(g, dust, rect(-260, -80, 260, 80), RED, { angle: -0.8, gap: 3, w: 4.6, alpha: f >= fo ? 0.6 : 0.32, seed: 1202, progress: q });
    [[[-260, -80], [260, -80]], [[260, -80], [260, 80]], [[260, 80], [-260, 80]], [[-260, 80], [-260, -80]]].forEach((s, i) => line(g, dust, s as P[], 3.4, CHALK, 1203 + i, 0.92, 0.5, clamp01(q * 4 - i)));
    write(g, "FOLLOW", 0, -42, 84, CHALK, 1208, span(f, a + 14, fo));
  });
  g.pop();
  if (f >= fo) chalk(g, (dust) => {   // the tap: a fingertip and two ripples
    const tp = span(f, fo, fo + 10);
    line(g, dust, loop(bx + 200, by + 40, 40 + tp * 30, 40 + tp * 30, 0, 1, 14), 2.4, CHALK, 1210, 0.8 * (1 - tp * 0.6), 0.4, 1);
    line(g, dust, [[bx + 200, by + 60], [bx + 250, by + 250]], 7, CHALK, 1211, 0.9, 0.4, 1);
  });
};

// the order on the board, each scene from the moment its eraser starts
const SCENES: Scene[] = [
  { id: "hook", from: 0, draw: sHook },
  { id: "bar", from: at(1) - WIPE, draw: sBar },
  { id: "shop", from: at(3) - WIPE, draw: sShop },
  { id: "eye", from: at(5) + 6, draw: sEye },
  { id: "squeeze", from: at(6) - WIPE, draw: sSqueeze },
  { id: "peaks", from: at(7) - WIPE, draw: sPeaks },
  { id: "mirage", from: at(9) - WIPE, draw: sMirage },
  { id: "shelf", from: at(10) - WIPE, draw: sShelf },
  { id: "same", from: at(11) - WIPE, draw: sSame },
  { id: "follow", from: at(12) - WIPE, draw: sFollow },
];
((): void => { for (let i = 1; i < SCENES.length; i++) if (SCENES[i].from <= SCENES[i - 1].from + WIPE) throw new Error(`shrink: scene ${SCENES[i].id} starts before ${SCENES[i - 1].id}'s eraser is done`); })();

// the hook card is wiped too: an extra eraser pass at HOOK_CARD_END inside scene 1
const wipeAt = (f: number): { scene: Scene; prev: Scene | null; p: number } => {
  let k = 0; for (let i = 0; i < SCENES.length; i++) if (f >= SCENES[i].from) k = i;
  const sc = SCENES[k], p = k === 0 ? 1 : span(f, sc.from, sc.from + WIPE);
  return { scene: sc, prev: k ? SCENES[k - 1] : null, p };
};

// captions: the current line split into chunks of <= 5 words (at commas and full stops)
type Chunk = { li: number; words: { t: string; key: boolean; s: number }[]; from: number; to: number };
const CHUNKS: Chunk[] = (() => {
  const out: Chunk[] = [];
  LINES.forEach((ln, li) => {
    let cur: Chunk["words"] = [];
    const flush = () => { if (cur.length) out.push({ li, words: cur, from: 0, to: 0 }); cur = []; };
    ln.words.forEach((w, i) => { cur.push({ t: w.t.toUpperCase(), key: w.key, s: sec(w.s) }); const left = ln.words.length - 1 - i; if (left === 0) return; if (left < 2) return; if (cur.length >= 5 || (/[.?!:]$/.test(w.t) && cur.length >= 2) || (/,$/.test(w.t) && cur.length >= 3)) flush(); });
    flush();
  });
  out.forEach((c, i) => { c.from = c.words[0].s - 2; c.to = i + 1 < out.length ? out[i + 1].words[0].s - 2 : 1e9; });
  return out;
})();

const draw = (ctx: Ctx, f: number, env: Env) => {
  const g = new Gfx(ctx, env, f, CHALK_M);
  ctx.setTransform(env.scale, 0, 0, env.scale, 0, 0);
  board(g, ctx, 5);
  const { scene, prev, p } = wipeAt(f);
  // the felt eraser crossing: ahead of it, the last scene's finished board; behind it, the new scene
  if (p < 1 && prev) {
    const wx = B0 + p * (B1 - B0), c = g.cur;
    c.save(); c.beginPath(); c.rect(wx, 0, W - wx, H); c.clip(); prev.draw(g, scene.from - 1); c.restore();
    c.save(); c.beginPath(); c.rect(0, 0, wx, H); c.clip(); scene.draw(g, f); c.restore();
    const ey = 760 + Math.sin(p * 9) * 260;
    g.group("plain", () => { fillShape(g, rect(wx - 70, ey - 130, wx + 30, ey + 130), "#a0714a"); fillShape(g, rect(wx - 20, ey - 130, wx + 30, ey + 130), "#8e8a86"); for (let i = 0; i < 20; i++) { const r = rng(i * 13 + Math.floor(f)); fillShape(g, blob(wx + 34 + r() * 30, ey - 130 + r() * 260, 2, 2, i, 0.3, 6), CHALK, 0.4); } });
  } else if (scene.id === "hook" && f >= HOOK_CARD_END && f < HOOK_CARD_END + WIPE) {
    const q = span(f, HOOK_CARD_END, HOOK_CARD_END + WIPE), wx = B0 + q * (B1 - B0), c = g.cur;
    c.save(); c.beginPath(); c.rect(wx, 0, W - wx, H); c.clip(); sHook(g, HOOK_CARD_END - 1); c.restore();
    c.save(); c.beginPath(); c.rect(0, 0, wx, H); c.clip(); sHook(g, f); c.restore();
    const ey = 760 + Math.sin(q * 9) * 260;
    g.group("plain", () => { fillShape(g, rect(wx - 70, ey - 130, wx + 30, ey + 130), "#a0714a"); fillShape(g, rect(wx - 20, ey - 130, wx + 30, ey + 130), "#8e8a86"); });
  } else scene.draw(g, f);
  // captions (not during the hook card, which is its own text)
  if (f >= HOOK_CARD_END) {
    const ch = CHUNKS.find((c) => f >= c.from && f < c.to);
    if (ch) captions(g, f, ch.words.map((w) => [w.t, w.key, w.s] as [string, boolean, number]), 3000 + ch.li * 97 + Math.round(ch.from) % 50);
  }
  frame(g);
};

export const shrink: Film = {
  meta: {
    title: "Money Mirage · shrinkflation", W, H, fps: FPS, bpm: BPM, durationFrames: DURATION, kind: "explainer",
    holds: [[Math.max(0, Math.floor(sec(LINES[LINES.length - 1].e))), DURATION, "the follow card"]],
  },
  assets: { images: {} },
  shots: [{ id: "lesson", start: 0, end: DURATION, draw }],
};
void textW; void PINK;
