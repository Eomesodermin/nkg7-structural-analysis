#!/usr/bin/env python3
"""Build AlphaFold3 inputs for NKG7 homo-oligomers C2-C6 from one monomer MSA.

AlphaFold3's data pipeline (MSA + templates) is run once on the monomer. This script reads that
``*_data.json`` and writes one input JSON per oligomer order with the same MSA and template
fields, so inference can run with ``--norun_data_pipeline``.

Usage:
    python af3_build_cn.py --af-out af_out --out-dir af_in
"""
import argparse
import glob
import json
import os

CARRIED_FIELDS = ("unpairedMsa", "pairedMsa", "templates")
ORDERS = range(2, 7)


def find_monomer_data(af_out):
    """Locate the monomer data JSON written by the AlphaFold3 data pipeline."""
    pattern_specific = os.path.join(af_out, "**", "nkg7_monomer*data*.json")
    pattern_any = os.path.join(af_out, "**", "*data*.json")
    candidates = glob.glob(pattern_specific, recursive=True) + glob.glob(pattern_any, recursive=True)
    if not candidates:
        raise FileNotFoundError(f"no monomer data JSON found under {af_out}/")
    return candidates[0]


def build_input(sequence, carried, order):
    """Return the AF3 input dict for ``order`` copies of the monomer."""
    protein = {"id": [chr(ord("A") + i) for i in range(order)], "sequence": sequence}
    protein.update(carried)
    return {
        "name": f"nkg7_c{order}",
        "modelSeeds": [1],
        "sequences": [{"protein": protein}],
        "dialect": "alphafold3",
        "version": 1,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--af-out", default="af_out", help="AF3 data-pipeline output directory")
    parser.add_argument("--out-dir", default="af_in", help="where to write the C2-C6 input JSONs")
    args = parser.parse_args()

    with open(find_monomer_data(args.af_out)) as handle:
        protein = json.load(handle)["sequences"][0]["protein"]
    carried = {key: protein[key] for key in CARRIED_FIELDS if key in protein}
    print("MSA fields carried:", {k: (len(v) if isinstance(v, str) else v) for k, v in carried.items()})

    os.makedirs(args.out_dir, exist_ok=True)
    for order in ORDERS:
        path = os.path.join(args.out_dir, f"af3_C{order}.json")
        with open(path, "w") as handle:
            json.dump(build_input(protein["sequence"], carried, order), handle)
        print(f"wrote {path} ({order} copies)")


if __name__ == "__main__":
    main()
