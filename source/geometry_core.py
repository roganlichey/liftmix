"""LiftMix v3 geometry utilities. Dimensions in mm. Python 3.11+.
Install: pip install manifold3d trimesh numpy
Run from any directory: python build_compact.py
Not a food-contact or pressure-qualified part. Receiver approximates a bottle neck; see README.md.
"""
from pathlib import Path
import json, math
import numpy as np
import trimesh
from manifold3d import Manifold, CrossSection

ROOT = Path(__file__).resolve().parents[1]
N = 96


class S:
    def __init__(self,m,c): self.m,self.c=m,c
    def __add__(self,o): return S(self.m+o.m, 'union(){'+self.c+o.c+'}')
    def __sub__(self,o): return S(self.m-o.m, 'difference(){'+self.c+o.c+'}')
    def __xor__(self,o): return S(self.m^o.m, 'intersection(){'+self.c+o.c+'}')
    def t(self,v): return S(self.m.translate(v),'translate('+json.dumps(v)+'){'+self.c+'}')
    def r(self,v): return S(self.m.rotate(v),'rotate('+json.dumps(v)+'){'+self.c+'}')

def cyl(r,h,z=0,r2=None):
    r2=r if r2 is None else r2
    return S(Manifold.cylinder(h,r,r2,N),f'cylinder(h={h},r1={r},r2={r2},$fn={N});').t([0,0,z])
def box(x,y,z,at=(0,0,0)):
    return S(Manifold.cube([x,y,z]),f'cube([{x},{y},{z}]);').t(list(at))
def ring(ro,ri,h,z=0): return cyl(ro,h,z)-cyl(ri,h+0.04,z-0.02)
def arc(ro,ri,z,h,angle,start=0):
    pts=[[ri,z],[ro,z],[ro,z+h],[ri,z+h]]
    m=Manifold.revolve(CrossSection([pts]),N,angle)
    s=S(m,f'rotate_extrude(angle={angle},$fn={N}) polygon(points={json.dumps(pts)});')
    return s.r([0,0,start])
def radial_pin(r,length,z): return cyl(r,length).r([0,90,0]).t([-length/2,0,z])
def tm(s):
    # Remove sub-micron CSG slivers before the float32 STL conversion.
    m=s.m.simplify(1e-6).to_mesh()
    mesh=trimesh.Trimesh(vertices=np.asarray(m.vert_properties)[:,:3],faces=np.asarray(m.tri_verts),process=True)
    # STL uses float32. Remove triangles collapsed by that conversion at CSG seams.
    mesh.update_faces(mesh.nondegenerate_faces(height=1e-8))
    mesh.update_faces(mesh.unique_faces())
    mesh.remove_unreferenced_vertices()
    return mesh
