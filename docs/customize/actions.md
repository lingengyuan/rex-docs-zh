> 原文：https://www.superlogical.com/rex/docs/customize/actions
> 原文版本：42768f1a7391（抓取于 2026-11-13）

# 自定义操作

自定义操作是在[配置文件](config.md)中使用 `rex.action` 定义的具名 Lua 函数。定义后，它的使用方式与内置操作完全相同：可以绑定到按键、显示在命令面板中，也可以通过 CLI 运行。

```lua
rex.action{
  name  = "scratch",
  title = "Open Scratch Window",
  run   = function(ctx, args)
    rex.session.new_window{
      layout = rex.layout.block{
        flavor = "com.superlogical.terminal.shell",
      },
    }
  end,
}

rex.bind("shift+cmd+n", "scratch")
```

修改文件后运行 `rex config reload`，使操作生效。随后即可按下 <kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>N</kbd>、在命令面板中搜索“Open Scratch Window”，或通过 CLI 运行它：

```sh
rex do scratch
```

## 定义操作

`rex.action` 接收一个表作为参数。其中 `name`、`title` 和 `run` 为必填项。

| 字段 | 说明 |
| --- | --- |
| `name` | 在 `rex.bind` 和 CLI 中引用该操作的名称。仅支持小写字母、数字和下划线。 |
| `title` | 在命令面板和菜单中显示的文本。 |
| `run` | 运行该操作时调用的函数。 |
| `description` | 命令面板中展示的详细说明。 |
| `category` | 命令面板中的分组。默认为 `Actions`。 |
| `keywords` | 命令面板搜索时匹配的额外关键词。 |
| `args` | 该操作接收的参数。详见[参数](#参数)。 |
| `repeats` | 设为 `true` 时，按住快捷键会重复运行该操作。 |

自定义操作的名称不能包含点号。像 `pane.split` 这样带有点号的名称属于客户端和块。所有自定义操作的名称均不包含点号。这种直观的命名约定有助于明确操作的来源。

重复定义相同名称的操作会收到警告，并以后定义的为准。

## 参数

`args` 用于声明操作接收的参数及其类型。后缀 `?` 表示该参数为可选参数：

```lua
rex.action{
  name  = "dev_layout",
  title = "Open Dev Layout",
  args  = { file = "string", ratio = "number?" },
  run   = function(ctx, args)
    local shell = "com.superlogical.terminal.shell"
    local w, err = rex.session.new_window{
      layout = rex.layout.horizontal(args.ratio or 0.5,
        rex.layout.block{ flavor = shell },
        rex.layout.block{
          flavor  = shell,
          options = { command = { "tail", "-f", args.file } },
        }),
    }
    if err ~= nil then error(err, 0) end
    return { window_id = w.window_id }
  end,
}
```

支持的类型包括 `string`、`number`、`integer`、`boolean`、`object`、`array` 和 `any`。

声明参数可以让 Rex 在操作运行前捕获错误。如果按键绑定传入了拼写错误或类型不符的参数，客户端在加载键位映射时会发出警告，CLI 则会直接拒绝执行：

```
$ rex do dev_layout file=app.log bogus=1
Error: no argument named "bogus"; the action takes file, ratio?
```

未声明 `args` 的操作可以接收任意参数。

如果需要更精细的控制，也可以将 `args` 写成 Lua 表形式的 [JSON Schema](https://json-schema.org)。包含 `type` 键的表会被视为 Schema 并原样使用。

## run 函数

调用 `run` 时会传入两个表：`ctx` 描述操作运行的上下文，`args` 包含传入的参数。即使没有传入参数，`args` 也始终是一个表。

| 字段 | 说明 |
| --- | --- |
| `ctx.session_id` | 操作所作用的会话。 |
| `ctx.block_id` | 操作所作用的块，通常是获得焦点的块。 |
| `ctx.client_id` | 请求执行该操作的客户端。 |
| `ctx.origin` | 操作的触发方式：`key`、`palette`、`cli`、`api` 或 `script`。 |

如果 Rex 无法获取对应的值，相应字段会不存在。

在 `run` 内部调用的 Rex API 默认作用于该操作所在的会话，因此本页示例均未传入 `session_id`。如果调用的 API 作用于单个块（例如 `rex.session.set_block_label`），仍需传入 `block_id`；若针对获得焦点的块，可传入 `ctx.block_id`。[Lua API 参考](https://www.superlogical.com/rex/docs/reference/lua.md)提供了完整的 API 列表。

### 错误处理

API 调用失败并不会中断函数执行。它会返回 `nil` 和一条错误信息，因此在需要关注结果时应检查第二个返回值：

```lua
local w, err = rex.session.new_window{ layout = layout }
if err ~= nil then error(err, 0) end
```

使用 `error` 抛出错误会使操作失败，并将错误信息报告给调用方。

### 返回值

`run` 返回的任何内容都会作为操作的执行结果，CLI 会将其输出为 JSON：

```
$ rex do dev_layout file=app.log
{"window_id":"window:01a10dd6-ce31-760a-a9e5-c273c73fdd7e"}
```

未返回任何内容、返回 `nil` 或返回 `true` 均表示没有结果。

## 运行操作

**通过快捷键运行。** 与内置操作一样按名称绑定即可。详见[快捷键](keyboard-shortcuts.md)。

```lua
rex.bind("shift+cmd+l", "dev_layout", { file = "app.log" })
```

**通过命令面板运行。** 搜索操作的标题。

**通过 CLI 运行。** 使用 `rex do` 加上操作名称，并以 `key=value` 键值对的形式传递参数。添加 `--json` 可以格式化输出结果。

```sh
rex do dev_layout file=app.log ratio=0.3
```

`rex actions` 会列出服务端已加载的自定义操作。

## 调用其他操作

`rex.invoke` 可以在 `run` 内部运行另一个自定义操作并返回其结果。它会在相同的会话、块和客户端环境下运行。

```lua
rex.action{
  name  = "dev_layout_main",
  title = "Open Dev Layout for app.log",
  run   = function(ctx, args)
    local result, err = rex.invoke("dev_layout", {
      file = "app.log",
    })
    if err ~= nil then error(err, 0) end
    return result
  end,
}
```

`rex.client.queue` 会请求执行该操作的客户端执行其自身的操作，例如关闭命令面板或缩放窗格。排队的操作会在 `run` 返回后按顺序执行；若 `run` 执行失败，排队的操作会被废弃。

```lua
rex.action{
  name  = "focus_mode",
  title = "Focus Mode",
  run   = function(ctx, args)
    rex.client.queue("pane.zoom")
    rex.client.queue("client.sidebar.toggle")
  end,
}
```

`rex.client.queue` 需要依赖客户端，因此如果从 CLI 运行操作且找不到客户端，它会抛出错误。此外，仅当应用设置中开启了 Remote Control（远程控制）时，应用才会接受来自 CLI 的操作。

## 执行系统命令

`rex.exec` 用于运行系统命令，并返回其输出内容和退出状态：

```lua
rex.action{
  name  = "pull_dotfiles",
  title = "Pull Dotfiles",
  run   = function(ctx, args)
    local r, err = rex.exec(
      { "git", "pull", "--ff-only" },
      { cwd = os.getenv("HOME") .. "/dotfiles", timeout = 20 })
    if r == nil then error(err, 0) end
    if not r.ok then error(r.stderr, 0) end
    return { output = r.stdout }
  end,
}
```

在操作等待命令执行期间，服务端会继续处理按键和其他操作，因此耗时较长的命令不会阻塞其他流程。操作仍须在 30 秒内完成，且其启动的任何命令都会在操作返回时停止。如果要执行需要持续运行的命令，可以使用 [`rex.exec.start`](https://www.superlogical.com/rex/docs/reference/lua.md#rexexecstartargv-opts) 并设置 `detach = true`。

[Lua 脚本](https://www.superlogical.com/rex/docs/automate/lua-scripts.md#running-commands)更详细地介绍了 `rex.exec`。

## 重新加载前测试操作

`rex do` 可以在不影响正在运行的配置的情况下，加载文件并运行其中的某个操作。向命令传入文件路径，并通过 `--action` 指定操作名称：

```sh
rex do ~/.config/rex/init.lua --action dev_layout file=app.log
```

这是快速迭代操作的一种便捷方式。操作会切实执行，并作用于运行该命令的会话。
