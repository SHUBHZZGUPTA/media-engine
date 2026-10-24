import { rng, type Ctx, type P } from "./core";
import { Cam, drawPart, order, PLATE, STUD, type Part } from "./toyBrickKit";
import { LINES } from "./s004timing";
import {
  span, clamp01, easeOut, easeIO, back, INK, RED, STAMP, GOLD, KEY, CREAM,
  scrapPage, comicPage, theatre, newsPage, card, onCard, tape, cutout, marker, brushLine,
  penLoop, penStrike, penArrow, stamp, ransom, label, hero, txt, burst, pow, clipping,
  rrect, ellipse, xf, makeFilm, followScene, timing, brickBg, bubble, person, lineChart, WHIP, HOOK_END, type Scene, type CardSpec,
} from "./mirageKit";

// MONEY MIRAGE · s004 THE FREE STOCK TIP (WhatsApp pump and dump), mixed media.
const { at, AT } = timing(LINES, "tipsMix");

/** a phone with a group chat (generic messenger, no brand marks) */
const chatPhone = (c: Ctx, x: number, y: number, s: number, rot: number, draw: () => void) => {
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s);
  marker(c, rrect(560, 1000, 70), "#2d3238", { seed: 801, contour: 9, shadow: "#1b1f23" });
  c.fillStyle = "#ece5d8"; c.fillRect(-245, -440, 490, 860);
  c.fillStyle = "#3f7a63"; c.fillRect(-245, -440, 490, 90); txt(c, "STOCK TIPS", 0, -395, 34, "#ffffff");
  draw(); c.restore();
};
/** a puppet member on a stick (toy theatre), with an optional string from above */
const puppet = (c: Ctx, x: number, y: number, s: number, col: string, seed: number, str: number, bob: number) => {
  if (str > 0) { c.save(); c.globalAlpha = str; c.strokeStyle = "#e8dcc0"; c.lineWidth = 3; c.beginPath(); c.moveTo(x, 0); c.lineTo(x, y - 70 * s + bob); c.stroke(); c.restore(); }
  c.save(); c.strokeStyle = "#3b2a18"; c.lineWidth = 8; c.beginPath(); c.moveTo(x, y + 100 * s + bob); c.lineTo(x, 1720); c.stroke(); c.restore();
  person(c, x, y + bob, s, col, seed);
};
let PID = 0;
const col = (x: number, h: number, color: string): Part => ({ id: PID++, color, kind: "prism", foot: [[x, 0], [x + 2, 0], [x + 2, 2], [x, 2]], y0: 0, h, studs: true, step: 0 });

