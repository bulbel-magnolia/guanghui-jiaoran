# 数据说明

本项目的计算数据与实验资料按分析任务保存，主要位置如下。

| 数据 | 位置 | 内容 |
|---|---|---|
| 共同代谢模型 | [common_model.json](../models/fabric_ai/common_model.json) | Yeast-GEM 与项目异源产色通路 |
| 候选与表型 | [计算结果](../results/fabric_ai/20260908/README.md) | 235 个候选及 v1、v2A 表型 |
| 实验反馈 | [前后对照](../results/fabric_ai/20260909/learn_mode_iteration/README.md) | 六个历史实验靶点的数据与评价变化 |
| 实验资料来源 | [来源清单](../results/evidence/20260909/recovered_v08/SOURCE_MANIFEST.json) | v0.8 保存的原始代码、规则与记录 |
| 元件表征 | [PhiReX](../parts/AISB26-045-001/characterization.md) · [BmCBP](../parts/AISB26-045-002/characterization.md) | 测量条件、结果和样品信息 |

`raw/` 和 `processed/` 是预留目录。当前可供复核的数据以以上索引为准。

## 数据使用范围

历史 Round 1 实验数据用于实验反馈评价，不参与设计阶段的候选生成和排序。图读值、条件均值与逐次原始测量值在相应记录中分别标注。

数据使用遵循来源许可；个人身份信息和受限数据不进入公开仓库。文件一致性检查见 [可验证性](../wiki/Verifiability.md)。
