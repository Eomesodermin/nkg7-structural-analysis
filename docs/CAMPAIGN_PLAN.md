# NKG7 Ion-Channel Hypothesis — In Silico Evaluation Plan

**A self-contained handoff document. A fresh session should be able to execute this cold.**

Version 1.0 · Authored 2026-07-14 · Project: `proj_d2fe638c3a6f` (NKG7 work) · Cluster: marvin (Uni Bonn HPC)

---

## 0. TL;DR for the picking-up session

We suspect the immune protein **NKG7** may function as an **ion channel** (most plausibly a Ca²⁺-permeable channel), despite no documented channel activity. This document lays out a **tiered in silico campaign** (Tier 0 → Tier 3) to build — or fail to build — a structural/biophysical case for that hypothesis, and to characterize NKG7's gene, transcripts, and domains comprehensively.

**Your first actions, in order:**
1. Read this whole document.
2. Read the three companion skills (Section 3) — they contain reusable machinery you will lean on: `denovo-minibinder-pipeline`, `protein-loop-flexibility`, `marvin-hpc-campaigns`.
3. Check the running binder campaign's footprint on marvin before submitting anything (Section 4).
4. Create the marvin workspace (Section 5).
5. Execute Tier 0 (Section 7). Gate on its results before escalating.
6. Generate the per-tier HTML report as you finish each tier (Section 11).
7. Capture any genuinely new, reusable method as a skill (Section 12).

**Hard rules for this project (read Section 4 in full):**
- A **binder design campaign is running on marvin right now** using the same account (`ag_iei_abdullah`) and fair-share allocation. Be a good cluster citizen.
- The account cap is **300 running + 300 submitted jobs**. The binder campaign already holds up to ~260 tasks in waves. **Do not blow the cap.**
- **Tier 0–2 are cheap** (minutes-to-hours, small jobs) → fine to run on marvin now as short jobs.
- **Tier 3 is a real MD campaign** (multi-day GPU) → sequence it AFTER the binder run drains, or run it at a low throttle. Get explicit user go/no-go before launching Tier 3.

---

## 1. Introduction & scientific background

### 1.1 What NKG7 is (established facts, with citations)

NKG7 (Natural Killer cell Granule protein 7; aliases GMP-17, GIG-1; human gene on chromosome 19; UniProt **Q16617**, mouse **Q99PA5**) is a small (165-residue) **integral membrane protein whose expression is restricted to cytotoxic lymphocytes** — NK cells, CD8⁺ T cells, and cytotoxic CD4⁺ subsets. It localizes to the membranes of **cytotoxic/lysosomal-related granules** and translocates toward the plasma membrane on target-cell recognition.

**Topology (important for the channel question):** NKG7 is predicted to be a **four-transmembrane (4-TM) helical bundle with two luminal loops, short cytoplasmic N- and C-terminal tails**, and a C-terminal **YExL (YETL) lysosomal-targeting motif**. Our own prior modelling (AlphaFold Q16617) places the TM helices at residues 9–29, 61–81, 92–112, 133–153, with the two extracellular/luminal loops **ECL1 = 30–60** and **ECL2 = 113–132**.

**Known molecular function(s):**
- Regulator of **cytotoxic granule exocytosis** — NKG7-null lymphocytes degranulate poorly (reduced CD107a surface translocation) and kill targets less efficiently (Ng et al., *Nat Immunol* 2020).
- More recently, a **lysosomal role**: NKG7 interacts with the **v-ATPase** proton pump (via accessory subunit ATP6AP2 / the V0 domain) and **inhibits v-ATPase assembly/activity**, thereby restraining **mTORC1** signalling and promoting CD8⁺ T-cell durability (Ham et al., *Nat Commun* 2025).

### 1.2 Why an ion-channel hypothesis is credible

Two independent structural clues motivate the hypothesis:

1. **Family assignment.** NKG7 is reported to belong to the **PMP-22 / EMP / MP20 / Claudin tetraspan superfamily** — a 4-TM group that includes **claudins** (which form paracellular ion pores) and **MP20 / lens-fibre tetraspans**. ⚠️ **TO VERIFY IN TIER 0D:** confirm the exact InterPro/Pfam family accessions by running InterProScan on Q16617 and reading the InterPro entry directly (do NOT trust any accession numbers quoted from memory — the specific IPR IDs must be pulled from interpro.org, not assumed). Family membership does not prove channel function, but if confirmed it places NKG7 among proteins that build and gate membrane pores.

2. **Direct structural analogy to a Ca²⁺-channel subunit.** The literature explicitly notes that NKG7's **four membrane-spanning domains are structurally similar to the γ subunit of an L-type voltage-gated calcium channel (Ca_V γ / CACNG family)**, and that **loss of NKG7 significantly decreases Ca²⁺ influx** in CD8⁺ T cells stimulated with an inducer of Ca²⁺ release from acidic organelles (reviewed in *A Dual Role for NKG7…*, PMC12485375, 2025; primary Ca²⁺ data in the Ng/Corvino *Nat Immunol* 2020 line of work).

### 1.3 The honest counter-hypothesis (must be tested, not assumed away)

The Ca_V γ subunit that NKG7 resembles is a **regulatory / auxiliary** tetraspan — it modulates a channel formed by *other* subunits; **it is not itself the conducting pore.** Likewise, claudins form pores only as **paracellular strands between two cells**, and MP20's channel role is contested. So the family precedent is fully compatible with NKG7 being a **channel modulator, scaffold, or v-ATPase regulator that affects Ca²⁺ indirectly** — exactly what the v-ATPase/mTORC1 work suggests. The in silico campaign must be designed to **distinguish "NKG7 is itself a pore" from "NKG7 looks like a channel-family protein but has no conduction pathway of its own."** Both outcomes are scientifically valuable.

