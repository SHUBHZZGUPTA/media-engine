import type { Ctx, Env } from "./core";
import type { Film } from "./film";
import { W, H, RED, KEY, INK, GOLD, STAMP, scrapPage, comicPage, grain, ransom, txt, logoChip, penLoop, burst, pow, stamp, label } from "./mirageKit";
import { tulip, house } from "./tulipMix";
let LOGO_IMG: CanvasImageSource | undefined;
const drawThumb = (c: Ctx, _f: number, env: Env) => {
  c.setTransform(env.scale, 0, 0, env.scale, 0, 0); LOGO_IMG = env.image("logo");
  scrapPage(c, 411);
  ransom(c, "1 BULB", 560, 380, 130, 2031, 1, 0.1);
  tulip(c, 330, 1000, 1.7, 2032, -0.05); house(c, 800, 1000, 1.5, 2033);
  txt(c, "=", 570, 1000, 180, INK);
  stamp(c, "MYTH?", 540, 1560, 170, -0.06, 1, STAMP, 2034);
  logoChip(c, LOGO_IMG, 36, 40, 280);
  grain(c, 0, true);
};
export const tulipThumb: Film = {
  meta: { title: "Money Mirage · thumbnail", W, H, fps: 30, bpm: 60, durationFrames: 1, raster: "cpu" },
  assets: { images: { logo: "logo_s.png" } },
  shots: [{ id: "thumb", start: 0, end: 1, draw: drawThumb }],
};
void RED; void KEY; void INK; void GOLD; void STAMP; void scrapPage; void comicPage; void ransom; void txt; void penLoop; void burst; void pow; void stamp; void label;
