import { type Ctx } from "./core";
import { Cam, drawPart, order, PLATE, STUD, type Part } from "./toyBrickKit";
import { LINES } from "./s012timing";
import {
  span, clamp01, easeOut, easeIO, back, INK, RED, STAMP, GOLD, KEY, CREAM,
  scrapPage, comicPage, theatre, newsPage, card, onCard, tape, cutout, marker, brushLine,
  penLoop, penStrike, penArrow, stamp, ransom, label, hero, txt, burst, pow, clipping,
  rrect, ellipse, makeFilm, followScene, timing, brickBg, person, WHIP, HOOK_END, type Scene, type CardSpec,
} from "./mirageKit";

// MONEY MIRAGE · s012 DRIP PRICING, mixed media. The $100 → $130 ticket is illustrative.
const { at, AT } = timing(LINES, "dripMix");

export const ticket = (c: Ctx, x: number, y: number, s: number, rot: number, price: string, p: number, seed: number) => {
  if (p <= 0) return; const k = back(p); c.save(); c.translate(x, y); c.rotate(rot); c.scale(k * s, k * s);
  marker(c, [[-260, -110], [260, -110], [260, -30], [236, 0], [260, 30], [260, 110], [-260, 110], [-260, 30], [-236, 0], [-260, -30]], "#f2c53d", { seed, contour: 7, shadow: "#c99a20" });
  c.setLineDash([10, 10]); c.strokeStyle = INK; c.lineWidth = 3; c.beginPath(); c.moveTo(150, -100); c.lineTo(150, 100); c.stroke(); c.setLineDash([]);
  txt(c, "ADMIT ONE", -50, -50, 34, INK); txt(c, price, -50, 30, 90, INK);
  c.restore();
};
/** fee drops falling from a tap into a cup over the checkout total */
const drips = (c: Ctx, x: number, y0: number, y1: number, f: number, n: number, seed: number) => { for (let i = 0; i < n; i++) { const t = ((f * 0.03 + i / n) % 1), yy = y0 + (y1 - y0) * t; marker(c, [[x, yy - 30], [x + 18, yy + 6], [x, yy + 20], [x - 18, yy + 6]], "#5aa8d8", { seed: seed + i, contour: 4, streak: false, hi: true }); } };
let PID = 0;
const bar = (x: number, h: number, color: string): Part => ({ id: PID++, color, kind: "prism", foot: [[x, 0], [x + 3, 0], [x + 3, 3], [x, 3]], y0: 0, h, studs: true, step: 0 });