### 1.4 What in silico can and cannot deliver (set expectations up front)

**Can:** build a layered, falsifiable structural hypothesis — fold matches a channel family → an oligomer encloses a hydrated pore → the pore has a plausible selectivity filter → ions permeate in MD with a sensible selectivity order.

**Cannot:** prove channel function. Channel activity is *defined electrophysiologically*. Every conclusion here must be framed "computationally consistent with / against channel function," and flagged as requiring wet-lab confirmation (patch clamp, planar-bilayer reconstitution, ion-flux / Ca²⁺-imaging assays).

---

## 2. Objectives & decision structure

The campaign answers a chain of nested questions. Each tier **gates** the next — do not spend Tier-3 compute unless Tier 0–2 justify it.

| Tier | Question | Method (headline) | Cost | Gate to next tier |
|------|----------|-------------------|------|-------------------|
| **0** | What is NKG7 — by fold, sequence, gene, transcript, domain? | Foldseek + BLAST/MMseqs2 + Ensembl/genome + InterProScan + monomer pore scan | Minutes–1 h, mostly local/short marvin | Fold or domain match to a channel/pore family, OR any hint of a monomer pathway → proceed |
| **1** | Does NKG7 oligomerize into a pore-enclosing assembly? | Boltz-2 + Chai-1 + AlphaFold-Multimer homo-oligomer prediction (C2–C6), consensus, pore re-scan | ½–1 day GPU | A symmetric oligomer with high interface confidence AND a continuous TM pore (radius ≳1.0–1.5 Å) → proceed |
| **2** | Could that pore conduct ions, and selectively? | Pore lining physicochemistry + electrostatics (APBS) + selectivity-filter ID + ortholog conservation | Hours, cheap | A plausible, conserved selectivity filter / polar lining → justify Tier 3 |
| **3** | Do ions actually permeate? | Membrane MD (POPC bilayer, explicit ions) → hydration + spontaneous permeation → PMF / computational electrophysiology | Multi-day GPU | (Definitive-ish in silico endpoint) |

**Overall verdict logic:** a *strong* computational case requires **all four** tiers to line up. Any tier failing is itself an informative, publishable negative (e.g. "NKG7 has channel-family fold but no monomer or oligomer pore → consistent with a regulatory/scaffold role, not a conducting channel").

---

## 3. Established skills to build on (READ THESE FIRST)

Three personal skills already exist in this project's catalog. Load each with `skill({skill: "<name>"})` before doing related work — they carry curated machinery, env recipes, and marvin-specific gotchas that will save you days.

1. **`marvin-hpc-campaigns`** — Operational playbook for the marvin cluster. **Essential.** Covers: 192×A40 GPU inventory, the `ag_iei_abdullah` account, the **300 running / 300 submitted job cap**, `sshare` fair-share checks, the **AVX-512/AMD SIGILL trap** (easybuild binaries die with exit 132 on the AMD GPU nodes → pip-install tools instead), miniforge/conda activation, throttled SLURM array patterns (`--array=0-N%K`), measured per-tool GPU unit costs, the base64-fetch 64 KB cap, and — added this week — the **"Long-lived launcher processes over SSH"** section (detach wrappers with `setsid`; SSH client timeout does NOT kill the remote process).

2. **`denovo-minibinder-pipeline`** — The binder-design pipeline (RFdiffusion→ProteinMPNN→Boltz-2→Chai-1). **Relevant here for its structure-prediction plumbing**: how Boltz-2 and Chai-1 are installed and invoked on marvin, YAML construction for complexes, the `boltz` and `chai` conda envs, and multi-conformer campaign rendering. Tier 1 oligomer prediction reuses the Boltz/Chai invocation patterns directly.

3. **`protein-loop-flexibility`** — Tiered loop-conformer / MD-ensemble machinery. **Relevant for Tier 3**: it documents the `openmm-env` conda env, explicit-solvent MD setup (TIP3P/PME/NPT), positional-restraint scheme, trajectory/basin analysis, and the marvin `alphaflow` env. The membrane-MD in Tier 3 is an extension of the same OpenMM machinery (add `Modeller.addMembrane()`).

**Reuse principle:** before writing new code, check whether one of these skills already does it. If you extend one materially (e.g. add membrane-building to the MD machinery), fold that back into the skill (Section 12).

---

## 4. Cluster footprint & good-citizenship rules (NON-NEGOTIABLE)

### 4.1 There is a binder campaign running RIGHT NOW

A **full-scale de novo binder campaign was launched on marvin 2026-07-13 ~22:47** under the same account `ag_iei_abdullah` (verified still running 2026-07-14 morning, PID 399729, ~214 tasks). It is a ~2.2-day run, so **it may have finished by the time you read this — verify current state with the commands in §4.1 before assuming footprint.** As launched:
- Detached wave wrapper (`submit_fullscale_waves.sh`, PID recorded in project memory) running 9 conformer chains + 4 consensus phases.
- Holds up to **~260 array tasks in flight** in waves (4 chains × 65 tasks), releasing more as chains drain.
- Estimated ~3,360 GPU-h over ~2.2 days at 16 GPU/arm throttle.
- Emails `dcorvino@uni-bonn.de` on completion.

**Check its state before you submit anything:**
```bash
squeue -u dcorvino_hpc -h -r | wc -l          # total tasks in flight
squeue -u dcorvino_hpc --format='%.12i %.24j %.2t %.10M %R' | head -40
pgrep -af submit_fullscale_waves               # is the wrapper still alive?
```

### 4.2 The account limits (from `marvin-hpc-campaigns`)

