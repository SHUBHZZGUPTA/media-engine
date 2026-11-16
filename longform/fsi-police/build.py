import json, re, subprocess, os, sys, difflib
ME="/home/claude/media-engine"
L=json.load(open(f"{ME}/longform/fsi-police/lines_en.json")); parts=["pA","pB","pC"]
SH=json.load(open("shots.json")); GAP=0.45
def dur(f): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)
norm=lambda w: re.sub(r"[^a-z0-9]","",w.lower())
def timing():
    off=0; lines=[]; words=[]; report=[]
    for p in parts:
        W=[r.split(" ",2) for r in open(f"{ME}/outputs/align/fsi-police-en-{p}/words.txt").read().strip().split("\n")]
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

# ---------------- visual plan ----------------
def S(k,i): a,b=SH[k][i]; return (k,a,b-a)
def R(k,a,l): return (k,a,l)
P={ # line -> dict(shots, ov=[(name,f0,f1,blur)], label, ch)
0:dict(shots=[S("t1",39),S("t2",7),S("t1",40)],label="l_intro"),
1:dict(shots=[S("t3",17)],ov=[("hook1",0.25,1,0)]),
2:dict(shots=[S("t3",4),S("t1",14),S("t3",9),S("t2",24)]),
3:dict(shots=[R("t2",105.6,3.4),S("t4",12),S("t1",37)]),
4:dict(shots=[S("t1",1),S("t1",13),S("t4",17),S("t2",8)]),
5:dict(shots=[S("t3",28),S("t2",41)],ov=[("hook2",0.62,1,0)]),
6:dict(shots=[S("t1",18),S("t3",21)],ov=[("intro_logo",0,1,0)]),
7:dict(shots=[S("t1",11),S("t1",8)],label="l_old",ch="ch1"),
8:dict(shots=[S("t1",16),S("t1",9)],ov=[("old_way",0,1,1)]),
9:dict(shots=[S("t2",43),S("t1",7)],ov=[("old_way",0,1,1)]),
10:dict(shots=[S("t5",6),S("t3",21)],ov=[("old_way",0,1,1)]),
11:dict(shots=[R("t3",48.3,2.6)],ov=[("throws",0,1,0)]),
12:dict(shots=[S("t2",37),S("t1",8)],label="l_wit",ch="ch2"),
13:dict(shots=[S("t2",35),S("t3",4),S("t2",26),S("t4",13)],ov=[("witness1",0.36,0.56,1),("witness2",0.56,0.74,1),("witness3",0.74,1,1)]),
14:dict(shots=[R("t2",73.7,2.1),S("t3",12),S("t3",16)]),
15:dict(shots=[S("t2",28),S("t1",12)],ov=[("states1",0.6,1,1)]),
16:dict(shots=[S("t1",13),R("t3",18.0,2.4)],ov=[("states1",0,1,1)]),
17:dict(shots=[S("t2",36),S("t2",21)],ov=[("ghost",0.55,1,0)]),
18:dict(shots=[S("t3",1),S("t2",1)],label="l_states",ch="ch3"),
19:dict(shots=[S("t1",34),S("t1",37)],ov=[("states1",0,1,1)]),
20:dict(shots=[S("t4",12),S("t2",11)],ov=[("states2",0,1,1)]),
21:dict(shots=[S("t3",28),R("t2",105.6,3.4)],ov=[("states3",0,1,1,"flashA"),("states3b",0,1,1,"flashB")]),
22:dict(shots=[S("t1",25),R("t3",73.3,4.0),S("t2",23)],ov=[("states4",0,1,1)]),
23:dict(shots=[R("t3",18.0,2.4),S("t1",13)],ov=[("six",0.12,1,1)]),
24:dict(shots=[S("t2",3),S("t2",5)],label="l_icons",ch="ch4"),
25:dict(shots=[S("t2",13)],ov=[("icons0",0.3,1,1)]),
26:dict(shots=[S("t3",4)],ov=[("icons1",0,1,1)]),
27:dict(shots=[S("t4",4)],ov=[("icons2",0,1,1)]),
28:dict(shots=[S("t1",14)],ov=[("icons3",0,1,1)]),
29:dict(shots=[S("t3",26)],ov=[("icons4",0,1,1)]),
30:dict(shots=[S("t1",24),S("t2",17)],ov=[("icons5",0,1,1)]),
31:dict(shots=[S("t2",24),S("t2",19)],ov=[("icons6",0,1,1)]),
32:dict(shots=[S("t3",27),S("t3",8)],ov=[("icons6",0,0.45,1)],label="l_fix"),
33:dict(shots=[S("t2",9),S("t2",10),S("t4",4)],ov=[("fix0",0.12,1,1)]),
34:dict(shots=[S("t1",39),R("t2",73.7,2.1),S("t3",24)],ov=[("fix1",0.1,1,1)]),
35:dict(shots=[S("t1",40)],ov=[("fix2",0.1,1,1)]),
36:dict(shots=[S("t4",12),S("t2",11)],ov=[("fix2",0,1,1)]),
37:dict(shots=[S("t3",9)],ov=[("fix3",0.1,1,1)]),
38:dict(shots=[S("t1",24),S("t2",34),S("t3",29)],ov=[("fix4",0.08,1,1)]),
39:dict(shots=[S("t2",30),S("t2",19),S("t3",8),S("t2",45)],ov=[("fix5",0.2,1,1)]),
40:dict(shots=[S("t1",34),S("t1",37)],label="l_hot",ch="ch5"),
41:dict(shots=[R("t3",73.3,4.0),S("t2",23)],ov=[("hot",0.2,1,1)]),
42:dict(shots=[S("t1",11),S("t2",8),S("t4",13)],ov=[("hot",0,1,1)]),
43:dict(shots=[S("t2",6)],ov=[("hot",0,0.5,1)]),
44:dict(shots=[S("t3",28),S("t2",41),S("t3",24)],ov=[("hot6",0.12,1,1)]),
45:dict(shots=[S("t4",7),S("t4",13)],ov=[("minimap",0.25,1,1)],label="l_mini"),
46:dict(shots=[S("t2",6),S("t1",32)],ov=[("minimap",0,1,1)]),
47:dict(shots=[S("t3",12),S("t3",10)],ov=[("focus",0.1,1,0)]),
48:dict(shots=[S("t5",7),S("t3",13)],ov=[("stealth",0.62,1,0)]),
49:dict(shots=[S("t4",10),R("t3",46.5,1.7)],label="l_run",ch="ch6"),
50:dict(shots=[S("t4",7),S("t2",44),S("t1",40)],ov=[("nelson",0.3,1,1)]),
51:dict(shots=[S("t1",14),R("t3",48.3,2.6),S("t4",6)],ov=[("nelson",0,0.6,1)]),
52:dict(shots=[S("t4",16),S("t2",2),S("t2",4)],ov=[("tracker",0.3,1,0)]),
53:dict(shots=[S("t1",36),S("t2",23)],label="l_k9",ch="ch7"),
54:dict(shots=[S("t2",44),S("t4",6),R("t3",48.3,2.6)],ov=[("k9",0,0.5,1)]),
55:dict(shots=[S("t2",23),S("t1",25)],ov=[("k9",0,1,1)]),
56:dict(shots=[S("t3",22),S("t2",25)],ov=[("dontshoot",0.3,1,0)]),
57:dict(shots=[S("t4",15),S("t5",7)]),
58:dict(shots=[S("t2",15),S("t1",4)],label="l_prof",ch="ch8"),
59:dict(shots=[S("t1",3),S("t2",14),S("t1",41)]),
60:dict(shots=[S("t2",17),S("t3",24),S("t3",29),S("t3",26)],ov=[("profile1",0.1,1,1)]),
61:dict(shots=[S("t3",25),S("t1",33)],ov=[("profile2",0,1,1)]),
62:dict(shots=[S("t3",27),S("t2",24),S("t2",45)]),
63:dict(shots=[S("t1",13),S("t1",1),S("t2",21)],ov=[("unknown",0.1,1,1)],label="l_unk"),
64:dict(shots=[R("t3",79.5,6.0)]),
65:dict(shots=[R("t2",105.6,3.4),S("t4",12),S("t1",37),S("t3",28),S("t2",23)],ov=[("recap",0.2,1,1)],label="l_out"),
66:dict(shots=[S("t1",8),S("t2",37),S("t1",11),S("t2",26)]),
67:dict(shots=[S("t1",18),S("t1",1),S("t3",21)],ov=[("endcard",0.05,1,1)]),
}
POOL=[S("t1",16),S("t1",9),S("t1",7),S("t2",43),S("t5",6),S("t3",21),S("t2",1),S("t2",21),S("t3",1),R("t1",11.0,2.3),S("t4",17),S("t1",18),S("t2",12),S("t1",2),S("t2",20),S("t3",2),S("t3",3),S("t4",9),S("t2",38),S("t3",19),S("t1",10),S("t1",17),S("t2",9),S("t3",5),S("t2",27),S("t3",14)]
FPS=30
def spans():
    T=json.load(open("timing.json")); ls=T["lines"]; out=[]
    for i,l in enumerate(ls):
        a=0 if i==0 else max(0,l["start"]-0.12); b=(ls[i+1]["start"]-0.12) if i+1<len(ls) else T["total"]
        out.append((round(a*FPS)/FPS,round(b*FPS)/FPS))
    return T,out
