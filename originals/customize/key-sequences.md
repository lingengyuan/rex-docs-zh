---
title: "Key Sequences"
canonical_url: https://www.superlogical.com/rex/docs/customize/key-sequences
---

# Key Sequences

A key sequence is two or more keys pressed one after another, such as
<kbd>Ctrl</kbd>+<kbd>B</kbd> and then <kbd>C</kbd>. Sequences are bound with
`rex.bind` like any other [keyboard shortcut](https://www.superlogical.com/rex/docs/customize/keyboard-shortcuts.md),
with the keys joined by `>`:

```lua
rex.bind("ctrl+b>c", "client.tab.new")
rex.bind("ctrl+b>z", "pane.zoom")
```

Each key in a sequence is written the same way as a single key, modifiers
included. A sequence can be longer than two keys:

```lua
rex.bind("ctrl+b>shift+5", "pane.split", { direction = "right" })
rex.bind("ctrl+x>ctrl+k>s", "session.switch")
```

Press <kbd>Escape</kbd> partway through a sequence to cancel it.

## Example: Tmux Bindings

```lua
rex.bind("ctrl+b>c", "client.tab.new")
rex.bind("ctrl+b>n", "client.tab.next")
rex.bind("ctrl+b>p", "client.tab.previous")
-- % and " on a US layout
rex.bind("ctrl+b>shift+5", "pane.split", { direction = "right" })
rex.bind("ctrl+b>shift+'", "pane.split", { direction = "down" })
rex.bind("ctrl+b>z", "pane.zoom")
rex.bind("ctrl+b>x", "pane.close")

-- Press Ctrl+B twice to send one to the terminal
rex.bind("ctrl+b>ctrl+b", "pane.send_key", { key = "ctrl+b" })
```

Note the last binding. Once <kbd>Ctrl</kbd>+<kbd>B</kbd> starts a sequence
it no longer reaches the terminal by itself, so programs that use it need
another way to receive it.

## Binding vs. Sequence Conflict

A key either runs an action immediately or starts a sequence. It can't do
both, because Rex would have to wait to find out which you meant.

When a key is bound both ways, the newer binding wins and the older one never
runs:

```lua
rex.bind("cmd+k", "pane.zoom")         -- never runs
rex.bind("cmd+k>s", "session.switch")  -- cmd+k starts a sequence
```

With the two lines swapped, <kbd>Cmd</kbd>+<kbd>K</kbd> zooms immediately and
the sequence can never start.

The same rule applies across the [three places shortcuts come from](https://www.superlogical.com/rex/docs/customize/keyboard-shortcuts.md#how-shortcuts-are-resolved).
A sequence in your configuration file hides the client's default shortcut for
its first key, and a shortcut set in the app hides a sequence in the file that
starts with the same key.

Rex doesn't reorder anything to avoid this. Instead, the client is given a
warning that names both bindings and where each was written.

## Removing a Sequence

`rex.unbind` removes exactly one binding:

```lua
rex.unbind("ctrl+b>c")   -- removes this one sequence
rex.unbind("ctrl+b")     -- removes ctrl+b alone, and no sequences
```

Unbinding a key never removes the sequences that start with it. Each sequence
has to be unbound by its full name. A future change to Rex will allow
removing all sequences by prefix.

## Binding a Lua Function

A sequence can run a Lua function. The function is called when the last key of
the sequence is pressed:

```lua
rex.bind("ctrl+x>ctrl+s", function(ctx, ev)
  -- ev.prefix is { "ctrl+x" } and ev.keybinding is "ctrl+s"
  return true
end)
```

`ev.keybinding` is the last key and `ev.prefix` is a list of the keys before
it. One function bound to several sequences can use these to tell which one
was pressed. A function bound to a single key has no `ev.prefix`.

If the function returns `false` or nothing, only the last key is sent to the
focused terminal. The earlier keys were already consumed by the client.
