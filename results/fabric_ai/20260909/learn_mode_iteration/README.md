<a id="learn-mode-定量状态转移"></a>
# 实验反馈前后的定量对照

本目录保存按 v0.8 原反馈规则重新计算的结果，以及新增的实验反馈前后对照。

| 文件 | 内容 |
|---|---|
| [before.json](before.json) | 仅来自实验前选择表；未评定等级记录为 `tier=null` |
| [experimental_feedback.json](experimental_feedback.json) | 原有近似读数及本轮可实施性记录，附来源哈希 |
| [after.json](after.json) | 原 v0.8 引擎计算后的证据等级与下一轮安排 |
| [comparison.csv](comparison.csv) | 同一六靶点的逐项前后对照 |
| [quantitative_delta.csv](quantitative_delta.csv) | 已评定 0→6，未评定 6→0，动作类别 1→3 |
| [recomputed_feedback.csv](recomputed_feedback.csv) | 与原保存反馈表逐列核对后的重算输出 |
| [run.log](run.log) | 本次真实执行日志 |
| [verification.json](verification.json) | 来源、状态、固定输入输出检查 |

[官方四环节与研究范围](../../../evidence/20260909/C3_1_QUANTITATIVE_ITERATION.md)。该表比较历史六靶点的实验前后评价状态，与新版 235 个候选的设计排序分别保存；更新数量不表示预测准确率提升。
