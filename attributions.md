# Attributions · 项目归属与贡献

## 1. 项目信息

- **队伍**：BIT-CHINA（045）
- **项目**：光绘酵染
- **赛道**：T3 工业生物制造
- **队长**：赵博研
- **Primary PI**：胡冰，北京理工大学化学与化工学院

---

## 2. 工作沿革

本项目延续 BIT-China 团队在 2025 年形成的 FABRIC 实验体系，使用团队此前获得的发酵、光控表达、色素合成、BmCBP 固色、硬件及 Human Practices 记录。2026 年 mAI + 合成生物创新大赛期间，团队完成数据结构化、FABRIC-AI 闭环重构、共同模型 benchmark、近期公开基线复现、反馈规则、代码实现、自动测试、元件提交与赛事材料整合。

三队共同编写可持续发展教育手册的工作发生于 2025 年 8–9 月，作为本届项目准备和内容形成过程中的 Collaboration 提交。两个元件保留 2025 年创建记录，并于 2026 年首次按 AISB26 格式正式提交。

---

## 3. 团队成员贡献

| 人员 | 身份 | 贡献 |
|---|---|---|
| **赵博研** | 队长、学生成员 | 整体统筹；FABRIC-AI 技术主线整合；数据与证据体系；benchmark 任务组织；代码仓库和发布管理；评审表、项目报告、展示视频和材料提交 |
| **徐士宸** | 学生成员 | 湿实验体系与实验记录复核；参与色素合成和光控表达；整理构建、PCR、测序和荧光表征证据；参与安全与湿实验页面审核 |
| **张意帆** | 学生成员 | 项目概念、硬件、软件可视化、Wiki 编排和 Human Practices 材料整理 |
| **范运涵** | 学生成员 | BmCBP、蛋白媒染、染色和材料界面实验资料整理；核对实验条件、对照和图表表述 |
| **宋吉羽** | 学生成员 | GSMM、OptKnock、Round 0/Round 1 与 feedback 数据整理；代码测试、结果复核和可复现性检查 |
| **慕金贝** | 学生成员 | 文献、遗传回路和引物设计相关工作；模型推进；元件、Human Practices、Education、Collaboration 和贡献材料整理 |
| **胡冰** | Primary PI | 项目方向、实验与生物安全指导、学术内容审核和最终材料批准 |

---

## 4. 资料与来源归属

| 内容 | 来源与时间 | 本届工作 |
|---|---|---|
| 发酵、光控表达、色素合成、BmCBP、染色与硬件记录 | BIT-China 2025 团队工作 | 结构化、证据分级、叙事整合与复现检查 |
| Yeast9/FBA/OptKnock 页面记录 | BIT-China 2025 项目记录 | 恢复 307→14→6 主链并接入 Round 1 反馈 |
| Yeast-GEM v9.1.0 | SysBioChalmers/yeast-GEM | 构建并审计共同代谢模型 |
| FastKnock 2024 | Hassani et al. 与固定公开代码 | corrected 235-gene replay、flux audit 与冻结结果 |
| CFSA 2024 | van Rosmalen et al. 与固定公开代码 | 3 场景采样、14 个映射 KO 与独立评价 |
| OptEnvelope 2023 | Motamedian et al. 与固定公开代码 | corrected GLPK compatibility run、11 个 target points 与 transfer audit |
| FABRIC-AI Production Optimizer v1.2 | BIT-CHINA 2026 | 235-gene 全空间表型评价、多条件分析、non-discrimination gate、确定性排序与测试 |
| Human Practices | BIT-China 2025 Wiki 归档 | 提取设计影响路径并连接 P0/P1/P2 技术叙事 |
| Education 与 Collaboration | BIT-China、NUDT-CHINA、SCU-China，2025 年 8–9 月 | 作为本届项目准备和内容形成过程中的合作成果提交 |
| AISB26-045-001、AISB26-045-002 | 本团队 2025 年创建；2026 年提交 | 首次按 AISB26 格式正式提交并计入本届元件数量 |

---

## 5. AI 辅助范围

完整声明见 [`AI-USE-DISCLOSURE.md`](./AI-USE-DISCLOSURE.md)。ChatGPT、Codex 等工具用于资料整理、代码建议、测试设计、一致性检查和材料起草。AI 未生成实验数据，未独立决定或执行湿实验，也未直接设计或修改两个提交元件的序列。所有技术解释、代码变更和公开材料由团队成员及 Primary PI 审核确认。

---

## 6. 许可

- 代码：MIT License；
- 团队原创文档、数据、图表和图片：CC BY 4.0；
- Registry 导出的元件序列、GenBank 及衍生说明：CC BY-SA 4.0；
- 第三方内容：沿用原始许可。

---

*最后更新：2026-09-08*