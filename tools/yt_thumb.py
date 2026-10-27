"""Replace the custom thumbnail of one of the channel's own videos (long-form; JPG/PNG under 2 MB). Touches nothing else.

Usage: python3 tools/yt_thumb.py jobs/ytthumb/<id>.json
Job:   {"id", "token_secret": "YT_RT_BHUGOL_EN", "video_id": "...", "thumbnail": "jobs/ytthumb/<id>.jpg"}
Writes outputs/ytthumb/<id>.json (thumbnail URLs returned by YouTube).
"""
import json, os, sys
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

J = json.load(open(sys.argv[1])); out = os.path.join("outputs", "ytthumb"); os.makedirs(out, exist_ok=True)
creds = Credentials(None, refresh_token=os.environ[J["token_secret"]], token_uri="https://oauth2.googleapis.com/token",
                    client_id=os.environ["YT_CLIENT_ID"], client_secret=os.environ["YT_CLIENT_SECRET"])
creds.refresh(Request())
yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
me = yt.channels().list(part="id", mine=True).execute()["items"][0]["id"]
v = yt.videos().list(part="snippet", id=J["video_id"]).execute()["items"][0]
if v["snippet"]["channelId"] != me: sys.exit("video does not belong to this token's channel")
mime = "image/png" if J["thumbnail"].lower().endswith(".png") else "image/jpeg"
r = yt.thumbnails().set(videoId=J["video_id"], media_body=MediaFileUpload(J["thumbnail"], mimetype=mime)).execute()
R = {"id": J["id"], "video_id": J["video_id"], "ok": True, "items": r.get("items", [])}
json.dump(R, open(os.path.join(out, J["id"] + ".json"), "w"), indent=1, ensure_ascii=False); print(json.dumps(R, ensure_ascii=False)[:500])
