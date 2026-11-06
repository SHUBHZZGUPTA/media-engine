"""Runs on Kaggle (T4 GPU). GPU-ONLY check: can headless Chrome render WebGL on the T4, so that the Remotion +
three.js "cartoon 3D short" skill (mromidev/claude-animated-shorts) renders fast? It never times a CPU render:
if the GPU cannot be used it says so and stops (verdict in remotion_check.json).

Proof that the GPU is really used (all three must hold, otherwise the verdict is NOT confirmed):
  - Chrome's own WebGL renderer string (WEBGL_debug_renderer_info) names the NVIDIA / Tesla T4, not SwiftShader / llvmpipe
  - the test frame is not blank
  - nvidia-smi shows real load (utilisation and memory) while the timed renders run

Steps (results are saved to /kaggle/working/remotion_check.json after every step, so a partial run still reports):
  1. GPU / driver / OpenGL-EGL-Vulkan library check
  2. Node + the Remotion project (pinned versions, bridge short template from the public repo)
  3. One still per GPU-capable Chrome backend; if none reaches the T4, install the NVIDIA OpenGL/EGL/Vulkan user-space
     libraries that match the driver and try again
  4. Timed renders with the working backend (8 and 16 frames of a heavy shot at 1080p and 2K, then 2 and 4 parallel
     workers), seconds per frame = (t16 - t8) / 8, extrapolated to the 2,025-frame example short
Writes only small files: result json, still jpgs, one 16-frame sample mp4."""
import json
import os
import platform
import re
import shutil
import subprocess
import threading
import time

OUT = "/kaggle/working"
W = "/tmp/studio"
SKILL = "/tmp/skill"
TOTAL_FRAMES = 2025
os.makedirs(OUT, exist_ok=True)
RES = {"python": platform.python_version(), "cpus": os.cpu_count(), "steps": {}}


def save():
    with open(f"{OUT}/remotion_check.json", "w") as f:
        json.dump(RES, f, indent=1)


def sh(cmd, timeout=900, cwd=None, env=None):
    t = time.time()
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout, cwd=cwd, env=env)
        return p.returncode, round(time.time() - t, 1), p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return 124, round(time.time() - t, 1), "TIMEOUT"


class GpuMon:
    """Samples nvidia-smi once every 1.5 s while a render runs: proof the GPU is doing the work."""

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
            time.sleep(1.5)

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


# ---- 1. hardware and graphics libraries -------------------------------------------------------------
_, _, smi = sh("nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader")
GRAPHICS_LIBS = "ldconfig -p | grep -i -E 'nvidia-(gl|egl)|libEGL|libGLX|libvulkan|libnvidia-glcore|nvidia_icd' | head -30"
_, _, libs = sh(GRAPHICS_LIBS)
_, _, icd = sh("ls /usr/share/vulkan/icd.d /etc/vulkan/icd.d /usr/share/glvnd/egl_vendor.d 2>&1 | head -20")
_, _, dev = sh("ls -l /dev/nvidia* /dev/dri 2>&1 | head -20")
RES["steps"]["hardware"] = {"nvidia_smi": smi.strip(), "graphics_libs": libs.strip(), "icd_files": icd.strip(), "dev_nodes": dev.strip()}
save()
DRIVER = smi.strip().splitlines()[0].split(",")[-1].strip() if smi.strip() else ""

# ---- 2. node + project ------------------------------------------------------------------------------
code, _, out = sh("node -v")
major = int(out.strip().lstrip("v").split(".")[0]) if code == 0 and out.strip().startswith("v") else 0
if major < 20:
    c, s, log = sh("pip install -q nodejs-wheel-binaries", timeout=600)
    RES["steps"]["node_install"] = {"exit": c, "secs": s, "tail": log[-400:] if c else ""}
_, _, nodev = sh("node -v && npm -v")
RES["steps"]["node"] = nodev.strip()

CHROME_LIBS = ("libnss3 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libxrandr2 libxkbcommon0 libxfixes3 libxcomposite1 "
               "libxdamage1 libgbm1 libcups2 libpango-1.0-0 libcairo2 libegl1 libgl1 libvulkan1 pciutils")
c, s, log = sh(f"apt-get update -qq && apt-get install -y -qq {CHROME_LIBS} libasound2", timeout=600)
if c != 0:  # newer Ubuntu names the sound library libasound2t64
    c, s, log = sh(f"apt-get install -y -qq {CHROME_LIBS} libasound2t64", timeout=600)
RES["steps"]["apt_chrome_libs"] = {"exit": c, "secs": s, "tail": log[-300:] if c else ""}

