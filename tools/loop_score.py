#!/usr/bin/env python3
"""loop_score.py — turn a ytdeep report into the BHUGOL Learning Loop records.

Usage:
    python3 tools/loop_score.py outputs/ytdeep/<id>/report.json [--out outputs/loop/<id>/loop.json]
                                [--prev outputs/loop/<prev>/loop.json]

Reads one ytdeep report (own channels with per-video analytics + competitor public data) and writes
one JSON with age-matched, comparable numbers:

  videos[]      own videos: views at 24 h / 48 h / 7 d from the daily series (null when the video is
                too young for that window), avg % viewed, engaged-view rate, traffic shares, retention
                shape, ×-median at 48 h against the channel's trailing 28-day cohort, auto topic type.
  weekly[]      per channel + format, ISO week: n, median 48 h views, median 7 d, avg %, engaged rate,
                subs gained, feed share.  Only videos old enough for each window are counted.
  alerts[]      regime changes (last 6 Shorts' 48 h median vs the prior 14 days), low/high avg % runs,
                stale pull.
  competitors[] each peer: age, views/day, subs per 1K views, class (big / young-exploding / peer /
                small), Shorts + long medians over its last uploads, timing habits (hour IST, weekday),
                description + tag habits, top outliers (×median).
  comp_videos[] every competitor video with ×median, title/description/tag features.

All numbers are from the report; nothing here is estimated.  Thresholds are listed in `rules` so a
reader can see what "young-exploding" or "regime change" means.
"""
import argparse, collections, datetime as dt, json, math, os, re, statistics as st, sys

IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
SHORT_MAX_S = 180

RULES = {
    "short_max_s": SHORT_MAX_S,
    "window_h": {"v24": 24, "v48": 48, "v7d": 168},
    "age_needed_h": {"v24": 36, "v48": 72, "v7d": 192},
    "x_med48_cohort_days": 28,
    "regime": {"recent_n": 6, "prior_days": 14, "down_ratio": 0.5, "up_ratio": 2.0},
    "avg_pct_low": 55, "avg_pct_high": 75,
    "competitor_class": {
        "big_subs": 250_000,
        "big_views_per_day": 200_000,
        "young_max_age_days": 540,
        "exploding_views_per_day": 20_000,
        "exploding_recent_median": 100_000,
        "exploding_min_subs": 5_000,
        "small_subs": 5_000,
    },
    "stale_pull_h": 36,
}

TOPIC_RULES = [
    ("news/pop", r"\b(black friday|halloween|pumpkin|f1|nasa|aliens?|diwali|christmas|new year|cop\d+|casino|police|burns? a man)\b"),
    ("nature event", r"\b(volcano|erupts?|waves?|quake|earthquake|storm|hurricane|tsunami|iceberg|snowfall|rain(ed)?)\b"),
    ("record journey", r"\b(walk|on foot|drive|cross(ed|ing)?|journey|longest road|fastest)\b"),
    ("border/enclave", r"\b(borders?|enclave|exclave|boundary|one line|neighbou?rs?|inside a country|invisible|cheated on coastline)\b"),
    ("extreme place", r"\b(deepest|driest|coldest|hottest|loneliest|closest|farthest|remote|never rain|million years)\b"),
    ("facts list", r"\b(\d+ facts|top \d|\d+ countries|facts that)\b"),
    ("size/scale", r"\b(size|bigger|smaller|small|empty|largest|biggest|tallest|half of|40%|size of|south of)\b"),
    ("history deal", r"\b(bought|sold|deal|treaty|history|didn't exist|until \d{4}|\b1[5-9]\d\d\b)\b"),
    ("name confusion", r"\b(not a country|vs\.?|difference|isn't|is not|secret(ly)?|actually|fake)\b"),
    ("space/science", r"\b(stars|twinkle|another earth|moon|planet|orbit|gps|satellite|space)\b"),
]


def parse_ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def median(xs):
    xs = [x for x in xs if x is not None]
    return st.median(xs) if xs else None


def mean(xs):
    xs = [x for x in xs if x is not None]
    return round(st.mean(xs), 2) if xs else None


def topic_type(title):
    t = (title or "").lower()
    for name, rx in TOPIC_RULES:
        if re.search(rx, t):
            return name
    return "other"


