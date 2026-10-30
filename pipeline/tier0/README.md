# Tier 0 workstream commands

Tier 0 ran against public web services rather than as standalone scripts. The exact
queries, accessions, and per-workstream method details are in the notes committed under
`reports/data/`:

- `NKG7_tier0b_sequence_homology_notes.md` — BLAST/Compara/phmmer commands + accessions
- `nkg7_tier0c_notes.md` — Ensembl isoform + GTEx queries
- `NKG7_Tier0D_domain_notes.md` — InterProScan job id + domain accessions
- `NKG7_monomer_pore_notes.md` — monomer pore-scan method

Foldseek (0A) ran as a CPU job on an HPC cluster:
`foldseek easy-search <NKG7.pdb> <PDB100db> <out.tsv> tmp --alignment-type 1`
(TM-align mode), then matched-chain identities resolved via the RCSB data API.
