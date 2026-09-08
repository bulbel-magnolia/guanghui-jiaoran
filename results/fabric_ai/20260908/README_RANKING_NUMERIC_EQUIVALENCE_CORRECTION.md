# FABRIC-AI v1.2 ranking numerical-equivalence correction closeout

Status: `RANKING_NUMERIC_EQUIVALENCE_CORRECTION_FROZEN`

This package is limited to ranking, tests and verification. It reuses the frozen v1 and v2A `candidate_metrics.csv` files and their WT summaries; `prepare` and `evaluate` were not rerun. The common model, 235-gene pool, v1/v2A condition membership, GPR footprints, growth floors, ranking priority, `top_k=6`, v2B, Wiki and judging form were not changed.

## Corrected numerical treatment

- Solver tolerance remains `1e-7` in native flux units.
- GR is set to the ranking-equivalent value 1 only when `abs(mutant_mu_max - WT_mu_max) <= 1e-7`.
- Primary PCR@0.1WT is set to the ranking-equivalent value 1 only when `abs(Pmax_mutant - Pmax_WT) <= 1e-7`.
- A knockout objective above its WT reference by more than `1e-7` is rejected as an inconsistency.
- Existing absolute-zero handling for GCP/Pmin95 and the fixed lexicographic priority are preserved.

## Actual regenerated result

The gate remains `NON_DISCRIMINATING_GUARANTEED_PRODUCTION`. The regenerated Top-6 is therefore only `SECONDARY_FEASIBILITY_ORDER_ONLY`:

1. `YAL060W`
2. `YBR006W`
3. `YBR011C`
4. `YBR183W`
5. `YBR281C`
6. `YCR005C`

These rows are not production-optimal candidates and do not support a production-superiority claim. Relative to the retained historical ratio-space ranking, 189 of 235 rank positions changed.

## Verification

- Frozen v1 metrics SHA-256: `2176df82d1f75ee7c38990836c3e185c658b2c615635664e800c68063332300d`
- Frozen v2A metrics SHA-256: `e270f2636e8fb0e52702f43e35fc6a7e8aea5acdffa344fb7b09c45d0839e150`
- Unit tests: `9 passed`
- Independent verification: `PASSED` (15/15 checks)
- Native-objective inconsistencies: `0`

See `ranking_numeric_correction_manifest.json` for the complete file inventory and hashes.
