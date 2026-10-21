"""Runs on Kaggle (2x T4). Generates photos with Z-Image-Turbo from the job's prompt and seeds,
and saves them with the prompt and timings to /kaggle/working.

T4 layout: GPU 1 encodes the prompt, GPU 0 runs the image model, and the VAE decodes in fp32 on
GPU 0 once the image model is moved off it. The model stays in bf16 (in fp16 it overflows and
gives black images), but a T4 can only run memory-efficient attention in fp16, and bf16 attention
there runs out of memory. So attention alone is computed in fp16, with a chunked fp32 fallback
for any call whose fp16 result overflows.

Job params: prompt (str), seeds (list of int), width, height (multiples of 16), steps."""
import gc
import json
import os
import subprocess
import sys
import time

os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
os.environ.setdefault("HF_HOME", "/tmp/hf")  # large scratch disk, not the 20 GB output disk

P = json.loads(globals().get("JOB_PARAMS", "{}"))
OUT = "/kaggle/working"
os.makedirs(OUT, exist_ok=True)
log = {"params": P, "timings": {}, "images": {}}
t0 = time.time()


def stamp(name):
    log["timings"][name] = round(time.time() - t0, 1)
    print(f"[{log['timings'][name]:>7}s] {name}", flush=True)


def save_log():
    with open(os.path.join(OUT, "run_log.json"), "w") as f:
        json.dump(log, f, indent=1)


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
import numpy as np
import torch

_sdpa = torch.nn.functional.scaled_dot_product_attention
_stats = {"fp16_calls": 0, "fp32_fallbacks": 0}


def _attention_t4(query, key, value, attn_mask=None, dropout_p=0.0, is_causal=False, scale=None,
                  enable_gqa=False):
    """bf16 attention on a T4: compute in fp16 with the memory-efficient kernel; if that
    overflows, recompute in fp32, 1024 queries at a time."""
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
log["diffusers"] = diffusers.__version__
log["gpus"] = [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]
text_dev = "cuda:1" if torch.cuda.device_count() > 1 else "cuda:0"
stamp("imports ready")

with open(os.path.join(OUT, "prompt.txt"), "w") as f:
    f.write(P["prompt"] + "\n")

pipe = ZImagePipeline.from_pretrained("Tongyi-MAI/Z-Image-Turbo", torch_dtype=torch.bfloat16,
                                      low_cpu_mem_usage=False)
stamp("model loaded to RAM")

# 1) Prompt -> embeddings on the second GPU.
templated = pipe.tokenizer.apply_chat_template([{"role": "user", "content": P["prompt"]}], tokenize=False,
                                               add_generation_prompt=True, enable_thinking=True)
log["prompt_tokens"] = len(pipe.tokenizer(templated).input_ids)
pipe.text_encoder.to(text_dev)
with torch.no_grad():
    embeds, _ = pipe.encode_prompt(P["prompt"], device=text_dev, do_classifier_free_guidance=False,
                                   max_sequence_length=1024)
embeds = [e.to("cuda:0", torch.bfloat16) for e in embeds]
pipe.text_encoder.to("cpu")
pipe.text_encoder = None
gc.collect()
torch.cuda.empty_cache()
stamp(f"prompt encoded ({log['prompt_tokens']} tokens)")

# 2) Image model in bf16 on GPU 0; attention goes through _attention_t4 above.
pipe.transformer.to("cuda:0")
stamp("image model on GPU 0")

width, height = int(P.get("width", 1152)), int(P.get("height", 1536))
steps = int(P.get("steps", 9))
latents = {}
for seed in P.get("seeds", [1]):
    with torch.no_grad():
        lat = pipe(prompt_embeds=embeds, height=height, width=width, num_inference_steps=steps,
                   guidance_scale=0.0, output_type="latent",
                   generator=torch.Generator("cuda:0").manual_seed(int(seed))).images
    bad = bool(torch.isnan(lat).any() or torch.isinf(lat).any())
    log["images"][str(seed)] = {"latent_nan_or_inf": bad}
    latents[seed] = lat.float().cpu()
    stamp(f"seed {seed} denoised{' (NaN/inf in result)' if bad else ''}")
log["peak_vram_gb_gpu0_denoise"] = round(torch.cuda.max_memory_allocated(0) / 1e9, 1)
log["attention"] = dict(_stats)
save_log()

# 3) Decode on GPU 0 in fp32 once the image model is off it.
pipe.transformer.to("cpu")
gc.collect()
torch.cuda.empty_cache()
vae = pipe.vae.to("cuda:0", torch.float32)
files = []
for seed, lat in latents.items():
    x = (lat.to("cuda:0") / vae.config.scaling_factor) + vae.config.shift_factor
    try:
        with torch.no_grad():
            img = vae.decode(x, return_dict=False)[0]
    except torch.OutOfMemoryError:
        torch.cuda.empty_cache()
        vae.enable_tiling()
        with torch.no_grad():
            img = vae.decode(x, return_dict=False)[0]
    image = pipe.image_processor.postprocess(img, output_type="pil")[0]
    arr = np.asarray(image)
    log["images"][str(seed)].update(mean_brightness=round(float(arr.mean()), 1),
                                    pixel_std=round(float(arr.std()), 1))
    name = f"photo_seed{seed}.png"
    image.save(os.path.join(OUT, name))
    files.append(name)
    stamp(f"saved {name}")

log["files"] = files
save_log()
print(json.dumps(log, indent=1))
