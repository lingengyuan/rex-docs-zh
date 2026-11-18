---
title: "Rex Lua API"
canonical_url: https://www.superlogical.com/rex/docs/reference/lua
---

# Rex Lua API

This page lists the full Lua API Rex exposes. Rex only adds API to the
global `rex` table.  Rex runs Lua 5.1 with the full standard library,
including `io`, `os`, and `require`. The one exception is `io.popen` and
`os.execute`, which raise an error. Use [`rex.exec`](#rexexecargv-opts) to run
commands instead.

## Where Each Function Works

Rex runs Lua in two places, the configuration file and scripts, and each
function below is tagged with where it works:

| Tag | Description |
| --- | --- |
| <span class="api-tag">Config</span> | Works in the [configuration file](https://www.superlogical.com/rex/docs/customize/config.md). |
| <span class="api-tag">Script</span> | Works in scripts run with [`rex do`](https://www.superlogical.com/rex/docs/automate/lua-scripts.md). |
| <span class="api-tag">Config <span class="when">at load</span></span> | Only at load, while the file runs from top to bottom. Either tag can be narrowed this way. |
| <span class="api-tag">Config <span class="when">later</span></span> | Only later, inside an action, a function bound to a key, or an event handler. |

Anything short of working is noted at the top of the function's docs.


| Function | Config, at load | Config, later | Script, at load | Script, later |
| --- | --- | --- | --- | --- |
| `rex.bind`, `rex.unbind` | Yes | Functions only | No effect | No effect |
| `rex.mode`, `rex.bindings`, `rex.modes` | Yes | Error | No effect | Error |
| `rex.action` | Yes | Error | Yes | Error |
| `rex.host` | Yes | Error | No effect | Error |
| `rex.on` | Warning | Error | Yes | Error |
| `rex.call`, `rex.session.*`, `rex.block.call` | Fails | Yes | Yes | Yes |
| `rex.invoke` | Warning | Yes | Yes | Yes |
| `rex.client.queue` | Error | Actions only | Yes | Yes |
| `rex.exec`, `rex.exec.start` | Yes | Yes | Yes | Yes |
| `rex.layout.*`, `rex.json.*`, `rex.log` | Yes | Yes | Yes | Yes |
| `rex.sleep`, `rex.wait`, `rex.stop` | Missing | Missing | Yes | Yes |
| `rex.after`, `rex.every` | Missing | Missing | Yes | Yes |
| `rex.args`, `rex.session_id`, `rex.block_id` | Missing | Missing | Yes | Yes |

- **No effect** means the call is accepted and does nothing useful. A script's
  key bindings and hosts never reach a keymap or the server.
- **Missing** means the name is `nil`. Calling it is an error, so a file shared
  between both should check for it first.
- **Fails** means the call returns `nil` and an error message, and is reported
  as a warning.

## Key Bindings

See [Keyboard Shortcuts](https://www.superlogical.com/rex/docs/customize/keyboard-shortcuts.md),
[Key Sequences](https://www.superlogical.com/rex/docs/customize/key-sequences.md), and [Key Modes](https://www.superlogical.com/rex/docs/customize/key-modes.md).

### `rex.bind(key, action[, args])`

Binds a key to an action by name. `args` is an optional table of arguments
passed to the action.

```lua
rex.bind("cmd+d", "pane.split", { direction = "right" })
```

`key` is a single key, a sequence written with `>`, or either one prefixed with
a mode and a slash.

### `rex.bind(key, fn)`

Binds a key to a Lua function called as `fn(ctx, ev)`. Return `true` to mark
the key as handled. Not allowed in a mode.

`ev.keybinding` is the key that was pressed. For a sequence, `ev.prefix` is a
list of the keys before it.

### `rex.unbind(key[, target])`

Removes the bindings of a key in this file and in the client's defaults.
Returns the number of this file's bindings it removed.

`target` is an action name or a function, and limits the removal to bindings
with that target. `rex.unbind("mode/key")` also blocks the key in that mode.

### `rex.unbind{ mode = name }`

Removes a whole mode: its bindings, its blocked keys, and its options.

### `rex.unbind(binding)`

Removes one binding, given a table returned by `rex.bindings`. Returns 1.

### `rex.mode(name[, options])`

Declares a mode and sets its options. The only option is `exclusive`, a
boolean that defaults to `false`.

### `rex.bindings([filter])`

Returns the bindings this file and the files it requires have made so far, in
order. `filter` is an optional table with any of `key`, `mode`, and `action`.

Each binding is a table:

| Field | Description |
| --- | --- |
| `key` | The key or sequence, without its mode. |
| `mode` | The mode, or `nil`. |
| `action` | The action name, or `nil` for a function binding. |
| `fn` | The function, or `nil` for an action binding. |
| `args` | The arguments table, or `nil`. |
| `source` | Where it was bound, such as `keys.lua:3`. |

### `rex.modes()`

Returns the modes declared or bound so far, each a table with `name`,
`exclusive`, and `source`.

## Actions

See [Custom Actions](https://www.superlogical.com/rex/docs/customize/actions.md).

### `rex.action{ ... }`

Defines an action.

| Field | Type | Description |
| --- | --- | --- |
| `name` | string | Required. Lowercase letters, digits, and underscores. |
| `title` | string | Required. Shown in the command palette. |
| `run` | function | Required. Called as `run(ctx, args)`. |
| `description` | string | A longer explanation. |
| `category` | string | A group for the palette. Defaults to `Actions`. |
| `keywords` | string | Extra words for search. |
| `args` | table | Argument types, or a JSON Schema. |
| `repeats` | boolean | Run again while the key is held. |

`args` types are `string`, `number`, `integer`, `boolean`, `object`, `array`,
and `any`. A trailing `?` marks an argument as optional.

`ctx` has `session_id`, `block_id`, `client_id`, `origin`, and `server`. A
field Rex doesn't know is absent. The value `run` returns is the action's
result.

### `rex.invoke(name[, args])`

Runs an action and returns its result, or `nil` and an error message.

In the configuration file, only that file's own actions can be invoked. In a
script, a name the script doesn't define is run by the server, so a script
can invoke actions from the configuration file.

Calls can nest up to 16 deep.

### `rex.client.queue(name[, args])`

Asks the client to perform one of its own actions, such as `pane.zoom`.

In an action, queued actions run in order after `run` returns, and are
discarded if it fails. In a script, each one is performed immediately.

Raises an error when there is no client to ask.

## Calling Rex

See [Lua Scripts](https://www.superlogical.com/rex/docs/automate/lua-scripts.md#calling-rex).

Every call in this section returns a result table, or `nil` and an error
message. A failure never raises an error.

### `rex.session.<method>(args)`

Calls a session method. `args` is a table. `session_id` is filled in when it
is left out. Other IDs, such as `block_id`, are not.

```lua
local view, err = rex.session.view{}
```

| Method | Description |
| --- | --- |
| `view` | Return the session's windows, layouts, and blocks. |
| `list_blocks` | List every block and whether it is placed or detached. |
| `list_clients` | List the clients attached to the session. |
| `describe_block` | Return a block's placement and the methods it offers. |
| `new_window` | Create a window from a layout. |
| `new_split` | Create a split beside an existing block. |
| `new_block` | Create a block without placing it in a layout. |
| `new_layer` | Create a floating layer in a window. |
| `close_window` | Close a window and every block in it. |
| `close_layer` | Close a floating layer and every block in it. |
| `move_block` | Move a block into a new split beside another. |
| `swap_blocks` | Exchange the positions of two blocks. |
| `detach_block` | Remove a block from its layout without closing it. |
| `float_block` | Move a tiled block into a new floating layer. |
| `zoom_block` | Toggle or set whether a block fills its window. |
| `resize_pane` | Move the border between two blocks. |
| `resize_layer` | Set a floating layer's position and size. |
| `raise_layer`, `lower_layer` | Change a floating layer's stacking order. |
| `move_window` | Move a window in the tab order. |
| `focus_block` | Focus a block. |
| `focus_window` | Focus a window. |
| `focus_direction` | Focus the nearest block in a direction. |
| `focus_next_pane`, `focus_previous_pane` | Focus the next or previous pane. |
| `focus_next_window`, `focus_previous_window` | Focus the next or previous window. |
| `set_label` | Set the session's label. |
| `set_window_label` | Set a window's label. |
| `set_block_label` | Set a block's label. |
| `attach`, `detach` | Change which session a script hears events from. |
| `help` | Describe the methods available through the session. |

For the arguments and result of a method, run `rex api describe` with its
full name:

```sh
rex api describe session.new_split
```

### `rex.call(method[, args])`

Calls any server method by its full name, including the ones `rex.session`
doesn't cover.

```lua
local result, err = rex.call("session.list")
```

`rex api list` prints every method.

### `rex.block.call(creator, method[, args])`

Calls a method on a block. `creator` is the full name of the kind of block.
`block_id` is filled in from the current block when it is left out.

```lua
local terminal = "com.superlogical.terminal"
local title = rex.block.call(terminal, "title", {}).title
```

The terminal's methods are:

| Method | Description |
| --- | --- |
| `format` | Return the screen as text, HTML, or VT sequences. |
| `process` | Describe the terminal's child and foreground processes. |
| `pwd` | Return the working directory the terminal last reported. |
| `title` | Return the terminal's title. |
| `size` | Return the terminal's size in cells and pixels. |
| `write` | Write bytes to the terminal as if they were typed. |
| `reset` | Reset the terminal. |
| `resize` | Request a size for the terminal. |
| `set_theme` | Replace the terminal's default colors. |
| `program_status` | Return the status records programs have reported. |
| `list_dir` | List the directories under a path. |

### `rex.layout`

Functions that build the `layout` table taken by `new_window`, `new_split`,
and `new_layer`. They only build tables and call nothing.

| Function | Description |
| --- | --- |
| `rex.layout.block{ flavor, options }` | One block. `flavor` names what to create, such as `com.superlogical.terminal.shell`. |
| `rex.layout.horizontal(ratio, a, b)` | Two layouts split horizontally. `ratio` is the share given to `a`, from 0 to 1. |
| `rex.layout.vertical(ratio, a, b)` | Two layouts split vertically. |

The options for a terminal are:

| Option | Description |
| --- | --- |
| `command` | A list with the program to run and its arguments. Without it, an interactive shell starts. |
| `shell` | The shell to use. `none` starts `command` directly. |
| `cwd` | The working directory. |
| `initial_input` | Text typed into the terminal once it starts. |
| `exit` | `{ on_completion = false }` keeps the terminal open after its program exits. |

## Events

See [Lua Events](https://www.superlogical.com/rex/docs/automate/lua-events.md). These work in scripts run with
`rex do` only.

### `rex.on(event, fn)`

Calls `fn(ctx, ev)` each time `event` happens. `ev` holds the event's fields.
`ctx` has `session_id`, and `block_id` for a block event.

The [events reference](https://www.superlogical.com/rex/docs/reference/events.md) lists the event names.

### `rex.wait(event[, filter][, timeout])`

Blocks until `event` happens, and returns `ev` and `ctx`. Returns `nil` and
`"timeout"` if `timeout` seconds pass first.

`filter` is a table of fields the event must match, or a function called as
`filter(ev, ctx)` that returns `true` for a match.

### `rex.sleep(seconds)`

Blocks for a number of seconds, which may be fractional.

### `rex.stop([code])`

Ends the script immediately. `rex do` exits with `code`, or 0.

## Hosts and Other Servers

### `rex.host{ ... }`

Declares another Rex server you connect to. Configuration file only.

| Field | Description |
| --- | --- |
| `label` | Required. The host's name. |
| `endpoints` | Required. A list of addresses, tried in order. |
| `endpoint` | A single address, in place of `endpoints`. |
| `id` | A stable ID, so the host keeps its identity when renamed. |
| `icon` | An icon name for clients to show. |

### `rex.servers()`

Returns the labels of the other servers available to the running action or
script, as a list.

### `rex.server(label)`

Returns a table with the same `session`, `block`, and `call` functions as
`rex`, whose calls go to that server. Raises an error for an unknown label.

Calls made through it don't fill in a `session_id` or `block_id`.

## Other Functions

Functions for running commands, timers, JSON, and logging. See
[Running Commands](https://www.superlogical.com/rex/docs/automate/lua-scripts.md#running-commands) and
[Timers](https://www.superlogical.com/rex/docs/automate/lua-scripts.md#timers).

### `rex.exec(argv[, opts])`

Runs a command, waits for it to exit, and returns a result table. Returns
`nil` and an error message only when the command never ran, such as when the
program doesn't exist.

```lua
local r, err = rex.exec({ "git", "status", "--short" }, { cwd = dir })
```

`argv` is a list of strings: the program, then each of its arguments. No shell
reads it, so arguments need no quoting. A program without a slash in its name
is looked up in the command's `PATH`.

`opts` is an optional table:

| Option | Description |
| --- | --- |
| `cwd` | The working directory. Defaults to Rex's own. |
| `env` | Environment variables to set, such as `{ GIT_DIR = "/repo/.git" }`. `false` removes one. |
| `clear_env` | `true` starts from an empty environment. `env` still applies. |
| `stdin` | A string written to the command's standard input. |
| `timeout` | Seconds until the command is sent `SIGTERM`, then `SIGKILL` two seconds later. |
| `stdout`, `stderr` | `false` discards the stream. Both are captured by default. |
| `text` | `false` keeps `\r\n` in the output on Windows. |

An option Rex doesn't know is ignored with a warning.

The result has:

| Field | Description |
| --- | --- |
| `code` | The exit status, or `-1` if a signal ended the command. |
| `signal` | The name of that signal, such as `SIGTERM`, or `nil`. |
| `stdout`, `stderr` | What the command printed. `""` when it printed nothing. |
| `timed_out` | `true` if `timeout` stopped the command. |
| `ok` | `true` if `code` is 0 and the command didn't time out. |

A non-zero exit is still a result, not an error. Check `ok`.

While an action in the configuration file waits for a command, the server
keeps handling keys and other actions. Everywhere else, the wait blocks the
script.

### `rex.exec.start(argv[, opts])`

Starts a command and returns a handle without waiting, or `nil` and an error
message. It takes the same arguments as `rex.exec`, and a few more options:

| Option | Description |
| --- | --- |
| `stdin` | `true` keeps standard input open for `h:write`. |
| `stdout`, `stderr` | A function called with each piece of output as it arrives. A piece may end mid-line. |
| `detach` | `true` lets the command outlive the work that started it. |

The handle has:

| Method | Description |
| --- | --- |
| `h:wait([seconds])` | Waits for the command to exit and returns the same result as `rex.exec`. Returns `nil` and `"timeout"` if `seconds` pass first. |
| `h:write(data)` | Writes to standard input. Returns `true`, or `nil` and an error message. |
| `h:close_stdin()` | Closes standard input. |
| `h:kill([signal])` | Sends a signal, `SIGTERM` by default. `signal` is a name, such as `SIGINT`, or a number. |
| `h:running()` | Returns whether the command is still running. |
| `h.pid` | The command's process ID. |

A command lasts as long as the work that started it. When an action, handler,
or timer returns, or a script's top level finishes, Rex stops the commands it
started. A command started with `detach = true` is never stopped this way.

### `rex.after(seconds, fn)`

Calls `fn(ctx)` once, after `seconds`, and returns a timer with the same
methods as [`rex.every`](#rexeveryseconds-fn)'s. `seconds` may be zero or
fractional.

`ctx` is the same table an action's `run` gets, with `ctx.origin` set to
`timer`. API calls default to the script's session and block.

### `rex.every(seconds, fn)`

Calls `fn(ctx)` every `seconds` until the timer is cancelled, and returns a
timer. `seconds` must be more than zero.

If the script is still busy when a tick comes, `fn` runs once when it is free,
and the missed ticks are dropped.

A timer has two methods:

| Method | Description |
| --- | --- |
| `t:cancel()` | Stops the timer. |
| `t:active()` | Returns `true` until the timer is cancelled or has fired for the last time. |

An error in `fn` is reported and the timer keeps running. A script can have at
most 1,024 timers at once. Creating one more stops the script with status 1.

### `rex.json.encode(value[, opts])`

Turns a Lua value into JSON text, or returns `nil` and an error message.
`opts.indent = true` indents the text by two spaces.

```lua
local text = rex.json.encode({ name = "work", panes = { 1, 2 } })
```

Tables convert the same way they do in an API call. A table whose keys are 1
to n becomes an array, and any other table, including an empty one, becomes
an object. A function, or a table that contains itself, can't be encoded.

### `rex.json.decode(text)`

Turns JSON text into a Lua value, or returns `nil` and an error message.
`null` becomes `nil`, and a `null` in an array is dropped.

### `rex.log([level, ]message)`

Writes a log message. `level` is `debug`, `info`, `warn`, or `error`, and
defaults to `info`. In a script the message is printed to the terminal.

## Script Values

Set in scripts run with `rex do` only.

| Value | Description |
| --- | --- |
| `rex.args` | The script's arguments, as a table. Empty when none were passed. |
| `rex.session_id` | The ID of the session the script runs against. |
| `rex.block_id` | The ID of the block the script runs against, or `nil`. |
