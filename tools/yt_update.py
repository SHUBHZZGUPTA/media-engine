"""Change status fields of one of the channel's own videos (e.g. the "altered or synthetic content" label) without touching
anything else. videos.update(part=status) replaces the whole status block, so this reads the current status first, keeps every
existing field (privacy, scheduled publishAt, license, embeddable, stats, made-for-kids) and changes only the fields in the job.

Usage: python3 tools/yt_update.py jobs/ytupdate/<id>.json
Job:   {"id", "token_secret": "YT_RT_BHUGOL_EN", "video_id": "...", "status": {"containsSyntheticMedia": false}}
       Allowed status keys: containsSyntheticMedia, selfDeclaredMadeForKids, embeddable, publicStatsViewable,
       and "unschedule": true (only for a not-yet-public scheduled video: removes publishAt so it stays private),
       or "publishAt": "<future ISO UTC>" (only for a private video: moves or sets its scheduled publish time).
       Optional "snippet": {"title": "...", "description": "...", "tags": [...]} renames / re-describes the video. The whole
       snippet is sent back with every other field kept (categoryId, language, ...), only the given keys change. A job may
       carry "status", "snippet" or both.
Writes outputs/ytupdate/<id>.json (before, the request, and what was read back after).
"""
import json, os, sys
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

ALLOWED = {"containsSyntheticMedia", "selfDeclaredMadeForKids", "embeddable", "publicStatsViewable", "unschedule", "publishAt"}
SNIP_ALLOWED = {"title", "description", "tags"}
SNIP_KEEP = ("title", "description", "tags", "categoryId", "defaultLanguage", "defaultAudioLanguage")
KEEP = ("privacyStatus", "publishAt", "license", "embeddable", "publicStatsViewable", "selfDeclaredMadeForKids", "containsSyntheticMedia")

J = json.load(open(sys.argv[1])); out = os.path.join("outputs", "ytupdate"); os.makedirs(out, exist_ok=True)
J.setdefault("status", {}); SN = J.get("snippet") or {}
bad = set(J["status"]) - ALLOWED
if bad: sys.exit(f"refusing to change {sorted(bad)}: only {sorted(ALLOWED)} are allowed")
bad = set(SN) - SNIP_ALLOWED
if bad: sys.exit(f"refusing to change snippet {sorted(bad)}: only {sorted(SNIP_ALLOWED)} are allowed")
if "title" in SN and not (0 < len(SN["title"]) <= 100): sys.exit("title must be 1-100 characters")
if not J["status"] and not SN: sys.exit("nothing to change")
creds = Credentials(None, refresh_token=os.environ[J["token_secret"]], token_uri="https://oauth2.googleapis.com/token",
                    client_id=os.environ["YT_CLIENT_ID"], client_secret=os.environ["YT_CLIENT_SECRET"])
creds.refresh(Request())
yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
me = yt.channels().list(part="id", mine=True).execute()["items"][0]["id"]
items = yt.videos().list(part="snippet,status", id=J["video_id"]).execute().get("items", [])
if not items:
    json.dump({"id": J["id"], "video_id": J["video_id"], "ok": False, "error": "video not found on this channel (deleted or never processed)"}, open(os.path.join(out, J["id"] + ".json"), "w"), indent=1)
    sys.exit("video not found")
v = items[0]
if v["snippet"]["channelId"] != me: sys.exit("video does not belong to this token's channel")
snip_before = v["snippet"]
if SN:
    sn = {k: snip_before[k] for k in SNIP_KEEP if k in snip_before}; sn.update(SN)
    yt.videos().update(part="snippet", body={"id": J["video_id"], "snippet": sn}).execute()
    snip_after = yt.videos().list(part="snippet", id=J["video_id"]).execute()["items"][0]["snippet"]
    snip_ok = all(snip_after.get(k) == v2 for k, v2 in SN.items())
    if not J["status"]:
        R = {"id": J["id"], "video_id": J["video_id"], "requested_snippet": SN, "before": {k: snip_before.get(k) for k in SN},
             "after": {k: snip_after.get(k) for k in SN}, "status_after": yt.videos().list(part="status", id=J["video_id"]).execute()["items"][0]["status"], "ok": snip_ok}
        json.dump(R, open(os.path.join(out, J["id"] + ".json"), "w"), indent=1, ensure_ascii=False); print(json.dumps(R, ensure_ascii=False)); sys.exit(0 if snip_ok else 1)
before = v["status"]
new = {k: before[k] for k in KEEP if k in before}
if "selfDeclaredMadeForKids" not in new and "madeForKids" in before: new["selfDeclaredMadeForKids"] = before["madeForKids"]
unsched = J["status"].pop("unschedule", False)
if unsched:
    if before.get("privacyStatus") != "private": sys.exit("unschedule only applies to a private (scheduled) video")
    new["publishAt"] = None; new["privacyStatus"] = "private"   # explicit null clears the schedule
resched = "publishAt" in J["status"]
if resched and before.get("privacyStatus") != "private": sys.exit("publishAt can only be set on a private (scheduled or draft) video")
new.update(J["status"])
yt.videos().update(part="status", body={"id": J["video_id"], "status": new}).execute()
after = yt.videos().list(part="status", id=J["video_id"]).execute()["items"][0]["status"]
ok = all(after.get(k) == v2 for k, v2 in J["status"].items() if k in after) and after.get("privacyStatus") == before.get("privacyStatus") \
     and (resched or (after.get("publishAt") == before.get("publishAt") if not unsched else "publishAt" not in after))
R = {"id": J["id"], "video_id": J["video_id"], "requested": dict(J["status"], unschedule=unsched), "before": before, "after": after, "ok": ok}
if SN: R.update(requested_snippet=SN, snippet_ok=snip_ok, ok=ok and snip_ok)
json.dump(R, open(os.path.join(out, J["id"] + ".json"), "w"), indent=1, ensure_ascii=False); print(json.dumps(R, ensure_ascii=False))
