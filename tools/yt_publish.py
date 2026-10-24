"""Upload one queued video to YouTube (resumable), optionally scheduled, then verify its final status.

Usage: python3 tools/yt_publish.py <queue dir containing publish.json> <out json>
publish.json: {"id", "file", "token_secret": "YT_RT_BHUGOL_EN", "title", "description", "tags": [...], "categoryId": "27",
               "privacy": "public"|"unlisted"|"private", "publishAt": "2026-10-25T12:30:00Z" | null,
               "containsSyntheticMedia": false, "madeForKids": false, "language": "en", "thumbnail": "thumbnail.jpg" (optional)}
With publishAt the video is uploaded private and YouTube publishes it at that time.
Upload pattern adapted from darkzOGx/youtube-automation-agent (MIT).
"""
import json, os, sys, time
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

qdir, out = sys.argv[1], sys.argv[2]
P = json.load(open(os.path.join(qdir, "publish.json")))
creds = Credentials(None, refresh_token=os.environ[P["token_secret"]], token_uri="https://oauth2.googleapis.com/token",
                    client_id=os.environ["YT_CLIENT_ID"], client_secret=os.environ["YT_CLIENT_SECRET"])
creds.refresh(Request())
yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
me = yt.channels().list(part="snippet", mine=True).execute()["items"][0]
status = {"selfDeclaredMadeForKids": bool(P.get("madeForKids", False)), "containsSyntheticMedia": bool(P.get("containsSyntheticMedia", False))}
if P.get("publishAt"): status.update(privacyStatus="private", publishAt=P["publishAt"])
else: status["privacyStatus"] = P.get("privacy", "public")
body = {"snippet": {"title": P["title"], "description": P["description"], "tags": P.get("tags", []), "categoryId": str(P.get("categoryId", "27")),
                    "defaultLanguage": P.get("language", "en"), "defaultAudioLanguage": P.get("language", "en")}, "status": status}
media = MediaFileUpload(os.path.join(qdir, P["file"]), mimetype="video/mp4", chunksize=8 * 1024 * 1024, resumable=True)
req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
resp = None
while resp is None:
    st, resp = req.next_chunk(num_retries=5)
    if st: print(f"uploaded {int(st.progress() * 100)}%", flush=True)
vid = resp["id"]; print("video id", vid)
R = {"id": P["id"], "video_id": vid, "url": f"https://youtube.com/shorts/{vid}", "channel": me["snippet"]["title"], "channel_id": me["id"],
     "requested": status, "returned_status": resp.get("status"), "checks": []}
if P.get("thumbnail"):   # optional custom thumbnail (long-form; JPG/PNG under 2 MB). Shorts thumbnails can't be set by API.
    try:
        th = yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(os.path.join(qdir, P["thumbnail"]), mimetype="image/jpeg")).execute()
        R["thumbnail"] = {"ok": True, "url": ((th.get("items") or [{}])[0].get("maxres") or (th.get("items") or [{}])[0].get("high") or {}).get("url")}
    except Exception as e:
        R["thumbnail"] = {"ok": False, "error": str(e)[:300]}
    print("thumbnail", R["thumbnail"], flush=True)
for wait in (60, 180):   # the private lock and processing show up after the upload finishes
    time.sleep(wait)
    v = yt.videos().list(part="status,processingDetails", id=vid).execute().get("items", [])
    R["checks"].append({"after_s": wait, "status": v[0].get("status") if v else None, "processing": v[0].get("processingDetails", {}).get("processingStatus") if v else None})
want = status["privacyStatus"]; got = (R["checks"][-1]["status"] or {}).get("privacyStatus")
R["locked_private"] = (want != "private" and got == "private")
R["ok"] = not R["locked_private"]
json.dump(R, open(out, "w"), indent=1, ensure_ascii=False); print(json.dumps(R, indent=1, ensure_ascii=False))
