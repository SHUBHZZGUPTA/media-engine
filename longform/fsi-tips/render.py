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

def numimg(n):
    im=Image.new("RGBA",(150,150),(0,0,0,0)); d=ImageDraw.Draw(im); d.ellipse((6,6,144,144),fill=(255,214,30,255),outline=(15,6,40,255),width=6); d.text((75,80),str(n),font=FA(96),fill=(15,6,40,255),anchor="mm"); return im
def prompt(name,h=96):
    im=Image.open(f"gfx/{name}.png").convert("RGBA"); r=h/im.height; im=im.resize((int(im.width*r),h),Image.LANCZOS)
    m=Image.new("L",im.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0,im.width-1,im.height-1),18,fill=255); im.putalpha(m); return im
def PC(t0,t1,head,main,sub,img,**kw):
    c=Callout(t0,t1,head,main,sub,icon=numimg(1),**kw); c.icon=img; x0,y0,x1,y1=c.box; ex=(img.width-108)//2; c.box=(x0-ex,y0,x1+ex,y1); return c
CY=CYAN; RD=(255,90,90)

CY=CYAN; RD=(255,90,90)
def C(i,head,main=None,sub=None,t0=None,t1=None,**kw): return Callout(st(i)+0.2 if t0 is None else t0, en(i)+0.25 if t1 is None else t1, head, main, sub, **kw)
def CH(i,head,pairs,**kw):
    ts=[wt(i,k,n) for _,k,n in pairs]; lab=[p[0] for p in pairs]
    chips=[(lab[j],ts[j],ts[j+1] if j+1<len(ts) else en(i)+0.3) for j in range(len(ts))]
    return Callout(ts[0]-0.3,en(i)+0.3,head,chips=chips,**kw)
