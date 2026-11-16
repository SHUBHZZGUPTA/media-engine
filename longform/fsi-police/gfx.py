import math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H=1920,1080
INK=(22,10,51); PINK=(255,46,147); YEL=(255,210,30); CYAN=(0,213,255); WHITE=(255,255,255); RED=(255,59,59); GREEN=(46,213,115)
FB=lambda s: ImageFont.truetype("fonts/BebasNeue-Regular.ttf",s)
FA=lambda s: ImageFont.truetype("fonts/Anton-Regular.ttf",s)
FS=lambda s: ImageFont.truetype("fonts/DMSerifDisplay-Regular.ttf",s)
FI=lambda s: ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Bold.otf",s)
FE=ImageFont.truetype("/home/claude/media-engine/money-mirage/mm3/library/fonts/emoji.ttf",109)
def new(): return Image.new("RGBA",(W,H),(0,0,0,0))
def save(im,name): im.save(f"gfx/{name}.png"); return name
def emoji(ch,size):
    t=Image.new("RGBA",(150,150),(0,0,0,0)); ImageDraw.Draw(t).text((10,10),ch,font=FE,embedded_color=True)
    bb=t.getbbox(); t=t.crop(bb); r=size/max(t.size); return t.resize((max(1,int(t.width*r)),max(1,int(t.height*r))),Image.LANCZOS)
def star_pts(cx,cy,R,r=None):
    r=r or R*0.42; return [(cx+(R if i%2==0 else r)*math.cos(math.radians(-90+i*36)), cy+(R if i%2==0 else r)*math.sin(math.radians(-90+i*36))) for i in range(10)]
def star(im,cx,cy,R,style):
    d=ImageDraw.Draw(im)
    if style=="glow":
        g=new(); ImageDraw.Draw(g).polygon(star_pts(cx,cy,R*1.25),fill=(255,255,255,200)); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(14))); d=ImageDraw.Draw(im)
    pts=star_pts(cx,cy,R)
    if style=="hollow":
        d.polygon(star_pts(cx,cy,R+5),fill=INK+(255,)); d.polygon(pts,fill=WHITE+(255,)); d.polygon(star_pts(cx,cy,R-9),fill=(60,40,110,255))
    else:
        col={"solid":WHITE,"glow":WHITE,"dimflash":(150,150,170),"red":RED,"yellow":YEL,"off":(70,55,110)}[style]
        d.polygon(star_pts(cx,cy,R+5),fill=INK+(255,)); d.polygon(pts,fill=col+(255,))
def card(im,x0,y0,x1,y1,border=PINK,alpha=235):
    sh=new(); ImageDraw.Draw(sh).rounded_rectangle((x0+10,y0+14,x1+10,y1+14),36,fill=(0,0,0,110)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))
    d=ImageDraw.Draw(im); d.rounded_rectangle((x0,y0,x1,y1),36,fill=INK+(alpha,),outline=border+(255,),width=7)
def text(im,xy,s,font,fill=WHITE,anchor="la",stroke=0,sfill=INK):
    ImageDraw.Draw(im).text(xy,s,font=font,fill=fill+(255,),anchor=anchor,stroke_width=stroke,stroke_fill=sfill+(255,))
