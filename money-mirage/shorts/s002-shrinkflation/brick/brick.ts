import { rng, type Ctx, type Env } from "./core";
import type { Film } from "./film";
import { Cam, drawPart, order, PLATE, STUD, type Part } from "./toyBrickKit";
import { INTER900, MUKTA800 } from "./fontdata";
import { LINES } from "./s002timing";

// MONEY MIRAGE · SHRINKFLATION, TOY BRICK. The same 9:16 Short as the chalkboard test, built from
// studded toy bricks (anidoodle's toyBrickKit: ortho 45/30 camera, cube-rule faces, real studs).
// Every part drops in on the word it belongs to and seats with a press-fit; parts that "go missing"
// pop off and fly away. Each idea gets its own set, whip-panned in. The camera never stops: a slow
// push-in on every set and a punch on every hero number. Text is one face: Inter 900 (the rupee
// sign falls back to Mukta, which Inter lacks). One pure function of the frame.

// ---------------------------------------------------------------- fonts (registered before frame 0)
const FONT = "Inter9, Mukta8";
if (typeof FontFace !== "undefined" && typeof document !== "undefined") {
  const faces = [new FontFace("Inter9", `url(data:font/woff2;base64,${INTER900})`), new FontFace("Mukta8", `url(data:font/woff2;base64,${MUKTA800})`)];
  (globalThis as unknown as { __FONTS_READY__: Promise<unknown> }).__FONTS_READY__ = Promise.all(faces.map((f) => f.load().then((l) => { document.fonts.add(l); })));
}

const W = 1080, H = 1920, FPS = 30, BPM = 60;
const sec = (s: number) => s * FPS;
const at = (li: number, wi = 0, off = 0) => sec(LINES[li].words[Math.min(wi, LINES[li].words.length - 1)].s + off);
const wix = (li: number, w: string) => { const i = LINES[li].words.findIndex((x) => x.t.toUpperCase().replace(/[,.?!:]+$/, "").startsWith(w.toUpperCase())); if (i < 0) throw new Error(`brick: no word '${w}' in line ${li}`); return i; };
const AT = (li: number, w: string, off = 0) => at(li, wix(li, w), off);
export const DURATION = Math.ceil(sec(LINES[LINES.length - 1].e + 1.6) / 30) * 30;
const clamp01 = (v: number) => Math.max(0, Math.min(1, v));
const span = (f: number, a: number, b: number) => (b <= a ? (f >= a ? 1 : 0) : clamp01((f - a) / (b - a)));
const easeOut = (t: number) => 1 - (1 - t) ** 3;
const easeIO = (t: number) => (t < 0.5 ? 4 * t * t * t : 1 - (-2 * t + 2) ** 3 / 2);

// real toy-brick colours (the toyBrick plate's table, plus chocolate and tan)
const C = { blue: "#1E5AA8", lbg: "#969696", dbg: "#646464", red: "#B40000", black: "#1B2A34", white: "#F4F4F4", yellow: "#FAC80A", brown: "#5F3109", choc: "#6B3A1E", tan: "#D7BA8C", azure: "#68C3E2", orange: "#D67923", green: "#237841", lime: "#A5CA18", dkred: "#720E0F" };
const BG0 = "#22324a", BG1 = "#101826", INK = "#ffffff", KEY = "#FF4D3D", GOLD = "#FFC23A";

// ---------------------------------------------------------------- parts with a life
// land: frame it seats (it falls for FALL frames before); off: frame it pops off and flies away
type SP = { p: Part; land: number; off?: number };
const FALL = 9, DROP = 240, FLY = 12;
let PID = 0;
const box = (x0: number, z0: number, x1: number, z1: number, y0: number, h: number, color: string, land: number, o: { studs?: boolean; off?: number; round?: boolean } = {}): SP =>
  ({ p: { id: PID++, color, kind: o.round ? "round" : "prism", foot: [[x0, z0], [x1, z0], [x1, z1], [x0, z1]], y0, h, studs: o.studs ?? true, step: 0 }, land, off: o.off });
