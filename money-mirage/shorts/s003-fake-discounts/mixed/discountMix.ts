import { rng, type Ctx, type Env, type P } from "./core";
import type { Film } from "./film";
import { Cam, drawPart, order, PLATE, STUD, type Part } from "./toyBrickKit";
import { LINES } from "./s003timing";
import {
  W, H, sec, span, clamp01, easeOut, easeIO, back, INK, RED, STAMP, GOLD, KEY, CREAM, NAVY,
  scrapPage, comicPage, theatre, newsPage, grain, card, onCard, tape, cutout, marker, brushLine,
  penLoop, penStrike, penArrow, stamp, ransom, label, hero, txt, burst, pow, clipping, halftoneFill,
  priceTag, brain, rect, rrect, ellipse, xf, makeChunks, captions, type CardSpec,
} from "./mirageKit";

// MONEY MIRAGE · s003 THE "WAS" PRICE THAT NEVER WAS, mixed media (scrapbook + marker comic base;
// toy theatre, newsprint and toy brick beats). Marks land on their words (s003timing.ts).

const at = (li: number, wi = 0, off = 0) => sec(LINES[li].words[Math.min(wi, LINES[li].words.length - 1)].s + off);
const wix = (li: number, w: string) => { const i = LINES[li].words.findIndex((x) => x.t.toUpperCase().replace(/[^A-Z0-9%₹]/g, "").startsWith(w.toUpperCase())); if (i < 0) throw new Error(`discountMix: no word '${w}' in line ${li}`); return i; };
const AT = (li: number, w: string, off = 0) => at(li, wix(li, w), off);
export const DURATION = Math.ceil(sec(LINES[LINES.length - 1].e + 1.6) / 30) * 30;
const HOOK_END = sec(2.4), WHIP = 10;
type Scene = { id: string; from: number; bg: (c: Ctx, f: number) => void; draw: (c: Ctx, f: number) => void; punch?: number[]; dark?: boolean };
let LOGO_IMG: CanvasImageSource | undefined;

