"""Collect public video listings (title, views, duration, subscriber count, thumbnail) for yt-viral / thumbnail studies.
Public pages only, no login.

Usage: python3 tools/yt_collect.py jobs/viral/<id>.json
Job: {"id": "...", "tab": "shorts", "per_channel": 60, "channels": ["@Glore3", "channel/UC..."], "thumbs": false}
Writes outputs/viral/<id>/collected.json (yt-viral swipe.py format + extra fields), report.json,
and with "thumbs": true, outputs/viral/<id>/thumbs/<video id>.jpg (270 px wide).
"""
import io, json, os, subprocess, sys, urllib.request

job = json.load(open(sys.argv[1]))
out = os.path.join("outputs", "viral", job["id"]); os.makedirs(out, exist_ok=True)
TH = job.get("thumbs"); tdir = os.path.join(out, "thumbs")
if TH:
    os.makedirs(tdir, exist_ok=True)
    from PIL import Image
rows, report = [], []

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r: return r.read()

for ch in job["channels"]:
    url = f"https://www.youtube.com/{ch}/{job.get('tab', 'shorts')}"
    r = subprocess.run(["yt-dlp", "--flat-playlist", "-J", "--playlist-end", str(job.get("per_channel", 60)), url],
                       capture_output=True, text=True, timeout=600)
    if r.returncode:
        report.append({"channel": ch, "ok": False, "error": r.stderr[-400:]}); continue
    d = json.loads(r.stdout); n = 0; nt = 0
    subs = d.get("channel_follower_count")
    name = d.get("channel") or d.get("uploader") or ch
    for e in d.get("entries") or []:
        if e.get("view_count") is None: continue
        vid = e.get("id")
        row = {"channel": name, "handle": ch, "subs": subs, "id": vid, "title": e.get("title"), "views": e["view_count"],
               "url": e.get("url") or f"https://www.youtube.com/shorts/{vid}", "duration": e.get("duration")}
        if TH and vid:
            for kind in ("oar2.jpg", "hq2.jpg", "hqdefault.jpg"):
                try:
                    im = Image.open(io.BytesIO(get(f"https://i.ytimg.com/vi/{vid}/{kind}"))).convert("RGB")
                    im.thumbnail((270, 480)); im.save(os.path.join(tdir, vid + ".jpg"), quality=82)
                    row["thumb"] = kind; nt += 1; break
                except Exception:  # noqa: BLE001
                    continue
        rows.append(row); n += 1
    report.append({"channel": ch, "name": name, "ok": True, "videos": n, "thumbs": nt, "subs": subs})
json.dump(rows, open(os.path.join(out, "collected.json"), "w"), indent=1)
json.dump(report, open(os.path.join(out, "report.json"), "w"), indent=1)
print(json.dumps(report))
