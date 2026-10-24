import { type Ctx } from "./core";
import { Cam, drawPart, order, PLATE, STUD, type Part } from "./toyBrickKit";
import { LINES } from "./s006timing";
import {
  span, clamp01, easeOut, easeIO, back, INK, RED, STAMP, GOLD, KEY, CREAM, NAVY,
  scrapPage, comicPage, theatre, newsPage, card, onCard, tape, cutout, marker, brushLine,
  penLoop, penStrike, penArrow, stamp, ransom, label, hero, txt, burst, pow, clipping,
  rrect, ellipse, xf, makeFilm, followScene, timing, brickBg, person, priceTag, WHIP, HOOK_END, type Scene, type CardSpec,
} from "./mirageKit";

// MONEY MIRAGE · s006 WHY PRICES END IN .99 (left-digit effect, $9 endings), mixed media.
const { at, AT } = timing(LINES, "charmMix");

/** a dress cut-out (toy theatre) with a price tag */
const dress = (c: Ctx, x: number, y: number, s: number, col: string, seed: number) => {
  c.save(); c.translate(x, y); c.scale(s, s);
  cutout(c, [[-50, -200], [50, -200], [70, -120], [40, -60], [150, 200], [-150, 200], [-40, -60], [-70, -120]], col, seed, 6);
  c.restore();
};
let PID = 0;
const P = (foot: [number, number][], y0: number, h: number, color: string, kind: "prism" | "round" = "prism", studs = true): Part => ({ id: PID++, color, kind, foot, y0, h, studs, step: 0 });
const R = (x0: number, z0: number, x1: number, z1: number) => [[x0, z0], [x1, z0], [x1, z1], [x0, z1]] as [number, number][];
const CAR: Part[] = [
  P(R(-1, -1, 15, 8), -1, 1, "#646464"),
  P(R(1, 1, 13, 6), 2, 3, "#1E5AA8", "prism", false), P(R(4, 1, 10, 6), 5, 6, "#1E5AA8", "prism", true), P(R(4.5, 1, 9.5, 6), 6, 4, "#68C3E2", "prism", false),
  P(R(2, 0.2, 4.5, 1.2), 0, 2, "#1B2A34", "prism", false), P(R(9.5, 0.2, 12, 1.2), 0, 2, "#1B2A34", "prism", false), P(R(2, 5.8, 4.5, 6.8), 0, 2, "#1B2A34", "prism", false), P(R(9.5, 5.8, 12, 6.8), 0, 2, "#1B2A34", "prism", false),
];