_crop={}
def crop_of(k):
    if k not in _crop:
        o=subprocess.run(["ffmpeg","-v","info","-ss","30","-t","20","-i",f"src/{k}.mp4","-vf","cropdetect=24:2:0","-f","null","-"],capture_output=True,text=True).stderr
        c=re.findall(r"crop=([0-9:]+)",o); from collections import Counter
        _crop[k]=Counter(c).most_common(1)[0][0] if c else "1920:1080:0:0"
    return _crop[k]
def bg():
    T,sp=spans(); os.makedirs("bg",exist_ok=True); pool=list(POOL); pi=0; files=[]
    for i,(a,b) in enumerate(sp):
        need=b-a; shots=list(P[i]["shots"])
        while sum(s[2] for s in shots)/0.6 < need: shots.append(pool[pi%len(pool)]); pi+=1
        tot=sum(s[2] for s in shots); acc=0
        for j,(k,ss,ln) in enumerate(shots):
            d=round((need*ln/tot)*FPS)/FPS if j<len(shots)-1 else round((need-acc)*FPS)/FPS
            acc+=d
            if d<=0: continue
            sp_=min(1.0,max(0.5,ln/d)); f=f"bg/l{i:02d}_{j}.mp4"; files.append(f)
            if os.path.exists(f): continue
            vf=f"crop={crop_of(k)},scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setpts=PTS/{sp_:.4f},fps={FPS},tpad=stop_mode=clone:stop_duration=3,trim=duration={d:.4f},setsar=1,format=yuv420p"
            r=subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{ss:.3f}","-t",f"{ln:.3f}","-i",f"src/{k}.mp4","-an","-vf",vf,"-frames:v",str(round(d*FPS)),"-c:v","libx264","-preset","veryfast","-crf","17","-g","30",f+".tmp.mp4"])
            if r.returncode==0: os.rename(f+".tmp.mp4",f)
            else: print("FAIL",f)
    open("bg/list.txt","w").write("".join(f"file '{os.path.abspath(x)}'\n" for x in files))
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i","bg/list.txt","-c","copy","bg_all.mp4"],check=True)
    print("bg",dur("bg_all.mp4"),"target",T["total"],len(files))
