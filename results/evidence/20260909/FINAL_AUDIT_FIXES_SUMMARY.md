# 提交前修复结果 · 2026-09-09

## 工作范围与版本

修复起点为 `88082e13d1a9e715f63a24d2b53c7e0fe9bbb523`。修复分支为 `final-audit-fixes-20260909`，承接该分支的只读验证工作流提交 `7f4752e93e970d81728286fa445141e72a34edbb`。本轮不合并 `master`，不同步 Gitee，不代替团队签署或提交评审表。正式应用的提交 ID 由交付包的 Git bundle、提交记录与交付清单确定。

本届工作在团队已有实验、元件与项目成果基础上继续迭代。

## 1. 修复项目、依据与结果

| 原终审问题 | 本轮实际修改 | 主要文件及新证据 |
|---|---|---|
| C.3.1 缺少可追溯的定量反馈前后状态 | 从 v0.8 恢复真实反馈引擎、规则和 pre/post 数据；新增可执行状态转移导出；未改旧阈值，未伪造历史模型版本 | [Learn 实现](../../../src/ai/fabric_ai_optimizer/learn_mode.py)、[配置](../../../configs/fabric_ai/learn_mode_v08_replay.json)、[C.3.1 定量证据](C3_1_QUANTITATIVE_ITERATION.md) |
| PhiReX 四段 CDS 边界可疑 | 保留原 DNA、坐标与方向；HY1、PcyA、EGFP、KanMX 改为 `misc_feature`；两个融合蛋白保留 CDS 并通过阅读框检查；重建真实序列图谱 | [GenBank](../../../parts/AISB26-045-001/registry_export.gb)、[图谱](../../../parts/AISB26-045-001/map.svg)、[变更依据与原件](phirex_annotation/README.md) |
| R5/R11/R13 身份、n 和统计标记不能追溯 | 搜索已恢复的八版工作簿与历史资料；保留身份、重复和误差线人工确认字段；区分 Fig.12 与 Fig.13；只移除 Fig.12 图上的未获支持星号及括号 | [恢复记录](phirex_annotation/phirex_digitized_records.csv)、[像素编辑记录](phirex_annotation/figure_edit_record.json)、[元数据](../../../parts/AISB26-045-001/metadata.yaml) |
| BmCBP 原始测量入口与实际提交矛盾 | Verifiability 改为每条件 3 次测量、当前仅保留均值、逐次原始值未恢复；不生成 SD/SEM 或误差线 | [可验证性](../../../wiki/Verifiability.md) |
| 排序器接受 NaN、失败状态、来源不一致或错误派生比例 | 在公共 `build_ranking` 与 CLI 增加状态感知校验；保持合法的 v2A 不可行情形；冻结排序内核不变 | [排序实现](../../../src/ai/fabric_ai_optimizer/fabric_ai_benchmark.py)、[新增测试](../../../tests/fabric_ai/test_ranker_input_validation.py) |
| C.3.5 参赛队伍身份需要复核 | 团队于 2026-09-10 再次核对本届参赛信息，确认 NUDT-CHINA、SCU-China 均为本届参赛队；三队手册合作及各方 Wiki 记录用于 C.3.5 佐证 | [合作资格说明](C3_5_COLLABORATION_STATUS.md)、[Collaboration](../../../wiki/Collaboration.md) |
| 历史成果与本届新增工作混淆 | 在重点正文使用统一承接句；底层资料保留准确时间、Registry 来源和本轮实现性质 | [贡献记录](../../../attributions.md)、[AI 使用披露](../../../AI-USE-DISCLOSURE.md)、[来源清单](recovered_v08/SOURCE_MANIFEST.json) |
| C.3.2 容易被误读为增产性能领先 | 保留显著创新路线；全量表型、多条件同池、目标区分度、数值等价与 Design/Learn 分离分别陈述 | [AI/计算方法](../../../wiki/AI-Computational-Methods.md)、[奖牌证据状态](medal_evidence_status.json) |

## 2. C.3.1 的定量前后结果

更新对象是同一组 6 个历史实验靶点的 Learn 决策状态，不是新版 Design Top-6。反馈前，真实选择表只记录进入 Round 1，证据等级为未评定；反馈后，原 v0.8 引擎根据实验数据给出具体等级与动作。

| 指标 | 反馈前 | 反馈后 |
|---|---:|---:|
| 对应靶点数 | 6 | 6 |
| 已评定靶点 | 0/6 | 6/6 |
| 未评定靶点 | 6 | 0 |
| 状态中已纳入定量发酵证据的靶点 | 0 | 2 |
| 下一轮动作类别 | 1 | 3 |

PAN5 更新为 Tier 1、优先推进；MDE1 更新为 Tier 2、复核机制；RIB2、MRI1、SPE2、FUM1 更新为 Tier 3、调整构建或培养。原反馈表的全部字段得到重放复核。

