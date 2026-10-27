#!/usr/bin/env python3
"""3D map clips for the Russia pilot's key map moments, and a spec that uses them.

Usage: python3 clips3d.py spec_in.json spec_out.json [--render] [--only A,B]
Each clip is a HyperFrames page (engine/map3d/clip.html) timed to its shot in spec_in (absolute times taken from the
shot and its overlay 'in' times). Rendered clips go to clips3d/<id>.mp4; spec_out swaps those shots' backgrounds for the
video and drops plate-space circles (the 3D scene draws its own pins and glows).
"""
import json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ENG = os.path.join(HERE, "..", "..", "engine"); sys.path.insert(0, os.path.join(ENG, "map3d"))
import overlays as OVL
ART = os.path.join(HERE, "..", "map3d_art"); WORK = "/home/claude/work3d"; OUT = os.path.join(HERE, "clips3d"); os.makedirs(OUT, exist_ok=True)
args = [a for a in sys.argv[1:] if not a.startswith("--")]; spec = json.load(open(args[0])); shots = spec["shots"]
ONLY = next((a.split("=")[1].split(",") for a in sys.argv if a.startswith("--only=")), None)

def find(bg, i0=0, need=None):
    for i, s in enumerate(shots):
        if i >= i0 and bg in str(s["bg"]["img"]) and not s["bg"].get("blur") and (need is None or any(need in str(o.get("img")) for o in s["bg"].get("over", []))):
            return i, s
    raise SystemExit(f"shot not found: {bg} {need}")
def ov_in(s, name):
    return next(o["in"] for o in s["bg"].get("over", []) if name in o["img"])

# ---------- overlay textures (built once) ----------
A = ART
def once(path, fn):
    if not os.path.exists(path): fn(path)
    return os.path.basename(path)
RU = [{"admin0": "Russia"}]; AK = [{"admin1": "Alaska"}]; MN = [{"admin0": "Mongolia"}]
once(os.path.join(A, "flag_ru.png"), OVL.flag_ru)
shutil.copy("/home/claude/media-engine/bhugol-v2/example-centralia-3d/flag_us.png", os.path.join(A, "flag_us.png"))
o_ru = once(os.path.join(A, "ov_ru_flag.png"), lambda p: OVL.fill(p, RU, flag=os.path.join(A, "flag_ru.png"), alpha=180, box=[27, 180, 41, 78]))
o_rue = once(os.path.join(A, "ov_ru_edge.png"), lambda p: OVL.edge(p, RU, (255, 230, 160), 4, 9))
o_akg = once(os.path.join(A, "ov_ak_gold.png"), lambda p: OVL.fill(p, AK, color=(255, 200, 40), alpha=230))
o_aku = once(os.path.join(A, "ov_ak_us.png"), lambda p: OVL.fill(p, AK, flag=os.path.join(A, "flag_us.png"), alpha=235, box=[-168, -141, 54, 71.5]))
o_ake = once(os.path.join(A, "ov_ak_edge.png"), lambda p: OVL.edge(p, AK, (255, 220, 120), 4, 9))
o_mn = once(os.path.join(A, "ov_mn_fill.png"), lambda p: OVL.fill(p, MN, color=(150, 20, 20), alpha=200))
o_mne = once(os.path.join(A, "ov_mn_edge.png"), lambda p: OVL.edge(p, MN, (255, 90, 60), 4, 10))
KR = [[23.5, 50.0], [24.5, 54.5], [27.5, 57.0], [29.5, 60.0], [34.5, 61.5], [40.0, 59.0], [42.0, 56.0], [40.0, 52.8], [37.0, 50.0], [34.0, 47.8], [30.0, 47.2], [26.0, 48.6]]
M3 = json.load(open(os.path.join(A, "map3d2.json"))); BB = M3["bbox"]
once(os.path.join(A, "mask_kr2.png"), lambda p: OVL.mask_poly(p, BB, KR))
once(os.path.join(A, "mask_none2.png"), lambda p: OVL.mask_poly(p, BB, [[0, 0], [0, .001], [.001, 0]]))

# ---------- clip definitions (local times: 0 = shot start) ----------
CL = []
def clip(cid, idx, data, tail=.6):
    s = shots[idx]; dur = round(s["t1"] - s["t0"] + tail, 3); CL.append((cid, idx, dict(data, dur=dur)))

