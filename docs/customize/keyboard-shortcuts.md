> 原文：https://www.superlogical.com/rex/docs/customize/keyboard-shortcuts
> 原文版本：4a48aaa5db26（抓取于 2026-11-13）

# 快捷键

快捷键在[配置文件](config.md)中使用 `rex.bind` 定义，使用 `rex.unbind` 移除。快捷键将按键绑定到**操作**（action），例如拆分窗格或切换会话。

```lua
rex.bind("cmd+e", "pane.zoom")
rex.bind("shift+cmd+d", "pane.split", { direction = "down" })
```

修改文件后运行 `rex config reload`，使快捷键生效。

## 绑定按键

`rex.bind` 接收按键、操作名称以及可选的操作参数表：

```lua
rex.bind(key, action, args)
```

部分操作需要参数，部分操作支持可选参数。例如 `pane.resize` 需要 `direction`，并支持可选的 `amount`：

```lua
rex.bind("ctrl+alt+left", "pane.resize", { direction = "left" })
rex.bind("ctrl+alt+shift+left", "pane.resize", {
  direction = "left",
  amount = 15,
})
```

为一个已有绑定的按键设置新绑定会替换原有绑定。同一个按键总是以最新的绑定为准。

## 查找操作

操作由客户端提供，因此操作列表取决于使用的客户端。通过 CLI 可以列出已连接客户端的操作：

```
$ rex client ls
LABEL     CLIENT                KIND  PRINCIPAL          AGE     ID
my-mac    Rex Beta 0.1.0 (996)  app   uid 501 over unix  1h ago  db494d

$ rex -C my-mac actions
NAME                   TITLE             ARGS
client.tab.new         New Tab
client.tab.goto        Go to Tab         index
pane.split             Split Pane        direction
pane.zoom              Zoom Pane
pane.resize            Resize Pane       direction, amount?
pane.send_key          Send Key          key
session.switch         Change Session…
...
```

`ARGS` 列列出了每个操作接收的参数。带 `?` 后缀的参数为可选参数。

也可以用 Lua 自定义操作并为其绑定按键。详见[自定义操作](actions.md)。

## 编写按键格式

按键由零个或多个修饰键加上一个按键组成，中间用 `+` 连接。修饰键不区分大小写，顺序也不受限制，因此 `shift+cmd+d` 和 `Cmd+Shift+D` 表示同一个按键。

| 修饰键 | 其他写法 |
| --- | --- |
| `cmd` | `command`, `super`, `meta`, `win` |
| `ctrl` | `control` |
| `alt` | `opt`, `option` |
| `shift` | |

按键可以是一个字符（如 `d`、`1`、`,`），也可以是一个名称（如 `enter`、`escape`、`tab`、`space`、`backspace`、`delete`、`left`、`right`、`up`、`down`、`home`、`end`、`pageup`、`pagedown` 或 `f1` 至 `f12`）。

按键遵循当前的键盘布局：`ctrl+a` 对应输入“a”的按键。如果要绑定不受键盘布局影响的物理按键，可以用中括号写入其美式键盘布局名称，例如 `ctrl+[KeyA]`。这些名称采用 [W3C `KeyboardEvent.code` 的取值](https://www.w3.org/TR/uievents-code/#code-value-tables)，例如 `[Digit1]`、`[Slash]` 和 `[ArrowLeft]`。

编写按键时不要包含 Shift 产生的影响。在美式键盘布局中，加号键应写为 `cmd+shift+=`，而不是 `cmd++`。绑定始终与未按 Shift 时的原始按键进行匹配。

快捷键也可以是按顺序依次按下的多个键，例如 `ctrl+b>c`。详见[按键序列](key-sequences.md)。

快捷键还可以分组为仅在进入时激活的模式，例如调整窗格大小的模式。详见[按键模式](key-modes.md)。

## 移除快捷键

`rex.unbind` 会移除某个按键的所有绑定。既可以用来移除自己设置的绑定，也可以解绑客户端默认提供的按键：

```lua
rex.unbind("cmd+d")
```

传入操作名称，可以在按键绑定到该操作时才将其移除：

```lua
rex.unbind("cmd+t", "client.tab.new")
```

未绑定的按键不会被 Rex 处理，而是直接发送给获得焦点的终端。

要更改默认快捷键的行为，直接重新绑定即可，无需先解绑：

```lua
-- 改为由 Cmd+K 执行清屏
rex.bind("cmd+k", "pane.send_key", { key = "ctrl+l" })
```

## 快捷键解析规则

按键的定义可能来自三个来源。优先级从低到高依次为：

1. 客户端自带的默认快捷键。
2. 配置文件。
3. 在客户端中自行设置的快捷键，例如应用中的 **Change Shortcut...**（更改快捷键…）命令。

因此，在应用中设置的快捷键优先级高于配置文件。如果配置文件中的绑定似乎没有生效，请检查应用中是否为同一按键设置了快捷键。

## 绑定 Lua 函数

按键也可以运行 Lua 函数而不是预定义操作。返回 `true` 表示该按键已处理完毕：

```lua
rex.bind("ctrl+shift+n", function(ctx, ev)
  rex.session.new_window{
    layout = rex.layout.block{
      flavor = "com.superlogical.terminal.shell",
    },
  }
  return true
end)
```

该函数可以调用任意 Rex API，例如上例中的 `rex.session.new_window`。[Lua API 参考](../reference/lua.md)提供了完整列表。

如果函数返回 `false` 或未返回任何内容，Rex 会尝试绑定到同一按键的次新函数；若均未处理，则将按键发送给获得焦点的终端。

函数绑定没有名称，因此不会出现在命令面板中，也无法通过 CLI 运行。如果某项功能需要通过多种途径触发，建议定义[自定义操作](actions.md)并将按键绑定到该操作。

## 查看绑定

通过 `require` 加载其他文件的配置可以检查已绑定的内容，并移除不需要的项。`rex.bindings()` 会按创建顺序返回当前已定义的所有绑定。

```lua
require("keys")

-- 移除 keys.lua 中以 ctrl+b 开头绑定的所有按键序列
for _, b in ipairs(rex.bindings()) do
  if b.key:find("ctrl+b>", 1, true) == 1 then
    rex.unbind(b)
  end
end
```

每个绑定都是一个包含 `key`、`mode`、`action`、`args` 和 `source`（创建该绑定的文件和行号）的表。将该表传给 `rex.unbind` 可以精确移除对应绑定。

`rex.bindings` 还支持按 `key`、`mode` 或 `action` 过滤，例如 `rex.bindings{ action = "pane.split" }`。`rex.modes()` 对[按键模式](key-modes.md)提供了相同功能。

这些函数只能看到当前配置文件及其加载的文件，无法获取客户端的默认快捷键或在应用中设置的快捷键。

## 调试

`rex config check` 会报告文件本身的错误，例如无法解析的按键：

```
$ rex config check
...
error init.lua:1: unknown key "foo"
Error: the configuration has errors
```

`rex keymap` 会向正在运行的服务端查询已加载的内容，并列出每个绑定及其对应的源文件行号：

```
$ rex keymap
KEY          ACTION          ARGS                  SOURCE
shift+cmd+d  pane.split      {"direction":"down"}  init.lua:2
cmd+e        pane.zoom       -                     init.lua:1
...
```

拼写错误的操作名不会在 `rex config check` 中报错，因为仅凭文件无法得知客户端拥有哪些操作。客户端会在加载键位映射（keymap）时将其作为警告报告。
