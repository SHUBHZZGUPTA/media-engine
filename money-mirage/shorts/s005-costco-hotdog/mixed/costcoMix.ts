import { type Ctx, type P } from "./core";
import { Cam, drawPart, order, PLATE, STUD, type Part } from "./toyBrickKit";
import { LINES } from "./s005timing";
import {
  span, clamp01, easeOut, easeIO, back, INK, RED, STAMP, GOLD, KEY, CREAM, NAVY,
  scrapPage, comicPage, theatre, newsPage, card, onCard, tape, cutout, marker, brushLine,
  penLoop, penStrike, penArrow, stamp, ransom, label, hero, txt, burst, pow, clipping,
  rrect, ellipse, rect, xf, makeFilm, followScene, timing, brickBg, bubble, person, lineChart, WHIP, HOOK_END, type Scene, type CardSpec,
} from "./mirageKit";

// MONEY MIRAGE · s005 THE $1.50 HOT DOG (loss leader + membership), mixed media. Generic warehouse
// store and food: no logos or brand marks are drawn.
const { at, AT } = timing(LINES, "costcoMix");

const hotdog = (c: Ctx, x: number, y: number, s: number, rot = 0, seed = 1001) => {
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s);
  marker(c, rrect(360, 120, 60, 0, 20), "#e8b46a", { seed, contour: 8, shadow: "#c48d45" });
  marker(c, rrect(400, 70, 35, 0, -10), "#c0543a", { seed: seed + 1, contour: 7, shadow: "#93382a" });
  const m: P[] = []; for (let k = 0; k <= 14; k++) m.push([-150 + k * 21.4, -16 + (k % 2 ? -14 : 10)]); brushLine(c, m, 11, "#f2c53d");
  marker(c, rrect(380, 70, 30, 0, 40), "#e8b46a", { seed: seed + 2, contour: 7, shadow: "#c48d45", hi: false });
  c.restore();
};
const cup = (c: Ctx, x: number, y: number, s: number, seed = 1011) => {
  c.save(); c.translate(x, y); c.scale(s, s);
  marker(c, [[-90, -140], [90, -140], [70, 150], [-70, 150]], "#e4473a", { seed, contour: 8 });
  marker(c, rrect(210, 36, 16, 0, -150), "#f6efe0", { seed: seed + 1, contour: 7, streak: false });
  brushLine(c, [[20, -168], [50, -280], [90, -300]], 14, "#ffffff"); brushLine(c, [[20, -168], [50, -280], [90, -300]], 5, INK);
  c.restore();
};
const memberCard = (c: Ctx, x: number, y: number, s: number, rot: number, p: number, seed = 1021) => {
  if (p <= 0) return; const k = back(p); c.save(); c.translate(x, y); c.rotate(rot); c.scale(k * s, k * s);
  marker(c, rrect(520, 320, 30), "#2a5ea8", { seed, contour: 8, shadow: "#1d4580" });
  c.fillStyle = "#e4473a"; c.fillRect(-260, -110, 520, 60); txt(c, "MEMBER", 0, -78, 46, "#ffffff");
  marker(c, rrect(110, 130, 14, -170, 50), "#e8c9a6", { seed: seed + 1, contour: 5, streak: false, hi: false });
  c.fillStyle = "rgba(255,255,255,0.8)"; c.fillRect(-80, 20, 250, 18); c.fillRect(-80, 60, 190, 18); c.fillRect(-80, 100, 220, 18);
  c.restore();
};
const store = (c: Ctx, x: number, y: number, seed = 1031) => {
  cutout(c, [[x - 330, y + 220], [x - 330, y - 120], [x - 200, y - 220], [x + 200, y - 220], [x + 330, y - 120], [x + 330, y + 220]], "#8fa3b0", seed, 8);
  cutout(c, rrect(220, 230, 10, x, y + 100), "#3b4650", seed + 1, 3);
  cutout(c, rrect(380, 80, 12, x, y - 120), "#e4473a", seed + 2, 4); txt(c, "WAREHOUSE", x, y - 120, 44, "#ffffff");
};
/** a marker pie chart with a share q (0..1) filled in red from 12 o'clock */
const pie = (c: Ctx, x: number, y: number, r: number, q: number, seed = 1041) => {
  marker(c, ellipse(x, y, r, r, 60), "#f3e9cf", { seed, contour: 8, shadow: "#d1c19c", streak: false });
  if (q > 0) { c.save(); c.beginPath(); c.moveTo(x, y); c.arc(x, y, r - 4, -Math.PI / 2, -Math.PI / 2 + q * Math.PI * 2); c.closePath(); c.fillStyle = KEY; c.fill(); c.restore(); c.strokeStyle = INK; c.lineWidth = 6; c.beginPath(); c.moveTo(x, y - r); c.lineTo(x, y); c.lineTo(x + Math.cos(-Math.PI / 2 + q * 6.283) * r, y + Math.sin(-Math.PI / 2 + q * 6.283) * r); c.stroke(); }
};
let PID = 0;
const bk = (x: number, z: number, y0: number, color: string): Part => ({ id: PID++, color, kind: "prism", foot: [[x, z], [x + 2, z], [x + 2, z + 2], [x, z + 2]], y0, h: 3, studs: true, step: 0 });

