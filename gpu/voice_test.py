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
rc, tail = sh("pip install -q chatterbox-tts 'kokoro>=0.9.4' soundfile librosa misaki[en]", 1500); REP["steps"]["pip"] = {"rc": rc, "s": round(time.time() - t), "tail": tail[-600:]}; save()
import numpy as np, soundfile as sf, librosa, torch
def pitch_st(w, sr):
    f0, _, _ = librosa.pyin(w, fmin=60, fmax=300, sr=sr); f0 = f0[~np.isnan(f0)]
    return float(12 * np.log2(np.median(f0) / 110.0)) if len(f0) > 10 else None
def finish(name, pieces, sr, secs, note=""):
    gap = np.zeros(int(.28 * sr), np.float32); out = np.concatenate([np.concatenate([p, gap]) for p in pieces])
    sf.write(f"{OUT}/{name}.wav", out, sr)
    st = [pitch_st(p, sr) for p in pieces]; st = [x for x in st if x is not None]
    rec = {"name": name, "note": note, "secs": round(secs, 1), "audio_s": round(len(out) / sr, 1), "rtf": round(secs / (len(out) / sr), 2),
           "pitch_st_median": round(float(np.median(st)), 2) if st else None, "pitch_spread_st": round(float(np.percentile(st, 90) - np.percentile(st, 10)), 2) if st else None}
    REP["variants"].append(rec); save(); print(rec, flush=True)
# reference pitch, for comparison
rw, rsr = librosa.load(REF, sr=24000); REP["ref_pitch_st"] = round(pitch_st(rw, rsr), 2); save()
# ---- C: Chatterbox clone of our Sadaltager ----
try:
    from chatterbox.tts import ChatterboxTTS
    t = time.time(); cb = ChatterboxTTS.from_pretrained(device="cuda"); REP["steps"]["chatterbox_load_s"] = round(time.time() - t); save()
    for name, ex, cfg in (("C1_clone_balanced", .5, .5), ("C2_clone_expressive", .65, .35), ("C3_clone_steady", .35, .6)):
        t = time.time(); pcs = []
        for s in SENTS:
            torch.manual_seed(7)
            w = cb.generate(s, audio_prompt_path=REF, exaggeration=ex, cfg_weight=cfg)
            pcs.append(w.squeeze(0).cpu().numpy().astype(np.float32))
        finish(name, pcs, cb.sr, time.time() - t, f"exaggeration {ex}, cfg {cfg}")
    del cb; torch.cuda.empty_cache()
except Exception:
    REP["variants"].append({"name": "chatterbox", "error": traceback.format_exc()[-1500:]}); save()
# ---- B: Kokoro licensed preset narrators ----
try:
    from kokoro import KPipeline
    pipes = {"a": KPipeline(lang_code="a"), "b": KPipeline(lang_code="b")}
    for voice in P.get("kokoro_voices", ["am_onyx", "am_michael", "bm_george", "bm_lewis"]):
        t = time.time(); pcs = []
        for s in SENTS:
            aud = [a for _, _, a in pipes[voice[0]](s, voice=voice, speed=P.get("kokoro_speed", 0.95))]
            pcs.append(np.concatenate([np.asarray(a, dtype=np.float32) for a in aud]))
        finish("B_kokoro_" + voice, pcs, 24000, time.time() - t, "Kokoro-82M preset")
except Exception:
    REP["variants"].append({"name": "kokoro", "error": traceback.format_exc()[-1500:]}); save()
REP["total_s"] = round(time.time() - T0); save()
