"""Runs on Kaggle (T4). Tests whether HyperFrames' WebGPU shader blocks render on a real GPU.

Steps: install Node 22 + hyperframes@0.8.181 + chrome-headless-shell, probe WebGPU in Chrome with
three flag sets, then snapshot and render a set of WebGPU blocks (plus vfx-magnetic, which stayed
blank on the CPU box). Everything lands in /kaggle/working: <block>.png, <block>.mp4, logs, report.json.
"""
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

P = json.loads(globals().get("JOB_PARAMS", "{}"))
BLOCKS = P.get("blocks", ["aurora", "nebula", "liquid-metal", "water", "hologram", "godrays",
                          "mesh-gradient", "chrome-orb", "vfx-magnetic"])
RENDER = set(P.get("render", BLOCKS))
OUT = Path("/kaggle/working"); OUT.mkdir(parents=True, exist_ok=True)
WORK = Path("/kaggle/tmp/hf"); WORK.mkdir(parents=True, exist_ok=True)
report = {"started": time.strftime("%Y-%m-%d %H:%M:%S"), "blocks": {}}
ENV = dict(os.environ, HYPERFRAMES_NO_TELEMETRY="1", DO_NOT_TRACK="1",
           HYPERFRAMES_NO_UPDATE_CHECK="1", HYPERFRAMES_SKIP_SKILLS="1")


def sh(cmd, cwd=None, env=None, timeout=1800, log=None):
    t = time.time()
    r = subprocess.run(cmd, shell=True, cwd=cwd, env=env or ENV, capture_output=True, text=True, timeout=timeout)
    text = (r.stdout or "") + (r.stderr or "")
    if log:
        (OUT / log).write_text(f"$ {cmd}\nrc={r.returncode} {time.time() - t:.0f}s\n{text}")
    return r.returncode, text, round(time.time() - t)


def save():
    (OUT / "report.json").write_text(json.dumps(report, indent=1))


# 1. System
report["nvidia_smi"] = sh("nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader")[1].strip()
report["vulkan_icd_files"] = sh("ls /usr/share/vulkan/icd.d /etc/vulkan/icd.d 2>&1")[1].strip()

# 2. Node 22 + hyperframes + headless shell
NODE = "node-v22.12.0-linux-x64"
if not Path(f"/kaggle/tmp/{NODE}").exists():
    sh(f"cd /kaggle/tmp && curl -sSL https://nodejs.org/dist/v22.12.0/{NODE}.tar.xz | tar xJ", log="00_node.log")
ENV["PATH"] = f"/kaggle/tmp/{NODE}/bin:" + ENV["PATH"]
# Vulkan loader + tools so Chrome can reach the NVIDIA driver; harmless if already present.
PKGS = ("libvulkan1 vulkan-tools mesa-vulkan-drivers libatk1.0-0t64 libatk1.0-0 libatk-bridge2.0-0t64 libatk-bridge2.0-0 libcups2t64 libcups2 "
        "libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2t64 libasound2 libnss3 libxss1 "
        "libxshmfence1 libdrm2 libegl1 libgl1 libatspi2.0-0t64 libatspi2.0-0 libxfixes3 libxext6 libx11-6 libxcb1").split()
sh("apt-get -qq update > /dev/null 2>&1", timeout=600)
report["apt"] = {p: sh(f"apt-get -qq install -y --no-install-recommends {p} > /dev/null 2>&1", timeout=600)[0] for p in PKGS}
report["nvidia_libs"] = sh("ls /usr/local/nvidia/lib64 2>&1 | grep -iE 'vulkan|glx|egl|gpucomp|glvk' | head -20")[1].strip()
report["driver_caps"] = os.environ.get("NVIDIA_DRIVER_CAPABILITIES", "unset")
icd = Path("/usr/share/vulkan/icd.d/nvidia_icd.json")
if not icd.exists():
    lib = sh("ldconfig -p | grep -o '/[^ ]*libGLX_nvidia.so.0' | head -1")[1].strip() or "libGLX_nvidia.so.0"
    icd.parent.mkdir(parents=True, exist_ok=True)
    icd.write_text(json.dumps({"file_format_version": "1.0.0",
                               "ICD": {"library_path": lib, "api_version": "1.3"}}))
    report["icd_written"] = lib
report["vulkaninfo"] = sh("vulkaninfo --summary 2>&1 | grep -E 'deviceName|driverName|apiVersion' | head -8")[1].strip()
report["vulkan_loader_errors"] = sh("VK_LOADER_DEBUG=error,warn vulkaninfo --summary 2>&1 | grep -iE 'nvidia|error|warn' | head -15")[1].strip()[-2500:]

rc, txt, s = sh("npm init -y >/dev/null && npm i hyperframes@0.8.181 puppeteer-core@23 >/dev/null 2>&1 && "
                "npx hyperframes browser ensure", cwd=WORK, log="01_install.log", timeout=1800)
report["install"] = {"rc": rc, "sec": s}
shell = sh("find ~/.cache /root/.cache -type f -name chrome-headless-shell 2>/dev/null | head -1")[1].strip()
report["headless_shell"] = shell
if shell:
    ENV["HYPERFRAMES_BROWSER_PATH"] = shell
save()

