---
name: my-skill-open-games
description: 查询 bobeff/open-source-games 全部条目及达到 100 Star 的 GitHub 补充游戏，按类别或名称查找并核对语言、引擎、构建工具和开源许可证。用于查询开源游戏目录、技术对比及寻找更多项目。
---

# my-skill-open-games

目录包含 [bobeff/open-source-games](https://github.com/bobeff/open-source-games) 的全部条目和 [已核验的 GitHub 补充游戏](references/github-games.md)。补充项目在录入时有至少 100 Star 和明确的源码开源许可证。技术栈以各项目的官方源码为准。

## 查目录

从 Skill 目录运行 Python 3.9 或更新版本。无参数时列出游戏分类，传入 README 的实际标题时返回该分类的条目和链接。默认查询两份目录并按仓库地址去重。

    python -X utf8 scripts/read_catalog.py
    python -X utf8 scripts/read_catalog.py "City-Building games"
    python -X utf8 scripts/read_catalog.py --find "OpenTTD"
    python -X utf8 scripts/read_catalog.py "Tower Defence games" --match "tower[- ]defen[cs]e|塔防"
    python -X utf8 scripts/read_catalog.py --all
    python -X utf8 scripts/read_catalog.py --scope github --all
    python -X utf8 scripts/read_catalog.py --scope upstream --all

脚本优先读上游主分支，网络失败时提示改用 [内置 README](references/catalog.md)。用 --snapshot 可直接读取 [内置版本 3a9ab8f](https://github.com/bobeff/open-source-games/blob/3a9ab8fc892a2cdadf8989a72ba7624a11e39cec/README.md)，它保留了 [原始 CC0 许可证](references/catalog-license.txt)。没有 Python 时，直接浏览上游 README 并读取补充目录。说明使用的上游版本和查询范围。

- 根据中文玩法映射目录标题。先查直接收录的项目，再用 --match 搜寻其他分类的同类玩法。用官方说明确认候选并标注原分类。用户指定只查单一分类时，按该分类回答。
- 以官方仓库或官网确认项目身份，合并重复地址，保留独立移植和重实现。若一条同时链接游戏和引擎，分别确认用途。用户要全部条目或全部技术栈时，按上游顺序覆盖两份清单，保留证据不足的条目并标注待核实字段。
- 对新增候选，检查两份目录是否已收录。核对项目官方仓库、实际玩法、开源许可证和 Star 数。新增条目默认至少 100 Star，用户可指定其他口径。原目录沿用上游的收录范围。补充清单的 Star 数是录入时的快照，用户问当前值或要求按 Star 数筛选时，查 GitHub 当前数据。
- 上游 Other lists 是外部目录链接。按用户要求使用外部目录和搜索发现候选，通过对应项目的官方来源确认后再引用。

## 查技术栈

- 看官方 README、构建清单、入口和核心代码的依赖。若目录源码链接错配或失效，沿项目官网、官方组织或迁移说明找新址。
- 区分主要语言、核心引擎或框架、运行时依赖和构建工具。Web 项目的依赖也可能从 HTML 或入口模块加载。对移植版使用该版证据。目录里的主要语言来自 GitHub 仓库元数据，进一步核对时以代码为准。
- 用 LICENSE 或官方发布说明核实源码许可。项目若仍需原版游戏数据则注明。用户关心改编和分发时另外查素材许可。
- 每款附官方源码和能支持主要技术结论的依据。比较多个项目时，可用表格列出游戏、分类、技术栈、源码许可及证据链接。无法核实的字段标为「未核实」。
