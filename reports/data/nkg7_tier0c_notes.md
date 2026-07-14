# NKG7 Tier-0C — Transcript / Splice-Variant / Expression Analysis

**Gene:** NKG7 (natural killer cell granule protein 7), ENSG00000105374, chr19:51,371,606–51,375,628 (GRCh38, minus strand). HGNC:7830, Entrez 4818.
**Canonical protein:** UniProt Q16617, 165 aa. **RefSeq mRNA:** NM_005601 → ENST00000221978.
All coordinates/accessions pulled live from Ensembl REST, UniProt REST, and GTEx portal API (v8 / GENCODE v26 & v46 annotation as returned).

## 1. Isoform catalog (Ensembl, 13 annotated transcripts)
Ensembl currently annotates **13 protein_coding transcripts** for ENSG00000105374 (no retained_intron/NMD biotypes returned in this release). UniProt Q16617 annotates only a **single canonical isoform** (no ALTERNATIVE PRODUCTS entry) — the alternative transcripts are Ensembl/GENCODE predictions, most lacking UniProt/RefSeq protein support.

Three transcripts encode the full 165-aa product with all 4 TM helices intact and the C-terminal YETL motif:
- **ENST00000221978** (CANONICAL; RefSeq NM_005601 matched) — 4 exons, 165 aa
- ENST00001103012 — 6 exons, 165 aa (same protein, alternative UTR/exon splicing)
- ENST00001135145 — 4 exons, 165 aa (same protein)

The remaining 10 transcripts are truncated/alternatively-spliced predictions (71–155 aa) that **lose one or more TM helices**. Notable domain impacts (canonical numbering; TM1 9-29, TM2 61-81, TM3 92-112, TM4 133-153):
- **ENST00000595217 (142 aa, RefSeq NM_001363693):** retains TM1, **loses TM2**, TM3 partial, **loses TM4** and the YETL motif. This is the ONLY non-canonical isoform with RefSeq support and the #2 transcript in GTEx.
- ENST00001103016 (155 aa): retains only TM1; TM2/3/4 all lost.
- ENST00000595157 (89 aa): N-terminal half deleted — **loses TM1 & TM2**, keeps TM3+TM4+YETL.
- Several short forms (71–128 aa) retain only 1–2 TMs.

Full per-isoform TM/loop/motif mapping in `nkg7_isoform_table.csv`.

## 2. Domain impact of splicing — bearing on pore competence
A conducting or oligomerising channel would require the intact **4-TM bundle**. The single UniProt/RefSeq-supported protein, the canonical transcript, and the dominant GTEx transcript are **all the full 4-TM 165-aa form**. No well-supported, abundant isoform preserves a *reduced-but-still-multi-TM* architecture that would suggest a functionally distinct channel variant. The alternative isoforms that lose TMs are minor and (for the RefSeq-supported 142-aa form) also lose the YETL lysosomal-targeting motif, i.e. they would mislocalise — not a productive channel variant.

## 3. Expression / dominance (GTEx v8, gene-level median TPM)
Strong immune/blood restriction, exactly as expected for a cytotoxic-lymphocyte granule protein:
- **Whole_Blood: 498.1 TPM** (highest of 54 tissues)
- **Spleen: 167.1 TPM**
- **Lung: 56.5 TPM** (lung is lymphocyte-rich)
- All other tissues ≤ 11.5 TPM; brain is low (most Brain_* subregions 1.0–1.5 TPM, max 4.02 in spinal cord), pancreas 0.63 and cultured fibroblasts 0.10 (near-absent).

Per-isoform dominance (GTEx transcript-median TPM, GENCODE v26 = 5 quantified transcripts):
- Canonical **ENST00000221978 dominates: 79% (blood), 82% (spleen), 83% (lung)** of transcript signal. Across the other 51 tissues canonical dominance is tightly clustered (median 87.9%, range 58.5–89.7%): about half (25/51) reach ≥88% and about half sit in the ~78–88% band (e.g. EBV-lymphocytes 77.7%, Brain_Cerebellum 82.5%, Fallopian_Tube 86.3%), with only a few low-abundance tissues falling to ~59–61% (Kidney_Medulla 58.5%, Testis 61.0%). It is the majority transcript in every tissue.
- The truncated **ENST00000595217 (142 aa, TM2-lost)** is the second isoform at ~11–12% in blood/spleen/lung, but its share is variable across tissues — rising to 13–19% in several (e.g. EBV-lymphocytes 18.6%, Brain_Cerebellum 17.5%) and up to 39% in Testis (a low-expression, non-immune outlier).
- No tissue shows a truncated isoform becoming dominant — the canonical 4-TM form is the majority transcript everywhere; usage is NOT tissue-switched.

Per-tissue table in `nkg7_tissue_expression.csv`.

## 4. Bearing on the ion-channel hypothesis — NEUTRAL / mildly consistent
- **Consistent with channel plausibility (permissive, not evidence FOR):** the dominant, RefSeq/UniProt-supported product in every tissue is the intact 4-TM 165-aa form — so the structural prerequisite for a TM bundle/pore is present in the functional protein, and splicing does NOT normally destroy the TM architecture.
- **Does NOT support the channel hypothesis specifically:** there is no channel-diagnostic isoform (e.g. a splice variant creating/removing a pore-lining segment), no tissue-specific isoform switch, and no UniProt-annotated pore/selectivity-filter feature. The same intact-4-TM finding is equally consistent with the scaffold/modulator counter-hypothesis.
- Expression restriction to cytotoxic-lymphocyte-rich compartments is consistent with the granule-membrane biology but is orthogonal to whether the protein conducts ions.

**Conclusion:** transcript/expression evidence is NEUTRAL on channel vs modulator. It removes a potential objection (the working protein is the full 4-TM form, not a TM-deficient splice form) but provides no positive channel signal. Splice diversity is real at the transcript level but functionally minor. Requires wet-lab (electrophysiology) confirmation.

## Data sources
- Ensembl REST rest.ensembl.org (/lookup, /sequence, /xrefs) — GRCh38.
- UniProt REST rest.uniprot.org/uniprotkb/Q16617 — TM features & isoform count.
- GTEx portal API gtexportal.org/api/v2 — gene & transcript median expression, dataset gtex_v8.
