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
E=[]
E.append(Callout(wt(3,"every")-0.2,en(3)+0.3,"OFFICIAL SOURCES ONLY",chips=[("TRAILERS",wt(3,"every"),wt(3,"every",2)),("CHARACTER PAGES",wt(3,"every",2),wt(3,"full")),("EXTENDED LOOK",wt(3,"full"),wt(3,"no")),("NO LEAKS",wt(3,"no"),en(3)+0.3)]))
E.append(Callout(wt(8,"jason")-0.2,en(8)+0.3,"ROCKSTAR'S ONE-LINER","WANTS AN EASY LIFE","But things just keep getting harder"))
E.append(Callout(wt(9,"grew")-0.2,en(9)+0.25,"JASON DUVAL",chips=[("GREW UP AROUND CROOKS",wt(9,"grew"),wt(9,"joined")),("JOINED THE ARMY",wt(9,"joined"),wt(9,"launch")),("TROUBLE THERE TOO",wt(9,"launch"),en(9)+0.25)]))
E.append(Callout(wt(10,"leonida")-0.3,en(10)+0.3,"TODAY","WORKS FOR LOCAL DRUG RUNNERS","Down in the Leonida Keys"))
E.append(Callout(st(11)+0.2,en(11)+0.2,"THE DEAL","LIVES RENT FREE IN HIS BOSS'S HOUSE","In return: help with a few shakedowns"))
E.append(Callout(wt(13,"best")-0.4,en(13)+0.3,"MEETING LUCIA","THE BEST OR THE WORST THING","From Rockstar's official description of Jason",headcol=CY))
E.append(Callout(st(15)+0.2,en(15)+0.2,"LUCIA CAMINOS","TAUGHT TO FIGHT BY HER DAD","As soon as she could walk"))
E.append(Callout(wt(16,"landed")-0.3,en(16)+0.2,"WHY SHE WAS LOCKED UP","FOUGHT FOR HER FAMILY","Leonida Penitentiary  ·  seen in Trailer 1"))
E.append(Callout(st(17)+0.2,en(17)+0.2,"HOW SHE GOT OUT","SHEER LUCK","Look for the ankle monitor in the trailers"))
E.append(Callout(wt(19,"only")-0.4,en(19)+0.3,"HER RULE NOW","ONLY SMART MOVES"))
E.append(Callout(st(20)+0.3,en(20)+0.2,"THE GOAL","THE GOOD LIFE HER MOM DREAMED OF","Since their days in Liberty City"))
E.append(Callout(wt(22,"first")-0.4,en(22)+0.3,"HISTORY","FIRST WOMAN TO LEAD A MODERN GTA",headcol=CY))
E.append(Callout(wt(23,"he")-0.2,en(23)+0.3,"PUT THEM TOGETHER",chips=[("HE WANTS EASY",wt(23,"he"),wt(23,"she")),("SHE WANTS OUT",wt(23,"she"),wt(23,"and")),("HE COULD BE HER WAY OUT",wt(23,"and"),en(23)+0.3)]))
E.append(Callout(wt(25,"darkest")-0.3,en(25)+0.4,"ROCKSTAR'S OWN WORDS","THE DARKEST SIDE OF THE SUNNIEST PLACE"))
E.append(Callout(wt(27,"jason")-0.5,en(27)+0.3,"THREE WAYS TO PLAY",chips=[("AS JASON",wt(27,"jason")-0.3,wt(27,"lucia")-0.3),("AS LUCIA",wt(27,"lucia")-0.3,wt(27,"roam")),("AS A COUPLE",wt(27,"roam"),en(27)+0.3)]))
E.append(Callout(st(28)+0.2,en(28)+0.2,"IN A CHASE","ONE DRIVES, ONE SHOOTS","The partner you don't control still fights"))
E.append(PC(wt(29,"hold")-0.5,wt(29,"partner")-0.1,"REAL IN-GAME PROMPT","HOLD HANDS","Extended Look  ·  PS5 capture",prompt("p_hold")))
E.append(PC(wt(29,"partner"),en(29)+0.3,"REAL IN-GAME PROMPT","HURRY THEM UP","Extended Look  ·  PS5 capture",prompt("p_hurry",128)))
E.append(Callout(wt(30,"pick")-0.3,en(30)+0.3,"SHARED APARTMENT",chips=[("PICK OUTFITS",wt(30,"pick"),wt(30,"raid")),("RAID THE FRIDGE",wt(30,"raid"),wt(30,"watch")),("WATCH TV",wt(30,"watch"),en(30)+0.3)]))
E.append(Callout(st(31)+0.2,en(31)+0.2,"PREVIEWS SAY","TEXTS AND TIME AWAY AFFECT THE RELATIONSHIP","Reported by press previews  ·  not shown in official footage",headcol=CY))
E.append(Callout(wt(32,"hit")-0.3,en(32)+0.3,"PREVIEWS SAY",chips=[("GYM = MUSCLE",wt(32,"hit"),wt(32,"eat")),("OVEREAT = WEIGHT",wt(32,"eat"),wt(32,"skip")),("NO SLEEP SHOWS",wt(32,"skip"),en(32)+0.3)],headcol=CY))
# the six: rail
names=["CAL","BOOBIE","DRE'QUAN","REAL DIMEZ","RAUL","BRIAN"]; rng=[(34,38),(39,41),(42,44),(45,48),(49,52),(53,59)]
a=[item(numimg(i+1),nm,st(33)+0.9+i*0.28,size=130,rsize=64) for i,nm in enumerate(names)]
for it in a: it["on"]=1e9
def sixstate(t,i):
    a_,b_=rng[i]
    if st(a_)-0.12<=t<en(b_)+0.3: return "active"
    return "done" if t>=en(b_)+0.3 else None
