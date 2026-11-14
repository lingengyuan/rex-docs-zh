# Rex 文档中文翻译

Rex 官方文档的社区中文译文。

- 原文：https://www.superlogical.com/rex/docs
- 非官方项目，与 Superlogical 无关，不代表官方立场
- 原文版权归 Superlogical 所有
- 译文采用 [CC BY-NC-SA 4.0](LICENSE)，不用于商业用途
- 官方要求时可随时下架

## 范围与阅读

已覆盖官方文档的全部公开页面，共 32 篇（均已译完）。登录 Discord 后才显示的内容（例如 Linux、FreeBSD 和 Windows 的安装命令）不在翻译范围内。

译文存放在 `docs/` 下，目录结构与官方文档一致，可从 [安装指南](docs/installation.md) 开始阅读。译文与原文不一致时，以原文为准。

| 章节 | 篇数 | 目录 |
| --- | --- | --- |
| Installation | 1 | [docs/installation.md](docs/installation.md) |
| Customize | 5 | [docs/customize](docs/customize) |
| Automate | 6 | [docs/automate](docs/automate) |
| Build for Rex | 1 | [docs/build](docs/build) |
| References | 9 | [docs/reference](docs/reference) |
| Server | 9 | [docs/linux](docs/linux)、[docs/freebsd](docs/freebsd)、[docs/windows](docs/windows) |
| Beta | 1 | [docs/beta](docs/beta) |

## 目录结构

```text
rex-docs-zh/
├── .github/workflows/    # 每日更新检查
├── docs/                 # 中文译文
├── originals/            # 原文快照与 manifest
├── tests/                # 验证工具单元测试
├── tools/                # sync.py、verify.py
├── pages.txt             # 页面清单
├── TRANSLATION.md        # 翻译规范
├── TRANSLATION-TASKS.md  # 翻译任务清单
└── glossary.md           # 术语表
```

## 译文格式

每篇译文开头记录原文地址和版本：

```markdown
> 原文：https://www.superlogical.com/rex/docs/installation
> 原文版本：1bbd80a7b3cc（抓取于 2026-11-13）
```

版本号取自 `originals/manifest.tsv`，`tools/sync.py` 用它判断译文是否落后。

## 维护

```sh
python3 tools/sync.py                  # 抓取原文，更新 originals/ 和 manifest
python3 tools/sync.py --dry-run        # 只检测，不写入
python3 tools/verify.py                # 校验清单中的全部 31 篇译文及任务清单
python3 tools/verify.py --page <路径>  # 校验单篇译文，例如 docs/automate/cli.md
python3 -m unittest discover tests     # 运行验证工具单元测试
```

`.github/workflows/docs-watch.yml` 每天 01:00 UTC（北京时间 09:00）运行：

1. 抓取 `llms.txt` 和各页 `.md`，与 `manifest.tsv` 对比。
2. 有变化时创建 `docs-update` 分支和 PR，只修改 `originals/` 和 `manifest.tsv`。
3. 创建或更新 `docs-update` 标签的 Issue。

有未合并的更新 PR 时，后续检查自动跳过。

## 贡献

翻译规范见 [TRANSLATION.md](TRANSLATION.md)，术语以 [glossary.md](glossary.md) 为准。修改 `docs/` 后请先运行 `python3 tools/verify.py` 确认校验通过，再提交 Pull Request。

注：[docs/installation.md](docs/installation.md) 按官网渲染页面补全了 `## macOS` 等小节，单独运行 `python3 tools/verify.py --page docs/installation.md` 时 `AC2_Structure` 会因与 `.md` 导出标题数不同而提示不匹配，属于已知差异。
