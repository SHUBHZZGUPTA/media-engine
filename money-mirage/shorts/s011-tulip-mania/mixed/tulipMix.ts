import { type Ctx, type P } from "./core";
import { Cam, drawPart, order, PLATE, STUD, type Part } from "./toyBrickKit";
import { LINES } from "./s011timing";
import {
  span, clamp01, easeOut, easeIO, back, INK, RED, STAMP, GOLD, KEY, CREAM,
  scrapPage, comicPage, theatre, newsPage, card, onCard, tape, cutout, marker, brushLine,
  penLoop, penStrike, penArrow, stamp, ransom, label, hero, txt, burst, clipping,
  rrect, ellipse, makeFilm, followScene, timing, brickBg, person, lineChart, WHIP, HOOK_END, type Scene, type CardSpec,
} from "./mirageKit";

// MONEY MIRAGE · s011 TULIP MANIA, 1637, mixed media. Legend vs. the historians' record.
const { at, AT } = timing(LINES, "tulipMix");

/** a flamed tulip (marker comic): white petals with red flames */
export const tulip = (c: Ctx, x: number, y: number, s: number, seed: number, sway = 0) => {
  c.save(); c.translate(x, y); c.rotate(sway); c.scale(s, s);
  brushLine(c, [[0, 0], [6, 140], [0, 300]], 16, "#3f7a3a");
  marker(c, [[0, 200], [-90, 120], [-60, 260]], "#4f9a4a", { seed: seed + 3, contour: 5, streak: false });
  const petal = (cx: number, rot: number, sd: number) => { const pts: P[] = []; for (let k = 0; k < 24; k++) { const a = (k / 24) * Math.PI * 2, rx = 46, ry = 100; const px = Math.cos(a) * rx, py = Math.sin(a) * ry * (Math.sin(a) < 0 ? 1.0 : 0.75); pts.push([cx + px * Math.cos(rot) - py * Math.sin(rot), -90 + px * Math.sin(rot) + py * Math.cos(rot)]); } marker(c, pts, "#fbf6ea", { seed: sd, contour: 6, shadow: "#e2d8c4" }); };
  petal(-34, -0.28, seed); petal(34, 0.28, seed + 1); petal(0, 0, seed + 2);
  for (let i = 0; i < 4; i++) brushLine(c, [[-30 + i * 20, -30], [-26 + i * 18, -110], [-30 + i * 20, -170]], 7, "#c23a2a");
  c.restore();
};
export const house = (c: Ctx, x: number, y: number, s: number, seed: number) => {
  c.save(); c.translate(x, y); c.scale(s, s);
  cutout(c, [[-110, 220], [-110, -60], [-60, -60], [-60, -120], [-20, -120], [-20, -190], [20, -190], [20, -120], [60, -120], [60, -60], [110, -60], [110, 220]], "#8a4a32", seed, 6);
  for (let r = 0; r < 3; r++) for (let k = -1; k <= 1; k++) cutout(c, rrect(40, 56, 4, k * 60, -10 + r * 76), "#f3e6c0", seed + 1 + r * 3 + k + 1, 2);
  c.restore();
};
let PID = 0;