const state = (s: SP, f: number): { dy: number; a: number } | null => {
  if (f < s.land - FALL) return null;
  if (s.off !== undefined && f >= s.off) { const t = (f - s.off) / FLY; if (t >= 1) return null; return { dy: 30 + easeIO(t) * 420, a: 1 - t }; }
  if (f < s.land) { const t = (f - (s.land - FALL)) / FALL; return { dy: DROP * (1 - easeOut(t)), a: 0.35 + 0.65 * Math.min(1, t / 0.6) }; }
  return { dy: f === s.land ? -1.5 : 0, a: 1 };   // the one-frame press-fit
};

// ---------------------------------------------------------------- text (one face)
const txt = (c: Ctx, s: string, x: number, y: number, size: number, color: string, o: { stroke?: number; align?: CanvasTextAlign; sc?: number; alpha?: number } = {}) => {
  const k = o.sc ?? 1; if (k <= 0 || (o.alpha ?? 1) <= 0) return;
  c.save(); c.translate(x, y); c.scale(k, k); c.globalAlpha = o.alpha ?? 1;
  c.font = `900 ${size}px ${FONT}`; c.textAlign = o.align ?? "center"; c.textBaseline = "middle"; c.lineJoin = "round";
  if (o.stroke) { c.strokeStyle = "rgba(8,12,20,0.92)"; c.lineWidth = o.stroke; c.strokeText(s, 0, 0); }
  c.fillStyle = color; c.fillText(s, 0, 0); c.restore();
};
/** a printed sticker: rounded label with text, popping in at p 0..1 */
const sticker = (c: Ctx, s: string, x: number, y: number, size: number, p: number, fg = "#1b2a34", bg = "#ffffff") => {
  if (p <= 0) return; const k = p < 1 ? easeOut(p) * (1 + 0.15 * Math.sin(p * Math.PI)) : 1;
  c.save(); c.translate(x, y); c.scale(k, k); c.font = `900 ${size}px ${FONT}`; const w = c.measureText(s).width + size * 0.7, h = size * 1.35, r = h * 0.3;
  c.fillStyle = "rgba(0,0,0,0.35)"; rr(c, -w / 2 + 6, -h / 2 + 8, w, h, r); c.fill();
  c.fillStyle = bg; rr(c, -w / 2, -h / 2, w, h, r); c.fill();
  c.fillStyle = fg; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText(s, 0, size * 0.04); c.restore();
};
const rr = (c: Ctx, x: number, y: number, w: number, h: number, r: number) => { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); };
/** a hero number slamming in on its word: big, stroked, with a little shake */
const hero = (c: Ctx, s: string, x: number, y: number, f: number, t: number, color = KEY, size = 170) => {
  if (f < t) return; const p = span(f, t, t + 6), sc = 1.6 - 0.6 * easeOut(p), sh = f < t + 8 ? (rng(f * 7 + 3)() - 0.5) * 14 * (1 - span(f, t + 4, t + 8)) : 0;
  txt(c, s, x + sh, y, size, color, { stroke: 16, sc, alpha: clamp01(p * 3) });
};

// ---------------------------------------------------------------- a set: parts, a camera, its 2D layer
type Set = { id: string; from: number; parts: SP[]; look: [number, number, number]; scale: number; labels: (c: Ctx, f: number, cam: Cam) => void; punch?: number[] };
// camera: world point (LDU) `look` sits at screen (540, 760); scale px/LDU, pushed in slowly over the set
const camFor = (s: Set, f: number, next: number) => {
  const life = clamp01((f - s.from) / Math.max(1, next - s.from)), push = 1 + 0.2 * life;
  let punch = 1; for (const t of s.punch ?? []) if (f >= t && f < t + 14) punch = Math.max(punch, 1 + 0.07 * Math.sin(((f - t) / 14) * Math.PI));
  const k = s.scale * push * punch, [X, Y, Z] = s.look, drift = (life - 0.5) * 90;
  const q = new Cam(k, 0, 0).p(X, Y, Z); return new Cam(k, 540 - q[0] + drift, 760 - q[1]);
};
const L = (x: number, z: number, cam: Cam, y = 0): [number, number] => cam.p(x * STUD, y * PLATE, z * STUD);

