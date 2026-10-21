"""Runs on Kaggle (2x T4). Generates photos with Z-Image-Turbo from the job's prompt and seeds,
and saves them with the prompt and timings to /kaggle/working.

T4 layout: GPU 1 encodes the prompt (bf16 text encoder), GPU 0 runs the image model in fp16 so
PyTorch's memory-efficient attention can be used (bf16 attention on a T4 runs out of memory),
then the VAE decodes in fp32 on GPU 0 after the image model is moved off it.

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
embeds = [e.to("cuda:0", torch.float16) for e in embeds]
pipe.text_encoder.to("cpu")
pipe.text_encoder = None
gc.collect()
torch.cuda.empty_cache()
stamp(f"prompt encoded ({log['prompt_tokens']} tokens)")

# 2) Image model in fp16 on GPU 0 with memory-efficient attention.
pipe.transformer.to(torch.float16).to("cuda:0")
pipe.transformer.set_attention_backend("_native_efficient")
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
