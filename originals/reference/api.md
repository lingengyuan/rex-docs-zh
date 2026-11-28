---
title: "Server API Methods"
canonical_url: https://www.superlogical.com/rex/docs/reference/api
---

# Server API Methods

This page lists every method in the control API. See [Server API](https://www.superlogical.com/rex/docs/automate/server-api.md) for how to call them. Anything tagged [Snapshot](https://www.superlogical.com/rex/docs/linux/installation.md#channels) is on the snapshot channel and not yet in preview.

<div class="reference-page methods" hidden></div>

## block

### `block.close`

Close a block and end the program running in it.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session that holds the block. |
| `block_id` |  | The block to close. It may be a detached block. Send this or window_id, not both. |
| `window_id` |  | The window whose focused block to close. It doesn't have to be the active window. Send this or block_id, not both. |
| `keep_last` |  | If true, fail rather than close the only block left in a window, counting floating layers. Ignored for detached blocks. |
| `undoable` |  | If true, hold the block for about a minute so that the calling client can bring it back with client.undo_close. Send it when a person closed the block. It only has an effect for a client attached to the session, and for a block that is in a window and has started. |

Send exactly one of `block_id` and `window_id`. If you send both, or neither, the call fails with `bad_request`.

The server sends `block_closed` when the block closes. If it was the last block in its window, the window closes too and the server sends `window_closed`.

If `undoable` is true and the caller is a client attached to the session, the server instead keeps the block running, out of every window, for about a minute, so that `client.undo_close` can put it back. The view changes at once, and `block_closed` arrives only once the block is freed. A block that is in no window, or is still starting, closes at once all the same.

If `keep_last` is true and the block is the only one left in its window, counting blocks in floating layers, the call fails with `bad_request` and closes nothing.

If the block's creator is still placing it, the call returns at once and the block closes when placement finishes.

On one connection, `block.close` waits for earlier requests that can change focus, such as `session.new_split` and `session.focus_block`, to finish. A close by `window_id` therefore closes the block those requests left focused.

If the session doesn't exist, the call fails with `session_not_found`. If `block_id` or `window_id` names something that isn't in the session, or the window has no focused block, it fails with `not_found`.

### `block.event`

Send an input event, such as a key press or a paste, to a block.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session that holds the block. |
| `block_id` | Yes | The block to send the event to. |
| `event` | Yes | The event to send: its type, such as paste, and its payload. |

A client may send only `key`, `paste`, `mouse`, `wheel`, and `focus` events. Every other event type is sent only by the server. A `paste` event's `payload` is `{"text": "..."}`, and a `focus` event's `payload` is `{"action": "in"}` or `{"action": "out"}`.

The event goes straight to the block, so Lua key bindings never see it. To give key bindings the first chance at a key, use `client.key` instead.

On one connection, `block.event` calls run one at a time, in order with `client.key`, so the block receives events in the order you send them.

The call returns once the block has received the event, which may be before the block has finished acting on it.

The call fails with `bad_request` if `event` is missing or its `payload` has the wrong shape for its type. It also fails with `bad_request` if `event.type` is empty, names an event only the server sends, or names an event this server doesn't know.

If the session doesn't exist, the call fails with `session_not_found`, and if `block_id` names a block that isn't in the session, it fails with `not_found`.

### `block.method`

Call a method that a block provides and return its result.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session that holds the block. |
| `block_id` | Yes | The block to call the method on. |
| `method` | Yes | The block method's short name, such as write or format. |
| `args` |  | The block method's own arguments. Leaving it out is the same as an empty object. |

Send the block method's short name, such as `write`, in `method`. `help.all` lists the methods each creator's blocks provide under `block_types`, with each method's `args_schema` and `output_schema`.

Each block method can also be called by its full name, such as `com.superlogical.terminal.write`, with the same `session_id`, `block_id`, and `args`. The full name names the block's creator, so the call works only on a block that creator made. On any other block, it fails with `conflict`.

The result is the block method's own result, as its `output_schema` describes it. `block.method` has no result schema of its own.

`block.method` doesn't wait for earlier requests on the same connection, and it can run at the same time as `client.key`. If a call depends on an earlier request, wait for that request's reply first. To call a block method in order with `client.key`, such as from a key binding, use `client.action`.

If `block_id` is missing, the call fails with `bad_request`. If the session doesn't exist, it fails with `session_not_found`. If `block_id` names a block that isn't in the session, it fails with `not_found`, and if the block has no method named `method`, it fails with `method_not_found`. If `args` is missing a required field or has a value of the wrong type, it fails with `bad_request`.

## block_creator

### `block_creator.list`

List the creators the server can make blocks with, and their flavors.

Creators are sorted by `name`.

To create a block, pass a flavor's `flavor` to `session.new_block` or in the `block` of a layout, with `options` that match its `options_schema`.

`api.methods` lists the methods that every block from the creator provides. Call one as `<creator>.<method>`, such as `com.superlogical.terminal.title`, with `session_id`, `block_id`, and its arguments under `args`.

A method's `actions` are things a person can do with a block, such as choosing an item in Rex.app's command palette or pressing a key. Performing one calls the method with the action's `args`, which are fixed values, not a schema like the `args` that `client.keymap` lists for an action.

## client

### `client.action`

Perform an action from the configuration file or a block, as this client.

| Field | Required | Description |
| --- | --- | --- |
| `action` | Yes | The full name of the action, such as dev_layout or com.superlogical.terminal.reset. client.keymap lists them. |
| `args` |  | The action's arguments, as a JSON object. Leave it out if there are none, and always for an action a creator declares. |
| `origin` |  | What caused the request: key, palette, or api (the default). The action reads it as ctx.origin. Other values count as api, but script makes the call fail with bad_request. |
| `session_id` |  | The session the action applies to. Required for a block action. A configuration file action may leave it out, and then has no default session. |
| `block_id` |  | The block the action applies to. Defaults to the session's focused block, unless server is set. Requires session_id. |
| `servers` |  | Other servers this client is connected to, which a configuration file action can call with rex.server(name). Don't list the server you're sending this to. |
| `server` |  | The name, from servers, of the server that holds session_id and block_id. Leave it out when they're on the server you're sending this to. |

`action` decides what runs. A name without a dot, such as `dev_layout`, is an action that the configuration file defines with `rex.action`. A name with a dot, such as `com.superlogical.terminal.reset`, is an action or method of a block, named after its creator. `client.keymap` lists every name in `actions`.

A block action, such as `com.superlogical.terminal.reset`, has fixed arguments, so a request for one with `args` fails with `bad_request`. A block method, such as `com.superlogical.terminal.write`, takes its arguments from `args`.

If `args` isn't an object, the call fails with `bad_request`. `null` counts as leaving it out.

The client's own actions, such as `pane.split`, run in the client and can't be sent here. A request for one, or for any name the server doesn't know, fails with `not_found`.

On each connection, `client.key`, `client.action`, `block.event`, and the methods that change focus or the layout run one at a time, in the order they arrive. For an action bound to a key, use this method rather than calling the block method by name, such as `com.superlogical.terminal.write`, so the action takes effect after the keys typed before it.

When `session_id` is set, the connection must be attached to that session, with `session.attach`, `session.bootstrap`, or `session.attach_all`, or the call fails with `conflict`. If `session_id` names no session, the call fails with `session_not_found`. Neither check applies when `server` is set.

Send `session_id` with any block action or method, and whenever you send `block_id`, or the call fails with `bad_request`. A block action or method runs on `block_id`, or on the session's focused block if you leave that out. If the session has no focused block, the call fails with `conflict`.

If the block isn't the kind the action or method belongs to, the call fails with `conflict`. If `block_id` names a block that isn't in the session, it fails with `not_found`.

An action from the configuration file may leave out `session_id`. It then has no `ctx.session_id`, and its `rex.session` calls have no default session. With `session_id`, it sees `block_id`, or the focused block, as `ctx.block_id`.

If `origin` is `script`, the call fails with `bad_request`, because only `rex.invoke` may report that origin.

An action from the configuration file may run for 30 seconds, including time spent waiting on other servers. If it runs longer, the call fails with `timeout`. If the file is reloaded while it runs, the call fails with `conflict`.

If an action from the configuration file raises an error, the call fails with a message that starts with where it happened, such as `init.lua:4: attempt to index a nil value`. However the action fails, part of it may already have run.

Each entry in `servers` needs a unique, non-empty `name` and a non-empty `id`, and `server` must name one of them. Otherwise the call fails with `bad_request`. The server doesn't interpret either value.

Set `server` when the session belongs to one of `servers`. The IDs then go to the action unchecked, and the focused block isn't filled in, so send `block_id` yourself. The action's `rex.session`, `rex.block.call`, and `rex.call` calls go to that server.

When `server` is set, any name with a dot fails with `bad_request`, because a block action must run on the server that holds the block. Send it to that server instead.

When the action calls another server, this connection receives a `client_call_requested` event. Make the call there and report the outcome with `client.reply`. If no reply comes within 10 seconds, or the reply is an error, the action's call fails and the action keeps running.

### `client.inspect`

Get one connected client's details, including the actions it offers.

| Field | Required | Description |
| --- | --- | --- |
| `client_id` | Yes | The client to describe. It can be any client, not only the one calling. |

If `client_id` is missing or isn't a client ID, the call fails with `bad_request`. If it names no connected client, including one that has left, the call fails with `not_found`.

To ask the client to perform one of the actions in `actions`, call `client.perform`.

### `client.key`

Send a key to a block, giving Lua key bindings the first chance at it.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session the key is typed in. |
| `key` | Yes | The key event, as the keyboard reported it. |
| `block_id` |  | The block to send the key to. Defaults to the session's focused block. |
| `prefix` |  | The keys pressed before key when key ends a key sequence, in order. For ctrl+b then x, send x as key and ctrl+b here. |

The connection must be attached to `session_id`, with `session.attach`, `session.bootstrap`, or `session.attach_all`, or the call fails with `conflict`. If `session_id` names no session, the call fails with `session_not_found`.

Without `block_id`, the key goes to the session's focused block. The server reads it once, before any Lua function runs, so a function that moves focus doesn't change where the key goes. Either way, Lua functions see the block the key goes to as `ctx.block_id`.

On each connection, `client.key`, `client.action`, `block.event`, and the methods that change focus or the layout run one at a time, in the order they arrive. That keeps keys in the order you send them.

The key goes first to the Lua functions bound to it in this client's scripts, then to those in the configuration file. If none of them takes the key, it goes to the block.

Only a key bound to a Lua function reaches Lua, and only when it's pressed or repeating. Every other key goes straight to the block. `client.keymap` reports the bound keys as bindings for `client.key.forward`.

If no Lua function takes the key and the session has no focused block, the key goes nowhere. The call still succeeds, with `handled` set to false.

To send a key sequence, wait until it's complete. Then send its last key as `key` and the keys before it in `prefix`, such as `["ctrl+b"]`. The server doesn't remember keys between requests.

A key with a `prefix` reaches only the functions bound to that exact sequence. A key without one reaches only the functions bound to that key alone.

If no function takes a key sequence, only `key` goes on to the block. The keys in `prefix` never do.

A Lua function bound to a key may run for 5 seconds. If it raises an error or runs longer, the call fails and the key doesn't reach the block.

If an element of `prefix` isn't a key the server can read, the call fails with `bad_request`, and the message names the element.

If no Lua function takes the key and `block_id` names a block that isn't in the session, the call fails with `not_found`.

### `client.keymap`

Get what each key does for this client. The result combines the client's own bindings with the configuration file and the client's Lua scripts.

| Field | Required | Description |
| --- | --- | --- |
| `actions` |  | The actions the client performs itself. Leave it out to skip the checks for unknown actions and wrong arguments. The server keeps the list for client.inspect and client.perform. |
| `server_actions` |  | Which of the server's actions the reply lists: all (the default), configured (only the configuration file's), or none. An unknown value means all. |
| `defaults` |  | The client's built-in layers, lowest first. They sit beneath the configuration file. Problems found only in them aren't reported, because the user can't edit them. |
| `overrides` |  | Layers of shortcuts a person recorded in the client, lowest first. They sit above the configuration file and this client's scripts. Problems in them come back as warnings. |

