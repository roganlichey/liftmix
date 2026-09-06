"""CAD-derived views and a short cutaway animation; no simulated powder flow."""
from pathlib import Path
import math,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from build_compact import build,poses,tm,ROOT,PALETTE,RIGID,lift_at

parts,aux,dims=build();OUT=ROOT/'visuals';OUT.mkdir(exist_ok=True)
BG='#f3f3eb';INK='#173c2c';MUTED='#53735e';GOLD='#dfa73b'
COL={n:tuple(v[:3]) for n,v in PALETTE.items()}
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size)

def render3d(path,items,zlim,azim=-58,elev=24):
    # Orthographic z-buffer renderer: avoids painter-order artifacts on nested CAD.
    W,H=960,1120;faces=[];colors=[];light=np.array([-.3,-.55,.8]);light/=np.linalg.norm(light)
    az,el=np.radians([azim,elev]);view=np.array([np.cos(el)*np.cos(az),np.cos(el)*np.sin(az),np.sin(el)])
    right=np.array([-np.sin(az),np.cos(az),0]);up=np.cross(view,right)
    for n,s in items.items():
        m=tm(s);take=m.face_normals@view>1e-9
        fac=.57+.43*np.clip(m.face_normals[take]@light,0,1)
        color=np.array(COL.get(n,(127,161,136)))/255
        faces.extend(m.triangles[take]);colors.extend(color[None,:]*fac[:,None])
    tri=np.asarray(faces);u=tri@right;v=tri@up;depth=tri@view
    scale=min(W*.77/np.ptp(u),H*.82/np.ptp(v))
    u=(u-(u.max()+u.min())/2)*scale+W/2
    v=-(v-(v.max()+v.min())/2)*scale+H/2
    bg=np.array([243,243,235],dtype=np.uint8);pixels=np.tile(bg,(H,W,1));zb=np.full((H,W),-np.inf)
    for xx,yy,zz,col in zip(u,v,depth,colors):
        x0=max(0,int(np.floor(xx.min())));x1=min(W-1,int(np.ceil(xx.max())))
        y0=max(0,int(np.floor(yy.min())));y1=min(H-1,int(np.ceil(yy.max())))
        den=(yy[1]-yy[2])*(xx[0]-xx[2])+(xx[2]-xx[1])*(yy[0]-yy[2])
        if abs(den)<1e-10 or x1<x0 or y1<y0:continue
        gx=np.arange(x0,x1+1)[None,:]+.5;gy=np.arange(y0,y1+1)[:,None]+.5
        w0=((yy[1]-yy[2])*(gx-xx[2])+(xx[2]-xx[1])*(gy-yy[2]))/den
        w1=((yy[2]-yy[0])*(gx-xx[2])+(xx[0]-xx[2])*(gy-yy[2]))/den;w2=1-w0-w1
        z=w0*zz[0]+w1*zz[1]+w2*zz[2]
        region=zb[y0:y1+1,x0:x1+1];hit=(w0>=-1e-7)&(w1>=-1e-7)&(w2>=-1e-7)&(z>region)
        region[hit]=z[hit];pixels[y0:y1+1,x0:x1+1][hit]=np.clip(np.asarray(col)*255,0,255).astype(np.uint8)
    Image.fromarray(pixels).save(path)

def section(s):
    return [np.column_stack([np.asarray(p)[:,0],-np.asarray(p)[:,1]])
            for p in s.m.rotate([90,0,0]).slice(0).to_polygons()]

def shapes(im,polys,col,cx,zero,scale):
    mask=Image.new('L',im.size);md=ImageDraw.Draw(mask);records=[]
    for p in polys:
        a=np.sum(p[:,0]*np.roll(p[:,1],-1)-p[:,1]*np.roll(p[:,0],-1))/2
        q=[(cx+x*scale,zero-z*scale) for x,z in p];records.append((abs(a),a,q))
    for _,a,q in sorted(records,key=lambda r:-r[0]):md.polygon(q,fill=255 if a<0 else 0)
    im.paste(col,(0,0),mask);d=ImageDraw.Draw(im)
    for _,_,q in records:d.line(q+[q[0]],fill='#365a42',width=2)

def draw_section(im,angle,cx,zero,scale):
    state=poses(parts,angle)
    # Outline of the powder space is obtained directly from the CAD cavity.
    for n in ['body','guide_lid','twist_crown','top_retainer','plunger','cross_pin']:
        shapes(im,section(state[n]),COL[n],cx,zero,scale)
    for n in ['bottle_gasket','lid_gasket','valve_gasket']:
        shapes(im,section(aux[n]),'#7b9182',cx,zero,scale)
    shapes(im,section(parts['stem_seal_TPU']),'#7b9182',cx,zero,scale)