const S: Scene[] = [];
// 1 · hook (comic): $9.99, and the .99 fades until only "$9" is read
{
  const a = HOOK_END, n9 = at(0, LINES[0].words.length - 1);
  S.push({ id: "hook", from: a, punch: [n9], bg: (c) => comicPage(c, 91),
    draw: (c, f) => {
      priceTag(c, 560, 760, 760, 380, -0.05, "", span(f, a, a + 12), 1201);
      const fade = easeIO(span(f, n9, n9 + 12));
      txt(c, "$9", 470, 780, 230, INK, { rot: -0.05 }); txt(c, ".99", 770, 760, 150, INK, { rot: -0.05, alpha: 1 - 0.85 * fade, sc: 1 - 0.4 * fade });
      if (f >= n9) penLoop(c, 470, 780, 170, 140, span(f, n9 + 4, n9 + 16), 1202, RED, 11);
      txt(c, "?", 860, 430, 200, RED, { stroke: 16, sc: back(span(f, a + 4, a + 14)), alpha: span(f, a + 4, a + 8), rot: 0.15 });
    } });
}
// 2 · left-digit effect (scrapbook): an eye-line sweeps left to right; tape slaps on the first digit
{
  const a = at(1), ld = AT(1, "LEFT"), rd = AT(1, "READ"), st = AT(1, "STICKS");
  const CD: CardSpec = { cx: 540, cy: 840, w: 900, h: 560, rot: 0.02, color: "#f2eadb", seed: 1211, from: [-100, 200] };
  S.push({ id: "leftdigit", from: a - WHIP, punch: [ld, st], bg: (c) => scrapPage(c, 361),
    draw: (c, f) => {
      card(c, CD, span(f, a, a + 12)); tape(c, 170, 590, -0.6, 180, span(f, a + 10, a + 16), 1212); tape(c, 910, 590, 0.6, 180, span(f, a + 12, a + 18), 1213);
      onCard(c, CD, span(f, a, a + 12), () => txt(c, "$9.99", 0, 20, 260, INK));
      stamp(c, "LEFT DIGIT", 540, 460, 80, -0.05, span(f, ld, ld + 8), STAMP, 1214);
      penArrow(c, [180, 1150], [900, 1150], span(f, rd, rd + 14), RED, 10);
      if (f >= st) { tape(c, 330, 860, -0.3, 230, span(f, st, st + 6), 1215); txt(c, "STUCK!", 330, 1050, 60, STAMP, { alpha: span(f, st + 4, st + 8), rot: -0.1 }); }
    } });
}
// 3 · ten vs nine-something (comic): two tags; the one cent drops between them
{
  const a = at(2), n10 = AT(2, "$10"), n999 = AT(2, "$9.99"), ce = AT(2, "CENT"), dl = AT(2, "DOLLAR");
  S.push({ id: "tags", from: a - WHIP, punch: [ce, dl], bg: (c) => comicPage(c, 93),
    draw: (c, f) => {
      priceTag(c, 300, 600, 400, 200, -0.08, "$10", span(f, n10 - 2, n10 + 10), 1221); priceTag(c, 790, 600, 400, 200, 0.08, "$9.99", span(f, n999 - 2, n999 + 10), 1222);
      label(c, "TEN", 300, 790, 56, span(f, n10 + 6, n10 + 14), INK, CREAM, -0.05, 1223); label(c, "NINE-ISH", 790, 790, 56, span(f, n999 + 6, n999 + 14), INK, GOLD, 0.05, 1224);
      if (f >= ce - 10) { const dropT = easeOut(span(f, ce - 10, ce + 2)); marker(c, ellipse(545, 300 + 700 * dropT, 60, 60), "#c98a4a", { seed: 1225, contour: 7, shadow: "#9a6430" }); txt(c, "1¢", 545, 300 + 700 * dropT, 46, INK); }
      hero(c, "−$1?", 545, 1250, f, dl, KEY, 170);
    } });
}
// 4 · the car odometer (toy brick): 79,999 → 80,000 and $200 drops off
{
  const a = at(3), n22 = AT(3, "22"), n200 = AT(3, "$200"), om = AT(3, "ODOMETER"), n10k = AT(3, "10,000");
  S.push({ id: "car", from: a - WHIP, punch: [n200, n10k], dark: true, bg: brickBg,
    draw: (c, f) => {
      const life = span(f, a, at(4)), k = 3.4 * (1 + 0.1 * life), q = new Cam(k, 0, 0).p(7 * STUD, 4 * PLATE, 3.5 * STUD), cam = new Cam(k, 540 - q[0], 900 - q[1]);
      const live = CAR.map((p, i) => { const land = a + 2 + i * 3, t = clamp01((f - (land - 9)) / 9); return f < land - 9 ? null : { p, dy: f < land ? 240 * (1 - easeOut(t)) : 0 }; }).filter(Boolean) as { p: Part; dy: number }[];
      order(live, cam).forEach((i) => drawPart(c, cam, live[i].p, live[i].dy, 0.7));
      label(c, "22 MILLION SALES", 540, 330, 60, span(f, n22, n22 + 8), INK, "#ffffff", -0.03, 1231);
      const roll = f >= n10k; label(c, roll ? "80,000 MI" : "79,999 MI", 540, 1280, 80, span(f, om - 4, om + 6), roll ? "#ffffff" : INK, roll ? KEY : CREAM, 0.03, 1232);
      hero(c, "−$200", 540, 520, f, Math.max(n200, n10k), KEY, 160);
    } });
}
// 5 · the dress experiment (newsprint): $34, $39, $44; the $39 is circled
{
  const a = at(4), wp = AT(4, "WEIRD"), ex = AT(4, "EXPERIMENT"), n39 = AT(4, "$39"), n34 = AT(4, "$34");
  S.push({ id: "dresses", from: a - WHIP, punch: [n39, n34], bg: (c) => newsPage(c, 121),
    draw: (c, f) => {
      clipping(c, 540, 880, 940, 1040, -0.02, 122, span(f, a, a + 12), [0, 360]);
      stamp(c, "EXPERIMENT", 540, 440, 80, -0.04, span(f, ex, ex + 8), "#1d1a17", 123);
      [["$34", "#d9483b", n34], ["$39", "#3d7fc2", n39], ["$44", "#3f9a5a", n34 + 6]].forEach(([p, cl, t], i) => { const x = 250 + i * 290, up = easeOut(span(f, ex + i * 4, ex + i * 4 + 12)); if (up <= 0) return; c.save(); c.translate(0, (1 - up) * 300); dress(c, x, 840, 0.85, cl as string, 124 + i); label(c, p as string, x, 1080, 60, span(f, (t as number) - 4, (t as number) + 6), INK, CREAM, (i - 1) * 0.05, 127 + i); c.restore(); });
      if (f >= n39) penLoop(c, 540, 900, 190, 300, span(f, n39, n39 + 14), 130, RED, 11);
      if (f >= wp) txt(c, "?!", 880, 560, 120, RED, { stroke: 12, alpha: span(f, wp, wp + 6), rot: 0.15 });
    } });
}
// 6 · nine means bargain (toy theatre): a giant 9 under a SALE pelmet, puppets cheering
{
  const a = at(5), fw = AT(5, "FEWER"), sl = AT(5, "SALES"), bg = AT(5, "BARGAIN");
  S.push({ id: "nine", from: a - WHIP, punch: [sl, bg], bg: (c, f) => theatre(c, f, 93, "#7a3c3c", "#552828"),
    draw: (c, f) => {
      const up = easeOut(span(f, a, a + 14)); c.save(); c.translate(0, (1 - up) * 600);
      cutout(c, rrect(420, 520, 60, 540, 880), "#f2c53d", 1241, 8); txt(c, "9", 540, 900, 440, INK); c.restore();
      stamp(c, "SALE!", 540, 420, 120, -0.06, span(f, sl, sl + 8), STAMP, 1242);
      ["#d9483b", "#3d7fc2", "#3f9a5a"].forEach((cl, i) => { const x = 220 + i * 320, bob = Math.sin((f + i * 9) * 0.5) * 18 * span(f, bg, bg + 6), u = easeOut(span(f, fw + i * 3, fw + i * 3 + 12)); c.save(); c.strokeStyle = "#3b2a18"; c.lineWidth = 7; c.beginPath(); c.moveTo(x, 1450 + (1 - u) * 400); c.lineTo(x, 1720); c.stroke(); c.restore(); person(c, x, 1370 + bob + (1 - u) * 400, 0.65, cl, 1243 + i); });
      label(c, "= BARGAIN", 540, 1220, 66, span(f, bg, bg + 8), INK, GOLD, 0.04, 1246);
    } });
}
// 7 · the mirage (scrapbook): the 9 is a signal, not a discount
{
  const a = at(6), mg = AT(6, "MIRAGE"), dc = AT(6, "DISCOUNT"), sg = AT(6, "SIGNAL");
  const CD: CardSpec = { cx: 540, cy: 900, w: 620, h: 720, rot: -0.03, color: "#efe5cf", seed: 1251, from: [0, 220] };
  S.push({ id: "mirage", from: a - WHIP, punch: [mg, sg], bg: (c) => scrapPage(c, 363),
    draw: (c, f) => {
      ransom(c, "MIRAGE", 540, 330, 108, 1252, span(f, mg - 4, mg + 18), 0.1);
      card(c, CD, span(f, a, a + 12)); tape(c, 540, 560, 0.03, 220, span(f, a + 10, a + 16), 1253);
      onCard(c, CD, span(f, a, a + 12), () => txt(c, "9", 0, 30, 460, INK));
      stamp(c, "NOT A DISCOUNT", 540, 1000, 66, -0.08, span(f, dc, dc + 8), STAMP, 1254);
      label(c, "JUST A SIGNAL", 540, 1340, 64, span(f, sg, sg + 8), INK, GOLD, 0.04, 1255);
    } });
}
// 8 · round up (comic): $9.99 → $10
{
  const a = at(7), ru = AT(7, "ROUND"), tn = AT(7, "TEN");
  S.push({ id: "roundup", from: a - WHIP, punch: [ru, tn], bg: (c) => comicPage(c, 95),
    draw: (c, f) => {
      priceTag(c, 540, 600, 560, 280, -0.05, "$9.99", span(f, a, a + 12), 1261);
      penArrow(c, [540, 800], [540, 1080], span(f, ru, ru + 10), RED, 12);
      burst(c, 540, 1240, 120, 300, 26, 1262, span(f, tn, tn + 8), GOLD); pow(c, 540, 1240, 260, 160, GOLD, 1263, span(f, tn - 2, tn + 6));
      hero(c, "$10", 540, 1240, f, tn, KEY, 190, -0.04);
    } });
}
S.push(followScene(at(8), AT(8, "MONEY"), AT(8, "FOLLOW")));

const hookCard = (c: Ctx, f: number) => {
  scrapPage(c, 365);
  ransom(c, "1¢", 540, 600, 220, 1271, span(f, 3, 18), 0.12);
  stamp(c, "TRICK?", 540, 980, 150, -0.06, span(f, 26, 38), STAMP, 1272);
};
export const charmMix = makeFilm({ title: "Money Mirage · why prices end in .99 (mixed media)", LINES, scenes: S, hookCard, name: "charmMix" });
void brushLine; void penStrike; void xf; void onCard; void NAVY; void card;
