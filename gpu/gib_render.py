"""Runs on Kaggle (T4 GPU). Renders a BHUGOL Short HyperFrames page (gibraltar; 1080x1920, silent) (satellite plates with WebGL water, three.js
terrain, characters) ON THE GPU ONLY and returns a silent CRF 13 x264 master in <36 MB parts; grading, audio and the upload encode happen in the chat.

Same GPU recipe as snake3d_render.py / lake_render.py (proven on this account): Chrome headless shell + NVIDIA GL
user-space libs unpacked from the matching driver debs + --use-gl=angle --use-angle=gl-egl. Every page checks its
WebGL renderer string first; if it is not the NVIDIA T4, the job stops and renders nothing (no CPU fallback).

Source = gpu/gib/<src parts> (cat'd in order, checked by sha256). The tarball holds hf/ (index.html + assets) and
mix.m4a. The page exposes window.__seek(t); <video> footage is seeked to the matching media time before each shot.
Outputs (each file < 38 MB so the repo can keep them): <name>.mp4.part01.. (cat to rejoin), stills/ for QC, <id>.json.
"""
import hashlib
import json
import os
import re
import subprocess
import time
import urllib.request

OUT = "/kaggle/working"
W = "/tmp/dr"
P = json.loads(JOB_PARAMS)  # noqa: F821  (prepended by tools/kaggle_run.py)
BASE = "https://raw.githubusercontent.com/SHUBHZZGUPTA/media-engine/main/gpu/gib/"
os.makedirs(OUT, exist_ok=True)
RES = {"params": P, "steps": {}}
REP = f"{OUT}/{P['name']}.json"


def save():
    json.dump(RES, open(REP, "w"), indent=1)


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
RES["steps"]["node"] = sh("node -v")[2].strip()
CHROME_LIBS = ("libnss3 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libxrandr2 libxkbcommon0 libxfixes3 libxcomposite1 "
               "libxdamage1 libgbm1 libcups2 libpango-1.0-0 libcairo2 libegl1 libgl1 libvulkan1 pciutils ffmpeg")
c, s, _ = sh(f"apt-get update -qq && apt-get install -y -qq {CHROME_LIBS} libasound2", timeout=900)
if c != 0:
    c, s, _ = sh(f"apt-get install -y -qq {CHROME_LIBS} libasound2t64", timeout=900)
RES["steps"]["apt"] = c
major_v = DRIVER.split(".")[0]
cmd = ("export DEBIAN_FRONTEND=noninteractive; mkdir -p /tmp/debs && cd /tmp/debs && "
       f"for p in libnvidia-gl-{major_v} libnvidia-gpucomp-{major_v} libnvidia-egl-wayland1; do "
       f"V=$(apt-cache madison $p | awk '{{print $3}}' | grep '^{DRIVER}' | head -1); "
       "[ -z \"$V\" ] && V=$(apt-cache madison $p | awk '{print $3}' | head -1); "
       "[ -n \"$V\" ] && apt-get download -qq $p=$V; done; for d in *.deb; do dpkg -x $d / && echo unpacked $d; done; ldconfig")
RES["steps"]["nvidia_debs"] = re.findall(r"unpacked (\S+)", sh(cmd, timeout=900)[2])
FF = "ffmpeg"
RES["steps"]["x265"] = "libx265" in sh("ffmpeg -hide_banner -encoders 2>/dev/null | grep 265")[2]
save()

# ---- source -------------------------------------------------------------------------------------------------------
os.makedirs(f"{W}/web", exist_ok=True)
tgz = f"{W}/src.tgz"
with open(tgz, "wb") as fo:
    for part in P["src_parts"]:
        fo.write(urllib.request.urlopen(BASE + part, timeout=300).read())
sha = hashlib.sha256(open(tgz, "rb").read()).hexdigest()
RES["steps"]["source"] = {"sha256": sha, "ok": sha == P["src_sha256"], "bytes": os.path.getsize(tgz)}
if sha != P["src_sha256"]:
    stop("SOURCE MISMATCH")
sh(f"tar -xzf {tgz} -C {W}/web")
json.dump({"name": "gr", "private": True, "type": "module", "dependencies": {"puppeteer-core": "23.11.1", "@puppeteer/browsers": "2.6.1"}},
          open(f"{W}/package.json", "w"))
c, s, log = sh("npm install --no-audit --no-fund 2>&1 | tail -3 && npx @puppeteer/browsers install chrome-headless-shell@stable --path /tmp/chs 2>&1 | tail -2", cwd=W, timeout=900)
RES["steps"]["npm"] = {"exit": c, "tail": log[-300:]}
CH = sh("find /tmp/chs -type f -name chrome-headless-shell | head -1")[2].strip()
if not CH:
    stop("NO BROWSER")
