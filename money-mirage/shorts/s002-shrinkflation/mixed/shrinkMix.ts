import { rng, type Ctx, type Env, type P } from "./core";
import type { Film } from "./film";
import { Cam, drawPart, order, PLATE, STUD, type Part } from "./toyBrickKit";
import { LINES } from "./s002timing";
import {
  W, H, sec, span, clamp01, easeOut, easeIO, back, INK, RED, STAMP, GOLD, KEY, CREAM, NAVY, LOGO_URL,
  scrapPage, comicPage, theatre, newsPage, grain, card, onCard, tape, cutout, marker, shade, brushLine,
  penLoop, penStrike, penArrow, stamp, ransom, label, hero, txt, burst, pow, clipping, halftoneFill,
  priceTag, chocBar, brain, eye, gavel, peaks, box, cart, rect, rrect, ellipse, xf, makeChunks, captions, type CardSpec,
} from "./mirageKit";

// MONEY MIRAGE · s002 SHRINKFLATION, MIXED MEDIA. Archival scrapbook pages and marker-comic panels
// carry the story; a toy theatre, a toy-brick table and two newspaper clippings break it up.
// Every mark lands on the word it belongs to (s002timing.ts, from the narration). One pure
// function of the frame.

const at = (li: number, wi = 0, off = 0) => sec(LINES[li].words[Math.min(wi, LINES[li].words.length - 1)].s + off);
const wix = (li: number, w: string) => { const i = LINES[li].words.findIndex((x) => x.t.toUpperCase().replace(/[,.?!:]+$/, "").startsWith(w.toUpperCase())); if (i < 0) throw new Error(`shrinkMix: no word '${w}' in line ${li}`); return i; };
const AT = (li: number, w: string, off = 0) => at(li, wix(li, w), off);
const END_HOLD = 1.6;
export const DURATION = Math.ceil(sec(LINES[LINES.length - 1].e + END_HOLD) / 30) * 30;
const HOOK_END = sec(2.4), WHIP = 10;

type Scene = { id: string; from: number; bg: (c: Ctx, f: number) => void; draw: (c: Ctx, f: number) => void; punch?: number[]; push?: number; dark?: boolean };

// ---------------------------------------------------------------- toy-brick helper (the elasticity table)
type SP = { p: Part; land: number };
let PID = 0;
const bx = (x0: number, z0: number, x1: number, z1: number, y0: number, h: number, color: string, land: number, studs = true): SP => ({ p: { id: PID++, color, kind: "prism", foot: [[x0, z0], [x1, z0], [x1, z1], [x0, z1]], y0, h, studs, step: 0 }, land });
const FALL = 9;
const brickSet = (c: Ctx, parts: SP[], f: number, cam: Cam) => {
  const live: { p: Part; dy: number; a: number }[] = [];
  for (const s of parts) { if (f < s.land - FALL) continue; const t = clamp01((f - (s.land - FALL)) / FALL); live.push({ p: s.p, dy: f < s.land ? 240 * (1 - easeOut(t)) : f === s.land ? -1.5 : 0, a: 0.35 + 0.65 * Math.min(1, t / 0.6) }); }
  c.save(); c.fillStyle = "rgba(0,0,0,0.22)"; for (const l of live) { if (l.p.y0 < 0 || l.dy > 40) continue; const o = l.p.h * PLATE * 0.35, y = Math.max(0, l.p.y0) * PLATE; c.beginPath(); l.p.foot.forEach(([x, z], i) => { const q = cam.p(x * STUD + o, y, z * STUD - o * 0.6); if (i) c.lineTo(q[0], q[1]); else c.moveTo(q[0], q[1]); }); c.closePath(); c.globalAlpha = l.a * 0.6; c.fill(); } c.restore();
  order(live.map((l) => ({ p: l.p, dy: l.dy })), cam).forEach((i) => { const l = live[i]; c.save(); c.globalAlpha = l.a; drawPart(c, cam, l.p, l.dy, 0.7); c.restore(); });
};
const BR = { red: "#B40000", azure: "#68C3E2", dbg: "#646464", lbg: "#969696", white: "#F4F4F4", yellow: "#FAC80A", blue: "#1E5AA8", green: "#237841" };

// ---------------------------------------------------------------- logo image (set from env at draw time)
let LOGO_IMG: CanvasImageSource | undefined;