def title_features(title):
    t = title or ""
    emoji_n = len(re.findall(r"[\U0001F300-\U0001FAFF☀-➿\U0001F1E6-\U0001F1FF]", t))
    return {
        "title_len": len(t),
        "has_number": bool(re.search(r"\d", t)),
        "has_question": "?" in t,
        "emoji_n": emoji_n,
        "caps_words": len([w for w in re.findall(r"\b[A-Z]{3,}\b", t)]),
        "hashtags_in_title": len(re.findall(r"#\w+", t)),
    }


def desc_features(desc):
    d = desc or ""
    return {
        "desc_len": len(d),
        "desc_links": len(re.findall(r"https?://", d)),
        "desc_hashtags": len(re.findall(r"#\w+", d)),
        "desc_lines": len([l for l in d.splitlines() if l.strip()]),
        "desc_first_line": (d.strip().splitlines() or [""])[0][:120],
    }


def retention_shape(ret):
    """ret = [[ratio, audienceWatchRatio, relativeRetentionPerformance], ...] (100 pts)."""
    if not ret:
        return None
    pts = {round(r[0], 2): r[1] for r in ret}
    def at(x):
        v = pts.get(x)
        return round(v, 3) if v is not None else None
    # biggest drop over any 5-point span
    seq = sorted(pts.items())
    worst, worst_at = 0.0, None
    for i in range(len(seq) - 5):
        drop = seq[i][1] - seq[i + 5][1]
        if drop > worst:
            worst, worst_at = drop, seq[i][0]
    rel = [r[2] for r in ret if len(r) > 2 and r[2] is not None]
    return {
        "at10": at(0.10), "at30": at(0.30), "at50": at(0.50), "at90": at(0.90), "end": at(1.0),
        "hook_loss": round(1 - pts.get(0.10, 1), 3) if 0.10 in pts else None,
        "biggest_drop": round(worst, 3), "biggest_drop_at": worst_at,
        "rel_mean": round(st.mean(rel), 3) if rel else None,
    }


def own_video(v, ch_key, checked):
    pub = parse_ts(v["published"])
    age_h = (checked - pub).total_seconds() / 3600
    daily = v.get("daily") or []
    def win(days, need_h):
        if age_h < need_h or not daily:
            return None
        return sum(x[1] for x in daily[:days])
    traffic = v.get("traffic") or {}
    tot = sum(traffic.values()) or 0
    def share(k):
        return round(100 * traffic.get(k, 0) / tot, 1) if tot else None
    dur = v.get("duration_s") or 0
    views = v.get("views") or 0
    eng = v.get("a_engagedViews")
    rec = {
        "video_id": v["video_id"], "channel": ch_key, "title": v.get("title"),
        "published": v["published"], "published_ist": pub.astimezone(IST).strftime("%Y-%m-%d %H:%M"),
        "upload_hour_ist": pub.astimezone(IST).hour, "upload_dow": pub.astimezone(IST).strftime("%a"),
        "format": "short" if dur and dur <= SHORT_MAX_S else "long", "duration_s": dur,
        "privacy": v.get("privacy"), "age_h": round(age_h, 1),
        "views": views, "likes": v.get("likes"), "comments": v.get("comments"),
        "avg_pct": v.get("a_averageViewPercentage"), "avg_dur_s": v.get("a_averageViewDuration"),
        "engaged": eng, "eng_rate": round(eng / views, 3) if eng and views else None,
        "likes_per_1k": round(1000 * (v.get("likes") or 0) / views, 1) if views else None,
        "comments_per_1k": round(1000 * (v.get("comments") or 0) / views, 2) if views else None,
        "subs_gained": v.get("a_subscribersGained"), "shares": v.get("a_shares"),
        "v24": win(1, RULES["age_needed_h"]["v24"]), "v48": win(2, RULES["age_needed_h"]["v48"]),
        "v7d": win(7, RULES["age_needed_h"]["v7d"]),
        "feed_share": share("SHORTS"), "search_share": share("YT_SEARCH"),
        "browse_share": round(sum(share(k) or 0 for k in ("BROWSE", "YT_CHANNEL", "SUBSCRIBER")), 1) if tot else None,
        "retention": retention_shape(v.get("retention")),
        "topic_type": topic_type(v.get("title")), "topic_type_auto": True,
        "tags_n": len(v.get("tags") or []), "thumb_url": v.get("thumb_url"),
    }
    rec.update(title_features(v.get("title")))
    rec.update(desc_features(v.get("description")))
    return rec


