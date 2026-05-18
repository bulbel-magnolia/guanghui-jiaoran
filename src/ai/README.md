# src/ai · AI / 计算代码

```
src/ai/
├── README.md          # 本文件
├── models/            # 模型定义（PyTorch / TF）
├── data/              # 数据加载与预处理
└── scripts/           # 入口脚本：train / inference / evaluate
```

## 入口脚本约定

| 脚本 | 用途 | 典型用法 |
|---|---|---|
| `scripts/train.py` | 训练 | `python scripts/train.py --config configs/baseline.yaml --seed 42` |
| `scripts/inference.py` | 推理 / 生成候选 | `python scripts/inference.py --checkpoint results/checkpoints/best.pt` |
| `scripts/evaluate.py` | 在测试集上评估 + 基线对比 | `python scripts/evaluate.py --eval-set data/processed/test.csv` |

## 配置管理

- 推荐使用 [Hydra](https://hydra.cc/) 或 OmegaConf；
- 把配置文件放在 `configs/` 而不是写死在代码里——这是可验证性的关键。

## 单元测试

把简单单元测试放在 `tests/`（与 src 同级），CI 自动跑：
```bash
pytest tests/ -v
```
