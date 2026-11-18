import subprocess, math, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import gfx
from gfx import FB,FA,FS,FI,emoji,INK,PINK,YEL,CYAN,WHITE,RED,W,H
def frame_at(t):
    raw=subprocess.run(["ffmpeg","-v","error","-ss",f"{t:.3f}","-i","bg_all.mp4","-frames:v","1","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
    return Image.frombytes("RGB",(W,H),raw).convert("RGBA")
def rmask(size,box,r):
    m=Image.new("L",size,0); ImageDraw.Draw(m).rounded_rectangle(box,r,fill=255); return m
def glass(fr,box,style,alpha=1.0,r=40):
    """style: dict(blur, tint=(r,g,b), ta, grad=None|((c1),(c2)), border=(rgb), ba)"""
    x0,y0,x1,y1=[int(v) for v in box]; out=fr.copy()
    if style.get("none"): return out
    sh=Image.new("RGBA",fr.size,(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((x0+6,y0+12,x1+6,y1+12),r,fill=(0,0,0,int(90*alpha))); out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    reg=fr.crop((x0,y0,x1,y1)).filter(ImageFilter.GaussianBlur(style["blur"])) if style["blur"] else fr.crop((x0,y0,x1,y1))
    w,h=x1-x0,y1-y0
    if style.get("grad"):
        c1,c2=style["grad"]; g=np.linspace(0,1,w)[None,:,None]; arr=(np.array(c1)[None,None,:]*(1-g)+np.array(c2)[None,None,:]*g).astype(np.uint8); arr=np.repeat(arr,h,axis=0)
        tint=Image.fromarray(arr,"RGB").convert("RGBA"); tint.putalpha(int(255*style["ta"]))
    else: tint=Image.new("RGBA",(w,h),style["tint"]+(int(255*style["ta"]),))
    reg=Image.alpha_composite(reg.convert("RGBA"),tint)
    # top sheen
    sheen=Image.new("RGBA",(w,h),(0,0,0,0)); sd=ImageDraw.Draw(sheen)
    for i in range(int(h*0.45)): sd.line((0,i,w,i),fill=(255,255,255,int(34*(1-i/(h*0.45)))))
    reg=Image.alpha_composite(reg,sheen)
    m=rmask((w,h),(0,0,w-1,h-1),r)
    if alpha<1: m=m.point(lambda a:int(a*alpha))
    out.paste(reg,(x0,y0),m)
    bd=Image.new("RGBA",fr.size,(0,0,0,0)); d=ImageDraw.Draw(bd); d.rounded_rectangle((x0,y0,x1,y1),r,outline=style.get("border",(255,255,255))+(int(255*style.get("ba",0.7)*alpha),),width=3)
    d.rounded_rectangle((x0+4,y0+4,x1-4,y1-4),r-4,outline=(255,255,255,int(40*alpha)),width=2); out.alpha_composite(bd)
    return out
STYLES={
 "A":dict(name="A  FROSTED GLASS · violet tint",blur=22,tint=(40,20,95),ta=0.42,border=(255,255,255),ba=0.75),
 "B":dict(name="B  CLEAR GLASS · light tint",blur=7,tint=(30,16,70),ta=0.24,border=(255,255,255),ba=0.85),
 "C":dict(name="C  COLOUR GLASS · pink to cyan",blur=22,grad=((255,46,147),(0,170,255)),ta=0.30,border=(255,255,255),ba=0.8),
 "D":dict(name="D  NO BOX · floating icons",none=True),
}
def txt(im,xy,s,font,fill=WHITE,anchor="mm",stroke=4,a=255):
    ImageDraw.Draw(im).text(xy,s,font=font,fill=fill+(a,),anchor=anchor,stroke_width=stroke,stroke_fill=(15,6,40,a))
def chrome(im,small,big,credit=1):
    d=ImageDraw.Draw(im); d.rectangle((44,28,104,30),fill=YEL+(255,)); txt(im,(44,46),small,FI(22),fill=YEL,anchor="lm",stroke=3); txt(im,(44,88),big,FS(46),anchor="lm",stroke=4)
    if credit==1: txt(im,(44,128),"Footage: Rockstar Games official trailers",FI(17),fill=(235,235,245),anchor="lm",stroke=2,a=215)
    lg=Image.open("gfx/logo.png"); im.alpha_composite(lg)
    if credit==2: txt(im,(176,1010),"Footage: Rockstar Games official trailers",FI(17),fill=(235,235,245),anchor="lm",stroke=2,a=215)
def icons_content(im,k,style):
    box=(250,300,1670,790)
    if not style.get("none"): pass
    txt(im,(W//2,372),"WHAT THE POLICE KNOW",FB(78),fill=YEL)
    gap=226; x0=W//2-gap*2.5
    for i,(e,l) in enumerate(gfx.ICONS):
        x=int(x0+i*gap); y=545; d=ImageDraw.Draw(im)
        t=Image.new("RGBA",im.size,(0,0,0,0)); ImageDraw.Draw(t).rounded_rectangle((x-88,y-88,x+88,y+88),30,fill=(255,255,255,46),outline=(255,90,110,255),width=5); im.alpha_composite(t)
        em=emoji(e,122); im.alpha_composite(em,(x-em.width//2,y-em.height//2)); txt(im,(x,y+128),l,FB(46))
    txt(im,(W//2,752),"ILLUSTRATION  ·  NOT THE REAL HUD",FI(20),fill=(235,230,250),stroke=2,a=200)
if __name__=="__main__":
    fr=frame_at(173.2); sheet=Image.new("RGB",(W,H))
    for n,(k,st) in enumerate(STYLES.items()):
        im=glass(fr,(250,300,1670,790),st); icons_content(im,6,st); chrome(im,"THE NOTEBOOK","What Police Know",credit=1 if k!="D" else 2)
        txt(im,(W-40,60),st["name"],FB(54),fill=YEL,anchor="rm",stroke=5)
        im.convert("RGB").save(f"samples/glass_{k}.jpg",quality=92)
        sheet.paste(im.convert("RGB").resize((960,540),Image.LANCZOS),((n%2)*960,(n//2)*540))
    sheet.save("samples/glass_options_sheet.jpg",quality=90)
