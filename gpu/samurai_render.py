"""Runs on Kaggle (T4 GPU). Renders the 2D-fighters-in-3D samurai duel breakdown short (Remotion + three.js) at 1440x2560, 30 fps,
in segments, ON THE GPU ONLY (same proven pipeline as lake_render.py: NVIDIA EGL via ANGLE, per-tab GLRENDERER proof, no software fallback).
Project source = gpu/samurai_short/<src_file> in this repo (sha256 checked). Audio is NOT in the render; it is muxed locally.
Results: /kaggle/working/samurai_render.json, samurai_seg{1..n}.mp4, probe_still.jpg."""
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import threading
import time
import urllib.request

OUT = "/kaggle/working"
W = "/tmp/samurai"
P = json.loads(JOB_PARAMS)  # noqa: F821  (prepended by tools/kaggle_run.py)
SRC_URL = "https://raw.githubusercontent.com/SHUBHZZGUPTA/media-engine/main/gpu/samurai_short/" + P.get("src_file", "samurai_src.tar.gz")
MAX_MB = 38  # the repo keeps files up to 40 MB
os.makedirs(OUT, exist_ok=True)
RES = {"python": platform.python_version(), "cpus": os.cpu_count(), "params": P, "steps": {}}


def save():
    with open(f"{OUT}/samurai_render.json", "w") as f:
        json.dump(RES, f, indent=1)


def sh(cmd, timeout=900, cwd=None, env=None):
    t = time.time()
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout, cwd=cwd, env=env)
        return p.returncode, round(time.time() - t, 1), p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return 124, round(time.time() - t, 1), "TIMEOUT"


class GpuMon:
    def __init__(self):
        self.util, self.mem, self.stop = [], [], False

    def _run(self):
        while not self.stop:
            try:
                p = subprocess.run("nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader,nounits",
                                   shell=True, capture_output=True, text=True, timeout=20)
                rows = [r.split(",") for r in p.stdout.strip().splitlines() if "," in r]
                if rows:
                    self.util.append(max(int(r[0]) for r in rows))
                    self.mem.append(max(int(r[1]) for r in rows))
            except Exception:
                pass
            time.sleep(2)

    def __enter__(self):
        self.t = threading.Thread(target=self._run, daemon=True)
        self.t.start()
        return self

    def __exit__(self, *a):
        self.stop = True
        self.t.join(timeout=5)

    def summary(self):
        return {"samples": len(self.util), "max_util_pct": max(self.util or [0]),
                "mean_util_pct": round(sum(self.util) / max(len(self.util), 1), 1),
                "max_mem_mib": max(self.mem or [0]), "min_mem_mib": min(self.mem or [0])}


def stop(verdict):
    RES["verdict"] = verdict
    save()
    print(verdict)
    raise SystemExit(0)


# ---- 1. hardware, node, chrome libs, project ---------------------------------------------------------------
_, _, smi = sh("nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader")
RES["steps"]["hardware"] = smi.strip()
DRIVER = smi.strip().splitlines()[0].split(",")[-1].strip() if smi.strip() else ""
if not DRIVER:
    stop("NO GPU: nvidia-smi reported nothing. Nothing was rendered.")
save()

code, _, out = sh("node -v")
major = int(out.strip().lstrip("v").split(".")[0]) if code == 0 and out.strip().startswith("v") else 0
if major < 20:
    sh("pip install -q nodejs-wheel-binaries", timeout=600)
RES["steps"]["node"] = sh("node -v && npm -v")[2].strip()

CHROME_LIBS = ("libnss3 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libxrandr2 libxkbcommon0 libxfixes3 libxcomposite1 "
               "libxdamage1 libgbm1 libcups2 libpango-1.0-0 libcairo2 libegl1 libgl1 libvulkan1 pciutils")
