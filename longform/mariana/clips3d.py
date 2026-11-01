#!/usr/bin/env python3
"""Build (and optionally render locally) the Mariana 3D clips listed in clips3d.json (written by plan_mt.py).
Usage: python3 clips3d.py <dir with clips3d.json> [--only=ID,ID] [--build-only] [--tar=out.tar.gz] [--force]
--build-only writes self-contained HyperFrames projects to WORK/<id>/ (assets copied, not linked); --tar packs them for Kaggle.
Rendered clips go to clips3d/<id>.mp4 + <id>_last.jpg (re-run plan_mt.py afterwards to swap them in).
"""
import json, os, shutil, subprocess, sys, tarfile, time
HERE = os.path.abspath([a for a in sys.argv[1:] if not a.startswith("--")][0]); ME = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(ME, "..", "engine"); ART = os.path.join(ME, "art", "map3d"); WORK = "/home/claude/work3d"; OUT = os.path.join(HERE, "clips3d"); os.makedirs(OUT, exist_ok=True)
CL = json.load(open(os.path.join(HERE, "clips3d.json")))
ONLY = next((a.split("=")[1].split(",") for a in sys.argv if a.startswith("--only=")), None)
TAR = next((a.split("=")[1] for a in sys.argv if a.startswith("--tar=")), None)
ENV = dict(os.environ, HYPERFRAMES_NO_TELEMETRY="1", DO_NOT_TRACK="1", HYPERFRAMES_NO_UPDATE_CHECK="1", HYPERFRAMES_SKIP_SKILLS="1",
           HYPERFRAMES_BROWSER_PATH="/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell")
def build(cid, data):
    P = os.path.join(WORK, "clips_mt", cid); shutil.rmtree(P, ignore_errors=True); os.makedirs(os.path.join(P, "assets"))
    m = data["mode"]; G = data[m]
    need = {G["tex"]} | {o["img"] for o in G.get("over", [])} if m == "globe" else {G[k] for k in ("ne", "hs", "dem", "mask")}
    # shared files live once in clips_mt/_shared (relative symlinks, so a tar of clips_mt keeps one copy of each)
    SH = os.path.join(WORK, "clips_mt", "_shared"); os.makedirs(SH, exist_ok=True)
    def share(src, name, dst):
        if not os.path.exists(os.path.join(SH, name)): shutil.copy(src, os.path.join(SH, name))
        os.symlink(os.path.relpath(os.path.join(SH, name), os.path.dirname(dst)), dst)
    for n in need: share(os.path.join(ART, n), n, os.path.join(P, "assets", n))
    share("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf", "poppins700.ttf", os.path.join(P, "assets", "poppins700.ttf"))
    for js in ("gsap/dist/gsap.min.js", "three/build/three.min.js"): share(os.path.join(WORK, "node_modules", js), os.path.basename(js), os.path.join(P, os.path.basename(js)))
    html = open(os.path.join(ENG, "map3d", "clip.html")).read().replace("__DATA__", json.dumps(data)).replace("__DUR__", "%.3f" % data["dur"])
    open(os.path.join(P, "index.html"), "w").write(html); return P
def last_frame(mp4, jpg):
    import cv2
    cap = cv2.VideoCapture(mp4); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, n - 21))
    ok, fr = cap.read(); cap.release()
    if ok: cv2.imwrite(jpg, fr, [cv2.IMWRITE_JPEG_QUALITY, 92])
stamp = os.path.join(OUT, "_stamps.json"); ST = json.load(open(stamp)) if os.path.exists(stamp) else {}
built = []
for cid, data in CL.items():
    if ONLY and cid not in ONLY: continue
    out = os.path.join(OUT, cid + ".mp4"); key = json.dumps(data, sort_keys=True)
    if os.path.exists(out) and ST.get(cid) == key and "--force" not in sys.argv: continue
    P = build(cid, data); built.append((cid, P))
    if "--build-only" in sys.argv: continue
    t = time.time(); tmp = out[:-4] + ".tmp.mp4"
    r = subprocess.run(["npx", "hyperframes", "render", "--crf", "16", "--no-browser-gpu", "--fps", "30", "--output", tmp], cwd=P, env=ENV, capture_output=True, text=True)
    if r.returncode == 0 and os.path.exists(tmp):
        os.replace(tmp, out); last_frame(out, os.path.join(OUT, cid + "_last.jpg")); ST[cid] = key; json.dump(ST, open(stamp, "w"))
        print(cid, "ok", round(data["dur"], 1), "s in", round(time.time() - t), "s", flush=True)
    else:
        print(cid, "FAILED", (r.stdout + r.stderr)[-500:], flush=True)
if TAR:
    with tarfile.open(TAR, "w:gz") as tf:
        tf.add(os.path.join(WORK, "clips_mt", "_shared"), arcname="_shared")
        for cid, P in built: tf.add(P, arcname=cid)
    json.dump({cid: json.dumps(CL[cid], sort_keys=True) for cid, _ in built}, open(TAR + ".keys.json", "w"))
    print("packed", len(built), "->", TAR, round(os.path.getsize(TAR) / 1e6, 1), "MB")
print("ALLDONE", flush=True)
