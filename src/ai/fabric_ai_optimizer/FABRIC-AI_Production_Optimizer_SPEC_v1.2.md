# FABRIC-AI Production Optimizer — 正式 benchmark 方法规范 v1.2

状态：`METHOD_SPEC_EXECUTABLE_V1_2_PRE_PUBLIC_BASELINE_RERUN`

## 1. 方法定位

本方法是 **2026 benchmark 的新可执行 FABRIC-AI Production Optimizer**。它继承历史 FABRIC-AI 的研究结构：

`代谢候选 -> 可实施性筛选 -> 有限实验预算优先排序 -> 湿实验反馈 -> 证据等级更新`

它**不是**对 2025 年原始 OptKnock/“307→14→6”未恢复代码和未恢复靶点特异评分规则的重建。历史材料只证明：307 个候选反应、14 个记录方案、6 个实验前靶点以及后续反馈链条存在；目标特异的文献权重和原始排序公式没有恢复。因此新方法必须把新规则、历史证据和后验实验结果严格分开。

## 2. Benchmark 任务

### 2.1 Design mode（用于公开 baseline 比较）

输入共同模型和**预先冻结的环境条件**，在共同允许空间内为单基因敲除候选计算生产—生长表型并排序，输出最多 6 个实验优先候选。

- intervention budget：每个菌株最多 1 个 gene knockout
- recommendation budget：`top_k = 6`（来自项目已有的六靶点实验预算，不根据 benchmark 结果调整）
- 不允许使用 Round 1 的 PAN5/MDE1 产量结果、feedback tier、历史六靶点身份作为输入特征或规则分支。

### 2.2 Learn mode（用于 DBTL 闭环，不用于 baseline 胜负）

Design mode 冻结后，实验结果可以进入已有的版本化 feedback rules，更新 evidence tier 和下一轮设计方向。Learn mode 体现闭环创新，不回填 Design mode 的 benchmark 排序。

## 3. 输入合同

1. canonical common model：指定 SHA-256。
2. biomass reaction：`r_2111`。
3. product reaction：`FABRIC_r_4799`。
4. condition set：在正式运行前冻结，至少区分 primary condition 与 sensitivity conditions。
5. protected reaction classes：boundary/exchange、transport、biomass、maintenance，以及比赛前已冻结的其他 protected reactions。
6. GPR：使用完整 Boolean gene-reaction rule；真实 gene knockout 后的全部失活反应共同施加。
7. solver tolerance：`1e-7`，显式设置并记录。
8. seed：仅用于需要随机性的步骤；当前 Design mode 排序本身应为确定性。

## 4. 候选空间

候选 gene 必须：

- 属于 native genes；
- 具有 non-empty effective GPR knockout footprint；
- footprint 不包含 protected reaction classes；
- 至少影响一个在 primary condition、`0.1 * WT_mu_max` 下 FVA-unblocked 的内部反应；
- knockout 后 `mutant_mu_max >= 0.1 * primary_WT_mu_max`。

历史靶点是否进入候选池不影响规则。

## 5. 每个候选必须计算的独立表型

对每个 condition `c` 和 gene `g`：

### 5.1 Growth

`GR(g,c) = mutant_mu_max / WT_mu_max`

### 5.2 Guaranteed production

在绝对 WT 生长下限 `f in {0.1, 0.5, 0.9}`：

- `Pmin(g,c,f)`
- `Pmax(g,c,f)`

另计算：

- `Pmin95(g,c)`：在 `biomass >= 0.95 * mutant_mu_max` 下最小 product
- `Pmax95(g,c)`：同一条件下最大 product

### 5.3 Normalized guaranteed-coupling score

对每个 condition：

`GCP(g,c) = mean_f [ Pmin(g,c,f) / max(Pmax_WT(c,f), eps) ]`

其中 `eps = 1e-12` 仅防止除零，不作为生物阈值。

该指标只奖励**在共同绝对生长要求下被敲除后仍被强制产生的产物下界**。若 `Pmin=0`，该项就是 0，不用 Pmax 替代。

### 5.4 Product-capacity ratio（描述性，不等同增产）

`PCR(g,c,f) = Pmax(g,c,f) / max(Pmax_WT(c,f), eps)`