Bindings stack in layers, from bottom to top: your `defaults`, then the account's configuration file, then the scripts this client loaded with `client.set_script`, then your `overrides`.

A layer's `name` becomes the `source` of its bindings and of warnings about it. If a name is empty, contains a colon, or is used by another layer in either list, the call fails with `bad_request`.

The keymap is always the calling client's, so a request that includes `client_id` fails with `bad_request`. So does a top-level `bindings` list, which older servers accepted. Send those bindings as a layer in `defaults` instead.

A key sequence such as ctrl+b followed by c is `["ctrl+b", "c"]` in `keys`. The configuration file writes it as `ctrl+b>c`, but the result always lists the keys separately. The server doesn't split an element such as `ctrl+b>c`. It treats it as a key it can't read.

Keys the server can read come back in their standard spelling. `cmd+d` and `cmd+[KeyD]` are still different keys: the first follows the keyboard layout and the second names a physical key.

A key spelling the server can't read is kept as written, in either list, so a newer client keeps its keys. Only a removal with the same spelling can take it off. A sequence with any such key is kept the same way.

A sequence sits on the stack of its first key, in order among that key's other bindings. If the top binding a client can perform is a sequence, the client waits for the next key. The server keeps no state between keys, so waiting is the client's job.

A key bound to a Lua function, in the configuration file or this client's scripts, comes back as a binding for `client.key.forward`. To perform it, send the key to `client.key`. Treat it as always available: the bindings below it on that key never run, even when no function takes the key.

For a sequence bound to a function, send its last key to `client.key` with the earlier keys in `prefix`. The binding ends the stack only for that exact sequence, so other sequences that start with the same key still work.

A key can't both run a binding of its own and start a sequence, so the higher of the two wins. The server keeps both and adds one warning per key, with the `source`, `action`, and `key` of the binding that can't run. It warns even about a binding in `defaults`, unless the one above it is in `defaults` too.

A removal matches keys in full. Removing `["ctrl+b"]` leaves every sequence that starts with ctrl+b, and removing `["ctrl+b", "c"]` leaves ctrl+b.

A removal that removes nothing gets a warning, unless it's in `defaults`, names a key the server can't read, or blocks a key in a mode.

A binding or removal with a `mode` belongs to that mode, a set of bindings the client uses only while the mode is active. If a mode name contains anything but lowercase letters, digits, `_`, and `-`, or is `root`, the call fails with `bad_request`.

Bindings in a mode stack and are checked like any others. A key in a mode never hides the same key outside it, and a removal affects only its own mode. The configuration file writes a key in a mode as `resize/left`.

`modes` lists a mode if any layer binds a key in it, blocks a key in it, or declares it with `rex.mode`.

A removal in a mode that names no `action` always blocks its key, so the key is listed in the mode's `blocked`, whether or not anything was removed. A removal that names an action never blocks.

A removal with a `mode` and no `keys` removes the whole mode: its bindings, its blocked keys, and its declarations in the layers beneath. If it also names an `action`, the call fails with `bad_request`.

Above a removed mode, a layer that binds, blocks, or declares a key in the mode brings the mode back, with only what that layer and the ones above it say. Otherwise the mode isn't in `modes`.

The client decides which mode is active, with its own `client.mode.enter`, `client.mode.exit`, and `client.mode.exit_all` actions. The server keeps no mode state.

The server warns about a `client.mode.enter` binding whose `name` argument isn't a mode in the keymap, and about a declared mode with nothing bound in it.

An empty request returns the bindings of the configuration file and this client's scripts, without checking for unknown actions or wrong arguments.

When `actions` isn't empty, the server adds its own actions before checking: those the configuration file defines with `rex.action`, every block method, and every block action. A binding to one of these is never reported as unknown.

A binding with wrong arguments is kept, with a warning. A binding to a block method must pass arguments that match the method's input schema, and passing none counts as `{}`. A binding to a block action, or to a method with no input schema, must pass no arguments.

A binding to an action from the configuration file must match the `args` schema the action declares, if it declares one. The client's own actions aren't checked, because the client checks their arguments itself.

`actions` in the result lists the configuration file's actions in the order it defines them, then each creator's methods and block actions, sorted by creator and then by method name. It doesn't repeat the actions you sent.

A block method in `actions` has no `title`, and its `args` is its input schema. Bind it, but don't show it in a menu. A block action has a `title` and no `args`.

`server_actions` changes only what `actions` lists in the result, not which actions bindings are checked against.

To show a diagnostic next to the binding it's about, match its `action`, `key`, and `mode` to the binding's.

A client can keep using a stored result while its request is unchanged and `config.instance_id` and `config.hash` both match. Call this method again after every `client.set_script` call, and after every `keymap_changed` event whose `hash` differs from the stored one.

### `client.list`

