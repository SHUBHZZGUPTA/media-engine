"""Runs on Kaggle (T4 GPU). Renders the India remake's new 3D globe clips (HyperFrames/three.js pages built by
longform/india/remake/clips_kaggle.py) ON THE GPU ONLY.

Same GPU recipe as snake3d_render.py (proven on this account): Chrome headless shell + NVIDIA GL user-space libs from the
matching driver debs + --use-gl=angle --use-angle=gl-egl. A probe checks the WebGL renderer string first; if it is not the
NVIDIA T4, the job stops and renders nothing (no CPU fallback).
Source = gpu/india_clips/<src_file> (checked by sha256): one folder per clip with index.html (seekable via
window.__timelines.main). Each clip is rendered at 1920x1080, 30 fps -> /kaggle/working/<id>.mp4 + <id>_last.jpg.
"""
import hashlib
import json
import os
import re
import subprocess
import time
import urllib.request

OUT = "/kaggle/working"
W = "/tmp/clips"
P = json.loads(JOB_PARAMS)  # noqa: F821  (prepended by tools/kaggle_run.py)
SRC_URL = "https://raw.githubusercontent.com/SHUBHZZGUPTA/media-engine/main/gpu/india_clips/" + P["src_file"]
os.makedirs(OUT, exist_ok=True)
RES = {"params": {k: v for k, v in P.items() if k != "clips"}, "steps": {}}


def save():
    json.dump(RES, open(f"{OUT}/india_clips.json", "w"), indent=1)


def sh(cmd, timeout=900, cwd=None):
    t = time.time()
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout, cwd=cwd)
        return p.returncode, round(time.time() - t, 1), p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return 124, round(time.time() - t, 1), "TIMEOUT"


def stop(v):
    RES["verdict"] = v; save(); print(v); raise SystemExit(0)


_, _, smi = sh("nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader")
RES["steps"]["hardware"] = smi.strip()
DRIVER = smi.strip().splitlines()[0].split(",")[-1].strip() if smi.strip() else ""
if not DRIVER:
    stop("NO GPU")
code, _, out = sh("node -v")
if code != 0 or int(out.strip().lstrip("v").split(".")[0] or 0) < 20:
    sh("pip install -q nodejs-wheel-binaries", timeout=600)
CHROME_LIBS = ("libnss3 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libxrandr2 libxkbcommon0 libxfixes3 libxcomposite1 "
               "libxdamage1 libgbm1 libcups2 libpango-1.0-0 libcairo2 libegl1 libgl1 libvulkan1 pciutils fonts-dejavu-core")
c, _, _ = sh(f"apt-get update -qq && apt-get install -y -qq {CHROME_LIBS} libasound2", timeout=600)
if c != 0:
    sh(f"apt-get install -y -qq {CHROME_LIBS} libasound2t64", timeout=600)
major_v = DRIVER.split(".")[0]
cmd = ("export DEBIAN_FRONTEND=noninteractive; mkdir -p /tmp/debs && cd /tmp/debs && "
       f"for p in libnvidia-gl-{major_v} libnvidia-gpucomp-{major_v} libnvidia-egl-wayland1; do "
       f"V=$(apt-cache madison $p | awk '{{print $3}}' | grep '^{DRIVER}' | head -1); "
       "[ -z \"$V\" ] && V=$(apt-cache madison $p | awk '{print $3}' | head -1); "
       "[ -n \"$V\" ] && apt-get download -qq $p=$V; done; for d in *.deb; do dpkg -x $d / && echo unpacked $d; done; ldconfig")
RES["steps"]["nvidia_debs"] = re.findall(r"unpacked (\S+)", sh(cmd, timeout=900)[2])
sh("pip install -q imageio-ffmpeg", timeout=600)
FF = sh("python3 -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())'")[2].strip().splitlines()[-1]
save()

os.makedirs(f"{W}/web", exist_ok=True)
tgz = f"{W}/web.tgz"; urllib.request.urlretrieve(SRC_URL, tgz)
sha = hashlib.sha256(open(tgz, "rb").read()).hexdigest()
RES["steps"]["source"] = {"sha256": sha, "ok": sha == P["src_sha256"]}
if sha != P["src_sha256"]:
    stop("SOURCE MISMATCH")
