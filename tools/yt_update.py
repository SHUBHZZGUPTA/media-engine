"""Change status fields of one of the channel's own videos (e.g. the "altered or synthetic content" label) without touching
anything else. videos.update(part=status) replaces the whole status block, so this reads the current status first, keeps every
existing field (privacy, scheduled publishAt, license, embeddable, stats, made-for-kids) and changes only the fields in the job.

Usage: python3 tools/yt_update.py jobs/ytupdate/<id>.json
Job:   {"id", "token_secret": "YT_RT_BHUGOL_EN", "video_id": "...", "status": {"containsSyntheticMedia": false}}
       Allowed status keys: containsSyntheticMedia, selfDeclaredMadeForKids, embeddable, publicStatsViewable,
       and "unschedule": true (only for a not-yet-public scheduled video: removes publishAt so it stays private),
       or "publishAt": "<future ISO UTC>" (only for a private video: moves or sets its scheduled publish time).
Writes outputs/ytupdate/<id>.json (status before, the request, and the status read back after).
"""
import json, os, sys
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

ALLOWED = {"containsSyntheticMedia", "selfDeclaredMadeForKids", "embeddable", "publicStatsViewable", "unschedule", "publishAt"}
KEEP = ("privacyStatus", "publishAt", "license", "embeddable", "publicStatsViewable", "selfDeclaredMadeForKids", "containsSyntheticMedia")

J = json.load(open(sys.argv[1])); out = os.path.join("outputs", "ytupdate"); os.makedirs(out, exist_ok=True)
bad = set(J.get("status", {})) - ALLOWED
if bad: sys.exit(f"refusing to change {sorted(bad)}: only {sorted(ALLOWED)} are allowed")
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
json.dump(R, open(os.path.join(out, J["id"] + ".json"), "w"), indent=1, ensure_ascii=False); print(json.dumps(R, ensure_ascii=False))
