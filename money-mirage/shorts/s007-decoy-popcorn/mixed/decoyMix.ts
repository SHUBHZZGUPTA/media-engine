import { type Ctx } from "./core";
import { Cam, drawPart, order, PLATE, STUD, type Part } from "./toyBrickKit";
import { LINES } from "./s007timing";
import {
  span, clamp01, easeOut, easeIO, back, INK, RED, STAMP, GOLD, KEY, CREAM, NAVY,
  scrapPage, comicPage, theatre, newsPage, card, onCard, tape, cutout, marker,
  penLoop, penStrike, penArrow, stamp, ransom, label, hero, txt, burst, pow, clipping,
  rrect, makeFilm, followScene, timing, brickBg, person, WHIP, HOOK_END, type Scene, type CardSpec,
} from "./mirageKit";

// MONEY MIRAGE · s007 THE DECOY THAT MIGHT BE A MIRAGE, mixed media. The popcorn prices are an
// illustration; the Economist numbers are Ariely's reported classroom test.
const { at, AT } = timing(LINES, "decoyMix");

/** a striped popcorn bucket (marker comic), size s */
const bucket = (c: Ctx, x: number, y: number, s: number, seed: number) => {
  c.save(); c.translate(x, y); c.scale(s, s);
  for (let i = 0; i < 9; i++) { const a = -0.9 + i * 0.22, r = 95 + (i % 3) * 16; marker(c, [[Math.cos(a - 1.57) * 0 + Math.sin(a) * r - 40, -150 - Math.cos(a) * 40], [Math.sin(a) * r + 40, -150 - Math.cos(a) * 40], [Math.sin(a) * r + 30, -110], [Math.sin(a) * r - 30, -110]].map(([px, py]) => [px * 0.9, py]) as [number, number][], "#fff2c4", { seed: seed + i, contour: 4, streak: false, hi: false, shadow: "#e8cf8a" }); }
  marker(c, [[-130, -130], [130, -130], [100, 180], [-100, 180]], "#ffffff", { seed, contour: 8, shadow: "#d9d3c6" });
  c.save(); c.beginPath(); c.moveTo(-130, -130); c.lineTo(130, -130); c.lineTo(100, 180); c.lineTo(-100, 180); c.closePath(); c.clip();
  c.fillStyle = "#e4473a"; for (let k = -3; k <= 3; k++) { c.beginPath(); c.moveTo(k * 58 - 18, -130); c.lineTo(k * 58 + 18, -130); c.lineTo(k * 46 + 14, 180); c.lineTo(k * 46 - 14, 180); c.fill(); }
  c.restore(); c.restore();
};
let PID = 0;
const bar = (x: number, h: number, color: string): Part => ({ id: PID++, color, kind: "prism", foot: [[x, 0], [x + 3, 0], [x + 3, 3], [x, 3]], y0: 0, h, studs: true, step: 0 });

