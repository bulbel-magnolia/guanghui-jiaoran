# AI Ethics & Safety · AI 伦理与安全

FABRIC-AI 的计算结果用于支持研究决策，所有实验选择、数据解释和公开结论由团队成员及 Primary PI 审核。ChatGPT、Codex 等工具用于既有资料整理、代码草拟与重构建议、测试设计、仓库一致性检查和赛事材料结构化；实验数据均来自团队实验记录。

---

## 1. AI 使用范围

AI 工具在本项目中的主要用途包括：

- 文献与既有实验材料整理；
- 代码结构建议、测试设计与错误排查；
- 共同模型和 benchmark 结果的一致性审计；
- Wiki、评审表和项目材料的结构化起草；
- 历史文件与当前提交版本之间的迁移检查。

AI 未生成实验数据，也未独立决定或执行湿实验。两个 AISB26 提交元件由团队创建，AISB26 提交过程中序列未由 AI 修改。

完整披露见 [`AI-USE-DISCLOSURE.md`](../AI-USE-DISCLOSURE.md)。

---

## 2. 决策责任与人工审核

P0 Production Optimizer 的模型输出先形成候选表，再由团队人工审核后决定是否进入实验。历史主闭环中，Round 0 数据和 Yeast9/FBA/OptKnock 分析形成候选空间，团队选择 6 个靶点开展 Round 1；实验结果随后进入反馈规则。

2026 Design mode 进一步把计算和后验实验反馈分离：

- Design mode 不读取 PAN5/MDE1 的历史 Round 1 结果；
- 公开 baseline 排序在冻结的共同模型和候选空间中完成；
- Learn mode 在 Design 结果冻结后读取湿实验反馈，更新证据等级与下一轮动作。

这一结构保证模型比较、实验反馈和最终研究决策均有明确责任主体和数据边界。

---

## 3. 数据来源与完整性

| 数据类型 | 来源 | 本届使用方式 |
|---|---|---|
| Round 0 / Round 1 发酵、BmCBP、PhiReX、染色与硬件记录 | BIT-China 2025 团队实验 | 结构化、证据分级、闭环和模型输入 |
| Yeast-GEM v9.1.0 | SysBioChalmers/yeast-GEM | 共同代谢模型底座 |
| FastKnock 2024 | 作者公开代码 | 近期公开 baseline |
| CFSA 2024 | 作者公开代码 | 近期公开 baseline |
| OptEnvelope 2023 | 作者公开代码 | 近期公开 baseline |
| Human Practices / Education / Collaboration | 团队公开 Wiki 与对方 Wiki | 设计影响和社会证据 |

项目不处理临床、身份证明或其他个人敏感生物医学数据。公众问卷和访谈材料用于汇总性 Human Practices 分析，不进入 Production Optimizer 的单基因排序。

---

## 4. 模型输出的解释边界

FABRIC-AI 使用约束代谢模型评价候选，不把模型输出直接等同于实验产量。系统分别记录 guaranteed-production 下界、理论产能上界、生长保持和工程可实施性。

当前 235-gene primary task 中全部 GCP 与 Pmin95 为 0，系统据此输出 `NON_DISCRIMINATING_GUARANTEED_PRODUCTION`，并把后续 Top-6 明确标记为 `SECONDARY_FEASIBILITY_ORDER_ONLY`。这一机制将“模型目标没有区分度”作为正式输出，避免利用求解器数值噪声制造候选差异。

排序前还在原始通量单位应用 `1e-7` 数值等价规则，所有排序修正均保存测试与验证记录。

---

## 5. 生物安全

团队按实验室 BSL-2 管理要求开展相关实验，并执行个人防护、样品标识、废弃物处理和实验区域管理。实验内容围绕工程酵母、蛋白表达、天然色素和材料测试，不涉及病原体增强、毒力设计或面向特定人群的有害生物功能。

当前公开 Production Optimizer 不生成新的生物序列，也不自动下发菌株构建、培养或实验设备命令。软件输出作为研究建议进入人工审核环节。

---

## 6. 双重用途与信息安全

FABRIC 项目的核心输出是色素生产、固色和光控表达设计。公开材料重点保存可复现的模型设定、实验结果和审计记录，同时避免在仓库中保存密钥、令牌、个人敏感信息和内部绝对路径。

模型与代码发布遵循以下原则：

- 明确第三方模型、代码和数据来源；
- 保存版本、commit、SHA-256 和执行状态；
- 历史无效/中间结果单独归档，不提升为正式结论；
- AI 辅助范围在 Attributions 和 AI 使用声明中公开。

---

## 7. 许可与贡献归属

- 代码：MIT License；
- 团队原创文档、数据、图表和图片：CC BY 4.0；
- Registry 导出的元件序列、GenBank 及衍生说明：CC BY-SA 4.0；
- 第三方内容沿用其原始许可。

团队成员贡献和外部来源见 [Attributions](./Attributions.md)。

---

## 8. 安全证据入口

- [`AI-USE-DISCLOSURE.md`](../AI-USE-DISCLOSURE.md)
- [`attributions.md`](../attributions.md)
- [`safety/`](../safety/)
- [可验证性](./Verifiability.md)
- [干湿结合验证](./Integrated-Validation.md)

---

*最后更新：2026-09-08*