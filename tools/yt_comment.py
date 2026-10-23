"""Post a top-level comment from the channel on one of its own videos (pinning is not possible through the API).

Usage: python3 tools/yt_comment.py jobs/ytcomment/<id>.json
Job:   {"id", "token_secret": "YT_RT_BHUGOL_EN", "video_id": "...", "text": "..."}
Writes outputs/ytcomment/<id>.json (comment id, text as posted).
"""
import json, os, sys
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

J = json.load(open(sys.argv[1])); out = os.path.join("outputs", "ytcomment"); os.makedirs(out, exist_ok=True)
creds = Credentials(None, refresh_token=os.environ[J["token_secret"]], token_uri="https://oauth2.googleapis.com/token",
                    client_id=os.environ["YT_CLIENT_ID"], client_secret=os.environ["YT_CLIENT_SECRET"])
creds.refresh(Request())
yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
v = yt.videos().list(part="snippet", id=J["video_id"]).execute()["items"][0]
r = yt.commentThreads().insert(part="snippet", body={"snippet": {"channelId": v["snippet"]["channelId"], "videoId": J["video_id"],
        "topLevelComment": {"snippet": {"textOriginal": J["text"]}}}}).execute()
R = {"id": J["id"], "video_id": J["video_id"], "comment_id": r["id"], "text": r["snippet"]["topLevelComment"]["snippet"]["textOriginal"]}
json.dump(R, open(os.path.join(out, J["id"] + ".json"), "w"), indent=1, ensure_ascii=False); print(json.dumps(R, ensure_ascii=False))