const S: Scene[] = [];
// 1 · hook (comic): the group chat, a FREE TIP bubble, EXIT stamped on "you"
{
  const a = HOOK_END, ft = AT(0, "FREE"), yu = AT(0, "YOU"), ex = AT(0, "EXIT");
  S.push({ id: "hook", from: a, punch: [yu, ex], bg: (c) => comicPage(c, 71),
    draw: (c, f) => {
      chatPhone(c, 540, 820, 1.0, -0.03, () => { bubble(c, "FREE TIP! BUY NOW", -40, -250, 34, span(f, Math.max(a, ft - 6), Math.max(a, ft - 6) + 10), false, 802); bubble(c, "BUY BUY BUY", 60, -140, 40, span(f, ft + 6, ft + 16), false, 803); });
      person(c, 820, 1310, 1.0, "#3d7fc2", 804); label(c, "YOU", 820, 1520, 54, span(f, yu, yu + 8), INK, GOLD, 0.05, 805);
      stamp(c, "EXIT", 820, 1100, 110, -0.1, span(f, ex, ex + 8), STAMP, 806);
    } });
}
// 2 · pump and dump, part one (newsprint): a flat, cheap stock, quietly bought
{
  const a = at(1), pd = AT(1, "PUMP"), op = AT(1, "OPERATORS"), ch = AT(1, "CHEAP");
  S.push({ id: "buy", from: a - WHIP, punch: [pd, ch], bg: (c) => newsPage(c, 101),
    draw: (c, f) => {
      const k = clipping(c, 540, 900, 900, 860, 0.02, 102, span(f, a, a + 12), [0, 360]);
      if (k) { c.save(); c.translate(k.cx, k.cy); c.rotate(k.rot); lineChart(c, 0, -60, 700, 300, [0.1, 0.12, 0.09, 0.11, 0.1, 0.12, 0.11, 0.13], span(f, a + 6, op + 10), INK, 10); c.restore(); }
      stamp(c, "PUMP & DUMP", 540, 420, 84, -0.04, span(f, pd, pd + 8), STAMP, 103);
      label(c, "₹5", 300, 1160, 80, span(f, ch, ch + 8), INK, CREAM, -0.06, 104);
      if (f >= op) { for (let i = 0; i < 5; i++) { const q = span(f, op + i * 4, op + i * 4 + 8); if (q > 0) marker(c, ellipse(680 + i * 12, 1220 - i * 26 - (1 - easeOut(q)) * 200, 70, 22), GOLD, { seed: 105 + i, contour: 5, streak: false }); } }
    } });
}
// 3 · the group lights up (comic): target bubbles and profit screenshots
{
  const a = at(2), lt = AT(2, "LIGHTS"), tg = AT(2, "TARGET"), sc = AT(2, "SCREENSHOTS"), hp = AT(2, "HUGE");
  S.push({ id: "hype", from: a - WHIP, punch: [tg, hp], bg: (c) => comicPage(c, 73),
    draw: (c, f) => {
      chatPhone(c, 540, 820, 1.0, 0.03, () => {
        bubble(c, "TARGET ₹500!", -20, -260, 46, span(f, tg, tg + 8), false, 811);
        bubble(c, "JACKPOT!!", 40, -140, 40, span(f, lt, lt + 8), false, 812);
        for (let i = 0; i < 2; i++) { const q = span(f, sc + i * 6, sc + i * 6 + 10); if (q > 0) { c.save(); c.translate(i ? 90 : -90, 60 + i * 150); c.rotate(i ? 0.06 : -0.05); c.scale(back(q), back(q)); marker(c, rrect(250, 140, 14), "#ffffff", { seed: 813 + i, contour: 5, hi: false, streak: false }); txt(c, i ? "+840%" : "+300%", 0, 0, 56, "#2f9a55"); c.restore(); } }
      });
      burst(c, 540, 820, 470, 640, 34, 814, span(f, hp, hp + 8), GOLD);
    } });
}
// 4 · the planted members (toy theatre): cheering puppets, then their strings appear
{
  const a = at(3), hm = AT(3, "HAPPY"), pl = AT(3, "PLANTED"), hy = AT(3, "HYPE");
  S.push({ id: "puppets", from: a - WHIP, punch: [pl, hy], bg: (c, f) => theatre(c, f, 85),
    draw: (c, f) => {
      const cols = ["#d9483b", "#f0b43a", "#3d7fc2", "#3f9a5a", "#8a5ab8"], str = span(f, pl, pl + 12);
      cols.forEach((cl, i) => { const up = easeOut(span(f, a + i * 3, a + i * 3 + 12)), bob = Math.sin((f + i * 7) * 0.5) * 16 * span(f, hm, hm + 6); puppet(c, 200 + i * 170, 1040 + (1 - up) * 700 + (i % 2) * 60, 0.8, cl, 821 + i, str, bob); });
      if (str > 0) { c.save(); c.globalAlpha = str; marker(c, rrect(900, 70, 20, 540, 130), "#7a4a26", { seed: 830, contour: 7 }); c.restore(); }
      stamp(c, "PLANTED", 540, 520, 110, -0.06, span(f, pl + 4, pl + 12), STAMP, 831);
    } });
}
// 5 · you buy, they sell (toy brick): columns climb; on "sell" the top falls away
{
  const a = at(4), bu = AT(4, "BUY"), jm = AT(4, "JUMPS"), sl = AT(4, "SELL");
  S.push({ id: "bricks", from: a - WHIP, punch: [jm, sl], dark: true, bg: brickBg,
    draw: (c, f) => {
      const life = span(f, a, at(5)), k = 3.3 * (1 + 0.1 * life), q = new Cam(k, 0, 0).p(7 * STUD, 10 * PLATE, 1 * STUD), cam = new Cam(k, 540 - q[0], 900 - q[1]);
      drawPart(c, cam, { id: 900, color: "#646464", kind: "prism", foot: [[-1, -1], [16, -1], [16, 3], [-1, 3]], y0: -1, h: 1, studs: true, step: 0 }, 0, 0.7);
      const hs = [3, 6, 10, 16, 24]; const live: { p: Part; dy: number }[] = [];
      hs.forEach((h, i) => { const land = (i < 2 ? a + 6 : jm - 8) + i * 4; if (f < land - 9) return; const t = clamp01((f - (land - 9)) / 9); const fell = i === 4 && f >= sl ? easeIO(span(f, sl, sl + 14)) * 300 : 0; live.push({ p: col(i * 3, h, i === 4 ? "#B40000" : "#2f9a55"), dy: (f < land ? 240 * (1 - easeOut(t)) : 0) - fell }); });
      order(live, cam).forEach((i) => drawPart(c, cam, live[i].p, live[i].dy, 0.7));
      label(c, "YOU BUY", 300, 1250, 60, span(f, bu, bu + 8), INK, "#ffffff", -0.04, 841);
      if (f >= sl) { stamp(c, "THEY SELL", 720, 420, 84, 0.06, span(f, sl, sl + 8), "#ff6b5a", 842); penArrow(c, [760, 520], [760, 760], span(f, sl + 4, sl + 12), "#ff6b5a", 10); }
    } });
}
// 6 · the crash, the quiet, the new group (comic)
{
  const a = at(5), cr = AT(5, "CRASHES"), qt = AT(5, "QUIET"), nw = AT(5, "NEW");
  S.push({ id: "crash", from: a - WHIP, punch: [cr, nw], bg: (c) => comicPage(c, 75),
    draw: (c, f) => {
      lineChart(c, 540, 560, 760, 420, [0.1, 0.15, 0.3, 0.6, 0.95, 0.4, 0.12, 0.05], span(f, a, cr + 8), KEY, 14);
      if (f >= cr) burst(c, 840, 700, 40, 200, 18, 851, span(f, cr, cr + 6));
      chatPhone(c, 540, 1240, 0.55, -0.04, () => { txt(c, "...", 0, -150, 120, "rgba(36,27,21,0.5)", { alpha: span(f, qt, qt + 6) }); bubble(c, "JOIN NEW GROUP", 0, 60, 40, span(f, nw, nw + 8), false, 852); });
      stamp(c, "NEW", 860, 1060, 90, 0.12, span(f, nw + 4, nw + 12), STAMP, 853);
    } });
}
// 7 · the SEBI order (newsprint): 2025, 59 barred, about ₹58 crore
{
  const a = at(6), y25 = AT(6, "2025"), n59 = AT(6, "59"), yt = AT(6, "YOUTUBE"), n58 = AT(6, "₹58");
  S.push({ id: "order", from: a - WHIP, punch: [y25, n59, n58], bg: (c) => newsPage(c, 105),
    draw: (c, f) => {
      clipping(c, 540, 860, 920, 1000, -0.02, 106, span(f, a, a + 12), [0, -360]);
      stamp(c, "2025", 300, 470, 110, -0.08, span(f, y25, y25 + 8), "#1d1a17", 107);
      label(c, "59 BARRED", 720, 650, 70, span(f, n59, n59 + 8), INK, GOLD, 0.05, 108);
      if (f >= yt) { const q = back(span(f, yt, yt + 10)); c.save(); c.translate(540, 860); c.scale(q, q); marker(c, rrect(300, 200, 50), "#d9483b", { seed: 109, contour: 8 }); marker(c, [[-40, -50], [60, 0], [-40, 50]], "#ffffff", { seed: 110, contour: 6, streak: false }); c.restore(); }
      hero(c, "₹58 CRORE", 540, 1180, f, n58, KEY, 140, -0.03);
    } });
}
// 8 · the mirage (scrapbook): you are the profit
{
  const a = at(7), mg = AT(7, "MIRAGE"), pr = AT(7, "PROFIT"), yu = AT(7, "YOU");
  const CD: CardSpec = { cx: 540, cy: 900, w: 700, h: 760, rot: -0.03, color: "#efe5cf", seed: 861, from: [0, 220] };
  S.push({ id: "mirage", from: a - WHIP, punch: [mg, yu], bg: (c) => scrapPage(c, 341),
    draw: (c, f) => {
      ransom(c, "MIRAGE", 540, 330, 108, 862, span(f, mg - 4, mg + 18), 0.1);
      card(c, CD, span(f, a, a + 12)); tape(c, 540, 530, 0.03, 220, span(f, a + 10, a + 16), 863);
      onCard(c, CD, span(f, a, a + 12), () => person(c, 0, 40, 1.4, "#3d7fc2", 864));
      if (f >= yu) { const q = back(span(f, yu, yu + 10)); c.save(); c.translate(720, 1060); c.rotate(0.2); c.scale(q, q); marker(c, xf([[-120, -50], [120, -50], [120, 50], [-120, 50], [-170, 0]], 0, 0), "#f3e9cf", { seed: 865, contour: 6, shadow: "#d1c19c" }); txt(c, "PROFIT", 10, 0, 50, STAMP); c.restore(); }
      void pr;
    } });
}
// 9 · check SEBI registration (scrapbook): a card stamped REGISTERED? with a tick
{
  const a = at(8), tr = AT(8, "TRUST"), rg = AT(8, "SEBI");
  const CD: CardSpec = { cx: 540, cy: 860, w: 820, h: 560, rot: 0.025, color: "#f2eadb", seed: 871, from: [-160, 160] };
  S.push({ id: "check", from: a - WHIP, punch: [tr, rg], bg: (c) => scrapPage(c, 343),
    draw: (c, f) => {
      card(c, CD, span(f, a, a + 12)); tape(c, 170, 610, -0.6, 180, span(f, a + 10, a + 16), 872); tape(c, 910, 610, 0.6, 180, span(f, a + 12, a + 18), 873);
      onCard(c, CD, span(f, a, a + 12), () => { txt(c, "ADVISER", 0, -150, 64, INK, { alpha: span(f, a + 8, a + 14) }); txt(c, "REG. NO. ?", 0, -40, 72, INK, { alpha: span(f, tr - 4, tr + 4) }); });
      stamp(c, "SEBI-REGISTERED?", 540, 1060, 70, -0.04, span(f, rg, rg + 8), "#2f6f4f", 874);
      if (f >= rg + 10) brushLine(c, [[740, 820], [800, 890], [930, 720]], 22, "#2f9a55", span(f, rg + 10, rg + 20));
    } });
}
// 10 · free is never free (toy theatre): the FREE tag on stage, struck through
{
  const a = at(9), nv = AT(9, "NEVER"), bt = AT(9, "BOUGHT");
  S.push({ id: "free", from: a - WHIP, punch: [nv, bt], bg: (c, f) => theatre(c, f, 87, "#5a4a73", "#3d3256"),
    draw: (c, f) => {
      const up = easeOut(span(f, a, a + 14)); c.save(); c.translate(0, (1 - up) * 600);
      c.strokeStyle = "#3b2a18"; c.lineWidth = 12; c.beginPath(); c.moveTo(540, 1120); c.lineTo(540, 1700); c.stroke();
      cutout(c, xf([[-250, -110], [250, -110], [250, 110], [-250, 110], [-330, 0]], 560, 980, 0), "#fbf6ea", 881, 8);
      txt(c, "FREE", 580, 985, 150, INK); c.restore();
      penStrike(c, 330, 1010, 800, 950, span(f, nv, nv + 8), RED, 18);
      if (f >= bt) { person(c, 230, 1330, 0.7, "#8a5ab8", 882); label(c, "FIRST IN", 230, 1480, 44, span(f, bt, bt + 8), INK, GOLD, -0.05, 883); }
    } });
}
// 11 · follow
S.push(followScene(at(10), AT(10, "MONEY"), AT(10, "FOLLOW")));

const hookCard = (c: Ctx, f: number) => {
  scrapPage(c, 343);
  ransom(c, "₹0 TIP", 540, 600, 170, 27, span(f, 3, 26), 0.1);
  stamp(c, "WHO PAYS?", 540, 980, 120, -0.06, span(f, 34, 46), STAMP, 28);
};
export const tipsMix = makeFilm({ title: "Money Mirage · the free stock tip (mixed media)", LINES, scenes: S, hookCard, name: "tipsMix" });
void rng; void penLoop; void pow; void onCard; void CREAM; void GOLD;
type _P = P;
