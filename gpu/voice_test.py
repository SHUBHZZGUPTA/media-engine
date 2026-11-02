"""Runs on Kaggle. Narrator-voice test for BHUGOL long-form (free, consistent voices):
  C  = Chatterbox (Resemble AI, MIT licence) zero-shot clone of OUR OWN Gemini Sadaltager narration (ref_sadaltager.wav)
  B  = Kokoro-82M (Apache-2.0) licensed preset male narrators
Every variant reads the same chapter-5 text (ch5.txt), sentence by sentence, joined with short pauses.
Writes <variant>.wav + voice.json (time, real-time factor, pitch per sentence -> consistency = spread in semitones)."""
import glob, json, os, re, subprocess, time, traceback
P = json.loads(JOB_PARAMS)  # noqa: F821
OUT = "/kaggle/working"; REP = {"params": P, "steps": {}, "variants": []}; T0 = time.time()
def save(): json.dump(REP, open(f"{OUT}/voice.json", "w"), indent=1)
def sh(c, t=1800):
    r = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t); return r.returncode, (r.stdout + r.stderr)[-1500:]
inp = {os.path.basename(p): p for p in glob.glob("/kaggle/input/**/*", recursive=True) if os.path.isfile(p)}
REP["inputs"] = list(inp); save()
TEXT = open(inp["ch5.txt"]).read(); REF = inp["ref_sadaltager.wav"]
SENTS = [s.strip() for s in re.split(r"(?<=[.!?])\s+", TEXT.replace("\n", " ")) if s.strip()]
REP["sentences"] = len(SENTS); save()
t = time.time(); REP["steps"]["apt"] = sh("apt-get install -y -qq espeak-ng > /dev/null 2>&1; echo ok")[0]
REP["steps"]["uv"] = sh("pip install -q uv && uv python install 3.12", 600)[0]; save()
DEPS = {"C": "chatterbox-tts soundfile librosa", "B": "'kokoro>=0.9.4' 'misaki[en]' soundfile librosa"}
env = dict(os.environ, JOB_PARAMS=JOB_PARAMS, CH5=inp["ch5.txt"], REF=REF)  # noqa: F821
for eng in ("C", "B"):
    t = time.time(); rc, tail = sh(f"uv venv -q -p 3.12 /tmp/v{eng} && uv pip install -q --python /tmp/v{eng}/bin/python {DEPS[eng]} && /tmp/v{eng}/bin/python -c \"import numpy, torch, librosa; print(torch.__version__, torch.cuda.is_available())\"", 1500)
    REP["steps"][f"pip_{eng}"] = {"rc": rc, "s": round(time.time() - t), "tail": tail[-500:]}; save()
    t = time.time(); r = subprocess.run([f"/tmp/v{eng}/bin/python", inp["voice_worker.py"], eng], env=env, capture_output=True, text=True, timeout=3600)
    REP["steps"][f"run_{eng}"] = {"rc": r.returncode, "s": round(time.time() - t), "tail": (r.stdout + r.stderr)[-1200:]}
    try: REP["variants"] += json.load(open(f"{OUT}/variants_{eng}.json"))
    except Exception as e: REP["variants"].append({"engine": eng, "error": str(e)})
    save()
REP["total_s"] = round(time.time() - T0); save()
