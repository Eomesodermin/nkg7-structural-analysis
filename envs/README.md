# Compute environments

All structure prediction and pore analysis ran on the **marvin** SLURM cluster
(University of Bonn), one NVIDIA A40 GPU per predictor job. Environments are conda
envs on marvin; key package versions below (verified 2026-07-14).

| Env | Purpose | Key packages |
|-----|---------|--------------|
| `boltz` | Boltz-2 oligomer prediction | boltz-2 (weights `boltz2_conf.ckpt`, `boltz2_aff.ckpt`), PyTorch, CUDA |
| `chai` | Chai-1 oligomer prediction | `chai_lab` 0.6.1, PyTorch, CUDA |
| `poreanalysis` | reference-HOLE pore scan | MDAnalysis 2.10.0, mdahole2 0.5.0, HOLE binary, gemmi 0.7.5 |
| AlphaFold3 (module) | AF3 oligomer prediction | `AlphaFold3/3.0.1-apptainer` (apptainer container) |

## Reproducing the environments

- **Boltz-2**: `pip install boltz` (weights auto-download to `~/.boltz` on first run, or pre-cache).
- **Chai-1**: `pip install chai_lab==0.6.1`. ESM embeddings are optional; the compute node
  here could not fetch the ~4 GB ESM weights, so folding ran with `--no-use-esm-embeddings`
  and a cached ColabFold MSA. This mainly affects per-residue accuracy, not interface confidence.
- **AlphaFold3 3.0.1**: apptainer container. NOTE — inside the container the entrypoint is
  `/app/alphafold/run_alphafold.py` (NOT at the host install dir). MSA data pipeline is run
  once on the monomer (`--norun_inference`) then reused across C2–C6 (`--norun_data_pipeline`).
- **poreanalysis**: `conda create -n poreanalysis python=3.11 mdanalysis`; `pip install mdahole2`;
  the HOLE binary ships with the MDAnalysis HOLE2 support. `gemmi` for CIF→PDB conversion.

## Tier-0 web-service tools (no local env)

Tier 0 used public web APIs, not GPU jobs:
- **Foldseek** (structural homology) — ran as a CPU job on marvin against PDB100 + AFDB/SwissProt.
- **NCBI BLAST+** (BLASTp/n, tBLASTn), **Ensembl REST** (Compara, isoforms, locus),
  **EBI InterProScan 5 + phmmer**, **GTEx v8** — all via their public REST endpoints.
