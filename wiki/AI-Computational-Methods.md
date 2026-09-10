<div align="center">

# AI / 计算方法

**FABRIC-AI Production Optimizer v1.2**

`235 个基因的表型评价` · `近三年公开基线` · `多条件稳健性` · `设计 / 实验反馈分离`

</div>

<div align="center">

[← Wiki 首页](./Home.md) · [四方法基准比较](#2-四方法-benchmark) · [方法细节](#3-fabric-ai-production-optimizer-v12) · [干湿闭环](./Integrated-Validation.md) · [复现](./Verifiability.md)

</div>

> FABRIC-AI 在统一的 235 个单基因敲除候选中完成 **235/235 表型评价**，并对相同候选进行生产阶段敏感性分析。系统检查产物下界能否区分候选，再按固定规则安排实验优先级。

| 主条件评价 | 生产阶段敏感性 | 公开基线 | 计算质量控制 |
|:---:|:---:|:---:|:---:|
| **235 / 235** | **235 / 235** | **3 种近期方法** | **0 项失活反应集合不一致 / 0 次求解失败** |

---

<a id="1-共同任务与冻结输入"></a>
## 1. 共同任务与固定输入

共同任务是：**使用相同的酵母代谢模型和单基因敲除候选集合，评价候选的生长—生产表型，并确定实验优先级。**

共同模型基于 Yeast-GEM v9.1.0，并加入 FABRIC 项目的异源产色通路。最终确定的单基因可实施空间包含 **235 个基因**，生物量反应为 `r_2111`，目标产物反应为 `FABRIC_r_4799`，数值容差统一为 `1e-7`。

| 条件 | 角色 | 是否进入正式比较 | 用途 |
|---|---|:---:|---|
| `v1_glucose_reference` | **主分析条件** | **是** | 候选纳入条件与统一基准比较 |
| `v2a_historical_ethanol_stage` | 生产阶段敏感性 | 是，作为稳健性报告 | 对同一组 235 个主分析候选再评价 |
| `v2b_vitamin_availability_*` | 培养基机制诊断 | 否 | 研究营养可获得性对候选纳入条件的影响 |

> 设计阶段（Design mode）使用固定的模型、条件和候选空间。实验反馈阶段（Learn mode）在设计结果固定后读取历史 Round 1 数据；PAN5、MDE1 的实验结果不参与设计阶段的候选生成、阈值设定或排序。

<p align="center">
  <img src="./assets/figures/fabric-ai-p0-workflow.webp" alt="FABRIC-AI P0 算法流程" width="88%">
</p>
<p align="center"><em>FABRIC-AI P0 计算流程：对 235 个基因候选进行 GPR 干预映射和多条件表型评价，检查产物下界区分度后，给出实验优先级。</em></p>

---

<a id="2-四方法-benchmark"></a>
## 2. 四方法基准比较

### 2.1 近期公开基线

本轮选择三种 2023–2024 年公开的菌株优化方法：

| 方法 | 年份 | 原生任务 |
|---|---:|---|
| **FastKnock** | 2024 | 搜索生长耦联的敲除方案 |
| **CFSA** | 2024 | 比较通量采样并发现干预候选 |
| **OptEnvelope** | 2023 | 根据生产包络设计反应干预集合 |

基准比较使用修订后的 v1 模型和 235 个单基因敲除候选。各方法保留其原始输出；能够映射为单基因敲除的结果，再按统一标准独立评价。

来源：FastKnock — Hassani et al., 2024；CFSA — van Rosmalen et al., 2024；OptEnvelope — Motamedian et al., 2023。

<a id="22-冻结结果"></a>
### 2.2 比较结果

| 方法 | 本轮基因水平输出 | 表型评价覆盖 | 产物通量下界结果 | 实验候选输出 | 运行时间 |
|---|---:|---:|---|---|---:|
| FastKnock 2024 | 0 个符合条件的单基因候选 | 0 / 235 | 无候选，质量指标 N/A | 无候选列表 | 9.912 s |
| CFSA 2024 | 14 个符合条件的单基因敲除 | 14 / 235 = 5.96% | 0 / 14 出现正 `Pmin` | 14 个映射的敲除候选 | ≤1416.77 s |
| OptEnvelope 2023 | 11 个目标点完成；0 条可映射为单基因干预的记录 | 0 / 235 | 基因水平指标 N/A | 无可映射单基因列表 | 3114.15 s |
| **FABRIC-AI v1.2** | **235 / 235 基因完成逐项表型计算与确定性排序** | **v1：235 / 235；v2A：同一 235 / 235** | **检出产物下界无区分度** | **完整表型表 + 可实施性 Top-6** | **635.91 s** |

运行时间用于记录正式执行成本和复现环境；四种方法的原生工作负载不同。

<p align="center">
  <img src="./assets/figures/benchmark-coverage.webp" alt="四方法表型评价覆盖率" width="86%">
</p>
<p align="center"><em>235 个候选的表型评价覆盖率，即完成表型评价的候选比例，不表示增产成功率。</em></p>

完整比较表：[`FOUR_METHOD_BENCHMARK_FINAL.md`](../results/baseline/20260908/FOUR_METHOD_BENCHMARK_FINAL.md)

<a id="23-benchmark-给出的核心判断"></a>
### 2.3 结果解释

FastKnock 在 235 个基因的共同任务上返回 0 个符合条件的候选；CFSA 映射得到 14 个单基因敲除；OptEnvelope 修正版完成 11 个目标点，未输出可映射的单基因干预。FABRIC-AI 对 **235 / 235 个可实施基因**完成主条件表型计算，并对同一组 235 个主分析候选在 v2A 乙醇生产阶段条件下再次评价。

在主分析条件下，235 个候选的 GCP 与 Pmin95 均为 0。这两个指标无法区分候选，系统按预先设定的可实施性规则继续排序。

---

## 3. FABRIC-AI Production Optimizer v1.2

<a id="31-design-mode全空间显式评价"></a>
### 3.1 设计阶段：全部候选的表型评价

设计阶段对主分析条件中的 235 个可实施单基因敲除逐一施加完整 GPR 失活反应集合，并计算统一表型。

| 指标 | 含义 | 在决策中的作用 |
|---|---|---|
| `mutant_mu_max` | 突变体最大生长 | 判断候选是否保持基本可实施性 |
| `Pmin / Pmax` | 10%、50%、90% WT 生长下的产物上下界 | 描述共同生长要求下的生产范围 |
| `Pmin95 / Pmax95` | 近突变体最大生长状态下的产物上下界 | 描述接近最优生长时的生产状态 |
| `GCP` | 生长耦联产物下界指标 | 衡量满足生长约束时必须保留的产物通量 |
| `GR` | 生长保持比例 | 评价敲除后的生长保持能力 |
| `PCR` | 理论产能保留比例 | 评价敲除后保留的产物通量上界 |
| `footprint_size` | 基因敲除导致的失活反应数 | 干预复杂度描述 |

对每个条件 `c`：

`GCP(g,c) = mean_f [ Pmin(g,c,f) / max(Pmax_WT(c,f), 1e-12) ]`

其中 `f ∈ {0.1, 0.5, 0.9}`。跨条件稳健性由 `Robust_GCP = min_c GCP`、`Median_GCP` 和 `Robust_GR = min_c GR` 描述。

<a id="32-目标区分度检测"></a>
### 3.2 产物下界区分度检查

正式排序前，系统检查主分析条件的 GCP 与 Pmin95。若全部候选在两个指标上均为 0，则标记：

> **`NON_DISCRIMINATING_GUARANTEED_PRODUCTION`**
>
> 当前产物通量下界目标无法继续区分 235 个候选，系统转入预先设定的可实施性排序规则。

该状态下的排序用于分配实验资源，生产性能仍按 GCP 与 Pmin95 评价。

<a id="33-数值等价感知的确定性排序"></a>
### 3.3 考虑数值等价的固定规则排序

排序采用预先设定的字典序，按以下指标依次比较：

1. `Robust_GCP` 降序；
2. `Median_GCP` 降序；
3. 主分析条件下的 `Pmin95` 降序；
4. `Robust_GR` 降序；
5. 主分析条件下的 `PCR@0.1WT` 降序；
6. `footprint_size` 升序；
7. 基因 ID 字典序。

排序前在原始通量单位应用 `1e-7` 数值等价规则。若 KO 与 WT 的目标差异不超过求解容差，则在排序中视为等价。

最终实验优先级 Top-6：

| 顺序 | 基因 | 用途 |
|---:|---|---|
| 1 | `YAL060W` | 可实施性实验优先级 |
| 2 | `YBR006W` | 可实施性实验优先级 |
| 3 | `YBR011C` | 可实施性实验优先级 |
| 4 | `YBR183W` | 可实施性实验优先级 |
| 5 | `YBR281C` | 可实施性实验优先级 |
| 6 | `YCR005C` | 可实施性实验优先级 |

结果文件中的用途标记为 `SECONDARY_FEASIBILITY_ORDER_ONLY`，表示仅按可实施性安排实验。该列表不作为增产效果的排序。

<a id="34-learn-mode湿实验反馈进入下一轮"></a>
### 3.4 实验反馈阶段：湿实验反馈进入下一轮

设计结果固定后，实验反馈程序读取终点产量、96–120 h 产量变化、生物量保持和构建或培养结果，按已确定版本的规则更新证据等级和下一轮安排。

`learn_mode.py` 按 v0.8 规则读取实验数据，六个历史靶点的已评定数量由 **0/6→6/6**，下一轮安排分为 **1 项优先推进、1 项机制复核、4 项构建/培养调整**。规则阈值保持不变，程序在运行前后核对设计阶段文件的 SHA-256。

[实验反馈定量更新与复现](../results/evidence/20260909/C3_1_QUANTITATIVE_ITERATION.md) · [干湿结合验证](./Integrated-Validation.md)。

---

## 4. FABRIC-AI 的方法创新

| 决策能力 | FastKnock | CFSA | OptEnvelope | **FABRIC-AI** |
|---|:---:|:---:|:---:|:---:|
| 统一基因水平 GPR 评价 | 候选子集 | 映射 KO 子集 | 映射子集 | **完整 235 个基因的候选空间** |
| 全候选表型评价 | — | — | — | **235 / 235** |
| 同一主分析候选集合的生产阶段敏感性评价 | — | — | — | **235 / 235** |
| 产物通量下界区分度检测 | — | — | — | **✓** |
| 根据区分度确定排序用途 | — | — | — | **✓** |
| 考虑数值等价的固定规则排序 | — | — | — | **✓** |
| 固定实验推荐预算 | — | — | — | **Top-k = 6** |
| 设计 / 实验反馈分离 | — | — | — | **✓** |
| DBTL 反馈接口 | — | — | — | **✓** |

“—”表示本次比较中对应方法未实现该项任务，不评价该方法的其他用途。

FABRIC-AI 对全部候选计算统一表型，比较不同培养条件下的结果，检查产物下界的区分度，并按固定规则给出实验优先级。实验完成后，反馈程序更新靶点的证据等级和下一轮安排。

---

## 5. 与 P1 / P2 的计算接口

FABRIC-AI 的项目级架构还包含两个实验决策接口：

| 模块 | 输入 | 输出 |
|---|---|---|
| **P1 材料固色模块** | BmCBP、色素结合、织物/基材实验 | 固色材料优先级与下一轮验证方向 |
| **P2 颜色与光控模块** | PhiReX 红光表征、光参数、硬件状态 | 可执行光输入与颜色—光照映射接口 |

P1 / P2 的湿实验结果与工程迭代见 [湿实验](./Wet-Lab-Experiments.md) 和 [干湿结合验证](./Integrated-Validation.md)。

---

<a id="提交版输入校验"></a>
### 输入校验

公开排序入口先校验非有限指标、求解状态、模型和候选池来源、GPR 集合，以及原通量单位中的 GR/PCR 一致性。明确标记的 v2A 不可行状态保留；异常输入被拒绝。新增校验在保存的表型数据上复现完全相同的排序、范围标签和 Top-6。

[40 项输入校验测试](../tests/fabric_ai/test_ranker_input_validation.py)检查公共入口；原有 9 项人工构造用例单独检查排序核心。两组测试分别记录结果。

## 6. 复现与证据入口

| 内容 | 入口 |
|---|---|
| 四方法最终比较 | [`FOUR_METHOD_BENCHMARK_FINAL.md`](../results/baseline/20260908/FOUR_METHOD_BENCHMARK_FINAL.md) |
| FABRIC-AI 结果版本记录 | [`DESIGN_MODE_FINAL_FREEZE.json`](../results/fabric_ai/20260908/DESIGN_MODE_FINAL_FREEZE.json) |
| Production Optimizer 方法规范 | [`FABRIC-AI_Production_Optimizer_SPEC_v1.2.md`](../src/ai/fabric_ai_optimizer/FABRIC-AI_Production_Optimizer_SPEC_v1.2.md) |
| 方法参数 | [`fabric_ai_optimizer_contract_v1.2.json`](../src/ai/fabric_ai_optimizer/fabric_ai_optimizer_contract_v1.2.json) |
| DBTL / HP 证据摘要 | [`DBTL_AND_HP_EVIDENCE.md`](../results/evidence/20260908/DBTL_AND_HP_EVIDENCE.md) |
| 完整复现 | [可验证性](./Verifiability.md) |

```bash
python -m pip install -r ../src/ai/fabric_ai_optimizer/requirements-frozen.txt
python ../tools/fabric_ai/reproduction_smoke.py --outdir .reproduction/smoke
```

---

<div align="center">

[← Wiki 首页](./Home.md) · [干湿结合验证](./Integrated-Validation.md) · [湿实验](./Wet-Lab-Experiments.md) · [元件](./Parts.md) · [可验证性](./Verifiability.md)

</div>

*最后更新：2026-09-10（文字修订）*
