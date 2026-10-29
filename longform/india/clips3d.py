#!/usr/bin/env python3
"""Render the India 3D globe clips listed in clips3d.json (written by plan_pilot.py / plan_full.py).
Usage: python3 clips3d.py <dir with clips3d.json> [--only=ID,ID] [--force]
Writes clips3d/<id>.mp4 and clips3d/<id>_last.jpg. Re-run plan_full.py afterwards to swap them into the spec.
"""
import json, os, shutil, subprocess, sys, time
HERE = os.path.abspath([a for a in sys.argv[1:] if not a.startswith("--")][0]); ENG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine")
ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), "map3d_art"); WORK = "/home/claude/work3d"; OUT = os.path.join(HERE, "clips3d"); os.makedirs(OUT, exist_ok=True)
CL = json.load(open(os.path.join(HERE, "clips3d.json")))
ONLY = next((a.split("=")[1].split(",") for a in sys.argv if a.startswith("--only=")), None)
ENV = dict(os.environ, HYPERFRAMES_NO_TELEMETRY="1", DO_NOT_TRACK="1", HYPERFRAMES_NO_UPDATE_CHECK="1", HYPERFRAMES_SKIP_SKILLS="1",
           HYPERFRAMES_BROWSER_PATH="/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell")
def build(cid, data):
    P = os.path.join(WORK, "clips_india", cid); shutil.rmtree(P, ignore_errors=True); os.makedirs(os.path.join(P, "assets"))
    G = data["globe"]
    for n in {G["tex"]} | {o["img"] for o in G.get("over", [])}:
        os.symlink(os.path.abspath(os.path.join(ART, n)), os.path.join(P, "assets", n))
    shutil.copy("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf", os.path.join(P, "assets", "poppins700.ttf"))
    for js in ("gsap/dist/gsap.min.js", "three/build/three.min.js"): shutil.copy(os.path.join(WORK, "node_modules", js), P)
    html = open(os.path.join(ENG, "map3d", "clip.html")).read().replace("__DATA__", json.dumps(data)).replace("__DUR__", "%.3f" % data["dur"])
    open(os.path.join(P, "index.html"), "w").write(html); return P
def last_frame(mp4, jpg):
    import cv2
    cap = cv2.VideoCapture(mp4); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, n - 21))
    ok, fr = cap.read(); cap.release()
    if ok: cv2.imwrite(jpg, fr, [cv2.IMWRITE_JPEG_QUALITY, 92])
stamp = os.path.join(OUT, "_stamps.json"); ST = json.load(open(stamp)) if os.path.exists(stamp) else {}
for cid, data in CL.items():
    if ONLY and cid not in ONLY: continue
    out = os.path.join(OUT, cid + ".mp4"); key = json.dumps(data, sort_keys=True)
    if os.path.exists(out) and ST.get(cid) == key and "--force" not in sys.argv: continue
    P = build(cid, data); t = time.time(); tmp = out[:-4] + ".tmp.mp4"
    r = subprocess.run(["npx", "hyperframes", "render", "--crf", "16", "--no-browser-gpu", "--fps", "30", "--output", tmp], cwd=P, env=ENV, capture_output=True, text=True)
    if r.returncode == 0 and os.path.exists(tmp):
        os.replace(tmp, out); last_frame(out, os.path.join(OUT, cid + "_last.jpg")); ST[cid] = key; json.dump(ST, open(stamp, "w"))
        print(cid, "ok", round(data["dur"], 1), "s in", round(time.time() - t), "s", flush=True)
    else:
        print(cid, "FAILED", (r.stdout + r.stderr)[-500:], flush=True)
print("ALLDONE", flush=True)
