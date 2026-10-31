"""Set a channel's banner image and/or description (brandingSettings), changing nothing else.
channels.update(part=brandingSettings) replaces the whole block, so this reads the current brandingSettings first, keeps every
existing field, and changes only channel.description and/or image.bannerExternalUrl. The previous values are saved in the
output so a change can be reverted.

Usage: python3 tools/yt_channel.py jobs/ytchannel/<id>.json
Job:   {"id", "token_secret": "YT_RT_MM_EN", "expect_channel_id": "UC...", "description": "...", "banner": "path/in/repo.jpg"}
       (description and banner are each optional; expect_channel_id is required so a wrong token can't edit another channel)
Writes outputs/ytchannel/<id>.json (before, request, after).
Profile pictures can't be set through the API (YouTube Studio only).
"""
import json, os, sys
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

J = json.load(open(sys.argv[1])); out = os.path.join("outputs", "ytchannel"); os.makedirs(out, exist_ok=True)
res = {"id": J["id"], "ok": False}
def done(): json.dump(res, open(os.path.join(out, J["id"] + ".json"), "w"), indent=1, ensure_ascii=False)
creds = Credentials(None, refresh_token=os.environ[J["token_secret"]], token_uri="https://oauth2.googleapis.com/token",
                    client_id=os.environ["YT_CLIENT_ID"], client_secret=os.environ["YT_CLIENT_SECRET"])
creds.refresh(Request())
yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
ch = yt.channels().list(part="id,snippet,brandingSettings", mine=True).execute()["items"][0]
res.update(channel_id=ch["id"], channel=ch["snippet"]["title"])
if ch["id"] != J["expect_channel_id"]:
    res["error"] = f"token belongs to {ch['id']} ({ch['snippet']['title']}), expected {J['expect_channel_id']}: nothing changed"; done(); sys.exit(1)
bs = ch.get("brandingSettings", {}); res["before"] = {"description": bs.get("channel", {}).get("description"), "bannerExternalUrl": bs.get("image", {}).get("bannerExternalUrl")}
if J.get("banner"):
    up = yt.channelBanners().insert(media_body=MediaFileUpload(J["banner"], mimetype="image/jpeg" if J["banner"].endswith(".jpg") else "image/png")).execute()
    bs.setdefault("image", {})["bannerExternalUrl"] = up["url"]; res["banner_url"] = up["url"]
if "description" in J: bs.setdefault("channel", {})["description"] = J["description"]
yt.channels().update(part="brandingSettings", body={"id": ch["id"], "brandingSettings": bs}).execute()
after = yt.channels().list(part="brandingSettings", id=ch["id"]).execute()["items"][0]["brandingSettings"]
res["after"] = {"description": after.get("channel", {}).get("description"), "bannerExternalUrl": after.get("image", {}).get("bannerExternalUrl")}
res["ok"] = True; done(); print(json.dumps(res, ensure_ascii=False)[:600])
