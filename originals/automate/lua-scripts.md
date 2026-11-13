---
title: "Lua Scripts"
canonical_url: https://www.superlogical.com/rex/docs/automate/lua-scripts
---

# Lua Scripts

`rex do` runs a [Lua](https://www.lua.org) script against a Rex server.

A script is extremely powerful. It can do anything a full-fledged client
can: inspect servers, create sessions, create windows, start terminals,
read a terminal screen, react to events, and more.

This script opens a new window running `htop`:

```lua
-- htop.lua
rex.session.new_window{
  layout = rex.layout.block{
    flavor  = "com.superlogical.terminal.shell",
    options = { command = { "htop" } },
  },
}
```

```sh
rex do htop.lua
```

A script uses the same `rex` API as the [configuration file](https://www.superlogical.com/rex/docs/customize/config.md).
Unlike the configuration file, a script runs once from top to bottom
and exits (unless there are active event handlers or timers running).

## Running a Script

`rex do` takes a script in three ways:

```sh
rex do ./layout.lua                           # a file
rex do -e 'return rex.call("session.list")'   # inline with -e
rex do - < layout.lua                         # stdin
```

The argument is treated as a file when it ends in `.lua` or contains a slash.
Anything else is the name of an [action](https://www.superlogical.com/rex/docs/customize/actions.md) to run.

A script run inside a Rex terminal acts on that terminal's session and block.
Use `-s` and `-b` to [target](https://www.superlogical.com/rex/docs/automate/cli.md#command-targets) a different one:

```sh
rex do -s build ./layout.lua
```

Scripts have Lua's full standard library, including `io` and `os`, and
`require` loads other Lua files. The exception is `io.popen` and `os.execute`.
Use [`rex.exec`](#running-commands) to run commands instead.

Scripts are executed locally where the `rex` CLI is, so security and program
access is up to you.

## Arguments

Arguments are passed as `key=value` pairs after the script and read from the
`rex.args` table:

```lua
-- greet.lua
return "hello " .. (rex.args.name or "world")
```

```
$ rex do greet.lua name=rex
"hello rex"
```

A value's type comes from how it is written. `n=2` is a number, `on=true` is a
boolean, and `name=x` is a string. To pass a string that looks like something
else, or a nested value, pass all the arguments as JSON with `--args`:

```sh
rex do greet.lua --args '{"name": "true"}'
rex do greet.lua --args @args.json
```

## Results and Errors

The value a script returns is printed as JSON. Tables become objects or
arrays. Add `--json` for indented output. A script that returns nothing
prints nothing.

```
$ rex do -e 'return { name = "rex", tabs = { 1, 2 } }'
{"name":"rex","tabs":[1,2]}
```

A script that raises an error prints the message and exits with status 1:

```
$ rex do -e 'error("no tests found", 0)'
Error: no tests found
```

To exit with a status of your choosing, call `rex.stop` with it. The script
ends immediately:

```lua
rex.stop(3)
```

`print` writes to the terminal as usual, and `rex.log` writes a log line.

## Calling Rex

A script starts with a few values describing where it was run:

| Value | Description |
| --- | --- |
| `rex.session_id` | The session the script is running against. |
| `rex.block_id` | The block the script is running against, when there is one. |
| `rex.args` | The script's arguments. |

Rex's API is grouped under `rex.session`. Each call takes one table of
arguments and returns one table:

```lua
rex.session.set_block_label{
  block_id = rex.block_id,
  label    = "tests",
}
```

Calls fill in the script's session, so most calls don't need a `session_id`.
A call that acts on one block, such as `set_block_label`, still needs its
`block_id`.

A failed call doesn't stop the script. It returns `nil` and an error message,
so check the second value when the result matters:

```lua
local w, err = rex.session.new_window{ layout = layout }
if err ~= nil then error(err, 0) end
```

Three more ways to call Rex:

- `rex.call(method, args)` calls any server method by name, including those
  outside `rex.session`, such as `rex.call("session.list")`.
- `rex.block.call(creator, method, args)` calls a method on a block, such as
  reading a terminal's screen.
- `rex.invoke(name, args)` runs an action, either one the script defines or one
  from your configuration file. `rex.client.queue(name, args)` asks the app to
  perform one of its own.

The [Lua API reference](https://www.superlogical.com/rex/docs/reference/lua.md) has the full list.

### Layouts

Calls that create blocks take a `layout`. Build one with `rex.layout`:

```lua
local shell = "com.superlogical.terminal.shell"

rex.session.new_window{
  layout = rex.layout.horizontal(0.5,
    rex.layout.block{ flavor = shell },
    rex.layout.block{
      flavor  = shell,
      options = { command = { "htop" } },
    }),
}
```

`rex.layout.block` is one block. `rex.layout.horizontal` and
`rex.layout.vertical` split the space between two layouts, with the first
argument giving the first one's share. They can be nested.

## Sleeping and Waiting

A script often needs to start something and then act on how it ended.

`rex.sleep(seconds)` pauses the script:

```lua
rex.sleep(0.5)
```

`rex.wait(event, filter, timeout)` pauses until an event arrives:

```lua
local ev = rex.wait(
  "terminal.child_exited", { block_id = id }, 600)
```

- `event` is the name of the event to wait for.
- `filter` is optional. A table matches an event whose fields equal the
  table's. A function is called with the event and matches when it returns
  `true`.
- `timeout` is optional, in seconds. Without it, `rex.wait` waits forever.

`rex.wait` returns the event as a table. If the timeout passes first, it
returns `nil` and `"timeout"`.

The [events reference](https://www.superlogical.com/rex/docs/reference/events.md) lists the events and their fields.

## Timers

`rex.every` calls a function at a fixed interval, and `rex.after` calls one
once after a delay:

```lua
rex.every(5, function(ctx)
  -- every five seconds
end)

rex.after(0.5, function(ctx)
  -- once, half a second from now
end)
```

Unlike `rex.sleep`, a timer doesn't pause the script. The script carries on,
and the function is called later.

Both functions return a timer. Call `t:cancel()` to stop it. A timer keeps
running even if the script drops it, so keep it around if it may need to be
stopped.

Timers can be created anywhere, including inside an event handler or another
timer. The function's `ctx` and API calls always default to the script's own
session and block, even when the timer was created in a handler.

Timers never run at the same time as other Lua in the script. A timer that
comes due while a handler is running waits for it to return. If the script is
still busy when the next tick of `rex.every` comes, the function runs once
when it is free rather than once for each tick it missed.

An error in a timer is printed and the timer keeps running, the same as
[an error in a handler](https://www.superlogical.com/rex/docs/automate/lua-events.md#handler-failures).

A script can have at most 1,024 timers at once. A cancelled timer, or a
`rex.after` timer that has already run, doesn't count. Going past the limit
stops the script with status 1, even inside `pcall`, because it almost always
means a handler creates a timer for every event and never cancels it.

## Running Commands

`rex.exec` runs a command and returns what it printed and how it exited:

```lua
local r, err = rex.exec{ "git", "rev-parse", "--abbrev-ref", "HEAD" }
if r == nil then error(err, 0) end

if r.ok then
  rex.session.set_block_label{
    block_id = rex.block_id,
    label    = r.stdout:gsub("\n$", ""),
  }
end
```

The command is a list: the program, then each of its arguments. No shell
reads it, so a path with spaces or a value from `rex.args` needs no quoting.
To use a shell, ask for one: `{ "sh", "-c", line }`.

A command that exits with a non-zero status still returns a result. Check
`r.ok`, or `r.code` for the exact status, and `r.stderr` for what it printed
to standard error. `rex.exec` only returns `nil` and an error message when the
command couldn't run at all, such as when the program isn't installed.

Options go in a second table:

```lua
local r = rex.exec({ "make", "test" }, {
  cwd     = "/src/app",
  env     = { CI = "1" },
  timeout = 300,
})
```

The [Lua API reference](https://www.superlogical.com/rex/docs/reference/lua.md#rexexecargv-opts) lists every option
and field.

### Streaming Output

`rex.exec.start` starts a command without waiting for it and returns a
handle. Pass a function as `stdout` or `stderr` to receive output as it
arrives:

```lua
local h = assert(rex.exec.start({ "make", "build" }, {
  stdout = function(data) io.write(data) end,
}))

local r = h:wait()
```

A command lasts as long as the part of the script that started it. When the
script's top level finishes, or a handler or timer returns, Rex stops the
commands it started. Pass `detach = true` for a command that should keep
running.

To watch a command run, start it in a terminal block instead, as in
[the example below](#example-run-tests-in-a-split).

## Example: Run Tests in a Split

This script runs a command in a new split beside the current terminal. If the
command fails, it zooms the split so the failure is front and center.

```lua
-- tests.lua
local cmd = rex.args.cmd or "make test"

local split, err = rex.session.new_split{
  direction = "horizontal",
  side      = "after",
  focus     = false,
  layout    = rex.layout.block{
    flavor  = "com.superlogical.terminal.shell",
    options = {
      command = { "sh", "-c", cmd },
      exit    = { on_completion = false },  -- keep the output
    },
  },
}
if err ~= nil then error(err, 0) end
local block_id = split.block_ids[1]

-- Wait up to ten minutes for the command to exit
local ev = rex.wait(
  "terminal.child_exited", { block_id = block_id }, 600)
if ev == nil then error("timed out waiting for: " .. cmd, 0) end

if ev.exit_code ~= 0 then
  rex.session.zoom_block{ block_id = block_id, zoom = true }
end

return { block_id = block_id, exit_code = ev.exit_code }
```

```
$ rex do tests.lua cmd="go test ./..."
{"block_id":"block:01a10deb-c752-789f-9add-5dfd3a5b3214","exit_code":1}
```

## Example: Export the Session

This script keeps a copy of the session's layout in a JSON file, written
every five seconds, for another program to read.

```lua
-- export.lua
local path = rex.args.path or "session.json"

local function export()
  local view, err = rex.session.view{}
  if err ~= nil then error(err, 0) end

  local f = assert(io.open(path, "w"))
  f:write(rex.json.encode(view, { indent = true }))
  f:close()
end

export()
rex.every(5, export)
```

```
$ rex do export.lua path=/tmp/work.json
running: 1 timer; Ctrl-C to stop
```

`rex.json.encode` converts a table the same way an API call does, so the file
matches what the server returned. `rex.json.decode` reads it back.

If the server is briefly unreachable, `export` raises an error, which is
printed, and the timer tries again five seconds later.
