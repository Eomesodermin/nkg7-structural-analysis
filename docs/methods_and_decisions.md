# Methods and decisions

How the analysis was designed, what each stage found, and why the campaign stopped
where it did. Written in the order the work was done.

## 1. Framing: a hypothesis and a pre-registered counter-hypothesis

NKG7 is a four-transmembrane (4-TM) protein of cytotoxic-lymphocyte granules. Loss of NKG7
reduces Ca²⁺ influx in CD8⁺ T cells, and its fold resembles the Ca_V-γ (CACNG) auxiliary
subunits of voltage-gated calcium channels. That raises the question of whether NKG7 is itself
an ion channel.

Two readings were fixed before any analysis was run, and every stage was set up to test both:

- **H1 (channel):** NKG7 assembles into an oligomer that encloses a conducting pore.
- **H0 (scaffold / auxiliary modulator):** NKG7 is a channel-family *lookalike* that modulates
  Ca²⁺ signalling indirectly, as its Ca_V-γ / TARP-γ / GSG1L relatives do, and consistent with its
  known role inhibiting the v-ATPase to restrain mTORC1.

Family-precedent hits (Ca_V-γ, claudin, MP20) are expected under either reading and are not
treated as evidence for a pore. All conclusions are computational and would need
electrophysiology, bilayer reconstitution or Ca²⁺-flux imaging to confirm.

## 2. Design: a tiered, gated campaign

Stages run from cheap to expensive, and a negative result at one stage stops the spend on the
next. This keeps the compute proportional to the evidence.

| Tier | Question | Gate |
|------|----------|------|
| 0 Triage | What is NKG7: fold, relatives, transcripts, domains? Does a monomer conduct? | Escalate only if the family architecture justifies an oligomer test. |
| 1 Oligomer | Does any oligomer (C2–C6) enclose a pore with confident interfaces? | Stop the channel track unless a model is both confident and pore-enclosing. |
| Pivot: hetero-complex | If NKG7 is not a pore, what does it dock onto? | Needs a positive control to pass before negatives mean anything. |

Accessions (InterPro, Pfam, RefSeq, Ensembl) were taken from the live databases at run time
and not typed from memory.

## 3. Tier 0: triage

| Workstream | Result |
|-----------|--------|
| Fold (Foldseek, TM-align, PDB100 and AFDB/SwissProt) | The top 20 hits are about 10 claudins and 8–9 Ca_V/TARP-γ auxiliary subunits (TM-score 0.85–0.90, sequence identity ~10–19%). A chain-level check showed the "Ca²⁺ channel" hits match the γ *auxiliary* subunit (e.g. 3jbr → CACNG1, 9b5z → CACNG2), not the pore-forming α-subunit. There are no standalone conducting pores among them. |
| Sequence and genome (BLAST, Ensembl Compara, phmmer) | NKG7 is a BLAST singleton. Its closest paralog, GSG1L, is a claudin-fold auxiliary subunit of AMPA receptors. NKG7 sits in a chr19q13.4 tandem cluster with LIM2/MP20 and CLDND2. |
| Transcripts (Ensembl, GTEx v8) | The intact 4-TM, 165-aa isoform dominates every expressing tissue (79–89%). Expression is immune-restricted. There is no channel-diagnostic splicing. |
| Domains (InterProScan) | Claudin family (PF00822 / IPR004031). No ion-transport domain, no channel GO term, no signalling domain (no ITAM, ITIM, SH2 or PDZ). The only short motif is YETL. |
| Monomer pore | Occluded: narrowest constriction 0.65 Å (human) and 0.79 Å (mouse), below the radius of a water molecule. This is expected for a lone 4-TM subunit. |

**Gate: escalate.** NKG7 is a genuine member of the claudin / PMP-22 / Ca_V-γ superfamily, so the
oligomer test is justified. But every specific analogue is non-conducting, so Tier 0 sets a
sceptical prior for H1.

Method note: reference HOLE was not available for the monomer scan, so a geometric probe-sphere
sweep (the method HOLE implements) was used. The verdict is robust to its ±0.2 Å uncertainty,
and every Tier-1 model was re-scanned with reference HOLE.