def add_x_med48(videos, checked):
    """×-median at 48 h against the same channel+format cohort published in the prior 28 days."""
    by = collections.defaultdict(list)
    for v in videos:
        if v["v48"] is not None and v["privacy"] == "public":
            by[(v["channel"], v["format"])].append(v)
    for v in videos:
        v["x_med48"] = None
        v["cohort_med48"] = None
        if v["v48"] is None:
            continue
        pub = parse_ts(v["published"])
        lo = pub - dt.timedelta(days=RULES["x_med48_cohort_days"])
        cohort = [c["v48"] for c in by[(v["channel"], v["format"])]
                  if c["video_id"] != v["video_id"] and lo <= parse_ts(c["published"]) < pub]
        if len(cohort) >= 3:
            m = st.median(cohort)
            v["cohort_med48"] = m
            v["x_med48"] = round(v["v48"] / m, 2) if m else None


def weekly(videos):
    out = []
    groups = collections.defaultdict(list)
    for v in videos:
        if v["privacy"] != "public":
            continue
        iso = parse_ts(v["published"]).isocalendar()
        groups[(v["channel"], v["format"], f"{iso[0]}-W{iso[1]:02d}")].append(v)
    for (ch, fmt, wk), g in sorted(groups.items()):
        out.append({
            "channel": ch, "format": fmt, "week": wk, "n": len(g),
            "med_v48": median([x["v48"] for x in g]), "n_v48": len([x for x in g if x["v48"] is not None]),
            "med_v7d": median([x["v7d"] for x in g]), "n_v7d": len([x for x in g if x["v7d"] is not None]),
            "med_views": median([x["views"] for x in g]),
            "avg_pct": mean([x["avg_pct"] for x in g]),
            "eng_rate": mean([x["eng_rate"] for x in g]),
            "subs_gained": sum(x["subs_gained"] or 0 for x in g),
            "feed_share": mean([x["feed_share"] for x in g]),
            "likes_per_1k": mean([x["likes_per_1k"] for x in g]),
        })
    return out


def alerts(videos, checked, report_checked):
    out = []
    age_pull_h = (dt.datetime.now(dt.timezone.utc) - report_checked).total_seconds() / 3600
    if age_pull_h > RULES["stale_pull_h"]:
        out.append({"kind": "stale_pull", "severity": "warn",
                    "text": f"Analytics pull is {age_pull_h:.0f} h old (threshold {RULES['stale_pull_h']} h). Push a jobs/ytdeep job."})
    R = RULES["regime"]
    for ch in sorted({v["channel"] for v in videos}):
        shorts = sorted([v for v in videos if v["channel"] == ch and v["format"] == "short"
                         and v["privacy"] == "public" and v["v48"] is not None],
                        key=lambda v: v["published"])
        if len(shorts) < R["recent_n"] + 3:
            continue
        recent = shorts[-R["recent_n"]:]
        start_recent = parse_ts(recent[0]["published"])
        prior = [v for v in shorts[:-R["recent_n"]]
                 if start_recent - dt.timedelta(days=R["prior_days"]) <= parse_ts(v["published"]) < start_recent]
        if len(prior) < 3:
            continue
        mr, mp = st.median([v["v48"] for v in recent]), st.median([v["v48"] for v in prior])
        ratio = mr / mp if mp else None
        if ratio is not None and ratio < R["down_ratio"]:
            out.append({"kind": "regime_down", "severity": "high", "channel": ch,
                        "text": f"{ch}: last {len(recent)} Shorts median {mr:.0f} views at 48 h vs {mp:.0f} in the prior {R['prior_days']} days ({ratio:.2f}×). Feed seeding dropped.",
                        "recent": [v["video_id"] for v in recent]})
        elif ratio is not None and ratio > R["up_ratio"]:
            out.append({"kind": "regime_up", "severity": "info", "channel": ch,
                        "text": f"{ch}: last {len(recent)} Shorts median {mr:.0f} at 48 h vs {mp:.0f} prior ({ratio:.2f}×). Feed seeding up.",
                        "recent": [v["video_id"] for v in recent]})
        low = [v for v in recent if v["avg_pct"] is not None and v["avg_pct"] < RULES["avg_pct_low"]]
        if len(low) >= 3:
            out.append({"kind": "low_avg_pct_run", "severity": "warn", "channel": ch,
                        "text": f"{ch}: {len(low)} of the last {len(recent)} Shorts under {RULES['avg_pct_low']}% average viewed: " +
                                "; ".join(f"{v['title'][:40]} ({v['avg_pct']:.0f}%)" for v in low),
                        "videos": [v["video_id"] for v in low]})
    return out


