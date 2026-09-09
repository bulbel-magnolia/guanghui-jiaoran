# GSMM evidence dataset v0.2

本目录保存 FABRIC-AI 生产优化闭环的结构化证据。证据链状态为 `evidence_chain_verified`；原始求解环境状态为 `solver_environment_not_in_release`。

- `round0_fermentation.csv`：初始发酵表格；
- `model_inputs.csv`：写入模型记录的两项实测速率；
- `candidate_reactions.csv`：保存可核实的 307 个候选计数，不构造未公开的逐项清单；
- `optknock_plans_pre_validation.csv`：14 个方案标识符与 `obj` 转录值，目标函数定义和跨方案可比性保持未恢复；
- `selected_targets_pre_validation.csv`：实验前选定的六个靶点；
- `target_selection_evidence.csv`：反应、基因、ORF、通路位置、预期影响、证据和证据状态的读者矩阵；
- `wetlab_validation.csv`：同批次发酵图的近似读图值；
- `round1_outcomes.csv`：实验后结果，与推荐前数据层分离；
- `feedback_rules.json`：项目级终点、持续性、生物量和可实施性规则及敏感性网格；
- `post_feedback_evidence.csv`：规则计算的证据层级、判定轨迹、稳定展示顺序和设计方向；
- `data_status_mapping.csv`：受控数据状态映射；
- `evidence_conflicts.csv`：批次、浓度、组别、公式、光通道和颜色查表等解释冲突。

反馈规则不按基因名称分支；六个靶点的映射和记录完整性检查依据本项目材料固定。`updated_evidence_tier` 是证据层级，`display_order` 只用于确定表格顺序。运行证据管线后，`results/gsmm/validation_summary.csv` 汇总 AST 对照与六个靶点，`feedback_threshold_sensitivity.csv` 记录 144 组项目阈值组合的分类稳定性。

所有 `source_file_internal` 均为相对仓库根目录的可解析公开路径，可回到 `docs/evidence/` 的事实摘录、证据图或工作簿来源。