// shared props
const plate = (x0: number, z0: number, x1: number, z1: number, color: string, land: number) => box(x0, z0, x1, z1, -1, 1, color, land);
const priceTag = (x: number, z: number, land: number, color = C.white): SP[] => [box(x, z, x + 6, z + 3, 0, 1, color, land, { studs: false }), box(x + 0.6, z + 1.1, x + 1.4, z + 1.9, 1, 1, C.dbg, land + 3, { round: true, studs: false })];

// ---------------------------------------------------------------- the sets, in order
const HOOK_END = sec(2.4), WHIP = 10;
const SETS: Set[] = (() => {
  const S: Set[] = [];
  // 1 · hook: a tag on a plate; +12%; the question
  {
    const a = Math.max(HOOK_END + WHIP, AT(0, "PRICE")), n12 = AT(0, "12%"), br = AT(0, "BRAIN");
    const parts = [plate(0, 0, 10, 7, C.dbg, a), ...priceTag(2, 2, a + 6)];
    S.push({ id: "hook", from: HOOK_END, parts, look: [5 * STUD, 0, 3.5 * STUD], scale: 4.4, punch: [n12, br],
      labels: (c, f, cam) => { const [x, y] = L(5, 3.5, cam, 1); sticker(c, "₹100", x, y - 10, 64, span(f, a + 8, a + 16)); hero(c, "+12%", 540, 300, f, n12); if (f >= br) txt(c, "?", 860, 1180, 260, GOLD, { stroke: 18, sc: 0.6 + 0.4 * easeOut(span(f, br, br + 8)), alpha: span(f, br, br + 4) }); } });
  }
  // 2 · the bar: thirty squares; the last column pops off on "changed"; the tag stays
  {
    const a = at(1), gm = AT(1, "100"), n90 = AT(1, "90"), wr = AT(1, "WRAPPER"), tiny = AT(2, "TINY"), chg = AT(2, "CHANGED"), shr = AT(2, "SHRINKFLATION");
    const parts: SP[] = [plate(-1, -1, 12, 11, C.dbg, a), box(0, 0, 10, 3, 0, 1, C.dkred, a + 4, { studs: false })];
    for (let x = 0; x < 10; x++) for (let z = 0; z < 3; z++) parts.push(box(x, z, x + 1, z + 1, 1, 2, C.choc, a + 6 + Math.round((x + z * 0.5) * 1.6), { off: x === 9 ? chg + z * 2 : undefined }));
    parts.push(...priceTag(2, 6, wr));
    S.push({ id: "bar", from: a - WHIP, parts, look: [6.8 * STUD, 0, 4.2 * STUD], scale: 3.25, punch: [n90, chg],
      labels: (c, f, cam) => {
        const [bx, by] = L(5, 0, cam, 3);
        sticker(c, "100G", bx - 120, by - 110, 72, span(f, gm, gm + 8), "#1b2a34", f >= tiny ? "#d9d9d9" : "#ffffff");
        if (f >= tiny) { const p = span(f, tiny, tiny + 6); c.save(); c.strokeStyle = KEY; c.lineWidth = 12; c.lineCap = "round"; c.beginPath(); c.moveTo(bx - 230, by - 100); c.lineTo(bx - 230 + 220 * p, by - 122); c.stroke(); c.restore(); }
        sticker(c, "90G", bx + 140, by - 120, 92, span(f, n90, n90 + 8), "#1b2a34", GOLD);
        const [tx, ty] = L(5, 7.5, cam, 1); sticker(c, "₹100", tx, ty - 10, 60, span(f, wr + 4, wr + 12));
        sticker(c, "SAME", tx + 250, ty - 60, 48, span(f, shr - 2, shr + 6), "#1b2a34", GOLD);
      } });
  }
  // 3 · how you shop: a shelf, four packs drop on; then the two "sales lost" towers
  {
    const a = at(3), p1 = AT(4, "RAISE"), d1 = AT(4, "DROP"), n12 = AT(4, "1.2%"), hf = AT(4, "HALF");
    const parts: SP[] = [plate(-1, -1, 13, 10, C.dbg, a), box(0, 0, 12, 2, 0, 3, C.lbg, a + 3)];
    const packs = [C.red, C.yellow, C.blue, C.green];
    packs.forEach((col, i) => { parts.push(box(i * 3, 0, i * 3 + 2, 2, 3, 6, col, a + 8 + i * 4)); parts.push(box(i * 3, 0, i * 3 + 2, 2, 9, 3, col, a + 10 + i * 4)); });
    // towers of plates: price +1% → 12 plates lost; size -1% → 6
    for (let k = 0; k < 12; k++) parts.push(box(2, 6, 4, 8, k, 1, C.red, d1 + Math.round(k * 1.2), { studs: k === 11 }));
    for (let k = 0; k < 6; k++) parts.push(box(8, 6, 10, 8, k, 1, C.azure, hf - 6 + k, { studs: k === 5 }));
    S.push({ id: "shop", from: a - WHIP, parts, look: [6 * STUD, 4 * PLATE, 4.5 * STUD], scale: 3.3, punch: [n12, hf],
      labels: (c, f, cam) => {
        const [ax, ay] = L(3, 9.2, cam, 0), [bx, byy] = L(9, 9.2, cam, 0);
        sticker(c, "₹ +1%", ax, ay + 40, 54, span(f, p1, p1 + 8), "#1b2a34", "#ffffff");
        sticker(c, "G -1%", bx, byy + 40, 54, span(f, AT(4, "SHRINK"), AT(4, "SHRINK") + 8), "#1b2a34", "#ffffff");
        const [tx, ty] = L(3, 7, cam, 12); hero(c, "1.2%", tx - 60, ty - 90, f, n12, KEY, 120);
        const [hx, hy] = L(9, 7, cam, 6); hero(c, "HALF", hx + 40, hy - 80, f, hf + 2, "#9fdcf2", 96);
      } });
  }
  // 4 · you watch the price, not the grams: a big tag in a spotlight; a tiny gram brick in the dark
  {
    const a = at(5) + 6, pr = AT(5, "PRICE"), gr = AT(5, "GRAMS");
    const parts: SP[] = [plate(-1, -1, 12, 9, C.dbg, a), box(0, 1, 8, 6, 0, 1, C.white, pr - 2, { studs: false }), box(0.8, 3, 1.8, 4, 1, 1, C.dbg, pr + 2, { round: true, studs: false }), box(10, 6.5, 11, 7.5, 0, 1, C.choc, gr - 2)];
    S.push({ id: "eye", from: a - WHIP, parts, look: [5 * STUD, 0, 4 * STUD], scale: 3.9, punch: [pr, gr],
      labels: (c, f, cam) => {
        const [x, y] = L(4.5, 3.5, cam, 1);
        if (f >= pr) { const g = c.createRadialGradient(x, y, 20, x, y, 420); g.addColorStop(0, `rgba(255,235,170,${0.28 * span(f, pr, pr + 8)})`); g.addColorStop(1, "rgba(255,235,170,0)"); c.fillStyle = g; c.fillRect(0, 0, W, H); }
        txt(c, "₹100", x + 50, y - 6, 140, "#1b2a34", { sc: easeOut(span(f, pr, pr + 8)) });
        const [gx, gy] = L(10.5, 7, cam, 1); sticker(c, "G", gx, gy - 50, 40, span(f, gr, gr + 6)); txt(c, "?", gx + 110, gy - 170, 140, GOLD, { stroke: 14, alpha: span(f, gr + 4, gr + 10) });
      } });
  }
  // 5 · brands shrink: a cereal-style pack of five bricks; on "downsize" the top two pop off; +12% per unit
  {
    const a = at(6), dn = AT(6, "DOWNSIZE"), n12 = AT(6, "12%");
    const parts: SP[] = [plate(-1, -1, 8, 6, C.dbg, a)];
    for (let k = 0; k < 6; k++) parts.push(box(1, 1, 6, 4, k * 3, 3, k % 2 ? C.orange : C.yellow, a + 4 + k * 3, { off: k >= 4 ? dn + (5 - k) * 3 : undefined, studs: k === 5 || k === 3 }));
    S.push({ id: "squeeze", from: a - WHIP, parts, look: [3.5 * STUD, 9 * PLATE, 2.5 * STUD], scale: 3.7, punch: [dn, n12],
      labels: (c, f, cam) => { hero(c, "+12%", 540, 1210, f, n12); if (f >= n12 + 6) txt(c, "PER UNIT", 540, 1330, 64, GOLD, { stroke: 12, alpha: span(f, n12 + 6, n12 + 12) }); } });
  }
  // 6 · the peaks: nine stepped peaks; every other one pops off on "widened the gaps"; then the gavel
  {
    const a = at(7), gp = AT(7, "WIDENED"), sm = AT(7, "SAME"), crt = AT(8, "COURT"), mis = AT(8, "MISLED"), y16 = AT(7, "2016");
    const parts: SP[] = [plate(-1, -1, 19, 12, C.dbg, a), box(0, 0, 18.5, 2, 0, 1, C.tan, a + 3, { studs: false })];
    for (let i = 0; i < 7; i++) {
      const x = i * 2.75, off = i % 2 === 1 ? gp + (i >> 1) * 3 : undefined;
      parts.push(box(x, 0, x + 2, 2, 1, 3, C.tan, a + 6 + i * 2, { off, studs: false }), box(x + 0.5, 0.5, x + 1.5, 1.5, 4, 3, C.tan, a + 8 + i * 2, { off, studs: false }), box(x + 0.75, 0.75, x + 1.25, 1.25, 7, 2, C.tan, a + 10 + i * 2, { off, studs: false }));
    }
    // the gavel: a sound block, the head and handle come down together on "misled"
    parts.push(box(10, 6, 14, 10, 0, 1, C.brown, crt));
    const g0 = mis - 1;
    parts.push(box(11, 6.5, 13, 9.5, 1, 6, C.brown, g0, { studs: false }), box(13, 7.5, 19, 8.5, 3, 2, C.tan, g0, { studs: false }));
    S.push({ id: "peaks", from: a - WHIP, parts, look: [9.5 * STUD, 2 * PLATE, 5.5 * STUD], scale: 2.5, punch: [gp, mis],
      labels: (c, f, cam) => {
        const [x, y] = L(4, 1, cam, 9); sticker(c, "2016", x - 60, y - 130, 60, span(f, y16, y16 + 8), "#1b2a34", "#9fdcf2");
        const [tx, ty] = L(3, 7, cam, 0); sticker(c, "SAME ₹", tx, ty, 60, span(f, sm, sm + 8));
        const [mx, my] = L(12, 8, cam, 0); if (f >= mis) hero(c, "MISLED", mx, my + 150, f, mis, KEY, 120);
      } });
  }
  // 7 · the mirage: the tag never changes; the rise is inside the pack
  {
    const a = at(9), tg = AT(9, "TAG"), ins = AT(9, "INSIDE");
    const parts: SP[] = [plate(-1, -1, 16, 8, C.dbg, a), ...priceTag(0, 3, a + 4)];
    for (let k = 0; k < 4; k++) parts.push(box(9, 2, 14, 5, k * 3, 3, k % 2 ? C.orange : C.yellow, a + 10 + k * 3, { studs: k === 3 }));
    S.push({ id: "mirage", from: a - WHIP, parts, look: [7.5 * STUD, 3 * PLATE, 3.5 * STUD], scale: 3.1, punch: [tg, ins],
      labels: (c, f, cam) => {
        txt(c, "MIRAGE", 540, 250, 120, GOLD, { stroke: 14, sc: easeOut(span(f, AT(9, "MIRAGE"), AT(9, "MIRAGE") + 8)) });
        const [x, y] = L(3, 4.5, cam, 1); sticker(c, "₹100", x, y - 10, 60, span(f, a + 8, a + 16));
        if (f >= tg) { c.save(); c.strokeStyle = GOLD; c.lineWidth = 8; c.globalAlpha = span(f, tg, tg + 6); c.beginPath(); c.ellipse(x, y - 10, 150, 70, -0.1, 0, Math.PI * 2 * span(f, tg, tg + 8)); c.stroke(); c.restore(); }
        const [bx, by] = L(11.5, 3.5, cam, 12);
        if (f >= ins) { const g = c.createRadialGradient(bx, by + 60, 10, bx, by + 60, 340); g.addColorStop(0, `rgba(255,90,70,${0.45 * span(f, ins, ins + 8)})`); g.addColorStop(1, "rgba(255,90,70,0)"); c.fillStyle = g; c.fillRect(0, 0, W, H); }
        hero(c, "+12%", bx, by - 60, f, ins + 2);
      } });
  }
  // 8 · the shelf label: check the price per kilo
  {
    const a = at(10), kilo = AT(10, "KILO");
    const parts: SP[] = [plate(-1, -1, 12, 8, C.dbg, a), box(0, 0, 11, 7, 0, 1, C.white, a + 4, { studs: false })];
    S.push({ id: "shelf", from: a - WHIP, parts, look: [5.5 * STUD, 0, 3.5 * STUD], scale: 3.0, punch: [kilo],
      labels: (c, f, cam) => {
        const [x, y] = L(5.5, 3.5, cam, 1);
        txt(c, "CHOCOLATE 90G", x, y - 178, 40, "#1b2a34", { alpha: span(f, a + 10, a + 16) });
        txt(c, "₹100", x, y - 10, 160, "#1b2a34", { sc: easeOut(span(f, a + 12, a + 20)) });
        txt(c, "₹1,111 / KG", x + 40, y + 120, 62, KEY, { alpha: span(f, AT(10, "PRICE") - 4, AT(10, "PRICE") + 4) });
        if (f >= kilo) { c.save(); c.strokeStyle = KEY; c.lineWidth = 9; c.beginPath(); c.ellipse(x + 40, y + 122, 250, 64, -0.05, -0.5, -0.5 + Math.PI * 2.1 * span(f, kilo, kilo + 10)); c.stroke(); c.restore(); }
      } });
  }
  // 9 · the same tag, twice
  {
    const a = at(11), ex = AT(11, "EXACTLY");
    const parts: SP[] = [plate(-1, -1, 15, 8, C.dbg, a), ...priceTag(0, 2, a + 4), ...priceTag(8, 2, a + 10)];
    S.push({ id: "same", from: a - WHIP, parts, look: [7 * STUD, 0, 3.5 * STUD], scale: 3.0, punch: [ex],
      labels: (c, f, cam) => {
        const [x1, y1] = L(3, 3.5, cam, 1), [x2, y2] = L(11, 3.5, cam, 1);
        sticker(c, "₹100", x1, y1 - 10, 56, span(f, a + 8, a + 14)); sticker(c, "₹100", x2, y2 - 10, 56, span(f, a + 14, a + 20));
        txt(c, "=", (x1 + x2) / 2, (y1 + y2) / 2 - 150, 160, GOLD, { stroke: 14, sc: easeOut(span(f, ex, ex + 8)) });
        sticker(c, "100G", x1, y1 + 150, 52, span(f, ex + 6, ex + 12), "#1b2a34", "#ffffff"); sticker(c, "90G", x2, y2 + 150, 52, span(f, ex + 10, ex + 16), "#ffffff", KEY);
      } });
  }
  // 10 · follow: the logo, a red button pressed on "Follow"
  {
    const a = at(12), fo = AT(12, "FOLLOW");
    const parts: SP[] = [plate(-1, -1, 9, 5, C.dbg, a), box(0, 0, 8, 4, 0, 3, C.red, a + 6, { studs: false })];
    S.push({ id: "follow", from: a - WHIP, parts, look: [4 * STUD, 0, 2 * STUD], scale: 3.8, punch: [fo],
      labels: (c, f, cam) => {
        txt(c, "MONEY", 540, 330, 150, INK, { stroke: 16, sc: easeOut(span(f, AT(12, "MONEY") - 4, AT(12, "MONEY") + 6)) });
        txt(c, "MIRAGE", 540, 490, 150, GOLD, { stroke: 16, sc: easeOut(span(f, AT(12, "MONEY") + 2, AT(12, "MONEY") + 12)) });
        const [x, y] = L(4, 2, cam, 3); txt(c, "FOLLOW", x, y, 86, INK, { stroke: 10, alpha: span(f, a + 10, a + 16) });
        if (f >= fo) { const t = span(f, fo, fo + 14); c.save(); c.strokeStyle = `rgba(255,255,255,${1 - t})`; c.lineWidth = 8; c.beginPath(); c.arc(x + 170, y + 60, 40 + t * 90, 0, Math.PI * 2); c.stroke(); c.restore(); }
      } });
  }
  return S;
})();
((): void => { for (let i = 1; i < SETS.length; i++) if (SETS[i].from <= SETS[i - 1].from + WHIP) throw new Error(`brick: set ${SETS[i].id} starts too soon`); })();
// the button press: the red brick dips on "Follow"
const pressDy = (s: Set, p: SP, f: number) => (s.id === "follow" && p.p.color === C.red && f >= AT(12, "FOLLOW") && f < AT(12, "FOLLOW") + 6 ? -8 : 0);

