import { type Ctx } from "./core";
import { Cam, drawPart, order, PLATE, STUD, type Part } from "./toyBrickKit";
import { LINES } from "./s009timing";
import {
  span, clamp01, easeOut, easeIO, back, INK, RED, STAMP, GOLD, KEY, CREAM, NAVY,
  scrapPage, comicPage, theatre, newsPage, card, onCard, tape, cutout, marker,
  penLoop, penStrike, penArrow, stamp, ransom, label, hero, txt, burst, pow, clipping,
  rrect, rect, ellipse, makeFilm, followScene, timing, brickBg, person, lineChart, WHIP, HOOK_END, type Scene, type CardSpec,
} from "./mirageKit";

// MONEY MIRAGE · s009 ZIMBABWE'S $100 TRILLION NOTE, mixed media. The note is a generic drawn
// banknote (no reproduction of the real design).
const { at, AT } = timing(LINES, "zimMix");

/** a generic banknote reading `val` */
export const note = (c: Ctx, x: number, y: number, s: number, rot: number, val: string, p: number, seed: number, col = "#c9a86a") => {
  if (p <= 0) return; const k = back(p); c.save(); c.translate(x, y); c.rotate(rot); c.scale(k * s, k * s);
  marker(c, rect(560, 270), col, { seed, contour: 6, shadow: "#a3864f", streak: true });
  c.strokeStyle = "rgba(60,40,20,0.6)"; c.lineWidth = 3; c.strokeRect(-260, -115, 520, 230);
  marker(c, ellipse(-160, 0, 70, 70), "#e8d9b0", { seed: seed + 1, contour: 4, streak: false, hi: false });
  txt(c, val, 70, -20, val.length > 8 ? 30 : 60, "#3a2a14"); txt(c, "DOLLARS", 70, 40, 30, "#3a2a14");
  c.restore();
};
let PID = 0;
const bk = (x: number, y0: number, color: string): Part => ({ id: PID++, color, kind: "prism", foot: [[x, 0], [x + 2, 0], [x + 2, 2], [x, 2]], y0, h: 3, studs: true, step: 0 });

