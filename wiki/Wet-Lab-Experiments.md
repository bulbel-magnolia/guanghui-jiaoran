<div align="center">

# Wet Lab / 湿实验

**P0 生产优化 · P1 BmCBP 材料接口 · P2 PhiReX 光控表征**

</div>

<div align="center">

[← Wiki 首页](./Home.md) · [干湿结合验证](./Integrated-Validation.md) · [AI / 计算方法](./AI-Computational-Methods.md) · [元件](./Parts.md)

</div>

> 湿实验分别测量工程化酵母的色素生产、BmCBP 的色素结合与织物固色效果，以及 PhiReX 在固定红光条件下的表达响应。

| 模块 | 关键实验 | 代表性结果 | 进入的计算模块 |
|---|---|---|---|
| **P0 生产优化** | Round 0 发酵 + Round 1 六靶点 | ΔPAN5 120 h 约 **0.67 mg/L**；同批 AST 约 0.47 mg/L；ΔMDE1 后期下降 | 生产优化模块 / 实验反馈阶段 |
| **P1 材料接口** | BmCBP 表达、A480、织物 | 三浓度平均 A480：**2.19190 → 2.00360 → 1.84980** | 材料固色模块 |
| **P2 光控** | PhiReX 红光 / 无光 EGFP | 原记录图 12 中 R5、R11、R13 红光条件下归一化 EGFP 均高于无光对照 | 颜色与光控模块 |

---

## 1. P0 · Round 0 发酵与模型输入

Round 0 在 0–144 h 记录 OD600，并在相应时间点记录葡萄糖和乙醇。葡萄糖在 12 h 达到记录下限，乙醇在后续阶段逐步消耗。历史模型据此记录乙醇消耗边界 `0.447596 mmol/(gDCW·h)`，用于描述产色阶段的碳流状态。

| 记录 | 用途 |
|---|---|
| OD600 | 描述培养过程与生物量变化 |
| 葡萄糖 | 确认早期碳源消耗阶段 |
| 乙醇 | 描述葡萄糖耗尽后的生产阶段 |
| `0.447596 mmol/(gDCW·h)` | 历史乙醇生产阶段的摄取约束 |

原始实验记录给出的 OD—细胞干重换算为：

`Cell concentration (gDCW/L) = 0.39859 × OD + 0.1206`

葡萄糖和乙醇数据按标准液与稀释倍数换算为 g/L，用于建立发酵阶段与模型边界之间的对应关系。

公开实验记录入口：BIT-China 2025 Notebook（`Improvement of Dye Production by GSMM` 附件）。

---

## 2. P0 · Round 1 六个基因靶点

团队审核历史模型候选，选择六个 Round 1 靶点：

| 靶点 | 对应反应 | Round 1 结果 |
|---|---|---|
| RIB2 | `r_0014` | 本轮构建或培养结果 |
| **PAN5** | `r_0019` | 进入定量发酵；正向结果 |
| **MDE1** | `r_0086` | 进入定量发酵；后期持续性下降 |
| MRI1 | `r_0087` | 本轮构建或培养结果 |
| SPE2 | `r_0145` | 本轮构建或培养结果 |
| FUM1 | `r_0452` | 本轮构建或培养结果 |

### 关键定量结果

| 组别 | 96 h | 120 h | 读出 |
|---|---:|---:|---|
| AST | — | **约 0.47 mg/L** | 同批参考 |
| ΔPAN5 | — | **约 0.67 mg/L** | 相对同批 AST 提升约 **42.6%** |
| ΔMDE1 | **约 0.42 mg/L** | **约 0.36 mg/L** | 后期持续性下降 |

<p align="center">
  <img src="./assets/figures/p0-astaxanthin-fermentation.webp" alt="P0 Round 1 虾青素浓度曲线" width="88%">
</p>
<p align="center"><em>同批次 AST、ΔPAN5、ΔMDE1 的虾青素浓度时间序列。72、96、120 h 数值均为历史实验曲线的数字化读取值。</em></p>

这些结果与其余四个靶点的可实施性状态共同进入反馈规则。反馈后的证据等级与后续动作见 [干湿结合验证](./Integrated-Validation.md)。

---

## 3. P1 · BmCBP 表达与纯化

BmCBP 使用密码子优化的截短编码序列，对应 UniProt Q8MYA9 第 68–297 位氨基酸，去除 N 端 1–67 位预测无序区；当前 CDS 长度为 **690 bp**。

| 项目 | 设置 |
|---|---|
| 表达宿主 | *E. coli* BL21(DE3) |
| 载体 | pET-28a(+) |
| 表达 | IPTG 诱导 |
| 纯化 | Ni-NTA 亲和纯化 |
| 检查 | SDS-PAGE、蛋白浓度测定 |
| 后续 | 虾青素结合与织物实验 |

原始实验附件：`Recombinant Expression and Purification for the Silkworm Carotenoid-Binding Protein BmCBP`，见 2025 Notebook。

---

## 4. P1 · BmCBP—虾青素结合实验

每个 BmCBP 浓度条件进行 **3 次测量**。

