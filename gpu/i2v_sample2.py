"""Runs on Kaggle. D1 sample round 2 (free image-to-video on the T4 x2):
  1. LTX-Video 2B, re-prompted so the motion is camera-led (the T4 test showed LTX ignores object motion like "sinks").
  2. Wan 2.2 TI2V-5B with the transformer split across BOTH T4s (accelerate device_map), text encoder kept off the GPUs.
     Fallback if the split fails: one GPU with sequential CPU offload (slow but small).
Writes <tag>_<shot>.mp4 + i2v2.json (time, peak memory per GPU, mean brightness, motion score).
"""
import glob, json, os, subprocess, time, traceback
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
P = json.loads(JOB_PARAMS)  # noqa: F821
OUT = "/kaggle/working"; REP = {"params": P, "runs": []}; T0 = time.time()
def save(): json.dump(REP, open(f"{OUT}/i2v2.json", "w"), indent=1)
r = subprocess.run("pip install -q -U diffusers transformers accelerate sentencepiece ftfy imageio imageio-ffmpeg", shell=True, capture_output=True, text=True)
REP["pip_s"] = round(time.time() - T0, 1); save()
import numpy as np, torch
from PIL import Image
from diffusers.utils import export_to_video
imgs = {os.path.basename(p)[:-4]: p for p in glob.glob("/kaggle/input/**/*.jpg", recursive=True)}
NEG = ("worst quality, blurry, jittery, distorted, morphing, melting, flicker, text, watermark, logo, people, extra objects, "
       "camera shake, sudden cuts, low resolution, deformed vehicle, warped shapes, static image, frozen frame")
def fit(img, w, h):
    s = max(w / img.width, h / img.height); im = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    l, t_ = (im.width - w) // 2, (im.height - h) // 2; return im.crop((l, t_, l + w, t_ + h))
def peaks(): return [round(torch.cuda.max_memory_allocated(i) / 1e9, 1) for i in range(torch.cuda.device_count())]
def record(tag, shot, frames, secs, extra=None):
    out = f"{OUT}/{tag}_{shot}.mp4"; export_to_video(frames, out, fps=24)
    a = [np.asarray(f, dtype=np.float32) for f in frames]
    rec = {"tag": tag, "shot": shot, "secs": round(secs, 1), "frames": len(frames), "mean_px": round(float(a[len(a) // 2].mean()), 1),
           "motion": round(float(np.mean([np.abs(a[i] - a[i - 1]).mean() for i in range(1, len(a))])), 2), "peak_gb": peaks()}
    if extra: rec.update(extra)
    REP["runs"].append(rec); save(); print(rec, flush=True)
def fail(tag, shot, e): REP["runs"].append({"tag": tag, "shot": shot, "error": e[-1500:]}); save(); print(tag, shot, "FAILED", e[-300:], flush=True)
DT = torch.float16

# ---------- 1. LTX, camera-led prompts ----------
try:
    from diffusers import LTXImageToVideoPipeline
    t = time.time(); pipe = LTXImageToVideoPipeline.from_pretrained("Lightricks/LTX-Video", torch_dtype=DT)
    pipe.enable_model_cpu_offload()
    pipe.transformer.set_attention_backend("_native_efficient"); pipe.vae.enable_tiling()
    REP["ltx_load_s"] = round(time.time() - t, 1); save()
    for shot in P["ltx_shots"]:
        img = fit(Image.open(imgs[shot["img"]]).convert("RGB"), 768, 512)
        for i in range(torch.cuda.device_count()): torch.cuda.reset_peak_memory_stats(i)
        t = time.time()
        try:
            fr = pipe(image=img, prompt=shot["prompt"], negative_prompt=NEG, width=768, height=512, num_frames=97, num_inference_steps=40,
                      guidance_scale=shot.get("cfg", 3.0), generator=torch.Generator("cpu").manual_seed(shot.get("seed", 7))).frames[0]
            record("ltx2", shot["name"], fr, time.time() - t)
        except Exception: fail("ltx2", shot["name"], traceback.format_exc())
    del pipe; torch.cuda.empty_cache()
except Exception: fail("ltx2", "load", traceback.format_exc())

# ---------- 2. Wan 2.2 TI2V-5B ----------
MID = "Wan-AI/Wan2.2-TI2V-5B-Diffusers"
def wan_split():
    """Transformer layers split over cuda:0 and cuda:1; text encoder + VAE handled by the pipeline's offload hooks."""
    from diffusers import WanImageToVideoPipeline, AutoencoderKLWan, WanTransformer3DModel
    tr = WanTransformer3DModel.from_pretrained(MID, subfolder="transformer", torch_dtype=DT, device_map="auto",
                                               max_memory={0: "6GiB", 1: "6GiB", "cpu": "24GiB"})
    REP["wan_split_map"] = sorted(set(str(v) for v in getattr(tr, "hf_device_map", {}).values())); save()
    vae = AutoencoderKLWan.from_pretrained(MID, subfolder="vae", torch_dtype=torch.float32).to("cuda:1")
    p = WanImageToVideoPipeline.from_pretrained(MID, transformer=tr, vae=vae, torch_dtype=DT)
    p.text_encoder.to("cuda:1")
    try: p.transformer.set_attention_backend("_native_efficient")
    except Exception: pass
    p.vae.enable_tiling(); return p
def wan_seq():
    from diffusers import WanImageToVideoPipeline, AutoencoderKLWan
    vae = AutoencoderKLWan.from_pretrained(MID, subfolder="vae", torch_dtype=torch.float32)
    p = WanImageToVideoPipeline.from_pretrained(MID, vae=vae, torch_dtype=DT); p.enable_sequential_cpu_offload()
    try: p.transformer.set_attention_backend("_native_efficient")
    except Exception: pass
    p.vae.enable_tiling(); return p
for mode, load in (("split2gpu", wan_split), ("seqoffload", wan_seq)):
    if any(r.get("tag", "").startswith("wan") and "error" not in r for r in REP["runs"]): break
    if time.time() - T0 > P.get("budget_s", 7800) - 1500: REP["skipped_" + mode] = "time budget"; save(); break
    try:
        t = time.time(); pipe = load(); REP[f"wan_{mode}_load_s"] = round(time.time() - t, 1); save()
    except Exception: fail("wan_" + mode, "load", traceback.format_exc()); torch.cuda.empty_cache(); continue
    for shot in P["wan_shots"]:
        img = fit(Image.open(imgs[shot["img"]]).convert("RGB"), 832, 480)
        for i in range(torch.cuda.device_count()): torch.cuda.reset_peak_memory_stats(i)
        t = time.time()
        try:
            fr = pipe(image=img, prompt=shot["prompt"], negative_prompt=NEG, width=832, height=480, num_frames=49, num_inference_steps=30,
                      guidance_scale=5.0, generator=torch.Generator("cpu").manual_seed(7)).frames[0]
            record("wan_" + mode, shot["name"], fr, time.time() - t)
        except Exception: fail("wan_" + mode, shot["name"], traceback.format_exc())
    del pipe; torch.cuda.empty_cache()
REP["total_s"] = round(time.time() - T0, 1); save()