def arrow(d,p0,p1,col=GOLD,width=5):
    d.line([p0,p1],fill=col,width=width);a=math.atan2(p1[1]-p0[1],p1[0]-p0[0])
    d.polygon([p1,(p1[0]-13*math.cos(a-.45),p1[1]-13*math.sin(a-.45)),
              (p1[0]-13*math.cos(a+.45),p1[1]-13*math.sin(a+.45))],fill=col)

print('Rendering assembled CAD view.',flush=True)
render3d(OUT/'assembled.png',{n:parts[n] for n in ['body','twist_crown','top_retainer']},(-14,47))
render3d(OUT/'underside.png',{n:parts[n] for n in ['body','twist_crown','top_retainer','plunger']},(-14,47),elev=-32)

im=Image.new('RGB',(1800,1240),BG);d=ImageDraw.Draw(im)
d.text((72,48),'LIFTMIX / COMPACT v3',font=font(48,True),fill=INK)
d.text((75,115),'Printable concealed-cam prototype  •  Flat twist crown  •  Internal bottle threads',font=font(25),fill=MUTED)
hero=Image.open(OUT/'assembled.png').resize((635,741),Image.Resampling.LANCZOS);im.paste(hero,(20,193))
d=ImageDraw.Draw(im)
d.text((87,195),'ASSEMBLED',font=font(25,True),fill=INK)
d.text((700,195),'CLOSED',font=font(25,True),fill=INK)
d.text((1215,195),'TURN TOP 90° CLOCKWISE',font=font(25,True),fill=INK)
draw_section(im,0,903,740,9.0);draw_section(im,90,1433,740,9.0)
d=ImageDraw.Draw(im)
# Fill line and leader labels are dimensioned from the actual chamber.
fy=740-dims['fill_z_mm']*9
d.line([(753,fy),(875,fy)],fill=GOLD,width=3);d.line([(931,fy),(1053,fy)],fill=GOLD,width=3)
d.text((745,278),'Suggested fill: 14 mL',font=font(21,True),fill=INK)
d.line([(1058,309),(1132,309),(1132,fy),(1060,fy)],fill=GOLD,width=2)
arrow(d,(1665,740-4*9),(1665,740-10*9))
d.text((1630,740-14*9),'6 mm',font=font(20,True),fill=INK)
arrow(d,(1389,740-2*9),(1389,740+7*9))
arrow(d,(1477,740-2*9),(1477,740+7*9))
d.text((1280,878),'Outlet opens into the bottle.',font=font(22),fill=MUTED)
d.text((746,878),'Plug compresses a soft seal.',font=font(22),fill=MUTED)
d.text((90,934),'Actual CAD geometry',font=font(24,True),fill=INK)
d.text((90,973),'46.2 mm wide × 54.6 mm tall',font=font(24),fill=MUTED)
d.text((700,963),'Gold = moving plug and cross pin. The outer crown rotates; the plug only lifts.',font=font(23),fill=MUTED)
d.line([(75,1051),(1720,1051)],fill='#c8d5c8',width=2)
d.text((75,1080),'7 rigid plastic parts + 4 soft seals. No metal fasteners or disposable membrane.',font=font(27,True),fill=INK)
d.text((75,1130),'14.6 mL geometric capacity below a 2 mm headspace. Weigh and measure your actual powder blend.',font=font(23),fill=MUTED)
d.text((75,1175),'Bench prototype: physical fit, powder flow, sealing and food-contact suitability are not validated.',font=font(23),fill=MUTED)
im.save(OUT/'LiftMix_v3_CAD.png')

# Legible exploded section: separation is illustrative, each solid is exact CAD.
im=Image.new('RGB',(1400,1450),BG);d=ImageDraw.Draw(im)
d.text((65,42),'LIFTMIX v3 / ASSEMBLY MAP',font=font(38,True),fill=INK)
d.text((65,101),'Side section; parts spread vertically for identification.',font=font(22),fill=MUTED)
cx=470;zero=1265;scale=5.8
offsets={'body':0,'plunger':32,'guide_lid':60,'cross_pin':86,'twist_crown':104,'top_retainer':135}
for n in ['body','plunger','guide_lid','cross_pin','twist_crown','top_retainer']:
    shapes(im,section(parts[n].t([0,0,offsets[n]])),COL[n],cx,zero,scale)
