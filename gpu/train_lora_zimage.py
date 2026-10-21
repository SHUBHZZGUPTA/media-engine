"""Runs on Kaggle (T4). Trains a character LoRA for Z-Image-Turbo with ostris/ai-toolkit,
using its Z-Image Turbo preset (training adapter, 8-bit quantized base model).

Job params:
  aitk_commit       ai-toolkit commit to use
  trigger           trigger word used in the captions (for the log only)
  dataset           list of {name, url, caption}; images are downloaded at run time
  steps, rank, lr   training length, LoRA rank, learning rate
  resolutions       e.g. [512, 768]
  save_every        checkpoint interval (checkpoints land in /kaggle/working/lora)
  sample_every      sample interval, 0 = no samples
  sample_prompts    prompts for sample images

Everything worth keeping (LoRA files, samples, logs, timing) is written to /kaggle/working."""
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request

P = json.loads(globals().get("JOB_PARAMS", "{}"))
OUT = "/kaggle/working"
WORK = "/tmp/train"
AITK = "/tmp/ai-toolkit"
os.makedirs(OUT, exist_ok=True)
os.makedirs(WORK, exist_ok=True)
os.environ["HF_HOME"] = "/tmp/hf"
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
log = {"params": {k: v for k, v in P.items() if k != "dataset"}, "images": len(P["dataset"]), "timings": {}}
t0 = time.time()


def stamp(name):
    log["timings"][name] = round(time.time() - t0, 1)
    print(f"[{log['timings'][name]:>8}s] {name}", flush=True)
    save_log()


def save_log():
    with open(os.path.join(OUT, "train_run.json"), "w") as f:
        json.dump(log, f, indent=1)


def sh(cmd, **kw):
    print("$", cmd, flush=True)
    return subprocess.run(cmd, shell=True, check=True, **kw)


# 1) ai-toolkit at a fixed commit, with its requirements minus pieces Kaggle's Python 3.13 / torch
#    can't take (the old scipy pin; torchcodec, which is tied to a torch version) and that training
#    never imports (gradio, pytorch_fid). Audio libraries are imported at startup, so they stay,
#    unpinned so Python 3.13 wheels are used.
sh(f"git init -q {AITK} && cd {AITK} && git remote add origin https://github.com/ostris/ai-toolkit.git"
   f" && git fetch -q --depth 1 origin {P['aitk_commit']} && git checkout -q FETCH_HEAD"
   f" && git submodule update --init --recursive --depth 1 -q || true")
skip = re.compile(r"^(scipy|torchcodec|gradio|pytorch_fid|torchao)\b")
unpin = re.compile(r"^(av|librosa|mutagen)==")
reqs = [l.strip() for l in open(f"{AITK}/requirements_base.txt") if l.strip() and not l.startswith("#")]
keep = [r.split("==")[0] if unpin.match(r) else r for r in reqs if not skip.match(r)]
with open(f"{WORK}/requirements.txt", "w") as f:
    f.write("\n".join(keep) + "\n")
sh(f"{sys.executable} -m pip install -q -r {WORK}/requirements.txt")
try:
    sh(f"{sys.executable} -m pip install -q torchao")
except subprocess.CalledProcessError:
    print("torchao install failed; continuing without it", flush=True)
stamp("ai-toolkit installed")

# 2) Dataset: download, cap the long side at 1536 px, write captions.
from PIL import Image  # noqa: E402

data_dir = f"{WORK}/dataset"
os.makedirs(data_dir, exist_ok=True)
for item in P["dataset"]:
    raw = f"{WORK}/{item['name']}.download"
    for attempt in range(3):
        try:
            urllib.request.urlretrieve(item["url"], raw)
            break
        except Exception:
            time.sleep(5)
    im = Image.open(raw).convert("RGB")
    im.thumbnail((1536, 1536))
    im.save(f"{data_dir}/{item['name']}.png")
    with open(f"{data_dir}/{item['name']}.txt", "w") as f:
        f.write(item["caption"])
    os.remove(raw)
stamp(f"dataset ready ({len(P['dataset'])} images)")

# 3) Config: ai-toolkit's Z-Image Turbo preset with the training adapter.
steps = int(P["steps"])
sample_every = int(P.get("sample_every", 0)) or steps * 10
config = {
    "job": "extension",
    "config": {
        "name": "tira_zimage_lora",
        "process": [{
            "type": "sd_trainer",
            "training_folder": f"{WORK}/output",
            "device": "cuda:0",
            "network": {"type": "lora", "linear": int(P.get("rank", 16)), "linear_alpha": int(P.get("rank", 16))},
            "save": {"dtype": "float16", "save_every": int(P.get("save_every", 250)),
                     "max_step_saves_to_keep": 20},
            "datasets": [{"folder_path": data_dir, "caption_ext": "txt", "caption_dropout_rate": 0.05,
                          "cache_latents_to_disk": True, "resolution": P.get("resolutions", [512, 768])}],
            "train": {"batch_size": 1, "steps": steps, "gradient_accumulation_steps": 1, "train_unet": True,
                      "train_text_encoder": False, "gradient_checkpointing": True, "noise_scheduler": "flowmatch",
                      "timestep_type": "weighted", "optimizer": "adamw8bit", "lr": float(P.get("lr", 1e-4)),
                      "dtype": "bf16", "unload_text_encoder": False, "skip_first_sample": True,
                      "ema_config": {"use_ema": False}},
            "model": {"name_or_path": "Tongyi-MAI/Z-Image-Turbo", "arch": "zimage", "quantize": True,
                      "qtype": "qfloat8", "quantize_te": True, "low_vram": True,
                      "assistant_lora_path": "ostris/zimage_turbo_training_adapter/"
                                             "zimage_turbo_training_adapter_v2.safetensors"},
            "sample": {"sampler": "flowmatch", "sample_every": sample_every, "width": 768, "height": 1024,
                       "prompts": P.get("sample_prompts", []), "seed": 42, "walk_seed": True,
                       "guidance_scale": 1, "sample_steps": 9},
        }],
    },
    "meta": {"name": "tira_zimage_lora", "version": "1.0"},
}
import yaml  # noqa: E402