KEY=set("shirt haircut car gun six five witness hollow ghost solid flashing red hot area icons icon notebook clothes face weapon camera cctv couple split star stars entire map blips eyes focus stealth impossible hypercar motorcycle trackers dogs dog k-9 shepherd criminal profile ruthless smart november nineteenth subscribe magic timer alarm tracker mask respray fire four legs biggest rockstar leonida".split())
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
def overlay():
    T,sp=spans(); total=T["total"]; os.makedirs("ov",exist_ok=True)
    events=[] # (name,a,b,blur,mode)
    lab=None; labs=[]
    for i,(a,b) in enumerate(sp):
        p=P[i]
        if p.get("label"):
            if lab: labs.append((lab[0],lab[1],a))
            lab=(p["label"],a)
        if p.get("ch"): events.append((p["ch"],a+0.05,min(b,a+2.0),0,""))
        for o in p.get("ov",[]):
            events.append((o[0],a+(b-a)*o[1],a+(b-a)*o[2],o[3],o[4] if len(o)>4 else ""))
    labs.append((lab[0],lab[1],total))
    # merge adjacent identical overlays
    events.sort(key=lambda e:(e[0],e[1])); merged=[]
    for e in events:
        if merged and merged[-1][0]==e[0] and merged[-1][4]==e[4] and abs(merged[-1][2]-e[1])<0.02: merged[-1]=(e[0],merged[-1][1],e[2],e[3],e[4])
        else: merged.append(e)
    events=merged+[(n,a+ (0.0 if a==0 else 2.05 if any(P[i].get("ch") and abs(sp[i][0]-a)<0.01 for i in P) else 0),b,0,"") for n,a,b in labs]
    json.dump(events,open("ov/events.json","w"))
    CH=60.0; n=int(total//CH)+1; outs=[]
    for c in range(n):
        t0=c*CH; t1=min(total,t0+CH)
        if t1-t0<0.05: continue
        out=f"ov/c{c:02d}.mp4"; outs.append(out)
        if os.path.exists(out): continue
        ass(t0,t1,f"ov/c{c:02d}.ass")
        ev=[e for e in events if e[2]>t0 and e[1]<t1]
        inputs=["-ss",f"{t0:.4f}","-t",f"{t1-t0:.4f}","-i","bg_all.mp4"]; fc=[]; last="[0:v]"
        blurs=[(max(e[1],t0)-t0,min(e[2],t1)-t0) for e in ev if e[3]]
        if blurs:
            cond="+".join(f"between(t,{a:.3f},{b:.3f})" for a,b in blurs); fc.append(f"{last}gblur=sigma=14:steps=2:enable='{cond}'[bl]"); last="[bl]"
        names=["logo","src"]+[e[0] for e in ev]; wins=[(0,t1-t0,""),(0,t1-t0,"")]+[(max(e[1],t0)-t0,min(e[2],t1)-t0,e[4]) for e in ev]
        for k,(nm,(a,b,mode)) in enumerate(zip(names,wins),1):
            inputs+=["-i",f"gfx/{nm}.png"]
            en=f"between(t,{a:.3f},{b:.3f})"
            if mode=="flashA": en+="*lt(mod(t,0.7),0.35)"
            if mode=="flashB": en+="*gte(mod(t,0.7),0.35)"
            fc.append(f"{last}[{k}:v]overlay=0:0:enable='{en}'[v{k}]"); last=f"[v{k}]"
        fc.append(f"{last}subtitles=ov/c{c:02d}.ass:fontsdir=fonts,format=yuv420p[out]")
        cmd=["ffmpeg","-v","error","-y"]+inputs+["-filter_complex",";".join(fc),"-map","[out]","-t",f"{t1-t0:.4f}","-r",str(FPS),"-c:v","libx264","-preset","veryfast","-crf","19","-g","60","-pix_fmt","yuv420p",out+".tmp.mp4"]
        r=subprocess.run(cmd,capture_output=True,text=True)
        if r.returncode==0: os.rename(out+".tmp.mp4",out); print("done",out,flush=True)
        else: print("FAIL",out,r.stderr[-800:],flush=True)
    open("ov/list.txt","w").write("".join(f"file '{os.path.abspath(x)}'\n" for x in outs))
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i","ov/list.txt","-c","copy","video_silent.mp4"],check=True); print("video",dur("video_silent.mp4"))
def audio(music="eighties_action"):
    T=json.load(open("timing.json")); total=T["total"]
    fc=f"[0:a][3:a][1:a][4:a][2:a]concat=n=5:v=0:a=1,loudnorm=I=-15:TP=-1.5:LRA=11,aresample=48000,apad=whole_dur={total:.3f},asplit=2[v1][v2];[5:a]aresample=48000,volume=0.16,afade=t=in:d=1.5,afade=t=out:st={total-3:.2f}:d=3[m];[m][v1]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[md];[md][v2]amix=inputs=2:normalize=0:duration=longest,atrim=duration={total:.3f}[a]"
    cmd=["ffmpeg","-v","error","-y","-i","audio/pA.wav","-i","audio/pB.wav","-i","audio/pC.wav","-f","lavfi","-t",str(GAP),"-i","anullsrc=r=24000:cl=mono","-f","lavfi","-t",str(GAP),"-i","anullsrc=r=24000:cl=mono","-stream_loop","-1","-i",f"audio/{music}.mp3","-filter_complex",fc,"-map","[a]","-c:a","aac","-b:a","192k","mix.m4a"]
    subprocess.run(cmd,check=True); print("audio",dur("mix.m4a"))
def mux(name="FiveStarIntel_GTA6_Police_EN_v1.mp4"):
    subprocess.run(["ffmpeg","-v","error","-y","-i","video_silent.mp4","-i","mix.m4a","-map","0:v","-map","1:a","-c:v","copy","-c:a","copy","-shortest","-movflags","+faststart",name],check=True); print(name,dur(name),os.path.getsize(name)//1e6,"MB")
if __name__=="__main__":
    for st in sys.argv[1:]:
        if st!="timing": globals()[st]()
