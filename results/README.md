# Results

## Tier-1 oligomer models (`tier1_models/`)

Best predicted model per stoichiometry per predictor (15 PDBs). Naming:
`boltz_C{N}_model0.pdb`, `chai_C{N}_best.pdb`, `nkg7_c{N}_model.pdb` (AlphaFold3), N = 2..6.
These are the exact structures scored in the Tier-1 report and pore scan.

## Cross-predictor dimer interface (`nkg7_dimer_interface_consensus.json`)

Prompted by wet-lab evidence (western-blot multimer bands + NKG7 self-coprecipitation),
this analysis asks whether the three predictors agree on *how* NKG7 self-associates.
They do: all three C2 dimers share a consensus interface core (residues 2,3,6,9,10,13,17,21,24
= N-terminus + TM1, plus 77,80,81 = TM2), Boltz–Chai Jaccard 0.59. It is a **lateral
TM1–TM1 helix-packing interface** (subunits side-by-side), which is exactly why every
model's pore is occluded — and the same self-association mode as claudins, Ca_V/TARP-γ,
GSG1L and PMP-22 (all multimerise and self-coIP; none is a channel alone).

**Takeaway:** oligomerisation (supported by wet-lab AND corroborated by a reproducible
predicted interface) and pore-formation (not supported) are separate claims. NKG7 is a
self-assembling tetraspan scaffold, not a self-contained conducting channel.

Score tables for every tier live in `../reports/data/` (JSON/CSV).
