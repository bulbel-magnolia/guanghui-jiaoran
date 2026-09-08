# FABRIC-AI v1.2 ranking numeric-equivalence correction

Reviewed correction ZIP SHA-256: `7cea8b7f7c501a7b5130cd069c952686d045c1406cdff06321f0cca8a02b15d7`.

## Freeze result

- Status remains `NON_DISCRIMINATING_GUARANTEED_PRODUCTION`.
- No `prepare` or `evaluate` rerun was performed.
- Frozen v1/v2A metric hashes are unchanged.
- Ranking numerical equivalence is now judged in native solver units at tolerance `1e-7` before using derived GR/PCR ratios.
- 9 ranking tests passed.
- Independent verification passed 15/15 checks.
- No KO native objective exceeded the corresponding WT value by more than tolerance.
- 189/235 candidate ranks changed relative to the historical ratio-space handling.

## Frozen secondary Top-6

1. `YAL060W`
2. `YBR006W`
3. `YBR011C`
4. `YBR183W`
5. `YBR281C`
6. `YCR005C`

All six rows are `SECONDARY_FEASIBILITY_ORDER_ONLY`. They are not production-optimal predictions and cannot support a production-superiority claim.

## Frozen source hashes

- v1 candidate metrics: `2176df82d1f75ee7c38990836c3e185c658b2c615635664e800c68063332300d`
- v2A candidate metrics: `e270f2636e8fb0e52702f43e35fc6a7e8aea5acdffa344fb7b09c45d0839e150`

The earlier ratio-space ranking is retained only as historical audit material.
