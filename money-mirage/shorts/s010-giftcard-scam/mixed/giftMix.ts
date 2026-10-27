import { type Ctx } from "./core";
import { Cam, drawPart, order, PLATE, STUD, type Part } from "./toyBrickKit";
import { LINES } from "./s010timing";
import {
  span, clamp01, easeOut, easeIO, back, INK, RED, STAMP, GOLD, KEY, CREAM,
  scrapPage, comicPage, theatre, newsPage, card, onCard, tape, cutout, marker, brushLine,
  penLoop, penStrike, penArrow, stamp, ransom, label, hero, txt, burst, pow, clipping,
  rrect, ellipse, makeFilm, followScene, timing, brickBg, person, bubble, WHIP, HOOK_END, type Scene, type CardSpec,
} from "./mirageKit";

// MONEY MIRAGE · s010 PAY WITH A GIFT CARD? IT'S A SCAM, mixed media. Generic gift cards only.
const { at, AT } = timing(LINES, "giftMix");

export const giftCard = (c: Ctx, x: number, y: number, s: number, rot: number, p: number, seed: number, col = "#e4473a", back_ = false) => {
  if (p <= 0) return; const k = back(p); c.save(); c.translate(x, y); c.rotate(rot); c.scale(k * s, k * s);
  marker(c, rrect(420, 260, 26), col, { seed, contour: 7 });
  if (!back_) { c.fillStyle = "#f2c53d"; c.fillRect(-30, -130, 60, 260); c.fillRect(-210, -30, 420, 60); marker(c, ellipse(-30, -60, 50, 30), "#f2c53d", { seed: seed + 1, contour: 4, streak: false }); marker(c, ellipse(30, -60, 50, 30), "#f2c53d", { seed: seed + 2, contour: 4, streak: false }); txt(c, "GIFT CARD", 0, 90, 34, "#ffffff"); }
  else { c.fillStyle = "#2b2b2b"; c.fillRect(-210, -90, 420, 50); c.fillStyle = "#d8d2c4"; c.fillRect(-170, 0, 340, 50); txt(c, "PIN  ••••", 0, 25, 30, INK); txt(c, "#### #### ####", 0, 90, 28, "#ffffff"); }
  c.restore();
};
const phoneRing = (c: Ctx, x: number, y: number, s: number, f: number, p: number, seed: number) => {
  if (p <= 0) return; const sh = Math.sin(f * 1.8) * 6 * (1 - span(p, 0.9, 1)); c.save(); c.translate(x + sh, y); c.scale(s, s);
  marker(c, rrect(300, 560, 50), "#2d3238", { seed, contour: 8 }); c.fillStyle = "#e7f0e8"; c.fillRect(-125, -240, 250, 470);
  txt(c, "INCOMING", 0, -170, 30, INK); txt(c, "UNKNOWN", 0, -120, 34, KEY);
  marker(c, ellipse(-60, 160, 40, 40), "#2f9a55", { seed: seed + 1, contour: 4, streak: false }); marker(c, ellipse(60, 160, 40, 40), "#d9483b", { seed: seed + 2, contour: 4, streak: false });
  c.restore(); for (let i = 0; i < 3; i++) { const r = 200 + i * 40 + ((f * 3) % 40); c.save(); c.strokeStyle = `rgba(36,27,21,${0.4 - i * 0.12})`; c.lineWidth = 6; c.beginPath(); c.arc(x, y, r * s, -0.6, 0.6); c.stroke(); c.beginPath(); c.arc(x, y, r * s, Math.PI - 0.6, Math.PI + 0.6); c.stroke(); c.restore(); }
};
let PID = 0;
const bk = (x: number, y0: number, color: string): Part => ({ id: PID++, color, kind: "prism", foot: [[x, 0], [x + 3, 0], [x + 3, 3], [x, 3]], y0, h: 3, studs: true, step: 0 });