| BmCBP 浓度（mol/L） | 平均 A480 | 游离虾青素（mol/L） |
|---:|---:|---:|
| 0 | **2.19190** | `1.6×10^-6` |
| `5.5×10^-7` | **2.00360** | `1.4×10^-6` |
| `1.1×10^-6` | **1.84980** | `1.2×10^-6` |

<p align="center">
  <img src="./assets/figures/bmcbp-a480.webp" alt="BmCBP 浓度与平均 A480" width="82%">
</p>
<p align="center"><em>BmCBP 浓度与平均 A480 的关系。每条件记录 3 次测量，本图展示保存的条件均值，不附误差线。</em></p>

平均 A480 和游离虾青素记录随 BmCBP 浓度增加而下降，支持 BmCBP 与虾青素结合。P1 将该结合结果与织物实验一同用于评价 BmCBP 固色方案。

---

## 5. P1 · 基材与固色方向

丝绸对照配方为 10 mL 乙醇和 0.5 mg 虾青素；实验组使用 2 mL 乙醇、0.5 mg 虾青素、7.6 mL 水和 0.4 mL 的 2.6 mg/mL BmCBP。

丝绸两组平行结果显示含 BmCBP 配方具有一致的洗后保色方向。棉和聚酯实验用于比较基材差异，当前优先研究**丝绸**。

产业反馈进一步推动“**BmCBP 蛋白媒染 + 壳聚糖物理保护**”的双层固色方向。详见 [人类实践](./Human-Practices.md)。

---

## 6. P2 · PhiReX 红光表征

| 参数 | 设置 |
|---|---|
| 红光中心波长 | 约 **630 nm** |
| 光强 | **200 μW/cm²** |
| 脉冲照射时长 | **2 h** |
| 总培养时间 | **24 h** |
| 报告基因 | EGFP |
| EGFP 激发 / 发射波长 | `485 / 528 nm` |
| 归一化 | EGFP / OD600 |

原记录图 12 中 R5、R11、R13 三个编号样品在红光条件下均表现出高于无光对照的归一化 EGFP 信号。

<p align="center">
  <img src="./assets/figures/phirex-expression.webp" alt="PhiReX 红光与对照归一化 EGFP" width="84%">
</p>
<p align="center"><em>原记录图 12 的红光/无光 EGFP/OD600 近似图读值。样品编号为 R5、R11、R13；重复类型、n 和误差线定义待原始记录确认，图中不附误差线或显著性标记。</em></p>

> **P2 测量流程**：设定光照参数 → 测量 EGFP / OD600 → 保存光响应数据。

---

原记录图 13 中，R11 与 R13 的 EGFP/OD600 低于对照。图 12 和图 13 分开报告，不合并为重复。

[两组独立图记录与样品字段](../results/evidence/20260909/phirex_annotation/README.md)。

## 7. 染色、混色与硬件接口

染色记录覆盖虾青素、番茄红素、玉米黄质、靛蓝，以及丝绸、棉和聚酯。混色记录保存虾青素/靛蓝与番茄红素/靛蓝的多种比例。

硬件将数字图案转换为空间化或时序化光输入，并通过传感、图形界面和远程通信接口连接培养状态与光照参数。红光和绿光通道已有 EGFP 功能表征，现有结构化数据用于支持后续颜色—光照映射。

---

## 8. 实验结果如何进入 FABRIC-AI

<div align="center">

**Round 0 / Round 1 / BmCBP / PhiReX → 结构化数据 → P0 / P1 / P2 → 证据等级与下一轮设计**

</div>

| 实验结果 | 进入模块 | 决策作用 |
|---|---|---|
| Round 1 基因靶点发酵 | P0 | 更新终点产量、持续性、生物量和可实施性证据 |
| BmCBP A480 / 织物 | P1 | 更新材料接口与基材优先级 |
| PhiReX 红光表征 | P2 | 记录光照参数与归一化测量结果 |

设计、实验与反馈过程见 [干湿结合验证](./Integrated-Validation.md)。

---

## 9. 元件与证据入口

| 内容 | 入口 |
|---|---|
| PhiReX 元件 | [`AISB26-045-001`](../parts/AISB26-045-001/) |
| BmCBP 元件 | [`AISB26-045-002`](../parts/AISB26-045-002/) |
| 元件总页 | [元件](./Parts.md) |
| 干湿闭环 | [干湿结合验证](./Integrated-Validation.md) |
| AI / 计算方法 | [AI / 计算方法](./AI-Computational-Methods.md) |
| 可验证性 | [可验证性](./Verifiability.md) |

---

## 10. 安全与记录

项目实验在团队批准的实验室安全范围内开展，相关生物安全、AI 使用与责任边界见 [AI 伦理与安全](./AI-Ethics-Safety.md)。原始 Notebook、实验附件和结构化数据用于支持结果追溯。

---

<div align="center">

[← Wiki 首页](./Home.md) · [干湿结合验证](./Integrated-Validation.md) · [AI / 计算方法](./AI-Computational-Methods.md) · [元件](./Parts.md) · [人类实践](./Human-Practices.md)

</div>

*最后更新：2026-09-10（文字修订）*
