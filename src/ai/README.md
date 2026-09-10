# AI / 计算代码

当前可执行程序位于 [fabric_ai_optimizer](fabric_ai_optimizer/README.md)。

| 程序 | 功能 |
|---|---|
| [fabric_ai_基准比较.py](fabric_ai_optimizer/fabric_ai_benchmark.py) | 准备候选、评价表型和排序 |
| [learn_mode.py](fabric_ai_optimizer/learn_mode.py) | 读取历史实验数据，生成反馈前后评价 |
| [核验脚本](../../tools/fabric_ai/verify_repo_freeze.py) | 检查保存的排序与来源一致性 |
| [输入与结果验证](../../tools/fabric_ai/validate_submission_fixes.py) | 排序、实验反馈和元件检查 |

运行环境与命令见 [使用说明](fabric_ai_optimizer/README.md)。相关测试保存在 [tests/fabric_ai](../../tests/fabric_ai/)；模型和实验反馈分别使用各自的数据。
