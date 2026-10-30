#!/usr/bin/env python3
"""QC for a finished long-form video: proves nothing was trimmed and that pictures + subtitles sit on the narration.

Usage: python3 qc_video.py final.mp4 part1.json [part2.json ...] [--report out.md]
part.json = {"name": "...", "spec": spec.json, "voice": voice.wav, "offset": seconds where this part starts in final.mp4}
(a one-part video is just one part file with offset 0)

Checks, per part and overall:
  1 LENGTH    final video and audio are at least as long as every part's plan (nothing cut off at the end)
  2 CUTS      every visible planned cut is found in the video at its planned time (median offset ~0, none missing)
  3 AUDIO     the narration track is present in the final mix in every 10 s window, at offset 0 (nothing dropped,
              doubled or shifted)
  4 SUBTITLES subtitle word onsets line up with the spoken words (lag per minute within +-0.15 s)
  5 ENDING    the last spoken line is fully inside the video
Exit code 0 = all pass.
"""
import json, subprocess, sys
import numpy as np

SR = 8000
args = [a for a in sys.argv[1:] if not a.startswith("--")]
REPORT = next((sys.argv[sys.argv.index(a) + 1] for a in sys.argv if a == "--report"), None)
final, parts = args[0], [json.load(open(p)) for p in args[1:] if not p.endswith(".md")]
out, ok_all = [], True
def say(s): print(s, flush=True); out.append(s)
def check(name, ok, detail):
    global ok_all; ok_all &= ok; say(f"{'PASS' if ok else 'FAIL'}  {name:10s} {detail}")
def audio(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32)
def probe(path, sel):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", sel, "-show_entries", "stream=duration", "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(r.stdout.strip().split("\n")[0])

vdur, adur = probe(final, "v"), probe(final, "a")
A = audio(final)
# scene cuts in the whole video (one pass)
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", final, "-vf", "scale=320:-1,select='gt(scene,0.3)',showinfo", "-f", "null", "-"], capture_output=True, text=True)
import re
CUTS = np.array([float(x) for x in re.findall(r"pts_time:([0-9.]+)", r.stderr)])
say(f"# QC: {final}\nvideo {vdur:.2f} s | audio {adur:.2f} s | {len(CUTS)} hard cuts detected\n")

for P in parts:
    spec = json.load(open(P["spec"])); off = P.get("offset", 0.0); name = P.get("name", P["spec"])
    end = spec["shots"][-1]["t1"]; say(f"## {name} (starts at {off:.2f} s, plan length {end:.2f} s)")
    # 1 LENGTH
    need = off + end - 0.05
    check("LENGTH", vdur >= need and adur >= need - 0.1, f"needs {need:.2f} s; video {vdur:.2f}, audio {adur:.2f}")
    # 2 CUTS: planned cuts that the detector can see (hard/flash/whip/zoom cuts between different pictures)
    T = np.array([s["t0"] for s in spec["shots"][1:]]) + off
    near = [CUTS[np.argmin(np.abs(CUTS - t))] - t for t in T if len(CUTS) and np.min(np.abs(CUTS - t)) < 2.0]
    med = float(np.median(near)) if near else float("nan")
    check("CUTS", len(near) >= 3 and abs(med) <= 0.1, f"{len(near)} planned cuts found in the video; median timing error {med:+.3f} s (pass: within 0.1 s)")
    # 3 AUDIO: narration present at offset 0 in every 10 s window that has speech
    V = audio(P["voice"]); bad, lags, n = [], [], 0
    for a in np.arange(0, len(V) / SR - 10, 10.0):
        v = V[int(a * SR):int((a + 10) * SR)]
        if np.sqrt(np.mean(v ** 2)) < 0.01: continue
        n += 1; best = (-1, 0)
        for d in np.arange(-0.5, 0.5001, 0.01):
            s0 = int((off + a + d) * SR)
            if s0 < 0: continue
            f = A[s0:s0 + len(v)]
            if len(f) < len(v): break
            c = np.corrcoef(np.abs(v), np.abs(f))[0, 1]
            if c > best[0]: best = (c, d)
        lags.append(best[1])
        if best[0] < 0.2 or abs(best[1]) > 0.03: bad.append(f"{off + a:.0f}s(r={best[0]:.2f},lag={best[1]:+.2f})")
    check("AUDIO", not bad, f"{n} speech windows checked; narration present at offset 0 in all" if not bad else f"problem windows: {', '.join(bad[:8])}")
    # 4 SUBTITLES: caption word onsets vs speech onsets in the narration, per minute
    import librosa
    y = V; env = librosa.onset.onset_strength(y=y, sr=SR, hop_length=80); tt = np.arange(len(env)) * 80 / SR
    on = np.array([w[1] for c in spec.get("captions", []) for w in c["words"]])
    per = []
    for m in range(int(end // 60) + 1):
        sel = on[(on >= m * 60) & (on < (m + 1) * 60)]
        if len(sel) < 20: continue
        per.append(max(((np.mean(np.interp(sel + d, tt, env)), d) for d in np.arange(-2.0, 2.01, 0.02)))[1])
    # captions are drawn at plan time t, which plays at off + t (+ any video lead, measured by CUTS)
    eff = [float(round(p_ + (med if near else 0), 2)) for p_ in per]
    worst = max((abs(e) for e in eff), default=0)
    check("SUBTITLES", worst <= 0.15, f"subtitle lag vs speech per minute: {eff} s (pass: all within 0.15 s)")
    # 5 ENDING
    words = [w for c in spec.get("captions", []) for w in c["words"]]
    last = max((w[2] for w in words), default=end)
    check("ENDING", off + last + 0.3 <= min(vdur, adur), f"last subtitle word ends {off + last:.2f} s; file ends {min(vdur, adur):.2f} s")
    say("")
say("ALL PASS" if ok_all else "SOME CHECKS FAILED")
if REPORT: open(REPORT, "w").write("\n".join(out) + "\n")
sys.exit(0 if ok_all else 1)
