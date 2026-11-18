import json, re, subprocess, os, sys, difflib
ME="/home/claude/media-engine"
L=json.load(open(f"{ME}/longform/fsi-duo/lines_en.json")); parts=["full"]
SH=json.load(open("shots.json")); GAP=0.45
def dur(f): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)
norm=lambda w: re.sub(r"[^a-z0-9]","",w.lower())
def timing():
    off=0; lines=[]; words=[]; report=[]
    for p in parts:
        W=[r.split(" ",2) for r in open(f"{ME}/outputs/align/fsi-duo-en-{p}/words.txt").read().strip().split("\n")]
        hw=[norm(w[2]) for w in W]; sw=[]; owner=[]
        for li,t in enumerate(L[p]):
            for w in t.split(): sw.append(w); owner.append(li)
        sn=[norm(w) for w in sw]; tm=[None]*len(sw)
        sm=difflib.SequenceMatcher(a=sn,b=hw,autojunk=False); matched=0
        for a,b,n in sm.get_matching_blocks():
            for k in range(n): tm[a+k]=(float(W[b+k][0]),float(W[b+k][1])); matched+=1
        report.append((p,len(sn),len(hw),matched))
        # interpolate gaps
        known=[i for i,x in enumerate(tm) if x]
        for i in range(len(tm)):
            if tm[i] is None:
                prev=max([k for k in known if k<i],default=None); nxt=min([k for k in known if k>i],default=None)
                a=tm[prev][1] if prev is not None else 0; b=tm[nxt][0] if nxt is not None else a+0.3
                n=(nxt if nxt is not None else i+1)-(prev if prev is not None else -1); j=i-(prev if prev is not None else -1)
                tm[i]=(a+(b-a)*(j-1)/max(1,n-1), a+(b-a)*j/max(1,n-1))
        base=len(lines)
        for li,t in enumerate(L[p]):
            idx=[i for i,o in enumerate(owner) if o==li]
            lines.append({"text":t,"start":off+tm[idx[0]][0],"end":off+tm[idx[-1]][1],"part":p})
            for i in idx: words.append({"w":sw[i],"s":off+tm[i][0],"e":off+tm[i][1],"line":base+li})
        off+=dur(f"audio/{p}.wav")+GAP
    total=off-GAP+0.8
    json.dump({"lines":lines,"words":words,"total":total},open("timing.json","w"),indent=1)
    print(report,"total",round(total,2))
    for i,l in enumerate(lines): print(i,round(l["start"],2),round(l["end"]-l["start"],2),l["text"][:50])
if __name__=="__main__" and sys.argv[1]=="timing": timing()


_crop={"x1":"1920:1080:0:0"}
FN=json.load(open("fine.json"))
def S(k,i): a,b=SH[k][i]; return (k,a,b-a)
def R(k,a,l): return (k,a,l)
def F(k,t):
    for a,b in FN[k]:
        if a<=t<=b: return (k,a,min(b-a,4.5))
    a,b=min(FN[k],key=lambda s_:min(abs(s_[0]-t),abs(s_[1]-t))); print("NEAR",k,t,"->",a,b); return (k,a,min(b-a,4.5))
