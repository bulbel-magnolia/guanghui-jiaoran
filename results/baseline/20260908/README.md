# FABRIC-AI benchmark closeout — 2026-09-08

This directory records the corrected v1 FastKnock closeout after the 237→235 candidate-pool erratum.

## FastKnock 2024 corrected replay

Status: `FASTKNOCK_CORRECTED_235_REPLAY_FROZEN`

- Canonical common-model SHA-256: `c7767f92ae22dfd1591ca138e99dc305f477728cffb9eee4eef71d3c162ed684`
- Corrected primary pool: 235 genes (historical 237 pool minus `YER014W` and `YOR176W`)
- Upstream FastKnock commit: `f7017250aaae67613d1ce233f63c556419969ad5`
- `K=1`
- Distinct effective actions: 216
- Root-active actions: 51
- Visited actions: 51
- FBA calls: 52 including root
- Native gene candidates: **0**
- Candidate-quality metrics: **N/A**
- Wall time: 9.9119562 s
- 51/51 visited actions passed saved-flux audit
- Maximum recorded mass-balance residual: `9.712566000567879e-08`
- Maximum recorded bound residual: `9.712563414734624e-08`
- Requested/read-back solver tolerance: `1e-7`

The zero candidate count is an observed native-compatible output. It must not be converted into zero-valued candidate-quality metrics.

Deliverable ZIP SHA-256: `fec5efd208049211c0b0b3755f4ca84b3f4dffb951a05a50bcea08bb5e9ad164`.

The FABRIC-AI v1.2 Design-mode package was also reviewed on 2026-09-08. Its primary conclusion (`NON_DISCRIMINATING_GUARANTEED_PRODUCTION`) is supported, but the emitted secondary Top-6 order requires a narrow numerical-equivalence correction before that order is treated as frozen. See `../../fabric_ai/20260908/DESIGN_MODE_V1_2_AUDIT.md`.
