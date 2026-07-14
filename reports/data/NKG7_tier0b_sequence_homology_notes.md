# Tier 0B — Sequence Homology (protein + nucleotide) & Genomic Neighborhood

**Query:** human NKG7 / UniProt Q16617 (165 aa); mRNA RefSeq **NM_005601.4** (774 nt; CDS 120..617, 498 nt).
Gene IDs (pulled live): NCBI GeneID **4818**, HGNC **7830**, OMIM 606008, CCDS12830.1.
All results retrieved 2026-07-14 from live NCBI BLAST, Ensembl REST (GRCh38), and EBI HMMER.

## 1. Protein homology (BLASTp Q16617 vs nr, 250 hits)
- **Every one of the top 250 hits is an NKG7 ortholog.** Best hits are primate NKG7 (Gorilla/Pan 95.8% id, 100% cov), grading down through mammals (~57–75% id). "hypothetical protein" / "unnamed product" titles are unannotated orthologs at high identity, not paralogs.
- **No detectable human paralog.** The only *Homo sapiens* hits are NKG7 itself (NP_005592, and EAW72008 = NKG7 CRA isoform). No MS4A, no CACNG/CaV-γ, no claudin (CLDN), no PMP22/EMP at BLAST-detectable identity.
- Alias confirmations from hit titles: **GIG-1** (S69115, "granulocyte colony-stimulating factor induced gene"), **NKG7 / NK cell group 7 / GMP-17**.
- **Interpretation:** NKG7's reported similarity to CaV-γ (CACNG) and claudins is NOT at the primary-sequence level detectable by BLAST — it is a *fold/family* relationship (see §4).

## 2. Nucleotide homology (BLASTn CDS vs nt, 250 hits)
- NKG7 CDS is a **nucleotide singleton in human**: 100% self-hits (NM_005601, BC015759, S69115=GIG-1, synthetic clones) and one partial X-transcript; **no human paralogous locus**.
- Cross-species hits are all NKG7 orthologs: Pan/Gorilla 98.6%, gibbons/orangutan ~95%, Old-World monkeys ~94%. Confirms strict 1:1 orthology, no lineage-specific duplication.

## 3. tBLASTn (protein vs translated nt, 250 hits)
- No unannotated human homolog and **no processed/unprocessed pseudogene** detected. Best non-self human hit is the same NKG7 X-transcript (78.8% over a partial). No channel/tetraspan family member surfaces in translated genomes.