E.append(IconCard("THE SIX PEOPLE AROUND THEM",a,st(33)+0.7,en(59)+0.4,t_min=st(34)-0.25,rail_title="THE SIX",state=sixstate))
E.append(Callout(st(35)+0.2,en(35)+0.2,"CAL HAMPTON","JASON'S FRIEND. SAME BOSS.","Deep into online conspiracies"))
E.append(Callout(wt(36,"beers")-0.5,en(36)+0.2,"CAL'S PERFECT NIGHT",chips=[("A FEW BEERS",wt(36,"beers")-0.4,wt(36,"coast")),("COAST GUARD RADIO",wt(36,"coast"),wt(36,"private")),("PRIVATE BROWSER TAB",wt(36,"private"),en(36)+0.2)]))
E.append(Callout(wt(37,"what")-0.2,en(37)+0.2,"CAL'S OFFICIAL QUOTE","WHAT IF EVERYTHING ON THE INTERNET WAS TRUE?"))
E.append(Callout(wt(40,"real")-0.3,en(40)+0.3,"BOOBIE IKE'S LEGIT EMPIRE",chips=[("REAL ESTATE",wt(40,"real"),wt(40,"strip")),("STRIP CLUB",wt(40,"strip"),wt(40,"recording")),("RECORDING STUDIO",wt(40,"recording"),en(40)+0.3)]))
E.append(Callout(st(41)+0.1,en(41)+0.3,"BOOBIE IKE","ALL SMILES, UNTIL IT'S BUSINESS"))
E.append(Callout(st(43)+0.2,en(43)+0.2,"DRE'QUAN PRIEST","MORE HUSTLER THAN GANGSTER","Music was always the dream"))
E.append(Callout(wt(44,"only")-0.4,en(44)+0.2,"ONLY RAW RECORDS","HIS LABEL. BOOBIE IS HIS PARTNER.","And they badly need a hit"))
E.append(Callout(st(46)+0.1,en(46)+0.2,"REAL DIMEZ","BAE-LUXE AND ROXY","Friends since high school"))
E.append(Callout(st(47)+0.3,en(47)+0.2,"THE CLOCK IS TICKING","FIRST HIT WAS FIVE YEARS AGO","Now: a fresh deal, and one more shot"))
E.append(Callout(st(48)-0.05,en(48)+0.3,"SEE THE CONNECTION?",chips=[("DRE'QUAN SIGNED THEM",st(48),wt(48,"boobies")),("BOOBIE'S CLUB BOOKS THEM",wt(48,"boobies"),en(48)+0.3)]))
E.append(Callout(wt(50,"confidence")-0.5,en(50)+0.3,"RAUL BAUTISTA  ·  BANK ROBBER",chips=[("CONFIDENCE",wt(50,"confidence")-0.3,wt(50,"charm")),("CHARM",wt(50,"charm"),wt(50,"cunning")),("CUNNING",wt(50,"cunning"),en(50)+0.3)]))
E.append(Callout(wt(51,"his")-0.2,en(51)+0.3,"ROCKSTAR'S WARNING","HIS RECKLESSNESS RAISES THE STAKES","On every single score",headcol=RD))
E.append(Callout(st(54)+0.2,en(54)+0.2,"BRIAN HEDER","KEYS DRUG RUNNER. JASON'S LANDLORD.","Moves product through his boat yard, with third wife Lori"))
E.append(Callout(wt(55,"brian")-0.2,en(56)+0.3,"FROM HIS OFFICIAL BIO","LETS OTHERS DO HIS DIRTY WORK","Others... like Jason",headcol=RD))
E.append(Callout(st(58)+0.1,en(58)+0.3,"MY THEORY  ·  NOT CONFIRMED","THE FREE HOUSE IS A LEASH","Jason takes the risk. Brian keeps the profit.",headcol=CY))
E.append(Callout(wt(60,"jasons")-0.2,en(60)+0.3,"ONE STORY, THREE WORLDS",chips=[("JASON: THE KEYS",wt(60,"jasons"),wt(60,"boobies")),("BOOBIE: VICE CITY",wt(60,"boobies"),wt(60,"raul")),("RAUL: BANKS",wt(60,"raul"),en(60)+0.3)]))
E.append(Callout(wt(61,"how")-0.3,en(61)+0.3,"STILL UNKNOWN",chips=[("HOW IT ENDS",wt(61,"how"),wt(61,"how",2)),("HOW LONG IT RUNS",wt(61,"how",2),wt(61,"whether")),("DO THEY MAKE IT OUT?",wt(61,"whether"),en(61)+0.3)],headcol=CY))
E.append(Callout(wt(64,"are")-0.2,en(64)+0.3,"COMMENT BELOW","JASON FIRST, OR LUCIA?","And who don't you trust?"))
E.append(EndCard(st(65)+0.3,TOTAL+1))

