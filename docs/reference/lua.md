> 原文：https://www.superlogical.com/rex/docs/reference/lua
> 原文版本：737ecc692c7f（抓取于 2026-11-13）

# Lua API

本页列出 Rex 提供的完整 Lua API。Rex 仅向全局 `rex` 表添加 API。Rex 运行 Lua 5.1 并提供完整的标准库，包括 `io`、`os` 和 `require`。唯一的例外是 `io.popen` 和 `os.execute`，调用它们会引发错误。请改用 [`rex.exec`](#rexexecargv-opts) 运行命令。

## 各函数的适用环境

Rex 在两个地方运行 Lua：配置文件和脚本。下文中的每个函数均标明了其适用环境：

| 标签 | 说明 |
| --- | --- |
| <span class="api-tag">Config</span> | 在[配置文件](../customize/config.md)中生效。 |
| <span class="api-tag">Script</span> | 在通过 [`rex do`](../automate/lua-scripts.md) 运行的脚本中生效。 |
| <span class="api-tag">Config <span class="when">at load</span></span> | 仅在加载时（文件自顶向下运行期间）生效。两种标签均可依此限定。 |
| <span class="api-tag">Config <span class="when">later</span></span> | 仅在后续阶段（在操作内部、绑定到按键的函数内或事件处理程序中）生效。 |

若函数无法正常工作，其限制说明会标注在对应函数文档的开头。

| 函数 | 配置（加载时） | 配置（后续） | 脚本（加载时） | 脚本（后续） |
| --- | --- | --- | --- | --- |
| `rex.bind`, `rex.unbind` | 是 | 仅函数 | 无效果 | 无效果 |
| `rex.mode`, `rex.bindings`, `rex.modes` | 是 | 错误 | 无效果 | 错误 |
| `rex.action` | 是 | 错误 | 是 | 错误 |
| `rex.host` | 是 | 错误 | 无效果 | 错误 |
| `rex.on` | 警告 | 错误 | 是 | 错误 |
| `rex.call`, `rex.session.*`, `rex.block.call` | 失败 | 是 | 是 | 是 |
| `rex.invoke` | 警告 | 是 | 是 | 是 |
| `rex.client.queue` | 错误 | 仅操作 | 是 | 是 |
| `rex.exec`, `rex.exec.start` | 是 | 是 | 是 | 是 |
| `rex.layout.*`, `rex.json.*`, `rex.log` | 是 | 是 | 是 | 是 |
| `rex.sleep`, `rex.wait`, `rex.stop` | 缺失 | 缺失 | 是 | 是 |
| `rex.after`, `rex.every` | 缺失 | 缺失 | 是 | 是 |
| `rex.args`, `rex.session_id`, `rex.block_id` | 缺失 | 缺失 | 是 | 是 |

- **无效果（No effect）** 表示调用被接受但不会产生任何实际作用。脚本中的按键绑定和主机定义绝不会进入按键映射或服务端。
- **缺失（Missing）** 表示该名称为 `nil`。调用它会报错，因此在两处共享的文件应先检查其是否存在。
- **失败（Fails）** 表示调用返回 `nil` 和错误消息，并作为警告报告。

## 按键绑定

参见[快捷键](../customize/keyboard-shortcuts.md)、[按键序列](../customize/key-sequences.md)和[按键模式](../customize/key-modes.md)。

### `rex.bind(key, action[, args])`

按名称将按键绑定到操作。`args` 是传递给该操作的可选参数表。

```lua
rex.bind("cmd+d", "pane.split", { direction = "right" })
```

`key` 可以是单个按键、用 `>` 编写的序列，或带有模式前缀和斜杠的任一种形式。

### `rex.bind(key, fn)`

将按键绑定到以 `fn(ctx, ev)` 形式调用的 Lua 函数。返回 `true` 将按键标记为已处理。不允许在模式中使用。

`ev.keybinding` 为所按下的按键。对于按键序列，`ev.prefix` 为其前面的按键列表。

### `rex.unbind(key[, target])`

移除本文件以及客户端默认设置中该按键的绑定。返回其移除的本文件绑定数量。

`target` 为操作名称或函数，用于将移除限制在具有该目标的操作绑定中。`rex.unbind("mode/key")` 还会阻止该按键在该模式下触发。

### `rex.unbind{ mode = name }`

移除整个模式：包括其绑定、被阻止的按键以及其选项。

### `rex.unbind(binding)`

根据 `rex.bindings` 返回的表移除单个绑定。返回 1。

### `rex.mode(name[, options])`

声明一个模式并设置其选项。唯一的选项是 `exclusive`，这是一个布尔值，默认为 `false`。

### `rex.bindings([filter])`

按顺序返回此文件及其引入的文件目前为止所创建的绑定。`filter` 是一个可选表，可包含 `key`、`mode` 和 `action` 中的任意字段。

每个绑定都是一个表：

| 字段 | 说明 |
| --- | --- |
| `key` | 按键或按键序列，不包含其模式。 |
| `mode` | 模式，或为 `nil`。 |
| `action` | 操作名称；函数绑定时为 `nil`。 |
| `fn` | 函数；操作绑定时为 `nil`。 |
| `args` | 参数表，或为 `nil`。 |
| `source` | 绑定的来源位置，例如 `keys.lua:3`。 |

### `rex.modes()`

返回目前声明或绑定的所有模式，每个模式为一个包含 `name`、`exclusive` 和 `source` 的表。

## 操作

参见[自定义操作](../customize/actions.md)。

### `rex.action{ ... }`

定义一个操作。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `name` | string | 必需。由小写字母、数字和下划线组成。 |
| `title` | string | 必需。显示在命令面板中。 |
| `run` | function | 必需。调用形式为 `run(ctx, args)`。 |
| `description` | string | 较详细的说明。 |
| `category` | string | 命令面板中的分组类别。默认为 `Actions`。 |
| `keywords` | string | 用于搜索的附加关键字。 |
| `args` | table | 参数类型或 JSON Schema。 |
| `repeats` | boolean | 按住按键时是否重复运行。 |

`args` 类型包括 `string`、`number`、`integer`、`boolean`、`object`、`array` 和 `any`。末尾的 `?` 表示该参数为可选参数。

`ctx` 包含 `session_id`、`block_id`、`client_id`、`origin` 和 `server`。Rex 未知的字段则不存在。`run` 返回的值即为该操作的结果。

### `rex.invoke(name[, args])`

运行一个操作并返回其结果，或返回 `nil` 和错误消息。

在配置文件中，只能调用该文件自身定义的操作。在脚本中，脚本未定义的名称由服务端运行，因此脚本可以调用配置文件中定义的操作。

调用最多可嵌套 16 层。

### `rex.client.queue(name[, args])`

请求客户端执行其自身的操作之一，例如 `pane.zoom`。

在操作中，排队的操作会在 `run` 返回后按顺序运行，若 `run` 失败则被丢弃。在脚本中，每个操作都会立即执行。

当没有客户端可请求时，会引发错误。

## 调用 Rex

参见 [Lua 脚本](../automate/lua-scripts.md#调用-rex)。

本节中的每个调用均返回一个结果表，或在失败时返回 `nil` 和错误消息。调用失败绝不会引发错误。

### `rex.session.<method>(args)`

调用会话方法。`args` 是一个表。若省略 `session_id`，则会自动填充。其他 ID（如 `block_id`）不会自动填充。

```lua
local view, err = rex.session.view{}
```

| 方法 | 说明 |
| --- | --- |
| `view` | 返回会话的窗口、布局和块。 |
| `list_blocks` | 列出每个块及其处于已放置还是已分离状态。 |
| `list_clients` | 列出连接到该会话的客户端。 |
| `describe_block` | 返回块的放置位置及其提供的方法。 |
| `new_window` | 从布局创建窗口。 |
| `new_split` | 在现有块旁边创建分屏。 |
| `new_block` | 创建块而不将其放置在布局中。 |
| `new_layer` | 在窗口中创建浮动层。 |
| `close_window` | 关闭窗口及其内部的所有块。 |
| `close_layer` | 关闭浮动层及其内部的所有块。 |
| `move_block` | 将块移动到另一个块旁的新分屏中。 |
| `swap_blocks` | 交换两个块的位置。 |
| `detach_block` | 从布局中移除块但不关闭它。 |
| `float_block` | 将平铺块移动到新的浮动层中。 |
| `zoom_block` | 切换或设置块是否填满其所在窗口。 |
| `resize_pane` | 移动两个块之间的边框。 |
| `resize_layer` | 设置浮动层的位置和大小。 |
| `raise_layer`, `lower_layer` | 更改浮动层的叠放顺序。 |
| `move_window` | 在标签页顺序中移动窗口。 |
| `focus_block` | 聚焦某个块。 |
| `focus_window` | 聚焦某个窗口。 |
| `focus_direction` | 聚焦指定方向上最近的块。 |
| `focus_next_pane`, `focus_previous_pane` | 聚焦下一个或上一个窗格。 |
| `focus_next_window`, `focus_previous_window` | 聚焦下一个或上一个窗口。 |
| `set_label` | 设置会话的标签。 |
| `set_window_label` | 设置窗口的标签。 |
| `set_block_label` | 设置块的标签。 |
| `attach`, `detach` | 更改脚本接收事件的目标会话。 |
| `help` | 描述会话中可用的方法。 |

如需了解方法的参数与结果，请附带完整方法名称运行 `rex api describe`：

```sh
rex api describe session.new_split
```

### `rex.call(method[, args])`

按完整名称调用任何服务端方法，包括 `rex.session` 未涵盖的方法。

```lua
local result, err = rex.call("session.list")
```

`rex api list` 可打印所有方法。

### `rex.block.call(creator, method[, args])`

在块上调用方法。`creator` 是块类型的完整名称。若省略 `block_id`，则从当前块自动填充。

```lua
local terminal = "com.superlogical.terminal"
local title = rex.block.call(terminal, "title", {}).title
```

终端的方法包括：

| 方法 | 说明 |
| --- | --- |
| `format` | 将屏幕内容以文本、HTML 或 VT 转义序列形式返回。 |
| `process` | 描述终端的子进程和前台进程。 |
| `pwd` | 返回终端最近报告的工作目录。 |
| `title` | 返回终端的标题。 |
| `size` | 返回终端的尺寸（以字符单元格和像素为单位）。 |
| `write` | 向终端写入字节，如同键盘输入。 |
| `reset` | 重置终端。 |
| `resize` | 请求调整终端尺寸。 |
| `set_theme` | 替换终端的默认颜色。 |
| `program_status` | 返回程序报告的状态记录。 |
| `list_dir` | 列出指定路径下的目录。 |

### `rex.layout`

用于构建 `new_window`、`new_split` 和 `new_layer` 所接受的 `layout` 表的函数。它们仅构建表结构，不调用任何内容。

| 函数 | 说明 |
| --- | --- |
| `rex.layout.block{ flavor, options }` | 单个块。`flavor` 指定要创建的类型，例如 `com.superlogical.terminal.shell`。 |
| `rex.layout.horizontal(ratio, a, b)` | 水平分割的两个布局。`ratio` 为分配给 `a` 的比例（0 到 1 之间）。 |
| `rex.layout.vertical(ratio, a, b)` | 垂直分割的两个布局。 |

终端的选项包括：

| 选项 | 说明 |
| --- | --- |
| `command` | 包含要运行的程序及其参数的列表。若省略，则启动交互式 Shell。 |
| `shell` | 要使用的 Shell。`none` 则直接启动 `command`。 |
| `cwd` | 工作目录。 |
| `initial_input` | 终端启动后自动输入的文本。 |
| `exit` | `{ on_completion = false }` 在程序退出后仍保持终端开启。 |

## 事件

参见 [Lua 事件](../automate/lua-events.md)。这些函数仅在通过 `rex do` 运行的脚本中生效。

### `rex.on(event, fn)`

每当发生 `event` 时调用 `fn(ctx, ev)`。`ev` 保存事件的各个字段。`ctx` 包含 `session_id`，对于块事件还包含 `block_id`。

[事件参考](events.md)列出了事件名称。

### `rex.wait(event[, filter][, timeout])`

阻塞直到发生 `event`，并返回 `ev` 和 `ctx`。若先达到 `timeout` 秒，则返回 `nil` 和 `"timeout"`。

`filter` 是事件必须匹配的字段表，或是以 `filter(ev, ctx)` 形式调用并在匹配时返回 `true` 的函数。

### `rex.sleep(seconds)`

阻塞指定的秒数，支持小数。

### `rex.stop([code])`

立即结束脚本。`rex do` 退出并返回状态码 `code`，默认为 0。

## 主机与其他服务端

### `rex.host{ ... }`

声明所连接的另一个 Rex 服务端。仅在配置文件中有效。

| 字段 | 说明 |
| --- | --- |
| `label` | 必需。主机的名称。 |
| `endpoints` | 必需。地址列表，按顺序尝试连接。 |
| `endpoint` | 单个地址，可替代 `endpoints`。 |
| `id` | 稳定 ID，使主机在重命名时仍能保持其身份标识。 |
| `icon` | 供客户端显示的图标名称。 |

### `rex.servers()`

以列表形式返回正在运行的操作或脚本可用的其他服务端的标签。

### `rex.server(label)`

返回一个包含与 `rex` 相同的 `session`、`block` 和 `call` 函数的表，其调用发往该服务端。对未知标签会引发错误。

通过其进行的调用不会自动填充 `session_id` 或 `block_id`。

## 其他函数

用于运行命令、定时器、JSON 和日志记录的函数。参见[运行命令](../automate/lua-scripts.md#运行命令)与[定时器](../automate/lua-scripts.md#定时器)。

### `rex.exec(argv[, opts])`

运行命令，等待其退出，并返回结果表。仅在命令完全未运行时（例如程序不存在时）返回 `nil` 和错误消息。

```lua
local r, err = rex.exec({ "git", "status", "--short" }, { cwd = dir })
```

`argv` 是由字符串组成的列表：首先是程序名，随后是其各项参数。没有 Shell 会对其进行解析，因此参数无需加引号。名称中不含斜杠的程序会在命令的 `PATH` 中查找。

`opts` 是一个可选表：

| 选项 | 说明 |
| --- | --- |
| `cwd` | 工作目录。默认为 Rex 自身的工作目录。 |
| `env` | 要设置的环境变量，例如 `{ GIT_DIR = "/repo/.git" }`。设为 `false` 可移除对应变量。 |
| `clear_env` | 设为 `true` 时从空环境启动。`env` 中的设置依然有效。 |
| `stdin` | 写入命令标准输入的字符串。 |
| `timeout` | 超时秒数，超时后向命令发送 `SIGTERM`，两秒后再发送 `SIGKILL`。 |
| `stdout`, `stderr` | 设为 `false` 时丢弃该流。默认均捕获。 |
| `text` | 设为 `false` 时在 Windows 上保留输出中的 `\r\n`。 |

Rex 未知的选项会被忽略并输出警告。

结果包含以下内容：

| 字段 | 说明 |
| --- | --- |
| `code` | 退出状态码；若因信号终止则为 `-1`。 |
| `signal` | 该信号的名称（例如 `SIGTERM`），若无信号则为 `nil`。 |
| `stdout`, `stderr` | 命令打印的内容。未输出任何内容时为 `""`。 |
| `timed_out` | 若因 `timeout` 终止命令则为 `true`。 |
| `ok` | 当 `code` 为 0 且命令未超时时为 `true`。 |

非零退出状态码依然属于有效结果，而非错误。请检查 `ok` 字段。

当配置文件中的操作等待命令执行时，服务端会继续处理按键和其他操作。而在其他所有场景下，该等待均会阻塞脚本。

### `rex.exec.start(argv[, opts])`

启动命令并在不等待其退出的情况下返回句柄，或返回 `nil` 和错误消息。它接受与 `rex.exec` 相同的参数，并额外支持以下选项：

| 选项 | 说明 |
| --- | --- |
| `stdin` | 设为 `true` 时保持标准输入开启以供 `h:write` 使用。 |
| `stdout`, `stderr` | 每当有输出到达时调用的函数。单次回调的内容可能在行中截断。 |
| `detach` | 设为 `true` 时允许命令在其启动者的生命周期结束后继续运行。 |

句柄包含以下方法和字段：

| 方法 | 说明 |
| --- | --- |
| `h:wait([seconds])` | 等待命令退出并返回与 `rex.exec` 相同的结果结构。若先达到 `seconds` 秒则返回 `nil` 和 `"timeout"`。 |
| `h:write(data)` | 写入标准输入。成功返回 `true`，失败返回 `nil` 和错误消息。 |
| `h:close_stdin()` | 关闭标准输入。 |
| `h:kill([signal])` | 发送信号，默认为 `SIGTERM`。`signal` 可以是名称（如 `SIGINT`）或数字。 |
| `h:running()` | 返回命令是否仍在运行。 |
| `h.pid` | 命令的进程 ID。 |

命令的存续周期与其启动者的工作周期相同。当操作、处理程序或定时器返回，或者脚本顶层执行结束时，Rex 会停止其启动的命令。使用 `detach = true` 启动的命令绝不会以此方式被停止。

### `rex.after(seconds, fn)`

在 `seconds` 秒后调用 `fn(ctx)` 一次，并返回一个具有与 [`rex.every`](#rexeveryseconds-fn) 相同方法的定时器。`seconds` 可以为零或小数。

`ctx` 是操作的 `run` 函数所接收的相同表，其中 `ctx.origin` 设置为 `timer`。API 调用默认针对脚本的会话和块。

### `rex.every(seconds, fn)`

每隔 `seconds` 秒调用 `fn(ctx)` 一次，直到定时器被取消，并返回一个定时器。`seconds` 必须大于零。

若定时器周期到达时脚本仍处于忙碌状态，`fn` 会在脚本空闲时运行一次，在此期间错过的周期将被丢弃。

定时器具有两个方法：

| 方法 | 说明 |
| --- | --- |
| `t:cancel()` | 停止定时器。 |
| `t:active()` | 返回 `true` 直到定时器被取消或完成最后一次触发。 |

`fn` 中的错误会被报告，定时器将继续运行。一个脚本最多可同时拥有 1,024 个定时器。若再创建一个，脚本将以状态码 1 终止。

### `rex.json.encode(value[, opts])`

将 Lua 值转换为 JSON 文本，或返回 `nil` 和错误消息。`opts.indent = true` 会将文本缩进两个空格。

```lua
local text = rex.json.encode({ name = "work", panes = { 1, 2 } })
```

表的转换方式与在 API 调用中相同。键为 1 到 n 的表转换为数组，其他任何表（包括空表）均转换为对象。函数或包含自身的循环引用表无法编码。

### `rex.json.decode(text)`

将 JSON 文本转换为 Lua 值，或返回 `nil` 和错误消息。`null` 变为 `nil`，数组中的 `null` 将被丢弃。

### `rex.log([level, ]message)`

写入日志消息。`level` 为 `debug`、`info`、`warn` 或 `error`，默认为 `info`。在脚本中，该消息会直接输出到终端。

## 脚本值

仅在通过 `rex do` 运行的脚本中可用。

| 变量 | 说明 |
| --- | --- |
| `rex.args` | 脚本的参数（作为表）。未传递参数时为空表。 |
| `rex.session_id` | 脚本所针对运行的会话 ID。 |
| `rex.block_id` | 脚本所针对运行的块 ID，若无则为 `nil`。 |
