# Hetero-complex screen

The post-Tier-1 pivot: instead of asking whether NKG7 is a pore, ask **what NKG7 docks onto**.
NKG7 (chain A) co-folded with three candidate partners (chain B), three predictors each,
all bundled per GPU job.

| File | Partner | Why |
|------|---------|-----|
| `*_ATP6AP2.*` | ATP6AP2 (O75787) | **Known NKG7 binder — positive control** (v-ATPase/mTORC1 axis) |
| `*_ORAI1.*` | ORAI1 (Q96D31) | CRAC channel pore subunit — primary T-cell Ca²⁺ hypothesis |
| `*_STIM1.*` | STIM1 (Q13586) | ER Ca²⁺ sensor gating ORAI1 |

- `boltz/nkg7_<p>.yaml` — Boltz-2 (`--use_msa_server --recycling_steps 3 --diffusion_samples 5 --no_kernels`)
- `chai/nkg7_<p>.fasta` — Chai-1 (`--use-msa-server --no-use-esm-embeddings --num-diffn-samples 5`)
- `af3/nkg7_<p>.json` — AlphaFold3 (full MSA data pipeline per complex, apptainer)
- `sequences.json` — all four sequences (NKG7 + 3 partners)

**Result:** no complex reaches confident interface (best cross-chain ipTM 0.59, AF3·STIM1); the
positive control ATP6AP2 also fails the confidence bar (0.10–0.33) → binary co-folding is
under-powered for NKG7's partnerships (negatives inconclusive). See
`reports/nkg7_hetero_complex_report.html`. Recommended follow-up: higher-order co-folds and
experimental partner discovery (co-IP/proximity-labelling MS).
