"""Collect public video listings (title, views, duration) for yt-viral. Public pages only, no login.

Usage: python3 tools/yt_collect.py jobs/viral/<id>.json
Job: {"id": "...", "tab": "shorts", "per_channel": 60, "channels": ["@Glore3", ...]}
Writes outputs/viral/<id>/collected.json (yt-viral swipe.py format) and report.json.
"""
import json, os, subprocess, sys

job = json.load(open(sys.argv[1]))
out = os.path.join("outputs", "viral", job["id"]); os.makedirs(out, exist_ok=True)
rows, report = [], []
for ch in job["channels"]:
    url = f"https://www.youtube.com/{ch}/{job.get('tab', 'shorts')}"
    r = subprocess.run(["yt-dlp", "--flat-playlist", "-J", "--playlist-end", str(job.get("per_channel", 60)), url],
                       capture_output=True, text=True, timeout=300)
    if r.returncode:
        report.append({"channel": ch, "ok": False, "error": r.stderr[-400:]}); continue
    d = json.loads(r.stdout); n = 0
    for e in d.get("entries") or []:
        if e.get("view_count") is None: continue
        rows.append({"channel": d.get("channel") or d.get("uploader") or ch, "title": e.get("title"),
                     "views": e["view_count"], "url": e.get("url") or f"https://www.youtube.com/shorts/{e.get('id')}",
                     "duration": e.get("duration")}); n += 1
    report.append({"channel": ch, "ok": True, "videos": n})
json.dump(rows, open(os.path.join(out, "collected.json"), "w"), indent=1)
json.dump(report, open(os.path.join(out, "report.json"), "w"), indent=1)
print(json.dumps(report))
