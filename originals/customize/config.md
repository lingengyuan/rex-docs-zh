---
title: "Configuration File"
canonical_url: https://www.superlogical.com/rex/docs/customize/config
---

# Configuration File

Rex configuration is written in [Lua](https://www.lua.org) and lives in
a single file: `init.lua`. It binds keys, defines custom actions, declares
the other servers you connect to, and more. It can load other Lua files
(via `require`) so you can split your configuration up as you'd like.

Rex doesn't require any configuration, so start using Rex without it
and start a configuration file when there is something you want to change.

## File Location

On **macOS and Linux**, the file is at `$XDG_CONFIG_HOME/rex/init.lua` when
that environment variable is set and `~/.config/rex/init.lua` when it isn't.

On **Windows**, the file is at `%AppData%\rex\init.lua`.

Set `REX_CONFIG` to the path of another file to use that one instead.
This environment variable must be set in the environment of the Rex server
process, since the server is what reads the file.

## Quick Example

Here is a minimal configuration example with one keybinding:

```lua
rex.bind("cmd+d", "pane.split", { direction = "right" })
```

Reload the configuration with the CLI. Connected clients will be notified of
the new configuration and it will take effect immediately. Rex does not
currently watch for file changes; you must use the CLI.

```sh
rex config reload
```

The configuration file is read by the Rex server, so it lives on the same
machine as the server. `rex config reload` must also be run on that machine;
it is refused over a remote connection.

Press <kbd>Cmd</kbd>+<kbd>D</kbd> and the focused pane splits to the right.

The [Lua API reference](https://www.superlogical.com/rex/docs/reference/lua.md) lists all available Lua APIs.

## Settings

`rex.set` sets a Rex setting:

```lua
rex.set("resume.trust.codex", false)
```

The setting name is a dot-delimited key which allows easily setting nested
values. The value can be a boolean, number, string, or table, and the proper
type depends on the setting key being configured.

Settings today are only used for [Resume Rules](https://www.superlogical.com/rex/docs/customize/resume-rules.md), but
a future version of Rex will use this same interface for all of its general
settings.

A setting this version of Rex doesn't know is a warning, not an error, so the
same file works with older and newer versions.

Settings are only set while the file loads. Calling `rex.set` from an action
is an error.

## Validation

`rex config check` loads the file without changing anything and reports any
issues. If there are no issues, it reports the changes it found:

```
$ rex config check
path: /Users/you/.config/rex/init.lua
exists: yes
bindings: 8
removals: 0
modes: 1
actions: 0
settings: 0
resume rules: 7
...
```

Both commands print the file's mistakes and exit with status 1 if any of them
is an error. Give `rex config check` a path to check a file other than your
own, such as a draft.

### Validation Errors

A bad call to a `rex` function is skipped, and the rest of the file still
loads. Here line 2 passes a table where a key belongs:

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

The other two bindings still work.

A mistake Lua itself can't get past, such as a syntax error, fails the whole
load. When that happens on a reload, the server keeps the bindings and actions
from the last load that worked.

Some mistakes can't be seen from the file alone. Whether `pane.split` is a
real action depends on the client, because clients provide those actions.
`rex keymap` asks the running server for the merged result and reports these.

## Splitting Configuration

`require` loads other Lua files stored beside it:

```lua
-- ~/.config/rex/init.lua
require("keys")
```

```lua
-- ~/.config/rex/keys.lua
rex.bind("cmd+d", "pane.split", { direction = "right" })
rex.bind("ctrl+b>c", "window.new")
```

Mistakes are reported with the name of the file they are in, such as
`keys.lua:2`.

## Execution Model

The file runs from top to bottom each time it loads.

This load-time execution is for defining bindings, actions, etc. The callbacks
for these are deferred until they're invoked. Rex APIs such as listing sessions
or creating a new window do not work at load-time, since API calls are made on
behalf of a client and load-time has no client. They're reported as a warning
and the rest of the file still loads.

Example:

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

This defines the `scratch` action, but it doesn't invoke the callback
with `rex.session.new_window` until the action is actually invoked via
the command palette, a keybinding, etc.

To run Lua once from top to bottom against a live session, write a separate
script and run it with `rex do` instead.
