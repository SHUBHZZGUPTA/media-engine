"""Runs on Kaggle. Reports the GPU, memory, disk and internet the session gets,
times a quick fp16 matrix multiply, and saves everything to gpu_check.json."""
import json
import os
import platform
import shutil
import subprocess
import time
import urllib.request

out = {"python": platform.python_version()}


def sh(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120).stdout.strip()
    except Exception as e:
        return f"error: {e}"


out["nvidia_smi"] = sh("nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader")
out["ram_gb"] = round(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 1e9, 1)
out["cpus"] = os.cpu_count()
for path in ("/kaggle/working", "/kaggle/tmp", "/tmp"):
    if os.path.exists(path):
        out[f"disk_free_gb {path}"] = round(shutil.disk_usage(path).free / 1e9, 1)

for name, url in (("huggingface", "https://huggingface.co"), ("github", "https://github.com")):
    try:
        out[f"internet {name}"] = urllib.request.urlopen(url, timeout=15).status
    except Exception as e:
        out[f"internet {name}"] = f"error: {type(e).__name__}"

try:
    import torch
    out["torch"] = torch.__version__
    out["cuda_available"] = torch.cuda.is_available()
    if torch.cuda.is_available():
        out["gpus"] = [
            {"name": torch.cuda.get_device_name(i),
             "vram_gb": round(torch.cuda.get_device_properties(i).total_memory / 1e9, 1),
             "compute_capability": ".".join(map(str, torch.cuda.get_device_capability(i)))}
            for i in range(torch.cuda.device_count())
        ]
        out["bf16_supported"] = torch.cuda.is_bf16_supported()
        a = torch.randn(4096, 4096, device="cuda", dtype=torch.float16)
        b = torch.randn(4096, 4096, device="cuda", dtype=torch.float16)
        for _ in range(3):
            a @ b
        torch.cuda.synchronize()
        n, t = 50, time.time()
        for _ in range(n):
            a @ b
        torch.cuda.synchronize()
        out["fp16_tflops_gpu0"] = round(2 * 4096 ** 3 * n / (time.time() - t) / 1e12, 1)
except Exception as e:
    out["torch_error"] = repr(e)

print(json.dumps(out, indent=1))
os.makedirs("/kaggle/working", exist_ok=True)
with open("/kaggle/working/gpu_check.json", "w") as f:
    json.dump(out, f, indent=1)
