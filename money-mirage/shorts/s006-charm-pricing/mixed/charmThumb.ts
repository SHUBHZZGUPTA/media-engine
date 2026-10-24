import type { Ctx, Env } from "./core";
import type { Film } from "./film";
import { W, H, RED, KEY, INK, comicPage, grain, ransom, txt, logoChip, priceTag, penLoop, burst, GOLD } from "./mirageKit";
let LOGO_IMG: CanvasImageSource | undefined;
// s006 thumbnail: 1 CENT TRICK in ransom tiles, a huge $9.99 tag with the 9 circled in red, logo chip.
const drawThumb = (c: Ctx, _f: number, env: Env) => {
  c.setTransform(env.scale, 0, 0, env.scale, 0, 0); LOGO_IMG = env.image("logo");
  comicPage(c, 91);
  ransom(c, "1 CENT", 540, 380, 150, 1281, 1, 0.1); ransom(c, "TRICK", 540, 570, 150, 1282, 1, 0.1);
  burst(c, 560, 1080, 360, 560, 30, 1283, 1, GOLD);
  priceTag(c, 560, 1080, 900, 430, -0.06, "", 1, 1284);
  txt(c, "$9", 460, 1100, 300, INK, { rot: -0.06 }); txt(c, ".99", 800, 1070, 180, INK, { rot: -0.06 });
  penLoop(c, 470, 1100, 210, 180, 1, 1285, RED, 14);
  txt(c, "≠ $10?", 560, 1560, 150, KEY, { stroke: 18, rot: -0.04 });
  logoChip(c, LOGO_IMG, 36, 40, 280);
  grain(c, 0, true);
};
export const charmThumb: Film = {
  meta: { title: "Money Mirage · .99 thumbnail", W, H, fps: 30, bpm: 60, durationFrames: 1, raster: "cpu" },
  assets: { images: { logo: "logo_s.png" } },
  shots: [{ id: "thumb", start: 0, end: 1, draw: drawThumb }],
};
