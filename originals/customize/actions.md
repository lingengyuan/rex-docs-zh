---
title: "Custom Actions"
canonical_url: https://www.superlogical.com/rex/docs/customize/actions
---

# Custom Actions

A custom action is a named Lua function defined in the
[configuration file](https://www.superlogical.com/rex/docs/customize/config.md) with `rex.action`. Once defined, it
works like any built-in action: it can be bound to a key, it appears in the
command palette, and it can be run from the CLI.

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

Run `rex config reload` after changing the file for the action to become
available. Then press <kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>N</kbd>, search for
"Open Scratch Window" in the command palette, or run it from the CLI:

```sh
rex do scratch
```

## Defining an Action

`rex.action` takes a table. `name`, `title`, and `run` are required.

| Field | Description |
| --- | --- |
| `name` | How the action is referred to in `rex.bind` and on the CLI. Lowercase letters, digits, and underscores only. |
| `title` | The text shown in the command palette and in menus. |
| `run` | The function to call when the action is run. |
| `description` | A longer explanation for the command palette. |
| `category` | A group for the command palette. Defaults to `Actions`. |
| `keywords` | Extra words the command palette search should match. |
| `args` | The arguments the action takes. See [Arguments](#arguments). |
| `repeats` | Set to `true` to run the action again while its key is held down. |

A custom action's name can't contain a dot. Dotted names such as `pane.split`
belong to clients and blocks. All custom actions have no dot. This is a small
visual language that makes it easier to tell where an action comes from.

Defining the same name twice is reported as a warning and the later
definition wins.

## Arguments

`args` declares each argument an action takes and its type. A trailing `?`
marks an argument as optional:

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

The types are `string`, `number`, `integer`, `boolean`, `object`, `array`, and
`any`.

Declaring arguments lets Rex catch mistakes before the action runs. A binding
that passes a misspelled or wrongly-typed argument is reported as a warning
when the client loads its keymap, and the CLI rejects it outright:

```
$ rex do dev_layout file=app.log bogus=1
Error: no argument named "bogus"; the action takes file, ratio?
```

An action that doesn't declare `args` accepts anything.

For more control, `args` can instead be a [JSON Schema](https://json-schema.org)
written as a Lua table. A table with a `type` key is treated as a schema and
used exactly as written.

## The Run Function

`run` is called with two tables: `ctx` describes where the action was run and
`args` holds its arguments. `args` is always a table, even when no arguments
were passed.

| Field | Description |
| --- | --- |
| `ctx.session_id` | The session the action applies to. |
| `ctx.block_id` | The block the action applies to, usually the focused one. |
| `ctx.client_id` | The client that asked for the action. |
| `ctx.origin` | How the action was run: `key`, `palette`, `cli`, `api`, or `script`. |

A field is absent when Rex doesn't know its value.

Rex API calls inside `run` default to the action's own session, so the
examples on this page never pass a `session_id`. A call that acts on one
block, such as `rex.session.set_block_label`, still needs a `block_id`. Pass
`ctx.block_id` for the focused one. The
[Lua API reference](https://www.superlogical.com/rex/docs/reference/lua.md) has the full list of calls.

### Errors

A failed API call doesn't stop the function. It returns `nil` and an error
message, so check the second return value when the result matters:

```lua
local w, err = rex.session.new_window{ layout = layout }
if err ~= nil then error(err, 0) end
```

Raising an error with `error` fails the action and reports the message to
whoever ran it.

### Return Values

Whatever `run` returns is the action's result, which the CLI prints as JSON:

```
$ rex do dev_layout file=app.log
{"window_id":"window:01a10dd6-ce31-760a-a9e5-c273c73fdd7e"}
```

Returning nothing, `nil`, or `true` means there is no result.

## Running an Action

**From a key.** Bind it by name, the same as a built-in action. See
[Keyboard Shortcuts](https://www.superlogical.com/rex/docs/customize/keyboard-shortcuts.md).

```lua
rex.bind("shift+cmd+l", "dev_layout", { file = "app.log" })
```

**From the command palette.** Search for the action's title.

**From the CLI.** Use `rex do` with the action's name and its arguments as
`key=value` pairs. Add `--json` for formatted output.

```sh
rex do dev_layout file=app.log ratio=0.3
```

`rex actions` lists the custom actions the server has loaded.

## Calling Other Actions

`rex.invoke` runs another custom action from inside `run` and returns its
result. It runs with the same session, block, and client.

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

`rex.client.queue` asks the client that ran the action to perform one of its
own actions, such as closing the command palette or zooming a pane. Queued
actions run in order after `run` returns, and are discarded if `run` fails.

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

`rex.client.queue` needs a client, so it raises an error when the action is
run from the CLI and no client can be found. The app also only accepts actions
from the CLI when Remote Control is turned on in its settings.

## Running Commands

`rex.exec` runs a command and returns what it printed and how it exited:

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

While an action waits for a command, the server keeps handling keys and
other actions, so a slow command doesn't hold anything else up. The action
still has 30 seconds to finish, and any command it started is stopped when it
returns. Use [`rex.exec.start`](https://www.superlogical.com/rex/docs/reference/lua.md#rexexecstartargv-opts) with
`detach = true` for a command that should keep running.

[Lua Scripts](https://www.superlogical.com/rex/docs/automate/lua-scripts.md#running-commands) covers `rex.exec` in
more detail.

## Trying an Action Before Reloading

`rex do` can load a file and run one of its actions without touching the
running configuration. Pass the path to the file and name the action with
`--action`:

```sh
rex do ~/.config/rex/init.lua --action dev_layout file=app.log
```

This is a quick way to iterate on an action. The action really runs, against
the session you run the command in.