由于 KO 的可行域是 WT 的子集，`PCR <= 1` 是正常数学结果。PCR 用于描述候选保留多少理论产能，**不允许写成“KO 提高理论最大产量”**。

### 5.5 Intervention complexity

- `footprint_size = number of reactions disabled by the gene knockout`

只用于同等生产证据下的可实施性 tie-breaker，不把 footprint 小自动解释为更高实验成功率。

## 6. 多条件稳健性

对冻结条件集合：

- `Robust_GCP(g) = min_c GCP(g,c)`
- `Median_GCP(g) = median_c GCP(g,c)`
- `Robust_GR(g) = min_c GR(g,c)`

如果某 sensitivity condition 代表短时生产阶段而非完整生长培养，则它可以进入 robustness **报告**，是否作为 hard admissibility condition 必须在条件冻结时预先声明；不能见结果后再改变。

## 7. 排序规则：不用结果后调权重

不采用可事后调节的线性加权总分。Design mode 使用固定的 lexicographic / Pareto-compatible 顺序：

1. `Robust_GCP` 降序；
2. `Median_GCP` 降序；
3. primary condition 的 `Pmin95` 降序；
4. `Robust_GR` 降序；
5. primary condition 在 10% WT growth floor 的 `PCR` 降序；
6. `footprint_size` 升序；
7. gene ID 字典序，保证完全确定性。

### 7.1 非区分状态

若 primary condition 中所有 eligible candidates 的 `GCP = 0` 且 `Pmin95 = 0`：

- 状态标记为 `NON_DISCRIMINATING_GUARANTEED_PRODUCTION`；
- 仍可输出“feasibility-oriented secondary order”，用于下一步实验规划；
- **不得把 secondary order 的第一名写成“生产性能优于 baseline”**；
- 金牌基线优势必须改用其他预先定义、可公平计算的关键任务，或走“显著创新”证据路线。

## 8. 与 FastKnock / CFSA / OptEnvelope 的公平比较

### 8.1 原生输出保留

- FastKnock：保留其 native KO 输出。
- CFSA：KO/OE/KD 原样保存；共同单基因 KO 表只评价可映射的 KO 子集。
- OptEnvelope：reaction-set 原样保存；只有完整 GPR 映射后真实单基因 KO 才进入共享 gene-level 表。
- FABRIC-AI：直接输出 single-gene ranked list。

### 8.2 独立 evaluator

所有进入共享表的候选都从 canonical model 重载、真实施加 gene knockout，再计算同一组 GR、Pmin/Pmax、Pmin95/Pmax95。算法自身 objective 不直接当成共享性能指标。

### 8.3 空输出

公开方法输出 0 个合法候选时：

- candidate count = 0；
- candidate-quality metrics = `N/A`；
- 不把 `N/A` 人工填 0 以制造提升百分比。

## 9. 正式 benchmark 指标

### 主表

- native candidate count
- legal gene candidate count
- `Best Robust_GCP`
- `Median Robust_GCP`（有候选时）
- `Best Pmin95`
- top-6 中满足 primary hard constraints 的数量
- wall-clock search time（模型准备和 independent evaluation 分开计时）

### 辅助表

- `Robust_GR`
- PCR
- footprint size
- condition-wise rank stability
- solver failure count / infeasible count

## 10. 历史湿实验结果怎样使用

历史 Round 1：PAN5 和 MDE1 有定量结果，其余四靶点是本轮可实施性未通过记录。它们：

- **不参与 Design mode 候选生成、阈值、排序或 tie-break**；
- Design mode 完全冻结后，可做 retrospective external check：例如 top-6 是否覆盖 PAN5；
- 由于定量 mutant 很少，该检查只作为项目闭环的一致性证据，不作为主要统计 benchmark。

## 11. Learn mode

沿用 v0.8 已版本化规则，输入实验后数据：终点产量、后期持续性、生物量保持和本轮可实施性，输出 evidence tier 与下一轮动作。Learn mode 的规则结果与 Design mode 的公开 baseline 比较分表呈现。

## 12. 禁止事项

