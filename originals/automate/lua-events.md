---
title: "Lua Events"
canonical_url: https://www.superlogical.com/rex/docs/automate/lua-events
---

# Lua Events

A [Lua script](https://www.superlogical.com/rex/docs/automate/lua-scripts.md) can keep running and react to what
happens in Rex: a terminal changes directory, a program exits, a window
closes, a session is created. A script asks for an event with `rex.on`.

```lua
-- label.lua: label each terminal with the directory it is in
rex.on("terminal.pwd_changed", function(ctx, ev)
  local dir = ev.pwd:match("([^/]+)/?$")
  rex.session.set_block_label{
    block_id = ctx.block_id,
    label    = dir,
  }
end)
```

```
$ rex do label.lua
listening: 1 handler, session work; Ctrl-C to stop
```

Change directory in any terminal in the session and its label will update.

## Handlers

`rex.on` takes the name of an event and a function to call each time that
event happens:

```lua
rex.on(event, function(ctx, ev)
  -- ...
end)
```

A script that calls `rex.on` doesn't exit when it reaches its last line.
`rex do` keeps it running and calls its handlers as events arrive, one at a
time.

Handlers are registered while the script first runs. Calling `rex.on` later,
from inside a handler, is an error.

`ev` holds the event's fields, and `ctx` says where it happened:

| Field | Description |
| --- | --- |
| `ctx.session_id` | The session the event happened in. |
| `ctx.block_id` | The block the event came from, for a block event. |

API calls inside a handler default to the event's session rather than the one
the script was started in, so one handler works across every session it hears.

## Event Names

There are three kinds of event name:

| Name | Matches |
| --- | --- |
| `block_closed`, `window_created`, ... | A session or server event, by its type. |
| `terminal.pwd_changed`, `terminal.bell`, ... | One kind of event from a block. |
| `block_event` | Every event from every block. |

A block event is named for the kind of block and the event, joined by a dot.
`terminal.bell` is short for `com.superlogical.terminal.bell`. Either spelling
works.

These are common events:

| Event | When | Fields on `ev` |
| --- | --- | --- |
| `terminal.pwd_changed` | A terminal changes directory. | `pwd`, a `file://` URL |
| `terminal.title_changed` | A terminal's title changes. | `title` |
| `terminal.bell` | A terminal rings its bell. | |
| `terminal.child_exited` | A terminal's program exits. | `exit_code` |
| `block_created`, `block_closed` | A block is created or closed. | `block_id` |
| `window_created`, `window_closed` | A window is created or closed. | `window_id` |
| `session_created`, `session_destroyed` | A session is created or destroyed. | |

The [events reference](https://www.superlogical.com/rex/docs/reference/events.md) has the full list.

Rex doesn't check an event name against a list, so a misspelled name is not an
error. The handler is registered and never called.

## Event Scope

By default, a script reacts to events of one session: the one it was run in,
or the one named with `-s`.

```sh
rex do label.lua            # the current session
rex do -s build label.lua   # the session labeled "build"
```

Pass `--all` to hear every session, including ones created after the script
starts:

```sh
rex do label.lua --all
```

## Stopping

A script with handlers runs until one of these happens:

- A handler calls `rex.stop(code)`. `rex do` exits with that status, or 0
  when it is left out.
- The time given with `--for` runs out, such as `--for 10m`.
- The session it hears is destroyed. A script run with `--all` never stops
  this way.
- You press <kbd>Ctrl</kbd>+<kbd>C</kbd>.

```lua
-- Exit with the status of the first program to fail
rex.on("terminal.child_exited", function(ctx, ev)
  if ev.exit_code ~= 0 then rex.stop(ev.exit_code) end
end)
```

## Handler Failures

An error in a handler or a [timer](https://www.superlogical.com/rex/docs/automate/lua-scripts.md#timers) is printed
and the script keeps running, so one bad event doesn't end a long-lived
script:

```
Error: watch.lua:7: attempt to index a nil value
```

Pass `--fail-fast` to exit with status 1 at the first failure instead.

Remember that a failed API call returns `nil` and a message rather than
raising an error. Check the second return value where it matters.

## Handlers or `rex.wait`

[`rex.wait`](https://www.superlogical.com/rex/docs/automate/lua-scripts.md#sleeping-and-waiting) and `rex.on` both
receive events, and suit different scripts.

- Use `rex.wait` when the script does one thing after another: start a
  command, wait for it to exit, then act on the result.
- Use `rex.on` when the script should respond every time something happens,
  for as long as it runs.

`rex.wait` and `rex.sleep` also work inside a handler. No other event is
handled until they return.

## Timers in Handlers

A handler that needs to do something later can start a
[timer](https://www.superlogical.com/rex/docs/automate/lua-scripts.md#timers) and return, rather than sleep and hold
up every other event.

This is useful for events that arrive in bursts. `session_view_changed`
follows almost every change to the layout, so this calls an `export` function
once, half a second after the last change of a burst:

```lua
local pending
rex.on("session_view_changed", function(ctx, ev)
  if pending then pending:cancel() end
  pending = rex.after(0.5, export)
end)
```

A timer's API calls default to the session the script was started in, not
the event's. To act on the event's session, pass `ctx.session_id` along:

```lua
rex.on("session_view_changed", function(ctx, ev)
  if pending then pending:cancel() end
  pending = rex.after(0.5, function()
    export(ctx.session_id)
  end)
end)
```

## Invalid in Configuration Files

`rex.on` only works in a script run with `rex do`. The
[configuration file](https://www.superlogical.com/rex/docs/customize/config.md) is never sent events, so a handler
registered there is reported as a warning and never called.

To have a handler running all the time, start the script when you start your
session, for example from a terminal you keep open for it.

## Example: Notify on Bell

Many programs ring the terminal bell when they finish or need attention. This
script turns a bell in any terminal, in any session, into a macOS
notification that names the session:

```lua
-- notify.lua
local function notify(title, text)
  rex.exec{
    "osascript", "-e",
    string.format("display notification %q with title %q", text, title),
  }
end

rex.on("terminal.bell", function(ctx, ev)
  local view = rex.session.view{}
  notify("Rex", "Bell in " .. view.label)
end)
```

```sh
rex do notify.lua --all
```

`rex.session.view` is called without a `session_id`, so it describes the
session the bell rang in. That is how one handler can name whichever session
needs you.
