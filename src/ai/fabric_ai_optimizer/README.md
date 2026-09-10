<a id="fabric-ai-v12-冻结代码复现"></a>
# FABRIC-AI v1.2 使用与复现

本目录提供 2026-09-08 设计阶段计算及排序数值等价修正后的代码。共同模型、235 个主分析候选、v1/v2A 条件和排序文件保持原始字节。结果见 [当前结果](../../../results/fabric_ai/20260908/README.md)；[旧排序](../../../results/history/fabric_ai/20260908/pre_numeric_correction/design_mode_ranking.csv)用于追溯修订过程。

## 环境

验证环境为 Python 3.12.10、COBRApy 0.30.0、SciPy 1.17.1、swiglpk 5.0.13、pandas 2.3.3、pytest 8.3.5。依赖见 [requirements-frozen.txt](requirements-frozen.txt)。在仓库根目录的 Python 3.12.10 环境中运行：

```bash
python -m pip install -r src/ai/fabric_ai_optimizer/requirements-frozen.txt
```

`prepare` 中的通量变动分析（FVA）使用 GLPK；基因生长检查和 `evaluate` 使用 SciPy HiGHS。求解容差均为 `1e-7`。参数见 [参数配置](fabric_ai_optimizer_contract_v1.2.json)：生长下限比例为 `0.1,0.5,0.9`，近最优生长比例为 `0.95`，推荐数量为 `top_k=6`。

## 最短复现流程

以下命令从仓库根目录运行，输出到 `.reproduction/`。`evaluate` 读取固定的同一组 235 个主分析候选；`prepare` 的重新计算文件另行保存，用于核对候选集合。

```bash
python src/ai/fabric_ai_optimizer/fabric_ai_benchmark.py prepare --model models/fabric_ai/common_model.json --condition configs/fabric_ai/v1_glucose_reference.json --outdir .reproduction/prepare --tol 1e-7
python src/ai/fabric_ai_optimizer/fabric_ai_benchmark.py evaluate --model models/fabric_ai/common_model.json --condition configs/fabric_ai/v1_glucose_reference.json --pool results/fabric_ai/20260908/candidate_space.json --outdir .reproduction/v1 --floors 0.1,0.5,0.9 --mutant-growth-fraction 0.95 --tol 1e-7
python src/ai/fabric_ai_optimizer/fabric_ai_benchmark.py evaluate --model models/fabric_ai/common_model.json --condition configs/fabric_ai/v2a_historical_ethanol_stage.json --pool results/fabric_ai/20260908/candidate_space.json --outdir .reproduction/v2a --floors 0.1,0.5,0.9 --mutant-growth-fraction 0.95 --tol 1e-7
python src/ai/fabric_ai_optimizer/fabric_ai_benchmark.py rank --metrics v1_glucose_reference=results/fabric_ai/20260908/v1_candidate_metrics.csv v2a_historical_ethanol_stage=results/fabric_ai/20260908/v2a_candidate_metrics.csv --summaries v1_glucose_reference=results/fabric_ai/20260908/v1_summary.json v2a_historical_ethanol_stage=results/fabric_ai/20260908/v2a_summary.json --primary v1_glucose_reference --outdir .reproduction/rank --top-k 6 --tol 1e-7
python -m pytest tests/fabric_ai/test_ranker.py -q
python tools/fabric_ai/verify_repo_freeze.py --outdir .reproduction/verification
```

独立重算的两组表型结果通过检查后，可在 `rank` 命令中将指标表和汇总文件路径替换为 `.reproduction/v1/`、`.reproduction/v2a/` 中的文件。上面的排序命令使用保存的指标表，核对最终排序。

分模块复现命令（执行候选准备、两组完整表型评价和排序，并核对固定文件）：

```bash
python tools/fabric_ai/reproduction_smoke.py --outdir .reproduction/smoke
```

原有测试和两个核验脚本保留原版本。`tests/optimizer/fabric_ai_benchmark.py` 连接原排序核心；`verify_repo_freeze.py` 在输出目录准备核验所需文件，运行原核验脚本及 9 项排序测试，完成 15/15 项检查。两个核验脚本分别检查历史排序和最终排序；请使用上述统一入口运行。

固定条件文件中的 `../config/protected_reaction_ids.json` 保留原文，由 [兼容路径副本](../../../configs/config/protected_reaction_ids.json)解析；它与 [规范位置](../../../configs/fabric_ai/protected_reaction_ids.json)逐字节一致。`.gitattributes` 保持不变文件的行尾字节。

## SHA-256

| 文件 | SHA-256 |
|---|---|
| [common_model.json](../../../models/fabric_ai/common_model.json) | `c7767f92ae22dfd1591ca138e99dc305f477728cffb9eee4eef71d3c162ed684` |
| [v1 表型指标](../../../results/fabric_ai/20260908/v1_candidate_metrics.csv) | `2176df82d1f75ee7c38990836c3e185c658b2c615635664e800c68063332300d` |
| [v2A 表型指标](../../../results/fabric_ai/20260908/v2a_candidate_metrics.csv) | `e270f2636e8fb0e52702f43e35fc6a7e8aea5acdffa344fb7b09c45d0839e150` |
| 排序数值修正包 | `7cea8b7f7c501a7b5130cd069c952686d045c1406cdff06321f0cca8a02b15d7` |
| 设计阶段重新计算包 | `ab6e65cce6d2358f75a687cae065ac72de57b5dc16329cf4a764a4c5dbb2764e` |

完整来源映射见 [同步清单](../../../results/evidence/20260908/code_parts_sync/source_sync_manifest.csv)。