// ---------------------------------------------------------------- props for this film (marker comic)
/** a magnifying glass, lens centred at (x, y) */
const magnifier = (c: Ctx, x: number, y: number, s: number, p: number) => {
  if (p <= 0) return; const k = back(p); c.save(); c.translate(x, y); c.scale(k * s, k * s);
  marker(c, xf(rrect(60, 260, 26), 150, 170, -0.75), "#7a4a26", { seed: 701, contour: 7, shadow: "#55331a" });
  marker(c, ellipse(0, 0, 150, 150, 48), "#c9a64e", { seed: 702, contour: 9, shadow: "#9a7a30", streak: false });
  c.save(); c.globalAlpha = 0.35; c.fillStyle = "#cfe7f2"; c.beginPath(); c.arc(0, 0, 122, 0, 6.283); c.fill(); c.restore();
  c.strokeStyle = "#ffffff"; c.globalAlpha = 0.7; c.lineWidth = 10; c.lineCap = "round"; c.beginPath(); c.arc(0, 0, 92, 3.6, 4.4); c.stroke(); c.globalAlpha = 1;
  c.restore();
};
/** a ship's anchor on a rope (toy-theatre cut-out) */
const anchor = (c: Ctx, x: number, y: number, s: number, seed = 711) => {
  c.save(); c.translate(x, y); c.scale(s, s);
  const shank = rrect(40, 300, 16, 0, 0), ring = ellipse(0, -190, 44, 44, 28), stock = rrect(200, 34, 14, 0, -120), arm: P[] = [];
  for (let k = 0; k <= 20; k++) { const a = Math.PI * 0.08 + (k / 20) * Math.PI * 0.84; arm.push([Math.cos(a) * 150, 120 + Math.sin(a) * 90]); }
  for (let k = 20; k >= 0; k--) { const a = Math.PI * 0.08 + (k / 20) * Math.PI * 0.84; arm.push([Math.cos(a) * 112, 120 + Math.sin(a) * 58]); }
  [ring, shank, stock, arm].forEach((pt, i) => cutout(c, pt, "#56606a", seed + i, 5));
  c.restore();
};
/** a phone showing a price-history line, drawn to q */
const phone = (c: Ctx, x: number, y: number, s: number, rot: number, q: number, f: number) => {
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s);
  marker(c, rrect(440, 820, 60), "#2d3238", { seed: 721, contour: 9, shadow: "#1b1f23" });
  c.fillStyle = "#f6f1e6"; c.fillRect(-190, -360, 380, 700);
  txt(c, "PRICE HISTORY", 0, -320, 30, INK);
  c.strokeStyle = "rgba(36,27,21,0.25)"; c.lineWidth = 2; for (let i = 0; i < 5; i++) { c.beginPath(); c.moveTo(-170, -240 + i * 110); c.lineTo(170, -240 + i * 110); c.stroke(); }
  const pts: P[] = []; for (let i = 0; i <= 30; i++) { const xx = -170 + (i / 30) * 340, spike = i >= 26 && i <= 28 ? -260 : 0; pts.push([xx, 120 + spike + Math.sin(i * 1.7) * 6]); }
  brushLine(c, pts, 9, KEY, q);
  txt(c, "₹999", -100, 70, 40, INK, { alpha: span(q, 0.3, 0.5) });
  txt(c, "₹1,999", 110, -200, 34, KEY, { alpha: span(q, 0.85, 1) });
  void f; c.restore();
};
/** a calendar sheet of 30 days, the lowest day circled */
const calendar = (c: Ctx, x: number, y: number, w: number, rot: number, p: number, lowP: number) => {
  if (p <= 0) return; c.save(); c.translate(x, y); c.rotate(rot); const k = back(p); c.scale(k, k);
  marker(c, rect(w, w * 0.92), "#fbf7ee", { seed: 731, contour: 7, shadow: "#ded4bf", hi: false, streak: false });
  c.fillStyle = STAMP; c.fillRect(-w / 2, -w * 0.46, w, w * 0.16); txt(c, "30 DAYS", 0, -w * 0.38, w * 0.09, "#ffffff");
  const cw = w / 6.4; for (let i = 0; i < 30; i++) { const cx = -w / 2 + cw * 0.7 + (i % 6) * cw, cy = -w * 0.2 + Math.floor(i / 6) * cw * 0.95; txt(c, `${i + 1}`, cx, cy, cw * 0.36, INK, { weight: 800, alpha: span(p, i / 40, i / 40 + 0.2) }); }
  if (lowP > 0) penLoop(c, -w / 2 + cw * 0.7 + 3 * cw, -w * 0.2 + 2 * cw * 0.95, cw * 0.48, cw * 0.36, lowP, 732, RED, 7);
  c.restore();
};

// ---------------------------------------------------------------- toy bricks: 10 shops, 3 turn red
let PID = 0;
const shopBrick = (x: number, z: number, color: string): Part => ({ id: PID++, color, kind: "prism", foot: [[x, z], [x + 2, z], [x + 2, z + 2], [x, z + 2]], y0: 0, h: 6, studs: true, step: 0 });

