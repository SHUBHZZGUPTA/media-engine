"""Deep, read-only analytics pull for the connected channels plus public competitor data. Uploads nothing, changes nothing.

Usage: python3 tools/yt_deep.py jobs/ytdeep/<id>.json
Job: {"id": "...", "tokens": ["YT_RT_BHUGOL_EN", ...],
      "competitors": {"bhugol": ["@Glore3", "channel/UC..."], "mirage": ["@TheMoneyGPS"]},
      "comp_per_channel": 60, "comp_thumbs": 8}
Writes outputs/ytdeep/<id>/report.json and thumbs/<video id>.jpg (own: all; competitors: top N by views).
Own channels: every upload with snippet (title, description, tags), stats, per-video Analytics (retention, shares,
subs gained), daily views since publish, traffic sources, retention curve; channel-level audience (age/gender,
country, device, subscribed status, traffic source, search terms, content type) and 90 daily rows.
Competitors: public channel stats + recent uploads with publish time, views, duration, description, tags.
Never writes tokens.
"""
import json, os, sys, urllib.parse, urllib.request, datetime, re, io

job = json.load(open(sys.argv[1])); out = os.path.join("outputs", "ytdeep", job["id"])
tdir = os.path.join(out, "thumbs"); os.makedirs(tdir, exist_ok=True)
CID, CSEC = os.environ.get("YT_CLIENT_ID", ""), os.environ.get("YT_CLIENT_SECRET", "")
NOW = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
TODAY = datetime.date.today()
try:
    from PIL import Image
except Exception:
    Image = None


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


def iso_seconds(d):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    if not m: return None
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s


def analytics(at, errs, label, **params):
    p = {"ids": "channel==MINE", "startDate": "2020-01-01", "endDate": TODAY.isoformat()}; p.update(params)
    s, r = call("https://youtubeanalytics.googleapis.com/v2/reports?" + urllib.parse.urlencode(p), token=at)
    if s != 200:
        errs.append(label + ": " + str((r.get("error") or {}).get("message") if isinstance(r.get("error"), dict) else r.get("error"))); return None
    cols = [h["name"] for h in r.get("columnHeaders", [])]
    return [dict(zip(cols, row)) for row in (r.get("rows") or [])]


def thumb(vid, url=None):
    dest = os.path.join(tdir, vid + ".jpg")
    if os.path.exists(dest): return True
    for u in ([url] if url else []) + [f"https://i.ytimg.com/vi/{vid}/oardefault.jpg", f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"]:
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=20) as r: b = r.read()
            if len(b) < 2000: continue
            if Image:
                im = Image.open(io.BytesIO(b)).convert("RGB"); w = 300
                im = im.resize((w, int(im.height * w / im.width))); im.save(dest, quality=82)
            else:
                open(dest, "wb").write(b)
            return True
        except Exception:
            continue
    return False


def video_rows(at, ids, errs, channel_label):
    rows = {}
    for i in range(0, len(ids), 50):
        s, vl = call("https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails,status&id=" + ",".join(ids[i:i + 50]), token=at)
        if s != 200: errs.append(channel_label + " videos.list: " + str(vl.get("error", {}).get("message"))); continue
        for v in vl.get("items", []):
            st, sn, su = v.get("statistics", {}), v["snippet"], v.get("status", {})
            th = sn.get("thumbnails", {})
            rows[v["id"]] = {"video_id": v["id"], "title": sn.get("title"), "published": sn.get("publishedAt"),
                             "description": (sn.get("description") or "")[:1500], "tags": sn.get("tags") or [],
                             "language": sn.get("defaultAudioLanguage") or sn.get("defaultLanguage"), "category": sn.get("categoryId"),
                             "privacy": su.get("privacyStatus"), "publish_at": su.get("publishAt"),
                             "duration_s": iso_seconds(v.get("contentDetails", {}).get("duration")),
                             "views": int(st["viewCount"]) if st.get("viewCount") else 0,
                             "likes": int(st["likeCount"]) if st.get("likeCount") else 0,
                             "comments": int(st["commentCount"]) if st.get("commentCount") else 0,
                             "thumb_url": (th.get("maxres") or th.get("high") or th.get("default") or {}).get("url")}
    return rows


def uploads(at, playlist, cap, errs, label):
    ids, page = [], ""
    while playlist:
        s, pl = call("https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId=" + playlist + ("&pageToken=" + page if page else ""), token=at)
        if s != 200: errs.append(label + " uploads: " + str(pl.get("error", {}).get("message"))); break
        ids += [i["contentDetails"]["videoId"] for i in pl.get("items", [])]
        page = pl.get("nextPageToken", "")
        if not page or len(ids) >= cap: break
    return ids[:cap]


