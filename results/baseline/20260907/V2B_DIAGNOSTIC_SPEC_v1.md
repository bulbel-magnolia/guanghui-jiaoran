# v2B — YPD-informed B-vitamin availability sensitivity

状态：`DIAGNOSTIC_ONLY_NOT_PRIMARY_BENCHMARK`

## 目的

项目原始附件确认 YPD 含 10 g/L yeast extract、20 g/L peptone、20 g/L glucose。由于复杂培养基浓度不能直接转换为 GEM exchange 的 mmol/(gDCW·h)，本轮不声称定量复原 YPD。

## 来源驱动的 B-vitamin panel

为避免根据历史六靶点结果挑选“救援营养物”，v2B panel 预先定义为以下 7 个 Yeast-GEM exchange：

| nutrient class | Yeast-GEM exchange |
|---|---|
| B1 thiamine | `r_2067` |
| B2 riboflavin | `r_2038` |
| B3 nicotinate | `r_1967` |
| B5 pantothenate | `r_1548` |
| B6 pyridoxine | `r_2028` |
| B7 biotin | `r_1671` |
| B9 folic acid | `r_1792` |

不同时打开同一维生素类别的多种衍生物 exchange，避免重复供应。

## 冻结 sweep

共同打开以上 7 个 exchange 的 uptake，统一 lower-bound cap：

`-1e-6, -1e-5, -1e-4, -1e-3 mmol/(gDCW·h)`

背景保持 v1 glucose reference，其余边界不变。整个 sweep 作为一组结果报告；不得从中挑选对历史靶点最有利的单点并改称主条件。

validated eligible-gene counts：

| cap | eligible genes |
|---:|---:|
| 1e-6 | 238 |
| 1e-5 | 256 |
| 1e-4 | 262 |
| 1e-3 | 262 |

四个 cap 下新增可通量的 7 条反应相同：`r_0774, r_0953, r_0954, r_0955, r_2025, r_2029, r_4212`。

相对 corrected v1 235 pool：1e-6 为 +3，1e-5 为 +21，1e-4 与 1e-3 均为 +27；没有 corrected-v1 gene 被该 panel 排除。

## 历史六靶点的使用边界

六靶点仅用于 post-definition diagnostic check。panel membership 和 cap sweep 在查看六靶点恢复结果前固定，不将命中情况用于改变 nutrient membership、cap 范围或 Design-mode 排序。

在 v1 glucose background + cap `1e-5` 时，RIB2/PAN5/MDE1/MRI1/SPE2 均达到 >=10% WT growth；FUM1 原本已在 v1 可生长。单维生素机制检查显示 RIB2 主要由 riboflavin availability 救援，PAN5/MDE1/MRI1/SPE2 在该模型中主要由 pantothenate availability 打开替代可行域。

该结果说明 nutrient availability 对 candidate admission 很敏感，**不证明 1e-5 或 1e-4 是真实 YPD uptake rate**。

## 禁止解释

- 不称为真实 YPD uptake rate；
- 不把某个 cap 的“全部靶点恢复”当作 cap 正确性的证据；
- 不把 v2B 纳入公开 baseline 胜负，除非以后获得独立定量 uptake 依据并在查看正式 benchmark 结果前冻结；
- 不以 v2B 中历史靶点恢复率作为 Production Optimizer 的评分项。