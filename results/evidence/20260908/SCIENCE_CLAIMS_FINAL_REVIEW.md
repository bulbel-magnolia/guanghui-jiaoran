# 科学声明最终复核

状态：`SCIENCE_CLAIMS_REVIEW_RESOLVED_20260908`

本文件是 `results/evidence/20260908/code_parts_sync/science_claims_reviewpoint.md` 的后续复核记录。原 closeout 报告如实保留同步当时的审核点；本轮在冻结 benchmark、湿实验证据和元件记录基础上完成正文清理，不改变共同模型、235-gene 候选空间、v1/v2A 条件、ranking、Top-6 或四方法 benchmark 数字。

## 已解决项目

### README.md

已删除或替换以下旧表述：

- “虾青素产量提升 45%”及不存在的旧 OptKnock 一键入口；
- “零化学废水 / 零毒排放”的绝对化结果表述；
- “8 条通路均已成功构建测试”；
- “SCI 论文 1 篇、北大核心 1 篇、48 项在申专利”等缺少本届证据映射的声明；
- `<your-repo-url>` 等模板内容。

README 现以 2026 冻结证据为主：235-gene benchmark、FastKnock/CFSA/OptEnvelope/FABRIC-AI 四方法结果、P0 Round 1 的 ΔPAN5/ΔMDE1 定量记录、PhiReX、BmCBP、两项 AISB26 元件和正式复现入口。

### wiki/Verifiability.md

已删除模板中的：

- “命中率 27%”；
- “Top-K 0.27 ± 0.03”；
- “Pearson r = 0.61 ± 0.05”；
- 虚构训练/测试集和 GPU 种子示例；
- “所有量化结果至少 n=3（生物学重复）”的统一化表述。

现页面以实际复现结果为准：235-gene prepare、v1/v2A 235/235 evaluate、9 项 ranking tests、15/15 verification、冻结 SHA-256、AISB26 FASTA/GenBank 一致性和真实 smoke 入口。实验重复按各 characterization 原始记录描述，“3 次测量”不自动升级为“3 个生物学重复”。

## 仍保留的历史审计内容

以下内容继续保留在 history/audit 文件中，不作为最终项目结论：

- 237-gene 旧候选池及纠错过程；
- 数值等价修正前的 YOR311C 等旧 secondary ranking；
- OptEnvelope “真实零候选”形式的禁止性说明；
- FABRIC-AI production-superiority 禁止字段。

这些记录用于解释版本演化和审核轨迹，与最终 README、Wiki、评审表的当前结论分开。

## 当前评审入口

- `README.md`
- `wiki/AI-Computational-Methods.md`
- `wiki/Integrated-Validation.md`
- `wiki/Wet-Lab-Experiments.md`
- `wiki/Verifiability.md`
- `wiki/Parts.md`
- `results/baseline/20260908/FOUR_METHOD_BENCHMARK_FINAL.md`
- `results/fabric_ai/20260908/DESIGN_MODE_FINAL_FREEZE.json`

*复核日期：2026-09-08*
