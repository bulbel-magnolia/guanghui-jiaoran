# Wet Lab / 湿实验

FABRIC 的湿实验围绕三个核心问题展开：工程化酵母能否形成可用于模型反馈的生产数据，BmCBP 能否承担色素—材料接口功能，PhiReX 是否能够在固定红光条件下产生可测量响应。实验结果分别进入 P0 Production Optimizer、P1 Material Interface Optimizer 和 P2 Color & Light Translator。

---

## 1. 实验总览

| 模块 | 实验对象 | 关键结果 | 进入的计算模块 |
|---|---|---|---|
| P0 生产优化 | Round 0 发酵与 Round 1 六靶点 | ΔPAN5 120 h 约 0.67 mg/L；同批 AST 约 0.47 mg/L；ΔMDE1 后期下降 | Production Optimizer / Learn mode |
| P1 材料接口 | BmCBP 表达、色素结合、织物 | 三浓度平均 A480 依次下降；丝绸为当前优先基材 | Material Interface Optimizer |
| P2 光控 | PhiReX 红光响应 | R5、R11、R13 红光条件下归一化 EGFP 均高于无光对照 | Color & Light Translator |

---

## 2. Round 0 发酵与模型输入

Round 0 在 0–144 h 记录 OD600，并在相应时间点记录葡萄糖和乙醇。葡萄糖在 12 h 达到记录下限，乙醇在后续阶段逐步消耗。历史模型据此记录乙醇消耗边界 `0.447596 mmol/(gDCW·h)`，用于描述产色阶段的碳流状态。

原始实验记录同时给出了 OD 与细胞干重换算：

`Cell concentration (gDCW/L) = 0.39859 × OD + 0.1206`

葡萄糖和乙醇数据按标准液与稀释倍数换算为 g/L。相关记录用于建立发酵阶段与模型边界之间的对应关系。

公开实验记录入口：

- BIT-China 2025 Notebook：https://2025.igem.wiki/bit-china/notebook
- `Improvement of Dye Production by GSMM` 附件由 Notebook 页面提供。

---

## 3. Round 1：六个基因靶点

历史模型筛选与人工审核最终形成六个 Round 1 靶点：

| 靶点 | 对应反应 | Round 1 结果 |
|---|---|---|
| RIB2 | `r_0014` | 本轮构建或培养可实施性状态 |
| PAN5 | `r_0019` | 进入定量发酵；正向结果 |
| MDE1 | `r_0086` | 进入定量发酵；后期持续性下降 |
| MRI1 | `r_0087` | 本轮构建或培养可实施性状态 |
| SPE2 | `r_0145` | 本轮构建或培养可实施性状态 |
| FUM1 | `r_0452` | 本轮构建或培养可实施性状态 |

AST、ΔPAN5 和 ΔMDE1 的产物数据覆盖 72、96、120 h，生物量记录覆盖 0–120 h。120 h 时三组产物浓度约为：

- AST：`0.47 mg/L`
- ΔPAN5：`0.67 mg/L`
- ΔMDE1：`0.36 mg/L`

ΔPAN5 相对同批 AST 提升约 **42.6%**。ΔMDE1 在 96–120 h 由约 `0.42 mg/L` 下降至 `0.36 mg/L`。这些结果与其余四个靶点的可实施性状态共同进入反馈规则。

反馈后的证据等级与后续动作见 [干湿结合验证](./Integrated-Validation.md)。

---

## 4. BmCBP 表达与纯化

BmCBP 使用密码子优化的截短编码序列，对应 UniProt Q8MYA9 的第 68–297 位氨基酸，去除 N 端 1–67 位预测无序区。当前 CDS 长度为 690 bp。

表达宿主为 *E. coli* BL21(DE3)，表达载体基于 pET-28a(+)。实验流程包括：

1. IPTG 诱导表达；
2. 细胞裂解；
3. Ni-NTA 亲和纯化；
4. SDS-PAGE 检查表达与纯化结果；
5. 蛋白浓度测定；
6. 进入色素结合与织物实验。

原始实验附件：

- `Recombinant Expression and Purification for the Silkworm Carotenoid-Binding Protein BmCBP`，见 2025 Notebook。

---

## 5. BmCBP—虾青素结合实验

每个 BmCBP 浓度条件进行 **3 次测量**。三组平均 A480 与游离虾青素记录如下：

| BmCBP 浓度（mol/L） | 平均 A480 | 游离 astaxanthin（mol/L） |
|---:|---:|---:|
| 0 | 2.19190 | `1.6×10^-6` |
| `5.5×10^-7` | 2.00360 | `1.4×10^-6` |
| `1.1×10^-6` | 1.84980 | `1.2×10^-6` |

随着 BmCBP 浓度增加，平均 A480 和游离虾青素记录均下降，支持 BmCBP 与虾青素结合。该结果进入 P1 Material Interface Optimizer，用于连接蛋白候选、色素结合与织物结果。

---

## 6. BmCBP 基材实验

丝绸对照配方为 10 mL 乙醇和 0.5 mg astaxanthin；实验组使用 2 mL 乙醇、0.5 mg astaxanthin、7.6 mL 水和 0.4 mL 的 2.6 mg/mL BmCBP。

丝绸两组平行结果的洗后保色方向一致；棉和聚酯形成跨基材比较。当前材料证据将丝绸作为优先基材，并把棉和聚酯的差异写入材料优先级。

Human Practices 中的产业反馈进一步推动“BmCBP 蛋白媒染 + 壳聚糖物理保护”的双层固色方向。详见 [Human Practices](./Human-Practices.md)。

---

## 7. PhiReX 红光表征

PhiReX 酵母培养物接受约 `630 nm`、`200 μW/cm²` 的红光脉冲，单次照射持续 2 h，总培养时间 24 h。培养结束后测定 EGFP 荧光和 OD600，并计算 EGFP/OD600 归一化信号。

EGFP 激发/发射波长为 `485/528 nm`。R5、R11、R13 三个编号样品在红光条件下均表现出高于无光对照的归一化 EGFP 信号。

该参数组合已经进入 P2 Color & Light Translator 的结构化记录：

- 波长：约 630 nm；
- 光强：约 200 μW/cm²；
- pulse：2 h；
- 总培养：24 h；
- 读出：EGFP、OD600、EGFP/OD600。

---

## 8. 染色、混色与硬件接口

染色记录覆盖 astaxanthin、lycopene、zeaxanthin、indigo，以及丝绸、棉和聚酯。混色记录保存 astaxanthin/indigo 与 lycopene/indigo 的多种比例。

硬件将数字图案转换为空间化或时序化光输入，并通过传感、GUI 和远程通信接口连接培养状态与光照参数。红光和绿光通道已有 EGFP 功能表征，现有结构化数据用于支持后续颜色—光照映射。

---

## 9. 与 AI / 计算模块的接口

湿实验结果进入模型的路径为：

`Round 0 / Round 1 / BmCBP / PhiReX → 结构化数据 → P0/P1/P2 → 证据等级与下一轮设计`

P0 的 Design–Build–Test–Learn 主闭环、P1 材料接口和 P2 光控迭代见 [干湿结合验证](./Integrated-Validation.md)。

---

## 10. 安全与记录

项目实验在团队批准的实验室安全范围内开展，相关生物安全、AI 使用与责任边界见 [AI Ethics & Safety](./AI-Ethics-Safety.md)。原始 Notebook、实验附件和结构化数据用于支持结果追溯。

---

*最后更新：2026-09-08*