"""Runs on Kaggle. Word-accuracy QC for the narrator voice test: Whisper large-v3 transcribes each wav,
compares to ch5.txt (word error rate + the words that differ), flags dropped/added/garbled words."""
import difflib, glob, json, os, re, subprocess
import librosa, torch
from transformers import pipeline  # transformers Whisper on the image's own torch (faster-whisper needs CUDA 12 libs Kaggle no longer has)
inp = {os.path.basename(p): p for p in glob.glob("/kaggle/input/**/*", recursive=True) if os.path.isfile(p)}
norm = lambda s: re.sub(r"[^a-z0-9' ]", " ", s.lower().replace("-", " ")).split()
REF = norm(open(inp["ch5.txt"]).read()); m = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3-turbo", torch_dtype=torch.float16, device="cuda:0"); R = {}
for f in sorted(k for k in inp if k.endswith(".wav")):
    txt = m(librosa.load(inp[f], sr=16000)[0], chunk_length_s=30, batch_size=8, generate_kwargs={"language": "en"})["text"]; hyp = norm(txt)
    sm = difflib.SequenceMatcher(a=REF, b=hyp, autojunk=False); errs = []; n = 0
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        if op != "equal": n += max(a1 - a0, b1 - b0); errs.append(f"{op}: '{' '.join(REF[a0:a1])}' -> '{' '.join(hyp[b0:b1])}'")
    R[f] = {"wer": round(n / len(REF), 3), "diffs": errs}; print(f, R[f]["wer"], flush=True)
    json.dump(R, open("/kaggle/working/qc.json", "w"), indent=1)