# 3. WebGPU probe: which Chrome flags give a hardware adapter?
probe = r"""
const p=require('puppeteer-core');(async()=>{const out={};
const sets={vulkan:['--enable-unsafe-webgpu','--enable-features=Vulkan,CanvasDrawElement','--use-angle=vulkan','--ignore-gpu-blocklist'],
 egl:['--enable-unsafe-webgpu','--use-gl=angle','--use-angle=gl-egl','--ignore-gpu-blocklist'],
 default:['--enable-unsafe-webgpu','--ignore-gpu-blocklist']};
for(const [k,args] of Object.entries(sets)){try{const b=await p.launch({executablePath:process.env.HYPERFRAMES_BROWSER_PATH,headless:'shell',args:['--no-sandbox',...args]});
const pg=await b.newPage();out[k+'_gpu_page']=await (async()=>{try{await pg.goto('chrome://gpu');return (await pg.evaluate(()=>document.body.innerText)).slice(0,1500)}catch(e){return 'gpu page: '+e.message}})();out[k]=await pg.evaluate(async()=>{if(!navigator.gpu)return 'no navigator.gpu';
const a=await navigator.gpu.requestAdapter({powerPreference:'high-performance'});if(!a)return 'no adapter';
const i=a.info||{};return {vendor:i.vendor,architecture:i.architecture,device:i.device,description:i.description,fallback:a.isFallbackAdapter||false};});
await b.close();}catch(e){out[k]='error: '+e.message}}console.log(JSON.stringify(out));})();
"""
(WORK / "probe.js").write_text(probe)
report["chrome_missing_libs"] = sh(f"ldd {shell} | grep 'not found'")[1].strip() if shell else "no shell"
rc, txt, s = sh("node probe.js", cwd=WORK, log="02_probe.log", timeout=300)
try:
    report["webgpu_probe"] = json.loads(txt.strip().splitlines()[-1])
except Exception:
    report["webgpu_probe"] = txt[-1500:]
save()

# 4. Blocks: install, snapshot one frame, render to MP4
sh("npx hyperframes init proj --example blank --non-interactive", cwd=WORK, log="03_init.log")
proj = WORK / "proj"
cat = json.loads(sh("npx hyperframes catalog --json", cwd=WORK)[1] or "[]")
dims = {i["name"]: ((i.get("dimensions") or {}).get("width") or 1280, (i.get("dimensions") or {}).get("height") or 720,
                    min(float(i.get("duration") or 5), 6)) for i in cat}

for n in BLOCKS:
    r = {}
    rc, txt, s = sh(f"npx hyperframes add {n} --no-clipboard --json", cwd=proj)
    r["add_rc"] = rc
    if n not in dims or rc != 0:
        report["blocks"][n] = r; save(); continue
    w, h, d = dims[n]
    bp = WORK / f"p_{n}"
    if bp.exists():
        shutil.rmtree(bp)
    shutil.copytree(proj, bp, ignore=shutil.ignore_patterns("node_modules", "renders", ".hyperframes"))
    for f in (bp / "compositions").glob("*.html"):
        if f.stem != n:
            f.unlink()
    (bp / "index.html").write_text(f"""<!doctype html><html><head><meta charset="UTF-8"><meta name="viewport" content="width={w}, height={h}">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0}}html,body{{width:{w}px;height:{h}px;overflow:hidden;background:#000}}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{d}" data-width="{w}" data-height="{h}">
<div data-composition-id="{n}" data-composition-src="compositions/{n}.html" data-start="0" data-duration="{d}" data-width="{w}" data-height="{h}" data-track-index="0"></div></div>
<script>const tl=gsap.timeline({{paused:true}});window.__timelines["main"]=tl;</script></body></html>""")
    # snapshot: try hardware GPU first, then let hyperframes auto-detect
    for gm in ("hardware", "auto"):
        env = dict(ENV, PRODUCER_BROWSER_GPU_MODE=gm)
        snapdir = WORK / f"snap_{n}_{gm}"
        rc, txt, s = sh(f"npx hyperframes snapshot {bp} --no-end --describe false --at {d * 0.5:.2f} "
                        f"-o {snapdir} --timeout 30000 --browser-gpu", env=env, log=f"snap_{n}_{gm}.log", timeout=600)
        pngs = sorted(snapdir.glob("*.png"))
        r[f"snap_{gm}"] = {"rc": rc, "sec": s, "frames": len(pngs)}
        if pngs:
            shutil.copy(pngs[0], OUT / f"{n}.png")
            r["gpu_mode"] = gm
            break
    if n in RENDER and "gpu_mode" in r:
        env = dict(ENV, PRODUCER_BROWSER_GPU_MODE=r["gpu_mode"])
        rc, txt, s = sh(f"npx hyperframes render {bp} -q draft --browser-gpu -o {OUT / (n + '.mp4')}",
                        env=env, log=f"render_{n}.log", timeout=1500)
        r["render"] = {"rc": rc, "sec": s, "video_sec": d,
                       "mb": round((OUT / f"{n}.mp4").stat().st_size / 1e6, 2) if (OUT / f"{n}.mp4").exists() else 0}
    report["blocks"][n] = r
    save()

report["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
save()
print(json.dumps(report, indent=1))
