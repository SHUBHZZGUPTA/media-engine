"""Download public files (map imagery, data) on GitHub Actions and commit them under outputs/fetch/<id>/.
Usage: python3 tools/fetch_files.py jobs/fetch/<id>.json
Job: {"id": "...", "files": [{"name": "europe.jpg", "url": "https://..."}]}
"""
import json, os, sys, urllib.request
job = json.load(open(sys.argv[1])); out = os.path.join("outputs", "fetch", job["id"]); os.makedirs(out, exist_ok=True)
rep = []
for f in job["files"]:
    try:
        req = urllib.request.Request(f["url"], headers={"User-Agent": "media-engine/1.0"})
        with urllib.request.urlopen(req, timeout=120) as r: data = r.read()
        open(os.path.join(out, f["name"]), "wb").write(data); rep.append({"name": f["name"], "ok": True, "bytes": len(data)})
    except Exception as e:  # noqa: BLE001
        rep.append({"name": f["name"], "ok": False, "error": repr(e)[:300]})
json.dump(rep, open(os.path.join(out, "report.json"), "w"), indent=1); print(rep)
