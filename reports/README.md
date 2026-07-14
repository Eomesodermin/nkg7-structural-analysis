# Reports

Self-contained HTML reports — open directly in a browser; all figures are embedded
(no external assets needed). Each report has an intro, methods, results tables, an
embedded figure, a gate decision, limitations, and a glossary of field terms.

- **`nkg7_tier0_triage_report.html`** — Tier 0 triage (fold, sequence, genome, transcripts,
  domains, monomer pore). Verdict: NKG7 is a genuine claudin/PMP-22/Ca_V-γ tetraspan
  (Pfam PF00822 / IPR004031), but every structural and evolutionary analog is non-conducting
  (auxiliary Ca_V/TARP-γ subunits, paracellular claudins); no ion-transport or signalling
  domain; monomer occluded. **Gate: ESCALATE to Tier 1.**
- **`nkg7_tier1_oligomer_report.html`** — Tier 1 homo-oligomer prediction (C2–C6, three
  predictors) + reference-HOLE pore re-scan of all 15 models. No confident oligomer
  (best interface ipTM 0.63); pore-opening anti-correlates with confidence — every confident
  model is occluded, the only "open" models are low-confidence 60–115 Å splayed aggregates.
  **Gate: STOP the channel track.** Evidence against a self-contained channel, for a
  scaffold/auxiliary-modulator role.

## `data/`

Every underlying table (CSV/TSV), score file (JSON), per-workstream note (MD), and figure
(PNG) that feeds the two reports. See the individual notes for method detail and accessions.