- **Account:** `ag_iei_abdullah` — required on every job (`#SBATCH --account=ag_iei_abdullah`).
- **QOS `normal`:** no explicit per-user GPU cap, but **300 max running + 300 max submitted jobs** (job COUNT, not GPU count). The binder campaign already consumes a big slice of this.
- **Fair-share:** bills total GPU-hours, not peak concurrency. Running wide to finish fast is fair-share-neutral; the only cost of going wide is queue-wait. Account was rank #82/214, FairShare ≈ 0.544 (unpenalized) as of last check — re-verify with `sshare -A ag_iei_abdullah`.

### 4.3 Rules for THIS project's jobs

1. **Tier 0–2 = short/small jobs.** Individually a handful of tasks, minutes-to-hours each. **Safe to run on marvin now**, alongside the binder campaign — they won't threaten the cap. Still: submit as **single jobs or tiny throttled arrays** (`%2`–`%4`), never dozens of separate `sbatch` calls.
2. **Tier 3 = a real MD campaign.** Multi-day GPU. **Do NOT launch it while the binder campaign is still running** unless throttled very low (`%2`) and cleared with the user. Preferred: wait for the binder campaign's completion email, then launch Tier 3. **Get explicit user go/no-go before any Tier-3 submission.**
3. **Watch the combined footprint.** Before each submission: `squeue -u dcorvino_hpc -h -r | wc -l` and make sure `(existing + new) << 300`.
4. **One completion email per campaign phase**, held `afterany` on the array — never per-task mail (floods the shared mail relay).
5. **Detach long-lived launchers** (`setsid … & disown`) — see the SSH-launcher section in `marvin-hpc-campaigns`; a foreground wrapper in a timed SSH call becomes an orphan.
6. **AVX-512/AMD SIGILL trap:** any tool that dies with exit 132 / "Illegal instruction" on a GPU node → pip-install it (AVX2-safe) instead of using the easybuild module. Confirmed-safe: pip Boltz-2, pip Chai, conda-forge OpenMM, pip torch.

---

## 5. Marvin workspace (create a NEW one for this project)

**Do not reuse the binder workspace.** Create a dedicated project workspace so outputs don't collide and the footprint is auditable.