E=[]
E.append(Callout(wt(0,"ninetynine")-0.3,wt(0,"and")-0.1,"METACRITIC","99 OUT OF 100","Critic score, checked 18 Nov 2026"))
E.append(C(3,"HONESTY CHECK","THESE TIPS COME FROM REVIEWERS","Every source is on screen and in the description",headcol=CY))
E.append(CH(7,"4 ACTIVE WEAPON SLOTS  ·  EARLY HANDS-ON REPORTS",[("2 LONG GUNS","two",1),("1 PISTOL","one",1),("1 MELEE WEAPON","one",2)]))
E.append(C(8,"EVERYTHING ELSE","STAYS IN YOUR CAR OR SAFEHOUSE","Pick your loadout before the mission"))
E.append(C(9,"GOOD NEWS","SWAP YOUR TWO MAIN GUNS INSTANTLY","No weapon wheel needed  ·  seen in the Extended Look",headcol=CY))
E.append(CH(12,"SHOVE IT  ·  PLAYSTATION",[("WALK INTO THE CAR","walk",1),("KEEP WALKING","keep",1),("HOLD SQUARE","hold",1)]))
E.append(C(13,"ALSO WORKS ON","FLIPPED CARS AND BEACHED BOATS","Source: 140-hour hands-on guide, The Big Lead"))
E.append(C(14,"WHY FREE MATTERS","CARS ARE FRAGILE. REPAIRS COST MONEY.","Mentioned across launch reviews"))
E.append(C(16,"WHILE DRIVING","PRESS SQUARE = DOOR ATTACK","Source: hands-on guide, The Big Lead"))
E.append(C(17,"ON A MOTORBIKE","IT BECOMES A KICK"))
E.append(CH(19,"SLIM JIM  ·  SEEN IN THE EXTENDED LOOK",[("PRESS TRIANGLE","triangle",1),("RIGHT STICK: 3 TO 9 O'CLOCK","sweep",1)]))
E.append(CH(20,"DO IT CLEAN",[("NO BROKEN GLASS","no",1),("NO ALARM","no",2),("NO WITNESS","no",3)]))
E.append(CH(22,"OPEN THE CAR MENU",[("HOLD D-PAD LEFT","hold",1),("PUSH STICK UP","push",1)]))
E.append(CH(23,"WHAT'S IN THE MENU",[("WINDOWS","windows",1),("HIGH BEAMS","high",1),("HAZARDS","hazard",1),("ROOF","roof",1)]))
E.append(C(24,"TURN SIGNALS","TAP D-PAD LEFT OR RIGHT","Does absolutely nothing. Still great."))
E.append(C(26,"FOCUS MODE","PRESS BOTH STICKS IN","L3 + R3 on PlayStation"))
E.append(C(27,"LOOK FOR","A RING OF SOUND ON SCREEN","It points to a unique encounter nearby"))
E.append(CH(30,"MAP COLOR CODE",[("DARK BLUE = YOU CAN ENTER","dark",1),("LIGHT BLUE = YOU CAN'T","light",1)]))
E.append(C(31,"PRO TIP","ROTATE THE MAP TO FIND THE DOORS"))
E.append(CH(33,"CASE THE JOINT",[("WALK IN AS A CUSTOMER","walk",1),("LOOK AROUND","look",1),("FIND THE ALARM","find",1)]))
E.append(CH(34,"MARK THE GUARD",[("LOCK ON","lock",1),("PRESS D-PAD RIGHT","press",1)]))
E.append(C(35,"RESULT","AN ARROW TRACKS THAT GUARD","For the whole robbery"))
E.append(CH(36,"FROM OUR POLICE VIDEO",[("NO WITNESS","no",1),("NO ALARM","no",2),("NO STARS","no",3)],headcol=CY))
E.append(C(38,"NO SAFE CODE?","YOU DON'T NEED A STICKY BOMB"))
E.append(CH(39,"ANY EXPLOSION WORKS",[("GRENADE","grenade",1),("ROCKET","rocket",1),("PROPANE TANK","propane",1)]))
E.append(CH(41,"ON THE SURFACE",[("CLICK STICK: BOOST","click",1),("CLICK AGAIN: TOP SPEED","click",2)]))
E.append(C(42,"OUT OF STAMINA?","DIVE. YOUR LUNGS TAKE OVER.","You keep top speed for longer"))
E.append(CH(44,"HIT MARKERS",[("RED = DEAD","red",1),("YELLOW = DOWN, NOT DEAD","yellow",1)]))
E.append(CH(47,"ON-SCREEN OPTIONS",[("CALM IT DOWN","calm",1),("OR WIND THEM UP","wind",1)]))
E.append(C(48,"ROCKSTAR SAYS","HOW YOU BEHAVE CHANGES HOW THE WORLD REACTS","Rob Nelson, Rockstar North, speaking to IGN",headcol=CY))
E.append(C(50,"NEW IN GTA 6","RESTART FROM THE LAST CHECKPOINT","Reported in launch reviews"))
E.append(C(53,"PERFORMANCE MODE?","NO. 30 FPS ON EVERY CONSOLE.","Including PS5 Pro, per launch reviews"))
E.append(C(54,"STORY LENGTH","50 TO 80 HOURS","Most reviewers: about 60"))
E.append(C(55,"DOES HAIR GROW?","NO. BARBER OR SAFEHOUSE."))
E.append(C(56,"ON PC?","NO PC VERSION ANNOUNCED","PS5 and Xbox Series X|S only"))
E.append(C(57,"GTA ONLINE?","NOT SHOWN TO CRITICS YET","Reviews cover the story only"))
E.append(C(58,"DOWNLOAD SIZE","OVER 200 GB","PlayStation asks for 212 GB of free space"))
c1=wt(59,"fishing"); c2=wt(59,"diving")
E.append(Callout(c1-0.3,c2-0.05,"BESIDES CRIME",chips=[("FISHING",c1,wt(59,"golf")),("GOLF",wt(59,"golf"),wt(59,"hunting")),("HUNTING",wt(59,"hunting"),c2)]))
E.append(Callout(c2,en(59)+0.3,"BESIDES CRIME",chips=[("DIVING",c2,wt(59,"bird")),("BIRD WATCHING",wt(59,"bird"),wt(59,"drone")),("DRONE RACES",wt(59,"drone"),en(59)+0.3)]))
E.append(C(61,"COMMENT BELOW","WHICH ONE ARE YOU TRYING FIRST?","Found a trick I missed? Drop it there too."))
E.append(EndCard(st(62)+0.3,TOTAL+1))

