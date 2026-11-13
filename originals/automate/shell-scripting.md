---
title: "Shell Scripting"
canonical_url: https://www.superlogical.com/rex/docs/automate/shell-scripting
---

# Shell Scripting

You can also use the [`rex` CLI](https://www.superlogical.com/rex/docs/automate/cli.md) with typical shell scripts
to automate everything in Rex:

```sh
#!/bin/sh
rex new work
rex split -s work -- htop
rex run -s work --label logs -- tail -f app.log
```

For anything beyond a few commands in a row, consider a
[Lua script](https://www.superlogical.com/rex/docs/automate/lua-scripts.md) instead. Lua can do everything on this
page with one connection to the server and without parsing JSON.

## Keeping Track of IDs

Commands that create something print its ID with `--json`. Save the ID and
pass it to later commands, so the script keeps working when a label changes
or focus moves.

```
$ rex split --json -- htop
{
  "anchor_block_id": "block:01a10e00-7268-78c6-8b85-86c56d6a53a9",
  "block_ids": [
    "block:01a10e00-729d-7c38-90f7-d6568611b1c4"
  ],
  "split_ids": [
    "split:01a10e00-72ab-7157-b9e0-0d4c2a8a1a68"
  ],
  "revision": 2
}
```

[`jq`](https://jqlang.org) is the easiest way to pull the ID out:

```sh
block=$(rex split --json -- htop | jq -r '.block_ids[0]')
rex zoom -b "$block"
```

| Command | Creates | ID is at |
| --- | --- | --- |
| `rex new --json` | A session with one window and one terminal | `.session_id` |
| `rex run --json` | A terminal in a new window | `.block_ids[0]`, `.window_id` |
| `rex split --json` | A terminal beside an existing one | `.block_ids[0]` |

A label is a fine alternative when the script sets it. Give the block a label
with `--label` and use that as the target:

```sh
rex split --label logs -- tail -f app.log
rex capture -b logs
```

## Building a Layout

`rex new` creates a session, `rex run` adds a window to it, and `rex split`
splits an existing block.

```sh
#!/bin/sh
# Open a project: an editor with a shell below it, and a second
# window that follows the logs.
rex new api --cwd ~/src/api -- nvim
rex split -s api --split=below --ratio 30 --cwd ~/src/api
rex run -s api --label logs --focus=false -- tail -f ~/src/api/app.log
```

These options are shared by `rex run` and `rex split`:

| Option | Does |
| --- | --- |
| `-- COMMAND` | Runs a command instead of an interactive shell. |
| `--cwd DIR` | Sets the working directory. |
| `--label TEXT` | Labels the new block. |
| `--split DIRECTION` | Places the block `right`, `left`, `above`, or `below` its anchor. |
| `--ratio PCT` | Gives the new block that percentage of the split. |
| `--focus=false` | Leaves focus where it was. |
| `--keep-open` | Keeps the terminal open after its command exits. |

A command runs with the environment of your login shell, so your `PATH`
applies but aliases don't. It isn't parsed by a shell. To use pipes or `&&`,
run a shell explicitly:

```sh
rex run -- sh -c 'make build && make test'
```

## Typing Into a Terminal

`rex send` types text into a terminal, and `rex send-key` presses keys:

```sh
rex send -b logs 'make test'
rex send-key -b logs enter
```

`rex send` doesn't press Enter for you. Follow it with `rex send-key enter`,
or include the newline in the text. It also reads from stdin:

```sh
printf 'make test\n' | rex send -b logs
```

`rex send-key` uses the same key names as
[keyboard shortcuts](https://www.superlogical.com/rex/docs/customize/keyboard-shortcuts.md#writing-keys), so
`rex send-key ctrl+c` interrupts whatever is running.

## Reading a Terminal

`rex capture` prints a terminal's screen and its scrollback:

```
$ rex capture -b logs --trim
hello from logs
```

| Option | Does |
| --- | --- |
| `--trim` | Removes trailing blank lines. |
| `--unwrap` | Joins lines the terminal wrapped. |
| `--format html` | Keeps colors and styling, as HTML. |
| `--format vt` | Keeps the terminal's control sequences. |

A terminal keeps about 64 MiB of scrollback. That is roughly 100,000 lines of
plain text at 80 columns, and fewer in a wider terminal or with styled output.
Once the limit is reached, the oldest lines are dropped. To keep everything a
long command prints, redirect its output to a file.

Full-screen programs, such as editors, pagers, and many TUI apps, draw on a
separate screen that has no scrollback. While one is running, `rex capture`
returns only what that program shows right now. Any history it has, like an
editor's file or a chat app's earlier messages, stays inside the program.

## Running a Command and Waiting

Add `--wait` to `rex run` or `rex split` to wait for the command to finish.
The `rex` command then exits with the command's own status:

```sh
if rex run --wait -- make test; then
  echo "tests passed"
fi
```

`rex wait` does the same for a terminal that is already running, given its
ID or label:

```sh
block=$(rex split --json -- make test | jq -r '.block_ids[0]')
# ... do other things ...
rex wait "$block"
echo "make exited with $?"
```

`rex wait` also accepts a window or a session, and returns when it closes.

Use `--for` to give up after a while. A wait that times out exits with
status 1:

```sh
rex wait --for 10m "$block" || echo "failed or timed out"
```

## Performing Actions

`rex do` performs an action by name, with arguments as `key=value` pairs. It
runs both the app's actions and the
[custom actions](https://www.superlogical.com/rex/docs/customize/actions.md) in your configuration file:

```sh
rex do dev_layout file=app.log
rex do pane.split direction=right
```

Actions such as `pane.split` are performed by the app, so the app must be
running, with Remote Control turned on in its settings.

## Watching Events

`rex events` prints events as they happen and runs until interrupted. With
`-s` it follows one session:

```
$ rex events -s work
14:38:07  block_created         …65951c  session …8f9d5d
14:38:07  session_view_changed  …8f9d5d  revision 11
14:38:07  block_event           …65951c  com.superlogical.terminal.bell {}
```

With `--json` it prints one JSON object per line, ready for `jq`. This prints
the ID of each terminal that rings its bell:

```sh
rex events -s work --json |
  jq -r 'select(.payload.event.payload.name == "bell")
         | .payload.event.payload.block_id'
```

The [events reference](https://www.superlogical.com/rex/docs/reference/events.md#events-on-the-cli) describes the
JSON and lists every event. To act on events rather than print them,
[Lua event handlers](https://www.superlogical.com/rex/docs/automate/lua-events.md) are much less work than a
pipeline.

## Example: Run Tests in a Split

This script runs a command in a split beside the current terminal. If the
command fails, it zooms the split and exits with a failure.

```sh
#!/bin/sh
# tests.sh
cmd="${1:-make test}"

block=$(rex split --keep-open --focus=false --json -- sh -c "$cmd" |
  jq -r '.block_ids[0]')

if ! rex wait --for 10m "$block"; then
  rex zoom -b "$block" --on
  exit 1
fi
```

```sh
./tests.sh 'go test ./...'
```

The [same script in Lua](https://www.superlogical.com/rex/docs/automate/lua-scripts.md#example-run-tests-in-a-split)
is a useful comparison.
