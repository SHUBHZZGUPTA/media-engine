#!/usr/bin/env python3
"""3D sea-floor relief assets for the Mariana Trench terrain clips (map3d clip.html, mode "terrain").

Source: AWS Terrarium elevation tiles (fetched by jobs/fetch/mt-dem.json); in the ocean they carry bathymetry.
The relief is the sea floor itself: the deepest point maps to 0 and sea level to 1, so the trench is a real canyon.
Colour = a depth ramp (shallow turquoise -> abyssal navy -> near-black at hadal depths), land in sand/green.
Usage: python3 prep_bathy.py   (writes art/map3d/: dem.png, dem8.png, ne.jpg, hs.png, mask_none.png, globe.jpg, bathy.json)
"""
import glob, json, math, os, shutil
import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..", "..")
J = json.load(open(os.path.join(ROOT, "jobs", "fetch", "mt-dem.json"))); F = os.path.join(ROOT, "outputs", "fetch", "mt-dem")
A = os.path.join(HERE, "art", "map3d"); os.makedirs(A, exist_ok=True)
L0, L1, B0, B1 = J["bbox"]; ZM = J["zoom"]; N = 2 ** ZM
tiles = {}
for f in glob.glob(os.path.join(F, f"dem_{ZM}_*.png")):
    _, _, x, y = os.path.basename(f)[:-4].split("_"); tiles[(int(x), int(y))] = np.array(Image.open(f).convert("RGB")).astype(np.float64)
print("tiles", len(tiles), "of", len(J["files"]))
W, H = 2048, int(2048 * (B1 - B0) / ((L1 - L0) * math.cos(math.radians((B0 + B1) / 2))))
LON, LAT = np.meshgrid(np.linspace(L0, L1, W), np.linspace(B1, B0, H))
X = (LON + 180) / 360 * N; Y = (1 - np.log(np.tan(np.radians(LAT)) + 1 / np.cos(np.radians(LAT))) / np.pi) / 2 * N
tx, ty = X.astype(int), Y.astype(int); px = ((X - tx) * 256).astype(int).clip(0, 255); py = ((Y - ty) * 256).astype(int).clip(0, 255)
el = np.full((H, W), np.nan)
for (x, y), t in tiles.items():
    m = (tx == x) & (ty == y); el[m] = t[py[m], px[m], 0] * 256 + t[py[m], px[m], 1] + t[py[m], px[m], 2] / 256 - 32768
el = np.where(np.isnan(el), np.nanmedian(el), el)
deep = float(el.min()); k = np.unravel_index(int(el.argmin()), el.shape)
print("deepest", round(deep), "m at", round(float(LON[k]), 3), round(float(LAT[k]), 3), "| highest", round(float(el.max())))
# relief: sea floor from the deepest point (0) to sea level (1); land is clamped just above sea level
rel = np.clip((el - deep) / (0 - deep), 0, 1.03)
Image.fromarray((np.clip(rel, 0, 1) * 65535).astype(np.uint16)).save(os.path.join(A, "dem.png"))
Image.fromarray((np.clip(rel, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0)).save(os.path.join(A, "dem8.png"))
# hillshade
lat0 = (B0 + B1) / 2; gy, gx = np.gradient(el * 4.0, (B1 - B0) / H * 111000, (L1 - L0) / W * 111000 * math.cos(math.radians(lat0)))
def shade(az, alt):
    az, alt = math.radians(az), math.radians(alt); sl = np.arctan(np.hypot(gx, gy)); asp = np.arctan2(-gx, gy)
    return np.sin(alt) * np.cos(sl) + np.cos(alt) * np.sin(sl) * np.cos(az - asp)
hs = .5 * shade(315, 40) + .25 * shade(270, 50) + .25 * shade(0, 55); med = np.median(hs); sp = np.percentile(hs, 99) - np.percentile(hs, 1)
Image.fromarray((np.clip(.8 + (hs - med) / sp * 1.1, .3, 1.2) / 1.2 * 255).astype(np.uint8)).save(os.path.join(A, "hs.png"))
# depth colour ramp (metres below sea level -> RGB)
ST = [(0, (64, 214, 214)), (200, (32, 150, 196)), (1500, (22, 92, 160)), (4000, (14, 52, 118)), (6000, (8, 28, 78)),
      (8000, (12, 14, 46)), (11000, (30, 6, 30))]
d = np.clip(-el, 0, None); col = np.zeros((H, W, 3))
for (d0, c0), (d1, c1) in zip(ST, ST[1:]):
    m = (d >= d0) & (d <= d1); u = ((d - d0) / (d1 - d0))[m][:, None]
    col[m] = np.array(c0) * (1 - u) + np.array(c1) * u
col[d > ST[-1][0]] = ST[-1][1]
land = el > 0; col[land] = np.array((196, 178, 120)) * .6 + np.array((70, 130, 60)) * .4
Image.fromarray(col.clip(0, 255).astype(np.uint8)).save(os.path.join(A, "ne.jpg"), quality=93)
Image.new("L", (W, H), 0).save(os.path.join(A, "mask_none.png"))
shutil.copy(os.path.join(ROOT, "longform", "india", "map3d_art", "globe.jpg"), os.path.join(A, "globe.jpg"))
json.dump({"bbox": [L0, L1, B0, B1], "deepest_m": round(deep), "deepest_lonlat": [round(float(LON[k]), 3), round(float(LAT[k]), 3)], "size": [W, H]},
          open(os.path.join(A, "bathy.json"), "w"), indent=1)
print("assets ->", A, W, "x", H)
