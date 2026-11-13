> 原文：https://www.superlogical.com/rex/docs/customize/key-modes
> 原文版本：34a6bcda7099（抓取于 2026-11-13）

# 按键模式

按键模式是一组命名的[快捷键](keyboard-shortcuts.md)，仅在模式激活时生效。模式可以让普通按键在一段时间内执行其他功能，例如让方向键用于调整窗格大小。在其他软件中，它们也被称为“键表”（key tables）。

```lua
rex.bind("cmd+r", "client.mode.enter", { name = "resize" })

rex.bind("resize/left", "pane.resize", { direction = "left" })
rex.bind("resize/right", "pane.resize", { direction = "right" })
rex.bind("resize/up", "pane.resize", { direction = "up" })
rex.bind("resize/down", "pane.resize", { direction = "down" })
```

按下 <kbd>Cmd</kbd>+<kbd>R</kbd> 进入该模式。此时方向键会调整获得焦点的窗格的大小。按下 <kbd>Escape</kbd> 退出该模式，方向键会恢复原本的功能。

## 在模式中绑定按键

要在模式中绑定按键，需在按键前写上模式名称和一个斜杠 `/`：

```lua
rex.bind("resize/shift+left", "pane.resize", {
  direction = "left",
  amount = 15,
})
```

只要在某个模式中绑定了按键，该模式就会存在。模式名称只能包含小写字母、数字、下划线和连字符。

斜杠后的按键可以是模式外快捷键支持的任意形式，包括像 `resize/g>g` 这样的[按键序列](key-sequences.md)。

模式内的绑定与模式外的绑定相互独立。绑定 `resize/left` 不会改变模式外 <kbd>Left</kbd> 键的行为。

模式中的绑定必须指定操作名称。如果要从模式中运行 Lua 代码，可以定义[自定义操作](actions.md)并绑定到该操作。

## 进入与退出模式

客户端提供了三个在模式之间切换的操作。绑定方式与其他操作相同：

| 操作 | 说明 |
| --- | --- |
| `client.mode.enter` | 进入 `name` 参数指定的模式。 |
| `client.mode.exit` | 退出当前模式。 |
| `client.mode.exit_all` | 退出所有模式。 |

按下 <kbd>Escape</kbd> 也会退出当前模式，除非该模式将 <kbd>Escape</kbd> 绑定到了其他操作。

模式会一直保持激活状态，直到主动退出。如果要执行一次快捷键后自动退出，可以在进入模式时传入 `once`：

```lua
rex.bind("cmd+r", "client.mode.enter", {
  name = "resize",
  once = true,
})
```

可以在一个模式中进入另一个模式。Rex 会优先检查最近进入的模式，此时执行 `client.mode.exit` 只会退出该模式。

## 模式中未绑定的按键

默认情况下，模式中未绑定的按键仍会执行模式外的原有行为。在上述调整大小的示例中，模式激活时依然可以在终端中正常输入文字。

将模式声明为 `exclusive`（独占），则会忽略这些按键：

```lua
rex.mode("resize", { exclusive = true })
```

当独占模式激活时，只有该模式自身的绑定会生效。这样可以避免误以为处于调整大小模式而在终端中意外输入文字。

只有设置选项时才需要调用 `rex.mode`。目前 `exclusive` 是唯一的可用选项。

## 移除绑定

向 `rex.unbind` 传入模式和按键，会移除该按键在该模式中的绑定，并在该模式中**屏蔽**该按键。被屏蔽的按键在模式激活期间不会执行任何操作，即使它在模式外有绑定也是如此：

```lua
rex.unbind("resize/left")
```

传入操作名称可以移除单个绑定而不屏蔽该按键：

```lua
rex.unbind("resize/left", "pane.resize")
```

要移除整个模式（包括其绑定、被屏蔽的按键及配置选项），可以传入一个表：

```lua
rex.unbind{ mode = "resize" }
```

`rex.unbind("left")` 绝不会影响模式内的绑定，`rex.unbind("resize/left")` 也绝不会影响模式外的 <kbd>Left</kbd> 按键。

## 示例：调整窗格大小模式

以下是一个完整的调整大小模式示例，通过 <kbd>Cmd</kbd>+<kbd>R</kbd> 进入：

```lua
rex.mode("resize", { exclusive = true })
rex.bind("cmd+r", "client.mode.enter", { name = "resize" })

rex.bind("resize/left", "pane.resize", { direction = "left" })
rex.bind("resize/right", "pane.resize", { direction = "right" })
rex.bind("resize/up", "pane.resize", { direction = "up" })
rex.bind("resize/down", "pane.resize", { direction = "down" })

-- 按住 Shift 以更大步幅调整
rex.bind("resize/shift+left", "pane.resize", {
  direction = "left",
  amount = 15,
})
rex.bind("resize/shift+right", "pane.resize", {
  direction = "right",
  amount = 15,
})

rex.bind("resize/=", "pane.balance")
rex.bind("resize/enter", "client.mode.exit")
```

## 调试

`rex keymap` 会在列出绑定之后列出服务端加载的每一个模式，包括该模式是否独占以及屏蔽了哪些按键：

```
$ rex keymap
KEY           ACTION       ARGS                  SOURCE
resize/left   pane.resize  {"direction":"left"}  init.lua:4
...

MODE    EXCLUSIVE  BLOCKED
resize  yes        -
```
