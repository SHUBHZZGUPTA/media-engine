"""Runs on Kaggle. Renders a batch of small HyperFrames projects (e.g. long-form 3D globe/terrain clips) on the
GPU(s), several at once, and records how long the whole batch and each clip took and how busy each GPU was.

The projects arrive as a private dataset: a .tar.gz holding <name>/index.html folders (self-contained: assets,
gsap/three copied in). Setup (Node, Chrome libraries, NVIDIA GL user-space libraries, HyperFrames) is the same as
gpu/render_bench.py.

params:
  hyperframes   version, e.g. "0.8.181"
  render_args   extra flags for every `hyperframes render`, e.g. "--crf 16 --fps 30 --workers 2"
  lanes         list of {"name", "env"}: one render runs per lane at a time. Two lanes with
                CUDA_VISIBLE_DEVICES / device hints = a two-GPU test; the GPU sampler records each GPU separately.
  gl_unpack     true: unpack the driver's GL/EGL/Vulkan libraries (needed for WebGL on the T4)
Writes /kaggle/working/clips/<name>.mp4 and batch.json.
"""
import glob
import json
import os
import queue
import re
import subprocess
import tarfile
import threading
import time

P = json.loads(JOB_PARAMS)  # noqa: F821  (written into line 1 by tools/kaggle_run.py)
OUT = "/kaggle/working"
WORK = "/kaggle/tmp/batch"
os.makedirs(f"{OUT}/clips", exist_ok=True)
os.makedirs(WORK, exist_ok=True)
REPORT = {"params": P, "steps": {}, "clips": []}
T_START = time.time()


def save():
    with open(os.path.join(OUT, "batch.json"), "w") as fh:
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


REPORT["machine"] = {
    "gpu": sh("nvidia-smi --query-gpu=index,name,memory.total,driver_version --format=csv,noheader")[2].strip(),
    "cpus": os.cpu_count(),
    "ram_gb": round(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 1e9, 1),
}
save()

# 1. projects
# Kaggle unpacks .tar.gz datasets itself and may drop symlinks, so the bundle is uploaded as <name>.tgz.bin
for tgz in glob.glob("/kaggle/input/**/*.tgz.bin", recursive=True) + glob.glob("/kaggle/input/**/*.tar.gz", recursive=True):
    with tarfile.open(tgz, "r:gz") as t:
        t.extractall(WORK)
REPORT["input_listing"] = sh("find /kaggle/input -maxdepth 4 | head -40")[2]
projects = sorted({os.path.dirname(p) for p in glob.glob(f"{WORK}/**/index.html", recursive=True)})
if not projects:
    REPORT["error"] = "no <name>/index.html projects found in the dataset"
    save()
    raise SystemExit(REPORT["error"])
REPORT["projects"] = [os.path.basename(p) for p in projects]
save()

# 2. toolchain (same as render_bench.py)
NODE = "/kaggle/tmp/node"
step("node", f"mkdir -p {NODE} && curl -fsSL https://nodejs.org/dist/v22.11.0/node-v22.11.0-linux-x64.tar.xz"
             f" | tar -xJ -C {NODE} --strip-components=1 && {NODE}/bin/node -v", timeout=600)
env = dict(os.environ, PATH=f"{NODE}/bin:" + os.environ["PATH"], HYPERFRAMES_NO_TELEMETRY="1", DO_NOT_TRACK="1",
           HYPERFRAMES_NO_UPDATE_CHECK="1", HYPERFRAMES_SKIP_SKILLS="1")
LIBS = ("libnss3 libnspr4 libatk1.0-0t64 libatk-bridge2.0-0t64 libcups2t64 libdrm2 libxkbcommon0 libatspi2.0-0t64 "
        "libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2t64 "
        "fonts-noto-color-emoji")
step("chrome_libs", "apt-get update -qq > /dev/null 2>&1; export DEBIAN_FRONTEND=noninteractive; "
                    f"for p in {LIBS}; do apt-get install -y -qq $p > /dev/null 2>&1 || "
                    "apt-get install -y -qq ${p%t64} > /dev/null 2>&1 || echo MISSING $p; done", timeout=900)
drv = REPORT["machine"]["gpu"].splitlines()[0].split(",")[-1].strip() if REPORT["machine"]["gpu"] else ""
major = drv.split(".")[0]
if P.get("gl_unpack", True) and drv:
    step("nvidia_gl", "export DEBIAN_FRONTEND=noninteractive; apt-get install -y -qq libegl1 libgl1 libglvnd0 "
                      "libvulkan1 > /dev/null 2>&1; mkdir -p /kaggle/tmp/debs && cd /kaggle/tmp/debs && "
                      f"for p in libnvidia-gl-{major} libnvidia-gpucomp-{major} libnvidia-egl-wayland1; do "
                      f"V=$(apt-cache madison $p | awk '{{print $3}}' | grep '^{drv}' | head -1); "
                      "[ -z \"$V\" ] && V=$(apt-cache madison $p | awk '{print $3}' | head -1); "
                      "[ -n \"$V\" ] && apt-get download -qq $p=$V; done; "
                      "for d in *.deb; do dpkg -x $d / && echo unpacked $d; done; ldconfig", timeout=900)