i, s = find("map_alaska"); t0 = s["t0"]; ta = ov_in(s, "alaska") - t0; d = s["t1"] - t0
clip("A_alaska", i, {"mode": "globe", "globe": {"tex": "globe.jpg",
    "cam": [[0, 172, 54, 3.2], [d, -174, 58, 2.3]],
    "over": [{"img": o_ru, "a": [[0, 0], [.6, .9]]}, {"img": o_rue, "add": 1, "a": [[0, 0], [.6, 1]]},
             {"img": o_akg, "a": [[ta, 0], [ta + .5, .95]]}, {"img": o_ake, "add": 1, "a": [[ta, 0], [ta + .5, 1]]}]}})
i, s = find("map_alaska", i + 1); t0 = s["t0"]; d = s["t1"] - t0
clip("B_america", i, {"mode": "globe", "globe": {"tex": "globe.jpg",
    "cam": [[0, -170, 58, 2.3], [d, -153, 63, 1.72]],
    "over": [{"img": o_ru, "a": [[0, .9], [.6, .55]]}, {"img": o_rue, "add": 1, "a": [[0, .6]]},
             {"img": o_akg, "a": [[0, .95], [.5, 0]]}, {"img": o_aku, "a": [[0, 0], [.5, .95]]}, {"img": o_ake, "add": 1, "a": [[0, 1]]}],
    "pins": [{"lon": -150, "lat": 61.2, "at": .7, "s": .045, "col": "#FFD84A"}]}})
i, s = find("map_eurasia"); t0 = s["t0"]; d = s["t1"] - t0
clip("C_size", i, {"mode": "globe", "globe": {"tex": "globe.jpg",
    "cam": [[0, 70, 58, 1.75], [d, 98, 58, 3.25]],
    "over": [{"img": o_ru, "a": [[0, .2], [.7, .9]]}, {"img": o_rue, "add": 1, "a": [[0, .3], [.7, 1]]}]}})
i, s = find("map_eurasia", i + 1, need="span"); t0 = s["t0"]; tsp = ov_in(s, "span") - t0; d = s["t1"] - t0
clip("C_zones", i, {"mode": "globe", "globe": {"tex": "globe.jpg",
    "cam": [[0, 96, 58, 3.1], [d, 104, 57, 2.9]],
    "over": [{"img": o_ru, "a": [[0, .9]]}, {"img": o_rue, "add": 1, "a": [[0, 1]]}],
    "arcs": [{"pts": [[37.6, 55.75], [158.6, 53.0]], "lift": .06, "rad": .007, "col": "#FFD84A", "draw": [[tsp, 0], [tsp + 1.4, 1]]}],
    "pins": [{"lon": 37.6, "lat": 55.75, "at": tsp, "s": .05, "label": "Moscow", "size": 44}, {"lon": 158.6, "lat": 53.0, "at": tsp + 1.3, "s": .05, "label": "Kamchatka", "size": 44}]}})
TER = {"bbox": BB, "ne": "ne2.jpg", "hs": "hs2.png", "dem": "dem2.png", "exag": .6}
ROUTE = [[24.0, 59.8], [29.8, 59.9], [31.27, 58.52], [31.0, 55.5], [30.6, 52.3], [30.52, 50.45], [32.4, 47.5], [31.6, 46.6], [30.6, 44.2], [29.4, 41.9], [28.98, 41.01]]
i, s = find("map_rus", need="pin_const"); t0 = s["t0"]; tr = ov_in(s, "trade") - t0; tc = ov_in(s, "pin_const") - t0; d = s["t1"] - t0
clip("D_trade", i, {"mode": "terrain", "terrain": dict(TER, mask="mask_none2.png", **{
    "cam": [[0, 31.0, 57.0, 14.0, 62, 0], [d, 30.6, 49.2, 36.0, 72, -4]],
    "routes": [{"pts": ROUTE, "rad": .11, "col": "#FFD84A", "draw": [[tr, 0], [tr + 3.4, 1]]}],
    "pins": [{"lon": 31.27, "lat": 58.52, "at": 0, "label": "Novgorod", "s": .9}, {"lon": 30.52, "lat": 50.45, "at": .2, "label": "Kyiv", "s": .9},
             {"lon": 28.98, "lat": 41.01, "at": tc, "label": "Constantinople", "col": "#FFD84A", "s": .9}]})})
