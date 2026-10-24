import type { Ctx, Env } from "./core";
import type { Film } from "./film";
import { W, H, RED, KEY, scrapPage, grain, card, onCard, tape, penLoop, ransom, txt, chocBar, type CardSpec } from "./mirageKit";
let LOGO_IMG: CanvasImageSource | undefined;

// ---------------------------------------------------------------- the thumbnail (burned into frames 0-2)
// Scrapbook page: the bar on its taped card with one column torn off in mid-air, "SAME PRICE?" in
// ransom tiles, a giant red −10g, a red pen loop round the gap, the logo top-left.
const drawThumb = (c: Ctx, _f: number, env: Env) => {
  c.setTransform(env.scale, 0, 0, env.scale, 0, 0); LOGO_IMG = env.image("logo");
  scrapPage(c, 301);
  ransom(c, "SAME", 540, 330, 150, 611, 1, 0.1); ransom(c, "PRICE?", 540, 520, 150, 612, 1, 0.1);
  const CD: CardSpec = { cx: 540, cy: 980, w: 960, h: 620, rot: -0.03, color: "#f2eadb", seed: 11 };
  card(c, CD, 1); tape(c, 110, 690, -0.6, 200, 1, 41); tape(c, 970, 690, 0.6, 200, 1, 42);
  onCard(c, CD, 1, () => chocBar(c, -30, 0, 122, 6, 3, -0.04, 0.55, 13));
  penLoop(c, 820, 900, 150, 230, 1, 23, RED, 13);
  c.save(); c.shadowColor = "rgba(0,0,0,0.35)"; c.shadowBlur = 18; txt(c, "−10g", 540, 1470, 300, KEY, { stroke: 30, rot: -0.04 }); c.restore();
  if (LOGO_IMG) c.drawImage(LOGO_IMG, 40, 40, 300, 188);
  grain(c, 0, true);
};
export const shrinkThumb: Film = {
  meta: { title: "Money Mirage · shrinkflation thumbnail", W, H, fps: 30, bpm: 60, durationFrames: 1, raster: "cpu" },
  assets: { images: { logo: "logo_s.png" } },
  shots: [{ id: "thumb", start: 0, end: 1, draw: drawThumb }],
};