sh(f"tar -xzf {tgz} -C {W}/web")
json.dump({"name": "clips", "private": True, "type": "module", "dependencies": {"puppeteer-core": "23.11.1", "@puppeteer/browsers": "2.6.1"}},
          open(f"{W}/package.json", "w"))
c, _, log = sh("npm install --no-audit --no-fund 2>&1 | tail -3 && npx @puppeteer/browsers install chrome-headless-shell@stable --path /tmp/chs 2>&1 | tail -2", cwd=W, timeout=900)
RES["steps"]["npm"] = {"exit": c, "tail": log[-400:]}
CH = sh("find /tmp/chs -type f -name chrome-headless-shell | head -1")[2].strip()
if not CH:
    stop("NO BROWSER")
save()
srv = subprocess.Popen(["python3", "-m", "http.server", "8765"], cwd=f"{W}/web", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)

RENDER = r'''import puppeteer from "puppeteer-core";
import { spawn } from "node:child_process";
import fs from "node:fs";
const [chrome, ff, outDir, clipsJson, q] = process.argv.slice(2);
const b = await puppeteer.launch({ executablePath: chrome, headless: "shell",
  args: ["--no-sandbox", "--ignore-gpu-blocklist", "--enable-gpu-rasterization", "--use-gl=angle", "--use-angle=gl-egl"] });
const p = await b.newPage(); await p.setViewport({ width: 1920, height: 1080 });
p.on("pageerror", e => console.log("PAGEERR", e.message));
let checked = false;
for (const [cid, dur] of JSON.parse(clipsJson)) {
  await p.goto(`http://127.0.0.1:8765/${cid}/index.html`);
  await p.waitForFunction(() => window.__timelines && window.__timelines.main, { timeout: 300000 });
  if (!checked) {
    const gl = await p.evaluate(() => { const c = document.querySelector("canvas"); const g = c.getContext("webgl2") || c.getContext("webgl");
      const e = g.getExtension("WEBGL_debug_renderer_info"); return e ? g.getParameter(e.UNMASKED_RENDERER_WEBGL) : g.getParameter(g.RENDERER); });
    fs.writeFileSync(`${outDir}/renderer.txt`, gl); console.log("GLRENDERER", gl);
    if (!/nvidia|tesla|t4/i.test(gl) || /swiftshader|llvmpipe|software/i.test(gl)) { console.log("NOT_GPU"); await b.close(); process.exit(3); }
    checked = true;
  }
  const t0 = Date.now(); const out = `${outDir}/${cid}.mp4`; const n = Math.round(dur * 30);
  const enc = spawn(ff, ["-v", "error", "-y", "-f", "image2pipe", "-framerate", "30", "-c:v", "mjpeg", "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", out], { stdio: ["pipe", "inherit", "inherit"] });
  let last = null;
  for (let f = 0; f < n; f++) {
    await p.evaluate(t => { window.__timelines.main.seek(t, false); }, f / 30);
    const buf = await p.screenshot({ type: "jpeg", quality: Number(q) }); last = buf;
    if (!enc.stdin.write(buf)) await new Promise(r => enc.stdin.once("drain", r));
  }
  enc.stdin.end(); await new Promise(r => enc.on("close", r));
  if (last) fs.writeFileSync(`${outDir}/${cid}_last.jpg`, last);
  console.log("CLIP_DONE", cid, n, ((Date.now() - t0) / 1000).toFixed(1) + "s");
}
await b.close(); console.log("ALL_DONE");
'''
open(f"{W}/render.mjs", "w").write(RENDER)
clips = [[c["id"], c["dur"]] for c in P["clips"]]
c, s, log = sh(f"node render.mjs {CH} {FF} {OUT} '{json.dumps(clips)}' {P.get('jpeg_q', 95)}", cwd=W, timeout=P.get("render_timeout_s", 5400))
srv.terminate()
RES["steps"]["render"] = {"exit": c, "secs": s, "tail": log[-1500:]}
RES["renderer"] = open(f"{OUT}/renderer.txt").read() if os.path.exists(f"{OUT}/renderer.txt") else None
done = sorted(f[:-4] for f in os.listdir(OUT) if f.endswith(".mp4"))
RES["files"] = done
RES["verdict"] = "GPU RENDER COMPLETE" if c == 0 and len(done) == len(clips) else f"INCOMPLETE exit {c}, {len(done)}/{len(clips)}"
save()
print(RES["verdict"])
