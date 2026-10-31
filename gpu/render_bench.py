"""Runs on Kaggle. Render-speed benchmark for a HyperFrames project (Money Mirage / BHUGOL engines).

The project arrives as a private dataset (a .tar.gz of the built `proj/` folder, or the folder itself).
It installs Node + HyperFrames + chrome-headless-shell, then renders one composition in each configuration
listed in params["runs"] and writes bench.json with wall time, frames/s and whether Chrome got the GPU.

params:
  composition   e.g. "seg01.html"
  hyperframes   version to install, e.g. "0.8.181"
  deps          extra npm packages, e.g. {"gsap": "3.15.0", "three": "0.149.0"}
  quality       HyperFrames quality preset (default "looks")
  runs          list of {"name", "args"}; args are extra flags for `hyperframes render`
  baseline_s    optional: the same render's time elsewhere, for the speed-up figure
"""
import glob
import json
import os
import shutil
import subprocess
import tarfile
import threading
import time

P = json.loads(JOB_PARAMS)  # noqa: F821  (written into line 1 by tools/kaggle_run.py)
OUT = "/kaggle/working"
WORK = "/kaggle/tmp/bench"
os.makedirs(OUT, exist_ok=True)
os.makedirs(WORK, exist_ok=True)
REPORT = {"params": P, "steps": {}, "runs": []}


def save():
    with open(os.path.join(OUT, "bench.json"), "w") as fh:
        json.dump(REPORT, fh, indent=1)


def sh(cmd, timeout=1800, env=None, log=None):
    t = time.time()
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout, env=env)
    if log:
        with open(os.path.join(OUT, log), "w") as fh:
            fh.write(r.stdout + "\n--- stderr ---\n" + r.stderr)
    return r.returncode, round(time.time() - t, 1), (r.stdout + r.stderr)[-3000:]


def step(name, cmd, timeout=1800, env=None):
    rc, secs, tail = sh(cmd, timeout, env, log=f"step_{name}.log")
    REPORT["steps"][name] = {"rc": rc, "secs": secs}
    if rc:
        REPORT["steps"][name]["tail"] = tail[-1500:]
    save()
    print(f"{name}: rc={rc} {secs}s", flush=True)
    return rc


# 1. machine
REPORT["machine"] = {
    "gpu": sh("nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader")[2].strip(),
    "cpus": os.cpu_count(),
    "ram_gb": round(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 1e9, 1),
    "egl_vulkan_libs": sh("ls /usr/lib/x86_64-linux-gnu | grep -Ei 'libEGL_nvidia|libGLX_nvidia|nvidia_icd|libvulkan' | head")[2].strip(),
}
save()

# 2. project files from the attached dataset
proj = None
hits = glob.glob(f"/kaggle/input/**/{P['composition']}", recursive=True)
if hits:
    proj = os.path.dirname(hits[0])
else:
    for tgz in glob.glob("/kaggle/input/**/*.tar.gz", recursive=True):
        with tarfile.open(tgz) as t:
            t.extractall(WORK)
        hits = glob.glob(f"{WORK}/**/{P['composition']}", recursive=True)
        if hits:
            proj = os.path.dirname(hits[0])
            break
if not proj:
    REPORT["error"] = "project not found in /kaggle/input"
    save()
    raise SystemExit(REPORT["error"])
# work on a writable copy (renders/ and caches are written next to the project)
if not proj.startswith(WORK):
    shutil.copytree(proj, f"{WORK}/proj", dirs_exist_ok=True)
    proj = f"{WORK}/proj"
if not os.path.exists(f"{proj}/index.html"):  # the CLI looks for an index.html even when -c names another page
    shutil.copy(f"{proj}/{P['composition']}", f"{proj}/index.html")
REPORT["project"] = proj
save()

# 3. toolchain: Node 22, Chrome libraries, HyperFrames, chrome-headless-shell
NODE = "/kaggle/tmp/node"
step("node", f"mkdir -p {NODE} && curl -fsSL https://nodejs.org/dist/v22.11.0/node-v22.11.0-linux-x64.tar.xz"
             f" | tar -xJ -C {NODE} --strip-components=1 && {NODE}/bin/node -v", timeout=600)
env = dict(os.environ, PATH=f"{NODE}/bin:" + os.environ["PATH"], HYPERFRAMES_NO_TELEMETRY="1", DO_NOT_TRACK="1",
           HYPERFRAMES_NO_UPDATE_CHECK="1", HYPERFRAMES_SKIP_SKILLS="1")
LIBS = ("libnss3 libnspr4 libatk1.0-0t64 libatk-bridge2.0-0t64 libcups2t64 libdrm2 libxkbcommon0 libatspi2.0-0t64 "
        "libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2t64 "
        "fonts-noto-color-emoji")
