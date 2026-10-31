#!/usr/bin/env python3
"""Run a GPU job on Kaggle from a job file and save what it produces.

Usage:
  python3 tools/kaggle_run.py jobs/kaggle/<id>.json            start the run and wait for it
  python3 tools/kaggle_run.py jobs/kaggle/<id>.json --collect  fetch results of a run left going
  python3 tools/kaggle_run.py jobs/kaggle/<id>.json --status   one quick status check, no waiting
  python3 tools/kaggle_run.py jobs/kaggle/<id>.json --dry-run  show what would be sent, no login

Job file fields:
  id               short name; used for the private Kaggle notebook and outputs/kaggle/<id>/
  script           path in this repo to the Python script that Kaggle runs
  accelerator      "NvidiaTeslaT4" (default), "NvidiaTeslaP100" or "none"
  internet         true (default); needed to download models
  timeout_minutes  hard limit for the run on Kaggle (default 60; Kaggle caps sessions at 12 h)
  wait_minutes     how long to wait here before leaving the run going (default 60)
  datasets, models, kernels  optional lists of Kaggle sources to attach ("owner/slug")
  params           optional settings for the script, readable there as json.loads(JOB_PARAMS)
  stage            optional {from_kernel, file_pattern, dataset_slug, title}: before the run, copy
                   matching files from an earlier notebook's output into a private Kaggle dataset on
                   the same account and attach it (outputs of a notebook that ended in an error
                   can't be attached directly). With {repo_paths: [...], dataset_slug, title} instead,
                   the listed files from this repo are uploaded (e.g. a built project as .tar.gz)

Credentials: KAGGLE_API_TOKEN, or KAGGLE_USERNAME + KAGGLE_KEY. They are never printed.
"""
import argparse
import json
import os
import re
import shutil
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FINAL = {"COMPLETE", "ERROR", "CANCEL_REQUESTED", "CANCEL_ACKNOWLEDGED"}
POLL_SECONDS = 30


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_job(path):
    job = json.loads(Path(path).read_text(encoding="utf-8"))
    for key in ("id", "script"):
        if key not in job:
            sys.exit(f"{path}: job file is missing '{key}'")
    return job


def slug_for(job_id):
    return "me-" + re.sub(r"[^a-z0-9]+", "-", job_id.lower()).strip("-")