# ---- persistent chrome + kept overlays (chapter cards, stamps) ----
_,SP=build.spans()
KEEP={"intro_logo"}|{f"ch{i}" for i in range(1,14)}
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
LABTXT={'l_intro': ('FIVE STAR INTEL', '13 Things GTA 6 Never Tells You'), 'l_g5': ('GTA 5  ·  2013', 'The Old Way'), 'l_q': ('QUICK ANSWERS', '7 Questions Everyone Is Asking'), 'l_out': ('RECAP', 'Try These First'), 'l1': ('1 OF 13', 'Four Weapon Slots'), 'l2': ('2 OF 13', 'Shove Your Flipped Car'), 'l3': ('3 OF 13', 'Your Door Is a Weapon'), 'l4': ('4 OF 13', "Slim Jim, Don't Smash"), 'l5': ('5 OF 13', 'The Hidden Car Menu'), 'l6': ('6 OF 13', 'Click Both Sticks'), 'l7': ('7 OF 13', 'The Map Color Code'), 'l8': ('8 OF 13', 'Case the Joint'), 'l9': ('9 OF 13', 'Any Explosion Opens a Safe'), 'l10': ('10 OF 13', 'Swim Faster'), 'l11': ('11 OF 13', 'Yellow Is Not Dead'), 'l12': ('12 OF 13', 'Talk Your Way Out'), 'l13': ('13 OF 13', 'Retry From a Checkpoint')}
_chrome={}
def chrome(t):
    lab=next(n for n,a_,b_ in LAB if a_<=t<b_); g5=(lab=="l_g5")
    hide_label=any(n.startswith("ch") and a_<=t<b_ for n,a_,b_ in OV)
    key=(lab,g5,hide_label)
    if key not in _chrome:
        ly=Image.new("RGBA",(W,H),(0,0,0,0)); ly.alpha_composite(Image.open("gfx/logo.png"))
        if not hide_label:
            sm,bg=LABTXT[lab]; d=ImageDraw.Draw(ly); d.rectangle((44,28,104,30),fill=YEL+(255,)); G.txt(ly,(44,46),sm,FI(22),fill=YEL,anchor="lm",stroke=3); G.txt(ly,(44,88),bg,FS(46),anchor="lm",stroke=4)
            G.txt(ly,(44,128),"Footage: Rockstar Games official "+("GTA V gameplay video" if g5 else "trailers and gameplay videos"),FI(17),fill=(235,235,245),anchor="lm",stroke=2,a=215)
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

def mkgfx():
    names=['Four Weapon Slots', 'Shove Your Flipped Car', 'Your Door Is a Weapon', "Slim Jim, Don't Smash", 'The Hidden Car Menu', 'Click Both Sticks', 'The Map Color Code', 'Case the Joint', 'Any Explosion Opens a Safe', 'Swim Faster', 'Yellow Is Not Dead', 'Talk Your Way Out', 'Retry From a Checkpoint']
    for i,big in enumerate(names):
        im=gfx.new(); gfx.text(im,(W//2,430),"N U M B E R   %d"%(i+1),FI(34),fill=YEL,anchor="mm",stroke=4); gfx.text(im,(W//2,540),big,FS(128 if len(big)<22 else 104),fill=WHITE,anchor="mm",stroke=8); ImageDraw.Draw(im).rectangle((W//2-90,640,W//2+90,648),fill=YEL+(255,)); im.save(f"gfx/ch{i+1}.png")
if __name__=="__main__":
    if sys.argv[1]=="gfx": mkgfx()
    elif sys.argv[1]=="stills": stills([float(x) for x in sys.argv[3:]],sys.argv[2])
    else: render(sys.argv[1],float(sys.argv[2]),float(sys.argv[3]))
