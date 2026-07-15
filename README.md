# NKG7 Structural Analysis

**In-silico structural and evolutionary characterisation of NKG7** — a four-transmembrane
granule-membrane protein of cytotoxic lymphocytes (NK and CD8⁺ T cells) — using structure
prediction, structural-homology search, and pore analysis on a GPU cluster.

> **Headline finding.** NKG7 is a genuine member of the claudin / PMP-22 / Ca_V-γ (CACNG)
> tetraspan superfamily, and it self-associates — but it does **not** form a self-contained
> ion channel. Across three independent structure predictors and five oligomeric states, no
> confident assembly encloses a conducting pore; the reproducible self-interface it does form
> is a lateral helix-packing contact, the hallmark of a **scaffold / auxiliary-modulator**,
> not a pore. This matches its closest relatives (non-conducting Ca_V/TARP-γ auxiliary subunits
> and GSG1L) and its known role inhibiting the v-ATPase to restrain mTORC1.

---

## Background

NKG7 (Natural Killer cell Granule protein 7; UniProt **Q16617** human / **Q99PA5** mouse;
gene **ENSG00000105374**, chr19q13.4; RefSeq **NM_005601**) is a 165-aa, four-transmembrane
protein of cytotoxic-lymphocyte lysosomal/granule membranes. It has no documented channel
activity, yet its loss reduces Ca²⁺ influx in CD8⁺ T cells, and its four-TM architecture
resembles the Ca_V-γ (CACNG) auxiliary subunit of L-type Ca²⁺ channels — prompting the
hypothesis that NKG7 might itself be an ion channel (most plausibly Ca²⁺-permeable).

This project tests that hypothesis computationally, with an explicit, pre-registered
counter-hypothesis: that NKG7 is a channel-family *lookalike* that modulates Ca²⁺ **indirectly**
(scaffold/auxiliary role), the way its γ-subunit relatives do.

## Approach — a tiered, gated campaign

Each tier is cheap-to-expensive and gates the next: a negative result stops the spend.

| Tier | Question | Methods | Verdict |
|------|----------|---------|---------|
| **0 — Triage** | What *is* NKG7? Fold, relatives, gene/transcripts, domains; does the monomer conduct? | Foldseek, BLAST/Compara/phmmer, Ensembl+GTEx, InterProScan, monomer pore scan | **ESCALATE** — bona-fide tetraspan; every analog non-conducting; monomer occluded (expected) |
| **1 — Oligomer** | Does an oligomer enclose a pore? | Boltz-2 + AlphaFold3 + Chai-1 (C2–C6) + **reference HOLE** | **STOP channel track** — no confident oligomer; every confident model occluded |
| **(pivot) — Hetero-complex** | What does NKG7 dock *onto*? | Boltz-2 + AlphaFold3 + Chai-1 (NKG7 + ATP6AP2/ORAI1/STIM1) | **INCONCLUSIVE** — no confident interface; positive control (ATP6AP2) also fails the bar → binary co-folding under-powered |

### The decisive Tier-1 result

Two criteria, both negative, and they reinforce each other:

1. **No confident oligomer.** Best interface confidence anywhere is ipTM **0.63** (Boltz-2 dimer),
   below the ~0.8 confident bar. The three predictors *disagree* on both preferred stoichiometry
   and confidence — the signature of no well-defined assembly.
2. **Pore-opening anti-correlates with confidence.** Every model any predictor is confident about
   is **occluded** (sub-water). The only "open" models are the lowest-confidence ones, with 60–115 Å
   pore axes — splayed, non-membrane-like aggregates, not a compact ~40 Å transmembrane channel.
   No model is *both* confident *and* pore-enclosing.

Wet-lab context (western-blot multimer bands, NKG7 self-coprecipitation) confirms NKG7 **does**
self-associate — and the predictors corroborate a reproducible dimer interface. But that interface
is a **lateral TM1–TM1 helix-packing contact**, exactly why the pore stays shut. Oligomerisation and
pore-formation are separate claims: the first is supported, the second is not.

### The hetero-complex screen (post-Tier-1 pivot)

Since NKG7's whole family (Ca_V/TARP-γ, GSG1L) works by *docking onto a partner channel and
regulating it*, the better-posed question after the negative pore result is **what NKG7 binds**.
NKG7 was co-folded with three candidate partners — **ATP6AP2** (a known binder, used as a
positive control), **ORAI1** (the CRAC channel pore), and **STIM1** (its ER sensor) — across all
three predictors.

**No complex reached a confident interface** (best cross-chain ipTM **0.59**, AlphaFold3·STIM1;
confident bar ~0.8). Decisively, the **ATP6AP2 positive control also failed** the confidence bar
(0.10–0.33) — so the method is under-powered for NKG7's partnerships and the ORAI1/STIM1 negatives
are *inconclusive*, not evidence of no interaction. Full analysis:
[`reports/nkg7_hetero_complex_report.html`](reports/nkg7_hetero_complex_report.html). Recommended
follow-up: higher-order co-folds (NKG7 + ORAI1 hexamer) and experimental partner discovery
(co-IP / proximity-labelling mass-spec), given the independent western-blot/pulldown evidence that
NKG7 self-associates.

## Repository layout

```
docs/        CAMPAIGN_PLAN.md (full self-contained plan), DESIGN_DECISIONS.md (decision log)
pipeline/    tier0/ (workstream command references), tier1/ (predictor inputs + HOLE scan script)
envs/        compute-environment specifications (marvin cluster; Boltz-2 / AF3 / Chai-1 / HOLE)
targets/     NKG7 human + mouse sequences
reports/     self-contained HTML reports (Tier 0, Tier 1) + data/ (all underlying tables/figures)
results/     15 Tier-1 oligomer models (PDB) + cross-predictor dimer-interface analysis
```

## Reproducing

Structure prediction and pore analysis ran on the **marvin** SLURM cluster (University of Bonn),
one A40 GPU per predictor job. See [`envs/README.md`](envs/README.md) for environment specs and
[`pipeline/README.md`](pipeline/README.md) for the per-tier commands. Tier 0 used public web
services (NCBI, Ensembl, EBI/InterProScan, GTEx, Foldseek); Tier 1 used Boltz-2, AlphaFold3 3.0.1,
and Chai-1 0.6.1, with reference HOLE (mdahole2/MDAnalysis) for the pore scan.

**Heavy data** (full prediction output trees, MSAs, raw Foldseek TSVs) stays on the cluster; this
repository holds the scripts, the curated small results, the models scored in the reports, and the
reports themselves — enough to trace and re-run every conclusion.

## Related

- [`nkg7-binder-design`](https://github.com/Eomesodermin/nkg7-binder-design) — de-novo mini-binder
  design campaign against NKG7 (same target, complementary approach).

## Caveats

All results are **computational**. Channel function is defined electrophysiologically; any
positive would require wet-lab confirmation (patch clamp / bilayer reconstitution / Ca²⁺-flux
imaging). Predicted interface confidences (ipTM) are model-confidence proxies, not free energies.

---

*Cytotoxic-lymphocyte biology · structural bioinformatics · GPU structure prediction. Part of
ongoing work on NK/T-cell effector-molecule structure–function.*
