"""Check each YouTube refresh token: which channel it reaches and which permissions it has. Read-only, uploads nothing.

Usage: python3 tools/yt_check.py jobs/ytcheck/<id>.json
Job:   {"id": "...", "tokens": ["YT_RT_BHUGOL_EN", ...]}   (names of GitHub secrets, passed in as env vars)
Writes outputs/ytcheck/<id>/report.json (channel id/title/handle, scopes, analytics reachable). Never writes tokens.
"""
import json, os, sys, urllib.parse, urllib.request, datetime

job = json.load(open(sys.argv[1])); out = os.path.join("outputs", "ytcheck", job["id"]); os.makedirs(out, exist_ok=True)
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

report = {"client_id_set": bool(CID), "client_secret_set": bool(CSEC), "tokens": []}
for name in job["tokens"]:
    rt = os.environ.get(name, ""); r = {"secret": name, "present": bool(rt)}
    if not rt or not CID or not CSEC: report["tokens"].append(r); continue
    s, tok = call("https://oauth2.googleapis.com/token", {"client_id": CID, "client_secret": CSEC, "refresh_token": rt, "grant_type": "refresh_token"})
    if s != 200: r["refresh"] = {"ok": False, "status": s, "error": tok.get("error"), "detail": tok.get("error_description")}; report["tokens"].append(r); continue
    at = tok["access_token"]; r["refresh"] = {"ok": True}; r["scopes"] = sorted(tok.get("scope", "").split())
    s, ch = call("https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&mine=true", token=at)
    items = ch.get("items", []) if s == 200 else []
    r["channels"] = [{"id": c["id"], "title": c["snippet"]["title"], "handle": c["snippet"].get("customUrl"),
                      "videos": c["statistics"].get("videoCount"), "subscribers": c["statistics"].get("subscriberCount")} for c in items]
    if s != 200: r["channels_error"] = {"status": s, "error": ch.get("error", {}).get("message")}
    if items:
        end = datetime.date.today(); start = end - datetime.timedelta(days=28)
        q = urllib.parse.urlencode({"ids": "channel==MINE", "startDate": start.isoformat(), "endDate": end.isoformat(), "metrics": "views,engagedViews"})
        s, an = call("https://youtubeanalytics.googleapis.com/v2/reports?" + q, token=at)
        r["analytics"] = {"ok": s == 200, "status": s, "rows": an.get("rows") if s == 200 else None, "error": None if s == 200 else an.get("error", {}).get("message")}
    report["tokens"].append(r)
json.dump(report, open(os.path.join(out, "report.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps(report, indent=1, ensure_ascii=False))