shutil.rmtree(SKILL, ignore_errors=True)
shutil.rmtree(W, ignore_errors=True)
c, s, log = sh(f"git clone --depth 1 https://github.com/mromidev/claude-animated-shorts {SKILL}")
RES["steps"]["clone_skill"] = {"exit": c, "secs": s, "tail": log[-300:] if c else ""}
os.makedirs(f"{W}/src/videos", exist_ok=True)
os.makedirs(f"{W}/out", exist_ok=True)
shutil.copytree(f"{SKILL}/templates/bridge", f"{W}/src/videos/bridge")

with open(f"{W}/package.json", "w") as f:
    json.dump({"name": "studio", "private": True, "type": "module", "dependencies": {
        "remotion": "4.0.541", "@remotion/cli": "4.0.541", "@remotion/bundler": "4.0.541", "@remotion/renderer": "4.0.541",
        "@remotion/three": "4.0.541", "react": "19.3.1", "react-dom": "19.3.1", "three": "0.178.0",
        "postprocessing": "6.37.6", "@react-three/fiber": "9.2.0", "@react-three/postprocessing": "3.0.4"}}, f, indent=1)
with open(f"{W}/src/index.ts", "w") as f:
    f.write('import { registerRoot } from "remotion";\nimport { Root } from "./Root";\nregisterRoot(Root);\n')
with open(f"{W}/src/Root.tsx", "w") as f:
    f.write('''import React, { useEffect } from "react";
import { Composition } from "remotion";
import { BridgeShort, BRIDGE_FRAMES } from "./videos/bridge/Bridge";
const Probe: React.FC = () => {
  useEffect(() => {
    try {
      const c = document.createElement("canvas");
      const g: any = c.getContext("webgl2") || c.getContext("webgl");
      const e = g && g.getExtension("WEBGL_debug_renderer_info");
      console.error("GLRENDERER " + (e ? g.getParameter(e.UNMASKED_RENDERER_WEBGL) : "none"));
    } catch (err) { console.error("GLRENDERER error " + err); }
  }, []);
  return null;
};
const Wrapped: React.FC = () => <><Probe /><BridgeShort /></>;
export const Root: React.FC = () => (
  <Composition id="BridgeShort" component={Wrapped} durationInFrames={BRIDGE_FRAMES} fps={30} width={1080} height={1920} />
);
''')
ENV = dict(os.environ, TEMP="/tmp/rtmp", TMP="/tmp/rtmp", TMPDIR="/tmp/rtmp")
os.makedirs("/tmp/rtmp", exist_ok=True)
c, s, log = sh("npm install --no-audit --no-fund 2>&1 | tail -5", cwd=W, env=ENV, timeout=900)
RES["steps"]["npm_install"] = {"exit": c, "secs": s, "tail": log[-400:]}
c, s, log = sh("npx remotion browser ensure 2>&1 | tail -5", cwd=W, env=ENV, timeout=600)
RES["steps"]["browser_ensure"] = {"exit": c, "secs": s, "tail": log[-400:]}

# Chrome wrapper: always adds the flags that let headless Chrome use a GPU (proven on this account's Kaggle T4 in the
# render-bench / mt-clips jobs: "--use-gl=angle --use-angle=gl-egl --ignore-gpu-blocklist" reported ANGLE (NVIDIA Tesla T4)).
_, _, found = sh(f"find {W}/node_modules/.remotion -type f \\( -name chrome-headless-shell -o -name chrome \\) | head -1")
CHROME = found.strip().splitlines()[0] if found.strip() else None
WRAP = "/tmp/chrome_gpu.sh"
if CHROME:
    with open(WRAP, "w") as f:
        f.write(f'#!/bin/bash\nexec {CHROME} "$@" --no-sandbox --ignore-gpu-blocklist --enable-gpu-rasterization\n')
    os.chmod(WRAP, 0o755)
BROWSER = f" --browser-executable={WRAP}" if CHROME else ""
RES["steps"]["chrome"] = {"path": CHROME, "wrapper": WRAP if CHROME else None}
save()


# ---- 3. which GPU-capable Chrome backend draws on the T4 ------------------------------------------------
SOFTWARE = re.compile(r"swiftshader|llvmpipe|software|softpipe|lavapipe|mesa offscreen", re.I)
NVIDIA = re.compile(r"nvidia|tesla|\bt4\b", re.I)


def glr(log):
    m = re.findall(r"GLRENDERER (.*)", log)
    return m[0].strip() if m else None


def is_gpu(renderer):
    return bool(renderer and NVIDIA.search(renderer) and not SOFTWARE.search(renderer))


