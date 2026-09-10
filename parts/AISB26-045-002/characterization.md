# AISB26-045-002 · Codon-optimized truncated BmCBP coding sequence

中文名称：密码子优化的截短 BmCBP 编码序列。

提交状态：本届正式提交；计入本届元件数量。

## 来源与设计

本元件由 BIT-China 团队创建，2025 年以 BBa_251P300A 保存于 Registry，2026 年首次按 AISB26 格式提交为 AISB26-045-002。提交目录保留原始编号、年份和 CC BY-SA 4.0 许可。

该序列对应 UniProt Q8MYA9 第 68–297 位氨基酸，去除 N 端第 1–67 位预测无序区。CDS 经密码子优化，当前元件序列为 690 bp。实际表达依赖载体提供的翻译起始和融合表达上下文。

## 表达与纯化

团队在 Escherichia coli BL21(DE3) 中使用 pET-28a-BmCBP 完成表达与纯化：

1. 将重组载体导入 BL21(DE3)；
2. 使用 IPTG 诱导蛋白表达；
3. 破碎细胞并收集蛋白组分；
4. 采用 Ni-NTA 亲和纯化；
5. 以 SDS-PAGE 检查流穿、洗涤和洗脱组分；
6. 测定纯化蛋白浓度并用于结合与染色实验。

<a id="astaxanthin-结合表征"></a>
## 虾青素结合表征

每个 BmCBP 浓度条件进行 3 次测量。随着 BmCBP 浓度增加，平均 A480 依次下降，支持 BmCBP 与虾青素结合。

| BmCBP 浓度（mol/L） | 平均 A480 | 游离虾青素（mol/L） |
|---:|---:|---:|
| 0 | 2.19190 | 1.6×10⁻⁶ |
| 5.5×10⁻⁷ | 2.00360 | 1.4×10⁻⁶ |
| 1.1×10⁻⁶ | 1.84980 | 1.2×10⁻⁶ |

测量次数：每个条件 3 次。

## 丝绸染色与跨基材结果

丝绸对照使用 10 mL 乙醇和 0.5 mg 虾青素；含 BmCBP 配方使用 2 mL 乙醇、0.5 mg 虾青素、7.6 mL 水和 0.4 mL 的 2.6 mg/mL BmCBP。两组平行结果显示含 BmCBP 配方具有一致的洗后保色方向。棉和聚酯结果弱于丝绸，支持将丝绸列为当前优先基材。

## 文件与许可

完整提交目录包含 `sequence.fasta`、`registry_export.gb`、`map.svg`、`metadata.yaml` 和 `characterization.md`。序列、GenBank 与衍生元件说明采用 CC BY-SA 4.0。AI 未直接设计或修改该序列。
