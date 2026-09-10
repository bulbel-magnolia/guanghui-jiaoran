# 可验证性与复现

FABRIC-AI 已分别复核候选准备、表型评价和排序，并通过 9 项排序测试、15/15 项最终核验及元件序列一致性检查。下文给出计算复现、元件检查和实验记录的位置。

---

## 1. 可独立验证的关键结果

| 关键结果 | 验证入口 | 保存的结果 |
|---|---|---|
| FABRIC-AI 主分析候选空间 | `prepare` | 235 个基因；600 条阻断反应 |
| v1 葡萄糖主分析条件全空间表型 | `evaluate` | 235/235 完成；0 次求解失败 |
| v2A 乙醇生产阶段敏感性分析 | `evaluate` | 235/235 保留并评价；记录 1 个不可行突变体、32 个无法满足生长下限的评价项 |
| 设计阶段排序 | `rank` | `NON_DISCRIMINATING_GUARANTEED_PRODUCTION`；最终可实施性 Top-6 固定 |
| 排序数值等价修正 | 测试与核验脚本 | 9 项测试通过；15/15 项核验通过 |
| 两项 AISB26 元件文件 | FASTA/GenBank/元数据/表征/图谱 | 文件齐全；FASTA 与 GenBank 逐碱基一致 |

最终结果入口：[`results/fabric_ai/20260908/README.md`](../results/fabric_ai/20260908/README.md)。

---

## 2. 计算复现

### 2.1 环境

验证环境：

- Python `3.12.10`
- COBRApy `0.30.0`
- SciPy `1.17.1`
- swiglpk `5.0.13`
- pandas `2.3.3`
- pytest `8.3.5`
- 求解容差：`1e-7`

冻结依赖文件：[`src/ai/fabric_ai_optimizer/requirements-frozen.txt`](../src/ai/fabric_ai_optimizer/requirements-frozen.txt)。

### 2.2 最短复现

在仓库根目录运行：

```bash
python -m pip install -r src/ai/fabric_ai_optimizer/requirements-frozen.txt
python tools/fabric_ai/reproduction_smoke.py --outdir .reproduction/smoke
```

该复现脚本分别执行：

`prepare → v1 evaluate → v2A evaluate → rank`

分别检查候选集合、GPR 失活反应集合、两组表型指标、排序和 Top-6 是否与保存的结果一致。

### 2.3 分步复现

```bash
python src/ai/fabric_ai_optimizer/fabric_ai_benchmark.py prepare \
  --model models/fabric_ai/common_model.json \
  --condition configs/fabric_ai/v1_glucose_reference.json \
  --outdir .reproduction/prepare \
  --tol 1e-7

python src/ai/fabric_ai_optimizer/fabric_ai_benchmark.py evaluate \
  --model models/fabric_ai/common_model.json \
  --condition configs/fabric_ai/v1_glucose_reference.json \
  --pool results/fabric_ai/20260908/candidate_space.json \
  --outdir .reproduction/v1 \
  --floors 0.1,0.5,0.9 \
  --mutant-growth-fraction 0.95 \
  --tol 1e-7

python src/ai/fabric_ai_optimizer/fabric_ai_benchmark.py evaluate \
  --model models/fabric_ai/common_model.json \
  --condition configs/fabric_ai/v2a_historical_ethanol_stage.json \
  --pool results/fabric_ai/20260908/candidate_space.json \
  --outdir .reproduction/v2a \
  --floors 0.1,0.5,0.9 \
  --mutant-growth-fraction 0.95 \
  --tol 1e-7

python src/ai/fabric_ai_optimizer/fabric_ai_benchmark.py rank \
  --metrics v1_glucose_reference=results/fabric_ai/20260908/v1_candidate_metrics.csv \
            v2a_historical_ethanol_stage=results/fabric_ai/20260908/v2a_candidate_metrics.csv \
  --summaries v1_glucose_reference=results/fabric_ai/20260908/v1_summary.json \
              v2a_historical_ethanol_stage=results/fabric_ai/20260908/v2a_summary.json \
  --primary v1_glucose_reference \
  --outdir .reproduction/rank \
  --top-k 6 \
  --tol 1e-7

python -m pytest tests/fabric_ai/test_ranker.py -q
python tools/fabric_ai/verify_repo_freeze.py --outdir .reproduction/verification
```

完整参数说明见 [`src/ai/fabric_ai_optimizer/README.md`](../src/ai/fabric_ai_optimizer/README.md)。

---

<a id="3-冻结文件指纹"></a>
## 3. 文件 SHA-256 校验值

