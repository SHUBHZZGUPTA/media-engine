"""Runs on Kaggle. D1 sample: free open-source image-to-video on the T4 (no paid credits).
Animates each input picture with two open models, one after the other, and records time + peak memory:
  LTX-Video 2B (Lightricks, fast) and Wan 2.2 TI2V-5B (Alibaba, higher quality, slower).
Pictures arrive as a private dataset (bench/i2v/*.jpg); prompts come in params["shots"]. Writes <model>_<shot>.mp4 + i2v.json.
"""
import glob, json, os, subprocess, sys, time, traceback
P = json.loads(JOB_PARAMS)  # noqa: F821
OUT = "/kaggle/working"; REP = {"params": P, "runs": []}
def save(): json.dump(REP, open(f"{OUT}/i2v.json", "w"), indent=1)
REP["gpu"] = subprocess.run("nvidia-smi --query-gpu=name,memory.total --format=csv,noheader", shell=True, capture_output=True, text=True).stdout.strip()
t = time.time(); r = subprocess.run("pip install -q -U diffusers transformers accelerate sentencepiece ftfy imageio imageio-ffmpeg", shell=True, capture_output=True, text=True)
REP["pip_s"] = round(time.time() - t, 1); REP["pip_tail"] = r.stderr[-600:]; save()
import torch
from PIL import Image
from diffusers.utils import export_to_video
imgs = {os.path.basename(p)[:-4]: p for p in glob.glob("/kaggle/input/**/*.jpg", recursive=True)}
REP["inputs"] = list(imgs); save()
NEG = ("worst quality, blurry, jittery, distorted, morphing, melting, flicker, text, watermark, logo, people, extra objects, "
       "camera shake, sudden cuts, low resolution, deformed vehicle, warped shapes")
def fit(img, w, h):
    s = max(w / img.width, h / img.height); im = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    l, t_ = (im.width - w) // 2, (im.height - h) // 2; return im.crop((l, t_, l + w, t_ + h))
def run(model, load, call, w, h, fps):
    t0 = time.time()
    try:
        pipe = load(); REP.setdefault("load_s", {})[model] = round(time.time() - t0, 1); save()
    except Exception:
        REP["runs"].append({"model": model, "error": traceback.format_exc()[-1500:]}); save(); return
    for shot in P["shots"]:
        if shot["img"] not in imgs: continue
        img = fit(Image.open(imgs[shot["img"]]).convert("RGB"), w, h)
        torch.cuda.reset_peak_memory_stats(); t1 = time.time()
        try:
            frames = call(pipe, img, shot["prompt"], w, h)
            out = f"{OUT}/{model}_{shot['img']}.mp4"; export_to_video(frames, out, fps=fps)
            REP["runs"].append({"model": model, "shot": shot["img"], "secs": round(time.time() - t1, 1), "frames": len(frames),
                                "size": [w, h], "peak_gb": round(torch.cuda.max_memory_allocated() / 1e9, 1)})
        except Exception:
            REP["runs"].append({"model": model, "shot": shot["img"], "error": traceback.format_exc()[-1500:]})
        save(); print(REP["runs"][-1], flush=True)
    del pipe; torch.cuda.empty_cache()
# 1. LTX-Video 2B
def ltx_load():
    from diffusers import LTXImageToVideoPipeline
    p = LTXImageToVideoPipeline.from_pretrained("Lightricks/LTX-Video", torch_dtype=torch.bfloat16); p.enable_model_cpu_offload(); return p
def ltx_call(p, img, prompt, w, h):
    return p(image=img, prompt=prompt, negative_prompt=NEG, width=w, height=h, num_frames=121, num_inference_steps=40,
             generator=torch.Generator("cpu").manual_seed(7)).frames[0]
if "ltx" in P.get("models", ["ltx", "wan"]): run("ltx", ltx_load, ltx_call, 768, 512, 24)
# 2. Wan 2.2 TI2V-5B
def wan_load():
    from diffusers import WanImageToVideoPipeline, AutoencoderKLWan
    mid = "Wan-AI/Wan2.2-TI2V-5B-Diffusers"
    vae = AutoencoderKLWan.from_pretrained(mid, subfolder="vae", torch_dtype=torch.float32)
    p = WanImageToVideoPipeline.from_pretrained(mid, vae=vae, torch_dtype=torch.bfloat16); p.enable_model_cpu_offload(); return p
def wan_call(p, img, prompt, w, h):
    return p(image=img, prompt=prompt, negative_prompt=NEG, width=w, height=h, num_frames=81, num_inference_steps=30, guidance_scale=5.0,
             generator=torch.Generator("cpu").manual_seed(7)).frames[0]
if "wan" in P.get("models", ["ltx", "wan"]): run("wan", wan_load, wan_call, 832, 480, 24)
REP["total_s"] = round(time.time() - t, 1); save()
