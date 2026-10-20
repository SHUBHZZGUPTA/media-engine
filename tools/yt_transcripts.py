"""Fetch public metadata + a transcript for given YouTube videos (captions first, Whisper on the audio as fallback).
Job: {"id": "...", "urls": ["https://youtube.com/shorts/..."]}
Writes outputs/yt/<id>/<video id>.json (title, channel, views, description, transcript, source).
"""
import glob, json, os, subprocess, sys, re
job = json.load(open(sys.argv[1])); out = os.path.join("outputs", "yt", job["id"]); os.makedirs(out, exist_ok=True)
tmp = "/tmp/yt"; os.makedirs(tmp, exist_ok=True)
def vtt_text(p):
    lines = []
    for ln in open(p, encoding="utf-8", errors="ignore"):
        ln = re.sub(r"<[^>]+>", "", ln).strip()
        if not ln or "-->" in ln or ln.startswith(("WEBVTT", "Kind:", "Language:")) or ln.isdigit(): continue
        if not lines or lines[-1] != ln: lines.append(ln)
    return " ".join(lines)
for url in job["urls"]:
    rec = {"url": url}
    r = subprocess.run(["yt-dlp", "-J", "--skip-download", url], capture_output=True, text=True, timeout=300)
    if r.returncode == 0:
        d = json.loads(r.stdout)
        rec.update({k: d.get(k) for k in ("id", "title", "channel", "channel_follower_count", "view_count", "like_count", "duration", "upload_date", "description", "tags")})
    else: rec["meta_error"] = r.stderr[-400:]
    vid = rec.get("id") or re.sub(r"\W", "", url)[-11:]
    subprocess.run(["yt-dlp", "--skip-download", "--write-subs", "--write-auto-subs", "--sub-langs", "en.*,hi.*", "--sub-format", "vtt",
                    "-o", f"{tmp}/{vid}.%(ext)s", url], capture_output=True, text=True, timeout=300)
    subs = sorted(glob.glob(f"{tmp}/{vid}*.vtt"))
    if subs:
        rec["transcripts"] = {os.path.basename(s): vtt_text(s) for s in subs}; rec["source"] = "captions"
    else:
        a = subprocess.run(["yt-dlp", "-x", "--audio-format", "wav", "-o", f"{tmp}/{vid}.%(ext)s", url], capture_output=True, text=True, timeout=600)
        wav = f"{tmp}/{vid}.wav"
        if os.path.exists(wav):
            from faster_whisper import WhisperModel
            m = WhisperModel("small", device="cpu", compute_type="int8")
            segs, info = m.transcribe(wav, beam_size=5)
            rec["transcripts"] = {"whisper": " ".join(s.text.strip() for s in segs)}; rec["source"] = f"whisper ({info.language})"
        else: rec["audio_error"] = a.stderr[-400:]
    json.dump(rec, open(os.path.join(out, f"{vid}.json"), "w"), indent=1, ensure_ascii=False); print(vid, rec.get("source"), rec.get("title"))