def I(k,i): a,b=FN[k][i]; return (k,a,min(b-a,4.5))
X=lambda t,l=3.5: ("x1",t,l)
P={
0:dict(shots=[I("t3",10),I("t3",19),I("t2",68),I("t1",17),I("t1",10),I("t2",11)],label="l_intro"),
1:dict(shots=[I("t3",19)],own=1),
2:dict(shots=[I("t3",36),I("t2",36)],own=1),
3:dict(shots=[I("t1",16),X(992),I("t2",11),X(504)]),
4:dict(shots=[I("t2",31),I("t2",33),X(594),I("t2",36)]),
5:dict(shots=[I("t3",11),I("t2",34),I("t2",33)],own=1),
6:dict(shots=[I("t1",21),I("t3",42)],ov=[("intro_logo",0,1,0)]),
7:dict(shots=[I("t2",8)],label="l_jason",ch="ch1"),
8:dict(shots=[I("t2",3),I("t3",3),I("t2",7)]),
9:dict(shots=[I("t3",19),I("t3",5),I("t2",10),I("t2",9)],own=1),
10:dict(shots=[I("t3",1),I("t3",2),I("t3",4),I("t3",6),I("t1",19)]),
11:dict(shots=[I("t2",1),I("t2",6),I("t2",2),I("t2",4)]),
12:dict(shots=[I("t2",13),I("t3",24),I("t2",69)]),
13:dict(shots=[I("t2",24),I("t2",25),I("t2",37),I("t3",10),I("t3",36)],own=1),
14:dict(shots=[I("t2",18)],label="l_lucia",ch="ch2"),
15:dict(shots=[I("t2",52),I("t3",41),I("t3",15)],own=1),
16:dict(shots=[I("t1",2),I("t1",3),I("t1",4),I("t1",5)],own=1),
17:dict(shots=[I("t2",15),I("t2",54),I("t2",53),I("t1",5)],own=1),
18:dict(shots=[I("t2",16),I("t2",17),I("t2",18)]),
19:dict(shots=[I("t3",33),I("t2",54),I("t3",15)],own=1),
20:dict(shots=[I("t2",31),I("t1",7),I("t1",10),I("t1",20)]),
21:dict(shots=[I("t3",41),I("t1",46)],own=1),
22:dict(shots=[I("t1",40),I("t3",33),I("t2",54)],own=1),
23:dict(shots=[I("t3",36),I("t2",36),I("t2",37),I("t2",38),I("t2",73)],own=1),
24:dict(shots=[I("t2",21),I("t2",20),I("t2",55),I("t2",66),I("t3",25),I("t2",67),I("t3",31)],own=1),
25:dict(shots=[I("t3",42),I("t1",1)]),
26:dict(shots=[X(488),X(496)],label="l_play",ch="ch3"),
27:dict(shots=[X(1008,3),X(1072,3),X(1064,3),X(504),X(1135.8,3.4)]),
28:dict(shots=[X(846),X(854),X(862),X(934)]),
29:dict(shots=[X(593,4.5),X(598,4),X(425.3,3.6),X(429,3)]),
30:dict(shots=[X(384),X(400),X(432),X(448,3),X(472,3)]),
31:dict(shots=[X(392,4),X(1424),X(512)]),
32:dict(shots=[I("t2",12),X(1040),I("t3",28),X(432)]),
33:dict(shots=[I("t2",33),I("t2",34),I("t1",14),I("t2",39)],label="l_six"),
34:dict(shots=[I("t2",26)],own=1,label="l_cal",ch="ch4"),
35:dict(shots=[I("t2",27),I("t2",26),X(1032)],own=1),
36:dict(shots=[I("t2",27),I("t2",25),I("t2",64)]),
37:dict(shots=[I("t2",64),I("t2",65)]),
38:dict(shots=[I("t3",5),I("t2",26),I("t2",3)],own=1),
39:dict(shots=[I("t3",17)],own=1,label="l_boobie",ch="ch5"),
40:dict(shots=[I("t1",7),I("t2",62),I("t1",18),I("t1",14)],own=1),
41:dict(shots=[I("t3",17),X(1056,3)],own=1),
42:dict(shots=[I("t2",56)],own=1,label="l_dre",ch="ch6"),
43:dict(shots=[I("t2",56),I("t1",13),I("t1",43),I("t1",15)],own=1),
44:dict(shots=[I("t2",39),I("t1",18),I("t2",41)],own=1),
45:dict(shots=[I("t1",26)],own=1,label="l_dimez",ch="ch7"),
46:dict(shots=[I("t1",26),I("t3",22)],own=1),
47:dict(shots=[I("t3",22),I("t1",18),I("t2",39)],own=1),
48:dict(shots=[I("t2",56),I("t2",39),I("t3",17),I("t1",26)],own=1),
49:dict(shots=[X(906,4)],label="l_raul",ch="ch8"),
50:dict(shots=[X(906.5,4),X(1000),I("t2",21)]),
51:dict(shots=[X(960),I("t2",55),X(944)]),
52:dict(shots=[X(880),X(968)]),
53:dict(shots=[I("t2",2),I("t2",4)],label="l_brian",ch="ch9"),
54:dict(shots=[I("t2",4),I("t2",28),I("t2",29),I("t3",4),I("t2",2)]),
55:dict(shots=[I("t2",4),I("t2",2)]),
56:dict(shots=[I("t2",3)]),
57:dict(shots=[I("t2",6),I("t2",1)],label="l_theory"),
58:dict(shots=[I("t2",1),I("t2",3),I("t2",7),I("t2",21),I("t2",4)]),
59:dict(shots=[I("t2",2),I("t2",4)]),
60:dict(shots=[I("t1",19),I("t1",10),X(992),I("t1",16),I("t2",21)]),
61:dict(shots=[I("t3",33),I("t3",36),I("t2",70)],label="l_unk"),
62:dict(shots=[I("t2",68),I("t2",69),I("t2",73)]),
63:dict(shots=[I("t3",19),I("t2",33),I("t2",36),I("t3",10)],label="l_out"),
64:dict(shots=[I("t2",31),I("t3",10),I("t2",37),I("t3",19)],own=1),
65:dict(shots=[I("t1",21),I("t3",42),I("t1",17)]),
}
POOL=[I("t1",8),I("t3",8),I("t1",20),I("t3",27),I("t1",35),I("t2",14),I("t1",47),I("t3",18),I("t1",9),I("t3",23),I("t1",10),I("t2",11),I("t1",13),I("t1",17),I("t2",68),I("t1",19),I("t3",42),I("t1",16),X(512),X(520),X(752),X(776),I("t2",69),I("t1",43),I("t1",11),I("t1",12)]
FPS=30
def spans():
    T=json.load(open("timing.json")); ls=T["lines"]; out=[]
    for i,l in enumerate(ls):
        a=0 if i==0 else max(0,l["start"]-0.12); b=(ls[i+1]["start"]-0.12) if i+1<len(ls) else T["total"]
        out.append((round(a*FPS)/FPS,round(b*FPS)/FPS))
    return T,out
