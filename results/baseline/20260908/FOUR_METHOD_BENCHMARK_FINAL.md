# FABRIC-AI four-method benchmark — final frozen comparison

Status: `FOUR_METHOD_BENCHMARK_FINAL_FROZEN`

## Common task

All shared gene-level comparisons use the corrected v1 common model and the corrected **235-gene** admissible single-gene knockout space. The product reaction is `FABRIC_r_4799`, biomass is `r_2111`, and the common numerical tolerance is `1e-7`.

Public baselines:

- FastKnock — Hassani et al., 2024, *Microbial Cell Factories*, DOI `10.1186/s12934-023-02277-x`.
- CFSA — van Rosmalen et al., 2024, *Metabolic Engineering Communications*, DOI `10.1016/j.mec.2024.e00244`.
- OptEnvelope — Motamedian et al., 2023, *PLOS ONE*, DOI `10.1371/journal.pone.0294313`.

FABRIC-AI method:

- `FABRIC-AI Production Optimizer benchmark v1.2`, Design mode, current project.

## Final benchmark table

| Method | Native/shared output in this benchmark | Gene-level phenotype coverage of corrected 235-space | Guaranteed-production result | Experiment-planning output | Recorded formal runtime | Numerical/audit result |
|---|---|---:|---|---|---:|---|
| FastKnock 2024 | 0 legal native gene candidates | 0 / 235 candidate rows | Candidate-quality metrics N/A | No candidate list returned | 9.912 s | 51/51 visited actions passed flux audit |
| CFSA 2024 | 14 legal mapped single-gene KO candidates from native sampling recommendations | 14 / 235 = 5.96% | 0/14 had positive `Pmin` at the shared 10% WT growth floor | 14 mapped KO candidates retained in native order | ≤1416.77 s active-execution accounting | 30,000/30,000 native valid samples across 3 scenarios; shared independent evaluation completed |
| OptEnvelope 2023 | Corrected GLPK compatibility run returned 11 empty sequential reaction sets and 0 mappable gene rows | 0 / 235 mapped candidate rows | Gene-level candidate-quality metrics N/A | No mappable single-gene list returned | 3114.15 s | 11/11 target points completed; corrected run and transfer audit frozen |
| **FABRIC-AI Production Optimizer v1.2** | **235/235 admissible genes explicitly phenotyped; deterministic Design-mode ordering generated** | **235 / 235 = 100% under v1, and the same 235 / 235 evaluated under v2A sensitivity** | **Automatically detected `NON_DISCRIMINATING_GUARANTEED_PRODUCTION`: all primary GCP and Pmin95 values were 0** | **Produces a complete auditable phenotype table and a deterministic `SECONDARY_FEASIBILITY_ORDER_ONLY` Top-6 when production lower bounds are non-discriminating** | **635.91 s for fresh prepare + v1 evaluate + v2A evaluate + rank** | **0 footprint mismatches, 0 solver failures; 9 ranking tests passed; independent ranking verification 15/15 passed** |

Runtime values are the recorded formal executions of each implementation and are reported for reproducibility; the methods perform different native workloads.

## What the benchmark establishes

The shared single-gene task contains no positive guaranteed-production discriminator under the current v1 model: CFSA's 14 mapped KO candidates and all 235 FABRIC-AI primary candidates have zero guaranteed-production lower bounds, while FastKnock and the corrected OptEnvelope compatibility run return no gene-level candidates for that metric.

FABRIC-AI adds a distinct experiment-planning layer on top of the common metabolic model. It evaluates the **entire admissible gene space**, preserves the same primary 235-gene set under the v2A production-stage sensitivity condition, detects when a production objective has lost discriminative power, applies native-unit numerical equivalence before ranking, and emits a deterministic secondary feasibility order without converting numerical noise or `Pmax` differences into an overproduction claim.

The current frozen secondary Top-6 is:

1. `YAL060W`
2. `YBR006W`
3. `YBR011C`
4. `YBR183W`
5. `YBR281C`
6. `YCR005C`

All six rows are explicitly labeled `SECONDARY_FEASIBILITY_ORDER_ONLY`.

## Silver C.2.3 evidence statement

**Claim:** FABRIC-AI has explicit evaluation metrics and is compared with three recent public strain-design baselines under a frozen common model and candidate contract.

Recommended judging-form table:

| Method | Source/year | Evaluation metric | Frozen result |
|---|---|---|---|
| FastKnock | Hassani et al., 2024 | legal single-gene output; shared guaranteed-production evaluation | 0 legal candidates; candidate-quality metrics N/A |
| CFSA | van Rosmalen et al., 2024 | mapped KO count; `Pmin` under shared 10% WT growth floor | 14 legal KO candidates; 0/14 positive `Pmin` |
| OptEnvelope | Motamedian et al., 2023 | mappable single-gene output from corrected compatibility run | 0 mappable gene rows from 11 completed target points |
| **FABRIC-AI** | **This project** | **full admissible-space phenotype coverage; GCP/Pmin95 non-discrimination detection; multi-condition robustness; deterministic experiment-priority output** | **235/235 evaluated under v1 and 235/235 under v2A; 0 solver failures; non-discrimination detected and secondary Top-6 generated** |

## Gold C.3.2 evidence route — significant innovation

Recommended key task name:

**Genome-scale intervention triage under non-discriminating production objectives**

Recommended statement:

> FABRIC-AI extends strain-design output from candidate discovery to a complete, auditable experiment-planning workflow. On the frozen 235-gene task, FastKnock returned 0 legal gene candidates, CFSA mapped 14 KO candidates, and the corrected OptEnvelope compatibility run returned 0 mappable gene rows. FABRIC-AI phenotyped all 235 admissible genes under the primary condition and all 235 again under a production-stage sensitivity condition, detected that guaranteed-production metrics were globally non-discriminating, and switched to a deterministic feasibility-oriented ordering governed by frozen numerical-equivalence and no-leakage rules. Design mode is separated from Learn mode, allowing wet-lab feedback to update later evidence tiers without backfilling the public-baseline ranking.

This supports C.3.2 through the **significant-innovation** route: full-space phenotype coverage, explicit non-discrimination detection, multi-condition robustness reporting, deterministic numerical-equivalence-aware ranking, and a Design/Learn separation that connects computational design to the project's DBTL feedback loop.

## Frozen evidence anchors

- FastKnock corrected replay: `FASTKNOCK_CORRECTED_235_REPLAY_FROZEN`.
- CFSA: 14 mapped KO candidates; existing independent-evaluation rows remain valid after the 237→235 correction.
- OptEnvelope: `OPTENVELOPE_V1_CORRECTED_COMPATIBILITY_RUN_FROZEN`; 0 mappable gene rows, not a universal theoretical zero-candidate claim.
- FABRIC-AI: `FABRIC_AI_V1_2_DESIGN_MODE_FINAL_FROZEN`; final ranking correction ZIP SHA-256 `7cea8b7f7c501a7b5130cd069c952686d045c1406cdff06321f0cca8a02b15d7`.
