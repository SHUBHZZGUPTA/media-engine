"""Runs on Kaggle (2x T4). Test of SamurAIGPT/AI-Influencer-Generator's pipeline:
character image (Stable Diffusion 2.1) -> voiceover (gTTS) -> talking video (SadTalker).

Differences from the original Colab notebook, so it runs on Kaggle's current image:
  * the OpenAI "write an image prompt" step is replaced by a fixed prompt template (no API key)
  * Stable Diffusion runs in fp16 on the T4
  * SadTalker (OpenTalker/SadTalker, the maintained home of Winfredy's repo) runs inside a Python
    3.10 venv with torch 2.0.1 + cu118, because Kaggle's own Python 3.13 / torch 2.11 is too new
    for its pinned dependencies (basicsr, librosa 0.9, numpy 1.23)

Every stage is logged to run_log.json with its status and error tail, and a failed stage does not
stop later stages that can still run, so one run shows exactly what works.

Job params: characteristics (str), script (str), seed (int)."""
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import time
import traceback

P = json.loads(globals().get("JOB_PARAMS", "{}"))
CHARS = P.get("characteristics", "male European, wearing glasses and leather jacket with a smile on face")
SCRIPT = P.get(
    "script",
    "Our planet is a masterpiece of life, a delicate balance of ecosystems. But this harmony is under threat. "
    "Every year, 8 million tons of plastic enter our oceans, choking marine life.",
)
SEED = int(P.get("seed", 7))

OUT = "/kaggle/working"
LOGS = f"{OUT}/logs"
TMP = "/tmp/ai_influencer"
SAD = f"{TMP}/SadTalker"
VENV = f"{TMP}/sadenv"
VPY = f"{VENV}/bin/python"
os.makedirs(LOGS, exist_ok=True)
os.makedirs(TMP, exist_ok=True)
os.environ.setdefault("HF_HOME", "/tmp/hf")

t0 = time.time()
log = {"params": P, "stages": {}}


def save_log():
    log["total_seconds"] = round(time.time() - t0, 1)
    with open(f"{OUT}/run_log.json", "w") as f:
        json.dump(log, f, indent=1)


def sh(cmd, name, env=None, cwd=None, timeout=None):
    """Run a shell command, send its output to logs/<name>.txt, return (returncode, tail)."""
    path = f"{LOGS}/{name}.txt"
    with open(path, "w") as f:
        p = subprocess.run(cmd, shell=True, stdout=f, stderr=subprocess.STDOUT, env=env, cwd=cwd,
                           timeout=timeout, executable="/bin/bash")
    with open(path, errors="replace") as f:
        tail = f.read()[-1500:]
    print(f"$ {cmd[:140]} -> rc={p.returncode}", flush=True)
    if p.returncode:
        print(tail, flush=True)
    return p.returncode, tail


def duration(path):
    rc, out = sh(f"ffprobe -v error -show_entries format=duration -of csv=p=0 '{path}'", "ffprobe")
    try:
        return round(float(out.strip().splitlines()[-1]), 2)
    except Exception:
        return None


def stage(name, fn):
    start = time.time()
    print(f"=== {name}", flush=True)
    try:
        info = fn() or {}
        log["stages"][name] = {"ok": True, "seconds": round(time.time() - start, 1), **info}
    except Exception as e:
        log["stages"][name] = {
            "ok": False,
            "seconds": round(time.time() - start, 1),
            "error": f"{type(e).__name__}: {e}"[:1500],
            "trace": traceback.format_exc()[-2000:],
        }
        print(f"!!! {name} failed: {type(e).__name__}: {str(e)[:500]}", flush=True)
    save_log()
    return log["stages"][name]["ok"]


def need(*stages):
    for s in stages:
        if not log["stages"].get(s, {}).get("ok"):
            raise RuntimeError(f"skipped: needs stage '{s}' to have succeeded")


# ---------------------------------------------------------------- environment
def env_info():
    _, smi = sh("nvidia-smi --query-gpu=name,memory.total --format=csv,noheader", "nvidia_smi")
    info = {"python": sys.version.split()[0], "gpus": smi.strip()}
    try:
        import torch
        info["torch"] = torch.__version__
        info["cuda"] = torch.cuda.is_available()
    except Exception as e:
        info["torch"] = f"error: {e}"
    return info


# ---------------------------------------------------------------- stage 1: image
NEG = "deformed, blurry, bad anatomy, extra fingers, cropped face, text, watermark, sunglasses, hat"


def make_image():
    try:
        import diffusers, transformers, accelerate  # noqa: F401
    except Exception:
        sh(f"{sys.executable} -m pip install -q -U diffusers transformers accelerate", "pip_sd")
    import torch
    from diffusers import StableDiffusionPipeline

    prompt = (
        f"professional portrait photo of a {CHARS}, front-facing, looking at the camera, head and shoulders, "
        "face centered and fully visible, plain neutral background, soft studio lighting, sharp focus, "
        "highly detailed skin, photorealistic, 4k"
    )
    pipe, used, last = None, None, None
    for repo, kw in (
        ("stabilityai/stable-diffusion-2-1", {"variant": "fp16"}),
        ("stabilityai/stable-diffusion-2-1", {}),
        ("sd2-community/stable-diffusion-2-1", {}),
    ):
        try:
            pipe = StableDiffusionPipeline.from_pretrained(repo, torch_dtype=torch.float16, **kw)
            used = repo
            break
        except Exception as e:
            last = e
            print(f"could not load {repo} {kw}: {str(e)[:200]}", flush=True)
    if pipe is None:
        raise last
    pipe = pipe.to("cuda")
    gen = torch.Generator("cuda").manual_seed(SEED)
    img = pipe(prompt, negative_prompt=NEG, height=768, width=768, num_inference_steps=30,
               guidance_scale=7.5, generator=gen).images[0]
    img.save(f"{OUT}/avatar.png")
    del pipe
    torch.cuda.empty_cache()
    return {"model": used, "prompt": prompt, "size": list(img.size)}


