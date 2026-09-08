# FABRIC-AI Production Optimizer v1.2 — independent closeout audit

Reviewed deliverable ZIP SHA-256: `ab6e65cce6d2358f75a687cae065ac72de57b5dc16329cf4a764a4c5dbb2764e`.

## Supported freeze conclusions

The package is internally complete and its main Design-mode conclusion is supported:

- fresh primary prepare reproduced exactly **235 genes** and **600 blocked reactions**;
- v1 and v2A both evaluated the full primary 235-gene pool;
- zero GPR-footprint mismatches;
- zero solver failures;
- v2A retained `YMR303C` as an infeasible sensitivity phenotype and recorded 32 `growth_floor_infeasible` cells rather than dropping them;
- all feasible evaluation residuals are within the frozen `1e-7` tolerance;
- primary-condition `GCP=0` and `Pmin95=0` for all 235 candidates;
- therefore `NON_DISCRIMINATING_GUARANTEED_PRODUCTION` is a supported status;
- no production-superiority claim is permitted from this run.

The package manifest hashes were independently rechecked: 35/35 manifest members matched size and SHA-256. The internal final verification reported all 18 listed checks as passed. The ranker test suite reported 5 passed (one pytest-cache warning only).

## Narrow issue: the specific secondary Top-6 order is not numerically frozen yet

The non-discrimination gate itself is unaffected. The issue is only the downstream `SECONDARY_FEASIBILITY_ORDER_ONLY` ordering.

The v1.2 specification states that `PCR <= 1` mathematically for a KO, and that solver-equivalent numerical noise should not break ties. The current ranker applies `abs(PCR-1) <= 1e-7` directly to the **dimensionless ratio**.

For the current run:

- WT `Pmax` at the 10% WT-growth floor: `0.06725532100612219` mmol/(gDCW·h)
- `YOR311C` mutant `Pmax`: `0.067255347296789` mmol/(gDCW·h)
- absolute objective difference: about `2.629e-08`, which is **below the frozen LP tolerance of `1e-7`**
- reported PCR: `1.000000390908355`

Because normalization divides by ~0.0673, a sub-tolerance absolute flux difference becomes a ratio difference of ~`3.91e-7`, which exceeds the ranker's fixed ratio-space `1e-7` equivalence threshold. The current Top-6 is consequently ordered partly by objective differences that are smaller than the solver tolerance in native flux units. Similar behavior is present in the other leading rows.

This does **not** invalidate:

- 235-gene admission;
- v1/v2A phenotype tables;
- the `NON_DISCRIMINATING_GUARANTEED_PRODUCTION` gate;
- the statement that the emitted Top-6 cannot support production superiority.

It does mean the exact secondary Top-6 identities/order should not be used for retrospective hit-rate analysis, experiment-priority claims, or final Wiki figures until the narrow ranking-only numerical-equivalence correction is applied.

## Required correction boundary

No model, condition, candidate pool, phenotype solve, ranking priority, `top_k`, or biological threshold should change. Reuse the frozen v1/v2A `candidate_metrics.csv` files and rerun only ranking/tests/verification after correcting numerical equivalence for derived ratios in native units.

Recommended semantics:

1. For GR, treat mutant and WT maximum growth as equivalent when `abs(mutant_mu_max - WT_mu_max) <= 1e-7`; then set the ranking GR value to 1.0.
2. For primary PCR, treat mutant and WT `Pmax_0.1` as equivalent when `abs(Pmax_mutant - Pmax_WT) <= 1e-7`; then set the ranking PCR value to 1.0.
3. If a KO exceeds WT by more than the native-unit tolerance, flag a numerical/model inconsistency rather than interpreting `PCR > 1` as a biological advantage.
4. Add tests proving that a sub-`1e-7` native-flux difference cannot break a derived-ratio tie.
5. Preserve the non-discrimination gate and `SECONDARY_FEASIBILITY_ORDER_ONLY` label.

Until this correction closes, the package's primary non-discrimination result is considered frozen, while the specific secondary Top-6 list is provisional.