## 4. Tier 1: oligomer prediction and pore test

**Predictors.** Homo-oligomers C2–C6 were predicted with three independent methods, so that no
single method's failure mode on membrane oligomers decides the result:

- Boltz-2 (MSA server, 3 recycling steps, 3 diffusion samples).
- AlphaFold3 3.0.1 (MSA computed once on the monomer and reused across orders).
- Chai-1 0.6.1 (cached ColabFold MSA, run without ESM embeddings because the ~4 GB weights
  could not be fetched on the compute node).

**Scoring.**
- Interface confidence is ipTM, taking the best model per stoichiometry. The ~0.5 floor and ~0.8
  "confident" bar are the usual conventions, not calibrated thresholds for this protein class.
- Pore radius is the minimum radius along each assembly's symmetry axis, from reference HOLE
  (MDAnalysis + mdahole2). A water molecule needs ~1.15 Å and a dehydrated Na⁺ ~1.0 Å.

**Result: the channel hypothesis is not supported on either criterion.**

1. *No confident oligomer.* The best interface ipTM is 0.63 (Boltz-2 dimer). The predictors
   disagree on both preferred stoichiometry and confidence: Boltz-2 prefers low orders and decays
   by C6, AlphaFold3 is uniformly low (0.16–0.22), and Chai-1 mildly prefers C5/C6 (~0.4). A
   well-defined assembly would not produce that divergence.
2. *Pore opening anti-correlates with confidence.* Every model with ipTM > 0.5 is occluded. The
   only "open" models are the lowest-confidence ones, and they have 60–115 Å pore axes, which
   means splayed, non-membrane-like aggregates and not a compact ~40 Å transmembrane channel. No
   model is both confident and pore-enclosing.

**Self-association is still real.** Independent wet-lab evidence (western-blot multimer bands and
NKG7 self-coprecipitation) shows NKG7 self-associates. The three predictors agree on a consensus
C2 interface (residues 2, 3, 6, 9, 10, 13, 17, 21, 24 in the N-terminus and TM1, plus 77, 80, 81
in TM2; Boltz–Chai Jaccard 0.59). It is a lateral TM1–TM1 helix-packing contact, which is exactly
why the pore stays shut, and it is the same self-association mode seen in claudins, Ca_V/TARP-γ,
GSG1L and PMP-22. Oligomerisation (supported) and pore formation (not supported) are separate
claims.

**Gate: stop the channel track.** Escalating to pore electrostatics or membrane MD on a
non-confident, occluded oligomer would not be informative.

## 5. Pivot: what does NKG7 dock onto?

Since NKG7's whole family works by docking onto a partner channel and regulating it, the
better-posed question after the negative pore result is what NKG7 binds. NKG7 was co-folded with
three candidates across all three predictors:

- **ATP6AP2**, a known NKG7 binder, as the **positive control**.
- **ORAI1**, the CRAC channel pore subunit.
- **STIM1**, the ER sensor that gates ORAI1.

No complex reached a confident interface (best cross-chain ipTM 0.59, AlphaFold3 with STIM1). The
positive control also failed the bar (0.10–0.33). So binary co-folding is under-powered for
NKG7's partnerships, and the ORAI1 and STIM1 negatives are **inconclusive**, not evidence of no
interaction. Follow-up should use higher-order co-folds (for example an NKG7–ORAI1 hexamer) and
experimental partner discovery (co-IP or proximity-labelling mass spectrometry).

## 6. Limitations

- All inputs are predicted structures (AlphaFold DB v6). No experimental NKG7 structure exists.
- Co-folding models are trained largely on soluble complexes. Their confidence on membrane
  homo-oligomers is less well characterised, and ipTM cut-offs are conventions, not calibrations.
- Static models cannot capture gating. This is why the result rests on *both* low confidence and
  occlusion in the confident models, not on occlusion alone.
- Chai-1 ran without ESM embeddings, which mainly affects per-residue accuracy, not interface
  confidence.
- No lipid environment or dynamics were modelled. Membrane MD was deliberately not escalated to
  (see the Tier 1 gate).
