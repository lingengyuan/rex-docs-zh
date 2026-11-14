> 原文：https://www.superlogical.com/rex/docs/automate/shell-scripting
> 原文版本：e23665fce370（抓取于 2026-11-13）

# Shell 脚本

也可以配合常见的 Shell 脚本使用 [`rex` CLI](cli.md) 来实现 Rex 中各项操作的自动化：

```sh
#!/bin/sh
rex new work
rex split -s work -- htop
rex run -s work --label logs -- tail -f app.log
```

如果不仅是连续执行几条命令，建议改用 [Lua 脚本](lua-scripts.md)。Lua 仅需与服务端建立一次连接即可完成本页展示的所有操作，且无需解析 JSON。

## 记录与跟踪 ID

创建资源的命令在添加 `--json` 参数时会输出其 ID。保存该 ID 并传递给后续命令，这样即使标签被更改或焦点发生移动，脚本也能正常工作。

```
$ rex split --json -- htop
{
  "anchor_block_id": "block:01a10e00-7268-78c6-8b85-86c56d6a53a9",
  "block_ids": [
    "block:01a10e00-729d-7c38-90f7-d6568611b1c4"
  ],
  "split_ids": [
    "split:01a10e00-72ab-7157-b9e0-0d4c2a8a1a68"
  ],
  "revision": 2
}
```

