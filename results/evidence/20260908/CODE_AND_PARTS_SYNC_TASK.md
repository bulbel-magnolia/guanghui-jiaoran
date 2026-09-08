# Codex task · 最终代码、模型与元件文件同步

目标分支：`benchmark/fabric-ai-20260907`

本任务只做**冻结产物同步、复现入口和仓库一致性检查**。不得修改共同模型数值、235-gene 候选空间、v1/v2A 条件、FABRIC-AI ranking priority、Top-6、FastKnock/CFSA/OptEnvelope/FABRIC-AI 冻结结论、Wiki 科学数字或评审表声明。

## 1. 同步 FABRIC-AI Production Optimizer 冻结代码

以以下两个最终冻结包为唯一来源：

1. `FABRIC-AI_Production_Optimizer_v1.2_fresh_Design-mode_freeze_20260908.zip`
2. `FABRIC-AI_Production_Optimizer_v1.2_ranking_numeric_equivalence_correction_20260908.zip`

同步到仓库：

- `src/ai/fabric_ai_optimizer/fabric_ai_benchmark.py`
- `src/ai/fabric_ai_optimizer/verify_design_mode.py`
- `tests/fabric_ai/test_ranker.py`
- `configs/fabric_ai/v1_glucose_reference.json`
- `configs/fabric_ai/v2a_historical_ethanol_stage.json`
- `configs/fabric_ai/protected_reaction_ids.json`
- `models/fabric_ai/common_model.json`
- `results/fabric_ai/20260908/candidate_space.json`
- `results/fabric_ai/20260908/v1_candidate_metrics.csv`
- `results/fabric_ai/20260908/v2a_candidate_metrics.csv`
- `results/fabric_ai/20260908/design_mode_ranking.csv`
- `results/fabric_ai/20260908/design_mode_topk.csv`
- 最终 correction 的 summary / verification / manifest

`design_mode_ranking.csv` 与 `design_mode_topk.csv` 必须使用数值等价修正后的最终版本。旧排序保留在历史审计目录，不覆盖最终文件。

## 2. 同步 AISB26 完整三件套/扩展文件

从 `FABRIC-AI_v0.8_phase2_baseline_signed_20260905.zip` 中逐字节同步：

### AISB26-045-001

- `sequence.fasta`
- `registry_export.gb`
- `map.svg`

现有 `metadata.yaml` 与 `characterization.md` 保留；若 v0.8 对应字段比当前分支更完整，可做字段级合并，但不得改变序列、编号、年份和实验结果。

### AISB26-045-002

- `registry_export.gb`
- `map.svg`

现有 `sequence.fasta`、`metadata.yaml`、`characterization.md` 保留，并核对 FASTA 与 GenBank CDS/sequence 一致性。

## 3. 建立复现入口

在 `src/ai/fabric_ai_optimizer/README.md` 写出最短复现流程，包括：

```bash
python src/ai/fabric_ai_optimizer/fabric_ai_benchmark.py prepare ...
python src/ai/fabric_ai_optimizer/fabric_ai_benchmark.py evaluate ...
python src/ai/fabric_ai_optimizer/fabric_ai_benchmark.py rank ...
python -m pytest tests/fabric_ai/test_ranker.py -q
```

参数必须来自冻结条件和 235-gene primary pool。不要新定义默认值来替代冻结合同。

记录：Python 版本、COBRApy/SciPy/swiglpk/pandas 依赖、solver tolerance `1e-7`、模型 SHA-256、v1/v2A metrics SHA-256、ranking correction ZIP SHA-256。

## 4. 仓库一致性扫描

仅扫描并报告，不自动改科学内容。重点查找：

- `YYYY-MM-DD`、`<例`、`<姓名`、`BBa_XXXX` 等模板残留；
- `237 genes` / `237-gene` 的旧候选池表述；
- 旧 Top-6 `YOR311C...`；
- `true zero candidate` / “真实零候选”形式的 OptEnvelope 旧结论；
- `production superiority` / “生产性能优于公开基线”形式的 FABRIC-AI 旧结论；
- broken relative links；
- `wiki/` 必设页和 `parts/` 文件完整性。

允许自动修复的只有：明显的相对路径、README 导航、已被最终冻结文件替代的旧状态入口。科学数字和结论必须停在审核门。

## 5. 运行验证

至少完成：

- FASTA/GenBank 一致性；
- 9 项 ranking tests 全部通过；
- 最终 ranking verification 15/15；
- 关键文件 SHA-256 与冻结包一致；
- 复现命令 smoke test；
- 所有新增相对路径存在。

## 6. 返回包

返回一个轻量 closeout ZIP，包含：

- `README_最终仓库同步结果.md`
- `final_repo_manifest.csv`
- `consistency_scan.csv`
- `reproduction_smoke_test.log`
- `parts_integrity_check.csv`
- `science_claims_reviewpoint.md`（只有发现需要人工裁定的科学内容时才列）

若没有科学内容冲突，状态写：

`REPO_SYNC_COMPLETE_READY_FOR_JUDGING_FORM_FINALIZATION`
