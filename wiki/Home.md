<div align="center">

# 光绘酵染 · FABRIC-AI

**工程化酵母天然色素 × 光响应调控 × BmCBP 固色 × 全空间计算决策**

`BIT-CHINA（045）` · `T3 工业生物制造` · `2026 mAI + 合成生物创新大赛`

</div>

> **项目目标**：围绕生物色素“产得出、留得住、可编程”三个问题，构建从菌株设计、材料固色到光控图案输出的一体化 FABRIC 系统，并用 FABRIC-AI 将计算设计与湿实验反馈组织成可执行的 DBTL 决策流程。

| 计算设计空间 | 近期公开基线 | 本届新元件 | 工程闭环 |
|:---:|:---:|:---:|:---:|
| **235 / 235** 基因完成全量表型评价 | **3** 种：FastKnock、CFSA、OptEnvelope | **2** 项 AISB26 元件 | **P0 / P1 / P2** 三条主线 |

---

## 评审快速入口

| 想快速核查什么 | 直接进入 | 30 秒可看到的核心证据 |
|---|---|---|
| **AI / 计算方法与近三年基线** | [AI / 计算方法](./AI-Computational-Methods.md) | 四方法 benchmark、235-gene 全空间评价、Design/Learn 分离 |
| **干湿结合闭环** | [干湿结合验证](./Integrated-Validation.md) | `307 → 14 → 6 → Round 1 → feedback tier` |
| **湿实验结果** | [湿实验](./Wet-Lab-Experiments.md) | ΔPAN5 / ΔMDE1、BmCBP、PhiReX |
| **两项新 DNA 元件** | [Parts](./Parts.md) | AISB26-045-001、AISB26-045-002 的序列、表征和图谱 |
| **复现与审计** | [可验证性](./Verifiability.md) | smoke 复现、9 项 tests、15/15 verification、SHA-256 |
| **项目影响** | [Human Practices](./Human-Practices.md) · [Education](./Education.md) · [Collaboration](./Collaboration.md) | 技术设计改变、教育活动、跨队伍互证 |

---

## 1. 项目架构

| 模块 | 核心问题 | 已完成工作 | 结果如何进入下一步 |
|---|---|---|---|
| **P0 · Production Optimizer** | 哪些代谢干预值得进入实验？ | corrected **235-gene** 全空间表型评价；FastKnock、CFSA、OptEnvelope 近期基线比较；历史 Round 1 形成 `307→14→6` 设计链 | 形成实验优先级并由 Learn mode 接收湿实验反馈 |
| **P1 · Material Interface Optimizer** | 如何让天然色素稳定结合织物？ | BmCBP 表达纯化、A480 结合、丝绸/棉/聚酯实验 | 更新材料优先级，并形成“蛋白媒染 + 物理保护”固色方向 |
| **P2 · Color & Light Translator** | 如何把目标颜色转化为可执行光输入？ | PhiReX 红光表征；硬件连接光参数、传感、GUI 与远程控制 | 为颜色—光照映射和可监测光控提供实验接口 |

---

## 2. P0 · 从代谢候选到实验决策

### 历史湿实验闭环

Round 0 发酵数据进入 Yeast9/FBA/OptKnock 分析，形成 **307 个候选反应**和 **Plan1–Plan14**。团队结合代谢通路与实验可实施性审核后，确定 `RIB2`、`PAN5`、`MDE1`、`MRI1`、`SPE2`、`FUM1` 六个 Round 1 靶点。

**307 个候选反应 → 14 个 Plan → 6 个实验靶点 → Round 1 → feedback tier**

| Round 1 关键结果 | 数值 | 对下一轮的作用 |
|---|---:|---|
| ΔPAN5，120 h | **约 0.67 mg/L** | 同批 AST 约 0.47 mg/L，进入高优先级证据 |
| ΔMDE1，96 → 120 h | **约 0.42 → 0.36 mg/L** | 进入后期持续性评价 |

### 2026 可执行 FABRIC-AI

Production Optimizer v1.2 在 corrected **235-gene** 共同空间中完成 v1 与 v2A 各 **235/235** 的表型评价，并与 FastKnock 2024、CFSA 2024、OptEnvelope 2023 完成冻结 benchmark。

