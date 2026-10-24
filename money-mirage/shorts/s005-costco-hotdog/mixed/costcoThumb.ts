import type { Ctx, Env } from "./core";
import type { Film } from "./film";
import { W, H, KEY, comicPage, grain, ransom, burst, pow, GOLD, txt, logoChip, marker, rrect, brushLine, INK } from "./mirageKit";
let LOGO_IMG: CanvasImageSource | undefined;
// s005 thumbnail: THE BAIT? in ransom tiles, a hot dog on a fishing hook, $5.9B in red, logo chip.
const drawThumb = (c: Ctx, _f: number, env: Env) => {
  c.setTransform(env.scale, 0, 0, env.scale, 0, 0); LOGO_IMG = env.image("logo");
  comicPage(c, 81);
  ransom(c, "THE", 560, 330, 110, 1161, 1, 0.1); ransom(c, "BAIT?", 540, 520, 160, 1167, 1, 0.1);
  brushLine(c, [[560, 640], [560, 700]], 6, INK);
  burst(c, 540, 930, 260, 470, 30, 1162, 1, GOLD); pow(c, 540, 930, 360, 230, GOLD, 1163, 1);
  c.save(); c.translate(540, 930); c.rotate(-0.12); c.scale(1.5, 1.5);
  marker(c, rrect(360, 120, 60, 0, 20), "#e8b46a", { seed: 1164, contour: 8, shadow: "#c48d45" });
  marker(c, rrect(400, 70, 35, 0, -10), "#c0543a", { seed: 1165, contour: 7, shadow: "#93382a" });
  marker(c, rrect(380, 70, 30, 0, 40), "#e8b46a", { seed: 1166, contour: 7, shadow: "#c48d45", hi: false });
  c.restore();
  brushLine(c, [[560, 700], [560, 820], [600, 860], [640, 820]], 10, "#6b6f74");
  c.save(); c.shadowColor = "rgba(0,0,0,0.35)"; c.shadowBlur = 18; txt(c, "$5.9B", 540, 1460, 260, KEY, { stroke: 28, rot: -0.04 }); c.restore();
  logoChip(c, LOGO_IMG, 36, 40, 280);
  grain(c, 0, true);
};
export const costcoThumb: Film = {
  meta: { title: "Money Mirage · hot dog thumbnail", W, H, fps: 30, bpm: 60, durationFrames: 1, raster: "cpu" },
  assets: { images: { logo: "logo_s.png" } },
  shots: [{ id: "thumb", start: 0, end: 1, draw: drawThumb }],
};
