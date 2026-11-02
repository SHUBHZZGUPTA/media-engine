"""Worker for gpu/voice_test.py, run inside a Python 3.12 venv. argv[1] = C (Chatterbox) or B (Kokoro)."""
import json, os, re, sys, time, traceback
import numpy as np, soundfile as sf, librosa, torch
ENG = sys.argv[1]; OUT = "/kaggle/working"; P = json.loads(os.environ["JOB_PARAMS"])
TEXT = open(os.environ["CH5"]).read(); REF = os.environ["REF"]
SENTS = [s.strip() for s in re.split(r"(?<=[.!?])\s+", TEXT.replace("\n", " ")) if s.strip()]
RES = []
def save(): json.dump(RES, open(f"{OUT}/variants_{ENG}.json", "w"), indent=1)
def pitch_st(w, sr):
    f0, _, _ = librosa.pyin(w, fmin=60, fmax=300, sr=sr); f0 = f0[~np.isnan(f0)]
    return float(12 * np.log2(np.median(f0) / 110.0)) if len(f0) > 10 else None
def finish(name, pieces, sr, secs, note=""):
    gap = np.zeros(int(.28 * sr), np.float32); out = np.concatenate([np.concatenate([p, gap]) for p in pieces])
    sf.write(f"{OUT}/{name}.wav", out, sr)
    st = [pitch_st(p, sr) for p in pieces]; st = [x for x in st if x is not None]
    rec = {"name": name, "note": note, "secs": round(secs, 1), "audio_s": round(len(out) / sr, 1), "rtf": round(secs / (len(out) / sr), 2),
           "pitch_st_median": round(float(np.median(st)), 2) if st else None, "pitch_spread_st": round(float(np.percentile(st, 90) - np.percentile(st, 10)), 2) if st else None}
    RES.append(rec); save(); print(rec, flush=True)
# reference pitch, for comparison
rw, rsr = librosa.load(REF, sr=24000); RES.append({'ref_pitch_st': round(pitch_st(rw, rsr), 2)}); save()
# ---- C: Chatterbox clone of our Sadaltager ----
if ENG == 'C':
 try:
     from chatterbox.tts import ChatterboxTTS
     t = time.time(); cb = ChatterboxTTS.from_pretrained(device="cuda"); RES.append({"chatterbox_load_s": round(time.time() - t)}); save()
     for name, ex, cfg in (("C1_clone_balanced", .5, .5), ("C2_clone_expressive", .65, .35), ("C3_clone_steady", .35, .6)):
         t = time.time(); pcs = []
         for s in SENTS:
             torch.manual_seed(7)
             w = cb.generate(s, audio_prompt_path=REF, exaggeration=ex, cfg_weight=cfg)
             pcs.append(w.squeeze(0).cpu().numpy().astype(np.float32))
         finish(name, pcs, cb.sr, time.time() - t, f"exaggeration {ex}, cfg {cfg}")
     del cb; torch.cuda.empty_cache()
 except Exception:
     RES.append({"name": "chatterbox", "error": traceback.format_exc()[-1500:]}); save()
# ---- B: Kokoro licensed preset narrators ----
if ENG == 'B':
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
     RES.append({"name": "kokoro", "error": traceback.format_exc()[-1500:]}); save()
