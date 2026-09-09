# 光绘酵染 · FABRIC-AI

本项目面向纺织印染中的染料合成、固色和图案控制三个环节，构建“工程化酵母产天然色素 + 光响应调控 + BmCBP 蛋白固色 + 计算模型辅助菌株设计”的一体化方案。2026 赛季重点完成了 FABRIC-AI Production Optimizer 的可执行版本、近三年公开基线比较、两项新 DNA 元件提交，以及 Design–Build–Test–Learn（DBTL）证据链整理。

## 1. 项目核心模块

### 1.1 FABRIC-AI：从候选搜索到实验决策

FABRIC-AI Production Optimizer v1.2 在冻结的共同酵母代谢模型上建立 235 个可实施单基因敲除候选空间，并对全部候选完成生长—生产表型评价。系统使用标准葡萄糖条件作为 primary condition，同时对相同 235-gene 空间在历史乙醇生产阶段条件下进行敏感性评价。

本轮四方法 benchmark 使用 FastKnock 2024、CFSA 2024、OptEnvelope 2023 作为公开基线。最终冻结结果：

| 方法 | 本轮 gene-level 输出 | 共同空间覆盖 |
|---|---:|---:|
| FastKnock 2024 | 0 个合法候选 | 0 / 235 |
| CFSA 2024 | 14 个映射单基因 KO | 14 / 235 |
| OptEnvelope 2023 | 0 个可映射 gene row | 0 / 235 |
| **FABRIC-AI v1.2** | **235 个候选全部完成表型评价并确定性排序** | **235 / 235** |

在 primary condition 中，235 个候选的 guaranteed-production 下界均为 0，系统自动触发 `NON_DISCRIMINATING_GUARANTEED_PRODUCTION`。这一状态进入预先冻结的可实施性排序层，而不利用数值噪声制造产量差异。最终 secondary Top-6 仅用于实验优先级：`YAL060W`、`YBR006W`、`YBR011C`、`YBR183W`、`YBR281C`、`YCR005C`。

- [AI / 计算方法](wiki/AI-Computational-Methods.md)
- [最终四方法 benchmark](results/baseline/20260908/FOUR_METHOD_BENCHMARK_FINAL.md)
- [FABRIC-AI 复现入口](src/ai/fabric_ai_optimizer/README.md)
- [最终冻结状态](results/fabric_ai/20260908/DESIGN_MODE_FINAL_FREEZE.json)

### 1.2 P0：计算设计—发酵验证—反馈更新

历史 P0 路线形成 `307 个候选反应 → 14 个 Plan → 6 个实验靶点` 的设计链。Round 1 中，ΔPAN5 在 120 h 的虾青素产量约为 `0.67 mg/L`，同批 AST 约为 `0.47 mg/L`，提升约 `42.6%`；ΔMDE1 在 96–120 h 由约 `0.42 mg/L` 降至 `0.36 mg/L`。反馈程序据此更新 PAN5、MDE1 及其余靶点的证据等级，形成下一轮设计依据。

完整闭环见 [干湿结合验证](wiki/Integrated-Validation.md)。

### 1.3 P1：BmCBP 蛋白固色

项目将家蚕类胡萝卜素结合蛋白 BmCBP 引入天然色素固色模块。团队完成了 BmCBP 表达与色素结合评价，并通过不同基材实验将丝绸确定为重点验证对象。产业交流进一步推动“BmCBP 蛋白媒染 + 壳聚糖物理保护”的双层固色方向。

新元件：[`AISB26-045-002`](parts/AISB26-045-002/)。

### 1.4 P2：PhiReX 光控表达

PhiReX 红光响应系统以约 `630 nm`、`200 μW/cm²`、2 h pulse 进行表征，Fig.12 中 R5、R11、R13 编号样品在红光条件下的 EGFP/OD600 均高于无光对照。硬件侧同步加入光传感、GUI 和远程参数调整接口，使光控系统由固定照射扩展为可监测、可调整的工程模块。

新元件：[`AISB26-045-001`](parts/AISB26-045-001/)。

## 2. 2026 新元件

| 元件编号 | 名称 | 长度 | 核心表征 |
|---|---|---:|---|
| `AISB26-045-001` | PhiReX 红光调控表达系统 | 12,584 bp | 红光 / 无光 EGFP/OD600 比较 |
| `AISB26-045-002` | BmCBP 色素结合蛋白 | 690 bp | A480 与织物/基材实验 |

两项元件均提供 FASTA、GenBank、元数据、表征记录和图谱文件，见 [`parts/`](parts/)。

## 3. 快速复现 FABRIC-AI

验证环境：Python 3.12.10、COBRApy 0.30.0、SciPy 1.17.1、swiglpk 5.0.13、pandas 2.3.3、pytest 8.3.5；solver tolerance 为 `1e-7`。

```bash
python -m pip install -r src/ai/fabric_ai_optimizer/requirements-frozen.txt
python tools/fabric_ai/reproduction_smoke.py --outdir .reproduction/smoke
```

完整复现将依次执行 prepare、v1 evaluate、v2A evaluate 和 rank，并检查最终 metrics、ranking、Top-6 与冻结版本一致。9 项 ranking tests 和 15/15 最终 verification 已通过。

详细说明见 [`src/ai/fabric_ai_optimizer/README.md`](src/ai/fabric_ai_optimizer/README.md) 和 [可验证性](wiki/Verifiability.md)。

## 4. 评审导航

| 内容 | 入口 |
|---|---|
| 项目总体方案 | [`wiki/Project-Description.md`](wiki/Project-Description.md) |
| AI / 计算方法与基线 | [`wiki/AI-Computational-Methods.md`](wiki/AI-Computational-Methods.md) |
| 湿实验与关键结果 | [`wiki/Wet-Lab-Experiments.md`](wiki/Wet-Lab-Experiments.md) |
| DBTL 干湿闭环 | [`wiki/Integrated-Validation.md`](wiki/Integrated-Validation.md) |
| 工程化循环 | [`wiki/Engineering-Cycle.md`](wiki/Engineering-Cycle.md) |
| 新元件 | [`wiki/Parts.md`](wiki/Parts.md) |
| 人类实践 | [`wiki/Human-Practices.md`](wiki/Human-Practices.md) |
| 教育与科普 | [`wiki/Education.md`](wiki/Education.md) |
| Collaboration | [`wiki/Collaboration.md`](wiki/Collaboration.md) |
| AI 伦理与安全 | [`wiki/AI-Ethics-Safety.md`](wiki/AI-Ethics-Safety.md) |
| 项目贡献与 AI 使用 | [`attributions.md`](attributions.md) / [`AI-USE-DISCLOSURE.md`](AI-USE-DISCLOSURE.md) |

## 5. 冻结与审计

2026-09-08 冻结代码、共同模型、条件配置、最终结果和 AISB26 元件文件已同步至 `benchmark/fabric-ai-20260907`。仓库同步提交为 `121a7d6032210c477292097c76073b5a7a676faf`；最终同步报告见 [`results/evidence/20260908/code_parts_sync/`](results/evidence/20260908/code_parts_sync/)。

项目以 Gitee 作为队伍协作主仓库，GitHub 作为镜像和自动审计入口。最终提交前将由本地双远程流程同步冻结版本。

---

*最后更新：2026-09-08*
