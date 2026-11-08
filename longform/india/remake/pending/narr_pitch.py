import json, os, re, sys, difflib, numpy as np, librosa
sys.path.insert(0, "/home/claude/media-engine/longform/india/full")
from num_in import digits
ROOT="/home/claude/media-engine"
def norm(w): return re.sub(r"[^a-z0-9]","",w.lower())
def toks(s):
    s=re.sub(r"\[[^\]]*\]"," ",s).replace("*","")
    return [norm(w) for w in re.split(r"[\s\-—–]+",digits(s).replace(",","")) if norm(w)]
job=sys.argv[1]; J=json.load(open(f"{ROOT}/jobs/tts/{job}.json")); REF=119.1
for it in J["items"]:
    n=it["name"]; W=[(float(a),float(b),norm(w)) for a,b,w in (r.split(None,2) for r in open(f"{ROOT}/outputs/align/{job}-{n}/words.txt") if r.strip())]
    S=[];own=[]
    for li,(who,txt) in enumerate(it["lines"]):
        for t in toks(txt): S.append(t); own.append((li,who))
    sm=difflib.SequenceMatcher(None,S,[w[2] for w in W],autojunk=False)
    span={}
    for b in sm.get_matching_blocks():
        for k in range(b.size):
            li,who=own[b.a+k]; t0,t1=W[b.b+k][0],W[b.b+k][1]
            s=span.setdefault(li,[who,t0,t1]); s[1]=min(s[1],t0); s[2]=max(s[2],t1)
    y,sr=librosa.load(f"{ROOT}/outputs/tts/{job}/{n}.wav",sr=16000)
    seg=np.concatenate([y[int(a*sr):int(b*sr)] for who,a,b in span.values() if who=="Narrator"])
    f0,v,_=librosa.pyin(seg,fmin=70,fmax=200,sr=sr,frame_length=1024); m=np.nanmedian(f0[v])
    st=12*np.log2(m/REF); print(f"{n} narrator {m:6.1f} Hz {st:+.1f} st {'OUT' if abs(st)>1.5 else 'ok'}")
