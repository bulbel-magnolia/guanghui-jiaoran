# FABRIC 项目 DBTL 与 Human Practices 证据摘要

状态：`EVIDENCE_SUMMARY_20260908`

本文件汇总已核对的项目证据，用于支撑 `wiki/Integrated-Validation.md` 与 `wiki/Human-Practices.md`。原始 2025 FABRIC Wiki 与 2026 V0.8 结构化材料分别保留其时间边界；本页只提取可直接核查的事实与设计变化。

## 1. P0：FABRIC-AI 生产优化主闭环

Round 0 发酵记录与 Yeast9/FBA/OptKnock 分析形成候选空间，历史页面记录 307 个候选反应和 Plan1–Plan14。团队结合代谢通路与文献证据完成人工审核，选择 `RIB2`、`PAN5`、`MDE1`、`MRI1`、`SPE2`、`FUM1` 六个基因进入 Round 1。

Round 1 中，ΔPAN5 与 ΔMDE1 获得定量发酵结果：

- ΔPAN5：120 h 约 `0.67 mg/L`；同批 AST 约 `0.47 mg/L`，提升约 `42.6%`；
- ΔMDE1：96–120 h 由约 `0.42 mg/L` 下降至 `0.36 mg/L`；
- 其余四个靶点保留本轮构建或培养可实施性记录。

版本化 feedback rules 使用四类项目指标：

- `terminal_yield_score`：120 h 同批次终点产量；
- `persistence_score`：96–120 h 产量变化；
- `biomass_score`：120 h 生物量保持；
- `feasibility_score`：本轮构建或培养可实施性。

反馈程序输出：PAN5 为 Tier 1、MDE1 为 Tier 2，RIB2/MRI1/SPE2/FUM1 为 Tier 3，并保存判定轨迹与下一轮动作。144 组阈值组合中，六个靶点的证据等级保持稳定。

## 2. P1：BmCBP 路线由计算推演转向实验验证

2025 FABRIC Human Practices 页面记录：团队先以 AutoDock 对 BmCBP 与色素进行分子对接，并尝试使用 AlphaFold 等工具模拟 BmCBP 与丝蛋白的结合。丝蛋白结构大且不规则，使该路线难以形成可靠判断。Yu Yang 老师建议将验证重点转入湿实验。

团队随后完成 BmCBP 异源表达与纯化，并开展色素结合和织物实验。2026 V0.8 结构化记录中，每个 BmCBP 浓度条件进行 3 次测量，0、`5.5×10^-7`、`1.1×10^-6 mol/L` 三个条件的平均 A480 分别为 `2.19190`、`2.00360`、`1.84980`。丝绸、棉和聚酯的后续比较被用于更新基材优先级。

产业交流进一步提出壳聚糖保护层思路，项目由此形成“蛋白媒染 + 物理保护”的双层固色设计方向。

## 3. P2：光控系统的工程化反馈

项目 Human Practices 与硬件记录显示，团队在硬件迭代中吸收机械、自动化和 iGEM 团队交流意见：

- 通过材料与结构比较优化支架和遮光结构；
- 受 CCiC 中远程监测方案启发，引入 4G 通信与远程参数调整；
- 将光传感、GUI 和远程控制纳入系统接口；
- PhiReX 表征记录约 `630 nm`、`200 μW/cm²`、`2 h pulse`、`24 h` 总培养时间，并以 EGFP/OD600 进行归一化；R5、R11、R13 在红光条件下均高于无光对照。

## 4. Human Practices 对技术设计的直接影响

| 外部输入 | 形成的技术变化 |
|---|---|
| 纺织与产业专家强调通用性、经济性、过程稳定和规模化风险 | 将可实施性、基材差异、设备稳定性纳入评价 |
| BmCBP—丝蛋白纯计算路线难以形成可靠判断 | 转向 BmCBP 表达纯化、A480/游离色素与织物实验 |
| 产业交流提出色素保护需求 | 增加壳聚糖物理保护层，形成双层固色方向 |
| CCiC 与自动化/机械交流 | 引入光传感、4G、GUI 与远程参数调整 |
| 391 份有效问卷 | 明确公众对环境价值、皮肤刺激风险、第三方检测和公开实验数据的关注重点 |
| 非遗蓝染与传统染色调研 | 将清洁生物过程、丝绸基材和生物纹理表达纳入项目设计 |

## 5. 公开来源

- BIT-China 2025 Human Practices：https://2025.igem.wiki/bit-china/human-practices
- BIT-China 2025 Hardware：https://2025.igem.wiki/bit-china/hardware
- BIT-China 2025 Notebook：https://2025.igem.wiki/bit-china/notebook

本页所列调研与交流发生于 2025 FABRIC 项目阶段；2026 赛事版本沿用已经形成的设计决策，并将其映射到 P0 Production Optimizer、P1 Material Interface Optimizer 与 P2 Color & Light Translator。