save()
srv = subprocess.Popen(["python3", "-m", "http.server", "8765"], cwd=f"{W}/web/{P.get('page_dir', 'hf')}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
RENDER = r'''import puppeteer from "puppeteer-core";
import { spawn } from "node:child_process";
import fs from "node:fs";
const [chrome, ff, outDir, f0s, f1s, tag, q, stillsJson, fpsS] = process.argv.slice(2);
const f0 = +f0s, f1 = +f1s, stills = new Set(JSON.parse(stillsJson)), FPS = +fpsS;
const b = await puppeteer.launch({ executablePath: chrome, headless: "shell",
  args: ["--no-sandbox", "--ignore-gpu-blocklist", "--enable-gpu-rasterization", "--use-gl=angle", "--use-angle=gl-egl", "--max-active-webgl-contexts=32"] });
const p = await b.newPage(); await p.setViewport({ width: 1080, height: 1920 });
p.on("pageerror", e => console.log("PAGEERR", tag, e.message));
p.on("console", m => { const t = m.text(); if (/error|warn/i.test(m.type())) console.log("CONSOLE", tag, t.slice(0, 300)); });
await p.goto("http://127.0.0.1:8765/index.html"); await p.waitForFunction(() => !!window.__seek, { timeout: 600000 });
await p.evaluate(() => document.fonts.ready);
const gl = await p.evaluate(() => { const c = document.createElement("canvas"); const g = c.getContext("webgl2") || c.getContext("webgl");
  const e = g.getExtension("WEBGL_debug_renderer_info"); return e ? g.getParameter(e.UNMASKED_RENDERER_WEBGL) : g.getParameter(g.RENDERER); });
console.log("GLRENDERER", tag, gl); fs.writeFileSync(`${outDir}/renderer_${tag}.txt`, gl);
if (!/nvidia|tesla|t4/i.test(gl) || /swiftshader|llvmpipe|software/i.test(gl)) { console.log("NOT_GPU"); await b.close(); process.exit(3); }
const out = `/tmp/dr/seg_${tag}.mp4`; const t0 = Date.now();
const enc = spawn(ff, ["-v", "error", "-y", "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "mjpeg", "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "13", "-pix_fmt", "yuv420p", out], { stdio: ["pipe", "inherit", "inherit"] });
for (let f = f0; f < f1; f++) {
  await p.evaluate(t => window.__seek(t), f / FPS);
  const buf = await p.screenshot({ type: "jpeg", quality: Number(q) });
  if (stills.has(f)) fs.writeFileSync(`${outDir}/stills/f${String(f).padStart(6, "0")}.jpg`, buf);
  if (!enc.stdin.write(buf)) await new Promise(r => enc.stdin.once("drain", r));
  if ((f - f0) % 300 === 0) console.log("PROGRESS", tag, f, ((Date.now() - t0) / 1000).toFixed(0) + "s");
}
enc.stdin.end(); await new Promise(r => enc.on("close", r));
console.log("SEG_DONE", tag, f0, f1, ((Date.now() - t0) / 1000).toFixed(1) + "s");
await b.close();
'''
open(f"{W}/render.mjs", "w").write(RENDER)
os.makedirs(f"{OUT}/stills", exist_ok=True)
FPS = int(P.get("fps", 30)); N = int(round(P["dur"] * FPS)); K = int(P.get("workers", 3))
cuts = [round(N * i / K) for i in range(K + 1)]
stills = sorted(set(P.get("stills", [])) | set(range(0, N, int(P.get("still_every_s", 5)) * FPS)))
procs = []
t = time.time()
for i in range(K):
    lg = open(f"{OUT}/render_{i}.log", "w")
    procs.append(subprocess.Popen(["node", "render.mjs", CH, "ffmpeg", OUT, str(cuts[i]), str(cuts[i + 1]), str(i), str(P.get("jpeg_q", 95)), json.dumps(stills), str(FPS)],
                                  cwd=W, stdout=lg, stderr=subprocess.STDOUT))
codes = [pp.wait(timeout=P.get("render_timeout_s", 13000)) for pp in procs]
srv.terminate()
RES["steps"]["render"] = {"codes": codes, "secs": round(time.time() - t, 1), "frames": N, "workers": K}
RES["renderer"] = [open(f"{OUT}/renderer_{i}.txt").read() for i in range(K) if os.path.exists(f"{OUT}/renderer_{i}.txt")]
save()
if any(codes):
    stop(f"RENDER FAILED codes {codes}")
open(f"{W}/segs.txt", "w").write("".join(f"file 'seg_{i}.mp4'\n" for i in range(K)))
c, s, log = sh(f"cd {W} && ffmpeg -v error -y -f concat -safe 0 -i segs.txt -c copy silent.mp4", timeout=1800)
RES["steps"]["concat"] = {"exit": c, "secs": s, "tail": log[-300:]}
name = P["name"]
RES["final"] = {"bytes": os.path.getsize(f"{W}/silent.mp4"), "sha256": hashlib.sha256(open(f"{W}/silent.mp4", "rb").read()).hexdigest(),
                "probe": sh(f"ffprobe -v error -count_frames -show_entries stream=nb_read_frames,width,height:format=duration -of csv=p=0 {W}/silent.mp4")[2].strip()}
sh(f"cd {W} && split -b 36m -d -a 2 silent.mp4 {OUT}/{name}.mp4.part")
RES["parts"] = sorted(f for f in os.listdir(OUT) if f.startswith(name + ".mp4.part"))
RES["verdict"] = "GPU RENDER COMPLETE"
save()
print(RES["verdict"])