List the clients connected to the server, in the order they connected.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` |  | List only the clients attached to this session with session.attach or session.bootstrap. |
| `kinds` |  | List only the clients of these kinds, such as app. A client that didn't report a kind matches none. |

With no arguments, the result lists every connected client, including short-lived ones such as the `rex` CLI.

`session_id` counts only clients attached to that session with `session.attach` or `session.bootstrap`. A connection that only called `session.attach_all` doesn't count. Any client may use this filter, attached or not.

In `kinds`, a kind this server doesn't know counts as `other`. A client that didn't report a kind matches no filter, not even `other`.

If a client's connection drops without closing, the client stays in the list for up to 60 seconds, with `connection_state` set to `lost`, so it can reconnect. A client that wasn't attached to anything and had no scripts leaves at once.

To keep a copy of this list up to date, call `session.attach_all` with `event_scope` set to `all`. The connection then receives `client_joined`, `client_left`, and `client_changed` events.

### `client.perform`

Ask another client to perform one of its actions and wait for its answer.

| Field | Required | Description |
| --- | --- | --- |
| `client_id` | Yes | The client to ask. To find one by its label, call target.resolve with kinds set to client. |
| `action` | Yes | The name of an action the client declared, such as pane.split. client.inspect lists them. At most 256 bytes. |
| `args` |  | The action's arguments, as a JSON object. Leave it out if there are none. |
| `origin` |  | What caused the request, such as key, palette, api, or cli. The client receives it unchanged. Empty means api. |
| `session_id` |  | The session the action applies to, if any. The client receives it without the server checking it. |
| `block_id` |  | The block to act on instead of the client's focused block, if any. The client receives it without the server checking it. |
| `timeout_ms` |  | How long to wait for the answer, in milliseconds, once the client is sent the request. Defaults to 10000. Values over 30000 count as 30000. |

The server sends the named client a `client_perform_requested` event and waits for it to answer with `client.reply`.

The server tells the named client which client asked, based on the connection the request arrived on, so a client can't claim to be another.

The connection doesn't need to be attached to `session_id`, because the server only passes it on to the client.

Requests to one client wait in line, and the client answers them one at a time in the order they arrived. `timeout_ms` counts from when a request reaches the front of the line.

A request without `client_id` or `action`, with an `action` longer than 256 bytes, with a negative `timeout_ms`, or with `args` that aren't an object or don't match the action's schema fails with `bad_request`. If `client_id` names no connected client, the call fails with `not_found`.

If the client has listed its actions and `action` isn't one of them, the call fails with `not_supported`. A client that listed none is asked anyway, and it may answer `not_supported` itself.

A client that declines answers `refused`, and the call fails with that code and a message that says why.

If the client is reconnecting, already has 16 requests waiting for it, or disconnects while the request waits, the call fails with `client_unavailable`.

If the client doesn't answer in time, the call fails with `timeout`. The client isn't told, so it may still perform the action later.

When a request ends, the server sends a `client_performed` event with the outcome to connections that called `session.attach_all` with `event_scope` set to `all`. A request that names no connected client sends no event.

### `client.reply`

Answer a client_call_requested, client_perform_requested, or client_prompt_requested event.

| Field | Required | Description |
| --- | --- | --- |
| `call_id` | Yes | The call_id of the event you're answering. |
| `result` |  | The call's result, what the action returned, or the prompt's answer. For a call or action with no output, use null. For a prompt, send a prompt result: text, ids, or cancelled. Set this or error, not both. |
| `error` |  | Why the call failed, the action wasn't performed, or the prompt couldn't be shown. Set this or result, not both. |

A `client_call_requested` event asks this client to make one call on another server, for a `client.action` request that is still running. Reply to every one, even when the call fails. Send the event's `call_id`, on the connection that received the event.

A `client_perform_requested` event asks this client to perform one of its own actions for another client's `client.perform` request. Reply the same way. `result` is what the action returned, or `null`.

A `client_prompt_requested` event asks this client to put a question to the person using it, for an action that called `rex.ui`. Reply once the person answers, with `result` set to `{"text": "..."}` for typed text, `{"ids": ["..."]}` for chosen items, or `{"cancelled": true}` if they closed the prompt. A result the prompt doesn't accept, such as an ID it didn't offer, fails with `bad_request` and leaves the prompt waiting. If you can't show the prompt, set `error.code` to `not_supported`.

The server sends a prompt to every connected app that can show it, so the same prompt may be open on several devices. The first answer ends it on all of them, and so does a cancel. Every other app then receives a `client_prompt_ended` event with its own `call_id`. Close the prompt whatever the event's `reason` is. A reply after that fails with `not_found`.

A reply that sets both `result` and `error`, or neither, fails with `bad_request`. For a call with no result, send `"result": null`.

For a call that failed, use the code and message the other server returned, or explain why you couldn't make the call. The waiting action sees only the message.

For an action you didn't perform, set `error.code` to `not_supported`, `refused`, or `internal`. The client that sent `client.perform` gets that code unchanged. An empty code is sent as `internal`.

If `error.message` is longer than 4096 bytes, the server shortens it and ends it with an ellipsis (…). The reply is still accepted.

A reply runs as soon as it arrives. It doesn't wait behind this connection's earlier `client.key` and `client.action` requests, because a `client.action` request that is waiting for the reply holds that line.

A `call_id` that nothing is waiting for fails with `not_found`. That includes a call that was already answered and one that timed out.

### `client.set_label`

Set or remove this client's label.

| Field | Required | Description |
| --- | --- | --- |
| `label` | Yes | The label to set, such as studio. An empty string removes it. At most 64 bytes, with no control characters. |

The label always belongs to the client that sends the request. A request that includes `client_id` fails with `bad_request`.

The server removes whitespace from both ends of `label` before it checks the label, so a label of only spaces removes the current one.

A label longer than 64 bytes, or one that isn't valid UTF-8 or contains a control character, fails with `bad_request`. The message says which rule it breaks.

Labels don't have to be unique. Two clients with the same label are told apart by their IDs.

Labels are for people to read. The server never uses one to decide what a client may do.

When the label changes, the server sends a `client_changed` event to connections that called `session.attach_all` with `event_scope` set to `all`.

A client can also send a label when it connects, in the `client` field of its `hello` message. The same rules apply, but the server fixes the label instead of failing: it cuts a label longer than 64 bytes down to size and drops one that is otherwise invalid. It also shortens a `name` or `version` that is longer than 256 bytes.

### `client.set_script`

Load Lua scripts for this client, replacing any it loaded before.

| Field | Required | Description |
| --- | --- | --- |
| `scripts` | Yes | Every Lua source to load, run in order. They replace all the scripts loaded before. An empty list unloads them. |

The scripts belong to this client and apply in every session it's attached to. A request that includes `session_id` or `client_id` fails with `bad_request`.

If a script has a syntax error, raises an error, or runs longer than 5 seconds while it loads, the call fails with `bad_request`. The scripts loaded before keep running.

To see every key and key sequence the scripts bound to a function, call `client.keymap`. It reports each one as a binding for `client.key.forward`.

The keys that reach the scripts are fixed when they load. A function that a script binds later, while it runs, receives a key only if a function was already bound to that key or sequence when the scripts loaded.

A successful call can still return `diagnostics`, even with severity `error`. An error marks a part of a script the server skipped, such as a binding to a key it can't read. The rest of the scripts still load.

Loading scripts changes this client's keymap without a `keymap_changed` event. Call `client.keymap` again after each call to this method.

### `client.undo_close`

Reopen what this client closed most recently, a pane, a window, or a session, if it can still be undone.

The call reopens the caller's newest close that can still be undone, in whichever session it was. Each client has one history of closes for the whole server, and calling again reopens the one before. There is no redo.

A close can be undone only if it asked to be, with `undoable` set to true. `block.close`, `session.close_window`, and `session.destroy` take it. Send it when a person closed something. A close without it can't be undone.

When an attached client closes a block with `block.close`, or a window with `session.close_window`, and sends `undoable`, the server keeps the blocks running, out of every window, for about a minute, and sends `block_closed` only once it frees a block. Leaving the session frees the client's held blocks there at once.

When an attached client destroys a session with `session.destroy`, and sends `undoable`, the server keeps the whole session, hidden, for about a minute. Undoing that brings the session back at its place in the session list, with the same ID, as it was. A `session_created` event announces it, and a `session_moved` event follows unless it is last. No client is attached to it, the caller included, and its blocks have no owner: attach to it as to a new session. The closes the caller could have undone in the session before it destroyed it are still its to undo, by calling again. Another client's are freed.

The blocks come back where they were, with the same block, split, layer, and window IDs, owned by the caller. A closed window comes back at its place in the window order.

Focus moves to what came back, for every client attached to the session. A reopened block becomes its window's focused block, its window becomes the active window, and a zoom on another block there ends. A reopened window becomes the active window, with the focus and zoom it had. A session comes back with the active window and focus it was destroyed with. The answer names the session, window, and block, so the client can show them, and the place becomes the newest in the caller's focus history.

The close ended the blocks' data streams with `block_closed`. Open them again.

If there is nothing left to reopen, the call fails with `not_found`. A request that includes `client_id` fails with `bad_request`.

## data

### `data.connect`

Get a one-time ticket for opening a data connection to a block. A data connection streams a block's content as it changes, such as a terminal's output.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session that holds the block. The connection must be attached to it with session.attach or session.bootstrap. |
| `block_id` | Yes | The block that provides the data. |
| `data_ref_id` | Yes | Which of the block's data sources to open, such as terminal. |
| `subprotocol` |  | The subprotocol the data connection will use, such as rex.data.terminal.v1. If set, the ticket works only on a connection that uses it. |

The connection must be attached to `session_id` with `session.attach` or `session.bootstrap`. `session.attach_all` isn't enough. If the connection isn't attached, the call fails with `conflict`.

To use the ticket, open a WebSocket to `/api/data` on the server and send the ticket in the HELLO message. A ticket works once, even if the handshake fails, and expires after `expires_in_ms`.

If another user presents the ticket, the data connection gets REJECT reason 0x01, as it would for an unknown ticket. The ticket is then used up, so your own data connection can't use it either.

The server checks only that `data_ref_id` is well formed. If the block has no data by that name, the server closes the data connection with WebSocket status 1008 after the handshake.

Set `subprotocol` to the subprotocol the data connection will use, such as `rex.data.terminal.v1`. The server then refuses a data connection that uses a different one with REJECT reason 0x07, before any data is sent.

If `subprotocol` is left out, the block checks the subprotocol after the handshake and closes the data connection with status 1008 if it doesn't support it.

The call fails with `bad_request` if `data_ref_id` or `subprotocol` is malformed, and with `not_found` if the block isn't in the session or has no data to offer.

## focus_history

### `focus_history.reverse`

Step back through the focus changes the calling principal made.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` |  | Only go back to a block in this session. The client must be attached to it. |
| `not_session_id` |  | Only go back to a block in another session than this one. |
| `window_id` |  | Only go back to a block in this window. |
| `not_window_id` |  | Only go back to a block in another window than this one. |
| `cursor` |  | The cursor from an earlier result, to keep stepping back from where that call stopped. Leave it out to start from where focus is now. |

## help

### `help.all`

Describe every method the server provides, including block methods.

The result has two lists. `methods` describes each method with its arguments, result, examples, and notes. `block_types` lists each creator whose blocks provide methods, with its flavors and those methods.

The result describes the server you are connected to, so it always matches that server's version.

Over HTTP, `GET /api/help` returns the same document with an added `http` field, and `/llms.txt` shows it as Markdown.

## hosts

### `hosts.list`

List the server's hosts: the other Rex servers you connect to by label.

Every Rex server keeps a host list. Each of your devices reads its hosts from the one server it uses as its home, so they all see the same list.

The list holds the hosts declared with `rex.host` in the server's configuration file, and the hosts that clients added with `hosts.put`. A declared host has a `source`, such as `init.lua:4`. A host added with `hosts.put` has none.

Each host comes back exactly as it was stored, including fields this server doesn't know. A client that sends a host back with `hosts.put` must keep those fields.

A declared host with a mistake in it, or whose label another host already uses, is left out of `hosts`. A warning in `diagnostics` names the line that declared it.

A server started without a state directory can't store hosts, so it lists only the declared ones.

If a hand edit broke the file that stores the hosts, the call fails with `conflict` and a message that names the file.

### `hosts.put`

Add a host to the server's host list, or replace the host with the same ID.

| Field | Required | Description |
| --- | --- | --- |
| `host` | Yes | The host to add, or to store in place of the host with the same id. |

The device that adds a host chooses its `id`, so sending the same request again is safe and adds nothing. If `host` has no `id`, the server creates one.

If `host` matches the stored host in every field except `updated_at`, nothing changes and the result holds the stored host.

`label` can't be empty, can't start or end with white space, and has at most 64 characters. No other host in the list may have the same label, ignoring case. If one does, the call fails with `conflict` and a message that names that host and, for a declared host, the line that declared it.

`endpoints` needs at least one endpoint, each in a form that the `-S` option of `rex` accepts. Unix sockets and named pipes aren't allowed, because their paths work only on their own machine.

To change a declared host, put a host with its `id`. The server never writes the configuration file. It stores the host you send, which takes the place of the declared one. A put also brings back a host that `hosts.remove` removed.

The server sets `updated_at` and drops `source`. It stores every other field as sent, including fields it doesn't know.

When the put changes the list, every connected client receives a `hosts_changed` event.

If `host` fails a check, the call fails with `bad_request` and a message that names the field. A server started without a state directory can't store hosts, and fails with `not_supported`. A hand edit that broke the file that stores the hosts makes the call fail with `conflict`.

The file that stores the hosts can hold at most 1 MiB, which is room for thousands of hosts. A put that would make it larger fails with `too_large`.

### `hosts.remove`

Remove a host from the server's host list.

| Field | Required | Description |
| --- | --- | --- |
| `id` | Yes | The host to remove. |

Removing a host that isn't in the list isn't an error. `removed` is false, nothing changes, and no event is sent, so calling it again is safe. The same happens if `id` is left out.

The server never writes the configuration file, so removing a declared host hides it. Removing a stored host that took the place of a declared one removes both. Either way, only a later `hosts.put` with the same `id` brings the host back.

When a host is removed, every connected client receives a `hosts_changed` event.

If `id` isn't a valid host ID, the call fails with `bad_request`. A server started without a state directory can't store hosts, and fails with `not_supported`. A hand edit that broke the file that stores the hosts makes the call fail with `conflict`.

## server

### `server.apple.grant_file_access`

Let the server, and every program it runs, read files a Mac app was given.

| Field | Required | Description |
| --- | --- | --- |
| `files` | Yes | The files to make readable, in the order they were dropped or pasted. At most 256. |

A Mac app calls this when a file is dropped on or pasted into a terminal. macOS lets the app open the file, but not always the server, which macOS treats as a different app.

For each file, the server first tries to open `path`. It uses `token` only if it can't, so most files, such as those in a project, come back `readable` and their tokens go unused.

A file the server can't open doesn't fail the call. A relative path is always `denied`.

Access lasts until the server exits. If a file comes back `denied`, or with an `access` value the client doesn't know, copy the file somewhere the server can read instead.

A request that names more than 256 files fails with `bad_request`.

The server accepts this method only over its local Unix socket, or its named pipe on Windows. Over any other connection, such as TCP or Tailscale, the call fails with status 403.

### `server.apple.privacy_status`

Report the macOS privacy permissions the server and its programs have.

