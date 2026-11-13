---
title: "Keyboard Shortcuts"
canonical_url: https://www.superlogical.com/rex/docs/customize/keyboard-shortcuts
---

# Keyboard Shortcuts

Keyboard shortcuts are defined in the [configuration file](https://www.superlogical.com/rex/docs/customize/config.md)
with `rex.bind` and removed with `rex.unbind`. A shortcut binds a key to an
**action**, such as splitting a pane or switching sessions.

```lua
rex.bind("cmd+e", "pane.zoom")
rex.bind("shift+cmd+d", "pane.split", { direction = "down" })
```

Run `rex config reload` after changing the file for the shortcuts to take
effect.

## Binding a Key

`rex.bind` takes a key, the name of an action, and optionally a table of
arguments for that action:

```lua
rex.bind(key, action, args)
```

Some actions require arguments and some have optional arguments. For
example, `pane.resize` requires a `direction` and accepts an optional
`amount`:

```lua
rex.bind("ctrl+alt+left", "pane.resize", { direction = "left" })
rex.bind("ctrl+alt+shift+left", "pane.resize", {
  direction = "left",
  amount = 15,
})
```

Binding a key that already has a binding replaces it. The newest binding
for a key always wins.

## Finding Actions

Actions are provided by the client, so the list depends on which client you
use. List the actions of a connected client with the CLI:

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

The `ARGS` column lists the arguments each action takes. An argument followed
by `?` is optional.

You can also define your own actions in Lua and bind keys to them. See
[Custom Actions](https://www.superlogical.com/rex/docs/customize/actions.md).

## Writing Keys

A key is written as zero or more modifiers followed by one key, joined by
`+`. Case and the order of modifiers don't matter, so `shift+cmd+d` and
`Cmd+Shift+D` are the same key.

| Modifier | Also Written |
| --- | --- |
| `cmd` | `command`, `super`, `meta`, `win` |
| `ctrl` | `control` |
| `alt` | `opt`, `option` |
| `shift` | |

The key is a character such as `d`, `1`, or `,` or a name such as `enter`,
`escape`, `tab`, `space`, `backspace`, `delete`, `left`, `right`, `up`, `down`,
`home`, `end`, `pageup`, `pagedown`, or `f1` through `f12`.

Keys follow your keyboard layout: `ctrl+a` is whichever key types "a". To bind
a physical key regardless of layout, write its US-layout name in brackets,
such as `ctrl+[KeyA]`. The names are the
[W3C `KeyboardEvent.code` values](https://www.w3.org/TR/uievents-code/#code-value-tables),
such as `[Digit1]`, `[Slash]`, and `[ArrowLeft]`.

Write the key without shift applied. On a US layout, plus is `cmd+shift+=`,
not `cmd++`. Bindings are always matched on unshifted keys.

A shortcut can also be several keys pressed one after another, such as
`ctrl+b>c`. See [Key Sequences](https://www.superlogical.com/rex/docs/customize/key-sequences.md).

Shortcuts can also be grouped into a mode that is only active when you enter
it, such as a mode for resizing panes. See [Key Modes](https://www.superlogical.com/rex/docs/customize/key-modes.md).

## Removing a Shortcut

`rex.unbind` removes every binding for a key. It can be used to remove
a binding you set as well as unbind a key that the client defaults with:

```lua
rex.unbind("cmd+d")
```

Pass an action name to remove the key only when it is bound to that action:

```lua
rex.unbind("cmd+t", "client.tab.new")
```

An unbound key isn't handled by Rex at all, so it is sent to the focused
terminal.

To change what a default shortcut does, bind it. There is no need to unbind
it first:

```lua
-- Cmd+K clears the screen instead
rex.bind("cmd+k", "pane.send_key", { key = "ctrl+l" })
```

## How Shortcuts Are Resolved

A key can get its meaning from three places. From lowest to highest priority:

1. The default shortcuts the client ships with.
2. Your configuration file.
3. Shortcuts you set in the client itself, such as with the app's
   **Change Shortcut...** command.

A shortcut set in the app therefore wins over the configuration file. If a
binding in your file appears to do nothing, check that the app doesn't have its
own shortcut for the same key.

## Binding a Lua Function

A key can run a Lua function instead of an action. Return `true` to say the
key was handled:

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

The function can call any Rex API, such as `rex.session.new_window` above.
The [Lua API reference](https://www.superlogical.com/rex/docs/reference/lua.md) has the full list.

If the function returns `false` or nothing, Rex tries the next-newest function
bound to the same key, and sends the key to the focused terminal if none of
them handle it.

A function binding has no name, so it doesn't appear in the command palette
and can't be run from the CLI. For anything you'd want to do more than one
way, define a [custom action](https://www.superlogical.com/rex/docs/customize/actions.md) and bind the key to that.

## Inspecting Bindings

A configuration that loads other files with `require` can look at what they
bound and remove what it doesn't want. `rex.bindings()` returns every binding
made so far, in the order they were made.

```lua
require("keys")

-- Remove every sequence keys.lua bound behind ctrl+b
for _, b in ipairs(rex.bindings()) do
  if b.key:find("ctrl+b>", 1, true) == 1 then
    rex.unbind(b)
  end
end
```

Each binding is a table with `key`, `mode`, `action`, `args`, and `source`
(the file and line that made it). Passing one to `rex.unbind` removes exactly
that binding.

`rex.bindings` also accepts a filter on `key`, `mode`, or `action`, such as
`rex.bindings{ action = "pane.split" }`. `rex.modes()` does the same for
[key modes](https://www.superlogical.com/rex/docs/customize/key-modes.md).

These functions only see your configuration file and the files it loads. They
can't see the client's default shortcuts or the ones set in the app.

## Debugging

`rex config check` reports mistakes in the file itself, such as a key that
can't be parsed:

```
$ rex config check
...
error init.lua:1: unknown key "foo"
Error: the configuration has errors
```

`rex keymap` asks the running server what it loaded and lists each binding
with the line that made it:

```
$ rex keymap
KEY          ACTION          ARGS                  SOURCE
shift+cmd+d  pane.split      {"direction":"down"}  init.lua:2
cmd+e        pane.zoom       -                     init.lua:1
...
```

A misspelled action name is not an error in `rex config check`, because the
file alone can't know which actions a client has. The client reports it as a
warning when it loads the keymap.