const S: Scene[] = [];
{ const a = HOOK_END, tr = AT(0, "TRILLION"), n30 = AT(0, "$30");
  S.push({ id: "hook", from: a, punch: [tr, n30], bg: (c) => scrapPage(c, 391), draw: (c, f) => {
    note(c, 540, 820, 1.6, -0.05, "100,000,000,000,000", span(f, a, a + 12), 1501);
    if (f >= tr) penLoop(c, 650, 790, 380, 90, span(f, tr, tr + 12), 1502, RED, 10);
    hero(c, "≈ $30", 540, 1280, f, n30, KEY, 190, -0.04); } }); }
{ const a = at(1), nv = AT(1, "NOVEMBER"), n98 = AT(1, "98%");
  S.push({ id: "daily", from: a - WHIP, punch: [nv, n98], bg: (c) => newsPage(c, 151), draw: (c, f) => {
    clipping(c, 540, 880, 920, 980, -0.02, 152, span(f, a, a + 12), [0, 360]);
    stamp(c, "NOV 2008", 540, 450, 90, -0.04, span(f, nv, nv + 8), "#1d1a17", 153);
    hero(c, "+98%", 540, 860, f, n98, KEY, 200, -0.03); label(c, "EVERY DAY", 540, 1060, 64, span(f, n98 + 6, n98 + 14), INK, GOLD, 0.03, 154); } }); }
{ const a = at(2), dbl = AT(2, "DOUBLED"), n25 = AT(2, "25"), bn = AT(2, "79.6");
  S.push({ id: "curve", from: a - WHIP, punch: [dbl, bn], bg: (c) => comicPage(c, 121), draw: (c, f) => {
    const v: number[] = []; for (let i = 0; i < 12; i++) v.push(Math.min(1, 0.02 * Math.pow(1.45, i))); lineChart(c, 540, 620, 760, 520, v, span(f, a, bn), KEY, 14);
    label(c, "×2 EVERY 25 HRS", 540, 1000, 60, span(f, n25, n25 + 8), INK, CREAM, -0.03, 1511);
    burst(c, 540, 1240, 120, 320, 28, 1512, span(f, bn, bn + 8), GOLD); hero(c, "79.6 BILLION %", 540, 1240, f, bn, KEY, 96, -0.03); } }); }
{ const a = at(3), zr = AT(3, "ZEROS"), n25 = AT(3, "25");
  S.push({ id: "zeros", from: a - WHIP, punch: [zr, n25], bg: (c) => scrapPage(c, 393), draw: (c, f) => {
    const CD: CardSpec = { cx: 540, cy: 760, w: 940, h: 380, rot: 0.02, color: "#f2eadb", seed: 1521, from: [0, 200] };
    card(c, CD, span(f, a, a + 12)); tape(c, 540, 580, 0, 200, span(f, a + 10, a + 16), 1522);
    const zs = "000000000000000000000000"; onCard(c, CD, span(f, a, a + 12), () => { const shown = Math.max(0, 24 - Math.floor(24 * easeIO(span(f, zr, n25 + 6)))); txt(c, "1" + zs.slice(0, shown), 0, 0, shown > 12 ? 40 : 70, INK); });
    for (let i = 0; i < 3; i++) stamp(c, ["−3", "−10", "−12"][i], 240 + i * 300, 1100, 90, (i - 1) * 0.08, span(f, zr + i * 8, zr + i * 8 + 8), STAMP, 1523 + i);
    hero(c, "25 ZEROS", 540, 1340, f, n25, KEY, 140, -0.03); } }); }
{ const a = at(4), ap = AT(4, "APRIL"), us = AT(4, "US");
  S.push({ id: "giveup", from: a - WHIP, punch: [ap, us], bg: (c, f) => theatre(c, f, 101, "#3f5a4a", "#2a3e33"), draw: (c, f) => {
    const up = easeOut(span(f, a, a + 14)); c.save(); c.translate(0, (1 - up) * 500);
    note(c, 540, 820, 1.0, -0.06, "Z$", 1, 1531); c.restore();
    stamp(c, "APRIL 2009", 540, 460, 90, -0.05, span(f, ap, ap + 8), STAMP, 1532);
    if (f >= us) { penStrike(c, 270, 870, 820, 760, span(f, us - 4, us + 4), RED, 18); note(c, 540, 1250, 0.9, 0.05, "US $", span(f, us, us + 10), 1533, "#9bbf8a"); } } }); }
{ const a = at(5), y15 = AT(5, "2015"), q35 = AT(5, "35");
  S.push({ id: "swap", from: a - WHIP, punch: [y15, q35], bg: (c) => newsPage(c, 155), draw: (c, f) => {
    clipping(c, 540, 860, 920, 980, 0.02, 156, span(f, a, a + 12), [0, -360]);
    stamp(c, "2015", 540, 450, 100, -0.05, span(f, y15, y15 + 8), "#1d1a17", 157);
    hero(c, "$1", 300, 860, f, q35 - 10, "#2f6f4f", 170); txt(c, "=", 540, 860, 130, INK, { alpha: span(f, q35 - 4, q35) });
    label(c, "35 QUADRILLION Z$", 540, 1100, 58, span(f, q35, q35 + 8), "#ffffff", KEY, 0.03, 158); } }); }
{ const a = at(6), n40 = AT(6, "40");
  S.push({ id: "cents", from: a - WHIP, punch: [n40], bg: (c) => comicPage(c, 123), draw: (c, f) => {
    note(c, 540, 700, 1.2, -0.05, "100,000,000,000,000", span(f, a, a + 10), 1541);
    hero(c, "40¢", 540, 1150, f, n40, KEY, 230, -0.04); } }); }
{ const a = at(7), tw = AT(7, "TWIST"), n100 = AT(7, "$100");
  S.push({ id: "collect", from: a - WHIP, punch: [tw, n100], dark: true, bg: brickBg, draw: (c, f) => {
    const k = 3.0, q = new Cam(k, 0, 0).p(4 * STUD, 8 * PLATE, 1 * STUD), cam = new Cam(k, 540 - q[0], 1060 - q[1]);
    drawPart(c, cam, { id: 998, color: "#646464", kind: "prism", foot: [[-1, -1], [10, -1], [10, 3], [-1, 3]], y0: -1, h: 1, studs: true, step: 0 }, 0, 0.7);
    const live: { p: Part; dy: number }[] = []; for (let n = 0; n < 6; n++) { const land = a + 4 + n * 4; if (f < land - 9) continue; const t = clamp01((f - (land - 9)) / 9); live.push({ p: bk(3, n * 3, "#FAC80A"), dy: f < land ? 240 * (1 - easeOut(t)) : 0 }); }
    order(live, cam).forEach((i) => drawPart(c, cam, live[i].p, live[i].dy, 0.7));
    stamp(c, "COLLECTORS", 540, 380, 80, -0.04, span(f, tw, tw + 8), "#ff6b5a", 1551); hero(c, "~$100", 540, 1330, f, n100, "#FAC80A", 170); } }); }
{ const a = at(8), mg = AT(8, "MIRAGE"), tr = AT(8, "TRUST");
  S.push({ id: "mirage", from: a - WHIP, punch: [mg, tr], bg: (c) => scrapPage(c, 395), draw: (c, f) => {
    ransom(c, "MIRAGE", 540, 330, 108, 1561, span(f, mg - 4, mg + 18), 0.1);
    note(c, 540, 800, 1.2, -0.04, "100,000,000,000,000", span(f, a, a + 12), 1562);
    stamp(c, "NOT WEALTH", 540, 1060, 90, -0.06, span(f, mg + 20, mg + 28), STAMP, 1563);
    label(c, "TRUST", 540, 1300, 90, span(f, tr, tr + 8), INK, GOLD, 0.03, 1564); } }); }
S.push(followScene(at(9), AT(9, "MONEY"), AT(9, "FOLLOW")));
const hookCard = (c: Ctx, f: number) => { scrapPage(c, 397); ransom(c, "RICH?", 540, 620, 190, 1571, span(f, 3, 24), 0.1); stamp(c, "$100,000,000,000,000", 540, 980, 62, -0.06, span(f, 30, 42), STAMP, 1572); };
export const zimMix = makeFilm({ title: "Money Mirage · the $100 trillion note (mixed media)", LINES, scenes: S, hookCard, name: "zimMix" });
void cutout; void penArrow; void person; void pow; void NAVY; void rrect;
