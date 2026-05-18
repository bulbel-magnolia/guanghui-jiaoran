# AI / Computational Methods

> ⭐ **必设页面** —— 评审委员会理解项目 AI / 计算工作的主要依据。
>
> 写作建议：**逻辑链 > 工具堆砌**。让评委读完这一页能回答三个问题：
> 1. 你们要 AI 解决什么具体问题？
> 2. 你们的方法和已有方案的差异在哪里？
> 3. 怎么知道方法真的有效？

---

## 1. 任务定义 / Task Formulation

**输入**：（例：氨基酸序列；目标功能描述；目标蛋白结构）

**输出**：（例：候选 AMP 序列；预测的结合亲和力；推荐的实验条件）

**评估标准**：（例：MIC ≤ 8 μg/mL 的命中率、对照已发表方法的提升幅度）

---

## 2. 模型架构 / Model Architecture

### 2.1 整体框架

> 一张系统框图，标清楚每个模块的输入输出。

```
[在这里嵌入架构图：../results/figures/architecture.png]
```

### 2.2 关键组件

| 组件 | 类型 | 是否原创 | 备注 |
|---|---|---|---|
| Encoder | <例：ESM-2 frozen> | 否（站在巨人肩膀上） | 见 attributions.md |
| Decoder | <例：自研 Transformer 解码器> | 是 | 6 层、d=512、注意力头数 8 |
| 评分头 | <例：MLP> | 是 | 在自有数据集上从零训练 |

### 2.3 关键超参数

| 参数 | 值 |
|---|---|
| 学习率 | 1e-4 |
| Batch size | 32 |
| 训练轮数 | 50 |
| 优化器 | AdamW (β₁=0.9, β₂=0.999, weight_decay=0.01) |
| Scheduler | cosine annealing, warmup 1 000 步 |
| 随机种子 | 42 / 1337 / 2024（三个种子取均值） |

### 2.4 计算资源

- 训练硬件：例如 1× A100 40GB
- 训练时长：约 X 小时
- 推理硬件：例如 RTX 3090 即可

---

## 3. 数据 / Data

### 3.1 数据来源与规模

| 数据集 | 用途 | 样本量 | 来源 | 授权 |
|---|---|---|---|---|
| <例：UniRef50> | 预训练（继承自 ESM） | — | UniProt | CC-BY 4.0 |
| <例：APD3> | 微调正样本 | ~3 000 条 | aps.unmc.edu | 学术免费 |
| <例：自产 MIC 数据> | 评估集 | 120 条 | 本队湿实验 | 本项目原创 |

### 3.2 数据划分

- 训练 / 验证 / 测试 = X / Y / Z%
- 划分依据：（例："按序列同源性聚类后划分，避免训练-测试同源泄漏"）

### 3.3 数据预处理

简要说明 + 链接到 `src/ai/data/` 中的脚本。

---

## 4. 训练与评估 / Training & Evaluation

### 4.1 损失函数

（写出公式并简要解释为何选这种损失）

### 4.2 评估指标

| 指标 | 定义 | 与项目目标的关系 |
|---|---|---|
| 命中率 @ Top-K | (实验验证 MIC ≤ 阈值) / Top-K 候选数 | 直接反映"AI 设计 → 真有效"的端到端能力 |
| Pearson r | 预测 vs 实测 MIC 的相关性 | 反映模型外推能力 |
| ……

### 4.3 基线对比 ⭐

> 大赛要求：**基线须使用近三年（2023 年及以后）发表 / 发布的主流模型**。详见赛事细则 §5.1。

| # | 基线 | 年份 | 来源 | 关键结果 |
|---|---|---|---|---|
| 1 | <例：HydrAMP> | 2023 | DOI: ... | 命中率 12% |
| 2 | <例：AMPGen-2024> | 2024 | DOI: ... | 命中率 18% |
| 3 | **本工作** | 2026 | — | 命中率 **27%** |

> 若因任务限制必须使用更老的基线，请在此处单独说明理由并附近期相关工作综述。

### 4.4 不确定性与失败模式

- 我们如何报告置信区间？（例：自助法 1 000 次重采样的 95% CI）
- 模型在什么类型的输入上失败？（请举例）

---

## 5. 复现指南 / Reproducibility

```bash
# 一键训练
python src/ai/scripts/train.py --config configs/baseline.yaml --seed 42

# 一键评估
python src/ai/scripts/evaluate.py --checkpoint results/checkpoints/best.pt
```

- 环境：见 [`requirements.txt`](../requirements.txt) 与 [`Dockerfile`](../Dockerfile)
- 完整复现指南：见 [Verifiability](./Verifiability.md)

---

## 6. 与湿实验的衔接 / Coupling with the Wet Lab

> 评审重点之一：**AI 的预测如何被湿实验检验？实验结果又如何反哺模型？**

请在 [Integrated Validation](./Integrated-Validation.md) 页面详细描述这一闭环；本页只列出关键接口：

- 模型输出 → 湿实验候选清单：`results/candidates_v1.csv`
- 湿实验结果 → 模型训练数据：`data/processed/wet_feedback_v1.csv`

---

## 7. 局限与未来工作 / Limitations & Future Work

诚实写出当前方法的局限。这是高质量项目的标志，不是减分项。

---

*最后更新：YYYY-MM-DD*
