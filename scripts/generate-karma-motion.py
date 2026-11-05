"""Create an original, project-specific animated GIF using Pillow."""
from PIL import Image, ImageDraw, ImageFont
import math, os
PROJECT = os.environ["KARMA_PROJECT"]
ACCENT = os.environ["KARMA_ACCENT"]
SECONDARY = os.environ["KARMA_SECONDARY"]
INDEX = int(os.environ["KARMA_INDEX"])
W,H=720,180
font=ImageFont.load_default()
frames=[]
for frame in range(18):
    im=Image.new("RGB",(W,H),(13,18,30))
    d=ImageDraw.Draw(im)
    for x in range(0,W,32):
        d.line((x,0,x,H),fill=(24,32,47))
    for y in range(0,H,32):
        d.line((0,y,W,y),fill=(24,32,47))
    d.rectangle((16,16,W-17,H-17),outline=ACCENT,width=2)
    d.text((35,32),"KARMA  /  ORIGINAL MOTION ARCHIVE",fill=ACCENT,font=font)
    d.text((35,83),PROJECT.upper(),fill="white",font=font,stroke_width=0)
    d.text((35,118),f"PROJECT SIGNAL {INDEX+1:02d}  /  FRAME {frame+1:02d}",fill=SECONDARY,font=font)
    cx,cy=575,89
    angle=2*math.pi*frame/18
    mode=INDEX%5
    if mode==0:
        for k in range(5):
            radius=14+k*12+5*math.sin(angle+k)
            d.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),outline=ACCENT if k%2 else SECONDARY,width=2)
    elif mode==1:
        for k in range(7):
            x=cx-77+k*25
            height=18+int(56*abs(math.sin(angle+k*.65)))
            d.rectangle((x,cy-height//2,x+12,cy+height//2),fill=ACCENT if k%2 else SECONDARY)
    elif mode==2:
        for k in range(12):
            a=angle+k*math.pi/6
            x=cx+int(64*math.cos(a));y=cy+int(64*math.sin(a))
            d.line((cx,cy,x,y),fill=SECONDARY,width=2)
            d.ellipse((x-5,y-5,x+5,y+5),fill=ACCENT)
    elif mode==3:
        for row in range(3):
            for col in range(4):
                x=cx-74+col*39;y=cy-47+row*39
                d.rectangle((x,y,x+25,y+25),outline=ACCENT,width=2)
                if (col+row+frame//3)%4==0:d.rectangle((x+5,y+5,x+20,y+20),fill=SECONDARY)
    else:
        pts=[]
        for k in range(60):
            x=cx-82+k*3
            y=cy+int(24*math.sin(k*.3+angle)*math.cos(k*.13+INDEX))
            pts.append((x,y))
        d.line(pts,fill=ACCENT,width=4)
        d.ellipse((pts[-1][0]-5,pts[-1][1]-5,pts[-1][0]+5,pts[-1][1]+5),fill=SECONDARY)
    d.line((35,152,35+int(420*(frame+1)/18),152),fill=ACCENT,width=3)
    frames.append(im)
os.makedirs("assets",exist_ok=True)
frames[0].save("assets/karma-motion.gif",save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True)
print("Created assets/karma-motion.gif:",os.path.getsize("assets/karma-motion.gif"),"bytes")
