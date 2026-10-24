import type { Ctx, Env } from "./core";
import type { Film } from "./film";
import { W, H, RED, KEY, INK, GOLD, STAMP, scrapPage, comicPage, grain, ransom, txt, logoChip, penLoop, burst, pow, stamp, label } from "./mirageKit";
import { gent } from "./ponziMix";
let LOGO_IMG: CanvasImageSource | undefined;
const drawThumb = (c: Ctx, _f: number, env: Env) => {
  c.setTransform(env.scale, 0, 0, env.scale, 0, 0); LOGO_IMG = env.image("logo");
  comicPage(c, 111);
  ransom(c, "TOO GOOD?", 560, 400, 92, 2001, 1, 0.1);
  burst(c, 540, 960, 300, 520, 30, 2002, 1, GOLD); gent(c, 540, 1000, 2.0, 2003);
  pow(c, 800, 700, 200, 120, GOLD, 2004, 1); txt(c, "+50%", 800, 700, 90, KEY, { stroke: 10, rot: -0.06 });
  txt(c, "$20M LOST", 540, 1560, 170, KEY, { stroke: 20, rot: -0.04 });
  logoChip(c, LOGO_IMG, 36, 40, 280);
  grain(c, 0, true);
};
export const ponziThumb: Film = {
  meta: { title: "Money Mirage · thumbnail", W, H, fps: 30, bpm: 60, durationFrames: 1, raster: "cpu" },
  assets: { images: { logo: "logo_s.png" } },
  shots: [{ id: "thumb", start: 0, end: 1, draw: drawThumb }],
};
void RED; void KEY; void INK; void GOLD; void STAMP; void scrapPage; void comicPage; void ransom; void txt; void penLoop; void burst; void pow; void stamp; void label;