const S: Scene[] = [];
{ const a = HOOK_END, gc = AT(0, "GIFT"), sc = AT(0, "SCAM"), ev = AT(0, "EVERY");
  S.push({ id: "hook", from: a, punch: [sc, ev], bg: (c) => comicPage(c, 131), draw: (c, f) => {
    giftCard(c, 540, 820, 1.5, -0.06, span(f, Math.max(a, gc - 4), Math.max(a, gc - 4) + 10), 1601);
    stamp(c, "SCAM", 540, 820, 190, -0.12, span(f, sc, sc + 8), STAMP, 1602);
    label(c, "EVERY TIME", 540, 1180, 70, span(f, ev, ev + 8), INK, GOLD, 0.03, 1603); } }); }
{ const a = at(1), ftc = AT(1, "FTC"), ev = AT(1, "EVER");
  S.push({ id: "ftc", from: a - WHIP, punch: [ftc, ev], bg: (c) => newsPage(c, 161), draw: (c, f) => {
    clipping(c, 540, 880, 920, 960, -0.02, 162, span(f, a, a + 12), [0, 360]);
    stamp(c, "FTC", 540, 470, 140, -0.04, span(f, ftc, ftc + 8), "#1d1a17", 163);
    giftCard(c, 540, 880, 0.9, 0.05, span(f, ftc + 6, ftc + 16), 164); penStrike(c, 330, 1000, 760, 760, span(f, ev, ev + 8), RED, 18);
    label(c, "NEVER ASKED BY REAL AGENCIES", 540, 1210, 44, span(f, ev + 6, ev + 14), INK, GOLD, 0.03, 165); } }); }
{ const a = at(2), ur = AT(2, "URGENT"), irs = AT(2, "IRS"), ts = AT(2, "TECH"), cu = AT(2, "CUT");
  S.push({ id: "call", from: a - WHIP, punch: [ur, cu], bg: (c) => comicPage(c, 133), draw: (c, f) => {
    phoneRing(c, 540, 760, 1.1, f, span(f, a, a + 10), 1611);
    bubble(c, "IRS!", 240, 400, 60, span(f, irs, irs + 8), false, 1612); bubble(c, "TECH SUPPORT", 790, 480, 46, span(f, ts, ts + 8), false, 1613); bubble(c, "POWER CUT!", 300, 1250, 56, span(f, cu, cu + 8), false, 1614);
    stamp(c, "URGENT", 790, 1200, 90, 0.08, span(f, ur, ur + 8), STAMP, 1615); } }); }
{ const a = at(3), ph = AT(3, "PHONE"), sv = AT(3, "SEVERAL");
  S.push({ id: "stores", from: a - WHIP, punch: [ph, sv], bg: (c, f) => theatre(c, f, 103, "#5a6a7a", "#3d4856"), draw: (c, f) => {
    for (let i = 0; i < 3; i++) { const u = easeOut(span(f, sv - 4 + i * 4, sv + 8 + i * 4)); if (u <= 0) continue; cutout(c, [[140 + i * 300, 980], [140 + i * 300, 800], [380 + i * 300 - 90, 760], [380 + i * 300 - 40, 800], [380 + i * 300 - 40, 980]], ["#d9483b", "#3d7fc2", "#3f9a5a"][i], 1621 + i, 6, u); }
    const w = easeIO(span(f, a, at(4))); person(c, 180 + w * 700, 1280, 0.8, "#8a5ab8", 1624);
    c.save(); c.translate(180 + w * 700 + 60, 1210); c.rotate(0.3); marker(c, rrect(50, 90, 10), "#2d3238", { seed: 1625, contour: 4, streak: false }); c.restore();
    label(c, "STAY ON THE LINE", 540, 470, 60, span(f, ph, ph + 8), INK, GOLD, -0.03, 1626); } }); }
{ const a = at(4), nm = AT(4, "NUMBER"), pin = AT(4, "PIN");
  S.push({ id: "pin", from: a - WHIP, punch: [nm, pin], bg: (c) => scrapPage(c, 401), draw: (c, f) => {
    const CD: CardSpec = { cx: 540, cy: 860, w: 820, h: 560, rot: 0.02, color: "#f2eadb", seed: 1631, from: [0, 200] };
    card(c, CD, span(f, a, a + 12)); tape(c, 540, 590, 0, 200, span(f, a + 10, a + 16), 1632);
    onCard(c, CD, span(f, a, a + 12), () => giftCard(c, 0, 0, 1.4, -0.03, 1, 1633, "#e4473a", true));
    if (f >= nm) penLoop(c, 540, 950, 300, 60, span(f, nm, nm + 10), 1634, RED, 9);
    if (f >= pin) penLoop(c, 540, 885, 260, 60, span(f, pin, pin + 10), 1635, RED, 9); } }); }
{ const a = at(5), mn = AT(5, "MINUTES"), hd = AT(5, "HAND");
  S.push({ id: "drain", from: a - WHIP, punch: [mn, hd], dark: true, bg: brickBg, draw: (c, f) => {
    const k = 3.2, q = new Cam(k, 0, 0).p(3 * STUD, 6 * PLATE, 1.5 * STUD), cam = new Cam(k, 540 - q[0], 1000 - q[1]);
    drawPart(c, cam, { id: 996, color: "#646464", kind: "prism", foot: [[-1, -1], [7, -1], [7, 4], [-1, 4]], y0: -1, h: 1, studs: true, step: 0 }, 0, 0.7);
    const drain = easeIO(span(f, mn - 10, mn + 14)), n = Math.round(8 * (1 - drain));
    const live: { p: Part; dy: number }[] = []; for (let i = 0; i < n; i++) live.push({ p: bk(1.5, i * 3, "#237841"), dy: f < a + 4 + i * 2 ? 200 : 0 });
    order(live, cam).forEach((i) => drawPart(c, cam, live[i].p, live[i].dy, 0.7));
    hero(c, "$0", 540, 360, f, mn + 14, KEY, 200);
    label(c, "CARD STILL IN HAND", 540, 1300, 56, span(f, hd, hd + 8), INK, "#ffffff", 0.03, 1641); } }); }
{ const a = at(6), fs = AT(6, "FAST"), tr = AT(6, "TRACE"), rv = AT(6, "REVERSE");
  S.push({ id: "why", from: a - WHIP, punch: [fs, tr, rv], bg: (c) => comicPage(c, 135), draw: (c, f) => {
    [[fs, "FAST", 400], [tr, "HARD TO TRACE", 700], [rv, "NO UNDO", 1000]].forEach(([t, s, y], i) => { const tt = t as number; stamp(c, s as string, 540, y as number, 96, (i - 1) * 0.06, span(f, tt, tt + 8), STAMP, 1651 + i); });
    giftCard(c, 540, 1300, 0.8, 0.06, span(f, a, a + 10), 1654); } }); }
{ const a = at(7), n200 = AT(7, "$200");
  S.push({ id: "losses", from: a - WHIP, punch: [n200], bg: (c) => newsPage(c, 163), draw: (c, f) => {
    clipping(c, 540, 880, 920, 900, 0.02, 164, span(f, a, a + 12), [0, -360]);
    hero(c, "$200M+", 540, 820, f, n200, KEY, 190, -0.03); label(c, "LOST EVERY YEAR", 540, 1040, 64, span(f, n200 + 6, n200 + 14), INK, GOLD, 0.03, 1661); } }); }
{ const a = at(8), mg = AT(8, "MIRAGE"), sp = AT(8, "SPENT");
  S.push({ id: "mirage", from: a - WHIP, punch: [mg, sp], bg: (c) => scrapPage(c, 403), draw: (c, f) => {
    ransom(c, "MIRAGE", 540, 330, 108, 1671, span(f, mg - 4, mg + 18), 0.1);
    giftCard(c, 540, 860, 1.3, -0.04, span(f, a, a + 12), 1672);
    if (f >= sp) { c.save(); c.globalAlpha = 0.5 * span(f, sp, sp + 8); c.fillStyle = "#e8d6b2"; c.fillRect(250, 680, 580, 360); c.restore(); }
    stamp(c, "ALREADY SPENT", 540, 1240, 86, -0.06, span(f, sp, sp + 8), STAMP, 1673); } }); }
{ const a = at(9), gf = AT(9, "GIFTS"), py = AT(9, "PAYMENTS");
  S.push({ id: "gifts", from: a - WHIP, punch: [gf, py], bg: (c, f) => theatre(c, f, 105, "#7a3c5a", "#552840"), draw: (c, f) => {
    const up = easeOut(span(f, a, a + 12)); c.save(); c.translate(0, (1 - up) * 500); marker(c, rrect(420, 320, 20, 540, 960), "#3d7fc2", { seed: 1681, contour: 8 }); c.fillStyle = "#f2c53d"; c.fillRect(510, 800, 60, 320); c.fillRect(330, 930, 420, 60); c.restore();
    label(c, "FOR GIFTS", 540, 620, 80, span(f, gf, gf + 8), INK, GOLD, -0.03, 1682);
    stamp(c, "NOT PAYMENTS", 540, 1300, 84, -0.05, span(f, py, py + 8), STAMP, 1683); } }); }
S.push(followScene(at(10), AT(10, "MONEY"), AT(10, "FOLLOW")));
const hookCard = (c: Ctx, f: number) => { scrapPage(c, 405); ransom(c, "PAY BY", 540, 560, 140, 1691, span(f, 3, 20), 0.1); ransom(c, "CARD?", 540, 760, 160, 1692, span(f, 20, 40), 0.1); penLoop(c, 540, 760, 320, 130, span(f, 44, 60), 1693, RED, 12); };
export const giftMix = makeFilm({ title: "Money Mirage · gift card scams (mixed media)", LINES, scenes: S, hookCard, name: "giftMix" });
void brushLine; void penArrow; void hero; void burst; void pow; void CREAM; void clamp01;