# The Remotion CLI does not print console messages from the page, but the Node API's onBrowserLog does, so the test
# frame is rendered through this small helper (it prints the "GLRENDERER ..." line the probe in Root.tsx emits).
PROBE_STILL = r'''import path from "node:path";
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
const [gl, out, exe] = process.argv.slice(2);
const browserExecutable = exe || undefined;
const chromiumOptions = { gl };
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });
const onBrowserLog = (l) => { if (/GLRENDERER/.test(l.text)) console.log(l.text); };
const composition = await selectComposition({ serveUrl, id: "BridgeShort", browserExecutable, chromiumOptions, onBrowserLog });
await renderStill({ composition, serveUrl, frame: 900, output: out, imageFormat: "jpeg", scale: 0.5, browserExecutable, chromiumOptions, onBrowserLog, timeoutInMilliseconds: 300000 });
console.log("STILL_DONE");
'''
os.makedirs(f"{W}/scripts", exist_ok=True)
with open(f"{W}/scripts/probe_still.mjs", "w") as f:
    f.write(PROBE_STILL)


def still(gl):
    path = f"{OUT}/still_{gl}.jpg"
    if os.path.exists(path):
        os.remove(path)
    c, s, log = sh(f"node scripts/probe_still.mjs {gl} {path} {WRAP if CHROME else ''}", cwd=W, env=ENV, timeout=600)
    std = None
    if os.path.exists(path):
        from PIL import Image
        import numpy as np
        std = round(float(np.asarray(Image.open(path).convert("L"), dtype=float).std()), 1)
    r = glr(log)
    return {"exit": c, "secs": s, "renderer": r, "pixel_std": std, "draws": bool(std and std > 15),
            "on_gpu": is_gpu(r) and bool(std and std > 15), "tail": log[-300:] if c else ""}


GL_BACKENDS = ["angle-egl", "egl", "vulkan", "angle"]  # the ones that can reach a GPU; software backends are never used
stills = {}


def try_backends(round_name):
    for gl in GL_BACKENDS:
        stills[f"{round_name}:{gl}"] = still(gl)
        RES["steps"]["stills"] = stills
        save()
    return [k.split(":")[1] for k, v in stills.items() if k.startswith(round_name) and v["on_gpu"]]


def unpack_nvidia_debs():
    """The method that worked in this account's earlier Kaggle jobs: apt refuses libnvidia-gl (held packages), so download
    the exact-version .debs without dependency resolution and unpack them over the system. This adds only the driver's
    EGL / GLX / Vulkan user-space libraries next to the CUDA libraries Kaggle already mounts."""
    major_v = DRIVER.split(".")[0]
    cmd = ("export DEBIAN_FRONTEND=noninteractive; mkdir -p /tmp/debs && cd /tmp/debs && "
           f"for p in libnvidia-gl-{major_v} libnvidia-gpucomp-{major_v} libnvidia-egl-wayland1; do "
           f"V=$(apt-cache madison $p | awk '{{print $3}}' | grep '^{DRIVER}' | head -1); "
           "[ -z \"$V\" ] && V=$(apt-cache madison $p | awk '{print $3}' | head -1); "
           "echo $p want " + DRIVER + " got $V; [ -n \"$V\" ] && apt-get download -qq $p=$V; done; "
           "ls -la; for d in *.deb; do dpkg -x $d / && echo unpacked $d; done; ldconfig; ls -la /dev/nvidia*")
    c, s, log = sh(cmd, timeout=900)
    _, _, libs_after = sh(GRAPHICS_LIBS)
    return {"driver": DRIVER, "exit": c, "secs": s, "log_tail": log[-900:], "graphics_libs_after": libs_after.strip()}


RES["steps"]["nvidia_gl_debs"] = unpack_nvidia_debs()
save()
gpu_ok = try_backends("after_deb_unpack")


def install_nvidia_userspace():
    """Install the NVIDIA OpenGL / EGL / Vulkan user-space libraries matching the driver already loaded (no kernel module)."""
    info = {"driver": DRIVER}
    if not DRIVER:
        info["error"] = "no driver version from nvidia-smi"
        return info
    run = "/tmp/nv.run"
    for u in (f"https://us.download.nvidia.com/tesla/{DRIVER}/NVIDIA-Linux-x86_64-{DRIVER}.run",
              f"https://us.download.nvidia.com/XFree86/Linux-x86_64/{DRIVER}/NVIDIA-Linux-x86_64-{DRIVER}.run"):
        c, s, log = sh(f"curl -fsSL -o {run} {u}", timeout=900)
        if c == 0 and os.path.exists(run) and os.path.getsize(run) > 50e6:
            info["downloaded_from"] = u
            break
        info.setdefault("download_failures", []).append({"url": u, "exit": c, "tail": log[-120:]})
    if "downloaded_from" in info:
        c, s, log = sh(f"chmod +x {run} && {run} --no-kernel-module --no-kernel-module-source --no-nouveau-check --no-questions "
                       f"--no-backup --no-x-check --no-nvidia-modprobe --install-libglvnd --silent", timeout=900)
        info["installer"] = {"exit": c, "secs": s, "tail": log[-500:]}
    else:  # fall back to the distro package with the same major version (only works if the minor version matches closely)
        major_v = DRIVER.split(".")[0]
        c, s, log = sh(f"apt-get install -y -qq libnvidia-gl-{major_v}", timeout=600)
        info["apt_libnvidia_gl"] = {"exit": c, "secs": s, "tail": log[-300:]}
    _, _, libs_after = sh(GRAPHICS_LIBS)
    _, _, icd_after = sh("ls /usr/share/vulkan/icd.d /etc/vulkan/icd.d /usr/share/glvnd/egl_vendor.d 2>&1 | head -20")
    info["graphics_libs_after"] = libs_after.strip()
    info["icd_files_after"] = icd_after.strip()
    return info


