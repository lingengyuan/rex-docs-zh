---
title: "Server API"
canonical_url: https://www.superlogical.com/rex/docs/automate/server-api
---

# Server API

The server documents its own API. You can list every method, read a method's
arguments and result, and call it, all from the CLI:

```sh
rex api list
rex api describe session.new_split
rex api call server.version
```

Because the documentation comes from the server you are connected to, it
always matches that server's version.

The CLI and Lua APIs all derive dynamically from the server API it is
connected to, so these commands are also important for scripting and
automation at a higher level.

## Discovering Methods

`rex api list` prints every method with a short description:

```
$ rex api list
METHOD              DESCRIPTION
block.close         Close a block within a session. ...
block.event         Deliver an external event to a block within a session.
block.method        Invoke a typed method on a block within a session ...
...
```

A second table lists the [methods that blocks provide](#block-methods), such
as reading a terminal's screen.

Use `-q` to print only the names, which is handy for searching:

```
$ rex api list -q | grep label
client.set_label
session.set_block_label
session.set_label
session.set_window_label
```

## Reading a Method's Documentation

`rex api describe` prints everything the server knows about one method: what
it does, the arguments it takes, what it returns, and an example of each.

```
$ rex api describe session.set_block_label
Update a block's human-readable display label. ...

Method: session.set_block_label

Input schema:
{
  "type": "object",
  "properties": {
    "block_id": { "type": ["string", "null"] },
    "label": { "type": "string" },
    "session_id": { "type": "string" }
  },
  "required": ["session_id"],
  "additionalProperties": false
}

Output schema:
{
  "type": "object",
  "properties": {
    "revision": { "type": "integer", "minimum": 0 }
  },
  "required": ["revision"],
  "additionalProperties": false
}

Request example:
{
  "session_id": "session:<uuid>",
  "block_id": "block:<uuid>",
  "label": "shell"
}

Response example:
{"revision": 42}
```

The schemas are [JSON Schema](https://json-schema.org). To read one:

- `properties` lists each argument and its type.
- `required` lists the arguments that must be present.
- `additionalProperties: false` means a misspelled argument is an error
  rather than being ignored.

The request example is usually the quickest way to see how a call should
look. Some methods also print validation notes, which describe rules the
schema can't express.

## Calling a Method

`rex api call` calls a method and prints its result as JSON:

```
$ rex api call server.version
{
  "rex_version": "0.1.0",
  "platform": "darwin_arm64",
  ...
}
```

Arguments are a single JSON object. Pass it directly, read it from a file
with `@`, or read it from stdin with `-`:

```sh
rex api call -s work session.set_label '{"label": "api"}'
rex api call session.create @layout.json
echo '{"label": "work"}' | rex api call session.create -
```

Most `session.` methods need a `session_id`. Name the session with `-s` and
`rex api call` adds it to the arguments for you:

```sh
rex api call -s work session.view
```

Unlike other `rex` commands, `rex api call` doesn't default to the session
you are in. Inside a Rex terminal, pass `-s "$REX_SESSION"` to use it.

Other IDs are never filled in. A method that acts on a block needs its
`block_id` in the arguments.

The result is indented when printed to a terminal and kept on one line when
piped, so it is ready for [`jq`](https://jqlang.org):

```sh
rex api call -s work session.view | jq '.windows | length'
```

### Errors

A call that fails prints the server's message and exits with a nonzero
status:

```
$ rex api call -s work session.set_block_label '{"lable": "x"}'
Error: ... input: validating: block_id is required (status=400 code=bad_request)
```

The `code` says what kind of failure it was. `bad_request` means the
arguments were wrong, and `method_not_found` means the server has no method
by that name, which can happen when the server is older than the docs you
are reading.

## Calling From Lua

`rex.call` takes a method's full name and its arguments as a table:

```lua
local version = rex.call("server.version")
print(version.rex_version)
```

Every `session.` method that acts on one session also has a helper under
`rex.session`, named after the method:

| API method | Lua |
| --- | --- |
| `session.view` | `rex.session.view{}` |
| `session.set_label` | `rex.session.set_label{ label = "work" }` |
| `session.new_split` | `rex.session.new_split{ ... }` |

The arguments and result are the same as `rex api describe` shows, written as
Lua tables instead of JSON. The helpers fill in `session_id` when it is left
out. `rex.call` doesn't, so pass `rex.session_id` yourself when calling a
`session.` method through it.

A few `session.` methods have no helper because they don't act on an existing
session, such as `session.list` and `session.create`. Call those with
`rex.call`.

A failed call returns `nil` and the server's error message:

```lua
local result, err = rex.session.set_block_label{ lable = "x" }
if err ~= nil then error(err, 0) end
```

The [Lua API reference](https://www.superlogical.com/rex/docs/reference/lua.md#calling-rex) covers these functions in
full.

## Block Methods

Blocks provide methods of their own. `rex api list` prints them in a second
table, named for the kind of block that provides them:

```
Block methods:
CREATOR                    METHOD                             DESCRIPTION
com.superlogical.terminal  com.superlogical.terminal.format   Format the current terminal screen ...
com.superlogical.terminal  com.superlogical.terminal.pwd      Return the working directory ...
com.superlogical.terminal  com.superlogical.terminal.title    Return the current terminal title.
...
```

Describe one the same way as any other method:

```sh
rex api describe com.superlogical.terminal.format
```

To call one, pass the `block_id` to call it on, and put the method's own
arguments under `args`:

```sh
rex api call -s work com.superlogical.terminal.format \
  '{"block_id": "block:01a1...", "args": {"trim": true}}'
```

In Lua, `rex.block.call` builds that wrapper for you and fills in the current
block:

```lua
local terminal = "com.superlogical.terminal"
local screen = rex.block.call(terminal, "format", { trim = true })
print(screen.content)
```

## Machine-Readable Documentation

Both discovery commands take `--json`, which prints the server's own
description of its API:

```sh
rex api list --json       # every method, with schemas and examples
rex api describe session.view --json
```

Each method has a `name`, a `description`, an `input_schema`, an
`output_schema`, and, where the server has them, a `request_example`, a
`response_example`, and `validation_notes`.

This is useful for generating bindings, for checking a script against a
server before running it, and for giving a coding agent the exact shape of
the API it is about to call.