// ---------------------------------------------------------------- the scenes, in order
const SCENES: Scene[] = (() => {
  const S: Scene[] = [];

  // 1 · hook (comic): the tag that never moved, +12% slammed on a pow, the brain with a red "?"
  {
    const tg = Math.max(HOOK_END + WHIP, AT(0, "TAG")), n12 = AT(0, "12%"), br = AT(0, "BRAIN"), ms = AT(0, "MISS");
    S.push({ id: "hook", from: HOOK_END, punch: [n12, br], bg: (c) => comicPage(c, 41),
      draw: (c, f) => {
        const sway = Math.sin((f - tg) * 0.12) * 0.05 * (1 - span(f, tg, tg + 60));
        priceTag(c, 330, 640, 380, 190, -0.12 + sway, "₹100", span(f, tg, tg + 14), 9);
        burst(c, 700, 330, 120, 330, 28, 5, span(f, n12, n12 + 8));
        pow(c, 700, 330, 250, 150, GOLD, 17, span(f, n12, n12 + 6));
        hero(c, "+12%", 700, 330, f, n12, KEY, 150, -0.06);
        brain(c, 560, 1100, 1.25, span(f, br - 4, br + 10), 31);
        txt(c, "?", 860, 900, 220, RED, { stroke: 18, sc: back(span(f, ms, ms + 10)), alpha: span(f, ms, ms + 4), rot: 0.15 });
      } });
  }
  // 2 · Milka (scrapbook): a torn card, the bar in its wrapper, 100G tag, 90 stamped; a column flies off on "changed"
  {
    const a = at(1), g100 = AT(1, "100"), n90 = AT(1, "90"), wr = AT(1, "WRAPPER"), tiny = AT(2, "TINY"), chg = AT(2, "CHANGED"), shr = AT(2, "SHRINKFLATION");
    const CD: CardSpec = { cx: 540, cy: 760, w: 900, h: 760, rot: -0.025, color: "#f2eadb", seed: 11, from: [-60, 160] };
    S.push({ id: "milka", from: a - WHIP, punch: [n90, chg, shr], bg: (c) => scrapPage(c, 301),
      draw: (c, f) => {
        const cp = span(f, a, a + 12); card(c, CD, cp); tape(c, 150, 400, -0.6, 190, span(f, a + 10, a + 16), 41); tape(c, 935, 400, 0.6, 190, span(f, a + 13, a + 19), 42);
        onCard(c, CD, cp, () => {
          const gone = easeIO(span(f, chg, chg + 18)) * 1.0;
          chocBar(c, 0, -10, 112, 6, 3, -0.04, gone, 13);
          // "same wrapper": a red pen outline traces the unchanged sleeve
          if (f >= wr) { c.save(); c.globalAlpha = 1 - span(f, tiny - 4, tiny + 6); c.strokeStyle = RED; c.setLineDash([22, 16]); c.lineWidth = 7; c.strokeRect(-382, -218, 764, 416); c.restore(); }
        });
        label(c, "100G", 300, 300, 84, span(f, g100 - 2, g100 + 8), INK, CREAM, -0.08, 21);
        penStrike(c, 200, 318, 410, 280, span(f, n90 - 6, n90 + 2));
        stamp(c, "90G", 800, 300, 110, 0.12, span(f, n90, n90 + 8), STAMP, 22);
        penLoop(c, 800, 300, 190, 110, span(f, tiny, tiny + 14), 23);
        stamp(c, "−10%", 540, 1250, 150, -0.05, span(f, shr, shr + 8), STAMP, 24);
      } });
  }
  // 3 · how you shop (toy theatre): a shopper's cart rolls on stage past a shelf of packs
  {
    const a = at(3), sh = AT(3, "SHOP");
    S.push({ id: "theatre", from: a - WHIP, punch: [sh], bg: (c, f) => theatre(c, f, 77),
      draw: (c, f) => {
        // a shelf flat with four packs, cut card on a stick
        const up = easeOut(span(f, a, a + 14));
        c.save(); c.translate(0, (1 - up) * 500);
        cutout(c, rrect(760, 30, 6, 540, 1180), "#8a6a44", 101, 6);
        ["#d9483b", "#f0b43a", "#3d7fc2", "#3f9a5a"].forEach((col, i) => cutout(c, rrect(150, 260, 14, 270 + i * 180, 1040), col, 110 + i, 6));
        ["#f6efe0", "#f6efe0", "#f6efe0", "#f6efe0"].forEach((col, i) => cutout(c, ellipse(270 + i * 180, 1010, 40, 40), col, 120 + i, 2));
        c.restore();
        // the cart on a stick, pushed in from the left on "shop"
        const cx = -300 + 760 * easeOut(span(f, sh - 14, sh + 6)), bob = Math.sin(f * 0.6) * 6;
        c.save(); c.strokeStyle = "#3b2a18"; c.lineWidth = 10; c.beginPath(); c.moveTo(cx, 1380 + bob); c.lineTo(cx - 60, 1720); c.stroke(); c.restore();
        cart(c, cx, 1330 + bob, 0.9, 91);
      } });
  }
  // 4 · elasticity (toy brick): price +1% loses 12 plates of sales; size −1% loses 6
  {
    const a = at(4), rz = AT(4, "RAISE"), d1 = AT(4, "DROP"), n12 = AT(4, "1.2%"), shk = AT(4, "SHRINK"), hf = AT(4, "HALF");
    const parts: SP[] = [bx(-1, -1, 13, 10, -1, 1, BR.dbg, a), bx(0, 0, 12, 2, 0, 3, BR.lbg, a + 3)];
    [BR.red, BR.yellow, BR.blue, BR.green].forEach((col, i) => { parts.push(bx(i * 3, 0, i * 3 + 2, 2, 3, 6, col, a + 8 + i * 4)); parts.push(bx(i * 3, 0, i * 3 + 2, 2, 9, 3, col, a + 10 + i * 4)); });
    for (let k = 0; k < 12; k++) parts.push(bx(2, 6, 4, 8, k, 1, BR.red, d1 + Math.round(k * 1.2), k === 11));
    for (let k = 0; k < 6; k++) parts.push(bx(8, 6, 10, 8, k, 1, BR.azure, hf - 6 + k, k === 5));
    S.push({ id: "brick", from: a - WHIP, punch: [n12, hf], dark: true,
      bg: (c) => { const g = c.createRadialGradient(540, 760, 80, 540, 900, 1300); g.addColorStop(0, "#22324a"); g.addColorStop(1, "#101826"); c.fillStyle = g; c.fillRect(0, 0, W, H); },
      draw: (c, f) => {
        const life = span(f, a, at(5)), k = 3.3 * (1 + 0.12 * life), q = new Cam(k, 0, 0).p(6 * STUD, 4 * PLATE, 4.5 * STUD), cam = new Cam(k, 540 - q[0] + (life - 0.5) * 70, 760 - q[1]);
        brickSet(c, parts, f, cam);
        const L = (x: number, z: number, y = 0) => cam.p(x * STUD, y * PLATE, z * STUD);
        const [ax, ay] = L(3, 9.2), [bxx, byy] = L(9, 9.2);
        label(c, "₹ +1%", ax, ay + 50, 58, span(f, rz, rz + 8), INK, "#ffffff", -0.04, 31);
        label(c, "G −1%", bxx, byy + 50, 58, span(f, shk, shk + 8), INK, "#ffffff", 0.04, 32);
        const cl = (v: number) => Math.max(230, Math.min(850, v));
        const [tx, ty] = L(3, 7, 12); hero(c, "1.2%", cl(tx), Math.max(260, ty - 110), f, n12, KEY, 130);
        const [hx, hy] = L(9, 7, 6); hero(c, "HALF", cl(hx + 40), Math.max(260, hy - 100), f, hf + 2, "#9fdcf2", 104);
      } });
  }
  // 5 · you watch the price, not the grams (comic): a giant eye on the tag in a spotlight; the grams in the dark
  {
    const a = at(5), pr = AT(5, "PRICE"), gr = AT(5, "GRAMS"), nb = AT(5, "NOBODY");
    S.push({ id: "eye", from: a - WHIP + 4, punch: [pr, gr], bg: (c) => comicPage(c, 43, "#f3ecdc"),
      draw: (c, f) => {
        const look: P = f < nb ? [0.6, 0.5] : [0.6 - 1.2 * easeIO(span(f, gr - 4, gr + 6)) * 0, 0.5];
        eye(c, 540, 470, 1.15, look, span(f, a, a + 12), f >= nb && f < nb + 5 ? 0.9 : 0, 51);
        if (f >= pr) { const g = c.createRadialGradient(700, 1080, 30, 700, 1080, 480); g.addColorStop(0, `rgba(255,235,160,${0.55 * span(f, pr, pr + 8)})`); g.addColorStop(1, "rgba(255,235,160,0)"); c.fillStyle = g; c.fillRect(0, 0, W, H); }
        priceTag(c, 700, 1080, 460, 230, 0.06, "₹100", span(f, pr - 2, pr + 10), 52);
        // the grams: a tiny tag in the corner, almost lost
        label(c, "90G", 200, 1330, 34, span(f, gr - 2, gr + 6), INK, "#cfc6b4", -0.2, 53);
        penArrow(c, [330, 1240], [235, 1310], span(f, gr + 2, gr + 12));
        txt(c, "?", 160, 1230, 130, RED, { stroke: 12, alpha: span(f, gr + 6, gr + 12), sc: back(span(f, gr + 6, gr + 16)) });
      } });
  }
  // 6 · brands shrink; per unit +12% (newsprint): a clipping, two boxes in halftone, the headline number
  {
    const a = at(6), bs = AT(6, "SHRINK"), us = AT(6, "US"), dn = AT(6, "DOWNSIZE"), n12 = AT(6, "12%");
    S.push({ id: "news", from: a - WHIP, punch: [dn, n12], bg: (c) => newsPage(c, 91),
      draw: (c, f) => {
        const k = clipping(c, 540, 860, 920, 1060, 0.02, 92, span(f, us - 8, us + 6), [0, 400]);
        // the picture box: two boxes printed in halftone with the orange spot
        if (k) { c.save(); c.translate(k.cx, k.cy); c.rotate(k.rot);
          const pic: P[] = rect(820, 440, 0, -170); c.fillStyle = "#d7cfb8"; c.fillRect(-410, -390, 820, 440);
          const shrinkT = easeIO(span(f, dn, dn + 14)), bh = 300 - 70 * shrinkT;
          halftoneFill(c, pic, (x, y) => { const inA = Math.abs(x + 200) < 95 && y > -40 - 300 + 0 && y < -40 ? 0.85 : 0, inB = Math.abs(x - 200) < 95 && y > -40 - bh && y < -40 ? 0.85 : 0; return Math.max(inA, inB, 0.12 + 0.06 * Math.sin(x * 0.02)); }, 12);
          halftoneFill(c, pic, (x, y) => (Math.abs(x + 200) < 70 && y > -300 && y < -80) || (Math.abs(x - 200) < 70 && y > -40 - bh + 20 && y < -80) ? 0.5 : 0, 12, "rgba(232,106,44,0.85)", Math.PI / 12);
          c.strokeStyle = "#1d1a17"; c.lineWidth = 3; c.strokeRect(-410, -390, 820, 440);
          c.restore(); }
        // the boxes also exist as marker cut-outs before the clipping lands ("brands shrink")
        if (f < us) { const t = easeIO(span(f, bs - 6, bs + 10)); box(c, 360, 900, 250, 380, "#e8a33a", 81); box(c, 720, 900 + 60 * t, 250, 380 - 120 * t, "#e8a33a", 82); }
        stamp(c, "US STORES", 540, 360, 64, -0.03, span(f, us, us + 8), "#1d1a17", 93);
        hero(c, "+12%", 540, 1210, f, n12, KEY, 190, -0.03);
        if (f >= n12 + 6) label(c, "PER UNIT", 540, 1360, 56, span(f, n12 + 6, n12 + 14), INK, GOLD, 0.03, 94);
      } });
  }
  // 7 · Toblerone 2016 (comic): a peaks bar; every other peak lifts away on "widened"; same price
  {
    const a = at(7), y16 = AT(7, "2016"), wd = AT(7, "WIDENED"), fw = AT(7, "FEWER"), sm = AT(7, "SAME");
    S.push({ id: "peaks", from: a - WHIP, punch: [wd, fw], bg: (c) => comicPage(c, 47),
      draw: (c, f) => {
        const up = easeOut(span(f, a, a + 12));
        c.save(); c.translate(0, (1 - up) * 300); peaks(c, 540, 820, 108, 230, 8, (i) => (i % 2 === 1 ? easeIO(span(f, wd + (i >> 1) * 3, wd + (i >> 1) * 3 + 14)) : 0), 71); c.restore();
        stamp(c, "2016", 250, 420, 110, -0.1, span(f, y16, y16 + 8), NAVY, 72);
        if (f >= wd) { [1, 3, 5, 7].forEach((i, k) => { const x = 540 - 432 + 108 * (i + 0.5); penArrow(c, [x, 720], [x, 600], span(f, wd + k * 3 + 6, wd + k * 3 + 14), RED, 7); }); }
        priceTag(c, 690, 1210, 380, 190, 0.08, "₹100", span(f, sm - 6, sm + 6), 73);
        label(c, "SAME", 900, 1080, 60, span(f, sm, sm + 8), INK, GOLD, 0.12, 74);
      } });
  }
  // 8 · the court (newsprint): a clipping, the gavel comes down on "misled"
  {
    const a = at(8), my = AT(8, "MAY"), ct = AT(8, "COURT"), ms = AT(8, "MISLED");
    S.push({ id: "court", from: a - WHIP, punch: [ct, ms], bg: (c) => newsPage(c, 95),
      draw: (c, f) => {
        const k = clipping(c, 540, 820, 900, 820, -0.03, 96, span(f, a, a + 12), [0, -300]);
        if (k) { c.save(); c.translate(k.cx, k.cy); c.rotate(k.rot); halftoneFill(c, rect(380, 300, -210, -110), (x, y) => 0.25 + 0.5 * Math.max(0, 1 - Math.hypot(x + 210, y + 110) / 190), 10); c.restore(); }
        stamp(c, "MAY", 300, 470, 70, -0.08, span(f, my, my + 8), "#1d1a17", 97);
        const sw = f < ms ? -0.9 * easeOut(span(f, ct, ct + 10)) : -0.9 + 0.9 * easeIO(span(f, ms - 4, ms)), hit = f >= ms && f < ms + 6;
        gavel(c, 660 + (hit ? (rng(f)() - 0.5) * 10 : 0), 980, 1.05, sw, 61);
        if (f >= ms) burst(c, 330, 1010, 70, 260, 22, 98, span(f, ms, ms + 6));
        stamp(c, "MISLED", 540, 1300, 150, -0.06, span(f, ms, ms + 6), STAMP, 99);
      } });
  }
  // 9 · the mirage (scrapbook): the tag never changes; the rise is inside the pack
  {
    const a = at(9), mg = AT(9, "MIRAGE"), tg = AT(9, "TAG"), ins = AT(9, "INSIDE");
    const C1: CardSpec = { cx: 300, cy: 760, w: 470, h: 560, rot: 0.03, color: "#efe5cf", seed: 201, from: [-200, 100] }, C2: CardSpec = { cx: 790, cy: 820, w: 470, h: 680, rot: -0.035, color: "#e7d9c0", seed: 202, from: [200, 100] };
    S.push({ id: "mirage", from: a - WHIP, punch: [mg, tg, ins], bg: (c) => scrapPage(c, 305),
      draw: (c, f) => {
        ransom(c, "MIRAGE", 540, 300, 108, 211, span(f, mg - 4, mg + 18), 0.1);
        card(c, C1, span(f, a, a + 12)); tape(c, 300, 495, 0.05, 160, span(f, a + 10, a + 16), 212);
        onCard(c, C1, span(f, a, a + 12), () => priceTag(c, 20, 0, 340, 170, -0.05, "₹100", span(f, a + 8, a + 18), 213));
        if (f >= tg) penLoop(c, 310, 760, 220, 130, span(f, tg, tg + 12), 214, GOLD, 10);
        card(c, C2, span(f, a + 6, a + 18)); tape(c, 790, 495, -0.05, 160, span(f, a + 16, a + 22), 215);
        onCard(c, C2, span(f, a + 6, a + 18), () => { const t = easeIO(span(f, ins, ins + 14)); box(c, 0, 40 + 50 * t, 260, 400 - 100 * t, "#e8a33a", 216); });
        if (f >= ins) { const g = c.createRadialGradient(790, 860, 10, 790, 860, 360); g.addColorStop(0, `rgba(255,80,60,${0.5 * span(f, ins, ins + 8)})`); g.addColorStop(1, "rgba(255,80,60,0)"); c.fillStyle = g; c.fillRect(0, 0, W, H); }
        hero(c, "+12%", 790, 1260, f, ins + 2, KEY, 170, 0.04);
      } });
  }
  // 10 · check the price per kilo (toy theatre): the shelf label on stage, red loop on "kilo"
  {
    const a = at(10), sk = AT(10, "SKIP"), pr = AT(10, "PRICE"), kg = AT(10, "KILO");
    S.push({ id: "kilo", from: a - WHIP, punch: [sk, kg], bg: (c, f) => theatre(c, f, 79, "#5a4a73", "#3d3256"),
      draw: (c, f) => {
        const up = easeOut(span(f, a, a + 14)); c.save(); c.translate(0, (1 - up) * 600);
        cutout(c, rrect(800, 520, 24, 540, 1000), "#fbf6ea", 301, 8);
        txt(c, "CHOCOLATE · 90G", 540, 820, 46, INK);
        txt(c, "₹100", 540, 960, 190, INK);
        if (f >= sk) penStrike(c, 330, 990, 750, 930, span(f, sk, sk + 8), RED, 14);
        txt(c, "₹1,111 / KG", 540, 1150, 76, KEY, { alpha: span(f, pr - 4, pr + 4) });
        c.restore();
        penLoop(c, 540, 1150, 300, 76, span(f, kg, kg + 12), 302, RED, 11);
      } });
  }
  // 11 · the same tag, twice (comic)
  {
    const a = at(11), ex = AT(11, "EXACTLY"), sm = AT(11, "SAME");
    S.push({ id: "twins", from: a - WHIP, punch: [ex, sm], bg: (c) => comicPage(c, 49),
      draw: (c, f) => {
        priceTag(c, 300, 760, 340, 170, -0.08, "₹100", span(f, a + 2, a + 14), 401); priceTag(c, 790, 760, 340, 170, 0.08, "₹100", span(f, a + 8, a + 20), 402);
        txt(c, "=", 545, 560, 200, GOLD, { stroke: 18, sc: back(span(f, ex, ex + 10)) });
        label(c, "100G", 300, 1010, 64, span(f, ex + 4, ex + 12), INK, "#ffffff", -0.05, 403); label(c, "90G", 790, 1010, 64, span(f, sm, sm + 8), "#ffffff", KEY, 0.05, 404);
        if (f >= sm) penLoop(c, 790, 1010, 150, 70, span(f, sm + 4, sm + 16), 405);
      } });
  }
  // 12 · follow (scrapbook): the logo on a taped card, a red FOLLOW button pressed on "Follow"
  {
    const a = at(12), mn = AT(12, "MONEY"), fo = AT(12, "FOLLOW");
    const CD: CardSpec = { cx: 540, cy: 700, w: 760, h: 560, rot: -0.02, color: "#1f1a16", seed: 501, from: [0, -200] };
    S.push({ id: "follow", from: a - WHIP, punch: [fo], bg: (c) => scrapPage(c, 309),
      draw: (c, f) => {
        const cp = span(f, mn - 8, mn + 6); card(c, CD, cp); tape(c, 210, 450, -0.5, 170, span(f, mn + 4, mn + 10), 502); tape(c, 870, 450, 0.5, 170, span(f, mn + 6, mn + 12), 503);
        onCard(c, CD, cp, () => { if (LOGO_IMG) { const iw = 640, ih = 400; c.drawImage(LOGO_IMG, -iw / 2, -ih / 2, iw, ih); } });
        const press = f >= fo && f < fo + 6 ? 8 : 0, bp = span(f, a + 6, a + 16);
        if (bp > 0) { c.save(); c.translate(540, 1180 + press); c.scale(back(bp), back(bp)); marker(c, rrect(520, 150, 75), "#e0322a", { seed: 504, contour: 8, shadow: "#a8211b" }); txt(c, "FOLLOW", 0, 4, 84, "#ffffff"); c.restore(); }
        if (f >= fo) { const t = span(f, fo, fo + 14); c.save(); c.strokeStyle = `rgba(194,58,42,${1 - t})`; c.lineWidth = 9; c.beginPath(); c.arc(700, 1230, 40 + t * 110, 0, 6.283); c.stroke(); c.restore(); }
        // the tapping finger: a marker-comic hand point
        if (f >= fo - 10) { const t = span(f, fo - 10, fo), dx = 820 - 120 * easeOut(t), dy = 1420 - 180 * easeOut(t); marker(c, xf([[0, 0], [26, -10], [40, -110], [64, -112], [62, -20], [110, -14], [120, 70], [30, 90]], dx, dy, -0.35), "#f2c9a0", { seed: 505, contour: 7, shadow: "#d3a274" }); }
      } });
  }
  return S;
})();
((): void => { for (let i = 1; i < SCENES.length; i++) if (SCENES[i].from <= SCENES[i - 1].from + WHIP) throw new Error(`shrinkMix: scene ${SCENES[i].id} starts too soon`); })();

