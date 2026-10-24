"""Per-video statistics for each connected YouTube channel. Read-only: uploads nothing, changes nothing.

Usage: python3 tools/yt_stats.py jobs/ytstats/<id>.json
Job:   {"id": "...", "tokens": ["YT_RT_BHUGOL_EN", ...]}   (names of GitHub secrets, passed in as env vars)
Writes outputs/ytstats/<id>/report.json:
  channels[]  : id, title, handle, subscribers, videos, views (lifetime), checked
  videos[]    : every upload with views/likes/comments, duration, privacy, publishAt, plus
                Analytics averageViewPercentage / averageViewDuration where available
  daily[]     : views, watch minutes, subscribers gained per day for the last 28 days
Never writes tokens.
"""
import json, os, sys, urllib.parse, urllib.request, datetime, re

job = json.load(open(sys.argv[1])); out = os.path.join("outputs", "ytstats", job["id"]); os.makedirs(out, exist_ok=True)
CID, CSEC = os.environ.get("YT_CLIENT_ID", ""), os.environ.get("YT_CLIENT_SECRET", "")
NOW = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def call(url, data=None, token=None):
    req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode() if data else None)
    if token: req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req, timeout=30) as r: return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        try: body = json.load(e)
        except Exception: body = {"raw": e.read()[:300].decode("utf-8", "replace")}
        return e.code, body


def iso_seconds(d):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    if not m: return None
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s


report = {"checked": NOW, "channels": [], "videos": [], "daily": [], "errors": []}
for name in job["tokens"]:
    rt = os.environ.get(name, "")
    if not rt or not CID or not CSEC:
        report["errors"].append({"secret": name, "error": "token not set"}); continue
    s, tok = call("https://oauth2.googleapis.com/token", {"client_id": CID, "client_secret": CSEC, "refresh_token": rt, "grant_type": "refresh_token"})
    if s != 200:
        report["errors"].append({"secret": name, "error": tok.get("error_description") or tok.get("error")}); continue
    at = tok["access_token"]
    s, ch = call("https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,contentDetails&mine=true", token=at)
    items = ch.get("items", []) if s == 200 else []
    if not items:
        report["errors"].append({"secret": name, "error": ch.get("error", {}).get("message") or "no channel"}); continue
    c = items[0]; cid = c["id"]
    report["channels"].append({"secret": name, "id": cid, "title": c["snippet"]["title"], "handle": c["snippet"].get("customUrl"),
                               "subscribers": c["statistics"].get("subscriberCount"), "videos": c["statistics"].get("videoCount"),
                               "views": c["statistics"].get("viewCount"), "checked": NOW})
    # every upload (paged), then statistics in batches of 50
    up = c.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads"); ids = []; page = ""
    while up:
        s2, pl = call("https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId=" + up + ("&pageToken=" + page if page else ""), token=at)
        if s2 != 200: report["errors"].append({"secret": name, "error": pl.get("error", {}).get("message")}); break
        ids += [i["contentDetails"]["videoId"] for i in pl.get("items", [])]
        page = pl.get("nextPageToken", "")
        if not page or len(ids) >= 500: break
    vids = {}
    for i in range(0, len(ids), 50):
        s3, vl = call("https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails,status&id=" + ",".join(ids[i:i + 50]), token=at)
        if s3 != 200: report["errors"].append({"secret": name, "error": vl.get("error", {}).get("message")}); continue
        for v in vl.get("items", []):
            st = v.get("statistics", {}); su = v.get("status", {}); sn = v["snippet"]
            vids[v["id"]] = {"video_id": v["id"], "channel_id": cid, "channel": c["snippet"]["title"], "title": sn.get("title"),
                             "published": sn.get("publishedAt"), "privacy": su.get("privacyStatus"), "publish_at": su.get("publishAt"),
                             "duration_s": iso_seconds(v.get("contentDetails", {}).get("duration")),
                             "views": int(st["viewCount"]) if st.get("viewCount") else None, "likes": int(st["likeCount"]) if st.get("likeCount") else None,
                             "comments": int(st["commentCount"]) if st.get("commentCount") else None}
    # Analytics: per-video retention (lifetime) and per-day views (28 days)
    end = datetime.date.today(); start28 = end - datetime.timedelta(days=28)
    q = urllib.parse.urlencode({"ids": "channel==MINE", "startDate": "2020-01-01", "endDate": end.isoformat(), "dimensions": "video",
                                "metrics": "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage", "sort": "-views", "maxResults": 200})
    s4, an = call("https://youtubeanalytics.googleapis.com/v2/reports?" + q, token=at)
    if s4 == 200:
        for row in an.get("rows") or []:
            vid = vids.get(row[0])
            if vid: vid.update(an_views=row[1], watch_minutes=row[2], avg_view_duration_s=row[3], avg_view_pct=row[4])
    else: report["errors"].append({"secret": name, "error": "analytics by video: " + str(an.get("error", {}).get("message"))})
    q = urllib.parse.urlencode({"ids": "channel==MINE", "startDate": start28.isoformat(), "endDate": end.isoformat(), "dimensions": "day",
                                "metrics": "views,estimatedMinutesWatched,subscribersGained", "sort": "day"})
    s5, dy = call("https://youtubeanalytics.googleapis.com/v2/reports?" + q, token=at)
    if s5 == 200:
        for row in dy.get("rows") or []:
            report["daily"].append({"channel_id": cid, "channel": c["snippet"]["title"], "day": row[0], "views": row[1], "watch_minutes": row[2], "subs_gained": row[3]})
    else: report["errors"].append({"secret": name, "error": "analytics by day: " + str(dy.get("error", {}).get("message"))})
    report["videos"] += list(vids.values())

json.dump(report, open(os.path.join(out, "report.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps({"channels": len(report["channels"]), "videos": len(report["videos"]), "daily": len(report["daily"]), "errors": report["errors"]}, indent=1))