def crop_of(k):
    if k not in _crop:
        o=subprocess.run(["ffmpeg","-v","info","-ss","30","-t","20","-i",f"src/{k}.mp4","-vf","cropdetect=24:2:0","-f","null","-"],capture_output=True,text=True).stderr
        c=re.findall(r"crop=([0-9:]+)",o); from collections import Counter
        _crop[k]=Counter(c).most_common(1)[0][0] if c else "1920:1080:0:0"
    return _crop[k]
MI=",minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,setpts=PTS-STARTPTS"
ONLY=set(int(x) for x in os.environ.get("BGONLY","").split(",") if x)
def bg():
    T,sp=spans(); os.makedirs("bg",exist_ok=True); pool=list(POOL); pi=0; files=[]
    for i,(a,b) in enumerate(sp):
        need=b-a; shots=list(P[i]["shots"])
        own=P[i].get("own")
        while (not own) and sum(s[2] for s in shots) < need+0.05*len(shots): shots.append(pool[pi%len(pool)]); pi+=1
        tot=sum(s[2] for s in shots); acc=0
        for j,(k,ss,ln) in enumerate(shots):
            d=round((need*ln/tot)*FPS)/FPS if j<len(shots)-1 else round((need-acc)*FPS)/FPS
            acc+=d
            if d<=0: continue
            r_=ln/d; sp_=1.0 if r_>=0.97 else max(0.5,r_); interp=sp_<1.0; f=f"bg/l{i:02d}_{j}.mp4"; files.append(f)
            if os.path.exists(f): continue
            if ONLY and i not in ONLY: continue
            vf=f"crop={crop_of(k)},scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setpts=PTS/{sp_:.4f},fps={FPS}{MI if interp else ""},tpad=stop_mode=clone:stop_duration=12,trim=duration={d:.4f},setsar=1,format=yuv420p"
            if own and ln/sp_<d-0.3: vf=vf.replace(",setsar=1",",scale=3840:2160,zoompan=z='1+0.0006*on':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30,setsar=1")
            r=subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{ss:.3f}","-t",f"{ln:.3f}","-i",f"src/{k}.mp4","-an","-vf",vf,"-frames:v",str(round(d*FPS)),"-c:v","libx264","-preset","veryfast","-crf","17","-g","30",f+".tmp.mp4"])
            if r.returncode==0: os.rename(f+".tmp.mp4",f)
            else: print("FAIL",f)
    open("bg/list.txt","w").write("".join(f"file '{os.path.abspath(x)}'\n" for x in files))
    if ONLY: return
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i","bg/list.txt","-c","copy","bg_all.mp4"],check=True)
    print("bg",dur("bg_all.mp4"),"target",T["total"],len(files))