**C.3.1 当前可支持的内容：**计算辅助选靶、已有实验验证和可执行规则型 Learn 状态更新形成有对象、有数值、可重放的闭环证据。0/6→6/6 是决策状态更新量；不表示模型准确率从 0% 提高到 100%，也不表示 GSMM 重训练或新实验增产。评审委员会对该状态更新是否满足条款中的模型迭代作最终认定。

[before.json](../../fabric_ai/20260909/learn_mode_iteration/before.json) · [实验输入](../../fabric_ai/20260909/learn_mode_iteration/experimental_feedback.json) · [after.json](../../fabric_ai/20260909/learn_mode_iteration/after.json) · [逐靶点变化](../../fabric_ai/20260909/learn_mode_iteration/comparison.csv) · [运行与核验](../../fabric_ai/20260909/learn_mode_iteration/README.md)

## 3. PhiReX 最终状态

FASTA 与 GenBank 序列逐碱基一致，12584 bp DNA 与修复前相同。PIF3-NLS-VP16、PhyBNT-Zif268 的 CDS 结构检查通过；HY1、PcyA、EGFP、KanMX 的原注释区段保留为 `misc_feature`，精确编码边界留给原设计/测序资料确认。修改 feature 类型并不等于证实这四段的功能或精确 ORF。

R5、R11、R13 只确认到原记录的样品编号，构建/克隆对应、重复类型、n 和误差线定义未恢复。恢复的 Fig.12 和 Fig.13 是两份分开保存的图记录，不合并为重复。正文“红光高于对照”限定到 Fig.12；Fig.13 中 R11、R13 没有相同方向，原始记录已保留。

表达图只清除三个统计标记区，区域外像素完全不变；原图、编辑坐标和哈希同时保存。修复后的 SVG 已实际渲染并检查。

## 4. 测试、冻结结果与复现入口

本轮分别保留三类测试：原有 9 项合成排序用例、基于真实冻结输入的 40 项校验测试、19 项 Learn 测试。原 9 项测试源码未变；其路径适配器明确指向未变的排序内核，公共入口的新增校验由真实输入测试单独覆盖。没有把新测试数量改写进旧日志。

最终汇总以 [实际验证报告](validation/verification.json) 为准；原始 stdout、命令、环境和退出码见同目录日志。

| 核验 | 证据位置 |
|---|---|
| 原 9 项排序测试 | [frozen9.log](validation/frozen9.log) |
| 40 项公共入口防错测试 | [hardening.log](validation/hardening.log) |
| 19 项 Learn 测试 | [learn_tests.log](validation/learn_tests.log) |
| 原 15 项最终 verification | [原 verification 输出](validation/frozen_verifiers/ranking_numeric_correction_verification.json) |
| 当前元件文件及源序列检查 | [parts_integrity.csv](validation/parts_integrity.csv) |
| PhiReX feature 审计 | [feature_audit.json](validation/feature_audit/feature_audit.json) |
| Learn 独立重放与提交输出逐字节比较 | [learn_reproduction_comparison.json](validation/learn_reproduction_comparison.json) |
| 公共 CLI 排序与冻结表逐单元格比较 | [rank_output_comparison.json](validation/rank_output_comparison.json) |
| 模型、条件、baseline、历史结果哈希保护 | [protected_files_comparison.json](validation/protected_files_comparison.json) |
| 重点页面相对文件路径与过期声明 | [relative_links.json](validation/relative_links.json)、[stale_claim_scan.json](validation/stale_claim_scan.json) |

```bash
python -m pip install -r requirements-submission-validation.txt
python tools/fabric_ai/validate_submission_fixes.py --outdir .reproduction/submission-fixes-check
```

使用新的空输出目录。验证环境是本轮记录的 Python 3.13 环境，未替换原代谢求解的冻结依赖。本轮无需也未重新求解 235×2 个表型；独立检查覆盖排序、状态重放、序列/注释和提交文件。

冻结表型、全部 235 行排序、Top-6 和 scope 继续保留原结果。数值单元格一致性与字节一致性分别报告；平台换行等序列化差异不被混作数值变化。

## 5. 奖牌条目与人工事项

**C.3.2：**继续走显著创新路线，不提出生产性能优于基线的声明。

**C.3.5：**团队于 2026-09-10 再次核对本届参赛信息，确认 NUDT-CHINA、SCU-China 均为本届参赛队伍。三队联合教育手册在 BIT-China、NUDT-CHINA 和 SCU-China 的 Wiki 中均有记录，本条按“其他参赛队伍合作 + 双方/多方记录”申报。

团队提交前继续核对 PhiReX 四段精确编码边界与 R5/R11/R13 身份和重复定义，并确认最终评审表、安全文件签字、Gitee 同步、邮件与视频交付。