const drawSet = (c: Ctx, s: Set, f: number, cam: Cam) => {
  const live: { p: Part; dy: number; a: number }[] = [];
  for (const sp of s.parts) { const st = state(sp, f); if (st) live.push({ p: sp.p, dy: st.dy + pressDy(s, sp, f), a: st.a }); }
  // contact shadows first: each seated part's footprint, pushed back and right along the light
  c.save(); c.fillStyle = "rgba(0,0,0,0.22)";
  for (const l of live) { if (l.p.y0 < 0 || l.dy > 40) continue; const b = l.p.foot, y = (l.p.y0 > 0 ? l.p.y0 : 0) * PLATE, o = (l.p.h * PLATE) * 0.35; c.beginPath(); b.forEach(([x, z], i) => { const q = cam.p(x * STUD + o, y, z * STUD - o * 0.6); if (i) c.lineTo(q[0], q[1]); else c.moveTo(q[0], q[1]); }); c.closePath(); c.globalAlpha = l.a * 0.6; c.fill(); }
  c.restore();
  order(live.map((l) => ({ p: l.p, dy: l.dy })), cam).forEach((i) => { const l = live[i]; c.save(); c.globalAlpha = l.a; drawPart(c, cam, l.p, l.dy, 0.7); c.restore(); });
  s.labels(c, f, cam);
};

