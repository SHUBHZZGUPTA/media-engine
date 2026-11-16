import subprocess, re, json, os
shots={}
for n in range(1,6):
    out=subprocess.run(["ffmpeg","-v","info","-i",f"src/t{n}.mp4","-vf","scale=480:270,select='gt(scene,0.28)',showinfo","-an","-f","null","-"],capture_output=True,text=True).stderr
    cuts=[float(x) for x in re.findall(r"pts_time:([\d.]+)",out)]
    dur=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"src/t{n}.mp4"],capture_output=True,text=True).stdout)
    b=[0]+cuts+[dur]; L=[]
    for a,c in zip(b,b[1:]):
        if c-a>=0.7: L.append((round(a+0.07,2),round(c-0.07,2)))
    shots[f"t{n}"]=L; print(n,len(L))
json.dump(shots,open("shots.json","w"))
os.makedirs("thumbs",exist_ok=True)
idx=0; items=[]
for k,L in shots.items():
    for i,(a,c) in enumerate(L):
        f=f"thumbs/{k}_{i:03d}.jpg"
        subprocess.run(["ffmpeg","-v","error","-y","-ss",str((a+c)/2),"-i",f"src/{k}.mp4","-frames:v","1","-vf",f"scale=320:180,drawtext=text='{k}#{i} {a:.1f}+{c-a:.1f}':x=4:y=4:fontsize=17:fontcolor=yellow:box=1:boxcolor=black@0.7","-q:v","4",f])
        items.append(f)
# sheets of 48
for s in range(0,len(items),48):
    chunk=items[s:s+48]
    open("l.txt","w").write("".join(f"file '{x}'\nduration 1\n" for x in chunk))
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-i","l.txt","-vf","tile=6x8","-frames:v","1","-q:v","4",f"sheets/shots_{s//48}.jpg"])
print(len(items))