## 4. Gene-family placement (Ensembl Compara gene tree) — KEY RESULT
BLAST misses paralogs because they sit at 8–24% identity (below BLAST's floor). Ensembl gene-tree paralogy places NKG7 in the **PMP22 / EMP / MP20 / claudin tetraspan (4-TM) superfamily**:

| Paralog | Gene | Family role | ~%id to NKG7 | Tax level |
|---|---|---|---|---|
| ENSG00000187806 | **TMEM202** | 4-TM tetraspan | ~14–24% | Amniota |
| ENSG00000160318 | **CLDND2** | claudin-domain-containing | ~19% | Gnathostomata |
| ENSG00000105370 | **LIM2 / MP20** | lens tetraspan (MP20) | ~23% | Gnathostomata |
| ENSG00000169181 | **GSG1L** | AMPA-receptor auxiliary subunit (claudin fold) | ~11–22% | Gnathostomata |
| ENSG00000111305 | **GSG1** | claudin-fold tetraspan | ~8–18% | Gnathostomata |
| ENSG00000214978 | **GSG1L2** | claudin-fold tetraspan | ~12–21% | Gnathostomata |
| ENSG00000142227 | **EMP3** | epithelial membrane protein (PMP22 family) | ~15% | Vertebrata |
| ENSG00000134531 | **EMP1** | PMP22 family | ~13% | Vertebrata |
| ENSG00000213853 | **EMP2** | PMP22 family | ~13% | Vertebrata |
| ENSG00000109099 | **PMP22** | peripheral myelin protein 22 (family archetype) | ~16% | Vertebrata |

- **GSG1L is the notable relative for the channel hypothesis:** it is a *claudin-fold auxiliary subunit of AMPA-type glutamate-receptor ion channels* — the same architectural niche as CACNG/CaV-γ (also claudin-superfamily, also an ion-channel auxiliary subunit). So NKG7's closest functionally-characterised family members are **non-conducting regulatory/auxiliary channel subunits**, not pore-forming channels themselves.

## 5. Genomic neighborhood (chr19q13.41, GRCh38)
- **NKG7 locus: chr19:51,371,606–51,375,628, minus strand, protein_coding.**
- Immediate flanking protein-coding genes:
  - 5' side (lower coord): **CLDND2** (51,367,098–51,369,003, −) only **2.6 kb** away → a paralogous claudin-domain gene; then ETFB (5.2 kb).
  - 3' side (higher coord): **LIM2 / MP20** (51,379,909–51,388,264, −) **4.3 kb** away → another paralogous tetraspan; then C19orf84.
- NKG7 is **physically sandwiched between two of its own tetraspan paralogs (CLDND2 and LIM2)** — a local tandem cluster of the claudin/PMP22 superfamily, embedded in the larger chr19q13.4 SIGLEC/CD33 immune-gene cluster.
- No voltage-gated / ligand-gated pore-forming ion-channel gene is an immediate neighbor.

## Bearing on the channel hypothesis
**MIXED, leaning against a novel pore.**
- *For a channel-family connection:* NKG7 is a bona fide member of the claudin/PMP22 4-TM superfamily (Compara), and its paralog **GSG1L** plus the cited **CACNG/CaV-γ** are ion-channel-associated proteins — genuine family precedent for channel involvement. It sits in a local cluster of tetraspan paralogs.
- *Against NKG7 being a conducting pore:* the family precedent is dominated by **auxiliary/regulatory, non-conducting subunits** (GSG1L, CACNG/γ) and by **claudins that form pores only paracellularly (between cells), not as a single-protein transmembrane conductance**. There is no NKG7 paralog with documented single-protein ion-conduction. This is consistent with NKG7 modulating Ca²⁺ indirectly (scaffold/auxiliary, e.g. via its v-ATPase interaction) rather than being a channel of its own.

**Gate:** the sequence/genomic evidence neither proves nor excludes a channel; it establishes the correct family (claudin/PMP22 tetraspan, channel-auxiliary-adjacent). The distinguishing test is structural — oligomerisation + pore geometry (Tier 1). **Escalate.**

## Sources (live, retrieved 2026-07-14)
- NCBI BLAST URL API (blastp/blastn/tblastn vs nr/nt): RIDs recorded in blast_rids.json.
- NCBI E-utilities efetch: NM_005601.4 (mRNA + GenBank).
- Ensembl REST GRCh38: /lookup, /overlap/region (neighborhood), /homology (paralogues+orthologues, Compara gene tree).
- EBI HMMER phmmer vs UniProtKB (remote homology): job submitted; see status in output.

## 6. Remote homology (EBI HMMER phmmer vs UniProtKB) — completed
- 100 reported hits (E ≤ 1); 98/100 are NKG7 orthologs.
- **Top hit is NOT NKG7:** `tr|A0A8J6BAY0` **"Claudin domain-containing protein"** (E = 1.7e-118, 4 domains / 4-TM), scoring above human NKG7 itself. A second non-NKG7 hit is an amphibian claudin-domain-containing protein (`A0A821SV16`, E = 1.5e-69).
- **This is the remote-homology evidence BLAST missed:** at the profile/HMM level NKG7 is explicitly recognised as a **claudin-domain 4-TM protein**, independently corroborating the Ensembl Compara claudin/PMP22-superfamily placement (§4).
