# AI + Synthetic Biology Project — Team Template

> 光绘酵染
>
> 一句话项目介绍（建议 60 字以内）。
用基因工程酵母在不同波长光照下合成三种天然色素,配合家蚕内源 BmCBP 蛋白做媒染剂,把数字图案直接"画"在布料上,全程零重金属、零化学废水。
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Wiki](https://img.shields.io/badge/Wiki-/wiki-blue)](./wiki/Home.md)

---


1. 项目简介 / Project Overview
研究问题:纺织印染是全球第二大污染产业,每年释放 2 万吨染料、消耗 930 亿立方米水,废水里有锑、铅、砷、铬这类重金属和苯胺等致癌物,处理成本高昂。我们要回答的核心问题是——能不能用合成生物学加上计算建模的手段,把化学染料和重金属媒染剂同时替换掉,在零毒排放的前提下还能做到精准的图案定制?
所选赛道:T3
核心方法:AI/计算端和湿实验端做闭环耦合—

计算建模驱动菌株设计:用 GSMM(基因组尺度代谢模型)加 OptKnock 算法,在虾青素合成路径上预测关键敲除靶点,把菌株迭代从"盲筛"变成"有理由的尝试",目前虾青素产量已经提升了 45%;
光遗传基因回路:在酿酒酵母里构建红、绿、蓝三种波长响应的启动子,分别诱导虾青素(红)、玉米黄素(黄)、靛蓝(蓝)合成,色素表达和光信号直接挂钩,共 8 条通路已经成功构建并测试;
蛋白-配体分子对接:用分子模拟筛选家蚕内源 BmCBP 蛋白做"桥联媒染剂",一端结合蚕丝、一端结合染料,把传统的铝/锑/铬媒染剂彻底换掉,色谱和体外结合实测都表现优异;
硬件-生物原位印染:50×50 像素的 LED 光生物反应器阵列加自研控制软件,把数字图案转化成空间分辨的光照方案,在布料上直接"显色",支持从设计稿到成品的全数字化流转。

预期产出:

三株可在 RGB 光信号下定向产色的酿酒酵母工程菌(虾青素 / 玉米黄素 / 靛蓝),菌株库和元件序列同步提交大赛 Registry;
BmCBP 蛋白表达质粒、大肠杆菌表达体系和色谱固色表征数据;
光生物反应器硬件原型(LED 阵列 + 3D 打印适配器)和配套的图案生成、光照调度软件;
GSMM / OptKnock 计算流水线代码、分子对接结构文件、干湿闭环数据集;
已发表 SCI 论文 1 篇(《Angew. Chem. Int. Ed.》,IF 16.9)、北大核心 1 篇,在申专利 48 项。


2. 目录结构 / Repository Layout
.
├── README.md                  # 你正在看的这份文件
├── LICENSE                    # 默认 MIT,必要时可替换
├── .gitignore
├── requirements.txt           # Python 依赖清单
├── Dockerfile                 # 一键复现的容器配置
├── attributions.md            # 项目贡献标注(每一行代码、每一份数据的来源都在这里)
│
├── src/
│   ├── ai/                    # AI / 计算代码
│   │   ├── README.md
│   │   ├── models/            # GSMM、OptKnock、分子对接、光照-表达回归模型
│   │   ├── data/              # 数据加载与预处理脚本
│   │   └── scripts/           # 训练 / 推理 / 评估的入口脚本
│   └── wet_lab/               # 与湿实验配套的脚本(数据分析、图表绘制等)
│       └── README.md
│
├── data/                      # 数据(大文件请配合 Git LFS 或公开数据集链接)
│   ├── raw/                   # 原始数据(光谱、色谱、发酵 OD/产量曲线等)
│   ├── processed/             # 处理后数据
│   └── README.md
│
├── notebooks/                 # 探索性分析与可视化(.ipynb)
├── docs/                      # 设计文档、技术备忘录、演示稿
├── results/                   # 关键结果与图表
│   ├── figures/
│   └── README.md
│
├── parts/                     # DNA 元件设计、序列与表征数据
│   └── README.md              # 含 RGB 响应启动子、产色通路、BmCBP 表达盒
│
├── safety/                    # 安全审批材料归档
│   ├── README.md
│   └── checkin_records/       # Check-In 记录
│
└── wiki/                      # 项目 Wiki 页面(评审依据之一)
    ├── Home.md
    ├── Project-Description.md
    ├── Design.md
    ├── AI-Computational-Methods.md   # 必设页面
    ├── Wet-Lab-Experiments.md         # 必设页面
    ├── Integrated-Validation.md
    ├── Verifiability.md
    ├── Engineering-Cycle.md
    ├── Parts.md
    ├── Human-Practices.md
    ├── AI-Ethics-Safety.md            # 必设页面
    ├── Education.md
    ├── Collaboration.md
    └── Attributions.md                # 必设页面

3. 快速开始 / Getting Started
3.1 环境准备
bash# 克隆仓库
git clone <your-repo-url> fabric
cd fabric

# 推荐用 conda 隔离环境(GSMM 依赖 COBRApy,对 Python 版本敏感)
conda create -n fabric python=3.10 -y
conda activate fabric

# 安装 Python 依赖
pip install -r requirements.txt

# 可选:用 Docker 一键拉起完整环境
docker build -t fabric:latest .
docker run -it --rm -v $(pwd):/workspace fabric:latest
3.2 一键复现关键结果
bash# 1) 跑 GSMM + OptKnock,复现虾青素产量提升 45% 的预测结果
python src/ai/scripts/run_optknock.py \
    --model data/raw/yeast_gsmm.xml \
    --target astaxanthin \
    --output results/figures/optknock_targets.csv

# 2) 跑分子对接,复现 BmCBP-色素结合能筛选
python src/ai/scripts/run_docking.py \
    --receptor data/raw/BmCBP.pdb \
    --ligands data/raw/pigments/ \
    --output results/figures/docking_scores.csv

# 3) 跑光照-色素表达回归,生成图案-光照方案映射
python src/ai/scripts/pattern_to_light.py \
    --input notebooks/demo_pattern.png \
    --output results/figures/light_schedule.json

# 4) 一键生成 Wiki 上 Figure 2-5 的所有图表
bash src/wet_lab/regen_figures.sh

完成度自查:当一位完全没接触过本项目的同行只跟着 README 操作,能在 1 小时内得到和 Wiki 上一致的关键数字(虾青素产量提升比例、BmCBP-色素结合能排序、典型图案的光照调度时长),"可验证性"就达标了。

## 4. 给评审 / 同行的快速导航

| 你想了解…… | 请打开 |
|---|---|
| 项目要解决什么问题、怎么做 | [`wiki/Project-Description.md`](./wiki/Project-Description.md) |
| AI 模型架构、数据、基线 | [`wiki/AI-Computational-Methods.md`](./wiki/AI-Computational-Methods.md) |
| 湿实验方案与原始数据 | [`wiki/Wet-Lab-Experiments.md`](./wiki/Wet-Lab-Experiments.md) |
| 干湿如何闭环 | [`wiki/Integrated-Validation.md`](./wiki/Integrated-Validation.md) |
| 第三方如何复现关键结果 | [`wiki/Verifiability.md`](./wiki/Verifiability.md) |
| AI 伦理与安全说明 | [`wiki/AI-Ethics-Safety.md`](./wiki/AI-Ethics-Safety.md) |
| 哪些部分是我们做的、哪些是站在巨人肩膀上 | [`attributions.md`](./attributions.md) |

---

## 5. 仓库同步说明 / Repository Sync Notes for AI Agents

本项目以 Gitee 仓库作为队伍协作主仓库，GitHub 仓库作为 AI 工具读取、审查和辅助修改的镜像入口。后续 AI 工具读取本仓库时，应先确认用户是否已经把 Gitee 最新内容同步到 GitHub；如果 GitHub 侧由 AI 工具产生了修改，应通过本地双远程仓库把修改合回 Gitee。

- Gitee 主仓库：`https://gitee.com/ai-synbio/guanghui-jiaoran.git`
- GitHub 镜像仓库：`https://github.com/bulbel-magnolia/guanghui-jiaoran.git`
- 当前默认分支：`master`

### 5.1 首次配置本地双远程仓库

```bash
# 1) 从 Gitee 克隆主仓库
git clone https://gitee.com/ai-synbio/guanghui-jiaoran.git
cd guanghui-jiaoran

# 2) 将默认远程名 origin 改为 gitee，避免后续混淆
git remote rename origin gitee

# 3) 添加 GitHub 镜像远程
git remote add github https://github.com/bulbel-magnolia/guanghui-jiaoran.git

# 4) 检查远程地址
git remote -v

# 5) 首次把 Gitee 当前内容推送到 GitHub
git push github master
git push github --tags
```

检查 `git remote -v` 时应看到两个远程仓库：

```text
gitee   https://gitee.com/ai-synbio/guanghui-jiaoran.git (fetch)
gitee   https://gitee.com/ai-synbio/guanghui-jiaoran.git (push)
github  https://github.com/bulbel-magnolia/guanghui-jiaoran.git (fetch)
github  https://github.com/bulbel-magnolia/guanghui-jiaoran.git (push)
```

### 5.2 Gitee 更新后，同步到 GitHub

当队友在 Gitee 提交新内容后，用下面命令把 Gitee 最新内容同步到 GitHub，供 AI 工具读取：

```bash
git checkout master
git status

# 从 Gitee 拉取最新 master，只允许快进合并，减少意外合并提交
git pull --ff-only gitee master

# 推送到 GitHub 镜像仓库
git push github master
git push github --tags
```

完成后刷新 GitHub 页面，确认文件列表、提交记录和 Gitee 保持一致。

### 5.3 GitHub 被 AI 修改后，同步回 Gitee

当 AI 工具或其他协作者在 GitHub 侧提交了修改后，用下面命令把 GitHub 的修改合并回 Gitee：

```bash
git checkout master
git status

# 先保证本地 master 与 Gitee 主仓库一致
git pull --ff-only gitee master

# 拉取 GitHub 侧最新提交
git fetch github

# 可选：查看最近提交图，确认 GitHub 侧新增了哪些提交
git log --oneline --graph --decorate --all -20

# 将 GitHub/master 合并到当前本地 master
git merge github/master

# 推回 Gitee 主仓库
git push gitee master

# 再推回 GitHub，保证两个远程仓库最终一致
git push github master
```

### 5.4 推荐的 AI 分支工作流

为了避免 AI 工具直接改动 `master`，建议在 GitHub 上使用专门的 AI 修改分支。例如：

```bash
# 从 Gitee 最新 master 创建 AI 工作分支
git checkout master
git pull --ff-only gitee master
git checkout -b ai-update-wiki

# 推送到 GitHub，交给 AI 工具修改
git push github ai-update-wiki
```

AI 修改完成后，再由本地检查并合并回主分支：

```bash
git checkout master
git pull --ff-only gitee master
git fetch github

git merge github/ai-update-wiki

git push gitee master
git push github master
```

### 5.5 冲突处理

如果 `git merge github/master` 或 `git merge github/<branch-name>` 出现冲突，先查看冲突文件：

```bash
git status
```

打开冲突文件，处理 Git 标记的冲突区：

```text
<<<<<<< HEAD
Gitee 当前版本
=======
GitHub / AI 修改版本
>>>>>>> github/master
```

保留最终需要的内容，删除冲突标记，然后提交合并结果：

```bash
git add .
git commit -m "Resolve sync conflicts from GitHub updates"
git push gitee master
git push github master
```

如需取消当前合并，执行：

```bash
git merge --abort
```

### 5.6 注意事项

- 不要把 GitHub Personal Access Token、Gitee 密码或任何访问令牌写入 README、Issue、Commit Message 或聊天记录。
- 默认分支目前是 `master`；如果后续改为 `main`，以上命令中的 `master` 需要同步替换为 `main`。
- GitHub 镜像主要服务于 AI 读取和辅助修改；Gitee 仍作为队伍协作与提交的主仓库。
- 在 Gitee 和 GitHub 同时独立修改同一个文件时，后续合并容易产生冲突。建议先同步，再修改，再合并。

---

## 6. 团队 / Team

| 姓名 | 角色 | 主要负责 |
|---|---|---|
| 赵博研 | 队长 |  |
| 徐士辰 | AI / 计算 |  |
| 张意帆 | 湿实验 |  |
| 慕金贝 | 人类实践 |  |
| 范运涵 | Primary PI |  |

---

## 7. 许可与引用 / License & Citation

- 代码以 MIT 协议开源（见 [`LICENSE`](./LICENSE)）。
- 提交至大赛 Registry 的 DNA 元件遵循大赛共享协议。
- 引用本项目：

```bibtex
@misc{your_team_2026,
  title  = {<Your Project Title>},
  author = {<Your Team>},
  year   = {2026},
  note   = {AI + 合成生物创新大赛 2026 赛季},
  url    = {<your-repo-url>}
}
```

---

## 8. 联系 / Contact

- 队长邮箱：1120240849@bit.edu.cn
- Primary PI 邮箱：binghu319@bit.edu.cn
- 大赛组委会：synbio@tju.edu.cn
