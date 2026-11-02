# Free TTS bake-off on Kaggle: the same India Ch6 passage read by several free / open-source engines, so Shubham can
# pick by ear. Every engine runs in try/except; failures are logged and skipped. Outputs: /kaggle/working/*.mp3 + log.
import json, os, subprocess, sys, time, traceback, asyncio
OUT = "/kaggle/working"; os.makedirs(OUT, exist_ok=True)
P = json.loads(globals().get("JOB_PARAMS") or os.environ.get("JOB_PARAMS", "{}"))
LINES = P.get("lines") or [
    "His name was Mahmud of Ghazni, from today's Afghanistan. Starting around the year one thousand, he raided north India again and again. Around seventeen times.",
    "He came for gold. His raiders looted cities and temples, including the famous temple of Somnath in Gujarat, in ten twenty-six. Then he went home.",
    "Mahmud didn't stay to rule. But about a hundred and fifty years later, another invader did: Muhammad of Ghor.",
]
HINDI = P.get("hindi", "उसका नाम था महमूद ग़ज़नवी। वह सोने के लिए आया था, और उसने सोमनाथ के मशहूर मंदिर को लूटा।")
log = open(f"{OUT}/log.txt", "a")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); log.write(s + "\n"); log.flush()
def sh(cmd): say("$", cmd); r = subprocess.run(cmd, shell=True, capture_output=True, text=True); say(r.stdout[-1500:], r.stderr[-1500:]); return r.returncode
def to_mp3(wav, name): sh(f"ffmpeg -v error -y -i {wav} -ac 1 -b:a 160k {OUT}/{name}.mp3 && rm -f {wav}")
def join(chunks, sr, name, gap=0.45):
    import numpy as np, soundfile as sf
    parts = []
    for c in chunks: parts += [np.asarray(c, dtype=np.float32).reshape(-1), np.zeros(int(sr * gap), np.float32)]
    w = f"/tmp/{name}.wav"; sf.write(w, np.concatenate(parts), sr); to_mp3(w, name)
def engine(name, fn):
    t = time.time()
    try: fn(); say(f"OK {name} ({time.time() - t:.0f}s)")
    except Exception: say(f"FAIL {name}\n{traceback.format_exc()[-2500:]}")

sh("pip install -q soundfile edge-tts")
# 1) Microsoft Edge neural voices (free, unlimited; used by many faceless channels)
def edge():
    import edge_tts
    async def go(voice, text, path): await edge_tts.Communicate(text, voice).save(path)
    for v in ("en-US-AndrewMultilingualNeural", "en-US-BrianMultilingualNeural", "en-GB-RyanNeural", "en-US-ChristopherNeural"):
        asyncio.run(go(v, "  ".join(LINES), f"{OUT}/edge_{v.split('-')[2]}.mp3"))
    asyncio.run(go("hi-IN-MadhurNeural", HINDI, f"{OUT}/hindi_edge_Madhur.mp3"))
if not P.get("skip_edge"): engine("edge-tts", edge)

# 2) Kokoro-82M (Apache 2.0, best small open model on the leaderboards)
def kokoro():
    sh("apt-get -qq install -y espeak-ng > /dev/null 2>&1 || true"); sh("pip install -q 'kokoro>=0.9.4' misaki[en]")
    from kokoro import KPipeline
    pa = KPipeline(lang_code="a"); pb = KPipeline(lang_code="b")
    for pipe, v in ((pa, "am_michael"), (pa, "am_fenrir"), (pa, "am_puck"), (pb, "bm_george"), (pb, "bm_fable")):
        chunks = [a for line in LINES for _, _, a in pipe(line, voice=v, speed=1.0)]
        join(chunks, 24000, f"kokoro_{v}")
    try:
        ph = KPipeline(lang_code="h"); join([a for _, _, a in ph(HINDI, voice="hm_omega")], 24000, "hindi_kokoro_hm_omega")
    except Exception: say("kokoro hindi failed", traceback.format_exc()[-800:])
