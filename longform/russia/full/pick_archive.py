#!/usr/bin/env python3
"""Pick one image per search result and write a download job + credits.
Usage: pick_archive.py job_id search_dir [search_dir2 ...]  (later dirs override earlier); OVR = manual picks by title substring."""
import json, glob, os, sys
OVR = {"bloody_sunday": "Q81561", "catherine_horse": "Eriksen (Hermita", "ivan4_portrait": "Vasnetsov Ioann", "kremlin": "Moskva river. Kremlin P5162723",
       "berlin_wall": "people walking", "peter_alexei": "Interrogating the Tsarevich Alexei Petr", "yeltsin_tank": "Yeltsin's tanks", "gorbachev": "Mikhail Gorbachev 1987.jpg",
       "nicholas2_family": "Romanov", "yermak": "Surikov Pokoreniye", "trotsky": "Leon Trotsky, 1924", "alaska_check": "Alaska Purchase (hi-res)",
       "st_basil": "Red Square, Moscow, Russia", "lenin_mausoleum": "Red Square Lenin's mausoleum.jpg", "moscow_1941": "RIAN archive 284", "putin_2000": "Presidential Oath",
       "stalingrad": "RIAN archive 2251", "gulag": "Canal Mer Blanche.jpg", "chernobyl": "IAEA 02790036", "collectivisation": "В нашем колхозе", "barbarossa": "NARA - 540155.jpg", "kyiv_1240": "Siege of Kiev (1240).png", "kalita": "Ivan Kalita.jpg", "arkhipov": "Vasili Arkhipov.jpg", "berlin_1945": "Ruins of the Reichstag", "false_dmitry": "False Dmitry I portrait.png", "feb_revolution": "Soldiers demonstration", "gagarin": "Yuri Gagarin (1961) - Restoration", "ipatiev": "Ipat'jev Haus", "golden_horde_tribute": "Менгу-Тимур", "streltsy": "Streltsy Uprising, 1839", "minin_pozharsky": "Moscow - 2025 - Bas-relief", "peter_portrait": "Andrei Matveev", "winter_palace_1917": "Winter Palace (21134849722)", "moscow_1990s": "White House Moscow (1992)", "cuba_missiles": "Cuban missiles.jpg", "poles_kremlin": "Lissner.jpg", "michael_romanov": "Michael titularnik2", "alaska_settlement": "Shelikhov settlement", "decembrists": "CPA 1591"}
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
json.dump({"id": job_id, "ua": "media-engine/1.0 (BHUGOL research; contact via GitHub)", "delay": 10, "files": files}, open(f"jobs/fetch/{job_id}.json", "w"), indent=1)
json.dump(credits, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"credits_{job_id}.json"), "w"), indent=1)
print(len(files), "files")