const S: Scene[] = [];
// 1 · hook (comic): three buckets; the medium gets a red "?"
{
  const a = HOOK_END, md = AT(0, "MEDIUM"), dc = AT(0, "DECOY");
  S.push({ id: "hook", from: a, punch: [md, dc], bg: (c) => comicPage(c, 101),
    draw: (c, f) => {
      const up = (k: number) => easeOut(span(f, a + k * 4, a + k * 4 + 12));
      bucket(c, 230, 1040 + (1 - up(0)) * 600, 0.7, 1301); bucket(c, 540, 1000 + (1 - up(1)) * 600, 0.9, 1311); bucket(c, 850, 960 + (1 - up(2)) * 600, 1.1, 1321);
      if (f >= md) penLoop(c, 540, 1010, 190, 260, span(f, md, md + 12), 1331, RED, 10);
      stamp(c, "DECOY?", 540, 500, 130, -0.06, span(f, dc, dc + 8), STAMP, 1332);
    } });
}
// 2 · the prices (scrapbook): three tags; the medium lands at $6.50
{
  const a = at(1), n3 = AT(1, "$3"), n7 = AT(1, "$7"), n65 = AT(1, "$6.50");
  S.push({ id: "prices", from: a - WHIP, punch: [n3, n7, n65], bg: (c) => scrapPage(c, 371),
    draw: (c, f) => {
      bucket(c, 230, 1000, 0.6, 1341); bucket(c, 850, 940, 1.0, 1342);
      label(c, "SMALL $3", 230, 660, 58, span(f, n3, n3 + 8), INK, CREAM, -0.05, 1343); label(c, "LARGE $7", 850, 560, 58, span(f, n7, n7 + 8), INK, CREAM, 0.05, 1344);
      if (f >= n65 - 6) { const d = easeOut(span(f, n65 - 6, n65 + 4)); bucket(c, 540, 300 + 680 * d, 0.8, 1345); label(c, "MEDIUM $6.50", 540, 1330, 60, span(f, n65, n65 + 8), "#ffffff", KEY, 0.03, 1346); }
    } });
}
// 3 · the large looks like a steal (comic): burst on the large; the medium shrinks to "just a prop"
{
  const a = at(2), stl = AT(2, "STEAL"), sl = AT(2, "SELL"), ch = AT(2, "CHEAP");
  S.push({ id: "steal", from: a - WHIP, punch: [stl, ch], bg: (c) => comicPage(c, 103),
    draw: (c, f) => {
      burst(c, 700, 900, 220, 520, 30, 1351, span(f, stl, stl + 8), GOLD); pow(c, 700, 560, 220, 130, GOLD, 1352, span(f, stl, stl + 6)); txt(c, "STEAL!", 700, 560, 76, KEY, { stroke: 10, alpha: span(f, stl + 2, stl + 6), rot: -0.05 });
      bucket(c, 700, 1000, 1.2, 1353);
      const shrink = 1 - 0.35 * easeIO(span(f, sl, sl + 12)); bucket(c, 260, 1080, 0.8 * shrink, 1354);
      if (f >= sl) label(c, "JUST A PROP", 260, 1340, 50, span(f, sl + 4, sl + 12), INK, GOLD, -0.06, 1355);
      if (f >= ch) penArrow(c, [330, 900], [560, 820], span(f, ch, ch + 10), RED, 10);
    } });
}
// 4 · the Economist offer (newsprint): three options in a clipping
{
  const a = at(3), w59 = AT(3, "$59"), p125 = AT(3, "PRINT"), al = AT(3, "ALSO");
  S.push({ id: "offer", from: a - WHIP, punch: [w59, al], bg: (c) => newsPage(c, 131),
    draw: (c, f) => {
      clipping(c, 540, 860, 920, 1000, -0.02, 132, span(f, a, a + 12), [0, 360]);
      stamp(c, "THE OFFER", 540, 440, 80, -0.04, span(f, a + 6, a + 14), "#1d1a17", 133);
      [["WEB", "$59", w59], ["PRINT", "$125", p125], ["PRINT + WEB", "$125", al]].forEach(([n, p, t], i) => { const y = 640 + i * 200, q = span(f, (t as number) - 4, (t as number) + 6); if (q <= 0) return; label(c, n as string, 380, y, 52, q, INK, CREAM, -0.03, 134 + i); txt(c, p as string, 760, y, 90, i === 2 ? KEY : INK, { alpha: q, sc: back(q) }); });
    } });
}
// 5 · 84% vs 32% (toy brick): two bars; the combo bar drops when print-only is removed
{
  const a = at(4), n84 = AT(4, "84%"), rm = AT(4, "REMOVE"), n32 = AT(4, "32%");
  S.push({ id: "bars", from: a - WHIP, punch: [n84, n32], dark: true, bg: brickBg,
    draw: (c, f) => {
      const k = 3.2, q = new Cam(k, 0, 0).p(5 * STUD, 10 * PLATE, 1.5 * STUD), cam = new Cam(k, 540 - q[0], 940 - q[1]);
      drawPart(c, cam, { id: 995, color: "#646464", kind: "prism", foot: [[-1, -1], [11, -1], [11, 4], [-1, 4]], y0: -1, h: 1, studs: true, step: 0 }, 0, 0.7);
      const after = easeIO(span(f, rm, n32)), hCombo = Math.round(34 - (34 - 13) * after), hWeb = Math.round(6 + (27 - 6) * after);
      const live = [{ p: bar(0, Math.max(1, hWeb), "#68C3E2"), dy: 240 * (1 - easeOut(span(f, a + 4, a + 13))) }, { p: bar(6, Math.max(1, hCombo), "#B40000"), dy: 240 * (1 - easeOut(span(f, a + 8, a + 17))) }];
      order(live, cam).forEach((i) => drawPart(c, cam, live[i].p, live[i].dy, 0.7));
      label(c, "WEB", 330, 1240, 54, span(f, a + 10, a + 18), INK, "#ffffff", -0.04, 1361); label(c, "COMBO", 740, 1240, 54, span(f, a + 14, a + 22), INK, "#ffffff", 0.04, 1362);
      hero(c, f < n32 ? "84%" : "32%", 540, 330, f, f < n32 ? n84 : n32, KEY, 180);
      if (f >= rm) stamp(c, "NO PRINT-ONLY", 540, 520, 60, -0.05, span(f, rm, rm + 8), "#ff6b5a", 1363);
    } });
}
// 6 · the twist (toy theatre): student puppets on stage, not subscribers
{
  const a = at(5), tw = AT(5, "TWIST"), sd = AT(5, "STUDENTS");
  S.push({ id: "students", from: a - WHIP, punch: [tw, sd], bg: (c, f) => theatre(c, f, 95),
    draw: (c, f) => {
      ["#d9483b", "#f0b43a", "#3d7fc2", "#3f9a5a"].forEach((cl, i) => { const x = 220 + i * 215, u = easeOut(span(f, a + i * 3, a + i * 3 + 12)); c.save(); c.strokeStyle = "#3b2a18"; c.lineWidth = 7; c.beginPath(); c.moveTo(x, 1160 + (1 - u) * 500); c.lineTo(x, 1720); c.stroke(); c.restore(); person(c, x, 1080 + (1 - u) * 500 + Math.sin((f + i * 8) * 0.4) * 6, 0.75, cl, 1371 + i); });
      stamp(c, "TWIST", 540, 460, 120, -0.06, span(f, tw, tw + 8), STAMP, 1375);
      label(c, "STUDENTS", 540, 1320, 64, span(f, sd, sd + 8), INK, GOLD, 0.03, 1376);
    } });
}
// 7 · retractions and weak effects (newsprint): two clippings stamped RETRACTED; WEAK in real life
{
  const a = at(6), tw = AT(6, "TWO"), rt = AT(6, "RETRACTED"), wk = AT(6, "WEAK");
  S.push({ id: "retracted", from: a - WHIP, punch: [rt, wk], bg: (c) => newsPage(c, 135),
    draw: (c, f) => {
      clipping(c, 330, 720, 520, 640, -0.06, 136, span(f, tw - 6, tw + 6), [-300, 0]); clipping(c, 760, 860, 520, 640, 0.05, 137, span(f, tw, tw + 12), [300, 0]);
      stamp(c, "RETRACTED", 330, 720, 66, -0.2, span(f, rt, rt + 8), STAMP, 138); stamp(c, "RETRACTED", 760, 860, 66, 0.12, span(f, rt + 6, rt + 14), STAMP, 139);
      hero(c, "WEAK", 540, 1300, f, wk, KEY, 170, -0.03);
    } });
}
// 8 · the mirage (scrapbook)
{
  const a = at(7), mg = AT(7, "MIRAGE"), il = AT(7, "ILLUSION");
  const CD: CardSpec = { cx: 540, cy: 900, w: 640, h: 700, rot: -0.03, color: "#efe5cf", seed: 1381, from: [0, 220] };
  S.push({ id: "mirage", from: a - WHIP, punch: [mg, il], bg: (c) => scrapPage(c, 373),
    draw: (c, f) => {
      ransom(c, "MIRAGE", 540, 330, 108, 1382, span(f, mg - 4, mg + 18), 0.1);
      card(c, CD, span(f, a, a + 12)); tape(c, 540, 560, 0.03, 220, span(f, a + 10, a + 16), 1383);
      onCard(c, CD, span(f, a, a + 12), () => bucket(c, 0, 40, 0.9, 1384));
      if (f >= il) { c.save(); c.globalAlpha = 0.45 * span(f, il, il + 10); c.fillStyle = "#efe5cf"; c.fillRect(260, 600, 560, 620); c.restore(); stamp(c, "ILLUSION?", 540, 1240, 90, -0.06, span(f, il, il + 8), STAMP, 1385); }
    } });
}
// 9 · ask yourself (comic): the large, the medium crossed out, a "?"
{
  const a = at(8), fr = AT(8, "FEAR"), wo = AT(8, "WITHOUT");
  S.push({ id: "ask", from: a - WHIP, punch: [fr, wo], bg: (c) => comicPage(c, 105),
    draw: (c, f) => {
      bucket(c, 330, 980, 0.8, 1391); penStrike(c, 170, 1140, 490, 820, span(f, wo - 4, wo + 6), RED, 16);
      bucket(c, 760, 940, 1.15, 1392);
      txt(c, "?", 760, 480, 240, RED, { stroke: 18, sc: back(span(f, wo, wo + 10)), alpha: span(f, wo, wo + 4) });
      label(c, "NO FEAR", 330, 640, 54, span(f, fr, fr + 8), INK, GOLD, -0.05, 1393);
    } });
}
S.push(followScene(at(9), AT(9, "MONEY"), AT(9, "FOLLOW")));

const hookCard = (c: Ctx, f: number) => {
  scrapPage(c, 375);
  ransom(c, "$6.50", 540, 600, 180, 1395, span(f, 3, 22), 0.12);
  stamp(c, "BAIT?", 540, 960, 160, -0.06, span(f, 30, 42), STAMP, 1396);
};
export const decoyMix = makeFilm({ title: "Money Mirage · the decoy (mixed media)", LINES, scenes: S, hookCard, name: "decoyMix" });
void clamp01; void cutout; void NAVY; void rrect;
