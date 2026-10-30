# Pipeline

Tiered, gated in-silico workflow. Each tier's result decides whether the next runs.

```
Tier 0  triage      structural + sequence + genome + transcript + domain; monomer pore
   │  gate: ESCALATE (NKG7 is a claudin/Ca_V-γ tetraspan; monomer occluded as expected)
   ▼
Tier 1  oligomer    homo-oligomer C2–C6 × 3 predictors + reference-HOLE pore re-scan
   │  gate: STOP channel track (no confident oligomer; every confident model occluded)
   ▼
(pivot) hetero-complex  NKG7 vs ATP6AP2 / ORAI1 / STIM1 (inconclusive; positive control fails)
```

## Tier 0 — triage (`pipeline/tier0/`)

Five independent workstreams, run in parallel; all use public web services (no GPU):

| Workstream | Tool | Question |
|-----------|------|----------|
| 0A fold | Foldseek (TM-align mode) vs PDB100 + AFDB/SwissProt | What fold is NKG7? What are its closest *structural* neighbours, and are they channels? |
| 0B sequence + genome | NCBI BLASTp/n, tBLASTn; Ensembl Compara; EBI phmmer | Closest sequence relatives, paralogs, genomic neighbourhood |
| 0C transcripts | Ensembl REST isoforms; GTEx v8 | Splice isoforms, TM integrity, tissue expression, dominant isoform |
| 0D domains | EBI InterProScan 5 (Pfam/PROSITE/PANTHER/TMHMM/Phobius) | Any ion-transport or signalling domain? TM topology? |
| 0E monomer pore | HOLE-equivalent probe sweep on the AF monomer | Does the monomer alone enclose a pore? |

Reproduce: the exact accessions and commands are documented in each Tier-0 note under
`reports/data/NKG7_tier0*_notes.md` and `NKG7_Tier0D_domain_notes.md`. Foldseek was the
only compute job; the rest are REST calls with the query = the NKG7 sequence/AF model.

## Tier 1 — oligomer prediction + pore test (`pipeline/tier1/`)

Homo-oligomer prediction for orders C2–C6 with **three independent predictors**, then a
**reference-HOLE** pore scan of every model. Consensus across predictors guards against any
single method's membrane-oligomer failure mode.

| File | Role |
|------|------|
| `boltz_C{2..6}.yaml` | Boltz-2 input specs (N protein copies) — run with `boltz predict --use_msa_server --recycling_steps 3 --diffusion_samples 3 --no_kernels --output_format pdb` |
| `chai_C{2..6}.fasta` | Chai-1 multi-record FASTAs — run with `chai-lab fold --msa-directory <cached> --no-use-esm-embeddings` |
| `af3_monomer.json` + `af3_C{2..6}.json` | AlphaFold3 inputs — MSA once on the monomer, reused across orders |
| `af3_build_cn.py` | Injects the monomer MSA (unpairedMsa/pairedMsa/templates) into the C2–C6 AF3 jsons (`--af-out`, `--out-dir`) |
| `hole_scan.py` | Reference-HOLE pore scan (mdahole2/MDAnalysis) along each assembly's symmetry axis; reports min pore radius (`--models-dir`, `--out-dir`, `--hole-exe`) |

Each predictor ran its full C2–C6 sweep as a single A40 GPU job.

Scoring: interface confidence = **ipTM** (best model per stoichiometry). Symmetry = chain-centroid
radial/angular CV. Pore = minimum HOLE radius (water needs ~1.15 Å, dehydrated Na⁺ ~1.0 Å).

## Hetero-complex screen (`pipeline/hetero/`)

See [`hetero/README.md`](hetero/README.md) for the partner inputs and commands.

## Run order

1. Tier 0: follow the notes listed in [`tier0/README.md`](tier0/README.md).
2. Tier 1: run each predictor on its inputs above. For AlphaFold3, run the monomer data
   pipeline first, then `af3_build_cn.py`, then inference for C2–C6.
3. Pore scan: `python tier1/hole_scan.py --models-dir <models> --out-dir <out>`.
4. Hetero-complex: run the three predictors on the inputs in `hetero/`.
