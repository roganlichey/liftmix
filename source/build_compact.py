"""LiftMix v3 / concealed cam, refillable powder-release cap.
Units: mm. Run: python source/build_compact.py
Requires numpy, trimesh, manifold3d. Parameters below are authoritative.
Unvalidated mechanical bench prototype; not a food-contact or pressure closure.
"""
from pathlib import Path
import math, json
import numpy as np
import trimesh
from manifold3d import Manifold, Mesh, CrossSection
from geometry_core import S, cyl, ring, box, arc, radial_pin, tm

ROOT=Path(__file__).resolve().parents[1]
CFG=dict(chamber_radius=17.5, body_top=24.0, seat_z=2.5,
         outlet_radius=8.0, outside_radius=23.1, lift=6.0,
         fill_headspace=2.0, pin_radius=1.7, cam_clearance=0.20,
         body_thread_pitch=2.1, bottle_thread_pitch=2.7,
         bottle_thread_crest_radius=12.75, bottle_thread_root_radius=14.29)

def helix(ri,ro,z0,turns,pitch,wi,wo):
    """Trapezoidal right-hand helix; axial widths at inner and outer radii."""
    n=math.ceil(turns*128); v=[]; f=[]
    for j in range(n+1):
        a=2*math.pi*turns*j/n; z=z0+pitch*turns*j/n
        for r,dz in [(ri,-wi/2),(ro,-wo/2),(ro,wo/2),(ri,wi/2)]:
            v.append([r*math.cos(a),r*math.sin(a),z+dz])
    for j in range(n):
        for k in range(4):
            a=j*4+k; b=j*4+(k+1)%4; c=(j+1)*4+(k+1)%4; d=(j+1)*4+k
            f.extend([[a,b,c],[a,c,d]])
    f.extend([[0,2,1],[0,3,2]])
    a=n*4; f.extend([[a,a+1,a+2],[a,a+2,a+3]])
    mesh=trimesh.Trimesh(v,f,process=True)
    if mesh.volume<0: mesh.invert()
    m=Manifold(Mesh(np.asarray(mesh.vertices,dtype=np.float32),np.asarray(mesh.faces,dtype=np.uint32)))
    return S(m,f'helix({ri},{ro},{z0},{turns},{pitch},{wi},{wo});')

def lift_at(angle):
    # Flat 8-degree dwell at both ends limits back-driving at the endpoints.
    return CFG['lift']*max(0,min(1,(angle-8)/74))

def rcyl(r,ri,ro,z):
    return cyl(r,ro-ri).r([0,90,0]).t([ri,0,z])

