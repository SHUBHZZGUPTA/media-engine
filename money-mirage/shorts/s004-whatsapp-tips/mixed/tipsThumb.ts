import type { Ctx, Env } from "./core";
import type { Film } from "./film";
import { W, H, STAMP, INK, GOLD, comicPage, grain, ransom, stamp, marker, rrect, txt, bubble, person, burst, label, logoChip } from "./mirageKit";
let LOGO_IMG: CanvasImageSource | undefined;
// s004 thumbnail: FREE? in ransom tiles, a phone shouting TARGET ₹500!, YOU stamped EXIT, logo top-left.
const drawThumb = (c: Ctx, _f: number, env: Env) => {
  c.setTransform(env.scale, 0, 0, env.scale, 0, 0); LOGO_IMG = env.image("logo");
  comicPage(c, 71);
  ransom(c, "FREE?", 560, 400, 165, 931, 1, 0.1);
  burst(c, 470, 900, 330, 520, 30, 932, 1, GOLD);
  c.save(); c.translate(470, 920); c.rotate(-0.06); c.scale(0.9, 0.9);
  marker(c, rrect(560, 900, 70), "#2d3238", { seed: 933, contour: 9, shadow: "#1b1f23" }); c.fillStyle = "#ece5d8"; c.fillRect(-245, -390, 490, 760);
  c.fillStyle = "#3f7a63"; c.fillRect(-245, -390, 490, 90); txt(c, "STOCK TIPS", 0, -345, 38, "#ffffff");
  bubble(c, "TARGET ₹500!", 0, -150, 62, 1, false, 934); bubble(c, "BUY NOW", 30, 20, 58, 1, false, 935);
  c.restore();
  person(c, 860, 1400, 1.25, "#3d7fc2", 936); label(c, "YOU", 860, 1650, 66, 1, INK, GOLD, 0.05, 937);
  stamp(c, "EXIT", 820, 1150, 150, -0.12, 1, STAMP, 938);
  logoChip(c, LOGO_IMG, 36, 40, 280);
  grain(c, 0, true);
};
export const tipsThumb: Film = {
  meta: { title: "Money Mirage · free tip thumbnail", W, H, fps: 30, bpm: 60, durationFrames: 1, raster: "cpu" },
  assets: { images: { logo: "logo_s.png" } },
  shots: [{ id: "thumb", start: 0, end: 1, draw: drawThumb }],
};