cfg_path = f"{WORK}/config.yaml"
with open(cfg_path, "w") as f:
    yaml.safe_dump(config, f, sort_keys=False)
shutil.copy(cfg_path, f"{OUT}/config.yaml")
stamp("config written")

# 4) Train. A T4 runs out of memory on bf16 attention at 768 px (it can only use the
#    memory-efficient attention kernel in fp16), so a small t4patch module, imported before
#    the trainer starts, computes attention in fp16, with a chunked fp32 fallback if a call overflows.
#    Output streams to train_log.txt; step speed is read from the progress bar.
patch_dir = f"{WORK}/t4patch"
os.makedirs(patch_dir, exist_ok=True)
with open(f"{patch_dir}/t4patch.py", "w") as f:
    f.write('''
import torch
_sdpa = torch.nn.functional.scaled_dot_product_attention
_stats = {"fp16": 0, "fp32_fallback": 0}

def _attention_t4(query, key, value, attn_mask=None, dropout_p=0.0, is_causal=False, scale=None,
                  enable_gqa=False):
    if query.dtype != torch.bfloat16 or not query.is_cuda:
        return _sdpa(query, key, value, attn_mask=attn_mask, dropout_p=dropout_p, is_causal=is_causal,
                     scale=scale, enable_gqa=enable_gqa)
    _stats["fp16"] += 1
    with torch.nn.attention.sdpa_kernel([torch.nn.attention.SDPBackend.EFFICIENT_ATTENTION,
                                         torch.nn.attention.SDPBackend.MATH]):
        out = _sdpa(query.half(), key.half(), value.half(), attn_mask=attn_mask, dropout_p=dropout_p,
                    is_causal=is_causal, scale=scale, enable_gqa=enable_gqa)
    if torch.isfinite(out).all():
        return out.to(torch.bfloat16)
    _stats["fp32_fallback"] += 1
    k, v = key.float(), value.float()
    chunks = []
    for i in range(0, query.shape[-2], 1024):
        m = attn_mask
        if m is not None and m.dim() >= 2 and m.shape[-2] > 1:
            m = m[..., i:i + 1024, :]
        chunks.append(_sdpa(query[..., i:i + 1024, :].float(), k, v, attn_mask=m, dropout_p=dropout_p,
                            is_causal=is_causal, scale=scale, enable_gqa=enable_gqa))
    return torch.cat(chunks, dim=-2).to(torch.bfloat16)

torch.nn.functional.scaled_dot_product_attention = _attention_t4
import atexit
atexit.register(lambda: print("T4 attention patch stats:", _stats, flush=True))
''')
env = dict(os.environ, PYTHONPATH=patch_dir + os.pathsep + os.environ.get("PYTHONPATH", ""))
train_log = open(f"{OUT}/train_log.txt", "w")
launcher = ("import sys, runpy, t4patch; sys.argv = ['run.py', sys.argv[1]]; "
            "runpy.run_path('run.py', run_name='__main__')")
proc = subprocess.Popen([sys.executable, "-c", launcher, cfg_path], cwd=AITK, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, text=True, bufsize=1, env=env)
step_re = re.compile(r"(\d+)/(\d+) \[[^\]]*?([\d.]+)(s/it|it/s)")
last = None
for line in proc.stdout:
    train_log.write(line)
    train_log.flush()
    for m in step_re.finditer(line):
        done, total, val, unit = int(m.group(1)), int(m.group(2)), float(m.group(3)), m.group(4)
        if total == steps:
            sec = val if unit == "s/it" else 1 / val
            log["last_step"], log["sec_per_step"] = done, round(sec, 2)
            if done != last and (done % 5 == 0 or done == total):
                last = done
                save_log()
    if "Traceback" in line or "Error" in line:
        print(line.rstrip(), flush=True)
rc = proc.wait()
log["exit_code"] = rc
stamp("training finished" if rc == 0 else f"training failed (exit {rc})")

# 5) Collect LoRA files and samples.
os.makedirs(f"{OUT}/lora", exist_ok=True)
for root, _, files in os.walk(f"{WORK}/output"):
    for name in files:
        if name.endswith(".safetensors") or root.endswith("samples"):
            shutil.copy(os.path.join(root, name), f"{OUT}/lora/{name}")
log["outputs"] = sorted(os.listdir(f"{OUT}/lora"))
log["peak_gpu_mem_note"] = "see train_log.txt"
save_log()
print(json.dumps(log, indent=1))
sys.exit(rc)