def build():
    H=CFG['body_top']; R=CFG['outside_radius']; seat=CFG['seat_z']; cr=CFG['chamber_radius']
    lid_z=H+.75; L=lid_z+3; pz=L+2.25
    guide_top=pz+11.4; crown_roof=pz+9; crown_top=pz+13.2
    bottom=H-5.65
    # Bottle socket, reservoir, and coarse refill-lid thread are a single part.
    body=cyl(R,H-6+11.2,-11.2)+cyl(19,H-(H-6)+.05,H-6-.05)
    body=body+helix(18.96,20,H-5.2,2,2.1,1.4,.65)
    chamber=cyl(8,seat+11.23,-11.21)
    chamber=chamber+cyl(11.8,cr-11.8,seat,r2=cr)+cyl(cr,H+1-seat-(cr-11.8),seat+cr-11.8)
    body=body-chamber-cyl(CFG['bottle_thread_root_radius'],11.22,-11.21)
    body=body-ring(11.12,7.9,.42,seat-.4)
    thread=helix(CFG['bottle_thread_crest_radius'],14.42,-9.75,2.8,2.7,.60,1.50)
    body=body+(thread ^ cyl(R-.1,11.18,-11.19))
    body=body-cyl(14.8,.65,-11.21,r2=14.28)
    # Shallow external grooves retain a continuous cylindrical silhouette.
    for a in range(0,360,12):
        body=body-box(.55,1.05,22,[R-.35,-.525,-9.2]).r([0,0,a])
    body=body-box(.7,1.4,3.6,[R-.45,-.7,H-9.6])
    # Fixed lid: threaded skirt, seal plate, and pin guide tower.
    lid=ring(21.4,19.2,6.7,H-5.9)+cyl(21.4,3,lid_z)
    lid=lid-helix(19.15,20.25,H-5.2-4.2,4,2.1,1.7,.95)
    lid=lid+cyl(8.8,guide_top-L+.05,L-.05)
    lid=lid-cyl(3.2,guide_top-lid_z+.1,lid_z-.05)-cyl(3.8,1.4,lid_z+.8)
    for a in [0,180]:
        slot=box(7.8,4.05,6,[2.0,-2.025,pz])
        for z in [pz,pz+6]:slot=slot+rcyl(2.025,2.0,9.8,z)
        lid=lid-slot.r([0,0,a])
    # Central blind hollow screw retains the crown; it bottoms on the guide.
    rt0=guide_top-3.4
    lid=lid-cyl(6.65,3.55,rt0-.05)-helix(6.60,7.65,rt0+.55,3.5,1.4,1.30,.76)
    # Hidden radial key positively prevents the refill lid from unscrewing.
    key_z=H-3.9
    hole=rcyl(1.40,17.8,23,key_z).r([0,0,90])
    body=body-hole; lid=lid-hole-rcyl(1.9,20.80,23,key_z).r([0,0,90])
    key=(rcyl(1.25,17.95,21.25,key_z)+rcyl(1.7,20.95,21.35,key_z)).r([0,0,90])
    # Poppet seals on the flat annular seat. A round shaft can use a round seal.
    plugbase=seat+.7; conez=plugbase+1.5; conetop=conez+8.5
    plunger=cyl(11.5,1.5,plugbase)+cyl(11.5,8.5,conez,r2=3)+cyl(3,pz+2-conetop+.04,conetop-.04)
    plunger=plunger-radial_pin(1.82,8,pz)
    # Cross pin is laterally captive inside the cam; no metal or exposed ends.
    pin=rcyl(CFG['pin_radius'],-10.8,10.8,pz)
    pin=pin+cyl(1.45,.2,r2=CFG['pin_radius']).r([0,90,0]).t([-11,0,pz])
    pin=pin+cyl(CFG['pin_radius'],.2,r2=1.45).r([0,90,0]).t([10.8,0,pz])
    crown=ring(R,21.65,crown_top-bottom,bottom)
    crown=crown+cyl(R,crown_top-crown_roof,crown_roof)
    crown=crown+ring(12.8,9.1,crown_roof-(L+.2)+.06,L+.2)
    crown=crown-cyl(9.05,crown_top-crown_roof+.10,crown_roof-.05)
    crown=crown-cyl(11.60,2.05,crown_top-2)
    # Two opposed rounded helical channels; both carry the same lift load.
    cutters=[]; sc=[]
    channel_r=CFG['pin_radius']+CFG['cam_clearance']
    for phase in [0,180]:
        for angle in np.linspace(0,90,91):
            cut=rcyl(channel_r,8.85,11.8,pz+lift_at(float(angle))).r([0,0,float(angle)+phase])
            cutters.append(cut.m);sc.append(cut.c)
        # Bottom entry permits assembly with the powder outlet CLOSED.
        entry=box(3.1,channel_r*2,pz-(L+.1),[8.8,-channel_r,L+.1])
        entry=entry.r([0,0,phase]);cutters.append(entry.m);sc.append(entry.c)
    combined=S(Manifold.batch_boolean(cutters, __import__('manifold3d').OpType.Add),'union(){'+''.join(sc)+'}')
    crown=crown-combined
    for a in range(0,360,12):
        crown=crown-box(.55,1.05,crown_top-bottom-3,[R-.35,-.525,bottom+1.5]).r([0,0,a])
    # A small radial index on the top, clear of the central retainer.
    crown=crown-box(6,1.0,.5,[13,-.5,crown_top-.35])
    retainer=ring(6.4,3.5,3.50,rt0)+helix(6.35,7.4,rt0+.55,1.5,1.4,1.05,.5)
    retainer=retainer+cyl(11.3,2,guide_top)
    retainer=retainer-box(18,1.7,1.0,[-9,-.85,guide_top+1.1])
    bottle_gasket=ring(13.4,10.65,1,-1)
    lid_gasket=ring(18.65,17.6,1,H)
    valve_gasket=ring(11.2,8.25,1.5,seat-.4)
    pts=[[3.5+.5*math.cos(t),.5*math.sin(t)] for t in np.linspace(0,2*math.pi,48,endpoint=False)]
    stem_seal=S(Manifold.revolve(CrossSection([pts]),96),f'rotate_extrude($fn=96) polygon({json.dumps(pts)});').t([0,0,lid_z+1.5])
    neck=ring(12.1,10.87,11.2,-11.95)+ring(12.535,10.87,1.7,-2.45)
    neck=neck+helix(12.04,13.7,-8.4,650/360,2.7,1.61,.75)+ring(16.5,10.87,1.5,-13.45)
    receiver=neck+ring(20,18,25.1,-43.45)+cyl(20,1.7,-45.05)
    receiver=receiver+(cyl(20,5.1,-18.45,r2=16.5)-cyl(18,5.14,-18.47,r2=10.87))
    # Small, fast full-profile bottle-thread coupon uses the same cap interface.
    coupon=body ^ cyl(16.7,12.7,-11.2)
    parts=dict(body=body,guide_lid=lid,twist_crown=crown,plunger=plunger,
               cross_pin=pin,lid_lock_key=key,top_retainer=retainer,
               bottle_gasket_TPU=bottle_gasket,lid_gasket_TPU=lid_gasket,
               valve_gasket_TPU=valve_gasket,stem_seal_TPU=stem_seal,
               thread_test_receiver=receiver,bottle_thread_coupon=coupon)
    fill_z=H-CFG['fill_headspace']
    compressed_valve=ring(11.12,8.25,1.1,seat-.4)
    fillspace=(chamber ^ cyl(cr,fill_z-seat,seat))-plunger-compressed_valve
    aux=dict(neck=neck,cavity=chamber,fillspace=fillspace,
             bottle_gasket=ring(13.4,10.65,.75,-.75),lid_gasket=ring(18.65,17.6,.75,H),
             valve_gasket=compressed_valve)
    dims=dict(height_mm=guide_top+2+11.2,diameter_mm=2*R,lift_mm=6,
              fill_z_mm=fill_z,usable_volume_ml=fillspace.m.volume()/1000,
              lid_z=lid_z,lid_top=L,pin_z=pz,guide_top=guide_top,crown_top=crown_top)
    return parts,aux,dims