// ---------------------------------------------------------------- scenes
const SCENES: Scene[] = (() => {
  const S: Scene[] = [];
  // 1 · hook (comic): the 70% OFF tag pows in; its old price turns into a ghost
  {
    const a = HOOK_END, n70 = AT(0, "70%"), nv = AT(0, "NEVER"), ex = AT(0, "EXISTED");
    S.push({ id: "hook", from: a, punch: [n70, ex], bg: (c) => comicPage(c, 61),
      draw: (c, f) => {
        burst(c, 540, 560, 150, 420, 30, 6, span(f, n70, n70 + 8));
        pow(c, 540, 560, 330, 210, GOLD, 18, span(f, n70 - 2, n70 + 6));
        hero(c, "70% OFF", 540, 560, f, n70, KEY, 140, -0.05);
        priceTag(c, 560, 1080, 520, 250, 0.05, "", span(f, a + 2, a + 14), 601);
        const ghost = span(f, nv, ex + 6);
        txt(c, "₹1,999", 600, 1090, 120, INK, { alpha: 1 - 0.8 * ghost });
        if (ghost > 0) { c.save(); c.globalAlpha = ghost; c.setLineDash([18, 14]); c.strokeStyle = RED; c.lineWidth = 6; c.strokeRect(410, 1020, 380, 140); c.restore(); txt(c, "?", 860, 960, 170, RED, { stroke: 14, sc: back(span(f, ex, ex + 10)), alpha: span(f, ex, ex + 4), rot: 0.15 }); }
      } });
  }
  // 2 · the trick (scrapbook): a taped card; the "was" label climbs before the sale
  {
    const a = at(1), tr = AT(1, "TRICK"), up = AT(1, "UP");
    const CD: CardSpec = { cx: 540, cy: 820, w: 860, h: 820, rot: 0.02, color: "#f2eadb", seed: 611, from: [-80, 180] };
    S.push({ id: "trick", from: a - WHIP, punch: [tr, up], bg: (c) => scrapPage(c, 321),
      draw: (c, f) => {
        const cp = span(f, a, a + 12); card(c, CD, cp); tape(c, 170, 430, -0.6, 190, span(f, a + 10, a + 16), 612); tape(c, 910, 430, 0.6, 190, span(f, a + 12, a + 18), 613);
        stamp(c, "SALE SOON", 540, 560, 74, -0.06, span(f, tr, tr + 8), STAMP, 614);
        const rise = easeIO(span(f, up - 10, up + 6)), y = 1000 - 260 * rise;
        label(c, rise < 0.5 ? "WAS ₹999" : "WAS ₹1,999", 540, y, 92, span(f, a + 8, a + 18), INK, CREAM, -0.03, 615);
        penArrow(c, [820, 1080], [820, 760], span(f, up - 6, up + 6), RED, 10);
      } });
  }
  // 3 · ₹1,999 crossed, ₹999, you won (comic)
  {
    const a = at(2), n1999 = AT(2, "₹1"), cr = AT(2, "CROSSED"), n999 = AT(2, "₹999"), wn = AT(2, "WON");
    S.push({ id: "crossed", from: a - WHIP, punch: [cr, n999, wn], bg: (c) => comicPage(c, 63),
      draw: (c, f) => {
        txt(c, "₹1,999", 540, 520, 150, INK, { sc: back(span(f, n1999 - 2, n1999 + 8)), alpha: span(f, n1999 - 2, n1999 + 2) });
        penStrike(c, 300, 560, 790, 470, span(f, cr, cr + 8), RED, 18);
        hero(c, "₹999", 540, 850, f, n999, KEY, 230);
        burst(c, 540, 1180, 60, 300, 24, 7, span(f, wn, wn + 8), GOLD);
        if (f >= wn) { const k = back(span(f, wn, wn + 10)); c.save(); c.translate(540, 1180); c.scale(k, k); marker(c, [[-110, -120], [110, -120], [80, 10], [24, 40], [24, 90], [80, 110], [-80, 110], [-24, 90], [-24, 40], [-80, 10]], GOLD, { seed: 621, contour: 8 }); c.restore(); }
      } });
  }
  // 4 · it sold for ₹999 all month (newsprint): a price-history chart in the paper
  {
    const a = at(3), mo = AT(3, "MONTH"), any = AT(3, "ANYWAY");
    S.push({ id: "history", from: a - WHIP, punch: [mo, any], bg: (c) => newsPage(c, 93),
      draw: (c, f) => {
        const k = clipping(c, 540, 860, 920, 900, -0.02, 94, span(f, a, a + 12), [0, 360]);
        if (k) { c.save(); c.translate(k.cx, k.cy); c.rotate(k.rot);
          halftoneFill(c, rect(800, 420, 0, -120), (x, y) => (y > -330 + 0 ? 0.08 : 0.08) + (Math.abs(y - (-80)) < 6 ? 0.9 : 0), 10);
          const q = span(f, a + 6, mo + 6), pts: P[] = []; for (let i = 0; i <= 30; i++) pts.push([-380 + i * (760 / 30), -60 + Math.sin(i * 1.3) * 5]);
          brushLine(c, pts, 10, "#1d1a17", q);
          if (f >= any - 10) { const s2 = easeIO(span(f, any - 10, any)); brushLine(c, [[380, -60], [380 + 0.1, -60 - 220 * s2]], 10, KEY, 1); }
          c.restore(); }
        stamp(c, "LAST 30 DAYS", 540, 390, 60, -0.03, span(f, mo - 4, mo + 6), "#1d1a17", 95);
        hero(c, "₹999", 540, 1240, f, any, KEY, 170, -0.03);
      } });
  }
  // 5 · the anchor (toy theatre): the first number drops on stage like an anchor
  {
    const a = at(4), fn = AT(4, "FIRST"), gm = AT(4, "GAME");
    S.push({ id: "anchor", from: a - WHIP, punch: [fn, gm], bg: (c, f) => theatre(c, f, 81, "#3d5a73", "#2b4256"),
      draw: (c, f) => {
        brain(c, 300, 760, 0.95, span(f, a, a + 12), 33);
        const drop = easeOut(span(f, fn - 8, fn + 4)), ay = -300 + 1360 * drop, bounce = f >= fn + 4 && f < fn + 12 ? Math.sin((f - fn - 4) * 0.8) * 14 : 0;
        c.save(); c.strokeStyle = "#e8dcc0"; c.lineWidth = 6; c.beginPath(); c.moveTo(720, 0); c.lineTo(720, ay - 190 + bounce); c.stroke(); c.restore();
        anchor(c, 720, ay + bounce, 0.95);
        if (drop > 0.2) cutout(c, rrect(330, 120, 18, 720, ay - 330 + bounce), "#fbf6ea", 811, 4), txt(c, "₹1,999", 720, ay - 330 + bounce, 70, INK);
        penArrow(c, [600, 1100], [400, 860], span(f, gm - 6, gm + 6), "#ffd166", 10);
      } });
  }
  // 6 · why don't shops get caught (scrapbook): the magnifier finds no real old price
  {
    const a = at(5), cg = AT(5, "CAUGHT"), rl = AT(5, "REAL");
    S.push({ id: "caught", from: a - WHIP, punch: [cg, rl], bg: (c) => scrapPage(c, 325),
      draw: (c, f) => {
        const CD: CardSpec = { cx: 540, cy: 860, w: 820, h: 620, rot: -0.03, color: "#efe5cf", seed: 641, from: [120, 160] };
        card(c, CD, span(f, a, a + 12)); tape(c, 540, 560, 0.02, 200, span(f, a + 10, a + 16), 642);
        onCard(c, CD, span(f, a, a + 12), () => { priceTag(c, -80, 0, 460, 220, -0.04, "₹999", span(f, a + 6, a + 16), 643); txt(c, "WAS ???", 0, 210, 60, STAMP, { alpha: span(f, a + 14, a + 22), rot: -0.04 }); });
        const mx = 300 + 500 * easeIO(span(f, cg - 10, rl + 4)), my = 1080 - 120 * Math.sin(span(f, cg - 10, rl + 4) * Math.PI);
        magnifier(c, mx, my, 1.0, span(f, cg - 14, cg - 4));
        txt(c, "?", mx, my, 130, RED, { stroke: 12, alpha: span(f, rl, rl + 6), sc: back(span(f, rl, rl + 10)) });
      } });
  }
  // 7 · India's new rule (newsprint): January 2027; the lowest price of the last 30 days
  {
    const a = at(6), jn = AT(6, "JANUARY"), lw = AT(6, "LOWEST"), d30 = AT(6, "30"), ev = AT(6, "EVERY");
    S.push({ id: "rule", from: a - WHIP, punch: [jn, lw, d30], bg: (c) => newsPage(c, 97),
      draw: (c, f) => {
        clipping(c, 540, 900, 940, 1040, 0.02, 98, span(f, a, a + 12), [0, -360]);
        stamp(c, "JAN 2027", 540, 470, 120, -0.05, span(f, jn, jn + 8), STAMP, 99);
        calendar(c, 540, 960, 560, 0.03, span(f, d30 - 8, d30 + 6), span(f, lw + 4, lw + 16));
        label(c, "LOWEST ₹", 820, 1250, 58, span(f, ev - 4, ev + 6), INK, GOLD, 0.08, 911);
      } });
  }
  // 8 · Europe: 314 shops, 30% wrong (toy brick): ten shop bricks, three turn red
  {
    const a = at(7), n314 = AT(7, "314"), n30 = AT(7, "30%"), wr = AT(7, "WRONG");
    const greys = ["#F4F4F4"]; void greys;
    S.push({ id: "eu", from: a - WHIP, punch: [n314, n30], dark: true,
      bg: (c) => { const g = c.createRadialGradient(540, 760, 80, 540, 900, 1300); g.addColorStop(0, "#22324a"); g.addColorStop(1, "#101826"); c.fillStyle = g; c.fillRect(0, 0, W, H); },
      draw: (c, f) => {
        const life = span(f, a, at(8)), k = 3.2 * (1 + 0.1 * life), q = new Cam(k, 0, 0).p(7 * STUD, 3 * PLATE, 3 * STUD), cam = new Cam(k, 540 - q[0] + (life - 0.5) * 60, 860 - q[1]);
        const live: { p: Part; dy: number }[] = [];
        for (let i = 0; i < 10; i++) { const land = a + 4 + i * 3; if (f < land - 9) continue; const t = clamp01((f - (land - 9)) / 9), red = [2, 5, 8].includes(i) && f >= n30 + [2, 5, 8].indexOf(i) * 3; live.push({ p: shopBrick((i % 5) * 3, Math.floor(i / 5) * 3.5, red ? "#B40000" : "#F4F4F4"), dy: f < land ? 240 * (1 - easeOut(t)) : 0 }); }
        const base: Part = { id: 999, color: "#646464", kind: "prism", foot: [[-1, -1], [15, -1], [15, 7], [-1, 7]], y0: -1, h: 1, studs: true, step: 0 };
        drawPart(c, cam, base, 0, 0.7);
        order(live, cam).forEach((i) => drawPart(c, cam, live[i].p, live[i].dy, 0.7));
        label(c, "314 SHOPS", 540, 460, 72, span(f, n314 - 2, n314 + 8), INK, "#ffffff", -0.03, 821);
        hero(c, "30%", 540, 1210, f, n30, KEY, 200);
        if (f >= wr) label(c, "DISCOUNTS WRONG", 540, 1370, 50, span(f, wr, wr + 8), "#ffffff", KEY, 0.03, 822);
      } });
  }
  // 9 · the mirage (scrapbook): the real price vs the made-up one
  {
    const a = at(8), mg = AT(8, "MIRAGE"), rl = AT(8, "REAL"), md = AT(8, "MADE");
    const C1: CardSpec = { cx: 300, cy: 840, w: 470, h: 560, rot: 0.03, color: "#efe5cf", seed: 651, from: [-200, 100] }, C2: CardSpec = { cx: 790, cy: 860, w: 470, h: 600, rot: -0.035, color: "#e7d9c0", seed: 652, from: [200, 100] };
    S.push({ id: "mirage", from: a - WHIP, punch: [mg, rl, md], bg: (c) => scrapPage(c, 327),
      draw: (c, f) => {
        ransom(c, "MIRAGE", 540, 330, 108, 661, span(f, mg - 4, mg + 18), 0.1);
        card(c, C1, span(f, a, a + 12)); tape(c, 300, 575, 0.05, 160, span(f, a + 10, a + 16), 653);
        onCard(c, C1, span(f, a, a + 12), () => { txt(c, "REAL", 0, -150, 54, INK, { alpha: span(f, rl, rl + 6) }); txt(c, "₹999", 0, 20, 120, INK); });
        if (f >= rl) penLoop(c, 300, 860, 190, 110, span(f, rl, rl + 12), 654, GOLD, 10);
        card(c, C2, span(f, a + 6, a + 18)); tape(c, 790, 575, -0.05, 160, span(f, a + 16, a + 22), 655);
        onCard(c, C2, span(f, a + 6, a + 18), () => { c.save(); c.globalAlpha = 0.55; c.setLineDash([16, 12]); c.strokeStyle = INK; c.lineWidth = 5; c.strokeRect(-170, -60, 340, 160); c.restore(); txt(c, "₹1,999", 0, 20, 100, INK, { alpha: 0.5 }); });
        stamp(c, "MADE UP", 790, 1060, 86, -0.12, span(f, md, md + 8), STAMP, 656);
      } });
  }
  // 10 · check the price history (comic): a phone; the flat line and the spike before the sale
  {
    const a = at(9), ig = AT(9, "IGNORE"), hs = AT(9, "HISTORY");
    S.push({ id: "phone", from: a - WHIP, punch: [ig, hs], bg: (c) => comicPage(c, 65),
      draw: (c, f) => {
        label(c, "₹1,999", 760, 380, 70, span(f, a, a + 10), INK, CREAM, 0.1, 671); penStrike(c, 640, 400, 880, 350, span(f, ig, ig + 8), RED, 12);
        stamp(c, "IGNORE", 760, 520, 60, 0.1, span(f, ig + 4, ig + 12), STAMP, 672);
        const up = easeOut(span(f, a + 4, a + 18)); phone(c, 420, 1080 + (1 - up) * 700, 1.0, -0.06, span(f, hs - 14, hs + 10), f);
        if (f >= hs + 10) penLoop(c, 430, 1150, 210, 60, span(f, hs + 10, hs + 22), 673, RED, 9);
      } });
  }
  // 11 · always this price (toy theatre): one tag in the spotlight
  {
    const a = at(10), bd = AT(10, "BEST"), al = AT(10, "ALWAYS");
    S.push({ id: "always", from: a - WHIP, punch: [bd, al], bg: (c, f) => theatre(c, f, 83, "#5a4a73", "#3d3256"),
      draw: (c, f) => {
        if (f >= bd) { const g = c.createRadialGradient(540, 980, 30, 540, 980, 520); g.addColorStop(0, `rgba(255,235,160,${0.5 * span(f, bd, bd + 8)})`); g.addColorStop(1, "rgba(255,235,160,0)"); c.fillStyle = g; c.fillRect(0, 0, W, H); }
        const up = easeOut(span(f, a, a + 14)); c.save(); c.translate(0, (1 - up) * 600);
        c.strokeStyle = "#3b2a18"; c.lineWidth = 12; c.beginPath(); c.moveTo(540, 1120); c.lineTo(540, 1700); c.stroke();
        cutout(c, xf([[-250, -110], [250, -110], [250, 110], [-250, 110], [-330, 0]], 560, 980, 0), "#fbf6ea", 851, 8);
        txt(c, "₹999", 580, 985, 150, INK);
        c.restore();
        label(c, "ALWAYS", 760, 780, 64, span(f, al, al + 8), INK, GOLD, 0.1, 852);
      } });
  }
  // 12 · follow (scrapbook)
  {
    const a = at(11), mn = AT(11, "MONEY"), fo = AT(11, "FOLLOW");
    const CD: CardSpec = { cx: 540, cy: 700, w: 760, h: 560, rot: -0.02, color: "#1f1a16", seed: 501, from: [0, -200] };
    S.push({ id: "follow", from: a - WHIP, punch: [fo], bg: (c) => scrapPage(c, 309),
      draw: (c, f) => {
        const cp = span(f, mn - 8, mn + 6); card(c, CD, cp); tape(c, 210, 450, -0.5, 170, span(f, mn + 4, mn + 10), 502); tape(c, 870, 450, 0.5, 170, span(f, mn + 6, mn + 12), 503);
        onCard(c, CD, cp, () => { if (LOGO_IMG) c.drawImage(LOGO_IMG, -320, -200, 640, 400); });
        const press = f >= fo && f < fo + 6 ? 8 : 0, bp = span(f, a + 6, a + 16);
        if (bp > 0) { c.save(); c.translate(540, 1180 + press); c.scale(back(bp), back(bp)); marker(c, rrect(520, 150, 75), "#e0322a", { seed: 504, contour: 8, shadow: "#a8211b" }); txt(c, "FOLLOW", 0, 4, 84, "#ffffff"); c.restore(); }
        if (f >= fo) { const t = span(f, fo, fo + 14); c.save(); c.strokeStyle = `rgba(194,58,42,${1 - t})`; c.lineWidth = 9; c.beginPath(); c.arc(700, 1230, 40 + t * 110, 0, 6.283); c.stroke(); c.restore(); }
        if (f >= fo - 10) { const t = span(f, fo - 10, fo), dx = 820 - 120 * easeOut(t), dy = 1420 - 180 * easeOut(t); marker(c, xf([[0, 0], [26, -10], [40, -110], [64, -112], [62, -20], [110, -14], [120, 70], [30, 90]], dx, dy, -0.35), "#f2c9a0", { seed: 505, contour: 7, shadow: "#d3a274" }); }
      } });
  }
  return S;
})();
((): void => { for (let i = 1; i < SCENES.length; i++) if (SCENES[i].from <= SCENES[i - 1].from + WHIP) throw new Error(`discountMix: scene ${SCENES[i].id} starts too soon`); })();

