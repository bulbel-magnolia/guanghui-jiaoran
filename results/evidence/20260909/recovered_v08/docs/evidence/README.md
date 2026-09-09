# 公开证据索引

本目录把结构化记录连接到可公开复核的事实摘录和证据图。CSV 的 `source_file_internal` 字段使用仓库相对路径；一致性检查验证每个路径都能在公开包内解析。

| 证据 | 公开文件 | 支持内容 |
|---|---|---|
| GSMM 实验记录摘录 | `records/gsmm-experiment-record-excerpt.md` | Round 0 发酵、两项模型输入、六个靶点与 Round 1 结果 |
| Round 0 完整转录 | `records/round0-fermentation-complete-transcript.csv` | OD600、葡萄糖和乙醇的 46 条逐点记录 |
| 模型记录摘录 | `gsmm-model-evidence.md` | 307 个候选计数、Plan1–Plan14、六靶点映射与验证图 |
| BmCBP 实验记录摘要 | `records/bmcbp-experiment-record-summary.md` | 结合趋势、浓度范围和基材反馈 |
| BmCBP 定性判据 | `records/bmcbp-qualitative-evidence-rubric.md` | 丝绸强证据、棉/聚酯弱证据及判定范围 |
| 证据图 | `figures/` | 模型方案与 Round 1 结果的图像证据 |

## 模型复现边界

公开证据能够追溯：

`Round 0 → Yeast9 约束记录 → 307 个候选计数 → 14 个方案编号 → 6 个实验靶点 → Round 1 → 反馈等级`

当前材料未包含 Yeast9 衍生模型文件、异源反应定义、完整培养基边界、目标函数或求解器配置。仓库代码用于验证和汇总证据链，不生成新的 FBA 或 OptKnock 结果。该边界集中记录于 `wiki/Verifiability.md` 与 `results/gsmm/model_evidence_manifest.json`。

## 原件与披露

公开摘录只保留当前项目需要的事实、数据状态和证据定位。原始 PDF、原始转录、来源名称、文件哈希及路径映射完整保存在内部审计档案，不随公开包发布。正式归属披露以赛事规则和最终提交材料为准。