labels=[('top_retainer',42.4,'1  Flat threaded retainer','Captures the crown with a small running gap.'),
        ('twist_crown',34,'2  Twist crown','Paired internal ramps move the cross pin.'),
        ('cross_pin',30,'3  Plastic cross pin','Passes through the stem and fixed guide slots.'),
        ('guide_lid',24.75,'4  Fixed guide lid + side key','Screws onto the body; the key stops rotation.'),
        ('plunger',8,'5  Plug and stem','Lifts 6 mm to release powder.'),
        ('body',7,'6  Reservoir and bottle socket','Bottom threads attach to the bottle neck.')]
for n,z,title,sub in labels:
    y=zero-(z+offsets[n])*scale
    d.line([(630,y),(738,y)],fill=MUTED,width=2)
    d.text((765,y-26),title,font=font(23,True),fill=INK)
    # Short labels deliberately wrap to avoid clipping the right edge.
    words=sub.split();line='';lines=[]
    for w in words:
        q=(line+' '+w).strip()
        if d.textlength(q,font=font(20))>545:lines.append(line);line=w
        else:line=q
    lines.append(line)
    for j,l in enumerate(lines):d.text((765,y+9+j*27),l,font=font(20),fill=MUTED)
d.text((65,1353),'Soft seals: bottle rim, refill lid, valve seat, and moving stem.',font=font(24,True),fill=INK)
d.text((65,1397),'See README.md for the assembly order, gasket placement and printer settings.',font=font(22),fill=MUTED)
im.save(OUT/'LiftMix_v3_assembly.png')

print('Rendering motion preview.',flush=True)
tmp=ROOT.parent/'animation_frames_v3';tmp.mkdir(exist_ok=True)
def frame(t):
    if t<1.5:angle=0;label='CLOSED / POWDER HELD ABOVE THE PLUG'
    elif t<5.0:angle=90*(t-1.5)/3.5;label='TWIST THE OUTER CROWN CLOCKWISE'
    elif t<7.0:angle=90;label='OPEN / POWDER CAN DROP THROUGH'
    elif t<10.5:angle=90*(1-(t-7)/3.5);label='TURN BACK TO RESEAT THE PLUG'
    else:angle=0;label='CLOSED AGAIN / UNSCREW CAP TO DRINK'
    out=Image.new('RGB',(1080,1080),BG);dr=ImageDraw.Draw(out)
    dr.text((52,38),'LIFTMIX / COMPACT v3',font=font(38,True),fill=INK)
    dr.text((52,100),label,font=font(23,True),fill=MUTED)
    draw_section(out,angle,540,801,11.7);dr=ImageDraw.Draw(out)
    dr.text((58,191),'CUTAWAY',font=font(21,True),fill=MUTED)
    dr.text((760,188),f'{angle:.0f}° turn',font=font(27,True),fill=INK)
    dr.text((760,234),f'{lift_at(angle):.1f} mm lift',font=font(24),fill=MUTED)
    # Top dial makes rotation visible even in a side section.
    cc=(540,168);rr=48;dr.ellipse([cc[0]-rr,cc[1]-rr,cc[0]+rr,cc[1]+rr],outline=MUTED,width=3)
    a=math.radians(-90+angle);q=(cc[0]+rr*.85*math.cos(a),cc[1]+rr*.85*math.sin(a))
    arrow(dr,cc,q)
    if angle>35:
        for x in [496,584]:arrow(dr,(x,778),(x,880))
    dr.line([(52,943),(1028,943)],fill='#cad5c8',width=2)
    dr.text((52,971),'Hold the lower body still while turning the crown.',font=font(26,True),fill=INK)
    dr.text((52,1020),'CAD motion preview. Powder flow and liquid sealing require physical tests.',font=font(20),fill=MUTED)
    return out

fps=10;duration=12
for i in range(fps*duration):frame(i/fps).save(tmp/f'frame_{i:04d}.png')
for p in tmp.glob('frame_*.png'):
    with Image.open(p) as check:check.verify()
subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(fps),'-i',str(tmp/'frame_%04d.png'),
    '-c:v','libx264','-pix_fmt','yuv420p','-crf','21','-movflags','+faststart',str(OUT/'LiftMix_v3_motion.mp4')],check=True)
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(OUT/'LiftMix_v3_motion.mp4'),
    '-filter_complex','fps=8,scale=650:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse',
    '-loop','0',str(OUT/'LiftMix_v3_motion.gif')],check=True)
print('Visuals complete.',flush=True)
