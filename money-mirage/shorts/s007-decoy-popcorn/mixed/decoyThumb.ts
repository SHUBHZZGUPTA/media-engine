import type { Ctx, Env } from "./core";
import type { Film } from "./film";
import { W, H, RED, KEY, comicPage, grain, ransom, txt, logoChip, penLoop, marker, burst, GOLD } from "./mirageKit";
let LOGO_IMG: CanvasImageSource | undefined;
/** a striped popcorn bucket (marker comic), size s */
const bucket = (c: Ctx, x: number, y: number, s: number, seed: number) => {
  c.save(); c.translate(x, y); c.scale(s, s);
  for (let i = 0; i < 9; i++) { const a = -0.9 + i * 0.22, r = 95 + (i % 3) * 16; marker(c, [[Math.cos(a - 1.57) * 0 + Math.sin(a) * r - 40, -150 - Math.cos(a) * 40], [Math.sin(a) * r + 40, -150 - Math.cos(a) * 40], [Math.sin(a) * r + 30, -110], [Math.sin(a) * r - 30, -110]].map(([px, py]) => [px * 0.9, py]) as [number, number][], "#fff2c4", { seed: seed + i, contour: 4, streak: false, hi: false, shadow: "#e8cf8a" }); }
  marker(c, [[-130, -130], [130, -130], [100, 180], [-100, 180]], "#ffffff", { seed, contour: 8, shadow: "#d9d3c6" });
  c.save(); c.beginPath(); c.moveTo(-130, -130); c.lineTo(130, -130); c.lineTo(100, 180); c.lineTo(-100, 180); c.closePath(); c.clip();
  c.fillStyle = "#e4473a"; for (let k = -3; k <= 3; k++) { c.beginPath(); c.moveTo(k * 58 - 18, -130); c.lineTo(k * 58 + 18, -130); c.lineTo(k * 46 + 14, 180); c.lineTo(k * 46 - 14, 180); c.fill(); }
  c.restore(); c.restore();
};

// s007 thumbnail: DECOY? in ransom tiles, three buckets with the medium circled, a red 84%?, logo chip.
const drawThumb = (c: Ctx, _f: number, env: Env) => {
  c.setTransform(env.scale, 0, 0, env.scale, 0, 0); LOGO_IMG = env.image("logo");
  comicPage(c, 101);
  ransom(c, "DECOY?", 560, 400, 135, 1901, 1, 0.1);
  burst(c, 540, 1000, 300, 520, 30, 1902, 1, GOLD);
  bucket(c, 230, 1060, 0.75, 1903); bucket(c, 540, 1010, 0.95, 1904); bucket(c, 850, 960, 1.15, 1905);
  penLoop(c, 540, 1020, 200, 270, 1, 1906, RED, 14);
  txt(c, "84%?", 540, 1560, 240, KEY, { stroke: 26, rot: -0.04 });
  logoChip(c, LOGO_IMG, 36, 40, 280);
  grain(c, 0, true);
};
export const decoyThumb: Film = {
  meta: { title: "Money Mirage · decoy thumbnail", W, H, fps: 30, bpm: 60, durationFrames: 1, raster: "cpu" },
  assets: { images: { logo: "logo_s.png" } },
  shots: [{ id: "thumb", start: 0, end: 1, draw: drawThumb }],
};
void marker;
