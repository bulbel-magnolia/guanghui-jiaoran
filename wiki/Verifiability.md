# 可验证性与复现

本页说明如何独立复核 FABRIC-AI 的关键计算结果、元件文件完整性和实验数据入口。2026 冻结版本已经完成完整 prepare → evaluate → rank 复现，并通过 9 项 ranking tests、15/15 最终 verification 和 parts 序列一致性检查。

---

## 1. 可独立验证的关键结果

| 关键结果 | 验证入口 | 冻结结果 |
|---|---|---|
| FABRIC-AI primary candidate space | `prepare` | 235 genes；600 blocked reactions |
| v1 glucose reference 全空间表型 | `evaluate` | 235/235 完成；0 solver failure |
| v2A ethanol-stage sensitivity | `evaluate` | 235/235 保留并评价；1 个不可行 mutant、32 个 growth-floor infeasible cells 如实记录 |
| Design-mode 排序 | `rank` | `NON_DISCRIMINATING_GUARANTEED_PRODUCTION`；最终 secondary Top-6 固定 |
| ranking 数值等价修正 | pytest + verification | 9 项测试通过；15/15 verification 通过 |
| 两项 AISB26 元件文件 | FASTA/GenBank/metadata/characterization/map | 文件齐全；FASTA 与 GenBank 逐碱基一致 |

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
- solver tolerance：`1e-7`

冻结依赖文件：[`src/ai/fabric_ai_optimizer/requirements-frozen.txt`](../src/ai/fabric_ai_optimizer/requirements-frozen.txt)。

### 2.2 最短复现

在仓库根目录运行：

```bash
python -m pip install -r src/ai/fabric_ai_optimizer/requirements-frozen.txt
python tools/fabric_ai/reproduction_smoke.py --outdir .reproduction/smoke
```

该 smoke 流程实际执行：

`prepare → v1 evaluate → v2A evaluate → rank`

并检查 candidate space、GPR footprint、两组 metrics、最终 ranking 和 Top-6 与冻结版本一致。

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

## 3. 冻结文件指纹

| 文件 | SHA-256 |
|---|---|
| `models/fabric_ai/common_model.json` | `c7767f92ae22dfd1591ca138e99dc305f477728cffb9eee4eef71d3c162ed684` |
| `results/fabric_ai/20260908/v1_candidate_metrics.csv` | `2176df82d1f75ee7c38990836c3e185c658b2c615635664e800c68063332300d` |
| `results/fabric_ai/20260908/v2a_candidate_metrics.csv` | `e270f2636e8fb0e52702f43e35fc6a7e8aea5acdffa344fb7b09c45d0839e150` |
| `results/fabric_ai/20260908/design_mode_ranking.csv` | `64e7493450278d3b616a66b6dc1d109b7d503d175bc3ffef5c9c36517ec23206` |
| `results/fabric_ai/20260908/design_mode_topk.csv` | `ea440d8e8bc5f96a8bf88b1579c4074f54ef4f4146eed6330058ad0edc62c561` |

最终 ranking correction ZIP SHA-256：`7cea8b7f7c501a7b5130cd069c952686d045c1406cdff06321f0cca8a02b15d7`。

---

## 4. 元件文件完整性

两项新元件均提供 FASTA、GenBank、metadata、characterization 和 map 文件：

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

元件入口：[`parts/`](../parts/)，表征摘要见 [Parts](./Parts.md)。

---

## 5. 实验结果复核入口

湿实验结果以现有实验记录和元件表征文件为准：

- P0 发酵闭环：ΔPAN5、ΔMDE1 及其余四个靶点的 Round 1 记录见 [干湿结合验证](./Integrated-Validation.md)；
- BmCBP：三档浓度条件各记录 3 次测量，A480 原始值与平均值见元件表征；
- PhiReX：R5、R11、R13 的红光 / 无光 EGFP 和 OD600 记录见元件表征。

重复类型、样品身份和 n 均按对应原始记录表述，不将“3 次测量”自动等同于“3 个生物学重复”。

---

## 6. 过程追溯

2026-09-08 冻结同步提交：

`121a7d6032210c477292097c76073b5a7a676faf`

该提交同步冻结 optimizer、共同模型、条件、最终结果和 AISB26 文件。最终同步报告与清单位于：

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

## 7. 当前评价范围

FABRIC-AI 当前公开 benchmark 以单基因敲除和冻结的共同代谢模型为核心任务。v1 是 primary standardized reference，v2A 是生产阶段敏感性条件，v2B 只用于营养可获得性机制诊断。Design mode 的排序不使用 Round 1 的 PAN5/MDE1 实验结果；实验结果在 Design mode 冻结后进入 Learn mode 更新证据等级。

这一区分保证公开基线比较、实验反馈和下一轮设计分别留有独立证据路径。

---

*最后更新：2026-09-08*
