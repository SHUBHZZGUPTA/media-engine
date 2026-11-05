"""Gemini video-watching job runner (standard library only).

Gemini receives a public YouTube URL directly (picture + sound), so nothing is downloaded.

Usage: python3 tools/gemini_watch.py jobs/watch/<id>.json
Job format:
{
  "id": "ziro-iran",
  "url": "https://www.youtube.com/watch?v=FZ7EKujN-pY",
  "models": ["gemini-2.5-pro", "gemini-2.5-flash"],      # tried in order (404/429/5xx -> next)
  "media_resolution": "MEDIA_RESOLUTION_LOW",             # optional, keeps long videos inside token limits
  "items": [
    {"name": "voice", "start": "0s", "end": "240s", "fps": 1, "prompt": "..."}
  ]
}
"start"/"end"/"fps" are optional (whole video otherwise).
Writes outputs/watch/<id>/<name>.md and outputs/watch/<id>/report.json.
The API key comes from GEMINI_API_KEY and is never written or printed.
"""
import json, os, sys, time, urllib.error, urllib.request

API = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def call(model, body, key):
    req = urllib.request.Request(API.format(model=model), data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.load(r)


def run_item(job, item, key):
    part = {"file_data": {"file_uri": job["url"]}}
    meta = {}
    if item.get("start"): meta["start_offset"] = item["start"]
    if item.get("end"): meta["end_offset"] = item["end"]
    if item.get("fps"): meta["fps"] = item["fps"]
    if meta: part["video_metadata"] = meta
    body = {"contents": [{"parts": [part, {"text": item["prompt"]}]}]}
    if job.get("media_resolution"):
        body["generationConfig"] = {"mediaResolution": job["media_resolution"]}
    errors = []
    for model in job.get("models", ["gemini-2.5-flash"]):
        for attempt in range(3):
            try:
                r = call(model, body, key)
                text = "".join(p.get("text", "") for c in r.get("candidates", [])
                               for p in c.get("content", {}).get("parts", []))
                return {"ok": bool(text), "model": model, "text": text,
                        "usage": r.get("usageMetadata", {}), "errors": errors}
            except urllib.error.HTTPError as e:
                msg = e.read().decode(errors="replace")[:600]
                errors.append(f"{model} HTTP {e.code}: {msg}")
                # Free tier counts failed calls too, so retry sparingly: one slow retry on overload/per-minute limits,
                # and stop the whole job on a daily-quota 429 (it won't clear for hours).
                if e.code == 429 and "per day" in msg:
                    raise SystemExit(f"daily quota exhausted on {model}; stopping job")
                if e.code in (429, 500, 503) and attempt < 1:
                    time.sleep(120); continue
                break
            except Exception as e:  # timeouts etc.
                errors.append(f"{model} {type(e).__name__}: {e}")
                break
    return {"ok": False, "model": None, "text": "", "usage": {}, "errors": errors}


def list_models(key, out):
    """Free metadata call (uses no generation quota): which models this key can call."""
    url = "https://generativelanguage.googleapis.com/v1beta/models?pageSize=1000"
    req = urllib.request.Request(url, headers={"x-goog-api-key": key})
    with urllib.request.urlopen(req, timeout=60) as r:
        models = json.load(r).get("models", [])
    rows = [f'{m["name"]} | {",".join(m.get("supportedGenerationMethods", []))} | in {m.get("inputTokenLimit")}'
            for m in models]
    open(os.path.join(out, "models.txt"), "w").write("\n".join(rows) + "\n")
    print(len(rows), "models listed")


def main(path):
    job = json.load(open(path))
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY missing")
    out = os.path.join("outputs", "watch", job["id"])
    os.makedirs(out, exist_ok=True)
    if job.get("list_models_only"):
        return list_models(key, out)
    report = {"id": job["id"], "url": job["url"], "items": {}}
    for item in job["items"]:
        res = run_item(job, item, key)
        with open(os.path.join(out, item["name"] + ".md"), "w") as f:
            f.write(res["text"] or "(no answer)\n\n" + "\n".join(res["errors"]))
        report["items"][item["name"]] = {k: res[k] for k in ("ok", "model", "usage", "errors")}
        print(item["name"], "ok" if res["ok"] else "FAILED", res["model"])
        for e in res["errors"]: print("  ", e[:400])
        time.sleep(20)  # stay under per-minute limits
    json.dump(report, open(os.path.join(out, "report.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