def note(im,y,s="ILLUSTRATION  ·  NOT THE REAL HUD"):
    text(im,(W//2,y),s,FI(22),fill=(190,180,220),anchor="mm")
def header(im,y,s,col=YEL): text(im,(W//2,y),s,FB(74),fill=col,anchor="mm")

# ---- persistent bits
def logo_bug():
    lg=Image.open("/home/claude/fsi_logo/five_star_intel_shield_800.png").convert("RGBA").resize((118,118),Image.LANCZOS)
    m=Image.new("L",(118,118),0); ImageDraw.Draw(m).ellipse((0,0,117,117),fill=255); im=new()
    ImageDraw.Draw(im).ellipse((36,926,36+126,926+126),fill=WHITE+(255,)); im.paste(lg,(40,930),m); save(im,"logo")
def label(name,small,big):
    im=new(); text(im,(44,34),small,FI(22),fill=YEL,stroke=3); ImageDraw.Draw(im).rectangle((44,28,104,30),fill=YEL+(255,))
    text(im,(44,62),big,FS(46),fill=WHITE,stroke=4); save(im,name)
def title_card(name,n,title):
    im=new(); text(im,(W//2,430),f"C H A P T E R   {n}",FI(34),fill=YEL,anchor="mm",stroke=4)
    text(im,(W//2,540),title,FS(150),fill=WHITE,anchor="mm",stroke=8); ImageDraw.Draw(im).rectangle((W//2-90,640,W//2+90,648),fill=YEL+(255,)); save(im,name)
def stamp(name,lines,hl=-1,y=420,size=150):
    im=new(); yy=y
    for i,s in enumerate(lines):
        f=FA(size); w=ImageDraw.Draw(im).textlength(s,font=f)
        if i==hl:
            ImageDraw.Draw(im).rounded_rectangle((W/2-w/2-30,yy-size*0.62,W/2+w/2+30,yy+size*0.62),18,fill=YEL+(255,)); text(im,(W//2,yy),s,f,fill=INK,anchor="mm")
        else: text(im,(W//2,yy),s,f,fill=WHITE,anchor="mm",stroke=10)
        yy+=int(size*1.3)
    save(im,name)

# ---- explainers
def old_way():
    im=new(); card(im,260,170,1660,800,border=CYAN); header(im,250,"GTA 5  ·  THE OLD WAY",CYAN)
    steps=[("👀","BREAK LINE OF SIGHT"),("🗺","AVOID THE CONES"),("⏱","WAIT")]
    for i,(e,s) in enumerate(steps):
        x=500+i*460; im.alpha_composite(emoji(e,170),(x-85,360)); text(im,(x,600),s,FB(60),anchor="mm")
        if i<2: text(im,(x+230,445),"→",FI(90),fill=YEL,anchor="mm")
    text(im,(W//2,715),"STARS GONE.  EVERY TIME.",FB(64),fill=YEL,anchor="mm"); save(im,"old_way")
def witness(k):
    im=new(); card(im,260,170,1660,800); header(im,250,"NO REPORT  =  NO WANTED LEVEL")
    items=[("📞","A WITNESS CALLS"),("🚨","AN ALARM TRIPS"),("📡","A CAR TRACKER PINGS")]
    for i,(e,s) in enumerate(items):
        x=500+i*460
        if i<k: im.alpha_composite(emoji(e,180),(x-90,370)); text(im,(x,640),s,FB(58),anchor="mm")
        else: ImageDraw.Draw(im).rounded_rectangle((x-90,370,x+90,550),30,fill=(60,40,110,255))
    save(im,f"witness{k}")
STATES=[("hollow","HOLLOW","REPORTED. THEY DON'T KNOW IT'S YOU."),("solid","SOLID WHITE","IDENTIFIED. EYES ON YOU. THE CHASE."),("glow","FLASHING WHITE","LOST SIGHT. SEARCHING YOUR LAST SPOT."),("red","RED","ESCAPED, BUT STILL IN A HOT AREA.")]
def states(k,flash_dim=False,name=None):
    im=new(); card(im,200,120,1720,850); header(im,195,"THE 4 STAR STATES")
    for i,(st,nm,desc) in enumerate(STATES):
        y=320+i*135
        if i<k:
            s2="dimflash" if (st=="glow" and flash_dim) else st
            for j in range(3): star(im,300+j*92,y,40,s2)
            text(im,(600,y-22),nm,FB(72),fill=(RED if st=="red" else WHITE),anchor="lm"); text(im,(600,y+34),desc,FI(30),fill=(215,205,240),anchor="lm")
        else:
            for j in range(3): star(im,300+j*92,y,40,"off")
    note(im,815); save(im,name or f"states{k}")
def six():
    im=new(); card(im,330,220,1590,760,border=YEL); 
    for r,(lab,n) in enumerate((("GTA 5",5),("GTA 6",6))):
        y=380+r*200; text(im,(420,y),lab,FB(110),anchor="lm")
        for j in range(6):
            star(im,790+j*125,y,52,("solid" if j<n else "off") if not (r==1 and j==5) else "yellow")
    text(im,(W//2,690),"THE SIXTH STAR IS BACK",FB(60),fill=YEL,anchor="mm"); save(im,"six")
ICONS=[("🧍","LOOKS"),("👕","CLOTHES"),("🚗","VEHICLE"),("🔫","WEAPON"),("📹","CCTV"),("👥","PARTNER")]
def icon_row(im,y,k,erased=(),size=150,gap=232):
    x0=W//2-gap*2.5
    for i,(e,l) in enumerate(ICONS):
        x=int(x0+i*gap); d=ImageDraw.Draw(im)
        on=i<k; col=(RED if on and i not in erased else (GREEN if i in erased else (70,55,110)))
        d.rounded_rectangle((x-size//2-14,y-size//2-14,x+size//2+14,y+size//2+14),28,fill=(45,25,90,255),outline=col+(255,),width=7)
        if on:
            em=emoji(e,size-30); 
            if i in erased: em.putalpha(em.getchannel("A").point(lambda a:int(a*0.28)))
            im.alpha_composite(em,(x-em.width//2,y-em.height//2)); text(im,(x,y+size//2+52),l,FB(46),fill=(GREEN if i in erased else WHITE),anchor="mm")
            if i in erased: d=ImageDraw.Draw(im); d.line((x-52,y+6,x-14,y+44),fill=GREEN+(255,),width=16); d.line((x-14,y+44,x+56,y-40),fill=GREEN+(255,),width=16)
        else: text(im,(x,y),"?",FB(110),fill=(110,95,160),anchor="mm")
def icons(k):
    im=new(); card(im,200,190,1720,790); header(im,265,"WHAT THE POLICE KNOW"); icon_row(im,480,k); note(im,745); save(im,f"icons{k}")
FIX=[(1,"CLOTHES KNOWN?","CHANGE YOUR OUTFIT","CLOTHING STORE  ·  OR A SPARE OUTFIT IN YOUR CAR TRUNK"),(0,"FACE KNOWN?","HAIRCUT  ·  OR MASK UP FIRST","A MASK BEFORE THE CRIME LIMITS WHAT WITNESSES SEE"),(2,"CAR KNOWN?","DUMP IT, SWAP IT, RESPRAY IT","PREVIEW DEMO: ICON GONE, CRUISER DROVE STRAIGHT PAST"),(3,"WEAPON KNOWN?","STASH IT","GET RID OF THE WEAPON THEY SAW"),(4,"ON CAMERA?","DESTROY THE FOOTAGE","EXTENDED LOOK: THE CREW BURNS THE GETAWAY CAR"),(5,"LOOKING FOR A COUPLE?","SPLIT UP","REPORTS SAY IT CAN DROP ONE STAR")]
def fix(n):
    idx,q,a,sub=FIX[n]; done=[f[0] for f in FIX[:n+1]]
    im=new(); card(im,200,150,1720,830,border=GREEN); icon_row(im,275,6,erased=done,size=112,gap=200)
    text(im,(W//2,470),q,FB(84),fill=RED,anchor="mm"); text(im,(W//2,585),a,FA(108),fill=WHITE,anchor="mm"); text(im,(W//2,720),sub,FI(34),fill=(215,205,240),anchor="mm"); save(im,f"fix{n}")
def grid_map(im,x0,y0,x1,y1):
    d=ImageDraw.Draw(im); d.rounded_rectangle((x0,y0,x1,y1),26,fill=(34,60,92,255))
    import random; random.seed(4)
    for gx in range(x0+20,x1-60,74):
        for gy in range(y0+20,y1-50,58):
            if random.random()<0.82: d.rounded_rectangle((gx,gy,gx+58,gy+42),6,fill=(58,92,128,255))
    d.polygon([(x0,y1-140),(x0+260,y1-90),(x0+420,y1),(x0,y1)],fill=(30,140,190,255))
def hot(full=False):
    im=new(); card(im,200,130,1720,850,border=RED); header(im,205,"HOT AREA" if not full else "SIX STARS  =  THE WHOLE MAP",RED)
    grid_map(im,300,270,1100,790)
    ov=new(); d=ImageDraw.Draw(ov)
    if full: d.rounded_rectangle((300,270,1100,790),26,fill=(255,40,40,150))
    else: d.ellipse((470,330,890,750),fill=(255,90,90,90)); d.ellipse((560,420,800,660),fill=(255,30,30,170))
    im.alpha_composite(ov)
    if not full: text(im,(680,540),"CRIME",FB(54),anchor="mm")
    lines=(["POLICE STAY HERE","WITH YOUR DESCRIPTION.","","COME BACK MATCHING IT,","AND THE CHASE RESTARTS."] if not full else ["NOWHERE TO COOL OFF.","","ALL OF LEONIDA","IS LOOKING FOR YOU."])
    for i,s in enumerate(lines): text(im,(1170,400+i*70),s,FB(60),fill=(YEL if i>=3 or full and i>=2 else WHITE),anchor="lm")
    note(im,815,"ILLUSTRATION  ·  NOT THE REAL MAP"); save(im,"hot6" if full else "hot")
def minimap():
    im=new(); card(im,200,130,1720,850,border=CYAN); header(im,205,"WHERE ARE THE COPS?",CYAN)
    import random; random.seed(7)
    for c,(cx,lab,sub) in enumerate(((620,"GTA 5","EVERY COP IS A BLIP"),(1300,"GTA 6","NO BLIPS.  USE YOUR EYES."))):
        d=ImageDraw.Draw(im); d.ellipse((cx-200,290,cx+200,690),fill=(34,60,92,255),outline=WHITE+(255,),width=8)
        for gx in range(-150,151,75): d.line((cx+gx,330,cx+gx,650),fill=(58,92,128,255),width=14)
        for gy in range(-150,151,75): d.line((cx-160,490+gy,cx+160,490+gy),fill=(58,92,128,255),width=14)
        d.polygon([(cx,472),(cx-14,506),(cx+14,506)],fill=WHITE+(255,))
        if c==0:
            for bx,by,a in ((cx-90,400,30),(cx+100,560,200),(cx+60,380,120)):
                ov=new(); ImageDraw.Draw(ov).pieslice((bx-90,by-90,bx+90,by+90),a-28,a+28,fill=(80,160,255,120)); im.alpha_composite(ov)
                ImageDraw.Draw(im).ellipse((bx-14,by-14,bx+14,by+14),fill=(60,140,255,255),outline=WHITE+(255,),width=3)
        text(im,(cx,238+30),"",FB(10)); text(im,(cx,740),lab,FB(80),anchor="mm"); text(im,(cx,800),sub,FI(30),fill=(YEL if c else (215,205,240)),anchor="mm")
    save(im,"minimap")
def focus():
    im=new(); card(im,360,560,1560,840,border=CYAN); text(im,(W//2,640),"FOCUS ABILITY",FB(90),fill=CYAN,anchor="mm"); text(im,(W//2,740),"HIGHLIGHTS NEARBY OFFICERS, EVEN THROUGH WALLS",FI(36),anchor="mm"); save(im,"focus")
def nelson():
    im=new(); card(im,260,200,1660,790,border=YEL)
    for j in range(3): star(im,W//2-110+j*110,300,46,"solid")
    text(im,(W//2,420),"3 STARS OR HIGHER",FB(96),fill=YEL,anchor="mm"); text(im,(W//2,545),"NORMAL CAR  =  NEARLY IMPOSSIBLE",FA(92),anchor="mm")
    text(im,(W//2,680),"YOU NEED A HYPERCAR OR A FAST MOTORCYCLE",FI(38),fill=(215,205,240),anchor="mm"); text(im,(W//2,745),"PER ROB NELSON, ROCKSTAR NORTH  ·  PARAPHRASED FROM PREVIEWS",FI(24),fill=(190,180,220),anchor="mm"); save(im,"nelson")
def tracker():
    im=new(); card(im,360,560,1560,840,border=RED); im.alpha_composite(emoji("📡",150),(430,625)); text(im,(640,650),"STOLEN CARS CAN HAVE TRACKERS",FB(80),fill=WHITE,anchor="lm"); text(im,(640,745),"STEAL THE WRONG ONE AND IT REPORTS ITSELF",FI(34),fill=YEL,anchor="lm"); save(im,"tracker")
def k9():
    im=new(); card(im,330,170,1590,820,border=YEL); im.alpha_composite(emoji("🐕",300),(430,330)); text(im,(820,330),"K-9 UNITS",FA(170),fill=YEL,anchor="lm")
    text(im,(820,480),"POLICE DOGS JOIN THE CHASE",FB(70),anchor="lm"); text(im,(820,570),"A GERMAN SHEPHERD PINNED JASON",FI(36),fill=(215,205,240),anchor="lm"); text(im,(820,625),"IN THE EDGE MAGAZINE DEMO",FI(36),fill=(215,205,240),anchor="lm")
    text(im,(W//2,765),"SOURCE: EDGE PREVIEW, AS REPORTED BY GAMESPOT",FI(24),fill=(190,180,220),anchor="mm"); save(im,"k9")
def profile(k):
    im=new(); card(im,200,130,1720,850); header(im,205,"CRIMINAL PROFILE")
    cols=[(600,"PLAY RUTHLESS",RED,["WITNESSES CALL POLICE FASTER","ARMED CITIZENS FIGHT BACK","RIVAL GANGS ATTACK ON SIGHT"]),(1320,"PLAY SMART",GREEN,["SCARE, DON'T SHOOT","LESS UNNEEDED VIOLENCE","THE WORLD GOES EASIER ON YOU"])]
    for i,(cx,h,col,ls) in enumerate(cols):
        if i<k:
            ImageDraw.Draw(im).rounded_rectangle((cx-320,280,cx+320,770),26,fill=(45,25,90,255),outline=col+(255,),width=6); text(im,(cx,345),h,FB(84),fill=col,anchor="mm")
            for j,s in enumerate(ls): text(im,(cx,470+j*95),s,FI(33),anchor="mm")
    save(im,f"profile{k}")
def unknown():
    im=new(); card(im,330,190,1590,800,border=CYAN); header(im,270,"STILL UNKNOWN",CYAN)
    for i,s in enumerate(["WHICH CRIMES EARN WHICH STAR?","WHAT SHOWS UP AT SIX STARS?"]):
        text(im,(450,420+i*130),"?",FA(110),fill=YEL,anchor="mm"); text(im,(530,420+i*130),s,FB(76),anchor="lm")
    text(im,(W//2,715),"WE FIND OUT NOVEMBER 19",FB(60),fill=YEL,anchor="mm"); save(im,"unknown")
def recap():
    im=new(); card(im,200,230,1720,800,border=YEL); header(im,305,"GTA 6 POLICE KNOW..."); icon_row(im,500,5,size=140,gap=215)
    x=int(W//2+215*2.5); ImageDraw.Draw(im).rounded_rectangle((x-84,416,x+84,584),28,fill=(45,25,90,255),outline=YEL+(255,),width=7); e=emoji("🐕",120); im.alpha_composite(e,(x-e.width//2,500-e.height//2)); text(im,(x,622),"+ A DOG",FB(46),fill=YEL,anchor="mm")
    # replace 6th tile label handled by drawing over
    save(im,"recap")
def endcard():
    im=new(); lg=Image.open("/mnt/user-data/uploads/969a9829-image.png").convert("RGBA").resize((520,520),Image.LANCZOS)
    card(im,330,150,1590,860,border=PINK,alpha=245); im.paste(lg,(400,245)); text(im,(1240,400),"SUBSCRIBE",FA(150),fill=YEL,anchor="mm"); text(im,(1240,540),"FIVE STAR INTEL",FB(96),anchor="mm"); text(im,(1240,640),"MORE GTA 6 EVERY WEEK",FI(36),fill=(215,205,240),anchor="mm"); save(im,"endcard")
def src_chip():
    im=new(); s="OFFICIAL ROCKSTAR GAMES TRAILER FOOTAGE  ·  COMMENTARY BY FIVE STAR INTEL"; f=FI(20); w=ImageDraw.Draw(im).textlength(s,font=f)
    text(im,(W-40-w,36),s,f,fill=(235,235,245),stroke=3); save(im,"src")
if __name__=="__main__":
    logo_bug(); src_chip(); old_way(); [witness(k) for k in (1,2,3)]; [states(k) for k in (1,2,3,4)]; states(3,True,"states3b"); six(); [icons(k) for k in range(1,7)]; [fix(n) for n in range(6)]
    hot(); hot(True); minimap(); focus(); nelson(); tracker(); k9(); [profile(k) for k in (1,2)]; unknown(); recap(); endcard()
    stamp("hook1",["THEY REMEMBER","YOUR SHIRT"],hl=1); stamp("hook2",["IT HAS","FOUR LEGS"],hl=1); stamp("ghost",["YOU ARE A","GHOST"],hl=1); stamp("dontshoot",["PLEASE.","DON'T SHOOT THE DOG."],hl=1,size=120); stamp("throws",["GTA 6","THROWS THAT OUT"],hl=1,size=130); stamp("stealth",["THIS IS A","STEALTH GAME NOW"],hl=1,size=130)
    for n,(sm,bg) in {"l_intro":("FIVE STAR INTEL","The New GTA 6 Police"),"l_old":("REWIND","GTA 5: The Old Way"),"l_wit":("RULE 1","No Witness, No Problem"),"l_states":("THE WANTED LEVEL","4 Star States"),"l_icons":("THE NOTEBOOK","What Police Know"),"l_fix":("ESCAPE","Erase the Clues"),"l_hot":("AFTER THE CHASE","Hot Areas"),"l_mini":("NO MORE BLIPS","Find Them Yourself"),"l_run":("OUTRUN THEM?","Good Luck"),"l_k9":("NEW","K-9 Units"),"l_prof":("THE LONG GAME","Criminal Profile"),"l_unk":("NOT CONFIRMED YET","Still Unknown"),"l_out":("RECAP","Smarter Than Ever")}.items(): label(n,sm,bg)
    for i,t in enumerate(["The Old Way","No Witness, No Problem","The 4 Star States","The Police Notebook","Hot Areas","Outrun Them?","The Dog","Criminal Profile"],1): title_card(f"ch{i}",i,t)
    print(len(os.listdir("gfx")))