// captions: Inter 900, words appear as spoken, key words in red; chunks of <= 5 words
type Chunk = { words: { t: string; key: boolean; s: number }[]; from: number; to: number };
const CHUNKS: Chunk[] = (() => {
  const out: Chunk[] = [];
  LINES.forEach((ln) => {
    let cur: Chunk["words"] = []; const flush = () => { if (cur.length) out.push({ words: cur, from: 0, to: 0 }); cur = []; };
    ln.words.forEach((w, i) => { cur.push({ t: w.t.toUpperCase(), key: w.key, s: sec(w.s) }); const left = ln.words.length - 1 - i; if (left < 2) return; if (cur.length >= 5 || (/[.?!:]$/.test(w.t) && cur.length >= 2) || (/,$/.test(w.t) && cur.length >= 3)) flush(); });
    flush();
  });
  out.forEach((c, i) => { c.from = c.words[0].s - 2; c.to = i + 1 < out.length ? out[i + 1].words[0].s - 2 : 1e9; });
  return out;
})();
const CAP = 68, CAP_Y = 1520;
const captions = (c: Ctx, f: number) => {
  const ch = CHUNKS.find((k) => f >= k.from && f < k.to); if (!ch) return;
  c.save(); c.font = `900 ${CAP}px ${FONT}`; const sp = CAP * 0.28, ws = ch.words.map((w) => c.measureText(w.t).width);
  const lines: number[][] = [[]]; let lw = 0; ws.forEach((w, i) => { if (lw && lw + sp + w > 960) { lines.push([]); lw = 0; } lines[lines.length - 1].push(i); lw += (lw ? sp : 0) + w; });
  lines.forEach((ln, li) => {
    const tot = ln.reduce((a, i, k) => a + ws[i] + (k ? sp : 0), 0); let x = 540 - tot / 2; const y = CAP_Y + (li - (lines.length - 1) / 2) * CAP * 1.18;
    ln.forEach((i) => { const w = ch.words[i], p = span(f, w.s - 1, w.s + 3); if (p > 0) txt(c, w.t, x + ws[i] / 2, y, CAP, w.key ? KEY : INK, { stroke: 13, sc: 0.85 + 0.15 * easeOut(p), alpha: clamp01(p * 2) }); x += ws[i] + sp; });
  });
  c.restore();
};