def build_folder(job, user, folder):
    script = ROOT / job["script"]
    if not script.is_file():
        sys.exit(f"script not found: {job['script']}")
    code = script.read_text(encoding="utf-8")
    if "params" in job:
        # Kaggle runs a single file, so the job's params are written into its first line.
        code = f"JOB_PARAMS = {json.dumps(job['params'])!r}\n" + code
    (folder / script.name).write_text(code, encoding="utf-8")
    slug = slug_for(job["id"])
    acc = job.get("accelerator", "NvidiaTeslaT4")
    meta = {
        "id": f"{user}/{slug}",
        "title": slug,
        "code_file": script.name,
        "language": "python",
        "kernel_type": "script",
        "is_private": True,
        "enable_gpu": acc.lower() != "none",
        "enable_internet": bool(job.get("internet", True)),
        "dataset_sources": job.get("datasets", []),
        "competition_sources": [],
        "kernel_sources": job.get("kernels", []),
        "model_sources": job.get("models", []),
    }
    (folder / "kernel-metadata.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    return meta, (None if acc.lower() == "none" else acc)


def login():
    for var in ("KAGGLE_API_TOKEN", "KAGGLE_USERNAME", "KAGGLE_KEY"):
        if os.environ.get(var, "") == "":
            os.environ.pop(var, None)
    has_token = "KAGGLE_API_TOKEN" in os.environ
    has_legacy = "KAGGLE_USERNAME" in os.environ and "KAGGLE_KEY" in os.environ
    if not (has_token or has_legacy):
        sys.exit("No Kaggle credentials. Add the KAGGLE_API_TOKEN secret in the repo's "
                 "Settings > Secrets and variables > Actions.")
    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi()
    api.authenticate()
    user = api.config_values.get("username")
    if not user:
        sys.exit("Kaggle accepted no username for these credentials; generate a new token.")
    return api, user


def gpu_quota(api):
    try:
        q = api.quota_view().gpu_quota
        used = q.time_used.total_seconds() / 3600
        total = q.total_time_allowed.total_seconds() / 3600
        return {"used_h": round(used, 2), "remaining_h": round(max(0.0, total - used), 2),
                "total_h": round(total, 2)}
    except Exception as e:  # quota is informational only
        return {"error": type(e).__name__}


def stage_files(api, user, stage, diag):
    """Copy files from an earlier notebook's output into a private dataset on this account and
    return the dataset ref to attach. Progress and errors are recorded in diag."""
    ref = f"{user}/{stage['dataset_slug']}"
    with tempfile.TemporaryDirectory() as dl, tempfile.TemporaryDirectory() as folder:
        if stage.get("repo_paths"):
            # files from this repo (e.g. a built project packed as .tar.gz) instead of a notebook's output
            files = [str(ROOT / p) for p in stage["repo_paths"]]
            missing = [p for p, f in zip(stage["repo_paths"], files) if not os.path.isfile(f)]
            if missing:
                raise RuntimeError(f"repo_paths not found: {missing}")
            diag["bundled"] = [{"file": os.path.basename(f), "mb": round(os.path.getsize(f) / 1e6, 1)}
                               for f in files]
            for f in files:
                shutil.copy(f, os.path.join(folder, os.path.basename(f)))
        else:
            files, token = [], None
            while True:
                got, token = api.kernels_output(stage["from_kernel"], path=dl, file_pattern=stage["file_pattern"],
                                                force=True, quiet=True, page_token=token, page_size=200)
                files += got or []
                if not token:
                    break
            pat = re.compile(stage["file_pattern"])
            files = [f for f in files if os.path.isfile(f) and pat.search(os.path.basename(f))]
            diag["downloaded"] = [{"file": os.path.basename(f), "mb": round(os.path.getsize(f) / 1e6, 1)}
                                  for f in files]
            if not files:
                raise RuntimeError(f"nothing in {stage['from_kernel']} matched {stage['file_pattern']}")
            for f in files:
                shutil.move(f, os.path.join(folder, os.path.basename(f)))
        try:
            api.dataset_status(ref)
            exists = True
        except Exception:
            exists = False
        version_before = 0
        if exists:
            try:
                version_before = int(json.loads(api.dataset_status(ref, format="json(current_version_number)"))
                                     .get("current_version_number") or 0)
            except Exception:
                version_before = 0
        diag["version_before"] = version_before
        diag["create"] = []
        for license_name in ("other", "unknown"):  # private dataset; Kaggle still requires a license
            meta = {"title": stage.get("title", stage["dataset_slug"]), "id": ref,
                    "licenses": [{"name": license_name}]}
            with open(os.path.join(folder, "dataset-metadata.json"), "w") as fh:
                json.dump(meta, fh)
            if exists:
                resp = api.dataset_create_version(folder, "staged from " + stage.get("from_kernel", "repo files"),
                                                  quiet=True)
            else:
                resp = api.dataset_create_new(folder, public=False, quiet=True)
            err = getattr(resp, "error", None)
            diag["create"].append({"license": license_name, "existed": exists, "error": err,
                                   "status": str(getattr(resp, "status", ""))})
            if not err or "license" not in err.lower():
                break
        if err:
            raise RuntimeError(f"Kaggle refused the dataset: {err}")
    print(f"[{now()}] staged {len(files)} file(s) into private dataset {ref}", flush=True)
    deadline = time.time() + 900
    seen = []
    while time.time() < deadline:
        try:
            info = json.loads(api.dataset_status(ref, format="json(status,current_version_number)"))
            version = int(info.get("current_version_number") or 0)
            st = f"{str(info.get('status', '')).lower()} (version {version})"
        except Exception as e:
            version, st = 0, f"lookup failed: {type(e).__name__}: {e}"[:200]
        if not seen or seen[-1] != st:
            seen.append(st)
            diag["statuses"] = seen
        # a new upload is only usable once its own version is ready, not the previous one
        if st.startswith("ready") and version > version_before:
            diag["version_ready"] = version
            return ref, [os.path.basename(f) for f in files]
        time.sleep(15)
    raise RuntimeError(f"dataset {ref} was not ready after 15 minutes (statuses seen: {seen})")


def wait_for(api, ref, minutes):
    deadline = time.time() + minutes * 60
    last = None
    while True:
        st = api.kernels_status(ref)
        name = st.status.name if hasattr(st.status, "name") else str(st.status)
        if name != last:
            print(f"[{now()}] {ref}: {name}", flush=True)
            last = name
        if name in FINAL:
            return name, (st.failure_message or "")
        if time.time() > deadline:
            return name, ""
        time.sleep(POLL_SECONDS)


MAX_REPO_FILE_MB = 40


def download(api, ref, outdir):
    """Download a run's outputs. Files over MAX_REPO_FILE_MB (e.g. LoRA weights) are not kept
    in the repo: they stay in the Kaggle notebook's output, where later jobs can attach them."""
    outdir.mkdir(parents=True, exist_ok=True)
    files, kept_on_kaggle, token = [], [], None
    while True:
        got, token = api.kernels_output(ref, path=str(outdir), force=True, quiet=True,
                                        page_token=token, page_size=200)
        files += got or []
        if not token:
            break
    for f in list(files):
        if os.path.isfile(f) and os.path.getsize(f) > MAX_REPO_FILE_MB * 1e6:
            kept_on_kaggle.append({"file": os.path.relpath(f, outdir),
                                   "mb": round(os.path.getsize(f) / 1e6, 1)})
            os.remove(f)
            files.remove(f)
    return files, kept_on_kaggle


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("job")
    ap.add_argument("--collect", action="store_true")
    ap.add_argument("--status", action="store_true", help="one status check without waiting")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    job = load_job(args.job)
    outdir = ROOT / "outputs" / "kaggle" / job["id"]

    if args.dry_run:
        with tempfile.TemporaryDirectory() as tmp:
            meta, acc = build_folder(job, "YOUR_KAGGLE_USERNAME", Path(tmp))
            print(json.dumps({"accelerator": acc, "metadata": meta}, indent=1))
        return 0

    api, user = login()
    ref = f"{user}/{slug_for(job['id'])}"
    record = {"job": job["id"], "kernel": ref, "url": f"https://www.kaggle.com/code/{ref}",
              "gpu_quota_before": gpu_quota(api)}
    if args.status:
        args.collect = True
    if args.collect and (outdir / "run.json").exists():
        # keep what the original run recorded (push time, version, accelerator)
        previous = json.loads((outdir / "run.json").read_text(encoding="utf-8"))
        record = {**previous, "gpu_quota_now": record["gpu_quota_before"],
                  **{k: record[k] for k in ("job", "kernel", "url")}}

    if not args.collect:
        if job.get("stage"):
            diag = {}
            try:
                ds_ref, staged = stage_files(api, user, job["stage"], diag)
            except Exception as e:
                record.update(status="STAGE_FAILED", stage_error=f"{type(e).__name__}: {e}"[:1000],
                              stage_diag=diag, checked_at=now())
                outdir.mkdir(parents=True, exist_ok=True)
                (outdir / "run.json").write_text(json.dumps(record, indent=1), encoding="utf-8")
                print(json.dumps(record, indent=1))
                return 1
            job["datasets"] = list(dict.fromkeys(job.get("datasets", []) + [ds_ref]))
            record.update(staged_dataset=ds_ref, staged_files=staged, stage_diag=diag)
        with tempfile.TemporaryDirectory() as tmp:
            meta, acc = build_folder(job, user, Path(tmp))
            timeout_s = int(job.get("timeout_minutes", 60)) * 60
            resp = api.kernels_push(tmp, timeout=str(timeout_s), acc=acc)
            err = getattr(resp, "error", None)
            if err:
                sys.exit(f"Kaggle refused the push: {err}")
            record.update(pushed_at=now(), accelerator=acc,
                          version=getattr(resp, "version_number", None))
            print(f"[{now()}] pushed {ref} (version {record['version']}) on {acc}", flush=True)

    status, failure = wait_for(api, ref, 0 if args.status else int(job.get("wait_minutes", 60)))
    record.update(status=status, checked_at=now())
    if failure:
        record["failure"] = failure

    if status in FINAL:
        files, kept = download(api, ref, outdir)
        record["files"] = sorted(os.path.relpath(f, outdir) for f in files)
        if kept:
            record["kept_on_kaggle"] = kept
        record["gpu_quota_after"] = gpu_quota(api)
    else:
        print(f"Still {status} after the wait; it keeps running on Kaggle. "
              f"Run this job again with mode 'collect' to fetch the results.")

    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "run.json").write_text(json.dumps(record, indent=1), encoding="utf-8")
    print(json.dumps(record, indent=1))
    return 1 if status == "ERROR" else 0


if __name__ == "__main__":
    sys.exit(main())
