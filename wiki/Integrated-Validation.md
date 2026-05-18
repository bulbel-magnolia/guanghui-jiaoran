# Integrated Validation · 干湿结合验证

> 推荐页面 —— 大赛金牌的硬性参考之一是"干湿结合的闭环验证"。这一页就是你们闭环故事的主舞台。

---

## 1. 我们的 DBTL 闭环 / The DBTL Loop

```
Design  →  Build  →  Test  →  Learn
   ↑___________________________|
```

- **Design**：模型基于 X 输入生成了 N 个候选 → `results/candidates_v1.csv`
- **Build**：选出 K 个候选进入湿实验 → 详见 [Wet-Lab §3](./Wet-Lab-Experiments.md)
- **Test**：实验得到的关键指标 → `data/processed/wet_feedback_v1.csv`
- **Learn**：实验数据反馈给模型，得到 v2 → 见 §3

## 2. 第一轮闭环 / Loop #1

- 时间：YYYY-MM 至 YYYY-MM
- 候选数：N
- 实测命中率：xx%
- 关键发现：…
- 反馈到模型的数据点：M 条

## 3. 第二轮闭环 / Loop #2（如适用）

- 命中率提升：xx% → yy%
- 我们学到了什么：…

## 4. 局限与未来 / Limitations

诚实写出闭环的不足（实验吞吐量、模型外推能力等）。

---

*最后更新：YYYY-MM-DD*
