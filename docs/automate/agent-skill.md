> 原文：https://www.superlogical.com/rex/docs/automate/agent-skill
> 原文版本：f6e761f139d5（抓取于 2026-11-13）

# 智能体

Rex 内置了智能体 Skill，使 Claude Code 或 Codex 等智能体能够高效打开标签页、拆分窗格、读取终端屏幕、控制已连接的 Rex 应用等。

即使没有该 Skill，现代智能体也足够智能，能够发现并使用 [`rex` CLI](cli.md) 来执行任务，但使用该 Skill 效率更高，因此推荐使用。达成相同任务所需的时间更短，消耗的 Token 也更少。

## 智能体能做什么

以下是智能体配合 Rex 可以完成的一些操作示例：

| 用户指令 | 智能体操作 |
| --- | --- |
| “打开 nvim，并在右侧窄窗格中运行 top。” | 打开一个标签页并聚焦编辑器，右侧三分之一区域分配给 `top`。 |
| “在另一个标签页中启动开发服务器，准备就绪后告诉我。” | 启动服务器而不抢占焦点，随后持续读取该标签页，直到服务器提示正在监听。 |
| “在你身旁运行测试，并修复所有失败项。” | 在分屏中运行测试，等待测试完成，从屏幕读取失败信息后进行修复。 |
| “在 psql 窗格中运行 `\dt` 并告诉我里面有什么。” | 向 psql 输入命令，按下回车键，并读取返回结果。 |
| “将我的 Mac 切换到该会话并调大字号。” | 请求该 Mac 上的应用显示此会话并调大字体。 |
| “关闭你打开的所有内容。” | 关闭由它创建的标签页和窗格，其他内容保持原样。 |

更改应用本身的操作（例如将 Mac 切换到某个会话），需要该应用保持运行且在其设置中开启了 Remote Control。

## 设置智能体

在 macOS 上，从命令面板运行 **Install Rex for Agents**。按 <kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> 打开命令面板。

在 CLI 中，`rex skill setup` 会查找本机已安装的智能体并为每一个进行配置。如果后续安装了新智能体，多次重复运行该命令是安全的。

```
$ rex skill setup
Claude Code
  skill  created      ~/.claude/skills/rex

Codex, OpenCode, Pi
  skill  created      ~/.agents/skills/rex

...

Start a new agent session inside Rex to use it.
```

这会安装两项内容：

- **Skill** 向智能体传授 `rex` 命令及适用场景。它直接从已安装的 `rex` 中读取指南，因此升级 Rex 会自动更新智能体掌握的知识，无需重新运行设置。
- **钩子（Hook）** 在每次会话启动时告知智能体它正在 Rex 中运行，以及它所处的会话和终端，避免智能体花费额外时间和 Token 去探查。

Rex 会将钩子添加到智能体的设置文件中，并保持该文件的其余部分不变。再次运行设置会将已是最新的项报告为 `unchanged`，并更新任何由旧版 Rex 安装的内容。

Rex 通过智能体的配置目录（例如 `~/.claude`）或其位于 `PATH` 中的程序来发现智能体。若要设置 Rex 未检测到的智能体，可使用 `--agent` 指定其名称。所有可用选项如下：

| 选项 | 说明 |
| --- | --- |
| `--agent NAME` | 仅配置指定的智能体，无论 Rex 是否检测到它。可重复传入以指定多个。 |
| `--dry-run` | 仅报告将发生的变更，不修改任何内容。 |
| `--project` | 配置当前仓库而非个人账户。 |
| `--force` | 替换非 Rex 安装的名为 `rex` 的 Skill。 |
| `--session-naming` | 让智能体主动以其任务为主体命名会话。再次运行设置若不带该参数，将保留已安装的选择。 |
| `--json` | 以 JSON 格式输出结果。 |

### 批准钩子

部分智能体在允许之前不会运行新钩子：

