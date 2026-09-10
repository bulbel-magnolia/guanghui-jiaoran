# C.3.1：实验驱动的定量决策状态更新

<a id="已完成的恢复与实现"></a>
## 实现与数据来源

本轮恢复了 v0.8 原始反馈引擎、固定规则、六靶点实验前选择记录、Round 1 记录和实验后输出。原引擎与规则按原字节保存，重放得到的完整反馈表与原保存表一致。新增 `learn_mode.py` 将这个既有算法的输入、反馈前状态、反馈后状态和定量变化分别导出，生成可复现的状态版本 ID。

来源检索覆盖 Git 历史中的 **77 次提交**及 v0.8 压缩包。反馈代码和实验前后表来自 v0.8 压缩包。`before.json` 由当前程序读取实验前选择表生成，未评定等级记为 `null`；它是反馈前的数据状态，不是恢复出的历史可执行模型。

## 官方四环节与证据

依据官方 Judging Form 第 7 页 C.3.1 及其关键佐证，按对象、数值、改动和前后指标填写：

| 环节 | 具体对象与数值 | 可核查证据 |
|---|---|---|
| ① 模型给出什么 | 历史 Yeast9/FBA/OptKnock 记录 307 个候选反应、14 个方案，经团队审核确定 6 个实验靶点。Plan `obj` 保留原转录值；其定义未恢复，不作为产量预测值或排名。 | [模型原图与记录](recovered_v08/docs/evidence/gsmm-model-evidence.md)、[实验前选择表](recovered_v08/data/processed/gsmm_evidence_v0_2/selected_targets_pre_validation.csv) |
| ② 验证什么 | 6 项保留本轮状态，其中 2 项有定量发酵，4 项为本轮构建/培养可实施性未通过。PAN5 120 h 约 0.67 mg/L，对照 AST 约 0.47 mg/L；MDE1 96–120 h 约 0.42→0.36 mg/L。按既有项目规则，定量的两项中 1 项满足正向终点、持续性和生物量保持条件。 | [测量表](recovered_v08/data/processed/gsmm_evidence_v0_2/wetlab_validation.csv)、[本轮状态](recovered_v08/data/processed/gsmm_evidence_v0_2/round1_outcomes.csv) |
| ③ 改了什么 | 将原本只有“进入 Round 1”选择状态的六行记录，补入实验指标，经未改动的 v0.8 规则更新证据等级与下一轮实验安排。更新对象是实验后的决策状态表；规则阈值、共同代谢模型和设计阶段排序保持不变。 | [原反馈引擎](recovered_v08/src/ai/fabric_ai/metabolic.py)、[规则](recovered_v08/data/processed/gsmm_evidence_v0_2/feedback_rules.json)、[状态转移实现](../../../src/ai/fabric_ai_optimizer/learn_mode.py) |
| ④ 前后指标 | 已评定靶点 **0/6→6/6**；未评定 **6→0**；可用的下一轮安排类别 **1→3**。同一 6 靶点更新为 1 项优先推进、1 项复核机制、4 项调整构建/培养。 | [before](../../fabric_ai/20260909/learn_mode_iteration/before.json)、[after](../../fabric_ai/20260909/learn_mode_iteration/after.json)、[逐项对照](../../fabric_ai/20260909/learn_mode_iteration/comparison.csv)、[定量变化](../../fabric_ai/20260909/learn_mode_iteration/quantitative_delta.csv) |

<a id="不调权重的实际规则"></a>
## 沿用的反馈规则

阈值沿用 v0.8：终点相对 AST ≥1.05、96–120 h 变化 ≥0%、生物量相对 AST ≥0.9，三项同时满足进入 Tier 1；终点 ≤0.95 或持续性下降进入 Tier 2，其他混合结果也为 Tier 2；本轮可实施性未通过为 Tier 3。规则按阈值分类，不采用线性加权。

| 靶点 | 终点相对 AST | 96–120 h 变化 | 生物量相对 AST | 更新后 |
|---|---:|---:|---:|---|
| PAN5 | 约 1.426 | 约 +9.84% | 约 1.120 | Tier 1；优先推进 |
| MDE1 | 约 0.766 | 约 −14.29% | 约 1.103 | Tier 2；复核机制 |
| RIB2、MRI1、SPE2、FUM1 | 未定量 | 未定量 | 未定量 | Tier 3；调整构建/培养 |

表中比值由近似图读值计算，精度取决于原图读数，不用于统计显著性判断。其余四项记录反映本轮构建或培养结果，不判定基因致死；Tier 表示证据类别，不表示基因名次。

## 数据隔离与版本

实验数据来自 BIT-China 团队 2025 年项目记录，反馈代码与规则来自 v0.8 包。规则已依据这些实验结果制定，本次工作属于历史数据的规则重放。状态导出程序于 2026-09-09 实现并运行；其结果用于评价反馈后的决策变化，不作为独立前瞻预测验证。

历史 6 个靶点与设计阶段的 235 个候选及新版 Top-6 分别保存。实验反馈程序在运行前后核对模型、两组表型指标、排序和 Top-6 的 SHA-256，保持设计阶段基准结果不变。

[来源文件 SHA-256](recovered_v08/SOURCE_MANIFEST.json) · [历史搜索范围](history_recovery.json) · [配置及哈希](../../../configs/fabric_ai/learn_mode_v08_replay.json)

## 可复现入口

在仓库根目录，用一个新的空输出目录执行：

```bash
python src/ai/fabric_ai_optimizer/learn_mode.py --config configs/fabric_ai/learn_mode_v08_replay.json --outdir .reproduction/learn-check
python -m pytest tests/fabric_ai/test_learn_mode.py -q
```

[本次运行日志](../../fabric_ai/20260909/learn_mode_iteration/run.log) · [状态更新校验](../../fabric_ai/20260909/learn_mode_iteration/verification.json) · [全修复验证](validation/verification.json)

## C.3.1 使用范围

本项研究报告计算辅助选靶、已有实验验证和规则型实验反馈更新。0/6→6/6 表示完成证据评定的靶点数量变化，不衡量模型准确率、泛化性能或新增实验的产量提升。共同代谢模型和反馈规则阈值保持不变，评价对象为实验后的决策状态。C.3.1 的认定由评委按官方条款完成。
