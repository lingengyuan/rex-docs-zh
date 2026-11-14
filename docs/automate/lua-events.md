> 原文：https://www.superlogical.com/rex/docs/automate/lua-events
> 原文版本：05299a522884（抓取于 2026-11-13）

# Lua 事件

[Lua 脚本](lua-scripts.md)可以保持持续运行并对 Rex 中发生的事件做出响应：终端更改目录、程序退出、窗口关闭、会话被创建等。脚本通过 `rex.on` 监听事件。

```lua
-- label.lua：用终端所在目录为各终端设置标签
rex.on("terminal.pwd_changed", function(ctx, ev)
  local dir = ev.pwd:match("([^/]+)/?$")
  rex.session.set_block_label{
    block_id = ctx.block_id,
    label    = dir,
  }
end)
```

```
$ rex do label.lua
listening: 1 handler, session work; Ctrl-C to stop
```

在该会话的任何终端中更改目录，其标签都会自动更新。

## 处理程序

`rex.on` 接收事件名称以及每次该事件发生时调用的函数：

```lua
rex.on(event, function(ctx, ev)
  -- ...
end)
```

调用 `rex.on` 的脚本在执行到最后一行时不会退出。`rex do` 会使其保持运行，并在事件到达时依次调用其处理程序。

处理程序在脚本首次运行时进行注册。在此之后从处理程序内部调用 `rex.on` 会引发错误。

`ev` 包含事件的字段，`ctx` 说明事件发生的上下文：

| 字段 | 说明 |
| --- | --- |
| `ctx.session_id` | 事件发生所在的会话。 |
| `ctx.block_id` | 事件来源的块（针对块事件）。 |

处理程序内部的 API 调用默认使用事件所在的会话，而非脚本启动时所在的会话，因此单个处理程序能够跨它监听到的所有会话工作。

## 事件名称

事件名称分为三类：

| 名称 | 匹配对象 |
| --- | --- |
| `block_closed`、`window_created`、... | 按类型匹配会话或服务端事件。 |
| `terminal.pwd_changed`、`terminal.bell`、... | 来自块的某一种事件。 |
| `block_event` | 来自所有块的所有事件。 |

块事件以块类型和事件名称命名，中间用点连接。`terminal.bell` 是 `com.superlogical.terminal.bell` 的简写形式。两种书写方式均可生效。

以下是常见事件：

| 事件 | 触发时机 | `ev` 上的字段 |
| --- | --- | --- |
| `terminal.pwd_changed` | 终端更改工作目录。 | `pwd`，一个 `file://` URL |
| `terminal.title_changed` | 终端标题发生更改。 | `title` |
| `terminal.bell` | 终端鸣响响铃。 | |
| `terminal.child_exited` | 终端中的程序退出。 | `exit_code` |
| `block_created`、`block_closed` | 块被创建或关闭。 | `block_id` |
| `window_created`、`window_closed` | 窗口被创建或关闭。 | `window_id` |
| `session_created`、`session_destroyed` | 会话被创建或销毁。 | |

完整列表请参阅[事件参考](../reference/events.md)。

Rex 不会根据预定义列表校验事件名称，因此拼写错误的名称不会报错。该处理程序将被注册但永远不会被调用。

## 事件作用域

默认情况下，脚本响应单个会话的事件：脚本在其内运行的会话，或通过 `-s` 指定的会话。

```sh
rex do label.lua            # 当前会话
rex do -s build label.lua   # 标签为 "build" 的会话
```

传入 `--all` 可监听所有会话，包括在脚本启动后创建的会话：

```sh
rex do label.lua --all
```

## 停止运行

包含处理程序的脚本会一直运行，直到发生以下情况之一：

- 处理程序调用 `rex.stop(code)`。`rex do` 会以该状态码退出，若省略则以 0 退出。
- 通过 `--for` 指定的时间耗尽，例如 `--for 10m`。
- 监听的会话被销毁。带 `--all` 运行的脚本永远不会因此停止。
- 按下 <kbd>Ctrl</kbd>+<kbd>C</kbd>。

```lua
-- 退出并返回首个失败程序的状态码
rex.on("terminal.child_exited", function(ctx, ev)
  if ev.exit_code ~= 0 then rex.stop(ev.exit_code) end
end)
```

## 处理程序失败

处理程序或[定时器](lua-scripts.md#定时器)中发生的错误会被打印出来，脚本继续保持运行，因此单个异常事件不会导致长期运行的脚本崩溃退出：

```
Error: watch.lua:7: attempt to index a nil value
```

传入 `--fail-fast` 可在首次失败时立即以状态码 1 退出。

请记住，失败的 API 调用会返回 `nil` 和错误消息而非抛出异常。在结果重要的位置请检查第二个返回值。

## 处理程序或 `rex.wait`

[`rex.wait`](lua-scripts.md#休眠与等待) 和 `rex.on` 均可接收事件，但适用于不同的脚本场景。

- 当脚本按顺序依次执行操作时使用 `rex.wait`：启动命令、等待命令退出、然后针对结果执行处理。
- 当脚本需要在运行期间对每次发生的特定情况都做出响应时，使用 `rex.on`。

`rex.wait` 和 `rex.sleep` 也可在处理程序内部使用。在它们返回之前，不会处理其他事件。

## 处理程序中的定时器

需要稍后执行某些操作的处理程序可以启动一个[定时器](lua-scripts.md#定时器)并立即返回，而不是休眠并阻塞其他所有事件。

这对于突发到来的事件非常有用。`session_view_changed` 几乎在每次布局发生变化后都会触发，因此以下代码在突发变动的最后一次发生 0.5 秒后调用一次 `export` 函数：

```lua
local pending
rex.on("session_view_changed", function(ctx, ev)
  if pending then pending:cancel() end
  pending = rex.after(0.5, export)
end)
```

定时器的 API 调用默认使用脚本启动所在的会话，而非事件所在的会话。若要作用于事件所在的会话，请显式传递 `ctx.session_id`：

```lua
rex.on("session_view_changed", function(ctx, ev)
  if pending then pending:cancel() end
  pending = rex.after(0.5, function()
    export(ctx.session_id)
  end)
end)
```

## 配置文件中无效

`rex.on` 仅在通过 `rex do` 运行的脚本中有效。[配置文件](../customize/config.md)不会接收事件，因此在其中注册的处理程序会被报告为警告且永远不会被调用。

若要让处理程序始终运行，请在启动会话时启动脚本，例如在专门为此保持打开的终端中启动。

## 示例：收到响铃时发送通知

许多程序在完成任务或需要关注时会鸣响终端响铃。该脚本将任何会话中任意终端的响铃转换为包含会话名称的 macOS 通知：

```lua
-- notify.lua
local function notify(title, text)
  rex.exec{
    "osascript", "-e",
    string.format("display notification %q with title %q", text, title),
  }
end

rex.on("terminal.bell", function(ctx, ev)
  local view = rex.session.view{}
  notify("Rex", "Bell in " .. view.label)
end)
```

```sh
rex do notify.lua --all
```

调用 `rex.session.view` 时未指定 `session_id`，因此它描述响铃发生所在的会话。这就是单个处理程序能够指明需要关注的具体会话的方式。
