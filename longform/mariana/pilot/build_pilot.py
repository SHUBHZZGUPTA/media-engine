#!/usr/bin/env python3
"""Mariana Trench: 90-second pilot in the new style (real NOAA/NASA footage, 3D trench, layered motion shots, minimal text,
no mascot). Reuses the approved narration; drops the two mascot lines. Writes out/pilot_spec.json, out/voice.wav, out/music.json."""
import json, os, subprocess
import numpy as np, soundfile as sf
M = "/home/claude/media-engine/longform/mariana"; F1 = "/home/claude/media-engine/outputs/fetch/mt-video"; F2 = "/home/claude/media-engine/outputs/fetch/mt-video2"
S = "/home/claude/pilot/shots"; O = "/home/claude/pilot/out"; os.makedirs(S, exist_ok=True)
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
SKIP = [(26.3, 30.45), (60.4, 63.4)]                     # mascot lines 3 and 7 (+ their pauses)
def nt(t):                                                  # original narration time -> pilot time
    d = 0.0
    for a, b in SKIP:
        if t >= b: d += b - a
        elif t > a: return a - d
    return t - d
END = 90.0
# ---- voice ----
v, sr = sf.read(f"{M}/voice_en.wav", dtype="float32")
keep, last = [], 0.0
for a, b in SKIP: keep.append(v[int(last * sr):int(a * sr)]); last = b
keep.append(v[int(last * sr):int((END + 7.15) * sr)])
vo = np.concatenate(keep)[:int(END * sr)]; n = int(.25 * sr); vo[-n:] *= np.linspace(1, 0, n)
sf.write(f"{O}/voice.wav", vo, sr, subtype="PCM_16")
# ---- footage segments, cut to exactly what each shot needs (1920x1080, 30 fps, fills the frame) ----
def seg(name, src, start, dur, crop=None, speed=1.0):
    out = f"{S}/{name}.mp4"
    vf = (crop + "," if crop else "") + (f"setpts=PTS/{speed}," if speed != 1 else "") + "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,format=yuv420p"
    if not os.path.exists(out):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-i", src, "-t", str((dur + .5) * speed), "-vf", vf, "-an",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", out], check=True)
    return out
C3 = f"{M}/clips3d"
shots = []
def shot(t0, video, layers=(), cut="curve"): shots.append({"t0": round(t0, 3), "bg": {"video": video, "img": "#02070d"}, "layers": list(layers), "cut": cut})
def title(text, t_in, t_out, y=600, size=104, box=None, color="#ffffff"):
    return {"img": {"text": text, "size": size, "color": color, "box": box, "font": FONT}, "x": 960, "y": y, "in": t_in, "out": t_out, "enter": "fade", "exit": "fade"}
shot(0.0, f"{S}/sink.mp4", cut="hard")                                                       # 0: sinking to 10,900 m (layered motion)
shot(10.62, seg("medusa", f"{F1}/v_medusa.webm", 12.0, 5.3))                      # 1: "only a handful... lights"
shot(15.85, seg("isopod_far", f"{F1}/v_bathynomus.webm", 9.0, 5.2))                          # 2: "looked out the window... sea floor"
shot(20.95, f"{S}/plastic.mp4")                                                               # 3: "A plastic bag." (circle at 22.85)
t = nt(30.46); shot(t, f"{C3}/G_pacific.mp4", [title("THE MARIANA TRENCH", nt(33.3), nt(36.4), y=170, size=96)])   # 4
shot(nt(37.4), seg("vents", f"{F1}/v_vents.webm", 12.0, 3.6))                                # 5: "water can crush steel"
shot(nt(40.9), seg("jelly_glow", f"{F1}/v_jelly_mariana.webm", 23.6, 2.2))                   # 6: "fish glow like lanterns"
shot(nt(43.0), seg("isopod_close", f"{F1}/v_bathynomus.webm", 34.0, 3.1))                    # 7: "as big as your hand"
shot(nt(46.0), seg("nasa_drain2", f"{F2}/v_nasa_drain.webm", 5.0, 6.9, crop="crop=iw:ih*0.86:0:0", speed=2.0))   # 8: "swallowing the ocean"
shot(nt(52.8), seg("descent", f"{F2}/v_okeanos_guyot.webm", 12.0, 3.6))                      # 9: "all the way down"
shot(nt(56.3), seg("floor_fish", f"{F1}/v_dive11_fish.webm", 0.0, 6.0))                      # 10: "until we hit the bottom of the world"
shots[-1]["layers"].append(title("CHAPTER 1", nt(63.5), nt(65.2), y=470, size=60, color="#9fd6ff", box="#0a0f18d0"))
shots[-1]["layers"].append(title("The Hole at the Bottom of the World", nt(63.5), nt(65.2), y=600, size=84, box="#0a0f18d0"))
shot(nt(65.22), f"{C3}/G_where.mp4", cut="zoom")                                             # 11: where is it (3D globe)
shot(nt(65.22) + 13.5, f"{C3}/T_length.mp4", [title("~2,550 km long", nt(81.3), nt(85.6), y=170, size=88)])   # 12: 3D trench length
shot(nt(65.22) + 13.5 + 7.05, f"{C3}/T_deep.mp4")                                                          # 13: Challenger Deep (3D)
for s, n_ in zip(shots, shots[1:] + [None]): s["t1"] = n_["t0"] if n_ else END
# ---- captions: the approved ones, mascot lines dropped, re-timed ----
spec0 = json.load(open(f"{M}/spec_en.json")); caps = []
for c in spec0["captions"]:
    if c["t0"] >= END + 7.15 or any(a <= c["t0"] < b for a, b in SKIP): continue
    caps.append({"t0": nt(c["t0"]), "t1": nt(c["t1"]), "words": [[w, nt(a), nt(b), k] for w, a, b, k in c["words"]]})
caps = [c for c in caps if c["t0"] < END - .2]
spec = {"w": 1920, "h": 1080, "fps": 30, "shots": shots, "punch": [], "shake": [], "captions": caps, "fx": []}
json.dump(spec, open(f"{O}/pilot_spec.json", "w"), indent=1)
# sound: only the chapter cut gets a designed whoosh; one low impact on "A plastic bag"; no pops on titles
mspec = dict(spec, shots=[shots[0]] + [s for s in shots[1:] if s["cut"] in ("zoom", "flash", "whip")], fx=[["impact-bass-1", 22.75, -16]])
for s in mspec["shots"]: s = dict(s, layers=[])
mspec["shots"] = [dict(s, layers=[]) for s in mspec["shots"]]
json.dump(mspec, open(f"{O}/mix_spec.json", "w"), indent=1)
MU = "/home/claude/media-engine/money-mirage/mm3/library/music/"
json.dump({"sfx_dir": "/home/claude/media-engine/money-mirage/mm3/library/sfx", "below_voice_db": 21, "swell_db": 3,
           "sections": [{"file": MU + "4_standoff.mp3", "from": 0, "to": nt(63.6), "gain_db": -18},
                        {"file": MU + "1_keys.mp3", "from": nt(63.0), "to": END, "gain_db": -19}]}, open(f"{O}/music.json", "w"), indent=1)
print(len(shots), "shots;", len(caps), "caption chunks; end", END)
for s in shots: print(round(s["t0"], 2), round(s["t1"] - s["t0"], 2), os.path.basename(s["bg"]["video"]), [l["img"]["text"] for l in s["layers"]])
