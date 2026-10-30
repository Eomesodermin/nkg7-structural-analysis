# Compute environments

Structure prediction ran on a SLURM GPU cluster (one NVIDIA A40 per predictor job). Tier 0 used
public web services and one CPU job. Key versions are below.

| Tool | Purpose | Version / notes |
|------|---------|-----------------|
| Boltz-2 | Oligomer and hetero-complex prediction | `pip install boltz`; weights download on first run |
| AlphaFold3 | Oligomer and hetero-complex prediction | 3.0.1, apptainer container |
| Chai-1 | Oligomer and hetero-complex prediction | `chai_lab==0.6.1` |
| MDAnalysis + mdahole2 + reference HOLE | Pore-radius profiles | MDAnalysis 2.10.0, mdahole2 0.5.0 (see `../environment.yml`) |
| gemmi | CIF to PDB conversion | 0.7.5 |

## Notes for reproducing

- **Boltz-2**: run with `--use_msa_server --recycling_steps 3 --diffusion_samples 3 --no_kernels`
  (homo-oligomers) or `--diffusion_samples 5` (hetero-complexes).
- **Chai-1**: ESM embeddings are optional. Folding ran with `--no-use-esm-embeddings` and a cached
  ColabFold MSA because the ~4 GB ESM weights could not be fetched on the compute node. This
  mainly affects per-residue accuracy, not interface confidence.
- **AlphaFold3**: the MSA data pipeline runs once on the monomer (`--norun_inference`), and
  inference then reuses it across C2–C6 (`--norun_data_pipeline`; see `pipeline/tier1/af3_build_cn.py`).
  Inside the container the entrypoint is `/app/alphafold/run_alphafold.py`, not the host install
  directory.
- **Reference HOLE**: `hole_scan.py` needs the HOLE2 binary on `PATH` (or `--hole-exe` /
  `$HOLE_EXE`). MDAnalysis's `mdahole2` is a wrapper around it.

## Tier 0 web services (no local environment)

- **Foldseek** (TM-align mode) against PDB100 and AFDB/SwissProt, run as a CPU job.
- **NCBI BLAST+** (BLASTp/n, tBLASTn), **Ensembl REST** (Compara, isoforms, locus),
  **EBI InterProScan 5 and phmmer**, and **GTEx v8**, all via their public REST endpoints.
