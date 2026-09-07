# FABRIC-AI benchmark status — 2026-09-07

Branch: `benchmark/fabric-ai-20260907`

This directory archives validated benchmark evidence before Wiki/Judging-Form freeze. Historical invalid/intermediate outputs are not promoted to final claims.

## Corrected v1 candidate space

- Canonical model unchanged.
- Corrected legal single-gene KO pool: **235 genes**.
- Historical 237-gene pool contained two false-feasible entries caused by stale solver state during KO growth admission: `YER014W` (`r_0942`) and `YOR176W` (`r_0436`).
- CFSA's 14 mapped KO candidates do not contain either gene, so their existing independent-evaluation rows remain valid.
- FastKnock must be replayed once on the corrected 235-gene pool before final freeze.

## OptEnvelope v1 corrected closeout

Status: `OPTENVELOPE_V1_CORRECTED_COMPATIBILITY_RUN_FROZEN`.

The corrected GLPK compatibility workflow completed all 11 target points and returned 11 empty sequential reaction sets. This means **zero mappable gene rows were returned by this compatibility run**. It must **not** be described as proof that OptEnvelope has a "true zero candidate" result in theory or under all solver formulations.

The 237→235 correction does not require rerunning the 11 OptEnvelope target points: `r_0942` and `r_0436` were independently confirmed essential for all 11 target floors, so moving them from deletable to protected status does not alter the feasible deletion design.

## v2A

Historical ethanol-stage sensitivity only:

- `r_1714` glucose uptake LB = 0
- `r_1761` ethanol uptake LB = -0.447596
- WT max growth ≈ 0.0104164340 h^-1
- eligible genes = 225
- all eligible candidates have `Pmin = 0` at 10/50/90% WT absolute growth floors
- `GCP > 1e-7`: 0/225
- `Pmin95 > 1e-7`: 0/225

Status: `NON_DISCRIMINATING_GUARANTEED_PRODUCTION`. v2A is retained as a production-stage sensitivity condition, not as the sole primary benchmark condition.

## v2B

YPD-informed B-vitamin availability sensitivity only. Panel: B1/B2/B3/B5/B6/B7/B9, common uptake cap sweep `1e-6, 1e-5, 1e-4, 1e-3 mmol/(gDCW*h)`.

Validated eligible-gene counts: 238, 256, 262, 262 respectively. v2B is `DIAGNOSTIC_ONLY_NOT_PRIMARY_BENCHMARK`; no cap may be selected post hoc and renamed as the real YPD uptake condition.

## FABRIC-AI Production Optimizer

Current executable benchmark method: v1.2.

- Design mode: one gene KO per strain, `top_k = 6`.
- Primary condition: corrected v1 glucose reference.
- v2A: reported sensitivity, not a hidden hard filter.
- v2B: diagnostic only.
- Historical six-target identity and Round-1 outcomes are prohibited as Design-mode ranking features.
- Ranking uses deterministic lexicographic order with a hard non-discrimination gate.

Current corrected-v1 + v2A run triggers `NON_DISCRIMINATING_GUARANTEED_PRODUCTION`; any emitted Top-6 rows are `SECONDARY_FEASIBILITY_ORDER_ONLY` and cannot support a production-superiority claim.

## Next execution order

1. FastKnock corrected-235 replay and freeze.
2. Keep CFSA 14-candidate evaluation; update final manifest with the 235-pool erratum.
3. Keep OptEnvelope corrected compatibility-run statement above.
4. Re-run FABRIC-AI Production Optimizer v1.2 once from a clean environment and freeze the Design-mode outputs.
5. Only after all four methods are frozen, generate the shared comparison table and decide whether C.3.2 is supported by a fair quantitative advantage or by the method's significant innovation.

See `RUNBOOK.md` for the exact execution sequence.