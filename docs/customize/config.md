> 原文：https://www.superlogical.com/rex/docs/customize/config
> 原文版本：adc963f645f4（抓取于 2026-11-26）

# 配置文件

Rex 的配置使用 [Lua](https://www.lua.org) 编写，保存在单个文件中：`init.lua`。它负责绑定按键、定义自定义操作、声明要连接的其他服务端等。它可以通过 `require` 加载其他 Lua 文件，方便按需拆分配置。

Rex 不需要任何配置即可使用。先直接上手体验 Rex，需要修改设置时再创建配置文件。

## 文件位置

在 **macOS 和 Linux** 上，如果设置了 `$XDG_CONFIG_HOME` 环境变量，文件位于 `$XDG_CONFIG_HOME/rex/init.lua`；未设置时位于 `~/.config/rex/init.lua`。

在 **Windows** 上，文件位于 `%AppData%\rex\init.lua`。

将 `REX_CONFIG` 环境变量设为其他文件路径，可以改用该文件。该环境变量必须在 Rex 服务端进程的环境中设置，因为配置文件由服务端读取。

## 快速示例

以下是包含一个按键绑定的最小配置示例：

```lua
rex.bind("cmd+d", "pane.split", { direction = "right" })
```

使用 CLI 重新加载配置。已连接的客户端会收到新配置通知，配置会立即生效。Rex 目前不会自动监听文件变动，必须通过 CLI 触发重新加载。

```sh
rex config reload
```

配置文件由 Rex 服务端读取，因此它与服务端位于同一台机器上。`rex config reload` 也必须在该机器上运行，不支持通过远程连接执行。

按下 <kbd>Cmd</kbd>+<kbd>D</kbd>，获得焦点的窗格就会向右拆分。

[Lua API 参考](../reference/lua.md)列出了所有可用的 Lua API。

## 设置

`rex.set` 用于设置 Rex 配置项：

```lua
rex.set("resume.trust.codex", false)
```

设置项名称是以点分隔的键，便于配置嵌套值。值可以是布尔值、数字、字符串或表，具体类型取决于所配置的设置项键。

目前设置项仅用于[恢复规则](https://www.superlogical.com/rex/docs/customize/resume-rules.md)，但未来版本的 Rex 将会使用同一套接口来管理所有通用设置。

如果当前版本的 Rex 不认识某个设置项，只会发出警告而非报错，因此同一份配置文件可以兼容新旧版本。

设置项只能在文件加载期间设置。在操作（action）中调用 `rex.set` 会报错。

## 校验配置

`rex config check` 会在不更改任何内容的情况下加载文件，并报告发现的问题。如果没有问题，它会报告检测到的改动：

```
$ rex config check
path: /Users/you/.config/rex/init.lua
exists: yes
bindings: 8
removals: 0
modes: 1
actions: 0
settings: 0
resume rules: 3
```

如果存在错误，这两个命令都会输出文件中的问题，并以状态码 1 退出。向 `rex config check` 传入路径，可以检查自身配置之外的文件，例如草稿文件。

### 校验错误

调用 `rex` 函数时如果传入错误参数，该调用会被跳过，文件的其余部分仍会正常加载。下例中第 2 行本应传入按键，却传入了一个表：

```lua
rex.bind("cmd+d", "pane.split", { direction = "right" })
rex.bind({ "cmd+k" }, "pane.split")
rex.bind("ctrl+b>c", "window.new")
```

```
$ rex config check
...
bindings: 2
...
error init.lua:2: rex.bind: expected a string, got table
Error: the configuration has errors
```

其余两个绑定仍会生效。

如果遇到 Lua 自身无法解析的问题（例如语法错误），整个加载过程都会失败。如果在重新加载时出现该情况，服务端会保留上一次成功加载的绑定和操作。

部分问题无法仅凭文件本身发现。例如 `pane.split` 是否为真实操作取决于客户端，因为这些操作由客户端提供。`rex keymap` 会向正在运行的服务端查询合并后的结果，并报告这类问题。

## 拆分配置

`require` 可以加载存放在同目录下的其他 Lua 文件：

```lua
-- ~/.config/rex/init.lua
require("keys")
```

```lua
-- ~/.config/rex/keys.lua
rex.bind("cmd+d", "pane.split", { direction = "right" })
rex.bind("ctrl+b>c", "window.new")
```

错误信息会包含所在文件的文件名，例如 `keys.lua:2`。

## 执行模型

每次加载时，文件都会从头到尾执行一遍。

加载时的执行用于定义绑定、操作等。它们的回调函数会推迟到被调用时执行。列出会话或新建窗口等 Rex API 在加载时无法调用，因为 API 调用需要代表客户端发起，而加载时并没有客户端。这类调用会记录为警告，文件的其余部分仍会继续加载。

示例：

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
```

这里定义了 `scratch` 操作，但在通过命令面板、按键绑定等方式实际调用该操作之前，并不会执行包含 `rex.session.new_window` 的回调函数。

如果想对运行中的会话自顶向下执行一次 Lua 代码，可以编写独立的脚本并通过 `rex do` 运行。
