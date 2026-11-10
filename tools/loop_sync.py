#!/usr/bin/env python3
"""loop_sync.py — compute the writes that bring the BHUGOL Learning Loop store up to date.

Usage:
    python3 tools/loop_sync.py --loop outputs/loop/<id>/loop.json --db <export dir> --out <writes dir>
                               [--watch-prompt tools/loop_watch_prompt.txt]

<export dir> holds the store as the ArtifactData tool exports it with `out_dir`:
    <export dir>/<collection>/<doc_id>.json          the document body
    <export dir>/<collection>.versions.txt           the tool's result text for that `list` call, saved verbatim
                                                     (it carries "<doc_id>"  N bytes  version V per document)
Collections expected: meta, channels, videos, hypotheses, learnings, competitors, comp_videos, alerts, techniques.

Writes out:
    <writes dir>/batchNN.json      ArtifactData `batch` entries (≤ 50 each) with if_version pinned for existing docs
    <writes dir>/summary.md        what changed, alerts, hypotheses ready for a verdict, competitors to add to the pull
    <writes dir>/competitors.txt   every handle the next ytdeep job should pull (active + queued)
    <writes dir>/watch_jobs/       jobs/watch/*.json for competitors flagged `watch: true` (top outliers)

Rules:
  - A viewer's own fields on a video (techniques, hypotheses, verdict, notes, taggedAt, taggedBy, topic_type once
    topic_type_auto is false) are never overwritten.
  - Hypotheses are never moved to won/lost here; the script only fills `autoEval` and `readyForVerdict`.
    The verdict is Shubham's.
  - Alerts: one open alert per kind+channel; refreshed in place, never duplicated; stale_pull closes itself.
"""
import argparse, datetime as dt, json, os, re, statistics as st, sys

NOW = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
KEEP = ["title", "channel", "published", "published_ist", "upload_hour_ist", "upload_dow", "format", "duration_s", "privacy", "age_h",
        "views", "likes", "comments", "avg_pct", "avg_dur_s", "engaged", "eng_rate", "likes_per_1k", "comments_per_1k", "subs_gained", "shares",
        "v24", "v48", "v7d", "feed_share", "search_share", "browse_share", "retention", "tags_n", "thumb_url",
        "title_len", "has_number", "has_question", "emoji_n", "desc_len", "desc_links", "desc_hashtags", "x_med48", "cohort_med48"]
USER_FIELDS = ["techniques", "hypotheses", "verdict", "notes", "taggedAt", "taggedBy"]


def slug(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9_\-.~:@+]", "-", s.lower().lstrip("@"))).strip("-")[:80]


def median(xs):
    xs = [x for x in xs if x is not None]
    return st.median(xs) if xs else None


def mean(xs):
    xs = [x for x in xs if x is not None]
    return round(st.mean(xs), 2) if xs else None


def load_db(root):
    db, ver = {}, {}
    if not os.path.isdir(root):
        return db, ver
    for col in os.listdir(root):
        p = os.path.join(root, col)
        if os.path.isdir(p):
            db[col] = {}
            for f in os.listdir(p):
                if f.endswith(".json"):
                    db[col][f[:-5]] = json.load(open(os.path.join(p, f)))
        elif col.endswith(".versions.txt"):
            c = col[:-len(".versions.txt")]
            ver[c] = {}
            for m in re.finditer(r'"([^"]+)"\s+\d+\s+bytes\s+version\s+(\d+)', open(p).read()):
                ver[c][m.group(1)] = int(m.group(2))
    return db, ver