ENG = f"{WORK}/engine"
os.makedirs(ENG, exist_ok=True)
with open(f"{ENG}/package.json", "w") as fh:
    json.dump({"name": "batch-engine", "private": True, "dependencies": {"hyperframes": P["hyperframes"]}}, fh)
step("npm", f"cd {ENG} && npm install --no-audit --no-fund --loglevel=error", timeout=900, env=env)
step("browser", f"cd {ENG} && npx hyperframes browser ensure", timeout=900, env=env)
bp = sh(f"cd {ENG} && npx hyperframes browser path", env=env)[2].strip().splitlines()
if bp and os.path.exists(bp[-1].strip()):
    env["HYPERFRAMES_BROWSER_PATH"] = bp[-1].strip()
HF = f"{ENG}/node_modules/.bin/hyperframes"

# WebGL probe per lane: which GPU / renderer does Chrome get with that lane's environment?
with open(f"{WORK}/probe.html", "w") as fh:
    fh.write("<canvas id=c></canvas><script>var g=document.getElementById('c').getContext('webgl2')||"
             "document.getElementById('c').getContext('webgl');var r='NO_WEBGL';if(g){var e=g.getExtension("
             "'WEBGL_debug_renderer_info');r=e?g.getParameter(e.UNMASKED_RENDERER_WEBGL):g.getParameter(g.RENDERER);}"
             "document.body.setAttribute('data-r',r);</script>")
REPORT["probe"] = {}
for lane in P["lanes"]:
    lenv = dict(env, **lane.get("env", {}))
    sh(f"timeout 60 {env.get('HYPERFRAMES_BROWSER_PATH')} --headless --no-sandbox --use-gl=angle --use-angle=gl-egl "
       f"--ignore-gpu-blocklist {lane.get('chrome_probe_flags', '')} --virtual-time-budget=3000 --dump-dom "
       f"file://{WORK}/probe.html", env=lenv, log=f"probe_{lane['name']}.log")
    m = re.search(r'data-r="([^"]*)"', open(f"{OUT}/probe_{lane['name']}.log").read())
    REPORT["probe"][lane["name"]] = m.group(1) if m else "no result"
save()
print("probe:", REPORT["probe"], flush=True)
REPORT["setup_s"] = round(time.time() - T_START, 1)

# 3. the batch: one worker thread per lane pulls clips off a shared queue (longest first)
def frames(p):
    m = re.search(r"__DUR__|data-duration=\"([\d.]+)\"", open(f"{p}/index.html").read())
    return float(m.group(1)) if m and m.group(1) else 0.0
q = queue.Queue()
for p in sorted(projects, key=frames, reverse=True):
    q.put(p)
util = {}
stop = threading.Event()


def sample():
    while not stop.is_set():
        for ln in sh("nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv,noheader,nounits")[2].splitlines():
            parts = [x.strip() for x in ln.split(",")]
            if len(parts) == 3 and parts[0].isdigit():
                util.setdefault(parts[0], []).append([int(parts[1]), int(parts[2])])
        stop.wait(3)


lock = threading.Lock()


def lane_worker(lane):
    lenv = dict(env, **lane.get("env", {}))
    while True:
        try:
            p = q.get_nowait()
        except queue.Empty:
            return
        name = os.path.basename(p)
        out = f"{OUT}/clips/{name}.mp4"
        rc, secs, tail = sh(f"cd {p} && {HF} render {P.get('render_args', '')} --output {out}",
                            timeout=int(P.get("render_timeout_s", 2400)), env=lenv, log=f"render_{name}.log")
        dur = sh(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {out}")[2].strip()
        rec = {"clip": name, "lane": lane["name"], "rc": rc, "wall_s": secs,
               "video_s": float(dur) if re.fullmatch(r"[\d.]+", dur or "") else None,
               "started_s": round(time.time() - T_START - secs, 1)}
        if rc:
            rec["tail"] = tail[-800:]
        with lock:
            REPORT["clips"].append(rec)
            save()
        print(json.dumps(rec)[:300], flush=True)


th = threading.Thread(target=sample, daemon=True)
th.start()
t0 = time.time()
workers = [threading.Thread(target=lane_worker, args=(ln,)) for ln in P["lanes"]]
for w in workers:
    w.start()
for w in workers:
    w.join()
stop.set()
th.join(10)
REPORT["batch_wall_s"] = round(time.time() - t0, 1)
REPORT["video_s_total"] = round(sum(c["video_s"] or 0 for c in REPORT["clips"]), 1)
REPORT["gpu_util"] = {k: {"max": max(u for u, _ in v), "avg": round(sum(u for u, _ in v) / len(v), 1),
                          "mem_max_mb": max(m for _, m in v), "busy_share": round(sum(1 for u, _ in v if u > 5) / len(v), 2)}
                      for k, v in util.items() if v}
REPORT["total_wall_s"] = round(time.time() - T_START, 1)
save()
print(json.dumps({k: REPORT[k] for k in ("setup_s", "batch_wall_s", "video_s_total", "gpu_util", "total_wall_s")}), flush=True)
