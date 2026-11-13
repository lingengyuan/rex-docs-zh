---
title: "Key Modes"
canonical_url: https://www.superlogical.com/rex/docs/customize/key-modes
---

# Key Modes

A key mode is a named set of [keyboard shortcuts](https://www.superlogical.com/rex/docs/customize/keyboard-shortcuts.md)
that only apply while the mode is active. Modes let ordinary keys do something
else for a while, such as making the arrow keys resize panes. They are also
called "key tables" in other software.

```lua
rex.bind("cmd+r", "client.mode.enter", { name = "resize" })

rex.bind("resize/left", "pane.resize", { direction = "left" })
rex.bind("resize/right", "pane.resize", { direction = "right" })
rex.bind("resize/up", "pane.resize", { direction = "up" })
rex.bind("resize/down", "pane.resize", { direction = "down" })
```

Press <kbd>Cmd</kbd>+<kbd>R</kbd> to enter the mode. The arrow keys now resize
the focused pane. Press <kbd>Escape</kbd> to leave the mode, and the arrow
keys go back to what they did before.

## Binding a Key in a Mode

To bind a key in a mode, write the mode's name and a slash `/` before the key:

```lua
rex.bind("resize/shift+left", "pane.resize", {
  direction = "left",
  amount = 15,
})
```

A mode exists as soon as a key is bound in it. A mode name may contain only
lowercase letters, digits, underscores, and hyphens.

The key after the slash can be anything a shortcut outside a mode can be,
including a [key sequence](https://www.superlogical.com/rex/docs/customize/key-sequences.md) such as `resize/g>g`.

Bindings in a mode are separate from bindings outside it. Binding `resize/left`
doesn't change what <kbd>Left</kbd> does outside the mode.

A binding in a mode must name an action. To run Lua from a mode, define a
[custom action](https://www.superlogical.com/rex/docs/customize/actions.md) and bind that.

## Entering and Leaving a Mode

The client provides three actions for moving between modes. Bind them like any
other action:

| Action | Description |
| --- | --- |
| `client.mode.enter` | Enters the mode given by `name`. |
| `client.mode.exit` | Leaves the current mode. |
| `client.mode.exit_all` | Leaves every mode. |

<kbd>Escape</kbd> also leaves the current mode, unless the mode binds
<kbd>Escape</kbd> to something else.

A mode stays active until you leave it. To leave automatically after one
shortcut, enter it with `once`:

```lua
rex.bind("cmd+r", "client.mode.enter", {
  name = "resize",
  once = true,
})
```

Modes can be entered from inside other modes. The most recently entered mode
is checked first, and `client.mode.exit` leaves only that one.

## Unbound Keys in a Mode

By default, a key the mode doesn't bind does what it does outside the mode.
In the resize example, you can still type in the terminal while the mode is
active.

Declare the mode as `exclusive` to ignore those keys instead:

```lua
rex.mode("resize", { exclusive = true })
```

While an exclusive mode is active, only its own bindings do anything. This
avoids typing into a terminal by accident while you think you're resizing.

`rex.mode` is only needed to set options. `exclusive` is the only option.

## Removing Bindings

`rex.unbind` with a mode and a key removes that key's bindings in the mode
and **blocks** the key there. A blocked key does nothing while the mode is
active, even if it is bound outside the mode:

```lua
rex.unbind("resize/left")
```

Pass an action name to remove one binding without blocking the key:

```lua
rex.unbind("resize/left", "pane.resize")
```

To remove a whole mode, including its bindings, blocked keys, and options,
pass a table:

```lua
rex.unbind{ mode = "resize" }
```

`rex.unbind("left")` never touches a mode, and `rex.unbind("resize/left")`
never touches <kbd>Left</kbd> outside the mode.

## Example: Resize Mode

A complete resize mode, entered with <kbd>Cmd</kbd>+<kbd>R</kbd>:

```lua
rex.mode("resize", { exclusive = true })
rex.bind("cmd+r", "client.mode.enter", { name = "resize" })

rex.bind("resize/left", "pane.resize", { direction = "left" })
rex.bind("resize/right", "pane.resize", { direction = "right" })
rex.bind("resize/up", "pane.resize", { direction = "up" })
rex.bind("resize/down", "pane.resize", { direction = "down" })

-- Hold shift for bigger steps
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

## Debugging

`rex keymap` lists every mode the server loaded after its bindings, along
with whether it is exclusive and which keys it blocks:

```
$ rex keymap
KEY           ACTION       ARGS                  SOURCE
resize/left   pane.resize  {"direction":"left"}  init.lua:4
...

MODE    EXCLUSIVE  BLOCKED
resize  yes        -
```
