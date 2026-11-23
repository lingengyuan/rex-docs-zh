> 原文：https://www.superlogical.com/rex/docs/customize/custom-ui
> 原文版本：aadf4426c65c（抓取于 2026-11-23）

# 自定义 UI

[自定义操作](actions.md)可以中途暂停，在命令面板中向用户提问，然后根据回答继续执行。`rex.ui.input` 用于请求输入一行文本，`rex.ui.pick` 则展示一个供选择的列表。

```lua
rex.action{
  name  = "new_branch",
  title = "Git: New Branch…",
  run   = function(ctx, args)
    local name, why = rex.ui.input{
      title       = "New branch",
      placeholder = "feature/…",
      value       = "feature/",
      confirm     = "Create branch",
    }
    if name == nil then return end

    -- 在获得焦点的终端提示符处输入命令。
    rex.block.call("com.superlogical.terminal", "write", {
      data = "git switch -c " .. name .. "\r",
    })
  end,
}

rex.bind("alt+cmd+b", "new_branch")
```

运行 `rex config reload`，然后按下 <kbd>Option</kbd>+<kbd>Cmd</kbd>+<kbd>B</kbd>。命令面板会打开一个标题为“New branch”的文本输入框。按下 <kbd>Return</kbd> 后，操作就会带着你输入的内容继续执行。

操作在等待回答期间不会阻塞其他流程。提问窗口打开时，按键、其他操作和事件仍可正常工作，且用户思考的时间不计入操作的超时限制。

## 请求输入文本

`rex.ui.input` 接收一个表，并返回用户提交的文本：

```lua
local name, why = rex.ui.input{ title = "Your name" }
```

| 字段 | 说明 |
| --- | --- |
| `title` | 问题的标题。必填。 |
| `placeholder` | 输入框为空时显示的提示文本。 |
| `value` | 输入框的初始文本，供用户编辑。 |
| `confirm` | 提交行的标签。未设置时，该行会显示为 `Use "…"` 并附带已输入的文本。 |
| `timeout` | 等待回答的秒数。默认为 300，上限为 3600。 |

返回的文本与用户输入完全一致，包括首尾空格。文本也可能为空字符串，因为用户可以提交空输入框。

## 请求选择列表项

`rex.ui.pick` 会展示一个列表，并返回用户所选列表项的 `id`。它接收与 `rex.ui.input` 相同的字段（其中 `placeholder` 和 `value` 作用于筛选列表的输入框），外加 `items`：

```lua
local dir, why = rex.ui.pick{
  title       = "Open project",
  placeholder = "Filter projects",
  items = {
    { id = "/Users/me/Apps/rex", title = "rex",
      subtitle = "~/Apps/rex", icon = "folder" },
    { id = "/Users/me/Apps/rex-app", title = "rex-app",
      subtitle = "~/Apps/rex-app", icon = "folder" },
  },
}
if dir == nil then return end

rex.session.new_window{
  layout = rex.layout.block{
    flavor  = "com.superlogical.terminal.shell",
    options = { cwd = dir },
  },
}
```

`items` 是按展示顺序排列的列表，最多包含 2,000 项，也可以为空。每个列表项都是一个表：

| 字段 | 说明 |
| --- | --- |
| `id` | `rex.ui.pick` 为该项返回的值。必填，且在列表内唯一。 |
| `title` | 列表项的主文本。默认为 `id`。 |
| `subtitle` | 第二行较弱化的副标题文本。 |
| `icon` | 下方列出的图标名称之一。 |
| `detail` | 显示在行尾的简短文本，例如文件状态。 |
| `selected` | 设为 `true` 时该项默认处于勾选状态。仅在启用 `multiple` 时有效。 |

列表项也可以直接是一个纯字符串，等价于 `id` 和 `title` 均为该字符串的表：

```lua
rex.ui.pick{ title = "Pick a fruit", items = { "Apple", "Banana", "Cherry" } }
```

### 图标

`icon` 可以是以下名称之一。各个 Rex 应用会按自身风格绘制这些图标。

`document`、`folder`、`branch`、`terminal`、`code`、`server`、`database`、`package`、`globe`、`link`、`person`、`tag`、`clock`、`star`、`gear`、`plus`

其他名称会被忽略并触发警告，该列表项将不显示图标。

### 多选列表项

设置 `multiple = true` 时，用户可以勾选任意数量的列表项，返回值为按 `items` 顺序排列的 `id` 列表。如果用户未勾选任何项直接确认，则返回空列表。命令面板会在 `confirm` 标签旁显示已勾选的数量，按下 <kbd>Cmd</kbd>+<kbd>Return</kbd> 即可确认。