macOS decides privacy permissions for the app it holds responsible for a process. Every shell and program the server runs belongs to the server, so they all get the permissions listed here, whatever the app that shows their terminals was allowed.

Only the server can read its own permissions. A Mac app calls this to show them, and calls it again after the person changes one in System Settings.

Reading the permissions never makes macOS ask the person anything.

`responsible_path` is the executable macOS holds responsible for the server. The permissions belong to the app that contains it. When the server was started in the foreground from a terminal app, that is the terminal app.

Skip a `service` you don't know, and treat a `status` you don't know as `unknown`. A server that isn't running on macOS lists no services.

The server accepts this method only over its local Unix socket, or its named pipe on Windows. Over any other connection, such as TCP or Tailscale, the call fails with status 403.

### `server.config_reload`

Reload the configuration file and tell every client to fetch its keymap again.

The server reads the same configuration file it read when it started, usually `init.lua`, along with the modules that file loads with `require`.

The next `client.keymap` result reports the same `generation` in `config.generation`, unless the file is reloaded again first.

A mistake that stops the file from loading, such as a Lua syntax error, doesn't fail the call. The server keeps the bindings, actions, and hosts from the last load that worked, and `diagnostics` reports the mistake.

If the file no longer exists, the reload removes the bindings, actions, and hosts it used to declare. That isn't an error.

`diagnostics` lists only problems in the file itself. A problem that depends on a client, such as a binding to an action that client doesn't have, is reported by `client.keymap` instead.

After the load, every connected client receives a `keymap_changed` event with the new `generation` and `hash`. A client can keep its keymap if its last `client.keymap` result has the same `hash` and came from the same server process, that is, the same `instance_id`.

If the reload changes the host list, such as by adding or removing a `rex.host` declaration, every connected client also receives a `hosts_changed` event.

The server accepts this method only over its local Unix socket, or its named pipe on Windows. Over any other connection, such as TCP or Tailscale, the call fails with status 403.

### `server.status`

Get the server's identity, session count, configuration, and Tailscale status.

Two servers report the same `host_id` only when they see the same files, as two servers run by one user on one machine usually do. If the values differ, or either one is missing, assume the servers don't share files. The value means nothing else.

`config` describes the last load of the configuration file. Its `generation` and `hash` match the `config` of a `client.keymap` result taken at the same moment.

A client that saved a keymap can compare `config.hash` and `instance_id` with the values it saved. If either differs, call `client.keymap` again.

Later changes to `tailscale` arrive as `tailscale_status_changed` events, which only connections that called `session.attach_all` or `session.bootstrap` receive.

### `server.stop`

Shut the server down, or with if_idle, only if nothing is using it.

| Field | Required | Description |
| --- | --- | --- |
| `if_idle` |  | Stop only if the server has no sessions and no other client is connected. A server that is in use refuses with conflict and keeps running. |

Only a client on the server's own machine, connected over its Unix socket or named pipe, can call this method.

Without `if_idle`, the server stops no matter what it is doing, and every program running in its sessions ends.

With `if_idle`, the server stops only if it has no sessions, including any still being created or closed, and no client is connected except the caller. Otherwise it keeps running and the call fails with `conflict`. The error message says what is using the server.

The server checks and stops in one step. A client that connects just after the check is refused.

The server replies before it shuts down. Close the connection after reading the reply. The server waits up to a second for the connection to close before it stops.

A server running inside another program, with no process of its own, fails the call with `not_supported`.

The server accepts this method only over its local Unix socket, or its named pipe on Windows. Over any other connection, such as TCP or Tailscale, the call fails with status 403.

### `server.tailscale.disable`

Turn off built-in Tailscale, keeping its sign-in for the next enable.

Turning off built-in Tailscale closes every connection that came in over the tailnet. Sessions keep running.

The device keeps its sign-in, so the next `server.tailscale.enable` reconnects without signing in. To sign out instead, call `server.tailscale.logout`.

If built-in Tailscale is already off, the call changes nothing and returns the current status, so calling it again is safe.

If the server can't run built-in Tailscale, the call fails with `not_supported`.

The server accepts this method only over its local Unix socket, or its named pipe on Windows. Over any other connection, such as TCP or Tailscale, the call fails with status 403.

### `server.tailscale.enable`

Turn on built-in Tailscale so devices on your tailnet can reach the server.

| Field | Required | Description |
| --- | --- | --- |
| `hostname` |  | The device name to use if this call starts the device, such as studio. If left out, the server uses its configured name, or rex. |
| `allow_tailnet_members` | Yes | True lets in anyone your tailnet's access rules allow. False lets in only the Tailscale user who signed the device in. Applies on every call, even when the device is already on. |
| `auth_key` |  | A Tailscale auth key that signs the device in without a browser. Used only when this call starts the device. Never logged or saved. |
| `advertise_tags` |  | Tailscale tags, such as tag:rex, for the device to sign in with. Used only when this call starts the device. Needs allow_tailnet_members set to true. |
| `control_url` |  | The control server to sign in with if this call starts the device, such as https://headscale.example.com. If left out, the server uses its configured control server, or Tailscale's own. |

Built-in Tailscale is a copy of Tailscale inside Rex. It makes the server join your tailnet as a device of its own, so the machine doesn't need Tailscale installed.

If built-in Tailscale is already on, the call only applies `allow_tailnet_members`, without restarting the device or dropping connections. It ignores `hostname`, `auth_key`, and `advertise_tags`.

The first time the device starts, it must sign in to Tailscale. With a valid `auth_key`, it signs in without a browser. Otherwise `state` becomes `needs_login`, and the sign-in link appears in `auth_url` and in the server's log.

The device keeps its sign-in, so later calls need no `auth_key`. The server never logs, saves, or returns the key.

`advertise_tags` signs the device in as a tagged device, which has no owner, so it needs `allow_tailnet_members` set to true. The auth key or OAuth client that signs the device in must be allowed to grant the tags.

The call returns once the device has started, before it has finished connecting. The server is reachable over the tailnet only once `https.state` is `available`. Follow the progress with `tailscale_status_changed` events, on a connection that called `session.attach_all` or `session.bootstrap`.

If the HTTPS listener fails later, built-in Tailscale turns off: `state` becomes `disabled` and `error` says why.

When the call starts the device, it fails with `bad_request` for a tag that isn't a valid Tailscale tag, and for tags with `allow_tailnet_members` set to false.

While the server is shutting down, the call fails with `conflict`.

If the server can't run built-in Tailscale, the call fails with `not_supported`.

The server accepts this method only over its local Unix socket, or its named pipe on Windows. Over any other connection, such as TCP or Tailscale, the call fails with status 403.

### `server.tailscale.login`

Ask Tailscale for a sign-in link for the server's Tailscale device.

The call starts the sign-in and returns without waiting for the link. If `auth_url` is empty, the link arrives later in a `tailscale_status_changed` event, which only connections that called `session.attach_all` or `session.bootstrap` receive. `server.status` also shows it once it is ready.

Calling it again while a sign-in is already under way is safe and doesn't start another one.

If built-in Tailscale is off, the call fails with `conflict`. Turn it on with `server.tailscale.enable` first.

If the request fails, or Tailscale doesn't accept it within 10 seconds, the call fails. The server keeps trying in the background.

If the server can't run built-in Tailscale, the call fails with `not_supported`.

The server accepts this method only over its local Unix socket, or its named pipe on Windows. Over any other connection, such as TCP or Tailscale, the call fails with status 403.

### `server.tailscale.logout`

Sign the server out of Tailscale and turn off built-in Tailscale.

After signing out, built-in Tailscale turns off. The next `server.tailscale.enable` must sign in again.

If built-in Tailscale is off, the call changes nothing and the saved sign-in stays. Turn it on first to sign out.

If signing out fails, or Tailscale doesn't answer within 10 seconds, the call fails and built-in Tailscale stays on, so you can try again.

If the server can't run built-in Tailscale, the call fails with `not_supported`.

The server accepts this method only over its local Unix socket, or its named pipe on Windows. Over any other connection, such as TCP or Tailscale, the call fails with status 403.

### `server.tailscale.rename`

Change the server's Tailscale device name without signing in again.

| Field | Required | Description |
| --- | --- | --- |
| `hostname` | Yes | The new device name, such as studio: 1 to 63 ASCII letters, digits, and hyphens, not starting or ending with a hyphen. |

The device keeps its identity and its sign-in. Until the server exits, a later `server.tailscale.enable` without a `hostname` uses the new name too.

`dns_name` in the result may still show the old name. The new one arrives in a `tailscale_status_changed` event, on a connection that called `session.attach_all` or `session.bootstrap`.

If built-in Tailscale is off, the call fails with `conflict`. To choose the name then, pass `hostname` to `server.tailscale.enable` instead.

If `hostname` isn't a valid device name, the call fails with `bad_request`.

If the server can't run built-in Tailscale, the call fails with `not_supported`.

The server accepts this method only over its local Unix socket, or its named pipe on Windows. Over any other connection, such as TCP or Tailscale, the call fails with status 403.

### `server.version`

Get the version of Rex that the server is running and how it was built.

A missing `api_revision` or `api_min_revision` means 0. Servers from before these fields existed leave both out.

### `server.whoami`

Get how the server identified you, and the account the server runs as.

Which fields `principal` has depends on its `kind`. A `peer` has `uid` and `gid`, and usually `pid`. A `windows_peer` has `sid`, and usually `pid`. A `tailscale` client has `user_id`, `login_name`, and `node`, plus `tags` if its device is tagged. An `anonymous` client has none of these.

The server identifies a client when its connection opens. `principal` stays the same for as long as the connection lasts.

`principal` describes a decision the server already made when it let the client in. Use it to show who is connected, not to decide what a client may do.

## session

### `session.attach`

Attach to a session: start receiving its events and get its current view.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to attach to. |

The connection starts receiving every event from the session, including `block_event`, before the server reads `view`. Apply `view` first, then each event whose `seq` is higher than the response's `seq`, even one that arrived before the response.

Most methods that take a `session_id` work only on a connection attached to that session, with this method, `session.bootstrap`, or `session.attach_all`. On a connection that isn't attached, they fail with `conflict`.

Attaching makes the connection's client one of the session's clients. The server sends `client_connected`, and `session.list_clients` lists the client.

`data.connect`, `session.own_block`, and `session.disown_block` need this kind of attachment. Attaching with `session.attach_all` isn't enough for them.

Calling it again for the same session is safe. It returns the same `client_id` and a fresh `view`.

If `session_id` names no session, the call fails with `session_not_found`.

### `session.attach_all`

Start receiving events from the whole server and get the list of sessions.

| Field | Required | Description |
| --- | --- | --- |
| `event_scope` | Yes | Which events to receive. 'session' sends every session's events except block_event, plus session_created, session_destroyed, session_moved, and tailscale_status_changed. 'all' also sends block_event and the client events, such as client_joined. |

