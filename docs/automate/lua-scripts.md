> 原文：https://www.superlogical.com/rex/docs/automate/lua-scripts
> 原文版本：95c00c40bfd9（抓取于 2026-11-13）

# Lua 脚本

`rex do` 针对 Rex 服务端运行 [Lua](https://www.lua.org) 脚本。

脚本功能极其强大。它能完成完整客户端可执行的任何操作：检查服务端、创建会话、创建窗口、启动终端、读取终端屏幕、响应事件等。

以下脚本打开一个运行 `htop` 的新窗口：

```lua
-- htop.lua
rex.session.new_window{
  layout = rex.layout.block{
    flavor  = "com.superlogical.terminal.shell",
    options = { command = { "htop" } },
  },
}
```

```sh
rex do htop.lua
```

脚本使用与[配置文件](../customize/config.md)相同的 `rex` API。不同于配置文件，脚本从上到下执行一次后退出（除非存在活跃的事件处理程序或正在运行的定时器）。

## 运行脚本

`rex do` 支持以三种方式接收脚本：

```sh
rex do ./layout.lua                           # 文件
rex do -e 'return rex.call("session.list")'   # 通过 -e 行内执行
rex do - < layout.lua                         # 标准输入
```

当参数以 `.lua` 结尾或包含斜杠时，Rex 会将其视为文件路径；其余情况则视为要运行的[操作](../customize/actions.md)名称。

在 Rex 终端内部运行的脚本会作用于该终端的会话和块。使用 `-s` 和 `-b` 可将[目标](cli.md#命令目标)指定为不同的会话或块：

```sh
rex do -s build ./layout.lua
```

脚本拥有完整的 Lua 标准库，包括 `io` 和 `os`，并且 `require` 可以加载其他 Lua 文件。唯一的例外是 `io.popen` 和 `os.execute`。如需运行命令，请改用 [`rex.exec`](#运行命令)。

脚本在 `rex` CLI 所在的本地执行，因此安全性和程序访问权限完全由运行环境决定。

## 参数

参数在脚本名称之后以 `key=value` 键值对的形式传递，并从 `rex.args` 表中读取：

```lua
-- greet.lua
return "hello " .. (rex.args.name or "world")
```

```
$ rex do greet.lua name=rex
"hello rex"
```

参数值的类型由其书写方式决定。`n=2` 是数字，`on=true` 是布尔值，`name=x` 是字符串。若要传递看起来像其他类型的字符串，或传递嵌套结构，请使用 `--args` 将所有参数作为 JSON 传递：

```sh
rex do greet.lua --args '{"name": "true"}'
rex do greet.lua --args @args.json
```

## 返回结果与错误处理

脚本返回的值将打印为 JSON。表会转换为对象或数组。添加 `--json` 可获得带缩进的格式化输出。不返回任何内容的脚本不会输出任何文本。

```
$ rex do -e 'return { name = "rex", tabs = { 1, 2 } }'
{"name":"rex","tabs":[1,2]}
```

引发错误的脚本会打印错误消息并以状态码 1 退出：

```
$ rex do -e 'error("no tests found", 0)'
Error: no tests found
```

若要以自定义的状态码退出，可调用 `rex.stop` 并传入该状态码。脚本将立即终止：

```lua
rex.stop(3)
```

`print` 如同往常一样写入终端，`rex.log` 则会写入一条日志。

## 调用 Rex

脚本启动时包含若干描述其运行位置的值：

| 变量 | 说明 |
| --- | --- |
| `rex.session_id` | 脚本运行所针对的会话。 |
| `rex.block_id` | 脚本运行所针对的块（如果存在）。 |
| `rex.args` | 脚本的参数。 |

Rex 的 API 归类在 `rex.session` 命名空间下。每次调用接收一个参数表，并返回一个表：

```lua
rex.session.set_block_label{
  block_id = rex.block_id,
  label    = "tests",
}
```

调用会自动填入脚本所在的会话，因此大多数调用无需传入 `session_id`。针对单个块的操作（例如 `set_block_label`）仍然需要传入其 `block_id`。

调用失败不会终止脚本。它会返回 `nil` 和错误消息，因此当结果重要时请检查第二个返回值：

```lua
local w, err = rex.session.new_window{ layout = layout }
if err ~= nil then error(err, 0) end
```

调用 Rex 的另外三种方式：

- `rex.call(method, args)` 按名称调用任何服务端方法，包括位于 `rex.session` 之外的方法，例如 `rex.call("session.list")`。
- `rex.block.call(creator, method, args)` 调用块上的方法，例如读取终端屏幕。
- `rex.invoke(name, args)` 运行操作，既包括脚本定义的操作，也包括来自配置文件的操作。`rex.client.queue(name, args)` 则请求应用执行其自身的操作。

完整的列表请参阅 [Lua API 参考](../reference/lua.md)。

### 布局

创建块的调用需要传入 `layout`。可以使用 `rex.layout` 构建布局：

```lua
local shell = "com.superlogical.terminal.shell"

rex.session.new_window{
  layout = rex.layout.horizontal(0.5,
    rex.layout.block{ flavor = shell },
    rex.layout.block{
      flavor  = shell,
      options = { command = { "htop" } },
    }),
}
```

`rex.layout.block` 代表一个块。`rex.layout.horizontal` 和 `rex.layout.vertical` 在两个布局之间划分空间，首个参数指定第一个布局所占的比例。它们可以相互嵌套。

## 休眠与等待

脚本常常需要启动某项操作，然后根据其结束状态进行处理。

`rex.sleep(seconds)` 会暂停脚本：

```lua
rex.sleep(0.5)
```

`rex.wait(event, filter, timeout)` 会暂停直到事件到达：

```lua
local ev = rex.wait(
  "terminal.child_exited", { block_id = id }, 600)
```

- `event` 是要等待的事件名称。
- `filter` 为可选项。表用于匹配字段与该表相等的事件；函数则会在传入事件时被调用，并在返回 `true` 时视为匹配。
- `timeout` 为可选项，单位为秒。若不指定，`rex.wait` 将永久等待。

`rex.wait` 将事件作为表返回。如果超时先发生，则返回 `nil` 和 `"timeout"`。

[事件参考](../reference/events.md)列出了所有事件及其字段。

## 定时器

`rex.every` 以固定间隔重复调用函数，`rex.after` 则在一段延迟后调用函数一次：

```lua
rex.every(5, function(ctx)
  -- 每 5 秒执行一次
end)

rex.after(0.5, function(ctx)
  -- 0.5 秒后执行一次
end)
```

与 `rex.sleep` 不同，定时器不会暂停脚本。脚本会继续向下执行，函数将在稍后被调用。

两个函数均返回一个定时器对象。调用 `t:cancel()` 可停止定时器。即使脚本丢弃了定时器引用，定时器仍会继续运行；因此如果后续可能需要停止它，请保留该引用。

定时器可以在任何位置创建，包括事件处理程序内部或其他定时器内部。函数的 `ctx` 和 API 调用始终默认使用脚本自身的会话和块，即便定时器是在处理程序中创建的也是如此。

定时器绝不会与脚本中的其他 Lua 代码同时并发执行。如果处理程序正在运行，到期的定时器会等待处理程序返回。如果下一次 `rex.every` 触发时脚本仍然繁忙，该函数将在空闲时执行一次，而不会为错过的每一次触发分别执行。

定时器中发生的错误会被打印出来，定时器继续保持运行，这与[处理程序中的错误](lua-events.md#处理程序失败)机制一致。

一个脚本最多可同时拥有 1,024 个定时器。已取消的定时器或已执行完成的 `rex.after` 定时器不计入在内。超出限制将导致脚本以状态码 1 终止（即便处于 `pcall` 保护中也是如此），因为这几乎总是意味着处理程序为每个事件都创建了定时器却从未进行取消。

## 运行命令

`rex.exec` 运行一条命令，并返回其输出内容与退出状态：

```lua
local r, err = rex.exec{ "git", "rev-parse", "--abbrev-ref", "HEAD" }
if r == nil then error(err, 0) end

if r.ok then
  rex.session.set_block_label{
    block_id = rex.block_id,
    label    = r.stdout:gsub("\n$", ""),
  }
end
```

命令是一个列表：首项为程序，后续为各项参数。没有 Shell 会对其进行解析，因此包含空格的路径或来自 `rex.args` 的值无需加引号。若需使用 Shell，可显式调用：`{ "sh", "-c", line }`。

以非零状态码退出的命令仍会返回结果。可检查 `r.ok`，或通过 `r.code` 获取准确的状态码，通过 `r.stderr` 获取其向标准错误打印的内容。仅当命令完全无法运行时（例如程序未安装），`rex.exec` 才会返回 `nil` 和错误消息。

配置选项放入第二个表中：

```lua
local r = rex.exec({ "make", "test" }, {
  cwd     = "/src/app",
  env     = { CI = "1" },
  timeout = 300,
})
```

[Lua API 参考](../reference/lua.md#rexexecargv-opts)列出了所有可用选项和字段。

### 流式输出

`rex.exec.start` 启动命令而不等待其完成，并返回一个句柄。传入一个函数作为 `stdout` 或 `stderr` 即可在输出到达时实时接收：

```lua
local h = assert(rex.exec.start({ "make", "build" }, {
  stdout = function(data) io.write(data) end,
}))

local r = h:wait()
```

命令的存活时间与启动它的脚本部分相同。当脚本顶层执行结束，或者处理程序或定时器返回时，Rex 会停止它启动的命令。若命令需要保持运行，可传入 `detach = true`。

若要观察命令的运行过程，可改在终端块中启动它，如[下文示例](#示例在分屏中运行测试)所示。

## 示例：在分屏中运行测试

该脚本在当前终端旁的新分屏中运行命令。如果命令失败，它会放大该分屏，使失败信息显现于中心。

```lua
-- tests.lua
local cmd = rex.args.cmd or "make test"

local split, err = rex.session.new_split{
  direction = "horizontal",
  side      = "after",
  focus     = false,
  layout    = rex.layout.block{
    flavor  = "com.superlogical.terminal.shell",
    options = {
      command = { "sh", "-c", cmd },
      exit    = { on_completion = false },  -- 保留输出
    },
  },
}
if err ~= nil then error(err, 0) end
local block_id = split.block_ids[1]

-- 最多等待命令退出 10 分钟
local ev = rex.wait(
  "terminal.child_exited", { block_id = block_id }, 600)
if ev == nil then error("timed out waiting for: " .. cmd, 0) end

if ev.exit_code ~= 0 then
  rex.session.zoom_block{ block_id = block_id, zoom = true }
end

return { block_id = block_id, exit_code = ev.exit_code }
```

```
$ rex do tests.lua cmd="go test ./..."
{"block_id":"block:01a10deb-c752-789f-9add-5dfd3a5b3214","exit_code":1}
```

## 示例：导出会话

该脚本每 5 秒将当前会话的布局保存到 JSON 文件中，供其他程序读取。

```lua
-- export.lua
local path = rex.args.path or "session.json"

local function export()
  local view, err = rex.session.view{}
  if err ~= nil then error(err, 0) end

  local f = assert(io.open(path, "w"))
  f:write(rex.json.encode(view, { indent = true }))
  f:close()
end

export()
rex.every(5, export)
```

```
$ rex do export.lua path=/tmp/work.json
running: 1 timer; Ctrl-C to stop
```

`rex.json.encode` 转换表的方式与 API 调用完全相同，因此生成的文件与服务端返回的内容一致。`rex.json.decode` 则可将其读回。

如果服务端短暂无法访问，`export` 会引发错误并将其打印出来，定时器会在 5 秒后再次尝试。