const S: Scene[] = [];
// 1 · hook (comic): the combo, $1.50 on a pow, 1985 stamped
{
  const a = HOOK_END, n150 = AT(0, "$1.50"), y85 = AT(0, "1985");
  S.push({ id: "hook", from: a, punch: [y85], bg: (c) => comicPage(c, 81),
    draw: (c, f) => {
      const up = easeOut(span(f, a, a + 14)); hotdog(c, 420, 1120 + (1 - up) * 500, 1.3, -0.08); cup(c, 830, 1060 + (1 - up) * 500, 1.0);
      burst(c, 540, 470, 150, 380, 28, 1051, span(Math.max(f, a), a, a + 8)); pow(c, 540, 470, 300, 190, GOLD, 1052, span(f, a, a + 8));
      txt(c, "$1.50", 540, 470, 150, KEY, { stroke: 16, rot: -0.05, alpha: span(f, Math.max(a, n150), Math.max(a, n150) + 4), sc: 1 });
      stamp(c, "SINCE 1985", 540, 760, 80, 0.05, span(f, y85, y85 + 8), NAVY, 1053);
    } });
}
// 2 · inflation says $4.50 (newsprint)
{
  const a = at(1), inf = AT(1, "INFLATION"), n450 = AT(1, "$4.50"), mv = AT(1, "MOVED");
  S.push({ id: "inflation", from: a - WHIP, punch: [n450, mv], bg: (c) => newsPage(c, 111),
    draw: (c, f) => {
      const k = clipping(c, 540, 880, 920, 900, -0.02, 112, span(f, a, a + 12), [0, 360]);
      if (k) { c.save(); c.translate(k.cx, k.cy); c.rotate(k.rot);
        lineChart(c, 0, -40, 700, 380, [0.1, 0.18, 0.27, 0.36, 0.45, 0.56, 0.7, 0.85, 0.95], span(f, inf - 4, n450 + 4), INK, 10);
        brushLine(c, [[-350, 120], [350, 120]], 12, KEY, span(f, mv - 6, mv + 8)); txt(c, "1985", -330, 210, 40, INK); txt(c, "2026", 330, 210, 40, INK); c.restore(); }
      hero(c, "$4.50", 720, 470, f, n450, "#2f6f4f", 130, 0.04);
      label(c, "STILL $1.50", 540, 1250, 64, span(f, mv, mv + 8), "#ffffff", KEY, -0.03, 113);
    } });
}
// 3 · the founder's warning (toy theatre): two puppets and a "!!!"
{
  const a = at(2), fd = AT(2, "FOUNDER"), sc = AT(2, "SUCCESSOR"), kl = AT(2, "KILL");
  S.push({ id: "founder", from: a - WHIP, punch: [kl], bg: (c, f) => theatre(c, f, 89),
    draw: (c, f) => {
      const up1 = easeOut(span(f, fd - 8, fd + 6)), up2 = easeOut(span(f, sc - 8, sc + 6)), shake = f >= kl && f < kl + 10 ? Math.sin(f * 2.4) * 10 : 0;
      c.save(); c.strokeStyle = "#3b2a18"; c.lineWidth = 8; [[330, up1], [760, up2]].forEach(([x, u]) => { c.beginPath(); c.moveTo(x, 1180 + (1 - u) * 700); c.lineTo(x, 1720); c.stroke(); }); c.restore();
      person(c, 330 + shake, 1060 + (1 - up1) * 700, 1.0, "#6a4c9c", 1061); person(c, 760, 1060 + (1 - up2) * 700, 1.0, "#3f9a5a", 1062);
      label(c, "FOUNDER", 330, 1290, 44, span(f, fd, fd + 8), INK, CREAM, -0.04, 1063); label(c, "SUCCESSOR", 760, 1290, 44, span(f, sc, sc + 8), INK, CREAM, 0.04, 1064);
      bubble(c, "!!!", 420, 800, 90, span(f, kl - 2, kl + 8), false, 1065);
      hotdog(c, 560, 560, 0.7, 0.1 + Math.sin(f * 0.1) * 0.05, 1066);
    } });
}
// 4 · you are the product (comic)
{
  const a = at(3), pr = AT(3, "PRODUCT"), yu = AT(3, "YOU");
  S.push({ id: "product", from: a - WHIP, punch: [pr, yu], bg: (c) => comicPage(c, 83),
    draw: (c, f) => {
      hotdog(c, 330, 560, 0.9, -0.1); label(c, "PRODUCT?", 330, 760, 60, span(f, pr - 4, pr + 6), INK, CREAM, -0.05, 1071); penStrike(c, 180, 790, 480, 730, span(f, yu - 4, yu + 4), RED, 12);
      person(c, 720, 1080, 1.4, "#3d7fc2", 1072);
      if (f >= yu) { const q = back(span(f, yu, yu + 10)); c.save(); c.translate(820, 1230); c.rotate(0.2); c.scale(q, q); marker(c, [[-130, -50], [130, -50], [130, 50], [-130, 50], [-180, 0]], "#f3e9cf", { seed: 1073, contour: 6, shadow: "#d1c19c" }); txt(c, "PRODUCT", 10, 0, 50, STAMP); c.restore(); }
    } });
}
// 5 · the loss leader (toy theatre): the store; shoppers pulled toward the hot-dog sign
{
  const a = at(4), ll = AT(4, "LOSS"), pl = AT(4, "PULLS"), st = AT(4, "STORE");
  S.push({ id: "leader", from: a - WHIP, punch: [ll, st], bg: (c, f) => theatre(c, f, 91, "#4d6a5a", "#344a3e"),
    draw: (c, f) => {
      const up = easeOut(span(f, a, a + 14)); c.save(); c.translate(0, (1 - up) * 500); store(c, 700, 900); c.restore();
      hotdog(c, 700, 520, 0.6, Math.sin(f * 0.15) * 0.08);
      stamp(c, "LOSS LEADER", 330, 420, 64, -0.08, span(f, ll, ll + 8), STAMP, 1081);
      const pull = easeIO(span(f, pl - 6, st + 10));
      ["#d9483b", "#f0b43a", "#3d7fc2"].forEach((cl, i) => { const x = 160 + i * 90 + pull * (430 - i * 40), y = 1320 + (i % 2) * 30; c.save(); c.strokeStyle = "#3b2a18"; c.lineWidth = 7; c.beginPath(); c.moveTo(x, y + 80); c.lineTo(x, 1720); c.stroke(); c.restore(); person(c, x, y, 0.6, cl, 1082 + i); });
    } });
}
// 6 · 245 million combos (toy brick): a tower climbing, red and yellow
{
  const a = at(5), n245 = AT(5, "245"), cb = AT(5, "COMBOS");
  S.push({ id: "tower", from: a - WHIP, punch: [n245, cb], dark: true, bg: brickBg,
    draw: (c, f) => {
      const life = span(f, a, at(6)), k = 2.6 * (1 + 0.12 * life), q = new Cam(k, 0, 0).p(4 * STUD, 18 * PLATE, 3 * STUD), cam = new Cam(k, 540 - q[0], 1000 - q[1]);
      drawPart(c, cam, { id: 990, color: "#646464", kind: "prism", foot: [[-1, -1], [9, -1], [9, 7], [-1, 7]], y0: -1, h: 1, studs: true, step: 0 }, 0, 0.7);
      const live: { p: Part; dy: number }[] = [];
      for (let n = 0; n < 36; n++) { const x = (n % 3) * 3, z = Math.floor(n / 3) % 2 ? 3 : 0, lvl = Math.floor(n / 6), land = a + 4 + n * 2; if (f < land - 9) continue; const t = clamp01((f - (land - 9)) / 9); live.push({ p: bk(x, z, lvl * 3, lvl % 2 ? "#FAC80A" : "#B40000"), dy: f < land ? 260 * (1 - easeOut(t)) : 0 }); }
      order(live, cam).forEach((i) => drawPart(c, cam, live[i].p, live[i].dy, 0.7));
      hero(c, "245 MILLION", 540, 330, f, n245, "#FAC80A", 110);
      label(c, "COMBOS / YEAR", 540, 1290, 56, span(f, cb, cb + 8), INK, "#ffffff", 0.03, 1091);
    } });
}
// 7 · membership (scrapbook): the card taped down, MEMBERS ONLY stamped
{
  const a = at(6), gi = AT(6, "GET"), mb = AT(6, "MEMBERSHIP");
  const CD: CardSpec = { cx: 540, cy: 860, w: 820, h: 620, rot: -0.025, color: "#f2eadb", seed: 1101, from: [-120, 200] };
  S.push({ id: "member", from: a - WHIP, punch: [mb], bg: (c) => scrapPage(c, 351),
    draw: (c, f) => {
      card(c, CD, span(f, a, a + 12)); tape(c, 170, 570, -0.6, 180, span(f, a + 10, a + 16), 1102); tape(c, 910, 570, 0.6, 180, span(f, a + 12, a + 18), 1103);
      memberCard(c, 540, 860, 1.15, 0.04, span(f, gi, gi + 12));
      stamp(c, "MEMBERS ONLY", 540, 1240, 84, -0.05, span(f, mb, mb + 8), STAMP, 1104);
    } });
}
// 8 · $5.9 billion in fees (newsprint)
{
  const a = at(7), lt = AT(7, "LATEST"), n59 = AT(7, "$5.9"), fe = AT(7, "FEES");
  S.push({ id: "fees", from: a - WHIP, punch: [n59, fe], bg: (c) => newsPage(c, 113),
    draw: (c, f) => {
      clipping(c, 540, 860, 920, 980, 0.02, 114, span(f, a, a + 12), [0, -360]);
      stamp(c, "ANNUAL REPORT", 540, 470, 70, -0.03, span(f, lt, lt + 8), "#1d1a17", 115);
      memberCard(c, 540, 800, 0.8, -0.06, span(f, a + 6, a + 16), 1111);
      hero(c, "$5.9 BILLION", 540, 1120, f, n59, KEY, 120, -0.02);
      label(c, "FEES ALONE", 540, 1270, 58, span(f, fe, fe + 8), INK, GOLD, 0.03, 116);
    } });
}
// 9 · two-thirds of the profit (comic): the pie fills
{
  const a = at(8), tt = AT(8, "TWO"), pf = AT(8, "PROFIT");
  S.push({ id: "pie", from: a - WHIP, punch: [tt, pf], bg: (c) => comicPage(c, 85),
    draw: (c, f) => {
      pie(c, 540, 760, 320, (2 / 3) * easeIO(span(f, a + 4, tt + 8)));
      hero(c, "≈ 2/3", 540, 1240, f, tt, KEY, 150);
      label(c, "OF ITS PROFIT", 540, 1390, 56, span(f, pf, pf + 8), INK, CREAM, -0.03, 1121);
    } });
}
// 10 · the mirage (scrapbook): the hot dog card → arrow → the membership
{
  const a = at(9), mg = AT(9, "MIRAGE"), ls = AT(9, "LOSING"), sl = AT(9, "SELLING");
  const C1: CardSpec = { cx: 300, cy: 860, w: 470, h: 520, rot: 0.03, color: "#efe5cf", seed: 1131, from: [-200, 100] }, C2: CardSpec = { cx: 790, cy: 880, w: 470, h: 560, rot: -0.035, color: "#e7d9c0", seed: 1132, from: [200, 100] };
  S.push({ id: "mirage", from: a - WHIP, punch: [mg, sl], bg: (c) => scrapPage(c, 353),
    draw: (c, f) => {
      ransom(c, "MIRAGE", 540, 330, 108, 1133, span(f, mg - 4, mg + 18), 0.1);
      card(c, C1, span(f, a, a + 12)); onCard(c, C1, span(f, a, a + 12), () => hotdog(c, 0, 0, 0.9, -0.1, 1134)); tape(c, 300, 610, 0.05, 160, span(f, a + 10, a + 16), 1135);
      if (f >= ls) stamp(c, "NOT A LOSS", 300, 1060, 52, -0.08, span(f, ls, ls + 8), STAMP, 1136);
      card(c, C2, span(f, sl - 10, sl + 2)); onCard(c, C2, span(f, sl - 10, sl + 2), () => memberCard(c, 0, 0, 0.75, 0.04, 1, 1137)); tape(c, 790, 610, -0.05, 160, span(f, sl, sl + 6), 1138);
      penArrow(c, [470, 760], [600, 760], span(f, sl - 4, sl + 6), RED, 10);
    } });
}
// 11 · ask what it's selling (comic): a too-good deal tag under a red "?"
{
  const a = at(10), tg = AT(10, "GOOD"), rs = AT(10, "REALLY");
  S.push({ id: "ask", from: a - WHIP, punch: [tg, rs], bg: (c) => comicPage(c, 87),
    draw: (c, f) => {
      burst(c, 540, 700, 180, 420, 28, 1141, span(f, a, a + 8), GOLD); pow(c, 540, 700, 300, 190, GOLD, 1142, span(f, a, a + 8)); txt(c, "DEAL!", 540, 700, 120, KEY, { stroke: 14, rot: -0.05, alpha: span(f, a + 2, a + 6) });
      penLoop(c, 540, 700, 360, 240, span(f, tg, tg + 12), 1143, RED, 10);
      txt(c, "?", 540, 1180, 300, RED, { stroke: 22, sc: back(span(f, rs, rs + 10)), alpha: span(f, rs, rs + 4) });
    } });
}
S.push(followScene(at(11), AT(11, "MONEY"), AT(11, "FOLLOW")));

const hookCard = (c: Ctx, f: number) => {
  scrapPage(c, 355);
  ransom(c, "WHY SO", 540, 560, 130, 1151, span(f, 3, 22), 0.1);
  ransom(c, "CHEAP?", 540, 780, 130, 1152, span(f, 20, 42), 0.1);
  penLoop(c, 540, 780, 340, 140, span(f, 44, 62), 1153, RED, 12);
};
export const costcoMix = makeFilm({ title: "Money Mirage · the $1.50 hot dog (mixed media)", LINES, scenes: S, hookCard, name: "costcoMix" });
void rect; void xf; void onCard; void cutout; void penArrow;
