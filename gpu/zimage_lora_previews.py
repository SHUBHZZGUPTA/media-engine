"""Runs on Kaggle (2x T4). Makes preview images from each saved LoRA version so they can be
compared: the same prompts and the same seed for every version, so differences come from training.

LoRA files come from an attached Kaggle input (a dataset staged by tools/kaggle_run.py).
T4 layout is the same as gpu/zimage_photos.py: prompts encoded once on GPU 1, image model in bf16
on GPU 0 with attention computed in fp16 (chunked fp32 fallback), VAE decode in fp32 at the end.

Job params: prompts (list), lora_glob (filename pattern), seed, width, height, steps,
lora_scale, include_base (also render without any LoRA)."""
import gc
import glob
import json
import os
import re
import subprocess
import sys
import time

os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
os.environ.setdefault("HF_HOME", "/tmp/hf")

P = json.loads(globals().get("JOB_PARAMS", "{}"))
OUT = "/kaggle/working"
os.makedirs(OUT, exist_ok=True)
log = {"params": P, "timings": {}, "images": []}
t0 = time.time()


def stamp(name):
    log["timings"][name] = round(time.time() - t0, 1)
    print(f"[{log['timings'][name]:>7}s] {name}", flush=True)
    with open(os.path.join(OUT, "run_log.json"), "w") as f:
        json.dump(log, f, indent=1)


def pip(*args):
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", *args], check=True)


# Kaggle's image ships torchao 0.10, which the LoRA loader (peft) rejects outright; it isn't needed.
subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "-q", "torchao"], check=False)
try:
    from diffusers import ZImagePipeline
    import peft  # noqa: F401  (needed for LoRA loading)
except Exception:
    pip("-U", "diffusers", "transformers", "accelerate", "peft")
    from diffusers import ZImagePipeline
import diffusers
import torch

log["diffusers"] = diffusers.__version__

# --- bf16 attention on a T4: compute in fp16 (memory-efficient kernel), fp32 fallback on overflow.
_sdpa = torch.nn.functional.scaled_dot_product_attention
_stats = {"fp16_calls": 0, "fp32_fallbacks": 0}


def _attention_t4(query, key, value, attn_mask=None, dropout_p=0.0, is_causal=False, scale=None,
                  enable_gqa=False):
    if query.dtype != torch.bfloat16 or not query.is_cuda:
        return _sdpa(query, key, value, attn_mask=attn_mask, dropout_p=dropout_p, is_causal=is_causal,
                     scale=scale, enable_gqa=enable_gqa)
    _stats["fp16_calls"] += 1
    with torch.nn.attention.sdpa_kernel([torch.nn.attention.SDPBackend.EFFICIENT_ATTENTION,
                                         torch.nn.attention.SDPBackend.MATH]):
        out = _sdpa(query.half(), key.half(), value.half(), attn_mask=attn_mask, dropout_p=dropout_p,
                    is_causal=is_causal, scale=scale, enable_gqa=enable_gqa)
    if torch.isfinite(out).all():
        return out.to(torch.bfloat16)
    _stats["fp32_fallbacks"] += 1
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

# --- LoRA versions, ordered by training step (the final file, with no step number, goes last).
def step_of(path):
    m = re.search(r"_(\d{9})\.safetensors$", path)
    return int(m.group(1)) if m else 10 ** 9


loras = sorted(glob.glob(f"/kaggle/input/**/{P['lora_glob']}", recursive=True), key=step_of)
if not loras:
    log["error"] = "no LoRA files matched " + P["lora_glob"]
    log["kaggle_input_listing"] = sorted(glob.glob("/kaggle/input/**", recursive=True))[:200]
    stamp("no LoRA files found; stopping")
    sys.exit(1)
versions = [("base", None)] if P.get("include_base") else []
versions += [(("final" if step_of(p) == 10 ** 9 else f"step{step_of(p)}"), p) for p in loras]
log["versions"] = [v for v, _ in versions]
stamp(f"found {len(loras)} LoRA files")

pipe = ZImagePipeline.from_pretrained("Tongyi-MAI/Z-Image-Turbo", torch_dtype=torch.bfloat16,
                                      low_cpu_mem_usage=False)
stamp("model loaded to RAM")

# 1) All prompts -> embeddings on GPU 1, then free the text encoder.
text_dev = "cuda:1" if torch.cuda.device_count() > 1 else "cuda:0"
pipe.text_encoder.to(text_dev)
embeds = []
with torch.no_grad():
    for prompt in P["prompts"]:
        e, _ = pipe.encode_prompt(prompt, device=text_dev, do_classifier_free_guidance=False,
                                  max_sequence_length=1024)
        embeds.append([x.to("cuda:0", torch.bfloat16) for x in e])
pipe.text_encoder.to("cpu")
pipe.text_encoder = None
gc.collect()
torch.cuda.empty_cache()
stamp(f"{len(embeds)} prompts encoded")

# 2) Denoise every (version, prompt) with the same seed.
pipe.transformer.to("cuda:0")
width, height = int(P.get("width", 768)), int(P.get("height", 1024))
steps, seed = int(P.get("steps", 9)), int(P.get("seed", 42))
latents = []
log["version_errors"] = {}
for name, path in versions:
    if path:
        try:
            pipe.load_lora_weights(path, adapter_name=name)
            pipe.set_adapters([name], adapter_weights=[float(P.get("lora_scale", 1.0))])
        except Exception as e:  # one bad file shouldn't lose the other versions
            log["version_errors"][name] = f"{type(e).__name__}: {e}"[:500]
            stamp(f"{name}: could not load LoRA, skipped")
            continue
    for i, emb in enumerate(embeds):
        with torch.no_grad():
            lat = pipe(prompt_embeds=emb, height=height, width=width, num_inference_steps=steps,
                       guidance_scale=0.0, output_type="latent",
                       generator=torch.Generator("cuda:0").manual_seed(seed)).images
        latents.append((name, i, lat.float().cpu(), bool(torch.isnan(lat).any())))
        stamp(f"{name} prompt {i + 1} denoised")
    if path:
        pipe.delete_adapters(name)
log["attention"] = dict(_stats)

# 3) Decode on GPU 0 in fp32 once the image model is off it.
pipe.transformer.to("cpu")
gc.collect()
torch.cuda.empty_cache()
vae = pipe.vae.to("cuda:0", torch.float32)
for name, i, lat, bad in latents:
    with torch.no_grad():
        img = vae.decode((lat.to("cuda:0") / vae.config.scaling_factor) + vae.config.shift_factor,
                         return_dict=False)[0]
    image = pipe.image_processor.postprocess(img, output_type="pil")[0]
    fname = f"{name}_p{i + 1}.jpg"
    image.save(os.path.join(OUT, fname), quality=92)
    log["images"].append({"file": fname, "version": name, "prompt": i + 1, "nan": bad})
stamp("all images saved")