c, s, log = sh(f"apt-get update -qq && apt-get install -y -qq {CHROME_LIBS} libasound2", timeout=600)
if c != 0:
    c, s, log = sh(f"apt-get install -y -qq {CHROME_LIBS} libasound2t64", timeout=600)
RES["steps"]["apt_chrome_libs"] = {"exit": c, "secs": s}

shutil.rmtree(W, ignore_errors=True)
os.makedirs(f"{W}/out", exist_ok=True)
tgz = f"{W}/samurai_src.tar.gz"
urllib.request.urlretrieve(SRC_URL, tgz)
sha = hashlib.sha256(open(tgz, "rb").read()).hexdigest()
RES["steps"]["source"] = {"sha256": sha, "expected": P["src_sha256"], "bytes": os.path.getsize(tgz)}
save()
if sha != P["src_sha256"]:
    stop("SOURCE MISMATCH: the downloaded project source does not match the sha256 in the job params. Nothing rendered.")
sh(f"tar -xzf {tgz} -C {W}")

with open(f"{W}/package.json", "w") as f:
    json.dump({"name": "samurai", "private": True, "type": "module", "dependencies": {
        "remotion": "4.0.541", "@remotion/cli": "4.0.541", "@remotion/bundler": "4.0.541", "@remotion/renderer": "4.0.541",
        "@remotion/three": "4.0.541", "react": "19.3.1", "react-dom": "19.3.1", "three": "0.178.0",
        "postprocessing": "6.37.6", "@react-three/fiber": "9.2.0", "@react-three/postprocessing": "3.0.4"}}, f, indent=1)
ENV = dict(os.environ, TEMP="/tmp/rtmp", TMP="/tmp/rtmp", TMPDIR="/tmp/rtmp")
os.makedirs("/tmp/rtmp", exist_ok=True)
c, s, log = sh("npm install --no-audit --no-fund 2>&1 | tail -5", cwd=W, env=ENV, timeout=900)
RES["steps"]["npm_install"] = {"exit": c, "secs": s, "tail": log[-300:]}
c, s, log = sh("npx remotion browser ensure 2>&1 | tail -3", cwd=W, env=ENV, timeout=600)
RES["steps"]["browser_ensure"] = {"exit": c, "secs": s, "tail": log[-300:]}

# ---- 2. NVIDIA EGL/GLX/Vulkan user-space libs (the unpack method proven on this account's T4) + chrome wrapper -------
major_v = DRIVER.split(".")[0]
cmd = ("export DEBIAN_FRONTEND=noninteractive; mkdir -p /tmp/debs && cd /tmp/debs && "
       f"for p in libnvidia-gl-{major_v} libnvidia-gpucomp-{major_v} libnvidia-egl-wayland1; do "
       f"V=$(apt-cache madison $p | awk '{{print $3}}' | grep '^{DRIVER}' | head -1); "
       "[ -z \"$V\" ] && V=$(apt-cache madison $p | awk '{print $3}' | head -1); "
       "echo $p want " + DRIVER + " got $V; [ -n \"$V\" ] && apt-get download -qq $p=$V; done; "
       "for d in *.deb; do dpkg -x $d / && echo unpacked $d; done; ldconfig")
c, s, log = sh(cmd, timeout=900)
RES["steps"]["nvidia_gl_debs"] = {"driver": DRIVER, "exit": c, "secs": s, "unpacked": re.findall(r"unpacked (\S+)", log)}

_, _, found = sh(f"find {W}/node_modules/.remotion -type f \\( -name chrome-headless-shell -o -name chrome \\) | head -1")
CHROME = found.strip().splitlines()[0] if found.strip() else None
if not CHROME:
    stop("NO BROWSER: Remotion's headless Chrome was not found. Nothing rendered.")
WRAP = "/tmp/chrome_gpu.sh"
with open(WRAP, "w") as f:
    f.write(f'#!/bin/bash\nexec {CHROME} "$@" --no-sandbox --ignore-gpu-blocklist --enable-gpu-rasterization\n')