const background = (c: Ctx) => { const g = c.createRadialGradient(540, 760, 80, 540, 900, 1300); g.addColorStop(0, BG0); g.addColorStop(1, BG1); c.fillStyle = g; c.fillRect(0, 0, W, H); };

const draw = (ctx: Ctx, f: number, env: Env) => {
  ctx.setTransform(env.scale, 0, 0, env.scale, 0, 0); background(ctx);
  if (f < HOOK_END + WHIP) {   // the hook card, in words the narrator does not say, then whipped away
    const out = span(f, HOOK_END, HOOK_END + WHIP), dx = -easeIO(out) * W;
    ctx.save(); ctx.translate(dx, 0);
    txt(ctx, "₹100", 540, 620, 220, INK, { stroke: 18, sc: easeOut(span(f, 4, 16)) });
    txt(ctx, "=", 540, 830, 200, GOLD, { stroke: 18, sc: easeOut(span(f, 18, 28)) });
    txt(ctx, "₹112?", 540, 1050, 220, KEY, { stroke: 18, sc: easeOut(span(f, 30, 44)) });
    ctx.restore();
  }
  let k = -1; for (let i = 0; i < SETS.length; i++) if (f >= SETS[i].from) k = i;
  if (k >= 0) {
    const s = SETS[k], next = SETS[k + 1]?.from ?? DURATION, q = span(f, s.from, s.from + WHIP);
    if (q < 1 && k > 0) {   // whip pan: the last set slides off left as this one slides in from the right
      const pv = SETS[k - 1], e = easeIO(q);
      ctx.save(); ctx.translate(-e * W, 0); drawSet(ctx, pv, s.from - 1, camFor(pv, s.from - 1, s.from)); ctx.restore();
      ctx.save(); ctx.translate((1 - e) * W, 0); drawSet(ctx, s, f, camFor(s, f, next)); ctx.restore();
    } else if (q < 1) { ctx.save(); ctx.translate((1 - easeIO(q)) * W, 0); drawSet(ctx, s, f, camFor(s, f, next)); ctx.restore(); }
    else drawSet(ctx, s, f, camFor(s, f, next));
  }
  if (f >= HOOK_END) captions(ctx, f);
};

export const brick: Film = {
  meta: { title: "Money Mirage · shrinkflation (toy brick)", W, H, fps: FPS, bpm: BPM, durationFrames: DURATION, kind: "explainer", raster: "cpu",
    holds: [[Math.floor(sec(LINES[LINES.length - 1].e)), DURATION, "the follow card"]] },
  assets: { images: {} },
  shots: [{ id: "build", start: 0, end: DURATION, draw }],
};
