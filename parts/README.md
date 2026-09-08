# Parts · AISB26 正式提交元件

BIT-CHINA（045）在本届正式提交两个团队创建的 DNA 元件。两个元件保留 2025 年创建与 Registry 来源信息，并于 2026 年首次按 AISB26 格式提交，均计入本届元件数量。FASTA 与 GenBank 序列逐碱基一致，AI 未直接设计或修改序列。

| AISB26 编号 | 正式名称 | 原 Registry 编号 | 类型 | 长度 | 提交状态 |
|---|---|---|---|---:|---|
| AISB26-045-001 | PhiReX red-light-regulated gene expression system | BBa_25UFORFE | Composite Part | 12,584 bp | 正式提交；计入本届元件数量 |
| AISB26-045-002 | Codon-optimized truncated BmCBP coding sequence | BBa_251P300A | Basic CDS | 690 bp | 正式提交；计入本届元件数量 |

## 文件索引

每个正式目录包含：

- `sequence.fasta`：AISB26 header 与原 Registry 碱基序列；
- `metadata.yaml`：队伍、年份、来源、设计、表征和许可；
- `characterization.md`：构建、实验方法、结果和证据范围；
- `registry_export.gb`：对应 Registry GenBank 副本；
- `map.svg`：由 GenBank feature 或 CDS 边界生成的线性图谱。

## 表征摘要

AISB26-045-001 保存 OE-PCR、Gibson Assembly、Plasmid 5/6、菌落 PCR、测序和红光/无光 EGFP 表征。实验采用约 630 nm、200 μW/cm²、2 h pulse，培养 24 h 后测量 EGFP Ex/Em 485/528 nm 与 OD600。R5、R11 和 R13 三个编号样品在红光条件下均表现出高于无光对照的归一化 EGFP 信号。

AISB26-045-002 对应 UniProt Q8MYA9 第 68–297 位氨基酸，去除 N 端第 1–67 位预测无序区，CDS 经密码子优化。团队完成表达纯化、结合测量和跨基材表征。每个浓度条件进行 3 次测量，平均 A480 随 BmCBP 浓度增加依次下降。

## 许可与溯源

两个元件均保存 `original_constructed_year: 2025`、`submitted_to_aisb26_year: 2026`、`source_team: BIT-China 2025`、`source_registry_id` 与 `source_license: CC-BY-SA-4.0`。序列、GenBank 文件和衍生元件说明采用 CC BY-SA 4.0。