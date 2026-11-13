---
title: "Events"
canonical_url: https://www.superlogical.com/rex/docs/reference/events
---

# Events

Rex emits an event whenever something changes: a window opens, a terminal
changes directory, a program exits, a session is destroyed. Events can be
handled in Lua with [`rex.on` and `rex.wait`](https://www.superlogical.com/rex/docs/automate/lua-events.md), or
streamed from the CLI with `rex events`.

Events come from three places:

| Kind | Describes | Lua name |
| --- | --- | --- |
| [Session events](#session-events) | Changes to one session's windows, blocks, and clients. | The event's type, such as `block_closed`. |
| [Terminal events](#terminal-events) | Things a terminal reports. | `terminal.` and the event, such as `terminal.bell`. |
| [Server events](#server-events) | Changes to the server as a whole. | The event's type, such as `session_created`. |

## Events in Lua

A handler is called with `ctx` and `ev`. The fields listed for each event on
this page are found directly on `ev`:

```lua
rex.on("terminal.child_exited", function(ctx, ev)
  print(ctx.block_id, ev.exit_code)
end)
```

Every `ev` also has these fields:

| Field | Description |
| --- | --- |
| `ev.type` | The event's type. For every terminal event this is `block_event`. |
| `ev.session_id` | The session the event happened in. Absent for most server events. |
| `ev.payload` | The event's own fields again, as a table of their own. |

A terminal event, and any other block event, adds:

| Field | Description |
| --- | --- |
| `ev.block_id` | The block the event came from. |
| `ev.creator_name` | The kind of block, such as `com.superlogical.terminal`. |
| `ev.name` | The event's name without the creator, such as `bell`. |

`ctx.session_id` and `ctx.block_id` hold the same IDs, and are what API calls
in the handler default to.

Register for `block_event` to receive every event from every block, and use
`ev.creator_name` and `ev.name` to tell them apart.

## Session Events

These describe one session. A script hears them for the session it runs
against, or for every session with `--all`.

| Event | When | Fields |
| --- | --- | --- |
| `window_created` | A window is created. | `window_id`, `label` |
| `window_closed` | A window is closed. | `window_id` |
| `window_label_changed` | A window is renamed. | `window_id`, `label` |
| `active_window_changed` | A different window becomes the active one. | `window_id` |
| `block_created` | A block is created. | `block_id` |
| `block_closed` | A block is closed. | `block_id` |
| `session_label_changed` | The session is renamed. | `label` |
| `session_view_changed` | The session's layout changes in any way. | `revision` |
| `client_connected` | A client attaches to the session. | `client_id`, `principal`, `connected_at` |
| `client_disconnected` | A client detaches from the session. | `client_id`, `principal` |
| `client_connection_changed` | An attached client's connection is lost or restored. | `client_id`, `principal`, `connection_state` |
| `creator_changed` | The kinds of block the session can create have changed. | |

`session_view_changed` follows almost every other event in this table, because
most of them change the layout. Handle it to react to any structural change,
and call `rex.session.view` to get the new layout.

## Terminal Events

These come from terminal blocks. In Lua, write them as `terminal.` followed by
the name, or in full as `com.superlogical.terminal.` followed by the name.

| Event | When | Fields |
| --- | --- | --- |
| `terminal.child_exited` | The terminal's program exits. | `exit_code`, and `error` when it is not zero |
| `terminal.pwd_changed` | The program reports a new working directory. | `pwd`, `owner` |
| `terminal.title_changed` | The terminal's title changes. | `title`, `owner` |
| `terminal.bell` | The terminal receives a bell character. | |
| `terminal.process_changed` | The foreground process changes. | `generation`, `foreground`, `ancestors` |
| `terminal.desktop_notification` | The program asks for a desktop notification. | `title`, `body` |
| `terminal.progress_report` | The program reports progress. | `state`, `progress` |
| `terminal.clipboard_written` | The program writes to the clipboard. | `text` |
| `terminal.program_status_changed` | A program reports or updates its status. | `id`, `record`, `reason` |
| `terminal.program_status_removed` | Program status records are removed. | `ids`, `reason` |

A few notes on these:

- `terminal.child_exited` is about the program the terminal started, which is
  usually your shell. It doesn't fire for each command you run inside a shell.
  A terminal started with a `command` fires it when that command exits.
- `pwd` is a URL such as `file://hostname/Users/you/src`, not a plain path. It
  is only reported by shells set up to report it.
- `owner` is a table with the `pid` and `name` of the process that made the
  change.
- `foreground` is a table describing the process in the foreground, with
  `name`, `cwd`, `pid`, and more. It can be `nil`.

## Server Events

These describe the server rather than one session. In Lua, a script hears them
when run with `--all`.

| Event | When | Fields |
| --- | --- | --- |
| `session_created` | A session is created. | `session`, a table with `session_id` and `label` |
| `session_destroyed` | A session is destroyed. | `session_id` |
| `client_joined` | A client connects to the server. | `client` |
| `client_left` | A client disconnects from the server. | `client_id` |
| `client_changed` | A connected client's details change. | `client` |
| `keymap_changed` | The configuration file is reloaded. | `generation`, `hash` |
| `hosts_changed` | The list of hosts changes. | `hash` |
| `tailscale_status_changed` | The server's Tailscale status changes. | |

`client` is a table with the client's `client_id`, `info` (its `kind`, `name`,
`platform`, and `version`), `principal`, and `connected_at`.

## Events on the CLI

`rex events --json` prints one JSON object per line. Each has a `type` and a
`payload` holding the fields listed on this page:

```json
{"type":"session_created","payload":{"session":{"session_id":"session:01a1...","label":"work"}}}
```

A session event arrives wrapped in a `session_event`, which adds the session
it belongs to. A terminal event is wrapped once more, in a `block_event`
(shown here on several lines):

```json
{"type":"session_event","payload":{
  "session_id":"session:01a1...",
  "event":{"type":"block_event","payload":{
    "block_id":"block:01a1...",
    "creator_name":"com.superlogical.terminal",
    "name":"child_exited",
    "payload":{"exit_code":2,"error":"exit status 2"}}}}}
```

Lua removes both layers of wrapping, which is why a handler sees `exit_code`
directly on `ev`.

What `rex events` prints depends on its scope:

| Command | Prints |
| --- | --- |
| `rex events` | Sessions being created, destroyed, and changed. |
| `rex events -s SESSION` | Everything in one session, including terminal events. |
| `rex events --all` | Everything, including clients joining and leaving. |

## Unknown Events

New versions of Rex add events and fields. Rex never checks an event name
against a list, so a handler can be registered for an event that only a newer
server sends. Ignore fields you don't recognize rather than failing on them.