- **Codex** 在运行新增或修改的钩子前会发起询问。在 Codex 中使用 `/hooks` 批准 Rex 的钩子。在此之前，Codex 会跳过该钩子。
- **Claude Code** 不会逐个询问每个钩子，但在信任其启动所在的目录之前，它不会运行任何钩子。

## 支持的智能体

`rex skill setup` 支持配置以下智能体：

| 智能体 | `--agent` | Skill | 钩子 |
| --- | --- | --- | --- |
| Claude Code | `claude` | `~/.claude/skills/rex` | `~/.claude/settings.json` |
| Codex | `codex` | `~/.agents/skills/rex` | `~/.codex/hooks.json` |
| OpenCode | `opencode` | `~/.agents/skills/rex` | 不支持 |
| Pi | `pi` | `~/.agents/skills/rex` | 不支持 |

Rex 遵循用于重定向智能体目录的环境变量，例如 `CLAUDE_CONFIG_DIR` 和 `CODEX_HOME`。

任何能够在 Rex 终端中运行命令的其他智能体也均可使用 Rex。`rex skill show` 会输出该 Skill 提供给智能体的指南，因此可指示智能体运行该命令并遵循该指南。

后续将持续添加对更多常见智能体的支持。

## 工作原理

智能体与其他程序一样在 Rex 终端中运行，因此它拥有与 Shell 相同的 `REX_SESSION` 和 `REX_BLOCK` [环境变量](cli.md#命令目标)。这些变量告知智能体它当前所处的会话和终端。

当前查看的会话可能与智能体所在的会话不同。智能体会根据指令内容选择在何处执行操作：

- **“这里”、“你身旁”或未做指定：** 智能体自身的会话和终端。
- **“当前聚焦窗格”或“当前标签页”：** 当前正在查看的会话中拥有焦点的窗格或标签页。
- **指定名称：** 带有该标签的会话、标签页或窗格。指定名称的优先级始终高于智能体自身位置和应用的焦点。

在 Rex 外部启动的智能体没有 `REX_SESSION`。它会使用 `rex ls` 列出会话并在符合指令的会话中工作；当有多个会话匹配时，会提示进行选择。

## 移除 Skill

`rex skill remove` 会从 Rex 已知的所有智能体中移除 Skill 和钩子，包括在此之后卸载的智能体：

```sh
rex skill remove
```

只有由 Rex 安装的内容会被移除，包括旧版 Rex 遗留在智能体读取的其他目录中的 Skill 副本。其他 Skill、其他钩子以及各设置文件的其余部分保持不变。`--agent`、`--project` 和 `--dry-run` 的用法与 `rex skill setup` 相同。

Codex 根据钩子在 `hooks.json` 中的位置来记录已批准的钩子。如果移除或更新 Rex 的钩子导致其后的钩子位置发生变动，Codex 会要求重新批准这些钩子，Rex 也会在输出中做出提示。

## 调试

`rex skill status` 报告各智能体中安装的内容，不更改任何设置：

```
$ rex skill status
Claude Code (found)
  skill  current      ~/.claude/skills/rex
  hook   current      ~/.claude/settings.json

Codex (found)
  skill  outdated     ~/.agents/skills/rex
  hook   current      ~/.codex/hooks.json
...

Run "rex skill setup" to install or update the skill.
```

| 状态 | 含义 |
| --- | --- |
| `current` | 已安装且为最新版本。 |
| `outdated` | 由旧版 Rex 安装，或在此后被修改。`rex skill setup` 会将其更新。 |
| `missing` | 未安装。 |
| `foreign` | 存在名为 `rex` 但非 Rex 安装的 Skill。除非传入 `--force`，否则 `rex skill setup` 不会修改它。 |
| `unreadable` | 文件无法读取。 |
| `unsupported` | 智能体不支持此项，例如不支持钩子的智能体中的钩子。 |

如果智能体似乎不知道自己处于 Rex 中，请确认其会话是在运行 `rex skill setup` 之后启动的，因为钩子仅在会话启动时执行。在 Codex 中，确认钩子已通过 `/hooks` 批准。在 Claude Code 中，确认已信任该目录。