def comp_video(c, v, checked, med_short, med_long):
    pub = parse_ts(v["published"])
    dur = v.get("duration_s") or 0
    fmt = "short" if dur and dur <= SHORT_MAX_S else "long"
    med = med_short if fmt == "short" else med_long
    views = v.get("views") or 0
    age_d = max((checked - pub).total_seconds() / 86400, 0.1)
    rec = {
        "channel": c["handle"], "channel_title": c["title"], "video_id": v["video_id"], "title": v.get("title"),
        "published": v["published"], "upload_hour_ist": pub.astimezone(IST).hour,
        "upload_dow": pub.astimezone(IST).strftime("%a"), "format": fmt, "duration_s": dur,
        "views": views, "likes": v.get("likes"), "comments": v.get("comments"), "age_d": round(age_d, 1),
        "views_per_day": round(views / age_d), "x_median": round(views / med, 2) if med else None,
        "tags_n": len(v.get("tags") or []), "topic_type": topic_type(v.get("title")), "topic_type_auto": True,
        "thumb_url": v.get("thumb_url"),
    }
    rec.update(title_features(v.get("title")))
    rec.update(desc_features(v.get("description")))
    return rec


def competitor(c, checked):
    vids = c.get("videos") or []
    shorts = [v for v in vids if (v.get("duration_s") or 0) <= SHORT_MAX_S and v.get("duration_s")]
    longs = [v for v in vids if (v.get("duration_s") or 0) > SHORT_MAX_S]
    med_s = median([v.get("views") for v in shorts])
    med_l = median([v.get("views") for v in longs])
    created = parse_ts(c["created"]) if c.get("created") else None
    age_d = (checked - created).total_seconds() / 86400 if created else None
    subs, views = c.get("subscribers") or 0, c.get("views") or 0
    vpd = round(views / age_d) if age_d else None
    K = RULES["competitor_class"]
    recent_med = median([v.get("views") for v in vids])
    young = age_d is not None and age_d <= K["young_max_age_days"]
    exploding = (vpd or 0) >= K["exploding_views_per_day"] or (recent_med or 0) >= K["exploding_recent_median"]
    if young and exploding and subs >= K["exploding_min_subs"]:
        klass = "young-exploding"          # young channels that explode outrank "big": they are the ones to copy
    elif subs >= K["big_subs"] or (vpd or 0) >= K["big_views_per_day"]:
        klass = "big"
    elif young:
        klass = "young"
    elif subs < K["small_subs"]:
        klass = "small"
    else:
        klass = "peer"
    cv = [comp_video(c, v, checked, med_s, med_l) for v in vids]
    hours = collections.Counter(v["upload_hour_ist"] for v in cv)
    dows = collections.Counter(v["upload_dow"] for v in cv)
    span_d = None
    if vids:
        pubs = sorted(parse_ts(v["published"]) for v in vids)
        span_d = max((pubs[-1] - pubs[0]).total_seconds() / 86400, 1)
    return {
        "handle": c["handle"], "id": c.get("id"), "title": c.get("title"), "group": c.get("group"),
        "country": c.get("country"), "created": c.get("created"), "age_days": round(age_d) if age_d else None,
        "subscribers": subs, "views": views, "video_count": c.get("video_count"),
        "views_per_day_lifetime": vpd, "subs_per_1k_views": round(1000 * subs / views, 2) if views else None,
        "class": klass, "n_pulled": len(vids), "n_shorts": len(shorts), "n_long": len(longs),
        "shorts_median": med_s, "long_median": med_l, "recent_median": recent_med,
        "uploads_per_week": round(7 * len(vids) / span_d, 1) if span_d else None,
        "top_hours_ist": [h for h, _ in hours.most_common(3)], "top_dows": [d for d, _ in dows.most_common(3)],
        "median_duration_s": median([v.get("duration_s") for v in vids]),
        "median_tags": median([v["tags_n"] for v in cv]),
        "median_desc_len": median([v["desc_len"] for v in cv]),
        "desc_link_share": round(100 * sum(1 for v in cv if v["desc_links"]) / len(cv)) if cv else None,
        "median_title_len": median([v["title_len"] for v in cv]),
        "likes_per_1k": median([1000 * (v["likes"] or 0) / v["views"] for v in cv if v["views"]]),
        "title_question_share": round(100 * sum(1 for v in cv if v["has_question"]) / len(cv)) if cv else None,
        "title_number_share": round(100 * sum(1 for v in cv if v["has_number"]) / len(cv)) if cv else None,
        "title_emoji_share": round(100 * sum(1 for v in cv if v["emoji_n"]) / len(cv)) if cv else None,
        "top_outliers": sorted([v for v in cv if v["x_median"]], key=lambda v: -v["x_median"])[:8],
        "topic_mix": dict(collections.Counter(v["topic_type"] for v in cv).most_common()),
    }, cv


