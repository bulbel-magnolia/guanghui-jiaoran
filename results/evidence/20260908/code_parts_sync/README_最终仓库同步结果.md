# 最终仓库同步结果

状态：`REPO_SYNC_COMPLETE_READY_FOR_JUDGING_FORM_FINALIZATION`

目标分支 `benchmark/fabric-ai-20260907`；同步基点 `9d1593e9696f0e7a6d1e8b92efc87af5b95c7258`。本次提交包含此前冻结代码/模型/结果同步及此次缺失 AISB26 文件同步。最终 closeout ZIP 中的 `publication_receipt.json` 记录实际提交 SHA、远端核验和发布状态。

## 同步来源与文件

- fresh Design-mode ZIP：SHA-256 `ab6e65cce6d2358f75a687cae065ac72de57b5dc16329cf4a764a4c5dbb2764e`。
- ranking numerical-equivalence correction ZIP：SHA-256 `7cea8b7f7c501a7b5130cd069c952686d045c1406cdff06321f0cca8a02b15d7`。
- 用户指定 signed ZIP（本地文件名带 `(1)`）：SHA-256 `3998a357006b30c22a513d44ca5dd3f46875c065b0a409839e39151ea714fd55`。
- 共 40 个同步文件与来源成员逐字节一致，其中 35 个代码/模型/结果/审计文件、5 个本次 AISB26 文件。两个优化器 ZIP 的内部 manifest 已通过 35/35 和 18/18 成员哈希检查。
- AISB26-045-001 同步 `sequence.fasta`、`registry_export.gb`、`map.svg`；AISB26-045-002 同步 `registry_export.gb`、`map.svg`。原有 metadata、characterization 与第二元件 FASTA 保持原样；未从 signed ZIP 引入其他内容。

## 检查结果

- 两元件 FASTA/GenBank 逐碱基一致，长度分别 12,584 bp 和 690 bp；第二元件 CDS `1..690` 与完整序列一致。两份 SVG XML 可解析，相对引用检查通过。
- ranking tests：9 passed；最终 correction verification：15/15 passed。原 fresh verifier另以原包历史目录布局通过 18 项结构检查，其历史排序仅用于审计。
- 完整 prepare、v1 evaluate（235）、v2A evaluate（235）、冻结 metrics rank 均已实际执行并 exit 0；prepare 基因集、blocked set 和 GPR footprints 一致，两组 metrics、最终 ranking/Top-6 均与冻结版本逐字节一致。
- 此次 parts 同步未改变上述代码或输入，已重新核对原 smoke 记录的全部 SHA-256，因此复用通过的完整复现结果。未重跑耗时求解，也未更新冻结 benchmark 运行数字。
- Python 3.12.10；COBRApy 0.30.0、SciPy 1.17.1、swiglpk 5.0.13、pandas 2.3.3、pytest 8.3.5；solver tolerance `1e-7`。依赖清单见冻结代码目录的 `requirements-frozen.txt`。
- 冻结 optimizer、测试和 verifier 保留来源字节；测试导入适配和临时验证目录解决原包相对路径。两份 protected reaction 配置逐字节相同，兼容冻结条件中的引用。Git 属性和 clean-filter 校验保护冻结文件字节。
- Wiki、四方法 benchmark、既有 parts 文件保持同步前 SHA-256；首页只增加导航；SPEC/contract 文本不变。共同模型、235-gene pool、v1/v2A 条件、ranking、Top-6 与科学结论均未修改。

## 独立科学审核点

此前首页和 `wiki/Verifiability.md` 的旧科学声明、模板指标继续列于 [科学内容审核点](science_claims_reviewpoint.md)，未自动改写。按用户续办要求，本次仓库同步状态设为完成；这不表示这些既有声明已经获得科学审核批准。

## 交付索引

- [逐文件仓库清单](final_repo_manifest.csv)：记录当前 checkout 文件的 SHA-256、变更类型与冻结来源；清单本身不列入自身，避免循环哈希。
- [一致性扫描](consistency_scan.csv)、[完整复现日志](reproduction_smoke_test.log)、[元件检查](parts_integrity_check.csv)。
- [来源映射](source_sync_manifest.csv)、[保护文件检查](preservation_check.json)、[本次最终验证](current_ranking_verification.json)。
- [冻结代码复现入口](../../../../src/ai/fabric_ai_optimizer/README.md)。

轻量 closeout ZIP 不重复装入模型、候选矩阵、源冻结包或临时运行目录；这些同步文件已纳入本次仓库提交。发布凭据在完成推送和远端核验后写入 ZIP。

扫描结果：14/14 Wiki 页面存在；10/10 元件文件齐全；109 个 Markdown/HTML 相对链接全部存在；两条冻结条件配置引用存在。外部 URL 与页内 anchor 不属于本轮文件存在性检查范围。
