import { type Ctx } from "./core";
import { Cam, drawPart, order, PLATE, STUD, type Part } from "./toyBrickKit";
import { LINES } from "./s008timing";
import {
  span, clamp01, easeOut, easeIO, back, INK, RED, STAMP, GOLD, KEY, CREAM, NAVY,
  scrapPage, comicPage, theatre, newsPage, card, onCard, tape, cutout, marker,
  penLoop, penStrike, penArrow, stamp, ransom, label, hero, txt, burst, pow, clipping, halftoneFill,
  rrect, rect, ellipse, makeFilm, followScene, timing, brickBg, person, WHIP, HOOK_END, type Scene, type CardSpec,
} from "./mirageKit";

// MONEY MIRAGE · s008 CHARLES PONZI, 1920, mixed media. Ponzi is drawn as a generic straw-hat
// figure, not a likeness.
const { at, AT } = timing(LINES, "ponziMix");

/** a 1920s gent: person + straw boater + cane */
export const gent = (c: Ctx, x: number, y: number, s: number, seed: number) => {
  person(c, x, y, s, "#3a3f55", seed);
  c.save(); c.translate(x, y); c.scale(s, s); marker(c, rrect(170, 26, 10, 0, -82), "#e8cf8a", { seed: seed + 5, contour: 6, streak: false }); marker(c, rrect(110, 46, 12, 0, -108), "#e8cf8a", { seed: seed + 6, contour: 6, streak: false }); c.fillStyle = "#7a2e2e"; c.fillRect(-55, -98, 110, 12); c.restore();
};
/** a postal reply coupon (engraved-looking card) */
const coupon = (c: Ctx, x: number, y: number, s: number, rot: number, p: number, seed: number) => {
  if (p <= 0) return; const k = back(p); c.save(); c.translate(x, y); c.rotate(rot); c.scale(k * s, k * s);
  marker(c, rect(300, 190), "#e9e2c6", { seed, contour: 5, shadow: "#cfc6a2", streak: false });
  c.strokeStyle = "#5a6e4a"; c.lineWidth = 3; c.strokeRect(-135, -80, 270, 160); c.strokeRect(-125, -70, 250, 140);
  txt(c, "REPLY COUPON", 0, -40, 26, "#3e4f33"); txt(c, "UNION POSTALE", 0, 0, 20, "#3e4f33"); marker(c, ellipse(90, 45, 26, 26), "#c96f4a", { seed: seed + 1, contour: 3, streak: false, hi: false });
  c.restore();
};
let PID = 0;
const bk = (x: number, z: number, y0: number, color: string): Part => ({ id: PID++, color, kind: "prism", foot: [[x, z], [x + 2, z], [x + 2, z + 2], [x, z + 2]], y0, h: 3, studs: true, step: 0 });

