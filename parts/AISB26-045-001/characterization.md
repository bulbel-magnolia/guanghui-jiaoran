# AISB26-045-001 · PhiReX red-light-regulated gene expression system

提交状态：本届正式提交；计入本届元件数量。

## 来源与提交关系

本元件由 BIT-China 团队创建，2025 年以 BBa_25UFORFE 保存于 Registry，2026 年首次按 AISB26 格式提交为 AISB26-045-001。元件为 12,584 bp Composite Part，团队在 Saccharomyces cerevisiae BY4742 中完成构建与功能测试。提交目录保留原始编号、年份和 CC BY-SA 4.0 许可。

## 红光调控设计

TDH3 promoter 驱动 HY1 与 PcyA，提供 PhyB 光敏色素所需的胆色素合成模块。TEF2 promoter 驱动 PIF3-NLS-VP16 与 PhyBNT-Zif268。红光诱导 PhyB 与 PIF3 相互作用，将 VP16 激活结构域定位至 GalZifBSp promoter 邻近区域并促进下游 EGFP 表达。

复合序列还包含 YPRC3L、TEF1 terminator、tENO2、FBA1 terminator、KanMX 和 YPRC3R。该元件由多个调控与编码单元组成，按 Composite Part 表达其完整功能结构。

## 构建证据

团队依次使用 Overlap Extension PCR 和 Gibson Assembly 组装多片段系统。Plasmid 5/6 构建示意、菌落 PCR 和测序记录共同支持元件构建结果，测序结论与设计序列一致。

## 功能表征

PhiReX 酵母培养物接受约 630 nm、200 μW/cm² 的红光脉冲照射，单次照射持续 2 h；培养 24 h 后测定 EGFP 荧光和 OD600，并计算归一化荧光强度。

| 参数 | 设置 |
|---|---|
| 红光中心波长 | 约 630 nm |
| 光强 | 200 μW/cm² |
| 照射方式 | 2 h pulse |
| 总培养时间 | 24 h |
| EGFP 测量 | Ex/Em 485/528 nm |
| 生物量测量 | OD600 |
| 结果计算 | EGFP/OD600 归一化荧光强度 |

R5、R11 和 R13 三个编号样品均在红光条件下表现出高于无光对照的归一化 EGFP 信号。

## 文件与许可

完整提交目录包含 `sequence.fasta`、`registry_export.gb`、`map.svg`、`metadata.yaml` 和 `characterization.md`。序列、GenBank 与衍生元件说明采用 CC BY-SA 4.0。AI 未直接设计或修改该序列。