Use `session` unless you need `block_event` or the client events. With `all`, the client events are `client_joined`, `client_left`, `client_changed`, `client_performed`, and `client_script_events_dropped`. Any value other than `session` or `all` fails with `bad_request`.

The connection still receives every event from a session it attached to with `session.attach`, whatever the scope.

The connection doesn't join any session. It can call methods on every session, but it isn't listed in `session.list_clients` and can't call `data.connect` or own blocks. To join a session too, call `session.attach`, or use `session.bootstrap` to do both in one call.

Calling it again replaces the scope with the new `event_scope`.

The session list is a snapshot taken after events start. Apply each event whose `seq` is higher than the response message's `seq` on top of it.

Events arrive in order, and their `seq` has no gaps. If the connection falls more than 8 MiB of events behind, the server closes it rather than skip events. Open a new connection to get a fresh snapshot.

### `session.bootstrap`

Set up a new connection in one call: receive events, list sessions, and attach.

| Field | Required | Description |
| --- | --- | --- |
| `event_scope` | Yes | Which events to receive. 'session' sends every session's events except block_event, plus session_created, session_destroyed, session_moved, and tailscale_status_changed. 'all' also sends block_event and the client events, such as client_joined. |
| `preferred_session_id` |  | The session to attach to, if it exists. Otherwise the server attaches the first session it can. Ignored when attach_session_ids is set. |
| `attach_session_ids` |  | The sessions to attach to, in order. Unknown and repeated IDs are skipped, and an empty list attaches none. Leave it out to let the server pick one. |
| `data_tickets` |  | The kinds of block to issue data tickets for. The response has a ticket for each visible block in an attached session that matches one. At most 8 entries. |

Send it as the first request on a new connection. Apply its result first, then each event whose `seq` is higher than the response's `seq`, even one that arrived before the response.

`event_scope` works as it does for `session.attach_all`, and the connection can then call methods on any session. A value other than `session` or `all` fails with `bad_request`.

If `attach_session_ids` is left out, the server attaches one session and returns it in `selected_session`, which is null when the server has no sessions.

If `attach_session_ids` is set, even to an empty array, the server returns the sessions it attached in `attached_sessions` and leaves `selected_session` null.

A session in `attach_session_ids` that is destroyed during the call is left out of `attached_sessions`. If the session chosen for `selected_session` is destroyed during the call, the call fails with `session_not_found`. Any other failure to attach also fails the whole call.

If the connection falls more than 8 MiB of events behind, the server closes it rather than skip events. Open a new connection and call `session.bootstrap` again.

If the call fails, close the connection and open a new one before you try again. Part of the setup may already have taken effect.

### `session.close_layer`

Close a floating layer and every block in it.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `layer_id` | Yes | The floating layer to close. Every block in it closes too. |

`layer_id` must name a floating layer. Naming the window's layout, the layer of kind `tiled` in `session.view`, fails the call with `bad_request`. Close the window with `session.close_window` instead.

The server closes every block in the layer, which ends the programs running in them. The call returns once the blocks have closed.

If the layer had focus, focus returns to the layer that had it before, at the block last focused there. Otherwise focus doesn't change.

If the layer held the window's last blocks, the server closes the window too.

If the session doesn't exist, the call fails with `session_not_found`. If `layer_id` names no layer in the session, it fails with `not_found`.

### `session.close_window`

Close a window and every block in it.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `window_id` |  | The window to close. Leave it out to close the active window. Every block in it closes too. |
| `undoable` |  | If true, hold the window's blocks for about a minute so that the calling client can bring the window back with client.undo_close. Send it when a person closed the window. It only has an effect for a client attached to the session. |

The server closes every block in the window, which ends the programs running in them. The call returns once the blocks have closed.

If `undoable` is true and the caller is a client attached to the session, the server instead keeps the window's blocks running, out of every window, for about a minute, so that `client.undo_close` can put the window back. `block_closed` arrives for each block only once it is freed.

If the window was active, the window after it becomes active, or the one before it if it was last.

If the session doesn't exist, the call fails with `session_not_found`. If `window_id` names a window that isn't in the session, it fails with `not_found`. A window leaves the session as soon as a close starts, so closing the same window twice also fails with `not_found`.

If `window_id` is left out and the session has no windows, the call fails with `conflict`.

### `session.create`

Create a session, optionally with its first windows already in it.

| Field | Required | Description |
| --- | --- | --- |
| `label` |  | The session's label, up to 128 characters. Leave it out to let the server choose one, such as quiet-meadow. |
| `initial_windows` |  | Windows to create with the session, in order. The last one becomes the active window. If any of them fails, the server creates no session. |
| `idempotency_key` |  | A key of up to 128 bytes, chosen by the caller, that makes the call safe to retry. A call that repeats the key of an earlier successful call to the same method by the same principal, a short time later, creates nothing and returns the earlier response. |

Every argument is optional. With none, the server creates a session with no windows.

If `label` is left out or empty, the server picks one that no other session has, such as `quiet-meadow`.

The server sends `session_created` only once every window in `initial_windows` is ready, so no client sees a half-built session. If any window fails, the server closes the session and its blocks, and the call fails.

The blocks in the initial windows start with no owner, because the calling client can't be attached to a session that doesn't exist yet. To own them, call `session.attach` and then `session.own_block`.

The call doesn't attach the connection to the new session. Call `session.attach` to receive its events.

If a layout is malformed, the call fails with `bad_request` before any block is created. A flavor that no creator provides fails with `not_found`.

If the server already has as many sessions as it allows, the call fails with `conflict`.

### `session.describe_block`

Get a block's details and the methods, events, and actions it provides.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `block_id` | Yes | The block to describe. It may be a detached block. |

`api` lists the methods and events the block provides, in the same form as `block_creator.list`. Call a method as `<creator>.<method>` with `session_id`, `block_id`, and its arguments under `args`.

If `block_id` names a block that isn't in the session, or one that is closing, the call fails with `not_found`.

### `session.destroy`

Destroy a session and close every block in it.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to destroy. Every block in it closes. |
| `undoable` |  | If true, hold the session for about a minute, hidden, so that the calling client can bring it back with client.undo_close. Send it when a person destroyed the session. It only has an effect for a client attached to the session, and for a session that has a window. |

The server closes every window and block in the session. Closing a terminal hangs up the program running in it, as closing a terminal window does.

The call returns once the session has closed. `session_destroyed` is the last event about the session, though a `client_script_events_dropped` event for it can still follow.

If `undoable` is true, the caller is attached to the session with `session.attach` or `session.bootstrap`, and the session has a window, the server instead keeps the session for about a minute, hidden, with its blocks running, so that `client.undo_close` can bring it back. To every client it is destroyed all the same: every client is detached, `session_destroyed` goes out, and requests that name it fail with `session_not_found`. No `block_closed` events go out, then or when the server closes the session for good.

The connection must be attached to the session, with `session.attach`, `session.bootstrap`, or `session.attach_all`, or the call fails with `conflict`.

If `session_id` names no session, the call fails with `session_not_found`.

### `session.detach`

Detach the connection from a session. The connection stays open and the session keeps running.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to detach from. |

The connection's other attachments, and any events it receives through `session.attach_all`, continue as before.

The client leaves the session. The server sends `client_disconnected`, and each block the client owned passes to the next client in line for it, if there is one.

If the connection isn't attached to the session, the call succeeds and changes nothing, even if the session doesn't exist.

A `session.attach` for the same session that is still in progress isn't canceled. This call succeeds without detaching, and the attach completes.

If the connection attaches to the session again later, its client keeps the same `client_id`.

### `session.detach_block`

Take a block out of its window without closing it. The block keeps running.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `block_id` | Yes | The block to detach. It keeps running but leaves its window. |

`session.list_blocks` lists the block with `placement` set to `detached`, and `session.move_block` places it in a window again.

Detaching a block that is already detached succeeds and changes nothing.

If the block was the last one in its window, the window closes too. If it was the only block in a floating layer, the layer closes.

If the block had focus, another block in its window gets focus.

To close the block instead, call `block.close`.

If `block_id` names a block that isn't in the session, the call fails with `not_found`.

### `session.disown_block`

Give up the calling client's claim on blocks. The result lists each block's owner.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `block_ids` |  | The blocks to give up. Leave it out or empty to give up every block in the session. |

The calling client must be attached to the session, with `session.attach` or `session.bootstrap`. A connection that only called `session.attach_all` fails with `bad_request`.

A block the caller owned passes to the next connected client in line for it, or is left with no owner. For a block the caller doesn't own, the caller only leaves the line.

`blocks` lists each block's owner after the call, in the order of `block_ids`, with a repeated ID listed once. When you give up every block, they are sorted by `block_id`.

Every change of owner sends `block_owner_changed`. If a block in a window changes owner, the call also sends one `session_view_changed`.

If any ID in `block_ids` isn't a block in the session, the call fails with `bad_request` and changes nothing.

### `session.float_block`

Move a block out of its window's layout into a new floating layer.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `block_id` | Yes | The block to float. It must be in its window's layout, not already in a floating layer. |
| `bounds` | Yes | Where the new floating layer sits, as [x, y, w, h] fractions of the window's width and height. It must fit inside the window. |

`bounds` is measured from the window's top-left corner. Its width and height must be greater than 0.

The new layer is in the block's own window, in front of every other floating layer there.

Focus and the active window don't change. If the block was the zoomed block of the window's layout, that zoom ends, because the block has left the layout. Any other zoom stays.

Floating the last block of a window's layout leaves the layout empty. The window stays open, and its layer of kind `tiled` in `session.view` keeps the same `layer_id`.

If the session doesn't exist, the call fails with `session_not_found`. If `block_id` names a block that isn't in any window, including a detached block, it fails with `not_found`, and bad `bounds` fail with `bad_request`.

If the block is already in a floating layer, the call fails with `bad_request`.

### `session.focus_block`

Focus a block, and make its window the active window if it isn't.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `block_id` | Yes | The block to focus. It must be in a window, which becomes the active window. |

The block can be in the window's layout or in a floating layer.

A zoomed block of a floating layer loses its zoom when focus moves to any other block. A zoomed block of the window's layout loses it only when focus moves to a different block of that layout, and stays zoomed behind a floating layer that takes focus.

If the block already has focus in the active window, the call changes nothing.

If the session doesn't exist, the call fails with `session_not_found`. If `block_id` names a block that isn't in any window, including a detached block, it fails with `not_found`.

### `session.focus_direction`

Move focus to the nearest block to the left, right, above, or below.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `direction` | Yes | Which way to move focus from the focused block in the active window. |
| `wrap` |  | Whether to continue from the opposite edge when no block lies that way. Defaults to false. Older servers ignore it and always wrap. |

The search starts at the focused block of the active window. It covers every block in that window, floating layers included, by where each appears on screen. When two blocks are equally close, the one in front wins.