const S: Scene[] = [];
{ const a = HOOK_END, n50 = AT(0, "50%"), n45 = AT(0, "45");
  S.push({ id: "hook", from: a, punch: [n50, n45], bg: (c) => comicPage(c, 111), draw: (c, f) => {
    gent(c, 300, 1180, 1.3, 1401);
    burst(c, 690, 520, 150, 360, 28, 1402, span(f, n50, n50 + 8), GOLD); pow(c, 690, 520, 280, 180, GOLD, 1403, span(f, n50, n50 + 6)); hero(c, "+50%", 690, 520, f, n50, KEY, 140, -0.05);
    stamp(c, "45 DAYS", 700, 860, 100, 0.06, span(f, n45, n45 + 8), NAVY, 1404);
    stamp(c, "1920", 260, 380, 90, -0.1, span(f, a + 4, a + 12), "#1d1a17", 1405); } }); }
{ const a = at(1), nm = AT(1, "PONZI"), cp = AT(1, "COUPONS");
  const CD: CardSpec = { cx: 540, cy: 860, w: 820, h: 680, rot: -0.025, color: "#f2eadb", seed: 1411, from: [-120, 200] };
  S.push({ id: "name", from: a - WHIP, punch: [nm, cp], bg: (c) => scrapPage(c, 381), draw: (c, f) => {
    card(c, CD, span(f, a, a + 12)); tape(c, 170, 540, -0.6, 180, span(f, a + 10, a + 16), 1412); tape(c, 910, 540, 0.6, 180, span(f, a + 12, a + 18), 1413);
    onCard(c, CD, span(f, a, a + 12), () => gent(c, -200, 60, 0.9, 1414));
    ransom(c, "PONZI", 540, 360, 120, 1415, span(f, nm - 4, nm + 16), 0.1);
    coupon(c, 720, 860, 1.1, 0.06, span(f, cp - 4, cp + 8), 1416); } }); }
{ const a = at(2), eu = AT(2, "EUROPE"), am = AT(2, "AMERICA"), pp = AT(2, "PAPER");
  S.push({ id: "arb", from: a - WHIP, punch: [eu, am, pp], bg: (c) => newsPage(c, 141), draw: (c, f) => {
    clipping(c, 540, 860, 940, 900, 0.02, 142, span(f, a, a + 12), [0, 360]);
    coupon(c, 280, 760, 0.9, -0.06, span(f, eu - 4, eu + 8), 1421); label(c, "EUROPE: CHEAP", 280, 940, 48, span(f, eu, eu + 8), INK, CREAM, -0.04, 1422);
    coupon(c, 800, 760, 0.9, 0.06, span(f, am - 4, am + 8), 1423); label(c, "U.S.: MORE", 800, 940, 48, span(f, am, am + 8), INK, GOLD, 0.04, 1424);
    penArrow(c, [420, 700], [660, 700], span(f, am - 2, am + 8), RED, 10);
    stamp(c, "ON PAPER", 540, 1240, 100, -0.05, span(f, pp, pp + 8), STAMP, 1425); } }); }
{ const a = at(3), sc = AT(3, "SCALE"), nw = AT(3, "NEW");
  S.push({ id: "loop", from: a - WHIP, punch: [sc, nw], bg: (c, f) => theatre(c, f, 97), draw: (c, f) => {
    const t = f * 0.05; ["#d9483b", "#f0b43a", "#3d7fc2", "#3f9a5a", "#8a5ab8"].forEach((cl, i) => { const ang = t + i * 1.256, x = 540 + Math.cos(ang) * 300, y = 1000 + Math.sin(ang) * 220; person(c, x, y, 0.55, cl, 1431 + i); });
    gent(c, 540, 1000, 0.9, 1436);
    if (f >= nw) for (let i = 0; i < 4; i++) { const q = span(f, nw + i * 5, nw + i * 5 + 14); if (q > 0 && q < 1) { const ang = t + i * 1.256 + 0.6, x = 540 + Math.cos(ang) * 300 * (1 - q), y = 1000 + Math.sin(ang) * 220 * (1 - q); marker(c, ellipse(x, y, 34, 34), GOLD, { seed: 1437 + i, contour: 4, streak: false }); } }
    stamp(c, "NEW MONEY PAYS OLD", 540, 440, 62, -0.04, span(f, nw, nw + 8), STAMP, 1438);
    if (f >= sc) label(c, "CAN'T SCALE", 540, 1380, 56, span(f, sc, sc + 8), INK, GOLD, 0.03, 1439); } }); }
{ const a = at(4), th = AT(4, "THOUSANDS"), n15 = AT(4, "$15"), mo = AT(4, "EIGHT");
  S.push({ id: "money", from: a - WHIP, punch: [n15, mo], dark: true, bg: brickBg, draw: (c, f) => {
    const life = span(f, a, at(5)), k = 2.8 * (1 + 0.1 * life), q = new Cam(k, 0, 0).p(4 * STUD, 14 * PLATE, 3 * STUD), cam = new Cam(k, 540 - q[0], 1000 - q[1]);
    drawPart(c, cam, { id: 997, color: "#646464", kind: "prism", foot: [[-1, -1], [9, -1], [9, 7], [-1, 7]], y0: -1, h: 1, studs: true, step: 0 }, 0, 0.7);
    const live: { p: Part; dy: number }[] = []; for (let n = 0; n < 30; n++) { const land = th + n * 2; if (f < land - 9) continue; const tt = clamp01((f - (land - 9)) / 9); live.push({ p: bk((n % 3) * 3, Math.floor(n / 3) % 2 ? 3 : 0, Math.floor(n / 6) * 3, "#237841"), dy: f < land ? 260 * (1 - easeOut(tt)) : 0 }); }
    order(live, cam).forEach((i) => drawPart(c, cam, live[i].p, live[i].dy, 0.7));
    hero(c, "~$15 MILLION", 540, 330, f, n15, "#FAC80A", 110); label(c, "8 MONTHS", 540, 1290, 60, span(f, mo, mo + 8), INK, "#ffffff", 0.03, 1441); } }); }
{ const a = at(5), bp = AT(5, "POST"), dg = AT(5, "DIGGING"), au = AT(5, "AUGUST");
  S.push({ id: "post", from: a - WHIP, punch: [bp, au], bg: (c) => newsPage(c, 143), draw: (c, f) => {
    const kk = clipping(c, 540, 860, 940, 1080, -0.02, 144, span(f, a, a + 12), [0, -360]);
    if (kk) { c.save(); c.translate(kk.cx, kk.cy); c.rotate(kk.rot); txt(c, "THE BOSTON POST", 0, -440, 54, "#1d1a17"); halftoneFill(c, rect(380, 300, -190, -160), (x, y) => 0.3 + 0.4 * Math.max(0, 1 - Math.hypot(x + 190, y + 160) / 180), 10); c.restore(); }
    if (f >= dg) penLoop(c, 360, 700, 230, 190, span(f, dg, dg + 12), 145, RED, 10);
    stamp(c, "AUG 1920", 760, 1180, 90, 0.08, span(f, au, au + 8), STAMP, 146); stamp(c, "OVER", 760, 1320, 80, -0.06, span(f, au + 8, au + 16), "#1d1a17", 147); } }); }
{ const a = at(6), n20 = AT(6, "$20"), n200 = AT(6, "$200"), pz = AT(6, "PULITZER");
  S.push({ id: "losses", from: a - WHIP, punch: [n20, n200, pz], bg: (c) => comicPage(c, 113), draw: (c, f) => {
    hero(c, "−$20M", 540, 480, f, n20, KEY, 170, -0.04);
    label(c, "≈ $200M+ TODAY", 540, 680, 70, span(f, n200, n200 + 8), INK, GOLD, 0.03, 1451);
    if (f >= pz) { const q = back(span(f, pz, pz + 10)); c.save(); c.translate(540, 1080); c.scale(q, q); marker(c, ellipse(0, 0, 170, 170), "#d9a83a", { seed: 1452, contour: 8, shadow: "#a87a20" }); marker(c, [[-70, 140], [-110, 290], [-40, 240], [0, 300], [0, 150]], "#c23a2a", { seed: 1453, contour: 6, streak: false }); marker(c, [[70, 140], [110, 290], [40, 240], [0, 300], [0, 150]], "#c23a2a", { seed: 1454, contour: 6, streak: false }); txt(c, "PULITZER", 0, 0, 44, INK); c.restore(); } } }); }
{ const a = at(7), pr = AT(7, "PRISON"), dp = AT(7, "DEPORTED"), y49 = AT(7, "1949");
  S.push({ id: "fate", from: a - WHIP, punch: [pr, y49], bg: (c, f) => theatre(c, f, 99, "#4a4a5a", "#2e2e3a"), draw: (c, f) => {
    gent(c, 540, 1080, 1.1, 1461);
    if (f >= pr) { c.save(); c.globalAlpha = span(f, pr, pr + 8); c.strokeStyle = "#2b2b2b"; c.lineWidth = 16; for (let i = -3; i <= 3; i++) { c.beginPath(); c.moveTo(540 + i * 70, 760); c.lineTo(540 + i * 70, 1400); c.stroke(); } c.restore(); }
    stamp(c, "DEPORTED", 540, 520, 100, -0.06, span(f, dp, dp + 8), STAMP, 1462);
    label(c, "RIO, 1949 · BROKE", 540, 680, 60, span(f, y49, y49 + 8), INK, CREAM, 0.03, 1463); } }); }
{ const a = at(8), mg = AT(8, "MIRAGE"), yr = AT(8, "YOUR");
  const CD: CardSpec = { cx: 540, cy: 900, w: 680, h: 720, rot: -0.03, color: "#efe5cf", seed: 1471, from: [0, 220] };
  S.push({ id: "mirage", from: a - WHIP, punch: [mg, yr], bg: (c) => scrapPage(c, 383), draw: (c, f) => {
    ransom(c, "MIRAGE", 540, 330, 108, 1472, span(f, mg - 4, mg + 18), 0.1);
    card(c, CD, span(f, a, a + 12)); tape(c, 540, 545, 0.03, 220, span(f, a + 10, a + 16), 1473);
    onCard(c, CD, span(f, a, a + 12), () => { for (let i = 0; i < 5; i++) marker(c, ellipse(-60 + i * 30, 120 - i * 50, 90, 28), GOLD, { seed: 1474 + i, contour: 5, streak: false }); });
    stamp(c, "YOUR MONEY", 540, 1150, 90, -0.06, span(f, yr, yr + 8), STAMP, 1479); } }); }
{ const a = at(9), hg = AT(9, "HUGE"), hw = AT(9, "HOW"), wa = AT(9, "WALK");
  S.push({ id: "walk", from: a - WHIP, punch: [hg, wa], bg: (c) => comicPage(c, 115), draw: (c, f) => {
    pow(c, 540, 520, 300, 190, GOLD, 1481, span(f, hg - 2, hg + 6)); txt(c, "+50%!!", 540, 520, 110, KEY, { stroke: 12, rot: -0.05, alpha: span(f, hg, hg + 4) });
    txt(c, "HOW?", 540, 820, 140, INK, { alpha: span(f, hw, hw + 6), sc: back(span(f, hw, hw + 10)) });
    const w = easeIO(span(f, wa, wa + 20)); person(c, 540 + w * 420, 1250, 1.0, "#3d7fc2", 1482);
    if (f >= wa) stamp(c, "WALK AWAY", 540, 1060, 80, -0.05, span(f, wa, wa + 8), STAMP, 1483); } }); }
S.push(followScene(at(10), AT(10, "MONEY"), AT(10, "FOLLOW")));
const hookCard = (c: Ctx, f: number) => { scrapPage(c, 385); ransom(c, "TOO GOOD?", 540, 620, 96, 1491, span(f, 3, 30), 0.08); stamp(c, "1920", 540, 960, 150, -0.06, span(f, 34, 46), STAMP, 1492); };
export const ponziMix = makeFilm({ title: "Money Mirage · Charles Ponzi (mixed media)", LINES, scenes: S, hookCard, name: "ponziMix" });
void cutout; void penStrike; void easeIO;