- 禁止使用 PAN5 已知正结果调权重或阈值；
- 禁止将未实验的 baseline 候选记为实验失败；
- 禁止把 Pmax 下降解释成产量改进；
- 禁止在不同共同模型/培养条件之间计算“本队提升百分比”；
- 禁止把历史 307→14→6 称为当前可执行 optimizer 的直接数值输出；
- 禁止事后改变 top_k、growth threshold、condition membership 或 ranking order。

## 13. v1.1 冻结补充：绝对 WT 生长下限不可行的处理

若候选在某个绝对 WT 生长下限 `f` 处不可行，则该 `f` 的 `GCP component = 0`，`PCR = N/A`，状态写为 `growth_floor_infeasible`。不得删除该生长档位后重新平均，也不得把不可行解释成更优的生产耦联。

## 14. 当前条件成员关系

- `v1_glucose_reference`：primary standardized reference，进入 Design-mode hard admissibility。
- `v2a_historical_ethanol_stage`：production-stage sensitivity；进入稳健性报告，但不作为 hard admissibility 门禁。
- `v2b_vitamin_availability_*`：机制/培养基可用性诊断；在未知定量摄取率得到可靠依据前，不进入正式 baseline 胜负或 Design-mode robustness 排名。

当前条件成员关系在 v2B 数值诊断之前固定，不根据历史六靶点的恢复情况修改。

## 15. 数值容差下的排序等价类

排序前保留 GCP/Pmin95 的绝对零处理：`abs(x) <= 1e-7` 视为 0。GR 与 primary PCR@0.1WT 必须在求解器原生通量单位上判断等价：若 `abs(mutant_mu_max - WT_mu_max) <= 1e-7`，则 `GR_equiv = 1`；若 `abs(Pmax_mutant - Pmax_WT) <= 1e-7`，则 `PCR_equiv = 1`。KO 原生目标值若高于对应 WT 超过 `1e-7`，必须标记为不一致并拒绝排序。只有原生差值超过容差且方向合法时才沿用记录的归一化比值。该处理只消除 LP 数值噪声，不改变超过容差的生物学差异。

## 16. sensitivity condition 不得隐式缩小 primary candidate pool

正式 Design mode 的候选集合由 primary condition 决定。对 v2A 等 sensitivity condition，应评价 **全部 primary eligible genes**；即使某基因在 sensitivity condition 中低于 10% WT 生长，也保留该行并如实记录低 `GR`、不可行 absolute-growth floor 与相应的 0 GCP component。排序程序禁止对不同 condition 的 condition-specific eligible pools 做静默交集，以免把 sensitivity condition 变成未声明的 hard admissibility filter。

## 17. candidate admission 的 solver-state 规则

FVA 在固定约束下仅切换目标反应时可以复用 LP basis；gene knockout 会改变反应 bounds，因此每个 gene 的最大生长准入必须执行 fresh/presolved solve。已验证的 no-presolve warm-basis shortcut 会产生 false-feasible gene KOs，禁止用于候选生成、hard admissibility 或正式 benchmark。

## 18. v1.2 执行补充：非区分状态不得伪装为 Top-k 生产推荐

当第 7.1 节的非区分门禁触发时，程序仍输出完整的确定性 secondary order，便于复现和后续可实施性分析；对应 `design_mode_topk.csv` 的每一行必须标记 `recommendation_scope = SECONDARY_FEASIBILITY_ORDER_ONLY`，summary 必须写 `topk_interpretation`。这些行**不是**“预测最优生产靶点”，不得填入“本队优于公开 baseline”的生产性能表。

## 19. v1.2 依赖分层

`rank` 子命令只依赖 pandas，可在没有 COBRApy/GLPK 的轻量环境中复核排序与门禁；`prepare/evaluate` 才需要 COBRApy、SciPy 与 swiglpk。该拆分不改变任何模型计算或排序规则，只减少结果复核对求解环境的依赖。

## 20. 当前第一次执行状态

在 corrected v1 primary candidate space（235 genes）与 v2A sensitivity 记录上，全部候选的 primary-condition GCP 与 Pmin95 均在 `1e-7` 容差内为 0，第一次执行状态为 `NON_DISCRIMINATING_GUARANTEED_PRODUCTION`。因此当前运行只产生 secondary feasibility order，**未产生可用于 production-superiority claim 的 Top-k**。
