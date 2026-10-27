import type { Ctx, Env } from "./core";
import type { Film } from "./film";
import { W, H, RED, KEY, INK, GOLD, STAMP, scrapPage, comicPage, grain, ransom, txt, logoChip, penLoop, burst, pow, stamp, label } from "./mirageKit";
import { giftCard } from "./giftMix";
let LOGO_IMG: CanvasImageSource | undefined;
const drawThumb = (c: Ctx, _f: number, env: Env) => {
  c.setTransform(env.scale, 0, 0, env.scale, 0, 0); LOGO_IMG = env.image("logo");
  comicPage(c, 131);
  ransom(c, "PAY BY", 560, 360, 120, 2021, 1, 0.1); ransom(c, "CARD?", 540, 540, 140, 2022, 1, 0.1);
  giftCard(c, 540, 1000, 1.7, -0.06, 1, 2023);
  stamp(c, "SCAM", 540, 1000, 200, -0.14, 1, STAMP, 2024);
  txt(c, "$200M/YR", 540, 1550, 170, KEY, { stroke: 20, rot: -0.04 });
  logoChip(c, LOGO_IMG, 36, 40, 280);
  grain(c, 0, true);
};
export const giftThumb: Film = {
  meta: { title: "Money Mirage · thumbnail", W, H, fps: 30, bpm: 60, durationFrames: 1, raster: "cpu" },
  assets: { images: { logo: "logo_s.png" } },
  shots: [{ id: "thumb", start: 0, end: 1, draw: drawThumb }],
};
void RED; void KEY; void INK; void GOLD; void STAMP; void scrapPage; void comicPage; void ransom; void txt; void penLoop; void burst; void pow; void stamp; void label;
