# AI / 计算方法

FABRIC-AI 面向工程化酵母产色与实验决策，将机制模型、约束优化、候选全量表型评价、实验优先级排序和湿实验反馈组织为一套可追溯的计算流程。当前系统由三个互相衔接的模块组成：

- **P0 Production Optimizer**：围绕酵母代谢网络筛选并评价基因干预；
- **P1 Material Interface Optimizer**：整合 BmCBP、色素结合与织物实验，支持固色材料选择；
- **P2 Color & Light Translator**：连接颜色目标、光照参数和 PhiReX 表征数据。

本页重点说明 P0 的可执行 benchmark 版本及其与近三年公开方法的比较。

---

## 1. 任务定义

共同任务定义为：**在统一酵母代谢模型和统一单基因敲除空间中，评价每个候选的生长—生产表型，并形成可进入湿实验的优先级决策。**

共同模型基于 Yeast-GEM v9.1.0，并加入 FABRIC 项目的异源产色通路。最终冻结的单基因可实施空间包含 **235 个基因**，生物量反应为 `r_2111`，目标产物反应为 `FABRIC_r_4799`，数值容差统一为 `1e-7`。

正式 Design mode 使用两个预先固定的条件：

| 条件 | 角色 | 用途 |
|---|---|---|
| `v1_glucose_reference` | 主条件 | 候选准入与共享 benchmark |
| `v2a_historical_ethanol_stage` | 生产阶段敏感性条件 | 对同一 235-gene primary pool 进行跨条件评价 |

YPD-informed 的 B-vitamin availability sweep 作为培养基机制诊断，保留在 v2B 分析中，不进入正式 baseline 胜负。

---

## 2. FABRIC-AI Production Optimizer v1.2

### 2.1 Design mode

Design mode 对 primary condition 中的 235 个可实施单基因敲除逐一施加完整 GPR 失活集合，并计算统一表型。历史 Round 1 的 PAN5、MDE1 等实验结果不进入候选生成、阈值或排序，保证公开 benchmark 与后验实验反馈分离。

每个候选记录：

- `mutant_mu_max`：突变体最大生长；
- `Pmin/Pmax`：在 10%、50%、90% WT 绝对生长下限下的最小/最大产物通量；
- `Pmin95/Pmax95`：在 `biomass >= 0.95 × mutant_mu_max` 条件下的产物上下界；
- `GCP`：Guaranteed Coupled Production；
- `GR`：Growth Retention；
- `PCR`：Product Capacity Ratio；
- `footprint_size`：真实基因敲除导致的失活反应数量。

对每个条件 `c`：

`GCP(g,c) = mean_f [ Pmin(g,c,f) / max(Pmax_WT(c,f), 1e-12) ]`

其中 `f ∈ {0.1, 0.5, 0.9}`。GCP 直接衡量在共同生长要求下被敲除后仍被强制保留的产物下界。

跨条件稳健性由 `Robust_GCP = min_c GCP`、`Median_GCP` 和 `Robust_GR = min_c GR` 描述。

### 2.2 目标区分度检测

系统在正式排序前检查 primary condition 的 GCP 与 Pmin95。如果全部候选在这两个指标上均为 0，则标记：

`NON_DISCRIMINATING_GUARANTEED_PRODUCTION`

这一状态表示当前 guaranteed-production 目标无法继续区分 235 个候选。程序随后进入预先冻结的可实施性排序层，对完整表型表进行确定性整理，并把输出范围标记为 `SECONDARY_FEASIBILITY_ORDER_ONLY`。

### 2.3 确定性排序

排序采用固定的字典序规则，不设置可事后调整的线性权重：

1. `Robust_GCP` 降序；
2. `Median_GCP` 降序；
3. primary `Pmin95` 降序；
4. `Robust_GR` 降序；
5. primary `PCR@0.1WT` 降序；
6. `footprint_size` 升序；
7. gene ID 字典序。

排序前先在原始通量单位应用 `1e-7` 数值等价规则。若 KO 与 WT 的目标差异不超过求解容差，则在排序中视为等价，避免把 LP 数值噪声放大成候选差异。

### 2.4 Learn mode

Design mode 冻结后，湿实验结果进入 Learn mode。版本化反馈规则读取终点产量、96–120 h 持续性、生物量保持和构建/培养可实施性，更新证据等级和下一轮动作。Design 与 Learn 分开保存，使公开 baseline 比较、历史实验结果和后续模型更新保持清晰的数据边界。

方法规范与冻结状态见：

- [`FABRIC-AI Production Optimizer v1.2 规范`](../src/ai/fabric_ai_optimizer/FABRIC-AI_Production_Optimizer_SPEC_v1.2.md)
- [`最终冻结状态`](../results/fabric_ai/20260908/DESIGN_MODE_FINAL_FREEZE.json)

---

## 3. 近三年公开基线

我们选择三种 2023–2024 年公开的菌株优化方法：

| 方法 | 年份 | 公开任务 |
|---|---:|---|
| FastKnock | 2024 | growth-coupled knockout search |
| CFSA | 2024 | comparative flux sampling 与干预发现 |
| OptEnvelope | 2023 | production-envelope guided reaction-set design |

共同 benchmark 统一使用 corrected v1 模型和 corrected 235-gene 单基因空间。公开方法保留各自原生输出；能够映射到真实单基因敲除的结果，再进入共享 gene-level 独立评价。

来源：

- FastKnock：Hassani et al., 2024；
- CFSA：van Rosmalen et al., 2024；
- OptEnvelope：Motamedian et al., 2023。

---

## 4. 四方法 Benchmark 结果