PALETTE={'body':[142,177,151,255],'guide_lid':[186,204,188,255],
         'twist_crown':[48,107,74,255],'plunger':[225,169,60,255],
         'cross_pin':[220,137,47,255],'lid_lock_key':[206,149,63,255],
         'top_retainer':[79,132,98,255],'thread_test_receiver':[176,202,214,255]}
RIGID=['body','guide_lid','twist_crown','plunger','cross_pin','lid_lock_key','top_retainer']

def poses(parts,angle=0):
    return {n:s.r([0,0,-angle]) if n=='twist_crown' else s.t([0,0,lift_at(angle)])
            if n in ['plunger','cross_pin'] else s for n,s in parts.items()}

def print_transform(name,mesh):
    rot=[0,0,0]
    if name in ['twist_crown','top_retainer','guide_lid']:rot=[180,0,0]
    if name=='cross_pin':rot=[0,-90,0]
    if name=='lid_lock_key':rot=[90,0,0]
    mat=trimesh.transformations.euler_matrix(*np.radians(rot))
    mesh.apply_transform(mat); shift=-mesh.bounds[0,2];mesh.apply_translation([0,0,shift])
    return rot,float(shift)

SCAD_HELIX=r'''
// Closed polyhedron for a trapezoidal right-hand helix.
module helix(ri,ro,z0,turns,pitch,wi,wo) {
 n=ceil(turns*128);
 p=[for(j=[0:n]) for(k=[0:3]) let(a=360*turns*j/n,
 r=(k==0||k==3)?ri:ro,
 dz=k==0?-wi/2:k==1?-wo/2:k==2?wo/2:wi/2)
 [r*cos(a),r*sin(a),z0+pitch*turns*j/n+dz]];
 f=concat([for(j=[0:n-1]) for(k=[0:3]) each
 [[j*4+k,j*4+(k+1)%4,(j+1)*4+(k+1)%4],
 [j*4+k,(j+1)*4+(k+1)%4,(j+1)*4+k]]],
 [[0,2,1],[0,3,2],[n*4,n*4+1,n*4+2],[n*4,n*4+2,n*4+3]]);
 // OpenSCAD uses clockwise face order viewed from outside.
 polyhedron(points=p,faces=f,convexity=20);
}
'''

