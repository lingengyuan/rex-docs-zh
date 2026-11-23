# Rex 文档中文翻译

Rex 官方文档的社区中文译文。

- 原文：https://www.superlogical.com/rex/docs
- 非官方项目，与 Superlogical 无关，不代表官方立场
- 原文版权归 Superlogical 所有
- 译文采用 [CC BY-NC-SA 4.0](LICENSE)，不用于商业用途
- 官方要求时可随时下架

## 范围与阅读

已覆盖官方文档的全部公开页面，共 33 篇（均已译完）。登录 Discord 后才显示的内容（例如 Linux、FreeBSD 和 Windows 的安装命令）不在翻译范围内。

译文存放在 `docs/` 下，目录结构与官方文档一致，完整导航也同步放在 [docs/README.md](docs/README.md)。译文与原文不一致时，以原文为准。

### 阅读目录（按官网侧边栏顺序）

- [安装](docs/installation.md)

**Customize（自定义）**
1. [配置文件](docs/customize/config.md)
2. [快捷键](docs/customize/keyboard-shortcuts.md)
3. [按键序列](docs/customize/key-sequences.md)
4. [按键模式](docs/customize/key-modes.md)
5. [自定义操作](docs/customize/actions.md)
6. [自定义 UI](docs/customize/custom-ui.md)

**Automate（自动化）**
1. [CLI](docs/automate/cli.md)
2. [智能体](docs/automate/agent-skill.md)
3. [Lua 脚本](docs/automate/lua-scripts.md)
4. [Lua 事件](docs/automate/lua-events.md)
5. [Shell 脚本](docs/automate/shell-scripting.md)
6. [服务端 API](docs/automate/server-api.md)

**Build for Rex（面向 Rex 开发）**
1. [程序状态协议（OSC 7501）](docs/build/program-status.md)

**References（参考）**
1. [CLI 命令](docs/reference/cli.md)
2. [服务端 API](docs/reference/api.md)
3. [Mac 操作](docs/reference/mac-actions.md)
4. [Mac 设置](docs/reference/mac-settings.md)
5. [iOS 操作](docs/reference/ios-actions.md)
6. [iOS 设置](docs/reference/ios-settings.md)
7. [Rex Lua API](docs/reference/lua.md)
8. [事件](docs/reference/events.md)
9. [隐私与遥测](docs/reference/privacy.md)

**Server（服务端）**
- **Linux**：[在 Linux 上安装](docs/linux/installation.md) → [服务端运行模式](docs/linux/server-modes.md) → [共享服务端](docs/linux/shared-server.md) → [登录服务端](docs/linux/login-server.md) → [远程访问](docs/linux/remote-access.md) → [升级](docs/linux/upgrading.md)
- **FreeBSD**：[在 FreeBSD 上安装](docs/freebsd/installation.md)
- **Windows**：[在 Windows 上安装](docs/windows/installation.md) → [在 Windows 上运行](docs/windows/running.md)

**Beta**
1. [社区 MCP](docs/beta/community-mcp.md)

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
