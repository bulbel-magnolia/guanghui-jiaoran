# 光绘酵染 · FABRIC-AI

**BIT-CHINA（045）｜T3 工业生物制造｜2026 mAI + 合成生物创新大赛**

光绘酵染围绕生物色素“**产得出、留得住、可编程**”构建 FABRIC 系统：工程化酵母负责色素生产，BmCBP 连接色素与织物界面，光控表达和数字投光负责颜色与图案输出。FABRIC-AI 将代谢模型、材料实验、光控数据和湿实验反馈组织为 P0/P1/P2 三个相互衔接的决策模块。

---

## 1. 项目架构

| 模块 | 核心问题 | 当前结果 |
|---|---|---|
| **P0 Production Optimizer** | 哪些代谢干预值得进入实验？ | 完成 corrected 235-gene 全空间表型评价；与 FastKnock、CFSA、OptEnvelope 进行近三年基线比较；历史 Round 1 形成 307→14→6→实验反馈闭环 |
| **P1 Material Interface Optimizer** | 如何让天然色素稳定结合织物？ | BmCBP 完成表达纯化、A480 结合与跨基材实验；丝绸为当前优先基材 |
| **P2 Color & Light Translator** | 如何把目标颜色转化为可执行光输入？ | PhiReX 在约 630 nm、200 μW/cm²、2 h pulse 下完成红光表征；硬件连接图案、光参数、传感和远程控制 |

---

## 2. P0：从代谢候选到实验决策

Round 0 发酵数据进入 Yeast9/FBA/OptKnock 分析，历史记录形成 **307 个候选反应**和 **Plan1–Plan14**。团队结合代谢通路与实验可实施性审核后，确定 `RIB2`、`PAN5`、`MDE1`、`MRI1`、`SPE2`、`FUM1` 六个 Round 1 靶点。

Round 1 中，ΔPAN5 120 h 约 `0.67 mg/L`，同批 AST 约 `0.47 mg/L`；ΔMDE1 在 96–120 h 由约 `0.42 mg/L` 降至 `0.36 mg/L`。实验结果进入版本化 feedback rules，更新终点产量、持续性、生物量和可实施性证据等级。

2026 可执行 Production Optimizer v1.2 在 corrected **235-gene** 共同空间中完成 v1 与 v2A 各 **235/235** 的表型评价，并与 FastKnock 2024、CFSA 2024、OptEnvelope 2023 完成冻结 benchmark。系统识别出当前 guaranteed-production 指标对全部 primary candidates 均失去区分能力，并进入预先固定的可实施性决策层。

---

## 3. P1：BmCBP 材料接口

BmCBP 路线从功能分析和分子对接进入湿实验。团队表达并纯化密码子优化的截短 BmCBP，对应 UniProt Q8MYA9 第 68–297 位氨基酸。三个 BmCBP 浓度条件各进行 3 次测量，平均 A480 依次为 `2.19190`、`2.00360`、`1.84980`，随 BmCBP 浓度增加而下降。

丝绸、棉和聚酯的比较用于更新材料优先级。Human Practices 的产业反馈进一步推动“**BmCBP 蛋白媒染 + 壳聚糖物理保护**”的双层固色方向。

---

## 4. P2：颜色、光与硬件

PhiReX 红光实验采用约 `630 nm`、`200 μW/cm²`、`2 h pulse`，总培养时间 24 h；培养结束后测量 EGFP Ex/Em `485/528 nm` 和 OD600。R5、R11、R13 三个编号样品在红光条件下均高于无光对照。

硬件将数字图案转换为空间化或时序化光输入，并通过光传感、GUI、4G 通信和远程参数调整连接培养状态与光照控制。

---

## 5. 关键成果

- **四方法 benchmark**：FastKnock 2024、CFSA 2024、OptEnvelope 2023 与 FABRIC-AI v1.2 在统一共同模型下完成冻结比较；
- **完整 Design–Build–Test–Learn 闭环**：307 候选反应 → 14 个 Plan → 6 个 Round 1 靶点 → 实验反馈 → 证据等级更新；
- **两项正式 AISB26 元件**：AISB26-045-001 PhiReX、AISB26-045-002 截短 BmCBP；
- **材料与光控实验**：BmCBP 色素结合/织物结果与 PhiReX 红光表征；
- **Human Practices、Education 与 Collaboration**：专家与产业反馈直接进入技术设计，联合教育手册具有对方 Wiki 互证。

---

## 6. Wiki 导航

### 核心页面

- [项目描述](./Project-Description.md)
- [系统设计](./Design.md)
- [AI / 计算方法](./AI-Computational-Methods.md)
- [湿实验](./Wet-Lab-Experiments.md)
- [干湿结合验证](./Integrated-Validation.md)
- [工程化循环](./Engineering-Cycle.md)
- [AI 伦理与安全](./AI-Ethics-Safety.md)
- [可验证性](./Verifiability.md)
- [元件库贡献](./Parts.md)
- [项目贡献标注](./Attributions.md)

### 项目影响

- [Human Practices](./Human-Practices.md)
- [Education](./Education.md)
- [Collaboration](./Collaboration.md)

---

## 7. 队伍信息

- **队伍**：BIT-CHINA（045）
- **项目**：光绘酵染
- **赛道**：T3 工业生物制造
- **队长**：赵博研
- **Primary PI**：胡冰，北京理工大学化学与化工学院
- **公开仓库**：本 GitHub/Gitee 项目仓库

成员贡献、外部来源和 AI 使用范围见 [Attributions](./Attributions.md) 与 [AI Ethics & Safety](./AI-Ethics-Safety.md)。

---

*最后更新：2026-09-08*