<div align="center">

# 干湿结合验证

**Design → Build → Test → Learn**

`P0 生产优化` · `P1 材料接口` · `P2 光控系统`

</div>

<div align="center">

[← Wiki 首页](./Home.md) · [AI / 计算方法](./AI-Computational-Methods.md) · [湿实验](./Wet-Lab-Experiments.md) · [工程化循环](./Engineering-Cycle.md)

</div>

> **闭环核心**：计算模型用于缩小设计空间并形成实验优先级；湿实验提供真实结果；版本化反馈规则把结果重新写回下一轮设计依据。P0、P1、P2 三条主线分别对应生产优化、材料接口和光控工程。

| 闭环 | Design | Build / Test | Learn / 下一步 |
|---|---|---|---|
| **P0 Production Optimizer** | `307 → 14 → 6` | ΔPAN5、ΔMDE1 定量发酵 + 其余四靶点可实施性记录 | feedback tier 与下一轮优先级 |
| **P1 Material Interface** | BmCBP 功能分析与分子对接 | 表达纯化、A480、织物/基材实验 | 丝绸优先；双层固色方向 |
| **P2 Color & Light** | 光控回路与参数设计 | PhiReX 红光表征、硬件迭代 | 光传感、GUI、4G 与可调整光控接口 |

---

## 1. P0 · FABRIC-AI 生产优化主闭环

### Design：从发酵记录到 6 个实验靶点

Round 0 发酵数据进入 Yeast9/FBA/OptKnock 分析。历史模型页面记录 **307 个候选反应**，OptKnock 页面进一步保存 **Plan1–Plan14**。团队结合代谢通路、文献证据和实验可实施性完成审核，最终选择 6 个 Round 1 基因靶点：

`RIB2` · `PAN5` · `MDE1` · `MRI1` · `SPE2` · `FUM1`

<div align="center">

**307 个候选反应 → 14 个 Plan → 6 个实验靶点 → Round 1 → feedback tier**

</div>

### Build / Test：Round 1 发酵结果

| 靶点 | Round 1 结果 | 对后续决策的作用 |
|---|---|---|
| **ΔPAN5** | 120 h 约 `0.67 mg/L`；同批 AST 约 `0.47 mg/L`，提升约 **42.6%** | 保留为高优先级证据 |
| **ΔMDE1** | 96–120 h 由约 `0.42 mg/L` 降至 `0.36 mg/L` | 进入后期持续性评价 |
| RIB2 / MRI1 / SPE2 / FUM1 | 构建或培养可实施性状态 | 进入工程可实施性反馈 |

### Learn：实验结果更新证据等级

版本化 feedback rules 读取四类项目指标：

| 指标 | 含义 |
|---|---|
| `terminal_yield_score` | 120 h 同批次终点产量 |
| `persistence_score` | 96–120 h 产量变化 |
| `biomass_score` | 120 h 生物量保持 |
| `feasibility_score` | 本轮构建或培养可实施性 |

反馈程序将 PAN5 更新为 **Tier 1**，MDE1 更新为 **Tier 2**，RIB2、MRI1、SPE2、FUM1 更新为 **Tier 3**。对 144 组阈值组合进行敏感性检查后，六个靶点的证据等级保持稳定。

> **P0 的闭环结果**：实验结果直接改变下一轮优先级。PAN5 的正向结果进入重点证据，MDE1 的后期下降进入持续性评价，其余四项结果进入可实施性判断。

---

## 2. P1 · BmCBP 从计算推演进入实验验证

BmCBP 路线首先通过天然功能分析和分子对接评估其与类胡萝卜素结合的可行性。随后团队尝试 BmCBP 与丝蛋白的结构模拟，验证重点根据专家建议转入湿实验。

### Test：A480 与材料实验

| BmCBP 浓度 | 平均 A480 | 测量数 |
|---:|---:|---:|
| 0 mol/L | **2.19190** | 3 |
| `5.5×10^-7 mol/L` | **2.00360** | 3 |
| `1.1×10^-6 mol/L` | **1.84980** | 3 |

平均 A480 随 BmCBP 浓度增加而下降，支持 BmCBP 与虾青素结合。丝绸、棉和聚酯的比较进一步更新基材优先级，丝绸成为当前重点基材。

### Learn：Human Practices 改变材料设计

产业交流提出壳聚糖物理保护层后，项目形成“**蛋白媒染 + 物理保护**”的双层固色方向：BmCBP 负责色素结合与材料接口，壳聚糖用于提升洗涤、摩擦和环境暴露下的保护能力。

[查看 BmCBP 元件与实验 →](./Parts.md#3-aisb26-045-002--密码子优化的截短-bmcbp-编码序列)

---

## 3. P2 · 光控系统的实验—工程迭代

PhiReX 表征使用约 `630 nm`、`200 μW/cm²` 的红光脉冲，单次照射 2 h，总培养时间 24 h。实验测量 EGFP 和 OD600，并以 EGFP/OD600 表示归一化信号。

| 样品 | 红光条件相对无光对照 |
|---|---|
| R5 | 归一化 EGFP 更高 |
| R11 | 归一化 EGFP 更高 |
| R13 | 归一化 EGFP 更高 |

硬件开发同步吸收机械、自动化和团队交流反馈：支架与遮光结构经过多轮设计—打印—测试，远程监测需求推动 4G 通信、GUI 与参数远程调整进入系统接口。光传感和反馈模块使光控模块从固定照射装置扩展为可监测、可调整的工程系统。

[查看 PhiReX 元件与实验 →](./Parts.md#2-aisb26-045-001--phirex-红光调控表达系统)

---

## 4. 2026 可执行 Design mode 与闭环接口

2026 benchmark 版本将历史 FABRIC 的“候选筛选—人工审核—实验反馈”研究结构转化为可执行的 Production Optimizer v1.2。

| 阶段 | 数据边界 | 作用 |
|---|---|---|
| **Design mode** | 冻结共同模型、235-gene 候选空间；不使用 PAN5 / MDE1 后验结果 | 全空间表型评价、目标区分度检测、实验优先级 |
| **Learn mode** | Design mode 冻结后读取湿实验结果 | 更新 evidence tier 与下一轮动作 |

<div align="center">

**共同模型与候选全量评价 → 实验优先级 → 湿实验 → 证据等级更新 → 下一轮设计**

</div>

四方法 benchmark 和最终 Design-mode 结果见 [AI / 计算方法](./AI-Computational-Methods.md)。

---

## 5. 证据入口

| 证据 | 路径 |
|---|---|
| DBTL 与 Human Practices 证据摘要 | [`DBTL_AND_HP_EVIDENCE.md`](../results/evidence/20260908/DBTL_AND_HP_EVIDENCE.md) |
| FABRIC-AI 最终冻结状态 | [`DESIGN_MODE_FINAL_FREEZE.json`](../results/fabric_ai/20260908/DESIGN_MODE_FINAL_FREEZE.json) |
| 湿实验 | [Wet Lab](./Wet-Lab-Experiments.md) |
| 工程化循环 | [Engineering Cycle](./Engineering-Cycle.md) |
| Human Practices | [Human Practices](./Human-Practices.md) |

---

<div align="center">

[← Wiki 首页](./Home.md) · [AI / 计算方法](./AI-Computational-Methods.md) · [湿实验](./Wet-Lab-Experiments.md) · [Parts](./Parts.md) · [可验证性](./Verifiability.md)

</div>

*最后更新：2026-09-09*