# Ubuntu 24.04 renamed several libraries (...t64); fall back to the old name one package at a time
step("chrome_libs", "apt-get update -qq > /dev/null 2>&1; export DEBIAN_FRONTEND=noninteractive; "
                    f"for p in {LIBS}; do apt-get install -y -qq $p > /dev/null 2>&1 || "
                    "apt-get install -y -qq ${p%t64} > /dev/null 2>&1 || echo MISSING $p; done", timeout=900)
# Kaggle mounts the NVIDIA driver for CUDA; Chrome's WebGL also needs the driver's GL/Vulkan user-space libraries.
# Try the package that matches the running driver exactly (a mismatched one would not load).
REPORT["gl_diag_before"] = sh("ls /usr/lib/x86_64-linux-gnu | grep -Ei 'nvidia' | head -30; "
                              "ls /usr/share/vulkan/icd.d /etc/vulkan/icd.d /usr/share/glvnd/egl_vendor.d 2>&1")[2]
drv = REPORT["machine"]["gpu"].splitlines()[0].split(",")[-1].strip() if REPORT["machine"]["gpu"] else ""
step("nvidia_gl", f"V=$(apt-cache madison libnvidia-gl-{drv.split('.')[0]} | awk '{{print $3}}' | grep '^{drv}' | head -1); "
                  f"echo want {drv} found $V; [ -n \"$V\" ] && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq "
                  f"libnvidia-gl-{drv.split('.')[0]}=$V", timeout=900)
REPORT["gl_diag_after"] = sh("ls /usr/lib/x86_64-linux-gnu | grep -Ei 'nvidia' | head -30; "
                             "ls /usr/share/vulkan/icd.d /usr/share/glvnd/egl_vendor.d 2>&1")[2]
ENG = f"{WORK}/engine"
os.makedirs(ENG, exist_ok=True)
deps = {"hyperframes": P["hyperframes"], **P.get("deps", {})}
with open(f"{ENG}/package.json", "w") as fh:
    json.dump({"name": "bench-engine", "private": True, "dependencies": deps}, fh)
step("npm", f"cd {ENG} && npm install --no-audit --no-fund --loglevel=error", timeout=900, env=env)
step("browser", f"cd {ENG} && npx hyperframes browser ensure", timeout=900, env=env)
bp = sh(f"cd {ENG} && npx hyperframes browser path", env=env)[2].strip().splitlines()
if bp and os.path.exists(bp[-1].strip()):
    env["HYPERFRAMES_BROWSER_PATH"] = bp[-1].strip()
REPORT["browser_path"] = env.get("HYPERFRAMES_BROWSER_PATH", "default")
sh(f"cd {ENG} && npx hyperframes doctor", env=env, log="doctor.log")
save()

# 4. renders
fps = 30
for run in P["runs"]:
    out = f"{OUT}/{run['name']}.mp4"
    cmd = (f"cd {ENG} && npx hyperframes render {proj} -c {P['composition']} -o {out} "
           f"--quality {P.get('quality', 'looks')} --no-low-memory-mode {run.get('args', '')}")
    util = []
    stop = threading.Event()

    def sample():  # GPU utilisation while rendering: shows whether Chrome really used the T4
        while not stop.is_set():
            s = sh("nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits")[2].split()
            util.append(max([int(x) for x in s if x.isdigit()] or [0]))
            stop.wait(5)
    th = threading.Thread(target=sample, daemon=True)
    th.start()
    rc, secs, tail = sh(cmd, timeout=int(P.get("render_timeout_s", 3600)), env=env, log=f"render_{run['name']}.log")
    stop.set()
    th.join(10)
    dur = sh(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {out}")[2].strip()
    try:
        dur = float(dur)
    except ValueError:
        dur = None
    log = open(f"{OUT}/render_{run['name']}.log").read()
    gpu_lines = [ln.strip() for ln in log.splitlines() if any(k in ln.lower() for k in
                 ("gpu", "swiftshader", "webgl", "angle", "nvenc", "worker"))][:40]
    rec = {"name": run["name"], "args": run.get("args", ""), "rc": rc, "wall_s": secs, "video_s": dur,
           "fps_rendered": round(dur * fps / secs, 2) if dur else None,
           "speedup_vs_baseline": round(P["baseline_s"] / secs, 2) if P.get("baseline_s") and rc == 0 else None,
           "mb": round(os.path.getsize(out) / 1e6, 1) if os.path.exists(out) else None,
           "gpu_util_max": max(util) if util else None,
           "gpu_util_avg": round(sum(util) / len(util), 1) if util else None,
           "gpu_log_lines": gpu_lines}
    if rc:
        rec["tail"] = tail[-1500:]
    REPORT["runs"].append(rec)
    save()
    print(json.dumps(rec)[:400], flush=True)
    if rc == 0 and os.path.exists(out):  # small preview that fits in the repo, for a visual check
        sh(f"ffmpeg -v error -y -i {out} -vf scale=960:-2 -c:v libx264 -crf 30 -preset veryfast -an "
           f"{OUT}/{run['name']}_preview.mp4")

sh(f"nvidia-smi > {OUT}/nvidia_smi_end.txt")
print(json.dumps(REPORT, indent=1)[:4000])