If no block lies in `direction`, focus doesn't change and the call still succeeds. Moving focus ends a zoom as `session.focus_block` describes.

If the session doesn't exist, the call fails with `session_not_found`. If the session has no windows, it fails with `conflict`.

### `session.focus_next_pane`

Move focus to the next block in the active window.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `wrap` |  | Whether to go from the last block back to the first. Defaults to false. |

Blocks are in layout order: the window's layout first, reading each split's `before` side ahead of its `after` side, then each floating layer from back to front.

If there's no next block, focus doesn't change and the call still succeeds. Moving focus ends a zoom as `session.focus_block` describes.

If the session doesn't exist, the call fails with `session_not_found`. If the session has no windows, it fails with `conflict`.

### `session.focus_next_window`

Make the next window the active window.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `wrap` |  | Whether to go from the last window back to the first. Defaults to false. |

The window order is the order of `windows` in `session.view`.

Each window keeps its own focused block, which then receives typing.

If there's no next window, nothing changes and the call still succeeds.

If the session doesn't exist, the call fails with `session_not_found`. If the session has no windows, it fails with `conflict`.

### `session.focus_previous_pane`

Move focus to the previous block in the active window.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `wrap` |  | Whether to go from the first block back to the last. Defaults to false. |

Blocks are in layout order: the window's layout first, reading each split's `before` side ahead of its `after` side, then each floating layer from back to front.

If there's no previous block, focus doesn't change and the call still succeeds. Moving focus ends a zoom as `session.focus_block` describes.

If the session doesn't exist, the call fails with `session_not_found`. If the session has no windows, it fails with `conflict`.

### `session.focus_previous_window`

Make the previous window the active window.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `wrap` |  | Whether to go from the first window back to the last. Defaults to false. |

The window order is the order of `windows` in `session.view`.

Each window keeps its own focused block, which then receives typing.

If there's no previous window, nothing changes and the call still succeeds.

If the session doesn't exist, the call fails with `session_not_found`. If the session has no windows, it fails with `conflict`.

### `session.focus_window`

Make a window the active window. Focus goes to the block it last had focused.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `window_id` | Yes | The window to make active. Focus goes to the block that was focused in it. |

If the window is already active, the call changes nothing.

If the session doesn't exist, the call fails with `session_not_found`. If `window_id` names a window that isn't in the session, it fails with `not_found`.

### `session.help`

Describe the methods this session accepts and the methods its blocks provide.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |

The result has the same form as `help.all`, with an added `http` field. It describes only the methods the session answers itself, such as `session.view` and `session.new_split`, and the block methods of the creators that session can use.

Most clients call `help.all` instead, which describes every method the server provides.

### `session.list`

List the sessions on the server.

Sessions are listed in the order they were created, until `session.move` changes that order. `session.attach_all` and `session.bootstrap` list them in the same order.

### `session.list_blocks`

List every block in the session, including detached blocks.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |

Treat a `placement` you don't recognize like `detached`. The block exists and you can call its methods, but don't assume where it is shown.

Blocks are sorted by `block_id`.

To see where each block sits in its window and which one has focus, call `session.view`.

### `session.list_clients`

List the clients attached to the session.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |

Only clients attached with `session.attach` or `session.bootstrap` are listed. A connection that only called `session.attach_all` isn't. To list every connected client, call `client.list`.

### `session.lower_layer`

Move a floating layer to the back, or just below another floating layer.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `layer_id` | Yes | The floating layer to move back. |
| `relative_layer_id` |  | Another floating layer in the same window to place it just below. Leave it out to move it behind every other floating layer. |

`layer_id` must name a floating layer. Naming the window's layout, the layer of kind `tiled` in `session.view`, fails the call with `bad_request`.

A floating layer never goes behind the window's layout. At the back, it sits behind every other floating layer and in front of the layout.

If the layer is already in place, the call changes nothing. Focus and the layer's bounds never change.

If the session doesn't exist, the call fails with `session_not_found`. If `layer_id` names no layer in the session, it fails with `not_found`, and if `relative_layer_id` is the same as `layer_id`, it fails with `bad_request`.

If `relative_layer_id` names a layer of kind `tiled`, or a layer in another window, the call fails with `bad_request`. If it names no layer in the session, it fails with `not_found`.

### `session.move`

Move a session to another place in the order that session.list returns.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to move. |
| `before_session_id` |  | The session to place it just before. Leave it out to move the session to the end. |

The order is the same for every client. Each move that changes it sends `session_moved` with the same `session_id` and `before_session_id`.

Moving a session to where it already is succeeds and changes nothing.

The connection must be attached to the session it moves, with `session.attach`, `session.bootstrap`, or `session.attach_all`, or the call fails with `conflict`.

If `before_session_id` names the session being moved, the call fails with `bad_request`.

If either ID names no session, the call fails with `session_not_found`, and the message says which one.

### `session.move_block`

Move a block, or place a detached one, in a new split beside another block.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `block_id` | Yes | The block to move. It may be detached or placed in any window. |
| `anchor_block_id` | Yes | The block to place it beside. It must be placed in a window. |
| `direction` |  | How to divide the anchor's space: 'horizontal' for side by side or 'vertical' for one above the other. Defaults to horizontal. |
| `side` |  | Where the moved block goes: 'before' for the left or top part, or 'after' for the right or bottom part. Defaults to after. |
| `ratio` |  | The fraction of the space that the before part gets, greater than 0 and less than 1. Defaults to 0.5. |

The block and the anchor can be in different windows or layers.

If the block had focus in its window, focus moves with it and its new window becomes active. A detached block doesn't take focus.

A zoom follows its block. Moving another block doesn't end it. Moving the zoomed block of the window's layout to a floating layer or another window ends its zoom. A zoomed block that keeps focus in a floating layer stays zoomed.

If the move empties a floating layer, the server removes it. If it empties a whole window, the server closes the window. A window's layout that empties while the window still has floating layers stays, with the same `layer_id`.

Apart from the two splits named in the result, every split keeps its ID.

If the session doesn't exist, the call fails with `session_not_found`. If `block_id` and `anchor_block_id` are the same, or `ratio` is out of range, it fails with `bad_request`. If either block isn't in the session, or the anchor isn't in a window, it fails with `not_found`.

If the block is detached or in another window, and the anchor's window already has as many blocks as it allows, the call fails with `conflict`.

### `session.move_window`

Move a window to another place in the session's window order.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `window_id` | Yes | The window to move. |
| `before_window_id` |  | The window to place it just before. Leave it out to move the window to the end. |

The window order is the order of `windows` in `session.view` and of the tabs in Rex.app. `session.focus_next_window` and `session.focus_previous_window` follow it.

The active window, focus, and the windows' blocks don't change. If the window is already in place, the call changes nothing.

If the session doesn't exist, the call fails with `session_not_found`. If either window isn't in the session, it fails with `not_found`, and if `before_window_id` is the same as `window_id`, it fails with `bad_request`.

### `session.new_block`

Create a block without placing it in a window. Place it later with session.move_block.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `flavor` | Yes | The flavor of block to create, such as com.superlogical.terminal.shell. block_creator.list lists them. |
| `options` |  | Settings for the block's creator, in the shape of the flavor's options_schema from block_creator.list. |
| `label` |  | The block's label, up to 128 characters. Defaults to the flavor's short name, such as shell. |
| `idempotency_key` |  | A key of up to 128 bytes, chosen by the caller, that makes the call safe to retry. A call that repeats the key of an earlier successful call to the same method by the same principal, a short time later, creates nothing and returns the earlier response. |

The server passes `options` to the flavor's creator unchanged.

The block starts detached: it runs, sends events, and answers method calls, but no window shows it. `session.move_block` can place it beside a block that is in a window.

If the calling client is attached to the session, it becomes the block's owner. Otherwise the block has no owner until an attached client claims it with `session.own_block`.

A malformed `flavor` or `label` fails with `bad_request`. A flavor that no creator provides fails with `not_found`.

If the server already has as many blocks as it allows, the call fails with `conflict`.

### `session.new_layer`

Create blocks in a new floating layer at the front of a window.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `window_id` |  | The window to add the floating layer to. Leave it out to use the active window. |
| `bounds` | Yes | Where the new floating layer sits, as [x, y, w, h] fractions of the window's width and height. It must fit inside the window. |
| `layout` | Yes | The blocks to create in the floating layer and how to arrange them. Each node holds either block, with a flavor and optional options and label, or split, with direction, before, after, and an optional ratio. |
| `focus` |  | Whether to make the window active and focus the first new block. Defaults to false. |
| `idempotency_key` |  | A key of up to 128 bytes, chosen by the caller, that makes the call safe to retry. A call that repeats the key of an earlier successful call to the same method by the same principal, a short time later, creates nothing and returns the earlier response. |

`bounds` is measured from the window's top-left corner. Its width and height must be greater than 0.

A `block` node in `layout` starts one new block from a `flavor`, such as `com.superlogical.terminal.shell`. A `split` node divides its space in two and holds another node in each of `before` and `after`.

In a `split` node, `direction` is `horizontal` to put `before` on the left of `after`, or `vertical` to put it on top. `ratio` is the fraction of the space that `before` gets, greater than 0 and less than 1. It defaults to 0.5.

`layout` always starts new blocks. To move a block that is already in a window's layout into a floating layer, use `session.float_block`.

The new layer starts in front of every other floating layer in the window.

A zoomed block of the window's layout stays zoomed behind the new layer, whether or not `focus` is set. A zoomed block of another floating layer loses its zoom only if `focus` takes focus from it.

Either the whole layout is created or none of it is. If a block fails to start, the server closes the blocks it already started, and the call fails.

If the session doesn't exist, the call fails with `session_not_found`. If `window_id` names a window that isn't in the session, or no creator provides a `flavor`, it fails with `not_found`. Bad `bounds`, or a malformed `layout` or `flavor`, fail with `bad_request`.

If `window_id` is left out and the session has no windows, the call fails with `conflict`.

If the call would go past a limit on blocks per window or blocks on the server, it fails with `conflict`.

### `session.new_split`

Create blocks in a new split beside an existing block or split.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `anchor_id` |  | The block or split whose space to split. A block ID splits that one block. A split ID puts the new blocks beside that split and everything under it. Leave it out to split the focused block of window_id, or of the active window. Don't send it with window_id. |
| `window_id` |  | The window whose focused block to split. Send it only when anchor_id is left out. |
| `direction` | Yes | How to divide the anchor's space: 'horizontal' for side by side or 'vertical' for one above the other. |
| `side` | Yes | Where the new blocks go: 'before' for the left or top part, or 'after' for the right or bottom part. |
| `ratio` |  | The fraction of the space that the before part gets, greater than 0 and less than 1. Defaults to 0.5. |
| `layout` | Yes | The blocks to create beside the anchor and how to arrange them. Each node holds either block, with a flavor and optional options and label, or split, with direction, before, after, and an optional ratio. |
| `focus` |  | Whether to make the anchor's window active and focus the first new block. Defaults to false. |
| `idempotency_key` |  | A key of up to 128 bytes, chosen by the caller, that makes the call safe to retry. A call that repeats the key of an earlier successful call to the same method by the same principal, a short time later, creates nothing and returns the earlier response. |