const S: Scene[] = [];
{ const a = HOOK_END, n130 = AT(0, "$130"), ac = AT(0, "ACCIDENT");
  S.push({ id: "hook", from: a, punch: [n130, ac], bg: (c) => comicPage(c, 151), draw: (c, f) => {
    ticket(c, 540, 700, 1.4, -0.05, f < n130 ? "$100" : "$130", span(f, a, a + 10), 1801);
    if (f >= n130) { burst(c, 540, 700, 340, 520, 30, 1802, span(f, n130, n130 + 8)); penLoop(c, 480, 740, 220, 110, span(f, n130, n130 + 12), 1803, RED, 10); }
    stamp(c, "NO ACCIDENT", 540, 1200, 96, -0.05, span(f, ac, ac + 8), STAMP, 1804); } }); }
{ const a = at(1), dr = AT(1, "DRIP"), en = AT(1, "END");
  S.push({ id: "drip", from: a - WHIP, punch: [dr, en], bg: (c, f) => theatre(c, f, 111), draw: (c, f) => {
    const up = easeOut(span(f, a, a + 12)); c.save(); c.translate(0, (1 - up) * 500);
    cutout(c, rrect(160, 60, 10, 540, 420), "#9aa4ad", 1811, 4); cutout(c, rrect(40, 120, 8, 540, 500), "#9aa4ad", 1812, 3);
    cutout(c, rrect(520, 260, 20, 540, 1220), "#fbf6ea", 1813, 6); txt(c, "TOTAL", 540, 1160, 44, INK); txt(c, "$" + (100 + Math.floor(30 * easeIO(span(f, dr, en + 10)))), 540, 1240, 100, KEY); c.restore();
    if (f >= dr) drips(c, 540, 580, 1080, f - dr, 4, 1814);
    label(c, "+ FEES", 820, 800, 60, span(f, dr + 4, dr + 12), INK, GOLD, 0.06, 1818); } }); }
{ const a = at(2), sh = AT(2, "STUBHUB"), ml = AT(2, "MILLIONS"), n21 = AT(2, "21%");
  S.push({ id: "spend", from: a - WHIP, punch: [sh, n21], dark: true, bg: brickBg, draw: (c, f) => {
    const k = 3.2, q = new Cam(k, 0, 0).p(4.5 * STUD, 12 * PLATE, 1.5 * STUD), cam = new Cam(k, 540 - q[0], 1000 - q[1]);
    drawPart(c, cam, { id: 993, color: "#646464", kind: "prism", foot: [[-1, -1], [10, -1], [10, 4], [-1, 4]], y0: -1, h: 1, studs: true, step: 0 }, 0, 0.7);
    const g = easeIO(span(f, n21 - 10, n21 + 4)); const live = [{ p: bar(0, 20, "#68C3E2"), dy: 240 * (1 - easeOut(span(f, a + 4, a + 13))) }, { p: bar(6, Math.round(20 + 4 * g), "#B40000"), dy: 240 * (1 - easeOut(span(f, a + 8, a + 17))) }];
    order(live, cam).forEach((i) => drawPart(c, cam, live[i].p, live[i].dy, 0.7));
    label(c, "FEES UP FRONT", 320, 1260, 44, span(f, ml, ml + 8), INK, "#ffffff", -0.04, 1821); label(c, "FEES AT CHECKOUT", 760, 1260, 44, span(f, ml + 4, ml + 12), "#ffffff", KEY, 0.04, 1822);
    stamp(c, "STUBHUB TEST", 540, 380, 70, -0.04, span(f, sh, sh + 8), "#ff6b5a", 1823); hero(c, "+21% SPENT", 540, 560, f, n21, KEY, 110); } }); }
{ const a = at(3), n14 = AT(3, "14%");
  S.push({ id: "buy", from: a - WHIP, punch: [n14], bg: (c) => comicPage(c, 153), draw: (c, f) => {
    person(c, 540, 1000, 1.4, "#3d7fc2", 1831);
    burst(c, 540, 520, 140, 320, 26, 1832, span(f, n14, n14 + 8), GOLD); pow(c, 540, 520, 280, 170, GOLD, 1833, span(f, n14, n14 + 6)); hero(c, "+14%", 540, 520, f, n14, KEY, 150, -0.05);
    label(c, "MORE LIKELY TO BUY", 540, 1330, 60, span(f, n14 + 6, n14 + 14), INK, CREAM, 0.03, 1834); } }); }
{ const a = at(4), ck = AT(4, "CHECKOUT"), st = AT(4, "SEATS"), yr = AT(4, "YOURS");
  S.push({ id: "seats", from: a - WHIP, punch: [st, yr], bg: (c, f) => theatre(c, f, 113, "#7a3c3c", "#552828"), draw: (c, f) => {
    for (let r = 0; r < 2; r++) for (let i = 0; i < 5; i++) { const x = 220 + i * 160, y = 1100 + r * 180, mine = r === 0 && i === 2; cutout(c, rrect(120, 140, 20, x, y), mine && f >= st ? "#2f9a55" : "#8a2e2e", 1841 + r * 5 + i, 4); }
    if (f >= yr) { label(c, "MINE!", 540, 900, 70, span(f, yr, yr + 8), INK, GOLD, -0.04, 1851); }
    stamp(c, "CHECKOUT", 540, 470, 90, -0.04, span(f, ck, ck + 8), STAMP, 1852); } }); }
{ const a = at(5), my = AT(5, "MAY"), fp = AT(5, "FULL");
  S.push({ id: "rule", from: a - WHIP, punch: [my, fp], bg: (c) => newsPage(c, 181), draw: (c, f) => {
    clipping(c, 540, 880, 920, 980, -0.02, 182, span(f, a, a + 12), [0, 360]);
    stamp(c, "MAY 2025", 540, 450, 100, -0.05, span(f, my, my + 8), "#1d1a17", 183);
    ticket(c, 540, 860, 1.0, 0.04, "$130", span(f, fp - 6, fp + 6), 184); label(c, "ALL-IN PRICE", 540, 1100, 64, span(f, fp, fp + 8), "#ffffff", KEY, 0.03, 185); } }); }
{ const a = at(6), tx = AT(6, "TAXES"), sp = AT(6, "SURPRISES");
  S.push({ id: "taxes", from: a - WHIP, punch: [tx, sp], bg: (c) => scrapPage(c, 421), draw: (c, f) => {
    const CD: CardSpec = { cx: 540, cy: 860, w: 820, h: 600, rot: 0.02, color: "#f2eadb", seed: 1861, from: [0, 200] };
    card(c, CD, span(f, a, a + 12)); tape(c, 540, 570, 0, 200, span(f, a + 10, a + 16), 1862);
    onCard(c, CD, span(f, a, a + 12), () => { txt(c, "TICKET  $100", 0, -150, 56, INK); txt(c, "FEES   $30", 0, -50, 56, INK); txt(c, "TAX    later", 0, 50, 56, "rgba(36,27,21,0.6)"); });
    if (f >= tx) penLoop(c, 540, 910, 300, 60, span(f, tx, tx + 10), 1863, RED, 9);
    stamp(c, "NO SURPRISES", 540, 1250, 90, -0.05, span(f, sp, sp + 8), STAMP, 1864); } }); }
{ const a = at(7), mg = AT(7, "MIRAGE"), bt = AT(7, "BAIT");
  S.push({ id: "mirage", from: a - WHIP, punch: [mg, bt], bg: (c) => scrapPage(c, 423), draw: (c, f) => {
    ransom(c, "MIRAGE", 540, 330, 108, 1871, span(f, mg - 4, mg + 18), 0.1);
    ticket(c, 540, 840, 1.2, -0.04, "$100", span(f, a, a + 12), 1872);
    if (f >= bt) { brushLine(c, [[540, 600], [540, 690]], 6, INK); brushLine(c, [[540, 690], [540, 740], [580, 780], [620, 740]], 10, "#6b6f74"); }
    stamp(c, "BAIT", 540, 1220, 130, -0.06, span(f, bt, bt + 8), STAMP, 1873); } }); }
{ const a = at(8), tt = AT(8, "TOTAL"), hk = AT(8, "HOOKED");
  S.push({ id: "total", from: a - WHIP, punch: [tt, hk], bg: (c) => comicPage(c, 155), draw: (c, f) => {
    ticket(c, 540, 560, 0.9, -0.05, "$100", span(f, a, a + 10), 1881); penStrike(c, 330, 620, 760, 500, span(f, hk - 4, hk + 4), RED, 16);
    penArrow(c, [540, 720], [540, 960], span(f, tt - 6, tt + 6), RED, 10);
    hero(c, "TOTAL: $130", 540, 1120, f, tt, KEY, 120, -0.03); } }); }
S.push(followScene(at(9), AT(9, "MONEY"), AT(9, "FOLLOW")));
const hookCard = (c: Ctx, f: number) => { scrapPage(c, 425); ransom(c, "+$30?", 540, 620, 190, 1891, span(f, 3, 22), 0.1); stamp(c, "WHERE FROM?", 540, 980, 110, -0.06, span(f, 30, 42), STAMP, 1892); };
export const dripMix = makeFilm({ title: "Money Mirage · drip pricing (mixed media)", LINES, scenes: S, hookCard, name: "dripMix" });
void clamp01; void ellipse; void person; void onCard;