class Writer:
    def __init__(self, db, ver):
        self.db, self.ver, self.writes, self.missing_version = db, ver, [], []

    def exists(self, col, did):
        return did in self.db.get(col, {})

    def set(self, col, did, data):
        w = {"op": "set", "collection": col, "doc_id": did, "data": data}
        if self.exists(col, did):
            v = self.ver.get(col, {}).get(did)
            if v is None:
                self.missing_version.append(f"{col}/{did}")
                return
            w["if_version"] = v
        self.writes.append(w)

    def update(self, col, did, data):
        if not self.exists(col, did):
            return self.set(col, did, data)
        v = self.ver.get(col, {}).get(did)
        if v is None:
            self.missing_version.append(f"{col}/{did}")
            return
        self.writes.append({"op": "update", "collection": col, "doc_id": did, "data": data, "if_version": v})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--loop", required=True)
    ap.add_argument("--db", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--watch-prompt", default=os.path.join(os.path.dirname(__file__), "loop_watch_prompt.txt"))
    a = ap.parse_args()
    L = json.load(open(a.loop))
    db, ver = load_db(a.db)
    W = Writer(db, ver)
    notes = []

    # ---- meta + channels
    meta = dict(db.get("meta", {}).get("board", {}))
    W.update("meta", "board", {"checked": L["checked"], "source": L["report"], "refreshedAt": NOW, "refreshedBy": "loop daily task",
                               "lastRun": NOW, "rules": L["rules"]})
    for c in L["channels"]:
        W.set("channels", c["key"], {**c, "id": c["key"], "pulledAt": L["checked"]})

    # ---- videos: merge metrics, keep the viewer's fields
    vids = db.get("videos", {})
    new_v, upd_v = 0, 0
    for v in L["videos"]:
        did = v["video_id"]
        fresh = {k: v.get(k) for k in KEEP}
        if did in vids:
            old = vids[did]
            changed = {k: fresh[k] for k in KEEP if old.get(k) != fresh[k]}
            if old.get("topic_type_auto", True) is not False and old.get("topic_type") != v.get("topic_type"):
                changed["topic_type"] = v.get("topic_type"); changed["topic_type_auto"] = True
            if changed:
                changed["snapshotAt"] = L["checked"]
                W.update("videos", did, changed); upd_v += 1
        else:
            d = {**fresh, "id": did, "topic_type": v.get("topic_type"), "topic_type_auto": True, "techniques": [], "hypotheses": [],
                 "verdict": "", "notes": "", "snapshotAt": L["checked"]}
            W.set("videos", did, d); new_v += 1
    notes.append(f"videos: {new_v} new, {upd_v} updated")

    # merged view of videos for evaluations (db + fresh metrics)
    merged = {}
    for did, old in vids.items():
        merged[did] = dict(old)
    for v in L["videos"]:
        m = merged.setdefault(v["video_id"], {"techniques": [], "hypotheses": []})
        for k in KEEP:
            m[k] = v.get(k)
        m.setdefault("techniques", []); m.setdefault("hypotheses", [])

    # ---- hypotheses: autoEval for testing ones
    ready = []
    for hid, h in db.get("hypotheses", {}).items():
        if h.get("status") != "testing":
            continue
        surf = h.get("surface", "shorts-en")
        ch = "bhugol-hi" if surf.endswith("-hi") else "bhugol-en"
        fmt = "long" if surf.startswith("long") else "short"
        pool = [m for m in merged.values() if m.get("channel") == ch and m.get("format") == fmt and m.get("privacy") == "public"]
        tagged = [m for m in pool if hid in (m.get("hypotheses") or [])]
        rest = [m for m in pool if hid not in (m.get("hypotheses") or []) and m.get("v48") is not None]
        ev = {"at": NOW, "n": len(tagged), "nWith48h": len([m for m in tagged if m.get("v48") is not None]),
              "tagged": {"med_v48": median([m.get("v48") for m in tagged]), "med_x_med48": median([m.get("x_med48") for m in tagged]),
                         "avg_pct": mean([m.get("avg_pct") for m in tagged]), "comments_per_1k": median([m.get("comments_per_1k") for m in tagged]),
                         "med_v7d": median([m.get("v7d") for m in tagged])},
              "others": {"n": len(rest), "med_v48": median([m.get("v48") for m in rest]), "avg_pct": mean([m.get("avg_pct") for m in rest]),
                         "comments_per_1k": median([m.get("comments_per_1k") for m in rest])},
              "videos": [m.get("title") for m in tagged][:12]}
        need = h.get("nNeeded") or 0
        rdy = bool(need and ev["nWith48h"] >= need)
        W.update("hypotheses", hid, {"autoEval": ev, "readyForVerdict": rdy})
        if rdy:
            ready.append((hid, h.get("title"), ev))
    notes.append(f"hypotheses evaluated: {sum(1 for h in db.get('hypotheses', {}).values() if h.get('status') == 'testing')}; ready for verdict: {len(ready)}")

    # ---- competitors
    comps_db = db.get("competitors", {})
    pulled = {slug(c["handle"]): c for c in L["competitors"]}
    for cid, c in pulled.items():
        d = {k: v for k, v in c.items() if k != "top_outliers"}
        d.update({"id": cid, "pulledAt": L["checked"]})
        if cid in comps_db:
            old = comps_db[cid]
            if old.get("status") == "queued":
                d["status"] = "active"
            if any(old.get(k) != v for k, v in d.items() if k != "pulledAt"):
                W.update("competitors", cid, d)
        else:
            d.update({"status": "active", "group": c.get("group") or "geo", "addedBy": "ytdeep job", "addedAt": L["checked"], "watch": False, "note": ""})
            W.set("competitors", cid, d)
        for v in c["top_outliers"][:6]:
            body = {**{k: v[k] for k in v if k != "video_id"}, "id": v["video_id"], "pulledAt": L["checked"]}
            old = db.get("comp_videos", {}).get(v["video_id"])
            if old is None or any(old.get(k) != val for k, val in body.items() if k != "pulledAt"):
                W.set("comp_videos", v["video_id"], body)
    # handles for the next pull: every active/queued competitor in the store (+ the pulled ones)
    handles = []
    for cid, c in comps_db.items():
        if c.get("status") in (None, "active", "queued"):
            h = c.get("handle") or c.get("url") or cid
            if h and h not in handles:
                handles.append(h)
    for c in L["competitors"]:
        if c["handle"] not in handles:
            handles.append(c["handle"])
    queued = [c.get("handle") for c in comps_db.values() if c.get("status") == "queued" and slug(c.get("handle") or "") not in pulled]
    if queued:
        notes.append("competitors queued on the board but not in this pull (add to the next ytdeep job): " + ", ".join(queued))

    # ---- watch jobs for competitors flagged watch:true (top 3 outliers each, not yet watched)
    os.makedirs(os.path.join(a.out, "watch_jobs"), exist_ok=True)
    prompt = open(a.watch_prompt).read() if os.path.exists(a.watch_prompt) else None
    watch_made = []
    for cid, c in comps_db.items():
        if not c.get("watch"):
            continue
        src = pulled.get(cid) or {}
        for v in (src.get("top_outliers") or [])[:3]:
            jid = f"loop-{cid[:20]}-{v['video_id']}"
            if os.path.exists(os.path.join("outputs", "watch", jid)) or os.path.exists(os.path.join("jobs", "watch", jid + ".json")):
                continue
            if prompt is None:
                continue
            job = {"id": jid, "url": f"https://www.youtube.com/watch?v={v['video_id']}",
                   "models": ["gemini-3.7-flash", "gemini-3.6-flash", "gemini-3.5-flash", "gemini-flash-latest", "gemini-3-flash-preview"],
                   "media_resolution": "MEDIA_RESOLUTION_LOW",
                   "items": [{"name": "full", "fps": 1, "prompt": prompt.replace("{CONTEXT}", f"{c.get('title') or cid} ({v.get('format')}, {v.get('views')} views, {v.get('x_median')}x the channel median)")}]}
            json.dump(job, open(os.path.join(a.out, "watch_jobs", jid + ".json"), "w"), indent=1)
            watch_made.append(jid)
    if watch_made:
        notes.append(f"watch jobs written: {len(watch_made)} (copy to jobs/watch/ and push)")

    # ---- alerts
    alerts_db = db.get("alerts", {})
    open_by_key = {}
    for aid, al in alerts_db.items():
        if al.get("status") != "closed":
            open_by_key[(al.get("kind"), al.get("channel") or "all")] = aid
    day = L["checked"][:10].replace("-", "")
    fresh_keys = set()
    for al in L["alerts"]:
        key = (al["kind"], al.get("channel") or "all")
        fresh_keys.add(key)
        if key in open_by_key:
            W.update("alerts", open_by_key[key], {"text": al["text"], "ts": L["checked"], "severity": al["severity"], "source": "loop_score " + os.path.basename(os.path.dirname(a.loop))})
        else:
            aid = f"a-{day}-{al['kind']}-{key[1].replace('bhugol-', '')}"
            W.set("alerts", aid, {**al, "id": aid, "status": "open", "ts": L["checked"], "source": "loop_score " + os.path.basename(os.path.dirname(a.loop))})
    for key, aid in open_by_key.items():
        if key not in fresh_keys and key[0] in ("stale_pull", "regime_down", "regime_up", "low_avg_pct_run"):
            W.update("alerts", aid, {"status": "closed", "closedAt": NOW, "closedBy": "loop daily task (condition cleared)"})
    notes.append(f"alerts now open: {len(fresh_keys)}: " + "; ".join(al["text"] for al in L["alerts"]))

    # ---- write batches + summary
    os.makedirs(a.out, exist_ok=True)
    for f in os.listdir(a.out):
        if f.startswith("batch") and f.endswith(".json"):
            os.remove(os.path.join(a.out, f))
    for i in range(0, len(W.writes), 50):
        json.dump(W.writes[i:i + 50], open(os.path.join(a.out, f"batch{i // 50 + 1:02d}.json"), "w"), ensure_ascii=False)
    open(os.path.join(a.out, "competitors.txt"), "w").write("\n".join(handles) + "\n")
    lines = [f"# Loop sync {NOW}", f"pull: {L['checked']} ({L['report']})", f"writes: {len(W.writes)} in {(len(W.writes) + 49) // 50} batch files", ""]
    lines += ["- " + n for n in notes]
    if W.missing_version:
        lines += ["", "MISSING VERSIONS (export these collections with their versions.txt and rerun): " + ", ".join(W.missing_version[:20])]
    if ready:
        lines += ["", "## Hypotheses ready for a verdict (Shubham decides; thresholds are in the card)"]
        for hid, t, ev in ready:
            lines.append(f"- {hid} {t}: n={ev['nWith48h']} tagged, med 48 h {ev['tagged']['med_v48']} (×cohort {ev['tagged']['med_x_med48']}), avg% {ev['tagged']['avg_pct']} vs others med 48 h {ev['others']['med_v48']}, avg% {ev['others']['avg_pct']}")
    wk = [w for w in L["weekly"] if w["format"] == "short"]
    lines += ["", "## Weekly (Shorts)", "| channel | week | n | med 48 h | avg % | eng | subs |", "|---|---|---|---|---|---|---|"]
    for w in wk[-8:]:
        lines.append(f"| {w['channel']} | {w['week']} | {w['n']} | {w['med_v48']} | {w['avg_pct']} | {w['eng_rate']} | {w['subs_gained']} |")
    open(os.path.join(a.out, "summary.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
