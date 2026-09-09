# Learn mode 定量状态转移

该目录记录 v0.8 原反馈规则的实际重放，以及本轮新增的显式 before/after 状态导出。

| 文件 | 内容 |
|---|---|
| [before.json](before.json) | 仅来自实验前选择表；未评定 tier=null |
| [experimental_feedback.json](experimental_feedback.json) | 原有近似读数及本轮可实施性记录，附来源哈希 |
| [after.json](after.json) | 原 v0.8 引擎计算后的 evidence state 与下一轮动作 |
| [comparison.csv](comparison.csv) | 同一六靶点的逐项前后对照 |
| [quantitative_delta.csv](quantitative_delta.csv) | 已评定 0→6，未评定 6→0，动作类别 1→3 |
| [recomputed_feedback.csv](recomputed_feedback.csv) | 与原保存反馈表逐列核对后的重算输出 |
| [run.log](run.log) | 本次真实执行日志 |
| [verification.json](verification.json) | 来源、状态、冻结输入输出检查 |

[官方四环节与研究范围](../../../evidence/20260909/C3_1_QUANTITATIVE_ITERATION.md)。记录更新量不表示预测准确率提升；历史六靶点不替代新版 235-gene Design Top-6。
