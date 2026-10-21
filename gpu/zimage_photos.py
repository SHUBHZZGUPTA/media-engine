"""Runs on Kaggle. Generates photos with Z-Image-Turbo from the job's prompt and seeds,
and saves them with the prompt and timings to /kaggle/working.

Job params: prompt (str), seeds (list of int), width, height (multiples of 16), steps."""
import json
import os
import subprocess
import sys
import time

P = json.loads(globals().get("JOB_PARAMS", "{}"))
OUT = "/kaggle/working"
os.makedirs(OUT, exist_ok=True)
os.environ.setdefault("HF_HOME", "/tmp/hf")  # large scratch disk, not the 20 GB output disk
log = {"params": P, "timings": {}}
t0 = time.time()


def stamp(name):
    log["timings"][name] = round(time.time() - t0, 1)
    print(f"[{log['timings'][name]:>7}s] {name}", flush=True)


def pip(*args):
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", *args], check=True)


try:
    from diffusers import ZImagePipeline
except Exception:
    pip("-U", "diffusers", "transformers", "accelerate")
    try:
        from diffusers import ZImagePipeline
    except Exception:
        pip("git+https://github.com/huggingface/diffusers")
        from diffusers import ZImagePipeline
import diffusers
import torch

log["diffusers"] = diffusers.__version__
stamp("imports ready")

pipe = ZImagePipeline.from_pretrained("Tongyi-MAI/Z-Image-Turbo", torch_dtype=torch.bfloat16,
                                      low_cpu_mem_usage=False)
pipe.enable_model_cpu_offload()  # T4 has 15.6 GB; parts move to the GPU only while in use
stamp("model loaded")

width, height = int(P.get("width", 1152)), int(P.get("height", 1536))
steps = int(P.get("steps", 9))
files = []
for seed in P.get("seeds", [1]):
    image = pipe(prompt=P["prompt"], height=height, width=width, num_inference_steps=steps,
                 guidance_scale=0.0, generator=torch.Generator("cuda").manual_seed(int(seed))).images[0]
    name = f"photo_seed{seed}.png"
    image.save(os.path.join(OUT, name))
    files.append(name)
    stamp(f"saved {name}")

log["files"] = files
log["gpu"] = torch.cuda.get_device_name(0)
log["peak_vram_gb"] = round(torch.cuda.max_memory_allocated() / 1e9, 1)
with open(os.path.join(OUT, "prompt.txt"), "w") as f:
    f.write(P["prompt"] + "\n")
with open(os.path.join(OUT, "run_log.json"), "w") as f:
    json.dump(log, f, indent=1)
print(json.dumps(log, indent=1))
