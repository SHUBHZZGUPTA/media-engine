"""Runs on Kaggle. Word-accuracy QC for the narrator voice test: Whisper large-v3 transcribes each wav,
compares to ch5.txt (word error rate + the words that differ), flags dropped/added/garbled words."""
import difflib, glob, json, os, re, subprocess
subprocess.run("pip install -q faster-whisper", shell=True)
from faster_whisper import WhisperModel
inp = {os.path.basename(p): p for p in glob.glob("/kaggle/input/**/*", recursive=True) if os.path.isfile(p)}
norm = lambda s: re.sub(r"[^a-z0-9' ]", " ", s.lower().replace("-", " ")).split()
REF = norm(open(inp["ch5.txt"]).read()); m = WhisperModel("large-v3", device="cuda", compute_type="float16"); R = {}
for f in sorted(k for k in inp if k.endswith(".wav")):
    segs, _ = m.transcribe(inp[f], language="en", beam_size=5); hyp = norm(" ".join(s.text for s in segs))
    sm = difflib.SequenceMatcher(a=REF, b=hyp, autojunk=False); errs = []; n = 0
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        if op != "equal": n += max(a1 - a0, b1 - b0); errs.append(f"{op}: '{' '.join(REF[a0:a1])}' -> '{' '.join(hyp[b0:b1])}'")
    R[f] = {"wer": round(n / len(REF), 3), "diffs": errs}; print(f, R[f]["wer"], flush=True)
    json.dump(R, open("/kaggle/working/qc.json", "w"), indent=1)