i, s = find("map_rus", i + 1, need="kievanrus"); t0 = s["t0"]; tk = ov_in(s, "kievanrus") - t0; d = s["t1"] - t0
clip("D_kievanrus", i, {"mode": "terrain", "terrain": dict(TER, mask="mask_kr2.png", outline=KR, wall=.9, **{
    "cam": [[0, 32.5, 53.4, 31.0, 70, -10], [d, 32.5, 53.8, 25.0, 60, 10]],
    "hl": [[tk, 0], [tk + .8, 1]], "rise": [[tk, 0], [tk + 1.2, 1]],
    "routes": [{"pts": ROUTE, "rad": .11, "col": "#FFD84A", "draw": [[0, 1]]}],
    "pins": [{"lon": 31.27, "lat": 58.52, "at": 0, "label": "Novgorod", "s": .9}, {"lon": 30.52, "lat": 50.45, "at": 0, "label": "Kyiv", "s": .9}]})})
i, s = find("map_mongol"); t0 = s["t0"]; th = ov_in(s, "horde") - t0; d = s["t1"] - t0
clip("E_mongols", i, {"mode": "globe", "globe": {"tex": "globe.jpg",
    "cam": [[0, 104, 46, 2.0], [th + .3, 96, 47, 2.15], [d, 62, 50, 2.35]],
    "over": [{"img": o_mn, "a": [[0, 0], [.5, .9]]}, {"img": o_mne, "add": 1, "a": [[0, 0], [.5, 1]]}],
    "arcs": [{"pts": [[104.0, 47.5], [85.0, 49.0], [65.0, 51.0], [48.0, 52.0], [31.5, 50.6]], "lift": .03, "rad": .011, "col": "#FF3B30", "draw": [[th, 0], [th + 2.2, 1]]}],
    "pins": [{"lon": 30.52, "lat": 50.45, "at": th + 2.0, "s": .05, "label": "Kyiv", "size": 44, "col": "#FF3B30"}]}})

# ---------- build + render ----------
def build_project(cid, data):
    P = os.path.join(WORK, "clips", cid); os.makedirs(os.path.join(P, "assets"), exist_ok=True)
    need = {data["globe"]["tex"]} | {o["img"] for o in data["globe"].get("over", [])} if data["mode"] == "globe" else \
           {data["terrain"][k] for k in ("ne", "hs", "dem", "mask")} | ({data["terrain"]["flag"]} if data["terrain"].get("flag") else set())
    for n in need:
        dst = os.path.join(P, "assets", n)
        if not os.path.exists(dst): os.symlink(os.path.abspath(os.path.join(A, n)), dst)
    f = os.path.join(P, "assets", "poppins700.ttf")
    if not os.path.exists(f): shutil.copy("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf", f)
    for js in ("gsap/dist/gsap.min.js", "three/build/three.min.js"): shutil.copy(os.path.join(WORK, "node_modules", js), P)
    html = open(os.path.join(ENG, "map3d", "clip.html")).read().replace("__DATA__", json.dumps(data)).replace("__DUR__", "%.3f" % data["dur"])
    open(os.path.join(P, "index.html"), "w").write(html); return P

ENV = dict(os.environ, HYPERFRAMES_NO_TELEMETRY="1", DO_NOT_TRACK="1", HYPERFRAMES_NO_UPDATE_CHECK="1", HYPERFRAMES_SKIP_SKILLS="1",
           HYPERFRAMES_BROWSER_PATH="/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell")
for cid, idx, data in CL:
    if ONLY and cid.split("_")[0] not in ONLY and cid not in ONLY: continue
    P = build_project(cid, data); out = os.path.join(OUT, cid + ".mp4")
    if "--render" in sys.argv and not os.path.exists(out):
        r = subprocess.run(["npx", "hyperframes", "render", "--crf", "16", "--no-browser-gpu", "--fps", "30", "--output", out], cwd=P, env=ENV,
                           capture_output=True, text=True)
        print(cid, "rendered" if r.returncode == 0 and os.path.exists(out) else "FAILED", (r.stdout + r.stderr)[-600:] if r.returncode else "", flush=True)

# ---------- spec with the clips swapped in ----------
for cid, idx, data in CL:
    s = shots[idx]; out = os.path.join(OUT, cid + ".mp4")
    if not os.path.exists(out): continue
    s["bg"] = {"video": out, "img": "#02070d"}
    s["layers"] = [L for L in s["layers"] if "circle" not in L and not (cid == "D_trade" and isinstance(L.get("img"), dict) and L["img"]["text"] == "Constantinople")]
json.dump(spec, open(args[1], "w"))
print("clips:", [(c, round(d["dur"], 1)) for c, _, d in CL])
