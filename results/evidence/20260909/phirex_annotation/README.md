# PhiReX：注释、样品字段与图记录

## 本次完成

FASTA 与 GenBank 的 12,584 bp 序列一致，两元件 FASTA 文件字节均未变化。PIF3-NLS-VP16、PhyBNT-Zif268 的原 CDS 区间通过阅读框检查，保留原坐标。HY1、PcyA、EGFP、KanMX 的精确 CDS 边界未确认，保留标签、原区段和方向，改为 `misc_feature`；没有为了获得正确 ORF 而改 DNA 或猜测边界。

| 区段 | 原坐标（1-based inclusive） | 提交版类型 |
|---|---|---|
| HY1 | 1599–2333 | misc_feature |
| PcyA | 2334–3092 | misc_feature |
| PIF3-NLS-VP16 | 4493–6328 | CDS，阅读框一致 |
| PhyBNT-Zif268 | 6329–8467 | CDS，阅读框一致 |
| EGFP | 9377–10089 | misc_feature；原区段 713 nt |
| KanMX | 10590–11945 | misc_feature；原盒区段 |

这项修复关闭了“把可疑区段作为已确定 CDS 发布”的问题。四段完整编码边界的生物学确认继续由原设计/测序记录完成，阅读框检查不替代测序验证。

[修订 manifest](change_manifest.json) · [逐 feature 审计](feature_audit.json) · [原 GenBank](original/AISB26-045-001/registry_export.gb) · [当前 GenBank](../../../../parts/AISB26-045-001/registry_export.gb) · [当前 map](../../../../parts/AISB26-045-001/map.svg)。

## 样品与表达图

检查了 v0.8 的八个工作簿、文本记录和可达 Git 历史。R5/R11/R13 仍只有编号及 red-light promoter 组别记录，不能确定其构建/克隆身份、重复类型、n、误差线和统计方法。相应字段保留 `manual_confirmation_required`。[搜索结果](sample_recovery_search.json)。本轮在线 Wiki/Registry 页面读取失败，没有用推断补字段。

当前 Wiki 图对应 **Fig.12**，六个数值与该表一致。原工作簿另有 **Fig.13**，其 R11/R13 的 +Light 小于 Control。两张图分别保留，不作为独立重复合并，不把 Fig.12 方向外推到全部条件。

[两组数字化读数](phirex_digitized_records.csv) · [原工作簿](FABRIC_wetlab_structured_dataset_v0_8.xlsx) · [原工作表 XML](source_light_sheet3.xml) · [文件指纹](source_files.json)。

星号来源在工作簿中只是转录的符号，没有相应统计检验依据。本轮仅从展示图移除星号和显著性括号；所有其他像素逐点一致。[原图归档](original/phirex-expression.webp) · [精确编辑记录](figure_edit_record.json)。原 CSV 的 significance 文本留作来源记录，不作为显著性结论。

## 复现

```bash
python tools/fabric_ai/audit_phirex_features.py --outdir .reproduction/parts-review
```

原坐标图由同一脚本加 `--write-map` 生成；生成与实际 SVG 渲染记录见本目录和总验证报告。
