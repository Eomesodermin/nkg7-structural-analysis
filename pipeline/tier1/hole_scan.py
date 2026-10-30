#!/usr/bin/env python3
"""Reference-HOLE pore scan of predicted NKG7 homo-oligomers.

For every ``*.pdb`` in ``--models-dir`` the script finds the assembly's symmetry axis,
runs HOLE along it (via MDAnalysis + mdahole2) and records the minimum pore radius.

Outputs (in ``--out-dir``):
    hole_results.json        per-model summary (min and median radius, axis length)
    profile_<model>.npz      radius profile along the pore axis, one file per model

Reference radii: a water molecule needs ~1.15 A and a dehydrated Na+ ~1.0 A.

Requires the ``hole`` binary on PATH (or set ``--hole-exe`` / ``$HOLE_EXE``).
"""
import argparse
import glob
import json
import os
import shutil
import warnings

import MDAnalysis as mda
import numpy as np
from mdahole2.analysis.hole import HoleAnalysis

WATER_RADIUS = 1.15  # A
NA_DEHYDRATED_RADIUS = 1.0  # A

warnings.filterwarnings("ignore")


def symmetry_axis(universe):
    """Return (centre, unit axis) of the assembly.

    With three or more chains the axis is the normal to the plane of the chain centroids.
    For a dimer the axis is the principal axis of all C-alpha atoms, which for a 4-TM
    protein lies along the membrane normal.
    """
    centroids = []
    for segment in universe.segments:
        ca = segment.atoms.select_atoms("name CA")
        if len(ca) > 0:
            centroids.append(ca.center_of_geometry())
    centroids = np.array(centroids)
    centre = centroids.mean(0)

    if len(centroids) >= 3:
        _, _, vt = np.linalg.svd(centroids - centre)
        axis = vt[2]
    else:
        ca = universe.select_atoms("name CA")
        _, _, vt = np.linalg.svd(ca.positions - ca.positions.mean(0))
        axis = vt[0]
    return centre, axis / np.linalg.norm(axis)


def scan_model(path, hole_exe, out_dir):
    """Run HOLE on one model and return its summary dict."""
    universe = mda.Universe(path)
    centre, axis = symmetry_axis(universe)
    analysis = HoleAnalysis(universe, executable=hole_exe, cpoint=centre, cvect=axis)
    analysis.run()

    profile = analysis.results.profiles[0]
    radii = np.array([p.radius for p in profile])
    zs = np.array([p.rxn_coord for p in profile])

    tag = os.path.splitext(os.path.basename(path))[0]
    np.savez(os.path.join(out_dir, f"profile_{tag}.npz"), radii=radii, zs=zs)
    analysis.delete_temporary_files()

    return {
        "min_radius_A": round(float(radii.min()), 2),
        "n_points": len(radii),
        "z_at_min": round(float(zs[radii.argmin()]), 1),
        "median_radius_A": round(float(np.median(radii)), 2),
        "axis_len_A": round(float(zs.max() - zs.min()), 1),
    }


def verdict(min_radius):
    """Classify a pore by its narrowest constriction."""
    if min_radius >= WATER_RADIUS:
        return "OPEN(water)"
    if min_radius >= NA_DEHYDRATED_RADIUS:
        return "Na+only"
    return "OCCLUDED"


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--models-dir", default=".", help="directory containing *.pdb models")
    parser.add_argument("--out-dir", default=".", help="where to write results and profiles")
    parser.add_argument(
        "--hole-exe",
        default=os.environ.get("HOLE_EXE") or shutil.which("hole"),
        help="path to the HOLE binary (default: $HOLE_EXE, else `hole` on PATH)",
    )
    args = parser.parse_args()

    if not args.hole_exe:
        parser.error("HOLE binary not found: put `hole` on PATH or pass --hole-exe")
    os.makedirs(args.out_dir, exist_ok=True)

    models = sorted(glob.glob(os.path.join(args.models_dir, "*.pdb")))
    if not models:
        parser.error(f"no *.pdb files in {args.models_dir}")
    print("HOLE binary:", args.hole_exe)

    results = {}
    for path in models:
        tag = os.path.splitext(os.path.basename(path))[0]
        try:
            results[tag] = scan_model(path, args.hole_exe, args.out_dir)
            r = results[tag]
            print(f"{tag}: min_radius={r['min_radius_A']:.2f}A  axis_len={r['axis_len_A']}A  npts={r['n_points']}")
        except Exception as exc:  # noqa: BLE001  one bad model must not stop the scan
            results[tag] = {"error": str(exc)[:200]}
            print(f"{tag}: ERROR {str(exc)[:150]}")

    with open(os.path.join(args.out_dir, "hole_results.json"), "w") as handle:
        json.dump(results, handle, indent=2)

    print(f"\n=== SUMMARY (min pore radius, A; water needs ~{WATER_RADIUS}, dehydrated Na+ ~{NA_DEHYDRATED_RADIUS}) ===")
    for tag in sorted(results):
        r = results[tag]
        if "error" in r:
            print(f"  {tag:12s} ERROR")
        else:
            print(f"  {tag:12s} min={r['min_radius_A']:.2f}A  {verdict(r['min_radius_A'])}")


if __name__ == "__main__":
    main()