// ---------------------------------------------------------------- camera: a slow push per scene, a punch on each beat
const camera = (c: Ctx, s: Scene, f: number, next: number) => {
  const life = clamp01((f - s.from) / Math.max(1, next - s.from)); let k = 1 + (s.push ?? 0.06) * easeIO(life);
  for (const t of s.punch ?? []) if (f >= t && f < t + 14) k *= 1 + 0.05 * Math.sin(((f - t) / 14) * Math.PI);
  c.translate(540, 820); c.scale(k, k); c.translate(-540, -820);
};
const drawScene = (c: Ctx, s: Scene, f: number, next: number) => { c.save(); camera(c, s, f, next); c.save(); c.translate(540, 820); c.scale(1.1, 1.1); c.translate(-540, -820); s.bg(c, f); c.restore(); s.draw(c, f); c.restore(); };

// the hook card: ransom tiles pasted fast on a scrapbook page, in words the narrator does not say
const hookCard = (c: Ctx, f: number) => {
  scrapPage(c, 333);
  ransom(c, "₹100", 540, 560, 170, 7, span(f, 3, 22), 0.12);
  stamp(c, "=", 540, 800, 150, 0, span(f, 22, 30), STAMP, 8);
  ransom(c, "₹112?", 540, 1040, 180, 9, span(f, 30, 58), 0.1);
  penLoop(c, 540, 1040, 330, 150, span(f, 56, 72), 10, RED, 12);
};