const camera = (c: Ctx, s: Scene, f: number, next: number) => {
  const life = clamp01((f - s.from) / Math.max(1, next - s.from)); let k = 1 + 0.06 * easeIO(life);
  for (const t of s.punch ?? []) if (f >= t && f < t + 14) k *= 1 + 0.05 * Math.sin(((f - t) / 14) * Math.PI);
  c.translate(540, 820); c.scale(k, k); c.translate(-540, -820);
};
const drawScene = (c: Ctx, s: Scene, f: number, next: number) => { c.save(); camera(c, s, f, next); c.save(); c.translate(540, 820); c.scale(1.1, 1.1); c.translate(-540, -820); s.bg(c, f); c.restore(); s.draw(c, f); c.restore(); };
const hookCard = (c: Ctx, f: number) => {
  scrapPage(c, 333);
  ransom(c, "₹1,999", 540, 620, 160, 17, span(f, 3, 26), 0.1);
  penStrike(c, 230, 650, 850, 590, span(f, 28, 38), RED, 18);
  stamp(c, "FAKE?", 540, 1000, 170, -0.08, span(f, 40, 50), STAMP, 18);
};
const CHUNKS = makeChunks(LINES);
const draw = (ctx: Ctx, f: number, env: Env) => {
  ctx.setTransform(env.scale, 0, 0, env.scale, 0, 0); LOGO_IMG = env.image("logo");
  ctx.fillStyle = "#1e1612"; ctx.fillRect(0, 0, W, H);
  let k = -1; for (let i = 0; i < SCENES.length; i++) if (f >= SCENES[i].from) k = i;
  if (k < 0 || f < HOOK_END + WHIP) {
    const out = span(f, HOOK_END, HOOK_END + WHIP); ctx.save(); ctx.translate(-easeIO(out) * W, 0); ctx.rotate(-0.06 * easeIO(out)); hookCard(ctx, f); ctx.restore();
    if (k >= 0) { ctx.save(); ctx.translate((1 - easeIO(out)) * W, 0); drawScene(ctx, SCENES[0], f, SCENES[1].from); ctx.restore(); }
  } else {
    const s = SCENES[k], next = SCENES[k + 1]?.from ?? DURATION, q = span(f, s.from, s.from + WHIP);
    if (q < 1 && k > 0) {
      const pv = SCENES[k - 1], e = easeIO(q), dir = k % 2 ? 1 : -1;
      ctx.save(); ctx.translate(-dir * e * W * 0.35, 0); drawScene(ctx, pv, s.from - 1, s.from); ctx.fillStyle = `rgba(0,0,0,${0.5 * e})`; ctx.fillRect(0, 0, W, H); ctx.restore();
      ctx.save(); ctx.translate(dir * (1 - e) * W, 0); ctx.rotate(dir * 0.05 * (1 - e)); ctx.shadowColor = "rgba(0,0,0,0.6)"; ctx.shadowBlur = 40; ctx.fillStyle = "#000"; ctx.fillRect(0, 0, W, H); ctx.shadowBlur = 0; drawScene(ctx, s, f, next); ctx.restore();
    } else drawScene(ctx, s, f, next);
  }
  grain(ctx, f, !(SCENES[Math.max(0, k)]?.dark));
  if (f >= HOOK_END) captions(ctx, f, CHUNKS);
};
export const discountMix: Film = {
  meta: { title: "Money Mirage · the was price (mixed media)", W, H, fps: 30, bpm: 60, durationFrames: DURATION, kind: "explainer", raster: "cpu",
    holds: [[Math.floor(sec(LINES[LINES.length - 1].e)), DURATION, "the follow card"]] },
  assets: { images: { logo: "logo_s.png" } },
  shots: [{ id: "build", start: 0, end: DURATION, draw }],
};
void rng; void NAVY; void cutout; void halftoneFill;
