# Verifiability

> 推荐页面 —— 大赛在评审中将"可验证性"视为核心维度之一。
>
> 这一页要回答的问题很简单：**一个我们没见过的、有基本训练的同行，能不能在合理时间内复现我们的关键结果？**

---

## 1. 能验证什么 / What can be verified

我们承诺以下结果可被独立验证：

| 关键结果 | 验证方式 | 预计时间 |
|---|---|---|
| 模型在测试集上的命中率 27% | 跑 `scripts/evaluate.py` | <30 分钟 |
| 候选序列 #5 在 E. coli 中的表达 | 见 Wet-Lab-Experiments §3.1 | 约 2 周 |
| ……

---

## 2. 计算可验证 / Computational

### 2.1 一键复现脚本

```bash
git clone <repo-url>
cd <repo-dir>
docker build -t ai-synbio-team .
docker run --rm -it -v $(pwd):/workspace ai-synbio-team \
    bash -c "python src/ai/scripts/evaluate.py --checkpoint results/checkpoints/best.pt"
```

预期输出（截至 YYYY-MM-DD）：
```
Top-K hit rate: 0.27 ± 0.03
Pearson r:      0.61 ± 0.05
```

### 2.2 环境

- Python 版本：3.11.X
- 关键库版本：见 [`requirements.txt`](../requirements.txt)
- 容器构建：见 [`Dockerfile`](../Dockerfile)

### 2.3 随机性控制

- 训练种子：`{42, 1337, 2024}`
- 评估随机性：所有 bootstrap 采样均使用 `np.random.default_rng(0)`
- GPU 非确定性来源（cuDNN）：通过 `torch.backends.cudnn.deterministic = True` 关闭

### 2.4 数据指纹

| 数据集 | 路径 | SHA-256 |
|---|---|---|
| 训练集 | `data/processed/train.parquet` | `<hash>` |
| 测试集 | `data/processed/test.parquet` | `<hash>` |

---

## 3. 实验可验证 / Experimental

- 完整实验方案：[Wet-Lab-Experiments](./Wet-Lab-Experiments.md)
- 关键试剂批号、仪器型号：见每个实验的"材料"小节
- 重复次数：所有量化结果至少 n=3（生物学重复）

---

## 4. 过程可追溯 / Audit Trail

- **代码版本**：所有关键结果对应的 commit hash 已在 `results/README.md` 中列出
- **数据版本**：通过 DVC / git-lfs / 链接到外部存储 + SHA-256 校验
- **实验记录**：电子实验记录（ELN）链接见 [Wet-Lab-Experiments §6](./Wet-Lab-Experiments.md#6-实验记录--lab-notebook)

---

## 5. 我们做不到完美的地方 / Honest Limitations

> 这一节是为了**坦诚**，不是减分项。

- <例：训练数据中 X 这一类样本只有 3 条，模型在其上表现的方差较大。>
- <例：湿实验中流式细胞仪的型号在 8 月发生过变更，对应数据已经标注。>
- ……

---

## 6. 反馈渠道 / Feedback

如果你尝试复现并遇到问题，请：
- 在仓库内提 Issue（推荐）；
- 或邮件联系：<队长邮箱>

我们会在一周内响应。

---

*最后更新：YYYY-MM-DD*
