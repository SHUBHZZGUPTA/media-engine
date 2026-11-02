#!/usr/bin/env python3
"""Shared Gemini TTS quota log: how many voice requests each key has used today, what is already pushed but not run yet,
and what other projects have reserved. Every chat runs `check` before pushing a jobs/tts job.

Usage (from the repo root, after `git pull`):
  python3 tools/tts_quota.py status [--date YYYY-MM-DD]
  python3 tools/tts_quota.py check jobs/tts/<id>.json --project <name>   (exit 1 = don't push today)
  python3 tools/tts_quota.py reserve <key> <YYYY-MM-DD> <n> <project> [note]   (then commit ops/tts_quota.json)
  python3 tools/tts_quota.py release <key> <YYYY-MM-DD> <project>

Quota is per API key AND per model (10/day each on the free tier; a job's fallback models have their own 10).
Days are Gemini quota days: they reset at midnight Pacific time (13:30 IST from Nov to mid-Mar, 12:30 IST in US summer time). Used = requests found in the outputs/tts/*/report.json versions committed that day (one per finished
item, plus failed attempts that weren't 429s; 429 = rejected, not counted). Pending = job files pushed today whose current
version has no outputs/tts/<id>/.ran marker yet. Limits and reservations live in ops/tts_quota.json.
"""
import json, os, subprocess, sys, datetime as dt
from zoneinfo import ZoneInfo

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CFG = os.path.join(ROOT, "ops", "tts_quota.json")
PT = ZoneInfo("America/Los_Angeles")

def git(*a): return subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True).stdout
def cfg(): return json.load(open(CFG))
def save(c): json.dump(c, open(CFG, "w"), indent=1); print("updated", os.path.relpath(CFG, ROOT), "- commit and push it")
def key_of(job): return job.get("key") or "default"
def first_model(job): return (job.get("models") or ["gemini-3.1-flash-tts-preview"])[0]
def day_window(day):
    s = dt.datetime.combine(day, dt.time(0), PT); return s, s + dt.timedelta(days=1)
def today(): return dt.datetime.now(PT).date()

def requests_in(report):
    """{model: requests} in one report version (quota is per key AND per model)"""
    n = {}
    for it in report.get("items", []):
        if it.get("ok"): n[it.get("model", "?")] = n.get(it.get("model", "?"), 0) + 1
        for a_ in it.get("attempts", []):
            if a_.get("status") not in (429, None): n[a_.get("model", "?")] = n.get(a_.get("model", "?"), 0) + 1
    return n

def used(day):
    """{key: [(requests, job_id, time)]} from report.json versions committed in the quota day."""
    s, e = day_window(day); out = {}
    log = git("log", f"--since={s.isoformat()}", f"--until={e.isoformat()}", "--format=%H %cI", "--name-only", "--", "outputs/tts/*/report.json")
    commit = None
    for ln in log.splitlines():
        if not ln.strip(): continue
        if " " in ln and len(ln.split()[0]) == 40: commit, when = ln.split(); continue
        try: rep = json.loads(git("show", f"{commit}:{ln}"))
        except Exception: continue
        jid = rep.get("job") or ln.split("/")[2]
        jf = os.path.join(ROOT, "jobs", "tts", jid + ".json")
        key = key_of(json.load(open(jf))) if os.path.exists(jf) else "default"
        for model, k in requests_in(rep).items():
            out.setdefault((key, model), []).append((k, jid, when[11:16] + " UTC"))
    return out

def pending():
    """job files whose current version hasn't run yet: {key: [(items, path)]}"""
    out = {}
    for f in sorted(set(git("log", "--since=2 days ago", "--name-only", "--format=", "--", "jobs/tts/*.json").split())):
        p = os.path.join(ROOT, f)
        if not os.path.exists(p): continue
        try: job = json.load(open(p))
        except Exception: continue
        jid = job.get("id") or os.path.basename(f)[:-5]
        want = git("log", "-1", "--format=%H", "--", f).strip()
        done = open(os.path.join(ROOT, "outputs", "tts", jid, ".ran")).read().strip() if os.path.exists(os.path.join(ROOT, "outputs", "tts", jid, ".ran")) else ""
        if want != done: out.setdefault((key_of(job), first_model(job)), []).append((len(job.get("items", [])), f))
    return out

