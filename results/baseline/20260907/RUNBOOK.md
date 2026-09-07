# FABRIC-AI benchmark execution runbook — 2026-09-07

状态：`FASTKNOCK_235_CLOSEOUT_THEN_FABRIC_AI_FINAL_DESIGN_RUN`

本 runbook 不修改共同模型、培养条件、Wiki 或评审表。OptEnvelope v1 corrected compatibility run 已单独冻结；CFSA 的 14 个合法 KO 不受 237→235 erratum 影响。

## A. FastKnock corrected 235-pool 收口

### A1. 输入

使用 2026-09-06 baseline checkpoint 的同一个 `model/common_model.json` 和 FastKnock adapted source。候选池替换为 corrected 235-gene pool。

**禁止重新运行旧版 `prepare_candidates.py` 作为正式候选生成入口**，因为旧候选生成存在 solver-state reuse erratum。corrected 235 pool 已由 fresh/presolved KO growth audit 独立确认，且等于旧 237 pool 删除 `YER014W` 与 `YOR176W`。

### A2. 执行

在原 baseline checkpoint 根目录中：

```bash
cp config/common_candidate_space.json config/common_candidate_space_237_HISTORICAL.json
cp /path/to/common_candidate_space_235.json config/common_candidate_space.json
python scripts/run_fastknock.py | tee logs/fastknock_235_replay.log
python scripts/audit_fastknock_fluxes.py | tee logs/fastknock_235_flux_validation.log
```

若 `gene_candidates.csv` 非空，再执行统一 independent evaluator；若为空，候选质量指标记 `N/A`，不要填 0。

### A3. 强制检查

正式 closeout 至少检查：

- `run_status.json.status == COMPLETED`；
- `common_gene_pool_size == 235`；
- model SHA-256 与冻结 v1 一致；
- `round1_used == false`；
- 不读取历史六靶点或 Round1 结果；
- 所有 visited fluxes 状态/残差通过既有审计；
- 保存实际的 `distinct_effective_actions`, `root_active_actions`, `visited_actions`, `fba_calls`, `gene_candidates`, wall time；
- 不预设输出必须为 0。

FastKnock closeout 完成后生成新的 frozen manifest，旧 237-pool 结果只作为历史审计记录。

## B. v2B：只做诊断归档，不进入公开 baseline 胜负

v2B 已冻结为 `DIAGNOSTIC_ONLY_NOT_PRIMARY_BENCHMARK`。当前不需要挑一个 cap 继续跑 FastKnock/CFSA/OptEnvelope。

若从干净环境复现 v2B candidate admission，分别运行：

```bash
python optimizer/fabric_ai_benchmark.py prepare \
  --model model/common_model.json \
  --condition conditions/v2b_bvitamin_panel_1e-6.json \
  --outdir results/v2b_1e-6

python optimizer/fabric_ai_benchmark.py prepare \
  --model model/common_model.json \
  --condition conditions/v2b_bvitamin_panel_1e-5.json \
  --outdir results/v2b_1e-5

python optimizer/fabric_ai_benchmark.py prepare \
  --model model/common_model.json \
  --condition conditions/v2b_bvitamin_panel_1e-4.json \
  --outdir results/v2b_1e-4

python optimizer/fabric_ai_benchmark.py prepare \
  --model model/common_model.json \
  --condition conditions/v2b_bvitamin_panel_1e-3.json \
  --outdir results/v2b_1e-3
```

复核对象是候选数量、blocked/unblocked reactions 和历史六靶点的 post-definition diagnostic；**不得按结果挑选某个 cap 改称真实 YPD 条件**。

## C. FABRIC-AI Production Optimizer v1.2 正式 Design-mode 冻结运行

### C1. primary pool

从干净环境重新生成 corrected v1 primary candidate pool：

```bash
python optimizer/fabric_ai_benchmark.py prepare \
  --model model/common_model.json \
  --condition conditions/v1_glucose_reference.json \
  --outdir results/fabric_ai_primary_prepare \
  --tol 1e-7
```

检查 `eligible_count == 235`。

### C2. primary 独立评价

```bash
python optimizer/fabric_ai_benchmark.py evaluate \
  --model model/common_model.json \
  --condition conditions/v1_glucose_reference.json \
  --pool results/fabric_ai_primary_prepare/candidate_space.json \
  --outdir results/fabric_ai_v1_metrics \
  --floors 0.1,0.5,0.9 \
  --mutant-growth-fraction 0.95 \
  --tol 1e-7
```

### C3. v2A sensitivity 必须评价全部 235 primary genes

不要使用 v2A 自己的 225-gene eligible pool 做静默交集。仍把 primary 235 pool 作为 `--pool`：

```bash
python optimizer/fabric_ai_benchmark.py evaluate \
  --model model/common_model.json \
  --condition conditions/v2a_historical_ethanol_stage.json \
  --pool results/fabric_ai_primary_prepare/candidate_space.json \
  --outdir results/fabric_ai_v2a_metrics \
  --floors 0.1,0.5,0.9 \
  --mutant-growth-fraction 0.95 \
  --tol 1e-7
```

### C4. 固定排序

```bash
python optimizer/fabric_ai_benchmark.py rank \
  --metrics \
    v1_glucose_reference=results/fabric_ai_v1_metrics/candidate_metrics.csv \
    v2a_historical_ethanol_stage=results/fabric_ai_v2a_metrics/candidate_metrics.csv \
  --primary v1_glucose_reference \
  --outdir results/fabric_ai_design_mode_final \
  --top-k 6 \
  --tol 1e-7
```

当前已知诊断提示 primary `GCP` 与 `Pmin95` 均为 0；fresh run 若再次触发门禁，则状态必须保留为：

`NON_DISCRIMINATING_GUARANTEED_PRODUCTION`

且 Top-6 只能标为：

`SECONDARY_FEASIBILITY_ORDER_ONLY`

不得用该 secondary ordering 支持“生产性能优于 baseline”。

### C5. 测试与冻结

```bash
python -m pytest tests/test_ranker.py -q
```

最终冻结包至少包括：

- method spec v1.2；
- contract v1.2；
- common model SHA；
- primary 235 candidate space；
- v1/v2A candidate metrics；
- ranking/top-k/summary；
- test log；
- solver/运行时间；
- manifest。

## D. 执行顺序

1. **先 FastKnock 235 replay**，因为它是最后一个尚未按 corrected pool 收口的公开 baseline。
2. 立即冻结 FastKnock v1 corrected result；CFSA 保留；OptEnvelope 使用 corrected compatibility-run frozen statement。
3. v2B 只做现有诊断归档，不追加公开 baseline 运行。
4. 做一次 FABRIC-AI v1.2 fresh Design-mode run 并冻结。
5. 之后再生成四方法共同 summary；在所有公开基线和本队结果冻结之前，不修改 Wiki/评审表中的胜负表述。