# ---------------------------------------------------------------- stage 2: voice
def make_voice():
    try:
        import gtts  # noqa: F401
    except Exception:
        rc, t = sh(f"{sys.executable} -m pip install -q gtts", "pip_gtts")
        assert rc == 0, t
    from gtts import gTTS

    gTTS(SCRIPT).save(f"{OUT}/voice.mp3")
    rc, t = sh(f"ffmpeg -y -i {OUT}/voice.mp3 -ar 16000 -ac 1 {OUT}/voice.wav", "ffmpeg_voice")
    assert rc == 0 and os.path.exists(f"{OUT}/voice.wav"), t
    return {"words": len(SCRIPT.split()), "seconds_of_audio": duration(f"{OUT}/voice.wav")}


# ---------------------------------------------------------------- stage 3: SadTalker
def sad_clone():
    rc, t = sh(f"git clone --depth 1 https://github.com/OpenTalker/SadTalker {SAD}", "sad_clone")
    assert rc == 0, t
    _, commit = sh(f"git -C {SAD} rev-parse HEAD", "sad_commit")
    return {"commit": commit.strip()}


def sad_env():
    need("sad_clone")
    sh("apt-get update -qq && apt-get install -y -qq libgl1 libglib2.0-0", "apt_libs")  # best effort
    rc, t = sh(f"{sys.executable} -m pip install -q uv", "pip_uv")
    assert rc == 0, t
    rc, t = sh(f"{sys.executable} -m uv venv --python 3.10 {VENV}", "uv_venv")
    assert rc == 0, t
    uv = f"{sys.executable} -m uv pip install --python {VPY}"
    rc, t = sh(f"{uv} torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 "
               "--extra-index-url https://download.pytorch.org/whl/cu118 --index-strategy unsafe-best-match",
               "uv_torch")
    assert rc == 0, t
    rc, t = sh(f"{uv} 'setuptools<70' wheel cython numpy==1.23.4", "uv_build_deps")
    assert rc == 0, t
    # SadTalker's own requirements, minus torch (installed above), numpy (pinned above) and gradio (UI only)
    with open(f"{SAD}/requirements.txt") as f:
        keep = [l for l in f.read().splitlines()
                if l.strip() and not re.match(r"\s*(gradio|torch|torchvision|torchaudio|numpy)\b", l, re.I)]
    with open(f"{TMP}/req_filtered.txt", "w") as f:
        f.write("\n".join(keep) + "\n")
    rc, t = sh(f"{uv} --no-build-isolation -r {TMP}/req_filtered.txt", "uv_reqs")
    assert rc == 0, t
    rc, t = sh(f"{VPY} -c \"import torch,cv2,librosa,face_alignment,basicsr,gfpgan;"
               "print(torch.__version__, torch.cuda.is_available())\"", "sad_import_check")
    assert rc == 0, t
    return {"requirements": keep, "import_check": t.strip().splitlines()[-1]}


def sad_models():
    need("sad_clone")
    rc, t = sh("bash scripts/download_models.sh", "sad_models", cwd=SAD, timeout=1800)
    assert rc == 0, t
    files = sorted(os.listdir(f"{SAD}/checkpoints")) if os.path.isdir(f"{SAD}/checkpoints") else []
    assert files, "checkpoints folder is empty"
    return {"checkpoints": files}


def sad_run(tag, extra):
    need("make_image", "make_voice", "sad_env", "sad_models")
    rdir = f"{TMP}/results_{tag}"
    env = dict(os.environ, CUDA_VISIBLE_DEVICES="0", PYTHONNOUSERSITE="1")
    t = time.time()
    rc, tail = sh(f"{VPY} inference.py --driven_audio {OUT}/voice.wav --source_image {OUT}/avatar.png "
                  f"--result_dir {rdir} --still --preprocess full {extra}",
                  f"sad_run_{tag}", env=env, cwd=SAD, timeout=1500)
    vids = sorted(glob.glob(f"{rdir}/*.mp4"))
    assert rc == 0 and vids, tail
    dst = f"{OUT}/sadtalker_{tag}.mp4"
    shutil.copy(vids[0], dst)
    return {"video": os.path.basename(dst), "size_mb": round(os.path.getsize(dst) / 1e6, 2),
            "video_seconds": duration(dst), "render_seconds": round(time.time() - t, 1)}


def trim_logs(limit=300_000):
    for p in glob.glob(f"{LOGS}/*.txt"):
        if os.path.getsize(p) > limit:
            with open(p, "rb") as f:
                f.seek(-limit, os.SEEK_END)
                data = f.read()
            with open(p, "wb") as f:
                f.write(b"[trimmed to last 300 KB]\n" + data)


stage("env_info", env_info)
stage("make_image", make_image)
stage("make_voice", make_voice)
stage("sad_clone", sad_clone)
stage("sad_env", sad_env)
stage("sad_models", sad_models)
stage("sad_run_plain", lambda: sad_run("plain", ""))
stage("sad_run_gfpgan", lambda: sad_run("gfpgan", "--enhancer gfpgan"))

trim_logs()
save_log()
print(json.dumps({k: v.get("ok") for k, v in log["stages"].items()}, indent=1), flush=True)
