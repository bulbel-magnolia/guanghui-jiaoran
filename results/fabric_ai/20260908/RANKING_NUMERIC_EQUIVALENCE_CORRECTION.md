# Codex task — FABRIC-AI v1.2 ranking-only numerical equivalence correction

Scope: **ranking/tests/verification only**. Do not rerun `prepare` or `evaluate`; do not modify the common model, conditions, 235-gene pool, GPR footprints, growth floors, `top_k`, ranking priority, v2B, Wiki or judging form.

## Why this correction is required

The frozen solver tolerance is `1e-7` in native flux units. The current ranker applies the same `1e-7` directly to dimensionless ratios. This can amplify sub-tolerance flux differences after division and use them to break ties.

Concrete current-run example:

- WT `Pmax_0.1 = 0.06725532100612219`
- `YOR311C Pmax_0.1 = 0.067255347296789`
- `delta = 2.629e-08 < 1e-7`
- current `PCR_0.1 = 1.000000390908355`

The native objectives are solver-equivalent, yet the derived ratio is outside the current ratio-space equivalence threshold and affects secondary ordering.

## Required implementation

Use the already-frozen v1 and v2A `candidate_metrics.csv` files and their `summary.json` WT reference values.

For ranking-only equivalent metrics:

- Growth: if `abs(mutant_mu_max - WT_mu_max) <= tol`, use `GR_equiv = 1.0`; otherwise use the recorded GR. If `mutant_mu_max > WT_mu_max + tol`, flag an inconsistency.
- Primary PCR at 10% WT floor: if `abs(Pmax_mutant - Pmax_WT) <= tol`, use `PCR_equiv = 1.0`; otherwise use the recorded PCR. If `Pmax_mutant > Pmax_WT + tol`, flag an inconsistency.
- Preserve existing absolute-zero handling for the current GCP/Pmin95 gate. The current gate must remain `NON_DISCRIMINATING_GUARANTEED_PRODUCTION` unless the source phenotype tables themselves differ, which they must not in this task.
- Preserve lexicographic priority exactly: Robust GCP → Median GCP → primary Pmin95 → Robust GR → primary PCR@0.1WT → footprint size → gene ID.

## Required tests

Add tests that:

1. `Pmax_mutant - Pmax_WT = 2.629e-08` at tol `1e-7` cannot break a PCR tie even though the raw ratio differs from 1 by >`1e-7`.
2. A growth difference smaller than `1e-7` in native growth units cannot break a GR tie after normalization.
3. A KO objective exceeding the WT objective by more than `1e-7` is rejected/flagged, not interpreted as a beneficial ratio >1.
4. The non-discrimination gate and `SECONDARY_FEASIBILITY_ORDER_ONLY` scope remain unchanged.
5. Condition gene sets are still required to match and `top_k=6` remains fixed.

## Output

Return a small correction closeout package containing:

- updated ranker code/spec/contract only where necessary;
- regenerated `design_mode_ranking.csv` and `design_mode_topk.csv` from the existing frozen metrics;
- updated rank summary;
- test log;
- verification report;
- manifest and ZIP SHA-256.

Do not assume or target any particular Top-6 identity. The corrected order must emerge from the frozen source metrics and corrected numerical-equivalence rule.
