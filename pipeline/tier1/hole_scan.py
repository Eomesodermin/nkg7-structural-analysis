#!/usr/bin/env python3
import os, glob, json, warnings, numpy as np
warnings.filterwarnings("ignore")
import MDAnalysis as mda
from mdahole2.analysis.hole import HoleAnalysis

MODELS = sorted(glob.glob("*.pdb"))
HOLE_EXE = os.path.expanduser(os.environ.get("HOLE_EXE","")) or None
# find hole binary
import shutil
hole_bin = shutil.which("hole")
print("HOLE binary:", hole_bin)

def sym_axis(u):
    # chain centroids
    cents=[]
    for seg in u.segments:
        ca=seg.atoms.select_atoms("name CA")
        if len(ca)>0: cents.append(ca.center_of_geometry())
    cents=np.array(cents); center=cents.mean(0)
    cc=cents-center
    if len(cc)>=3:
        _,_,Vt=np.linalg.svd(cc); axis=Vt[2]  # normal to centroid plane
    else:
        # dimer: axis = perpendicular to the line joining the two, in the long-axis membrane direction
        # use overall principal axis of all CA instead
        ca=u.select_atoms("name CA"); X=ca.positions-ca.positions.mean(0)
        _,_,Vt=np.linalg.svd(X); axis=Vt[0]
    axis=axis/np.linalg.norm(axis)
    return center, axis

results={}
for m in MODELS:
    tag=m.replace(".pdb","")
    try:
        u=mda.Universe(m)
        center,axis=sym_axis(u)
        ha=HoleAnalysis(u, executable=hole_bin, cpoint=center, cvect=axis)
        ha.run()
        # profile: radius along pore for frame 0
        prof=ha.results.profiles[0]
        radii=np.array([p.radius for p in prof])
        zs=np.array([p.rxn_coord for p in prof])
        rmin=float(radii.min())
        results[tag]={"min_radius_A":round(rmin,2),
                      "n_points":len(radii),
                      "z_at_min":round(float(zs[radii.argmin()]),1),
                      "median_radius_A":round(float(np.median(radii)),2),
                      "axis_len_A":round(float(zs.max()-zs.min()),1)}
        # save profile
        np.savez(f"profile_{tag}.npz", radii=radii, zs=zs)
        print(f"{tag}: min_radius={rmin:.2f}A  axis_len={results[tag]['axis_len_A']}A  npts={len(radii)}")
        ha.delete_temporary_files()
    except Exception as e:
        results[tag]={"error":str(e)[:200]}
        print(f"{tag}: ERROR {str(e)[:150]}")

json.dump(results, open("hole_results.json","w"), indent=2)
print("\n=== SUMMARY (min pore radius, A) ===")
print("water needs ~1.15A, dehydrated Na+ ~1.0A")
for tag in sorted(results):
    r=results[tag]
    if "error" not in r:
        verdict="OPEN(water)" if r["min_radius_A"]>=1.15 else ("Na+only" if r["min_radius_A"]>=1.0 else "OCCLUDED")
        print(f"  {tag:12s} min={r['min_radius_A']:.2f}A  {verdict}")
    else:
        print(f"  {tag:12s} ERROR")
