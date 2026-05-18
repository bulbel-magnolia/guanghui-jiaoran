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

## 5. 团队 / Team

| 姓名 | 角色 | 主要负责 |
|---|---|---|
| 赵博研 | 队长 |  |
| 徐士辰 | AI / 计算 |  |
| 张意帆 | 湿实验 |  |
| 慕金贝 | 人类实践 |  |
| 范运涵 | Primary PI |  |

---

## 6. 许可与引用 / License & Citation

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

## 7. 联系 / Contact

- 队长邮箱：1120240849@bit.edu.cn
- Primary PI 邮箱：binghu319@bit.edu.cn
- 大赛组委会：synbio@tju.edu.cn