def summary(day, key, project=None):
    """key = (api key name, model)"""
    c = cfg(); lim = c["limits"].get(key[1], 10)
    u = sum(n for n, _, _ in used(day).get(key, []))
    pd = sum(n for n, _ in pending().get(key, [])) if day == today() else 0
    res = [r for r in c.get("reservations", []) if r["key"] == key[0] and r.get("model", "gemini-3.1-flash-tts-preview") == key[1] and r["date"] == day.isoformat()]
    held = sum(r["n"] for r in res if r["project"] != project)
    return lim, u, pd, res, held, lim - u - pd - held

def status(day):
    c = cfg(); U = used(day); P = pending() if day == today() else {}
    print(f"Gemini TTS quota day {day} (resets midnight Pacific)\n")
    keys = set(U) | set(P) | {(r["key"], r.get("model", "gemini-3.1-flash-tts-preview")) for r in c.get("reservations", []) if r["date"] == day.isoformat()}
    for key in sorted(keys | {("longform", "gemini-3.1-flash-tts-preview"), ("default", "gemini-3.1-flash-tts-preview")}):
        lim, u, pd, res, held, free = summary(day, key)
        print(f"[{key[0]} key / {key[1]}] limit {lim} | used {u} | pushed, not run yet {pd} | reserved {held} | FREE {free}")
        for n, jid, when in U.get(key, []): print(f"    used     {n:2d}  {jid}  ({when})")
        for n, f in P.get(key, []): print(f"    pending  {n:2d}  {f}")
        for r in res: print(f"    reserved {r['n']:2d}  {r['project']}  {r.get('note', '')}")
    print("\nNote:", c.get("note", ""))

def check(path, project):
    job = json.load(open(path)); key = (key_of(job), first_model(job)); need = len(job.get("items", [])); day = today()
    lim, u, pd, res, held, free = summary(day, key, project)
    mine = next((r for r in res if r["project"] == project), None)
    own_pd = sum(n for n, f in pending().get(key, []) if os.path.abspath(os.path.join(ROOT, f)) == os.path.abspath(path))
    free += own_pd   # this job itself may already be counted as pending
    print(f"[{key[0]} key / {key[1]}] {day}: this job needs {need}; limit {lim}, used {u}, pending {pd - own_pd}, held by other projects {held} -> free {free}"
          + (f"; your reservation {mine['n']}" if mine else ""))
    if need > free:
        print("DON'T PUSH TODAY: not enough requests left. Run `tts_quota.py status`, split the job, or reserve a later day."); sys.exit(1)
    print("OK to push.")

def reserve(key, date, n, project, note=""):
    c = cfg(); rs = c.setdefault("reservations", [])
    rs[:] = [r for r in rs if not (r["key"] == key and r["date"] == date and r["project"] == project)]
    rs.append({"key": key, "date": date, "n": int(n), "project": project, "note": note})
    old = (today() - dt.timedelta(days=7)).isoformat(); rs[:] = [r for r in rs if r["date"] >= old]
    rs.sort(key=lambda r: (r["date"], r["key"], r["project"])); save(c)

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "status":
        d = next((a[i + 1] for i, x in enumerate(a) if x == "--date"), None)
        status(dt.date.fromisoformat(d) if d else today())
    elif a[0] == "check":
        check(a[1], next((a[i + 1] for i, x in enumerate(a) if x == "--project"), None))
    elif a[0] == "reserve": reserve(*a[1:6])
    elif a[0] == "release":
        c = cfg(); c["reservations"] = [r for r in c.get("reservations", []) if not (r["key"] == a[1] and r["date"] == a[2] and r["project"] == a[3])]; save(c)
    else: print(__doc__); sys.exit(2)
