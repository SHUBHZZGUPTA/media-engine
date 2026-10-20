"""Gemini text-to-speech job runner (standard library only).

Usage: python3 tools/gemini_tts.py jobs/tts/<id>.json
Job format:
{
  "id": "skits-test",
  "models": ["gemini-3.1-flash-tts-preview", "gemini-2.5-flash-preview-tts"],
  "items": [
    {"name": "skit_a",
     "direction": "Free-text performance notes for the whole clip.",
     "speakers": {"Farmer": "Puck", "Pharaoh": "Algenib"},     # 1 speaker = single voice, 2 = dialogue
     "lines": [["Farmer", "[cheerful] Another flood?"], ["Pharaoh", "..."]]}
  ]
}
Writes outputs/tts/<id>/<name>.wav (24 kHz mono 16-bit) and outputs/tts/<id>/report.json.
The API key comes from the GEMINI_API_KEY environment variable and is never written or printed.
"""
import base64, json, os, sys, time, urllib.error, urllib.request, wave

API = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def call(model, body, key):
    req = urllib.request.Request(API.format(model=model), data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)


def build(item):
    sp = item["speakers"]
    script = "\n".join(f"{who}: {text}" for who, text in item["lines"])
    names = list(sp)
    prompt = (item.get("direction", "").strip() + "\n\n" if item.get("direction") else "")
    if len(names) == 1:
        prompt += "\n".join(text for _, text in item["lines"])
        speech = {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": sp[names[0]]}}}
    else:
        prompt += f"TTS the following conversation between {' and '.join(names)}:\n{script}"
        speech = {"multiSpeakerVoiceConfig": {"speakerVoiceConfigs": [
            {"speaker": n, "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": v}}} for n, v in sp.items()]}}
    return {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": speech}}


def main(job_path):
    key = os.environ.get("GEMINI_API_KEY", "")
    job = json.load(open(job_path))
    out = os.path.join("outputs", "tts", job["id"]); os.makedirs(out, exist_ok=True)
    report = {"job": job["id"], "items": []}
    for item in job["items"]:
        entry = {"name": item["name"], "ok": False}
        if not key:
            entry["error"] = "GEMINI_API_KEY secret is missing"; report["items"].append(entry); continue
        for model in job.get("models", ["gemini-3.1-flash-tts-preview"]):
            try:
                t0 = time.time(); res = call(model, build(item), key)
                part = res["candidates"][0]["content"]["parts"][0]["inlineData"]
                pcm = base64.b64decode(part["data"])
                path = os.path.join(out, item["name"] + ".wav")
                with wave.open(path, "wb") as w:
                    w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
                entry.update(ok=True, model=model, mime=part.get("mimeType"), seconds=round(len(pcm) / 48000, 2),
                             took=round(time.time() - t0, 1))
                break
            except urllib.error.HTTPError as e:
                msg = e.read().decode(errors="replace")[:600]
                entry.setdefault("attempts", []).append({"model": model, "status": e.code, "error": msg})
            except Exception as e:  # noqa: BLE001
                entry.setdefault("attempts", []).append({"model": model, "error": repr(e)[:300]})
        report["items"].append(entry); print(item["name"], "ok" if entry["ok"] else "FAILED", flush=True)
        time.sleep(2)
    json.dump(report, open(os.path.join(out, "report.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
