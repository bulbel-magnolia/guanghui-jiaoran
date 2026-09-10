# AISB26-045-001 · PhiReX red-light-regulated gene expression system

提交状态：本届正式提交；计入本届元件数量。

## 来源与提交关系

本元件由 BIT-China 团队创建，2025 年以 BBa_25UFORFE 保存于 Registry，2026 年首次按 AISB26 格式提交为 AISB26-045-001。元件为 12,584 bp Composite Part，团队在 Saccharomyces cerevisiae BY4742 中完成构建与功能测试。提交目录保留原始编号、年份和 CC BY-SA 4.0 许可。

## 红光调控设计

TDH3 启动子驱动 HY1 与 PcyA，提供 PhyB 光敏色素所需的胆色素合成模块。TEF2 启动子驱动 PIF3-NLS-VP16 与 PhyBNT-Zif268。红光诱导 PhyB 与 PIF3 相互作用，将 VP16 激活结构域定位至 GalZifBSp 启动子邻近区域并促进下游 EGFP 表达。

复合序列还包含 YPRC3L、TEF1 终止子、tENO2、FBA1 终止子、KanMX 和 YPRC3R。该元件由多个调控与编码单元组成，按 Composite Part 表达其完整功能结构。

## 构建证据

团队依次使用重叠延伸 PCR 和 Gibson Assembly 组装多片段系统。Plasmid 5/6 构建示意、菌落 PCR 和测序记录共同支持元件构建结果，测序结论与设计序列一致。

## 功能表征

PhiReX 酵母培养物接受约 630 nm、200 μW/cm² 的红光脉冲照射，单次照射持续 2 h；培养 24 h 后测定 EGFP 荧光和 OD600，并计算归一化荧光强度。

| 参数 | 设置 |
|---|---|
| 红光中心波长 | 约 630 nm |
| 光强 | 200 μW/cm² |
| 照射方式 | 2 h 脉冲照射 |
| 总培养时间 | 24 h |
| EGFP 测量 | 激发/发射波长 485/528 nm |
| 生物量测量 | OD600 |
| 结果计算 | EGFP/OD600 归一化荧光强度 |

原记录图 12 中 R5、R11 和 R13 三个编号样品均在红光条件下表现出高于无光对照的归一化 EGFP 信号。

## 注释与图记录复核（2026-09-09）

DNA 全长 12,584 bp，序列与修订前相同，FASTA 与 GenBank 提取序列逐碱基一致。PIF3-NLS-VP16 与 PhyBNT-Zif268 保留 CDS，并通过起始、终止和阅读框检查。HY1、PcyA、EGFP、KanMX 保留原标签、区段及方向，改记 `misc_feature`；完整 CDS 边界由原设计/测序记录核实后再更新。

当前展示的原记录图 12 数字化记录中，R5、R11、R13 红光条件下的 EGFP/OD600 均高于对照。原记录图 13 中，R11 与 R13 低于对照；两组记录分开保存，不合并为重复。

| 图记录 | 样品 | +Light | Control |
|---|---|---:|---:|
| 原记录图 12 | R5 | 约 1900 | 约 720 |
| 原记录图 12 | R11 | 约 1985 | 约 685 |
| 原记录图 12 | R13 | 约 1550 | 约 800 |
| 原记录图 13 | R5 | 约 1120 | 约 1050 |
| 原记录图 13 | R11 | 约 1480 | 约 1550 |
| 原记录图 13 | R13 | 约 1100 | 约 1220 |

表中数值为 EGFP/OD600 的近似图读值。R5/R11/R13 对应的构建或克隆身份、重复类型、n、误差线和统计方法待原始记录确认。图中不标统计显著性，柱高与数值保留原记录。

[原序列、修订与图记录](../../results/evidence/20260909/phirex_annotation/README.md)。

## 文件与许可

完整提交目录包含 `sequence.fasta`、`registry_export.gb`、`map.svg`、`metadata.yaml` 和 `characterization.md`。序列、GenBank 与衍生元件说明采用 CC BY-SA 4.0。AI 未直接设计或修改该序列。
