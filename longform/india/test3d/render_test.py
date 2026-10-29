#!/usr/bin/env python3
"""India 3D globe test clip (official boundary): space -> India, tricolour fill + gold border glow."""
import json, os, shutil, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__)); ENG = os.path.join(HERE, "..", "..", "engine"); ART = os.path.join(HERE, "..", "map3d_art")
WORK = "/home/claude/work3d"; OUT = os.path.join(HERE, "india_globe_test.mp4")
data = {"mode": "globe", "dur": 10.0, "globe": {"tex": "globe.jpg",
    "cam": [[0.0, 55, 12, 3.6], [6.5, 80, 22, 2.15], [10.0, 81, 23, 2.0]],
    "over": [{"img": "ov_in_edge.png", "a": [[0, 0], [2.6, 0], [3.8, 1]], "add": 1},
             {"img": "ov_in_flag.png", "a": [[0, 0], [4.2, 0], [5.6, 0.85]]}],
    "arcs": [], "pins": []}}
P = os.path.join(WORK, "clips", "india_test"); shutil.rmtree(P, ignore_errors=True); os.makedirs(os.path.join(P, "assets"))
for n in {data["globe"]["tex"]} | {o["img"] for o in data["globe"]["over"]}:
    os.symlink(os.path.abspath(os.path.join(ART, n)), os.path.join(P, "assets", n))
shutil.copy("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf", os.path.join(P, "assets", "poppins700.ttf"))
for js in ("gsap/dist/gsap.min.js", "three/build/three.min.js"): shutil.copy(os.path.join(WORK, "node_modules", js), P)
html = open(os.path.join(ENG, "map3d", "clip.html")).read().replace("__DATA__", json.dumps(data)).replace("__DUR__", "%.3f" % data["dur"])
open(os.path.join(P, "index.html"), "w").write(html)
ENV = dict(os.environ, HYPERFRAMES_NO_TELEMETRY="1", DO_NOT_TRACK="1", HYPERFRAMES_NO_UPDATE_CHECK="1", HYPERFRAMES_SKIP_SKILLS="1",
           HYPERFRAMES_BROWSER_PATH="/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell")
t = time.time()
r = subprocess.run(["npx", "hyperframes", "render", "--crf", "16", "--no-browser-gpu", "--fps", "30", "--output", OUT], cwd=P, env=ENV, capture_output=True, text=True)
print("ok" if r.returncode == 0 and os.path.exists(OUT) else "FAILED " + (r.stdout + r.stderr)[-800:], round(time.time() - t), "s", flush=True)