os.chmod(WRAP, 0o755)
RES["steps"]["chrome"] = CHROME
save()

# ---- 3. the Node renderer: probe mode (one still) and render mode (segments) ---------------------------------------
RENDER_MJS = r'''import fs from "node:fs";
import path from "node:path";
import { bundle } from "@remotion/bundler";
import { renderMedia, renderStill, selectComposition } from "@remotion/renderer";
const [mode, wrapper, outDir, scale, crf, conc, segJson] = process.argv.slice(2);
const GL = "angle-egl";                                   // the one and only backend; no software fallback exists here
const SOFT = /swiftshader|llvmpipe|software|softpipe|lavapipe|mesa offscreen|none|error/i;
const NV = /nvidia|tesla|\bt4\b/i;
const seen = new Map();
const bad = [];
const onBrowserLog = (l) => {
  const m = /GLRENDERER (.*)/.exec(l.text);
  if (!m) return;
  const r = m[1].trim();
  seen.set(r, (seen.get(r) || 0) + 1);
  if (!NV.test(r) || SOFT.test(r)) bad.push(r);
};
const chromiumOptions = { gl: GL };
const browserExecutable = wrapper;
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });
const composition = await selectComposition({ serveUrl, id: "SamuraiShort", browserExecutable, chromiumOptions, onBrowserLog });
const report = (extra = {}) => fs.writeFileSync(path.join(outDir, "renderer_seen.json"), JSON.stringify({ seen: Object.fromEntries(seen), bad, ...extra }, null, 1));
if (mode === "probe") {
  await renderStill({ composition, serveUrl, frame: 1275, output: path.join(outDir, "probe_still.jpg"), imageFormat: "jpeg", scale: 0.5,
    browserExecutable, chromiumOptions, onBrowserLog, timeoutInMilliseconds: 300000 });
  report();
  console.log("PROBE_DONE", JSON.stringify([...seen.keys()]));
  process.exit(bad.length ? 3 : 0);
}
const segs = JSON.parse(segJson);
for (const [i, [a, b]] of segs.entries()) {
  const t0 = Date.now();
  const output = path.join(outDir, `samurai_seg${i + 1}.mp4`);
  let last = -1;
  await renderMedia({ composition, serveUrl, codec: "h264", crf: Number(crf), scale: Number(scale), frameRange: [a, b],
    outputLocation: output, concurrency: Number(conc), browserExecutable, chromiumOptions, onBrowserLog,
    timeoutInMilliseconds: 300000, logLevel: "error",
    onProgress: ({ renderedFrames }) => { if (bad.length) throw new Error("GPU_FALLBACK " + bad[0]); if (renderedFrames - last >= 100) { last = renderedFrames; console.log(`seg${i + 1} ${renderedFrames}/${b - a + 1}`); } } });
  report({ done_segments: i + 1 });
  if (bad.length) { console.log("GPU_FALLBACK", bad[0]); process.exit(3); }
  console.log(`SEG_DONE ${i + 1} ${a}-${b} ${((Date.now() - t0) / 1000).toFixed(1)}s`);
}
console.log("ALL_DONE");
'''
with open(f"{W}/render.mjs", "w") as f:
    f.write(RENDER_MJS)


def node(mode, segs="[]"):
    return sh(f"node render.mjs {mode} {WRAP} {OUT} {P['scale']} {P['crf']} {P['concurrency']} '{segs}'",
              cwd=W, env=ENV, timeout=P.get("render_timeout_s", 4200))


def renderer_seen():
    try:
        return json.load(open(f"{OUT}/renderer_seen.json"))
    except Exception:
        return {"seen": {}, "bad": ["no renderer report"]}


# probe: is the frame drawn on the NVIDIA GPU? if not, stop without rendering anything
c, s, log = node("probe")
rs = renderer_seen()
std = None
if os.path.exists(f"{OUT}/probe_still.jpg"):
    from PIL import Image
    import numpy as np
    std = round(float(np.asarray(Image.open(f"{OUT}/probe_still.jpg").convert("L"), dtype=float).std()), 1)