在 primary condition 中，235 个候选的 guaranteed-production 下界均为 0，系统自动识别 `NON_DISCRIMINATING_GUARANTEED_PRODUCTION`，随后进入预先固定的可实施性排序层。该机制把“当前目标是否真正有区分力”本身纳入实验决策，而不是从数值噪声中制造候选差异。

[查看四方法 Benchmark →](./AI-Computational-Methods.md)

---

## 3. P1 · BmCBP 材料接口

BmCBP 路线从功能分析和分子对接进入湿实验。团队表达并纯化密码子优化的截短 BmCBP，对应 UniProt Q8MYA9 第 68–297 位氨基酸。

| BmCBP 浓度 | 平均 A480 | 测量数 |
|---:|---:|---:|
| 0 mol/L | **2.19190** | 3 |
| `5.5×10^-7 mol/L` | **2.00360** | 3 |
| `1.1×10^-6 mol/L` | **1.84980** | 3 |

平均 A480 随 BmCBP 浓度增加而下降，支持 BmCBP 与虾青素结合。丝绸、棉和聚酯的比较用于更新材料优先级，Human Practices 的产业反馈进一步推动“**BmCBP 蛋白媒染 + 壳聚糖物理保护**”的双层固色方向。

[查看 BmCBP 元件与表征 →](./Parts.md)

---

## 4. P2 · 颜色、光与硬件

PhiReX 红光实验采用约 `630 nm`、`200 μW/cm²`、`2 h pulse`，总培养时间 24 h；培养结束后测量 EGFP Ex/Em `485/528 nm` 和 OD600。R5、R11、R13 三个编号样品在红光条件下均高于无光对照。

硬件将数字图案转换为空间化或时序化光输入，并通过光传感、GUI、4G 通信和远程参数调整连接培养状态与光照控制。

[查看 PhiReX 元件与表征 →](./Parts.md)

---

## 5. 关键成果一览

- **四方法 benchmark**：FastKnock 2024、CFSA 2024、OptEnvelope 2023 与 FABRIC-AI v1.2 完成统一共同模型下的冻结比较；
- **完整 DBTL 证据链**：`307 → 14 → 6 → Round 1 → 实验反馈 → 证据等级更新`；
- **两项正式 AISB26 元件**：AISB26-045-001 PhiReX、AISB26-045-002 截短 BmCBP；
- **P1 / P2 湿实验接口**：BmCBP 色素结合/织物实验与 PhiReX 红光表征；
- **可复现计算流程**：完整 smoke 复现通过，9 项 ranking tests 与 15/15 verification 通过；
- **Human Practices、Education、Collaboration**：专家和产业反馈进入技术设计，并保留跨队伍 Wiki 互证。

---

## 6. 完整 Wiki 导航

| 项目设计与方法 | 实验与验证 | 项目影响与合规 |
|---|---|---|
| [项目描述](./Project-Description.md) | [湿实验](./Wet-Lab-Experiments.md) | [Human Practices](./Human-Practices.md) |
| [系统设计](./Design.md) | [干湿结合验证](./Integrated-Validation.md) | [Education](./Education.md) |
| [AI / 计算方法](./AI-Computational-Methods.md) | [工程化循环](./Engineering-Cycle.md) | [Collaboration](./Collaboration.md) |
| [元件库贡献](./Parts.md) | [可验证性](./Verifiability.md) | [AI 伦理与安全](./AI-Ethics-Safety.md) |
|  |  | [项目贡献标注](./Attributions.md) |

---

## 7. 队伍信息

- **队伍**：BIT-CHINA（045）
- **项目**：光绘酵染
- **赛道**：T3 工业生物制造
- **队长**：赵博研
- **Primary PI**：胡冰，北京理工大学化学与化工学院
- **公开仓库**：本 GitHub / Gitee 项目仓库

成员贡献、外部来源和 AI 使用范围见 [Attributions](./Attributions.md) 与 [AI Ethics & Safety](./AI-Ethics-Safety.md)。

---

<div align="center">

[AI / 计算方法](./AI-Computational-Methods.md) · [干湿结合验证](./Integrated-Validation.md) · [湿实验](./Wet-Lab-Experiments.md) · [Parts](./Parts.md) · [可验证性](./Verifiability.md)

</div>

*最后更新：2026-09-09*