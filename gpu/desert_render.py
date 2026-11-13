"""Runs on Kaggle (T4 GPU). Renders a BHUGOL long-form HyperFrames page (satellite plates with WebGL water, three.js
terrain moments) ON THE GPU ONLY, then makes the upload copy (x265 2-pass, audio muxed) right here.

Same GPU recipe as snake3d_render.py / lake_render.py (proven on this account): Chrome headless shell + NVIDIA GL
user-space libs unpacked from the matching driver debs + --use-gl=angle --use-angle=gl-egl. Every page checks its
WebGL renderer string first; if it is not the NVIDIA T4, the job stops and renders nothing (no CPU fallback).

Source = gpu/desert/<src parts> (cat'd in order, checked by sha256). The tarball holds hf/ (index.html + assets) and
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
BASE = "https://raw.githubusercontent.com/SHUBHZZGUPTA/media-engine/main/gpu/desert/"
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
json.dump({"name": "dr", "private": True, "type": "module", "dependencies": {"puppeteer-core": "23.11.1", "@puppeteer/browsers": "2.6.1"}},
          open(f"{W}/package.json", "w"))
c, s, log = sh("npm install --no-audit --no-fund 2>&1 | tail -3 && npx @puppeteer/browsers install chrome-headless-shell@stable --path /tmp/chs 2>&1 | tail -2", cwd=W, timeout=900)
RES["steps"]["npm"] = {"exit": c, "tail": log[-300:]}
CH = sh("find /tmp/chs -type f -name chrome-headless-shell | head -1")[2].strip()
if not CH:
    stop("NO BROWSER")
save()
srv = subprocess.Popen(["python3", "-m", "http.server", "8765"], cwd=f"{W}/web/{P.get('page_dir', 'hf')}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)

# ---- render: N pages in parallel, each a contiguous frame range -> high-quality intermediate ------------------------
RENDER = r'''import puppeteer from "puppeteer-core";
import { spawn } from "node:child_process";
import fs from "node:fs";
const [chrome, ff, outDir, f0s, f1s, tag, q, stillsJson] = process.argv.slice(2);
const f0 = +f0s, f1 = +f1s, stills = new Set(JSON.parse(stillsJson));
const b = await puppeteer.launch({ executablePath: chrome, headless: "shell",
  args: ["--no-sandbox", "--ignore-gpu-blocklist", "--enable-gpu-rasterization", "--use-gl=angle", "--use-angle=gl-egl", "--autoplay-policy=no-user-gesture-required"] });
const p = await b.newPage(); await p.setViewport({ width: 1920, height: 1080 });
p.on("pageerror", e => console.log("PAGEERR", tag, e.message));
await p.goto("http://127.0.0.1:8765/index.html"); await p.waitForFunction(() => window.__seek, { timeout: 600000 });
await p.evaluate(() => document.fonts.ready);
const gl = await p.evaluate(() => { const c = document.createElement("canvas"); const g = c.getContext("webgl2") || c.getContext("webgl");
  const e = g.getExtension("WEBGL_debug_renderer_info"); return e ? g.getParameter(e.UNMASKED_RENDERER_WEBGL) : g.getParameter(g.RENDERER); });
console.log("GLRENDERER", tag, gl); fs.writeFileSync(`${outDir}/renderer_${tag}.txt`, gl);
if (!/nvidia|tesla|t4/i.test(gl) || /swiftshader|llvmpipe|software/i.test(gl)) { console.log("NOT_GPU"); await b.close(); process.exit(3); }
const out = `/tmp/dr/seg_${tag}.mp4`; const t0 = Date.now();
const enc = spawn(ff, ["-v", "error", "-y", "-f", "image2pipe", "-framerate", "30", "-c:v", "mjpeg", "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-pix_fmt", "yuv420p", out], { stdio: ["pipe", "inherit", "inherit"] });
for (let f = f0; f < f1; f++) {
  await p.evaluate(async t => { window.__seek(t);
    const vs = [...document.querySelectorAll("video")];
    await Promise.all(vs.map(v => { const a = +v.dataset.start, d = +v.dataset.duration, ms = +(v.dataset.mediaStart || 0);
      if (!(t >= a - .05 && t <= a + d + .05)) return null; const tt = Math.max(0, Math.min(d, t - a) + ms);
      if (Math.abs(v.currentTime - tt) < 1e-3 && v.readyState >= 2) return null;
      return new Promise(r => { const done = () => r(); v.addEventListener("seeked", done, { once: true }); v.currentTime = tt; setTimeout(done, 4000); }); }));
  }, f / 30);
  const buf = await p.screenshot({ type: "jpeg", quality: Number(q) });
  if (stills.has(f)) fs.writeFileSync(`${outDir}/stills/f${String(f).padStart(6, "0")}.jpg`, buf);
  if (!enc.stdin.write(buf)) await new Promise(r => enc.stdin.once("drain", r));
  if ((f - f0) % 900 === 0) console.log("PROGRESS", tag, f, ((Date.now() - t0) / 1000).toFixed(0) + "s");
}
enc.stdin.end(); await new Promise(r => enc.on("close", r));
console.log("SEG_DONE", tag, f0, f1, ((Date.now() - t0) / 1000).toFixed(1) + "s");
await b.close();
'''
open(f"{W}/render.mjs", "w").write(RENDER)
os.makedirs(f"{OUT}/stills", exist_ok=True)
N = int(round(P["dur"] * 30)); K = int(P.get("workers", 2)); F0 = int(round(P.get("start", 0) * 30))
cuts = [F0 + round(N * i / K) for i in range(K + 1)]
stills = list(range(F0, F0 + N, int(P.get("still_every_s", 30)) * 30))
procs = []
t = time.time()
for i in range(K):
    lg = open(f"{OUT}/render_{i}.log", "w")
    procs.append(subprocess.Popen(["node", "render.mjs", CH, FF, OUT, str(cuts[i]), str(cuts[i + 1]), str(i), str(P.get("jpeg_q", 92)), json.dumps(stills)],
                                  cwd=W, stdout=lg, stderr=subprocess.STDOUT))
codes = [pp.wait(timeout=P.get("render_timeout_s", 14000)) for pp in procs]
srv.terminate()
RES["steps"]["render"] = {"codes": codes, "secs": round(time.time() - t, 1), "frames": N, "workers": K}
RES["renderer"] = [open(f"{OUT}/renderer_{i}.txt").read() for i in range(K) if os.path.exists(f"{OUT}/renderer_{i}.txt")]
save()
if any(codes):
    stop(f"RENDER FAILED codes {codes}")
if P.get("test"):   # probe run: keep small copies of the raw segments, no upload encode
    for i in range(K):
        sh(f"ffmpeg -v error -y -i {W}/seg_{i}.mp4 -c:v libx264 -crf 24 -preset fast {OUT}/test_seg{i}.mp4", timeout=1800)
    RES["verdict"] = "GPU TEST COMPLETE"; save(); print(RES["verdict"]); raise SystemExit(0)

# ---- join, 2-pass x265 at the upload bitrate, mux audio, split for the repo -------------------------------------
open(f"{W}/segs.txt", "w").write("".join(f"file 'seg_{i}.mp4'\n" for i in range(K)))
c, s, log = sh(f"cd {W} && ffmpeg -v error -y -f concat -safe 0 -i segs.txt -c copy video.mp4", timeout=1800)
RES["steps"]["concat"] = {"exit": c, "secs": s, "tail": log[-300:]}
rate = P.get("rate", "1280k"); name = P["name"]
x = (f"cd {W} && ffmpeg -v error -y -i video.mp4 -c:v libx265 -preset medium -b:v {rate} -x265-params pass=1:log-level=error -an -f null /dev/null && "
     f"ffmpeg -v error -y -i video.mp4 -i web/mix.m4a -map 0:v -map 1:a -c:v libx265 -preset medium -b:v {rate} -x265-params pass=2:log-level=error "
     f"-tag:v hvc1 -c:a copy -movflags +faststart -shortest {name}.mp4")
c, s, log = sh(x, timeout=7200)
RES["steps"]["encode"] = {"exit": c, "secs": s, "tail": log[-400:]}
if c != 0:
    stop("ENCODE FAILED")
RES["final"] = {"bytes": os.path.getsize(f"{W}/{name}.mp4"), "sha256": hashlib.sha256(open(f"{W}/{name}.mp4", "rb").read()).hexdigest(),
                "probe": sh(f"ffprobe -v error -show_entries format=duration:stream=codec_name,width,height -of csv=p=0 {W}/{name}.mp4")[2].strip()}
sh(f"cd {W} && split -b 36m -d -a 2 {name}.mp4 {OUT}/{name}.mp4.part")
RES["parts"] = sorted(f for f in os.listdir(OUT) if f.startswith(name + ".mp4.part"))
RES["verdict"] = "GPU RENDER COMPLETE"
save()
print(RES["verdict"])
