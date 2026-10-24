import type { Ctx, Env } from "./core";
import type { Film } from "./film";
import { W, H, RED, KEY, INK, GOLD, STAMP, scrapPage, comicPage, grain, ransom, txt, logoChip, penLoop, burst, pow, stamp, label } from "./mirageKit";
import { note } from "./zimMix";
let LOGO_IMG: CanvasImageSource | undefined;
const drawThumb = (c: Ctx, _f: number, env: Env) => {
  c.setTransform(env.scale, 0, 0, env.scale, 0, 0); LOGO_IMG = env.image("logo");
  scrapPage(c, 391);
  ransom(c, "RICH?", 560, 400, 170, 2011, 1, 0.1);
  note(c, 540, 900, 1.7, -0.06, "100,000,000,000,000", 1, 2012);
  penLoop(c, 640, 870, 400, 100, 1, 2013, RED, 12);
  txt(c, "= 40¢", 540, 1500, 240, KEY, { stroke: 26, rot: -0.04 });
  logoChip(c, LOGO_IMG, 36, 40, 280);
  grain(c, 0, true);
};
export const zimThumb: Film = {
  meta: { title: "Money Mirage · thumbnail", W, H, fps: 30, bpm: 60, durationFrames: 1, raster: "cpu" },
  assets: { images: { logo: "logo_s.png" } },
  shots: [{ id: "thumb", start: 0, end: 1, draw: drawThumb }],
};
void RED; void KEY; void INK; void GOLD; void STAMP; void scrapPage; void comicPage; void ransom; void txt; void penLoop; void burst; void pow; void stamp; void label;
