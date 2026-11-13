# Rex 文档中文翻译

Rex 官方文档的社区中文译文。

- 原文：https://www.superlogical.com/rex/docs
- 非官方项目，与 Superlogical 无关，不代表官方立场
- 原文版权归 Superlogical 所有
- 译文采用 [CC BY-NC-SA 4.0](LICENSE)，不用于商业用途
- 官方要求时可随时下架

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

译文在 `docs/` 下，目录结构与官方文档一致。译文与原文不一致时，以原文为准。

## 目录结构

```text
rex-docs-zh/
├── .github/workflows/  # 每日更新检查
├── docs/               # 中文译文
├── originals/          # 原文快照与 manifest
├── tools/              # sync.py
├── pages.txt           # 页面清单
└── glossary.md         # 术语表
```

## 译文格式

每篇译文开头记录原文地址和版本：

```markdown
> 原文：https://www.superlogical.com/rex/docs/installation
> 原文版本：1bbd80a7b3cc（抓取于 2026-11-14）
```

版本号取自 `originals/manifest.tsv`，`tools/sync.py` 用它判断译文是否落后。

## 维护

```sh
tools/sync.py            # 抓取原文，更新 originals/ 和 manifest
tools/sync.py --dry-run  # 只检测，不写入
```

`.github/workflows/docs-watch.yml` 每天 01:00 UTC（北京时间 09:00）运行：

1. 抓取 `llms.txt` 和各页 `.md`，与 `manifest.tsv` 对比。
2. 有变化时创建 `docs-update` 分支和 PR，只修改 `originals/` 和 `manifest.tsv`。
3. 创建或更新 `docs-update` 标签的 Issue。

有未合并的更新 PR 时，后续检查自动跳过。

## 贡献

修改 `docs/` 下的 Markdown，术语以 `glossary.md` 为准，然后提交 Pull Request。