```lua
local files = rex.ui.pick{
  title       = "Stage files",
  placeholder = "Filter changed files",
  multiple    = true,
  confirm     = "Stage",
  items = {
    { id = "README.md", icon = "document", detail = "??", selected = true },
    { id = "docs/notes.md", title = "notes.md", subtitle = "docs",
      icon = "document", detail = "??" },
  },
}
-- files 是一个列表，例如 { "README.md", "docs/notes.md" }
```

### 接受手动输入的文本

设置 `allow_other = true` 时，用户可以直接提交输入框中键入的文本，而不必从列表中选择。此时返回值为表 `{ text = "..." }`，以免与列表项的 `id` 混淆。`allow_other` 不能与 `multiple` 同时使用。

```lua
local fruit = rex.ui.pick{
  title       = "Favourite fruit",
  items       = { "Apple", "Banana", "Cherry" },
  allow_other = true,
}
if type(fruit) == "table" then fruit = fruit.text end
```

## 无回答时的返回值

当没有收到回答时，两个函数都会返回 `nil`、一个原因以及可选的详细信息：

```lua
local name, why, detail = rex.ui.input{ title = "New branch" }
if name == nil then
  if why == "cancelled" then return end
  rex.log("warn", "new_branch: " .. why .. " " .. (detail or ""))
  return
end
```

原因始终为以下词之一：

| 原因 | 含义 |
| --- | --- |
| `cancelled` | 用户未回答即关闭了提示。 |
| `timeout` | 在超时时间内无人回答。 |
| `no_client` | 没有已连接的 Rex 应用，或所有正在显示该提示的应用都断开了连接。 |
| `unsupported` | 没有能够显示提示的已连接应用（通常是因为客户端版本低于服务端）。 |
| `busy` | 所有能够显示提示的应用当前都在显示另一个提示。 |
| `failed` | 其他原因。`detail` 为说明具体原因的一句话。 |

除 `failed` 外，其他所有原因对应的 `detail` 均为 `nil`。`detail` 的措辞可能在不同版本的 Rex 之间变化，因此代码中应判断原因而非详细信息。

调用本身的错误（例如缺少 `title` 或两个列表项使用了相同的 `id`）则会直接抛出错误。

## 哪些应用会收到提问

连接到服务端的每一个 Rex 应用都会收到提问（包括你的其他设备），只要该应用版本足够新以支持显示提示且当前未在显示其他提示。最先提交的回答会生效，其他应用上的提示随之关闭；在任意一个应用上取消，所有应用都会同步取消。

通过 `rex do` 运行操作时也是如此：问题会显示在所有已连接的应用中，`rex do` 会等待直到有人回答。使用 `--timeout` 可限制等待时间。详见 [`rex do`](../reference/cli.md)。

## 可以在何处提问

提示会暂停发起提问的操作，因此它只能在 Rex 支持暂停的上下文中工作：即操作的 `run` 函数内部，以及由 `run` 直接调用的函数中。以下位置不支持：

- 直接绑定到按键的函数，例如 `rex.bind(key, function() ... end)`
- 通过 [`rex.on`](../automate/lua-events.md) 注册的事件处理程序
- 配置文件的顶层代码
- 通过 `pcall` 或 `xpcall` 调用的函数
- 由 `rex.invoke` 运行的操作
- 由标准库调用的函数，例如 `table.sort` 的比较器

在这些位置调用时，两个函数都不会向任何人提问，而是直接返回 `nil` 和 `failed`，并在日志中记录一条警告。若要通过按键触发提问，请先定义一个操作，再将按键绑定到该操作的名称。

## 在无人值守环境下运行

操作可以支持通过参数传入回答，仅在参数缺失时才弹出提问。这样脚本或 CI 任务就可以在无人值守时运行该操作：

```lua
rex.action{
  name  = "greet",
  title = "Greet",
  args  = { name = "string?" },
  run   = function(ctx, args)
    local name = args.name or rex.ui.input{ title = "Your name" }
    if name == nil then return end
    rex.log("info", "Hello, " .. name)
  end,
}
```

```sh
rex do greet name=Ada
```

## 服务端 API

应用通过 `client_prompt_requested` 事件接收提示，并通过 `client.reply` 进行应答。收到提问但未作答的应用会在提示关闭时收到 `client_prompt_ended` 事件。提示功能需要控制 API 修订版 17。详见[服务端 API](../reference/api.md)。
