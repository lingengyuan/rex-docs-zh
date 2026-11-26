> 原文：https://www.superlogical.com/rex/docs/reference/events
> 原文版本：0fed8f7e22f8（抓取于 2026-11-26）

# 事件

每当有状态发生变更时，Rex 就会发出一个事件：窗口打开、终端更改目录、程序退出、会话被销毁等。可以在 Lua 中使用 [`rex.on` 与 `rex.wait`](../automate/lua-events.md) 处理事件，也可以在 CLI 中使用 `rex events` 流式获取事件。

事件来源于三个地方：

| 类别 | 描述 | Lua 名称 |
| --- | --- | --- |
| [会话事件](#会话事件) | 描述单个会话的窗口、块和客户端的变更。 | 事件的类型，例如 `block_closed`。 |
| [终端事件](#终端事件) | 终端所上报的内容。 | `terminal.` 加上事件名称，例如 `terminal.bell`。 |
| [服务端事件](#服务端事件) | 整个服务端的变更。 | 事件的类型，例如 `session_created`。 |

## Lua 中的事件

处理程序被调用时会接收 `ctx` 和 `ev`。本页中为每个事件列出的字段都可以直接在 `ev` 上访问：

```lua
rex.on("terminal.child_exited", function(ctx, ev)
  print(ctx.block_id, ev.exit_code)
end)
```

每个 `ev` 还具有以下字段：

| 字段 | 说明 |
| --- | --- |
| `ev.type` | 事件的类型。对于所有终端事件，该值均为 `block_event`。 |
| `ev.session_id` | 事件发生所在的会话。大多数服务端事件不包含此字段。 |
| `ev.payload` | 再次包含事件本身的各个字段，以独立的表形式提供。 |

终端事件以及任何其他块事件还会增加以下字段：

| 字段 | 说明 |
| --- | --- |
| `ev.block_id` | 事件来源的块。 |
| `ev.creator_name` | 块的类型，例如 `com.superlogical.terminal`。 |
| `ev.name` | 不带创建者前缀的事件名称，例如 `bell`。 |

`ctx.session_id` 和 `ctx.block_id` 保存相同的 ID，也是处理程序内部 API 调用默认使用的 ID。

注册 `block_event` 可以接收来自所有块的每一个事件，并可通过 `ev.creator_name` 和 `ev.name` 对它们进行区分。

## 会话事件

此类事件描述单个会话。脚本会接收其运行所针对的会话的事件，若指定 `--all` 则接收所有会话的事件。

| 事件 | 触发时机 | 字段 |
| --- | --- | --- |
| `window_created` | 创建窗口。 | `window_id`, `label` |
| `window_closed` | 关闭窗口。 | `window_id` |
| `window_label_changed` | 重命名窗口。 | `window_id`, `label` |
| `active_window_changed` | 另一个窗口变为活动窗口。 | `window_id` |
| `block_created` | 创建块。 | `block_id` |
| `block_closed` | 关闭块。 | `block_id` |
| `session_label_changed` | 重命名会话。 | `label` |
| `session_view_changed` | 会话布局发生任何变化。 | `revision` |
| `client_connected` | 客户端连接到会话。 | `client_id`, `principal`, `connected_at` |
| `client_disconnected` | 客户端断开与会话的连接。 | `client_id`, `principal` |
| `client_connection_changed` | 已连接客户端的连接断开或恢复。 | `client_id`, `principal`, `connection_state` |
| `creator_changed` | 会话可以创建的块类型发生变更。 | |

`session_view_changed` 紧随本表中几乎所有其他事件之后触发，因为大多数事件都会改变布局。通过处理该事件可对任何结构变化做出响应，并可调用 `rex.session.view` 获取新的布局。

## 终端事件

此类事件来源于终端块。在 Lua 中，可以写作 `terminal.` 后跟事件名称，或者写作完整形式 `com.superlogical.terminal.` 后跟事件名称。

| 事件 | 触发时机 | 字段 |
| --- | --- | --- |
| `terminal.child_exited` | 终端的程序退出。 | `exit_code`，非零时还包含 `error` |
| `terminal.pwd_changed` | 程序上报新的工作目录。 | `pwd`, `owner` |
| `terminal.title_changed` | 终端标题发生变化。 | `title`, `owner` |
| `terminal.bell` | 终端收到响铃字符。 | |
| `terminal.process_changed` | 前台进程发生变更。 | `generation`, `foreground`, `ancestors` |
| `terminal.desktop_notification` | 程序请求桌面通知。 | `title`, `body` |
| `terminal.progress_report` | 程序上报进度。 | `state`, `progress` |
| `terminal.clipboard_written` | 程序向剪贴板写入内容。 | `text` |
| `terminal.program_status_changed` | 程序上报或更新其状态。 | `id`, `record`, `reason` |
| `terminal.program_status_removed` | 程序状态记录被移除。 | `ids`, `reason` |
| `terminal.program_resume_changed` | 终端的程序恢复（Program Resume）记录发生变更。 | `records`, `reason` |

关于上述事件的几点说明：

- `terminal.child_exited` 针对终端所启动的程序（通常是你的 Shell）。它不会在 Shell 内部运行的每个命令退出时触发。通过 `command` 启动的终端会在该命令退出时触发此事件。
- `pwd` 是一个形如 `file://hostname/Users/you/src` 的 URL，而非普通路径。它仅由配置了上报功能的 Shell 进行上报。
- `owner` 是一个包含引起变更的进程的 `pid` 与 `name` 的表。
- `foreground` 是一个描述前台进程的表，包含 `name`、`cwd`、`pid` 等字段。它可以为 `nil`。
- `records` 是终端最新的完整[程序恢复](https://www.superlogical.com/rex/docs/build/program-resume.md)记录列表。每条记录包含 `owner`、`program`、`cwd`、`reported_at`、`chosen`、`trusted`、`rule` 和 `untrusted_reason`，其中为 false 或空的字段会被省略。由于命令中可能包含敏感信息且所有监听者都会收到该事件，因此记录中不包含命令内容。如需读取命令，请调用终端的 `program_resume_records` [方法](../automate/server-api.md#块方法)。
- `terminal.program_resume_changed` 中的 `reason` 为 `report`、`clear`、`rejected`、`owner_exited` 或 `rules_changed`。较新的服务端可能会增加更多原因。

## 服务端事件

此类事件描述服务端而非单个会话。在 Lua 中，脚本在携带 `--all` 运行时会接收此类事件。

| 事件 | 触发时机 | 字段 |
| --- | --- | --- |
| `session_created` | 创建会话。 | `session`（包含 `session_id` 和 `label` 的表） |
| `session_destroyed` | 销毁会话。 | `session_id` |
| `client_joined` | 客户端连接到服务端。 | `client` |
| `client_left` | 客户端断开与服务端的连接。 | `client_id` |
| `client_changed` | 已连接客户端的详细信息变更。 | `client` |
| `keymap_changed` | 配置文件重新加载。 | `generation`, `hash` |
| `hosts_changed` | 主机列表发生变更。 | `hash` |
| `tailscale_status_changed` | 服务端的 Tailscale 状态发生变更。 | |

`client` 是一个表，包含客户端的 `client_id`、`info`（其 `kind`、`name`、`platform` 和 `version`）、`principal` 以及 `connected_at`。

## CLI 中的事件

`rex events --json` 每行打印一个 JSON 对象。每个对象均包含 `type` 以及保存本页所列字段的 `payload`：

```json
{"type":"session_created","payload":{"session":{"session_id":"session:01a1...","label":"work"}}}
```

会话事件到达时会被包装在 `session_event` 中，其中增加了该事件所属的会话。终端事件还会额外多包装一层，封装在 `block_event` 中（此处分为多行展示）：

```json
{"type":"session_event","payload":{
  "session_id":"session:01a1...",
  "event":{"type":"block_event","payload":{
    "block_id":"block:01a1...",
    "creator_name":"com.superlogical.terminal",
    "name":"child_exited",
    "payload":{"exit_code":2,"error":"exit status 2"}}}}}
```

Lua 会自动剥除这两层包装，这也是处理程序能够直接在 `ev` 上访问 `exit_code` 的原因。

`rex events` 打印的内容取决于其作用范围：

| 命令 | 打印内容 |
| --- | --- |
| `rex events` | 会话的创建、销毁与变更。 |
| `rex events -s SESSION` | 单个会话中的全部内容，包含终端事件。 |
| `rex events --all` | 全部内容，包含客户端的加入与离开。 |

## 未知事件

Rex 的新版本会增加新的事件和字段。Rex 从不对照预设列表校验事件名称，因此可以为仅在更新版本服务端中发送的事件注册处理程序。对于无法识别的字段，应当直接忽略，而非将其视为错误。
