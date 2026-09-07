# FABRIC-AI OptEnvelope v1 修正版收尾审核

## 结论

本次修正版包可冻结为 **OptEnvelope v1 / GLPK compatibility run 的正式执行与审计记录**。

可冻结的正式表述是：

> 在冻结的 v1 共同模型、11 个目标点与 sequential reinsertion 规则下，经数值认证的修正版 OptEnvelope/GLPK 流程完成 11/11 个目标点，最终返回 11 个空 reaction sets；因此没有产生可进入共享单基因映射表的 reaction-to-gene mapping rows。

不得扩展为：

- “OptEnvelope 真实零候选”；
- “OptEnvelope 在该任务上理论上找不到候选”；
- “修复后的 activity pattern 已证明是原始最小活跃反应 MILP 的全局最优解”。

## 审核通过项

- manifest 内 57 个文件：57/57 大小与 SHA-256 一致。
- 3 个冻结输入与原 handoff 包逐字节哈希一致。
- 11/11 MILP target-point certifications 标记通过。
- 11/11 MAR target retention 通过。
- 16,426/16,426 MAR cleanup 记录通过。
- 16,426/16,426 sequential LP 记录通过。
- 最大 MILP/MAR mass-balance residual = 1.2553094e-08。
- 最大 MILP/MAR bound residual = 1.0460911e-08。
- 最大 sequential mass-balance residual = 1.7763568e-15。
- 最大 sequential bound residual = 2.5196928e-16。
- 11 个 native reaction sets 均为空。
- 231 个 production-envelope 点均为 optimal；11 组空干预曲线完全一致。
- 对 21 个唯一 growth fractions 用独立 SciPy/HiGHS 重算，Pmin 完全一致，Pmax 最大绝对差约 1.13e-08。
- 3114.15 s 外层正式运行低于 3600 s 预算。
- stderr 为空，stdout 未发现新的 error/warning/timeout 记录。

## 数值认证的解释边界

11 个点中：

- 8/11 通过 fixed-model LP re-solve；
- 3/11（target points 3, 8, 9）由经批准的 target-LP primal witness 路径认证，原 fixed-model GLPK re-solve 状态保留为 infeasible；
- 25 次 certification attempts 中 14 次被拒绝；
- 所有 11 个点都发生了 support repair。

因此，本包证明的是 **修正版兼容流程的可行性与残差合格**。它没有独立证明 support-repaired pattern 仍然实现原始“最小活跃反应数”MILP 目标的全局最优性。最终材料应继续使用 manifest 的保守表述，不把空 reaction sets 解释成方法能力上的“真实零候选”。

## 237 → 235 v1 候选池纠错的影响

后续 v1 审计已排除 YER014W 与 YOR176W：

- YER014W 的唯一 footprint：r_0942
- YOR176W 的唯一 footprint：r_0436

原 237-gene reaction domain 为 1139 reactions；纠正后的 235-gene union 为 1137 reactions，只减少 r_0942 与 r_0436。

独立 HiGHS 检查表明，在 11/11 个 OptEnvelope target floors 下：

- 固定 r_0436 = 0 → 不可行；
- 固定 r_0942 = 0 → 不可行；
- 两者同时固定为 0 → 不可行。

因此两条反应在所有正式 target points 中都属于必需活跃反应。把它们从“可删反应域”移到“保护域”只去掉两个在所有可行解中恒为 1 的 activity indicators，不改变 target-space 可行删除设计；无需因此重跑 OptEnvelope 原生 11 点。

正式跨基线候选池使用 **235 genes**。旧包中的 2607 条 GPR 审计是实际执行记录；最终共享候选空间解释时排除这两个基因对应的 22 条 not-applicable rows，即 11 × 235 = 2585 条适用审计行，合法映射仍为 0。

## 最终冻结建议

状态：

`OPTENVELOPE_V1_CORRECTED_COMPATIBILITY_RUN_FROZEN`

候选层解释：

`ZERO_RETURNED_REACTION_SETS / ZERO_MAPPABLE_GENE_ROWS; NOT A TRUE-ZERO-CANDIDATE CLAIM`

不需要再次修改共同模型、培养条件或重跑 11 个 target points。