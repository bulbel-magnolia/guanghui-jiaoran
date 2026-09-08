# Parts · 元件库贡献

BIT-CHINA（045）在本届正式提交两个团队创建并完成表征的 DNA 元件：PhiReX 红光调控表达系统和密码子优化的截短 BmCBP 编码序列。两个元件均保留原始 Registry 编号、创建年份、序列来源和许可信息，并于 2026 年首次按 AISB26 格式提交。

---

## 1. 本届正式提交元件

| AISB26 编号 | 名称 | 类型 | 长度 | 主要表征 | 状态 |
|---|---|---|---:|---|---|
| **AISB26-045-001** | PhiReX red-light-regulated gene expression system | Composite Part | 12,584 bp | 红光/无光 EGFP 功能表征 | **已表征，正式提交** |
| **AISB26-045-002** | Codon-optimized truncated BmCBP coding sequence | Basic CDS | 690 bp | 表达纯化、A480 结合、织物结果 | **已表征，正式提交** |

完整索引见 [`parts/README.md`](../parts/README.md)。

---

## 2. AISB26-045-001 · PhiReX 红光调控表达系统

### 2.1 元件设计

PhiReX 为多单元复合调控系统。TDH3 promoter 驱动 HY1 与 PcyA，提供 PhyB 光敏色素所需的胆色素合成模块；TEF2 promoter 驱动 PIF3-NLS-VP16 与 PhyBNT-Zif268。红光诱导 PhyB 与 PIF3 相互作用，将 VP16 激活结构域定位到 GalZifBSp promoter 邻近区域，从而促进下游 EGFP 表达。

元件还包含 YPRC3L、TEF1 terminator、tENO2、FBA1 terminator、KanMX 和 YPRC3R 等结构，用于形成完整的酵母红光调控表达系统。

### 2.2 构建与功能表征

团队使用 Overlap Extension PCR 与 Gibson Assembly 完成多片段组装，并以菌落 PCR 和测序记录支持构建结果。

功能表征参数：

| 参数 | 设置 |
|---|---|
| 宿主 | *Saccharomyces cerevisiae* BY4742 |
| 红光中心波长 | 约 630 nm |
| 光强 | 200 μW/cm² |
| 照射方式 | 2 h pulse |
| 总培养时间 | 24 h |
| 报告基因 | EGFP |
| EGFP Ex/Em | 485/528 nm |
| 归一化 | EGFP/OD600 |

R5、R11、R13 三个编号样品在红光条件下均表现出高于无光对照的归一化 EGFP 信号。

证据文件：

- [`metadata.yaml`](../parts/AISB26-045-001/metadata.yaml)
- [`characterization.md`](../parts/AISB26-045-001/characterization.md)

---

## 3. AISB26-045-002 · 密码子优化的截短 BmCBP 编码序列

### 3.1 元件设计

该元件对应 UniProt Q8MYA9 第 68–297 位氨基酸，去除 N 端第 1–67 位预测无序区。CDS 经密码子优化，长度为 690 bp。实际表达使用 pET-28a-BmCBP，在 *E. coli* BL21(DE3) 中完成。

### 3.2 表达与结合表征

团队完成 IPTG 诱导、Ni-NTA 亲和纯化、SDS-PAGE 和蛋白浓度测定，并将纯化蛋白用于虾青素结合与织物实验。

每个 BmCBP 浓度条件进行 3 次测量：

| BmCBP 浓度（mol/L） | 平均 A480 | 游离 astaxanthin（mol/L） |
|---:|---:|---:|
| 0 | 2.19190 | `1.6×10^-6` |
| `5.5×10^-7` | 2.00360 | `1.4×10^-6` |
| `1.1×10^-6` | 1.84980 | `1.2×10^-6` |

随着 BmCBP 浓度增加，平均 A480 与游离虾青素记录均下降，支持 BmCBP 与虾青素结合。丝绸、棉和聚酯比较进一步支持将丝绸作为当前优先基材。

证据文件：

- [`sequence.fasta`](../parts/AISB26-045-002/sequence.fasta)
- [`metadata.yaml`](../parts/AISB26-045-002/metadata.yaml)
- [`characterization.md`](../parts/AISB26-045-002/characterization.md)

---

## 4. 溯源与许可

两个元件均由 BIT-China 团队创建，保留 2025 年 Registry 来源信息，并于 2026 年首次按 AISB26 格式提交：

| AISB26 编号 | 原 Registry 编号 | 原创建年份 | AISB26 提交年份 | 许可 |
|---|---|---:|---:|---|
| AISB26-045-001 | BBa_25UFORFE | 2025 | 2026 | CC BY-SA 4.0 |
| AISB26-045-002 | BBa_251P300A | 2025 | 2026 | CC BY-SA 4.0 |

元件序列在 AISB26 提交过程中未由 AI 修改。AI 主要用于资料整理、计算分析和文档生成，具体披露见 [Attributions](./Attributions.md) 与 [AI Ethics & Safety](./AI-Ethics-Safety.md)。

---

## 5. 与项目主线的关系

- **AISB26-045-001** 对应 P2 Color & Light Translator，为光控表达和硬件参数提供实验接口；
- **AISB26-045-002** 对应 P1 Material Interface Optimizer，为 BmCBP 色素结合和固色实验提供蛋白元件基础。

两项元件表征均与 [湿实验](./Wet-Lab-Experiments.md) 和 [干湿结合验证](./Integrated-Validation.md) 中的项目结果直接对应。

---

*最后更新：2026-09-08*