| 方法 | 本轮共同任务输出 | 235-gene 空间的 gene-level 表型覆盖 | Guaranteed-production 结果 | 面向实验的输出 | 正式运行时间 |
|---|---|---:|---|---|---:|
| FastKnock 2024 | 0 个合法 native gene candidate | 0/235 | 无候选，质量指标 N/A | 未形成候选列表 | 9.912 s |
| CFSA 2024 | 14 个合法单基因 KO | 14/235 = 5.96% | 0/14 出现正 `Pmin` | 14 个映射 KO | ≤1416.77 s |
| OptEnvelope 2023 | 11 个 target point 完成；0 个可映射 gene row | 0/235 | gene-level 指标 N/A | 未形成可映射单基因列表 | 3114.15 s |
| **FABRIC-AI v1.2** | **235/235 基因完成显式表型计算与确定性排序** | **v1：235/235；v2A：同一 235/235** | **自动识别 `NON_DISCRIMINATING_GUARANTEED_PRODUCTION`** | **完整 phenotype table + 可实施性 Top-6** | **635.91 s** |

运行时间用于记录正式执行成本和复现环境；四种方法的原生工作负载不同。

完整冻结表见 [`FOUR_METHOD_BENCHMARK_FINAL.md`](../results/baseline/20260908/FOUR_METHOD_BENCHMARK_FINAL.md)。

### 4.1 结果解释

FastKnock 在 corrected 235-gene 任务上返回 0 个合法候选；CFSA 映射得到 14 个单基因 KO；OptEnvelope 修正版完成 11 个目标点后没有形成可映射 gene-level 输出。FABRIC-AI 对 **235/235 个可实施基因**完成主条件表型计算，并对同一 235-gene primary pool 在 v2A 乙醇生产阶段条件下再次评价，得到 **100% 的完整候选空间表型覆盖**。

在 primary condition 中，235 个候选的 GCP 与 Pmin95 均为 0。系统据此识别出 guaranteed-production 指标已经失去区分能力，并进入冻结的可实施性决策层。该流程保留完整表型信息，直接回答实验设计中的三个问题：哪些基因可实施、这些干预在不同条件下如何影响生长与生产、当前优化目标是否足以支持候选优先级。

最终 secondary experiment-priority set 为：

1. `YAL060W`
2. `YBR006W`
3. `YBR011C`
4. `YBR183W`
5. `YBR281C`
6. `YCR005C`

六个候选均标记为 `SECONDARY_FEASIBILITY_ORDER_ONLY`。该列表服务于实验资源配置；生产性能评价继续使用独立的 GCP/Pmin95 指标。

---

## 5. FABRIC-AI 的方法创新

四方法比较显示，FABRIC-AI 将菌株优化从候选搜索扩展为**完整候选空间的实验决策流程**：

| 决策能力 | FastKnock | CFSA | OptEnvelope | **FABRIC-AI** |
|---|:---:|:---:|:---:|:---:|
| 统一 gene-level GPR 评价 | 候选子集 | 映射 KO 子集 | 映射子集 | **完整 235-gene 空间** |
| 全候选 phenotype profiling | — | — | — | **235/235** |
| 同一 primary pool 的生产阶段敏感性评价 | — | — | — | **235/235** |
| Guaranteed-production 区分度检测 | — | — | — | **✓** |
| 显式 non-discrimination gate | — | — | — | **✓** |
| 数值等价感知的确定性排序 | — | — | — | **✓** |
| 固定实验推荐预算 | — | — | — | **Top-k = 6** |
| Design / Learn 分离 | — | — | — | **✓** |
| DBTL 反馈接口 | — | — | — | **✓** |

“—”表示该能力未作为对应公开方法在本次共享 benchmark 中的实现任务。

FABRIC-AI 的核心价值在于把模型计算转化为可直接进入实验决策的结构化输出：完整候选空间、统一表型、跨条件稳健性、目标区分度、数值等价和反馈接口在同一框架中保持可审计。

---

## 6. 与湿实验的衔接

历史 P0 闭环记录了完整的 Design–Build–Test–Learn 链条：Round 0 数据进入代谢分析，307 个候选反应经过 14 个 Plan 与人工审核形成 6 个 Round 1 靶点；ΔPAN5、ΔMDE1 获得定量发酵结果，六个靶点的结果进入版本化反馈规则，形成新的证据等级与后续动作。

P1 和 P2 分别将 BmCBP 色素结合/织物结果与 PhiReX 红光表征纳入结构化证据。完整闭环见 [干湿结合验证](./Integrated-Validation.md)。

---

## 7. 复现与证据入口

- 四方法最终比较：[`results/baseline/20260908/FOUR_METHOD_BENCHMARK_FINAL.md`](../results/baseline/20260908/FOUR_METHOD_BENCHMARK_FINAL.md)
- FABRIC-AI 最终冻结状态：[`results/fabric_ai/20260908/DESIGN_MODE_FINAL_FREEZE.json`](../results/fabric_ai/20260908/DESIGN_MODE_FINAL_FREEZE.json)
- Production Optimizer 方法合同：[`src/ai/fabric_ai_optimizer/fabric_ai_optimizer_contract_v1.2.json`](../src/ai/fabric_ai_optimizer/fabric_ai_optimizer_contract_v1.2.json)
- DBTL 与 Human Practices 证据摘要：[`results/evidence/20260908/DBTL_AND_HP_EVIDENCE.md`](../results/evidence/20260908/DBTL_AND_HP_EVIDENCE.md)
- 完整复现说明：[Verifiability](./Verifiability.md)

---

*最后更新：2026-09-08*