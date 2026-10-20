"""Word timings with faster-whisper (runs on GitHub Actions; model downloads there).

Usage: python3 tools/whisper_words.py jobs/align/<id>.json
Job: {"id": "...", "audio": "outputs/tts/<job>/<name>.wav", "lang": "en", "model": "small.en"}
Writes outputs/align/<id>/words.txt ("start end word" per line) and segments.json.
"""
import json, os, sys, wave
import numpy as np
from faster_whisper import WhisperModel

job = json.load(open(sys.argv[1]))
out = os.path.join("outputs", "align", job["id"]); os.makedirs(out, exist_ok=True)
m = WhisperModel(job.get("model", "small.en"), device="cpu", compute_type="int8")
with wave.open(job["audio"]) as w:  # decode ourselves: avoids a PyAV version clash in faster-whisper
    sr, ch = w.getframerate(), w.getnchannels()
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
a = a.reshape(-1, ch).mean(1)
if sr != 16000:
    a = np.interp(np.arange(0, len(a) / sr, 1 / 16000), np.arange(len(a)) / sr, a).astype(np.float32)
segs, info = m.transcribe(a, language=job.get("lang", "en"), word_timestamps=True, beam_size=5,
                          condition_on_previous_text=False, vad_filter=False)
rows, S = [], []
for s in segs:
    S.append({"start": s.start, "end": s.end, "text": s.text})
    for w in s.words or []:
        rows.append(f"{w.start:.3f} {w.end:.3f} {w.word.strip()}")
open(os.path.join(out, "words.txt"), "w").write("\n".join(rows) + "\n")
json.dump(S, open(os.path.join(out, "segments.json"), "w"), indent=1)
print(len(rows), "words")