KEY=set("jason lucia duval caminos thirteen hundred leaks spoilers six couple trust easy harder army keys rent boss fight penitentiary luck ankle smart liberty history first conspiracy darkest sunniest hold hands hurry apartment texts relationship muscle cal hampton conspiracies boobie ike empire business drequan priest hustler raw hit dimez bae-luxe roxy dwnply raul bautista risks recklessness brian heder landlord dirty theory leash wrong ends controller subscribe leonida rockstar vice".split())
def ass(t0,t1,path):
    T=json.load(open("timing.json")); W=T["words"]; chunks=[]; cur=[]
    for w in W:
        if cur and (w["line"]!=cur[-1]["line"] or len(cur)>=3 or sum(len(x["w"]) for x in cur)+len(w["w"])>17 or re.search(r"[.?!,]$",cur[-1]["w"]) or w["s"]-cur[-1]["e"]>0.45): chunks.append(cur); cur=[]
        cur.append(w)
    if cur: chunks.append(cur)
    def ts(x): x=max(0,x); return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
    hdr="[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nWrapStyle: 2\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: C,Bebas Neue,96,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,1,0,1,6,3,2,60,60,58,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    ev=[]
    for n,c in enumerate(chunks):
        s=c[0]["s"]-0.03; e=c[-1]["e"]+0.12
        if n+1<len(chunks): e=min(e,chunks[n+1][0]["s"]-0.03)
        if e<=t0 or s>=t1: continue
        txt=" ".join(("{\\c&H1ED2FF&}"+re.sub(r",$","",w["w"]).upper()+"{\\c&HFFFFFF&}") if re.sub(r"[^a-z0-9-]","",w["w"].lower()) in KEY else re.sub(r",$","",w["w"]).upper() for w in c)
        ev.append(f"Dialogue: 0,{ts(s-t0)},{ts(e-t0)},C,,0,0,0,,{{\\fad(40,0)}}{txt}")
    open(path,"w").write(hdr+"\n".join(ev)+"\n")
def audio(music="eighties_action"):
    T=json.load(open("timing.json")); total=T["total"]
    fc=f"[0:a]loudnorm=I=-15:TP=-1.5:LRA=11,aresample=48000,apad=whole_dur={total:.3f},asplit=2[v1][v2];[1:a]aresample=48000,volume=0.16,afade=t=in:d=1.5,afade=t=out:st={total-3:.2f}:d=3[m];[m][v1]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[md];[md][v2]amix=inputs=2:normalize=0:duration=longest,atrim=duration={total:.3f}[a]"
    cmd=["ffmpeg","-v","error","-y","-i","audio/full.wav","-stream_loop","-1","-i",f"audio/{music}.mp3","-filter_complex",fc,"-map","[a]","-c:a","aac","-b:a","192k","mix.m4a"]
    subprocess.run(cmd,check=True); print("audio",dur("mix.m4a"))
if __name__=="__main__":
    for st in sys.argv[1:]:
        if st!="timing": globals()[st]()