**Create it via the remote-compute layer** (load `skill({skill: "remote-compute-ssh"})` for the workspace-allocation call). Target path convention (mirrors the binder project's `dcorvino_hpc-nkg7_binder_design`):

```
WS=/lustre/scratch/data/dcorvino_hpc-nkg7_channel_hypothesis
```

Standard subdirectory layout to create:
```
$WS/
├── targets/            # input structures: NKG7 monomer AF models (human Q16617, mouse Q99PA5)
├── pipeline/           # all scripts + sbatch (MIRROR of the local repo pipeline/)
├── software/           # any tool installs (Foldseek, HOLE/CHAP, APBS) not in a conda env
├── envs/               # conda env export specs (yaml + pip freeze) for reproducibility
├── runs/
│   ├── tier0_triage/   # homology, genome, domain, monomer-pore outputs
│   ├── tier1_oligomer/ # Boltz/Chai/AF-multimer oligomer predictions + pore rescans
│   ├── tier2_pore/     # electrostatics, selectivity-filter, conservation
│   └── tier3_md/        # membrane MD (only if escalated)
└── reports/            # per-tier HTML reports
```

The AF monomer models already exist in the binder workspace at
`/lustre/scratch/data/dcorvino_hpc-nkg7_binder_design/targets/NKG7_human_Q16617_AF.pdb` and
`.../NKG7_mouse_Q99PA5_AF.pdb` — copy them into the new `$WS/targets/`, or re-fetch from AlphaFold DB
(`https://alphafold.ebi.ac.uk/files/AF-Q16617-F1-model_v6.pdb`, mouse `AF-Q99PA5-F1-model_v6.pdb`).

**Record the workspace path in project memory once created**, and append any new marvin operational learning to the `compute_details` doc for `ssh:marvin` (not to project memory).

---

## 6. Local mirroring & data organization (explicit destinations)

Three destinations, each with a defined purpose. **Keep them organized and documented.**

### 6.1 Code / scripts / SLURM / envs → local git repo `HPC_workflows`
**Path:** `/Users/dilloncorvino/Documents/Github/Eomesodermin/HPC_workflows/nkg7_channel_hypothesis/`
- Everything that is *not* heavy data: this plan, all pipeline scripts, sbatch files, conda env specs, per-tier HTML reports (they're small), READMEs, the design-decisions log.
- Structure:
  ```
  nkg7_channel_hypothesis/
  ├── NKG7_CHANNEL_HYPOTHESIS_PLAN.md   ← this document
  ├── README.md                          ← short orientation + status
  ├── docs/                              ← DESIGN_DECISIONS.md, glossary, per-tier method notes
  ├── pipeline/                          ← all scripts + sbatch (mirror of $WS/pipeline/)
  ├── envs/                              ← conda env yaml + pip freeze
  └── reports/                           ← the per-tier .html reports (small; commit them)
  ```
- **Remote is** `https://github.com/Eomesodermin/HPC_workflows.git`. Push via token URL: `https://x-access-token:${GITHUB_TOKEN}@github.com/...` (read `GITHUB_TOKEN` from the bash environment — **never write it to a file**; the `gh` CLI is not installed). The keychain `failed to store` / `-50` warnings are harmless.
- **`.gitignore`** heavy/regenerable output: `*.pdb`, `*.cif`, `*.dcd`, `*.xtc`, trajectory files, `*.mp4`, MD run dirs. Commit code, CSVs, small figures, and HTML reports.
- ⚠️ The `HPC_workflows` repo also holds `binder_design/`, `thymic_nk_development/`, and `ligand_cofold/` for OTHER projects — **leave those untouched.**

### 6.2 Small data products (.pdf, .csv, .html, small .png) → local `HPC_data`
**Path:** `/Users/dilloncorvino/Documents/HPC_data/nkg7_channel_hypothesis/`
- Fetched papers (PDF), result tables (CSV), the rendered HTML reports (a copy — canonical lives in the repo `reports/`), key figures, small representative structures worth keeping locally.
- This is the "look at the results without SSHing to marvin" directory. Organize by tier:
  `tier0/`, `tier1/`, `tier2/`, `tier3/`.

### 6.3 Heavy data (trajectories, full prediction sets, large structures) → stays on marvin `$WS/runs/`
- Do not pull multi-GB MD trajectories or full oligomer prediction ensembles to local. Keep them on marvin; pull only representative frames / ranked summaries / figures.
- Respect the **base64-fetch 64 KB cap** when pulling files through stdout — use the compute layer's output-staging or `split`/reassemble for anything larger, and always verify byte counts.

---

## 7. TIER 0 — Structural, sequence, genomic & domain triage

**Goal:** establish *what NKG7 is* from every cheap angle before spending GPU. **Cost:** minutes to ~1 h. **Venue:** mostly local + short marvin jobs. **Gate:** any channel/pore-family match (fold, domain, or sequence), or a hint of a monomer pathway, justifies Tier 1.

Tier 0 has **five workstreams (0A–0E)**, runnable in parallel.

### 0A — Fold-based homology search
- **Tool:** Foldseek (`easy-search`) against PDB100 + AFDB50; optionally the DALI web server for a second opinion. Foldseek is a small conda/pip install (`conda install -c conda-forge -c bioconda foldseek`); not GPU-bound.
- **Input:** NKG7 human AF monomer PDB (`$WS/targets/NKG7_human_Q16617_AF.pdb`), mouse as replicate.
- **Method:** `foldseek easy-search NKG7.pdb pdb100 aln.m8 tmp --alignment-type 1` (TM-align mode). Rank hits by TM-score / LDDT.
- **Read out:** Does the top structural neighborhood include **claudins (PF00822), MP20/MP17 lens tetraspans, tetraspanins (CD9/CD81), CACNG (Ca_V γ) subunits, connexins/pannexins, CALHM, or any bona fide ion channel**? Record top-20 hits with TM-score, target family, and whether it's a pore-former, a channel auxiliary subunit, or a non-channel tetraspan.
- **Interpretation:** a Ca_V γ / claudin / MP20 hit is *expected* (family precedent) and does NOT itself prove a pore. A hit to a genuine pore-forming channel would be a strong positive.

### 0B — Sequence homology: protein AND nucleotide (the user explicitly wants both)
- **Protein-level:**
  - **BLASTp / MMseqs2** of NKG7 (Q16617) against UniProt/nr — closest paralogs and orthologs, % identity, family boundaries. Expect MS4A? tetraspanins? the CACNG family? Report the closest *human paralogs* specifically (is there an NKG7-like gene family?).
  - **HMMER / hmmscan** against Pfam to get domain-level family assignment with E-values.
  - **jackhmmer / MMseqs2 profile** search for remote homologs the simple BLAST misses (channel homology may be distant).
- **Nucleotide / DNA-level:**
  - **BLASTn** of the NKG7 mRNA/CDS (RefSeq **NM_005601**) against nt / RefSeq_genomes — closest matching genes across species, synteny hints.
  - **Genomic neighborhood:** what genes flank NKG7 on chr19? (Its locus neighbors are informative — e.g. proximity to other immune/tetraspan genes.) Pull from Ensembl.
  - **tBLASTn** (protein query vs translated nucleotide) to find unannotated homologs / pseudogenes in genomes.
- **Tools/venue:** NCBI BLAST+ (`blastp`, `blastn`, `tblastn`) or the faster MMseqs2, both cheap CPU jobs on marvin's `intelsr_short`; or the web APIs for one-off queries. Ensembl REST API for genomic context.
- **Read out:** a ranked closest-match table (protein) + (nucleotide), the gene family, and any surprising channel-family relative.

### 0C — Transcript / splice-variant / expression analysis (user explicitly wants this)
Answer, with sources: **What are NKG7's splice variants? How dominant is each? Is usage tissue-distributed? Does any variant lose a domain (e.g. a TM helix)?**
- **Isoform catalog:** Ensembl (gene **ENSG00000105374**) + GENCODE + RefSeq + UniProt isoforms. Enumerate every annotated transcript, its exon structure, coding length, and biotype (protein-coding vs retained-intron vs NMD).
- **Dominance / expression:** **GTEx** (bulk tissue) and the **Human Protein Atlas** for transcript-level and per-isoform expression across tissues; expect NKG7 to be restricted to immune/blood, spleen, lung — quantify. If per-isoform quantification is available (GTEx isoform TPMs), report the dominant transcript per tissue.
- **Domain impact of splicing:** map each isoform's coding exons onto the 4-TM topology — does any variant **skip a TM helix or a loop**, truncate the YExL motif, or alter the N/C tails? A variant lacking a TM would be strong evidence about oligomer/pore competence.
- **Tools/venue:** Ensembl REST + `pyensembl`, GTEx portal API, HPA API — all lightweight local/API calls (allowlisted domains: ensembl, ncbi; GTEx/HPA may need a `request_network_access` grant — ask the user).
- **Read out:** an isoform table (transcript ID, length, biotype, TM/loop content, tissue dominance) + a per-tissue dominant-isoform summary.

### 0D — Comprehensive domain / motif search (user explicitly wants this)
Answer: **Does NKG7 have any known signalling or binding domains?**
- **InterProScan** (the umbrella: Pfam, PROSITE, SMART, CDD, PANTHER, TMHMM, SignalP, PHOBIUS) on the Q16617 sequence — the authoritative domain/motif call. Run the InterProScan container/module on marvin or the EBI web API.
- **Targeted motif checks:** the C-terminal **YExL/YETL lysosomal-targeting motif** (already known); any **ITAM/ITIM** immunoreceptor signalling motifs (NKG7 has short cytoplasmic tails — are they long enough to host one?); phosphorylation sites (NetPhos); palmitoylation/myristoylation (tetraspans are often palmitoylated — relevant to membrane microdomain partitioning).
- **TM topology confirmation:** DeepTMHMM / TMHMM / Phobius to independently confirm the 4-TM topology and loop boundaries we assumed from AlphaFold.
- **Read out:** annotated domain diagram (residue ranges), list of signalling/binding/trafficking motifs with confidence, and confirmed TM topology.

### 0E — Monomer pore analysis (the informative negative)
- **Tool:** HOLE2 (via `mdanalysis` `MDAnalysis.analysis.hole2`) or CHAP — compute the pore-radius profile along the membrane normal of the NKG7 **monomer** AF model.
- **Expectation:** a lone 4-TM bundle almost never encloses a continuous pore → expect **no through-membrane pathway** in the monomer. This is the *expected negative* that motivates the Tier-1 oligomer search.
- **Read out:** pore-radius-vs-axis plot; narrowest constriction radius; verdict (pore present/absent in monomer).

### Tier 0 gate
Escalate to Tier 1 if **any** of: (a) Foldseek/domain search matches a channel or pore-forming family; (b) a plausible remote channel homolog appears; (c) the monomer shows even a partial pathway; (d) the family/analogy precedent (Ca_V γ, claudin, MP20) is structurally confirmed. Given the strong prior (Section 1.2), Tier 1 is very likely warranted — but **let the data say so** and record the decision in `DESIGN_DECISIONS.md`.

---

## 8. TIER 1 — Oligomer prediction (the decisive structural step)

**Goal:** determine whether NKG7 assembles into a **symmetric oligomer that encloses a continuous transmembrane pore.** This is the make-or-break tier: most 4-TM proteins are not channels as monomers; a conducting pore, if any, forms at an oligomeric interface. **Cost:** ~½–1 day GPU (short jobs, small footprint). **Venue:** marvin GPU, small throttled jobs.

### Method
1. **Predict homo-oligomers C2 → C6** with three independent predictors and take consensus (membrane-protein oligomer prediction is individually unreliable):
   - **Boltz-2** (env `boltz`, installed) — build a complex YAML with N copies of the NKG7 sequence; request several diffusion samples. Reuse the YAML/invocation patterns from `denovo-minibinder-pipeline`.
   - **Chai-1** (env `chai`, installed) — same N-copy input, ESM-embedding mode (no MSA server needed).
   - **AlphaFold-Multimer / ColabFold** — the marvin ColabFold module (**beware the AVX-512 SIGILL trap** — if the easybuild ColabFold dies exit 132, use a pip/conda ColabFold or run AF-Multimer via the AF3 apptainer / a pip AF2). Provide the MSA; request all multimer models.
   - Optionally **AlphaFold3** (apptainer, on marvin) if available — best current multimer predictor.
2. **Symmetry & confidence gate:** for each stoichiometry, assess **ipTM / PAE-interface** (interface confidence) and visual symmetry. Keep assemblies with high interface confidence (ipTM ≳ 0.6) that form a **closed symmetric ring** with TM helices lining a central axis. Record all stoichiometries' scores even if they fail — the *preferred oligomeric state* is itself a finding.
3. **Pore re-scan** (HOLE2/CHAP) on each candidate oligomer: compute the radius profile along the symmetry axis. **A continuous radius ≳1.0–1.5 Å through the full TM span** = passable to water and (partially dehydrated) ions. Compare across C2–C6 to find which stoichiometry (if any) opens a pathway.
4. **Cross-check against the Ca_V γ analogy:** if a specific stoichiometry matches the known assembly geometry of the claudin/MP20/Ca_V γ relatives found in Tier 0, note it.

### Tier 1 gate
Proceed to Tier 2 only if a **confident symmetric oligomer with a continuous TM pore** emerges. If the best oligomer is confident but has **no pore** (helices pack tightly, no central pathway), that is a strong result **against** the channel hypothesis and **for** a scaffold/regulatory role — report it as such and stop (or pivot to characterizing the interface for its regulatory role). If no oligomer is confident at all, note the prediction is inconclusive and consider it a limit of current methods for small membrane proteins.

---

## 9. TIER 2 — Pore physicochemistry, electrostatics & conservation

**Goal:** given a candidate pore, decide whether it *could* conduct ions and with what selectivity — cheaply, before committing to MD. **Cost:** hours, cheap CPU. **Venue:** local or short marvin jobs.

1. **Pore-lining characterization:** identify residues lining the pore (within ~5 Å of the axis across the TM span). Profile **hydrophobicity vs position** — a long hydrophobic constriction ("hydrophobic gate") argues *against* conduction; a polar/charged lining argues *for*. Identify a candidate **selectivity filter** (the narrowest, most polar/charged ring).
2. **Electrostatics:** run **APBS + PDB2PQR** to compute the electrostatic potential along and around the pore axis. A net-negative (acidic) lining → cation-selective (consistent with a Ca²⁺/Na⁺ channel); net-positive → anion-selective. Map the potential onto the pore surface for the report figure.
3. **Selectivity-filter hypothesis:** name the specific residues forming the putative filter; check whether their identity/geometry resembles known Ca²⁺-selective filters (rings of acidic Asp/Glu, e.g. the EEEE locus of Ca_V channels) vs Na⁺/K⁺ filters.
4. **Conservation:** align NKG7 orthologs (start with human/mouse, already in hand; broaden with the Tier-0B ortholog set) and check whether the pore-lining / selectivity-filter residues are **conserved**. Real selectivity filters are under purifying selection; a non-conserved "filter" is likely an artifact. Reuse the ortholog-alignment approach from the binder project.

### Tier 2 gate
A **plausible, conserved, appropriately-charged selectivity filter** justifies the expensive Tier 3. A hydrophobic, non-conserved, or geometrically implausible lining argues the "pore" is non-conductive → report as a negative and stop.

---

## 10. TIER 3 — Membrane MD & permeation (definitive-ish, expensive)

**Goal:** test whether ions actually permeate the candidate pore, and quantify selectivity. **Cost:** multi-day GPU — a real campaign. **Venue:** marvin GPU. **⚠️ Do NOT launch while the binder campaign is running unless throttled to `%2` and cleared with the user. Get explicit go/no-go.**

1. **System build:** embed the best Tier-1 oligomer in an explicit **POPC bilayer + TIP3P water + physiological ions** (150 mM NaCl or KCl + added CaCl₂ for the Ca²⁺ hypothesis). Use OpenMM `Modeller.addMembrane()` (extends the `openmm-env` / `protein-loop-flexibility` MD machinery) or CHARMM-GUI Membrane Builder for a more curated system. Neutralize, add ions.
2. **Equilibration:** standard membrane-protein protocol — minimize, NVT with restrained protein, gradual restraint release, NPT (semi-isotropic barostat for the membrane), 310 K.
3. **Unbiased production MD:** 100+ ns × replicates. Watch for **(a) pore hydration** — does a continuous water wire form through the TM pore? (a dry pore cannot conduct) — and **(b) spontaneous ion permeation** events.
4. **Free-energy / quantitative selectivity (if a pore hydrates):**
   - **PMF** of Ca²⁺ / Na⁺ / K⁺ / Cl⁻ along the pore axis via umbrella sampling → predicted energy barrier per ion and the selectivity ordering.
   - **Computational electrophysiology** (applied transmembrane voltage / ion-gradient, the "double-bilayer" method) → estimate conductance if a genuine pore survives.
5. **Controls:** run the same protocol on (a) a known channel (positive control, e.g. a claudin pore or a small viroporin) and (b) a known non-channel tetraspan (negative control) so the NKG7 result is calibrated, not absolute.

### Tier 3 read-out
"NKG7 oligomer forms a hydrated pore that spontaneously conducts Ca²⁺ with barrier X kcal/mol and selectivity Ca²⁺ > Na⁺ > K⁺ ≫ Cl⁻" (strong positive) — or "the pore dehydrates / no permeation over N ns" (negative). Either is a genuine, publishable computational endpoint. **Still requires wet-lab confirmation.**

---

## 11. HTML report per tier (REQUIRED deliverable)

**Generate one self-contained `.html` report per tier**, written to both `$WS/reports/` (marvin) and `HPC_data/nkg7_channel_hypothesis/tierN/` + repo `reports/` (local). Each report is a standalone artifact a collaborator can open in a browser with no dependencies.

### Required contents of every tier report
1. **Header:** project title, tier name/number, date, author session, NKG7 identifiers (Q16617 / Q99PA5 / ENSG00000105374).
2. **Introduction:** what this tier asks and why (2–4 paragraphs, drawn from Sections 1–2), so the report reads standalone.
3. **Glossary box:** every field-specific term and program used in THIS tier, defined in one line each (Foldseek, TM-score, ipTM, PAE, HOLE, pore radius, selectivity filter, PMF, POPC, etc. — see Section 13 for the master glossary; include only the tier's relevant subset).
4. **Inputs:** exact input files (paths, checksums, sequence/structure IDs), parameters, and any decisions made (with rationale).
5. **Methods & code:** the actual commands/scripts run, embedded as formatted code blocks (syntax-highlighted `<pre>`). A reader should be able to reproduce the tier from the report alone.
6. **Compute stats:** for each job — tool + version, partition, GPUs/CPUs, wall time, GPU-hours, node, exit code. Pull from `sacct`. Include a small table.
7. **Results:** embedded figures (base64-inline the PNGs so the HTML is self-contained — do NOT link external files), result tables, and the numeric read-outs.
8. **Interpretation & gate decision:** what the tier found, whether the gate to the next tier is passed, and the explicit go/no-go recorded.
9. **Limitations:** method caveats specific to this tier.
10. **References:** the papers/tools cited in this tier (link to Section 14 master list).

### Implementation guidance
- Build reports with a small reusable Python helper (Jinja2 or f-string template → single `.html`). **This helper is itself a candidate reusable skill** (Section 12) — a "tiered-analysis-html-report" generator that any project could use. Base64-embed images via `<img src="data:image/png;base64,...">`.
- Follow the `figure-style` skill for any plots that go into the reports (`apply_figure_style()` before plotting).
- Keep a running **master report** (`reports/nkg7_channel_hypothesis_summary.html`) that links all tier reports and states the current overall verdict.

---

## 12. Reusable-skill generation (REQUIRED — do this as you go)

**Whenever this campaign produces a new, reusable method, capture it as a skill.** Do not wait until the end. Use the `customize` skill's `host.skills.*` API (load `skill({skill: "customize"})`). Candidate skills this project is likely to spawn:

1. **`membrane-protein-channel-eval`** (the headline new skill) — the whole Tier 0→3 ladder for "is protein X a channel?": fold/sequence/domain triage → oligomer prediction + pore scan → electrostatics/selectivity → membrane MD/permeation. This is broadly reusable for any candidate channel/transporter. Ship the pore-analysis, oligomer-prediction-wrapper, and APBS-driver code as `assets/` + a `kernel.py` with helper functions.
2. **`protein-pore-analysis`** (narrower, if the above is too big) — just the HOLE/CHAP pore-radius + APBS electrostatics + selectivity-filter-ID toolkit, taking any PDB/oligomer.
3. **`membrane-md-openmm`** — extend `protein-loop-flexibility` (or fork) with `Modeller.addMembrane()` bilayer building, computational-electrophysiology setup, and permeation/PMF analysis. **Prefer folding this into `protein-loop-flexibility`** if it fits, since that skill already owns the OpenMM MD machinery.
4. **`tiered-analysis-html-report`** — the self-contained per-tier HTML report generator from Section 11. Genuinely project-agnostic.
5. **`gene-transcript-domain-profile`** — the Tier-0C/0D workstream: given a gene/UniProt ID, produce the isoform catalog + tissue expression + domain/motif annotation as a standard report. Reusable for any gene-characterization task.

**For each:** follow `customize` → `skill-creator` guidance. Write `SKILL.md` (clear `description` with the field's own vocabulary so lexical search finds it), ship helper code as `kernel.py` / `assets/`, publish with `host.skills.publish`. **Offer the skill to the user** when a procedure settles, per platform norms. Record created skill IDs in project memory and in `docs/DESIGN_DECISIONS.md`.

**Also update the EXISTING skills** where this project teaches them something: any new marvin operational gotcha → `marvin-hpc-campaigns`; any MD/membrane extension → `protein-loop-flexibility`; any Boltz/Chai oligomer-prediction trick → `denovo-minibinder-pipeline`.

---

## 13. Master glossary (field-specific terms & programs)

*Include the relevant subset in each tier's HTML report.*

**Biology / structure**
- **NKG7** — Natural Killer cell Granule protein 7; 165-aa 4-TM lysosomal-granule membrane protein of cytotoxic lymphocytes. UniProt Q16617 (human), Q99PA5 (mouse); gene ENSG00000105374; RefSeq NM_005601.
- **TM (transmembrane) helix** — a membrane-spanning α-helix. NKG7 has 4 (res ~9–29, 61–81, 92–112, 133–153).
- **ECL (extracellular/luminal loop)** — loop between TM helices facing the granule lumen / extracellular space. NKG7 ECL1 = 30–60, ECL2 = 113–132.
- **Tetraspan / 4-TM superfamily** — proteins with four membrane passes; includes claudins, MP20, tetraspanins, PMP-22/EMP, Ca_V γ subunits.
- **Claudin** — tight-junction tetraspan that forms **paracellular** ion pores between cells.
- **Ca_V γ subunit (CACNG)** — auxiliary (regulatory, non-conducting) tetraspan subunit of L-type voltage-gated Ca²⁺ channels; the structural analog cited for NKG7.
- **v-ATPase** — vacuolar proton pump; NKG7 binds it (via ATP6AP2) and inhibits it, restraining mTORC1.
- **YExL / YETL motif** — C-terminal tyrosine-based lysosomal-targeting sequence.
- **Selectivity filter** — the narrowest, chemically-selective region of a channel pore that discriminates between ion species (e.g. the acidic EEEE ring of Ca_V channels).
- **Ion channel vs transporter** — a channel is a passive, gated pore for down-gradient ion flux; a transporter actively moves solutes with conformational cycling.

**Methods / programs**
- **AlphaFold / AF-Multimer / AF3** — deep-learning structure predictors (monomer / complex).
- **Boltz-2**, **Chai-1** — diffusion-based complex structure predictors (installed on marvin; AVX2-safe pip installs).
- **ipTM** — interface predicted TM-score (0–1); confidence in the *relative placement* of chains in a predicted complex. Higher = more reliable interface. Pass threshold here ≳0.6.
- **PAE** — Predicted Aligned Error (Å); per-residue-pair positional uncertainty; low interface PAE = confident interface.
- **TM-score** — structural-similarity score (0–1) between two folds; >0.5 = same fold.
- **Foldseek** — ultra-fast structural homology search (structure-vs-structure BLAST analog).
- **DALI** — structural alignment/comparison server.
- **BLASTp / BLASTn / tBLASTn** — sequence homology search (protein / nucleotide / translated-nucleotide).
- **MMseqs2**, **HMMER / hmmscan**, **jackhmmer** — fast sequence search and profile-HMM domain/family detection.
- **InterProScan** — umbrella domain/motif annotation (Pfam, PROSITE, SMART, CDD, PANTHER, TMHMM, SignalP).
- **DeepTMHMM / TMHMM / Phobius** — transmembrane-topology predictors.
- **HOLE2 / CHAP** — pore-radius profiling along a channel axis.
- **APBS + PDB2PQR** — Poisson–Boltzmann electrostatics of biomolecules (pore charge/selectivity).
- **GTEx**, **Human Protein Atlas (HPA)** — tissue expression databases (bulk and isoform-level).
- **Ensembl / GENCODE / pyensembl** — gene/transcript/isoform annotation.
- **MD (molecular dynamics)** — physics simulation of atomic motion over time.
- **OpenMM** — GPU MD engine (installed; `openmm-env`).
- **POPC** — a common phospholipid used to build model bilayers.
- **TIP3P** — a 3-point explicit water model. **PME** — Particle-Mesh Ewald (long-range electrostatics). **NPT/NVT** — constant pressure-temperature / volume-temperature ensembles.
- **PMF (Potential of Mean Force)** — free-energy profile along a reaction coordinate (here, ion position along the pore) from umbrella sampling; gives the permeation energy barrier.
- **Computational electrophysiology** — MD with an applied transmembrane voltage/ion gradient to measure simulated conductance.
- **Pore hydration / water wire** — a continuous column of water through a pore; prerequisite for ion conduction (a dry pore cannot conduct).

---

## 14. Key references (verify/expand as you go; fetch full text into HPC_data/…/tierN/)

**NKG7 function**
- Ng SS, et al. "The NK cell granule protein NKG7 regulates cytotoxic granule exocytosis and inflammation." *Nature Immunology* 21, 1205–1218 (2020). DOI 10.1038/s41590-020-0758-6. — degranulation/Ca²⁺ role; the founding functional paper.
- Ham H, et al. "Lysosomal NKG7 restrains mTORC1 activity to promote CD8⁺ T cell durability and tumor control." *Nature Communications* 16 (2025). DOI 10.1038/s41467-025-56931-6 (PMC11829009). — v-ATPase interaction, lysosomal role.
- "A Dual Role for NKG7 in T-cell Cytotoxicity and Longevity." *(review)* 2025, PMC12485375 / PubMed 40824199. — states the Ca_V γ structural analogy and the Ca²⁺-influx dependence explicitly.
- NKG7 enhances CD8⁺ T-cell synapse efficiency (PMC9299089); NKG7 in ITP platelet apoptosis (PMC12361763); ImmunoHorizons 2021 (exocytosis optimization).

**Family / structural context**
- InterPro PMP-22/EMP/MP20/Claudin tetraspan superfamily — NKG7's reported superfamily. ⚠️ Confirm the exact IPR/Pfam accessions via InterProScan on Q16617 in Tier 0D; do not cite specific IDs until retrieved from interpro.org.
- Claudin pore structure & paracellular selectivity (e.g. Suzuki et al., *Science* 2014, claudin-15) — for the pore-forming tetraspan comparison and as a Tier-3 positive control.

**Methods (cite the tool papers in reports)**
- Foldseek: van Kempen et al., *Nat Biotechnol* 2024. — AlphaFold: Jumper et al., *Nature* 2021; AF-Multimer: Evans et al. 2022; AF3: Abramson et al., *Nature* 2024. — Boltz-2: Passaro & Wohlwend et al. 2025. — Chai-1: Chai Discovery 2024. — HOLE: Smart et al., *J Mol Graph* 1996; CHAP: Klesse et al. 2019. — APBS: Jurrus et al., *Protein Sci* 2018. — InterProScan: Jones et al., *Bioinformatics* 2014. — OpenMM: Eastman et al., *PLoS Comput Biol* 2017. — MDAnalysis: Michaud-Agrawal et al. 2011 / Gowers et al. 2016.

*(Fetch full text with the article-fetch tool where DOIs are known; save PDFs to `HPC_data/nkg7_channel_hypothesis/tierN/refs/`.)*

---

## 15. Execution checklist for the picking-up session

```
[ ]  0. Read this document end-to-end.
[ ]  1. Load skills: marvin-hpc-campaigns, denovo-minibinder-pipeline,
        protein-loop-flexibility, remote-compute-ssh, customize, figure-style.
[ ]  2. Check binder-campaign footprint on marvin (squeue; pgrep wrapper).
        Confirm (existing + planned Tier0-2 jobs) << 300 cap.
[ ]  3. Create marvin workspace  $WS=/lustre/scratch/data/dcorvino_hpc-nkg7_channel_hypothesis
        + subdir layout (Section 5). Record path in memory.
[ ]  4. Copy/fetch NKG7 monomer AF models into $WS/targets/.
[ ]  5. Set up local dirs (already created):
        HPC_workflows/nkg7_channel_hypothesis/{docs,pipeline,envs,reports}
        HPC_data/nkg7_channel_hypothesis/{tier0..3}
[ ]  6. TIER 0 (0A fold, 0B seq+genome, 0C transcripts/expression,
        0D domains/motifs, 0E monomer pore). Short marvin/local jobs.
[ ]  7. Generate tier0 HTML report -> reports/ + HPC_data. Record gate decision.
[ ]  8. If gate passed: TIER 1 oligomer prediction (Boltz+Chai+AF-multimer,
        consensus, pore rescan). Small GPU jobs; mind the cap.
[ ]  9. tier1 HTML report + gate.
[ ] 10. TIER 2 electrostatics/selectivity/conservation. tier2 report + gate.
[ ] 11. TIER 3 membrane MD — ONLY after binder campaign drains OR throttled %2,
        AND explicit user go/no-go. tier3 report.
[ ] 12. Mirror ALL code/scripts/sbatch/envs -> HPC_workflows repo; commit + push.
        Copy small data/reports/PDFs -> HPC_data. Heavy data stays on $WS.
[ ] 13. Capture reusable skills as you go (Section 12); update existing skills.
[ ] 14. Maintain docs/DESIGN_DECISIONS.md (every decision + rationale) and the
        master summary HTML with the running overall verdict.
[ ] 15. One completion email per campaign phase; detach long-lived launchers.
```

### Overall verdict framing (for the final summary)
State the outcome as a **weight-of-evidence conclusion across tiers**, always caveated as computational:
- **Strong FOR:** channel-family fold + confident pore-enclosing oligomer + conserved charged selectivity filter + MD permeation with sensible selectivity.
- **Strong AGAINST:** no oligomer pore / hydrophobic non-conserved lining / no MD permeation → consistent with a regulatory/scaffold (e.g. v-ATPase-modulating) role, not a conducting channel.
- **Inconclusive:** predictions don't converge (a real limit for small membrane proteins) — state honestly and recommend the wet-lab experiments that would decide it.

**In all cases:** the deliverable is a computational hypothesis, not proof. Recommend the decisive wet-lab assays (patch clamp / bilayer reconstitution / Ca²⁺-flux imaging in NKG7-null vs WT cytotoxic lymphocytes).

---

*End of plan. This document + the three companion skills are sufficient to execute the campaign from a clean session.*
