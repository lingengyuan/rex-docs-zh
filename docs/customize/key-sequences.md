> 原文：https://www.superlogical.com/rex/docs/customize/key-sequences
> 原文版本：948e67da2d21（抓取于 2026-11-13）

# 按键序列

按键序列是指按顺序依次按下的两个或多个按键，例如先按 <kbd>Ctrl</kbd>+<kbd>B</kbd> 再按 <kbd>C</kbd>。按键序列与其他[快捷键](keyboard-shortcuts.md)一样使用 `rex.bind` 进行绑定，按键之间使用 `>` 连接：

```lua
rex.bind("ctrl+b>c", "client.tab.new")
rex.bind("ctrl+b>z", "pane.zoom")
```

序列中的每个按键（包括修饰键）的写法与单个按键相同。按键序列也可以包含两个以上的按键：

```lua
rex.bind("ctrl+b>shift+5", "pane.split", { direction = "right" })
rex.bind("ctrl+x>ctrl+k>s", "session.switch")
```

在按键序列输入途中按下 <kbd>Escape</kbd> 可以取消该序列。

## 示例：Tmux 键位绑定

```lua
rex.bind("ctrl+b>c", "client.tab.new")
rex.bind("ctrl+b>n", "client.tab.next")
rex.bind("ctrl+b>p", "client.tab.previous")
-- 美式键盘布局下的 % 和 "
rex.bind("ctrl+b>shift+5", "pane.split", { direction = "right" })
rex.bind("ctrl+b>shift+'", "pane.split", { direction = "down" })
rex.bind("ctrl+b>z", "pane.zoom")
rex.bind("ctrl+b>x", "pane.close")

-- 连按两次 Ctrl+B 向终端发送一个 Ctrl+B
rex.bind("ctrl+b>ctrl+b", "pane.send_key", { key = "ctrl+b" })
```

注意最后一个绑定。一旦 <kbd>Ctrl</kbd>+<kbd>B</kbd> 作为按键序列的开头，它本身就不会再直接发送给终端；因此需要使用该按键的程序必须通过其他方式接收它。

## 单键绑定与按键序列冲突

一个按键要么立即运行某个操作，要么开启一个按键序列，两者不能兼得，否则 Rex 必须等待才能判断意图。

当同一个按键同时以这两种方式绑定时，以较新的绑定为准，较旧的绑定将永远不会执行：

```lua
rex.bind("cmd+k", "pane.zoom")         -- 永远不会执行
rex.bind("cmd+k>s", "session.switch")  -- cmd+k 用于开启按键序列
```

如果调换这两行，按下 <kbd>Cmd</kbd>+<kbd>K</kbd> 会立即缩放窗格，按键序列永远无法触发。

这条规则同样适用于[快捷键的三个来源](keyboard-shortcuts.md#快捷键解析规则)。配置文件中的按键序列会覆盖客户端为其首个按键提供的默认快捷键；而在应用中设置的快捷键又会覆盖配置文件中以相同按键开头的序列。

Rex 不会为了避免冲突调整顺序，而是会向客户端发出警告，指出冲突的两个绑定及其定义位置。

## 移除按键序列

`rex.unbind` 会精确移除单个绑定：

```lua
rex.unbind("ctrl+b>c")   -- 仅移除这一个按键序列
rex.unbind("ctrl+b")     -- 仅移除单独的 ctrl+b，不影响任何按键序列
```

解绑某个按键绝不会移除以该按键开头的按键序列。每个按键序列都必须使用完整名称进行解绑。Rex 后续会支持通过前缀批量移除所有按键序列。

## 绑定 Lua 函数

按键序列也可以运行 Lua 函数。当按下序列中的最后一个按键时，该函数会被调用：

```lua
rex.bind("ctrl+x>ctrl+s", function(ctx, ev)
  -- ev.prefix 为 { "ctrl+x" }，ev.keybinding 为 "ctrl+s"
  return true
end)
```

`ev.keybinding` 表示最后一个按键，`ev.prefix` 是此前按下的按键列表。如果一个函数绑定了多个按键序列，可以通过这些属性判断触发的是哪一个序列。绑定到单个按键的函数没有 `ev.prefix`。

如果函数返回 `false` 或未返回任何内容，只有最后一个按键会被发送到获得焦点的终端，前面的按键已在此前被客户端消耗。
