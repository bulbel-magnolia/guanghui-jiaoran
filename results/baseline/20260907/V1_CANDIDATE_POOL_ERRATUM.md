# v1 candidate-space erratum — 2026-09-07

状态：`ERRATUM_IDENTIFIED_BEFORE_FINAL_BASELINE_FREEZE`

## 发现

以 fresh/presolved gene-KO LP 重新复算 v1 候选空间后，冻结的 237-gene pool 中有 2 个基因被错误记录为可生长：

| gene | exact KO footprint | old audit growth | fresh KO max growth | corrected status |
|---|---|---:|---:|---|
| YER014W | r_0942 (protoporphyrinogen oxidase) | ~0.080938 | 0 | exclude |
| YOR176W | r_0436 (ferrochelatase) | ~0.080938 | 0 | exclude |

两者都参与血红素合成相关反应；在 canonical v1 model 中严格关闭对应反应后最大生长为 0。direct GLPK 与独立 SciPy/HiGHS 路径一致支持该修正。

## FVA 本身没有变化

重新计算内部、gene-associated reactions 的 FVA 后，blocked set 与冻结 v1 的 600 条 blocked reactions完全一致。因此问题定位于原候选生成时的 gene-KO growth solve / solver state，而不是共同模型、FVA 规则或 GPR footprint 定义。

## 修正后候选池

- frozen historical v1：237 genes
- corrected v1：235 genes
- 删除：`YER014W`, `YOR176W`

## 对已完成 baseline 的影响

- CFSA 的 14 个最终合法 KO 候选中不包含这两个基因，因此 14-candidate independent-evaluation rows 不变。
- FastKnock 正式 v1 搜索输入曾包含旧 237 pool；最终冻结前必须在 corrected 235 pool 上做一次低成本 replay。
- OptEnvelope corrected compatibility run 的原 11 点不需因该 erratum 重跑：`r_0942` 与 `r_0436` 在全部 11 个正式 target floors 下均被独立确认是必需活跃反应。跨基线正式 gene space 统一使用 235 genes。

## 处理原则

不覆盖历史文件。旧 237 pool 只保留为审计记录；最终 manifest 以 235 作为 corrected v1 gene-level candidate space。