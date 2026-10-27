import type { Ctx, Env } from "./core";
import type { Film } from "./film";
import { W, H, RED, KEY, INK, GOLD, STAMP, scrapPage, comicPage, grain, ransom, txt, logoChip, penLoop, burst, pow, stamp, label } from "./mirageKit";
import { ticket } from "./dripMix";
let LOGO_IMG: CanvasImageSource | undefined;
const drawThumb = (c: Ctx, _f: number, env: Env) => {
  c.setTransform(env.scale, 0, 0, env.scale, 0, 0); LOGO_IMG = env.image("logo");
  comicPage(c, 151);
  ransom(c, "+$30?", 560, 400, 170, 2041, 1, 0.1);
  burst(c, 540, 960, 300, 520, 30, 2042, 1, GOLD); ticket(c, 540, 960, 1.6, -0.06, "$130", 1, 2043);
  penLoop(c, 470, 1010, 250, 120, 1, 2044, RED, 13);
  txt(c, "WAS $100", 540, 1540, 160, KEY, { stroke: 20, rot: -0.04 });
  logoChip(c, LOGO_IMG, 36, 40, 280);
  grain(c, 0, true);
};
export const dripThumb: Film = {
  meta: { title: "Money Mirage · thumbnail", W, H, fps: 30, bpm: 60, durationFrames: 1, raster: "cpu" },
  assets: { images: { logo: "logo_s.png" } },
  shots: [{ id: "thumb", start: 0, end: 1, draw: drawThumb }],
};
void RED; void KEY; void INK; void GOLD; void STAMP; void scrapPage; void comicPage; void ransom; void txt; void penLoop; void burst; void pow; void stamp; void label;