const CHUNKS = makeChunks(LINES);
const draw = (ctx: Ctx, f: number, env: Env) => {
  ctx.setTransform(env.scale, 0, 0, env.scale, 0, 0); LOGO_IMG = env.image("logo");
  ctx.fillStyle = "#1e1612"; ctx.fillRect(0, 0, W, H);
  let k = -1; for (let i = 0; i < SCENES.length; i++) if (f >= SCENES[i].from) k = i;
  if (k < 0 || f < HOOK_END + WHIP) {   // hook card, then slid away like a page turned
    const out = span(f, HOOK_END, HOOK_END + WHIP); ctx.save(); ctx.translate(-easeIO(out) * W, 0); ctx.rotate(-0.06 * easeIO(out)); hookCard(ctx, f); ctx.restore();
    if (k >= 0) { ctx.save(); ctx.translate((1 - easeIO(out)) * W, 0); drawScene(ctx, SCENES[0], f, SCENES[1].from); ctx.restore(); }
  } else {
    const s = SCENES[k], next = SCENES[k + 1]?.from ?? DURATION, q = span(f, s.from, s.from + WHIP);
    if (q < 1 && k > 0) {   // the new page slides over the old, which is pushed aside and darkened
      const pv = SCENES[k - 1], e = easeIO(q), dir = k % 2 ? 1 : -1;
      ctx.save(); ctx.translate(-dir * e * W * 0.35, 0); drawScene(ctx, pv, s.from - 1, s.from); ctx.fillStyle = `rgba(0,0,0,${0.5 * e})`; ctx.fillRect(0, 0, W, H); ctx.restore();
      ctx.save(); ctx.translate(dir * (1 - e) * W, 0); ctx.rotate(dir * 0.05 * (1 - e)); ctx.shadowColor = "rgba(0,0,0,0.6)"; ctx.shadowBlur = 40; ctx.fillStyle = "#000"; ctx.fillRect(0, 0, W, H); ctx.shadowBlur = 0; drawScene(ctx, s, f, next); ctx.restore();
    } else drawScene(ctx, s, f, next);
  }
  grain(ctx, f, !(SCENES[Math.max(0, k)]?.dark));
  if (f >= HOOK_END) captions(ctx, f, CHUNKS);
};

export const shrinkMix: Film = {
  meta: { title: "Money Mirage · shrinkflation (mixed media)", W, H, fps: 30, bpm: 60, durationFrames: DURATION, kind: "explainer", raster: "cpu",
    holds: [[Math.floor(sec(LINES[LINES.length - 1].e)), DURATION, "the follow card"]] },
  assets: { images: { logo: "logo_s.png" } },
  shots: [{ id: "build", start: 0, end: DURATION, draw }],
};
void ellipse; void brushLine; void shade; void penArrow;

export const setLogo = (img: CanvasImageSource | undefined) => { LOGO_IMG = img; };
