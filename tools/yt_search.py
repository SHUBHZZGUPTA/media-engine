"""Read-only YouTube search via the Data API (search.list + videos.list). Uploads nothing, changes nothing.
Results are not personalised: no watch history, and region/language are set explicitly.

Usage: python3 tools/yt_search.py jobs/ytsearch/<id>.json
Job: {"id": "...", "token": "YT_RT_MM_EN",            (name of the GitHub secret holding a refresh token, used only to authenticate)
      "regionCode": "US", "relevanceLanguage": "en",
      "publishedAfter": "2026-10-10T00:00:00Z", "maxResults": 50, "min_duration_s": 240,
      "queries": {"group_a": ["query 1", ...], "group_b": [...]}}
Quota: 100 units per query (search.list) + 1 unit per 50 videos (videos.list).
Writes outputs/ytsearch/<id>/report.json: per query the returned videos (id, title, channel id/title, published, duration, views)
and per group the distinct channels with at least one result >= min_duration_s. Never writes tokens.
"""
import json, os, re, sys, urllib.parse, urllib.request, datetime

job = json.load(open(sys.argv[1])); out = os.path.join("outputs", "ytsearch", job["id"]); os.makedirs(out, exist_ok=True)
CID, CSEC = os.environ.get("YT_CLIENT_ID", ""), os.environ.get("YT_CLIENT_SECRET", "")


def call(url, data=None, token=None):
    req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode() if data else None)
    if token: req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req, timeout=30) as r: return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        try: body = json.load(e)
        except Exception: body = {"raw": e.read()[:300].decode("utf-8", "replace")}
        return e.code, body
    except Exception as e:
        return 0, {"error": {"message": str(e)}}


def secs(d):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1))) if m else None


report = {"checked": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
          "params": {k: job.get(k) for k in ("regionCode", "relevanceLanguage", "publishedAfter", "maxResults", "min_duration_s")},
          "queries": {}, "groups": {}, "errors": []}
s, tok = call("https://oauth2.googleapis.com/token", {"client_id": CID, "client_secret": CSEC,
                                                       "refresh_token": os.environ.get(job["token"], ""), "grant_type": "refresh_token"})
if s != 200:
    report["errors"].append({"auth": s, "error": tok.get("error")})
    json.dump(report, open(os.path.join(out, "report.json"), "w"), indent=1); sys.exit(0)
at = tok["access_token"]; mind = job.get("min_duration_s", 240)
for group, qs in job["queries"].items():
    chans = {}
    for q in qs:
        p = {"part": "snippet", "type": "video", "q": q, "maxResults": job.get("maxResults", 50), "order": "relevance",
             "regionCode": job.get("regionCode", "US"), "relevanceLanguage": job.get("relevanceLanguage", "en"),
             "publishedAfter": job["publishedAfter"], "safeSearch": "none"}
        s, r = call("https://www.googleapis.com/youtube/v3/search?" + urllib.parse.urlencode(p), token=at)
        if s != 200:
            report["errors"].append({"query": q, "status": s, "error": (r.get("error") or {}).get("message") if isinstance(r.get("error"), dict) else r.get("error")}); continue
        items = [i for i in r.get("items", []) if i.get("id", {}).get("videoId")]
        ids = [i["id"]["videoId"] for i in items]
        det = {}
        if ids:
            s2, v = call("https://www.googleapis.com/youtube/v3/videos?part=contentDetails,statistics&id=" + ",".join(ids), token=at)
            if s2 == 200:
                for x in v.get("items", []): det[x["id"]] = x
        vids = []
        for rank, i in enumerate(items, 1):
            vid = i["id"]["videoId"]; d = det.get(vid, {})
            row = {"rank": rank, "id": vid, "title": i["snippet"]["title"], "channel_id": i["snippet"]["channelId"],
                   "channel": i["snippet"]["channelTitle"], "published": i["snippet"]["publishedAt"],
                   "duration_s": secs(d.get("contentDetails", {}).get("duration")), "views": int(d.get("statistics", {}).get("viewCount", 0) or 0)}
            vids.append(row)
            if (row["duration_s"] or 0) >= mind:
                chans.setdefault(row["channel_id"], {"channel": row["channel"], "first_query": q, "results": 0})["results"] += 1
        report["queries"][q] = {"group": group, "returned": len(items), "videos": vids}
    report["groups"][group] = chans
json.dump(report, open(os.path.join(out, "report.json"), "w"), indent=1, ensure_ascii=False)
print({g: len(c) for g, c in report["groups"].items()}, "errors:", len(report["errors"]))
