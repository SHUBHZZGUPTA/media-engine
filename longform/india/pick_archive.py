#!/usr/bin/env python3
"""Pick one image per search result and write a download job + credits.
Usage: pick_archive.py job_id search_dir [search_dir2 ...]  (later dirs override earlier); OVR = manual picks by title substring."""
import json, glob, os, sys
OVR = {"great_bath": "Great bath view Mohenjodaro", "unicorn_seal": "IndusValleySeals", "akbar_painting": "Court of Akbar from Akbarnama", "lion_capital": "Lion capital of Ashoka, Sarnath.jpg", "indira_gandhi": "Indira Gandhi official portrait (cropped)", "qutb_minar": "Qutb Minar with Neem Tree", "mahabodhi": "Worshipper at Mahabodhi", "koh_i_noor": "Replica of the Koh-i-Noor (cropped)"}
SKIP_EXT = (".pdf", ".djvu", ".tif", ".tiff", ".svg", ".gif", ".webm", ".ogv")
job_id, dirs = sys.argv[1], sys.argv[2:]
res = {}
for d in dirs:
    for f in glob.glob(os.path.join(d, "s_*.json")):
        try: q = json.load(open(f))
        except Exception: continue
        pages = sorted(q.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 0))
        if pages: res[os.path.basename(f)[2:-5]] = pages
files, credits = [], {}
for k, pages in sorted(res.items()):
    cand = [p for p in pages if p.get("imageinfo") and not p["title"].lower().endswith(SKIP_EXT) and p["imageinfo"][0].get("width", 0) >= 380]
    if k in OVR: cand = [p for p in cand if OVR[k] in p["title"]] or cand
    if not cand: print("none:", k); continue
    land = [p for p in cand if p["imageinfo"][0]["width"] >= p["imageinfo"][0]["height"] * 1.1]
    p = cand[0] if k in OVR else (land or cand)[0]
    ii = p["imageinfo"][0]; url = ii.get("thumburl") or ii["url"]
    ext = ".png" if p["title"].lower().endswith(".png") else ".jpg"
    files.append({"name": k + ext, "url": url})
    md = ii.get("extmetadata", {}); credits[k] = {"title": p["title"], "license": md.get("LicenseShortName", {}).get("value"), "artist": md.get("Artist", {}).get("value", "")[:200], "page": ii.get("descriptionurl")}
    print(f"{k:26s} {p['title'][5:70]}  [{credits[k]['license']}]")
json.dump({"id": job_id, "ua": "media-engine/1.0 (BHUGOL research; contact via GitHub)", "delay": 10, "files": files}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "jobs", "fetch", job_id + ".json"), "w"), indent=1)
json.dump(credits, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"credits_{job_id}.json"), "w"), indent=1)
print(len(files), "files")
