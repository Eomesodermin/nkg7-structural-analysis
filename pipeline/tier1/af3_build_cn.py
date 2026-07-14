#!/usr/bin/env python3
import json, sys, glob, os
# locate the monomer data json produced by the AF3 data pipeline
cands = glob.glob("af_out/**/nkg7_monomer*data*.json", recursive=True) + \
        glob.glob("af_out/**/*data*.json", recursive=True)
assert cands, "no monomer data.json found under af_out/"
data = json.load(open(cands[0]))
prot = data["sequences"][0]["protein"]
seq = prot["sequence"]
# carry over MSA + templates fields the data pipeline populated
carry = {k: prot[k] for k in ("unpairedMsa","pairedMsa","templates") if k in prot}
print("MSA fields carried:", {k:(len(v) if isinstance(v,str) else v) for k,v in carry.items()})
for n in range(2,7):
    p = {"id":[chr(ord('A')+i) for i in range(n)], "sequence":seq}
    p.update(carry)
    j = {"name":f"nkg7_c{n}","modelSeeds":[1],
         "sequences":[{"protein":p}],
         "dialect":"alphafold3","version":1}
    json.dump(j, open(f"af_in/af3_C{n}.json","w"))
    print("wrote af_in/af3_C%d.json (%d copies)"%(n,n))
