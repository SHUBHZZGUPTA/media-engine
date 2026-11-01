"""Runs on Kaggle (CPU only). Checks whether manim installs and renders a Money-Mirage-style
chart clip, how long it takes at three qualities, and whether MathTex works without LaTeX.
Saves manim_check.json plus the small test clips into /kaggle/working."""
import json
import os
import platform
import shutil
import subprocess
import sys
import time

OUT = "/kaggle/working"
os.makedirs(OUT, exist_ok=True)
res = {"python": platform.python_version(), "cpus": os.cpu_count()}


def sh(cmd, timeout=900):
    t = time.time()
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return p.returncode, round(time.time() - t, 1), (p.stdout + p.stderr)[-1500:]


# 1. install (pip first; add system libs only if the wheel build needs them)
code, secs, log = sh("pip install -q manim")
res["pip_manim"] = {"exit": code, "secs": secs}
if code != 0:
    res["pip_manim"]["log_tail"] = log
    c2, s2, l2 = sh("apt-get update -qq && apt-get install -y -qq libpango1.0-dev libcairo2-dev pkg-config ffmpeg")
    res["apt_libs"] = {"exit": c2, "secs": s2, "log_tail": l2 if c2 else ""}
    code, secs, log = sh("pip install -q manim")
    res["pip_manim_retry"] = {"exit": code, "secs": secs, "log_tail": log if code else ""}

res["ffmpeg"] = shutil.which("ffmpeg")
res["latex"] = shutil.which("latex")

# 2. a compounding-curve scene, text via Pango only (no LaTeX needed)
SCENE = '''
from manim import *

class Compound(Scene):
    def construct(self):
        ax = Axes(x_range=[0, 30, 5], y_range=[0, 100000, 25000], x_length=9, y_length=4.6,
                  axis_config={"include_numbers": False, "color": GREY_B})
        lo = ax.plot(lambda x: 10000 * 1.07 ** x, x_range=[0, 30], color=BLUE)
        hi = ax.plot(lambda x: 10000 * 1.12 ** x, x_range=[0, 30], color=ORANGE)
        t1 = Text("7% a year", font_size=28, color=BLUE).next_to(ax.c2p(30, 76000), LEFT)
        t2 = Text("12% a year", font_size=28, color=ORANGE).next_to(ax.c2p(22, 100000), UP, buff=0.1)
        title = Text("Why 5 points of return changes everything", font_size=34).to_edge(UP)
        self.play(FadeIn(title), Create(ax), run_time=1)
        self.play(Create(lo), FadeIn(t1), run_time=2)
        self.play(Create(hi), FadeIn(t2), run_time=2)
        dot = Dot(ax.c2p(30, 10000 * 1.12 ** 30), color=YELLOW)
        self.play(FadeIn(dot, scale=2), Indicate(t2), run_time=1)
        self.wait(1)
'''
open("scene.py", "w").write(SCENE)

res["renders"] = {}
for name, flags in [("480p15", "-ql"), ("720p30", "-qm"), ("1080p60", "-qh")]:
    code, secs, log = sh(f"manim render {flags} --media_dir media_{name} scene.py Compound", timeout=1500)
    entry = {"exit": code, "secs": secs}
    if code != 0:
        entry["log_tail"] = log
    else:
        for root, _, files in os.walk(f"media_{name}"):
            for f in files:
                if f.endswith(".mp4") and "partial" not in root:
                    dst = os.path.join(OUT, f"compound_{name}.mp4")
                    shutil.copy(os.path.join(root, f), dst)
                    entry["mp4_kb"] = round(os.path.getsize(dst) / 1024)
    res["renders"][name] = entry

# 3. does MathTex work without LaTeX? (expected: no)
MT = '''
from manim import *
class M(Scene):
    def construct(self):
        self.add(MathTex(r"A = P(1+r)^n"))
'''
open("mt.py", "w").write(MT)
code, secs, log = sh("manim render -ql --media_dir media_mt mt.py M")
res["mathtex_without_latex"] = {"exit": code, "secs": secs, "log_tail": log if code else ""}

json.dump(res, open(os.path.join(OUT, "manim_check.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