The server picks the block to split before it starts the new blocks, so a focus change while they start doesn't move the split.

A `block` node in `layout` starts one new block from a `flavor`, such as `com.superlogical.terminal.shell`. A `split` node divides its space in two and holds another node in each of `before` and `after`.

In a `split` node, `direction` is `horizontal` to put `before` on the left of `after`, or `vertical` to put it on top. `ratio` is the fraction of the space that `before` gets, greater than 0 and less than 1. It defaults to 0.5.

A new split doesn't end a zoom by itself. If `focus` is set, focus moves to the new block, and that ends a zoom as `session.focus_block` describes. Without `focus`, a zoomed block stays zoomed and the new blocks are hidden behind it.

If `anchor_id` is a split ID, the new split takes that split's place. The old split, with everything under it, goes on one side and `layout` on the other. Anchoring a layer's top split makes the new blocks span the whole layer. A layer with one block has no split, so anchor its block instead.

Splits that already existed keep their IDs.

Either the whole layout is created or none of it is. If a block fails to start, the server closes the blocks it already started, and the call fails.

If the session doesn't exist, the call fails with `session_not_found`. If `window_id` names a window that isn't in the session, or no creator provides a `flavor`, it fails with `not_found`. Sending both `anchor_id` and `window_id`, a bad `ratio`, or a malformed `layout` or `flavor` fail with `bad_request`.

If `anchor_id` names a block that isn't in a window, including a detached block, or a split that isn't in any window, the call fails with `not_found`. If both `anchor_id` and `window_id` are left out and the session has no windows, it fails with `conflict`.

If the call would go past a limit on blocks per window or blocks on the server, it fails with `conflict`.

### `session.new_window`

Create a window and the blocks in its layout. It becomes the active window by default.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `window_label` |  | The window's label, up to 128 characters. Leave it out for a label made from the window's ID, such as Window 89abcdef. |
| `layout` |  | The blocks to create in the window and how to arrange them. Required. Each node holds either block, with a flavor and optional options and label, or split, with direction, before, after, and an optional ratio. |
| `focus` |  | Whether to make the new window the active window. Defaults to true. A session with no active window always makes the new one active. |
| `idempotency_key` |  | A key of up to 128 bytes, chosen by the caller, that makes the call safe to retry. A call that repeats the key of an earlier successful call to the same method by the same principal, a short time later, creates nothing and returns the earlier response. |

A `block` node in `layout` starts one new block from a `flavor`, such as `com.superlogical.terminal.shell`. A `split` node divides its space in two and holds another node in each of `before` and `after`.

In a `split` node, `direction` is `horizontal` to put `before` on the left of `after`, or `vertical` to put it on top. `ratio` is the fraction of the space that `before` gets, greater than 0 and less than 1. It defaults to 0.5.

`layout` always starts new blocks. To place a detached block that already exists, use `session.move_block`.

In the new window, the first block in `block_ids` has focus.

Either the whole layout is created or none of it is. If a block fails to start, the server closes the blocks it already started, and the call fails.

If the session doesn't exist, the call fails with `session_not_found`. If `layout` is missing or malformed, or a `flavor` is malformed, it fails with `bad_request`, and if no creator provides a `flavor`, it fails with `not_found`.

If the call would go past a limit on windows per session, blocks per window, or blocks on the server, it fails with `conflict`.

### `session.own_block`

Claim blocks for the calling client. The result lists each block's owner.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `block_ids` |  | The blocks to claim. Leave it out or empty to claim every block in the session. |
| `mode` |  | How to claim them. 'take' makes the calling client the owner right away. 'request' makes it the owner only of blocks that have none, and it may get the rest when their owner gives them up or leaves. Defaults to take. |

When the clients attached to a session want different things for a block, such as a terminal's size, the block follows its owner. Owning a block gives no other rights over it.

The calling client must be attached to the session, with `session.attach` or `session.bootstrap`. A connection that only called `session.attach_all` fails with `bad_request`.

Either mode puts the caller in line for the block. When the owner gives it up, detaches, or loses its connection, the block passes to the connected client in line that claimed it most recently, with any `take` ahead of every `request`.

An owner whose connection drops gets each of its blocks back when it reconnects, unless that block's owner has changed again since.

`blocks` lists each block's owner after the call, in the order of `block_ids`, with a repeated ID listed once. When you claim every block, they are sorted by `block_id`.

Every change of owner sends `block_owner_changed`. If a block in a window changes owner, the call also sends one `session_view_changed`, because `session.view` shows owners.

A `mode` other than `take` or `request` fails with `bad_request`.

If any ID in `block_ids` isn't a block in the session, the call fails with `bad_request` and changes nothing.

### `session.raise_layer`

Move a floating layer to the front, or just above another floating layer.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `layer_id` | Yes | The floating layer to move forward. |
| `relative_layer_id` |  | Another floating layer in the same window to place it just above. Leave it out to move it in front of every other floating layer. |

`layer_id` must name a floating layer. Naming the window's layout, the layer of kind `tiled` in `session.view`, fails the call with `bad_request`.

If the layer is already in place, the call changes nothing. Focus and the layer's bounds never change.

If the session doesn't exist, the call fails with `session_not_found`. If `layer_id` names no layer in the session, it fails with `not_found`, and if `relative_layer_id` is the same as `layer_id`, it fails with `bad_request`.

If `relative_layer_id` names a layer of kind `tiled`, or a layer in another window, the call fails with `bad_request`. If it names no layer in the session, it fails with `not_found`.

### `session.resize_layer`

Move or resize a floating layer.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `layer_id` | Yes | The floating layer to move or resize. |
| `bounds` | Yes | The layer's new position and size, as [x, y, w, h] fractions of the window's width and height. It must fit inside the window. |

`layer_id` must name a floating layer. Naming the window's layout, the layer of kind `tiled` in `session.view`, fails the call with `bad_request`.

`bounds` is measured from the window's top-left corner. Its width and height must be greater than 0.

Focus and the order of floating layers don't change. Setting the bounds the layer already has changes nothing.

If the session doesn't exist, the call fails with `session_not_found`. If `layer_id` names no layer in the session, it fails with `not_found`, and bad `bounds` fail with `bad_request`.

### `session.resize_pane`

Move the border between two blocks to change their sizes.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `direction` | Yes | The kind of split between the two blocks: 'horizontal' for a border between left and right, or 'vertical' for one between top and bottom. |
| `before_block_id` | Yes | A block on the left of the border, or above it when direction is vertical. |
| `after_block_id` | Yes | A block on the right of the border, or below it when direction is vertical. |
| `ratio` | Yes | The fraction of the split's space that the before part gets, greater than 0 and less than 1. |

The two blocks pick the border. The server finds the innermost split in `direction` that has `before_block_id` on its left or top side and `after_block_id` on its right or bottom side. The blocks don't need to touch.

`ratio` has no default. Unlike in `session.new_split`, 0 doesn't mean an even split.

The blocks can be in any window, active or not. Focus doesn't change.

The call always raises `revision` and sends `session_view_changed`, even if the border was already where you asked.

If the session doesn't exist, the call fails with `session_not_found`. If the two block IDs are the same, or `ratio` is out of range, it fails with `bad_request`, and if either block isn't in any window, it fails with `not_found`.

If the blocks are in different windows or layers, or no split between them matches, the call fails with `bad_request`.

### `session.set_block_label`

Set a block's label.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `block_id` |  | The block to relabel. Required. |
| `label` |  | The new label, up to 128 characters. An empty or missing label restores a default made from the block's ID. |

`block_id` is required. Leaving it out fails with `bad_request`.

The server trims whitespace from both ends of `label`. An empty `label` restores a default made from the block's ID, such as `Block 89abcdef`, rather than the flavor name a new block starts with.

A label longer than 128 characters, or one that contains a control character, fails with `bad_request`.

Relabeling a block that is in a window sends `session_view_changed`. A detached block isn't part of the view, so relabeling it sends no event and leaves `revision` unchanged.

If `block_id` names a block that isn't in the session, the call fails with `not_found`.

### `session.set_label`

Set the session's label.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `label` |  | The new label, up to 128 characters. An empty or missing label restores the label the server chose when it created the session. |

The server trims whitespace from both ends of `label`. An empty `label` restores the label the server chose when it created the session, such as `quiet-meadow`. It does so even if the session was created with a label.

A label longer than 128 characters, or one that contains a control character, fails with `bad_request`.

A new label sends `session_label_changed`, then `session_view_changed`. Setting the label the session already has changes nothing.

### `session.set_layer_state`

Minimize a floating layer or return it to normal, optionally raising and focusing it.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `layer_id` | Yes | The layer to change. |
| `state` | Yes | The state to set: 'normal' or 'minimized'. |
| `focus` |  | Whether to also raise the layer, focus the block last focused in it, and make its window active, all in one change. Needs state to be 'normal' and the layer to have a block. Defaults to false. |

Only a floating layer can be minimized. Minimizing the window's layout, the layer of kind `tiled` in `session.view`, fails with `bad_request`. Setting it to `normal` succeeds and changes nothing.

With `focus` set to `true`, the layer is also raised, the block last focused in it takes focus, or its first block, and its window becomes active, all in one revision. This also works on a layer that is already normal and on the tiled layer. `focus` with `minimized`, or on a layer with no blocks, fails with `bad_request` and changes nothing.

`state` must be `normal` or `minimized`. Any other value fails with `bad_request`.

A minimized layer stays in `session.view` with `state` set to `minimized`, its blocks keep running, and it keeps its bounds and its place in the stack. `state` is left out for a normal layer.

Minimizing the layer that has focus moves focus to the layer used before it, or to the nearest visible pane. That ends a zoom in the layer. A zoomed block of the window's layout stays zoomed unless focus lands on a different block of that layout. Returning a layer to normal leaves focus where it is. Setting the state the layer already has changes nothing.

A window must keep a visible pane, so minimizing the layer that holds its last visible panes fails with `bad_request`.

If the session doesn't exist, the call fails with `session_not_found`. If `layer_id` names no layer in the session, it fails with `not_found`.

### `session.set_window_label`

Set a window's label.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `window_id` | Yes | The window to relabel. |
| `label` |  | The new label, up to 128 characters. An empty or missing label restores a default made from the window's ID. |

The server trims whitespace from both ends of `label`. An empty `label` restores a default made from the window's ID, such as `Window 89abcdef`.

A label longer than 128 characters, or one that contains a control character, fails with `bad_request`.

