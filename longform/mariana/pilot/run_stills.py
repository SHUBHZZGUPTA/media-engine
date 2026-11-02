#!/usr/bin/env python3
"""Render every living still not done yet (out_full/stills.json), 2 at a time; prints progress."""
import json, os, subprocess, time
from concurrent.futures import ThreadPoolExecutor
os.chdir("/home/claude/pilot"); st = json.load(open("out_full/stills.json")); t0 = time.time()
todo = [(n, v) for n, v in st.items() if not os.path.exists(f"shots/{n}.mp4")]
def job(nv):
    n, v = nv; r = subprocess.run(["plate/render_plate.sh", n, v["src"], json.dumps(v["cfg"])], capture_output=True, text=True)
    ok = r.returncode == 0 and os.path.exists(f"shots/{n}.mp4"); print(n, "ok" if ok else "FAIL " + r.stderr[-200:], round(time.time() - t0), flush=True); return ok
with ThreadPoolExecutor(2) as ex: res = list(ex.map(job, todo))
print(f"STILLS DONE {sum(res)}/{len(res)} in {round(time.time() - t0)}s", flush=True)
