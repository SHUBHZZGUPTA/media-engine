import type { Ctx, Env } from "./core";
import type { Film } from "./film";
import { W, H, RED, KEY, INK, scrapPage, grain, card, onCard, tape, penStrike, ransom, txt, priceTag, type CardSpec } from "./mirageKit";
let LOGO_IMG: CanvasImageSource | undefined;
// s003 thumbnail: FAKE DISCOUNT? in ransom tiles, a taped tag with ₹1,999 struck out, a giant red ₹999, logo top-left.
const drawThumb = (c: Ctx, _f: number, env: Env) => {
  c.setTransform(env.scale, 0, 0, env.scale, 0, 0); LOGO_IMG = env.image("logo");
  scrapPage(c, 321);
  ransom(c, "FAKE", 540, 330, 160, 621, 1, 0.1); ransom(c, "DISCOUNT?", 540, 530, 92, 622, 1, 0.1);
  const CD: CardSpec = { cx: 540, cy: 960, w: 900, h: 520, rot: 0.025, color: "#f2eadb", seed: 611 };
  card(c, CD, 1); tape(c, 140, 720, -0.6, 200, 1, 612); tape(c, 940, 720, 0.6, 200, 1, 613);
  onCard(c, CD, 1, () => priceTag(c, 40, 0, 640, 300, -0.05, "", 1, 601));
  txt(c, "₹1,999", 570, 960, 150, INK, { rot: -0.03 }); penStrike(c, 300, 1010, 860, 900, 1, RED, 22);
  c.save(); c.shadowColor = "rgba(0,0,0,0.35)"; c.shadowBlur = 18; txt(c, "₹999", 540, 1460, 300, KEY, { stroke: 30, rot: -0.04 }); c.restore();
  if (LOGO_IMG) c.drawImage(LOGO_IMG, 40, 40, 300, 188);
  grain(c, 0, true);
};
export const discountThumb: Film = {
  meta: { title: "Money Mirage · was-price thumbnail", W, H, fps: 30, bpm: 60, durationFrames: 1, raster: "cpu" },
  assets: { images: { logo: "logo_s.png" } },
  shots: [{ id: "thumb", start: 0, end: 1, draw: drawThumb }],
};
