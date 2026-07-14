# Tier 0D — NKG7 (Q16617) Domain / Motif / Topology Annotation

**Method:** InterProScan 5 run via EBI REST API (job `iprscan5-R20260714-092415-0953-39633323-p2m`, 2026-07-14) on the
full 165-aa human NKG7 sequence (UniProt Q16617). All accessions below are pulled **live** from that
run's JSON/TSV output — not from memory. Targeted motifs analysed by regex on the sequence in the
context of the InterProScan-derived topology.

## 1. Does NKG7 have any signalling or binding domains?
**No dedicated signalling or ligand-binding domain is detected.** The only domain-family assignments
are all the same tetraspan membrane-protein family — there is no kinase, phosphatase, SH2/SH3, PDZ,
ITAM/ITIM, ion-transport (e.g. Pfam Ion_trans / channel) or any enzymatic/adaptor domain.

Family / fold assignments (live accessions):
| Source | Accession | InterPro | Range | Score |
|---|---|---|---|---|
| Pfam | **PF00822** (PMP22_Claudin) | **IPR004031** "PMP-22/EMP/MP20/Claudin" | 11-149 | E=8.7e-7 |
| PROSITE pattern | **PS01221** (PMP22_1) | **IPR004032** "PMP-22/EMP/MP20" | 18-46 | pattern |
| PANTHER | **PTHR10671** "Epithelial membrane protein-related" | **IPR050579** "PMP22/EMP-like" | 2-154 | E=2.8e-26 |
| CATH-Gene3D | G3DSA:1.20.140.150 (claudin-like fold) | - | 2-158 | E=1.7e-14 |
| CATH-FunFam | G3DSA:1.20.140.150:FF:000033 "NK cell granule protein 7" | - | 48-162 | E=7.3e-65 |

**Channel-family assignment - CONFIRMED with exact IDs.** NKG7 is a bona-fide member of the
**PMP-22/EMP/MP20/claudin tetraspan superfamily** (Pfam **PF00822** / InterPro **IPR004031**;
PROSITE **PS01221**/**IPR004032**; PANTHER **PTHR10671**/**IPR050579**; CATH claudin-like fold
1.20.140.150). The plan's family assignment is therefore verified against the live databases.

**Bearing on the channel hypothesis - this cuts BOTH ways (mixed):**
- The claudin/PMP-22 fold IS the fold of tetraspan membrane proteins; claudins themselves build the
  paracellular pore, and the CACNG (Ca_V gamma) subunits belong to the broader claudin/PMP-22 structural
  clan. So NKG7 has the *architectural* prerequisite of this family.
- BUT PF00822/IPR004031 carries **no** ion-transport/pore Pfam domain, no channel GO term, no
  Ion_trans signature. The associated GO term is only GO:0016020 (membrane). Claudin pores are
  *paracellular* (between two cells), and Ca_V gamma is a *non-conducting regulatory* subunit. So the
  domain content is fully consistent with NKG7 being a tetraspan scaffold/modulator rather than a
  self-contained conducting channel. No domain-level evidence forces a channel interpretation.

## 2. TM topology - 4-TM CONFIRMED
**TMHMM predicts exactly four TM helices**, matching the assumed 4-TM topology within +/-2-4 residues:

| Element | Assumed | TMHMM | Phobius |
|---|---|---|---|
| TM1 | 9-29 | 7-29 | (merged into predicted signal peptide 1-37) |
| TM2 | 61-81 | 63-85 | 61-85 |
| TM3 | 92-112 | 92-114 | 92-113 |
| TM4 | 133-153 | 129-151 | 133-153 |

- **Orientation (Phobius):** N-tail cytoplasmic -> ECL1 non-cytoplasmic (38-60) -> TM2 -> short
  cytoplasmic loop (86-91) -> TM3 -> ECL2 non-cytoplasmic (114-132) -> TM4 -> C-tail cytoplasmic (154-165).
  Both inter-TM loops face the **luminal/extracellular** side; both tails are **cytoplasmic**. This
  matches the assumed topology (ECL1~30-60, ECL2~113-132).
- **Caveat:** Phobius mis-classifies TM1 as a cleaved signal peptide (1-37, hydrophobic core 7-25) -
  a well-known ambiguity for N-terminal TM helices of polytopic proteins. TMHMM (no signal-peptide
  model) recovers TM1 cleanly. NKG7 is not secreted, so TM1 is a genuine membrane anchor, not a
  cleaved signal. **4-TM topology stands.**

## 3. Targeted motifs
- **C-terminal tyrosine-sorting motif: YETL at 162-165** - matches the canonical **YxxPhi** endosomal/
  lysosomal-sorting signature (Y-x-x-[LIMFV]; here Y162-E-T-L165) at the exact C-terminus, on the
  **cytoplasmic** tail (correct side to be read by AP adaptor complexes). Consistent with NKG7's
  reported granule/lysosomal-membrane localisation. (Method: motif regex + topology.)
- **ITAM: none.** No Yxx[LI]-x(6-12)-Yxx[LI] pattern. The cytoplasmic segments are far too short to
  hold an ITAM/ITIM signalling module: N-tail = 6 aa, TM2-TM3 loop = 6 aa (PPGHGP), C-tail = 12 aa.
  There are only 4 tyrosines total (Y54 in ECL1, Y112 at TM3 edge, Y134 in TM4, Y162 in YETL) - none
  in a cytoplasmic context that could form an immunoreceptor signalling motif.
- **ITIM: a loose [SILV]xYxx[LV] match (SGYIHV, 52-57) exists but lies inside ECL1 (extracellular/
  luminal), so it is NOT a functional cytoplasmic ITIM.** Reported only for completeness.
- **Palmitoylation candidates:** 5 Cys total (C4, C19, C80, C145, C155). C19/C80/C145 are buried in
  TM helices. **C4 (cytoplasmic N-tail) and C155 (cytoplasmic, immediately after TM4)** are
  juxtamembrane cytoplasmic cysteines - plausible S-palmitoylation sites, typical for tetraspan
  proteins that partition into membrane microdomains. (Sequence/topology-based prediction; no
  dedicated palmitoylation API was available on the allowlist - flagged as candidate, not confirmed.)
- **Phosphorylation:** the only cytoplasmic S/T/Y available are in the 12-aa C-tail (HCGGPRPGYETL:
  no S/T) and 6-aa loops - negligible cytoplasmic phospho-acceptor surface; no evidence of a
  regulated phospho-site cluster.

## Summary bearing on the Ca2+-channel hypothesis
NKG7 is architecturally a **tetraspan claudin/PMP-22-fold protein** (confirmed, exact accessions
above) with a clean **4-TM topology**, two luminal loops, short cytoplasmic tails, a cytoplasmic
**YETL** lysosomal-sorting motif, and candidate juxtamembrane palmitoylation sites. It has **no
signalling, binding, or ion-transport domain**. The fold is *compatible* with the channel-adjacent
families invoked in the hypothesis (claudins, Ca_V gamma), but the domain content provides **no positive
signature of a conducting pore** and is equally consistent with a scaffold/modulator role. Domain
annotation is therefore **neutral-to-mixed**: it neither confirms nor excludes channel function, and
the decision must rest on the structural pore/oligomer analyses (Tier 1). All computational - requires
wet-lab confirmation.
