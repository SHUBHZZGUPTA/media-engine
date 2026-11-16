import subprocess, json, sys, os, re
from PIL import Image, ImageDraw, ImageFilter
import glass as G, gfx, build
from gfx import FB,FA,FS,FI,emoji,YEL,WHITE,RED,GREEN,CYAN,PINK,W,H
T=json.load(open("timing.json")); Ls=T["lines"]; Ws=T["words"]; TOTAL=T["total"]; FPS=30
ST=G.STYLES["C"]; R="real/"
st=lambda i:Ls[i]["start"]; en=lambda i:Ls[i]["end"]
nrm=lambda w: re.sub(r"[^a-z0-9]","",w.lower())
def wt(line,key,nth=1):
    c=0
    for w in Ws:
        if w["line"]==line and nrm(w["w"]).startswith(key):
            c+=1
            if c==nth: return w["s"]
    raise KeyError((line,key))
ease=lambda x:x*x*(3-2*x)
ic=lambda n: Image.open(R+f"icon_{n}.png")
def fit(im,size):
    r=size/max(im.size); return im.resize((max(1,int(im.width*r)),max(1,int(im.height*r))),Image.LANCZOS)
def fade(ly,a):
    if a<1: ly.putalpha(ly.getchannel("A").point(lambda v:int(v*a)))
    return ly
def tile(ly,x,y,hw,hh,state):
    t=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(t); box=(x-hw,y-hh,x+hw,y+hh)
    if state=="active":
        g=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(g).rounded_rectangle((box[0]-10,box[1]-10,box[2]+10,box[3]+10),30,fill=(255,220,40,150)); t.alpha_composite(g.filter(ImageFilter.GaussianBlur(14))); d=ImageDraw.Draw(t)
    col={"active":(255,214,30,255),"done":(60,220,120,255)}.get(state,(255,255,255,150))
    d.rounded_rectangle(box,24,fill=(255,255,255,54 if state=="active" else 34),outline=col,width=7 if state=="active" else 3); ly.alpha_composite(t)
    if state=="done":
        d=ImageDraw.Draw(ly); d.line((x+hw-34,y-hh+16,x+hw-24,y-hh+26),fill=(60,220,120,255),width=6); d.line((x+hw-24,y-hh+26,x+hw-8,y-hh+6),fill=(60,220,120,255),width=6)