if not gpu_ok:
    RES["steps"]["install_nvidia_userspace_libs"] = install_nvidia_userspace()
    save()
    gpu_ok = try_backends("after_run_installer")

RES["gpu_gl_that_draws_on_t4"] = gpu_ok
if not gpu_ok:
    RES["verdict"] = ("GPU NOT USABLE: Chrome could not render WebGL on the T4 with any GPU backend, even after installing the "
                      "matching NVIDIA user-space libraries. No CPU render was run. See steps.stills for the renderer string "
                      "each backend reported.")
    save()
    print(RES["verdict"])
    raise SystemExit(0)
save()


# ---- 4. timed renders on the GPU backend only ---------------------------------------------------------------
def render(gl, frames, scale, label, conc=None):
    out = f"{W}/out/{label}.mp4"
    cmd = (f"npx remotion render src/index.ts BridgeShort {out} --frames={frames} --scale={scale} --gl={gl} "
           f"--crf=16 --codec=h264 --log=error{BROWSER}" + (f" --concurrency={conc}" if conc else ""))
    with GpuMon() as mon:
        c, s, log = sh(cmd, cwd=W, env=ENV, timeout=1500)
    return {"exit": c, "secs": s, "ok": c == 0 and os.path.exists(out), "gpu_load": mon.summary(),
            "tail": log[-200:] if c else ""}


def per_frame(gl, scale, tag, conc=None):
    a = render(gl, "900-907", scale, f"{tag}_8", conc)
    b = render(gl, "900-915", scale, f"{tag}_16", conc)
    r = {"t8": a["secs"], "t16": b["secs"], "ok": a["ok"] and b["ok"], "gpu_load_16_frames": b["gpu_load"]}
    if r["ok"]:
        pf = (b["secs"] - a["secs"]) / 8
        r["sec_per_frame"] = round(pf, 2)
        r["overhead_s"] = round(a["secs"] - 8 * pf, 1)
        r["est_total_min_for_%d_frames" % TOTAL_FRAMES] = round(pf * TOTAL_FRAMES / 60, 1)
    else:
        r["tail"] = (a["tail"] + b["tail"])[-300:]
    return r


bench = {}
gl = gpu_ok[0]
RES["backend_used"] = gl
bench["1080p"] = per_frame(gl, "1", "r1080")
RES["steps"]["bench"] = bench
save()
if bench["1080p"].get("ok"):
    bench["2k"] = per_frame(gl, "1.3333333333333333", "r2k")
    save()
    for n in (2, 4):
        bench[f"1080p_concurrency{n}_16frames"] = render(gl, "900-915", "1", f"r1080_c{n}", n)
        save()
    sample = f"{W}/out/r1080_16.mp4"
    if os.path.exists(sample):
        shutil.copy(sample, f"{OUT}/sample_1080p_16frames.mp4")
RES["steps"]["bench"] = bench

# ---- verdict: the GPU must be proven, not assumed ---------------------------------------------------------
load = bench.get("1080p", {}).get("gpu_load_16_frames", {})
renderer_ok = any(is_gpu(v.get("renderer")) for k, v in stills.items() if k.endswith(f":{gl}") and v.get("on_gpu"))
load_ok = load.get("max_util_pct", 0) >= 5 and (load.get("max_mem_mib", 0) - load.get("min_mem_mib", 0)) >= 50
RES["gpu_proof"] = {"chrome_renderer_is_nvidia": renderer_ok, "nvidia_smi_load_seen": load_ok, "load": load}
RES["verdict"] = ("GPU RENDERING CONFIRMED" if renderer_ok and load_ok and bench["1080p"].get("ok")
                  else "NOT CONFIRMED: Chrome reported an NVIDIA renderer but nvidia-smi saw too little load, or the renders failed; "
                       "do not trust the timings")
save()
print(RES["verdict"])
print(json.dumps(RES.get("gpu_proof"), indent=1))
print(json.dumps(bench, indent=1))