def main():
    parts,aux,dims=build();(ROOT/'stl').mkdir(exist_ok=True)
    print('Geometry constructed. Exporting meshes.',flush=True)
    report={'version':'LiftMix v3 compact concealed cam bench prototype','config_mm':CFG,
            'dimensions':dims,'mesh_checks':{},'physical_tests':'Not performed'}
    transforms={}
    for name,s in parts.items():
        mesh=tm(s); transforms[name]=print_transform(name,mesh)
        rec=dict(watertight=bool(mesh.is_watertight),winding_consistent=bool(mesh.is_winding_consistent),
                 components=len(mesh.split()),volume_mm3=float(mesh.volume),extents_mm=mesh.extents.tolist())
        report['mesh_checks'][name]=rec
        assert rec['watertight'] and rec['winding_consistent'] and rec['components']==1 and rec['volume_mm3']>0,(name,rec)
        mesh.export(ROOT/'stl'/f'{name}.stl')
        assert trimesh.load_mesh(ROOT/'stl'/f'{name}.stl').is_watertight,name
        print(name,rec['extents_mm'],flush=True)
    worst={}
    for angle in np.linspace(0,90,37):
        state=poses(parts,float(angle))
        for i,a in enumerate(RIGID):
            for b in RIGID[i+1:]:
                k=a+' / '+b;v=(state[a]^state[b]).m.volume()
                worst[k]=max(worst.get(k,0),v)
    report['motion_checks']={'poses':37,'max_overlap_mm3':worst}
    print('Motion max overlaps',worst,flush=True)
    assert max(worst.values())<1e-4,worst
    # Check thread insertion under simultaneous translation and right-hand rotation.
    threadworst={}
    for name,part,obstacle,pitch,travel in [
        ('bottle',parts['body'],aux['neck'],2.7,5.4),
        ('refill_lid',parts['guide_lid'],parts['body'],2.1,4.2),
        ('retainer',parts['top_retainer'],parts['guide_lid'],1.4,2.8)]:
        vol=0
        for rise in np.linspace(0,travel,25):
            v=(part.r([0,0,float(rise/pitch*360)]).t([0,0,float(rise)])^obstacle).m.volume()
            vol=max(vol,v)
        threadworst[name]=vol
    report['thread_insertion_checks']={'poses_per_joint':25,'max_overlap_mm3':threadworst}
    print('Thread overlaps',threadworst,flush=True)
    assert max(threadworst.values())<1e-4,threadworst
    assembly_worst=0
    for rise in np.linspace(0,20,21):
        moving=parts['twist_crown'].t([0,0,float(rise)])
        for n in ['body','guide_lid','plunger','cross_pin','lid_lock_key']:
            assembly_worst=max(assembly_worst,(moving^parts[n]).m.volume())
    report['crown_installation']={'state':'closed valve; top retainer removed',
                                'sampled_positions':21,'max_overlap_mm3':assembly_worst}
    assert assembly_worst<1e-4,assembly_worst
    report['seals']={'bottle_compression_mm':.25,'lid_compression_mm':.25,
                     'valve_compression_mm':.4,'stem_radial_squeeze_mm':.2,
                     'note':'Nominal CAD squeeze only. TPU sealing has not been tested.'}
    for state,angle in [('closed',0),('open',90)]:
        scene=trimesh.Scene()
        for n,s in poses(parts,angle).items():
            if n not in RIGID:continue
            mesh=tm(s);mesh.visual.face_colors=PALETTE[n];scene.add_geometry(mesh,node_name=n)
        scene.export(ROOT/f'LiftMix_v3_{state}.glb')
    scad='// LiftMix v3. Generated CSG CAD; edit source/build_compact.py for dimensional changes.\n'
    scad+='// Select part below, then F6 and export STL. Individual parts are oriented for printing.\n'
    scad+='part="assembly"; // [assembly,'+','.join(parts)+']\nangle=0; // [0:90]\n'
    scad+=SCAD_HELIX
    for n,s in parts.items():scad+=f'module {n}(){{{s.c}}}\n'
    for n,(rot,shift) in transforms.items():
        scad+=f'if(part=="{n}") translate([0,0,{shift}]) rotate({json.dumps(rot)}) {n}();\n'
    scad+='if(part=="assembly") {\n'
    for n in RIGID:
        tr='rotate([0,0,-angle]) ' if n=='twist_crown' else 'translate([0,0,6*min(1,max(0,(angle-8)/74))]) ' if n in ['plunger','cross_pin'] else ''
        scad+=f'color({(np.array(PALETTE[n][:3])/255).tolist()}) {tr}{n}();\n'
    scad+='}\n'
    (ROOT/'LiftMix_v3.scad').write_text(scad)
    (ROOT/'validation.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(dims,indent=2),flush=True)

if __name__=='__main__':main()