| 文件 | SHA-256 |
|---|---|
| `models/fabric_ai/common_model.json` | `c7767f92ae22dfd1591ca138e99dc305f477728cffb9eee4eef71d3c162ed684` |
| `results/fabric_ai/20260908/v1_candidate_metrics.csv` | `2176df82d1f75ee7c38990836c3e185c658b2c615635664e800c68063332300d` |
| `results/fabric_ai/20260908/v2a_candidate_metrics.csv` | `e270f2636e8fb0e52702f43e35fc6a7e8aea5acdffa344fb7b09c45d0839e150` |
| `results/fabric_ai/20260908/design_mode_ranking.csv` | `64e7493450278d3b616a66b6dc1d109b7d503d175bc3ffef5c9c36517ec23206` |
| `results/fabric_ai/20260908/design_mode_topk.csv` | `ea440d8e8bc5f96a8bf88b1579c4074f54ef4f4146eed6330058ad0edc62c561` |

最终排序修正包的 SHA-256：`7cea8b7f7c501a7b5130cd069c952686d045c1406cdff06321f0cca8a02b15d7`。

---

## 4. 元件文件完整性

两项新元件均提供 FASTA、GenBank、元数据、表征记录和图谱文件：

### AISB26-045-001 · PhiReX

- FASTA：12,584 bp
- GenBank：12,584 bp
- FASTA / GenBank：逐碱基一致
- 关键表征：红光与无光条件下 EGFP/OD600

### AISB26-045-002 · BmCBP

- FASTA：690 bp
- GenBank：690 bp
- FASTA / GenBank：逐碱基一致
- CDS：`1..690`，与完整序列一致
- 关键表征：A480 与织物/基材实验

元件入口：[`parts/`](../parts/)，表征摘要见 [元件](./Parts.md)。

---

## 5. 实验结果复核入口

湿实验结果以现有实验记录和元件表征文件为准：

- P0 发酵闭环：ΔPAN5、ΔMDE1 及其余四个靶点的 Round 1 记录见 [干湿结合验证](./Integrated-Validation.md)；
- BmCBP：每条件记录 3 次测量，现有文件保存条件均值。逐次原始值未恢复，图中不附误差线；生物学重复数未确认。见 [元件表征](../parts/AISB26-045-002/characterization.md)。
- PhiReX：[元件表征](../parts/AISB26-045-001/characterization.md)分别保留原记录图 12、原记录图 13 的归一化 EGFP/OD600 近似图读值；未恢复逐次原始荧光和 OD600 测量表。

样品身份、重复类型与 n 的确认情况见各元件表征记录。

---

## 6. 过程追溯

2026-09-08 的版本同步提交：

`121a7d6032210c477292097c76073b5a7a676faf`

该提交同步优化程序、共同模型、条件、最终结果和 AISB26 文件。最终同步报告与清单位于：

[`results/evidence/20260908/code_parts_sync/`](../results/evidence/20260908/code_parts_sync/)

其中包括：

- `README_最终仓库同步结果.md`
- `final_repo_manifest.csv`
- `source_sync_manifest.csv`
- `parts_integrity_check.csv`
- `reproduction_smoke_test.log`
- `current_ranking_verification.json`

最终同步检查结果：14/14 Wiki 页面存在，10/10 元件文件齐全，109 个 Markdown/HTML 相对链接存在。

---

<a id="7-提交修复版复核"></a>
## 7. 更新后的程序与记录核验

```bash
python tools/fabric_ai/validate_submission_fixes.py --outdir .reproduction/submission-fixes-check
```

该脚本分别运行 9 项原有排序测试、40 项输入校验测试、19 项实验反馈测试、15/15 项最终核验，以及元件一致性检查和实验反馈重算。脚本还重新执行公共排序入口，与已保存的 235 行排序及六行 Top-6 逐项比较数值和用途标签。本项验证范围为排序、实验反馈和文件检查，不包含 235×2 代谢表型重算。

PhiReX 的 FASTA 与 GenBank 序列一致；四个边界未定的区段按 `misc_feature` 保存，两个保留 CDS 通过阅读框检查。[注释状态与原始导出](../results/evidence/20260909/phirex_annotation/README.md)。

[本轮验证结果](../results/evidence/20260909/validation/verification.json) · [实验反馈前后数值](../results/evidence/20260909/C3_1_QUANTITATIVE_ITERATION.md)。

## 8. 当前评价范围

FABRIC-AI 当前公开基准比较以单基因敲除和固定的共同代谢模型为核心任务。v1 是标准主分析条件，v2A 是生产阶段敏感性条件，v2B 只用于营养可获得性机制诊断。设计阶段的排序不使用 Round 1 的 PAN5/MDE1 实验结果；实验结果在设计结果固定后进入实验反馈阶段更新证据等级。

公开基线比较与实验反馈分别保存输入和结果。

---

*最后更新：2026-09-10（文字修订）*
