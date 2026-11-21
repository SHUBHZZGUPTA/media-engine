import json, re, subprocess, os, sys, difflib
ME="/home/claude/me2"
L=json.load(open(f"{ME}/longform/fsi-secrets/lines_en.json")); parts=["full"]
SH=json.load(open("shots.json")); GAP=0.45
def dur(f): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)
norm=lambda w: re.sub(r"[^a-z0-9]","",w.lower())
def timing():
    off=0; lines=[]; words=[]; report=[]
    for p in parts:
        W=[r.split(" ",2) for r in open(f"{ME}/outputs/align/fsi-secrets-en-{p}/words.txt").read().strip().split("\n")]
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
G=lambda t,l=4.0: ("g5",t,l)
X=lambda t,l=4.0: ("x1",t,l)
Cc=lambda k,t,l: (k,t,l)
MD="MrDalekJD"; GS="GTA Series Videos"; WZ="WhizL"; ML="Mr Lore"; ZC="ZacCoxTV"; RR="Robbin Rams"; MB="MeBashButtons"; RC="Robotic Capybara"
P={
0:dict(shots=[X(512,5),X(520),X(1016,1.5)],label="l_intro"),
1:dict(shots=[X(752),X(760,1.5)]),
2:dict(shots=[Cc("u1",52,2.6),Cc("s1",52,2.2),Cc("d1",36,2.4),X(1128,2.2)],cr="Mr Lore  ·  WhizL  ·  GTA Series Videos"),
3:dict(shots=[X(536),X(992,2.2)]),
4:dict(shots=[X(708),X(1076,3.5)],ov=[("intro_logo",0.55,1,0)]),
5:dict(shots=[Cc("e3",1,4.2)],label="l1",ch="ch1",cr=MD),
6:dict(shots=[Cc("e1",1,2.6),Cc("e1",19,2.4),Cc("e2",10,2.2),Cc("e2",37,2.2)],cr=MD),
7:dict(shots=[Cc("e3",7,3.6),Cc("e3",16,4.4)],cr=MD),
8:dict(shots=[Cc("e3",25,3.6),Cc("e3",40,3.4)],cr=MD),
9:dict(shots=[Cc("e2",46,4.4),Cc("e3",46,4.6)],cr=MD),
10:dict(shots=[Cc("d1",37,2.4)],label="l2",ch="ch2",cr=GS),
11:dict(shots=[Cc("d1",1,3.2),Cc("d1",7,3.8)],cr=GS),
12:dict(shots=[Cc("d1",25,3.4),Cc("d1",40,4.2)],cr=GS),
13:dict(shots=[Cc("d1",76,2.8),Cc("d2",1,2.8),Cc("d2",22,3.4)],cr=GS),
14:dict(shots=[Cc("d3",13,3.4),Cc("d2",37,3.2)],cr=GS),
15:dict(shots=[Cc("s1",52,3.0)],label="l3",ch="ch3",cr=WZ),
16:dict(shots=[Cc("s1",19,2.8),Cc("s1",25,2.8)],cr=WZ),
17:dict(shots=[Cc("s1",9,3.0),Cc("s1",3.5,2.4),Cc("s1",33,2.8)],cr=WZ),
18:dict(shots=[Cc("s1",48,2.6),Cc("s1",55,3.0)],cr=WZ),
19:dict(shots=[Cc("s2",13,3.2),Cc("s2",42,2.8),Cc("s3",16,3.4)],cr=WZ),
20:dict(shots=[Cc("u1",56,3.0)],label="l4",ch="ch4",cr=ML),
21:dict(shots=[Cc("u1",14,3.0),Cc("u1",24,2.8)],cr=ML),
22:dict(shots=[Cc("u1",33,3.4),Cc("u1",42,3.6)],cr=ML),
23:dict(shots=[Cc("u1",50,3.2),Cc("u1",64,3.8)],cr=ML),
24:dict(shots=[Cc("u1",139,2.2),Cc("u2",12,2.8)],cr=ML),
25:dict(shots=[Cc("u1",148.5,5.9)],cr=ML),
26:dict(shots=[Cc("u3",1,4.0)],label="l5",ch="ch5",cr=ML),
27:dict(shots=[Cc("u2",3,4.0),Cc("u3",6,4.3)],cr=ML),
28:dict(shots=[Cc("u4",8,3.0),Cc("u5",1,3.0)],cr=ML),
29:dict(shots=[Cc("u6",30,2.8),Cc("u7",11.5,3.0)],cr=ML),
30:dict(shots=[Cc("u7",57,4.0),Cc("u5",22,3.9)],cr=ML),
31:dict(shots=[Cc("h2",21,3.9)],label="l6",ch="ch6",cr=ZC),
32:dict(shots=[Cc("h2",1,4.6),Cc("h2",16,5.6)],cr=ZC),
33:dict(shots=[Cc("h2",33,4.3)],cr=ZC),
34:dict(shots=[Cc("h3",12,3.0),Cc("h3",21,2.6),Cc("h3",45,2.4)],cr=ZC),
35:dict(shots=[Cc("h4",15,3.6),Cc("h4",45,3.9)],cr=ZC),
36:dict(shots=[Cc("h4",51,4.6),Cc("h4",61,4.7)],cr=ZC),
37:dict(shots=[Cc("ya",15,3.9)],label="l7",ch="ch7",cr=RR),
38:dict(shots=[Cc("ya",1,2.6),Cc("ya",37,2.4),Cc("ya",52,3.0)],cr=RR),
39:dict(shots=[Cc("ya",55.5,3.4),Cc("ya",64,3.7)],cr=RR),
40:dict(shots=[Cc("ha",55,3.0)],label="l8",ch="ch8",cr=MB),
41:dict(shots=[Cc("ha",34.5,3.6),Cc("ha",57,2.6),Cc("ha",75,2.6)],cr=MB),
42:dict(shots=[Cc("ha",67,3.4),Cc("ha",60,3.1)],cr=MB),
43:dict(shots=[Cc("dx",55,5.5)],label="l9",ch="ch9",cr=RC),
44:dict(shots=[Cc("dx",30.5,6.2),Cc("dx",56,5.3)],cr=RC),
45:dict(shots=[X(496),X(504),X(1072,3.5)],label="l9b"),
46:dict(shots=[X(760)],label="l10",ch="ch10"),
47:dict(shots=[X(1032),X(1136,2.0)]),
48:dict(shots=[X(1128),X(768)]),
49:dict(shots=[X(752,4.5),X(776,4.5)]),
50:dict(shots=[X(536,4.5),X(784)]),
51:dict(shots=[Cc("e3",8,0.9),Cc("d1",38,0.9),Cc("s1",53,0.8),Cc("u1",58,0.8),Cc("h4",62,0.9)],label="l_out",cr="Clips: creators credited in each chapter"),
52:dict(shots=[X(1064),X(1088,3.5)]),
53:dict(shots=[I("t1",21),I("t1",17),I("t1",10)]),
}
for _k in "e1 e2 e3 d1 d2 d3 s1 s2 s3 u1 u2 u3 u4 u5 u6 u7 h1 ya ha dx".split(): _crop[_k]="1920:1080:0:0"
for _k in "h2 h3 h4".split(): _crop[_k]="1560:878:360:202"
POOL=[X(752),X(512),X(1128),X(760),X(528),X(992),X(1064),X(480),X(776),X(1136),X(520),X(784),X(536),X(1224),X(928),X(936)]
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
KEY=set("billion million secrets ufo bigfoot dog mystery ten spoilers players egg eggs tower climb nest cutscene xgarbett cool barking goggles jet ski island twelve hundred skunk ape florida deer focus figure blacks kirk night abduction two clothes woman beam car trophy truth alien dream puzzle facility permanent health stamina house belville garage conspiracy notes identical j l video game yacht gps los santos michael thirteen arthur morgan hat five dollars legend dexter roof green fast furious monument stallions wildlife corruption humanity yeyo vibrates morse nobody chiliad subscribe leonida rockstar".split())
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
