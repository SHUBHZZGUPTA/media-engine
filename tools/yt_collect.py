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

# Optional search-demand study: "searches": ["query", ...]. For each query: YouTube autocomplete suggestions
# (what people type), the top results by relevance (views = demand) and the newest uploads (competition and
# whether fresh videos still get views). Public endpoints only. Writes outputs/viral/<id>/search.json.
if job.get("searches"):
    import urllib.parse
    def flat(q, n):
        r = subprocess.run(["yt-dlp", "--flat-playlist", "-J", q], capture_output=True, text=True, timeout=600)
        if r.returncode:
            return {"error": r.stderr[-300:]}
        es = json.loads(r.stdout).get("entries") or []
        return [{"title": e.get("title"), "views": e.get("view_count"), "channel": e.get("channel") or e.get("uploader"),
                 "duration": e.get("duration"), "id": e.get("id")} for e in es[:n]]
    study = []
    for q in job["searches"]:
        rec = {"query": q}
        try:
            raw = get("https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q=" + urllib.parse.quote(q))
            rec["suggest"] = json.loads(raw.decode("utf-8", "replace"))[1]
        except Exception as e:  # noqa: BLE001
            rec["suggest_error"] = type(e).__name__
        rec["top"] = flat(f"ytsearch{job.get('search_n', 30)}:{q}", job.get("search_n", 30))
        rec["newest"] = flat(f"ytsearchdate20:{q}", 20)
        study.append(rec)
    json.dump(study, open(os.path.join(out, "search.json"), "w"), indent=1, ensure_ascii=False)
    print(f"search study: {len(study)} queries")

# Optional upload-date lookup: "date_ids": ["videoId", ...]. Public flat listings only (no per-video page fetch).
# For each id: a flat search for the id finds its channel, then the channel's flat /videos listing with yt-dlp's
# approximate_date option gives an approximate upload date ("3 years ago" -> timestamp). Writes outputs/viral/<id>/dates.json.
if job.get("date_ids"):
    import datetime
    def fj(args):
        r = subprocess.run(["yt-dlp", "--flat-playlist", "-J"] + args, capture_output=True, text=True, timeout=900)
        return (json.loads(r.stdout), None) if not r.returncode else (None, r.stderr[-300:])
    dates, chans = [], {}
    for vid in job["date_ids"]:
        rec = {"id": vid}
        d, err = fj([f"ytsearch10:{vid}"])
        hit = next((e for e in (d or {}).get("entries") or [] if e.get("id") == vid), None)
        cid = (hit or {}).get("channel_id")
        rec.update({"title": (hit or {}).get("title"), "channel": (hit or {}).get("channel"), "channel_id": cid, "views": (hit or {}).get("view_count")})
        if not cid:
            rec["error"] = err or "not found in search"; dates.append(rec); continue
        if cid not in chans:
            chans[cid] = fj(["--extractor-args", "youtubetab:approximate_date", "--playlist-end", str(job.get("date_depth", 1500)),
                             f"https://www.youtube.com/channel/{cid}/videos"])
        cd, cerr = chans[cid]
        ents = (cd or {}).get("entries") or []
        e = next((x for x in ents if x.get("id") == vid), None)
        rec["listed"] = len(ents); rec["subs"] = (cd or {}).get("channel_follower_count")
        ts = (e or {}).get("timestamp") or (e or {}).get("release_timestamp")
        if ts:
            rec["approx_upload"] = datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d")
            rec["days"] = max(1, (datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(ts)).days)
            if rec.get("views"): rec["views_per_day"] = round(rec["views"] / rec["days"])
        else:
            rec["error"] = cerr or ("not in first %d uploads" % len(ents) if not e else "no date")
        dates.append(rec)
    json.dump(dates, open(os.path.join(out, "dates.json"), "w"), indent=1, ensure_ascii=False)
    print(f"dates: {sum(1 for r in dates if r.get('approx_upload'))}/{len(dates)}")