VENV = "/tmp/py312"
def venv():
    sh("pip install -q uv"); sh(f"uv venv -q -p 3.12 {VENV}")
    sh(f"uv pip install -q --python {VENV}/bin/python soundfile numpy 'kokoro>=0.9.4' 'misaki[en]' chatterbox-tts 'setuptools<81' "   # perth (chatterbox watermark) needs pkg_resources
       "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl")   # else misaki installs it into the system python
def sub(code):
    path = "/tmp/sub.py"; open(path, "w").write("import json, os, sys, numpy as np, soundfile as sf\nOUT = %r\nLINES = %r\nHINDI = %r\n" % (OUT, LINES, HINDI) +
        "def join(chunks, sr, name, gap=0.45):\n    parts = []\n    for c in chunks: parts += [np.asarray(c, dtype=np.float32).reshape(-1), np.zeros(int(sr * gap), np.float32)]\n"
        "    w = f'/tmp/{name}.wav'; sf.write(w, np.concatenate(parts), sr); os.system(f'ffmpeg -v error -y -i {w} -ac 1 -b:a 160k {OUT}/{name}.mp3 && rm -f {w}'); print('wrote', name, flush=True)\n" + code)
    if sh(f"{VENV}/bin/python {path}") != 0: raise RuntimeError("sub-process failed (see log)")
KOKORO = """
from kokoro import KPipeline
pa = KPipeline(lang_code='a'); pb = KPipeline(lang_code='b')
for pipe, v in ((pa, 'am_michael'), (pa, 'am_fenrir'), (pa, 'am_puck'), (pb, 'bm_george'), (pb, 'bm_fable')):
    join([a for line in LINES for _, _, a in pipe(line, voice=v, speed=1.0)], 24000, f'kokoro_{v}')
try:
    ph = KPipeline(lang_code='h'); join([a for _, _, a in ph(HINDI, voice='hm_omega')], 24000, 'hindi_kokoro_hm_omega')
except Exception as e: print('kokoro hindi failed', e)
"""
CHATTER = """
import torch
from chatterbox.tts import ChatterboxTTS
dev = 'cuda' if torch.cuda.is_available() else 'cpu'
m = ChatterboxTTS.from_pretrained(device=dev)
for tag, ex, cfg in (('calm', 0.5, 0.5), ('expressive', 0.7, 0.3), ('documentary', 0.4, 0.6)):
    join([m.generate(line, exaggeration=ex, cfg_weight=cfg).squeeze(0).cpu().numpy() for line in LINES], m.sr, f'chatterbox_{tag}')
try:
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    mm = ChatterboxMultilingualTTS.from_pretrained(device=dev)
    join([mm.generate(HINDI, language_id='hi').squeeze(0).cpu().numpy()], mm.sr, 'hindi_chatterbox')
except Exception as e: print('chatterbox hindi failed', e)
"""
sh("apt-get -qq install -y espeak-ng > /dev/null 2>&1 || true")
engine("py3.12 venv", venv)
engine("kokoro", lambda: sub(KOKORO))
engine("chatterbox", lambda: sub(CHATTER))

# 3) Chatterbox (Resemble AI, MIT; won a blind test vs ElevenLabs; emotion 'exaggeration' control; Hindi in the multilingual model)
def chatterbox():
    sh("pip install -q chatterbox-tts")
    import torch, torchaudio as ta
    from chatterbox.tts import ChatterboxTTS
    m = ChatterboxTTS.from_pretrained(device="cuda" if torch.cuda.is_available() else "cpu")
    for tag, ex, cfg in (("calm", 0.5, 0.5), ("expressive", 0.7, 0.3), ("documentary", 0.4, 0.6)):
        chunks = [m.generate(line, exaggeration=ex, cfg_weight=cfg).squeeze(0).cpu().numpy() for line in LINES]
        join(chunks, m.sr, f"chatterbox_{tag}")
    try:
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS
        mm = ChatterboxMultilingualTTS.from_pretrained(device="cuda" if torch.cuda.is_available() else "cpu")
        join([mm.generate(HINDI, language_id="hi").squeeze(0).cpu().numpy()], mm.sr, "hindi_chatterbox")
    except Exception: say("chatterbox hindi failed", traceback.format_exc()[-800:])
say("DONE"); log.close()