A new label sends `window_label_changed`, then `session_view_changed`. Setting the label the window already has changes nothing.

If `window_id` names a window that isn't in the session, the call fails with `not_found`.

### `session.swap_blocks`

Swap the places of two blocks.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `block_id` | Yes | One of the two blocks to swap. |
| `other_block_id` | Yes | The other block. The order of the two doesn't matter. |

Both blocks must be in a window. They can be in different windows or layers.

Only the two blocks move. Splits, their sizes and IDs, floating layers, and the window order stay the same.

If one of the blocks has focus in the active window, focus follows it to its new place, and that place's window becomes active.

A zoom follows its block, so the other block doesn't take it over. A zoomed block stays zoomed if it is still where its zoom allows: in the window's layout for that zoom, or focused in a floating layer. Otherwise the zoom ends.

If the session doesn't exist, the call fails with `session_not_found`. If `block_id` and `other_block_id` are the same, it fails with `bad_request`. If either block isn't in any window, including a detached block, it fails with `not_found`.

### `session.transfer_window`

Move a window, with its blocks still running, to another session.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session that holds the window. |
| `window_id` | Yes | The window to move. |
| `to_session_id` | Yes | The session to move the window to. It must be a different session. |
| `before_window_id` |  | The window in the destination session to place it just before. Leave it out to put the window at the end. |
| `focus` |  | Whether to make the window the destination session's active window. Defaults to false. A session with no active window always makes it active. |

The window keeps its ID, label, layout, focused block and zoom, and its blocks keep their IDs and go on running. A terminal keeps its program and its scrollback.

The session the window leaves sends `window_closed` and a `block_closed` for each block, as if the window had closed. The destination sends a `block_created` for each block and then `window_created`. A client that is attached to both sees the same IDs close in one and open in the other.

Streams opened on the window's blocks through the session it left end. Open them again through the destination session.

The calling client becomes the owner of the blocks if it is attached to the destination session. Otherwise they have no owner until a client claims them.

A program already running in a terminal keeps the `REX_SESSION` value it started with, which names the session the window left.

If the window's session has no other window, it is left with none, as after `session.close_window`.

To reorder windows within one session, use `session.move_window`. If `to_session_id` equals `session_id`, the call fails with `bad_request`.

If the destination already has its maximum number of windows, or a block of the window is still starting or is being moved by another call, the call fails with `conflict` and the window stays where it is.

If either session doesn't exist, the call fails with `session_not_found`, and the message says which one. If `window_id` isn't in the session, or `before_window_id` isn't in the destination, it fails with `not_found`.

### `session.view`

Get the session's windows, their layouts, and their blocks in one snapshot.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |

`revision` starts at zero for a new session and goes up by one each time the view changes. Compare revisions only within one session, and keep the view with the highest revision.

A `session_view_changed` event carries only the new revision, not the view. These events can arrive out of revision order, so call `session.view` only when an event's revision is higher than the one in the view you hold.

`window_created`, `window_closed`, `window_label_changed`, `active_window_changed`, and `session_label_changed` arrive before the `session_view_changed` event for the same change.

The view holds only blocks that are in a window. `session.list_blocks` also lists detached blocks.

The view describes structure, not content. To read what a block shows, call one of its own methods, such as `com.superlogical.terminal.format`.

### `session.zoom_block`

Zoom a block to fill its window, or undo the zoom.

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | Yes | The session to act on. |
| `block_id` |  | The block to zoom. It takes focus, and its window becomes active. Leave it out to use the focused block of window_id, or of the active window. |
| `window_id` |  | A window whose focused block to zoom. The active window doesn't change. Send it only when block_id is left out. |
| `zoom` |  | Set true to zoom or false to restore the layout. Leave it out to switch between the two. |

With `block_id`, the server first focuses the block and makes its window active, as `session.focus_block` does. With `window_id`, focus and the active window don't change.

A window has two zooms, one for its layout and one for its floating layers, and both can be on at once. The call changes the one for the layer the block is in. `session.view` reports them as `tiled_zoomed_block_id` and `zoomed_block_id`.

A zoomed block of the window's layout is shown behind the floating layers. It stays zoomed while a floating layer has focus, and the zoom ends when focus moves to a different block of the layout. A zoomed block of a floating layer is shown in front of everything, and its zoom ends when focus moves to any other block.

Zoom changes only what is shown. The layout stays the same. A change to a layout, such as a new split, doesn't end a zoom unless it moves focus as above or takes the zoomed block out of the window's layout.

If the session doesn't exist, the call fails with `session_not_found`. If `block_id` names a block that isn't in any window, or `window_id` names a window that isn't in the session, it fails with `not_found`. Sending both fails with `bad_request`.

If both `block_id` and `window_id` are left out and the session has no windows, the call fails with `conflict`.

## target

### `target.complete`

List the labels, window positions, and short IDs that start with a prefix. Use it to complete a name as someone types it.

| Field | Required | Description |
| --- | --- | --- |
| `kinds` | Yes | What to complete: session, window, block, or client, with the same rules as in target.resolve. Completions come back in this order. |
| `prefix` | Yes | The text typed so far. It matches the start of labels (ignoring case), window positions, and short IDs. An empty prefix matches everything. |
| `context` |  | Where the caller is. Only the caller's session is used, found from block_id or session_id as in target.resolve. Without scope.session, windows and blocks come from that session. |
| `scope` |  | Limits completion to one session, or block completion to one window, as in target.resolve. |

`kinds`, `scope`, and `context` choose what to search the same way as in `target.resolve`, and the call fails with `bad_request` in the same cases. Only the caller's session is taken from `context`.

`prefix` matches the start of labels, ignoring case, and label completions keep the label's own case. White space around `prefix` is ignored. A control character inside it, such as a tab, fails the call with `bad_request`.

Windows also match by position, so the prefix `1` matches windows 1, 10, 11, and so on. An empty prefix matches every position.

An empty prefix, or one made only of hexadecimal digits, also matches the start of short IDs. A short ID is the last six hexadecimal digits of an ID, such as `12bef5`, and `target.resolve` accepts it as the end of an ID.

One thing can appear more than once, such as a window whose label and short ID both start with the prefix.

Completions are grouped by kind, in the order of `kinds`. Within each kind, labels come first, sorted ignoring case, then window positions in order, then short IDs in sorted order.

If `scope.session` or `scope.window` matches nothing or several things, `completions` is empty. The call doesn't fail.

Detached blocks are included unless `scope.window` is set.

To complete a client, set `kinds` to `["client"]`. Clients complete by label and short ID, and each target's `where` names the program, such as `Rex.app 1.6.0`.

### `target.resolve`

Look up sessions, windows, blocks, or clients by ID, label, or position. Each query gets its own result, which says whether it matched one thing, nothing, or several.

| Field | Required | Description |
| --- | --- | --- |
| `kinds` | Yes | What each query may name: session, window, block, or client. List each kind once, and list client only on its own. |
| `queries` | Yes | The names to look up. Each is a full ID, a label, a window position, the end of an ID, or an empty string for the default. When kinds includes session but not block, the full ID of a block names the session that holds it. |
| `context` |  | Where the caller is, such as the terminal a script runs in. IDs in it that no longer exist are ignored. |
| `scope` |  | Limits the search to one session, or a block search to one window. Not allowed when kinds includes session. |

List at least one kind in `kinds`, each only once, and `client` only on its own, or the call fails with `bad_request`. A kind the server doesn't know fails the same way, which can happen when the server is older than your client.

Send at least one query, or the call fails with `bad_request`. Each query gets one entry in `results`, in the same order. A query that matches nothing or several things doesn't fail the call: its `status` is `not_found` or `ambiguous`.

The server tries each query in four steps and stops at the first step that matches anything: full ID, label (ignoring case), window position, then the end of an ID (4 to 32 hexadecimal digits). So a window labeled `2` wins over the second window. If the winning step matches more than one thing, the result is `ambiguous`.

A query that starts like a full ID, such as `block:`, is only tried as a full ID. Its result is `not_found` if the ID is malformed, if `kinds` doesn't include that kind, or if nothing has that ID.

There's one exception. When `kinds` includes `session` but not `block`, the full ID of a block, such as `$REX_BLOCK`, names the session that holds the block. Every session is searched, even if the context names a different one. `scope.session` accepts a block ID the same way. If no open block has the ID, the result is `not_found`. A block that is closing doesn't count. Only a full block ID works this way. A block's label or the end of its ID never names a session.

Only windows have positions. `1` is the first window in its session, in the order Rex.app shows them as tabs. When several sessions are searched, a position can match a window in each one.

When `kinds` lists more than one kind, one query can match different kinds of things, such as a session and a window with the same label. The result is then `ambiguous`, and each candidate's `kind` says what it is.

Without `scope.session`, windows and blocks are searched only in the caller's session. That's the session that holds `context.block_id`, if the block is open, or else the session named by `context.session_id`. The block comes first because it stays with its window when the window moves to another session, while a saved session ID keeps naming the old one. If neither applies, every session is searched. This applies to full IDs too, so a window or block query for the full ID of a block in another session is `not_found`.

If a scope matches nothing or several things, every result gets that `not_found` or `ambiguous` status, and its `reason` says which scope failed. For an ambiguous scope, `candidates` lists what the scope could mean.

An empty query, or one of only spaces, asks for a default, such as the block a script runs in. When `kinds` lists several kinds, an empty query gets the default for the most specific one: block, then window, then session.

An empty session query selects the caller's session, or the only session if there's just one. With no sessions it's `not_found`, and with several it's `ambiguous`.

An empty window query selects the window that holds `context.block_id`. If that block isn't set or is detached, it selects the active window of the session being searched. If several sessions are searched, because neither `scope.session` nor the context names one, it's `ambiguous`, and `candidates` lists the sessions to choose from.

An empty block query selects `context.block_id` if that block is among those searched. Otherwise it selects the focused block of the window an empty window query would choose. With `scope.window`, it ignores `context.block_id` and selects that window's focused block.

Block searches include detached blocks, which are running but aren't placed in any window. `scope.window` leaves them out. A block's `where` reads `window 2` or `detached`. When several sessions are searched, it names the session too, as in `window 2 of work`, and a window's `where` reads `in work`.

To look up a connected client, such as Rex.app, set `kinds` to `["client"]`. A client query matches a full ID, a label, or the end of an ID, since clients have no positions. Every connected client is searched, unless `scope.session` limits the search to clients attached to that session.

An empty client query selects `context.client_id` if that client is among those searched. Otherwise it selects the only client that reported its kind as `app` when it connected, such as Rex.app. With no app it's `not_found`, and with several it's `ambiguous`.

`scope.window` is looked up among the sessions being searched. The call fails with `bad_request` if `kinds` includes `session` and `scope` is sent, even as an empty object, or if `scope.window` is set and `kinds` isn't just `block`. A query or scope that contains a control character, such as a newline, fails the same way.

