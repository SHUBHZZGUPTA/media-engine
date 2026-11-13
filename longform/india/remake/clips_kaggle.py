#!/usr/bin/env python3
"""Package the India remake's new 3D globe clips (voice/clips3d.json, written by plan_remake.py) for the Kaggle GPU render.
Usage: python3 clips_kaggle.py [--only=ID,ID]
Writes gpu/india_clips/clips_<sha8>.tar.gz (one folder per clip, shared files once via relative symlinks) and
jobs/kaggle/india-clips-<sha8>.json for gpu/india_clips_render.py. Results come back to outputs/kaggle/<job id>/;
copy them to remake/clips3d/ (fetch_clips step) and re-run plan_remake.py to swap them in.
"""
import hashlib, json, os, shutil, sys, tarfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ENG = os.path.join(ROOT, "longform", "engine"); ART = os.path.join(HERE, "..", "map3d_art"); NM = "/home/claude/work3d/node_modules"
CL = json.load(open(os.path.join(HERE, "voice", "clips3d.json")))
ONLY = next((a.split("=")[1].split(",") for a in sys.argv if a.startswith("--only=")), None)
W = os.path.join("/tmp", "india_clips_build"); shutil.rmtree(W, ignore_errors=True); SH = os.path.join(W, "_shared"); os.makedirs(SH)
def share(src, name, dst):
    if not os.path.exists(os.path.join(SH, name)): shutil.copy(src, os.path.join(SH, name))
    os.symlink(os.path.relpath(os.path.join(SH, name), os.path.dirname(dst)), dst)
built = []
for cid, data in CL.items():
    if ONLY and cid not in ONLY: continue
    P = os.path.join(W, cid); os.makedirs(os.path.join(P, "assets")); G = data["globe"]
    for n in {G["tex"]} | {o["img"] for o in G.get("over", [])}: share(os.path.join(ART, n), n, os.path.join(P, "assets", n))
    share("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf", "poppins700.ttf", os.path.join(P, "assets", "poppins700.ttf"))
    for js in ("gsap/dist/gsap.min.js", "three/build/three.min.js"): share(os.path.join(NM, js), os.path.basename(js), os.path.join(P, os.path.basename(js)))
    html = open(os.path.join(ENG, "map3d", "clip.html")).read().replace("__DATA__", json.dumps(data)).replace("__DUR__", "%.3f" % data["dur"])
    open(os.path.join(P, "index.html"), "w").write(html); built.append({"id": cid, "dur": data["dur"]})
tmp = os.path.join(W, "..", "india_clips.tar.gz")
with tarfile.open(tmp, "w:gz") as tf:
    for n in sorted(os.listdir(W)): tf.add(os.path.join(W, n), arcname=n)
sha = hashlib.sha256(open(tmp, "rb").read()).hexdigest(); name = f"clips_{sha[:8]}.tar.gz"
os.makedirs(os.path.join(ROOT, "gpu", "india_clips"), exist_ok=True); shutil.copy(tmp, os.path.join(ROOT, "gpu", "india_clips", name))
jid = f"india-clips-{sha[:8]}"; secs = sum(c["dur"] for c in built)
job = {"id": jid, "script": "gpu/india_clips_render.py", "accelerator": "NvidiaTeslaT4", "internet": True,
       "timeout_minutes": 90, "wait_minutes": 95, "params": {"src_file": name, "src_sha256": sha, "clips": built, "jpeg_q": 95}}
json.dump(job, open(os.path.join(ROOT, "jobs", "kaggle", jid + ".json"), "w"), indent=1)
print(f"{len(built)} clips, {secs:.0f} s of video, {os.path.getsize(tmp) / 1e6:.1f} MB -> gpu/india_clips/{name}; job jobs/kaggle/{jid}.json")
