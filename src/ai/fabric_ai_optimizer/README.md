# FABRIC-AI v1.2 冻结代码复现

本目录同步 2026-09-08 fresh Design-mode 与 ranking numerical-equivalence correction 两个最终包。共同模型、235-gene primary pool、v1/v2A 条件和 ranking 文件均保留来源字节。最终入口为 [最终结果](../../../results/fabric_ai/20260908/README.md)；[旧排序](../../../results/history/fabric_ai/20260908/pre_numeric_correction/design_mode_ranking.csv)仅用于历史审计。

## 环境

验证环境为 Python 3.12.10、COBRApy 0.30.0、SciPy 1.17.1、swiglpk 5.0.13、pandas 2.3.3、pytest 8.3.5。依赖见 [requirements-frozen.txt](requirements-frozen.txt)。在仓库根目录的 Python 3.12.10 环境中运行：

```bash
python -m pip install -r src/ai/fabric_ai_optimizer/requirements-frozen.txt
```

prepare 的 FVA 使用 GLPK；基因生长检查和 evaluate 使用 SciPy HiGHS。solver tolerance 均为 `1e-7`。参数来自 [冻结合同](fabric_ai_optimizer_contract_v1.2.json)，growth floors 为 `0.1,0.5,0.9`，mutant growth fraction 为 `0.95`，`top_k=6`。

## 最短复现流程

以下命令从仓库根目录运行，输出到 `.reproduction/`。evaluate 始终读取冻结的 235-gene primary pool；prepare 的重算文件作为独立验证产物保存。

```bash
python src/ai/fabric_ai_optimizer/fabric_ai_benchmark.py prepare --model models/fabric_ai/common_model.json --condition configs/fabric_ai/v1_glucose_reference.json --outdir .reproduction/prepare --tol 1e-7
python src/ai/fabric_ai_optimizer/fabric_ai_benchmark.py evaluate --model models/fabric_ai/common_model.json --condition configs/fabric_ai/v1_glucose_reference.json --pool results/fabric_ai/20260908/candidate_space.json --outdir .reproduction/v1 --floors 0.1,0.5,0.9 --mutant-growth-fraction 0.95 --tol 1e-7
python src/ai/fabric_ai_optimizer/fabric_ai_benchmark.py evaluate --model models/fabric_ai/common_model.json --condition configs/fabric_ai/v2a_historical_ethanol_stage.json --pool results/fabric_ai/20260908/candidate_space.json --outdir .reproduction/v2a --floors 0.1,0.5,0.9 --mutant-growth-fraction 0.95 --tol 1e-7
python src/ai/fabric_ai_optimizer/fabric_ai_benchmark.py rank --metrics v1_glucose_reference=results/fabric_ai/20260908/v1_candidate_metrics.csv v2a_historical_ethanol_stage=results/fabric_ai/20260908/v2a_candidate_metrics.csv --summaries v1_glucose_reference=results/fabric_ai/20260908/v1_summary.json v2a_historical_ethanol_stage=results/fabric_ai/20260908/v2a_summary.json --primary v1_glucose_reference --outdir .reproduction/rank --top-k 6 --tol 1e-7
python -m pytest tests/fabric_ai/test_ranker.py -q
python tools/fabric_ai/verify_repo_freeze.py --outdir .reproduction/verification
```

独立重算的两组 metrics 通过检查后，可在 rank 命令中将对应 metrics 和 summaries 路径替换为 `.reproduction/v1/`、`.reproduction/v2a/` 中的文件。上面的冻结 metrics rank 命令用于逐字节核对最终排名。

自动 smoke 入口（实际执行 prepare、两组完整 evaluate 和 rank，并核对冻结文件未改变）：

```bash
python tools/fabric_ai/reproduction_smoke.py --outdir .reproduction/smoke
```

原包测试和两个 verifier 脚本未改动。`tests/optimizer/fabric_ai_benchmark.py` 仅将原测试的导入路径连接到本目录代码；`verify_repo_freeze.py` 在输出目录复制当前仓库文件形成原包路径布局，执行原 verifier，并用本次 9 项测试日志完成最终 15/15 检查。其 fresh verifier 输出对应历史排序，correction verifier 输出对应最终排序。请通过此入口运行 verifier。

冻结条件中的 `../config/protected_reaction_ids.json` 保留原文，由 [兼容路径副本](../../../configs/config/protected_reaction_ids.json)解析；它与 [规范位置](../../../configs/fabric_ai/protected_reaction_ids.json)逐字节一致。`.gitattributes` 保持冻结文件的行尾字节。

## SHA-256

| 文件 | SHA-256 |
|---|---|
| [common_model.json](../../../models/fabric_ai/common_model.json) | `c7767f92ae22dfd1591ca138e99dc305f477728cffb9eee4eef71d3c162ed684` |
| [v1 metrics](../../../results/fabric_ai/20260908/v1_candidate_metrics.csv) | `2176df82d1f75ee7c38990836c3e185c658b2c615635664e800c68063332300d` |
| [v2A metrics](../../../results/fabric_ai/20260908/v2a_candidate_metrics.csv) | `e270f2636e8fb0e52702f43e35fc6a7e8aea5acdffa344fb7b09c45d0839e150` |
| ranking correction ZIP | `7cea8b7f7c501a7b5130cd069c952686d045c1406cdff06321f0cca8a02b15d7` |
| fresh Design-mode ZIP | `ab6e65cce6d2358f75a687cae065ac72de57b5dc16329cf4a764a4c5dbb2764e` |

完整来源映射见 [同步清单](../../../results/evidence/20260908/code_parts_sync/source_sync_manifest.csv)。