# ---- persistent chrome + kept overlays (chapter cards, stamps) ----
_,SP=build.spans()
KEEP={"intro_logo"}|{f"ch{i}" for i in range(1,10)}
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
LABTXT={"l_intro":("FIVE STAR INTEL","Meet Jason and Lucia"),"l_jason":("PROTAGONIST 1","Jason Duval"),"l_lucia":("PROTAGONIST 2","Lucia Caminos"),"l_play":("GAMEPLAY","Playing As Two"),"l_six":("THE CAST","Six People Around Them"),"l_cal":("1 OF 6","Cal Hampton"),"l_boobie":("2 OF 6","Boobie Ike"),"l_dre":("3 OF 6","Dre'Quan Priest"),"l_dimez":("4 OF 6","Real Dimez"),"l_raul":("5 OF 6","Raul Bautista"),"l_brian":("6 OF 6","Brian Heder"),"l_theory":("MY THEORY","Watch Brian"),"l_unk":("NOT CONFIRMED YET","Still Unknown"),"l_out":("RECAP","Before You Press Start")}
_chrome={}
def chrome(t):
    lab=next(n for n,a_,b_ in LAB if a_<=t<b_); g5=False
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

def mkgfx():
    cards=[("ch1","C H A P T E R   1","Jason Duval"),("ch2","C H A P T E R   2","Lucia Caminos"),("ch3","C H A P T E R   3","Playing As Two"),("ch4","N U M B E R   1","Cal Hampton"),("ch5","N U M B E R   2","Boobie Ike"),("ch6","N U M B E R   3","Dre'Quan Priest"),("ch7","N U M B E R   4","Real Dimez"),("ch8","N U M B E R   5","Raul Bautista"),("ch9","N U M B E R   6","Brian Heder")]
    for n,sm,big in cards:
        im=gfx.new(); gfx.text(im,(W//2,430),sm,FI(34),fill=YEL,anchor="mm",stroke=4); gfx.text(im,(W//2,540),big,FS(150),fill=WHITE,anchor="mm",stroke=8); ImageDraw.Draw(im).rectangle((W//2-90,640,W//2+90,648),fill=YEL+(255,)); im.save(f"gfx/{n}.png")
if __name__=="__main__":
    if sys.argv[1]=="gfx": mkgfx()
    elif sys.argv[1]=="stills": stills([float(x) for x in sys.argv[3:]],sys.argv[2])
    else: render(sys.argv[1],float(sys.argv[2]),float(sys.argv[3]))