const S: Scene[] = [];
{ const a = HOOK_END, bl = AT(0, "BULB"), hs = AT(0, "HOUSE");
  S.push({ id: "hook", from: a, punch: [bl, hs], bg: (c) => scrapPage(c, 411), draw: (c, f) => {
    stamp(c, "1637", 540, 400, 110, -0.06, span(f, a, a + 8), "#1d1a17", 1701);
    tulip(c, 330, 860, 1.2, 1702, Math.sin(f * 0.07) * 0.05);
    txt(c, "=", 560, 900, 160, INK, { alpha: span(f, hs - 6, hs) });
    if (f >= hs - 4) house(c, 800, 880, 1.0 * back(span(f, hs - 4, hs + 8)), 1703);
    label(c, "LEGEND SAYS", 540, 1300, 60, span(f, a + 6, a + 14), INK, GOLD, -0.03, 1704); } }); }
{ const a = at(1), sa = AT(1, "SEMPER"), fl = AT(1, "FLAMES");
  S.push({ id: "semper", from: a - WHIP, punch: [sa, fl], bg: (c) => comicPage(c, 141), draw: (c, f) => {
    tulip(c, 540, 700, 1.9, 1711, Math.sin(f * 0.06) * 0.04);
    label(c, "SEMPER AUGUSTUS", 540, 1290, 70, span(f, sa, sa + 8), INK, CREAM, -0.03, 1712);
    if (f >= fl) penLoop(c, 540, 520, 200, 160, span(f, fl, fl + 12), 1713, RED, 9); } }); }
{ const a = at(2), n12 = AT(2, "1,200"), n10 = AT(2, "10,000");
  S.push({ id: "price", from: a - WHIP, punch: [n12, n10], bg: (c) => newsPage(c, 171), draw: (c, f) => {
    clipping(c, 540, 860, 920, 900, -0.02, 172, span(f, a, a + 12), [0, 360]);
    lineChart(c, 540, 820, 720, 480, [0.12, 0.2, 0.3, 0.45, 0.55, 0.75, 1.0], span(f, n12 - 4, n10 + 6), "#1d1a17", 12);
    label(c, "1,200", 260, 1080, 60, span(f, n12, n12 + 8), INK, CREAM, -0.04, 173); hero(c, "10,000", 760, 520, f, n10, KEY, 130, 0.03); label(c, "GUILDERS", 760, 680, 46, span(f, n10 + 6, n10 + 14), INK, GOLD, 0.03, 174); } }); }
{ const a = at(3), gr = AT(3, "GROUND"), tv = AT(3, "TAVERNS");
  S.push({ id: "tavern", from: a - WHIP, punch: [gr, tv], bg: (c, f) => theatre(c, f, 107, "#6a4a2a", "#4a3218"), draw: (c, f) => {
    const up = easeOut(span(f, a, a + 12)); c.save(); c.translate(0, (1 - up) * 500);
    cutout(c, rrect(780, 60, 10, 540, 1180), "#8a6a44", 1721, 6);
    for (let i = 0; i < 3; i++) { const x = 300 + i * 240; c.save(); c.strokeStyle = "#3b2a18"; c.lineWidth = 7; c.beginPath(); c.moveTo(x, 1180); c.lineTo(x, 1720); c.stroke(); c.restore(); person(c, x, 1080 + Math.sin((f + i * 9) * 0.3) * 6, 0.7, ["#7a2e2e", "#2e4a7a", "#2e7a4a"][i], 1722 + i); }
    c.restore();
    if (f >= tv) for (let i = 0; i < 3; i++) { const q = back(span(f, tv + i * 5, tv + i * 5 + 10)); if (q <= 0) continue; c.save(); c.translate(360 + i * 180, 760); c.rotate((i - 1) * 0.15); c.scale(q, q); marker(c, rrect(170, 220, 8), "#f3e9cf", { seed: 1726 + i, contour: 5, streak: false }); for (let l = 0; l < 4; l++) { c.fillStyle = "rgba(36,27,21,0.5)"; c.fillRect(-60, -70 + l * 34, 120, 7); } c.restore(); }
    stamp(c, "STILL IN THE GROUND", 540, 470, 60, -0.04, span(f, gr, gr + 8), STAMP, 1729); } }); }
{ const a = at(4), fb = AT(4, "FEBRUARY"), nb = AT(4, "NOBODY"), cl = AT(4, "COLLAPSED");
  S.push({ id: "crash", from: a - WHIP, punch: [nb, cl], bg: (c) => comicPage(c, 143), draw: (c, f) => {
    stamp(c, "FEB 1637", 540, 380, 100, -0.05, span(f, fb, fb + 8), "#1d1a17", 1731);
    lineChart(c, 540, 820, 760, 500, [0.3, 0.5, 0.75, 1.0, 0.25, 0.08, 0.04], span(f, a, cl + 8), KEY, 14);
    if (f >= nb) label(c, "NO BIDS", 300, 1180, 70, span(f, nb, nb + 8), INK, GOLD, -0.05, 1732);
    if (f >= cl) burst(c, 760, 900, 40, 220, 20, 1733, span(f, cl, cl + 6)); } }); }
{ const a = at(5), rn = AT(5, "RUINED"), ev = AT(5, "EVERYTHING");
  S.push({ id: "legend", from: a - WHIP, punch: [rn, ev], bg: (c) => scrapPage(c, 413), draw: (c, f) => {
    const CD: CardSpec = { cx: 540, cy: 860, w: 820, h: 640, rot: -0.03, color: "#e7d9c0", seed: 1741, from: [0, 200] };
    card(c, CD, span(f, a, a + 12)); tape(c, 540, 550, 0.02, 200, span(f, a + 10, a + 16), 1742);
    onCard(c, CD, span(f, a, a + 12), () => { person(c, -150, 40, 0.9, "#7a2e2e", 1743); person(c, 150, 40, 0.9, "#2e4a7a", 1744); });
    stamp(c, "RUINED?", 540, 1210, 110, -0.06, span(f, rn, rn + 8), STAMP, 1745);
    label(c, "THE STORY", 540, 470, 64, span(f, a + 6, a + 14), INK, GOLD, 0.03, 1746); } }); }
{ const a = at(6), tw = AT(6, "TWIST"), gd = AT(6, "GOLDGAR"), bk = AT(6, "BANKRUPT");
  S.push({ id: "records", from: a - WHIP, punch: [tw, bk], bg: (c) => newsPage(c, 175), draw: (c, f) => {
    clipping(c, 340, 760, 520, 680, -0.06, 176, span(f, a, a + 12), [-300, 0]); clipping(c, 760, 900, 520, 680, 0.05, 177, span(f, a + 6, a + 18), [300, 0]);
    stamp(c, "TWIST", 540, 380, 110, -0.05, span(f, tw, tw + 8), STAMP, 178);
    label(c, "HISTORIAN: ANNE GOLDGAR", 540, 520, 46, span(f, gd, gd + 8), INK, GOLD, 0.02, 179);
    hero(c, "0 BANKRUPTCIES", 540, 1330, f, bk, KEY, 100, -0.03); } }); }
{ const a = at(7), n200 = AT(7, "200");
  S.push({ id: "book", from: a - WHIP, punch: [n200], bg: (c, f) => theatre(c, f, 109, "#3d5a73", "#2b4256"), draw: (c, f) => {
    const up = easeOut(span(f, a, a + 12)); c.save(); c.translate(0, (1 - up) * 500);
    cutout(c, rrect(440, 560, 14, 540, 950), "#7a2e2e", 1751, 8); cutout(c, rrect(360, 80, 8, 540, 820), "#d7b25c", 1752, 3); txt(c, "1841", 540, 822, 54, INK); c.restore();
    hero(c, "+200 YEARS", 540, 450, f, n200, "#ffd166", 120); } }); }
{ const a = at(8), mg = AT(8, "MIRAGE"), bb = AT(8, "BUBBLE");
  S.push({ id: "mirage", from: a - WHIP, punch: [mg, bb], bg: (c) => scrapPage(c, 415), draw: (c, f) => {
    ransom(c, "MIRAGE", 540, 330, 108, 1761, span(f, mg - 4, mg + 18), 0.1);
    tulip(c, 540, 860, 1.3, 1762, Math.sin(f * 0.07) * 0.05);
    if (f >= bb) { const r = 260 + 30 * Math.sin(f * 0.2); c.save(); c.globalAlpha = 0.6 * span(f, bb, bb + 8); c.strokeStyle = "#8fc6e0"; c.lineWidth = 10; c.beginPath(); c.arc(540, 760, r, 0, 6.283); c.stroke(); c.restore(); }
    stamp(c, "A STORY BUBBLE", 540, 1300, 80, -0.05, span(f, bb, bb + 8), STAMP, 1763); } }); }
{ const a = at(9), ev = AT(9, "EVERYONE"), tl = AT(9, "TELLING");
  S.push({ id: "who", from: a - WHIP, punch: [ev, tl], bg: (c) => comicPage(c, 145), draw: (c, f) => {
    person(c, 540, 1000, 1.4, "#3d7fc2", 1771);
    const bq = back(span(f, ev, ev + 10)); if (bq > 0) { c.save(); c.translate(540, 560); c.scale(bq, bq); marker(c, rrect(620, 200, 60), "#ffffff", { seed: 1772, contour: 7, hi: false, streak: false }); txt(c, "THEY LOST ALL!", 0, 0, 60, INK); c.restore(); }
    txt(c, "WHO SAYS?", 540, 1300, 96, KEY, { stroke: 12, alpha: span(f, tl, tl + 6), sc: back(span(f, tl, tl + 10)) }); } }); }
S.push(followScene(at(10), AT(10, "MONEY"), AT(10, "FOLLOW")));
const hookCard = (c: Ctx, f: number) => { scrapPage(c, 417); ransom(c, "ONE BULB", 540, 560, 120, 1781, span(f, 3, 26), 0.08); ransom(c, "A HOUSE?", 540, 760, 120, 1782, span(f, 26, 48), 0.08); };
export const tulipMix = makeFilm({ title: "Money Mirage · tulip mania (mixed media)", LINES, scenes: S, hookCard, name: "tulipMix" });
void Cam; void drawPart; void order; void PLATE; void STUD; void PID; void brickBg; void clamp01; void easeIO; void penStrike; void penArrow; void GOLD;
type _P = Part;