class IconCard:
    """Big glass card with a row of tiles; reveals + highlights synced to speech; optional minimise to a left rail."""
    def __init__(s,title,items,t_in,t_out,t_min=None,rail_title="",foot="",state=None,big=None):
        s.title,s.items,s.t_in,s.t_out,s.t_min,s.rail_title,s.foot=title,items,t_in,t_out,t_min,rail_title,foot
        s.n=len(items); s.state=state or (lambda t,i:None); s.cache={}
        gap=226 if s.n>=5 else (300 if s.n==4 else 400); s.gap=gap; bw=max(900,gap*s.n+70)
        s.BIG=big or ((W-bw)//2,250,(W+bw)//2,740 if foot else 710)
        rh=112 if s.n>=5 else 150; s.rh=rh; s.RAIL=(36,158,236,158+62+rh*s.n+ (0 if s.n>=5 else 10))
        s.bigim=[fit(it["img"],it.get("size",120)) for it in items]; s.smallim=[fit(it["img"],it.get("rsize",70)) for it in items]
    def active(s,t): return s.t_in<=t<s.t_out
    def big_state(s,t,i):
        it=s.items[i]
        if t<it["rv"]: return "hidden"
        return "active" if it["on"]<=t<it["off"] else "shown"
    def big_layer(s,t):
        key=("b",)+tuple(s.big_state(t,i) for i in range(s.n))
        if key not in s.cache:
            ly=Image.new("RGBA",(W,H),(0,0,0,0)); x0,y0,x1,y1=s.BIG; G.txt(ly,(W//2,y0+72),s.title,FB(76),fill=YEL)
            xs=W//2-s.gap*(s.n-1)/2
            for i,it in enumerate(s.items):
                x=int(xs+i*s.gap); y=y0+250; stt=key[1+i]
                tile(ly,x,y,88,88,"active" if stt=="active" else None)
                if stt=="hidden": G.txt(ly,(x,y),"?",FB(100),fill=(235,230,250),stroke=3,a=170)
                else:
                    im=s.bigim[i]; ly.alpha_composite(im,(x-im.width//2,y-im.height//2)); G.txt(ly,(x,y+128),it["label"],FB(44),fill=(YEL if stt=="active" else WHITE))
            if s.foot: G.txt(ly,(W//2,y1-36),s.foot,FI(19),fill=(240,236,250),stroke=2,a=210)
            s.cache[key]=ly
        return s.cache[key]
    def rail_layer(s,t):
        key=("r",)+tuple(s.state(t,i) for i in range(s.n))
        if key not in s.cache:
            ly=Image.new("RGBA",(W,H),(0,0,0,0)); G.txt(ly,(136,190),s.rail_title,FB(30),fill=YEL,stroke=3)
            for i,it in enumerate(s.items):
                y=262+i*s.rh; stt=key[1+i]; tile(ly,136,y,40 if s.n>=5 else 62,40 if s.n>=5 else 40,stt)
                im=s.smallim[i]; ly.alpha_composite(im,(136-im.width//2,y-im.height//2)); G.txt(ly,(136,y+56),it["label"],FB(24),fill=(YEL if stt=="active" else WHITE),stroke=3)
            s.cache[key]=ly
        return s.cache[key]
    def draw(s,fr,t):
        u=t-s.t_in
        if u<0.3:
            k=ease(u/0.3); fr=G.glass(fr,s.BIG,ST,alpha=k); fr.alpha_composite(fade(s.big_layer(t).copy(),k)); return fr
        if s.t_min is None or t<s.t_min:
            if s.t_out-t<0.25:
                k=max(0,(s.t_out-t)/0.25); fr=G.glass(fr,s.BIG,ST,alpha=k); fr.alpha_composite(fade(s.big_layer(t).copy(),k)); return fr
            fr=G.glass(fr,s.BIG,ST); fr.alpha_composite(s.big_layer(t)); return fr
        M=0.55
        if t<s.t_min+M:
            k=ease((t-s.t_min)/M); box=tuple(s.BIG[i]+(s.RAIL[i]-s.BIG[i])*k for i in range(4)); fr=G.glass(fr,box,ST,r=int(40-8*k))
            if k<0.45: fr.alpha_composite(fade(s.big_layer(t).copy(),1-k/0.45))
            if k>0.55: fr.alpha_composite(fade(s.rail_layer(t).copy(),(k-0.55)/0.45))
            return fr
        k=min(1,max(0,(s.t_out-t)/0.3)); fr=G.glass(fr,s.RAIL,ST,alpha=k,r=32); ly=s.rail_layer(t); fr.alpha_composite(ly if k>=1 else fade(ly.copy(),k)); return fr

class Callout:
    """Compact glass panel in the lower third: icon + heading + main line (+ sub), or heading + chips revealed in sync."""
    def __init__(s,t_in,t_out,head,main="",sub="",icon=None,chips=None,headcol=YEL,width=None):
        s.t_in,s.t_out,s.head,s.main,s.sub,s.icon,s.chips,s.headcol=t_in,t_out,head,main,sub,(fit(icon,108) if icon is not None else None),chips,headcol; s.cache={}
        d=ImageDraw.Draw(Image.new("RGB",(4,4)))
        tw=max(d.textlength(head,font=FB(52)),d.textlength(main,font=FA(60)) if main else 0,d.textlength(sub,font=FI(26)) if sub else 0)
        if chips: tw=max(tw,sum(d.textlength(c[0],font=FB(40))+56 for c in chips)+18*(len(chips)-1))
        w=width or int(tw+(150 if s.icon else 0)+110); w=min(max(w,620),1500); s.h=200 if (sub or chips) else 170
        s.box=((W-w)//2,888-s.h,(W+w)//2,888)
    def active(s,t): return s.t_in<=t<s.t_out
    def layer(s,t):
        key=tuple((t>=c[1], c[1]<=t<c[2]) for c in s.chips) if s.chips else (t>=s.t_in+0.45,)
        if key not in s.cache:
            ly=Image.new("RGBA",(W,H),(0,0,0,0)); x0,y0,x1,y1=s.box; tx=x0+50
            if s.icon: ly.alpha_composite(s.icon,(x0+38,(y0+y1)//2-s.icon.height//2)); tx=x0+38+s.icon.width+30
            G.txt(ly,(tx,y0+48),s.head,FB(52),fill=s.headcol,anchor="lm")
            if s.chips:
                d=ImageDraw.Draw(ly); cx=tx
                for (txt_,rv,off),(shown,act) in zip(s.chips,key):
                    wd=int(d.textlength(txt_,font=FB(40)))+40
                    if shown:
                        c=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(c).rounded_rectangle((cx,y0+92,cx+wd,y0+160),18,fill=(255,255,255,60 if act else 34),outline=((255,214,30,255) if act else (255,255,255,150)),width=6 if act else 3); ly.alpha_composite(c)
                        G.txt(ly,(cx+wd//2,y0+126),txt_,FB(40),fill=(YEL if act else WHITE),stroke=3)
                    cx+=wd+18
            else:
                if s.main and key[0]: G.txt(ly,(tx,y0+(112 if s.sub else 116)),s.main,FA(60),anchor="lm")
                if s.sub and key[0]: G.txt(ly,(tx,y0+168),s.sub,FI(26),fill=(240,236,250),anchor="lm",stroke=2,a=225)
            s.cache[key]=ly
        return s.cache[key]
    def draw(s,fr,t):
        k=min(ease(min(1,(t-s.t_in)/0.28)),min(1,max(0,(s.t_out-t)/0.22))); fr=G.glass(fr,s.box,ST,alpha=k,r=34); ly=s.layer(t); fr.alpha_composite(ly if k>=1 else fade(ly.copy(),k)); return fr

class EndCard:
    def __init__(s,t_in,t_out):
        s.t_in,s.t_out=t_in,t_out; s.box=(330,170,1590,850); ly=Image.new("RGBA",(W,H),(0,0,0,0))
        lg=Image.open("/mnt/user-data/uploads/969a9829-image.png").convert("RGBA").resize((500,500),Image.LANCZOS)
        for c in ((0,0),(499,0),(0,499),(499,499)): ImageDraw.floodfill(lg,c,(0,0,0,0),thresh=40)
        ly.alpha_composite(lg,(410,260)); G.txt(ly,(1250,410),"SUBSCRIBE",FA(150),fill=YEL); G.txt(ly,(1250,550),"FIVE STAR INTEL",FB(96)); G.txt(ly,(1250,650),"MORE GTA 6 EVERY WEEK",FI(36),fill=(240,236,250),stroke=3); s.ly=ly
    def active(s,t): return s.t_in<=t<s.t_out
    def draw(s,fr,t):
        k=ease(min(1,(t-s.t_in)/0.3)); fr=G.glass(fr,s.box,ST,alpha=k); fr.alpha_composite(s.ly if k>=1 else fade(s.ly.copy(),k)); return fr

def item(img,label,rv,on=None,off=None,**kw): return dict(img=img,label=label,rv=rv,on=rv if on is None else on,off=off if off is not None else 1e9,**kw)
def seq(items):
    for a,b in zip(items,items[1:]): a["off"]=b["on"]
    return items
E=[]
# 1 GTA 5 old way
a=seq([item(emoji("👀",150),"LINE OF SIGHT",wt(9,"break")),item(emoji("🗺",150),"VISION CONES",wt(9,"stay")),item(emoji("⏱",150),"WAIT",wt(9,"wait"))]); a[-1]["off"]=en(9)+0.5
E.append(IconCard("GTA 5  ·  THE OLD WAY",a,wt(9,"break")-0.5,en(10)+0.2,t_min=en(9)+0.5,rail_title="GTA 5"))
# 2 witnesses
a=seq([item(emoji("📞",150),"WITNESS",wt(13,"witness")),item(emoji("🚨",150),"ALARM",wt(13,"alarm")),item(emoji("📡",150),"TRACKER",wt(13,"tracker"))]); a[-1]["off"]=en(13)+0.4
E.append(IconCard("NO REPORT  =  NO WANTED LEVEL",a,wt(13,"witness")-0.5,en(14)+0.1,t_min=en(13)+0.4,rail_title="REPORTED BY"))
# 3 hollow stars
hol,whi,red,six=[Image.open(R+f"stars_{n}.png") for n in ("hollow","white","red","six")]
E.append(Callout(wt(15,"hollow")-0.2,st(17)+2.6,"HOLLOW STARS","REPORTED. NOT IDENTIFIED.","Leave before the police arrive and they find an empty scene",icon=hol))
# 4 star states
a=[item(hol,"HOLLOW",st(19)-0.1,st(19),st(20),size=150,rsize=92),item(whi,"SOLID WHITE",st(19)-0.1,st(20),st(21),size=160,rsize=110),item(whi,"FLASHING",st(19)-0.1,st(21),st(22),size=160,rsize=110),item(red,"RED",st(19)-0.1,st(22),en(22)+0.3,size=160,rsize=110)]
lines4={0:19,1:20,2:21,3:22}
E.append(IconCard("THE 4 STAR STATES",a,st(19)-0.1,en(22)+0.3,t_min=st(20)-0.15,rail_title="STAR STATES",foot="STARS: OFFICIAL GTA 6 FOOTAGE",state=lambda t,i:"active" if st(lines4[i])<=t<(st(lines4[i]+1) if i<3 else en(22)+0.3) else None))
E.append(Callout(st(20)+0.1,st(21)-0.1,"SOLID WHITE","IDENTIFIED. EYES ON YOU.","This is the chase",icon=whi))
E.append(Callout(st(21)+0.1,st(22)-0.1,"FLASHING WHITE","LOST SIGHT OF YOU","Searching the last place they saw you",icon=whi))
E.append(Callout(st(22)+0.1,en(22)+0.2,"RED","ESCAPED, BUT IN A HOT AREA","More on Hot Areas in a minute",icon=red,headcol=(255,90,90)))
# 5 six stars
E.append(Callout(wt(23,"stars")-0.2,en(23)+0.3,"THE SIXTH STAR IS BACK","GTA 5: FIVE STARS   →   GTA 6: SIX",icon=six))
# 6 the six clues + fixes
names=["looks","clothes","vehicle","weapon","cctv","partner"]; labels=["LOOKS","CLOTHES","VEHICLE","WEAPON","CCTV","PARTNER"]
a=seq([item(ic(n),l,st(26+i)-0.05) for i,(n,l) in enumerate(zip(names,labels))]); a[-1]["off"]=en(31)+0.3
fixline={1:(33,33),0:(34,34),2:(35,36),3:(37,37),4:(38,38),5:(39,39)}
def fixstate(t,i):
    a_,b_=fixline[i]
    if st(a_)<=t<en(b_)+0.2: return "active"
    return "done" if t>=en(b_)+0.2 else None
E.append(IconCard("WHAT THE POLICE KNOW",a,st(25)+1.6,en(39)+0.4,t_min=st(32)+2.3,rail_title="POLICE KNOW",foot="ICONS: OFFICIAL GTA 6 FOOTAGE",state=fixstate))
FX=[(33,33,"clothes","CLOTHES KNOWN?","CHANGE YOUR OUTFIT","Clothing store, or a spare outfit in your car trunk"),(34,34,"looks","FACE KNOWN?","HAIRCUT, OR MASK UP FIRST","A mask before the crime limits what witnesses see"),(35,36,"vehicle","CAR KNOWN?","DUMP IT, SWAP IT, RESPRAY IT","Preview demo: icon gone, cruiser drove straight past"),(37,37,"weapon","WEAPON KNOWN?","STASH IT",""),(38,38,"cctv","ON CAMERA?","DESTROY THE FOOTAGE","Extended Look: the crew burns the getaway car"),(39,39,"partner","LOOKING FOR A COUPLE?","SPLIT UP","Reports say it can drop one star")]
for a_,b_,n,h,m,sub in FX: E.append(Callout(st(a_)+0.1,en(b_)+0.35,h,m,sub,icon=ic(n)))
# 7 hot areas
mp=Image.new("RGBA",(150,150),(0,0,0,0)); d=ImageDraw.Draw(mp); d.rounded_rectangle((0,0,149,149),22,fill=(34,60,92,255))
for gx in range(12,140,34):
    for gy in range(12,140,34): d.rounded_rectangle((gx,gy,gx+24,gy+24),4,fill=(58,92,128,255))
ov=Image.new("RGBA",(150,150),(0,0,0,0)); ImageDraw.Draw(ov).ellipse((22,22,128,128),fill=(255,60,60,120)); ImageDraw.Draw(ov).ellipse((48,48,102,102),fill=(255,30,30,200)); mp.alpha_composite(ov)
E.append(Callout(wt(41,"hot")-0.3,st(43)+3.2,"HOT AREA","POLICE STAY, WITH YOUR DESCRIPTION","Come back matching it and the chase restarts  ·  map is an illustration",icon=mp,headcol=(255,90,90)))
E.append(Callout(st(44)+0.6,en(44)+0.3,"SIX STARS","THE WHOLE MAP IS A HOT AREA","Nowhere to cool off",icon=six,headcol=(255,90,90)))
# 8 minimap, focus
E.append(Callout(wt(45,"every")-0.2,en(46)+0.2,"GTA 5: EVERY COP WAS A BLIP","GTA 6: NO BLIPS. USE YOUR EYES."))
E.append(Callout(st(47)+0.4,en(47)+0.3,"FOCUS ABILITY","HIGHLIGHTS NEARBY OFFICERS","Even through walls, but you have to choose to use it",headcol=CYAN))
# 9 outrun
E.append(Callout(wt(50,"three")-0.3,st(51)+3.6,"3 STARS OR HIGHER","NORMAL CAR = NEARLY IMPOSSIBLE","Per Rob Nelson, Rockstar North  ·  paraphrased from previews",icon=whi))
E.append(Callout(wt(52,"modern")-0.2,en(52)+0.3,"STOLEN CARS CAN HAVE TRACKERS","THE WRONG ONE REPORTS ITSELF",icon=emoji("📡",108)))
# 10 K-9
E.append(Callout(wt(54,"k")-0.2,en(55)+0.2,"K-9 UNITS","POLICE DOGS JOIN THE CHASE","Source: Edge magazine preview, as reported by GameSpot",icon=emoji("🐕",108)))
# 11 criminal profile
E.append(Callout(wt(60,"play")-0.2,en(60)+0.25,"PLAY RUTHLESS",chips=[("WITNESSES CALL FASTER",wt(60,"witnesses"),wt(60,"armed")),("CITIZENS FIGHT BACK",wt(60,"armed"),wt(60,"rival")),("GANGS ATTACK ON SIGHT",wt(60,"rival"),en(60)+0.25)],headcol=(255,90,90)))
E.append(Callout(st(61)+0.1,en(61)+0.25,"PLAY SMART","LEONIDA GOES EASIER ON YOU","Scare people instead of shooting them",headcol=(90,230,140)))
# 12 unknowns
E.append(Callout(wt(63,"we")-0.2,en(63)+0.3,"STILL UNKNOWN",chips=[("WHICH CRIMES = WHICH STAR?",wt(63,"we"),wt(63,"nobody")),("WHAT COMES AT SIX STARS?",wt(63,"nobody"),en(63)+0.3)],headcol=CYAN))
# 13 recap
a=seq([item(ic("looks"),"FACE",wt(65,"face")),item(ic("clothes"),"CLOTHES",wt(65,"clothes")),item(ic("vehicle"),"CAR",wt(65,"car")),item(ic("weapon"),"WEAPON",wt(65,"weapon")),item(ic("partner"),"PARTNER",wt(65,"partner")),item(emoji("🐕",120),"+ A DOG",wt(65,"dog"))]); a[-1]["off"]=en(65)+0.3
E.append(IconCard("GTA 6 POLICE KNOW YOUR...",a,wt(65,"face")-0.6,en(65)+0.3))
# 14 end card
E.append(EndCard(st(67)+0.3,TOTAL+1))

# ---- persistent chrome + kept overlays (chapter cards, stamps) ----
_,SP=build.spans()
KEEP={"hook1","hook2","intro_logo","throws","ghost","stealth","dontshoot"}|{f"ch{i}" for i in range(1,9)}
OV=[]; LAB=[]; cur=None
for i,(a_,b_) in enumerate(SP):
    p=build.P[i]
    if p.get("label"):
        if cur: LAB.append((cur[0],cur[1],a_))
        cur=(p["label"],a_)
    if p.get("ch"): OV.append((p["ch"],a_+0.05,min(b_,a_+2.0)))
    for o in p.get("ov",[]):
        if o[0] in KEEP: OV.append((o[0],a_+(b_-a_)*o[1],a_+(b_-a_)*o[2]))
LAB.append((cur[0],cur[1],TOTAL+1))
LABTXT={"l_intro":("FIVE STAR INTEL","The New GTA 6 Police"),"l_old":("REWIND","GTA 5: The Old Way"),"l_wit":("RULE 1","No Witness, No Problem"),"l_states":("THE WANTED LEVEL","4 Star States"),"l_icons":("THE NOTEBOOK","What Police Know"),"l_fix":("ESCAPE","Erase the Clues"),"l_hot":("AFTER THE CHASE","Hot Areas"),"l_mini":("NO MORE BLIPS","Find Them Yourself"),"l_run":("OUTRUN THEM?","Good Luck"),"l_k9":("NEW","K-9 Units"),"l_prof":("THE LONG GAME","Criminal Profile"),"l_unk":("NOT CONFIRMED YET","Still Unknown"),"l_out":("RECAP","Smarter Than Ever")}
GTA5_LINES=(7,8,9,10)
_chrome={}
def chrome(t):
    lab=next(n for n,a_,b_ in LAB if a_<=t<b_); g5=st(7)-0.12<=t<st(11)-0.12 or (st(45)-0.12<=t<st(45)+ (SP[45][1]-SP[45][0]))
    hide_label=any(n.startswith("ch") and a_<=t<b_ for n,a_,b_ in OV)
    key=(lab,g5,hide_label)
    if key not in _chrome:
        ly=Image.new("RGBA",(W,H),(0,0,0,0)); ly.alpha_composite(Image.open("gfx/logo.png"))
        if not hide_label:
            sm,bg=LABTXT[lab]; d=ImageDraw.Draw(ly); d.rectangle((44,28,104,30),fill=YEL+(255,)); G.txt(ly,(44,46),sm,FI(22),fill=YEL,anchor="lm",stroke=3); G.txt(ly,(44,88),bg,FS(46),anchor="lm",stroke=4)
            G.txt(ly,(44,128),"Footage: Rockstar Games official "+("GTA V gameplay video" if g5 else "trailers and Extended Look"),FI(17),fill=(235,235,245),anchor="lm",stroke=2,a=215)
        _chrome[key]=ly
    return _chrome[key]
_ovc={}
def ovimg(n):
    if n not in _ovc: _ovc[n]=Image.open(f"gfx/{n}.png").convert("RGBA")
    return _ovc[n]
def compose(fr,t):
    for e in E:
        if e.active(t): fr=e.draw(fr,t)
    for n,a_,b_ in OV:
        if a_<=t<b_: fr.alpha_composite(ovimg(n))
    fr.alpha_composite(chrome(t)); return fr
def render(path,t0,t1):
    n=round((t1-t0)*FPS)
    inp=subprocess.Popen(["ffmpeg","-v","error","-ss",f"{t0:.4f}","-i","bg_all.mp4","-frames:v",str(n),"-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
    assf=path+".ass"; build.ass(t0,t1,assf)
    out=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-vf",f"subtitles={assf}:fontsdir=fonts:force_style='MarginV=40',format=yuv420p","-frames:v",str(n),"-c:v","libx264","-preset","veryfast","-crf","19","-g","60",path+".tmp.mp4"],stdin=subprocess.PIPE)
    for f in range(n):
        raw=inp.stdout.read(W*H*3)
        if len(raw)<W*H*3: print("short read at",f,flush=True); break
        fr=compose(Image.frombytes("RGB",(W,H),raw).convert("RGBA"),t0+f/FPS); out.stdin.write(fr.convert("RGB").tobytes())
        if f%900==0: print(path,f,"/",n,flush=True)
    out.stdin.close(); rc=out.wait(); inp.kill()
    if rc==0: os.rename(path+".tmp.mp4",path); print("done",path,flush=True)
def stills(times,path):
    ims=[]
    for t in times:
        f=round(t*FPS)/FPS; fr=compose(G.frame_at(f),f); ims.append(fr.convert("RGB").resize((640,360),Image.LANCZOS))
    cols=4; sh=Image.new("RGB",(cols*640,((len(ims)+cols-1)//cols)*360))
    for i,im in enumerate(ims): sh.paste(im,((i%cols)*640,(i//cols)*360))
    sh.save(path,quality=88)
if __name__=="__main__":
    if sys.argv[1]=="stills": stills([float(x) for x in sys.argv[3:]],sys.argv[2])
    else: render(sys.argv[1],float(sys.argv[2]),float(sys.argv[3]))