report = {"checked": NOW, "channels": [], "competitors": [], "errors": []}
any_at = None
for name in job["tokens"]:
    errs = []
    rt = os.environ.get(name, "")
    if not rt or not CID or not CSEC:
        report["errors"].append({"secret": name, "error": "token not set"}); continue
    s, tok = call("https://oauth2.googleapis.com/token", {"client_id": CID, "client_secret": CSEC, "refresh_token": rt, "grant_type": "refresh_token"})
    if s != 200:
        report["errors"].append({"secret": name, "error": tok.get("error_description") or tok.get("error")}); continue
    at = tok["access_token"]; any_at = any_at or at
    s, ch = call("https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,contentDetails&mine=true", token=at)
    items = ch.get("items", []) if s == 200 else []
    if not items:
        report["errors"].append({"secret": name, "error": "no channel"}); continue
    c = items[0]
    C = {"secret": name, "id": c["id"], "title": c["snippet"]["title"], "handle": c["snippet"].get("customUrl"),
         "created": c["snippet"].get("publishedAt"), "country": c["snippet"].get("country"),
         "subscribers": int(c["statistics"].get("subscriberCount") or 0), "video_count": int(c["statistics"].get("videoCount") or 0),
         "views": int(c["statistics"].get("viewCount") or 0), "errors": errs}
    ids = uploads(at, c.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads"), 500, errs, name)
    vids = video_rows(at, ids, errs, name)
    # per-video lifetime analytics
    for r in analytics(at, errs, "by video", dimensions="video", sort="-views", maxResults=200,
                       metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,likes,comments,shares,subscribersGained,subscribersLost") or []:
        if r["video"] in vids: vids[r["video"]].update({"a_" + k: v for k, v in r.items() if k != "video"})
    for r in analytics(at, errs, "engagedViews", dimensions="video", sort="-engagedViews", maxResults=200, metrics="engagedViews") or []:
        if r["video"] in vids: vids[r["video"]]["a_engagedViews"] = r["engagedViews"]
    for vid, v in vids.items():
        if v["privacy"] != "public": continue
        thumb(vid, v.get("thumb_url"))
        if not v.get("a_views") and not v["views"]: continue
        pub = (v["published"] or "")[:10] or "2020-01-01"
        v["daily"] = [[r["day"], r["views"]] for r in analytics(at, errs, "daily " + vid, dimensions="day", filters="video==" + vid,
                                                                  metrics="views", startDate=pub, sort="day") or []]
        v["traffic"] = {r["insightTrafficSourceType"]: r["views"] for r in analytics(at, errs, "traffic " + vid, dimensions="insightTrafficSourceType",
                                                                                     filters="video==" + vid, metrics="views") or []}
        rc = analytics(at, errs, "retention " + vid, dimensions="elapsedVideoTimeRatio", filters="video==" + vid,
                       metrics="audienceWatchRatio,relativeRetentionPerformance")
        if rc: v["retention"] = [[r["elapsedVideoTimeRatio"], r["audienceWatchRatio"], r.get("relativeRetentionPerformance")] for r in rc]
    C["videos"] = list(vids.values())
    A = {}
    A["age_gender"] = analytics(at, errs, "age_gender", dimensions="ageGroup,gender", metrics="viewerPercentage")
    A["country"] = analytics(at, errs, "country", dimensions="country", metrics="views,estimatedMinutesWatched,averageViewPercentage", sort="-views", maxResults=30)
    A["device"] = analytics(at, errs, "device", dimensions="deviceType", metrics="views,estimatedMinutesWatched", sort="-views")
    A["os"] = analytics(at, errs, "os", dimensions="operatingSystem", metrics="views", sort="-views", maxResults=10)
    A["subscribed"] = analytics(at, errs, "subscribed", dimensions="subscribedStatus", metrics="views,averageViewPercentage")
    A["traffic"] = analytics(at, errs, "traffic", dimensions="insightTrafficSourceType", metrics="views,estimatedMinutesWatched", sort="-views")
    A["search_terms"] = analytics(at, errs, "search terms", dimensions="insightTrafficSourceDetail", filters="insightTrafficSourceType==YT_SEARCH",
                                  metrics="views", sort="-views", maxResults=25)
    A["content_type"] = analytics(at, errs, "content type", dimensions="creatorContentType", metrics="views,estimatedMinutesWatched,averageViewPercentage")
    A["sharing"] = analytics(at, errs, "sharing", dimensions="sharingService", metrics="shares", sort="-shares", maxResults=10)
    A["daily"] = analytics(at, errs, "daily channel", dimensions="day", startDate=(TODAY - datetime.timedelta(days=90)).isoformat(),
                           metrics="views,estimatedMinutesWatched,subscribersGained,subscribersLost", sort="day")
    C["audience"] = A
    report["channels"].append(C)

# competitors (public data through the Data API)
for group, handles in (job.get("competitors") or {}).items():
    for h in handles:
        errs = []
        if not any_at: break
        q = ("forHandle=" + urllib.parse.quote(h)) if h.startswith("@") else ("id=" + h.split("/")[-1])
        s, ch = call("https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,contentDetails&" + q, token=any_at)
        items = ch.get("items", []) if s == 200 else []
        if not items:
            report["competitors"].append({"group": group, "handle": h, "error": "not found"}); continue
        c = items[0]
        ids = uploads(any_at, c["contentDetails"]["relatedPlaylists"]["uploads"], job.get("comp_per_channel", 60), errs, h)
        vids = list(video_rows(any_at, ids, errs, h).values())
        for v in sorted(vids, key=lambda v: -v["views"])[:job.get("comp_thumbs", 8)]:
            v["thumb"] = thumb(v["video_id"], v.get("thumb_url"))
        report["competitors"].append({"group": group, "handle": h, "id": c["id"], "title": c["snippet"]["title"],
                                      "country": c["snippet"].get("country"), "created": c["snippet"].get("publishedAt"),
                                      "subscribers": int(c["statistics"].get("subscriberCount") or 0),
                                      "views": int(c["statistics"].get("viewCount") or 0),
                                      "video_count": int(c["statistics"].get("videoCount") or 0), "videos": vids, "errors": errs})

json.dump(report, open(os.path.join(out, "report.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps({"channels": [(c["title"], len(c["videos"]), c["errors"][:5]) for c in report["channels"]],
                  "competitors": [(c.get("title") or c["handle"], len(c.get("videos", []))) for c in report["competitors"]],
                  "errors": report["errors"]}, indent=1, ensure_ascii=False))