def channel_key(ch):
    h = (ch.get("handle") or ch.get("title") or "").lower()
    if "hindi" in h:
        return "bhugol-hi"
    if "bhugol" in h:
        return "bhugol-en"
    return h.strip("@") or ch.get("id")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    ap.add_argument("--out")
    ap.add_argument("--prev", help="previous loop.json (unused for now; reserved for deltas)")
    a = ap.parse_args()
    r = json.load(open(a.report))
    checked = parse_ts(r["checked"])
    videos, chans = [], []
    for ch in r.get("channels", []):
        key = channel_key(ch)
        aud = ch.get("audience") or {}
        ctry = aud.get("country") or []
        tot = sum(c.get("views", 0) for c in ctry) or 1
        chans.append({
            "key": key, "id": ch.get("id"), "handle": ch.get("handle"), "title": ch.get("title"), "created": ch.get("created"),
            "age_days": round((checked - parse_ts(ch["created"])).total_seconds() / 86400) if ch.get("created") else None,
            "subscribers": ch.get("subscribers"), "views": ch.get("views"), "video_count": ch.get("video_count"),
            "countries": [{"c": c["country"], "share": round(100 * c["views"] / tot, 1),
                           "avg_pct": c.get("averageViewPercentage")} for c in ctry[:6]],
            "traffic": {t["insightTrafficSourceType"]: t["views"] for t in (aud.get("traffic") or [])},
            "search_terms": [(s.get("insightTrafficSourceDetail"), s.get("views")) for s in (aud.get("search_terms") or [])[:10]],
            "content_type": aud.get("content_type"),
        })
        for v in ch.get("videos", []):
            if v.get("published"):
                videos.append(own_video(v, key, checked))
    add_x_med48(videos, checked)
    comps, comp_videos = [], []
    for c in r.get("competitors", []):
        rec, cv = competitor(c, checked)
        comps.append(rec)
        comp_videos.extend(cv)
    out = {
        "generated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "report": a.report, "checked": r["checked"], "rules": RULES,
        "channels": chans, "videos": videos, "weekly": weekly(videos),
        "alerts": alerts(videos, checked, checked), "competitors": comps, "comp_videos": comp_videos,
    }
    path = a.out or os.path.join("outputs", "loop", os.path.basename(os.path.dirname(a.report)), "loop.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(out, open(path, "w"), indent=1, ensure_ascii=False)
    # console summary
    print(f"loop.json → {path}")
    for w in out["weekly"]:
        if w["format"] == "short":
            print(f"  {w['channel']:10} {w['week']} n={w['n']:>2} med48={w['med_v48'] if w['med_v48'] is not None else '-':>6} "
                  f"avg%={w['avg_pct'] if w['avg_pct'] is not None else '-':>5} eng={w['eng_rate'] if w['eng_rate'] is not None else '-':>5} subs={w['subs_gained']}")
    for al in out["alerts"]:
        print("  ALERT", al["severity"], al["text"])
    for c in comps:
        print(f"  comp {c['handle']:28} {c['class']:16} subs={c['subscribers']:>9} age={c['age_days']}d vpd={c['views_per_day_lifetime']} shorts_med={c['shorts_median']} long_med={c['long_median']}")


if __name__ == "__main__":
    main()
