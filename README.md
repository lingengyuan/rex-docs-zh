# Rex 文档中文翻译

Rex 官方文档的社区中文译文。

原文：https://www.superlogical.com/rex/docs

> **非官方项目。** 本项目与 Superlogical 无关，不代表官方立场。
> 原文版权归 Superlogical 所有。译文采用 CC BY-NC-SA 4.0 许可。
> 如官方要求，本项目可随时下架。

## 范围

覆盖官方文档的全部公开页面，共 32 篇。登录 Discord 后才显示的内容，例如 Linux、FreeBSD 和 Windows 的安装命令，不在翻译范围内。

| 章节 | 篇数 | 目录 |
| --- | --- | --- |
| Installation | 1 | [docs/installation.md](docs/installation.md) |
| Customize | 5 | [docs/customize](docs/customize) |
| Automate | 6 | [docs/automate](docs/automate) |
| Build for Rex | 1 | [docs/build](docs/build) |
| References | 9 | [docs/reference](docs/reference) |
| Server | 9 | [docs/linux](docs/linux)、[docs/freebsd](docs/freebsd)、[docs/windows](docs/windows) |
| Beta | 1 | [docs/beta](docs/beta) |

## 阅读

译文在 `docs/` 下，目录结构与官方文档一致。每篇开头有原文链接和抓取日期。

官方文档更新较快。译文与原文不一致时，以原文为准。

## 目录结构

```text
rex-docs-zh/
├── docs/          # 中文译文
├── originals/     # 官方原文快照，用于校对和更新检测
├── tools/         # 抓取与更新检测脚本
├── pages.txt      # 页面清单
└── glossary.md    # 术语表
```

## 维护

```sh
tools/fetch.sh          # 抓取最新原文到 originals/
tools/check-updates.sh  # 比较线上原文与快照，列出变化的页面
```

`originals/manifest.tsv` 记录每篇原文的 SHA-256 和抓取时间。`check-updates.sh` 用它们找出需要重译的页面。

## 贡献

1. 修改 `docs/` 下的 Markdown。
2. 术语以 `glossary.md` 为准。
3. 提交 Pull Request。

## 许可

- 原文版权归 Superlogical 所有。
- 译文采用 [CC BY-NC-SA 4.0](LICENSE)。
- 本项目不用于商业用途。

Rex 由 Superlogical 开发：https://www.superlogical.com