[`jq`](https://jqlang.org) 是提取 ID 最便捷的方式：

```sh
block=$(rex split --json -- htop | jq -r '.block_ids[0]')
rex zoom -b "$block"
```

| 命令 | 创建内容 | ID 所在位置 |
| --- | --- | --- |
| `rex new --json` | 包含一个窗口和一个终端的会话 | `.session_id` |
| `rex run --json` | 新窗口中的终端 | `.block_ids[0]`、`.window_id` |
| `rex split --json` | 现有终端旁的分屏终端 | `.block_ids[0]` |

如果由脚本主动设置标签，使用标签也是一种不错的方式。使用 `--label` 为块指定标签，并将其作为目标：

```sh
rex split --label logs -- tail -f app.log
rex capture -b logs
```

## 构建布局

`rex new` 创建会话，`rex run` 向其中添加窗口，`rex split` 则拆分现有块。

```sh
#!/bin/sh
# 打开项目：上方是编辑器，下方是 shell；
# 第二个窗口用于跟随日志。
rex new api --cwd ~/src/api -- nvim
rex split -s api --split=below --ratio 30 --cwd ~/src/api
rex run -s api --label logs --focus=false -- tail -f ~/src/api/app.log
```

`rex run` 和 `rex split` 共用以下选项：

| 选项 | 说明 |
| --- | --- |
| `-- COMMAND` | 运行指定命令而非交互式 Shell。 |
| `--cwd DIR` | 设置工作目录。 |
| `--label TEXT` | 为新块设置标签。 |
| `--split DIRECTION` | 将块放置在其锚点的 `right`、`left`、`above` 或 `below`。 |
| `--ratio PCT` | 分配给新块的分屏占比。 |
| `--focus=false` | 保持原有焦点不变。 |
| `--keep-open` | 命令退出后保持终端打开。 |

命令以登录 Shell 的环境运行，因此 `PATH` 会生效，但别名（alias）不会生效。命令本身不会由 Shell 进一步解析。若要使用管道或 `&&`，请显式运行 Shell：

```sh
rex run -- sh -c 'make build && make test'
```

## 向终端输入文本

`rex send` 向终端输入文本，`rex send-key` 则模拟按键操作：

```sh
rex send -b logs 'make test'
rex send-key -b logs enter
```

`rex send` 不会自动按下回车键。请在后面跟上 `rex send-key enter`，或者在输入文本中包含换行符。它也支持从标准输入读取：

```sh
printf 'make test\n' | rex send -b logs
```

`rex send-key` 使用与[快捷键](../customize/keyboard-shortcuts.md#编写按键格式)相同的按键名称，因此 `rex send-key ctrl+c` 可中断正在运行的程序。

## 读取终端屏幕

`rex capture` 打印终端屏幕内容及其回滚缓冲区：

```
$ rex capture -b logs --trim
hello from logs
```

| 选项 | 说明 |
| --- | --- |
| `--trim` | 移除末尾空白行。 |
| `--unwrap` | 合并终端自动折行的文本。 |
| `--format html` | 保留颜色与样式，输出为 HTML。 |
| `--format vt` | 保留终端控制序列。 |

终端保留约 64 MiB 的回滚缓冲区。在 80 列宽度下大约相当于 100,000 行纯文本；在更宽的终端中或存在样式输出时行数会相应减少。一旦达到上限，最旧的行将被丢弃。若要完整保留长命令打印的所有内容，请将其输出重定向到文件。

全屏程序（例如编辑器、分页器以及众多 TUI 应用）绘制在没有回滚缓冲区的独立屏幕上。在这类程序运行期间，`rex capture` 仅返回该程序当前所显示的内容。其历史记录（例如编辑器的文件内容或聊天应用较早的消息）仍保存在程序内部。

## 运行命令并等待

在 `rex run` 或 `rex split` 中添加 `--wait` 可等待命令执行完毕。随后 `rex` 命令将以该命令自身的退出状态码退出：

```sh
if rex run --wait -- make test; then
  echo "tests passed"
fi
```

`rex wait` 对已在运行的终端执行相同操作，传入其 ID 或标签即可：

```sh
block=$(rex split --json -- make test | jq -r '.block_ids[0]')
# ... 执行其他操作 ...
rex wait "$block"
echo "make exited with $?"
```

`rex wait` 也支持传入窗口或会话，并在其关闭时返回。

使用 `--for` 可在超过指定时间后放弃等待。超时的等待将以状态码 1 退出：

```sh
rex wait --for 10m "$block" || echo "failed or timed out"
```

## 执行操作

`rex do` 按名称执行操作，参数以 `key=value` 键值对形式传递。它既支持运行应用自身的操作，也支持运行配置文件中的[自定义操作](../customize/actions.md)：

```sh
rex do dev_layout file=app.log
rex do pane.split direction=right
```

诸如 `pane.split` 等操作由应用执行，因此应用必须处于运行状态，并在其设置中开启了 Remote Control。

## 监听事件

`rex events` 实时打印发生的事件并持续运行直到被中断。配合 `-s` 可跟踪单个会话：

```
$ rex events -s work
14:38:07  block_created         …65951c  session …8f9d5d
14:38:07  session_view_changed  …8f9d5d  revision 11
14:38:07  block_event           …65951c  com.superlogical.terminal.bell {}
```

配合 `--json` 可每行输出一个 JSON 对象，便于 `jq` 解析。以下示例输出鸣响响铃的每个终端的 ID：

```sh
rex events -s work --json |
  jq -r 'select(.payload.event.payload.name == "bell")
         | .payload.event.payload.block_id'
```

[事件参考](../reference/events.md#cli-中的事件)说明了 JSON 格式并列出了所有事件。若需对事件执行响应操作而非单纯打印，使用 [Lua 事件处理程序](lua-events.md)相比管道会轻松得多。

## 示例：在分屏中运行测试

该脚本在当前终端旁的分屏中运行命令。如果命令失败，它会放大该分屏并以失败状态退出。

```sh
#!/bin/sh
# tests.sh
cmd="${1:-make test}"

block=$(rex split --keep-open --focus=false --json -- sh -c "$cmd" |
  jq -r '.block_ids[0]')

if ! rex wait --for 10m "$block"; then
  rex zoom -b "$block" --on
  exit 1
fi
```

```sh
./tests.sh 'go test ./...'
```

[对应的 Lua 脚本](lua-scripts.md#示例在分屏中运行测试)是一个很好的对照参考。
