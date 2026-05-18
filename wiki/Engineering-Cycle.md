# Engineering Cycle · 工程化循环

> 这一页与 Integrated Validation 互为补充——后者强调"AI 与实验如何对话"，本页强调"作为一个工程项目，我们如何迭代"。

---

## 1. 迭代历程 / Iteration Log

| 版本 | 时间 | 关键变更 | 触发原因 |
|---|---|---|---|
| v0.1 | YYYY-MM | 最早能跑通的端到端管线 | 初稿 |
| v0.2 | YYYY-MM | 替换为新的 encoder | v0.1 在长序列上崩 |
| v1.0 | YYYY-MM | 引入主动学习循环 | 标注预算有限 |
| | | | |

## 2. 工程化清单 / Engineering Checklist

- [ ] 代码可一键复现
- [ ] CI / CD 自动跑测试
- [ ] 模型推理脚本 < 1 分钟启动
- [ ] 标注流程文档化
- [ ] 数据版本控制（DVC / Git LFS）
- [ ] 关键超参数有 ablation

---

*最后更新：YYYY-MM-DD*