RES["steps"]["probe"] = {"exit": c, "secs": s, "renderers": rs.get("seen"), "bad": rs.get("bad"), "pixel_std": std,
                         "tail": log[-400:] if c else ""}
save()
if c != 0 or rs.get("bad") or not rs.get("seen") or not (std and std > 15):
    stop("GPU NOT USABLE: the probe frame was not drawn by the NVIDIA T4 (see steps.probe.renderers). "
         "No CPU render was run and nothing was rendered.")

# ---- 4. real render on the GPU, in segments -----------------------------------------------------------------------------
total = P["frames"]
n = P["segments"]
per = -(-total // n)
SEGS = [[i * per, min(total, (i + 1) * per) - 1] for i in range(n)]
RES["segments"] = SEGS
save()
with GpuMon() as mon:
    t = time.time()
    c, s, log = node("render", json.dumps(SEGS))
    RES["steps"]["render"] = {"exit": c, "secs": s, "tail": log[-1500:], "gpu_load": mon.summary()}
rs = renderer_seen()
RES["renderers_seen_in_render"] = rs.get("seen")
RES["renderer_bad"] = rs.get("bad")
save()
done = [f for f in (f"{OUT}/samurai_seg{i + 1}.mp4" for i in range(n)) if os.path.exists(f)]
if c != 0 or rs.get("bad") or len(done) != n:
    stop("RENDER NOT COMPLETE (" + ("GPU FALLBACK DETECTED, render aborted: " + str(rs.get("bad"))[:200] if rs.get("bad")
         else f"exit {c}, {len(done)}/{n} segments") + "). No CPU render was run.")


# ---- 5. keep every segment under the repo's file-size limit (re-encode only if one is too big) ----------------------------
def ffmpeg_cmd():
    w = shutil.which("ffmpeg")
    return w if w else f"cd {W} && npx remotion ffmpeg"


info = []
for i, f in enumerate(done):
    mb = os.path.getsize(f) / 1e6
    rec = {"file": os.path.basename(f), "mb": round(mb, 1), "frames": SEGS[i][1] - SEGS[i][0] + 1}
    if mb > MAX_MB:
        dur = rec["frames"] / 30
        br = int(MAX_MB * 0.93 * 8e6 / dur)
        tmp = f + ".re.mp4"
        c2, s2, l2 = sh(f"{ffmpeg_cmd()} -y -i {f} -c:v libx264 -preset slow -b:v {br} -maxrate {int(br * 1.25)} "
                        f"-bufsize {br * 2} -pix_fmt yuv420p -an {tmp}", timeout=1500)
        if c2 == 0 and os.path.exists(tmp):
            os.replace(tmp, f)
            rec["reencoded_to_mb"] = round(os.path.getsize(f) / 1e6, 1)
            rec["reencode_kbps"] = br // 1000
        else:
            rec["reencode_failed"] = l2[-200:]
    info.append(rec)
RES["segment_files"] = info
load = RES["steps"]["render"]["gpu_load"]
nv = any(NV_ok for NV_ok in [bool(re.search(r"nvidia|tesla|\bt4\b", k, re.I)) for k in (rs.get("seen") or {})])
load_ok = load["max_util_pct"] >= 5 and load["max_mem_mib"] - load["min_mem_mib"] >= 50
RES["gpu_proof"] = {"every_tab_reported_nvidia": nv and not rs.get("bad"), "tabs_logged": sum((rs.get("seen") or {}).values()),
                    "nvidia_smi_load_seen": load_ok, "load": load}
RES["verdict"] = ("GPU RENDER COMPLETE" if RES["gpu_proof"]["every_tab_reported_nvidia"] and load_ok
                  else "RENDER COMPLETE BUT GPU PROOF INCOMPLETE: check gpu_proof before trusting it")
save()
print(RES["verdict"])
