# Wiki 图片二进制同步任务

目标分支：`wiki/visual-layout-20260909`

本页只用于最后一次图片二进制同步。Wiki 正文的图位、图注和相对路径已经完成，不修改科学数字或页面正文。

## 目标目录

将以下 10 个文件完整复制到：

`wiki/assets/figures/`

文件名必须保持：

1. `fabric-ai-overview.webp`
2. `fabric-ai-p0-workflow.webp`
3. `benchmark-coverage.webp`
4. `dbtl-307-14-6.webp`
5. `p0-astaxanthin-fermentation.webp`
6. `bmcbp-dual-fixation.webp`
7. `bmcbp-a480.webp`
8. `phirex-mechanism.webp`
9. `phirex-expression.webp`
10. `human-practices-design-change.webp`

## 同步后检查

确认以下页面中的全部图片正常渲染：

- `wiki/Home.md`
- `wiki/Project-Description.md`
- `wiki/Design.md`
- `wiki/AI-Computational-Methods.md`
- `wiki/Integrated-Validation.md`
- `wiki/Engineering-Cycle.md`
- `wiki/Wet-Lab-Experiments.md`
- `wiki/Parts.md`
- `wiki/Human-Practices.md`

两个正式元件图谱继续使用现有文件，不复制、不重画：

- `parts/AISB26-045-001/map.svg`
- `parts/AISB26-045-002/map.svg`

## 禁止修改

- 不修改四方法 benchmark 数字；
- 不修改 corrected 235-gene 候选空间；
- 不修改 FABRIC-AI Top-6；
- 不修改 P0/P1/P2 湿实验数值；
- 不修改元件 FASTA/GenBank/map.svg；
- 不对图片重新压缩、重新生成或改名。

同步后运行 Markdown 相对路径检查，并返回最终 commit SHA。